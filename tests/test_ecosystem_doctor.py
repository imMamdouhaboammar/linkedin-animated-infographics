import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "helper" / "modules.json"
SCRIPT = ROOT / "scripts" / "ecosystem_doctor.py"
PUBLIC_SCRIPT_TOOLS = {"demo_gallery", "demo_submit"}


def load_module():
    if not SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location("ecosystem_doctor", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_repo_fixture(root: Path):
    for relative in ("helper", "skills", "agents", "tools", "architecture", "research", "scripts", "tests"):
        source = ROOT / relative
        if source.exists():
            shutil.copytree(source, root / relative)


class EcosystemDoctorTests(unittest.TestCase):
    def test_manifest_and_strict_doctor_exist(self):
        self.assertTrue(MANIFEST.exists(), "missing helper/modules.json")
        self.assertTrue(SCRIPT.exists(), "missing scripts/ecosystem_doctor.py")

    def test_manifest_matches_public_filesystem_inventory(self):
        self.assertTrue(MANIFEST.exists())
        modules = json.loads(MANIFEST.read_text())["modules"]
        public_scripts = {
            name for name in PUBLIC_SCRIPT_TOOLS if (ROOT / "scripts" / f"{name}.py").is_file()
        }
        expected = {
            "skills": {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")},
            "agents": {path.stem for path in (ROOT / "agents").glob("*.md")},
            "tools": {path.stem for path in (ROOT / "tools").glob("*.py")} | public_scripts,
        }
        self.assertEqual(expected["skills"], set(modules["skills"]))
        self.assertEqual(expected["agents"], set(modules["agents"]))
        self.assertEqual(expected["tools"], set(modules["tools"]))

    def test_every_manifest_entry_has_real_contract(self):
        self.assertTrue(MANIFEST.exists())
        modules = json.loads(MANIFEST.read_text())["modules"]
        failures = []
        for module_type, entries in modules.items():
            for name, contract in entries.items():
                for field in ("path", "role", "tests", "reachable_from"):
                    if contract.get(field) in (None, "", []):
                        failures.append(f"{module_type}:{name}: missing {field}")
                path = ROOT / contract.get("path", "")
                if not path.exists():
                    failures.append(f"{module_type}:{name}: missing path")
                for test_path in contract.get("tests", []):
                    if not (ROOT / test_path).exists():
                        failures.append(f"{module_type}:{name}: missing test {test_path}")
        self.assertEqual([], failures)

    def test_doctor_reports_clean_repository(self):
        module = load_module()
        self.assertIsNotNone(module, "strict doctor implementation missing")
        self.assertEqual([], module.validate_ecosystem_doctor(ROOT))

    def test_doctor_rejects_undeclared_public_tool(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_repo_fixture(root)
            (root / "tools" / "fake_public_tool.py").write_text("def main():\n    return 0\n")
            errors = module.validate_ecosystem_doctor(root)
            self.assertTrue(any("undeclared public tool" in error.lower() for error in errors), errors)

    def test_doctor_rejects_declared_tool_referenced_only_by_manifest(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_repo_fixture(root)
            tool_path = root / "tools" / "fake_declared_tool.py"
            tool_path.write_text("#!/usr/bin/env python3\n\ndef main():\n    print('real enough for the fixture')\n    return 0\n")
            manifest_path = root / "helper" / "modules.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["modules"]["tools"]["fake_declared_tool"] = {
                "path": "tools/fake_declared_tool.py",
                "role": "Fixture tool that is deliberately unused",
                "tests": ["tests/test_ecosystem_doctor.py"],
                "reachable_from": ["helper/modules.json"],
            }
            manifest_path.write_text(json.dumps(manifest))
            errors = module.validate_ecosystem_doctor(root)
            self.assertTrue(
                any("fake_declared_tool" in error and "executable guidance" in error.lower() for error in errors),
                errors,
            )

    def test_doctor_rejects_module_path_that_escapes_repository(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            copy_repo_fixture(root)
            outside = root.parent / "outside.md"
            outside.write_text("outside repository file that must never satisfy a module contract")
            manifest_path = root / "helper" / "modules.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["modules"]["skills"]["post"]["path"] = "../outside.md"
            manifest_path.write_text(json.dumps(manifest))
            errors = module.validate_ecosystem_doctor(root)
            self.assertTrue(any("unsafe module path" in error.lower() and "post" in error for error in errors), errors)

    def test_doctor_rejects_test_path_that_escapes_repository(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            copy_repo_fixture(root)
            outside = root.parent / "outside_test.py"
            outside.write_text("# outside test")
            manifest_path = root / "helper" / "modules.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["modules"]["agents"]["creative-director"]["tests"] = ["../outside_test.py"]
            manifest_path.write_text(json.dumps(manifest))
            errors = module.validate_ecosystem_doctor(root)
            self.assertTrue(any("unsafe test path" in error.lower() and "creative-director" in error for error in errors), errors)

    def test_doctor_rejects_tool_guidance_path_that_escapes_repository(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            copy_repo_fixture(root)
            outside = root.parent / "outside-guide.md"
            outside.write_text("route_request.py is mentioned outside the repository")
            manifest_path = root / "helper" / "modules.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["modules"]["tools"]["route_request"]["reachable_from"] = ["../outside-guide.md"]
            manifest_path.write_text(json.dumps(manifest))
            errors = module.validate_ecosystem_doctor(root)
            self.assertTrue(any("unsafe executable guidance path" in error.lower() and "route_request" in error for error in errors), errors)

    def test_doctor_rejects_unreachable_agent(self):
        module = load_module()
        self.assertIsNotNone(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_repo_fixture(root)
            graph_path = root / "architecture" / "plugin-graph.json"
            graph = json.loads(graph_path.read_text())
            graph["workflows"]["new-post"]["sequence"].remove("creative-director")
            graph_path.write_text(json.dumps(graph))
            router_path = root / "helper" / "router.json"
            router = json.loads(router_path.read_text())
            for route in router["routes"].values():
                route["agents"] = [agent for agent in route.get("agents", []) if agent != "creative-director"]
            router_path.write_text(json.dumps(router))
            errors = module.validate_ecosystem_doctor(root)
            self.assertTrue(any("unreachable active agent creative-director" in error.lower() for error in errors), errors)

    def test_doctor_requires_critical_shipping_workers(self):
        module = load_module()
        self.assertIsNotNone(module)
        errors = module.validate_ecosystem_doctor(ROOT)
        self.assertFalse(any("critical shipping worker" in error.lower() for error in errors), errors)

    def test_active_modules_are_not_placeholder_stubs(self):
        self.assertTrue(MANIFEST.exists())
        modules = json.loads(MANIFEST.read_text())["modules"]
        failures = []
        for entries in modules.values():
            for name, contract in entries.items():
                text = (ROOT / contract["path"]).read_text()
                if len(text.strip()) < 80:
                    failures.append(f"{name}: too small")
                lowered = text.lower()
                if "todo: implement" in lowered or "placeholder module" in lowered:
                    failures.append(f"{name}: placeholder")
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
