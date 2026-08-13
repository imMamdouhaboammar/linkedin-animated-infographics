#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main():
    data = json.load(sys.stdin)
    if data.get("hook_event_name") != "SubagentStart":
        return 0
    stage = str(data.get("agent_type", "")).rsplit(":", 1)[-1]
    root = Path(data.get("cwd") or ".").resolve()
    path = root / "build" / "runtime-context" / f"{stage}.json"
    if not path.exists():
        return 0
    capsule = json.loads(path.read_text())
    text = "Runtime capsule for " + stage + ":\n" + json.dumps(capsule, separators=(",", ":"), ensure_ascii=False)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": text}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
