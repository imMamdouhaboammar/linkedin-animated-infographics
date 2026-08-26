#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

from scripts.final_frame_policy import apply_policy, contract_min_visible_sample_ratio


BASE = {
    "required_visible_elements": [
        {
            "element": "h1#headline",
            "reasons": [],
            "hit_test": {
                "sample_count": 5,
                "visible_samples": 5,
                "blockers": [],
            },
        }
    ],
    "violations": [],
    "verdict": "PASS",
}


class FinalFramePolicyTests(unittest.TestCase):
    def test_default_threshold_comes_from_visual_contract(self):
        self.assertEqual(contract_min_visible_sample_ratio(), 0.60)

    def test_fully_visible_required_element_passes(self):
        report = apply_policy(copy.deepcopy(BASE), 0.60)
        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["violations"], [])
        self.assertEqual(report["required_visible_elements"][0]["visible_sample_ratio"], 1.0)

    def test_two_of_five_visible_samples_fail_as_partial_occlusion(self):
        source = copy.deepcopy(BASE)
        source["required_visible_elements"][0]["hit_test"].update(
            visible_samples=2,
            blockers=["div.cover"],
        )
        report = apply_policy(source, 0.60)
        self.assertEqual(report["verdict"], "FAIL")
        self.assertEqual(len(report["violations"]), 1)
        violation = report["violations"][0]
        self.assertIn("partially-occluded", violation["reasons"])
        self.assertEqual(violation["visible_sample_ratio"], 0.4)
        self.assertIn("div.cover", violation["hit_test"]["blockers"])

    def test_three_of_five_visible_samples_meet_default_threshold(self):
        source = copy.deepcopy(BASE)
        source["required_visible_elements"][0]["hit_test"]["visible_samples"] = 3
        report = apply_policy(source, 0.60)
        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["violations"], [])
        self.assertEqual(report["required_visible_elements"][0]["visible_sample_ratio"], 0.6)

    def test_full_occlusion_is_not_duplicated(self):
        source = copy.deepcopy(BASE)
        row = source["required_visible_elements"][0]
        row["hit_test"]["visible_samples"] = 0
        row["reasons"] = ["occluded"]
        source["violations"] = [{**copy.deepcopy(row), "reason": "required-final-element-hidden"}]
        source["verdict"] = "FAIL"
        report = apply_policy(source, 0.60)
        self.assertEqual(report["verdict"], "FAIL")
        self.assertEqual(len(report["violations"]), 1)
        self.assertNotIn("partially-occluded", report["required_visible_elements"][0]["reasons"])

    def test_invalid_threshold_is_rejected(self):
        with self.assertRaises(ValueError):
            apply_policy(copy.deepcopy(BASE), 0)
        with self.assertRaises(ValueError):
            apply_policy(copy.deepcopy(BASE), 1.1)

    def test_non_object_root_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "JSON object"):
            apply_policy([], 0.60)

    def test_null_required_row_is_rejected(self):
        source = copy.deepcopy(BASE)
        source["required_visible_elements"] = [None]
        with self.assertRaisesRegex(ValueError, "invalid row"):
            apply_policy(source, 0.60)

    def test_non_object_hit_test_is_rejected(self):
        source = copy.deepcopy(BASE)
        source["required_visible_elements"][0]["hit_test"] = "broken"
        with self.assertRaisesRegex(ValueError, "hit-test evidence"):
            apply_policy(source, 0.60)


if __name__ == "__main__":
    unittest.main()
