#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ALLOWED_SOURCE_TYPES = {
    "user-official",
    "original-owner",
    "lobe",
    "vibe-svgs-logo",
    "vibe-svgs-community",
}
ALLOWED_RENDER_DISPOSITIONS = {"local", "embedded"}
LOBE_PACKAGE_RE = re.compile(r"^@lobehub/icons-(?:static-svg|static-avatar)@[^@\s:]+$")
HEX40_RE = re.compile(r"^[0-9a-fA-F]{40}$")
HEX64_RE = re.compile(r"^[0-9a-fA-F]{64}$")
VIBE_REPO = "imMamdouhaboammar/vibe-svgs"
VIBE_BLOB_PREFIX = "https://github.com/imMamdouhaboammar/vibe-svgs/blob/"


def _nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_hash(asset, prefix, field, regex, errors):
    value = asset.get(field)
    if not isinstance(value, str) or not regex.fullmatch(value.strip()):
        errors.append(f"{prefix}.{field} must be a pinned hexadecimal digest")


def _validate_vibe_source(asset: dict, prefix: str, errors: list[str]) -> None:
    if asset.get("source_repo") != VIBE_REPO:
        errors.append(f"{prefix}.source_repo must be {VIBE_REPO}")

    _require_hash(asset, prefix, "source_commit", HEX40_RE, errors)
    _require_hash(asset, prefix, "source_blob_sha", HEX40_RE, errors)
    _require_hash(asset, prefix, "integrity_sha256", HEX64_RE, errors)

    source_path = asset.get("source_path")
    if not _nonempty_string(source_path) or not source_path.endswith(".svg"):
        errors.append(f"{prefix}.source_path must be a repository-relative SVG path")

    source_ref = asset.get("source_ref")
    commit = asset.get("source_commit")
    if isinstance(commit, str) and HEX40_RE.fullmatch(commit.strip()):
        expected_prefix = VIBE_BLOB_PREFIX + commit.strip() + "/"
        if not isinstance(source_ref, str) or not source_ref.startswith(expected_prefix):
            errors.append(f"{prefix}.source_ref must be immutable and pinned to source_commit")

    if isinstance(source_path, str) and source_path and isinstance(source_ref, str) and source_path not in source_ref:
        errors.append(f"{prefix}.source_ref must identify the same source_path")


def validate(payload: dict) -> list[str]:
    errors = []
    if not isinstance(payload, dict):
        return ["asset plan must be a JSON object"]
    assets = payload.get("assets")
    if not isinstance(assets, list):
        return ["asset plan must contain an assets array"]

    for index, asset in enumerate(assets):
        prefix = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{prefix} must be an object")
            continue

        for field in ("name", "kind", "source_type", "source_ref", "render_disposition", "status"):
            if not _nonempty_string(asset.get(field)):
                errors.append(f"{prefix}.{field} must be a non-empty string")

        source_type = asset.get("source_type")
        if not isinstance(source_type, str) or source_type not in ALLOWED_SOURCE_TYPES:
            errors.append(
                f"{prefix}.source_type must be one of "
                "user-official, original-owner, lobe, vibe-svgs-logo, vibe-svgs-community"
            )

        if source_type == "lobe":
            if not _nonempty_string(asset.get("lobe_slug")):
                errors.append(f"{prefix}.lobe_slug must be a non-empty string for Lobe assets")

            package = asset.get("package")
            if not isinstance(package, str):
                errors.append(f"{prefix}.package must be a versioned @lobehub/icons static package string")
            elif not LOBE_PACKAGE_RE.fullmatch(package.strip()):
                errors.append(
                    f"{prefix}.package must include an explicit version, "
                    "for example @lobehub/icons-static-svg@1.91.0"
                )

            source_ref = asset.get("source_ref")
            if isinstance(package, str) and LOBE_PACKAGE_RE.fullmatch(package.strip()):
                if not isinstance(source_ref, str) or not source_ref.startswith(package.strip() + ":"):
                    errors.append(
                        f"{prefix}.source_ref must include the same versioned Lobe package "
                        "followed by an immutable asset reference"
                    )

        if source_type == "original-owner":
            if not _nonempty_string(asset.get("source_owner")):
                errors.append(f"{prefix}.source_owner must identify the original identity owner")
            _require_hash(asset, prefix, "integrity_sha256", HEX64_RE, errors)

        if isinstance(source_type, str) and source_type in {"vibe-svgs-logo", "vibe-svgs-community"}:
            _validate_vibe_source(asset, prefix, errors)

        if source_type == "vibe-svgs-logo":
            source_path = asset.get("source_path")
            if isinstance(source_path, str) and not source_path.startswith("svgs/logos/"):
                errors.append(f"{prefix}.source_path must stay under svgs/logos/ for vibe-svgs-logo")
            kind = asset.get("kind")
            if isinstance(kind, str) and "logo" not in kind.lower():
                errors.append(f"{prefix}.kind must identify a logo for vibe-svgs-logo")
            if asset.get("identity_status") != "supplied-third-party-mark":
                errors.append(
                    f"{prefix}.identity_status must be supplied-third-party-mark for vibe-svgs-logo"
                )
            if asset.get("alteration_policy") != "placement-only":
                errors.append(f"{prefix}.alteration_policy must be placement-only for mirrored logos")

        if source_type == "vibe-svgs-community":
            source_path = asset.get("source_path")
            if isinstance(source_path, str) and not (
                source_path.startswith("svgs/mascots/") or source_path.startswith("svgs/scenes/")
            ):
                errors.append(
                    f"{prefix}.source_path must stay under svgs/mascots/ or svgs/scenes/ "
                    "for vibe-svgs-community"
                )
            if asset.get("community_artwork") is not True:
                errors.append(f"{prefix}.community_artwork must be true for vibe-svgs-community")
            identity_status = asset.get("identity_status")
            if identity_status != "community-artwork":
                errors.append(
                    f"{prefix}.identity_status must be community-artwork; community artwork cannot be called official"
                )
            if asset.get("user_confirmed") is not True:
                errors.append(
                    f"{prefix}.user_confirmed must be true before community artwork is used as a mascot"
                )

        disposition = asset.get("render_disposition")
        if not isinstance(disposition, str) or disposition not in ALLOWED_RENDER_DISPOSITIONS:
            errors.append(f"{prefix}.render_disposition must be local or embedded")
        if disposition == "local" and not _nonempty_string(asset.get("local_path")):
            errors.append(f"{prefix}.local_path must be a non-empty string for local render disposition")

        if asset.get("identity_locked") is not True:
            errors.append(f"{prefix}.identity_locked must be true")
        if asset.get("status") != "PASS":
            errors.append(f"{prefix}.status must be PASS before production")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a verified identity asset plan")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2))
        return 1
    errors = validate(payload)
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
