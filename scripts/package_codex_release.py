#!/usr/bin/env python3
"""Build the public ChatGPT/Codex Skills-only plugin archive deterministically.

The package is allowlist-driven on purpose. Repository demos, demo media, canonical
Claude/Antigravity worker internals, tests, CI files, caches, and local artifacts do
not enter the public Codex ZIP.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DIRS = (Path(".codex-plugin"), Path("openai-skills"), Path("assets"))
ALLOWED_FILES = (
    Path("README.md"),
    Path("LICENSE"),
    Path("PRIVACY.md"),
    Path("TERMS.md"),
    Path("SUPPORT.md"),
)
FORBIDDEN_PARTS = {
    "demos",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".DS_Store",
}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}
FIXED_DATE = (1980, 1, 1, 0, 0, 0)


def _is_forbidden(relative: Path) -> bool:
    if any(part in FORBIDDEN_PARTS for part in relative.parts):
        return True
    return relative.suffix.lower() in FORBIDDEN_SUFFIXES


def collect_members(root: Path) -> list[Path]:
    members: list[Path] = []
    for directory in ALLOWED_DIRS:
        source = root / directory
        if not source.is_dir():
            raise FileNotFoundError(f"required package directory missing: {directory}")
        for path in source.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"symlinks are not allowed in plugin ZIP: {path.relative_to(root)}")
            if not path.is_file():
                continue
            relative = path.relative_to(root)
            if _is_forbidden(relative):
                continue
            members.append(relative)

    for relative in ALLOWED_FILES:
        source = root / relative
        if not source.is_file():
            raise FileNotFoundError(f"required package file missing: {relative}")
        if source.is_symlink():
            raise ValueError(f"symlinks are not allowed in plugin ZIP: {relative}")
        members.append(relative)

    members = sorted(set(members), key=lambda value: value.as_posix())
    names = [member.as_posix() for member in members]
    if ".codex-plugin/plugin.json" not in names:
        raise ValueError(".codex-plugin/plugin.json must be present at archive root")
    if any(name == "demos" or name.startswith("demos/") for name in names):
        raise ValueError("demos/ must never be included in the Codex release ZIP")
    if any(name.startswith(".codex-plugin/") and name != ".codex-plugin/plugin.json" for name in names):
        raise ValueError("only plugin.json may be present inside .codex-plugin/")
    return members


def build_archive(root: Path, output: Path) -> dict[str, object]:
    members = collect_members(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in members:
            source = root / relative
            data = source.read_bytes()
            info = zipfile.ZipInfo(PurePosixPath(relative).as_posix(), FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.create_system = 3
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return {
        "path": str(output),
        "sha256": digest,
        "members": len(members),
        "bytes": output.stat().st_size,
        "excluded": ["demos/**", "tests/**", ".github/**", "agents/**", "skills/**", "helper/**", "research/**"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="dist/linkedin-animated-infographics-codex-plugin-v3.7.0.zip")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_archive(Path(args.root).resolve(), Path(args.output).resolve())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Built {result['path']}")
        print(f"SHA256 {result['sha256']}")
        print(f"Members {result['members']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
