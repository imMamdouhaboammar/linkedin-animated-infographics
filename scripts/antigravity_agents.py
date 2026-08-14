#!/usr/bin/env python3
"""Antigravity agent definition generator, manager, and catalog exporter.

Parses canonical Markdown agent definitions in agents/*.md and converts them into
Antigravity subagent specifications (name, description, system_prompt, role,
tools, and recommended model tier).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
CATALOG_PATH = ROOT / ".agents" / "agents" / "catalog.json"

WRITE_AGENTS = frozenset({
    "artboard-builder",
    "community-publisher",
    "layout-composer",
    "mascot-animator",
    "motion-director",
    "motion-engineer",
})

PRO_MODEL_AGENTS = frozenset({
    "creative-director",
    "post-critic",
    "story-verifier",
    "layout-composer",
    "motion-director",
})

FLASH_MODEL_AGENTS = frozenset({
    "evidence-checker",
    "design-study",
    "palette-curator",
    "type-curator",
    "copy-compressor",
    "caption-writer",
    "render-qa",
    "masterone",
})


def parse_agent_md(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    frontmatter: dict[str, Any] = {}
    body = text

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            for line in fm_text.strip().splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    key = key.strip()
                    val = val.strip()
                    if key in ("name", "description", "model", "tools"):
                        frontmatter[key] = val

    name = frontmatter.get("name", path.stem)
    description = frontmatter.get("description", f"Specialized agent for {name}")
    role = " ".join(word.capitalize() for word in name.split("-"))

    is_write = name in WRITE_AGENTS
    if name in PRO_MODEL_AGENTS:
        model_tier = "pro"
    elif name in FLASH_MODEL_AGENTS:
        model_tier = "flash"
    else:
        model_tier = "inherit"

    return {
        "name": name,
        "role": role,
        "description": description,
        "enable_write_tools": is_write,
        "enable_mcp_tools": False,
        "enable_subagent_tools": False,
        "model": model_tier,
        "system_prompt": body,
        "source_file": str(path.relative_to(ROOT)),
    }


def load_agent_catalog(agents_dir: Path = AGENTS_DIR) -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}
    for md_file in sorted(agents_dir.glob("*.md")):
        agent_def = parse_agent_md(md_file)
        catalog[agent_def["name"]] = agent_def
    return catalog


def export_catalog(dest_path: Path = CATALOG_PATH) -> None:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    catalog = load_agent_catalog()
    dest_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Exported {len(catalog)} agent definitions to {dest_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Antigravity agent definition manager")
    parser.add_argument("command", choices=["list", "export", "get", "check"], default="list", nargs="?")
    parser.add_argument("--name", help="Agent name for 'get' command")
    args = parser.parse_args(argv)

    catalog = load_agent_catalog()

    if args.command == "list":
        print(f"Discovered {len(catalog)} Antigravity agents:")
        for name, spec in catalog.items():
            write_flag = "WRITE" if spec["enable_write_tools"] else "READ"
            print(f"  - {name:<22} [{write_flag:<5}] [Model: {spec['model']:<7}] : {spec['description'][:65]}...")
        return 0

    if args.command == "export":
        export_catalog()
        return 0

    if args.command == "get":
        if not args.name:
            print("ERROR: --name required for 'get' command", file=sys.stderr)
            return 1
        if args.name not in catalog:
            print(f"ERROR: Agent '{args.name}' not found", file=sys.stderr)
            return 1
        print(json.dumps(catalog[args.name], indent=2, ensure_ascii=False))
        return 0

    if args.command == "check":
        if len(catalog) < 19:
            print(f"ERROR: Expected at least 19 agents, found {len(catalog)}", file=sys.stderr)
            return 1
        for name, spec in catalog.items():
            if not spec["description"] or not spec["system_prompt"]:
                print(f"ERROR: Agent {name} missing description or system prompt", file=sys.stderr)
                return 1
        print(f"Antigravity agents check: OK ({len(catalog)} agents verified)")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
