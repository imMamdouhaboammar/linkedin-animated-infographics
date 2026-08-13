# MasterOne Orchestrator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add MasterOne as the front-door onboarding, persistent-preference, and routing experience without replacing the existing production parent workflows.

**Architecture:** A public `masterone` skill owns entry orchestration and downstream route transfer. A bounded `masterone` agent normalizes context and readiness but returns decisions to its parent workflow. A stdlib-only profile CLI persists project preferences and manages a bounded `CLAUDE.md` pointer section.

**Tech Stack:** Markdown agent/skill contracts, JSON registries/schema, Python 3 stdlib, unittest, existing plugin graph/router validators.

## Global Constraints

- Preserve `new-post` as the canonical complete-production parent workflow.
- Keep workers from coordinating peer workers.
- Do not change the existing `create-post` agent order.
- Do not invent copyright, attribution, fonts, identity assets, mascot identities, or reference intent.
- Keep preferences project-local in `.linkedin-infographics/profile.json`.
- Keep transient post facts in the existing runtime-context request.
- `CLAUDE.md` is an instruction index; MasterOne may change only its managed marker region.

---

### Task 1: Profile CLI and schema

**Files:**
- Create: `schemas/masterone-profile.schema.json`
- Create: `scripts/masterone_profile.py`
- Create: `tests/test_masterone_profile.py`

**Interfaces:**
- Consumes: project workspace path and a supported intent.
- Produces: `init`, `status`, `set`, `sync-claude`, and `check` CLI behavior plus `.linkedin-infographics/profile.json`.

- [ ] Write integration tests for first-run initialization, intent-aware readiness, safe dotted updates, invalid-update preservation, and idempotent CLAUDE managed-section syncing.
- [ ] Confirm those tests fail before the script exists.
- [ ] Implement the minimum stdlib CLI and schema contract to pass the tests.
- [ ] Run `python3 -m unittest tests.test_masterone_profile -v`.

### Task 2: MasterOne skill, agent, and routing registration

**Files:**
- Create: `skills/masterone/SKILL.md`
- Create: `agents/masterone.md`
- Modify: `helper/router.json`
- Modify: `helper/modules.json`
- Modify: `architecture/plugin-graph.json`
- Modify: `tests/test_agent_contracts.py`
- Modify: `tests/test_plugin_graph.py`
- Create: `tests/test_masterone_contract.py`

**Interfaces:**
- Consumes: profile readiness and existing router intents.
- Produces: a discoverable front-door route that transfers control to existing parent workflows.

- [ ] Add tests proving MasterOne is the front door, is reachable in module/graph registries, preserves the existing `new-post` sequence, and names all supported downstream intents.
- [ ] Confirm the contract tests fail before registration.
- [ ] Add the agent and skill using the existing contract format.
- [ ] Register `route:masterone`, `front_door`, module inventory, and graph agent/workflow metadata.
- [ ] Run the focused contract, plugin-graph, and ecosystem-doctor tests.

### Task 3: Agent-facing documentation

**Files:**
- Modify: `CLAUDE.md`
- Modify: `AGENTS.md`
- Modify: `helper/GUIDE.md`
- Modify: `docs/agents.md`
- Modify: `docs/routing.md`

**Interfaces:**
- Consumes: the machine-readable MasterOne contracts.
- Produces: concise context pointers that make MasterOne the first entry experience without duplicating the full schema.

- [ ] Add the bounded MasterOne pointer and managed-marker contract to `CLAUDE.md`.
- [ ] Add equivalent cross-client guidance to `AGENTS.md`.
- [ ] Document MasterOne in helper and routing docs while keeping `new-post` authoritative for production sequencing.
- [ ] Run documentation and ecosystem validation tests.

### Task 4: Full verification and review

**Files:**
- No new production files.

**Interfaces:**
- Consumes: the complete branch.
- Produces: passing repository checks and reviewed changes.

- [ ] Run `python3 -m unittest discover -s tests -v`.
- [ ] Run `python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts`.
- [ ] Run `python3 scripts/ecosystem_router.py check`.
- [ ] Run `python3 scripts/plugin_graph.py check`.
- [ ] Run `python3 scripts/ecosystem_doctor.py check`.
- [ ] Run `python3 scripts/runtime_context.py check`.
- [ ] Run `python3 scripts/validate_marketplace.py`.
- [ ] Review the final diff for spec compliance and repository standards before merge.
