#!/usr/bin/env python3
"""
artboard_audit.py — measure the visual quality contract on a built artboard.

This is the gate that `check_render.py` never was. `check_render.py` prints an audit and
always exits 0, so its numbers are advice. This script compares measurements against
`helper/visual-contract.json` and exits non-zero when a blocking threshold fails, which
is what lets `render-qa` return a real HOLD instead of a narrated one.

What it measures, and why each one needs a browser rather than a grep:

  occupancy          vertical span of real content over the artboard height
  footer detachment  gap between the end of the primary composition and the footer
  containment depth  nested bordered surfaces, counted from every leaf upward
  type floors        rendered font sizes, after cascade and fallback
  rendered contrast  text against its composited background, including alpha
  fonts              whether each stack's first choice actually resolved

Gate ids match the failure taxonomy already used by the OpenAI runtime
(`bottom-dead-zone`, `footer-detachment`, `nested-card-density`, `feed-scale-legibility`),
so both hosts speak one vocabulary.

Usage:
    python3 artboard_audit.py build/post.html
    python3 artboard_audit.py build/post.html --json build/artboard-audit.json
    python3 artboard_audit.py build/post.html --exception-reason "sparse concept, negative space is the point"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.info_stories import contrast_ratio
from scripts.render_probe import FONT_JS, GEOMETRY_JS, TYPE_JS, open_artboard
from scripts.visual_contract import (
    ContractError,
    VisualContract,
    exit_code,
    finding,
    render_lines,
    skipped,
    summarize,
)

# Roles whose text is load-bearing by convention. Text in these is judged against the
# feed floor even when the script cannot otherwise tell load-bearing from decorative.
LOAD_BEARING_HINTS = ("headline", "hero", "title", "takeaway", "subline", "lede", "kicker")


def audit(page, contract: VisualContract, *, exception_reason: str = "") -> tuple[list[dict], dict]:
    geometry = page.evaluate(GEOMETRY_JS)
    typography = page.evaluate(TYPE_JS)
    fonts = page.evaluate(FONT_JS)

    findings: list[dict] = []
    if geometry.get("error"):
        for tid in ("artboard.width", "artboard.height", "occupancy.min_pct",
                    "occupancy.max_pct", "footer.max_gap_px",
                    "containment.max_border_depth"):
            findings.append(skipped(contract, tid, geometry["error"]))
        return findings, {"geometry": geometry, "typography": typography, "fonts": fonts}

    board = geometry["board"]

    findings.append(finding(
        contract, "artboard.width", ok=board["w"] == contract.value("artboard.width"),
        measured=board["w"], detail="" if board["w"] == contract.value("artboard.width")
        else "artboard is not the declared canvas width",
    ))
    findings.append(finding(
        contract, "artboard.height", ok=board["h"] == contract.value("artboard.height"),
        measured=board["h"], detail="" if board["h"] == contract.value("artboard.height")
        else "artboard is not the declared canvas height",
    ))

    content = geometry.get("content") or {}
    occupancy = content.get("occupancy_pct")
    if occupancy is None:
        findings.append(skipped(contract, "occupancy.min_pct", "no content measured"))
        findings.append(skipped(contract, "occupancy.max_pct", "no content measured"))
    else:
        findings.append(finding(
            contract, "occupancy.min_pct",
            ok=occupancy >= contract.value("occupancy.min_pct"),
            measured=occupancy,
            detail="" if occupancy >= contract.value("occupancy.min_pct")
            else "composition ends early; confirm the negative space has a job",
            evidence=[f"content spans y={content['top']}..{content['bottom']}"],
        ))
        findings.append(finding(
            contract, "occupancy.max_pct",
            ok=occupancy <= contract.value("occupancy.max_pct"),
            measured=occupancy,
            detail="" if occupancy <= contract.value("occupancy.max_pct")
            else "composition is crowding its own margins",
        ))

    footer = geometry.get("footer")
    if not footer or footer.get("gap_px") is None:
        findings.append(skipped(contract, "footer.max_gap_px",
                                "no footer block identified"))
    else:
        gap = footer["gap_px"]
        limit = contract.value("footer.max_gap_px")
        excused = bool(exception_reason) and gap > limit
        findings.append(finding(
            contract, "footer.max_gap_px", ok=gap <= limit or excused, measured=gap,
            detail=(f"excused: {exception_reason}" if excused else
                    "" if gap <= limit else
                    "footer is detached from the composition above it"),
            evidence=[f"footer <{footer['tag']} class=\"{footer['cls']}\"> "
                      f"top y={footer['top']}"],
        ))

    depth = geometry.get("containment", 0)
    limit = contract.value("containment.max_border_depth")
    findings.append(finding(
        contract, "containment.max_border_depth", ok=depth <= limit, measured=depth,
        detail="" if depth <= limit else "bordered surfaces nested too deeply",
        evidence=[geometry.get("deepest", "")] if geometry.get("deepest") else [],
    ))

    nodes = typography.get("nodes", [])
    if not nodes:
        for tid in ("type.absolute_floor_px", "type.min_headline_px",
                    "type.feed_floor_px", "contrast.text_min_ratio"):
            findings.append(skipped(contract, tid, "no rendered text found"))
    else:
        findings.extend(_type_findings(contract, nodes))
        findings.append(_contrast_finding(contract, nodes))

    findings.append(_font_finding(contract, fonts))
    return findings, {"geometry": geometry, "typography": typography, "fonts": fonts}


def _type_findings(contract: VisualContract, nodes: list[dict]) -> list[dict]:
    absolute = contract.value("type.absolute_floor_px")
    below_absolute = [n for n in nodes if n["size"] < absolute]
    rows = [finding(
        contract, "type.absolute_floor_px", ok=not below_absolute,
        measured=min(n["size"] for n in nodes),
        detail="" if not below_absolute else
        f"{len(below_absolute)} text node(s) below the absolute floor",
        evidence=[f"{n['size']}px {n['sample']!r}" for n in below_absolute[:6]],
    )]

    largest = max(n["size"] for n in nodes)
    minimum_headline = contract.value("type.min_headline_px")
    rows.append(finding(
        contract, "type.min_headline_px", ok=largest >= minimum_headline,
        measured=largest,
        detail="" if largest >= minimum_headline else
        "no dominant headline: the artboard has no type hierarchy",
    ))

    floor = contract.value("type.feed_floor_px")
    below_floor = [n for n in nodes if n["size"] < floor]
    load_bearing = [
        n for n in below_floor
        if any(hint in (n["cls"] + " " + n["tag"]).lower() for hint in LOAD_BEARING_HINTS)
    ]
    rows.append(finding(
        contract, "type.feed_floor_px", ok=not below_floor,
        measured=min(n["size"] for n in nodes),
        detail=(f"{len(below_floor)} node(s) below the feed floor"
                + (f", {len(load_bearing)} in a load-bearing role" if load_bearing else "")
                + " — micro labels and card body may stay, load-bearing text may not")
        if below_floor else "",
        evidence=[f"{n['size']}px <{n['tag']} class=\"{n['cls']}\"> {n['sample']!r}"
                  for n in sorted(below_floor, key=lambda n: n["size"])[:8]],
    ))
    return rows


def _contrast_finding(contract: VisualContract, nodes: list[dict]) -> dict:
    floor = contract.value("contrast.text_min_ratio")
    worst = None
    violations = []
    for node in nodes:
        try:
            ratio = contrast_ratio(node["fg"], node["bg"])
        except ValueError:
            continue
        node["contrast"] = round(ratio, 2)
        if worst is None or ratio < worst:
            worst = ratio
        if ratio < floor:
            violations.append((ratio, node))
    if worst is None:
        return skipped(contract, "contrast.text_min_ratio", "no parseable text colours")
    violations.sort(key=lambda pair: pair[0])
    return finding(
        contract, "contrast.text_min_ratio", ok=not violations, measured=round(worst, 2),
        detail="" if not violations else
        f"{len(violations)} text node(s) below the rendered contrast floor",
        evidence=[f"{ratio:.2f}:1 {node['fg']} on {node['bg']} "
                  f"({node['size']}px {node['sample']!r})"
                  for ratio, node in violations[:8]],
    )


def _font_finding(contract: VisualContract, fonts: dict) -> dict:
    """Record which font stacks actually resolved to their first choice.

    Advisory by contract: a fallback face can be acceptable, but a silent substitution
    invalidates every type measurement above it, so the resolved family is always named.
    """
    stacks = fonts.get("stacks", [])
    if not stacks:
        return skipped(contract, "fonts.first_choice_available", "no font stacks found")
    missing = [s for s in stacks if s.get("first_available") is False]
    row = finding(
        contract, "fonts.first_choice_available", ok=not missing,
        measured=len(stacks) - len(missing),
        detail="" if not missing else
        f"{len(missing)} of {len(stacks)} stack(s) fell back: rendered type is not "
        f"the designed type on this machine",
        evidence=[f"{s['first']!r} unavailable, resolved to {s['resolved']!r}"
                  for s in missing[:6]],
    )
    return row


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="write the machine-readable audit to this path")
    ap.add_argument("--at", type=float, default=0.0,
                    help="seek every animation to this time before measuring")
    ap.add_argument("--width", type=int, default=None)
    ap.add_argument("--height", type=int, default=None)
    ap.add_argument("--browser", default=None,
                    help="path to a Chrome/Chromium binary")
    ap.add_argument("--exception-reason", default="",
                    help="documented reason that excuses a footer gap over the limit")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress the human-readable audit")
    args = ap.parse_args(argv)

    try:
        contract = VisualContract()
    except ContractError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    width = args.width or contract.int_value("artboard.width")
    height = args.height or contract.int_value("artboard.height")

    with open_artboard(args.html, width=width, height=height, at=args.at,
                       browser=args.browser) as (page, info):
        findings, raw = audit(page, contract, exception_reason=args.exception_reason)

    summary = summarize(findings)
    report = {
        "schema_version": 1,
        "stage": "artboard",
        "artifact": str(Path(args.html).resolve()),
        "seeked_at_s": args.at,
        "capture": info,
        "verdict": summary["verdict"],
        "summary": summary,
        "findings": findings,
        "measurements": {
            "board": raw["geometry"].get("board"),
            "content": raw["geometry"].get("content"),
            "footer": raw["geometry"].get("footer"),
            "containment_depth": raw["geometry"].get("containment"),
            "containment_path": raw["geometry"].get("deepest"),
            "text_nodes": len(raw["typography"].get("nodes", [])),
            "font_stacks": raw["fonts"].get("stacks", []),
        },
    }

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    if not args.quiet:
        print("── artboard audit ───────────────────────────")
        print(f"  browser         {info['browser']} ({info['browser_version']})")
        print(f"  seeked at       {args.at}s")
        print("\n".join(render_lines(findings)))
        print(f"── verdict: {summary['verdict']} "
              f"({summary['counts']['PASS']} pass, {summary['counts']['FAIL']} fail, "
              f"{summary['counts']['WARN']} warn, {summary['counts']['NA']} n/a)")
        for row in findings:
            if row["status"] in ("FAIL", "WARN") and row["evidence"]:
                print(f"\n  {row['status']} {row['threshold_id']} — {row['detail']}")
                for item in row["evidence"]:
                    print(f"    {item}")
        if args.json_out:
            print(f"\n  report          {args.json_out}")

    return exit_code(findings)


if __name__ == "__main__":
    raise SystemExit(main())
