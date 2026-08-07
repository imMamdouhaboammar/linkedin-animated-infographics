#!/usr/bin/env python3
"""Validate and index owned/community demo packages.

The repository is the gallery source of truth. Every demo directory contains
exactly demo.gif, index.html, and demo.json. The generated demos/catalog.json
is deterministic and must not be edited by hand.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {"demo.gif", "index.html", "demo.json"}
DEMO_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GITHUB_AUTHOR = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
LOCAL_PATH_MARKERS = ("file:///", "/Users/", "C:\\Users\\")
REQUIRED_FIELDS = {
    "schema_version",
    "id",
    "title",
    "author",
    "author_url",
    "description",
    "created_with",
    "language",
    "story_type",
    "tags",
    "gif",
    "html",
    "created_at",
    "license",
    "rights_confirmed",
}
OPTIONAL_FIELDS = {"source_prompt", "repo_url", "notes"}
ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS
CATALOG_FIELDS = (
    "id",
    "title",
    "author",
    "author_url",
    "description",
    "created_with",
    "language",
    "story_type",
    "tags",
    "gif",
    "html",
    "created_at",
    "license",
)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing JSON file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from None
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def load_demo(path: Path) -> dict[str, Any]:
    """Load demo metadata from either a demo directory or demo.json path."""
    manifest = path / "demo.json" if path.is_dir() else path
    return _read_json(manifest)


def safe_child(base: Path, relative: str) -> Path | None:
    """Resolve a path only when it stays inside base and is not absolute."""
    candidate_path = Path(relative)
    if candidate_path.is_absolute():
        return None
    candidate = (base / candidate_path).resolve()
    try:
        candidate.relative_to(base.resolve())
    except ValueError:
        return None
    return candidate


def _location(path: Path, root: Path) -> tuple[str | None, str | None, str | None]:
    """Return (kind, author_namespace, slug) for a demo directory."""
    try:
        rel = path.resolve().relative_to((root / "demos").resolve())
    except ValueError:
        return None, None, None
    parts = rel.parts
    if len(parts) == 2 and parts[0] == "owned":
        return "owned", None, parts[1]
    if len(parts) == 3 and parts[0] == "community":
        return "community", parts[1], parts[2]
    return None, None, None


def _validate_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))


def _string_ok(value: Any, *, minimum: int = 1, maximum: int | None = None) -> bool:
    if not isinstance(value, str):
        return False
    length = len(value.strip())
    return length >= minimum and (maximum is None or length <= maximum)


def _scan_metadata_for_local_paths(data: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    for key, value in data.items():
        values = value if isinstance(value, list) else [value]
        for item in values:
            if not isinstance(item, str):
                continue
            if any(marker in item for marker in LOCAL_PATH_MARKERS) or re.search(r"/home/[^/\s]+/", item):
                findings.append(f"demo.json field {key!r} contains a local absolute path")
    return findings


def validate_demo_dir(path: Path, root: Path = ROOT) -> list[str]:
    """Return validation errors for one demo directory."""
    errors: list[str] = []
    kind, author_namespace, slug = _location(path, root)
    if kind is None:
        errors.append("demo directory must be under demos/owned/<slug> or demos/community/<github-user>/<slug>")
        return errors

    entries = {entry.name for entry in path.iterdir()} if path.exists() else set()
    if entries != PUBLIC_FILES:
        errors.append("demo directory must contain exactly demo.gif, index.html, demo.json")

    manifest_path = path / "demo.json"
    try:
        data = load_demo(manifest_path)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    missing = sorted(REQUIRED_FIELDS - data.keys())
    for field in missing:
        errors.append(f"missing required demo.json field: {field}")
    for field in sorted(data.keys() - ALLOWED_FIELDS):
        errors.append(f"unknown demo.json field: {field}")

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    demo_id = data.get("id")
    if not isinstance(demo_id, str) or not DEMO_ID.fullmatch(demo_id):
        errors.append("id must be a stable lowercase filesystem-safe slug")
    if not isinstance(slug, str) or not DEMO_ID.fullmatch(slug):
        errors.append("demo directory slug must be lowercase and filesystem-safe")

    author = data.get("author")
    if not _string_ok(author, maximum=80):
        errors.append("author must be a non-empty string")
    if kind == "community":
        if not author_namespace or not GITHUB_AUTHOR.fullmatch(author_namespace):
            errors.append("community author namespace must be a valid GitHub username")
        if author != author_namespace:
            errors.append("community author namespace must match demo.json author")
    author_url = data.get("author_url")
    if not isinstance(author_url, str) or not re.fullmatch(r"https://github\.com/[A-Za-z0-9-]+/?", author_url):
        errors.append("author_url must be an https://github.com/<user> URL")

    for field, maximum in (("title", 160), ("description", 500), ("created_with", None), ("language", 32), ("story_type", 80), ("license", 80)):
        if not _string_ok(data.get(field), maximum=maximum):
            errors.append(f"{field} must be a non-empty string")

    tags = data.get("tags")
    if not isinstance(tags, list) or not tags or any(not _string_ok(tag, maximum=60) for tag in tags):
        errors.append("tags must be a non-empty list of non-empty strings")
    elif len(set(tags)) != len(tags):
        errors.append("tags must be unique")

    if data.get("gif") != "demo.gif":
        errors.append("gif must be the safe local demo path demo.gif")
    if data.get("html") != "index.html":
        errors.append("html must be the safe local demo path index.html")
    for field in ("gif", "html"):
        value = data.get(field)
        if not isinstance(value, str) or safe_child(path, value) is None:
            errors.append(f"{field} must be a safe local demo path")

    if not _validate_date(data.get("created_at")):
        errors.append("created_at must use YYYY-MM-DD")
    if data.get("rights_confirmed") is not True:
        errors.append("rights_confirmed must be true")

    for optional in OPTIONAL_FIELDS:
        if optional in data and not _string_ok(data[optional], maximum=10000 if optional == "source_prompt" else 2000):
            errors.append(f"{optional} must be a non-empty string when present")
    if "repo_url" in data and not str(data["repo_url"]).startswith("https://"):
        errors.append("repo_url must use https://")

    errors.extend(_scan_metadata_for_local_paths(data))

    for filename in ("demo.gif", "index.html"):
        file_path = path / filename
        if not file_path.is_file() or file_path.stat().st_size == 0:
            errors.append(f"{filename} must exist and be non-empty")

    return errors


def _demo_dirs(root: Path) -> list[Path]:
    result: list[Path] = []
    for namespace in (root / "demos" / "owned", root / "demos" / "community"):
        if not namespace.exists():
            continue
        for manifest in namespace.rglob("demo.json"):
            result.append(manifest.parent)
    return sorted(result, key=lambda p: p.as_posix())


def discover_demos(root: Path = ROOT) -> list[dict[str, Any]]:
    demos: list[dict[str, Any]] = []
    ids: set[str] = set()
    for directory in _demo_dirs(root):
        errors = validate_demo_dir(directory, root)
        if errors:
            joined = "; ".join(errors)
            raise ValueError(f"invalid demo {directory.relative_to(root)}: {joined}")
        data = load_demo(directory)
        demo_id = data["id"]
        if demo_id in ids:
            raise ValueError(f"duplicate demo id: {demo_id}")
        ids.add(demo_id)
        kind, _, _ = _location(directory, root)
        rel_dir = directory.relative_to(root).as_posix()
        entry = {field: data[field] for field in CATALOG_FIELDS}
        entry["kind"] = kind
        entry["path"] = rel_dir
        entry["gif"] = f"{rel_dir}/demo.gif"
        entry["html"] = f"{rel_dir}/index.html"
        demos.append(entry)
    return sorted(demos, key=lambda item: (item["id"], item["path"]))


def build_catalog(root: Path = ROOT) -> dict[str, Any]:
    return {"schema_version": 1, "demos": discover_demos(root)}


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def check_repository(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        expected = build_catalog(root)
    except ValueError as exc:
        return [str(exc)]
    catalog_path = root / "demos" / "catalog.json"
    try:
        tracked = _read_json(catalog_path)
    except ValueError as exc:
        return [str(exc)]
    if _canonical_json(tracked) != _canonical_json(expected):
        errors.append("demo catalog drift: run python3 scripts/demo_gallery.py build")
    return errors


def write_catalog(root: Path = ROOT) -> Path:
    path = root / "demos" / "catalog.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_canonical_json(build_catalog(root)), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "build", "list"))
    args = parser.parse_args(argv)

    if args.command == "check":
        errors = check_repository(ROOT)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("Demo gallery: OK")
        return 0
    if args.command == "build":
        path = write_catalog(ROOT)
        print(path.relative_to(ROOT))
        return 0
    print(_canonical_json(build_catalog(ROOT)), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
