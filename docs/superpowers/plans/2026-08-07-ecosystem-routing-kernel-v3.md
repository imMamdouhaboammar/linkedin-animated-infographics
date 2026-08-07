# Ecosystem Routing Kernel v3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a central LLM routing helper, standardize all skill and agent contracts, synchronize capability/artifact ownership, refresh README/docs, and ship the same repository as Claude Marketplace plugin version 3.0.0.

**Architecture:** `helper/` is the routing authority. `scripts/ecosystem_router.py` validates and executes deterministic routing over helper registries. Existing workflow skills remain the execution entrypoints, while every agent/skill adopts a consistent contract and returns artifacts through the parent workflow. CI validates the helper, graph, docs, marketplace, Claude plugin, and actual local marketplace install.

**Tech Stack:** Python 3.12, JSON, Markdown, shell, Claude Code plugin/marketplace manifests, unittest, GitHub Actions.

## Global Constraints

- Keep marketplace name `mamdouh-creative-tools` and plugin name `linkedin-animated-infographics`.
- Keep same-repository marketplace source `./` with strict mode.
- Bump plugin and marketplace plugin version to `3.0.0`.
- Keep Info-stories authority in `scripts/info_stories.py::load_catalog()`.
- Named or official mascots require exact user-supplied/task-attached SVG.
- Workers return to the parent workflow; no hidden peer orchestration.
- Do not replace the deterministic HTML/SVG/GIF rendering pipeline.
- Do not re-merge historical branches already represented in `main`.

---

### Task 1: Helper registries and deterministic router

**Files:**
- Create: `helper/README.md`
- Create: `helper/GUIDE.md`
- Create: `helper/router.json`
- Create: `helper/capabilities.json`
- Create: `helper/artifacts.json`
- Create: `scripts/ecosystem_router.py`
- Create: `tools/route_request.py`
- Create: `tests/test_ecosystem_router.py`

**Interfaces:**
- Consumes: `architecture/plugin-graph.json`, skill/agent file inventory, Info-stories workflow names.
- Produces: `load_ecosystem(root)`, `validate_ecosystem(root)`, `route_request(request, root)`, CLI `check|route|explain`.

- [ ] Write tests that fail when helper files are absent, when registry owners reference unknown agents/skills, or when a named mascot has no exact SVG.
- [ ] Implement helper JSON registries with full production path, focused routes, Arabic/UI/mascot/reference/static-animation conditions, and artifact producers/consumers.
- [ ] Implement deterministic loading, cross-registry validation, routing, and human-readable explanation.
- [ ] Add thin `tools/route_request.py` wrapper.
- [ ] Run `python3 -m unittest tests.test_ecosystem_router -v` and require zero failures.

### Task 2: Synchronize executable architecture graph

**Files:**
- Modify: `architecture/plugin-graph.json`
- Modify: `scripts/plugin_graph.py`
- Modify: `tests/test_plugin_graph.py`

**Interfaces:**
- Consumes: `helper/capabilities.json`, `helper/router.json`.
- Produces: graph/helper consistency validation.

- [ ] Add failing tests for capability ownership drift, missing conditional route agents, and workflow-order mismatch.
- [ ] Extend `plugin_graph.py` to compare helper capability owners and workflow sequence with the graph.
- [ ] Keep mascot conditional edge between still construction and motion integration.
- [ ] Run graph tests and `python3 scripts/plugin_graph.py check`.

### Task 3: Skill contracts v3

**Files:**
- Modify every `skills/*/SKILL.md` entrypoint.
- Add/modify: `tests/test_skill_contracts.py`.

**Interfaces:**
- Consumes: `helper/GUIDE.md`, router intent names, artifact contracts.
- Produces: consistent Purpose / Use when / Inputs / Outputs / Procedure / HOLD conditions / Related components sections.

- [ ] Add structural tests covering every public `SKILL.md`.
- [ ] Refactor `post` into lightweight helper-backed routing guidance.
- [ ] Refactor `new-post`, `qa-post`, and `render-gif` around named helper artifacts and HOLD semantics.
- [ ] Standardize domain skills without duplicating orchestration.
- [ ] Keep Arabic, Info-stories, render, motion, mascot, and exact-SVG behavior intact.
- [ ] Run all skill-contract tests plus existing Info-stories/mascot tests.

### Task 4: Agent contracts v3

**Files:**
- Modify every `agents/*.md`.
- Add/modify: `tests/test_agent_contracts.py`.

**Interfaces:**
- Consumes: graph required skill preloads, helper artifact contracts.
- Produces: consistent Role / Inputs / Method / HOLD conditions / Quality gates / Outputs sections.

- [ ] Add structural tests for all agents.
- [ ] Standardize all 14 agents while preserving specialist responsibilities.
- [ ] Ensure every output maps to a declared artifact or explicit parent-workflow return.
- [ ] Ban peer-orchestration language and ensure required `skills:` preload entries match the graph.
- [ ] Run agent tests and graph validator.

### Task 5: Repository guidance and cross-agent entrypoints

**Files:**
- Create: `AGENTS.md`
- Create: `CLAUDE.md`
- Modify: `.agents/skills/linkedin-animated-infographics/SKILL.md`
- Modify: `.claude/skills/linkedin-animated-infographics/SKILL.md`
- Modify: `.codex/AGENTS.md`
- Add/modify: `tests/test_repository_guidance.py`

**Interfaces:**
- Consumes: `helper/GUIDE.md` as authority.
- Produces: one consistent entry path for Claude, Codex, and generic coding agents.

- [ ] Add tests that all repository guidance points to `helper/GUIDE.md` and does not redefine registry authority incorrectly.
- [ ] Write concise root guidance files and update existing adapter guidance.
- [ ] Run guidance tests.

### Task 6: README and durable documentation

**Files:**
- Rewrite: `README.md`
- Create: `docs/ecosystem.md`
- Create: `docs/routing.md`
- Create: `docs/agents.md`
- Create: `docs/skills.md`
- Create: `docs/marketplace.md`
- Create: `docs/development.md`
- Add/modify: `tests/test_docs_contract.py`

**Interfaces:**
- Consumes: helper registries, actual skill/agent inventory, marketplace identity.
- Produces: concise README plus focused long-form docs.

- [ ] Add tests for required docs, inventory coverage, install commands, and broken local Markdown links.
- [ ] Rewrite README for product value, quick start, helper routing, workflows, examples, and validation.
- [ ] Generate/update focused docs from actual repository contracts.
- [ ] Run docs tests.

### Task 7: Marketplace release 3.0.0 and CI ecosystem doctor

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `scripts/validate_marketplace.py`
- Modify: `.github/workflows/claude-plugin-validation.yml`
- Modify: `tests/test_marketplace.py`
- Modify version assertions in existing tests.

**Interfaces:**
- Consumes: version `3.0.0`, `scripts/ecosystem_router.py check`.
- Produces: clean Claude validation and real marketplace add/list/install smoke.

- [ ] Change version assertions to 3.0.0 and verify RED.
- [ ] Bump manifest and marketplace plugin version.
- [ ] Add ecosystem helper validation and docs-contract tests to CI via full suite.
- [ ] Keep full-history checkout for whitespace integrity.
- [ ] Run local validators where possible and let PR CI run current Claude Code official validation/install smoke.

### Task 8: Full verification, review, and merge

**Files:**
- No new product files unless review finds a concrete defect.

**Interfaces:**
- Consumes: complete branch and all CI/review feedback.
- Produces: merged `main` commit only after verified head is green.

- [ ] Run full unit suite, compile, Info-stories, plugin graph, ecosystem helper, marketplace, shell/JSON, and whitespace checks.
- [ ] Open PR with architecture summary and exact validation matrix.
- [ ] Inspect Qlty, CodeRabbit/Qodo/review threads; fix concrete findings with regression tests.
- [ ] Require official `claude plugin validate .` and marketplace add/install smoke to pass on PR head.
- [ ] Squash merge with `expected_head_sha`.
- [ ] Verify merged files and `main` state after merge.