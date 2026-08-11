#!/usr/bin/env python3
"""Ask a CLI script whether a documented command line would actually parse.

Two approaches were tried. Introspecting the parser and comparing flag names looks
tidy but lies about two shapes this repo genuinely uses:

* `tools/route_request.py` is a shim that calls `ecosystem_router.main(["route", ...])`,
  so `--request` is real even though it appears on no parser the shim builds.
* `skills/svg-mascot-animator/scripts/check_asset.py` reads `sys.argv` by hand, so it
  accepts `--runtime` while building no parser at all.

So instead of inspecting the parser, this module runs the documented argument list
through the program's real entry point and stops at the moment of parsing:
`parse_args` is allowed to do its actual work, then execution is halted before the
script renders, writes or launches anything. `parser.error` is captured rather than
exiting, which is what turns "argparse would have killed the process here" into a
readable assertion.

That distinction matters, because argparse fails for reasons that are not doc bugs.
Only `unrecognized arguments` and `invalid choice` mean the docs promise something the
code does not have. A missing required argument means the doc quoted a fragment.

This is not a test module. `unittest discover` only collects `test*.py`.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# argparse error text that means the documented command is genuinely wrong.
BROKEN_MARKERS = ("unrecognized arguments", "invalid choice")

NO_ARGPARSE = "no-argparse"

# `tools/route_request.py` re-exports another module's main() and forwards argv to it.
# Such a shim owns no parser but is still argparse-backed, and executing it is safe for
# the same reason executing any argparse script is: parsing happens before the work.
DELEGATION_RE = re.compile(
    r"from\s+(?:scripts|tools)[.\w]*\s+import\s+[^\n]*\bmain\b")


class _Stop(Exception):
    """Raised right after parsing so nothing the script would do next runs."""


class ProbeFailed(RuntimeError):
    """The script could not be loaded far enough to parse arguments."""


def parses_arguments(script_relpath: str) -> bool:
    """Whether the script reaches argparse at all, directly or through a shim.

    A script that reads ``sys.argv`` by hand returns False: there is no parser to ask,
    and importing it would run its real work instead of stopping at a parse.
    """
    path = ROOT / script_relpath
    if not path.is_file():
        return False
    source = path.read_text(errors="replace")
    return "argparse" in source or bool(DELEGATION_RE.search(source))


def parse_outcome(script_relpath: str, argv: list[str]) -> str | None:
    """Run ``argv`` through the script's real parser.

    Returns ``None`` when the command parses cleanly, ``NO_ARGPARSE`` when the script
    never parses arguments, or the argparse error message when parsing fails.
    """
    path = ROOT / script_relpath
    if not path.is_file():
        raise ProbeFailed(f"no such script: {script_relpath}")
    if not parses_arguments(script_relpath):
        return NO_ARGPARSE

    # Load under the name "__main__" so a shim's `if __name__ == "__main__"` block runs;
    # that block is where the real argument list gets assembled.
    spec = importlib.util.spec_from_file_location("__main__", path)
    module = importlib.util.module_from_spec(spec)

    state: dict[str, object] = {"error": None, "parsed": False}
    real_parse = argparse.ArgumentParser.parse_args
    real_error = argparse.ArgumentParser.error

    def fake_error(self, message):
        state["error"] = message
        raise _Stop()

    def fake_parse(self, args=None, namespace=None):
        try:
            real_parse(self, args, namespace)
            state["parsed"] = True
        finally:
            raise _Stop()

    saved_argv = sys.argv
    argparse.ArgumentParser.parse_args = fake_parse
    argparse.ArgumentParser.error = fake_error
    sys.argv = [str(path), *argv]
    try:
        # argparse prints usage on failure; keep it out of the test output.
        with contextlib.redirect_stderr(io.StringIO()), \
                contextlib.redirect_stdout(io.StringIO()):
            try:
                spec.loader.exec_module(module)
            except _Stop:
                pass
            except SystemExit as exc:
                if not state["parsed"] and state["error"] is None:
                    raise ProbeFailed(
                        f"{script_relpath} exited before parsing: {exc}") from exc
    finally:
        argparse.ArgumentParser.parse_args = real_parse
        argparse.ArgumentParser.error = real_error
        sys.argv = saved_argv

    if state["parsed"]:
        return None
    if state["error"] is not None:
        return str(state["error"])
    return NO_ARGPARSE


def is_broken(outcome: str | None) -> bool:
    """True only when the failure means the documented CLI does not exist."""
    if outcome is None or outcome == NO_ARGPARSE:
        return False
    return any(marker in outcome for marker in BROKEN_MARKERS)


# ---------------------------------------------------------------------------
# Parser introspection, for tests that compare documented defaults to real ones.
# ---------------------------------------------------------------------------

class _ParserCaptured(Exception):
    def __init__(self, parser: argparse.ArgumentParser):
        super().__init__("parser captured")
        self.parser = parser


def load_parser(script_relpath: str) -> argparse.ArgumentParser:
    """Return the ArgumentParser a script builds, without executing its work."""
    path = ROOT / script_relpath
    if not path.is_file():
        raise ProbeFailed(f"no such script: {script_relpath}")

    spec = importlib.util.spec_from_file_location(f"probe_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)

    captured: dict[str, argparse.ArgumentParser] = {}
    real_parse = argparse.ArgumentParser.parse_args

    def intercept(self, *args, **kwargs):
        captured["parser"] = self
        raise _ParserCaptured(self)

    argparse.ArgumentParser.parse_args = intercept
    try:
        try:
            spec.loader.exec_module(module)
        except _ParserCaptured:
            pass
        except SystemExit as exc:
            raise ProbeFailed(f"{script_relpath} exited on import: {exc}") from exc
        if "parser" not in captured:
            entry = getattr(module, "main", None)
            if entry is None:
                raise ProbeFailed(f"{script_relpath} has no main()")
            # main() signatures differ across the repo: main(), main(argv), main(paths).
            for call in (lambda: entry(), lambda: entry([])):
                try:
                    call()
                except (_ParserCaptured, SystemExit):
                    break
                except TypeError as exc:
                    if "positional argument" not in str(exc):
                        break
                except Exception:
                    break
                if "parser" in captured:
                    break
    finally:
        argparse.ArgumentParser.parse_args = real_parse

    if "parser" not in captured:
        raise ProbeFailed(f"{script_relpath} never called parse_args()")
    return captured["parser"]


def option_strings(parser: argparse.ArgumentParser) -> set[str]:
    """Every ``--flag`` and ``-f`` the parser itself accepts, excluding subcommands."""
    found: set[str] = set()
    for action in parser._actions:
        found.update(action.option_strings)
    return found


def defaults(parser: argparse.ArgumentParser) -> dict:
    """``{dest: default}`` for every action, for comparing docs against real defaults."""
    return {action.dest: action.default for action in parser._actions}
