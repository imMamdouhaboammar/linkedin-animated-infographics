# Upstream Capability Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Pull five external skill repositories into a local research area, analyze their transferable patterns, and add independently worded capabilities and tests to this repository without shipping the upstream working copies.

**Architecture:** `research/upstreams/` contains ignored shallow clones used only for inspection and repeatable experiments. `research/capability-notes/` contains tracked provenance and adoption notes. Product-facing changes are rewritten as local rules, gates, and agent behaviors, not wholesale copies.

**Tech Stack:** Git, Python 3 standard library, Markdown, existing skills/agents.

## Global Constraints

- Upstream working copies never ship in the plugin package.
- Record repository URL, inspected commit SHA, license, adopted patterns, and rejected patterns.
- Preserve attribution for any substantial copied material; prefer independent re-expression of ideas.
- Do not let marketing-site frontend rules override infographic-specific constraints.
- Capabilities must be testable through local rules or deterministic checks.

---

### Task 1: Pull and inventory upstreams

**Files:**
- Modify: `.gitignore`
- Create: `research/capability-notes/sources.json`
- Create: `scripts/audit_upstreams.py`
- Create: `tests/test_upstream_capabilities.py`

**Sources:**
- `hardikpandya/stop-slop`
- `Leonxlnx/taste-skill`
- `Nutlope/hallmark`
- `petergyang/no-ai-slop`
- `huytieu/COG-second-brain`

- [x] Add `research/upstreams/` to `.gitignore`.
- [x] Shallow-clone all five repositories into `research/upstreams/<name>`.
- [x] Add failing tests requiring all five source records, commit SHAs, and MIT license classification.
- [x] Implement `audit_upstreams.py inventory` to emit a deterministic source inventory from local clones.
- [x] Run tests and confirm GREEN.
- [x] Commit `chore: add upstream capability lab inventory`.

### Task 2: Extract capability matrix

**Files:**
- Create: `research/capability-notes/stop-slop.md`
- Create: `research/capability-notes/taste-skill.md`
- Create: `research/capability-notes/hallmark.md`
- Create: `research/capability-notes/no-ai-slop.md`
- Create: `research/capability-notes/cog-second-brain.md`
- Create: `research/capability-notes/adoption-matrix.md`

- [x] Inspect each upstream's skill entry points, references, gates, and evaluator/verification patterns.
- [x] For each source record: what to adopt, what to adapt, what to reject, and why.
- [x] Map adopted ideas to concrete local files or tests.
- [x] Commit `docs: map upstream capability patterns`.

### Task 3: Add anti-slop and design-taste capability

**Files:**
- Create: `skills/info-stories/references/anti-slop-gates.md`
- Create: `skills/info-stories/references/design-taste-gates.md`
- Modify: `agents/copy-compressor.md`
- Modify: `agents/layout-composer.md`
- Modify: `agents/post-critic.md`
- Modify: `tests/test_info_stories.py`

- [x] Write failing tests for banned structural writing patterns and visual-template repetition rules.
- [x] Add local anti-slop gates that preserve voice and flag binary contrast, throat-clearing, faux insight, generic puffery, and repetitive sentence rhythm.
- [x] Add design-taste gates for layout fingerprint variance, density, hierarchy, spacing, and avoiding palette-only reskins.
- [x] Wire the gates into copy-compressor, layout-composer, and post-critic.
- [x] Run tests and confirm GREEN.
- [x] Commit `feat: add anti-slop and design-taste gates`.

### Task 4: Add study, verifier, and closed-loop behaviors

**Files:**
- Create: `agents/design-study.md`
- Create: `agents/story-verifier.md`
- Create: `skills/info-stories/references/study-protocol.md`
- Create: `skills/info-stories/references/verification-loop.md`
- Modify: `skills/info-stories/SKILL.md`
- Modify: `tests/test_upstream_capabilities.py`

- [x] Write failing tests requiring independent study output fields and verifier evidence fields.
- [x] Add a study protocol that extracts macrostructure, type hierarchy, palette roles, density, motion, and reusable principles from references without pixel cloning.
- [x] Add a read-only verifier contract that receives artifact paths and acceptance criteria rather than worker summaries.
- [x] Add a bounded fix loop: verifier verdict, targeted fix, re-verify, maximum two fix attempts.
- [x] Run tests and confirm GREEN.
- [x] Commit `feat: add study and verification capabilities`.

### Task 5: Cross-source experiment and final report

**Files:**
- Create: `research/capability-notes/experiment-report.md`
- Modify: `README.md`

- [x] Run the same two Info-stories briefs with base rules and with the new capability gates.
- [x] Record which gates trigger and whether they produce a more distinct composition without violating artboard/motion constraints.
- [x] Run all unit tests, Python compile checks, diff checks, and plugin validation if the CLI is available.
- [x] Document upstream inspiration and local capability-lab workflow in README without presenting upstream projects as bundled dependencies.
- [x] Commit `docs: report upstream capability experiment`.


## Completion evidence

- Final unit suite: **40 tests, 40 passed**
- `python3 -m compileall -q scripts tools`: passed
- Info-stories catalog validation: passed
- Upstream snapshot validation: passed
- Two acceptance compositions: passed
- Structured reference-study contract: passed
- `git diff --check`: passed
- Browser render smoke: environment-blocked after Playwright install because the Codespace image lacks `libatk-1.0.so.0`; no privileged package-install workaround was attempted
