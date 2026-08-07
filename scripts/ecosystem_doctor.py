#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_TYPES = ("skills", "agents", "tools")
CRITICAL_SHIPPING = ("creative-director", "post-critic", "story-verifier")
PUBLIC_SCRIPT_TOOLS = ("demo_gallery", "demo_submit")
PARENT_WORKFLOWS = frozenset({"new-post", "share-demo"})


def _load_json(path: Path, errors: list[str], label: str):
    if not path.exists():
        errors.append(f"missing {label}: {path}")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {label}: {exc}")
        return None


def _safe_repo_path(root: Path, relative: str):
    if not isinstance(relative, str) or not relative:
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


def _inventory(root: Path) -> dict[str, set[str]]:
    tools = {path.stem for path in (root / "tools").glob("*.py")}
    for name in PUBLIC_SCRIPT_TOOLS:
        if (root / "scripts" / f"{name}.py").is_file():
            tools.add(name)
    return {
        "skills": {path.parent.name for path in (root / "skills").glob("*/SKILL.md")},
        "agents": {path.stem for path in (root / "agents").glob("*.md")},
        "tools": tools,
    }


def _skill_reachable_from(claim: str, skill: str, routes: dict, conditions: dict, graph_agents: dict) -> bool:
    kind, sep, name = claim.partition(":")
    if not sep:
        return False
    if kind == "route":
        route = routes.get(name, {})
        return skill in route.get("skills", []) or route.get("workflow") == skill
    if kind == "condition":
        return skill in conditions.get(name, {}).get("adds_skills", [])
    if kind == "agent":
        return skill in graph_agents.get(name, {}).get("required_skills", [])
    return False


def _agent_reachable_from(claim: str, agent: str, routes: dict, conditions: dict, sequence: list, conditional_edges: dict) -> bool:
    kind, sep, name = claim.partition(":")
    if not sep:
        return False
    if kind == "workflow" and name == "new-post":
        return agent in sequence
    if kind == "route":
        return agent in routes.get(name, {}).get("agents", [])
    if kind == "condition":
        return agent in conditions.get(name, {}).get("adds_agents", [])
    if kind == "conditional":
        return conditional_edges.get(name, {}).get("agent") == agent
    return False


def _validate_tool_references(root: Path, tool: str, contract: dict, errors: list[str]):
    filename = Path(contract.get("path", "")).name
    references = contract.get("reachable_from", [])
    evidence_found = False
    for relative in references:
        if relative == "helper/modules.json":
            errors.append(f"active tool {tool} cannot use helper/modules.json as executable guidance")
            continue
        target = _safe_repo_path(root, relative)
        if target is None:
            errors.append(f"active tool {tool} has unsafe executable guidance path: {relative}")
            continue
        if not target.is_file():
            errors.append(f"active tool {tool} has invalid executable guidance target: {relative}")
            continue
        try:
            text = target.read_text()
        except UnicodeDecodeError:
            errors.append(f"active tool {tool} guidance target is not readable text: {relative}")
            continue
        if filename and filename in text:
            evidence_found = True
        else:
            errors.append(f"active tool {tool} is not referenced by declared executable guidance: {relative}")
    if not evidence_found:
        errors.append(f"active tool {tool} is not referenced by executable guidance")


def _parent_participants(routes: dict) -> set[str]:
    routed_workflows = {route.get("workflow") for route in routes.values()}
    return {
        f"parent:{workflow}"
        for workflow in PARENT_WORKFLOWS
        if workflow in routed_workflows
    }


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
            path = _safe_repo_path(root, relative)
            if relative and path is None:
                errors.append(f"unsafe module path for {module_type}:{name}: {relative}")
            elif path is not None and not path.exists():
                errors.append(f"{module_type}:{name} path does not exist: {relative}")
            if path is not None and path.exists():
                text = path.read_text()
                if len(text.strip()) < 80:
                    errors.append(f"{module_type}:{name} is too small to be a real active module")
                lowered = text.lower()
                if "todo: implement" in lowered or "placeholder module" in lowered:
                    errors.append(f"{module_type}:{name} is a placeholder module")
            for test_path in contract.get("tests", []):
                test = _safe_repo_path(root, test_path)
                if test is None:
                    errors.append(f"unsafe test path for {module_type}:{name}: {test_path}")
                elif not test.exists():
                    errors.append(f"{module_type}:{name} test contract missing: {test_path}")

    routes = router_doc.get("routes", {})
    conditions = router_doc.get("conditions", {})
    graph_agents = graph_doc.get("agents", {})
    workflow = graph_doc.get("workflows", {}).get("new-post", {})
    sequence = workflow.get("sequence", [])
    conditional_edges = workflow.get("conditional", {})

    routed_workflows = {route.get("workflow") for route in routes.values()}
    missing_parent_workflows = sorted(PARENT_WORKFLOWS - routed_workflows)
    if missing_parent_workflows:
        errors.append(f"missing explicit parent workflows: {', '.join(missing_parent_workflows)}")

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

    for skill, contract in manifest.get("skills", {}).items():
        claims = contract.get("reachable_from", [])
        if not any(_skill_reachable_from(claim, skill, routes, conditions, graph_agents) for claim in claims):
            errors.append(f"active skill {skill} has no truthful reachable_from claim")
        for claim in claims:
            if not _skill_reachable_from(claim, skill, routes, conditions, graph_agents):
                errors.append(f"active skill {skill} has false reachable_from claim: {claim}")

    for agent, contract in manifest.get("agents", {}).items():
        claims = contract.get("reachable_from", [])
        if not any(_agent_reachable_from(claim, agent, routes, conditions, sequence, conditional_edges) for claim in claims):
            errors.append(f"active agent {agent} has no truthful reachable_from claim")
        for claim in claims:
            if not _agent_reachable_from(claim, agent, routes, conditions, sequence, conditional_edges):
                errors.append(f"active agent {agent} has false reachable_from claim: {claim}")

    for tool, contract in manifest.get("tools", {}).items():
        _validate_tool_references(root, tool, contract, errors)

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

    participants = manifest_agent_names | _parent_participants(routes)
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
            implementation = _safe_repo_path(root, relative)
            if implementation is None:
                errors.append(f"research gate {gate_id} has unsafe implementation ref: {relative}")
            elif not implementation.exists():
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
    parser = argparse.ArgumentParser(description="Strictly validate that every public ecosystem module is real, reachable, tested, and cross-linked")
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
