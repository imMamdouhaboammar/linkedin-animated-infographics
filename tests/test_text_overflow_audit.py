#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'scripts' / 'text_overflow_audit.py'
FIXTURES = ROOT / 'tests' / 'fixtures'
TOOLCHAIN_MARKERS = ('playwright is not installed', 'Chromium could not start', 'No Chrome build available')


def run_audit(fixture: str) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / 'overflow.json'
        proc = subprocess.run(
            [sys.executable, str(AUDIT), str(FIXTURES / fixture), '--json', str(report)],
            capture_output=True, text=True, cwd=ROOT, timeout=180,
        )
        if any(marker in proc.stderr for marker in TOOLCHAIN_MARKERS):
            raise unittest.SkipTest(proc.stderr.strip())
        if not report.is_file():
            raise AssertionError(f'overflow audit produced no report: {proc.stderr}')
        return proc.returncode, json.loads(report.read_text())


class TextOverflowAuditTests(unittest.TestCase):
    def test_clipped_headline_fails_with_evidence(self):
        code, data = run_audit('text-overflow.html')
        self.assertEqual(code, 1)
        self.assertEqual(data['verdict'], 'FAIL')
        self.assertGreaterEqual(len(data['violations']), 1)
        joined = ' '.join(v['element'] for v in data['violations'])
        self.assertIn('headline', joined)
        reasons = ' '.join(r for v in data['violations'] for r in v['reasons'])
        self.assertIn('clipped-x', reasons)

    def test_compliant_artboard_has_no_overflow_false_positive(self):
        code, data = run_audit('artboard-min.html')
        self.assertEqual(code, 0, data['violations'])
        self.assertEqual(data['verdict'], 'PASS')
        self.assertEqual(data['violations'], [])


if __name__ == '__main__':
    unittest.main()
