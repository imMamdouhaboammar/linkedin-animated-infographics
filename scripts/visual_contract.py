#!/usr/bin/env python3
"""Load and apply the repository's measurable visual contract.

``helper/visual-contract.json`` is the base contract. Small feature-scoped additions can
live in ``helper/visual-contract.d/*.json``; they are merged deterministically and may not
replace an existing threshold or gate. The result is one logical contract consumed by all
render stages and tests.

Scripts must not hardcode a number that appears in the contract. They look it up, compare
a measured value against it, and record a finding carrying both numbers so the render
report can show the measurement beside the threshold that judged it.

Severity is part of the contract, not the caller's choice:

* ``blocking``  -> the measuring script exits non-zero
* ``advisory``  -> reported for the critic to judge, never fails the script

Some metrics are advisory on purpose. ``motion.max_moving_area_pct`` is the clearest
case: this repository's own measurements show a reference that moves ~85% of the canvas
encoding at an eighth of the per-frame cost of one that moves ~11%, so bounding-box
area cannot be a pass/fail gate.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "helper" / "visual-contract.json"
CONTRACT_FRAGMENTS = ROOT / "helper" / "visual-contract.d"

BLOCKING = "blocking"
ADVISORY = "advisory"
PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"
NA = "NA"


class ContractError(RuntimeError):
    """The contract is missing, unparseable, internally conflicting, or incomplete."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid JSON in {path}: {exc}") from exc


def _merge_fragment(document: dict, fragment: dict, source: Path) -> None:
    if fragment.get("schema_version") != document.get("schema_version"):
        raise ContractError(
            f"contract fragment schema mismatch in {source}: "
            f"{fragment.get('schema_version')} != {document.get('schema_version')}"
        )

    thresholds = document.setdefault("thresholds", {})
    for threshold_id, spec in fragment.get("thresholds", {}).items():
        if threshold_id in thresholds:
            raise ContractError(
                f"duplicate threshold {threshold_id!r} in contract fragment {source}"
            )
        thresholds[threshold_id] = spec

    gates = document.setdefault("gates", {})
    for gate_id, description in fragment.get("gates", {}).items():
        if gate_id in gates and gates[gate_id] != description:
            raise ContractError(f"conflicting gate {gate_id!r} in contract fragment {source}")
        gates[gate_id] = description


def load_contract(path: Path | None = None) -> dict:
    """Return the merged logical visual contract.

    Passing ``path`` intentionally loads only that document, which keeps unit tests and
    callers able to validate an isolated contract. The default repository load also merges
    sorted fragments from ``helper/visual-contract.d``.
    """
    target = Path(path) if path else CONTRACT_PATH
    if not target.is_file():
        raise ContractError(f"missing visual contract: {target}")
    document = _read_json(target)

    if path is None and CONTRACT_FRAGMENTS.is_dir():
        for fragment_path in sorted(CONTRACT_FRAGMENTS.glob("*.json")):
            _merge_fragment(document, _read_json(fragment_path), fragment_path)
    return document


class VisualContract:
    """Thin accessor so callers read thresholds by id instead of hardcoding them."""

    def __init__(self, document: dict | None = None):
        self._doc = document if document is not None else load_contract()

    @property
    def gates(self) -> dict:
        return self._doc.get("gates", {})

    @property
    def thresholds(self) -> dict:
        return self._doc["thresholds"]

    def threshold(self, threshold_id: str) -> dict:
        try:
            return self._doc["thresholds"][threshold_id]
        except KeyError as exc:
            raise ContractError(f"unknown threshold: {threshold_id}") from exc

    def value(self, threshold_id: str):
        return self.threshold(threshold_id)["value"]

    def int_value(self, threshold_id: str) -> int:
        return int(self.value(threshold_id))

    def severity(self, threshold_id: str) -> str:
        return self.threshold(threshold_id)["severity"]

    def is_blocking(self, threshold_id: str) -> bool:
        return self.severity(threshold_id) == BLOCKING

    def gate_of(self, threshold_id: str) -> str:
        return self.threshold(threshold_id)["gate"]


def finding(
    contract: VisualContract,
    threshold_id: str,
    *,
    ok: bool,
    measured,
    detail: str = "",
    evidence: list | None = None,
) -> dict:
    """Build one render-report row: what was measured, against what, and how it fared.

    A failed ``advisory`` threshold becomes WARN rather than FAIL, so a real defect is
    still visible in the artifact without the script claiming authority it should not
    have over a metric that over-reports.
    """
    spec = contract.threshold(threshold_id)
    if ok:
        status = PASS
    else:
        status = FAIL if spec["severity"] == BLOCKING else WARN
    return {
        "threshold_id": threshold_id,
        "gate": spec["gate"],
        "severity": spec["severity"],
        "status": status,
        "measured": measured,
        "threshold": spec["value"],
        "unit": spec["unit"],
        "detail": detail,
        "evidence": evidence or [],
    }


def skipped(contract: VisualContract, threshold_id: str, reason: str) -> dict:
    spec = contract.threshold(threshold_id)
    return {
        "threshold_id": threshold_id,
        "gate": spec["gate"],
        "severity": spec["severity"],
        "status": NA,
        "measured": None,
        "threshold": spec["value"],
        "unit": spec["unit"],
        "detail": reason,
        "evidence": [],
    }


def summarize(findings: list[dict]) -> dict:
    counts = {PASS: 0, FAIL: 0, WARN: 0, NA: 0}
    for row in findings:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    blocking_missing = [
        row for row in findings
        if row["status"] == NA and row["severity"] == BLOCKING
    ]
    failed = [row for row in findings if row["status"] == FAIL] + blocking_missing
    return {
        "verdict": FAIL if failed else PASS,
        "counts": counts,
        "failed_gates": sorted({row["gate"] for row in failed}),
        "warned_gates": sorted({row["gate"] for row in findings if row["status"] == WARN}),
    }


def render_lines(findings: list[dict]) -> list[str]:
    """Human-readable audit lines: measurement, threshold, and verdict together."""
    lines = []
    marks = {PASS: "ok  ", FAIL: "FAIL", WARN: "warn", NA: "n/a "}
    for row in findings:
        measured = row["measured"]
        shown = f"{measured:g}" if isinstance(measured, (int, float)) else str(measured)
        lines.append(
            f"  {marks[row['status']]}  {row['threshold_id']:<32} "
            f"{shown:>10} {row['unit']:<8} (limit {row['threshold']:g})"
            + (f"  {row['detail']}" if row["detail"] else "")
        )
    return lines


def exit_code(findings: list[dict]) -> int:
    return 1 if summarize(findings)["verdict"] == FAIL else 0
