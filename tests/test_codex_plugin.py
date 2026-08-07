import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX_PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_PLUGIN = ROOT / ".claude-plugin" / "plugin.json"


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
        self.assertTrue(CODEX_PLUGIN.exists(), "missing .codex-plugin/plugin.json")
        codex = json.loads(CODEX_PLUGIN.read_text())
        claude = json.loads(CLAUDE_PLUGIN.read_text())
        self.assertEqual(claude["name"], codex["name"])


if __name__ == "__main__":
    unittest.main()
