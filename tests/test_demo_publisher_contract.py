import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DemoPublisherContractTests(unittest.TestCase):
    def setUp(self):
        self.router = json.loads((ROOT / "helper" / "router.json").read_text())
        self.graph = json.loads((ROOT / "architecture" / "plugin-graph.json").read_text())
        self.modules = json.loads((ROOT / "helper" / "modules.json").read_text())["modules"]

    def test_share_demo_is_a_focused_route(self):
        route = self.router["routes"]["share-demo"]
        self.assertEqual("share-demo", route["workflow"])
        self.assertEqual(["share-demo"], route["skills"])
        self.assertEqual(["community-publisher"], route["agents"])

    def test_share_demo_is_not_in_new_post_critical_sequence(self):
        sequence = self.graph["workflows"]["new-post"]["sequence"]
        self.assertNotIn("community-publisher", sequence)

    def test_skill_and_agent_exist_as_real_modules(self):
        skill = ROOT / "skills" / "share-demo" / "SKILL.md"
        agent = ROOT / "agents" / "community-publisher.md"
        self.assertTrue(skill.is_file())
        self.assertTrue(agent.is_file())
        self.assertGreater(len(skill.read_text().strip()), 500)
        self.assertGreater(len(agent.read_text().strip()), 500)

    def test_publisher_contract_forbids_merge_and_upstream_main_push(self):
        text = (ROOT / "agents" / "community-publisher.md").read_text()
        self.assertIn("Never merge", text)
        self.assertIn("Never enable auto-merge", text)
        self.assertIn("Never push directly to upstream `main`", text)
        self.assertIn("manual review", text.lower())
        self.assertIn("PR URL", text)

    def test_publisher_contract_requires_fork_branch_commit_push_pr(self):
        text = (ROOT / "agents" / "community-publisher.md").read_text().lower()
        for needle in ("fork", "community/<user>/<slug>", "commit", "push", "pull request"):
            self.assertIn(needle, text)

    def test_publisher_preloads_share_demo_skill(self):
        self.assertEqual(["share-demo"], self.graph["agents"]["community-publisher"]["required_skills"])

    def test_new_modules_are_declared_and_tested(self):
        self.assertIn("share-demo", self.modules["skills"])
        self.assertIn("community-publisher", self.modules["agents"])
        self.assertIn("demo_gallery", self.modules["tools"])
        self.assertIn("demo_submit", self.modules["tools"])
        for kind, name in (("skills", "share-demo"), ("agents", "community-publisher"), ("tools", "demo_gallery"), ("tools", "demo_submit")):
            contract = self.modules[kind][name]
            self.assertTrue(contract["tests"], f"{kind}:{name}")
            self.assertTrue(contract["reachable_from"], f"{kind}:{name}")

    def test_share_skill_names_export_safety_and_hold_semantics(self):
        text = (ROOT / "skills" / "share-demo" / "SKILL.md").read_text().lower()
        for needle in (
            "explicit opt-in",
            "verification pass",
            "rights confirmation",
            "source prompt",
            "demo_submit.py prepare",
            "demo_submit.py check",
            "demo_gallery.py check",
            "hold",
        ):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
