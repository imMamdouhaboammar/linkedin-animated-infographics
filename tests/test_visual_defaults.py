import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "helper" / "capabilities.json"
DESIGN_GATES = ROOT / "skills" / "info-stories" / "references" / "design-taste-gates.md"


class VisualDefaultTests(unittest.TestCase):
    def test_design_taste_declares_plugin_wide_visual_defaults(self):
        design_taste = json.loads(CAPABILITIES.read_text())["capabilities"]["design-taste"]
        defaults = design_taste.get("local_defaults", {})
        self.assertEqual("creative-attractive-restrained", defaults.get("palette_character"))
        self.assertEqual("center-first", defaults.get("composition_alignment"))
        exceptions = set(defaults.get("alignment_exceptions", []))
        for expected in ("tables", "ui-mockups", "code-or-terminal", "timelines", "arabic-rtl", "reference-dna"):
            self.assertIn(expected, exceptions)

    def test_design_gate_documents_restrained_color_and_center_first_rule(self):
        text = DESIGN_GATES.read_text().lower()
        self.assertIn("creative-attractive-restrained", text)
        self.assertIn("center-first", text)
        self.assertIn("avoid exaggerated saturation", text)
        self.assertIn("alignment exception", text)

    def test_shipping_visual_workers_enforce_defaults(self):
        expectations = {
            "palette-curator": ("creative-attractive-restrained", "avoid exaggerated saturation"),
            "layout-composer": ("center-first", "alignment exception"),
            "artboard-builder": ("center-first", "creative-attractive-restrained"),
            "post-critic": ("center-first", "exaggerated saturation"),
        }
        failures = []
        for agent, needles in expectations.items():
            text = (ROOT / "agents" / f"{agent}.md").read_text().lower()
            for needle in needles:
                if needle not in text:
                    failures.append(f"{agent}: missing {needle}")
        self.assertEqual([], failures)

    def test_helper_guide_names_center_first_default(self):
        text = (ROOT / "helper" / "GUIDE.md").read_text().lower()
        self.assertIn("center-first", text)
        self.assertIn("creative-attractive-restrained", text)


if __name__ == "__main__":
    unittest.main()
