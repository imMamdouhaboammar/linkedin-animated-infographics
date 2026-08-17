#!/usr/bin/env python3
"""Adversarial browser tests for text clipping semantics."""

import unittest
from pathlib import Path

from scripts.artboard_audit import CLIPPING_JS, LOAD_BEARING_HINTS
from scripts.render_probe import open_artboard

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
REAL_MOTION_EXAMPLE = ROOT / "examples" / "motion" / "roas-reality-check.html"
TOOLCHAIN_MARKERS = (
    "playwright is not installed",
    "Chromium could not start",
    "No Chrome build available",
)


def probe(path: Path, *, at: float = 0.0) -> dict:
    try:
        with open_artboard(path, width=1080, height=1350, at=at, settle=0) as (page, _):
            return page.evaluate(CLIPPING_JS, list(LOAD_BEARING_HINTS))
    except SystemExit as exc:
        message = str(exc)
        if any(marker in message for marker in TOOLCHAIN_MARKERS):
            raise unittest.SkipTest(f"render toolchain unavailable: {message}") from exc
        raise


class TextClippingProbeTests(unittest.TestCase):
    def test_visible_overflow_is_not_reported_as_clipping(self):
        result = probe(FIXTURES / "artboard-visible-overflow.html")
        self.assertIsNone(result["error"])
        self.assertEqual([], result["nodes"], result)

    def test_real_motion_example_has_no_load_bearing_clipping_across_story_states(self):
        for timestamp in (0.0, 1.2, 2.4, 3.6):
            with self.subTest(timestamp=timestamp):
                result = probe(REAL_MOTION_EXAMPLE, at=timestamp)
                self.assertIsNone(result["error"])
                clipped = [node for node in result["nodes"] if node.get("load_bearing")]
                self.assertEqual([], clipped, result)


if __name__ == "__main__":
    unittest.main()
