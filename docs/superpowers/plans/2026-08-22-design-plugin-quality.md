# Design and OpenAI Plugin Quality Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen design perception, reference transfer, visual-slop detection, and targeted revision behavior while keeping the public OpenAI package self-contained and Skills-only.

**Architecture:** Extend canonical design guidance first, then carry the same behavioral contract into the self-contained OpenAI Studio, Autopilot, and Review Skills. Lock the behavior with tests, refresh current 3.6.0 candidate metadata, update submission evidence, then merge only from an exact head with required checks green.

**Tech Stack:** Markdown Agent Skills, Python 3.11 validators/tests, JSON plugin manifests and compatibility registries, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-22-design-plugin-quality.md`

## Global Constraints

- Public OpenAI submission remains `skills-only`.
- Public Skill set remains compact; internal worker roles do not become duplicate public Skills.
- User facts, official identities, exact SVGs, approved typography, and evidence boundaries remain higher priority than aesthetic preferences.
- Motion remains blocked until the still passes.
- Capability negotiation remains truthful and host-observed.
- Current pre-submission candidate remains version `3.6.0` across release-coupled surfaces.
- Submission state remains `prepared-not-submitted`.

---

### Task 1: Lock the design contract with regression tests

**Files:**
- Create: `tests/test_design_quality_upgrade.py`

**Interfaces:**
- Consumes: existing text-based contract validation patterns.
- Produces: assertions for perception preflight, reference-transfer protocol, severity pressure, targeted revision routing, and current release-candidate metadata.

- [ ] Add assertions for one-second hierarchy, 100x100 thumbnail, squint, grayscale, negative-space audit, tangency, brand-off specificity, effect-subtraction, `Evidence -> Observation -> Transferable Rule -> Anti-Rule`, cumulative pressure, and smallest responsible dimension.
- [ ] Require the Review Skill to expose critical/major/minor severity and bounded targeted repair.
- [ ] Require OpenAI metadata to remain Skills-only, 3.6.0, and `prepared-not-submitted`.

### Task 2: Strengthen canonical design judgment

**Files:**
- Modify: `skills/info-stories/references/design-taste-gates.md`
- Modify: `agents/creative-director.md`
- Modify: `agents/layout-composer.md`
- Modify: `agents/post-critic.md`

**Interfaces:**
- Consumes: evidence boundary, selected concept, design dials, reference DNA, asset plan, type spec.
- Produces: canonical perception-preflight and revision-routing guidance.

- [ ] Add perception preflight before still construction.
- [ ] Add job-based reference transfer with explicit anti-rules.
- [ ] Add critical/major/minor visual-slop pressure while preserving named hard gates.
- [ ] Route repairs to the smallest responsible dimension and preserve unrelated approved work.

### Task 3: Bring self-contained OpenAI Skills to parity

**Files:**
- Modify: `openai-skills/linkedin-infographic-studio/SKILL.md`
- Modify: `openai-skills/linkedin-infographic-studio/references/role-passes.md`
- Modify: `openai-skills/linkedin-infographic-studio/references/visual-quality-contract.md`
- Modify: `openai-skills/linkedin-infographic-autopilot/SKILL.md`
- Modify: `openai-skills/linkedin-infographic-autopilot/references/visual-quality-contract.md`
- Modify: `openai-skills/linkedin-infographic-review/SKILL.md`

**Interfaces:**
- Consumes: host-observed capabilities and self-contained references.
- Produces: equivalent design judgment in ChatGPT/Codex without repository-only dependencies.

- [ ] Add blocking perception preflight before still construction.
- [ ] Add reference-transfer behavior for inspectable visual references.
- [ ] Extend QA output with severity, pressure, evidence, responsible dimension, and exact repair.
- [ ] Keep Review bounded to the supplied artifact rather than turning critique into a new design job.

### Task 4: Refresh current plugin candidate metadata

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `plugin.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `.agents/plugins/linkedin-animated-infographics/plugin.json`
- Modify: `compatibility/codex.json`
- Modify: `compatibility/antigravity.json`

**Interfaces:**
- Consumes: implemented design behavior.
- Produces: clearer directory-facing descriptions and cross-host parity invariants with version preserved at 3.6.0.

- [ ] Refresh descriptions to name stronger design perception checks and targeted QA.
- [ ] Add cross-host invariants for perception preflight, reference transfer, severity pressure, and smallest-responsible-dimension repair.
- [ ] Do not add an MCP/App dependency to a workflow that remains self-contained.

### Task 5: Refresh Skills-only submission evidence

**Files:**
- Modify: `submission/openai-plugin.json`
- Modify: `submission/test-cases.json`
- Modify: `tests/test_openai_submission.py` only if the existing assertions require new supported behavior.

**Interfaces:**
- Consumes: implemented 3.6.0 behavior.
- Produces: a prepared-not-submitted Skills-only pack with exactly five positive and three negative reviewer cases.

- [ ] Update description and release-candidate notes from confirmed behavior only.
- [ ] Strengthen create/review cases to exercise perception preflight and targeted revision behavior.
- [ ] Preserve exactly five positive and three negative cases.
- [ ] Preserve `submission_status: prepared-not-submitted`.

### Task 6: Full verification and staff-engineer review

**Files:**
- No production changes unless verification exposes a defect.

**Interfaces:**
- Consumes: complete branch.
- Produces: exact-head evidence for merge decision.

- [ ] Run or observe the repository minimum deterministic gate:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
python3 scripts/validate_codex_plugin.py
python3 scripts/validate_antigravity_plugin.py
```

- [ ] Inspect the pull-request diff for behavior and packaging drift.
- [ ] Require exact-head Plugin Validation, Security Gates, Plugin Scanner, CodeRabbit, and QLTY when available.
- [ ] Merge only the exact verified head.
