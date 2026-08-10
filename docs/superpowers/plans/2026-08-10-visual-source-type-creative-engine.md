# Visual Source, Typography, and Creative Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add blocking Lobe-first identity sourcing, intentional typography selection, and cleaner structurally varied concept generation to the complete infographic workflow.

**Architecture:** Add two bounded workers, `asset-curator` and `type-curator`, with blocking artifacts consumed by downstream production. Extend machine-readable helper registries and quality gates, add deterministic artifact validators, then mirror the behavior inside the isolated OpenAI infographic studio. Preserve the existing parent-worker architecture and deterministic static/render pipeline.

**Tech Stack:** Python 3, Markdown agent/Skill contracts, JSON helper registries, unittest, HTML/CSS/SVG production contracts

## Global Constraints

- User-supplied official identity assets take precedence.
- Supported named AI/tool identities use Lobe as the canonical source.
- Missing verified named identities return HOLD instead of approximation.
- Final render assets must be local or embedded, not network-dependent.
- User-specified typography takes precedence.
- Remote font imports are forbidden in frame capture.
- Creative direction must produce real structural variation and preserve the existing evidence boundary.
- Existing Claude and OpenAI host isolation must remain valid.

---

### Task 1: Add red contract tests for the new behavior

**Files:**
- Create: `tests/test_visual_source_typography_engine.py`
- Modify: `tests/test_plugin_graph.py`
- Modify: `tests/test_repository_guidance.py`

**Interfaces:**
- Consumes: current helper registries and worker graph
- Produces: failing tests that define the new workers, capabilities, gates, artifacts, Lobe source rules, typography rules, and OpenAI parity

- [ ] **Step 1: Write tests that require the new graph order**

Require `asset-curator` after `evidence-checker` and before `creative-director`, and `type-curator` after `palette-curator` and before `copy-compressor`.

- [ ] **Step 2: Write tests for helper registries and quality gates**

Require `visual-asset-sourcing`, `typography-direction`, `verified-identity-assets`, `intentional-typography`, and `clean-creative-structure`.

- [ ] **Step 3: Write tests for source and typography contracts**

Assert that the asset policy names `https://lobehub.com/icons/skill.md`, `@lobehub/icons-static-svg`, the user-official then Lobe precedence, local/embedded render assets, and HOLD on unresolved named identities. Assert that typography rejects remote `@import` and produces a deterministic type artifact.

- [ ] **Step 4: Write OpenAI parity assertions**

Require asset and type passes plus both reference files in the OpenAI studio.

- [ ] **Step 5: Run focused tests and confirm RED**

Run:

```bash
python3 -m unittest tests.test_visual_source_typography_engine tests.test_plugin_graph tests.test_repository_guidance -v
```

Expected: failures for missing workers, capabilities, gates, artifacts, and references.

---

### Task 2: Add the identity and typography reference contracts plus validators

**Files:**
- Create: `skills/info-stories/references/asset-source-policy.md`
- Create: `skills/info-stories/references/typography-direction.md`
- Create: `tools/asset_policy_check.py`
- Create: `tools/type_spec_check.py`
- Modify: `helper/modules.json`

**Interfaces:**
- Produces: `asset_policy_check.validate(payload) -> list[str]`
- Produces: `type_spec_check.validate(payload) -> list[str]`
- Consumed by: new workers, artboard/QA contracts, tests, public tool registry

- [ ] **Step 1: Implement asset policy reference**

Document supported named identity precedence and the required `build/asset-plan.json` fields.

- [ ] **Step 2: Implement typography reference**

Document selection precedence, curated type directions, loading strategies, minimum output fields, and render determinism.

- [ ] **Step 3: Implement asset validator**

Reject named identity records whose `source_type` is not `user-official` or `lobe`, reject missing Lobe source metadata for `lobe`, reject unresolved identity status, and require local/embedded render disposition.

- [ ] **Step 4: Implement type validator**

Reject missing role families, missing fallbacks, unknown loading strategy, remote font imports, and unreasoned same-family headline/body use.

- [ ] **Step 5: Register both tools**

Add them to `helper/modules.json` with explicit tests and reachability.

- [ ] **Step 6: Run validator tests**

Expected: new tool-level tests PASS.

---

### Task 3: Add bounded asset and type workers and wire the machine-readable graph

**Files:**
- Create: `agents/asset-curator.md`
- Create: `agents/type-curator.md`
- Modify: `helper/router.json`
- Modify: `helper/capabilities.json`
- Modify: `helper/quality-gates.json`
- Modify: `helper/artifacts.json`
- Modify: `helper/modules.json`
- Modify: `architecture/plugin-graph.json`

**Interfaces:**
- `asset-curator` produces `build/asset-plan.json`
- `type-curator` produces `build/type-spec.json`
- Downstream consumers read those artifacts rather than re-sourcing assets or inventing type choices

- [ ] **Step 1: Create `asset-curator`**

The worker reads the evidence record and asset policy, resolves explicit assets, applies Lobe-first sourcing where covered, records source metadata, runs `asset_policy_check.py`, and returns HOLD when unresolved.

- [ ] **Step 2: Create `type-curator`**

The worker reads story/palette/reference context, selects a deterministic type direction, runs `type_spec_check.py`, and returns a complete type artifact.

- [ ] **Step 3: Add capabilities and gates**

Add `visual-asset-sourcing`, `typography-direction`, `verified-identity-assets`, `intentional-typography`, and `clean-creative-structure` with exact owners.

- [ ] **Step 4: Add artifacts and routing order**

Insert both workers into the canonical sequence and register artifact producers/consumers.

- [ ] **Step 5: Run graph and agent contract tests**

Run:

```bash
python3 -m unittest tests.test_plugin_graph tests.test_agent_contracts -v
python3 scripts/plugin_graph.py check
```

Expected: PASS.

---

### Task 4: Make downstream creative, layout, artboard, mascot, critic, and verifier honor the artifacts

**Files:**
- Modify: `agents/creative-director.md`
- Modify: `agents/story-architect.md`
- Modify: `agents/layout-composer.md`
- Modify: `agents/artboard-builder.md`
- Modify: `agents/mascot-animator.md`
- Modify: `agents/post-critic.md`
- Modify: `agents/story-verifier.md`
- Modify: `skills/artboard/SKILL.md`
- Modify: `skills/info-stories/references/design-taste-gates.md`
- Modify: `skills/new-post/SKILL.md`

**Interfaces:**
- Consumes: `build/asset-plan.json`, `build/type-spec.json`
- Preserves: selected identity assets and type decisions through final output

- [ ] **Step 1: Strengthen creative concept grammar**

Require relationship, dominant anchor, structural archetype, containment strategy, negative-space strategy, and motion job for each direction. Add the blocking `clean-creative-structure` check.

- [ ] **Step 2: Bind layout and artboard to approved assets and type**

Require exact asset references from `asset-plan` and exact typography roles from `type-spec`; no downstream substitutions.

- [ ] **Step 3: Update mascot path**

Use the verified identity asset from `asset-plan` when the identity is Lobe-backed or user-supplied. Keep existing exact identity preservation.

- [ ] **Step 4: Update critic and verifier**

Explicitly evaluate all three new gates and reject remote render-time identity/font dependencies.

- [ ] **Step 5: Update parent workflow order and outputs**

Add both artifacts and worker steps to `new-post` while preserving the rest of the shipping sequence.

---

### Task 5: Mirror the behavior in the OpenAI infographic studio

**Files:**
- Modify: `openai-skills/linkedin-infographic-studio/SKILL.md`
- Modify: `openai-skills/linkedin-infographic-studio/references/openai-runtime.md`
- Modify: `openai-skills/linkedin-infographic-studio/references/role-passes.md`
- Modify: `openai-skills/linkedin-infographic-studio/references/visual-quality-contract.md`
- Create: `openai-skills/linkedin-infographic-studio/references/asset-source-policy.md`
- Create: `openai-skills/linkedin-infographic-studio/references/typography-direction.md`

**Interfaces:**
- OpenAI sequence gains asset-curator and type-curator reasoning passes
- Final verification checks identity provenance and render-safe typography

- [ ] **Step 1: Add references to the studio preload list**

- [ ] **Step 2: Add asset and typography passes to the required sequence**

- [ ] **Step 3: Add OpenAI-specific HOLD and verification behavior**

- [ ] **Step 4: Run OpenAI contract tests**

Expected: PASS with no Claude-only dependency introduced.

---

### Task 6: Update repository guidance and run the full gate

**Files:**
- Modify: `helper/GUIDE.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `.agents/skills/linkedin-animated-infographics/SKILL.md`
- Modify: `.claude/skills/linkedin-animated-infographics/SKILL.md`
- Modify: `.codex/AGENTS.md`
- Modify: `tests/test_repository_guidance.py`
- Modify: `tests/test_visual_defaults.py`

**Interfaces:**
- All host guidance points to the same machine-readable authority and names the new identity/type rules

- [ ] **Step 1: Update guidance with concise pointers only**

Keep detailed behavior in the reference contracts and helper registries. Guidance names the leading concepts `Lobe-first identity sourcing` and `intentional typography` and points to their source files.

- [ ] **Step 2: Run focused guidance tests**

- [ ] **Step 3: Run the complete repository gate**

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/validate_marketplace.py
```

Expected: all checks PASS.

- [ ] **Step 4: Review diff for duplicated policy text and stale pointers**

Detailed policy must exist in one authoritative reference per host distribution, with other files pointing to it instead of duplicating it.

- [ ] **Step 5: Commit and open PR**

Use a focused PR that explains the new behavioral gates, artifacts, validators, and host parity.
