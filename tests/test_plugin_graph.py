import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "plugin_graph.py"
GRAPH = ROOT / "architecture" / "plugin-graph.json"


def load_module():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("plugin_graph", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PluginGraphTests(unittest.TestCase):
    def test_graph_contract_files_exist(self):
        self.assertTrue(SCRIPT.exists(), "missing scripts/plugin_graph.py")
        self.assertTrue(GRAPH.exists(), "missing architecture/plugin-graph.json")

    def test_graph_validator_reports_no_errors(self):
        module = load_module()
        self.assertIsNotNone(module)
        self.assertEqual([], module.validate_component_graph(ROOT))

    def test_shipping_agents_are_reachable(self):
        graph = json.loads(GRAPH.read_text())
        sequence = graph["workflows"]["new-post"]["sequence"]
        required = {
            "story-architect", "palette-curator", "copy-compressor", "layout-composer",
            "caption-writer", "artboard-builder", "render-qa", "post-critic", "story-verifier",
        }
        self.assertTrue(required.issubset(sequence))

    def test_knowledge_workers_preload_required_skills(self):
        graph = json.loads(GRAPH.read_text())
        for agent, contract in graph["agents"].items():
            required = set(contract.get("required_skills", []))
            if not required:
                continue
            text = (ROOT / "agents" / f"{agent}.md").read_text()
            for skill in required:
                self.assertIn(f"  - {skill}", text, f"{agent} does not preload {skill}")

    def test_capability_families_have_shipping_owners(self):
        graph = json.loads(GRAPH.read_text())
        expected = {"anti-slop", "design-taste", "structural-fingerprint", "evidence", "verification-loop"}
        self.assertEqual(expected, set(graph["capabilities"]))
        shipping = set(graph["workflows"]["new-post"]["sequence"])
        for capability, owners in graph["capabilities"].items():
            self.assertTrue(shipping.intersection(owners), f"{capability} has no shipping owner")


class WorkerCoordinationTests(unittest.TestCase):
    def test_planning_workers_return_to_parent_orchestrator(self):
        for name in ("story-architect", "layout-composer", "motion-director"):
            text = (ROOT / "agents" / f"{name}.md").read_text()
            self.assertIn("parent workflow", text.lower(), name)
            self.assertNotIn("Handoff the approved brief to", text, name)


if __name__ == "__main__":
    unittest.main()
