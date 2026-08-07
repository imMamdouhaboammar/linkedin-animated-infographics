#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.info_stories import FINGERPRINT_AXES, validate_fingerprint  # noqa: E402


def load_object(path):
    payload = json.loads(Path(path).read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check an Info-stories structural fingerprint")
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--min-changes", type=int, default=2)
    args = parser.parse_args(argv)
    try:
        current = load_object(args.current)
        previous = load_object(args.previous) if args.previous else None
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    errors = validate_fingerprint(current, previous, min_changes=args.min_changes)
    changed = []
    if previous:
        changed = [axis for axis in FINGERPRINT_AXES if current.get(axis) != previous.get(axis)]
    print(json.dumps({"ok": not errors, "changed_axes": changed, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
