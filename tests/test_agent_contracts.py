import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT_ROOT = ROOT / "agents"
GRAPH = json.loads((ROOT / "architecture" / "plugin-graph.json").read_text())
ARTIFACTS = json.loads((ROOT / "helper" / "artifacts.json").read_text())["artifacts"]
RESEARCH = json.loads((ROOT / "research" / "capability-notes" / "gates.json").read_text())["gates"]
QUALITY = json.loads((ROOT / "helper" / "quality-gates.json").read_text())["gates"]

REQUIRED_SECTIONS = (
    "Role",
    "Inputs",
    "Method",
    "HOLD conditions",
    "Quality gates",
    "Research gates",
    "Outputs",
)


class AgentContractTests(unittest.TestCase):
    def test_every_agent_has_v3_worker_sections(self):
        agents = sorted(AGENT_ROOT.glob("*.md"))
        self.assertGreaterEqual(len(agents), 15)
        failures = []
        for path in agents:
            text = path.read_text()
            for section in REQUIRED_SECTIONS:
                if not re.search(rf"^## {re.escape(section)}\s*$", text, re.MULTILINE):
                    failures.append(f"{path.stem}: missing {section}")
        self.assertEqual([], failures)

    def test_every_agent_points_to_helper_and_parent_contract(self):
        failures = []
        for path in sorted(AGENT_ROOT.glob("*.md")):
            text = path.read_text().lower()
            if "helper/guide.md" not in text:
                failures.append(f"{path.stem}: missing helper")
            if "parent workflow" not in text:
                failures.append(f"{path.stem}: missing parent workflow")
        self.assertEqual([], failures)

    def test_frontmatter_name_matches_filename(self):
        failures = []
        for path in sorted(AGENT_ROOT.glob("*.md")):
            text = path.read_text()
            match = re.search(r"^name:\s*([^\n]+)$", text, re.MULTILINE)
            if not match or match.group(1).strip() != path.stem:
                failures.append(path.name)
        self.assertEqual([], failures)

    def test_graph_skill_preloads_remain_declared(self):
        failures = []
        for agent, contract in GRAPH["agents"].items():
            text = (AGENT_ROOT / f"{agent}.md").read_text()
            for skill in contract.get("required_skills", []):
                if f"  - {skill}" not in text:
                    failures.append(f"{agent}: missing preload {skill}")
        self.assertEqual([], failures)

    def test_research_gate_owners_name_the_gate(self):
        failures = []
        for gate_id, gate in RESEARCH.items():
            for owner in gate["owners"]:
                text = (AGENT_ROOT / f"{owner}.md").read_text()
                if f"`{gate_id}`" not in text:
                    failures.append(f"{owner}: missing research gate {gate_id}")
        self.assertEqual([], failures)

    def test_local_quality_gate_owners_name_the_gate(self):
        failures = []
        for gate_id, gate in QUALITY.items():
            for owner in gate["owners"]:
                text = (AGENT_ROOT / f"{owner}.md").read_text()
                if f"`{gate_id}`" not in text:
                    failures.append(f"{owner}: missing quality gate {gate_id}")
        self.assertEqual([], failures)

    def test_artifact_producers_name_their_output(self):
        by_producer = {}
        for artifact, contract in ARTIFACTS.items():
            producer = contract.get("producer")
            if producer and not producer.startswith("parent:"):
                by_producer.setdefault(producer, []).append(artifact)
        failures = []
        for producer, artifacts in by_producer.items():
            text = (AGENT_ROOT / f"{producer}.md").read_text()
            if not any(artifact in text for artifact in artifacts):
                failures.append(f"{producer}: no declared produced artifact")
        self.assertEqual([], failures)

    def test_no_worker_claims_peer_orchestration(self):
        banned = ("delegate to another agent", "handoff the approved brief to", "coordinate the other agents")
        failures = []
        for path in sorted(AGENT_ROOT.glob("*.md")):
            text = path.read_text().lower()
            for phrase in banned:
                if phrase in text:
                    failures.append(f"{path.stem}: {phrase}")
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
