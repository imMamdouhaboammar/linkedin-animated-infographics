import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SISTER_URLS = {
    "https://chatgpt.com/plugins/plugins_6a894aa0f3f48191b1987e6245fc2a35",
    "https://chatgpt.com/plugins/plugins_6a8936fa5798819182ef2a60f1c08a71",
    "https://chatgpt.com/plugins/plugins_6a893288a1008191857f5437d78ab047",
    "https://chatgpt.com/plugins/plugins_6a891ce942648191994f57393f2e765b",
    "https://chatgpt.com/plugins/plugins_6a8366789d3081919bf20654f87e082b",
    "https://chatgpt.com/plugins/plugins_6a80500711748191bee28e0649499efa",
}


class NarrativeTasteTests(unittest.TestCase):
    def setUp(self):
        from scripts import info_stories

        self.mod = info_stories
        self.query = {
            "stage": "narrative",
            "story_jobs": ["explain-system"],
            "content_shapes": ["process"],
            "output_mode": "gif",
            "language": "en",
            "density": "medium",
            "evidence_mode": "documented",
            "top_k": 3,
            "byte_budget": 6000,
        }

    def test_narrative_stage_exposes_story_progression_without_layout_payload(self):
        catalog = self.mod.load_catalog()
        ranked = self.mod.rank_mechanisms(catalog, self.query)
        capsule = self.mod.build_context_capsule(catalog, ranked, "narrative", 6000)

        self.assertEqual("narrative", capsule["stage"])
        self.assertTrue(capsule["mechanisms"])
        first = capsule["mechanisms"][0]
        for field in ("story_jobs", "hook", "beats", "hierarchy", "originality", "anti_patterns", "reference_ids"):
            self.assertIn(field, first)
        self.assertNotIn("layout", first)
        self.assertNotIn("motion", first)

    def test_demo_taste_cli_returns_bounded_repo_candidates_without_embedding_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            query_path = Path(tmp) / "query.json"
            query_path.write_text(json.dumps(self.query), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "demo_taste.py"), "--query", str(query_path), "--max-demos", "3"],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("abstract-transfer-only", payload["source_policy"])
        self.assertLessEqual(len(payload["demo_candidates"]), 3)
        self.assertTrue(payload["transfer_contract"])
        self.assertNotIn("data:image", result.stdout)
        self.assertNotIn("base64", result.stdout.lower())
        for candidate in payload["demo_candidates"]:
            path = candidate.get("path")
            if path is not None:
                self.assertTrue(path.startswith("demos/"), path)

    def test_portable_narrative_taste_contract_is_identical_for_studio_and_autopilot(self):
        studio = ROOT / "openai-skills/linkedin-infographic-studio/references/narrative-taste.md"
        autopilot = ROOT / "openai-skills/linkedin-infographic-autopilot/references/narrative-taste.md"
        canonical = ROOT / "skills/info-stories/references/narrative-taste.md"
        for path in (studio, autopilot, canonical):
            self.assertTrue(path.is_file(), path)
        self.assertEqual(studio.read_text(encoding="utf-8"), autopilot.read_text(encoding="utf-8"))
        text = studio.read_text(encoding="utf-8")
        for marker in (
            "Hook -> Tension -> Evidence -> Turn -> Payoff",
            "Reader question",
            "Beat-to-visual mapping",
            "Evidence -> Observation -> Transferable Rule -> Anti-Rule",
            "Do not copy",
        ):
            self.assertIn(marker, text)

    def test_sister_plugin_refs_are_exact_unique_and_capability_safe(self):
        portable = ROOT / "openai-skills/masterone/references/sister-plugins.md"
        canonical = ROOT / "docs/sister-plugins.md"
        for path in (portable, canonical):
            self.assertTrue(path.is_file(), path)
            text = path.read_text(encoding="utf-8")
            found = {token.rstrip(")>,.;") for token in text.split() if token.startswith("https://chatgpt.com/plugins/plugins_")}
            self.assertEqual(SISTER_URLS, found)
            self.assertIn("Do not infer", text)
            self.assertIn("optional", text.lower())


if __name__ == "__main__":
    unittest.main()
