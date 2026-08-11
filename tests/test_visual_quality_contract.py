import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "info_stories.py"
AXES = ("Purpose", "Hierarchy", "Execution", "Specificity", "Restraint", "Variety")


def load_module():
    spec = importlib.util.spec_from_file_location("info_stories_quality", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def quality_report(score=4):
    return {
        "verdict": "PASS" if score >= 3 else "HOLD",
        "render_evidence": {"artifact": "build/render-report.json", "sha256": "a" * 64},
        "axes": [
            {
                "axis": axis,
                "applicable": True,
                "score": score,
                "evidence": f"build/still.png region for {axis}",
                "finding": f"Preserve the observed {axis.lower()} decision",
            }
            for axis in AXES
        ],
    }


class VisualQualityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_evidence_backed_six_axis_report_passes(self):
        self.assertEqual([], self.mod.validate_visual_quality_report(quality_report()))

    def test_missing_axis_evidence_and_actionable_finding_fail(self):
        report = quality_report()
        report["axes"].pop()
        report["axes"][0]["evidence"] = ""
        report["axes"][1]["finding"] = ""
        errors = self.mod.validate_visual_quality_report(report)
        self.assertTrue(any("Variety" in error for error in errors))
        self.assertTrue(any("evidence" in error for error in errors))
        self.assertTrue(any("finding" in error for error in errors))

    def test_applicable_score_below_three_requires_hold(self):
        report = quality_report(score=2)
        self.assertEqual([], self.mod.validate_visual_quality_report(report))
        report["verdict"] = "PASS"
        self.assertTrue(any("HOLD" in error for error in self.mod.validate_visual_quality_report(report)))

    def test_non_applicable_axis_requires_reason_not_score(self):
        report = quality_report()
        report["axes"][0] = {"axis": "Purpose", "applicable": False, "reason": "No CTA in this reference-only study"}
        self.assertEqual([], self.mod.validate_visual_quality_report(report))
        report["axes"][0].pop("reason")
        self.assertTrue(any("reason" in error for error in self.mod.validate_visual_quality_report(report)))

    def test_ready_study_requires_ranked_traceable_focused_evidence(self):
        study = {
            "source": "library",
            "source_kind": "gif",
            "provenance": "public reference",
            "surface": {"tone": "dark"},
            "type_roles": {"display": "grotesk"},
            "structure": {"topology": "ladder"},
            "rhythm": {"density": "medium"},
            "motion": {"visible": True},
            "visual_anchor": "ladder",
            "recommendations": {axis: ["candidate"] for axis in ("house", "style", "archetype", "motion")},
            "copy_boundaries": ["do not copy wording"],
            "reference_status": "READY",
            "ranked_evidence": [{
                "reference_id": "REF-005", "rank": 1, "confidence": "high",
                "provenance_state": "unverified", "rights_state": "unverified",
                "focused_contexts": {"layout": ["ladder topology"], "motion": ["active-stage highlight"]},
            }],
        }
        self.assertEqual([], self.mod.validate_study_report(study))
        study["ranked_evidence"][0]["rights_state"] = ""
        self.assertTrue(any("rights_state" in error for error in self.mod.validate_study_report(study)))

    def test_reference_hold_and_no_reference_skip_are_explicit(self):
        base = {"reference_status": "HOLD", "status_reason": "requested asset unreadable"}
        self.assertEqual([], self.mod.validate_study_evidence(base))
        self.assertEqual([], self.mod.validate_study_evidence({"reference_status": "SKIP", "status_reason": "no reference supplied"}))
        self.assertTrue(self.mod.validate_study_evidence({"reference_status": "HOLD"}))

    def test_typography_roles_and_exact_policy_are_validated(self):
        spec = {"roles": [
            {"role": role, "stack_id": "latin-grotesk", "families": ["Inter", "Arial"], "scripts": ["latin"], "weights": [400, 700], "font_policy": "fallback-accepted"}
            for role in ("display", "body", "label")
        ]}
        self.assertEqual([], self.mod.validate_typography_spec(spec))
        spec["roles"][0]["font_policy"] = "guessed-from-pixels"
        self.assertTrue(self.mod.validate_typography_spec(spec))

    def test_motion_contract_requires_one_complete_job_and_static_regions(self):
        motion = {"output_mode": "gif", "motions": [{
            "communication_job": "reading-sequence", "target": "#stage-2", "sequence": ["stage-1", "stage-2"],
            "duration_ms": 800, "easing_family": "ease-out", "hold_ms": 1200, "reset": "loop-start",
            "static_regions": ["headline", "footer"],
        }]}
        self.assertEqual([], self.mod.validate_motion_direction(motion))
        motion["motions"][0]["static_regions"] = []
        self.assertTrue(self.mod.validate_motion_direction(motion))
        motion = {"output_mode": "static", "motions": [motion["motions"][0]]}
        self.assertTrue(any("static" in error for error in self.mod.validate_motion_direction(motion)))


if __name__ == "__main__":
    unittest.main()
