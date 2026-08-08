# OpenAI Visual Parity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship an isolated OpenAI skill distribution that reaches Claude-level process discipline without changing Claude behavior.

**Architecture:** Keep the Claude plugin, workers, and canonical `skills/` path intact. Add `openai-skills/` as a self-contained compiled workflow for ChatGPT/Codex, point only the OpenAI manifest to it, add blocking visual-quality contracts and regression tests, and bump package metadata to `3.2.1`.

**Tech Stack:** Markdown Agent Skills, JSON plugin manifests, Python unittest/validator contracts, GitHub Actions repository validation.

## Global Constraints

- Claude is a regression baseline: no behavioral changes to `.claude-plugin/` or `agents/`.
- OpenAI execution may choose a different visual direction from Claude, but must follow equivalent quality gates.
- OpenAI runtime content must not depend on `.claude-plugin/`, `agents/`, `${CLAUDE_PLUGIN_ROOT}`, `helper/`, or `architecture/`.
- Still QA is blocking before motion.
- Maximum two targeted repair attempts before HOLD/FAIL.
- Keep directory compliance: at most three default prompts, square `composerIcon` and `logo`, no `interface.screenshots`.
- Version target: `3.2.1`.

---

### Task 1: Add the isolated OpenAI studio skill

**Files:**
- Create: `openai-skills/linkedin-infographic-studio/SKILL.md`
- Create: `openai-skills/linkedin-infographic-studio/references/openai-runtime.md`
- Create: `openai-skills/linkedin-infographic-studio/references/role-passes.md`
- Create: `openai-skills/linkedin-infographic-studio/references/visual-quality-contract.md`
- Create: `openai-skills/linkedin-infographic-studio/references/motion-quality-contract.md`

**Interfaces:**
- Consumes: user topic/source files, intended output mode, optional visual references and brand assets.
- Produces: a sequential evidence → concept → story → layout → still → critique → motion → verification workflow with explicit HOLD semantics.

- [ ] **Step 1: Write the OpenAI runtime contract**
  Define that unavailable Claude workers are represented as sequential role passes and that no hidden delegation is assumed.

- [ ] **Step 2: Write the role-pass contract**
  Define bounded outputs for evidence, creative direction, story, palette, copy, layout, still critique, motion, render QA, and final verification.

- [ ] **Step 3: Write the visual-quality contract**
  Include measurable occupancy/dead-zone/containment/footer rules and the failure taxonomy from the design spec.

- [ ] **Step 4: Write the motion-quality contract**
  Require motion to explain reading order, change, travel, or active state and reject motion added to a weak still.

- [ ] **Step 5: Write the parent SKILL.md**
  Make the workflow self-contained and require reading all four local references before production.

- [ ] **Step 6: Commit**
  Commit the new OpenAI distribution as one coherent change.

### Task 2: Point OpenAI packaging at the isolated distribution

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `submission/openai-plugin.json`
- Modify: `compatibility/codex.json`
- Modify: `.claude-plugin/plugin.json` only for version parity if required by existing contract

**Interfaces:**
- Consumes: `openai-skills/` created in Task 1.
- Produces: publish metadata for version `3.2.1`.

- [ ] **Step 1: Change `.codex-plugin/plugin.json`**
  Set `version` to `3.2.1` and `skills` to `./openai-skills/`. Preserve the three directory-compliant prompts, logo, composer icon, and absence of screenshots.

- [ ] **Step 2: Update OpenAI submission metadata**
  Set version to `3.2.1`, set `skills_bundle` to `./openai-skills/`, and describe the isolated compiled workflow in release notes.

- [ ] **Step 3: Update compatibility metadata**
  Record the OpenAI distribution root separately while keeping the Claude canonical skill root intact.

- [ ] **Step 4: Keep identity/version parity**
  If the repository contract requires Claude/OpenAI version equality, bump only Claude manifest version metadata to `3.2.1`; do not alter Claude paths, agents, hooks, skills, or behavior.

- [ ] **Step 5: Commit**
  Commit packaging/version changes.

### Task 3: Harden the validator against the observed failure mode

**Files:**
- Modify: `scripts/validate_codex_plugin.py`
- Modify: `tests/test_codex_plugin.py`

**Interfaces:**
- Consumes: OpenAI manifest and OpenAI studio skill files.
- Produces: validation errors for packaging drift, unavailable-runtime references, missing visual gates, and directory compliance regressions.

- [ ] **Step 1: Add failing manifest-path tests**
  Assert the OpenAI manifest uses `./openai-skills/` and the directory exists.

- [ ] **Step 2: Add failing self-containment tests**
  Scan the OpenAI studio bundle and reject `.claude-plugin/`, `agents/`, `${CLAUDE_PLUGIN_ROOT}`, `helper/`, and `architecture/` runtime references.

- [ ] **Step 3: Add failing visual-contract tests**
  Assert the required failure taxonomy, 82-92% occupancy guidance, 120px dead-zone threshold, maximum two containment levels, still-before-motion gate, and two-attempt repair limit are present.

- [ ] **Step 4: Add directory-compliance tests**
  Assert at most three default prompts, required logo/composer icon, and no screenshots field.

- [ ] **Step 5: Update validator implementation**
  Change the expected OpenAI skill root and add the new self-containment and visual-contract checks.

- [ ] **Step 6: Preserve Claude regression assertions**
  Ensure tests still require existing Claude plugin and worker files but do not rewrite them.

- [ ] **Step 7: Commit**
  Commit validator and regression tests.

### Task 4: Update submission documentation

**Files:**
- Modify: `submission/README.md`
- Modify: `docs/codex.md`
- Modify: `docs/marketplace.md` if it describes the old shared skill root

**Interfaces:**
- Consumes: final packaging layout.
- Produces: accurate maintainer instructions for future OpenAI updates without implying GitHub auto-publishes the directory version.

- [ ] **Step 1: Document host isolation**
  Explain that Claude keeps native workers while OpenAI receives a self-contained skill workflow.

- [ ] **Step 2: Document update lifecycle**
  State that repository commits do not automatically replace the published directory package; a new version must be submitted/published through the platform update flow.

- [ ] **Step 3: Document parity target**
  State explicitly that parity means quality/process parity, not identical visual output.

- [ ] **Step 4: Commit**
  Commit documentation updates.

### Task 5: Remote verification

**Files:**
- Read: all modified files
- Check: latest commit statuses/workflow runs

**Interfaces:**
- Consumes: repository state after Tasks 1-4.
- Produces: evidence that the GitHub state is internally consistent and ready for the next directory update.

- [ ] **Step 1: Re-fetch the OpenAI manifest and studio skill from GitHub**
  Verify version/path/default prompts/icon/logo/screenshots state.

- [ ] **Step 2: Re-fetch Claude manifest and representative agent**
  Verify Claude behavior paths remain intact.

- [ ] **Step 3: Inspect remote CI/status**
  Check GitHub status/workflow evidence available for the latest commit.

- [ ] **Step 4: Report blockers honestly**
  If no remote workflow executes the tests, state that repository-level inspection passed but runtime tests were not executed locally because the task is GitHub-connector-only.
