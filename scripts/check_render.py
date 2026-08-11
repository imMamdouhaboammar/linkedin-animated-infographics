#!/usr/bin/env python3
"""Render a deterministic still and emit measured still/motion evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.render_probe import GEOMETRY_JS, MOTION_JS, open_artboard
from scripts.visual_contract import (
    ContractError,
    VisualContract,
    exit_code,
    finding,
    render_lines,
    skipped,
    summarize,
)


def still_findings(page, contract: VisualContract, margin: int) -> tuple[list[dict], dict]:
    geometry = page.evaluate(GEOMETRY_JS)
    motion = page.evaluate(MOTION_JS, margin)
    board = geometry.get("board")
    if not board:
        return [
            skipped(contract, "motion.max_moving_area_pct", geometry.get("error", "no artboard")),
            skipped(contract, "safe_margin_px", geometry.get("error", "no artboard")),
        ], {"geometry": geometry, "motion": motion}

    canvas = board["w"] * board["h"]
    moving_pct = 100.0 * motion["motionArea"] / canvas if canvas else 0.0
    margin_motion = motion["marginMotion"]
    clearance = motion["minClearance"]
    measured_clearance = margin if clearance is None else clearance
    findings = [
        finding(
            contract,
            "motion.max_moving_area_pct",
            ok=moving_pct <= contract.value("motion.max_moving_area_pct"),
            measured=round(moving_pct, 2),
            detail="" if moving_pct <= contract.value("motion.max_moving_area_pct")
            else "animated bounding boxes exceed the advisory area budget",
        ),
        finding(
            contract,
            "safe_margin_px",
            ok=not margin_motion,
            measured=measured_clearance,
            detail="no animated elements" if clearance is None else "" if not margin_motion else
            f"{len(margin_motion)} animated element(s) enter the safe margin",
            evidence=[f"<{row['tag']} class=\"{row['cls']}\">" for row in margin_motion[:6]],
        ),
    ]
    return findings, {"geometry": geometry, "motion": motion}


def save_mobile_preview(still: Path, width: int) -> Path | None:
    try:
        from PIL import Image
    except ImportError:
        return None
    mobile = still.with_name(still.stem + f"_mobile{width}.png")
    with Image.open(still) as image:
        height = round(image.height * width / image.width)
        image.resize((width, height), Image.Resampling.LANCZOS).save(mobile)
    return mobile


def write_report(path: str, report: dict) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def main(argv=None) -> int:
    try:
        contract = VisualContract()
    except ContractError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html")
    parser.add_argument("--out", default="still.png")
    parser.add_argument("--json", dest="json_out", default=None)
    parser.add_argument("--at", type=float, default=0.0)
    parser.add_argument("--selector", default="#artboard")
    parser.add_argument("--width", type=int, default=contract.int_value("artboard.width"))
    parser.add_argument("--height", type=int, default=contract.int_value("artboard.height"))
    parser.add_argument("--margin", type=int, default=contract.int_value("safe_margin_px"))
    parser.add_argument("--browser", default=None)
    mobile = parser.add_mutually_exclusive_group()
    mobile.add_argument("--mobile", dest="mobile", action="store_true")
    mobile.add_argument("--no-mobile", dest="mobile", action="store_false")
    parser.set_defaults(mobile=True)
    args = parser.parse_args(argv)

    still = Path(args.out)
    still.parent.mkdir(parents=True, exist_ok=True)
    with open_artboard(
        args.html,
        width=args.width,
        height=args.height,
        at=args.at,
        browser=args.browser,
    ) as (page, capture):
        findings, measurements = still_findings(page, contract, args.margin)
        target = page.query_selector(args.selector)
        (target or page).screenshot(path=str(still))

    feed_width = contract.int_value("type.feed_width_px")
    mobile_path = save_mobile_preview(still, feed_width) if args.mobile else None
    if args.mobile:
        findings.append(
            finding(contract, "type.feed_width_px", ok=mobile_path is not None,
                    measured=feed_width if mobile_path else None,
                    detail="" if mobile_path else "Pillow unavailable; no mobile preview")
        )
    else:
        findings.append(skipped(contract, "type.feed_width_px", "disabled by --no-mobile"))

    summary = summarize(findings)
    report = {
        "schema_version": 1,
        "stage": "still",
        "artifact": str(Path(args.html).resolve()),
        "capture": capture,
        "outputs": {
            "still": str(still.resolve()),
            "mobile": str(mobile_path.resolve()) if mobile_path else None,
        },
        "verdict": summary["verdict"],
        "summary": summary,
        "findings": findings,
        "measurements": measurements,
    }
    if args.json_out:
        write_report(args.json_out, report)

    print("── still audit ──────────────────────────────")
    print("\n".join(render_lines(findings)))
    print(f"── verdict: {summary['verdict']}")
    print(f"  still           {still}")
    if mobile_path:
        print(f"  mobile preview  {mobile_path}")
    if args.json_out:
        print(f"  report          {args.json_out}")
    return exit_code(findings)


if __name__ == "__main__":
    raise SystemExit(main())
