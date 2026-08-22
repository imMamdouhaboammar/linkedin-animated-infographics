#!/usr/bin/env python3
"""Merge measured render evidence into one fail-closed report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.visual_contract import (
    ADVISORY, BLOCKING, FAIL, NA, PASS, WARN, ContractError, VisualContract,
    file_sha256, skipped, summarize,
)

FRAGMENT_PRODUCERS = {
    "artboard": "scripts/artboard_audit.py",
    "still": "scripts/check_render.py",
    "gif": "scripts/build_gif.py",
}
OVERFLOW_KIND = "text-overflow"
FINAL_FRAME_KIND = "final-frame"
ROW_FIELDS = {
    "threshold_id", "gate", "severity", "status", "measured", "threshold",
    "unit", "detail", "evidence",
}


def digest(path: Path) -> dict:
    return {"path": str(path.resolve()), "sha256": file_sha256(path)}


def _measurement_passes(row: dict, threshold: dict) -> bool:
    measured = row["measured"]
    if not isinstance(measured, (int, float)) or isinstance(measured, bool):
        raise ValueError(f"non-numeric measurement for {row['threshold_id']}")
    comparison = threshold["comparison"]
    if comparison == "eq": return measured == threshold["value"]
    if comparison == "min": return measured >= threshold["value"]
    if comparison == "max": return measured <= threshold["value"]
    raise ValueError(f"invalid comparison for {row['threshold_id']}")


def read_fragment(path: Path, kind: str, contract: VisualContract) -> dict:
    if not path.is_file(): raise ValueError(f"missing render fragment: {path}")
    try: fragment = json.loads(path.read_text())
    except json.JSONDecodeError as exc: raise ValueError(f"invalid render fragment {path}: {exc}") from exc
    if fragment.get("schema_version") != 1: raise ValueError(f"unsupported render fragment schema: {path}")
    if fragment.get("stage") != kind: raise ValueError(f"render fragment stage is not {kind}: {path}")
    if not isinstance(fragment.get("artifact"), str) or not fragment["artifact"]: raise ValueError(f"render fragment has no artifact metadata: {path}")
    artifact_sha256 = fragment.get("artifact_sha256")
    if not isinstance(artifact_sha256, str) or len(artifact_sha256) != 64: raise ValueError(f"render fragment has no artifact digest: {path}")
    findings = fragment.get("findings")
    if not isinstance(findings, list): raise ValueError(f"render fragment has no findings list: {path}")
    seen = set()
    for row in findings:
        missing = ROW_FIELDS - row.keys() if isinstance(row, dict) else ROW_FIELDS
        if missing: raise ValueError(f"render fragment row missing {sorted(missing)}: {path}")
        threshold_id = row["threshold_id"]
        if threshold_id in seen: raise ValueError(f"duplicate threshold {threshold_id} in {kind} fragment")
        seen.add(threshold_id)
        try: threshold = contract.threshold(threshold_id)
        except ContractError as exc: raise ValueError(f"unknown threshold {threshold_id} in {kind} fragment") from exc
        if threshold["measured_by"] != FRAGMENT_PRODUCERS[kind]: raise ValueError(f"threshold {threshold_id} does not belong to {kind} fragment")
        canonical = {key: threshold[key] for key in ("gate", "severity", "value", "unit")}
        declared = {"gate": row["gate"], "severity": row["severity"], "value": row["threshold"], "unit": row["unit"]}
        if declared != canonical: raise ValueError(f"contract metadata drift for {threshold_id} in {kind} fragment")
        allowed = {PASS, FAIL, NA} if threshold["severity"] == BLOCKING else {PASS, WARN, NA}
        if row["status"] not in allowed or threshold["severity"] not in {BLOCKING, ADVISORY}: raise ValueError(f"invalid status for {threshold_id} in {kind} fragment")
        if row["status"] == NA:
            if row["measured"] is not None: raise ValueError(f"NA row has a measurement for {threshold_id}")
            continue
        passes = _measurement_passes(row, threshold)
        if threshold.get("exception_field") and row.get("exception_applied") is True and isinstance(row["detail"], str) and row["detail"].startswith("excused: "): passes = True
        expected = PASS if passes else FAIL if threshold["severity"] == BLOCKING else WARN
        if row["status"] != expected: raise ValueError(f"status does not match measurement for {threshold_id}")
    return fragment


def read_sidecar_fragment(path: Path, kind: str) -> dict:
    if not path.is_file(): raise ValueError(f"missing render fragment: {path}")
    try: fragment = json.loads(path.read_text())
    except json.JSONDecodeError as exc: raise ValueError(f"invalid render fragment {path}: {exc}") from exc
    if fragment.get("schema_version") != 1: raise ValueError(f"unsupported render fragment schema: {path}")
    if fragment.get("stage") != kind: raise ValueError(f"render fragment stage is not {kind}: {path}")
    if not isinstance(fragment.get("artifact"), str) or not fragment["artifact"]: raise ValueError(f"render fragment has no artifact metadata: {path}")
    artifact_sha256 = fragment.get("artifact_sha256")
    if not isinstance(artifact_sha256, str) or len(artifact_sha256) != 64: raise ValueError(f"render fragment has no artifact digest: {path}")
    violations = fragment.get("violations")
    if not isinstance(violations, list): raise ValueError(f"{kind} fragment has no violations list: {path}")
    expected = FAIL if violations else PASS
    if fragment.get("verdict") != expected: raise ValueError(f"{kind} verdict does not match violations")
    return fragment


def overflow_finding(fragment: dict) -> dict:
    violations = fragment["violations"]
    evidence = [{"element": r.get("element"), "sample": r.get("sample"), "reasons": r.get("reasons", []), "text_rect": r.get("text_rect")} for r in violations[:8] if isinstance(r, dict)]
    return {
        "threshold_id": "text.visible_nodes", "gate": OVERFLOW_KIND, "severity": BLOCKING,
        "status": FAIL if violations else PASS, "measured": len(violations), "threshold": 0,
        "unit": "violations",
        "detail": f"{len(violations)} rendered text node(s) clipped or outside the artboard" if violations else "no clipped or overflowing rendered text detected",
        "evidence": evidence,
    }


def final_frame_finding(fragment: dict) -> dict:
    violations = fragment["violations"]
    evidence = [{"element": r.get("element"), "animation": r.get("animation"), "remaining_ms": r.get("remaining_ms"), "reason": r.get("reason")} for r in violations[:8] if isinstance(r, dict)]
    return {
        "threshold_id": "motion.final_frame_complete", "gate": FINAL_FRAME_KIND, "severity": BLOCKING,
        "status": FAIL if violations else PASS, "measured": len(violations), "threshold": 0,
        "unit": "violations",
        "detail": f"{len(violations)} finite animation(s) unfinished on the last exported frame" if violations else "all finite animations in the exported subtree complete by the last frame",
        "evidence": evidence,
    }


def merge_fragments(paths: dict[str, Path], overflow_path: Path, final_frame_path: Path, input_path: Path, output_path: Path) -> dict:
    contract = VisualContract()
    fragments = {kind: read_fragment(path, kind, contract) for kind, path in paths.items()}
    overflow = read_sidecar_fragment(overflow_path, OVERFLOW_KIND)
    final_frame = read_sidecar_fragment(final_frame_path, FINAL_FRAME_KIND)
    expected_artifacts = {"artboard": input_path.resolve(), "still": input_path.resolve(), "gif": output_path.resolve()}
    for kind, fragment in fragments.items():
        if Path(fragment["artifact"]).resolve() != expected_artifacts[kind]: raise ValueError(f"stale artifact metadata in {kind} render fragment")
        if fragment["artifact_sha256"] != file_sha256(expected_artifacts[kind]): raise ValueError(f"stale artifact digest in {kind} render fragment")
    for kind, fragment in ((OVERFLOW_KIND, overflow), (FINAL_FRAME_KIND, final_frame)):
        if Path(fragment["artifact"]).resolve() != input_path.resolve(): raise ValueError(f"stale artifact metadata in {kind} render fragment")
        if fragment["artifact_sha256"] != file_sha256(input_path): raise ValueError(f"stale artifact digest in {kind} render fragment")

    findings = [row for fragment in fragments.values() for row in fragment["findings"]]
    for kind, producer in FRAGMENT_PRODUCERS.items():
        present = {row["threshold_id"] for row in fragments[kind]["findings"]}
        for threshold_id, threshold in contract.thresholds.items():
            if threshold["measured_by"] == producer and threshold_id not in present:
                findings.append(skipped(contract, threshold_id, f"missing from {kind} render fragment"))
    findings.extend([overflow_finding(overflow), final_frame_finding(final_frame)])

    summary = summarize(findings)
    all_sources = {**fragments, OVERFLOW_KIND: overflow, FINAL_FRAME_KIND: final_frame}
    all_paths = {**paths, OVERFLOW_KIND: overflow_path, FINAL_FRAME_KIND: final_frame_path}
    return {
        "schema_version": 1, "verdict": summary["verdict"], "summary": summary, "findings": findings,
        "sources": {kind: {"path": str(all_paths[kind].resolve()), "verdict": fragment.get("verdict")} for kind, fragment in all_sources.items()},
        "digests": {"input": digest(input_path), "output": digest(output_path), "fragments": {kind: digest(path) for kind, path in all_paths.items()}},
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    merge = commands.add_parser("merge")
    for kind in FRAGMENT_PRODUCERS: merge.add_argument(f"--{kind}", required=True)
    merge.add_argument("--text-overflow", required=True)
    merge.add_argument("--final-frame", required=True)
    merge.add_argument("--input", required=True)
    merge.add_argument("--output", required=True)
    merge.add_argument("--out", default="build/render-report.json")
    args = parser.parse_args(argv)
    paths = {kind: Path(getattr(args, kind)) for kind in FRAGMENT_PRODUCERS}
    input_path, output_path = Path(args.input), Path(args.output)
    try:
        if not input_path.is_file() or not output_path.is_file():
            missing = input_path if not input_path.is_file() else output_path
            raise ValueError(f"missing render artifact: {missing}")
        report = merge_fragments(paths, Path(args.text_overflow), Path(args.final_frame), input_path, output_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"render report: {target} ({report['verdict']})")
    return 1 if report["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
