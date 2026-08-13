import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/masterone_profile.py"
TEMPLATE = ROOT / "templates/masterone-profile.json"


class MasterOneProfileTests(unittest.TestCase):
    def run_cli(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd or ROOT,
            text=True,
            capture_output=True,
        )

    def test_init_creates_template_without_overwriting_existing_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            first = self.run_cli("init", "--workspace", str(ws))
            self.assertEqual(first.returncode, 0, first.stderr)
            path = ws / ".linkedin-infographics/profile.json"
            self.assertEqual(json.loads(path.read_text()), json.loads(TEMPLATE.read_text()))
            profile = json.loads(path.read_text())
            profile["project"]["name"] = "Keep Me"
            path.write_text(json.dumps(profile))
            second = self.run_cli("init", "--workspace", str(ws))
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(json.loads(path.read_text())["project"]["name"], "Keep Me")

    def test_status_is_intent_aware_and_reports_only_material_blockers(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            self.run_cli("init", "--workspace", str(ws))
            create = self.run_cli("status", "--workspace", str(ws), "--intent", "create-post")
            self.assertEqual(create.returncode, 2)
            payload = json.loads(create.stdout)
            self.assertEqual(
                payload["missing_blocking_fields"],
                ["content.default_language", "content.audience", "linkedin.output_mode"],
            )
            render = self.run_cli("status", "--workspace", str(ws), "--intent", "render")
            self.assertEqual(render.returncode, 0, render.stderr)
            self.assertEqual(json.loads(render.stdout)["profile_state"], "READY")

    def test_set_updates_safe_dotted_path_and_invalid_update_preserves_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            self.run_cli("init", "--workspace", str(ws))
            ok = self.run_cli("set", "--workspace", str(ws), "content.default_language", "en")
            self.assertEqual(ok.returncode, 0, ok.stderr)
            path = ws / ".linkedin-infographics/profile.json"
            before = path.read_text()
            bad = self.run_cli("set", "--workspace", str(ws), "content.unknown", "x")
            self.assertEqual(bad.returncode, 1)
            self.assertEqual(path.read_text(), before)

    def test_merge_accepts_only_known_profile_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            self.run_cli("init", "--workspace", str(ws))
            patch = ws / "patch.json"
            patch.write_text(json.dumps({"content": {"audience": "B2B marketers"}}))
            ok = self.run_cli("merge", "--workspace", str(ws), "--input", str(patch))
            self.assertEqual(ok.returncode, 0, ok.stderr)
            profile = json.loads((ws / ".linkedin-infographics/profile.json").read_text())
            self.assertEqual(profile["content"]["audience"], "B2B marketers")
            before = (ws / ".linkedin-infographics/profile.json").read_text()
            patch.write_text(json.dumps({"surprise": True}))
            bad = self.run_cli("merge", "--workspace", str(ws), "--input", str(patch))
            self.assertEqual(bad.returncode, 1)
            self.assertEqual((ws / ".linkedin-infographics/profile.json").read_text(), before)

    def test_sync_claude_is_idempotent_and_preserves_unmanaged_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            claude = ws / "CLAUDE.md"
            claude.write_text("# Existing\n\nKeep this text.\n")
            first = self.run_cli("sync-claude", "--workspace", str(ws))
            self.assertEqual(first.returncode, 0, first.stderr)
            once = claude.read_text()
            second = self.run_cli("sync-claude", "--workspace", str(ws))
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(claude.read_text(), once)
            self.assertIn("Keep this text.", once)
            self.assertEqual(once.count("<!-- MASTERONE:START -->"), 1)
            self.assertEqual(once.count("<!-- MASTERONE:END -->"), 1)

    def test_discover_lists_candidates_without_confirming_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            (ws / "assets").mkdir()
            (ws / "assets/logo.svg").write_text("<svg></svg>")
            (ws / "assets/mascot.svg").write_text("<svg></svg>")
            (ws / "assets/reference.gif").write_bytes(b"GIF89a")
            (ws / "assets/font.woff2").write_bytes(b"font")
            proc = self.run_cli("discover", "--workspace", str(ws))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["advisory_only"])
            self.assertIn("assets/logo.svg", payload["logo_candidates"])
            self.assertIn("assets/mascot.svg", payload["mascot_candidates"])
            self.assertIn("assets/reference.gif", payload["reference_candidates"])
            self.assertIn("assets/font.woff2", payload["font_candidates"])


if __name__ == "__main__":
    unittest.main()
