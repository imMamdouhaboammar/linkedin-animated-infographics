# Ecosystem Routing Kernel v3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a central LLM routing helper, activate research-derived capability gates, standardize all skill and agent contracts, synchronize capability/artifact ownership, refresh README/docs, and ship the same repository as Claude Marketplace plugin version 3.0.0.

**Architecture:** `helper/` is the routing authority. `scripts/ecosystem_router.py` validates and executes deterministic routing over helper registries. `research/capability-notes/gates.json` turns adopted research into explicit runtime quality gates linked to provenance and shipping owners. Existing workflow skills remain the execution entrypoints, while every agent/skill adopts a consistent contract and returns artifacts through the parent workflow. CI validates the helper, research gates, graph, docs, marketplace, Claude plugin, and actual local marketplace install.

**Tech Stack:** Python 3.12, JSON, Markdown, shell, Claude Code plugin/marketplace manifests, unittest, GitHub Actions.

## Global Constraints

- Keep marketplace name `mamdouh-creative-tools` and plugin name `linkedin-animated-infographics`.
- Keep same-repository marketplace source `./` with strict mode.
- Bump plugin and marketplace plugin version to `3.0.0`.
- Keep Info-stories authority in `scripts/info_stories.py::load_catalog()`.
- Keep research provenance in `research/capability-notes/sources.json`; do not package upstream clones.
- Every adopted research gate must have provenance, local behavior, stage, owners, implementation references, and tests.
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

- [x] Write tests that fail when helper files are absent, when registry owners reference unknown agents/skills, or when a named mascot has no exact SVG.
- [x] Implement helper JSON registries with full production path, focused routes, Arabic/UI/mascot/reference/static-animation conditions, and artifact producers/consumers.
- [x] Implement deterministic loading, cross-registry validation, routing, and human-readable explanation.
- [x] Add thin `tools/route_request.py` wrapper.
- [x] Verify full CI including official Claude validation and marketplace install smoke.

### Task 2: Synchronize executable architecture graph

**Files:**
- Modify: `scripts/plugin_graph.py`
- Modify: `tests/test_plugin_graph.py`

**Interfaces:**
- Consumes: `helper/capabilities.json`, `helper/router.json`.
- Produces: graph/helper consistency validation.

- [x] Add failing tests for capability ownership drift and workflow-order mismatch.
- [x] Extend `plugin_graph.py` to compare helper capability owners and workflow sequence with the graph.
- [x] Keep mascot conditional edge between still construction and motion integration.
- [x] Verify graph tests and full Claude CI.

### Task 2A: Activate research as runtime capability gates

**Files:**
- Create: `research/capability-notes/gates.json`
- Create: `scripts/research_gates.py`
- Create: `tests/test_research_gates.py`
- Modify: `helper/capabilities.json`
- Modify: `scripts/ecosystem_router.py`
- Modify: `helper/GUIDE.md`
- Modify: `research/capability-notes/adoption-matrix.md`

**Interfaces:**
- Consumes: `research/capability-notes/sources.json`, existing local capability references, helper capability owners.
- Produces: machine-readable gate IDs, provenance validation, route-level `research_gates`, CLI `python3 scripts/research_gates.py check`.

- [ ] Write RED tests requiring eight research gates and source/provenance linkage.
- [ ] Require every gate to name source(s), stage, severity, owners, local behavior, and implementation references.
- [ ] Link each helper capability to one or more gate IDs and reject missing/unknown gate references.
- [ ] Return applicable research gates from `route_request()` for complete and focused routes.
- [ ] Validate that all gate owners are shipping agents and all source names exist in `sources.json`.
- [ ] Update adoption matrix so it describes the runtime gate IDs rather than only prose mappings.
- [ ] Add `research_gates.py check` to CI and verify GREEN.

### Task 3: Skill contracts v3

**Files:**
- Modify every `skills/*/SKILL.md` entrypoint.
- Add/modify: `tests/test_skill_contracts.py`.

**Interfaces:**
- Consumes: `helper/GUIDE.md`, router intent names, artifact contracts, research gate IDs.
- Produces: consistent Purpose / Use when / Inputs / Outputs / Procedure / HOLD conditions / Related components / Research gates sections.

- [ ] Add structural tests covering every public `SKILL.md`.
- [ ] Refactor `post` into lightweight helper-backed routing guidance.
- [ ] Refactor `new-post`, `qa-post`, and `render-gif` around named helper artifacts and HOLD semantics.
- [ ] Standardize domain skills without duplicating orchestration.
- [ ] Wire relevant research gate IDs into every skill that owns or consumes them.
- [ ] Keep Arabic, Info-stories, render, motion, mascot, and exact-SVG behavior intact.
- [ ] Run all skill-contract tests plus existing Info-stories/mascot/research tests.

### Task 4: Agent contracts v3

**Files:**
- Modify every `agents/*.md`.
- Add/modify: `tests/test_agent_contracts.py`.

**Interfaces:**
- Consumes: graph required skill preloads, helper artifact contracts, research gate ownership.
- Produces: consistent Role / Inputs / Method / HOLD conditions / Quality gates / Research gates / Outputs sections.

- [ ] Add structural tests for all agents.
- [ ] Standardize all 14 agents while preserving specialist responsibilities.
- [ ] Ensure every output maps to a declared artifact or explicit parent-workflow return.
- [ ] Ban peer-orchestration language and ensure required `skills:` preload entries match the graph.
- [ ] Require each research gate owner to name and execute its gate in the worker contract.
- [ ] Run agent, graph, and research-gate validators.

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

- [ ] Add tests that all repository guidance points to `helper/GUIDE.md` and `research/capability-notes/gates.json` without redefining authority incorrectly.
- [ ] Write concise root guidance files and update existing adapter guidance.
- [ ] Run guidance tests.

### Task 6: README and durable documentation

**Files:**
- Rewrite: `README.md`
- Create: `docs/ecosystem.md`
- Create: `docs/routing.md`
- Create: `docs/agents.md`
- Create: `docs/skills.md`
- Create: `docs/research.md`
- Create: `docs/marketplace.md`
- Create: `docs/development.md`
- Add/modify: `tests/test_docs_contract.py`

**Interfaces:**
- Consumes: helper registries, research gate registry, actual skill/agent inventory, marketplace identity.
- Produces: concise README plus focused long-form docs.

- [ ] Add tests for required docs, inventory coverage, research-gate coverage, install commands, and broken local Markdown links.
- [ ] Rewrite README for product value, quick start, helper routing, research gates, workflows, examples, and validation.
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
- Consumes: version `3.0.0`, `scripts/ecosystem_router.py check`, `scripts/research_gates.py check`.
- Produces: clean Claude validation and real marketplace add/list/install smoke.

- [ ] Change version assertions to 3.0.0 and verify RED.
- [ ] Bump manifest and marketplace plugin version.
- [ ] Add ecosystem helper and research-gate validation to CI.
- [ ] Keep full-history checkout for whitespace integrity.
- [ ] Run validators and let PR CI run current Claude Code official validation/install smoke.

### Task 8: Full verification, review, and merge

**Files:**
- No new product files unless review finds a concrete defect.

**Interfaces:**
- Consumes: complete branch and all CI/review feedback.
- Produces: merged `main` commit only after verified head is green.

- [ ] Run full unit suite, compile, Info-stories, plugin graph, ecosystem helper, research gates, marketplace, shell/JSON, and whitespace checks.
- [ ] Update PR with architecture summary and exact validation matrix.
- [ ] Inspect Qlty, CodeRabbit/Qodo/review threads; fix concrete findings with regression tests.
- [ ] Require official `claude plugin validate .` and marketplace add/install smoke to pass on PR head.
- [ ] Squash merge with `expected_head_sha`.
- [ ] Verify merged files and `main` state after merge.