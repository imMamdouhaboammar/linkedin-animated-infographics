import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "runtime_context.py"


class RuntimeEfficiencyTests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(RUNTIME), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def _inputs(self, workspace: Path, claim="Claim A", note="note-a"):
        build = workspace / "build"
        build.mkdir(parents=True, exist_ok=True)
        (build / "evidence.json").write_text(json.dumps({
            "protected_claims": [claim],
            "blocked_proof_slots": [],
            "exact_labels": ["Product X"],
            "internal_notes": note,
        }))
        (build / "asset-plan.json").write_text(json.dumps({
            "assets": [{"name": "Product X", "identity_locked": True, "status": "verified"}],
            "debug_notes": "ignore",
        }))
        (build / "design-study.json").write_text(json.dumps({
            "selected_mechanisms": ["comparison"],
            "focused_contexts": {"creative-director": "Use two-state contrast."},
            "raw_reference_notes": "ignore",
        }))
        return build

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

    def test_prepare_projects_context_and_hashes_relevant_fields(self):
        self.assertTrue(RUNTIME.exists(), "missing runtime CLI")
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._inputs(workspace)
            first = self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            self.assertEqual(0, first.returncode, first.stderr)
            one = json.loads(first.stdout)
            capsule = json.loads(Path(one["capsule_path"]).read_text())
            self.assertNotIn("internal_notes", capsule["inputs"]["build/evidence.json"])
            self.assertNotIn("raw_reference_notes", capsule["inputs"]["build/design-study.json"])

            self._inputs(workspace, note="note-b")
            second = self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            self.assertEqual(one["cache_key"], json.loads(second.stdout)["cache_key"])

            self._inputs(workspace, claim="Claim B", note="note-b")
            third = self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            self.assertNotEqual(one["cache_key"], json.loads(third.stdout)["cache_key"])

    def test_store_then_prepare_restores_stage_output(self):
        self.assertTrue(RUNTIME.exists(), "missing runtime CLI")
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            build = self._inputs(workspace)
            prepared = self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            self.assertEqual(0, prepared.returncode, prepared.stderr)
            self.assertFalse(json.loads(prepared.stdout)["cache_hit"])

            output = build / "creative-concepts.json"
            output.write_text(json.dumps({"directions": [{"concept_name": "Contrast"}]}))
            stored = self._run("store", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            self.assertEqual(0, stored.returncode, stored.stderr)
            output.unlink()

            restored = self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            data = json.loads(restored.stdout)
            self.assertTrue(data["cache_hit"])
            self.assertEqual("Contrast", json.loads(output.read_text())["directions"][0]["concept_name"])

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
