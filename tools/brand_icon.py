#!/usr/bin/env python3
"""Resolve official AI and LLM brand marks from a pinned upstream icon set.

The repository rule for a named or official mark is that the exact SVG is
mandatory and a lookalike is never acceptable. Until now the only answer to a
missing mark was `HOLD: exact SVG required`. This tool is the supply route for
that gate: it fetches the vendor's own artwork from a pinned release of
`@lobehub/icons-static-svg`, sanitises it, and records provenance so the asset
can be audited later.

It never draws, approximates or substitutes. An unknown slug fails with the
nearest real choices, and a slug the upstream set does not carry fails as a
documented gap.

    python3 tools/brand_icon.py list --query claude
    python3 tools/brand_icon.py fetch claude --variant color
    python3 tools/brand_icon.py check
"""
import argparse
import difflib
import hashlib
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "assets" / "brand-icons"
MANIFEST = CACHE / "manifest.json"
PROVENANCE = CACHE / "provenance.json"

MAX_BYTES = 256 * 1024
SVG_NS = "http://www.w3.org/2000/svg"

# Anything that can reach the network, execute, or embed a remote document at
# render time. A fetched artboard asset must be inert.
FORBIDDEN_TAGS = {"script", "foreignobject", "iframe", "audio", "video", "animate"}
REMOTE_SCHEME = re.compile(r"^\s*(?:https?:|//|javascript:|data:text/html)", re.I)

VARIANT_SUFFIX = {"mono": "", "color": "-color", "text": "-text", "brand": "-brand-color"}


def load_manifest(path=MANIFEST):
    return json.loads(Path(path).read_text())


def resolve_name(manifest, slug, variant="color"):
    """Map a slug plus variant to a real file name in the pinned set.

    Falls back from a colour variant to the monochrome mark when the vendor
    only ships one, which is a real property of the upstream set rather than a
    substitution: it is still that vendor's own artwork.
    """
    icons = set(manifest["icons"])
    if variant not in VARIANT_SUFFIX:
        raise ValueError(f"Unknown variant {variant!r}. Valid choices: {', '.join(sorted(VARIANT_SUFFIX))}")
    slug = slug.strip().lower()
    candidates = [slug + VARIANT_SUFFIX[variant]]
    if variant in {"color", "brand"}:
        candidates += [slug + "-color", slug]
    elif variant == "text":
        candidates += [slug]
    for name in candidates:
        if name in icons:
            return name
    near = difflib.get_close_matches(slug, sorted({i.split("-")[0] for i in icons}), n=3, cutoff=0.6)
    hint = f" Closest available: {', '.join(near)}." if near else ""
    raise LookupError(
        f"{slug!r} is not in {manifest['package']}@{manifest['version']}.{hint} "
        f"{manifest['scope_note']} Supply the exact SVG yourself, or keep the literal product name."
    )


def sanitise(data: bytes, name: str) -> str:
    """Reject anything that is not an inert, self-contained SVG document."""
    if len(data) > MAX_BYTES:
        raise ValueError(f"{name}: {len(data)} bytes exceeds the {MAX_BYTES} byte ceiling")
    text = data.decode("utf-8")
    if "<!DOCTYPE" in text or "<!ENTITY" in text:
        raise ValueError(f"{name}: document type or entity declaration is not allowed")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise ValueError(f"{name}: not parseable as XML: {exc}") from exc
    if root.tag not in ("svg", f"{{{SVG_NS}}}svg"):
        raise ValueError(f"{name}: root element is {root.tag}, expected svg")
    for element in root.iter():
        tag = element.tag.split("}")[-1].lower()
        if tag in FORBIDDEN_TAGS:
            raise ValueError(f"{name}: contains a forbidden <{tag}> element")
        for attribute, value in element.attrib.items():
            local = attribute.split("}")[-1].lower()
            if local.startswith("on"):
                raise ValueError(f"{name}: contains an event handler attribute {attribute}")
            if local in {"href", "src"} and REMOTE_SCHEME.match(value or ""):
                raise ValueError(f"{name}: references a remote resource in {attribute}")
            if local == "style" and "url(" in (value or "").lower():
                raise ValueError(f"{name}: style attribute pulls an external url")
    return text


def fetch(slug, variant="color", out=None, manifest_path=MANIFEST, timeout=30):
    manifest = load_manifest(manifest_path)
    name = resolve_name(manifest, slug, variant)
    url = manifest["url_template"].format(version=manifest["version"], name=name)
    request = urllib.request.Request(url, headers={"User-Agent": "linkedin-animated-infographics/brand-icon"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - pinned https host
        data = response.read(MAX_BYTES + 1)
    text = sanitise(data, name)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    target = Path(out) if out else CACHE / f"{name}.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    record = {
        "slug": slug.strip().lower(),
        "variant": variant,
        "file": str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target),
        "resolved_name": name,
        "source_url": url,
        "package": manifest["package"],
        "package_version": manifest["version"],
        "license": manifest["license"],
        "license_scope": manifest["license_scope"],
        "sha256": digest,
        "fetched_on": date.today().isoformat(),
        "trademark": "This mark is the trademark of its owner. Use it to identify that product and nothing else.",
    }
    _record(record)
    return record


def _record(record):
    doc = {"schema_version": 1, "assets": []}
    if PROVENANCE.exists():
        doc = json.loads(PROVENANCE.read_text())
    assets = [a for a in doc.get("assets", []) if a.get("file") != record["file"]]
    assets.append(record)
    doc["assets"] = sorted(assets, key=lambda a: a["file"])
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text(json.dumps(doc, indent=2) + "\n")


def check(manifest_path=MANIFEST):
    """Verify every cached mark still matches its recorded hash and stays inert."""
    errors = []
    manifest = load_manifest(manifest_path)
    for field in ("package", "version", "license", "icons", "url_template"):
        if not manifest.get(field):
            errors.append(f"manifest is missing {field}")
    if not PROVENANCE.exists():
        return errors
    doc = json.loads(PROVENANCE.read_text())
    for asset in doc.get("assets", []):
        path = ROOT / asset["file"]
        if not path.is_file():
            errors.append(f"{asset['file']} is recorded but missing from the cache")
            continue
        text = path.read_text()
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != asset.get("sha256"):
            errors.append(f"{asset['file']} does not match its recorded sha256")
        try:
            sanitise(text.encode("utf-8"), asset["file"])
        except ValueError as exc:
            errors.append(str(exc))
        if asset.get("package_version") != manifest["version"]:
            errors.append(
                f"{asset['file']} came from {asset.get('package_version')} but the manifest pins {manifest['version']}"
            )
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Resolve official brand marks from a pinned upstream set")
    sub = parser.add_subparsers(dest="command", required=True)
    lp = sub.add_parser("list", help="list marks available in the pinned set")
    lp.add_argument("--query", default="")
    lp.add_argument("--limit", type=int, default=40)
    fp = sub.add_parser("fetch", help="download one mark and record its provenance")
    fp.add_argument("slug")
    fp.add_argument("--variant", default="color", choices=sorted(VARIANT_SUFFIX))
    fp.add_argument("--out", default=None)
    sub.add_parser("check", help="verify cached marks against recorded hashes")
    args = parser.parse_args(argv)

    try:
        if args.command == "list":
            manifest = load_manifest()
            names = [n for n in manifest["icons"] if args.query.lower() in n] if args.query else manifest["icons"]
            if not names:
                print(f"No mark matches {args.query!r}. {manifest['scope_note']}", file=sys.stderr)
                return 1
            for name in names[: args.limit]:
                print(name)
            if len(names) > args.limit:
                print(f"... {len(names) - args.limit} more", file=sys.stderr)
            return 0
        if args.command == "fetch":
            record = fetch(args.slug, args.variant, args.out)
            print(json.dumps(record, indent=2))
            return 0
        errors = check()
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("Brand icons: OK")
        return 0
    except (LookupError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Could not reach the pinned icon set: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
