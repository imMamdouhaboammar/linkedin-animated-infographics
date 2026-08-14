import json
import unittest
from pathlib import Path

from scripts.antigravity_agents import load_agent_catalog
from scripts.validate_antigravity_plugin import (
    EXPECTED_AGENTS,
    EXPECTED_NAME,
    EXPECTED_VERSION,
    validate_antigravity_plugin,
)

ROOT = Path(__file__).resolve().parents[1]


class AntigravityPluginTests(unittest.TestCase):
    def test_validator_returns_no_errors(self):
        errors = validate_antigravity_plugin(ROOT)
        self.assertEqual([], errors, f"Antigravity validation errors: {errors}")

    def test_root_plugin_json_schema(self):
        plugin_file = ROOT / "plugin.json"
        self.assertTrue(plugin_file.is_file())
        data = json.loads(plugin_file.read_text(encoding="utf-8"))
        self.assertEqual(EXPECTED_NAME, data["name"])
        self.assertEqual(EXPECTED_VERSION, data["version"])
        self.assertIn("interface", data)
        self.assertEqual("LinkedIn Animated Infographics", data["interface"]["displayName"])

    def test_all_19_canonical_agents_in_catalog(self):
        catalog = load_agent_catalog()
        self.assertEqual(19, len(catalog))
        self.assertEqual(EXPECTED_AGENTS, set(catalog.keys()))

        # Check write permissions match expected roles
        self.assertTrue(catalog["artboard-builder"]["enable_write_tools"])
        self.assertTrue(catalog["layout-composer"]["enable_write_tools"])
        self.assertTrue(catalog["mascot-animator"]["enable_write_tools"])
        self.assertTrue(catalog["motion-engineer"]["enable_write_tools"])
        self.assertTrue(catalog["community-publisher"]["enable_write_tools"])

        # Check read-only workers
        self.assertFalse(catalog["creative-director"]["enable_write_tools"])
        self.assertFalse(catalog["evidence-checker"]["enable_write_tools"])
        self.assertFalse(catalog["story-verifier"]["enable_write_tools"])
        self.assertFalse(catalog["post-critic"]["enable_write_tools"])

    def test_hooks_json_validity(self):
        hooks_file = ROOT / ".agents" / "hooks.json"
        self.assertTrue(hooks_file.is_file())
        data = json.loads(hooks_file.read_text(encoding="utf-8"))
        self.assertIn("artboard-lint-checker", data)
        self.assertIn("runtime-context-injector", data)

    def test_compatibility_antigravity_manifest(self):
        compat_file = ROOT / "compatibility" / "antigravity.json"
        self.assertTrue(compat_file.is_file())
        data = json.loads(compat_file.read_text(encoding="utf-8"))
        self.assertEqual(EXPECTED_NAME, data["plugin_name"])
        self.assertEqual(EXPECTED_VERSION, data["plugin_version"])
        self.assertIn("antigravity", data["surfaces"])
        self.assertEqual(19, len(data["distributions"]["antigravity"]["supported_agents"]))


if __name__ == "__main__":
    unittest.main()
