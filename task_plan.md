# Task Plan: LinkedIn Animated Infographics Intelligent Orchestration Engine

## Goal
Design, author, and integrate a dedicated, intelligent orchestration skill and multi-agent execution workflow that positions `masterone` as the mandatory front-door onboarding entry point, handles persistent project profiling (`.linkedin-infographics/profile.json`), routes requests safely, coordinates the sequential handoff through `new-post` and the 17-worker pipeline, and incorporates an **Intelligent Agent Router (GPT-5.6 Sol / High-Reasoning Tier Delegation)** with a **30-Second Watchdog Liveness Heartbeat** to ensure stall-free, deterministic execution.

---

## Current Status
- **Current Phase:** Phase 6: Agent Router & 30s Watchdog Integration
- **Overall Progress:** 100%
- **Status:** complete

---

## Phases

### Phase 1: Ecosystem Audit & Contract Synthesis [COMPLETE]
- [x] Audit `helper/router.json`, `helper/capabilities.json`, `skills/masterone/SKILL.md`, and `architecture/plugin-graph.json`.
- [x] Define the complete contract between MasterOne, router, and the 17-subagent production chain.
- [x] Record findings in `findings.md`.

### Phase 2: Authoring the Intelligent Orchestrator Skill [COMPLETE]
- [x] Author `.agents/skills/linkedin-animated-infographics/SKILL.md` following `writing-skills` standards.
- [x] Include detailed front-door interaction rules for `masterone` (language, audience, footer, typography, brand assets).
- [x] Document intent classification (`create-post`, `qa`, `render`, `design-study`, `mascot-animation`, `info-story`, `share-demo`).
- [x] Define step-by-step worker handoffs and artifact contracts (`build/story-brief.json`, `build/asset-plan.json`, `build/type-spec.json`, etc.).
- [x] Author `.agents/skills/linkedin-animated-infographics/references/orchestration-playbook.md` with complete schemas and prompts.
- [x] Add anti-rationalization tables, common pitfalls, and verification checklists.

### Phase 3: Agent Catalog & Host Packaging Integration [COMPLETE]
- [x] Verify `.agents/skills.json` and `.agents/agents/catalog.json`.
- [x] Sync with `scripts/antigravity_agents.py` and `compatibility/antigravity.json`.

### Phase 4: Verification & Test Suite Execution [COMPLETE]
- [x] Run `python3 scripts/validate_antigravity_plugin.py` -> PASS
- [x] Run `python3 scripts/antigravity_agents.py check` -> PASS (19 agents verified)
- [x] Run `python3 scripts/ecosystem_doctor.py check` -> PASS
- [x] Run `python3 scripts/ecosystem_router.py check` -> PASS
- [x] Run `python3 scripts/research_gates.py check` -> PASS
- [x] Run `python3 scripts/plugin_graph.py check` -> PASS
- [x] Run `python3 -m unittest discover -s tests -v` -> 469 tests PASSED

### Phase 5: Comprehensive Walkthrough & Knowledge Transfer [COMPLETE]
- [x] Produce complete English documentation and instructions for seamless execution.
- [x] Update `progress.md`.

### Phase 6: Agent Router (GPT-5.6 Sol Delegation) & 30s Watchdog Integration [COMPLETE]
- [x] Defined Model Tier Routing (High-Reasoning GPT-5.6 Sol / Pro for Director, Critic, Verifier vs High-Speed Flash for Copy, Captions, Checks).
- [x] Defined 30-Second Liveness Watchdog Protocol via `schedule` tool.
- [x] Updated `.agents/skills/linkedin-animated-infographics/SKILL.md` and `references/orchestration-playbook.md`.
- [x] Defined and registered `linkedin-orchestrator-watchdog` subagent with Watchdog & Router directives.
- [x] Ran validator suite -> 100% PASS.

---

## Decisions Made
| Decision | Rationale |
| :--- | :--- |
| Use `masterone` as mandatory front-door | Prevents re-asking user preferences repeatedly; loads `.linkedin-infographics/profile.json` first. |
| Strict single-clock `--loop` motion | Guarantees zero-seam infinite loops and headless seekability. |
| Pure embedded/system fonts & SVGs | Eliminates network latency / blank frames during Puppeteer frame capture. |
| GPT-5.6 Sol / Pro Tier Delegation | Allocates high-compute models specifically to non-linear cognitive tasks (Concept, Layout, Motion Physics, Critique, Verification). |
| 30s Watchdog Liveness Heartbeat | Prevents silent hangs in multi-agent pipelines and enforces a strict 2-attempt bounded repair limit. |
