import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MasterOneOpenAIContractTests(unittest.TestCase):
    def test_openai_masterone_skill_is_packaged_and_routes_to_existing_skills(self):
        path = ROOT / "openai-skills/masterone/SKILL.md"
        self.assertTrue(path.is_file())
        text = path.read_text()
        for name in (
            "linkedin-infographic-autopilot",
            "linkedin-infographic-studio",
            "linkedin-infographic-review",
            "exact-svg-mascot",
            "share-community-demo",
        ):
            self.assertIn(f"`{name}`", text)

    def test_openai_default_prompt_starts_with_masterone(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        prompts = manifest["interface"]["defaultPrompt"]
        self.assertTrue(prompts)
        self.assertIn("MasterOne", prompts[0])


if __name__ == "__main__":
    unittest.main()
