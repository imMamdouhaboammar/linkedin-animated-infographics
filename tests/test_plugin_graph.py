import importlib.util
import json
import shutil
import tempfile
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


def copy_graph_fixture(destination: Path):
    for relative in ("architecture", "agents", "skills", "helper"):
        shutil.copytree(ROOT / relative, destination / relative)


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
            "asset-curator", "creative-director", "story-architect", "palette-curator",
            "type-curator", "copy-compressor", "layout-composer", "caption-writer",
            "artboard-builder", "render-qa", "post-critic", "story-verifier",
        }
        self.assertTrue(required.issubset(sequence))

    def test_asset_and_creative_order_is_explicit(self):
        sequence = json.loads(GRAPH.read_text())["workflows"]["new-post"]["sequence"]
        self.assertLess(sequence.index("evidence-checker"), sequence.index("asset-curator"))
        self.assertLess(sequence.index("asset-curator"), sequence.index("creative-director"))
        self.assertLess(sequence.index("creative-director"), sequence.index("story-architect"))

    def test_type_direction_runs_before_copy(self):
        sequence = json.loads(GRAPH.read_text())["workflows"]["new-post"]["sequence"]
        self.assertLess(sequence.index("palette-curator"), sequence.index("type-curator"))
        self.assertLess(sequence.index("type-curator"), sequence.index("copy-compressor"))

    def test_conditional_mascot_edge_is_explicit(self):
        edge = json.loads(GRAPH.read_text())["workflows"]["new-post"]["conditional"]["mascot"]
        self.assertEqual("mascot-animator", edge["agent"])
        self.assertEqual("verified-identity", edge["asset_gate"])
        self.assertEqual("artboard-builder", edge["after"])
        self.assertEqual("motion-engineer", edge["before"])

    def test_design_study_stage_condition_precedes_evidence(self):
        workflow = json.loads(GRAPH.read_text())["workflows"]["new-post"]
        condition = workflow["stage_conditions"]["design-study"]
        self.assertEqual(
            {
                "condition": "visual_reference",
                "before": "evidence-checker",
                "on_absent": "SKIP",
                "on_missing": "HOLD",
            },
            condition,
        )

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
        expected = {
            "anti-slop", "creative-direction", "design-taste", "evidence", "hook-design-copy",
            "mascot-identity", "structural-fingerprint", "ui-mockup-fidelity", "verification-loop",
            "visual-asset-sourcing", "typography-direction",
        }
        self.assertEqual(expected, set(graph["capabilities"]))
        workflow = graph["workflows"]["new-post"]
        shipping = set(workflow["sequence"]) | {edge["agent"] for edge in workflow.get("conditional", {}).values()}
        for capability, owners in graph["capabilities"].items():
            self.assertTrue(shipping.intersection(owners), f"{capability} has no shipping owner")

    def test_new_post_executes_graph_order(self):
        text = (ROOT / "skills" / "new-post" / "SKILL.md").read_text()
        sequence = json.loads(GRAPH.read_text())["workflows"]["new-post"]["sequence"]
        positions = []
        for agent in sequence:
            self.assertIn(agent, text, f"new-post never invokes {agent}")
            positions.append(text.index(agent))
        self.assertEqual(sorted(positions), positions)

    def test_qa_post_runs_adversarial_and_independent_review(self):
        text = (ROOT / "skills" / "qa-post" / "SKILL.md").read_text()
        self.assertIn("post-critic", text)
        self.assertIn("story-verifier", text)

    def test_validator_detects_helper_capability_owner_drift(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_graph_fixture(root)
            capabilities_path = root / "helper" / "capabilities.json"
            capabilities = json.loads(capabilities_path.read_text())
            capabilities["capabilities"]["anti-slop"]["owners"] = ["story-verifier"]
            capabilities_path.write_text(json.dumps(capabilities))
            errors = module.validate_component_graph(root)
            self.assertTrue(any("helper capability anti-slop" in error.lower() for error in errors), errors)

    def test_validator_detects_helper_workflow_order_drift(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_graph_fixture(root)
            router_path = root / "helper" / "router.json"
            router = json.loads(router_path.read_text())
            agents = router["routes"]["create-post"]["agents"]
            router["routes"]["create-post"]["agents"] = list(reversed(agents))
            router_path.write_text(json.dumps(router))
            errors = module.validate_component_graph(root)
            self.assertTrue(any("helper create-post agent order" in error.lower() for error in errors), errors)


class WorkerCoordinationTests(unittest.TestCase):
    def test_planning_workers_return_to_parent_orchestrator(self):
        for name in ("asset-curator", "creative-director", "story-architect", "type-curator", "layout-composer", "motion-director"):
            text = (ROOT / "agents" / f"{name}.md").read_text()
            self.assertIn("parent workflow", text.lower(), name)
            self.assertNotIn("Handoff the approved brief to", text, name)


if __name__ == "__main__":
    unittest.main()
