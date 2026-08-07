#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_GATE_FIELDS = ("sources", "stage", "severity", "owners", "local_behavior", "implementation_refs")
VALID_SEVERITIES = {"blocking", "advisory"}


def _load(path: Path, errors: list[str], label: str):
    if not path.exists():
        errors.append(f"missing {label}: {path}")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {label}: {exc}")
        return None


def load_research_gates(root: Path = ROOT) -> dict:
    base = root / "research" / "capability-notes"
    return {
        "sources": json.loads((base / "sources.json").read_text()),
        "gates": json.loads((base / "gates.json").read_text()),
    }


def validate_research_gates(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    base = root / "research" / "capability-notes"
    sources_doc = _load(base / "sources.json", errors, "research sources")
    gates_doc = _load(base / "gates.json", errors, "research gates")
    capabilities_doc = _load(root / "helper" / "capabilities.json", errors, "helper capabilities")
    graph = _load(root / "architecture" / "plugin-graph.json", errors, "plugin graph")
    if not all((sources_doc, gates_doc, capabilities_doc, graph)):
        return errors

    source_items = sources_doc.get("sources", [])
    source_names = {item.get("name") for item in source_items if item.get("name")}
    for item in source_items:
        name = item.get("name", "<unknown>")
        commit = item.get("commit", "")
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append(f"research source {name} has invalid commit SHA")
        if item.get("license") != "MIT":
            errors.append(f"research source {name} is not recorded as MIT")
        repository = item.get("repository", "")
        if not repository.startswith("https://github.com/"):
            errors.append(f"research source {name} has invalid repository URL")

    graph_agents = set(graph.get("agents", {}))
    workflow = graph.get("workflows", {}).get("new-post", {})
    shipping_agents = set(workflow.get("sequence", [])) | {
        edge.get("agent") for edge in workflow.get("conditional", {}).values() if edge.get("agent")
    }

    gates = gates_doc.get("gates", {})
    known_gate_ids = set(gates)
    referenced_gate_ids: set[str] = set()

    for gate_id, gate in gates.items():
        for field in REQUIRED_GATE_FIELDS:
            value = gate.get(field)
            if value in (None, "", []):
                errors.append(f"research gate {gate_id} missing {field}")
        if gate.get("severity") not in VALID_SEVERITIES:
            errors.append(f"research gate {gate_id} has invalid severity {gate.get('severity')!r}")
        unknown_sources = sorted(set(gate.get("sources", [])) - source_names)
        if unknown_sources:
            errors.append(f"research gate {gate_id} references unknown sources: {', '.join(unknown_sources)}")
        owners = set(gate.get("owners", []))
        unknown_owners = sorted(owners - graph_agents)
        if unknown_owners:
            errors.append(f"research gate {gate_id} references unknown owners: {', '.join(unknown_owners)}")
        if owners and not owners.intersection(shipping_agents):
            errors.append(f"research gate {gate_id} has no owner on the shipping path")
        for relative in gate.get("implementation_refs", []):
            if not (root / relative).exists():
                errors.append(f"research gate {gate_id} implementation ref missing: {relative}")
        intents = gate.get("applies_to_intents", [])
        if not intents:
            errors.append(f"research gate {gate_id} has no applies_to_intents")

    capabilities = capabilities_doc.get("capabilities", {})
    for capability, contract in capabilities.items():
        research_gates = contract.get("research_gates", [])
        local_native = contract.get("local_native") is True
        if not research_gates and not local_native:
            errors.append(f"helper capability {capability} has neither research_gates nor local_native")
        if research_gates and local_native:
            errors.append(f"helper capability {capability} cannot be both research-derived and local_native")
        unknown = sorted(set(research_gates) - known_gate_ids)
        if unknown:
            errors.append(f"helper capability {capability} references unknown research gates: {', '.join(unknown)}")
        referenced_gate_ids.update(research_gates)

        capability_owners = set(contract.get("owners", []))
        for gate_id in research_gates:
            gate_owners = set(gates.get(gate_id, {}).get("owners", []))
            if gate_owners and capability_owners and not gate_owners.intersection(capability_owners):
                errors.append(f"helper capability {capability} has no shared owner with research gate {gate_id}")

    unreferenced = sorted(known_gate_ids - referenced_gate_ids)
    if unreferenced:
        errors.append(f"unreferenced research gates: {', '.join(unreferenced)}")
    return errors


def gates_for_capabilities(capability_ids, intent: str, request: dict, root: Path = ROOT) -> list[str]:
    data = load_research_gates(root)
    gates = data["gates"].get("gates", {})
    capabilities = json.loads((root / "helper" / "capabilities.json").read_text()).get("capabilities", {})
    gate_ids = []
    for capability_id in capability_ids:
        for gate_id in capabilities.get(capability_id, {}).get("research_gates", []):
            if gate_id not in gate_ids:
                gate_ids.append(gate_id)

    result = []
    for gate_id in gate_ids:
        gate = gates.get(gate_id, {})
        intents = gate.get("applies_to_intents", [])
        if intents and intent not in intents:
            continue
        requirement = gate.get("requires")
        if requirement and not request.get(requirement):
            continue
        result.append(gate_id)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate research-derived runtime capability gates")
    parser.add_argument("command", nargs="?", default="check", choices=("check",))
    parser.parse_args(argv)
    errors = validate_research_gates(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Research gates: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
