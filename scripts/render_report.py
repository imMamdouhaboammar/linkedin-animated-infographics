#!/usr/bin/env python3
"""Merge measured artboard, still, and GIF evidence into one fail-closed report."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.visual_contract import VisualContract, skipped, summarize

FRAGMENT_PRODUCERS = {
    "artboard": "scripts/artboard_audit.py",
    "still": "scripts/check_render.py",
    "gif": "scripts/build_gif.py",
}
ROW_FIELDS = {
    "threshold_id", "gate", "severity", "status", "measured", "threshold",
    "unit", "detail", "evidence",
}


def digest(path: Path) -> dict:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def read_fragment(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"missing render fragment: {path}")
    try:
        fragment = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid render fragment {path}: {exc}") from exc
    findings = fragment.get("findings")
    if not isinstance(findings, list):
        raise ValueError(f"render fragment has no findings list: {path}")
    for row in findings:
        missing = ROW_FIELDS - row.keys() if isinstance(row, dict) else ROW_FIELDS
        if missing:
            raise ValueError(f"render fragment row missing {sorted(missing)}: {path}")
    return fragment


def merge_fragments(paths: dict[str, Path], input_path: Path, output_path: Path) -> dict:
    contract = VisualContract()
    fragments = {kind: read_fragment(path) for kind, path in paths.items()}
    findings = [row for fragment in fragments.values() for row in fragment["findings"]]
    for kind, producer in FRAGMENT_PRODUCERS.items():
        present = {row["threshold_id"] for row in fragments[kind]["findings"]}
        for threshold_id, threshold in contract.thresholds.items():
            if threshold["measured_by"] == producer and threshold_id not in present:
                findings.append(skipped(
                    contract, threshold_id, f"missing from {kind} render fragment"))

    summary = summarize(findings)
    return {
        "schema_version": 1,
        "verdict": summary["verdict"],
        "summary": summary,
        "findings": findings,
        "sources": {
            kind: {"path": str(paths[kind].resolve()), "verdict": fragment.get("verdict")}
            for kind, fragment in fragments.items()
        },
        "digests": {
            "input": digest(input_path),
            "output": digest(output_path),
            "fragments": {kind: digest(path) for kind, path in paths.items()},
        },
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    merge = commands.add_parser("merge")
    for kind in FRAGMENT_PRODUCERS:
        merge.add_argument(f"--{kind}", required=True)
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
        report = merge_fragments(paths, input_path, output_path)
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
