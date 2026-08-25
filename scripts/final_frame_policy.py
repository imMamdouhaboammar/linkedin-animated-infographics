#!/usr/bin/env python3
"""Apply deterministic final-frame visibility policy to browser evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_MIN_VISIBLE_SAMPLE_RATIO = 0.60


def rounded(value: float) -> float:
    return round(value, 3)


def apply_policy(report: dict, min_visible_sample_ratio: float) -> dict:
    if not 0 < min_visible_sample_ratio <= 1:
        raise ValueError("min-visible-sample-ratio must be > 0 and <= 1")

    required = report.get("required_visible_elements")
    violations = report.get("violations")
    if not isinstance(required, list) or not isinstance(violations, list):
        raise ValueError("final-frame report is missing required visibility evidence")

    existing_elements = {
        row.get("element")
        for row in violations
        if row.get("reason") == "required-final-element-hidden"
    }

    for row in required:
        hit_test = row.get("hit_test") or {}
        sample_count = int(hit_test.get("sample_count") or 0)
        visible_samples = int(hit_test.get("visible_samples") or 0)
        ratio = visible_samples / sample_count if sample_count > 0 else None
        row["visible_sample_ratio"] = rounded(ratio) if ratio is not None else None

        reasons = row.setdefault("reasons", [])
        is_partial_occlusion = (
            ratio is not None
            and 0 < visible_samples < sample_count
            and ratio < min_visible_sample_ratio
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
        "min_visible_sample_ratio": min_visible_sample_ratio,
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
        default=DEFAULT_MIN_VISIBLE_SAMPLE_RATIO,
    )
    args = parser.parse_args(argv)

    path = Path(args.report)
    if not path.is_file():
        print(f"No such final-frame report: {path}", file=sys.stderr)
        return 2

    try:
        report = json.loads(path.read_text())
        apply_policy(report, args.min_visible_sample_ratio)
    except (ValueError, json.JSONDecodeError) as exc:
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

    print(
        "final-frame policy: PASS "
        f"(minimum visible hit-test ratio {args.min_visible_sample_ratio:.0%})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
