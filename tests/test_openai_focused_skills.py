import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPENAI_ROOT = ROOT / "openai-skills"
CASES = ROOT / "submission" / "test-cases.json"


class OpenAIFocusedSkillTests(unittest.TestCase):
    def test_expected_public_openai_skills_exist(self):
        expected = {
            "linkedin-infographic-autopilot": "linkedin-infographic-autopilot",
            "linkedin-infographic-studio": "linkedin-infographic-studio",
            "linkedin-infographic-review": "linkedin-infographic-review",
            "exact-svg-mascot": "exact-svg-mascot",
            "share-community-demo": "share-community-demo",
        }
        for directory, skill_name in expected.items():
            path = OPENAI_ROOT / directory / "SKILL.md"
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))
            text = path.read_text()
            self.assertTrue(text.startswith("---\n"), directory)
            self.assertIn(f"name: {skill_name}", text)
            self.assertIn("description:", text)

    def test_studio_supporting_contracts_are_complete(self):
        refs = OPENAI_ROOT / "linkedin-infographic-studio" / "references"
        for filename in (
            "openai-runtime.md",
            "role-passes.md",
            "visual-archetypes.md",
            "copy-quality-contract.md",
            "visual-quality-contract.md",
            "motion-quality-contract.md",
        ):
            self.assertTrue((refs / filename).is_file(), filename)

    def test_autopilot_has_executable_runtime_helper(self):
        runtime = OPENAI_ROOT / "linkedin-infographic-autopilot" / "scripts" / "autopilot_runtime.py"
        self.assertTrue(runtime.is_file())
        text = runtime.read_text()
        self.assertIn("select_execution_path", text)
        self.assertIn("build_dispatch_plan", text)
        self.assertIn("create_workspace", text)

    def test_focused_review_preserves_visual_failure_taxonomy(self):
        text = (OPENAI_ROOT / "linkedin-infographic-review" / "SKILL.md").read_text()
        for marker in (
            "120px",
            "top-heavy-composition",
            "bottom-dead-zone",
            "nested-card-density",
            "generic-ui-grammar",
            "footer-detachment",
            "motion-on-weak-still",
            "decorative-motion",
            "feed-scale-legibility",
        ):
            self.assertIn(marker, text)

    def test_exact_svg_skill_fails_closed_without_identity_asset(self):
        text = (OPENAI_ROOT / "exact-svg-mascot" / "SKILL.md").read_text()
        for marker in (
            "exact SVG",
            "HOLD",
            "redraw the mascot",
            "generate a lookalike",
            "silhouette",
            "proportions",
        ):
            self.assertIn(marker, text)

    def test_share_skill_requires_consent_safe_export_and_pr_stop(self):
        text = (OPENAI_ROOT / "share-community-demo" / "SKILL.md").read_text()
        for marker in (
            "explicitly agreed",
            "demo.gif",
            "index.html",
            "demo.json",
            "Never merge",
            "HOLD",
            "pull request",
        ):
            self.assertIn(marker, text)

    def test_openai_reviewer_cases_name_real_public_skills(self):
        cases = json.loads(CASES.read_text())
        positive = {case["id"]: case["expected_behavior"] for case in cases["positive"]}
        self.assertIn("linkedin-infographic-autopilot", positive["create-post"])
        self.assertIn("linkedin-infographic-studio", positive["info-story"])
        self.assertIn("linkedin-infographic-review", positive["qa"])
        self.assertIn("exact-svg-mascot", positive["exact-svg-mascot"])
        self.assertIn("share-community-demo", positive["share-demo"])


if __name__ == "__main__":
    unittest.main()
