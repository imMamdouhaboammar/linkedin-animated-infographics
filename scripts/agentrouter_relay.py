#!/usr/bin/env python3
"""
AgentRouter Codex Relay — Unified Dispatch for Creative Design & Coding Tasks.

Dispatches a self-contained brief to OpenAI Codex via AgentRouter (gpt-5.6-sol),
captures execution events, touched files, and token usage, and writes a structured
result.json for orchestrating agents (Antigravity/Gemini/Claude) to review and land.

Trust posture:
- Credentials are read from ~/.agentrouter/.env, ~/.codex-agentrouter/auth.json,
  or AGENT_ROUTER_TOKEN environment variable. Never stored in tracked repository files.
- The relay deliberately does NOT commit. The orchestrator reviews and commits.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_credentials() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Load API token, base URL, and model from environment or dotfiles."""
    token = os.environ.get("AGENT_ROUTER_TOKEN") or os.environ.get("AGENTROUTER_API_KEY")
    base_url = os.environ.get("AGENTROUTER_BASE_URL", "https://agentrouter.org/v1")
    model = os.environ.get("AGENTROUTER_MODEL", "gpt-5.6-sol")

    # Check ~/.agentrouter/.env
    env_file = Path.home() / ".agentrouter" / ".env"
    if env_file.exists():
        try:
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("\"'")
                if k in ("AGENTROUTER_API_KEY", "AGENT_ROUTER_TOKEN") and not token:
                    token = v
                elif k == "AGENTROUTER_BASE_URL" and not os.environ.get("AGENTROUTER_BASE_URL"):
                    base_url = v
                elif k == "AGENTROUTER_MODEL" and not os.environ.get("AGENTROUTER_MODEL"):
                    model = v
        except Exception:
            pass

    # Check ~/.codex-agentrouter/auth.json
    auth_file = Path.home() / ".codex-agentrouter" / "auth.json"
    if not token and auth_file.exists():
        try:
            auth_data = json.loads(auth_file.read_text(encoding="utf-8"))
            token = auth_data.get("AGENT_ROUTER_TOKEN") or auth_data.get("OPENAI_API_KEY")
        except Exception:
            pass

    return token, base_url, model


def ensure_codex_home(token: str, base_url: str, model: str) -> Path:
    """Ensure ~/.codex-agentrouter exists with proper configuration."""
    home_dir = Path.home() / ".codex-agentrouter"
    home_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    config_content = f"""model = "{model}"
model_provider = "openai-chat-completions"
preferred_auth_method = "apikey"
sandbox_mode = "workspace-write"
approval_policy = "never"
web_search = "disabled"

[model_providers.openai-chat-completions]
name = "AgentRouter"
base_url = "{base_url}"
env_key = "AGENT_ROUTER_TOKEN"
wire_api = "responses"
query_params = {{}}
stream_idle_timeout_ms = 300000

[agents]
enabled = true
max_concurrent_threads_per_session = 6
default_subagent_model = "{model}"
default_subagent_reasoning_effort = "high"
"""
    config_file = home_dir / "config.toml"
    config_file.write_text(config_content, encoding="utf-8")
    config_file.chmod(0o600)

    auth_file = home_dir / "auth.json"
    auth_file.write_text(json.dumps({"AGENT_ROUTER_TOKEN": token}, indent=2), encoding="utf-8")
    auth_file.chmod(0o600)

    return home_dir


def get_git_status(cwd: Path) -> Optional[List[str]]:
    """Return porcelain git status or None if not in a git repo."""
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if res.returncode == 0:
            return [line.rstrip() for line in res.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return None


def run_relay(
    brief: str,
    cwd: Path,
    model: Optional[str] = None,
    sandbox: str = "workspace-write",
    read_only: bool = False,
    out_dir: Optional[Path] = None,
    timeout: int = 300,
    resume_last: bool = False,
) -> Dict[str, Any]:
    """Execute Codex via AgentRouter with the given brief."""
    token, base_url, default_model = load_credentials()
    if not token:
        print("Error: No AgentRouter token found in ~/.agentrouter/.env or ~/.codex-agentrouter/auth.json", file=sys.stderr)
        return {
            "schema": "delegate-team.agentrouter-codex.result.v1",
            "backend": "agentrouter-codex",
            "status": "unauthenticated",
            "exitCode": 127,
            "finalMessage": "Missing AGENT_ROUTER_TOKEN credential",
            "touchedFiles": [],
        }

    active_model = model or default_model or "gpt-5.6-sol"
    if read_only:
        sandbox = "read-only"

    codex_home = ensure_codex_home(token, base_url, active_model)

    # Setup run output directory
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    if not out_dir:
        out_dir = Path(f"/tmp/delegate-agentrouter/{cwd.name}-{timestamp_str}")
    out_dir.mkdir(parents=True, exist_ok=True)

    brief_path = out_dir / "brief.txt"
    events_path = out_dir / "events.jsonl"
    final_path = out_dir / "final.txt"
    result_path = out_dir / "result.json"

    brief_path.write_text(brief, encoding="utf-8")

    git_before = set(get_git_status(cwd) or [])
    started_at = datetime.now(timezone.utc).isoformat()
    start_time = time.time()

    # Build command
    cmd = [
        "codex",
        "exec",
    ]
    if resume_last:
        cmd.extend(["resume", "--last"])
    else:
        cmd.extend(["-s", sandbox])
        cmd.extend(["-m", active_model])

    cmd.extend([
        "--json",
        "-o", str(final_path),
        "--skip-git-repo-check",
        "-C", str(cwd),
        "-",
    ])

    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    env["AGENT_ROUTER_TOKEN"] = token

    print(f"relay: dispatching to Codex ({active_model}) via AgentRouter in {cwd} ...", file=sys.stderr)

    events_file = open(events_path, "w", encoding="utf-8")
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=events_file,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
    )

    try:
        _, stderr_text = proc.communicate(input=brief, timeout=timeout)
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        _, stderr_text = proc.communicate()
        exit_code = 124
        stderr_text = (stderr_text or "") + f"\n[relay: timeout exceeded {timeout}s]"
    finally:
        events_file.close()

    duration = round(time.time() - start_time, 2)
    finished_at = datetime.now(timezone.utc).isoformat()

    final_message = ""
    if final_path.exists():
        final_message = final_path.read_text(encoding="utf-8").strip()

    # Extract tokens from events if available
    tokens_info = {}
    if events_path.exists():
        try:
            for line in events_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                data = json.loads(line)
                if data.get("type") == "turn_completed" and "tokens" in data:
                    tokens_info = data["tokens"]
        except Exception:
            pass

    git_after = set(get_git_status(cwd) or [])
    new_touched = sorted(list(git_after - git_before)) if git_after or git_before else []

    status = "completed" if exit_code == 0 else "failed"
    stderr_tail = [line for line in (stderr_text or "").splitlines() if line.strip()][-10:]

    result_data = {
        "schema": "delegate-team.agentrouter-codex.result.v1",
        "backend": "agentrouter-codex",
        "model": active_model,
        "status": status,
        "exitCode": exit_code,
        "durationSeconds": duration,
        "finalMessage": final_message,
        "touchedFiles": new_touched,
        "tokens": tokens_info,
        "briefPath": str(brief_path),
        "eventsPath": str(events_path),
        "finalPath": str(final_path),
        "resultPath": str(result_path),
        "startedAt": started_at,
        "finishedAt": finished_at,
        "stderrTail": stderr_tail,
    }

    result_path.write_text(json.dumps(result_data, indent=2), encoding="utf-8")

    # Print human-readable summary
    print(f"\nrelay: {status} (exit {exit_code}) · Codex (AgentRouter) · {active_model} ({duration}s)", file=sys.stderr)
    if new_touched:
        print(f"touched files ({len(new_touched)}):", file=sys.stderr)
        for f in new_touched[:10]:
            print(f"  {f}", file=sys.stderr)
    print(f"result: {result_path}", file=sys.stderr)
    print("relay does not commit. Review the diff and land from the orchestrator.\n", file=sys.stderr)

    return result_data


def main() -> int:
    parser = argparse.ArgumentParser(description="AgentRouter Codex Relay — Unified Multi-Agent Worker")
    parser.add_argument("--brief", help="Path to brief file (or stdin)")
    parser.add_argument("--cd", default=os.getcwd(), help="Target directory (default: current dir)")
    parser.add_argument("--model", default="gpt-5.6-sol", help="Model override (default: gpt-5.6-sol)")
    parser.add_argument("--sandbox", default="workspace-write", choices=["read-only", "workspace-write", "danger-full-access"])
    parser.add_argument("--read-only", action="store_true", help="Read-only mode")
    parser.add_argument("--out-dir", help="Output artifacts directory")
    parser.add_argument("--timeout", type=int, default=300, help="Max execution timeout in seconds")
    parser.add_argument("--resume-last", action="store_true", help="Resume previous Codex session")

    args = parser.parse_args()

    brief_text = ""
    if args.brief:
        brief_path = Path(args.brief)
        if not brief_path.exists():
            print(f"Error: brief file not found: {args.brief}", file=sys.stderr)
            return 2
        brief_text = brief_path.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        brief_text = sys.stdin.read()
    else:
        print("Error: No brief provided via --brief or stdin", file=sys.stderr)
        return 2

    res = run_relay(
        brief=brief_text,
        cwd=Path(args.cd).resolve(),
        model=args.model,
        sandbox=args.sandbox,
        read_only=args.read_only,
        out_dir=Path(args.out_dir).resolve() if args.out_dir else None,
        timeout=args.timeout,
        resume_last=args.resume_last,
    )

    print(json.dumps(res, indent=2))
    return 0 if res["status"] == "completed" else res["exitCode"]


if __name__ == "__main__":
    sys.exit(main())
