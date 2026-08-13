#!/usr/bin/env python3
import json
import sys

PROTOCOL = """Token-efficient runtime is active for this plugin.
For a complete production run, write the normalized request once to build/runtime-context/request.json. Include topic/source identity, audience, language, output mode, CTA, and approved constraints that can change stage output.
Before spawning a cacheable worker, run: python3 scripts/runtime_context.py prepare --intent create-post --stage <agent> --workspace .
If the JSON response has cache_hit=true, treat it as CACHE HIT: use the restored registered output and do not spawn that worker. A missing request record disables cache reuse.
On a cache miss, spawn the worker normally. After its registered output passes the stage's blocking gates, run: python3 scripts/runtime_context.py store --intent create-post --stage <agent> --workspace .
Never bypass HOLD semantics or verification. post-critic and story-verifier always run fresh. The generated build/runtime-context/<agent>.json capsule is the focused stage context and may be used instead of rereading unrelated registries."""


def main():
    data = json.load(sys.stdin)
    if data.get("hook_event_name") != "SessionStart":
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": PROTOCOL,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
