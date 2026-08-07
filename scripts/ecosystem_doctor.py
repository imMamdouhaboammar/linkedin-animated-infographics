#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_TYPES = ("skills", "agents", "tools")
CRITICAL_SHIPPING = ("creative-director", "post-critic", "story-verifier")


def _load_json(path: Path, errors: list[str], label: str):
    if not path.exists():
        errors.append(f"missing {label}: {path}")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {label}: {exc}")
        return None


def _inventory(root: Path) -> dict[str, set[str]]:
    return {
        "skills": {path.parent.name for path in (root / "skills").glob("*/SKILL.md")},
        "agents": {path.stem for path in (root / "agents").glob("*.md")},
        "tools": {path.stem for path in (root / "tools").glob("*.py")},
    }


def _text_reference_corpus(root: Path) -> str:
    parts = []
    for base in (root / "skills", root / "agents", root / "helper"):
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in {".md", ".json"}:
                try:
                    parts.append(path.read_text())
                except UnicodeDecodeError:
                    pass
    return "\n".join(parts)


def validate_ecosystem_doctor(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    helper = root / "helper"

    manifest_doc = _load_json(helper / "modules.json", errors, "module manifest")
    router_doc = _load_json(helper / "router.json", errors, "router registry")
    capabilities_doc = _load_json(helper / "capabilities.json", errors, "capability registry")
    artifacts_doc = _load_json(helper / "artifacts.json", errors, "artifact registry")
    quality_doc = _load_json(helper / "quality-gates.json", errors, "local quality gates")
    graph_doc = _load_json(root / "architecture" / "plugin-graph.json", errors, "plugin graph")
    research_doc = _load_json(root / "research" / "capability-notes" / "gates.json", errors, "research gates")
    if not all((manifest_doc, router_doc, capabilities_doc, artifacts_doc, quality_doc, graph_doc, research_doc)):
        return errors

    manifest = manifest_doc.get("modules", {})
    inventory = _inventory(root)

    for module_type in MODULE_TYPES:
        declared = set(manifest.get(module_type, {}))
        actual = inventory[module_type]
        for name in sorted(actual - declared):
            label = module_type[:-1]
            errors.append(f"undeclared public {label} {name}")
        for name in sorted(declared - actual):
            errors.append(f"declared {module_type[:-1]} missing from filesystem: {name}")

    for module_type, entries in manifest.items():
        if module_type not in MODULE_TYPES:
            errors.append(f"unknown module type in manifest: {module_type}")
            continue
        for name, contract in entries.items():
            for field in ("path", "role", "tests", "reachable_from"):
                if contract.get(field) in (None, "", []):
                    errors.append(f"{module_type}:{name} missing {field}")
            relative = contract.get("path", "")
            path = root / relative
            if relative and not path.exists():
                errors.append(f"{module_type}:{name} path does not exist: {relative}")
            if path.exists():
                text = path.read_text()
                if len(text.strip()) < 80:
                    errors.append(f"{module_type}:{name} is too small to be a real active module")
                lowered = text.lower()
                if "todo: implement" in lowered or "placeholder module" in lowered:
                    errors.append(f"{module_type}:{name} is a placeholder module")
            for test_path in contract.get("tests", []):
                if not (root / test_path).exists():
                    errors.append(f"{module_type}:{name} test contract missing: {test_path}")

    routes = router_doc.get("routes", {})
    conditions = router_doc.get("conditions", {})
    graph_agents = graph_doc.get("agents", {})
    workflow = graph_doc.get("workflows", {}).get("new-post", {})
    sequence = workflow.get("sequence", [])
    conditional_edges = workflow.get("conditional", {})

    reachable_skills: set[str] = set()
    reachable_agents: set[str] = set(sequence)
    for edge in conditional_edges.values():
        if edge.get("agent"):
            reachable_agents.add(edge["agent"])
    for route in routes.values():
        reachable_skills.update(route.get("skills", []))
        if route.get("workflow") not in (None, "focused"):
            reachable_skills.add(route["workflow"])
        reachable_agents.update(route.get("agents", []))
    for condition in conditions.values():
        reachable_skills.update(condition.get("adds_skills", []))
        reachable_agents.update(condition.get("adds_agents", []))
    for contract in graph_agents.values():
        reachable_skills.update(contract.get("required_skills", []))

    for skill in sorted(set(manifest.get("skills", {})) - reachable_skills):
        errors.append(f"unreachable active skill {skill}")
    for agent in sorted(set(manifest.get("agents", {})) - reachable_agents):
        errors.append(f"unreachable active agent {agent}")

    reference_corpus = _text_reference_corpus(root)
    for tool, contract in manifest.get("tools", {}).items():
        filename = Path(contract.get("path", "")).name
        if filename and filename not in reference_corpus:
            errors.append(f"active tool {tool} is not referenced by executable guidance")

    graph_agent_names = set(graph_agents)
    manifest_agent_names = set(manifest.get("agents", {}))
    if graph_agent_names != manifest_agent_names:
        missing = sorted(manifest_agent_names - graph_agent_names)
        extra = sorted(graph_agent_names - manifest_agent_names)
        if missing:
            errors.append(f"plugin graph missing active agents: {', '.join(missing)}")
        if extra:
            errors.append(f"plugin graph contains undeclared agents: {', '.join(extra)}")

    helper_capabilities = capabilities_doc.get("capabilities", {})
    graph_capabilities = graph_doc.get("capabilities", {})
    if set(helper_capabilities) != set(graph_capabilities):
        errors.append("helper capability set differs from plugin graph capability set")
    for capability, contract in helper_capabilities.items():
        owners = set(contract.get("owners", []))
        undeclared = sorted(owners - manifest_agent_names)
        if undeclared:
            errors.append(f"capability {capability} has undeclared owners: {', '.join(undeclared)}")
        graph_owners = set(graph_capabilities.get(capability, []))
        if owners != graph_owners:
            errors.append(f"capability {capability} owner drift between helper and plugin graph")

    participants = manifest_agent_names | {"parent:new-post"}
    for artifact, contract in artifacts_doc.get("artifacts", {}).items():
        producer = contract.get("producer")
        if producer not in participants:
            errors.append(f"artifact {artifact} has undeclared producer {producer}")
        for consumer in contract.get("consumers", []):
            if consumer not in participants:
                errors.append(f"artifact {artifact} has undeclared consumer {consumer}")

    for gate_id, gate in quality_doc.get("gates", {}).items():
        owners = set(gate.get("owners", []))
        undeclared = sorted(owners - manifest_agent_names)
        if undeclared:
            errors.append(f"quality gate {gate_id} has undeclared owners: {', '.join(undeclared)}")
        if gate.get("severity") not in {"blocking", "advisory"}:
            errors.append(f"quality gate {gate_id} has invalid severity")
        unknown_intents = sorted(set(gate.get("applies_to_intents", [])) - set(routes))
        if unknown_intents:
            errors.append(f"quality gate {gate_id} has unknown intents: {', '.join(unknown_intents)}")

    for gate_id, gate in research_doc.get("gates", {}).items():
        owners = set(gate.get("owners", []))
        undeclared = sorted(owners - manifest_agent_names)
        if undeclared:
            errors.append(f"research gate {gate_id} has undeclared owners: {', '.join(undeclared)}")
        for relative in gate.get("implementation_refs", []):
            if not (root / relative).exists():
                errors.append(f"research gate {gate_id} has dead implementation reference: {relative}")

    helper_create_agents = routes.get("create-post", {}).get("agents", [])
    if helper_create_agents != sequence:
        errors.append("create-post helper route differs from plugin graph new-post sequence")

    for worker in CRITICAL_SHIPPING:
        if worker not in sequence:
            errors.append(f"critical shipping worker missing from new-post sequence: {worker}")

    mascot_condition = conditions.get("official_mascot", {})
    mascot_edge = conditional_edges.get("mascot", {})
    if mascot_condition.get("adds_agents", []) != ([mascot_edge.get("agent")] if mascot_edge.get("agent") else []):
        errors.append("official mascot router condition differs from graph mascot edge")
    if mascot_condition.get("asset_gate") != mascot_edge.get("asset_gate"):
        errors.append("official mascot asset gate differs from graph mascot edge")

    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Strictly validate that every public ecosystem module is real, reachable, and cross-linked")
    parser.add_argument("command", nargs="?", default="check", choices=("check",))
    parser.parse_args(argv)
    errors = validate_ecosystem_doctor(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Ecosystem doctor: FAIL ({len(errors)} findings)")
        return 1
    print("Ecosystem doctor: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
