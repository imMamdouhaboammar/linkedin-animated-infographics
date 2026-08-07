import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mascot_contract.py"


def load_module():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("mascot_contract", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MascotContractTests(unittest.TestCase):
    def test_named_mascot_requires_exact_user_svg(self):
        module = load_module()
        self.assertIsNotNone(module, "missing scripts/mascot_contract.py")
        request = {"requested_name": "Official Brand Mascot", "source": "missing", "svg_path": None}
        errors = module.validate_mascot_request(request)
        self.assertTrue(any("exact" in error.lower() and "svg" in error.lower() for error in errors))

    def test_user_supplied_svg_passes_identity_gate(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            svg = Path(tmp) / "official.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0h10v10H0z"/></svg>')
            request = {"requested_name": "Official Brand Mascot", "source": "user-supplied", "svg_path": str(svg), "allow_substitute": False}
            self.assertEqual([], module.validate_mascot_request(request))

    def test_substitution_is_rejected(self):
        module = load_module()
        request = {"requested_name": "Official Brand Mascot", "source": "generated", "svg_path": "fake.svg", "allow_substitute": True}
        errors = module.validate_mascot_request(request)
        self.assertTrue(any("substitut" in error.lower() for error in errors))

    def test_creative_direction_catalog_is_actionable(self):
        module = load_module()
        directions = module.creative_directions()
        self.assertGreaterEqual(len(directions), 10)
        slugs = {item["slug"] for item in directions}
        self.assertEqual(len(directions), len(slugs))
        for item in directions:
            for key in ("purpose", "communication_job", "allowed_parts", "loop_behavior", "motion_budget"):
                self.assertTrue(item.get(key), f"{item['slug']} missing {key}")

    def test_workflow_routes_exact_svg_through_mascot_animator(self):
        text = (ROOT / "skills" / "new-post" / "SKILL.md").read_text()
        self.assertIn("exact SVG", text)
        self.assertIn("mascot-animator", text)
        self.assertLess(text.index("artboard-builder"), text.index("mascot-animator"))
        self.assertLess(text.index("mascot-animator"), text.index("motion-engineer"))

    def test_direct_skill_tells_main_model_to_request_svg(self):
        text = (ROOT / "skills" / "svg-mascot-animator" / "SKILL.md").read_text().lower()
        self.assertIn("ask the user to upload the exact svg", text)
        self.assertIn("hold: exact svg required", text)

    def test_mascot_agent_preloads_both_mascot_skills(self):
        path = ROOT / "agents" / "mascot-animator.md"
        self.assertTrue(path.exists())
        text = path.read_text()
        self.assertIn("  - svg-mascot-animator", text)
        self.assertIn("  - mascots", text)
        self.assertIn("exact user-supplied SVG", text)


if __name__ == "__main__":
    unittest.main()
