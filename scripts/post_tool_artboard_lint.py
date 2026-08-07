#!/usr/bin/env python3
"""Run the artboard linter after Claude/Codex file-edit hook events.

The hook is advisory: lint output is useful during iteration, but this adapter
always exits successfully so a PostToolUse hook cannot turn a completed edit
into a blocking product failure.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

PATCH_FILE_RE = re.compile(r"^\*\*\* (?:Update|Add) File: (.+)$", re.MULTILINE)
DIFF_FILE_RE = re.compile(r"^\+\+\+ b/(.+)$", re.MULTILINE)


def extract_html_targets(payload: dict[str, Any]) -> list[str]:
    """Extract edited HTML paths from Claude Write/Edit or Codex apply_patch input."""
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return []

    candidates: list[str] = []
    file_path = tool_input.get("file_path")
    if isinstance(file_path, str) and file_path.lower().endswith(".html"):
        candidates.append(file_path)

    command = tool_input.get("command")
    if isinstance(command, str):
        candidates.extend(PATCH_FILE_RE.findall(command))
        candidates.extend(DIFF_FILE_RE.findall(command))

    result: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate.lower().endswith(".html") or candidate in seen:
            continue
        seen.add(candidate)
        result.append(candidate)
    return result


def _workspace_file(cwd: Path, value: str) -> Path | None:
    supplied = Path(value).expanduser()
    resolved = supplied.resolve() if supplied.is_absolute() else (cwd / supplied).resolve()
    try:
        resolved.relative_to(cwd.resolve())
    except ValueError:
        return None
    return resolved


def _plugin_root() -> Path:
    value = os.environ.get("PLUGIN_ROOT") or os.environ.get("CLAUDE_PLUGIN_ROOT")
    if value:
        return Path(value).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def run(payload: dict[str, Any]) -> int:
    cwd_value = payload.get("cwd")
    cwd = Path(cwd_value).expanduser().resolve() if isinstance(cwd_value, str) and cwd_value else Path.cwd().resolve()
    lint_script = _plugin_root() / "scripts" / "lint_artboard.sh"
    if not lint_script.is_file():
        return 0

    for value in extract_html_targets(payload):
        target = _workspace_file(cwd, value)
        if target is None or not target.is_file():
            continue
        try:
            text = target.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not re.search(r"\bid\s*=\s*['\"]artboard['\"]", text, re.IGNORECASE):
            continue
        subprocess.run(["bash", str(lint_script), str(target)], cwd=cwd, check=False)
    return 0


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0
    return run(payload)


if __name__ == "__main__":
    raise SystemExit(main())
