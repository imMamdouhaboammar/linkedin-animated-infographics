#!/usr/bin/env python3
"""Validate native OpenAI/Codex plugin packaging and shared-core parity."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAME = "linkedin-animated-infographics"
EXPECTED_VERSION = "3.2.0"
EXPECTED_CODEX_AGENTS = {"explorer", "reviewer", "docs_researcher"}
EXPECTED_CANONICAL = {
    "skills_root": "skills",
    "agents_root": "agents",
    "router": "helper/router.json",
    "capabilities": "helper/capabilities.json",
    "quality_gates": "helper/quality-gates.json",
    "artifacts": "helper/artifacts.json",
    "modules": "helper/modules.json",
    "research_gates": "research/capability-notes/gates.json",
    "worker_graph": "architecture/plugin-graph.json",
}
REQUIRED_INTERFACE = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "websiteURL",
    "privacyPolicyURL",
    "termsOfServiceURL",
    "defaultPrompt",
}


def _load_json(path: Path, errors: list[str], label: str) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing {label}: {path}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {label}: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{label} root must be an object")
        return None
    return data


def _load_toml(path: Path, errors: list[str], label: str) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing {label}: {path}")
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        errors.append(f"invalid TOML in {label}: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{label} root must be a table")
        return None
    return data


def _safe_repo_path(root: Path, relative: str) -> Path | None:
    if not isinstance(relative, str) or not relative.strip():
        return None
    candidate = Path(relative)
    if candidate.is_absolute():
        return None
    root_resolved = root.resolve()
    resolved = (root_resolved / candidate).resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError:
        return None
    return resolved


def _validate_openai_manifest(root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("name") != EXPECTED_NAME:
        errors.append("OpenAI plugin name drift")
    if manifest.get("version") != EXPECTED_VERSION:
        errors.append("OpenAI plugin version drift")

    skills_value = manifest.get("skills")
    if skills_value != "./skills/":
        errors.append("OpenAI plugin skills path must be ./skills/")
    skills_path = _safe_repo_path(root, skills_value or "")
    if skills_path is None:
        errors.append("unsafe OpenAI plugin skills path")
    elif not skills_path.is_dir():
        errors.append("OpenAI plugin skills path does not resolve to a directory")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("OpenAI plugin interface must be an object")
        return
    for field in sorted(REQUIRED_INTERFACE):
        value = interface.get(field)
        if value in (None, "", []):
            errors.append(f"OpenAI plugin interface missing {field}")
    if interface.get("category") != "Productivity":
        errors.append("OpenAI plugin interface category must be Productivity")
    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, list) or len(prompts) < 3 or any(not isinstance(item, str) or not item.strip() for item in prompts):
        errors.append("OpenAI plugin defaultPrompt must contain at least three non-empty prompts")

    for field in ("composerIcon", "logo"):
        value = interface.get(field)
        if value is None:
            continue
        target = _safe_repo_path(root, value)
        if target is None:
            errors.append(f"unsafe OpenAI plugin {field} path")
        elif not target.is_file():
            errors.append(f"OpenAI plugin {field} path does not exist")
    screenshots = interface.get("screenshots", [])
    if screenshots is not None:
        if not isinstance(screenshots, list):
            errors.append("OpenAI plugin screenshots must be a list")
        else:
            for value in screenshots:
                target = _safe_repo_path(root, value) if isinstance(value, str) else None
                if target is None:
                    errors.append("unsafe OpenAI plugin screenshot path")
                elif not target.is_file():
                    errors.append(f"OpenAI plugin screenshot path does not exist: {value}")


def _validate_marketplace(root: Path, marketplace: dict[str, Any], errors: list[str]) -> None:
    if marketplace.get("name") != "mamdouh-creative-tools":
        errors.append("Codex marketplace name drift")
    interface = marketplace.get("interface")
    if not isinstance(interface, dict) or not interface.get("displayName"):
        errors.append("Codex marketplace missing interface.displayName")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        errors.append("Codex marketplace must expose exactly one plugin")
        return
    entry = plugins[0]
    if not isinstance(entry, dict):
        errors.append("Codex marketplace plugin entry must be an object")
        return
    if entry.get("name") != EXPECTED_NAME:
        errors.append("Codex marketplace plugin name drift")
    source = entry.get("source")
    if source != {"source": "local", "path": "./"}:
        errors.append("Codex marketplace source must resolve to local plugin root ./")
    else:
        target = _safe_repo_path(root, source["path"])
        if target is None or target != root.resolve():
            errors.append("Codex marketplace source path is unsafe or does not resolve to plugin root")
    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append("Codex marketplace policy must be an object")
    else:
        if policy.get("installation") != "AVAILABLE":
            errors.append("Codex marketplace installation policy must be AVAILABLE")
        if policy.get("authentication") != "ON_INSTALL":
            errors.append("Codex marketplace authentication policy must be ON_INSTALL")
    if entry.get("category") != "Productivity":
        errors.append("Codex marketplace category must be Productivity")


def _validate_compatibility(root: Path, registry: dict[str, Any], errors: list[str]) -> None:
    if registry.get("plugin_name") != EXPECTED_NAME:
        errors.append("compatibility plugin name drift")
    if registry.get("plugin_version") != EXPECTED_VERSION:
        errors.append("compatibility plugin version drift")
    surfaces = registry.get("surfaces")
    if not isinstance(surfaces, list) or not {"codex", "chatgpt"}.issubset(set(surfaces)):
        errors.append("compatibility surfaces must include codex and chatgpt")

    manifests = registry.get("manifests")
    expected_manifests = {
        "openai": ".codex-plugin/plugin.json",
        "claude": ".claude-plugin/plugin.json",
        "openai_marketplace": ".agents/plugins/marketplace.json",
        "claude_marketplace": ".claude-plugin/marketplace.json",
    }
    if not isinstance(manifests, dict):
        errors.append("compatibility manifests must be an object")
    else:
        for key, expected in expected_manifests.items():
            if manifests.get(key) != expected:
                errors.append(f"compatibility manifest path drift: {key}")

    canonical = registry.get("canonical")
    if not isinstance(canonical, dict):
        errors.append("compatibility canonical registry must be an object")
    else:
        for key, expected in EXPECTED_CANONICAL.items():
            actual = canonical.get(key)
            if actual != expected:
                errors.append(f"compatibility canonical {key.replace('_', ' ')} path drift")
                continue
            target = _safe_repo_path(root, actual)
            if target is None:
                errors.append(f"unsafe compatibility canonical path: {key}")
            elif not target.exists():
                errors.append(f"compatibility canonical path does not exist: {key}")

    submission = registry.get("public_submission")
    if not isinstance(submission, dict) or submission.get("type") != "skills-only":
        errors.append("compatibility public submission type must be skills-only")


def _validate_codex_config(root: Path, errors: list[str]) -> None:
    config_path = root / ".codex" / "config.toml"
    config = _load_toml(config_path, errors, "Codex repository config")
    if config is None:
        return
    agents = config.get("agents", {})
    if not isinstance(agents, dict):
        errors.append("Codex repository config agents must be a table")
        return
    if agents.get("enabled") is not True:
        errors.append("Codex repository config must explicitly enable agents")
    if agents.get("max_concurrent_threads_per_session") != 6:
        errors.append("Codex repository config max_concurrent_threads_per_session must be 6")
    if "max_threads" in agents:
        errors.append("Codex repository config must not use legacy agents.max_threads")

    for key, contract in agents.items():
        if not isinstance(contract, dict):
            continue
        config_file = contract.get("config_file")
        if config_file is None:
            continue
        if not isinstance(config_file, str):
            errors.append(f"Codex agent config reference for {key} must be a string")
            continue
        target = _safe_repo_path(root / ".codex", config_file)
        if target is None:
            errors.append(f"unsafe Codex agent config reference for {key}: {config_file}")
        elif not target.is_file():
            errors.append(f"Codex agent config reference does not exist for {key}: {config_file}")

    agent_dir = root / ".codex" / "agents"
    if not agent_dir.is_dir():
        errors.append("missing .codex/agents directory")
        return
    found: set[str] = set()
    for path in sorted(agent_dir.glob("*.toml")):
        data = _load_toml(path, errors, f"Codex agent {path.name}")
        if data is None:
            continue
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"Codex agent {path.name} missing required name")
            continue
        found.add(name)
        if path.stem != name:
            errors.append(f"Codex agent filename/name drift: {path.name} != {name}")
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            errors.append(f"Codex agent {path.name} missing required description")
        if not isinstance(data.get("developer_instructions"), str) or not data["developer_instructions"].strip():
            errors.append(f"Codex agent {path.name} missing required developer_instructions")
    missing = sorted(EXPECTED_CODEX_AGENTS - found)
    if missing:
        errors.append(f"missing required project-scoped Codex agents: {', '.join(missing)}")


def validate_codex_plugin(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifest = _load_json(root / ".codex-plugin" / "plugin.json", errors, "OpenAI plugin manifest")
    marketplace = _load_json(root / ".agents" / "plugins" / "marketplace.json", errors, "Codex marketplace")
    registry = _load_json(root / "compatibility" / "codex.json", errors, "Codex compatibility registry")
    claude = _load_json(root / ".claude-plugin" / "plugin.json", errors, "Claude plugin manifest")

    if manifest:
        _validate_openai_manifest(root, manifest, errors)
    if marketplace:
        _validate_marketplace(root, marketplace, errors)
    if registry:
        _validate_compatibility(root, registry, errors)
    if manifest and claude and manifest.get("name") != claude.get("name"):
        errors.append("Claude/OpenAI plugin name drift")
    _validate_codex_config(root, errors)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", default="check", choices=("check",))
    parser.parse_args(argv)
    errors = validate_codex_plugin(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Codex plugin validation: FAIL ({len(errors)} findings)")
        return 1
    print("Codex plugin validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
