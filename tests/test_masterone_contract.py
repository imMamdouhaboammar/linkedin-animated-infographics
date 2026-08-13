import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MasterOneContractTests(unittest.TestCase):
    def test_profile_contract_files_exist(self):
        for rel in (
            "schemas/masterone-profile.schema.json",
            "templates/masterone-profile.json",
            "scripts/masterone_profile.py",
            "skills/masterone/SKILL.md",
            "agents/masterone.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_front_door_is_registered_without_replacing_new_post(self):
        router = json.loads((ROOT / "helper/router.json").read_text())
        self.assertEqual(router["front_door"]["route"], "masterone")
        self.assertEqual(router["front_door"]["agent"], "masterone")
        self.assertEqual(router["front_door"]["skill"], "masterone")
        self.assertEqual(router["routes"]["create-post"]["workflow"], "new-post")

    def test_masterone_names_every_supported_downstream_intent(self):
        router = json.loads((ROOT / "helper/router.json").read_text())
        expected = {"create-post", "qa", "render", "design-study", "mascot-animation", "info-story", "share-demo"}
        self.assertEqual(set(router["front_door"]["downstream_intents"]), expected)
        skill = (ROOT / "skills/masterone/SKILL.md").read_text()
        for intent in expected:
            self.assertIn(f"`{intent}`", skill)

    def test_agent_is_bounded_to_onboarding_not_peer_orchestration(self):
        agent = (ROOT / "agents/masterone.md").read_text().lower()
        self.assertIn("parent workflow", agent)
        self.assertIn("do not", agent)
        self.assertNotIn("spawn peer", agent)
        self.assertNotIn("orchestrate peer agents", agent)

    def test_claude_has_bounded_masterone_section(self):
        claude = (ROOT / "CLAUDE.md").read_text()
        self.assertEqual(claude.count("<!-- MASTERONE:START -->"), 1)
        self.assertEqual(claude.count("<!-- MASTERONE:END -->"), 1)
        self.assertIn(".linkedin-infographics/profile.json", claude)
        self.assertIn("`new-post` remains the complete-production parent workflow", claude)


if __name__ == "__main__":
    unittest.main()
