import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "helper" / "capabilities.json"
QUALITY = ROOT / "helper" / "quality-gates.json"
DESIGN_GATES = ROOT / "skills" / "info-stories" / "references" / "design-taste-gates.md"


class VisualDefaultTests(unittest.TestCase):
    def test_design_taste_declares_plugin_wide_visual_defaults(self):
        capabilities = json.loads(CAPABILITIES.read_text())["capabilities"]
        design_taste = capabilities["design-taste"]
        defaults = design_taste.get("local_defaults", {})
        self.assertEqual("creative-attractive-restrained", defaults.get("palette_character"))
        self.assertEqual("center-first", defaults.get("composition_alignment"))
        exceptions = set(defaults.get("alignment_exceptions", []))
        for expected in ("tables", "ui-mockups", "code-or-terminal", "timelines", "arabic-rtl", "reference-dna"):
            self.assertIn(expected, exceptions)

        identity = capabilities["visual-asset-sourcing"]["local_defaults"]
        self.assertEqual(["user-official", "lobe", "hold"], identity.get("identity_precedence"))
        self.assertIn("lobehub.com/icons/skill.md", identity.get("lobe_skill", ""))
        self.assertEqual(["local", "embedded"], identity.get("render_disposition"))

        typography = capabilities["typography-direction"]["local_defaults"]
        self.assertEqual(["system", "embedded", "local-file"], typography.get("loading_strategies"))
        self.assertEqual("forbidden", typography.get("remote_font_loading"))

    def test_design_gate_documents_visual_defaults(self):
        text = DESIGN_GATES.read_text().lower()
        self.assertIn("creative-attractive-restrained", text)
        self.assertIn("center-first", text)
        self.assertIn("lobe-first", text)
        self.assertIn("intentional typography", text)
        self.assertIn("clean creative structure", text)
        self.assertIn("avoid exaggerated saturation", text)
        self.assertIn("alignment exception", text)

    def test_blocking_gates_cover_asset_type_and_structure(self):
        gates = json.loads(QUALITY.read_text())["gates"]
        for gate in ("verified-identity-assets", "intentional-typography", "clean-creative-structure"):
            self.assertEqual("blocking", gates[gate]["severity"])

    def test_shipping_visual_workers_enforce_defaults(self):
        expectations = {
            "asset-curator": ("lobe", "verified-identity-assets"),
            "creative-director": ("clean-creative-structure", "negative-space"),
            "palette-curator": ("creative-attractive-restrained", "avoid exaggerated saturation"),
            "type-curator": ("intentional-typography", "remote @import"),
            "layout-composer": ("center-first", "verified-identity-assets", "intentional-typography"),
            "artboard-builder": ("center-first", "creative-attractive-restrained", "verified-identity-assets", "intentional-typography"),
            "post-critic": ("clean-creative-structure", "verified-identity-assets", "intentional-typography"),
        }
        failures = []
        for agent, needles in expectations.items():
            text = (ROOT / "agents" / f"{agent}.md").read_text().lower()
            for needle in needles:
                if needle not in text:
                    failures.append(f"{agent}: missing {needle}")
        self.assertEqual([], failures)

    def test_helper_guide_names_all_core_visual_defaults(self):
        text = (ROOT / "helper" / "GUIDE.md").read_text().lower()
        self.assertIn("center-first", text)
        self.assertIn("creative-attractive-restrained", text)
        self.assertIn("lobe-first", text)
        self.assertIn("intentional typography", text)
        self.assertIn("clean creative structure", text)


if __name__ == "__main__":
    unittest.main()
