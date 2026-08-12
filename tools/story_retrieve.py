#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.info_stories import (  # noqa: E402
    build_context_capsule,
    load_catalog,
    rank_mechanisms,
    validate_mechanisms,
)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Retrieve deterministic Info-stories mechanisms")
    parser.add_argument("--query", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        query = json.loads(args.query.read_text())
        catalog = load_catalog()
        errors = validate_mechanisms(catalog)
        if errors:
            raise ValueError("; ".join(errors))
        ranked = rank_mechanisms(catalog, query)
        capsule = build_context_capsule(
            catalog,
            ranked,
            query.get("stage", "concept"),
            query.get("byte_budget", 8000),
        )
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(capsule, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
