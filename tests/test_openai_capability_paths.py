import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTOPILOT = ROOT / "openai-skills" / "linkedin-infographic-autopilot"
COMPAT = ROOT / "compatibility" / "codex.json"


class OpenAICapabilityPathTests(unittest.TestCase):
    def test_capability_negotiation_names_required_capabilities(self):
        text = (AUTOPILOT / "references" / "capability-negotiation.md").read_text()
        for capability in (
            "subagents",
            "sandbox_write",
            "shell_or_code_execution",
            "image_inspection",
            "web_research",
            "connected_apps",
            "workspace_agents",
            "publishing_tools",
        ):
            self.assertIn(capability, text)
        self.assertIn("Unknown capabilities are unavailable", text)
        self.assertIn("observed", text)

    def test_execution_paths_are_explicit_and_mutually_ordered(self):
        text = (AUTOPILOT / "references" / "execution-paths.md").read_text()
        for path_name in ("full-autopilot", "tool-rich-sequential", "safe-skill-only"):
            self.assertIn(path_name, text)
        self.assertIn("full-autopilot > tool-rich-sequential > safe-skill-only", text)
        self.assertIn("Do not claim", text)

    def test_compatibility_declares_capability_negotiated_openai_execution(self):
        data = json.loads(COMPAT.read_text())
        openai = data["distributions"]["openai"]
        self.assertEqual("openai-skills", openai["skills_root"])
        self.assertEqual("capability-negotiated-autopilot", openai["execution"])
        self.assertTrue(openai["sandbox_artifacts"])
        self.assertTrue(openai["side_jobs"])
        self.assertEqual("optional", openai["workspace_agents"])


if __name__ == "__main__":
    unittest.main()
