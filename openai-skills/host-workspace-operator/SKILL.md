---
name: host-workspace-operator
description: Inspect, search, modify, and verify files or repository state using the safest host-native ChatGPT/Codex capabilities available.
---

# Host Workspace Operator

Use workspace capabilities supplied by the current ChatGPT/Codex host. This Skill does not grant filesystem access and must never invent a tool that the host did not expose.

## Capability order

Prefer the narrowest operation that can complete the job:

1. `read` for a known file or exact range
2. `list` when the workspace shape is unknown
3. `search` for broad or semantic discovery
4. `grep` for exact text, symbols, fields, or regex patterns
5. `patch` for a focused existing-file edit
6. `write` only when the requested workflow authorizes mutation
7. `shell` for repository commands when narrower file tools are insufficient
8. `python` for deterministic parsing, transformations, hashing, package inspection, or verification

Do not use shell or Python merely to imitate a safer read/search operation that the host already provides.

## Read-only first

Before creating an infographic artifact or changing workspace state:

- inspect repository/workspace instructions when present
- discover relevant files with read/list/search/grep
- distinguish source files from generated artifacts
- avoid loading vendor, dependency, cache, and build trees without need
- keep evidence, reference, asset, and output locations explicit

## Mutation boundary

Write, patch, delete, move, rename, formatting changes, and mutating shell commands are state changes.

Before mutation, require clear user authorization from the current request or an already approved parent workflow. Preserve unrelated work and prefer focused edits over broad rewrites.

After mutation, read the changed area back when practical and run the relevant verifier when the host exposes an execution capability.

Never write secrets into source, manifests, logs, examples, generated visuals, or release artifacts.

## Infographic workspace behavior

For this Plugin, workspace operations commonly support:

- reading briefs, exports, references, brand assets, SVGs, and source data
- searching a repository for existing design rules or evidence
- writing HTML/SVG/CSS, image manifests, QA reports, and final artifacts when authorized
- patching a focused visual or copy defect after critique
- running render or validation commands when shell execution exists
- using Python for deterministic file processing, hashes, archive inspection, or verification

The parent infographic workflow remains responsible for evidence integrity, identity provenance, narrative taste, visual QA, and final acceptance.

## If a capability is unavailable

Do not claim that a read, search, write, patch, shell command, render, or Python execution happened unless the host produced evidence that it did.

Use another available capability only when it preserves the task semantics. Otherwise return the strongest truthful planning/critique result and mark execution-dependent output as unavailable or `HOLD`.

## Python handoff

When deterministic local computation is materially useful and host-native Python exists, apply the `sandbox-python-executor` Skill. Use actual execution evidence rather than mental simulation.