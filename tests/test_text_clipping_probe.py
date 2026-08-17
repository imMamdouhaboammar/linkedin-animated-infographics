#!/usr/bin/env python3
"""Adversarial browser tests for text clipping semantics."""

import unittest
from pathlib import Path

from scripts.artboard_audit import CLIPPING_JS, LOAD_BEARING_HINTS
from scripts.render_probe import open_artboard

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class TextClippingProbeTests(unittest.TestCase):
    def test_visible_overflow_is_not_reported_as_clipping(self):
        try:
            with open_artboard(
                FIXTURES / "artboard-visible-overflow.html",
                width=1080,
                height=1350,
                settle=0,
            ) as (page, _):
                result = page.evaluate(CLIPPING_JS, list(LOAD_BEARING_HINTS))
        except SystemExit as exc:
            message = str(exc)
            if any(marker in message for marker in (
                "playwright is not installed",
                "Chromium could not start",
                "No Chrome build available",
            )):
                self.skipTest(f"render toolchain unavailable: {message}")
            raise

        self.assertIsNone(result["error"])
        self.assertEqual([], result["nodes"], result)


if __name__ == "__main__":
    unittest.main()
