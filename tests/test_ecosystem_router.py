import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "helper"
SCRIPT = ROOT / "scripts" / "ecosystem_router.py"
REQUIRED_CONDITIONS = {"arabic", "ui_mockup", "visual_reference", "official_mascot"}


def load_module():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("ecosystem_router", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_router_fixture(root: Path):
    for relative in ("helper", "research", "skills", "agents", "architecture"):
        shutil.copytree(ROOT / relative, root / relative)


def mutate_router_fixture(root: Path, mutator):
    router_path = root / "helper" / "router.json"
    router = json.loads(router_path.read_text())
    mutator(router)
    router_path.write_text(json.dumps(router))


class EcosystemRouterTests(unittest.TestCase):
    def test_helper_contract_files_exist(self):
        for relative in ("README.md", "GUIDE.md", "router.json", "capabilities.json", "artifacts.json", "quality-gates.json"):
            self.assertTrue((HELPER / relative).exists(), relative)
        self.assertTrue(SCRIPT.exists(), "missing scripts/ecosystem_router.py")
        self.assertTrue((ROOT / "tools" / "route_request.py").exists(), "missing public route_request tool")

    def test_registry_validator_is_clean(self):
        module = load_module()
        self.assertIsNotNone(module, "ecosystem router implementation missing")
        self.assertEqual([], module.validate_ecosystem(ROOT))

    def test_validator_requires_all_runtime_condition_ids(self):
        module = load_module()
        self.assertIsNotNone(module)
        for condition_id in sorted(REQUIRED_CONDITIONS):
            with self.subTest(condition=condition_id), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "repo"
                root.mkdir()
                copy_router_fixture(root)
                mutate_router_fixture(root, lambda router, key=condition_id: router["conditions"].pop(key))
                errors = module.validate_ecosystem(root)
                self.assertTrue(
                    any("required condition" in error.lower() and condition_id in error for error in errors),
                    errors,
                )

    def test_validator_requires_runtime_condition_schema(self):
        module = load_module()
        self.assertIsNotNone(module)
        cases = (
            ("arabic", "adds_skills", None),
            ("ui_mockup", "adds_agents", "not-a-list"),
            ("visual_reference", "adds_capabilities", None),
            ("official_mascot", "asset_gate", 42),
            ("official_mascot", "adds_skills", None),
        )
        for condition_id, field, bad_value in cases:
            with self.subTest(condition=condition_id, field=field), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "repo"
                root.mkdir()
                copy_router_fixture(root)

                def break_field(router, key=condition_id, field_name=field, value=bad_value):
                    if value is None:
                        router["conditions"][key].pop(field_name, None)
                    else:
                        router["conditions"][key][field_name] = value

                mutate_router_fixture(root, break_field)
                errors = module.validate_ecosystem(root)
                self.assertTrue(
                    any(condition_id in error and field in error and "required field" in error.lower() for error in errors),
                    errors,
                )

    def test_route_request_fails_fast_with_value_error_for_malformed_required_condition(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            copy_router_fixture(root)
            mutate_router_fixture(root, lambda router: router["conditions"]["arabic"].pop("adds_skills"))
            with self.assertRaisesRegex(ValueError, "arabic.*adds_skills"):
                module.route_request({"request": "اعمل انفوجرافيك عربي", "language": "ar"}, root)

    def test_full_post_route_uses_canonical_workflow(self):
        module = load_module()
        self.assertIsNotNone(module)
        route = module.route_request({"request": "Create an animated LinkedIn infographic", "output": "gif"}, ROOT)
        self.assertEqual("create-post", route["intent"])
        self.assertEqual("new-post", route["workflow"])
        self.assertIn("creative-director", route["agents"])
        self.assertIn("story-architect", route["agents"])
        self.assertIn("render-qa", route["agents"])
        self.assertIn("story-verifier", route["agents"])

    def test_named_mascot_without_svg_holds(self):
        module = load_module()
        self.assertIsNotNone(module)
        route = module.route_request({"request": "Create a post with the official Acme mascot", "mascot": {"name": "Acme", "official": True}}, ROOT)
        self.assertEqual("HOLD", route["status"])
        self.assertIn("exact SVG", route["reason"])

    def test_named_mascot_with_exact_absolute_svg_routes_mascot_agent(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            svg = Path(tmp) / "official.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0h10v10H0z"/></svg>')
            route = module.route_request({"request": "Create a post with the official Acme mascot", "mascot": {"name": "Acme", "official": True, "svg_path": str(svg)}}, ROOT)
            self.assertEqual("READY", route["status"])
            self.assertIn("mascot-animator", route["conditional_agents"])

    def test_repo_relative_mascot_svg_is_resolved_against_router_root_not_cwd(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repo"
            root.mkdir()
            copy_router_fixture(root)
            asset = root / "fixtures" / "official.svg"
            asset.parent.mkdir()
            asset.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0h10v10H0z"/></svg>')
            elsewhere = base / "elsewhere"
            elsewhere.mkdir()
            previous = Path.cwd()
            try:
                os.chdir(elsewhere)
                route = module.route_request(
                    {
                        "request": "Create a post with the official Acme mascot",
                        "mascot": {"name": "Acme", "official": True, "svg_path": "fixtures/official.svg"},
                    },
                    root,
                )
            finally:
                os.chdir(previous)
            self.assertEqual("READY", route["status"])
            self.assertIn("mascot-animator", route["conditional_agents"])

    def test_focused_mascot_route_holds_when_svg_path_string_does_not_exist(self):
        module = load_module()
        self.assertIsNotNone(module)
        route = module.route_request(
            {"request": "Animate this mascot", "intent": "mascot-animation", "mascot": {"svg_path": "missing.svg"}},
            ROOT,
        )
        self.assertEqual("HOLD", route["status"])
        self.assertIn("exact SVG", route["reason"])

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
