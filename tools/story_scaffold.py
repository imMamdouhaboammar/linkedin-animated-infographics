#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.info_stories import build_brief, load_catalog  # noqa: E402

def main(argv=None):
    p=argparse.ArgumentParser(description="Write a deterministic Info-stories story brief")
    p.add_argument("--topic", required=True); p.add_argument("--takeaway", required=True); p.add_argument("--cta", required=True)
    p.add_argument("--house", required=True); p.add_argument("--style", required=True); p.add_argument("--archetype", required=True)
    p.add_argument("--motion", action="append", default=[]); p.add_argument("--language", default="en")
    p.add_argument("--output-mode", choices=("gif","static"), default="gif"); p.add_argument("--out", type=Path)
    a=p.parse_args(argv)
    try:
        brief=build_brief(load_catalog(), topic=a.topic, takeaway=a.takeaway, cta=a.cta, house=a.house, style=a.style, archetype=a.archetype, motions=a.motion, language=a.language, output_mode=a.output_mode)
    except ValueError as exc:
        print(str(exc), file=sys.stderr); return 2
    payload=json.dumps(brief, indent=2, sort_keys=True)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True); a.out.write_text(payload); print(a.out)
    else: print(payload, end="")
    return 0
if __name__ == "__main__": raise SystemExit(main())
