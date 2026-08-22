#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGIN_VERSION = "3.7.0"


def validate_marketplace(root: Path = ROOT) -> list[str]:
    errors = []
    try:
        market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
        plugin = json.loads((root / ".claude-plugin/plugin.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid marketplace contract: {exc}"]

    if market.get("name") != "mamdouh-creative-tools":
        errors.append("unexpected marketplace name")
    entries = market.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        return errors + ["marketplace must expose exactly one root plugin"]
    entry = entries[0]
    if entry.get("name") != plugin.get("name"):
        errors.append("marketplace plugin name does not match plugin.json")
    if entry.get("source") != "./":
        errors.append("root plugin source must be ./")
    if entry.get("strict") is not True:
        errors.append("root plugin must use strict mode")
    if entry.get("version") != plugin.get("version"):
        errors.append("marketplace plugin version does not match plugin.json")
    if plugin.get("version") != EXPECTED_PLUGIN_VERSION:
        errors.append(f"plugin release version must be {EXPECTED_PLUGIN_VERSION}")

    for relative in ("skills", "agents", "hooks/hooks.json", "helper", "demos", "schemas/demo.schema.json"):
        if not (root / relative).exists():
            errors.append(f"missing standard plugin component {relative}")
    return errors


def main():
    errors = validate_marketplace()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Claude marketplace: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
