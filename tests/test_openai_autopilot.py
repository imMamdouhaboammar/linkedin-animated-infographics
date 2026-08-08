import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTOPILOT = ROOT / "openai-skills" / "linkedin-infographic-autopilot"
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"


class OpenAIAutopilotPackagingTests(unittest.TestCase):
    def test_autopilot_skill_and_required_references_exist(self):
        required = (
            "SKILL.md",
            "references/capability-negotiation.md",
            "references/execution-paths.md",
            "references/side-jobs.md",
            "references/artifact-workspace.md",
            "references/tool-usage-policy.md",
            "references/autopilot-failure-policy.md",
            "references/workspace-agents-bridge.md",
        )
        for relative in required:
            self.assertTrue((AUTOPILOT / relative).is_file(), relative)

    def test_autopilot_skill_is_self_contained_and_truthful(self):
        text = (AUTOPILOT / "SKILL.md").read_text()
        self.assertIn("name: linkedin-infographic-autopilot", text)
        for marker in (
            "full-autopilot",
            "tool-rich-sequential",
            "safe-skill-only",
            "still",
            "motion",
            "HOLD",
            "observed",
        ):
            self.assertIn(marker, text)
        for forbidden in (
            "${CLAUDE_PLUGIN_ROOT}",
            ".claude-plugin/",
            "helper/",
            "architecture/",
        ):
            self.assertNotIn(forbidden, text)

    def test_openai_manifest_points_to_distribution_and_release_3_2_2(self):
        data = json.loads(PLUGIN.read_text())
        self.assertEqual("3.2.2", data["version"])
        self.assertEqual("./openai-skills/", data["skills"])
        prompts = data["interface"]["defaultPrompt"]
        self.assertGreaterEqual(len(prompts), 1)
        self.assertLessEqual(len(prompts), 3)
        self.assertTrue(any("autopilot" in prompt.lower() or "animated linkedin infographic" in prompt.lower() for prompt in prompts))


if __name__ == "__main__":
    unittest.main()
