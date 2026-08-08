import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTOPILOT = ROOT / "openai-skills" / "linkedin-infographic-autopilot"


class OpenAISideJobTests(unittest.TestCase):
    def test_side_job_contract_names_parallel_safe_jobs(self):
        text = (AUTOPILOT / "references" / "side-jobs.md").read_text()
        for job in (
            "evidence-research",
            "creative-direction-exploration",
            "visual-archetype-exploration",
            "copy-compression-critique",
            "still-critique",
            "render-qa",
            "final-verification",
        ):
            self.assertIn(job, text)
        self.assertIn("bounded artifact", text)
        self.assertIn("wait", text.lower())
        self.assertIn("real delegation", text)

    def test_artifact_workspace_has_stable_logical_paths(self):
        text = (AUTOPILOT / "references" / "artifact-workspace.md").read_text()
        for relative in (
            "evidence/evidence.json",
            "concepts/directions.md",
            "selected-direction/decision.md",
            "copy/copy-slots.md",
            "layout/layout-plan.json",
            "build/index.html",
            "still-review/report.json",
            "motion/motion-plan.json",
            "render-qa/report.json",
            "verifier/report.json",
            "final/delivery.json",
        ):
            self.assertIn(relative, text)
        self.assertIn("logical artifact", text)

    def test_tool_policy_forbids_decorative_or_fake_tool_use(self):
        text = (AUTOPILOT / "references" / "tool-usage-policy.md").read_text()
        self.assertIn("Never claim", text)
        self.assertIn("materially improve", text)
        self.assertIn("tool result", text.lower())
        self.assertIn("explicit consent", text)


if __name__ == "__main__":
    unittest.main()
