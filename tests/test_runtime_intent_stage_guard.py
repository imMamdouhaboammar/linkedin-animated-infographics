import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "runtime_context.py"


class RuntimeIntentStageGuardTests(unittest.TestCase):
    def _run(self, *args, workspace=None):
        cmd = [sys.executable, str(RUNTIME), *args]
        if workspace is not None:
            cmd.extend(["--workspace", str(workspace)])
        return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)

    def _workspace(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        workspace = Path(tmp.name)
        (workspace / "build" / "runtime-context").mkdir(parents=True)
        (workspace / "build" / "runtime-context" / "request.json").write_text(
            json.dumps({"topic": "guard", "audience": "test", "language": "en", "output_mode": "animated"})
        )
        return workspace

    def _error_codes(self, result):
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stderr.strip().splitlines()[-1])
        self.assertFalse(payload.get("ok", True))
        return [e["code"] for e in payload["errors"]]

    def test_rejects_unknown_intent(self):
        ws = self._workspace()
        result = self._run("prepare", "--intent", "not-a-real-intent", "--stage", "creative-director", workspace=ws)
        self.assertIn("unknown-intent", self._error_codes(result))
        self.assertFalse((ws / "build" / "runtime-context" / "creative-director.json").exists())

    def test_rejects_unknown_stage(self):
        ws = self._workspace()
        result = self._run("prepare", "--intent", "create-post", "--stage", "not-a-real-stage", workspace=ws)
        self.assertIn("unknown-stage", self._error_codes(result))

    def test_rejects_path_like_stage(self):
        ws = self._workspace()
        for stage in ("../evil", "foo/bar", "foo\\bar", "a..b"):
            with self.subTest(stage=stage):
                result = self._run("prepare", "--intent", "create-post", "--stage", stage, workspace=ws)
                codes = self._error_codes(result)
                self.assertTrue("unsafe-stage" in codes or "unknown-stage" in codes, codes)

    def test_rejects_parent_pseudo_stage(self):
        ws = self._workspace()
        result = self._run("prepare", "--intent", "create-post", "--stage", "parent:new-post", workspace=ws)
        self.assertIn("parent-stage-rejected", self._error_codes(result))
        self.assertFalse(any((ws / "build" / "runtime-context").glob("parent*")))

    def test_known_cacheable_stage_still_prepares(self):
        ws = self._workspace()
        result = self._run("prepare", "--intent", "create-post", "--stage", "creative-director", workspace=ws)
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("creative-director", payload["stage"])
        self.assertTrue((ws / "build" / "runtime-context" / "creative-director.json").exists())

    def test_known_non_cacheable_acceptance_stage_still_prepares(self):
        ws = self._workspace()
        result = self._run("prepare", "--intent", "create-post", "--stage", "post-critic", workspace=ws)
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("post-critic", payload["stage"])
        self.assertFalse(payload["cacheable"])

    def test_store_also_rejects_unknown_stage(self):
        ws = self._workspace()
        result = self._run("store", "--intent", "create-post", "--stage", "totally-unknown", workspace=ws)
        self.assertIn("unknown-stage", self._error_codes(result))


if __name__ == "__main__":
    unittest.main()
