import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "runtime_context.py"
SESSION_HOOK = ROOT / "scripts" / "runtime_session_context.py"


class RuntimeEfficiencyTests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(RUNTIME), *args], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )

    def _inputs(self, workspace: Path, claim="Claim A", note="note-a", audience="engineering leaders"):
        build = workspace / "build"
        build.mkdir(parents=True, exist_ok=True)
        request_dir = build / "runtime-context"
        request_dir.mkdir(parents=True, exist_ok=True)
        (request_dir / "request.json").write_text(json.dumps({
            "topic": "Runtime efficiency", "audience": audience,
            "language": "en", "output_mode": "animated"
        }))
        (build / "evidence.json").write_text(json.dumps({
            "protected_claims": [claim], "blocked_proof_slots": [],
            "exact_labels": ["Product X"], "internal_notes": note,
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
            "helper/runtime-contract.json", "helper/artifact-views.json",
            "helper/cache-policy.json", "helper/model-policy.json",
            "helper/token-budgets.json", "scripts/runtime_context.py",
            "scripts/runtime_subagent_context.py", "scripts/runtime_session_context.py",
            ".claude/settings.json",
        )
        self.assertEqual([], [path for path in required if not (ROOT / path).exists()])

    def test_cache_policy_is_exact_local_and_keeps_acceptance_uncached(self):
        policy = json.loads((ROOT / "helper" / "cache-policy.json").read_text())
        self.assertEqual("content-addressed", policy["strategy"])
        self.assertFalse(policy["semantic_reuse"])
        self.assertEqual("local-only", policy["scope"])
        for stage in ("post-critic", "story-verifier"):
            self.assertFalse(policy["stages"][stage]["cacheable"], stage)

    def test_critical_workers_keep_opus(self):
        policy = json.loads((ROOT / "helper" / "model-policy.json").read_text())
        for stage in ("creative-director", "post-critic", "story-verifier"):
            self.assertEqual("opus", policy["stages"][stage]["model"], stage)
            self.assertEqual("critical", policy["stages"][stage]["quality_tier"], stage)

    def test_prepare_projects_context_and_hashes_only_relevant_fields(self):
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

    def test_request_record_participates_in_cache_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._inputs(workspace, audience="engineering leaders")
            first = json.loads(self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace)).stdout)
            self._inputs(workspace, audience="designers")
            second = json.loads(self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace)).stdout)
            self.assertNotEqual(first["cache_key"], second["cache_key"])

    def test_missing_request_record_disables_cache_reuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._inputs(workspace)
            (workspace / "build" / "runtime-context" / "request.json").unlink()
            result = self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            data = json.loads(result.stdout)
            self.assertFalse(data["cacheable"])
            self.assertEqual("missing-request-record", data["cache_reason"])

    def test_store_then_prepare_restores_stage_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            build = self._inputs(workspace)
            prepared = self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            self.assertFalse(json.loads(prepared.stdout)["cache_hit"])
            output = build / "creative-concepts.json"
            output.write_text(json.dumps({"directions": [{"concept_name": "Contrast"}]}))
            stored = self._run("store", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace))
            self.assertEqual(0, stored.returncode, stored.stderr)
            output.unlink()
            restored = json.loads(self._run("prepare", "--intent", "create-post", "--stage", "creative-director", "--workspace", str(workspace)).stdout)
            self.assertTrue(restored["cache_hit"])
            self.assertEqual("Contrast", json.loads(output.read_text())["directions"][0]["concept_name"])

    def test_session_hook_documents_prepare_store_skip_protocol(self):
        self.assertTrue(SESSION_HOOK.exists(), "missing runtime session hook")
        text = SESSION_HOOK.read_text()
        for needle in ("runtime_context.py prepare", "runtime_context.py store", "CACHE HIT", "request.json"):
            self.assertIn(needle, text)

    def test_project_marketplace_enables_native_auto_update(self):
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text())
        marketplace = settings["extraKnownMarketplaces"]["mamdouh-creative-tools"]
        self.assertTrue(marketplace["autoUpdate"])
        self.assertTrue(settings["enabledPlugins"]["linkedin-animated-infographics@mamdouh-creative-tools"])


if __name__ == "__main__":
    unittest.main()
