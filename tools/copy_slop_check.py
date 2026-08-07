#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.info_stories import detect_copy_slop  # noqa: E402

def main(argv=None):
    p=argparse.ArgumentParser(description="Detect named copy patterns before an Info-stories build")
    p.add_argument("text", nargs="?"); p.add_argument("--file", type=Path)
    a=p.parse_args(argv)
    if bool(a.text) == bool(a.file):
        p.error("provide text or --file, not both")
    text=a.file.read_text() if a.file else a.text
    findings=detect_copy_slop(text)
    print(json.dumps({"ok": not findings, "findings": findings}, indent=2, ensure_ascii=False))
    return 0 if not findings else 1
if __name__ == "__main__": raise SystemExit(main())
