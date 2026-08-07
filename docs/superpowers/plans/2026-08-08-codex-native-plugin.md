# Codex Native Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship version 3.2.0 as a first-class OpenAI skills-only plugin for Codex and ChatGPT, with repo marketplace distribution, host parity validation, public-submission materials, and no duplicated product core.

**Architecture:** Keep `skills/`, `agents/`, `helper/`, `research/`, and `architecture/` canonical. Add OpenAI packaging and marketplace adapters around that core, then enforce cross-host parity with a dedicated validator and CI gate. Public submission remains prepared but manual.

**Tech Stack:** JSON manifests, TOML Codex config, Markdown policy/docs, Python 3 validators, unittest, GitHub Actions, Claude Code validator, documented Codex plugin marketplace CLI where non-interactive smoke is reliable.

## Global Constraints

- Release version is `3.2.0`.
- OpenAI plugin type is `skills-only`; do not add an MCP server.
- `.codex-plugin/plugin.json` is the OpenAI package entry point.
- `.agents/plugins/marketplace.json` is the repo-scoped Codex/ChatGPT marketplace.
- Canonical skills remain `./skills/`; do not copy them into a Codex-only tree.
- Public submission is prepared but never claimed as submitted or published automatically.
- Five positive and three negative reviewer test cases are mandatory.
- Claude and Codex must share plugin identity, version, routes, safety gates, exact-SVG rules, and community publishing semantics.
- Community contributions still stop at a PR and require maintainer manual review/merge.

---

### Task 1: OpenAI plugin manifest and repo marketplace

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `.agents/plugins/marketplace.json`
- Create: `tests/test_codex_plugin.py`

**Interfaces:**
- Consumes: canonical `skills/` root and `.claude-plugin/plugin.json` identity/version
- Produces: OpenAI manifest and marketplace data loaded later by `validate_codex_plugin.py`

- [ ] **Step 1: Write failing manifest/marketplace tests**

Add tests asserting `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` exist, use version `3.2.0`, reference `./skills/`, expose root plugin source `./`, and contain `AVAILABLE` / `ON_INSTALL` / `Productivity` marketplace fields.

- [ ] **Step 2: Run tests to verify RED**

Run: `python3 -m unittest tests.test_codex_plugin -v`
Expected: FAIL because OpenAI package files do not exist.

- [ ] **Step 3: Add minimal valid OpenAI packaging**

Create `.codex-plugin/plugin.json` with top-level identity/publisher fields, `skills: "./skills/"`, and an `interface` object containing display name, descriptions, developer name, category, capabilities, repository-hosted website/legal links, starter prompts, and real visual asset paths only.

Create `.agents/plugins/marketplace.json` with a single root plugin entry using:

```json
{
  "name": "mamdouh-creative-tools",
  "interface": {"displayName": "Mamdouh Creative Tools"},
  "plugins": [{
    "name": "linkedin-animated-infographics",
    "source": {"source": "local", "path": "./"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Productivity"
  }]
}
```

- [ ] **Step 4: Run focused tests to verify GREEN**

Run: `python3 -m unittest tests.test_codex_plugin -v`
Expected: PASS for packaging tests added in this task.

- [ ] **Step 5: Commit**

Commit message: `feat: add native Codex plugin packaging`

---

### Task 2: Codex parity registry and strict validator

**Files:**
- Create: `compatibility/codex.json`
- Create: `scripts/validate_codex_plugin.py`
- Modify: `tests/test_codex_plugin.py`

**Interfaces:**
- Consumes: Claude plugin/marketplace, OpenAI plugin/marketplace, `.codex/config.toml`, `skills/`, helper registries
- Produces: `validate_codex_plugin(root: Path) -> list[str]` and CLI exit status

- [ ] **Step 1: Write failing parity/validator tests**

Cover version mismatch, unsafe manifest path, missing skills root, malformed marketplace policy, dead `.codex/agents/*.toml` references, and mismatch between compatibility registry and live paths.

- [ ] **Step 2: Run tests to verify RED**

Run: `python3 -m unittest tests.test_codex_plugin -v`
Expected: FAIL because validator/registry do not exist.

- [ ] **Step 3: Implement `compatibility/codex.json`**

Declare version `3.2.0`, manifest/marketplace paths, canonical skills/helper/graph paths, surfaces (`codex`, `chatgpt`), submission type `skills-only`, and parity invariants.

- [ ] **Step 4: Implement `scripts/validate_codex_plugin.py`**

Implement repo-bound path resolution and deterministic checks for:

```python
def validate_codex_plugin(root: Path = ROOT) -> list[str]:
    ...
```

Validate manifest identity/version, canonical skills path, install metadata, marketplace source/policies/category, compatibility registry drift, Codex config custom-agent references, legal/support files, submission case counts, and all release-version copies.

- [ ] **Step 5: Run focused tests to verify GREEN**

Run: `python3 -m unittest tests.test_codex_plugin -v`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `feat: add Codex parity validator`

---

### Task 3: Repair and strengthen Codex repository configuration

**Files:**
- Modify: `.codex/AGENTS.md`
- Modify: `.codex/config.toml`
- Create: `.codex/agents/explorer.toml`
- Create: `.codex/agents/reviewer.toml`
- Create: `.codex/agents/docs-researcher.toml`
- Modify: `tests/test_codex_plugin.py`

**Interfaces:**
- Consumes: current Codex config schema conventions and repository helper authority
- Produces: a self-consistent repo-development Codex setup with no dead config-file references

- [ ] **Step 1: Write failing config-reference tests**

Require every `.codex/config.toml` custom agent `config_file` to resolve inside `.codex/agents/`, and require each role to be narrow maintenance guidance rather than a parallel product worker graph.

- [ ] **Step 2: Run focused tests to verify RED**

Run: `python3 -m unittest tests.test_codex_plugin -v`
Expected: FAIL because the three referenced agent TOMLs are missing.

- [ ] **Step 3: Add the real agent TOMLs and update guidance**

Create read-only explorer, correctness/security reviewer, and docs researcher configs. Update `.codex/AGENTS.md` to cover `share-demo`, OpenAI packaging, parity validation, and optional subagent use with parent-controlled orchestration.

- [ ] **Step 4: Run focused tests to verify GREEN**

Run: `python3 -m unittest tests.test_codex_plugin -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: complete Codex repository configuration`

---

### Task 4: Public OpenAI submission preparation and legal/support material

**Files:**
- Create: `PRIVACY.md`
- Create: `TERMS.md`
- Create: `SUPPORT.md`
- Create: `submission/openai-plugin.json`
- Create: `submission/test-cases.json`
- Create: `submission/README.md`
- Modify: `tests/test_codex_plugin.py`

**Interfaces:**
- Consumes: plugin metadata and current OpenAI public-submission requirements
- Produces: repository-hosted review materials and deterministic submission readiness data

- [ ] **Step 1: Write failing submission-material tests**

Require public docs, submission type `skills-only`, five positive cases, three negative cases, starter prompts, release notes, and explicit external prerequisites for Apps Management write access and verified publisher identity.

- [ ] **Step 2: Run focused tests to verify RED**

Run: `python3 -m unittest tests.test_codex_plugin -v`
Expected: FAIL because submission/legal files are missing.

- [ ] **Step 3: Add accurate legal/support docs**

Describe the plugin as local skills-based software. State that community publication is opt-in, only approved demo package data is sent through user-authenticated GitHub tooling, and source prompts stay excluded unless separately consented to.

- [ ] **Step 4: Add submission metadata and exactly eight tests**

Positive reviewer cases cover create-post, Info-story, QA, exact-SVG mascot with asset, and explicit community sharing. Negative cases cover missing exact mascot SVG, unverified/unsafe demo export, and community sharing without explicit consent.

- [ ] **Step 5: Run focused tests and validator to verify GREEN**

Run:

```bash
python3 -m unittest tests.test_codex_plugin -v
python3 scripts/validate_codex_plugin.py
```

Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `docs: prepare OpenAI plugin submission materials`

---

### Task 5: Dual-host docs and release metadata

**Files:**
- Create: `docs/codex.md`
- Modify: `README.md`
- Modify: `docs/marketplace.md`
- Modify: `docs/development.md`
- Modify: `docs/ecosystem.md`
- Modify: `AGENTS.md`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `tests/test_marketplace.py`
- Modify: `tests/test_docs_contract.py`
- Modify: `tests/test_repository_guidance.py`

**Interfaces:**
- Consumes: final OpenAI and Claude package data
- Produces: user-facing dual-host installation docs and release version `3.2.0`

- [ ] **Step 1: Write failing release/docs tests**

Require version `3.2.0` across Claude/OpenAI manifests and marketplace data, README sections for Claude and Codex, documented Codex repo marketplace commands, and a focused `docs/codex.md` link from the README.

- [ ] **Step 2: Run relevant tests to verify RED**

Run:

```bash
python3 -m unittest tests.test_marketplace tests.test_docs_contract tests.test_repository_guidance -v
```

Expected: FAIL on stale `3.1.0` and missing Codex docs.

- [ ] **Step 3: Update release metadata and concise docs**

Keep README as a gateway. Add Codex/ChatGPT installation beside Claude installation, explain that the same canonical Skills power both hosts, and document public-directory status as submission-ready rather than published.

- [ ] **Step 4: Run docs/release tests to verify GREEN**

Run the command from Step 2 plus `python3 scripts/validate_codex_plugin.py`.
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `docs: publish dual-host 3.2.0 guidance`

---

### Task 6: CI dual-host gate and final verification

**Files:**
- Modify: `.github/workflows/claude-plugin-validation.yml`
- Modify: `docs/development.md` if CI command list changes
- Modify: `tests/test_codex_plugin.py` only if CI contract requires a regression assertion

**Interfaces:**
- Consumes: all prior tasks
- Produces: a PR gate proving shared runtime + Claude packaging + OpenAI packaging are coherent

- [ ] **Step 1: Add a failing CI-contract assertion if needed**

Require workflow text to execute `python3 scripts/validate_codex_plugin.py` and JSON-parse `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `compatibility/codex.json`, `submission/openai-plugin.json`, and `submission/test-cases.json`.

- [ ] **Step 2: Update CI**

Rename display name to a host-neutral title such as `Plugin Validation`, keep all existing shared/Claude gates, add the Codex validator and JSON syntax checks, and do not add a fake interactive marketplace smoke.

If a documented non-interactive Codex CLI marketplace smoke can be proven in the runner, add it; otherwise retain deterministic structural validation and document the limitation.

- [ ] **Step 3: Run full deterministic gate**

Run through GitHub Actions on the feature PR:

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
```

Expected: all pass, plus official Claude plugin validation and existing Claude Marketplace smoke in CI.

- [ ] **Step 4: Review and merge gate**

Open a PR, inspect Qodo/Qlty/CodeRabbit output, fix reproducible findings with regression coverage, resolve threads only after fixes, re-run the exact-head gate, then squash merge with expected head SHA.

- [ ] **Step 5: Post-merge verification**

Fetch from `main` and verify `.codex-plugin/plugin.json` version `3.2.0`, `.agents/plugins/marketplace.json`, `compatibility/codex.json`, public submission materials, and merged PR state.
