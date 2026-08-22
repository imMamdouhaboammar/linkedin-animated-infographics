# Design and OpenAI Plugin Quality v3.7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship version 3.7.0 with stronger design perception, reference-transfer, visual-slop, and targeted-revision contracts while keeping the public OpenAI package self-contained and Skills-only.

**Architecture:** Extend the existing canonical design guidance first, then project the same behavioral markers into the self-contained OpenAI Studio, Autopilot, and Review Skills. Strengthen tests and package validators before the behavior change, then bump all release-coupled metadata together and prepare submission material without claiming publication.

**Tech Stack:** Markdown Agent Skills, Python 3.11 validators/tests, JSON plugin manifests and compatibility registries, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-22-design-plugin-quality-v37.md`

## Global Constraints

- Public OpenAI submission remains `skills-only`.
- Public Skill set remains compact; do not expose internal worker roles as duplicate Skills.
- User facts, official identities, exact SVGs, approved typography, and evidence boundaries remain higher priority than aesthetic preferences.
- Motion remains blocked until the still passes.
- Capability negotiation remains truthful and host-observed.
- Release version is `3.7.0` across every release-coupled host surface.
- Submission state remains `prepared-not-submitted`.

---

### Task 1: Lock the new design contract with regression tests

**Files:**
- Modify: `tests/test_codex_plugin.py`
- Modify: `tests/test_openai_focused_skills.py`
- Modify: `tests/test_info_stories.py` only if canonical design-taste coverage belongs there

**Interfaces:**
- Consumes: existing text-based contract validation patterns.
- Produces: failing assertions for perception preflight, reference-transfer protocol, severity pressure, targeted revision routing, and version 3.7.0.

- [ ] **Step 1: Add failing OpenAI contract assertions**

Require these markers in the Studio visual contract and/or role passes:

```python
for marker in (
    "one-second hierarchy test",
    "100x100",
    "squint",
    "grayscale",
    "negative-space audit",
    "tangency",
    "brand-off specificity",
    "effect-subtraction",
    "Evidence -> Observation -> Transferable Rule -> Anti-Rule",
    "cumulative pressure",
    "two or more major",
    "four or more minor",
    "smallest responsible dimension",
):
    self.assertIn(marker, combined_contract_text)
```

- [ ] **Step 2: Add focused-review assertions**

Require the Review Skill to expose perception tests, severity labels, and targeted repair routing rather than only binary taxonomy output.

- [ ] **Step 3: Change release expectations from 3.6.0 to 3.7.0 in release-coupled tests**

Update exact version constants only; do not loosen version-drift checks.

- [ ] **Step 4: Run focused tests and confirm they fail before implementation**

Run in CI or an available execution environment:

```bash
python3 -m unittest tests.test_codex_plugin tests.test_openai_focused_skills tests.test_info_stories -v
```

Expected: FAIL on missing new design markers and/or version mismatch before Tasks 2-4.

### Task 2: Strengthen canonical design judgment

**Files:**
- Modify: `skills/info-stories/references/design-taste-gates.md`
- Modify: `agents/creative-director.md`
- Modify: `agents/layout-composer.md`
- Modify: `agents/post-critic.md` if its current contract owns final visual criticism

**Interfaces:**
- Consumes: evidence boundary, selected concept, design dials, reference DNA, asset plan, type spec.
- Produces: canonical perception-preflight and revision-routing guidance consumed by repository workers.

- [ ] **Step 1: Add perception preflight to canonical design-taste gates**

Document the one-primary-anchor rule, one-second/thumbnail/squint/grayscale tests, intentional-negative-space test, tangency/crop test, brand-off specificity, and effect-subtraction test.

- [ ] **Step 2: Add the four-stage reference-transfer protocol**

Use the exact sequence `Evidence -> Observation -> Transferable Rule -> Anti-Rule` and require job-based reference assignment when multiple references exist.

- [ ] **Step 3: Add severity-aware visual-slop pressure**

Keep existing hard gates. For non-hard-gate defects add critical/major/minor and block at any critical, 2+ major, 4+ minor, or cumulative pressure >=6 where major=3 and minor=1.

- [ ] **Step 4: Add targeted revision ownership**

Creative concept failures route to creative direction; hierarchy/composition failures route to layout; type failures route to type; copy density to copy; motion to motion; render/runtime to render QA. Do not rerun unrelated upstream stages.

### Task 3: Bring the self-contained OpenAI Skills to the same design standard

**Files:**
- Modify: `openai-skills/linkedin-infographic-studio/SKILL.md`
- Modify: `openai-skills/linkedin-infographic-studio/references/role-passes.md`
- Modify: `openai-skills/linkedin-infographic-studio/references/visual-quality-contract.md`
- Modify: `openai-skills/linkedin-infographic-autopilot/SKILL.md`
- Modify: `openai-skills/linkedin-infographic-autopilot/references/visual-quality-contract.md`
- Modify: `openai-skills/linkedin-infographic-review/SKILL.md`

**Interfaces:**
- Consumes: host-observed capabilities plus the self-contained OpenAI references.
- Produces: equivalent design judgment in ChatGPT/Codex without depending on repository-only workers.

- [ ] **Step 1: Add a blocking preflight before still construction**

Studio and Autopilot must perform the perception checks before build/motion gates.

- [ ] **Step 2: Add reference transfer behavior**

When references are inspectable, derive transferable mechanisms and anti-rules, assign distinct jobs to multiple references, and prevent literal cloning.

- [ ] **Step 3: Extend visual QA output**

Return named taxonomy rows plus severity, pressure, evidence, smallest responsible dimension, and precise repair action.

- [ ] **Step 4: Update focused Review Skill**

Review should apply the same perception checks and aggregation without expanding into an unrelated redesign.

### Task 4: Upgrade the public Plugin release to 3.7.0

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `.agents/plugins/linkedin-animated-infographics/plugin.json`
- Modify: `plugin.json`
- Modify: `compatibility/codex.json`
- Modify: `compatibility/antigravity.json`
- Modify: `scripts/validate_codex_plugin.py`
- Modify: `scripts/validate_antigravity_plugin.py`
- Modify: `scripts/validate_marketplace.py` when it pins the release
- Modify: `tests/test_codex_plugin.py`
- Modify: `tests/test_antigravity_plugin.py`
- Modify: `tests/test_marketplace.py`
- Modify: `README.md`
- Modify: `docs/codex.md`, `docs/marketplace.md`, `docs/antigravity.md`, `docs/development.md` only where release-coupled version text exists

**Interfaces:**
- Consumes: passing Task 1-3 behavior.
- Produces: cross-host release metadata with no version drift.

- [ ] **Step 1: Update exact expected version constants to 3.7.0**
- [ ] **Step 2: Update all host manifests and compatibility registries to 3.7.0**
- [ ] **Step 3: Refresh listing text only where behavior changed**

Keep the product promise concrete: evidence-backed visual stories, stronger design preflight, still-first QA, disciplined motion, and truthful capability-aware execution.

- [ ] **Step 4: Update release documentation without claiming platform publication**

### Task 5: Refresh Skills-only submission evidence

**Files:**
- Modify: `submission/openai-plugin.json`
- Modify: `submission/test-cases.json`
- Modify: `submission/README.md` if it contains release-specific instructions
- Modify: `tests/test_openai_submission.py`

**Interfaces:**
- Consumes: implemented v3.7.0 behavior and current repository test evidence.
- Produces: a prepared-not-submitted Skills-only pack with exactly five positive and three negative reviewer cases.

- [ ] **Step 1: Update package version and release notes to 3.7.0**
- [ ] **Step 2: Strengthen existing create/review cases to exercise perception preflight and targeted revision behavior**
- [ ] **Step 3: Preserve exactly five positive and three negative cases**
- [ ] **Step 4: Keep `submission_status` equal to `prepared-not-submitted`**

### Task 6: Full verification and staff-engineer review

**Files:**
- No production changes unless verification exposes a defect.

**Interfaces:**
- Consumes: complete branch.
- Produces: exact-head evidence for merge decision.

- [ ] **Step 1: Run the repository minimum deterministic gate**

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

- [ ] **Step 2: Open a PR and inspect the exact diff**

Trace public behavior changes, package/version coupling, and design-contract blast radius.

- [ ] **Step 3: Require exact-head GitHub checks**

Plugin Validation, Security Gates, Plugin Scanner, CodeRabbit, and QLTY must pass when available.

- [ ] **Step 4: Merge only the exact verified head**

Use an expected-head pin and a clean merge method consistent with repository history.
