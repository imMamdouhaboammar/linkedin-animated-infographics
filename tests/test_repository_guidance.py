import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDANCE = [
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / ".codex" / "AGENTS.md",
    ROOT / ".agents" / "skills" / "linkedin-animated-infographics" / "SKILL.md",
    ROOT / ".claude" / "skills" / "linkedin-animated-infographics" / "SKILL.md",
]


class RepositoryGuidanceTests(unittest.TestCase):
    def test_root_guidance_files_exist(self):
        self.assertTrue((ROOT / "AGENTS.md").exists())
        self.assertTrue((ROOT / "CLAUDE.md").exists())

    def test_all_guidance_points_to_same_authority(self):
        failures = []
        for path in GUIDANCE:
            self.assertTrue(path.exists(), str(path))
            text = path.read_text()
            for needle in (
                "helper/GUIDE.md",
                "research/capability-notes/gates.json",
                "helper/quality-gates.json",
                "helper/modules.json",
                "scripts/ecosystem_doctor.py",
            ):
                if needle not in text:
                    failures.append(f"{path.relative_to(ROOT)}: missing {needle}")
        self.assertEqual([], failures)

    def test_guidance_names_creative_and_exact_asset_rules(self):
        for path in (ROOT / "AGENTS.md", ROOT / "CLAUDE.md"):
            text = path.read_text().lower()
            self.assertIn("creative-director", text)
            self.assertIn("hooked-design-copy", text)
            self.assertIn("creative-attractive-restrained", text)
            self.assertIn("center-first", text)
            self.assertIn("exact svg", text)

    def test_guidance_does_not_claim_catalog_json_alone_is_authority(self):
        banned = "catalog.json is the source of truth"
        for path in GUIDANCE:
            self.assertNotIn(banned, path.read_text().lower(), str(path))


if __name__ == "__main__":
    unittest.main()
