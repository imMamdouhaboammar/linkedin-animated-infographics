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
FIXTURE = ROOT / 'tests' / 'fixtures' / 'text-overflow.html'
TOOLCHAIN_MARKERS = ('playwright is not installed', 'Chromium could not start', 'No Chrome build available')


class TextOverflowAuditTests(unittest.TestCase):
    def test_clipped_headline_fails_with_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / 'overflow.json'
            proc = subprocess.run(
                [sys.executable, str(AUDIT), str(FIXTURE), '--json', str(report)],
                capture_output=True, text=True, cwd=ROOT, timeout=180,
            )
            if any(marker in proc.stderr for marker in TOOLCHAIN_MARKERS):
                self.skipTest(proc.stderr.strip())
            self.assertTrue(report.is_file(), proc.stderr)
            data = json.loads(report.read_text())
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(data['verdict'], 'FAIL')
            self.assertGreaterEqual(len(data['violations']), 1)
            joined = ' '.join(v['element'] for v in data['violations'])
            self.assertIn('headline', joined)


if __name__ == '__main__':
    unittest.main()
