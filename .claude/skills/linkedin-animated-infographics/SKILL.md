---
name: linkedin-animated-infographics-conventions
description: Development conventions for a Python, Markdown, HTML, CSS, SVG, and shell based LinkedIn infographic plugin with Info-stories composition.
---

# Linkedin Animated Infographics Conventions

Use this skill when changing this repository, adding a skill or agent, modifying the render pipeline, or writing regression tests.

## Tech Stack

- **Python 3**: registries, validators, frame capture, GIF assembly, and utility tools
- **Markdown**: skills, agents, references, plans, and research notes
- **HTML / CSS / SVG**: 1080x1350 artboards and deterministic animation
- **Shell**: setup, lint, and render wrappers
- **JSON**: plugin metadata, hooks, Story House / style registry data, and structured briefs
- **unittest**: regression and acceptance tests

There is no TypeScript application layer in the current repository. Do not introduce frontend framework conventions unless a task explicitly adds one.

## Architecture

- `skills/`: user-facing capabilities and their references
- `agents/`: focused worker contracts with narrow inputs and outputs
- `scripts/`: implementation and validation logic shared by skills and tools
- `tools/`: thin public CLIs over shared Python logic
- `assets/`: templates and generated-but-tracked visual reference assets
- `tests/`: unit, contract, portability, and acceptance tests
- `research/`: tracked provenance and design/capability studies; ignored upstream clones never ship

## Info-stories

Info-stories is the composition layer. Keep its four axes independent:

1. Story House
2. Visual Style
3. Story Archetype
4. Motion Pattern

`skills/info-stories/catalog.json` is the machine-readable source of truth. Human references explain the registry but must not contradict it. Existing artboard, motion, render, Arabic, and mascot skills remain the execution layer.

When adding a registry item, add or update tests before implementation. Preserve 4.5:1 text contrast, 3:1 state-pair contrast, deterministic briefs, and explicit compatibility failures.

## Development Method

- Follow existing architecture before adding a parallel implementation
- Prefer one shared implementation with thin CLIs rather than duplicated logic
- Write a failing regression test for behavior changes, then implement the minimum fix
- Run the focused test first, then the complete test suite
- Run `python3 -m compileall -q scripts tools`
- Run `python3 scripts/info_stories.py check` when the registry changes
- Run `git diff --check` before committing
- Treat browser render verification separately from non-browser tests and report environment blockers precisely

## Commit Conventions

Use conventional commits such as `feat:`, `fix:`, `test:`, `docs:`, and `chore:`. Keep one coherent concern per commit when practical.

## Safety and Provenance

- Never commit credentials, private MCP configuration, or user secrets
- Never ship `research/upstreams/`
- Track source URL, inspected SHA, license, adopted ideas, and rejected ideas for capability research
- Prefer independently worded local rules over wholesale copying
- Do not fabricate visual proof or factual content to satisfy a template slot
