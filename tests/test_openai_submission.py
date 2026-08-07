import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "submission" / "openai-plugin.json"
CASES = ROOT / "submission" / "test-cases.json"
README = ROOT / "submission" / "README.md"
LEGAL = (ROOT / "PRIVACY.md", ROOT / "TERMS.md", ROOT / "SUPPORT.md")


class OpenAISubmissionContractTests(unittest.TestCase):
    def test_public_legal_and_support_documents_exist(self):
        for path in LEGAL:
            self.assertTrue(path.is_file(), f"missing {path.name}")
            self.assertGreater(len(path.read_text().strip()), 200, path.name)

    def test_submission_metadata_is_skills_only_3_2_0(self):
        self.assertTrue(SUBMISSION.is_file(), "missing submission/openai-plugin.json")
        data = json.loads(SUBMISSION.read_text())
        self.assertEqual("linkedin-animated-infographics", data["name"])
        self.assertEqual("3.2.0", data["version"])
        self.assertEqual("skills-only", data["submission_type"])
        self.assertEqual("Productivity", data["category"])
        self.assertGreaterEqual(len(data["starter_prompts"]), 4)
        self.assertTrue(data["release_notes"])

    def test_submission_metadata_has_public_urls_and_external_prerequisites(self):
        data = json.loads(SUBMISSION.read_text())
        urls = data["urls"]
        for field in ("website", "support", "privacy", "terms"):
            self.assertTrue(urls[field].startswith("https://github.com/imMamdouhaboammar/linkedin-animated-infographics"), field)
        prereqs = " ".join(data["external_prerequisites"]).lower()
        self.assertIn("apps management", prereqs)
        self.assertIn("verified", prereqs)
        self.assertIn("manual", prereqs)
        self.assertIn("review", prereqs)

    def test_exactly_five_positive_and_three_negative_cases(self):
        self.assertTrue(CASES.is_file(), "missing submission/test-cases.json")
        data = json.loads(CASES.read_text())
        self.assertEqual(5, len(data["positive"]))
        self.assertEqual(3, len(data["negative"]))

    def test_positive_cases_have_required_reviewer_fields(self):
        data = json.loads(CASES.read_text())
        for case in data["positive"]:
            for field in ("id", "user_prompt", "expected_behavior", "expected_result_shape", "fixture_data"):
                self.assertTrue(case.get(field), f"positive {case.get('id')}: {field}")

    def test_negative_cases_have_required_reviewer_fields(self):
        data = json.loads(CASES.read_text())
        for case in data["negative"]:
            for field in ("id", "user_prompt_or_scenario", "expected_safe_behavior", "why_not_complete"):
                self.assertTrue(case.get(field), f"negative {case.get('id')}: {field}")

    def test_cases_cover_product_safety_boundaries(self):
        data = json.loads(CASES.read_text())
        positive_ids = {case["id"] for case in data["positive"]}
        negative_ids = {case["id"] for case in data["negative"]}
        self.assertTrue({"create-post", "info-story", "qa", "exact-svg-mascot", "share-demo"}.issubset(positive_ids))
        self.assertTrue({"missing-exact-svg", "unsafe-demo-export", "share-without-consent"}.issubset(negative_ids))

    def test_submission_readme_states_manual_external_submission(self):
        self.assertTrue(README.is_file(), "missing submission/README.md")
        text = README.read_text().lower()
        self.assertIn("manual", text)
        self.assertIn("openai platform", text)
        self.assertIn("five positive", text)
        self.assertIn("three negative", text)
        self.assertNotIn("already published", text)


if __name__ == "__main__":
    unittest.main()
