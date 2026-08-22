#!/usr/bin/env python3
"""Validate Antigravity plugin packaging, agent catalog, lifecycle hooks, and host parity."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAME = "linkedin-animated-infographics"
EXPECTED_VERSION = "3.6.0"

EXPECTED_AGENTS = {
    "artboard-builder",
    "asset-curator",
    "caption-writer",
    "community-publisher",
    "copy-compressor",
    "creative-director",
    "design-study",
    "evidence-checker",
    "layout-composer",
    "mascot-animator",
    "masterone",
    "motion-director",
    "motion-engineer",
    "palette-curator",
    "post-critic",
    "render-qa",
    "story-architect",
    "story-verifier",
    "type-curator",
}

REQUIRED_FILES = [
    "plugin.json",
    ".agents/plugins/linkedin-animated-infographics/plugin.json",
    ".agents/plugins.json",
    ".agents/skills.json",
    ".agents/hooks.json",
    ".agents/rules/linkedin-animated-infographics.md",
    ".agents/agents/catalog.json",
    "compatibility/antigravity.json",
    "scripts/antigravity_agents.py",
]


def _load_json(path: Path, errors: list[str], label: str) -> Any:
    if not path.exists():
        errors.append(f"missing {label}: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {label} ({path}): {exc}")
        return None


def validate_antigravity_plugin(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    # 1. Verify required files exist
    for rel_path in REQUIRED_FILES:
        target = root / rel_path
        if not target.exists():
            errors.append(f"required file missing: {rel_path}")

    # 2. Validate root plugin.json
    root_plugin = _load_json(root / "plugin.json", errors, "root plugin.json")
    if root_plugin:
        if root_plugin.get("name") != EXPECTED_NAME:
            errors.append(f"root plugin.json name must be '{EXPECTED_NAME}', found: '{root_plugin.get('name')}'")
        if root_plugin.get("version") != EXPECTED_VERSION:
            errors.append(f"root plugin.json version must be '{EXPECTED_VERSION}', found: '{root_plugin.get('version')}'")
        if not root_plugin.get("description"):
            errors.append("root plugin.json missing description")
        if not root_plugin.get("interface"):
            errors.append("root plugin.json missing interface declaration")

    # 3. Validate .agents/plugins/linkedin-animated-infographics/plugin.json
    local_plugin = _load_json(root / ".agents/plugins/linkedin-animated-infographics/plugin.json", errors, "local plugin.json")
    if local_plugin:
        if local_plugin.get("name") != EXPECTED_NAME:
            errors.append(f"local plugin.json name mismatch: {local_plugin.get('name')}")
        if local_plugin.get("version") != EXPECTED_VERSION:
            errors.append(f"local plugin.json version mismatch: {local_plugin.get('version')}")

    # 4. Validate .agents/plugins.json & skills.json
    plugins_cfg = _load_json(root / ".agents/plugins.json", errors, "plugins.json")
    if plugins_cfg and "entries" not in plugins_cfg:
        errors.append(".agents/plugins.json missing 'entries' array")

    skills_cfg = _load_json(root / ".agents/skills.json", errors, "skills.json")
    if skills_cfg and "entries" not in skills_cfg:
        errors.append(".agents/skills.json missing 'entries' array")

    # 5. Validate .agents/hooks.json
    hooks_cfg = _load_json(root / ".agents/hooks.json", errors, "hooks.json")
    if hooks_cfg:
        if not isinstance(hooks_cfg, dict):
            errors.append(".agents/hooks.json must be a JSON object mapping hook names to configurations")

    # 6. Validate .agents/rules
    rules_path = root / ".agents/rules/linkedin-animated-infographics.md"
    if rules_path.exists():
        rules_text = rules_path.read_text(encoding="utf-8")
        for marker in ("1080x1350", "Lobe-first", "center-first", "Still-First QA"):
            if marker.lower() not in rules_text.lower():
                errors.append(f"rules missing critical guideline marker: '{marker}'")

    # 7. Validate agent catalog
    catalog = _load_json(root / ".agents/agents/catalog.json", errors, "catalog.json")
    if catalog:
        catalog_names = set(catalog.keys())
        missing_agents = sorted(EXPECTED_AGENTS - catalog_names)
        if missing_agents:
            errors.append(f"agent catalog missing canonical agents: {', '.join(missing_agents)}")

        for agent_name, agent_def in catalog.items():
            for field in ("name", "role", "description", "system_prompt", "model"):
                if not agent_def.get(field):
                    errors.append(f"agent {agent_name} in catalog missing required field: {field}")
            if "enable_write_tools" not in agent_def:
                errors.append(f"agent {agent_name} missing enable_write_tools")

    # 8. Validate compatibility/antigravity.json
    compat = _load_json(root / "compatibility/antigravity.json", errors, "antigravity.json")
    if compat:
        if compat.get("plugin_name") != EXPECTED_NAME:
            errors.append(f"compatibility plugin_name mismatch: {compat.get('plugin_name')}")
        if compat.get("plugin_version") != EXPECTED_VERSION:
            errors.append(f"compatibility plugin_version mismatch: {compat.get('plugin_version')}")
        dist = compat.get("distributions", {}).get("antigravity", {})
        supported_agents = set(dist.get("supported_agents", []))
        if supported_agents != EXPECTED_AGENTS:
            diff = sorted(EXPECTED_AGENTS.symmetric_difference(supported_agents))
            errors.append(f"supported_agents mismatch in compatibility/antigravity.json: {diff}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Antigravity plugin packaging and agents")
    parser.add_argument("command", nargs="?", default="check", choices=["check"])
    parser.parse_args(argv)

    errors = validate_antigravity_plugin()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Antigravity plugin validation: FAIL ({len(errors)} errors)", file=sys.stderr)
        return 1

    print("Antigravity plugin validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
