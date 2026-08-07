#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.info_stories import contrast_ratio, load_catalog  # noqa: E402


def find_house(catalog, slug):
    for house in catalog["houses"]:
        if house["slug"] == slug:
            return house
    choices = ", ".join(item["slug"] for item in catalog["houses"])
    raise ValueError(f"Unknown house {slug!r}. Valid choices: {choices}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check one Story House foreground/background contrast pair")
    parser.add_argument("--house", required=True)
    parser.add_argument("--fg", required=True, help="foreground semantic token name")
    parser.add_argument("--bg", required=True, help="background semantic token name")
    parser.add_argument("--minimum", type=float, default=4.5)
    args = parser.parse_args(argv)
    try:
        house = find_house(load_catalog(), args.house)
        tokens = house["tokens"]
        if args.fg not in tokens or args.bg not in tokens:
            available = ", ".join(sorted(tokens))
            raise ValueError(f"Unknown token. Available tokens: {available}")
        ratio = contrast_ratio(tokens[args.fg], tokens[args.bg])
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = {
        "ok": ratio >= args.minimum,
        "house": args.house,
        "foreground": {"token": args.fg, "value": tokens[args.fg]},
        "background": {"token": args.bg, "value": tokens[args.bg]},
        "ratio": round(ratio, 3),
        "minimum": args.minimum,
    }
    print(json.dumps(payload, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
