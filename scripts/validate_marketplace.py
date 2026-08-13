#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGIN_VERSION = "3.3.0"


def _load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        errors.append(f"missing {path}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
    return None


def _require_frontmatter(paths, root: Path, errors: list[str]):
    for path in paths:
        if not path.read_text().startswith("---\n"):
            errors.append(f"missing YAML frontmatter: {path.relative_to(root)}")


def validate_marketplace(root: Path = ROOT) -> list[str]:
    errors = []
    market = _load_json(root / ".claude-plugin" / "marketplace.json", errors)
    plugin = _load_json(root / ".claude-plugin" / "plugin.json", errors)
    if not market or not plugin:
        return errors
    if market.get("name") != "mamdouh-creative-tools":
        errors.append("unexpected marketplace name")
    if not (market.get("owner") or {}).get("name"):
        errors.append("marketplace owner.name is required")
    entries = market.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        errors.append("marketplace must expose exactly one root plugin")
        return errors
    entry = entries[0]
    if entry.get("name") != plugin.get("name"):
        errors.append("marketplace plugin name does not match plugin.json")
    if entry.get("source") != "./":
        errors.append("root plugin source must be ./")
    if entry.get("strict") is not True:
        errors.append("root plugin must use strict mode")
    if "version" in entry:
        errors.append("marketplace plugin entry must omit version; plugin.json is authoritative")
    if plugin.get("version") != EXPECTED_PLUGIN_VERSION:
        errors.append(f"plugin release version must be {EXPECTED_PLUGIN_VERSION}")
    for relative in ("skills", "agents", "hooks/hooks.json", "helper", "demos", "schemas/demo.schema.json"):
        if not (root / relative).exists():
            errors.append(f"missing standard plugin component {relative}")
    hooks = _load_json(root / "hooks" / "hooks.json", errors)
    if hooks is not None and "hooks" not in hooks:
        errors.append("hooks/hooks.json is missing top-level hooks")
    _require_frontmatter((root / "skills").glob("*/SKILL.md"), root, errors)
    _require_frontmatter((root / "agents").glob("*.md"), root, errors)
    return errors


def main():
    errors = validate_marketplace(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Claude marketplace: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
