#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_UPSTREAMS = ROOT / "research" / "upstreams"
DEFAULT_OUTPUT = ROOT / "research" / "capability-notes" / "sources.json"


def _git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def _repository_url(repo):
    url = _git(repo, "config", "--get", "remote.origin.url")
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url.split(":", 1)[1]
    if url.endswith(".git"):
        url = url[:-4]
    return url


def _license_name(repo):
    for name in ("LICENSE", "LICENSE.md", "LICENCE", "LICENCE.md"):
        path = repo / name
        if path.exists():
            text = path.read_text(errors="replace").lstrip()
            if text.startswith("MIT License") or "## License\n\nMIT" in text:
                return "MIT"
            return "OTHER"
    return "MISSING"


def build_inventory(upstreams=DEFAULT_UPSTREAMS):
    upstreams = Path(upstreams)
    items = []
    for repo in sorted((p for p in upstreams.iterdir() if p.is_dir()), key=lambda p: p.name):
        if not (repo / ".git").exists():
            continue
        items.append(
            {
                "name": repo.name,
                "repository": _repository_url(repo),
                "commit": _git(repo, "rev-parse", "HEAD"),
                "license": _license_name(repo),
                "readme_present": (repo / "README.md").exists(),
            }
        )
    return items


def write_inventory(upstreams=DEFAULT_UPSTREAMS, output=DEFAULT_OUTPUT):
    payload = {"schema_version": 1, "sources": build_inventory(upstreams)}
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inventory local capability-lab upstream repositories")
    parser.add_argument("command", choices=("inventory", "check"))
    parser.add_argument("--upstreams", type=Path, default=DEFAULT_UPSTREAMS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    live = build_inventory(args.upstreams)
    if args.command == "inventory":
        payload = write_inventory(args.upstreams, args.output)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    if not args.output.exists():
        print(f"missing snapshot: {args.output}")
        return 1
    snapshot = json.loads(args.output.read_text()).get("sources", [])
    if snapshot != live:
        print("upstream snapshot differs from local working copies")
        return 1
    print("Upstream capability inventory: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
