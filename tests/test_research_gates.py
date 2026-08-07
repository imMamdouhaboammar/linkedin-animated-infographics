import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "research" / "capability-notes" / "gates.json"
SOURCES = ROOT / "research" / "capability-notes" / "sources.json"
SCRIPT = ROOT / "scripts" / "research_gates.py"
CAPABILITIES = ROOT / "helper" / "capabilities.json"
ROUTER_SCRIPT = ROOT / "scripts" / "ecosystem_router.py"

EXPECTED_GATES = {
    "prose-specificity",
    "voice-preservation",
    "design-dials",
    "structural-originality",
    "reference-dna",
    "contrast-discipline",
    "evidence-traceability",
    "bounded-verification",
}


def load_module(path: Path, name: str):
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ResearchGateTests(unittest.TestCase):
    def test_gate_registry_and_validator_exist(self):
        self.assertTrue(GATES.exists(), "missing research/capability-notes/gates.json")
        self.assertTrue(SCRIPT.exists(), "missing scripts/research_gates.py")

    def test_expected_research_gates_are_first_class(self):
        self.assertTrue(GATES.exists())
        gates = json.loads(GATES.read_text())["gates"]
        self.assertEqual(EXPECTED_GATES, set(gates))

    def test_each_gate_has_complete_runtime_contract(self):
        self.assertTrue(GATES.exists())
        gates = json.loads(GATES.read_text())["gates"]
        failures = []
        for gate_id, gate in gates.items():
            for field in ("sources", "stage", "severity", "owners", "local_behavior", "implementation_refs"):
                value = gate.get(field)
                if value in (None, "", []):
                    failures.append(f"{gate_id}: missing {field}")
            if gate.get("severity") not in ("blocking", "advisory"):
                failures.append(f"{gate_id}: invalid severity")
        self.assertEqual([], failures)

    def test_gate_sources_exist_in_provenance_snapshot(self):
        self.assertTrue(GATES.exists())
        source_names = {item["name"] for item in json.loads(SOURCES.read_text())["sources"]}
        failures = []
        for gate_id, gate in json.loads(GATES.read_text())["gates"].items():
            missing = sorted(set(gate["sources"]) - source_names)
            if missing:
                failures.append(f"{gate_id}: unknown sources {missing}")
        self.assertEqual([], failures)

    def test_gate_implementation_refs_exist(self):
        self.assertTrue(GATES.exists())
        failures = []
        for gate_id, gate in json.loads(GATES.read_text())["gates"].items():
            for relative in gate["implementation_refs"]:
                if not (ROOT / relative).exists():
                    failures.append(f"{gate_id}: missing {relative}")
        self.assertEqual([], failures)

    def test_gate_owners_are_real_shipping_agents(self):
        self.assertTrue(GATES.exists())
        graph = json.loads((ROOT / "architecture" / "plugin-graph.json").read_text())
        agents = set(graph["agents"])
        workflow = graph["workflows"]["new-post"]
        shipping = set(workflow["sequence"]) | {
            edge["agent"] for edge in workflow.get("conditional", {}).values()
        }
        failures = []
        for gate_id, gate in json.loads(GATES.read_text())["gates"].items():
            owners = set(gate["owners"])
            unknown = sorted(owners - agents)
            if unknown:
                failures.append(f"{gate_id}: unknown owners {unknown}")
            if not owners & shipping:
                failures.append(f"{gate_id}: no shipping owner")
        self.assertEqual([], failures)

    def test_helper_capabilities_reference_known_research_gates(self):
        self.assertTrue(GATES.exists())
        known = set(json.loads(GATES.read_text())["gates"])
        capabilities = json.loads(CAPABILITIES.read_text())["capabilities"]
        failures = []
        referenced = set()
        for capability, contract in capabilities.items():
            gates = contract.get("research_gates", [])
            if not gates:
                failures.append(f"{capability}: no research_gates")
            unknown = sorted(set(gates) - known)
            if unknown:
                failures.append(f"{capability}: unknown gates {unknown}")
            referenced.update(gates)
        self.assertEqual([], failures)
        self.assertEqual(EXPECTED_GATES, referenced)

    def test_validator_reports_no_errors(self):
        module = load_module(SCRIPT, "research_gates")
        self.assertIsNotNone(module, "research gate validator missing")
        self.assertEqual([], module.validate_research_gates(ROOT))

    def test_router_returns_research_gates_for_create_route(self):
        module = load_module(ROUTER_SCRIPT, "ecosystem_router")
        route = module.route_request({"request": "Create an animated LinkedIn infographic"}, ROOT)
        self.assertIn("research_gates", route)
        self.assertIn("prose-specificity", route["research_gates"])
        self.assertIn("design-dials", route["research_gates"])
        self.assertIn("evidence-traceability", route["research_gates"])
        self.assertIn("bounded-verification", route["research_gates"])

    def test_reference_route_activates_reference_dna_gate(self):
        module = load_module(ROUTER_SCRIPT, "ecosystem_router")
        route = module.route_request(
            {"request": "Study this reference and build a post", "visual_reference": True}, ROOT
        )
        self.assertIn("reference-dna", route["research_gates"])

    def test_adoption_matrix_names_runtime_gate_ids(self):
        text = (ROOT / "research" / "capability-notes" / "adoption-matrix.md").read_text()
        for gate_id in EXPECTED_GATES:
            self.assertIn(f"`{gate_id}`", text)


if __name__ == "__main__":
    unittest.main()
