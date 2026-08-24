#!/usr/bin/env python3
from __future__ import annotations

import unittest

from scripts.render_report import final_frame_finding


class FinalFrameOcclusionReportTests(unittest.TestCase):
    def test_hit_test_blockers_are_preserved_in_merged_evidence(self):
        fragment = {
            "violations": [
                {
                    "element": "div.headline",
                    "reason": "required-final-element-hidden",
                    "reasons": ["occluded"],
                    "rect": {"x": 120, "y": 180, "width": 760, "height": 142},
                    "visible_ratio": 1.0,
                    "clipping": {"left_px": 0, "right_px": 0, "top_px": 0, "bottom_px": 0},
                    "hit_test": {
                        "sample_count": 5,
                        "visible_samples": 0,
                        "blockers": ["div.cover"],
                    },
                }
            ]
        }

        finding = final_frame_finding(fragment)

        self.assertEqual(finding["status"], "FAIL")
        evidence = finding["evidence"][0]
        self.assertEqual(evidence["reasons"], ["occluded"])
        self.assertEqual(evidence["hit_test"]["visible_samples"], 0)
        self.assertEqual(evidence["hit_test"]["blockers"], ["div.cover"])


if __name__ == "__main__":
    unittest.main()
