import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "research" / "capability-notes" / "sources.json"


class InfoStoriesFollowupTests(unittest.TestCase):
    def test_main_post_router_uses_resolved_story_house(self):
        text = (ROOT / "skills/post/SKILL.md").read_text()
        self.assertIn("linkedin-animated-infographics:info-stories", text)
        self.assertIn("Story House", text)
        self.assertNotIn("Colour comes from **House 0", text)

    def test_repo_convention_skills_describe_actual_stack(self):
        for path in [
            ROOT / ".agents/skills/linkedin-animated-infographics/SKILL.md",
            ROOT / ".claude/skills/linkedin-animated-infographics/SKILL.md",
        ]:
            text = path.read_text()
            self.assertIn("Python", text)
            self.assertIn("Markdown", text)
            self.assertIn("Info-stories", text)
            self.assertNotIn("Primary Language**: TypeScript", text)

    def test_missing_upstream_corpus_is_supported(self):
        from scripts import audit_upstreams
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "not-cloned"
            self.assertEqual([], audit_upstreams.build_inventory(missing))

    def test_upstream_check_cli_accepts_clean_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "not-cloned"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/audit_upstreams.py"), "check", "--upstreams", str(missing), "--output", str(SOURCES)],
                cwd=ROOT, text=True, capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr or result.stdout)
            self.assertIn("tracked snapshot", result.stdout.lower())

    def test_public_contrast_tool_reports_ratio(self):
        tool = ROOT / "tools/contrast_check.py"
        self.assertTrue(tool.exists())
        result = subprocess.run(
            [sys.executable, str(tool), "--house", "ember-paper", "--fg", "accent_deep", "--bg", "bg", "--minimum", "4.5"],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertGreaterEqual(payload["ratio"], 4.5)
        self.assertIn("tools/contrast_check.py", (ROOT / "README.md").read_text())

    def test_public_fingerprint_tool_rejects_palette_only_reskin(self):
        tool = ROOT / "tools/fingerprint_check.py"
        self.assertTrue(tool.exists())
        fingerprint = {
            "zone_topology": "three-column-board",
            "card_grammar": "equal-rounded-cards",
            "divider": "hairline",
            "visual_anchor": "headline",
            "density": "medium",
            "motion_grammar": "sequential-highlight",
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            current = tmp / "current.json"
            previous = tmp / "previous.json"
            current.write_text(json.dumps(fingerprint))
            previous.write_text(json.dumps(fingerprint))
            result = subprocess.run(
                [sys.executable, str(tool), "--current", str(current), "--previous", str(previous), "--min-changes", "2"],
                cwd=ROOT, text=True, capture_output=True,
            )
        self.assertEqual(1, result.returncode)
        self.assertFalse(json.loads(result.stdout)["ok"])
        self.assertIn("tools/fingerprint_check.py", (ROOT / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
