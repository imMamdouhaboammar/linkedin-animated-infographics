---
name: sandbox-python-executor
description: Use host-native Python for deterministic file processing, package inspection, hashing, validation, and other executable verification when Python is actually available.
---

# Sandbox Python Executor

Use the current ChatGPT/Codex host's Python execution capability to produce evidence. This Skill is not an MCP server and does not grant a runtime by itself.

## Execute Python when it adds evidence

Use host-native Python for work such as:

- parsing or comparing JSON and generated reports
- inspecting ZIP archives and package boundaries
- computing SHA-256 or other deterministic hashes
- checking file trees, duplicate names, or path safety
- validating SVG/XML or structured output
- transforming user-provided files when local Python is the appropriate tool
- reproducing a deterministic bug or calculation
- running reviewed local validators when the surrounding workflow permits execution

Do not invoke Python just to rewrite prose or simulate a check that can be performed with a narrower host capability.

## Execution contract

When Python is available:

1. actually execute the operation before claiming a result
2. prefer reviewed bundled logic or small deterministic checks over arbitrary untrusted scripts
3. inspect target-repository scripts before running them
4. keep repository access read-only unless the user authorized mutation
5. do not assume sandbox internet access
6. do not expose secrets, tokens, credentials, or unrelated user files
7. preserve generated artifacts the user needs and report their real path/reference
8. include enough evidence to distinguish an executed check from a proposed command

## Infographic jobs

Python may be useful for:

- verifying dimensions, frame manifests, asset hashes, and identity provenance
- inspecting generated package archives
- checking deterministic export metadata
- comparing before/after structured QA reports
- validating file naming and output boundaries

Python does not replace visual inspection. A mathematically valid artifact can still fail narrative, hierarchy, typography, identity, or feed-scale visual QA.

## Evidence to report

Report the relevant subset of:

- operation executed
- pass/fail status
- important counts or findings
- generated path/reference
- SHA-256 when package or asset identity matters
- warnings and checks that could not be executed

Never fabricate stdout, hashes, paths, test counts, generated files, or tool availability.

## If Python is unavailable

Do not claim Python, tests, package validation, hashing, or file transformation occurred. Continue with static inspection only where sufficient and mark execution-dependent conclusions as unverified or `HOLD`.