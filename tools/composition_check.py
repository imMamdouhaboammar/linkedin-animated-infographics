#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.info_stories import check_composition, load_catalog  # noqa: E402

def main(argv=None):
    p=argparse.ArgumentParser(description="Check an Info-stories style/archetype/motion combination")
    p.add_argument("--style", required=True); p.add_argument("--archetype", required=True); p.add_argument("--motion", action="append", default=[])
    a=p.parse_args(argv)
    try: errors=check_composition(load_catalog(), a.style, a.archetype, a.motion)
    except ValueError as exc: errors=[str(exc)]
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1
if __name__ == "__main__": raise SystemExit(main())
