import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RuntimeEfficiencyTests(unittest.TestCase):
    def test_runtime_contract_registries_exist(self):
        required = (
            "helper/runtime-contract.json",
            "helper/artifact-views.json",
            "helper/cache-policy.json",
            "helper/model-policy.json",
            "helper/token-budgets.json",
            "scripts/runtime_context.py",
            "scripts/runtime_subagent_context.py",
            ".claude/settings.json",
        )
        missing = [path for path in required if not (ROOT / path).exists()]
        self.assertEqual([], missing)

    def test_cache_policy_is_exact_local_and_keeps_acceptance_uncached(self):
        path = ROOT / "helper" / "cache-policy.json"
        self.assertTrue(path.exists(), "missing cache policy")
        policy = json.loads(path.read_text())
        self.assertEqual("content-addressed", policy["strategy"])
        self.assertFalse(policy["semantic_reuse"])
        self.assertEqual("local-only", policy["scope"])
        for stage in ("post-critic", "story-verifier"):
            self.assertFalse(policy["stages"][stage]["cacheable"], stage)

    def test_critical_workers_keep_opus(self):
        path = ROOT / "helper" / "model-policy.json"
        self.assertTrue(path.exists(), "missing model policy")
        policy = json.loads(path.read_text())
        for stage in ("creative-director", "post-critic", "story-verifier"):
            self.assertEqual("opus", policy["stages"][stage]["model"], stage)
            self.assertEqual("critical", policy["stages"][stage]["quality_tier"], stage)

    def test_parent_workflow_uses_runtime_prepare_store_protocol(self):
        text = (ROOT / "skills" / "new-post" / "SKILL.md").read_text()
        self.assertIn("runtime_context.py prepare", text)
        self.assertIn("runtime_context.py store", text)
        self.assertIn("CACHE HIT", text)

    def test_project_marketplace_enables_native_auto_update(self):
        settings_path = ROOT / ".claude" / "settings.json"
        self.assertTrue(settings_path.exists(), "missing project Claude settings")
        settings = json.loads(settings_path.read_text())
        marketplace = settings["extraKnownMarketplaces"]["mamdouh-creative-tools"]
        self.assertTrue(marketplace["autoUpdate"])
        self.assertTrue(settings["enabledPlugins"]["linkedin-animated-infographics@mamdouh-creative-tools"])


if __name__ == "__main__":
    unittest.main()
