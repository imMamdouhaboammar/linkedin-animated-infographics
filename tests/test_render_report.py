#!/usr/bin/env python3
"""The merged render report must fail closed and preserve content digests."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_report.py"
CONTRACT = json.loads((ROOT / "helper" / "visual-contract.json").read_text())
KINDS = {"artboard": "scripts/artboard_audit.py", "still": "scripts/check_render.py", "gif": "scripts/build_gif.py"}


def passing_fragment(kind: str) -> dict:
    measured_by = KINDS[kind]
    findings = []
    for threshold_id, threshold in CONTRACT["thresholds"].items():
        if threshold["measured_by"] != measured_by: continue
        findings.append({
            "threshold_id": threshold_id, "gate": threshold["gate"], "severity": threshold["severity"],
            "status": "PASS", "measured": threshold["value"], "threshold": threshold["value"],
            "unit": threshold["unit"], "detail": "", "evidence": [],
        })
    return {"schema_version": 1, "stage": kind, "artifact": f"{kind}.artifact", "findings": findings}


def sidecar_fragment(stage: str, violations: list | None = None) -> dict:
    violations = violations or []
    return {"schema_version": 1, "stage": stage, "artifact": f"{stage}.artifact", "verdict": "FAIL" if violations else "PASS", "violations": violations}


def bind_fragment(fragment: dict, artifact: Path) -> dict:
    fragment["artifact"] = str(artifact)
    fragment["artifact_sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
    return fragment


class RenderReportMergeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.html = self.root / "post.html"; self.gif = self.root / "post.gif"
        self.html.write_bytes(b"<html>measured input</html>"); self.gif.write_bytes(b"GIF89a-measured-output")
        self.fragments = {}
        for kind in KINDS:
            path = self.root / f"{kind}.json"
            path.write_text(json.dumps(bind_fragment(passing_fragment(kind), self.gif if kind == "gif" else self.html)))
            self.fragments[kind] = path
        self.overflow = self.root / "text-overflow.json"
        self.overflow.write_text(json.dumps(bind_fragment(sidecar_fragment("text-overflow"), self.html)))
        self.final_frame = self.root / "final-frame.json"
        self.final_frame.write_text(json.dumps(bind_fragment(sidecar_fragment("final-frame"), self.html)))
        self.report = self.root / "render-report.json"

    def tearDown(self): self.temp.cleanup()

    def run_merge(self) -> subprocess.CompletedProcess:
        return subprocess.run([
            sys.executable, str(SCRIPT), "merge",
            "--artboard", str(self.fragments["artboard"]), "--text-overflow", str(self.overflow),
            "--final-frame", str(self.final_frame), "--still", str(self.fragments["still"]),
            "--gif", str(self.fragments["gif"]), "--input", str(self.html), "--output", str(self.gif),
            "--out", str(self.report),
        ], capture_output=True, text=True, cwd=ROOT)

    def test_passing_fragments_merge_with_input_and_output_digests(self):
        outcome = self.run_merge(); self.assertEqual(outcome.returncode, 0, outcome.stderr)
        report = json.loads(self.report.read_text()); self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["digests"]["input"]["sha256"], hashlib.sha256(self.html.read_bytes()).hexdigest())
        self.assertEqual(report["digests"]["output"]["sha256"], hashlib.sha256(self.gif.read_bytes()).hexdigest())
        self.assertEqual(set(report["digests"]["fragments"]), {"artboard", "still", "gif", "text-overflow", "final-frame"})
        self.assertEqual(next(r for r in report["findings"] if r["gate"] == "text-overflow")["status"], "PASS")
        self.assertEqual(next(r for r in report["findings"] if r["gate"] == "final-frame")["status"], "PASS")

    def test_text_overflow_is_a_blocking_final_report_failure(self):
        violation = {"element": '<div class="headline">', "sample": "A clipped headline", "reasons": ["clipped-x"], "text_rect": {"left": 90}}
        self.overflow.write_text(json.dumps(bind_fragment(sidecar_fragment("text-overflow", [violation]), self.html)))
        outcome = self.run_merge(); self.assertEqual(outcome.returncode, 1, outcome.stderr)
        report = json.loads(self.report.read_text()); self.assertIn("text-overflow", report["summary"]["failed_gates"])

    def test_final_frame_is_a_blocking_final_report_failure(self):
        violation = {"element": "div.headline", "animation": "enter", "remaining_ms": 100.0, "reason": "finite-animation-incomplete"}
        self.final_frame.write_text(json.dumps(bind_fragment(sidecar_fragment("final-frame", [violation]), self.html)))
        outcome = self.run_merge(); self.assertEqual(outcome.returncode, 1, outcome.stderr)
        report = json.loads(self.report.read_text()); self.assertEqual(report["verdict"], "FAIL")
        self.assertIn("final-frame", report["summary"]["failed_gates"])
        finding = next(r for r in report["findings"] if r["gate"] == "final-frame")
        self.assertEqual(finding["severity"], "blocking"); self.assertEqual(finding["evidence"][0]["remaining_ms"], 100.0)

    def test_hidden_required_final_state_is_preserved_as_blocking_evidence(self):
        violation = {
            "element": "div.headline",
            "reason": "required-final-element-hidden",
            "reasons": ["opacity-zero"],
            "opacity": 0.0,
            "rect": {"x": 120, "y": 120, "width": 500, "height": 80},
        }
        self.final_frame.write_text(json.dumps(bind_fragment(sidecar_fragment("final-frame", [violation]), self.html)))
        outcome = self.run_merge(); self.assertEqual(outcome.returncode, 1, outcome.stderr)
        report = json.loads(self.report.read_text()); self.assertEqual(report["verdict"], "FAIL")
        finding = next(r for r in report["findings"] if r["gate"] == "final-frame")
        self.assertIn("completion or visibility", finding["detail"])
        evidence = finding["evidence"][0]
        self.assertEqual(evidence["reason"], "required-final-element-hidden")
        self.assertEqual(evidence["reasons"], ["opacity-zero"])
        self.assertEqual(evidence["opacity"], 0.0)
        self.assertEqual(evidence["rect"]["width"], 500)

    def test_sidecar_verdict_must_match_violations(self):
        fragment = bind_fragment(sidecar_fragment("final-frame"), self.html); fragment["verdict"] = "FAIL"
        self.final_frame.write_text(json.dumps(fragment)); outcome = self.run_merge()
        self.assertEqual(outcome.returncode, 2); self.assertIn("final-frame verdict does not match violations", outcome.stderr)
        self.assertFalse(self.report.exists())

    def test_na_blocking_evidence_writes_a_failing_report(self):
        fragment = bind_fragment(passing_fragment("gif"), self.gif)
        row = next(f for f in fragment["findings"] if f["severity"] == "blocking")
        row.update(status="NA", measured=None, detail="probe unavailable"); self.fragments["gif"].write_text(json.dumps(fragment))
        outcome = self.run_merge(); self.assertEqual(outcome.returncode, 1, outcome.stderr)

    def test_missing_blocking_evidence_is_materialized_and_fails(self):
        fragment = bind_fragment(passing_fragment("still"), self.html)
        missing = next(f for f in fragment["findings"] if f["severity"] == "blocking")
        fragment["findings"].remove(missing); self.fragments["still"].write_text(json.dumps(fragment))
        outcome = self.run_merge(); self.assertEqual(outcome.returncode, 1, outcome.stderr)
        report = json.loads(self.report.read_text()); row = next(f for f in report["findings"] if f["threshold_id"] == missing["threshold_id"])
        self.assertEqual(row["status"], "NA")

    def test_missing_fragment_stops_without_claiming_a_report(self):
        self.fragments["still"] = self.root / "missing.json"; outcome = self.run_merge()
        self.assertEqual(outcome.returncode, 2); self.assertFalse(self.report.exists())

    def test_missing_sidecar_stops_without_claiming_a_report(self):
        self.final_frame = self.root / "missing-final-frame.json"; outcome = self.run_merge()
        self.assertEqual(outcome.returncode, 2); self.assertFalse(self.report.exists())

    def test_stale_contract_metadata_is_rejected(self):
        fragment = bind_fragment(passing_fragment("gif"), self.gif); row = fragment["findings"][0]
        row["severity"] = "blocking" if row["severity"] == "advisory" else "advisory"; row["threshold"] += 1
        self.fragments["gif"].write_text(json.dumps(fragment)); outcome = self.run_merge()
        self.assertEqual(outcome.returncode, 2); self.assertIn("contract metadata", outcome.stderr)

    def test_threshold_from_wrong_stage_is_rejected(self):
        still = bind_fragment(passing_fragment("still"), self.html); misplaced = still["findings"].pop()
        artboard = bind_fragment(passing_fragment("artboard"), self.html); artboard["findings"].append(misplaced)
        self.fragments["still"].write_text(json.dumps(still)); self.fragments["artboard"].write_text(json.dumps(artboard))
        outcome = self.run_merge(); self.assertEqual(outcome.returncode, 2); self.assertIn("does not belong", outcome.stderr)

    def test_declared_pass_must_match_measurement(self):
        fragment = json.loads(self.fragments["artboard"].read_text()); row = next(r for r in fragment["findings"] if r["threshold_id"] == "artboard.width")
        row["measured"] = 1; self.fragments["artboard"].write_text(json.dumps(fragment)); outcome = self.run_merge()
        self.assertEqual(outcome.returncode, 2); self.assertIn("status does not match measurement", outcome.stderr)

    def test_fragment_digest_must_match_current_artifact(self):
        self.html.write_bytes(b"<html>changed after measurement</html>"); outcome = self.run_merge()
        self.assertEqual(outcome.returncode, 2); self.assertIn("artifact digest", outcome.stderr)

    def test_final_frame_digest_must_match_current_artifact(self):
        fragment = bind_fragment(sidecar_fragment("final-frame"), self.html)
        self.html.write_bytes(b"<html>changed after final-frame measurement</html>"); self.final_frame.write_text(json.dumps(fragment))
        for kind in ("artboard", "still"):
            current = json.loads(self.fragments[kind].read_text()); bind_fragment(current, self.html); self.fragments[kind].write_text(json.dumps(current))
        overflow = json.loads(self.overflow.read_text()); bind_fragment(overflow, self.html); self.overflow.write_text(json.dumps(overflow))
        outcome = self.run_merge(); self.assertEqual(outcome.returncode, 2); self.assertIn("final-frame render fragment", outcome.stderr)


if __name__ == "__main__": unittest.main()
