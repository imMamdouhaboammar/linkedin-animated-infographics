#!/usr/bin/env python3
from __future__ import annotations

import unittest

from scripts.render_report import final_frame_finding


class FinalFrameClippingReportTests(unittest.TestCase):
    def test_clipping_measurements_are_preserved_in_merged_evidence(self):
        fragment = {
            "violations": [
                {
                    "element": "div.headline",
                    "reason": "required-final-element-hidden",
                    "reasons": ["clipped-by-export-root"],
                    "rect": {"x": 100, "y": 1310, "width": 700, "height": 100},
                    "visible_ratio": 0.4,
                    "clipping": {"left_px": 0, "right_px": 0, "top_px": 0, "bottom_px": 60},
                }
            ]
        }

        finding = final_frame_finding(fragment)

        self.assertEqual(finding["status"], "FAIL")
        evidence = finding["evidence"][0]
        self.assertEqual(evidence["reasons"], ["clipped-by-export-root"])
        self.assertEqual(evidence["visible_ratio"], 0.4)
        self.assertEqual(evidence["clipping"]["bottom_px"], 60)


if __name__ == "__main__":
    unittest.main()
