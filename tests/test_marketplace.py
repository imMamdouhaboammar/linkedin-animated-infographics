import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
VALIDATOR = ROOT / "scripts" / "validate_marketplace.py"
README = ROOT / "README.md"


def load_validator():
    if not VALIDATOR.exists():
        return None
    spec = importlib.util.spec_from_file_location("validate_marketplace", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MarketplaceTests(unittest.TestCase):
    def test_same_repo_marketplace_manifest(self):
        self.assertTrue(MARKETPLACE.exists(), "missing .claude-plugin/marketplace.json")
        data = json.loads(MARKETPLACE.read_text())
        self.assertEqual("mamdouh-creative-tools", data["name"])
        self.assertEqual("1.0.0", data["version"])
        self.assertEqual("Mamdouh Aboammar", data["owner"]["name"])
        self.assertEqual(1, len(data["plugins"]))
        entry = data["plugins"][0]
        self.assertEqual("linkedin-animated-infographics", entry["name"])
        self.assertEqual("./", entry["source"])
        self.assertIs(True, entry["strict"])

    def test_marketplace_and_plugin_versions_match(self):
        market = json.loads(MARKETPLACE.read_text())["plugins"][0]
        plugin = json.loads(PLUGIN.read_text())
        self.assertEqual("2.2.0", plugin["version"])
        self.assertEqual(plugin["version"], market["version"])

    def test_standard_component_directories_exist(self):
        for relative in ("skills", "agents", "hooks/hooks.json"):
            self.assertTrue((ROOT / relative).exists(), relative)

    def test_readme_documents_marketplace_install(self):
        text = README.read_text()
        self.assertIn("/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics", text)
        self.assertIn("/plugin install linkedin-animated-infographics@mamdouh-creative-tools", text)

    def test_local_marketplace_validator_is_clean(self):
        module = load_validator()
        self.assertIsNotNone(module, "missing scripts/validate_marketplace.py")
        self.assertEqual([], module.validate_marketplace(ROOT))


if __name__ == "__main__":
    unittest.main()
