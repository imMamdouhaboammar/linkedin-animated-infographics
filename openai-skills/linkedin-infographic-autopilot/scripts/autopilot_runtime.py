#!/usr/bin/env python3
"""Deterministic helper for the OpenAI infographic autopilot skill.

The helper does not discover host capabilities by itself. The parent skill passes
only capabilities it has actually observed in the current host. Unknown or
non-boolean values fail closed to False.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

CAPABILITY_KEYS = (
    "subagents",
    "sandbox_write",
    "shell_or_code_execution",
    "image_inspection",
    "web_research",
    "connected_apps",
    "workspace_agents",
    "publishing_tools",
)

EXECUTION_CAPABILITIES = (
    "sandbox_write",
    "shell_or_code_execution",
    "image_inspection",
    "web_research",
    "connected_apps",
    "workspace_agents",
    "publishing_tools",
)

WORKSPACE_DIRECTORIES = (
    "brief",
    "evidence",
    "concepts",
    "selected-direction",
    "copy",
    "layout",
    "build",
    "still-review",
    "motion",
    "render-qa",
    "verifier",
    "final",
)

LOGICAL_ARTIFACTS = (
    "evidence/evidence.json",
    "concepts/directions.md",
    "selected-direction/decision.md",
    "copy/copy-slots.md",
    "layout/layout-plan.json",
    "build/index.html",
    "still-review/report.json",
    "motion/motion-plan.json",
    "render-qa/report.json",
    "verifier/report.json",
    "final/delivery.json",
)

DISCOVERY_JOBS = (
    "evidence-research",
    "creative-direction-exploration",
    "visual-archetype-exploration",
    "copy-compression-critique",
)

DEPENDENCY_BOUND_JOBS = (
    "still-critique",
    "render-qa",
    "final-verification",
)


def normalize_capabilities(raw: Mapping[str, Any] | None = None) -> dict[str, bool]:
    """Return the canonical capability map and fail closed on unknown values."""
    raw = raw or {}
    return {key: raw.get(key) is True for key in CAPABILITY_KEYS}


def select_execution_path(capabilities: Mapping[str, bool]) -> str:
    """Choose the strongest safe runtime path from observed capabilities."""
    has_execution = any(capabilities.get(key) is True for key in EXECUTION_CAPABILITIES)
    if capabilities.get("subagents") is True and has_execution:
        return "full-autopilot"
    if has_execution:
        return "tool-rich-sequential"
    return "safe-skill-only"


def build_dispatch_plan(capabilities: Mapping[str, bool]) -> dict[str, Any]:
    """Build a bounded side-job plan without pretending delegation exists."""
    real_delegation = capabilities.get("subagents") is True
    return {
        "execution_path": select_execution_path(capabilities),
        "discovery_mode": "parallel" if real_delegation else "sequential",
        "real_delegation": real_delegation,
        "discovery_jobs": list(DISCOVERY_JOBS),
        "dependency_bound_jobs": list(DEPENDENCY_BOUND_JOBS),
        "must_wait_for_discovery": True,
        "shared_write_policy": "single-owner",
    }


def create_workspace(root: Path) -> list[str]:
    """Create directories only. Do not fabricate logical artifact files."""
    root = Path(root)
    created: list[str] = []
    for relative in WORKSPACE_DIRECTORIES:
        (root / relative).mkdir(parents=True, exist_ok=True)
        created.append(relative)
    return created


def runtime_summary(raw: Mapping[str, Any]) -> dict[str, Any]:
    capabilities = normalize_capabilities(raw)
    return {
        "capabilities": capabilities,
        "execution_path": select_execution_path(capabilities),
        "dispatch_plan": build_dispatch_plan(capabilities),
        "logical_artifacts": list(LOGICAL_ARTIFACTS),
    }


def _parse_capabilities(value: str) -> dict[str, Any]:
    data = json.loads(value)
    if not isinstance(data, dict):
        raise ValueError("capabilities JSON must be an object")
    return data


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("select-path", "dispatch-plan", "summary"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--capabilities-json", required=True)

    init = subparsers.add_parser("init-workspace")
    init.add_argument("root")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "init-workspace":
        root = Path(args.root)
        created = create_workspace(root)
        print(json.dumps({"root": str(root), "created_directories": created}, indent=2))
        return 0

    raw = _parse_capabilities(args.capabilities_json)
    capabilities = normalize_capabilities(raw)

    if args.command == "select-path":
        print(select_execution_path(capabilities))
    elif args.command == "dispatch-plan":
        print(json.dumps(build_dispatch_plan(capabilities), indent=2, sort_keys=True))
    else:
        print(json.dumps(runtime_summary(raw), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
