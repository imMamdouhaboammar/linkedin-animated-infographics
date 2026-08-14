import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
PLUGIN = ROOT / ".claude-plugin/plugin.json"
CODEX_PLUGIN = ROOT / ".codex-plugin/plugin.json"
CODEX_MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
VALIDATOR = ROOT / "scripts/validate_marketplace.py"
README = ROOT / "README.md"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_marketplace", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MarketplaceTests(unittest.TestCase):
    def test_same_repo_marketplace_manifest(self):
        data = json.loads(MARKETPLACE.read_text())
        self.assertEqual("mamdouh-creative-tools", data["name"])
        self.assertEqual("1.0.0", data["version"])
        self.assertEqual("Mamdouh Aboammar", data["owner"]["name"])
        self.assertEqual(1, len(data["plugins"]))
        entry = data["plugins"][0]
        self.assertEqual("linkedin-animated-infographics", entry["name"])
        self.assertEqual("./", entry["source"])
        self.assertIs(True, entry["strict"])
        self.assertEqual("3.5.0", entry["version"])

    def test_all_host_packages_share_release_version(self):
        market = json.loads(MARKETPLACE.read_text())["plugins"][0]
        claude = json.loads(PLUGIN.read_text())
        codex = json.loads(CODEX_PLUGIN.read_text())
        self.assertEqual("3.5.0", claude["version"])
        self.assertEqual(claude["version"], market["version"])
        self.assertEqual(claude["version"], codex["version"])

    def test_standard_component_directories_exist(self):
        for relative in ("skills", "openai-skills", "agents", "hooks/hooks.json", "helper", "demos", "schemas/demo.schema.json", ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json"):
            self.assertTrue((ROOT / relative).exists(), relative)

    def test_readme_documents_both_install_surfaces(self):
        text = README.read_text()
        for needle in ("mamdouh-creative-tools", "linkedin-animated-infographics", "docs/codex.md", "3.5.0"):
            self.assertIn(needle, text)

    def test_codex_marketplace_is_repo_scoped(self):
        data = json.loads(CODEX_MARKETPLACE.read_text())
        self.assertEqual("./", data["plugins"][0]["source"]["path"])
        self.assertEqual("AVAILABLE", data["plugins"][0]["policy"]["installation"])

    def test_local_marketplace_validator_is_clean(self):
        self.assertEqual([], load_validator().validate_marketplace(ROOT))


if __name__ == "__main__":
    unittest.main()
