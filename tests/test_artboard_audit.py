#!/usr/bin/env python3
"""Prove the artboard audit actually blocks.

A gate that cannot fail is documentation. These tests run the real audit against two
committed fixtures and assert on the exit code and the named gates, because that is
exactly what CI and `render-qa` depend on:

* ``tests/fixtures/artboard-min.html``        must pass and exit 0
* ``tests/fixtures/artboard-violations.html`` must fail and name every violated gate

The violations fixture carries one defect per blocking gate, so a regression here says
which gate stopped working rather than only that something did.

Requires Chromium. Skipped, never silently passed, when the browser is unavailable,
so a machine without the render toolchain cannot report these gates as verified.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
AUDIT = ROOT / "scripts" / "artboard_audit.py"

# Every gate the violations fixture is built to trip, by the threshold that trips it.
EXPECTED_FAILURES = {
    "footer.max_gap_px": "footer-detachment",
    "containment.max_border_depth": "nested-card-density",
    "type.absolute_floor_px": "feed-scale-legibility",
    "type.min_headline_px": "weak-visual-anchor",
    "type.max_clipped_load_bearing_nodes": "text-clipping",
    "contrast.text_min_ratio": "contrast-floor",
}

TOOLCHAIN_MARKERS = ("playwright is not installed", "Chromium could not start",
                     "No Chrome build available")


def run_audit(fixture: str) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "audit.json"
        proc = subprocess.run(
            [sys.executable, str(AUDIT), str(FIXTURES / fixture),
             "--json", str(report), "--quiet"],
            capture_output=True, text=True, cwd=ROOT, timeout=180,
        )
        if any(marker in proc.stderr for marker in TOOLCHAIN_MARKERS):
            raise unittest.SkipTest(f"render toolchain unavailable: {proc.stderr.strip()}")
        if not report.is_file():
            raise AssertionError(
                f"audit produced no report for {fixture}\n"
                f"exit={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}")
        return proc.returncode, json.loads(report.read_text())


class CompliantArtboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.code, cls.report = run_audit("artboard-min.html")

    def test_compliant_fixture_exits_zero(self):
        self.assertEqual(self.code, 0,
                         f"compliant fixture failed: {self.report['summary']}")

    def test_compliant_fixture_has_no_failures_or_warnings(self):
        counts = self.report["summary"]["counts"]
        self.assertEqual(counts["FAIL"], 0, self.report["summary"]["failed_gates"])
        self.assertEqual(counts["WARN"], 0, self.report["summary"]["warned_gates"])

    def test_nothing_was_skipped(self):
        """An NA row means a measurement did not happen, so the fixture proves nothing."""
        skipped = [row["threshold_id"] for row in self.report["findings"]
                   if row["status"] == "NA"]
        self.assertEqual(skipped, [], f"unmeasured thresholds: {skipped}")

    def test_report_records_its_capture_conditions(self):
        capture = self.report["capture"]
        for key in ("browser", "browser_version", "launch_mode", "viewport",
                    "seeked_at_s"):
            self.assertIn(key, capture)
        self.assertEqual(capture["viewport"], {"width": 1080, "height": 1350})

    def test_compliant_fixture_has_no_clipped_text(self):
        self.assertEqual(self.report["measurements"]["clipped_text_nodes"], 0)
        self.assertEqual(
            self.report["measurements"]["clipped_load_bearing_text_nodes"], 0)


class ViolatingArtboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.code, cls.report = run_audit("artboard-violations.html")

    def test_violating_fixture_exits_non_zero(self):
        self.assertEqual(self.code, 1, "a blocking violation did not fail the script")

    def test_every_planted_defect_is_caught(self):
        by_id = {row["threshold_id"]: row for row in self.report["findings"]}
        for threshold_id, gate in EXPECTED_FAILURES.items():
            with self.subTest(threshold=threshold_id):
                row = by_id.get(threshold_id)
                self.assertIsNotNone(row, f"{threshold_id} was never measured")
                self.assertEqual(row["status"], "FAIL",
                                 f"{threshold_id} measured {row['measured']} "
                                 f"against {row['threshold']} and did not fail")
                self.assertEqual(row["gate"], gate)

    def test_failed_gates_are_exactly_the_planted_ones(self):
        """No extra gates. An unexpected failure means the fixture drifted."""
        self.assertEqual(sorted(set(EXPECTED_FAILURES.values())),
                         self.report["summary"]["failed_gates"])

    def test_advisory_violation_warns_instead_of_failing(self):
        """61.5% occupancy is a real defect, but the band is advisory by contract."""
        row = next(r for r in self.report["findings"]
                   if r["threshold_id"] == "occupancy.min_pct")
        self.assertEqual(row["status"], "WARN")
        self.assertEqual(row["severity"], "advisory")

    def test_failures_carry_evidence(self):
        for row in self.report["findings"]:
            if row["status"] != "FAIL":
                continue
            with self.subTest(threshold=row["threshold_id"]):
                self.assertTrue(row["detail"], "a failure with no explanation")
                self.assertIsNotNone(row["measured"],
                                     "a failure with no measured value")

    def test_containment_failure_names_the_nesting_path(self):
        row = next(r for r in self.report["findings"]
                   if r["threshold_id"] == "containment.max_border_depth")
        self.assertIn("div.panel", row["evidence"][0])
        self.assertIn("div.inner", row["evidence"][0])

    def test_clipping_failure_names_rendered_box_dimensions(self):
        row = next(r for r in self.report["findings"]
                   if r["threshold_id"] == "type.max_clipped_load_bearing_nodes")
        self.assertGreaterEqual(row["measured"], 1)
        evidence = "\n".join(row["evidence"])
        self.assertIn("headline", evidence)
        self.assertIn("client=", evidence)
        self.assertIn("scroll=", evidence)
        self.assertGreaterEqual(
            self.report["measurements"]["clipped_load_bearing_text_nodes"], 1)


class RenderPipelineBrowserTests(unittest.TestCase):
    def test_all_render_stages_record_one_browser_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "post.gif"
            env = os.environ.copy()
            env["PATH"] = f"/opt/homebrew/bin:{env['PATH']}"

            # Allow up to 3 attempts to guard against transient CI browser contention.
            max_attempts = 3
            outcome = None
            for attempt in range(max_attempts):
                outcome = subprocess.run(
                    ["bash", str(ROOT / "scripts" / "render.sh"),
                     str(FIXTURES / "artboard-min.html"), str(output),
                     "--duration", "0.3", "--fps", "10", "--no-mobile"],
                    capture_output=True, text=True, cwd=ROOT, timeout=180, env=env,
                )
                if outcome.returncode == 0:
                    break
                if any(marker in outcome.stderr for marker in TOOLCHAIN_MARKERS):
                    self.skipTest(f"render toolchain unavailable: {outcome.stderr.strip()}")
                if attempt < max_attempts - 1:
                    time.sleep(1.0)

            self.assertIsNotNone(outcome)
            self.assertEqual(
                outcome.returncode, 0,
                f"Render pipeline failed with returncode {outcome.returncode}.\n"
                f"STDERR:\n{outcome.stderr}\nSTDOUT:\n{outcome.stdout}"
            )
            evidence = output.parent / ".render-evidence"
            fragments = [
                json.loads((evidence / name).read_text())
                for name in ("artboard.json", "still.json", "gif.json")
            ]
            browsers = {fragment["capture"]["browser"] for fragment in fragments}
            versions = {fragment["capture"]["browser_version"] for fragment in fragments}
            self.assertEqual(len(browsers), 1, browsers)
            self.assertEqual(len(versions), 1, versions)


if __name__ == "__main__":
    unittest.main()
