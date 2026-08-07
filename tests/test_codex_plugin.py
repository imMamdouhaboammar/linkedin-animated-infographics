import importlib.util
import json
import shutil
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX_PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
COMPATIBILITY = ROOT / "compatibility" / "codex.json"
VALIDATOR = ROOT / "scripts" / "validate_codex_plugin.py"
CODEX_CONFIG = ROOT / ".codex" / "config.toml"
CODEX_AGENT_DIR = ROOT / ".codex" / "agents"
EXPECTED_CODEX_AGENTS = {
    "explorer": "read-only",
    "reviewer": "read-only",
    "docs_researcher": "read-only",
}


def load_validator():
    if not VALIDATOR.exists():
        return None
    spec = importlib.util.spec_from_file_location("validate_codex_plugin", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_fixture(root: Path):
    for relative in (
        ".claude-plugin",
        ".codex-plugin",
        ".agents",
        ".codex",
        "skills",
        "helper",
        "architecture",
        "research",
        "compatibility",
        "submission",
    ):
        source = ROOT / relative
        if source.exists():
            shutil.copytree(source, root / relative)
    for relative in ("PRIVACY.md", "TERMS.md", "SUPPORT.md"):
        source = ROOT / relative
        if source.exists():
            shutil.copy2(source, root / relative)


class CodexPluginPackagingTests(unittest.TestCase):
    def test_openai_plugin_manifest_exists_and_uses_canonical_skills(self):
        self.assertTrue(CODEX_PLUGIN.exists(), "missing .codex-plugin/plugin.json")
        data = json.loads(CODEX_PLUGIN.read_text())
        self.assertEqual("linkedin-animated-infographics", data["name"])
        self.assertEqual("3.2.0", data["version"])
        self.assertEqual("./skills/", data["skills"])
        self.assertEqual("Mamdouh Aboammar", data["author"]["name"])
        self.assertEqual(
            "https://github.com/imMamdouhaboammar/linkedin-animated-infographics",
            data["repository"],
        )

    def test_openai_plugin_manifest_has_install_surface_metadata(self):
        self.assertTrue(CODEX_PLUGIN.exists(), "missing .codex-plugin/plugin.json")
        interface = json.loads(CODEX_PLUGIN.read_text())["interface"]
        for field in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
            "capabilities",
            "websiteURL",
            "privacyPolicyURL",
            "termsOfServiceURL",
            "defaultPrompt",
        ):
            self.assertTrue(interface.get(field), field)
        self.assertEqual("Productivity", interface["category"])
        self.assertGreaterEqual(len(interface["defaultPrompt"]), 3)

    def test_repo_marketplace_exposes_root_plugin(self):
        self.assertTrue(CODEX_MARKETPLACE.exists(), "missing .agents/plugins/marketplace.json")
        data = json.loads(CODEX_MARKETPLACE.read_text())
        self.assertEqual("mamdouh-creative-tools", data["name"])
        self.assertEqual("Mamdouh Creative Tools", data["interface"]["displayName"])
        self.assertEqual(1, len(data["plugins"]))
        entry = data["plugins"][0]
        self.assertEqual("linkedin-animated-infographics", entry["name"])
        self.assertEqual({"source": "local", "path": "./"}, entry["source"])
        self.assertEqual("AVAILABLE", entry["policy"]["installation"])
        self.assertEqual("ON_INSTALL", entry["policy"]["authentication"])
        self.assertEqual("Productivity", entry["category"])

    def test_codex_and_claude_plugin_identity_stays_shared(self):
        codex = json.loads(CODEX_PLUGIN.read_text())
        claude = json.loads(CLAUDE_PLUGIN.read_text())
        self.assertEqual(claude["name"], codex["name"])


class CodexPluginParityTests(unittest.TestCase):
    def require_validator(self):
        module = load_validator()
        self.assertIsNotNone(module, "missing scripts/validate_codex_plugin.py")
        return module

    def test_compatibility_registry_declares_shared_core(self):
        self.assertTrue(COMPATIBILITY.exists(), "missing compatibility/codex.json")
        data = json.loads(COMPATIBILITY.read_text())
        self.assertEqual("3.2.0", data["plugin_version"])
        self.assertEqual("skills", data["canonical"]["skills_root"])
        self.assertEqual("helper/router.json", data["canonical"]["router"])
        self.assertEqual("architecture/plugin-graph.json", data["canonical"]["worker_graph"])
        self.assertEqual("skills-only", data["public_submission"]["type"])
        self.assertIn("codex", data["surfaces"])
        self.assertIn("chatgpt", data["surfaces"])

    def test_validator_reports_clean_repository(self):
        module = self.require_validator()
        self.assertEqual([], module.validate_codex_plugin(ROOT))

    def test_validator_rejects_version_drift(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".codex-plugin" / "plugin.json"
            data = json.loads(path.read_text())
            data["version"] = "9.9.9"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("version" in error.lower() and "drift" in error.lower() for error in errors), errors)

    def test_validator_rejects_skills_path_escape(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".codex-plugin" / "plugin.json"
            data = json.loads(path.read_text())
            data["skills"] = "../outside-skills"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("unsafe" in error.lower() and "skills" in error.lower() for error in errors), errors)

    def test_validator_rejects_marketplace_policy_drift(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / ".agents" / "plugins" / "marketplace.json"
            data = json.loads(path.read_text())
            data["plugins"][0]["policy"]["installation"] = "INSTALLED_BY_DEFAULT"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("marketplace" in error.lower() and "installation" in error.lower() for error in errors), errors)

    def test_validator_rejects_compatibility_path_drift(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            path = root / "compatibility" / "codex.json"
            data = json.loads(path.read_text())
            data["canonical"]["router"] = "helper/not-real.json"
            path.write_text(json.dumps(data))
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("compatibility" in error.lower() and "router" in error.lower() for error in errors), errors)


class CodexRepositoryAgentTests(unittest.TestCase):
    def require_validator(self):
        module = load_validator()
        self.assertIsNotNone(module, "missing scripts/validate_codex_plugin.py")
        return module

    def test_codex_config_uses_current_subagent_controls(self):
        data = tomllib.loads(CODEX_CONFIG.read_text())
        agents = data.get("agents", {})
        self.assertIs(True, agents.get("enabled"))
        self.assertEqual(6, agents.get("max_concurrent_threads_per_session"))
        self.assertNotIn("max_threads", agents)

    def test_project_scoped_codex_agents_are_real_and_narrow(self):
        self.assertTrue(CODEX_AGENT_DIR.is_dir(), "missing .codex/agents")
        for filename, expected_sandbox in EXPECTED_CODEX_AGENTS.items():
            path = CODEX_AGENT_DIR / f"{filename}.toml"
            self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
            data = tomllib.loads(path.read_text())
            self.assertEqual(filename, data.get("name"))
            self.assertTrue(data.get("description"))
            self.assertTrue(data.get("developer_instructions"))
            self.assertEqual(expected_sandbox, data.get("sandbox_mode"))

    def test_installed_plugin_does_not_depend_on_repo_codex_config(self):
        manifest = json.loads(CODEX_PLUGIN.read_text())
        text = json.dumps(manifest)
        self.assertNotIn(".codex/config.toml", text)
        self.assertNotIn(".codex/agents", text)

    def test_validator_rejects_explicit_dead_agent_config_reference(self):
        module = self.require_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture(root)
            config_path = root / ".codex" / "config.toml"
            config_path.write_text(
                config_path.read_text()
                + '\n[agents.broken]\ndescription = "broken fixture"\nconfig_file = "agents/not-real.toml"\n'
            )
            errors = module.validate_codex_plugin(root)
            self.assertTrue(any("agent config" in error.lower() and "not-real.toml" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
