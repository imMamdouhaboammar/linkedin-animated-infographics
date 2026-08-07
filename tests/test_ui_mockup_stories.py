import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import info_stories


class UIMockupStoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = info_stories.load_catalog()

    def test_ui_styles_are_first_class_catalog_entries(self):
        styles = {item["slug"]: item for item in self.catalog["styles"]}
        self.assertIn("ui-storyboard", styles)
        self.assertIn("interface-cutaway", styles)
        for slug in ("ui-storyboard", "interface-cutaway"):
            self.assertEqual({"design_variance", "motion_intensity", "visual_density"}, set(styles[slug]["dials"]))

    def test_ui_archetypes_are_available(self):
        archetypes = {item["slug"] for item in self.catalog["archetypes"]}
        self.assertTrue({"screen-to-outcome", "inside-the-interface", "state-change-story"}.issubset(archetypes))

    def test_ui_motion_patterns_are_available(self):
        motions = {item["slug"] for item in self.catalog["motions"]}
        self.assertTrue({"cursor-focus", "state-transition"}.issubset(motions))

    def test_ui_storyboard_composes_screen_to_outcome(self):
        errors = info_stories.check_composition(self.catalog, "ui-storyboard", "screen-to-outcome", ["cursor-focus", "state-transition"])
        self.assertEqual([], errors)

    def test_interface_cutaway_composes_inside_interface(self):
        errors = info_stories.check_composition(self.catalog, "interface-cutaway", "inside-the-interface", ["cursor-focus"])
        self.assertEqual([], errors)

    def test_ui_mockup_rules_block_fake_product_evidence(self):
        rules = (ROOT / "skills/info-stories/references/ui-mockup-rules.md").read_text()
        for needle in ("fictional data", "unsupported product claim", "feed width", "frame 0"):
            self.assertIn(needle, rules.lower())

    def test_tracked_ui_examples_match_scaffold(self):
        examples = [
            ("ui-storyboard-brief.json", "ui-storyboard", "screen-to-outcome", ["cursor-focus", "state-transition"]),
            ("interface-cutaway-brief.json", "interface-cutaway", "inside-the-interface", ["cursor-focus"]),
        ]
        for filename, style, archetype, motions in examples:
            path = ROOT / "examples/info-stories" / filename
            self.assertTrue(path.exists(), filename)
            payload = json.loads(path.read_text())
            self.assertEqual(style, payload["selection"]["style"])
            self.assertEqual(archetype, payload["selection"]["archetype"])
            self.assertEqual(motions, payload["selection"]["motions"])


if __name__ == "__main__":
    unittest.main()
