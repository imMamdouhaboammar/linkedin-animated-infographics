#!/usr/bin/env python3
"""Prepare and validate a public community demo contribution package."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

PUBLIC_FILES = {"demo.gif", "index.html", "demo.json"}
REQUIRED_METADATA = {
    "id",
    "title",
    "author",
    "author_url",
    "description",
    "created_with",
    "language",
    "story_type",
    "tags",
    "created_at",
    "license",
    "rights_confirmed",
}
OPTIONAL_PUBLIC_METADATA = {"source_prompt", "repo_url", "notes"}

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("GitHub token", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("API key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("bearer credential", re.compile(r"Authorization\s*:\s*Bearer\s+[^\s<>'\"]+", re.IGNORECASE)),
    ("AWS signed URL", re.compile(r"[?&]X-Amz-Signature=", re.IGNORECASE)),
    ("Google signed URL", re.compile(r"[?&]X-Goog-Signature=", re.IGNORECASE)),
    ("local file URL", re.compile(r"file:///", re.IGNORECASE)),
    ("macOS local absolute path", re.compile(r"/Users/[^/\s]+/")),
    ("Linux local absolute path", re.compile(r"/home/[^/\s]+/")),
    ("Windows local absolute path", re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\", re.IGNORECASE)),
)
REMOTE_EXECUTABLE = re.compile(
    r"<script\b[^>]*\bsrc\s*=\s*['\"](?:https?:)?//[^'\"]+['\"][^>]*>",
    re.IGNORECASE,
)


def scan_public_text(label: str, text: str) -> list[str]:
    """Return named findings that make text unsafe for automatic public export."""
    findings: list[str] = []
    for name, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(f"{label}: {name} detected")
    if REMOTE_EXECUTABLE.search(text):
        findings.append(f"{label}: remote executable resource requires maintainer review")
    return findings


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing required file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from None
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def require_verification_pass(build_dir: Path) -> None:
    report = _read_json(build_dir / "verification-report.json")
    verdict = str(report.get("verdict", report.get("status", ""))).strip().upper()
    if verdict != "PASS":
        raise ValueError("community publishing requires final verification PASS")


def _resolve_build_file(build_dir: Path, relative: str, expected_suffix: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute():
        raise ValueError("public build artifact path must be relative to build directory")
    candidate = (build_dir / rel).resolve()
    try:
        candidate.relative_to(build_dir.resolve())
    except ValueError:
        raise ValueError("public build artifact path may not escape build directory") from None
    if candidate.suffix.lower() != expected_suffix:
        raise ValueError(f"public build artifact must be {expected_suffix}")
    if not candidate.is_file() or candidate.stat().st_size == 0:
        raise ValueError(f"missing non-empty public build artifact: {relative}")
    return candidate


def _validate_slug(value: Any) -> str:
    slug = str(value or "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("slug must be lowercase and filesystem-safe")
    return slug


def _validate_author(value: Any) -> str:
    author = str(value or "")
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", author):
        raise ValueError("author must be a valid GitHub username")
    return author


def _require_matching_author_url(author: str, value: Any) -> str:
    author_url = str(value or "")
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9-]+)/?", author_url)
    if not match:
        raise ValueError("author_url must be an https://github.com/<user> URL")
    if match.group(1).casefold() != author.casefold():
        raise ValueError("author_url must match author")
    return author_url


def _public_manifest(metadata: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(field for field in REQUIRED_METADATA if field not in metadata)
    if missing:
        raise ValueError("missing publication metadata: " + ", ".join(missing))
    if metadata.get("rights_confirmed") is not True:
        raise ValueError("explicit rights confirmation is required before community publishing")

    author = _validate_author(metadata.get("author"))
    _require_matching_author_url(author, metadata.get("author_url"))

    manifest = {"schema_version": 1}
    for field in REQUIRED_METADATA:
        manifest[field] = metadata[field]
    for field in ("repo_url", "notes"):
        if field in metadata and metadata[field] not in (None, ""):
            manifest[field] = metadata[field]
    if metadata.get("publish_source_prompt") is True:
        prompt = metadata.get("source_prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("source prompt consent was enabled but no source_prompt was supplied")
        manifest["source_prompt"] = prompt
    manifest["gif"] = "demo.gif"
    manifest["html"] = "index.html"
    return manifest


def _scan_manifest(manifest: dict[str, Any]) -> list[str]:
    return scan_public_text("demo.json", json.dumps(manifest, ensure_ascii=False, sort_keys=True))


def check_submission(demo_dir: Path, repo_root: Path | None = None) -> list[str]:
    """Validate a staged three-file package before any GitHub operation."""
    errors: list[str] = []
    if not demo_dir.is_dir():
        return [f"submission directory does not exist: {demo_dir}"]
    entries = {entry.name for entry in demo_dir.iterdir()}
    if entries != PUBLIC_FILES:
        errors.append("submission must contain exactly demo.gif, index.html, demo.json")
    try:
        manifest = _read_json(demo_dir / "demo.json")
    except ValueError as exc:
        return errors + [str(exc)]
    if manifest.get("rights_confirmed") is not True:
        errors.append("rights_confirmed must be true")
    if manifest.get("gif") != "demo.gif" or manifest.get("html") != "index.html":
        errors.append("submission paths must be demo.gif and index.html")
    allowed = {"schema_version", *REQUIRED_METADATA, *OPTIONAL_PUBLIC_METADATA, "gif", "html"}
    for field in sorted(set(manifest) - allowed):
        errors.append(f"unknown public metadata field: {field}")
    for field in REQUIRED_METADATA:
        if field not in manifest:
            errors.append(f"missing required public metadata field: {field}")
    author = manifest.get("author")
    if isinstance(author, str):
        try:
            _require_matching_author_url(author, manifest.get("author_url"))
        except ValueError as exc:
            errors.append(str(exc))
    for filename in ("demo.gif", "index.html"):
        path = demo_dir / filename
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"{filename} must exist and be non-empty")
    html_path = demo_dir / "index.html"
    if html_path.is_file():
        errors.extend(scan_public_text("index.html", html_path.read_text(encoding="utf-8", errors="replace")))
    errors.extend(_scan_manifest(manifest))
    return errors


def prepare_submission(build_dir: Path, stage_root: Path, metadata: dict[str, Any]) -> Path:
    """Create a validated community/<author>/<slug> package from verified build output."""
    build_dir = build_dir.resolve()
    stage_root = stage_root.resolve()
    require_verification_pass(build_dir)

    if metadata.get("rights_confirmed") is not True:
        raise ValueError("explicit rights confirmation is required before community publishing")
    slug = _validate_slug(metadata.get("slug"))
    author = _validate_author(metadata.get("author"))
    _require_matching_author_url(author, metadata.get("author_url"))

    html_source = _resolve_build_file(build_dir, str(metadata.get("html_path", "post.html")), ".html")
    gif_source = _resolve_build_file(build_dir, str(metadata.get("gif_path", "post.gif")), ".gif")

    html_text = html_source.read_text(encoding="utf-8", errors="replace")
    manifest = _public_manifest(metadata)
    findings = scan_public_text("index.html", html_text) + _scan_manifest(manifest)
    if findings:
        detail = "; ".join(findings)
        if any("remote executable resource" in item for item in findings):
            raise ValueError(f"remote executable resource requires maintainer review: {detail}")
        raise ValueError(f"public export scan failed: {detail}")

    destination = stage_root / "community" / author / slug
    if destination.exists():
        raise ValueError(f"submission destination already exists: {destination}")
    destination.mkdir(parents=True, exist_ok=False)

    try:
        shutil.copyfile(gif_source, destination / "demo.gif")
        (destination / "index.html").write_text(html_text, encoding="utf-8")
        (destination / "demo.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        errors = check_submission(destination)
        if errors:
            raise ValueError("submission preflight failed: " + "; ".join(errors))
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        raise

    return destination


def _metadata_from_args(args: argparse.Namespace) -> dict[str, Any]:
    metadata_path = Path(args.metadata)
    data = _read_json(metadata_path)
    data["author"] = args.author
    data["slug"] = args.slug
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare")
    prepare.add_argument("--build-dir", default="build")
    prepare.add_argument("--stage-root", default="build/community-submission")
    prepare.add_argument("--author", required=True)
    prepare.add_argument("--slug", required=True)
    prepare.add_argument("--metadata", required=True, help="JSON file containing explicit publication metadata")

    check = sub.add_parser("check")
    check.add_argument("demo_dir")

    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            output = prepare_submission(
                Path(args.build_dir),
                Path(args.stage_root),
                _metadata_from_args(args),
            )
            print(output)
            return 0
        errors = check_submission(Path(args.demo_dir))
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("Demo submission: OK")
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
