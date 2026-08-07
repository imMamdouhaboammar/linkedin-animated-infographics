import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAMS = ROOT / "research" / "upstreams"
SOURCES = ROOT / "research" / "capability-notes" / "sources.json"
EXPECTED = {
    "stop-slop": "https://github.com/hardikpandya/stop-slop",
    "taste-skill": "https://github.com/Leonxlnx/taste-skill",
    "hallmark": "https://github.com/Nutlope/hallmark",
    "no-ai-slop": "https://github.com/petergyang/no-ai-slop",
    "COG-second-brain": "https://github.com/huytieu/COG-second-brain",
}


@unittest.skipUnless(UPSTREAMS.exists(), "local upstream research corpus is intentionally not shipped")
class UpstreamInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts import audit_upstreams
        cls.mod = audit_upstreams
        cls.inventory = audit_upstreams.build_inventory(UPSTREAMS)

    def test_all_requested_sources_are_present(self):
        self.assertEqual(set(EXPECTED), {item["name"] for item in self.inventory})

    def test_inventory_records_url_sha_and_mit_license(self):
        by_name = {item["name"]: item for item in self.inventory}
        for name, url in EXPECTED.items():
            item = by_name[name]
            self.assertEqual(url, item["repository"])
            self.assertRegex(item["commit"], r"^[0-9a-f]{40}$")
            self.assertEqual("MIT", item["license"])
            self.assertTrue(item["readme_present"])

    def test_tracked_sources_snapshot_matches_live_inventory(self):
        snapshot = json.loads(SOURCES.read_text())
        self.assertEqual(self.inventory, snapshot["sources"])

    def test_inventory_is_sorted_and_deterministic(self):
        first = self.mod.build_inventory(UPSTREAMS)
        second = self.mod.build_inventory(UPSTREAMS)
        self.assertEqual(first, second)
        self.assertEqual(sorted(item["name"] for item in first), [item["name"] for item in first])


class TrackedUpstreamSnapshotTests(unittest.TestCase):
    def test_snapshot_is_self_contained_and_records_all_sources(self):
        snapshot = json.loads(SOURCES.read_text())["sources"]
        by_name = {item["name"]: item for item in snapshot}
        self.assertEqual(set(EXPECTED), set(by_name))
        for name, url in EXPECTED.items():
            item = by_name[name]
            self.assertEqual(url, item["repository"])
            self.assertRegex(item["commit"], r"^[0-9a-f]{40}$")
            self.assertEqual("MIT", item["license"])
            self.assertTrue(item["readme_present"])


class StudyAndVerificationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts import info_stories
        cls.mod = info_stories

    def test_study_report_requires_design_dna_fields(self):
        valid = {
            "source": "attached-image",
            "source_kind": "image",
            "provenance": "public reference",
            "surface": {"paper": "warm-light", "accent": "burnt-orange"},
            "type_roles": {"display": "neutral-grotesque", "body": "neutral-grotesque", "labels": "compact-sans"},
            "structure": {"topology": "dense-board", "card_grammar": "mixed-panels"},
            "rhythm": {"density": "dense", "asymmetry": "balanced-grid"},
            "motion": {"visible": True, "grammar": ["sequential-highlight"]},
            "visual_anchor": "headline-and-flow",
            "recommendations": {"house": ["ember-paper"], "style": ["signal-sheet"], "archetype": ["framework-in-one-page"], "motion": ["sequential-highlight"]},
            "copy_boundaries": ["do not copy source wording"],
        }
        self.assertEqual([], self.mod.validate_study_report(valid))
        broken = dict(valid)
        broken.pop("rhythm")
        self.assertTrue(any("rhythm" in error for error in self.mod.validate_study_report(broken)))

    def test_verifier_requires_direct_evidence_per_criterion(self):
        report = {
            "verdict": "PASS",
            "attempt": 0,
            "criteria": [
                {"id": "IS-01", "status": "PASS", "artifact": "build/still.png", "observation": "Headline remains readable at mobile preview", "evidence": "still_mobile350.png"}
            ],
        }
        self.assertEqual([], self.mod.validate_verification_report(report))
        report["criteria"][0]["evidence"] = ""
        self.assertTrue(any("evidence" in error.lower() for error in self.mod.validate_verification_report(report)))

    def test_verifier_rejects_more_than_two_fix_attempts(self):
        report = {"verdict": "FAIL:fixable", "attempt": 3, "criteria": []}
        errors = self.mod.validate_verification_report(report)
        self.assertTrue(any("two" in error.lower() for error in errors))

    def test_study_and_verifier_agents_are_wired(self):
        required = [
            ROOT / "agents/design-study.md",
            ROOT / "agents/story-verifier.md",
            ROOT / "skills/info-stories/references/study-protocol.md",
            ROOT / "skills/info-stories/references/verification-loop.md",
        ]
        for path in required:
            self.assertTrue(path.exists(), str(path))
        skill = (ROOT / "skills/info-stories/SKILL.md").read_text()
        self.assertIn("study-protocol.md", skill)
        self.assertIn("verification-loop.md", skill)


if __name__ == "__main__":
    unittest.main()
