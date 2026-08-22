#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO_CATALOG = ROOT / "demos" / "catalog.json"
OWNED_ROOT = ROOT / "demos" / "owned"

TRANSFER_CONTRACT = [
    "Evidence -> Observation -> Transferable Rule -> Anti-Rule",
    "Extract the narrative mechanism, not the source composition.",
    "Do not copy source wording, logos, mascot geometry, palette measurements, or distinctive layout signatures.",
    "Assign each selected demo one explicit inspiration job such as hook, progression, reveal, proof, pacing, or motion.",
    "Build a new story from the brief and evidence boundary before styling details.",
]


def _tokens(value):
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    return set(re.findall(r"[a-z0-9]+", str(value).lower()))


def _query_tokens(query):
    fields = (
        "story_jobs",
        "content_shapes",
        "content_shape",
        "language",
        "evidence_mode",
        "density",
    )
    tokens = set()
    for field in fields:
        tokens.update(_tokens(query.get(field, "")))
    return tokens


def _catalog_candidates(query):
    if not DEMO_CATALOG.is_file():
        return []
    payload = json.loads(DEMO_CATALOG.read_text(encoding="utf-8"))
    query_tokens = _query_tokens(query)
    rows = []
    for demo in payload.get("demos", []):
        haystack = " ".join(
            str(demo.get(field, ""))
            for field in ("id", "title", "description", "story_type", "language", "tags")
        )
        demo_tokens = _tokens(haystack)
        overlap = sorted(query_tokens.intersection(demo_tokens))
        score = len(overlap) * 4
        if query.get("language") and query.get("language") == demo.get("language"):
            score += 2
        rows.append(
            {
                "id": demo.get("id"),
                "path": demo.get("path"),
                "kind": "curated-demo",
                "story_type": demo.get("story_type"),
                "language": demo.get("language"),
                "title": demo.get("title"),
                "score": score,
                "match_terms": overlap,
                "inspiration_job": "inspect narrative progression and visual payoff",
            }
        )
    return sorted(rows, key=lambda row: (-row["score"], row.get("id") or ""))


def _raw_owned_candidates():
    if not OWNED_ROOT.is_dir():
        return []
    rows = []
    for path in sorted(OWNED_ROOT.iterdir(), key=lambda candidate: candidate.name.lower()):
        if path.suffix.lower() not in {".gif", ".jpg", ".jpeg", ".png", ".webp"}:
            continue
        rows.append(
            {
                "id": path.stem,
                "path": path.relative_to(ROOT).as_posix(),
                "kind": "raw-owned-reference",
                "score": 0,
                "match_terms": [],
                "inspiration_job": "inspect manually for one transferable narrative or pacing rule",
            }
        )
    return rows


def build_demo_taste(query, max_demos):
    if not isinstance(max_demos, int) or not 1 <= max_demos <= 8:
        raise ValueError("max_demos must be an integer from 1 to 8")

    candidates = _catalog_candidates(query)
    seen = {row.get("path") for row in candidates}
    for row in _raw_owned_candidates():
        if row.get("path") not in seen:
            candidates.append(row)
            seen.add(row.get("path"))

    return {
        "schema_version": 1,
        "source_policy": "abstract-transfer-only",
        "repository_source": "demos/",
        "demo_candidates": candidates[:max_demos],
        "transfer_contract": TRANSFER_CONTRACT,
        "media_embedding": "forbidden",
        "note": (
            "Repository demos are inspiration evidence, not templates. Inspect only selected examples, "
            "extract one bounded rule per inspiration job, then create a structurally original story."
        ),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Select bounded demo references for narrative taste")
    parser.add_argument("--query", type=Path, required=True)
    parser.add_argument("--max-demos", type=int, default=3)
    args = parser.parse_args(argv)
    try:
        query = json.loads(args.query.read_text(encoding="utf-8"))
        payload = build_demo_taste(query, args.max_demos)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc))
        return 2
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
