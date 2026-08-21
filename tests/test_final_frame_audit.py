#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "final_frame_audit.py"
FIXTURES = ROOT / "tests" / "fixtures"
TOOLCHAIN_MARKERS = (
    "playwright is not installed",
    "Chromium could not start",
    "No Chrome build available",
)


def run_audit(fixture: str) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "final-frame.json"
        proc = subprocess.run(
            [
                sys.executable,
                str(AUDIT),
                str(FIXTURES / fixture),
                "--duration", "4",
                "--fps", "10",
                "--json", str(report),
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=180,
        )
        if any(marker in proc.stderr for marker in TOOLCHAIN_MARKERS):
            raise unittest.SkipTest(proc.stderr.strip())
        if not report.is_file():
            raise AssertionError(f"final-frame audit produced no report: {proc.stderr}")
        return proc.returncode, json.loads(report.read_text())


class FinalFrameAuditTests(unittest.TestCase):
    def test_completed_finite_animation_passes_and_infinite_loop_is_ignored(self):
        code, data = run_audit("final-frame-pass.html")
        self.assertEqual(code, 0, data)
        self.assertEqual(data["verdict"], "PASS")
        self.assertEqual(data["violations"], [])
        self.assertEqual(data["frames"], 40)
        self.assertEqual(data["final_sample_ms"], 3900.0)
        self.assertEqual(len(data["finite_animations"]), 1)

    def test_animation_that_only_finishes_at_loop_endpoint_fails(self):
        code, data = run_audit("final-frame-fail.html")
        self.assertEqual(code, 1, data)
        self.assertEqual(data["verdict"], "FAIL")
        self.assertEqual(len(data["violations"]), 1)
        violation = data["violations"][0]
        self.assertEqual(violation["reason"], "finite-animation-incomplete")
        self.assertIn("headline", violation["element"])
        self.assertAlmostEqual(violation["remaining_ms"], 100.0, places=1)
        self.assertLess(violation["progress"], 1)


if __name__ == "__main__":
    unittest.main()
