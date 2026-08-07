import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "helper"
SCRIPT = ROOT / "scripts" / "ecosystem_router.py"


def load_module():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("ecosystem_router", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EcosystemRouterTests(unittest.TestCase):
    def test_helper_contract_files_exist(self):
        for relative in ("README.md", "GUIDE.md", "router.json", "capabilities.json", "artifacts.json"):
            self.assertTrue((HELPER / relative).exists(), relative)
        self.assertTrue(SCRIPT.exists(), "missing scripts/ecosystem_router.py")
        self.assertTrue((ROOT / "tools" / "route_request.py").exists(), "missing public route_request tool")

    def test_registry_validator_is_clean(self):
        module = load_module()
        self.assertIsNotNone(module, "ecosystem router implementation missing")
        self.assertEqual([], module.validate_ecosystem(ROOT))

    def test_full_post_route_uses_canonical_workflow(self):
        module = load_module()
        self.assertIsNotNone(module)
        route = module.route_request({"request": "Create an animated LinkedIn infographic", "output": "gif"}, ROOT)
        self.assertEqual("create-post", route["intent"])
        self.assertEqual("new-post", route["workflow"])
        self.assertIn("story-architect", route["agents"])
        self.assertIn("render-qa", route["agents"])
        self.assertIn("story-verifier", route["agents"])

    def test_named_mascot_without_svg_holds(self):
        module = load_module()
        self.assertIsNotNone(module)
        route = module.route_request({"request": "Create a post with the official Acme mascot", "mascot": {"name": "Acme", "official": True}}, ROOT)
        self.assertEqual("HOLD", route["status"])
        self.assertIn("exact SVG", route["reason"])

    def test_named_mascot_with_exact_svg_routes_mascot_agent(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            svg = Path(tmp) / "official.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0h10v10H0z"/></svg>')
            route = module.route_request({"request": "Create a post with the official Acme mascot", "mascot": {"name": "Acme", "official": True, "svg_path": str(svg)}}, ROOT)
            self.assertEqual("READY", route["status"])
            self.assertIn("mascot-animator", route["conditional_agents"])

    def test_arabic_request_adds_arabic_skill(self):
        module = load_module()
        self.assertIsNotNone(module)
        route = module.route_request({"request": "اعمل انفوجرافيك عربي", "language": "ar"}, ROOT)
        self.assertIn("arabic", route["skills"])

    def test_ui_mockup_request_requires_evidence_capability(self):
        module = load_module()
        self.assertIsNotNone(module)
        route = module.route_request({"request": "Create a UI mockup story for our product", "ui_mockup": True}, ROOT)
        self.assertIn("ui-mockup-fidelity", route["capabilities"])
        self.assertIn("evidence-checker", route["agents"])

    def test_focused_qa_routes_to_qa_workflow(self):
        module = load_module()
        self.assertIsNotNone(module)
        route = module.route_request({"request": "QA this finished infographic", "intent": "qa"}, ROOT)
        self.assertEqual("qa-post", route["workflow"])
        self.assertIn("post-critic", route["agents"])
        self.assertIn("story-verifier", route["agents"])

    def test_helper_guide_names_machine_readable_authority(self):
        guide = HELPER / "GUIDE.md"
        self.assertTrue(guide.exists())
        text = guide.read_text()
        for needle in ("router.json", "capabilities.json", "artifacts.json", "parent workflow", "HOLD"):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
