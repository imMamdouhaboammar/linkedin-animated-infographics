#!/usr/bin/env python3
"""Every documented command must actually run.

`python3 .../scripts/check_render.py <path> --mobile` shipped in four files —
`agents/render-qa.md`, `skills/artboard/SKILL.md`, `skills/qa-post/SKILL.md` and
`skills/render/references/qa-gates.md` — while `check_render.py` had no `--mobile` flag.
argparse exits 2 on an unknown flag, so an agent following its own instructions hit a
hard error. 273 tests and eight validators missed it, because nothing compared the
documented CLI against the real one.

This test closes the class of defect rather than that one instance: it extracts every
`python3 .../scripts|tools/*.py …` invocation from every shipped `*.md` and
`.codex/agents/*.toml`, then feeds each documented argument list to that script's real
entry point and stops at the moment of parsing.

Only `unrecognized arguments` and `invalid choice` are treated as failures. A missing
required argument means the doc quoted a fragment, which is a documentation style, not a
broken instruction.

A doc that promises a flag the code does not have is a broken instruction, and an agent
is the one who finds out.
"""

from __future__ import annotations

import re
import shlex
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from argparse_probe import (
    NO_ARGPARSE,
    ProbeFailed,
    defaults,
    is_broken,
    load_parser,
    parse_outcome,
    parses_arguments,
)

ROOT = Path(__file__).resolve().parents[1]

# python3 <any prefix>/scripts|tools/<name>.py <rest of the command>
COMMAND_RE = re.compile(
    r"python3\s+(\S*?(?:scripts|tools)/[A-Za-z0-9_]+\.py)([^\n`]*)")
FLAG_RE = re.compile(r"--[a-z][a-z0-9-]*")
# argparse never sees anything past a shell operator.
SHELL_BREAK_RE = re.compile(r"\s(?:\||&&|;|>|2>)")

# Working copies and generated state are not shipped instructions.
EXCLUDED_PREFIXES = ("research/upstreams/", "node_modules/", ".plugin-state/", "build/")

# Optional heavy dependencies. A machine without them cannot load the script, and saying
# so is honest; silently passing would not be.
OPTIONAL_DEPS = ("playwright", "PIL", "pillow")


def resolve_script(documented_path: str) -> str:
    """Map a documented path to its repo-relative path.

    Docs invoke scripts through an installed plugin root (`${CLAUDE_PLUGIN_ROOT}/…`,
    `~/.claude/plugins/<plugin>/…`) or a bare relative path, and some scripts live in a
    skill's own `scripts/` directory rather than the top-level one. Taking the longest
    suffix that exists resolves every case without guessing, and falling back to the
    `scripts|tools/<name>.py` tail keeps a genuinely missing script reportable.
    """
    parts = documented_path.split("/")
    for index in range(len(parts)):
        candidate = "/".join(parts[index:])
        if (ROOT / candidate).is_file():
            return candidate
    for index, part in enumerate(parts):
        if part in ("scripts", "tools"):
            return "/".join(parts[index:])
    return documented_path


def split_arguments(tail: str) -> list[str]:
    """Turn the rest of a documented command line into an argument list."""
    cut = SHELL_BREAK_RE.search(tail)
    if cut:
        tail = tail[: cut.start()]
    try:
        return shlex.split(tail)
    except ValueError:
        return tail.split()


def documented_invocations() -> list[dict]:
    """Every documented CLI call, with the file that promises it."""
    sources: list[Path] = sorted(ROOT.glob("**/*.md"))
    sources += sorted(ROOT.glob(".codex/agents/*.toml"))

    invocations: list[dict] = []
    for path in sources:
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(EXCLUDED_PREFIXES) or "/node_modules/" in rel:
            continue
        # Honour shell line continuations so a multi-line command parses as one command.
        text = re.sub(r"\\\s*\n\s*", " ", path.read_text(errors="replace"))
        for match in COMMAND_RE.finditer(text):
            tail = match.group(2)
            invocations.append({
                "script": resolve_script(match.group(1)),
                "argv": split_arguments(tail),
                "flags": sorted(set(FLAG_RE.findall(tail))),
                "documented_in": rel,
                "command": " ".join(match.group(0).split()),
            })
    return invocations


class DocumentedCliContractTests(unittest.TestCase):
    """The documented CLI surface must be a subset of the real one."""

    @classmethod
    def setUpClass(cls):
        cls.invocations = documented_invocations()

    def test_the_docs_actually_contain_commands(self):
        """Guard against a silently passing suite if the extractor ever stops matching."""
        self.assertGreater(len(self.invocations), 25,
                           "extracted too few commands; the extractor likely broke")
        self.assertGreater(len({i["script"] for i in self.invocations}), 10)

    def test_every_documented_script_exists(self):
        for script in sorted({inv["script"] for inv in self.invocations}):
            with self.subTest(script=script):
                self.assertTrue((ROOT / script).is_file(),
                                f"documented script does not exist: {script}")

    def test_every_documented_command_parses(self):
        for inv in self.invocations:
            with self.subTest(script=inv["script"], doc=inv["documented_in"],
                              argv=" ".join(inv["argv"])):
                if not (ROOT / inv["script"]).is_file():
                    continue  # reported by test_every_documented_script_exists
                try:
                    outcome = parse_outcome(inv["script"], inv["argv"])
                except ProbeFailed as exc:
                    if any(dep in str(exc) for dep in OPTIONAL_DEPS):
                        self.skipTest(f"{inv['script']}: {exc}")
                    self.fail(f"{inv['script']} could not be probed: {exc}")
                self.assertFalse(
                    is_broken(outcome),
                    f"{inv['documented_in']} documents\n    {inv['command']}\n"
                    f"but {inv['script']} rejects it: {outcome}")

    def test_manually_parsed_flags_are_handled_in_the_source(self):
        """Scripts that read `sys.argv` by hand still have to know their own flags.

        `check_asset.py` accepts `--runtime` without building a parser, so there is no
        parser to ask. Requiring the flag to appear in the source is weaker than parsing,
        and is stated as such, but it still catches a documented flag no code mentions.
        """
        for inv in self.invocations:
            script = inv["script"]
            if not (ROOT / script).is_file() or parses_arguments(script):
                continue
            source = (ROOT / script).read_text(errors="replace")
            for flag in inv["flags"]:
                with self.subTest(script=script, flag=flag, doc=inv["documented_in"]):
                    self.assertIn(
                        flag, source,
                        f"{inv['documented_in']} documents `{flag}` for {script}, "
                        f"which parses argv by hand and never mentions it")

    def test_the_probe_can_still_detect_a_bad_flag(self):
        """A guard on the guard: if the probe stopped detecting, every test above lies."""
        outcome = parse_outcome("scripts/check_render.py",
                                ["x.html", "--flag-that-does-not-exist"])
        self.assertTrue(is_broken(outcome),
                        f"probe failed to flag a bogus argument (got {outcome!r})")


class MobileFlagRegressionTests(unittest.TestCase):
    """The specific bug this file was written for, pinned so it cannot come back."""

    def test_check_render_accepts_the_documented_mobile_flags(self):
        for flag in ("--mobile", "--no-mobile"):
            with self.subTest(flag=flag):
                outcome = parse_outcome("scripts/check_render.py", ["x.html", flag])
                self.assertFalse(is_broken(outcome),
                                 f"check_render.py rejects {flag}: {outcome}")

    def test_mobile_flag_is_still_documented(self):
        """If the docs drop the flag the pairing is moot, so keep them honest together."""
        promising = [
            path.relative_to(ROOT).as_posix()
            for path in ROOT.glob("**/*.md")
            if not path.relative_to(ROOT).as_posix().startswith(EXCLUDED_PREFIXES)
            and "--mobile" in path.read_text(errors="replace")
        ]
        self.assertTrue(promising, "no doc documents --mobile any more")

    def test_mobile_preview_defaults_on(self):
        self.assertIs(defaults(load_parser("scripts/check_render.py"))["mobile"], True)


class RenderJsonContractTests(unittest.TestCase):
    def test_render_checks_accept_json_report_paths(self):
        commands = {
            "scripts/check_render.py": ["x.html", "--json", "still.json"],
            "scripts/build_gif.py": ["frames", "--json", "gif.json"],
        }
        for script, argv in commands.items():
            with self.subTest(script=script):
                outcome = parse_outcome(script, argv)
                self.assertFalse(is_broken(outcome), f"{script} rejects --json: {outcome}")


if __name__ == "__main__":
    unittest.main()
