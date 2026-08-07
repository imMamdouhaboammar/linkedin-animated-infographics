# Info-stories Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a deterministic Info-stories composition layer with named palettes, visual styles, story archetypes, motion patterns, focused agents, and zero-dependency validation tools.

**Architecture:** Info-stories is an orchestration and registry layer over the existing artboard, motion, render, mascot, Arabic, and QA skills. JSON is the machine-readable source of truth; markdown references explain usage. Existing execution agents remain authoritative for HTML and GIF production.

**Tech Stack:** Python 3 standard library, JSON, Markdown, existing shell/Python render scripts.

## Global Constraints

- Preserve the existing 1080x1350 artboard contract.
- Preserve deterministic seekable animation and current render pipeline.
- Text contrast floor is 4.5:1; state-defining boundaries use 3:1 where applicable.
- No external runtime dependency for registry or validation tools.
- Existing workflows stay valid without migration.
- Explicit user choices win unless a hard constraint is violated.
- Unknown or incompatible selections fail with useful diagnostics.

---

### Task 1: Registry schema and validation

**Files:**
- Create: `skills/info-stories/catalog.json`
- Create: `scripts/info_stories.py`
- Create: `tests/test_info_stories.py`

**Interfaces:**
- Produces: `load_catalog() -> dict`, `validate_catalog(catalog) -> list[str]`, `contrast_ratio(fg, bg) -> float`, CLI commands `list`, `show`, `check`.

- [x] Write failing tests for unique slugs, required fields, palette contrast, and CLI unknown-slug errors.
- [x] Run `python3 -m unittest tests.test_info_stories -v` and confirm RED.
- [x] Implement the minimal catalog loader, WCAG contrast calculation, schema checks, and CLI dispatch.
- [x] Populate 10 Story Houses, 10 Visual Styles, 12 Story Archetypes, and 10 Motion Patterns in `catalog.json`.
- [x] Run `python3 -m unittest tests.test_info_stories -v` and confirm GREEN.
- [x] Commit `feat: add info-stories registry and validator`.

### Task 2: Composition and scaffold behavior

**Files:**
- Modify: `scripts/info_stories.py`
- Modify: `tests/test_info_stories.py`

**Interfaces:**
- Produces: `check_composition(style, archetype, motions) -> list[str]`, `build_brief(...) -> dict`, CLI commands `compose` and `scaffold`.

- [x] Add failing tests for one accepted editorial combination, one accepted terminal combination, incompatible motion/style rejection, deterministic scaffold output, and nearest-choice diagnostics.
- [x] Run focused tests and confirm RED.
- [x] Implement compatibility resolution and deterministic story-brief generation.
- [x] Run the full Info-stories test module and confirm GREEN.
- [x] Commit `feat: add info-stories composition engine`.

### Task 3: Skill references and focused agents

**Files:**
- Create: `skills/info-stories/SKILL.md`
- Create: `skills/info-stories/references/palette-houses.md`
- Create: `skills/info-stories/references/visual-styles.md`
- Create: `skills/info-stories/references/story-archetypes.md`
- Create: `skills/info-stories/references/motion-patterns.md`
- Create: `skills/info-stories/references/composition-matrix.md`
- Create: `agents/story-architect.md`
- Create: `agents/palette-curator.md`
- Create: `agents/layout-composer.md`
- Create: `agents/motion-director.md`
- Create: `agents/copy-compressor.md`
- Create: `agents/evidence-checker.md`

**Interfaces:**
- Consumes: `catalog.json`, existing `artboard`, `motion`, `arabic`, `mascots`, and `render` skills.
- Produces: narrow agent contracts that hand off to existing execution agents.

- [x] Add a failing structure test that requires every public registry axis and every agent reference to exist.
- [x] Write the router skill and reference docs without duplicating existing render rules.
- [x] Write six focused agent files with explicit inputs, outputs, and handoff boundaries.
- [x] Run tests and grep checks for broken relative references.
- [x] Commit `feat: add info-stories skills and agents`.

### Task 4: Integrate with current workflow and docs

**Files:**
- Modify: `skills/new-post/SKILL.md`
- Modify: `agents/artboard-builder.md`
- Modify: `agents/motion-engineer.md`
- Modify: `README.md`
- Modify: `.claude-plugin/plugin.json`

- [x] Add failing tests/assertions for the router mentioning Info-stories selection before artboard execution.
- [x] Add Info-stories selection to `new-post` while preserving existing approval gates.
- [x] Teach artboard-builder and motion-engineer to consume a resolved story brief rather than invent new palette/motion decisions.
- [x] Document the four-axis model and starter examples in README.
- [x] Bump plugin minor version from 2.0.0 to 2.1.0.
- [x] Run unit tests, `python3 -m compileall -q scripts`, and `git diff --check`.
- [x] Commit `docs: integrate info-stories workflow`.

### Task 5: Acceptance smoke tests

**Files:**
- Modify: `tests/test_info_stories.py`
- Create: `examples/info-stories/README.md`

- [x] Add smoke tests for Ember Paper + Signal Sheet + Framework in One Page and Midnight Operator + Command Canvas + One Prompt Full Workflow.
- [x] Generate both briefs twice and assert byte-identical JSON output.
- [x] Verify every palette's declared text pairs meet 4.5:1.
- [x] Run all tests and record exact pass count in the branch review notes.
- [x] Commit `test: cover info-stories acceptance flows`.


## Completion evidence

- Final unit suite: **40 tests, 40 passed**
- `python3 -m compileall -q scripts tools`: passed
- Info-stories catalog validation: passed
- Upstream snapshot validation: passed
- Two acceptance compositions: passed
- Structured reference-study contract: passed
- `git diff --check`: passed
- Browser render smoke: environment-blocked after Playwright install because the Codespace image lacks `libatk-1.0.so.0`; no privileged package-install workaround was attempted
