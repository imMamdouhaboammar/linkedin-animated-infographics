#!/usr/bin/env python3
import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER_FILES = ("router.json", "capabilities.json", "artifacts.json", "quality-gates.json")
REQUIRED_CONDITIONS = frozenset({"arabic", "ui_mockup", "visual_reference", "official_mascot"})
PARENT_WORKFLOWS = frozenset({"new-post", "share-demo"})
CONDITION_SCHEMA = {
    "arabic": {"adds_skills": list},
    "ui_mockup": {"adds_capabilities": list, "adds_agents": list},
    "visual_reference": {"adds_agents": list, "adds_capabilities": list},
    "official_mascot": {
        "asset_gate": str,
        "adds_skills": list,
        "adds_agents": list,
        "adds_capabilities": list,
    },
}


def _load_json(path: Path, errors=None):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        if errors is not None:
            try:
                display = path.relative_to(ROOT)
            except ValueError:
                display = path
            errors.append(f"missing {display}")
    except json.JSONDecodeError as exc:
        if errors is not None:
            errors.append(f"invalid JSON in {path}: {exc}")
    return None


def _resolve_asset_path(root: Path, value):
    if not value or not isinstance(value, (str, Path)):
        return None
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def _is_svg_file(path: Path | None) -> bool:
    return bool(path and path.is_file() and path.suffix.lower() == ".svg")


def _validate_required_conditions(router: dict) -> list[str]:
    errors = []
    conditions = router.get("conditions", {})
    if not isinstance(conditions, dict):
        return ["router conditions must be an object"]

    for condition_id in sorted(REQUIRED_CONDITIONS - set(conditions)):
        errors.append(f"router missing required condition {condition_id}")

    for condition_id, required_fields in CONDITION_SCHEMA.items():
        if condition_id not in conditions:
            continue
        contract = conditions[condition_id]
        if not isinstance(contract, dict):
            errors.append(f"condition {condition_id} must be an object")
            continue
        for field, expected_type in required_fields.items():
            value = contract.get(field)
            invalid = not isinstance(value, expected_type)
            if expected_type is str and isinstance(value, str) and not value.strip():
                invalid = True
            if invalid:
                errors.append(
                    f"condition {condition_id} required field {field} must be {expected_type.__name__}"
                )
    return errors


def load_ecosystem(root: Path = ROOT) -> dict:
    helper = root / "helper"
    research = root / "research" / "capability-notes"
    return {
        "router": json.loads((helper / "router.json").read_text()),
        "capabilities": json.loads((helper / "capabilities.json").read_text()),
        "artifacts": json.loads((helper / "artifacts.json").read_text()),
        "quality_gates": json.loads((helper / "quality-gates.json").read_text()),
        "research_gates": json.loads((research / "gates.json").read_text()),
    }


def _dedupe(values):
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _parent_participants(routes: dict) -> set[str]:
    routed_workflows = {route.get("workflow") for route in routes.values()}
    return {
        f"parent:{workflow}"
        for workflow in PARENT_WORKFLOWS
        if workflow in routed_workflows
    }


def validate_ecosystem(root: Path = ROOT) -> list[str]:
    errors = []
    helper = root / "helper"
    for relative in ("README.md", "GUIDE.md", *HELPER_FILES):
        if not (helper / relative).exists():
            errors.append(f"missing helper/{relative}")

    router = _load_json(helper / "router.json", errors)
    capabilities_doc = _load_json(helper / "capabilities.json", errors)
    artifacts_doc = _load_json(helper / "artifacts.json", errors)
    quality_gates_doc = _load_json(helper / "quality-gates.json", errors)
    research_gates_doc = _load_json(root / "research" / "capability-notes" / "gates.json", errors)
    if not router or not capabilities_doc or not artifacts_doc or not quality_gates_doc or not research_gates_doc:
        return errors

    errors.extend(_validate_required_conditions(router))

    skills = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    agents = {path.stem for path in (root / "agents").glob("*.md")}
    capabilities = capabilities_doc.get("capabilities", {})
    quality_gates = quality_gates_doc.get("gates", {})
    research_gates = research_gates_doc.get("gates", {})

    routes = router.get("routes", {})
    if router.get("default_intent") not in routes:
        errors.append("router default_intent does not resolve to a route")

    routed_workflows = {route.get("workflow") for route in routes.values()}
    missing_parent_workflows = sorted(PARENT_WORKFLOWS - routed_workflows)
    if missing_parent_workflows:
        errors.append(f"router missing explicit parent workflows: {', '.join(missing_parent_workflows)}")

    conditions = router.get("conditions", {})
    if not isinstance(conditions, dict):
        conditions = {}

    for intent, route in routes.items():
        workflow = route.get("workflow")
        if workflow != "focused" and workflow not in skills:
            errors.append(f"route {intent} references missing workflow skill {workflow}")
        for skill in route.get("skills", []):
            if skill not in skills:
                errors.append(f"route {intent} references missing skill {skill}")
        for agent in route.get("agents", []):
            if agent not in agents:
                errors.append(f"route {intent} references missing agent {agent}")
        for capability in route.get("capabilities", []):
            if capability not in capabilities:
                errors.append(f"route {intent} references missing capability {capability}")

    for condition, contract in conditions.items():
        if not isinstance(contract, dict):
            continue
        for skill in contract.get("adds_skills", []):
            if skill not in skills:
                errors.append(f"condition {condition} references missing skill {skill}")
        for agent in contract.get("adds_agents", []):
            if agent not in agents:
                errors.append(f"condition {condition} references missing agent {agent}")
        for capability in contract.get("adds_capabilities", []):
            if capability not in capabilities:
                errors.append(f"condition {condition} references missing capability {capability}")

    referenced_research_gates = set()
    for capability, contract in capabilities.items():
        owners = contract.get("owners", [])
        if not owners:
            errors.append(f"capability {capability} has no owners")
        unknown = sorted(set(owners) - agents)
        if unknown:
            errors.append(f"capability {capability} has unknown owners: {', '.join(unknown)}")
        gate_ids = contract.get("research_gates", [])
        local_native = contract.get("local_native") is True
        if not gate_ids and not local_native:
            errors.append(f"capability {capability} has neither research_gates nor local_native")
        if gate_ids and local_native:
            errors.append(f"capability {capability} cannot be both research-derived and local_native")
        unknown_gates = sorted(set(gate_ids) - set(research_gates))
        if unknown_gates:
            errors.append(f"capability {capability} references unknown research gates: {', '.join(unknown_gates)}")
        referenced_research_gates.update(gate_ids)

    unreferenced = sorted(set(research_gates) - referenced_research_gates)
    if unreferenced:
        errors.append(f"research gates not connected to helper capabilities: {', '.join(unreferenced)}")

    for gate_id, gate in quality_gates.items():
        if gate.get("severity") not in {"blocking", "advisory"}:
            errors.append(f"quality gate {gate_id} has invalid severity")
        owners = set(gate.get("owners", []))
        if not owners:
            errors.append(f"quality gate {gate_id} has no owners")
        unknown = sorted(owners - agents)
        if unknown:
            errors.append(f"quality gate {gate_id} has unknown owners: {', '.join(unknown)}")
        if not gate.get("applies_to_intents"):
            errors.append(f"quality gate {gate_id} has no applies_to_intents")
        unknown_intents = sorted(set(gate.get("applies_to_intents", [])) - set(routes))
        if unknown_intents:
            errors.append(f"quality gate {gate_id} references unknown intents: {', '.join(unknown_intents)}")
        if not gate.get("behavior"):
            errors.append(f"quality gate {gate_id} has no behavior")

    allowed_participants = agents | _parent_participants(routes)
    for artifact, contract in artifacts_doc.get("artifacts", {}).items():
        producer = contract.get("producer")
        if producer not in allowed_participants:
            errors.append(f"artifact {artifact} has unknown producer {producer}")
        for consumer in contract.get("consumers", []):
            if consumer not in allowed_participants:
                errors.append(f"artifact {artifact} has unknown consumer {consumer}")

    graph_path = root / "architecture" / "plugin-graph.json"
    if graph_path.exists():
        graph = _load_json(graph_path, errors) or {}
        graph_caps = set(graph.get("capabilities", {}))
        helper_caps = set(capabilities)
        if graph_caps != helper_caps:
            missing = sorted(helper_caps - graph_caps)
            extra = sorted(graph_caps - helper_caps)
            if missing:
                errors.append(f"plugin graph missing helper capabilities: {', '.join(missing)}")
            if extra:
                errors.append(f"helper registry missing graph capabilities: {', '.join(extra)}")
    return errors


def _infer_intent(request: dict, router: dict) -> str:
    explicit = (request.get("intent") or "").strip().lower()
    aliases = {
        "create": "create-post",
        "create-post": "create-post",
        "post": "create-post",
        "qa": "qa",
        "review": "qa",
        "render": "render",
        "render-gif": "render",
        "design-study": "design-study",
        "study": "design-study",
        "mascot": "mascot-animation",
        "mascot-animation": "mascot-animation",
        "info-story": "info-story",
        "info-stories": "info-story",
        "share": "share-demo",
        "share-demo": "share-demo",
        "publish-demo": "share-demo",
        "community-demo": "share-demo",
    }
    if explicit in aliases:
        return aliases[explicit]

    text = (request.get("request") or "").lower()
    if any(token in text for token in ("share this demo", "publish this demo", "submit this demo", "community gallery")):
        return "share-demo"
    if any(token in text for token in ("qa this", "review this", "audit this", "check this finished")):
        return "qa"
    if "render" in text and any(token in text for token in ("html", "gif", "artboard")):
        return "render"
    if "design study" in text or "study this reference" in text:
        return "design-study"
    if "animate" in text and "mascot" in text and not any(token in text for token in ("post", "infographic")):
        return "mascot-animation"
    if "info-story" in text or "info story" in text:
        return "info-story"
    return router.get("default_intent", "create-post")


def _research_gates_for(capability_ids, intent: str, request: dict, ecosystem: dict) -> list[str]:
    capabilities = ecosystem["capabilities"].get("capabilities", {})
    gates = ecosystem["research_gates"].get("gates", {})
    candidates = []
    for capability_id in capability_ids:
        candidates.extend(capabilities.get(capability_id, {}).get("research_gates", []))
    result = []
    for gate_id in _dedupe(candidates):
        gate = gates.get(gate_id, {})
        intents = gate.get("applies_to_intents", [])
        if intents and intent not in intents:
            continue
        requirement = gate.get("requires")
        if requirement and not request.get(requirement):
            continue
        result.append(gate_id)
    return result


def _quality_gates_for(intent: str, ecosystem: dict) -> list[str]:
    gates = ecosystem["quality_gates"].get("gates", {})
    return [gate_id for gate_id, gate in gates.items() if intent in gate.get("applies_to_intents", [])]


def _finalize_route(result: dict, request: dict, ecosystem: dict) -> dict:
    for key in ("skills", "agents", "conditional_agents", "capabilities", "asset_gates"):
        result[key] = _dedupe(result[key])
    result["research_gates"] = _research_gates_for(result["capabilities"], result["intent"], request, ecosystem)
    result["quality_gates"] = _quality_gates_for(result["intent"], ecosystem)
    return result


def route_request(request: dict, root: Path = ROOT) -> dict:
    ecosystem = load_ecosystem(root)
    router = ecosystem["router"]
    intent = _infer_intent(request, router)
    if intent not in router["routes"]:
        raise ValueError(f"unknown routing intent: {intent}")

    condition_errors = _validate_required_conditions(router)
    if condition_errors:
        raise ValueError("invalid router conditions: " + "; ".join(condition_errors))
    conditions = router["conditions"]

    base = copy.deepcopy(router["routes"][intent])
    result = {
        "status": "READY",
        "reason": None,
        "intent": intent,
        "workflow": base["workflow"],
        "skills": list(base.get("skills", [])),
        "agents": list(base.get("agents", [])),
        "conditional_agents": [],
        "capabilities": list(base.get("capabilities", [])),
        "asset_gates": [],
        "research_gates": [],
        "quality_gates": [],
    }

    language = (request.get("language") or "").lower()
    if language in ("ar", "arabic") or request.get("rtl") is True:
        result["skills"].extend(conditions["arabic"]["adds_skills"])

    if request.get("ui_mockup") is True:
        condition = conditions["ui_mockup"]
        result["capabilities"].extend(condition.get("adds_capabilities", []))
        result["agents"].extend(condition.get("adds_agents", []))

    if request.get("visual_reference") is True:
        condition = conditions["visual_reference"]
        result["agents"].extend(condition.get("adds_agents", []))
        result["capabilities"].extend(condition.get("adds_capabilities", []))

    mascot = request.get("mascot") or {}
    svg_asset = _resolve_asset_path(root, mascot.get("svg_path"))
    has_exact_svg = _is_svg_file(svg_asset)
    official_mascot = bool(mascot.get("official") or mascot.get("name"))
    if official_mascot:
        condition = conditions["official_mascot"]
        result["asset_gates"].append(condition["asset_gate"])
        result["capabilities"].extend(condition.get("adds_capabilities", []))
        if not has_exact_svg:
            result["status"] = "HOLD"
            result["reason"] = "exact SVG required for named or official mascot"
            return _finalize_route(result, request, ecosystem)
        result["skills"].extend(condition.get("adds_skills", []))
        result["conditional_agents"].extend(condition.get("adds_agents", []))

    if intent == "mascot-animation" and not has_exact_svg:
        result["status"] = "HOLD"
        result["reason"] = "exact SVG required for mascot animation"
        result["asset_gates"].append("exact-svg")
        return _finalize_route(result, request, ecosystem)

    if (request.get("output") or "").lower() in ("static", "png", "still"):
        result["agents"] = [agent for agent in result["agents"] if agent not in ("motion-director", "motion-engineer")]
        result["skills"] = [skill for skill in result["skills"] if skill != "motion"]

    return _finalize_route(result, request, ecosystem)


def explain_route(route: dict) -> str:
    lines = [
        f"status: {route['status']}",
        f"intent: {route['intent']}",
        f"workflow: {route['workflow']}",
        f"skills: {', '.join(route['skills']) or 'none'}",
        f"agents: {', '.join(route['agents']) or 'none'}",
        f"conditional agents: {', '.join(route['conditional_agents']) or 'none'}",
        f"capabilities: {', '.join(route['capabilities']) or 'none'}",
        f"research gates: {', '.join(route['research_gates']) or 'none'}",
        f"quality gates: {', '.join(route['quality_gates']) or 'none'}",
        f"asset gates: {', '.join(route['asset_gates']) or 'none'}",
    ]
    if route.get("reason"):
        lines.append(f"reason: {route['reason']}")
    return "\n".join(lines)


def _request_from_args(args):
    mascot = {}
    if getattr(args, "mascot_name", None):
        mascot["name"] = args.mascot_name
    if getattr(args, "official_mascot", False):
        mascot["official"] = True
    if getattr(args, "svg_path", None):
        mascot["svg_path"] = args.svg_path
    request = {
        "request": getattr(args, "request", ""),
        "intent": getattr(args, "intent", None),
        "language": getattr(args, "language", None),
        "output": getattr(args, "output", None),
        "ui_mockup": getattr(args, "ui_mockup", False),
        "visual_reference": getattr(args, "visual_reference", False),
    }
    if mascot:
        request["mascot"] = mascot
    return request


def _add_route_args(parser):
    parser.add_argument("--request", required=True)
    parser.add_argument("--intent")
    parser.add_argument("--language")
    parser.add_argument("--output")
    parser.add_argument("--ui-mockup", action="store_true")
    parser.add_argument("--visual-reference", action="store_true")
    parser.add_argument("--mascot-name")
    parser.add_argument("--official-mascot", action="store_true")
    parser.add_argument("--svg-path")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Route and validate the LinkedIn infographic ecosystem")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    route_parser = sub.add_parser("route")
    explain_parser = sub.add_parser("explain")
    _add_route_args(route_parser)
    _add_route_args(explain_parser)
    args = parser.parse_args(argv)

    if args.command == "check":
        errors = validate_ecosystem(ROOT)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("Ecosystem helper: OK")
        return 0

    route = route_request(_request_from_args(args), ROOT)
    if args.command == "route":
        print(json.dumps(route, indent=2, ensure_ascii=False))
    else:
        print(explain_route(route))
    return 2 if route["status"] == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
