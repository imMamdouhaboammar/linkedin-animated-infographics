# OpenAI Autopilot Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a capability-negotiated OpenAI autopilot runtime that uses real Codex subagents, sandbox artifacts, side jobs, and host tools when available while preserving Claude behavior.

**Architecture:** Keep Claude on its current `skills/` + `agents/` worker graph. Add a self-contained `openai-skills/linkedin-infographic-autopilot/` parent skill and expand project-scoped `.codex/agents/` roles for real Codex delegation. The public skill selects `full-autopilot`, `tool-rich-sequential`, or `safe-skill-only` based on observed host capabilities and never fabricates execution.

**Tech Stack:** Markdown Agent Skills, Codex TOML agent configuration, Python `unittest`, JSON compatibility/submission metadata, GitHub Actions validation

## Global Constraints

- Preserve Claude behavior as a regression baseline
- Keep the public OpenAI package self-contained
- Never claim a tool call, delegation, render, app action, or publish action that did not actually happen
- Still QA must pass before motion
- Exact named mascot identity requires the exact SVG
- Community publishing requires explicit consent and stops at a pull request
- Maximum two targeted repair attempts
- Release version is 3.2.2

---

### Task 1: Add failing contract tests for autopilot packaging

**Files:**
- Create: `tests/test_openai_autopilot.py`
- Create: `tests/test_openai_capability_paths.py`
- Create: `tests/test_openai_side_jobs.py`
- Create: `tests/test_workspace_agents_bridge.py`

**Interfaces:**
- Consumes: existing `openai-skills/`, `.codex/agents/`, `compatibility/codex.json`
- Produces: contract expectations for autopilot skill, execution paths, side jobs, sandbox artifacts, workspace-agent fallback, and real Codex agent roles

- [ ] **Step 1:** Write tests that require `openai-skills/linkedin-infographic-autopilot/SKILL.md` and required reference files
- [ ] **Step 2:** Write tests for exact path names `full-autopilot`, `tool-rich-sequential`, `safe-skill-only`
- [ ] **Step 3:** Write tests proving unknown capabilities default to unavailable and fake delegation/tool claims are forbidden
- [ ] **Step 4:** Write tests for canonical sandbox artifact paths and side-job outputs
- [ ] **Step 5:** Write tests that workspace agents are optional and installation does not claim automatic registration
- [ ] **Step 6:** Write tests requiring nine project-scoped Codex roles with narrow write/read-only permissions
- [ ] **Step 7:** Open a verification PR and run GitHub Actions
- [ ] **Step 8:** Confirm the new tests fail because the feature does not exist yet

### Task 2: Implement the self-contained OpenAI autopilot skill

**Files:**
- Create: `openai-skills/linkedin-infographic-autopilot/SKILL.md`
- Create: `openai-skills/linkedin-infographic-autopilot/references/capability-negotiation.md`
- Create: `openai-skills/linkedin-infographic-autopilot/references/execution-paths.md`
- Create: `openai-skills/linkedin-infographic-autopilot/references/side-jobs.md`
- Create: `openai-skills/linkedin-infographic-autopilot/references/artifact-workspace.md`
- Create: `openai-skills/linkedin-infographic-autopilot/references/tool-usage-policy.md`
- Create: `openai-skills/linkedin-infographic-autopilot/references/autopilot-failure-policy.md`
- Create: `openai-skills/linkedin-infographic-autopilot/references/workspace-agents-bridge.md`

**Interfaces:**
- Consumes: focused OpenAI skill contracts and user task inputs
- Produces: selected execution path, bounded side-job artifacts, build/QA workflow, truthful final verification

- [ ] **Step 1:** Implement capability discovery rules using observed host capabilities only
- [ ] **Step 2:** Implement the three execution paths and deterministic fallback order
- [ ] **Step 3:** Implement parallelizable side-job contracts and required bounded outputs
- [ ] **Step 4:** Implement sandbox artifact workspace contract
- [ ] **Step 5:** Implement tool-selection and failure behavior
- [ ] **Step 6:** Implement optional workspace-agent bridge without claiming automatic registration
- [ ] **Step 7:** Wire still-before-motion and final independent verification into the parent skill

### Task 3: Add real Codex project-scoped creative agents

**Files:**
- Create: `.codex/agents/creative_director.toml`
- Create: `.codex/agents/evidence_researcher.toml`
- Create: `.codex/agents/copy_director.toml`
- Create: `.codex/agents/layout_composer.toml`
- Create: `.codex/agents/still_critic.toml`
- Create: `.codex/agents/motion_director.toml`
- Create: `.codex/agents/render_qa.toml`
- Create: `.codex/agents/final_verifier.toml`
- Create: `.codex/agents/tool_runner.toml`
- Modify: `.codex/config.toml`

**Interfaces:**
- Consumes: root Codex task and workspace artifacts
- Produces: role-specific bounded outputs; only builder/tool roles may write

- [ ] **Step 1:** Define read-only research/review/verifier roles
- [ ] **Step 2:** Define workspace-write build/layout/motion/tool roles
- [ ] **Step 3:** Register role descriptions/config files under `[agents]`
- [ ] **Step 4:** Keep concurrency bounded at six and retain approval/sandbox defaults

### Task 4: Wire package metadata, compatibility, and validator coverage

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `compatibility/codex.json`
- Modify: `submission/openai-plugin.json`
- Modify: `submission/README.md`
- Modify: `scripts/validate_codex_plugin.py`
- Modify: relevant release/version tests

**Interfaces:**
- Consumes: new autopilot skill root and Codex roles
- Produces: validated 3.2.2 release metadata and parity guarantees

- [ ] **Step 1:** Bump release version to 3.2.2 everywhere the validator requires parity
- [ ] **Step 2:** Add autopilot to OpenAI package metadata and starter prompt wording without exceeding Directory prompt limits
- [ ] **Step 3:** Update compatibility execution metadata to capability-negotiated autopilot
- [ ] **Step 4:** Extend validator to require autopilot files, capability markers, workspace-agent optionality, and agent roles
- [ ] **Step 5:** Preserve Claude skills/agents roots and native worker graph

### Task 5: Verify, review, and merge

**Files:**
- All changed files from Tasks 1-4

**Interfaces:**
- Consumes: complete feature branch
- Produces: green PR and merged main

- [ ] **Step 1:** Run full GitHub Actions validation on the feature PR
- [ ] **Step 2:** Inspect failing job logs and fix root causes without weakening tests
- [ ] **Step 3:** Confirm Python unit tests, Codex/OpenAI validation, Claude marketplace validation, official Claude plugin validation, and Claude install smoke all pass
- [ ] **Step 4:** Inspect PR review threads and resolve actionable findings
- [ ] **Step 5:** Merge only after the latest head is green
- [ ] **Step 6:** Verify merged `main` contains the new OpenAI autopilot skill and unchanged Claude execution roots
