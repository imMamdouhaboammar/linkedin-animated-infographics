#!/usr/bin/env python3
"""Validate native OpenAI/Codex packaging, submission readiness, and host parity."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAME = "linkedin-animated-infographics"
EXPECTED_VERSION = "3.3.0"
EXPECTED_OPENAI_SKILLS_ROOT = "openai-skills"
EXPECTED_OPENAI_SKILL = Path("openai-skills/linkedin-infographic-studio")
EXPECTED_OPENAI_AUTOPILOT = Path("openai-skills/linkedin-infographic-autopilot")
EXPECTED_AUTOPILOT_CODEX_AGENTS = {
    "creative_director",
    "evidence_researcher",
    "copy_director",
    "layout_composer",
    "still_critic",
    "motion_director",
    "render_qa",
    "final_verifier",
    "tool_runner",
}
EXPECTED_CODEX_AGENTS = {"explorer", "reviewer", "docs_researcher"} | EXPECTED_AUTOPILOT_CODEX_AGENTS
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
REQUIRED_OPENAI_SKILL_FILES = (
    "SKILL.md",
    "references/openai-runtime.md",
    "references/role-passes.md",
    "references/visual-quality-contract.md",
    "references/motion-quality-contract.md",
)
REQUIRED_AUTOPILOT_FILES = (
    "SKILL.md",
    "references/capability-negotiation.md",
    "references/execution-paths.md",
    "references/side-jobs.md",
    "references/artifact-workspace.md",
    "references/tool-usage-policy.md",
    "references/autopilot-failure-policy.md",
    "references/workspace-agents-bridge.md",
)
FORBIDDEN_OPENAI_RUNTIME_REFERENCES = (
    ".claude-plugin/",
    "agents/",
    "${CLAUDE_PLUGIN_ROOT}",
    "helper/",
    "architecture/",
)
REQUIRED_VISUAL_MARKERS = (
    "82-92%",
    "120px",
    "Maximum bordered containment depth is two levels",
    "top-heavy-composition",
    "bottom-dead-zone",
    "nested-card-density",
    "generic-ui-grammar",
    "weak-macro-rhythm",
    "weak-visual-anchor",
    "footer-detachment",
    "motion-on-weak-still",
    "decorative-motion",
    "feed-scale-legibility",
    "Maximum two targeted repair attempts",
)
REQUIRED_AUTOPILOT_CAPABILITIES = (
    "subagents",
    "sandbox_write",
    "shell_or_code_execution",
    "image_inspection",
    "web_research",
    "connected_apps",
    "workspace_agents",
    "publishing_tools",
)
REQUIRED_AUTOPILOT_PATHS = (
    "full-autopilot",
    "tool-rich-sequential",
    "safe-skill-only",
)
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
    "composerIcon",
    "logo",
}
REQUIRED_POSITIVE_CASE_FIELDS = {
    "id",
    "user_prompt",
    "expected_behavior",
    "expected_result_shape",
    "fixture_data",
}
REQUIRED_NEGATIVE_CASE_FIELDS = {
    "id",
    "user_prompt_or_scenario",
    "expected_safe_behavior",
    "why_not_complete",
}
POLICY_FILES = ("PRIVACY.md", "TERMS.md", "SUPPORT.md")


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
    supplied = Path(relative)
    if supplied.is_absolute():
        return None
    root_resolved = root.resolve()
    resolved = (root_resolved / supplied).resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError:
        return None
    return resolved


def _validate_square_asset(path: Path, field: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"OpenAI plugin {field} path does not exist")
        return
    if path.suffix.lower() != ".svg":
        return
    text = path.read_text(encoding="utf-8")
    viewbox = re.search(r'viewBox=["\']\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*["\']', text)
    if not viewbox:
        errors.append(f"OpenAI plugin {field} SVG must declare a viewBox")
        return
    width = float(viewbox.group(3))
    height = float(viewbox.group(4))
    if width != height:
        errors.append(f"OpenAI plugin {field} must reference a square image")


def _validate_openai_skill_bundle(root: Path, errors: list[str]) -> None:
    skill_root = root / EXPECTED_OPENAI_SKILL
    if not skill_root.is_dir():
        errors.append(f"missing OpenAI studio skill: {EXPECTED_OPENAI_SKILL.as_posix()}")
    else:
        for relative in REQUIRED_OPENAI_SKILL_FILES:
            path = skill_root / relative
            if not path.is_file():
                errors.append(f"missing OpenAI studio skill file: {path.relative_to(root)}")

        markdown_files = sorted(skill_root.rglob("*.md"))
        combined = "\n".join(path.read_text(encoding="utf-8") for path in markdown_files)
        for forbidden in FORBIDDEN_OPENAI_RUNTIME_REFERENCES:
            if forbidden in combined:
                errors.append(f"OpenAI studio skill contains unavailable runtime reference: {forbidden}")

        visual_contract = skill_root / "references" / "visual-quality-contract.md"
        if visual_contract.is_file():
            text = visual_contract.read_text(encoding="utf-8")
            for marker in REQUIRED_VISUAL_MARKERS:
                if marker not in text:
                    errors.append(f"OpenAI visual quality contract missing marker: {marker}")

        main_skill = skill_root / "SKILL.md"
        if main_skill.is_file():
            text = main_skill.read_text(encoding="utf-8")
            if "Do not proceed to motion while a blocking still defect remains" not in text:
                errors.append("OpenAI studio skill must block motion until still QA passes")

    autopilot_root = root / EXPECTED_OPENAI_AUTOPILOT
    if not autopilot_root.is_dir():
        errors.append(f"missing OpenAI autopilot skill: {EXPECTED_OPENAI_AUTOPILOT.as_posix()}")
        return

    for relative in REQUIRED_AUTOPILOT_FILES:
        path = autopilot_root / relative
        if not path.is_file():
            errors.append(f"missing OpenAI autopilot skill file: {path.relative_to(root)}")

    markdown_files = sorted(autopilot_root.rglob("*.md"))
    combined = "\n".join(path.read_text(encoding="utf-8") for path in markdown_files)
    for forbidden in FORBIDDEN_OPENAI_RUNTIME_REFERENCES:
        if forbidden in combined:
            errors.append(f"OpenAI autopilot contains unavailable runtime reference: {forbidden}")

    for path_name in REQUIRED_AUTOPILOT_PATHS:
        if path_name not in combined:
            errors.append(f"OpenAI autopilot missing execution path: {path_name}")
    for capability in REQUIRED_AUTOPILOT_CAPABILITIES:
        if capability not in combined:
            errors.append(f"OpenAI autopilot missing capability contract: {capability}")
    if "Unknown capabilities are unavailable" not in combined:
        errors.append("OpenAI autopilot must fail closed on unknown capabilities")
    if "not automatically registered" not in combined and "does not automatically register Workspace Agents" not in combined:
        errors.append("OpenAI autopilot must state that Workspace Agents are not automatically registered")
    if "Never claim" not in combined:
        errors.append("OpenAI autopilot must forbid fabricated tool or agent execution claims")


def _validate_openai_manifest(root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("name") != EXPECTED_NAME:
        errors.append("OpenAI plugin name drift")
    if manifest.get("version") != EXPECTED_VERSION:
        errors.append("OpenAI plugin version drift")

    skills_value = manifest.get("skills")
    skills_path = _safe_repo_path(root, skills_value) if isinstance(skills_value, str) else None
    expected_skills = (root / EXPECTED_OPENAI_SKILLS_ROOT).resolve()
    if skills_path is None:
        errors.append("unsafe OpenAI plugin skills path")
    elif skills_path != expected_skills:
        errors.append("OpenAI plugin skills path must resolve to the isolated OpenAI skills root")
    elif not skills_path.is_dir():
        errors.append("OpenAI plugin skills path does not resolve to a directory")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("OpenAI plugin interface must be an object")
        return
    for field in sorted(REQUIRED_INTERFACE):
        if interface.get(field) in (None, "", []):
            errors.append(f"OpenAI plugin interface missing {field}")
    if interface.get("category") != "Productivity":
        errors.append("OpenAI plugin interface category must be Productivity")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or any(
        not isinstance(item, str) or not item.strip() for item in prompts
    ):
        errors.append("OpenAI plugin defaultPrompt must contain one to three non-empty prompts")

    if "screenshots" in interface:
        errors.append("OpenAI plugin interface must not declare screenshots for a skills-only ZIP")

    for field in ("composerIcon", "logo"):
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"OpenAI plugin interface missing {field}")
            continue
        target = _safe_repo_path(root, value)
        if target is None:
            errors.append(f"unsafe OpenAI plugin {field} path")
        else:
            _validate_square_asset(target, field, errors)


def _validate_codex_marketplace(root: Path, marketplace: dict[str, Any], errors: list[str]) -> None:
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
    if not isinstance(source, dict):
        errors.append("Codex marketplace source must be an object")
    else:
        if source.get("source") != "local":
            errors.append("Codex marketplace source type must be local")
        source_path = source.get("path")
        target = _safe_repo_path(root, source_path) if isinstance(source_path, str) else None
        if target is None:
            errors.append("Codex marketplace source path is unsafe")
        elif target != root.resolve():
            errors.append("Codex marketplace source path must resolve to plugin root")

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


def _validate_claude_release(
    claude: dict[str, Any] | None,
    claude_marketplace: dict[str, Any] | None,
    openai_manifest: dict[str, Any] | None,
    errors: list[str],
) -> None:
    if claude:
        if claude.get("name") != EXPECTED_NAME:
            errors.append("Claude plugin name drift")
        if claude.get("version") != EXPECTED_VERSION:
            errors.append("Claude plugin version drift")
        if openai_manifest and claude.get("name") != openai_manifest.get("name"):
            errors.append("Claude/OpenAI plugin name drift")
        if openai_manifest and claude.get("version") != openai_manifest.get("version"):
            errors.append("Claude/OpenAI plugin version drift")

    if not claude_marketplace:
        return
    entries = claude_marketplace.get("plugins")
    if not isinstance(entries, list):
        errors.append("Claude marketplace plugins must be a list")
        return
    matching = [entry for entry in entries if isinstance(entry, dict) and entry.get("name") == EXPECTED_NAME]
    if len(matching) != 1:
        errors.append("Claude marketplace must contain exactly one matching plugin entry")
        return
    entry = matching[0]
    if entry.get("version") != EXPECTED_VERSION:
        errors.append("Claude marketplace version drift")
    if claude and entry.get("version") != claude.get("version"):
        errors.append("Claude marketplace/plugin version drift")


def _validate_compatibility(root: Path, registry: dict[str, Any], errors: list[str]) -> None:
    if registry.get("plugin_name") != EXPECTED_NAME:
        errors.append("compatibility plugin name drift")
    if registry.get("plugin_version") != EXPECTED_VERSION:
        errors.append("compatibility plugin version drift")

    surfaces = registry.get("surfaces")
    if not isinstance(surfaces, list) or not {"codex", "chatgpt"}.issubset(set(surfaces)):
        errors.append("compatibility surfaces must include codex and chatgpt")

    expected_manifests = {
        "openai": ".codex-plugin/plugin.json",
        "claude": ".claude-plugin/plugin.json",
        "openai_marketplace": ".agents/plugins/marketplace.json",
        "claude_marketplace": ".claude-plugin/marketplace.json",
    }
    manifests = registry.get("manifests")
    if not isinstance(manifests, dict):
        errors.append("compatibility manifests must be an object")
    else:
        for key, expected in expected_manifests.items():
            if manifests.get(key) != expected:
                errors.append(f"compatibility manifest path drift: {key}")

    distributions = registry.get("distributions")
    if not isinstance(distributions, dict):
        errors.append("compatibility distributions must be an object")
    else:
        claude_dist = distributions.get("claude")
        openai_dist = distributions.get("openai")
        if not isinstance(claude_dist, dict) or claude_dist.get("skills_root") != "skills":
            errors.append("Claude distribution must keep the canonical skills root")
        if not isinstance(claude_dist, dict) or claude_dist.get("execution") != "native-worker-graph":
            errors.append("Claude distribution must preserve native worker graph execution")
        if not isinstance(openai_dist, dict) or openai_dist.get("skills_root") != EXPECTED_OPENAI_SKILLS_ROOT:
            errors.append("OpenAI distribution must use the isolated OpenAI skills root")
        elif openai_dist.get("execution") != "capability-negotiated-autopilot":
            errors.append("OpenAI distribution must use capability-negotiated-autopilot execution")
        elif openai_dist.get("sandbox_artifacts") is not True or openai_dist.get("side_jobs") is not True:
            errors.append("OpenAI distribution must enable sandbox artifact and side-job contracts")
        elif openai_dist.get("workspace_agents") != "optional":
            errors.append("OpenAI Workspace Agents support must remain optional")

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
    elif submission.get("skills_root") != EXPECTED_OPENAI_SKILLS_ROOT:
        errors.append("compatibility public submission must use the OpenAI skills root")


def _validate_codex_config(root: Path, errors: list[str]) -> None:
    config = _load_toml(root / ".codex" / "config.toml", errors, "Codex repository config")
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

    for name in sorted(EXPECTED_AUTOPILOT_CODEX_AGENTS):
        contract = agents.get(name)
        if not isinstance(contract, dict):
            errors.append(f"Codex repository config missing autopilot agent registration: {name}")
            continue
        expected_ref = f"agents/{name}.toml"
        if contract.get("config_file") != expected_ref:
            errors.append(f"Codex agent config reference drift for {name}")
        if not isinstance(contract.get("description"), str) or not contract["description"].strip():
            errors.append(f"Codex agent registration missing description: {name}")

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


def _validate_submission(root: Path, errors: list[str]) -> None:
    for filename in POLICY_FILES:
        path = root / filename
        if not path.is_file():
            errors.append(f"missing public policy document {filename}")
        elif len(path.read_text(encoding="utf-8").strip()) < 200:
            errors.append(f"public policy document is unexpectedly small: {filename}")

    metadata = _load_json(root / "submission" / "openai-plugin.json", errors, "OpenAI submission metadata")
    cases = _load_json(root / "submission" / "test-cases.json", errors, "OpenAI submission test cases")
    if not (root / "submission" / "README.md").is_file():
        errors.append("missing OpenAI submission README")

    if metadata:
        if metadata.get("name") != EXPECTED_NAME:
            errors.append("OpenAI submission plugin name drift")
        if metadata.get("version") != EXPECTED_VERSION:
            errors.append("OpenAI submission version drift")
        if metadata.get("submission_type") != "skills-only":
            errors.append("OpenAI submission type must be skills-only")
        if metadata.get("category") != "Productivity":
            errors.append("OpenAI submission category must be Productivity")
        if metadata.get("submission_status") != "prepared-not-submitted":
            errors.append("OpenAI submission status must remain prepared-not-submitted until external publication completes")
        if metadata.get("skills_bundle") != "./openai-skills/":
            errors.append("OpenAI submission skills bundle must use ./openai-skills/")

        prompts = metadata.get("starter_prompts")
        if not isinstance(prompts, list) or len(prompts) < 4 or any(
            not isinstance(item, str) or not item.strip() for item in prompts
        ):
            errors.append("OpenAI submission must include at least four starter prompts")
        if not isinstance(metadata.get("release_notes"), str) or not metadata["release_notes"].strip():
            errors.append("OpenAI submission release notes are required")

        urls = metadata.get("urls")
        if not isinstance(urls, dict) or any(
            not isinstance(urls.get(key), str) or not urls[key].startswith("https://")
            for key in ("website", "support", "privacy", "terms")
        ):
            errors.append("OpenAI submission requires public HTTPS website/support/privacy/terms URLs")

        prerequisites = metadata.get("external_prerequisites")
        prerequisite_text = (
            " ".join(prerequisites).lower()
            if isinstance(prerequisites, list) and all(isinstance(item, str) for item in prerequisites)
            else ""
        )
        for marker in ("apps management", "verified", "manual", "review"):
            if marker not in prerequisite_text:
                errors.append(f"OpenAI submission external prerequisites missing marker: {marker}")

    if cases:
        positive = cases.get("positive")
        negative = cases.get("negative")
        if not isinstance(positive, list) or len(positive) != 5:
            errors.append("OpenAI submission requires exactly five positive reviewer test cases")
        if not isinstance(negative, list) or len(negative) != 3:
            errors.append("OpenAI submission requires exactly three negative reviewer test cases")

        if isinstance(positive, list):
            for index, case in enumerate(positive, start=1):
                if not isinstance(case, dict):
                    errors.append(f"OpenAI positive reviewer case {index} must be an object")
                    continue
                missing = sorted(field for field in REQUIRED_POSITIVE_CASE_FIELDS if not case.get(field))
                if missing:
                    errors.append(f"OpenAI positive reviewer case {index} missing: {', '.join(missing)}")

        if isinstance(negative, list):
            for index, case in enumerate(negative, start=1):
                if not isinstance(case, dict):
                    errors.append(f"OpenAI negative reviewer case {index} must be an object")
                    continue
                missing = sorted(field for field in REQUIRED_NEGATIVE_CASE_FIELDS if not case.get(field))
                if missing:
                    errors.append(f"OpenAI negative reviewer case {index} missing: {', '.join(missing)}")


def validate_codex_plugin(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    openai_manifest = _load_json(root / ".codex-plugin" / "plugin.json", errors, "OpenAI plugin manifest")
    codex_marketplace = _load_json(root / ".agents" / "plugins" / "marketplace.json", errors, "Codex marketplace")
    registry = _load_json(root / "compatibility" / "codex.json", errors, "Codex compatibility registry")
    claude = _load_json(root / ".claude-plugin" / "plugin.json", errors, "Claude plugin manifest")
    claude_marketplace = _load_json(root / ".claude-plugin" / "marketplace.json", errors, "Claude marketplace")

    if openai_manifest:
        _validate_openai_manifest(root, openai_manifest, errors)
    _validate_openai_skill_bundle(root, errors)
    if codex_marketplace:
        _validate_codex_marketplace(root, codex_marketplace, errors)
    if registry:
        _validate_compatibility(root, registry, errors)
    _validate_claude_release(claude, claude_marketplace, openai_manifest, errors)
    _validate_codex_config(root, errors)
    _validate_submission(root, errors)
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
