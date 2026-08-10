#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ALLOWED_SOURCE_TYPES = {"user-official", "lobe"}
ALLOWED_RENDER_DISPOSITIONS = {"local", "embedded"}
LOBE_PACKAGE_RE = re.compile(r"^@lobehub/icons-(?:static-svg|static-avatar)@[^@\s:]+$")


def _nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


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
            errors.append(f"{prefix}.source_type must be user-official or lobe")

        if source_type == "lobe":
            if not _nonempty_string(asset.get("lobe_slug")):
                errors.append(f"{prefix}.lobe_slug must be a non-empty string for Lobe assets")

            package = asset.get("package")
            if not isinstance(package, str):
                errors.append(f"{prefix}.package must be a versioned @lobehub/icons static package string")
            elif not LOBE_PACKAGE_RE.fullmatch(package.strip()):
                errors.append(f"{prefix}.package must include an explicit version, for example @lobehub/icons-static-svg@1.91.0")

            source_ref = asset.get("source_ref")
            if isinstance(package, str) and LOBE_PACKAGE_RE.fullmatch(package.strip()):
                if not isinstance(source_ref, str) or not source_ref.startswith(package.strip() + ":"):
                    errors.append(f"{prefix}.source_ref must include the same versioned Lobe package followed by an immutable asset reference")

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
