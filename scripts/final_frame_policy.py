#!/usr/bin/env python3
"""Apply deterministic final-frame visibility policy to browser evidence."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path

# Keep direct CLI execution consistent with the rest of the render scripts. When Python
# executes ``scripts/final_frame_policy.py`` directly, sys.path starts at ``scripts/``;
# add the repository root so package imports resolve the same way they do in unit tests.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.visual_contract import VisualContract

THRESHOLD_ID = "final_frame.min_visible_sample_ratio"


def rounded(value: float) -> float:
    return round(value, 3)


def contract_min_visible_sample_ratio() -> float:
    return float(VisualContract().value(THRESHOLD_ID))


def apply_policy(report: dict, min_visible_sample_ratio: float | None = None) -> dict:
    if not isinstance(report, Mapping):
        raise ValueError("final-frame report must be a JSON object")

    threshold = (
        contract_min_visible_sample_ratio()
        if min_visible_sample_ratio is None
        else min_visible_sample_ratio
    )
    if not 0 < threshold <= 1:
        raise ValueError("min-visible-sample-ratio must be > 0 and <= 1")

    required = report.get("required_visible_elements")
    violations = report.get("violations")
    if not isinstance(required, list) or not isinstance(violations, list):
        raise ValueError("final-frame report is missing required visibility evidence")
    if not all(isinstance(row, Mapping) for row in [*required, *violations]):
        raise ValueError("final-frame visibility evidence contains an invalid row")

    existing_elements = {
        row.get("element")
        for row in violations
        if row.get("reason") == "required-final-element-hidden"
    }

    for row in required:
        hit_test = row.get("hit_test") or {}
        if not isinstance(hit_test, Mapping):
            raise ValueError("final-frame hit-test evidence must be a JSON object")

        sample_count = int(hit_test.get("sample_count") or 0)
        visible_samples = int(hit_test.get("visible_samples") or 0)
        ratio = visible_samples / sample_count if sample_count > 0 else None
        row["visible_sample_ratio"] = rounded(ratio) if ratio is not None else None

        reasons = row.setdefault("reasons", [])
        if not isinstance(reasons, list):
            raise ValueError("final-frame visibility reasons must be a list")

        is_partial_occlusion = (
            ratio is not None
            and 0 < visible_samples < sample_count
            and ratio < threshold
        )
        if not is_partial_occlusion:
            continue

        if "partially-occluded" not in reasons:
            reasons.append("partially-occluded")

        if row.get("element") not in existing_elements:
            violations.append({
                **row,
                "reason": "required-final-element-hidden",
            })
            existing_elements.add(row.get("element"))

    report["final_frame_policy"] = {
        "threshold_id": THRESHOLD_ID,
        "min_visible_sample_ratio": threshold,
        "sampling_basis": "browser-hit-test",
    }
    report["verdict"] = "FAIL" if violations else "PASS"
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="final-frame JSON evidence to update in place")
    parser.add_argument(
        "--min-visible-sample-ratio",
        type=float,
        default=None,
        help="Override the visual-contract threshold for diagnostics only",
    )
    args = parser.parse_args(argv)

    path = Path(args.report)
    if not path.is_file():
        print(f"No such final-frame report: {path}", file=sys.stderr)
        return 2

    try:
        report = json.loads(path.read_text())
        apply_policy(report, args.min_visible_sample_ratio)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    violations = report["violations"]
    if violations:
        partial = sum(
            "partially-occluded" in row.get("reasons", [])
            for row in violations
            if row.get("reason") == "required-final-element-hidden"
        )
        print(
            "final-frame policy: FAIL "
            f"({len(violations)} violation(s), {partial} partial-occlusion violation(s))"
        )
        return 1

    threshold = report["final_frame_policy"]["min_visible_sample_ratio"]
    print(
        "final-frame policy: PASS "
        f"(minimum visible hit-test ratio {threshold:.0%})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
