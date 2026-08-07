#!/usr/bin/env python3
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "skills" / "info-stories" / "catalog.json"
AXIS_ALIASES = {"house": "houses", "style": "styles", "archetype": "archetypes", "motion": "motions"}
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_catalog(path=DEFAULT_CATALOG):
    return json.loads(Path(path).read_text())


def _linear(channel):
    channel /= 255.0
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def _luminance(hex_color):
    if not HEX_RE.match(hex_color):
        raise ValueError(f"Expected #RRGGBB, got {hex_color!r}")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def contrast_ratio(foreground, background):
    a, b = _luminance(foreground), _luminance(background)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def validate_catalog(catalog):
    errors = []
    for axis in ("houses", "styles", "archetypes", "motions"):
        items = catalog.get(axis)
        if not isinstance(items, list):
            errors.append(f"{axis}: expected list")
            continue
        slugs, names = set(), set()
        for item in items:
            slug, name = item.get("slug"), item.get("name")
            if not slug or not SLUG_RE.match(slug):
                errors.append(f"{axis}: invalid slug {slug!r}")
            if slug in slugs:
                errors.append(f"{axis}: duplicate slug {slug}")
            if name in names:
                errors.append(f"{axis}: duplicate name {name}")
            slugs.add(slug); names.add(name)
    required_dials = {"design_variance", "motion_intensity", "visual_density"}
    for style in catalog.get("styles", []):
        dials = style.get("dials", {})
        if set(dials) != required_dials:
            errors.append(f"{style.get('slug')}: expected design dials {sorted(required_dials)}")
        else:
            for name, value in dials.items():
                if not isinstance(value, int) or not 1 <= value <= 10:
                    errors.append(f"{style.get('slug')}: {name} must be integer 1-10")
    required = {"bg", "surface", "ink", "ink_2", "muted", "line", "accent", "accent_deep"}
    for house in catalog.get("houses", []):
        tokens = house.get("tokens", {})
        missing = sorted(required - set(tokens))
        if missing:
            errors.append(f"{house.get('slug')}: missing tokens {', '.join(missing)}")
            continue
        for fg, bg in house.get("text_pairs", []):
            try:
                ratio = contrast_ratio(tokens[fg], tokens[bg])
            except (KeyError, ValueError) as exc:
                errors.append(f"{house['slug']}: invalid text pair {fg}/{bg}: {exc}")
                continue
            if ratio < 4.5:
                errors.append(f"{house['slug']}: text {fg}/{bg} contrast {ratio:.2f} < 4.5")
        for fg, bg in house.get("state_pairs", []):
            try:
                ratio = contrast_ratio(tokens[fg], tokens[bg])
            except (KeyError, ValueError) as exc:
                errors.append(f"{house['slug']}: invalid state pair {fg}/{bg}: {exc}")
                continue
            if ratio < 3.0:
                errors.append(f"{house['slug']}: state {fg}/{bg} contrast {ratio:.2f} < 3.0")
    return errors


def _items_for(catalog, singular):
    axis = AXIS_ALIASES.get(singular, singular)
    if axis not in catalog:
        raise KeyError(singular)
    return catalog[axis]


def _find(catalog, singular, slug):
    items = _items_for(catalog, singular)
    for item in items:
        if item["slug"] == slug:
            return item
    slugs = [item["slug"] for item in items]
    choices = ", ".join(slugs)
    match = difflib.get_close_matches(slug, slugs, n=1, cutoff=0.6)
    hint = f" Did you mean {match[0]!r}?" if match else ""
    raise ValueError(f"Unknown {singular} {slug!r}.{hint} Valid choices: {choices}")


COPY_SLOP_PATTERNS = [
    ("throat-clearing", re.compile(r"\b(here(?:'|’)s the thing|let(?:'|’)s be clear|the truth is|it(?:'|’)s important to note)\b", re.I)),
    ("binary-contrast", re.compile(r"\bnot\s+(?:just\s+|only\s+)?[^.!?]{1,120}?,\s*(?:but\s+)?it(?:'|’)s\b", re.I)),
    ("faux-insight", re.compile(r"\b(what most people get wrong|the real lesson|the deeper truth|here(?:'|’)s what nobody tells you)\b", re.I)),
    ("importance-puffery", re.compile(r"\b(revolution(?:ary)?|game[- ]changing|groundbreaking|changes everything|transformative)\b", re.I)),
    ("recap-ending", re.compile(r"\b(in conclusion|to sum up|in summary)\b", re.I)),
    ("rhetorical-setup", re.compile(r"(?:^|[.!?]\s+)(?:so,?\s+)?(?:what if|why does this matter|ready to|the question is)\b", re.I)),
    ("dash-crutch", re.compile(r"[—–]")),
]

FINGERPRINT_AXES = (
    "zone_topology",
    "card_grammar",
    "divider",
    "visual_anchor",
    "density",
    "motion_grammar",
)


def detect_copy_slop(text):
    findings = []
    for name, pattern in COPY_SLOP_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append({"pattern": name, "evidence": match.group(0)})
    return findings


def validate_fingerprint(current, previous=None, min_changes=2):
    missing = [axis for axis in FINGERPRINT_AXES if not current.get(axis)]
    if missing:
        return [f"Structural fingerprint is missing: {', '.join(missing)}"]
    if not previous:
        return []
    changed = sum(current.get(axis) != previous.get(axis) for axis in FINGERPRINT_AXES)
    if changed < min_changes:
        return [
            f"Structural fingerprint changes only {changed}/{len(FINGERPRINT_AXES)} axes; "
            f"change at least {min_changes}. A palette-only reskin is not a new visual style."
        ]
    return []


STUDY_REQUIRED_FIELDS = (
    "source", "source_kind", "provenance", "surface", "type_roles", "structure",
    "rhythm", "motion", "visual_anchor", "recommendations", "copy_boundaries",
)


def validate_study_report(report):
    errors = []
    for field in STUDY_REQUIRED_FIELDS:
        if field not in report or report[field] in (None, "", [], {}):
            errors.append(f"Study report missing {field}")
    if report.get("source_kind") not in {"image", "gif", "url", "user-work", None}:
        errors.append("Study report source_kind must be image, gif, url, or user-work")
    recs = report.get("recommendations", {})
    for axis in ("house", "style", "archetype", "motion"):
        if isinstance(recs, dict) and axis not in recs:
            errors.append(f"Study recommendations missing {axis}")
    return errors


VERIFIER_VERDICTS = {"PASS", "FAIL:fixable", "FAIL:escalate"}
VERIFIER_STATUSES = {"PASS", "FAIL", "NA"}


def validate_verification_report(report):
    errors = []
    verdict = report.get("verdict")
    if verdict not in VERIFIER_VERDICTS:
        errors.append(f"Unknown verifier verdict: {verdict!r}")
    attempt = report.get("attempt")
    if not isinstance(attempt, int) or attempt < 0:
        errors.append("Verifier attempt must be a non-negative integer")
    elif attempt > 2:
        errors.append("Verification allows at most two targeted fix attempts")
    criteria = report.get("criteria")
    if not isinstance(criteria, list):
        errors.append("Verifier criteria must be a list")
        return errors
    if verdict == "PASS" and not criteria:
        errors.append("PASS requires at least one acceptance criterion with evidence")
    seen = set()
    for index, row in enumerate(criteria):
        if not isinstance(row, dict):
            errors.append(f"Criterion {index} must be an object")
            continue
        criterion_id = row.get("id")
        if not criterion_id:
            errors.append(f"Criterion {index} missing id")
        elif criterion_id in seen:
            errors.append(f"Duplicate criterion id {criterion_id}")
        seen.add(criterion_id)
        if row.get("status") not in VERIFIER_STATUSES:
            errors.append(f"Criterion {criterion_id or index} has invalid status")
        for field in ("artifact", "observation", "evidence"):
            if not row.get(field):
                errors.append(f"Criterion {criterion_id or index} missing {field}")
    return errors


def check_composition(catalog, style, archetype, motions):
    style_item = _find(catalog, "style", style)
    archetype_item = _find(catalog, "archetype", archetype)
    errors = []
    if archetype not in style_item.get("archetypes", []):
        errors.append(f"{style} is not compatible with {archetype}")
    if len(motions) > 2:
        errors.append("Use at most two motion patterns")
    structures = set(style_item.get("structures", []))
    primary_count = 0
    for motion_slug in motions:
        motion = _find(catalog, "motion", motion_slug)
        if not structures.intersection(motion.get("structures", [])):
            errors.append(f"{motion_slug} is not compatible with {style}")
        roles = motion.get("roles", [])
        if roles == ["primary"]:
            primary_count += 1
    if primary_count > 1:
        errors.append("Use at most one primary-only motion pattern")
    return errors


def build_brief(catalog, *, topic, takeaway, cta, house, style, archetype, motions, language="en", output_mode="gif"):
    house_item = _find(catalog, "house", house)
    style_item = _find(catalog, "style", style)
    archetype_item = _find(catalog, "archetype", archetype)
    for motion_slug in motions:
        _find(catalog, "motion", motion_slug)
    if output_mode not in {"gif", "static"}:
        raise ValueError("output_mode must be 'gif' or 'static'")
    if output_mode == "static" and motions:
        raise ValueError("static output must not declare motion patterns")
    errors = check_composition(catalog, style, archetype, motions)
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "schema_version": 1,
        "topic": topic,
        "takeaway": takeaway,
        "cta": cta,
        "language": language,
        "output_mode": output_mode,
        "selection": {
            "house": house,
            "style": style,
            "archetype": archetype,
            "motions": list(motions),
        },
        "content_contract": {
            "required_beats": list(archetype_item["required_beats"]),
            "density_range": list(archetype_item["density_range"]),
        },
        "execution": {
            "artboard_archetype": style_item["preferred_artboard"],
            "structures": list(style_item["structures"]),
            "design_dials": dict(style_item["dials"]),
            "house_tokens": dict(house_item["tokens"]),
            "motion_limit": 2,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect and validate Info-stories registries")
    sub = parser.add_subparsers(dest="command", required=True)
    lp = sub.add_parser("list")
    lp.add_argument("axis", choices=tuple(AXIS_ALIASES))
    sp = sub.add_parser("show")
    sp.add_argument("axis", choices=tuple(AXIS_ALIASES))
    sp.add_argument("slug")
    sub.add_parser("check")
    cp = sub.add_parser("compose")
    cp.add_argument("--style", required=True)
    cp.add_argument("--archetype", required=True)
    cp.add_argument("--motion", action="append", default=[])
    bp = sub.add_parser("scaffold")
    bp.add_argument("--topic", required=True)
    bp.add_argument("--takeaway", required=True)
    bp.add_argument("--cta", required=True)
    bp.add_argument("--house", required=True)
    bp.add_argument("--style", required=True)
    bp.add_argument("--archetype", required=True)
    bp.add_argument("--motion", action="append", default=[])
    bp.add_argument("--language", default="en")
    bp.add_argument("--output-mode", choices=("gif", "static"), default="gif")
    args = parser.parse_args(argv)
    catalog = load_catalog()
    try:
        if args.command == "list":
            for item in _items_for(catalog, args.axis):
                print(f"{item['slug']}\t{item['name']}")
            return 0
        if args.command == "show":
            print(json.dumps(_find(catalog, args.axis, args.slug), indent=2, sort_keys=True))
            return 0
        if args.command == "compose":
            errors = check_composition(catalog, args.style, args.archetype, args.motion)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print("Composition: OK")
            return 0
        if args.command == "scaffold":
            brief = build_brief(
                catalog, topic=args.topic, takeaway=args.takeaway, cta=args.cta,
                house=args.house, style=args.style, archetype=args.archetype,
                motions=args.motion, language=args.language, output_mode=args.output_mode,
            )
            print(json.dumps(brief, indent=2, sort_keys=True))
            return 0
        errors = validate_catalog(catalog)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("Info-stories catalog: OK")
        return 0
    except (KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
