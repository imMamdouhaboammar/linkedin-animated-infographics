import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUALITY = ROOT / "helper" / "quality-gates.json"
ROUTER = ROOT / "helper" / "router.json"
CAPABILITIES = ROOT / "helper" / "capabilities.json"
ARTIFACTS = ROOT / "helper" / "artifacts.json"
GRAPH = ROOT / "architecture" / "plugin-graph.json"
CREATIVE_AGENT = ROOT / "agents" / "creative-director.md"
HOOK_DOC = ROOT / "skills" / "info-stories" / "references" / "hook-driven-design-copy.md"

EXPECTED_QUALITY_GATES = {
    "reference-evidence-readiness",
    "hooked-design-copy",
    "creative-payoff",
    "restrained-palette",
    "center-first-composition",
}


class CreativeRuntimeTests(unittest.TestCase):
    def test_local_quality_gate_registry_exists(self):
        self.assertTrue(QUALITY.exists(), "missing helper/quality-gates.json")
        gates = json.loads(QUALITY.read_text())["gates"]
        self.assertEqual(EXPECTED_QUALITY_GATES, set(gates))

    def test_local_quality_gates_have_runtime_contracts(self):
        self.assertTrue(QUALITY.exists())
        failures = []
        for gate_id, gate in json.loads(QUALITY.read_text())["gates"].items():
            for field in ("stage", "severity", "owners", "behavior", "applies_to_intents"):
                if gate.get(field) in (None, "", []):
                    failures.append(f"{gate_id}: missing {field}")
            if gate.get("severity") not in ("blocking", "advisory"):
                failures.append(f"{gate_id}: invalid severity")
        self.assertEqual([], failures)

    def test_creative_director_is_a_real_shipping_agent(self):
        self.assertTrue(CREATIVE_AGENT.exists(), "missing agents/creative-director.md")
        graph = json.loads(GRAPH.read_text())
        self.assertIn("creative-director", graph["agents"])
        sequence = graph["workflows"]["new-post"]["sequence"]
        self.assertLess(sequence.index("evidence-checker"), sequence.index("creative-director"))
        self.assertLess(sequence.index("creative-director"), sequence.index("story-architect"))

    def test_create_route_includes_creative_director_and_quality_gates(self):
        router = json.loads(ROUTER.read_text())
        route = router["routes"]["create-post"]
        self.assertIn("creative-director", route["agents"])
        self.assertIn("creative-direction", route["capabilities"])
        self.assertIn("hook-design-copy", route["capabilities"])

    def test_info_story_route_keeps_creative_concepting_available(self):
        router = json.loads(ROUTER.read_text())
        route = router["routes"]["info-story"]
        self.assertIn("creative-director", route["agents"])
        self.assertIn("creative-direction", route["capabilities"])

    def test_creative_capabilities_are_local_native_and_owned(self):
        capabilities = json.loads(CAPABILITIES.read_text())["capabilities"]
        for capability in ("creative-direction", "hook-design-copy"):
            contract = capabilities[capability]
            self.assertTrue(contract.get("local_native"), capability)
            self.assertIn("creative-director", contract["owners"])

    def test_creative_concepts_artifact_is_declared(self):
        artifacts = json.loads(ARTIFACTS.read_text())["artifacts"]
        contract = artifacts["build/creative-concepts.json"]
        self.assertEqual("creative-director", contract["producer"])
        for consumer in ("story-architect", "copy-compressor", "layout-composer", "motion-director"):
            self.assertIn(consumer, contract["consumers"])
        for field in (
            "concept_name", "visual_hook", "copy_hook", "aha_mechanic", "story_shape",
            "recommended_visual_style", "recommended_story_archetype",
            "recommended_motion_behavior", "evidence_dependencies", "risk_notes",
            "why_it_earns_attention",
        ):
            self.assertIn(field, contract["required_fields"])

    def test_creative_agent_requires_three_directions_and_evidence_safety(self):
        self.assertTrue(CREATIVE_AGENT.exists())
        text = CREATIVE_AGENT.read_text().lower()
        self.assertRegex(text, r"at least\s+three|minimum\s+three")
        for needle in ("visual hook", "copy hook", "aha", "evidence", "parent workflow", "do not invent"):
            self.assertIn(needle, text)

    def test_hook_driven_design_copy_reference_exists(self):
        self.assertTrue(HOOK_DOC.exists())
        text = HOOK_DOC.read_text().lower()
        for needle in ("hero headline", "specificity", "portable", "do not invent", "literal labels"):
            self.assertIn(needle, text)

    def test_hook_gate_is_wired_into_copy_owners(self):
        for agent in ("creative-director", "copy-compressor", "caption-writer", "post-critic"):
            text = (ROOT / "agents" / f"{agent}.md").read_text().lower()
            self.assertIn("hooked-design-copy", text, agent)

    def test_creative_payoff_is_not_spectacle(self):
        self.assertTrue(QUALITY.exists())
        behavior = json.loads(QUALITY.read_text())["gates"]["creative-payoff"]["behavior"].lower()
        for needle in ("useful visual payoff", "not spectacle", "reveal", "relationship"):
            self.assertIn(needle, behavior)

    def test_complete_route_exposes_local_quality_gates(self):
        script = (ROOT / "scripts" / "ecosystem_router.py").read_text()
        self.assertIn('"quality_gates"', script)


if __name__ == "__main__":
    unittest.main()
