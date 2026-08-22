#!/usr/bin/env python3
"""Build the public ChatGPT/Codex Skills-only plugin archive deterministically.

Repository source keeps the OpenAI-specific Skills under ``openai-skills/`` so the
multi-host source tree can coexist with the canonical Claude runtime under
``skills/``. The public archive intentionally remaps ``openai-skills/`` to the
OpenAI-documented ``skills/`` install layout and rewrites the packaged manifest to
point at ``./skills/``.

The archive is allowlist-driven. Repository demos, demo/template media,
Claude/Antigravity worker internals, tests, CI files, caches, and transient local
artifacts never enter the public ChatGPT/Codex ZIP.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

DIRECTORY_MAP = (
    (Path(".codex-plugin"), PurePosixPath(".codex-plugin")),
    (Path("openai-skills"), PurePosixPath("skills")),
    (Path("assets/brand-icons"), PurePosixPath("assets/brand-icons")),
)

ALLOWED_FILES = (
    Path("README.md"),
    Path("LICENSE"),
    Path("PRIVACY.md"),
    Path("TERMS.md"),
    Path("SUPPORT.md"),
    Path("assets/logo-light.svg"),
    Path("assets/logo-dark.svg"),
    Path("assets/plugin-icon.svg"),
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
PACKAGED_SKILLS_ROOT = "skills"


def _is_forbidden(relative: Path) -> bool:
    if any(part in FORBIDDEN_PARTS for part in relative.parts):
        return True
    return relative.suffix.lower() in FORBIDDEN_SUFFIXES


def collect_members(root: Path) -> list[tuple[Path, PurePosixPath]]:
    members: list[tuple[Path, PurePosixPath]] = []

    for source_relative, archive_root in DIRECTORY_MAP:
        source_root = root / source_relative
        if not source_root.is_dir():
            raise FileNotFoundError(f"required package directory missing: {source_relative}")
        for path in source_root.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"symlinks are not allowed in plugin ZIP: {path.relative_to(root)}")
            if not path.is_file():
                continue
            relative_to_source = path.relative_to(source_root)
            source_relative_path = path.relative_to(root)
            if _is_forbidden(source_relative_path):
                continue
            archive_path = archive_root.joinpath(*relative_to_source.parts)
            members.append((source_relative_path, archive_path))

    for relative in ALLOWED_FILES:
        source = root / relative
        if not source.is_file():
            raise FileNotFoundError(f"required package file missing: {relative}")
        if source.is_symlink():
            raise ValueError(f"symlinks are not allowed in plugin ZIP: {relative}")
        members.append((relative, PurePosixPath(relative.as_posix())))

    deduped: dict[str, tuple[Path, PurePosixPath]] = {}
    for source_relative, archive_path in members:
        key = archive_path.as_posix()
        if key in deduped:
            raise ValueError(f"archive path collision: {key}")
        deduped[key] = (source_relative, archive_path)

    ordered = [deduped[key] for key in sorted(deduped)]
    _validate_archive_shape(ordered)
    return ordered


def _validate_archive_shape(members: list[tuple[Path, PurePosixPath]]) -> None:
    names = [archive_path.as_posix() for _, archive_path in members]

    if ".codex-plugin/plugin.json" not in names:
        raise ValueError(".codex-plugin/plugin.json must be present at archive root")

    if any(name.startswith("openai-skills/") for name in names):
        raise ValueError("public archive must remap openai-skills/ to skills/")

    if any(name == "demos" or name.startswith("demos/") for name in names):
        raise ValueError("demos/ must never be included in the Codex release ZIP")

    if any(name.startswith(".codex-plugin/") and name != ".codex-plugin/plugin.json" for name in names):
        raise ValueError("only plugin.json may be present inside .codex-plugin/")

    skill_files = [name for name in names if name.startswith(f"{PACKAGED_SKILLS_ROOT}/")]
    if not skill_files:
        raise ValueError("public archive must contain skills/<skill>/SKILL.md entries")

    direct_files = [name for name in skill_files if name.count("/") == 1]
    if direct_files:
        raise ValueError(f"loose files are not allowed directly under skills/: {direct_files}")

    skill_dirs = sorted({name.split("/", 2)[1] for name in skill_files})
    for slug in skill_dirs:
        expected = f"skills/{slug}/SKILL.md"
        if expected not in names:
            raise ValueError(f"packaged Skill is missing required SKILL.md: {slug}")

    for asset in (
        "assets/logo-light.svg",
        "assets/logo-dark.svg",
        "assets/plugin-icon.svg",
    ):
        if asset not in names:
            raise ValueError(f"required public brand asset missing: {asset}")

    forbidden_public_assets = [
        name
        for name in names
        if name.startswith("assets/")
        and (
            name.lower().endswith((".html", ".gif", ".webp", ".jpg", ".jpeg", ".png"))
            and name not in {"assets/plugin-icon.png"}
        )
    ]
    if forbidden_public_assets:
        raise ValueError(
            "demo/template media must not enter the public Skills-only package: "
            + ", ".join(forbidden_public_assets)
        )


def _packaged_bytes(root: Path, source_relative: Path, archive_path: PurePosixPath) -> bytes:
    source = root / source_relative
    if archive_path.as_posix() != ".codex-plugin/plugin.json":
        return source.read_bytes()

    manifest = json.loads(source.read_text(encoding="utf-8"))
    manifest["skills"] = "./skills/"
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        raise ValueError("plugin manifest interface must be an object")

    if len(str(interface.get("displayName", ""))) > 30:
        raise ValueError("interface.displayName must be at most 30 characters")
    if len(str(interface.get("shortDescription", ""))) > 30:
        raise ValueError("interface.shortDescription must be at most 30 characters")

    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        raise ValueError("interface.defaultPrompt must contain one to three prompts")
    if any(not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 128 for prompt in prompts):
        raise ValueError("each default prompt must be non-empty and at most 128 characters")

    for field in ("logo", "composerIcon"):
        value = interface.get(field)
        if not isinstance(value, str) or not value.startswith("./assets/"):
            raise ValueError(f"interface.{field} must be a package-relative ./assets/ path")

    return (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def build_archive(root: Path, output: Path) -> dict[str, object]:
    members = collect_members(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source_relative, archive_path in members:
            data = _packaged_bytes(root, source_relative, archive_path)
            info = zipfile.ZipInfo(archive_path.as_posix(), FIXED_DATE)
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
        "skills_root": "skills",
        "source_skills_root": "openai-skills",
        "excluded": [
            "demos/**",
            "tests/**",
            ".github/**",
            "agents/**",
            "canonical skills/**",
            "helper/**",
            "research/**",
            "demo/template assets",
        ],
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
