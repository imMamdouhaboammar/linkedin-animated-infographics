import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "3.7.0"


class DesignQualityUpgradeTests(unittest.TestCase):
    def test_canonical_design_taste_has_perception_reference_and_slop_contracts(self):
        text = (ROOT / "skills" / "info-stories" / "references" / "design-taste-gates.md").read_text()
        for marker in (
            "one-second hierarchy test",
            "100x100",
            "squint",
            "grayscale",
            "negative-space audit",
            "tangency",
            "brand-off specificity",
            "effect-subtraction",
            "Evidence -> Observation -> Transferable Rule -> Anti-Rule",
            "cumulative pressure",
            "two or more major",
            "four or more minor",
            "smallest responsible dimension",
        ):
            self.assertIn(marker, text)

    def test_openai_studio_carries_same_design_quality_markers(self):
        root = ROOT / "openai-skills" / "linkedin-infographic-studio"
        combined = "\n".join(
            (root / relative).read_text()
            for relative in (
                "SKILL.md",
                "references/role-passes.md",
                "references/visual-quality-contract.md",
            )
        )
        for marker in (
            "one-second hierarchy test",
            "100x100",
            "squint",
            "grayscale",
            "negative-space audit",
            "tangency",
            "brand-off specificity",
            "effect-subtraction",
            "Evidence -> Observation -> Transferable Rule -> Anti-Rule",
            "cumulative pressure",
            "smallest responsible dimension",
        ):
            self.assertIn(marker, combined)

    def test_openai_autopilot_carries_blocking_perception_preflight(self):
        root = ROOT / "openai-skills" / "linkedin-infographic-autopilot"
        combined = "\n".join(
            (root / relative).read_text()
            for relative in (
                "SKILL.md",
                "references/visual-quality-contract.md",
            )
        )
        for marker in (
            "perception preflight",
            "one-second hierarchy test",
            "brand-off specificity",
            "effect-subtraction",
            "cumulative pressure",
        ):
            self.assertIn(marker, combined)

    def test_focused_review_uses_severity_pressure_and_targeted_revision(self):
        text = (ROOT / "openai-skills" / "linkedin-infographic-review" / "SKILL.md").read_text()
        for marker in (
            "one-second hierarchy test",
            "100x100",
            "grayscale",
            "brand-off specificity",
            "effect-subtraction",
            "critical",
            "major",
            "minor",
            "cumulative pressure",
            "smallest responsible dimension",
        ):
            self.assertIn(marker, text)

    def test_release_candidate_metadata_remains_aligned(self):
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        compatibility = json.loads((ROOT / "compatibility" / "codex.json").read_text())
        submission = json.loads((ROOT / "submission" / "openai-plugin.json").read_text())
        self.assertEqual(EXPECTED_VERSION, codex["version"])
        self.assertEqual(EXPECTED_VERSION, compatibility["plugin_version"])
        self.assertEqual(EXPECTED_VERSION, submission["version"])
        self.assertEqual("skills-only", submission["submission_type"])
        self.assertEqual("prepared-not-submitted", submission["submission_status"])


if __name__ == "__main__":
    unittest.main()
