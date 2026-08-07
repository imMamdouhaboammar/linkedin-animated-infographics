# Ecosystem Routing Kernel v3 Design

## Goal

Turn the repository from a collection of strong skills, agents, and research notes into one coherent, self-describing creative-production ecosystem with a central LLM routing helper, enforceable contracts, active research-derived gates, consistent worker interfaces, durable documentation, and a Claude Marketplace package that remains installable from the same repository.

## Design principles

1. One routing authority. `helper/` becomes the canonical guide for deciding what workflow, skills, agents, asset gates, research gates, and artifacts a request needs.
2. One execution path. `new-post` remains the parent production orchestrator; workers never rely on hidden peer-to-peer delegation.
3. Machine-readable contracts first. Human docs explain contracts but do not redefine them.
4. Evidence before generation. Claims, product UI, brand assets, and official mascots are gated before visual production.
5. Exact assets stay exact. Named official mascots require the exact user-supplied/task-attached SVG and may not be substituted.
6. Extend, do not fork. Info-stories extensions merge deterministically through `load_catalog()`.
7. Research must ship as behavior. Adopted research capability notes must map to explicit runtime gates, owners, stages, and tests; research may not remain dead documentation.
8. All public surfaces are testable. Router, research gates, skills, agents, docs, marketplace, hooks, and registries get structural validation.
9. Preserve the existing install identity unless a concrete incompatibility requires change.

## Architecture

### 1. Top-level helper

Create `helper/` beside `skills/` and `agents/`.

It contains:

- `helper/README.md`: concise explanation for humans and coding agents
- `helper/GUIDE.md`: LLM-facing routing and decision protocol
- `helper/router.json`: intent-to-workflow routing rules and conditional gates
- `helper/capabilities.json`: capability ownership, prerequisites, and research-gate references
- `helper/artifacts.json`: artifact names, producers, consumers, and blocking semantics

The helper does not render or generate content itself. It decides which existing capability should act, what it must receive, what research-derived gates apply, and what evidence it must return.

### 2. Router implementation

Add `scripts/ecosystem_router.py` as a deterministic validator/router over the helper registries. It exposes:

- `load_ecosystem(root)`
- `validate_ecosystem(root) -> list[str]`
- `route_request(request: dict, root) -> dict`
- CLI commands `check`, `route`, and `explain`

A thin public CLI `tools/route_request.py` calls the shared implementation.

Routing is explicit for these intents:

- full post creation
- QA/review
- GIF rendering
- focused design study
- focused mascot animation
- focused Info-stories composition

Conditional gates include Arabic/RTL, official mascot SVG, UI mockup evidence fidelity, reference-study input, static versus animated output, and research-derived quality gates.

### 3. Artifact contracts

Every important handoff gets a named artifact contract. Minimum production artifacts:

- `build/design-study.json`
- `build/evidence.json`
- `build/story-brief.json`
- `build/palette-check.json`
- `build/artboard-copy.json`
- `build/layout-spec.json`
- `build/caption.md`
- `build/first-comment.md`
- `build/post.html`
- `build/still.png`
- `build/motion-direction.json`
- `build/mascot-request.json`
- `build/mascot/motion-contract.json`
- `build/render-report.json`
- `build/critic-report.json`
- `build/verification-report.json`

`helper/artifacts.json` records producer, consumers, required inputs, and blocking semantics.

### 4. Research capability gates

`research/` becomes an active, validated input to production rather than a passive archive.

The existing provenance snapshot in `research/capability-notes/sources.json` remains the source record for inspected upstream repositories. Add `research/capability-notes/gates.json` as the machine-readable adoption contract. Each gate records:

- a stable gate ID
- one or more source names from `sources.json`
- the local independently-worded behavior being adopted
- the stage where the gate runs
- owning agents
- blocking versus advisory severity
- direct references to the local implementation or reference document

Required first-party gates:

- `prose-specificity`: named prose-pattern detection and removal of generic filler, informed by stop-slop and no-ai-slop
- `voice-preservation`: preserve specific facts, voice, and intentional short labels while editing, informed by no-ai-slop
- `design-dials`: explicit variance/density/motion decisions, informed by taste-skill
- `structural-originality`: reject palette-only reskins and require meaningful structural variation, informed by taste-skill and Hallmark
- `reference-dna`: extract reusable structural design DNA without signature-work copying, informed by Hallmark
- `contrast-discipline`: enforce semantic token and contrast floors, informed by taste-skill and Hallmark
- `evidence-traceability`: require evidence rows for factual claims and proof, informed by COG-second-brain and Hallmark
- `bounded-verification`: independent verification with a maximum two targeted repair attempts, informed by COG-second-brain

Add `scripts/research_gates.py` to validate provenance, source names, gate ownership, local implementation references, and linkage to `helper/capabilities.json`. The ecosystem router loads the gates and returns applicable gate IDs with each route.

No upstream working copy is packaged with the plugin. Only provenance, independently-worded local rules, and machine-readable adoption contracts ship.

### 5. Skill contracts v3

All user-facing skills adopt a consistent structure:

- Purpose
- Use when
- Inputs
- Outputs
- Procedure
- HOLD conditions
- Related components
- Research gates

`post` becomes a lightweight entry router that points to the helper and canonical workflows. `new-post`, `qa-post`, and `render-gif` remain explicit workflow skills. Domain skills stay focused and stop duplicating orchestration prose.

### 6. Agent contracts v3

Every agent adopts a consistent worker contract:

- Role
- Inputs
- Method
- HOLD conditions
- Quality gates
- Research gates
- Outputs / return contract

Required skills are preloaded through `skills:` frontmatter. Worker output always returns to the parent workflow. No agent is allowed to assume it can coordinate peer agents directly.

The existing 14 agents remain, including `mascot-animator`. Capability ownership is synchronized between `helper/capabilities.json`, `research/capability-notes/gates.json`, and `architecture/plugin-graph.json`.

### 7. Info-stories and UI Mockup Stories

The merged registry produced by `scripts/info_stories.py::load_catalog()` remains authoritative. UI Mockup Stories remain a first-party extension.

The helper adds routing knowledge for UI stories:

- documented product UI must be evidence-backed
- concept UI must be labeled when it could be mistaken for real product evidence
- unsupported metrics/features/integrations remain blocked
- feed-width legibility is a production gate
- structural-originality, design-dials, evidence-traceability, and contrast-discipline research gates apply where relevant

### 8. Mascot Animator v3 integration

The existing exact-SVG identity gate remains mandatory.

The helper adds a routing rule: a named/official mascot without an exact SVG results in `HOLD: exact SVG required`. The main model asks the user for the SVG; a subagent returns the HOLD to its parent.

Creative directions remain adaptable starting points, not fixed templates. Identity-critical geometry, proportions, brand colors, marks, and distinctive face details cannot be silently redrawn.

### 9. Documentation model

README becomes a concise product and quick-start document. Detailed material moves to focused docs:

- `docs/ecosystem.md`: architecture, capability, and research-gate overview
- `docs/routing.md`: helper routing protocol and examples
- `docs/agents.md`: complete agent catalog and handoff/research-gate contracts
- `docs/skills.md`: complete skill catalog and selection guidance
- `docs/research.md`: provenance, adopted gates, deliberate exclusions, and how research becomes local behavior
- `docs/marketplace.md`: install, validate, release, and versioning
- `docs/development.md`: tests, validators, contribution workflow, browser-render caveats

Repository-specific coding-agent guidance in `.agents/`, `.claude/`, and `.codex/` must point to the same helper authority rather than inventing parallel rules.

### 10. Claude Marketplace

Keep the same-repository marketplace and stable install identity:

- marketplace: `mamdouh-creative-tools`
- plugin: `linkedin-animated-infographics`
- source: `./`
- strict mode: true

Bump the plugin release to `3.0.0` because the internal routing/contracts architecture changes materially. Marketplace and plugin versions must match.

CI continues to install the current Claude Code release and must run:

- full Python unit suite
- Python compilation
- Info-stories validation
- plugin graph validation
- ecosystem helper validation
- research-gate/provenance validation
- marketplace validation
- hook/shell syntax
- whitespace integrity
- `claude plugin validate .`
- local marketplace add/list/install smoke

### 11. Branch and PR policy

Historical branches already represented in `main` are not re-merged. New work starts from current `main` on `feat/ecosystem-routing-kernel-v3`.

The feature is merged only when:

- all deterministic tests pass
- research gates are linked to provenance and shipping owners
- Claude plugin validation/install smoke pass
- no unresolved review thread remains
- Qlty or equivalent repository checks do not report a blocking failure
- the PR head SHA verified is the SHA merged

## Non-goals

- no new rendering engine
- no framework migration
- no replacement of the deterministic HTML/SVG/GIF pipeline
- no duplication of Info-stories registries
- no automatic mascot generation when an official mascot was requested
- no packaging of cloned upstream repositories
- no verbatim import of upstream prose or implementation
- no requirement to use every agent for every focused request

## Success criteria

A fresh LLM or coding agent can enter the repository, read `helper/GUIDE.md`, route a request to the correct workflow, identify required assets and HOLD states, know the exact artifacts each worker exchanges, see which research-derived gates apply and why, and discover the authoritative docs without reading the entire repository.

Every adopted research capability is traceable from upstream provenance to a local gate, local implementation, shipping owner, and regression test.

A clean Claude Code environment can add the same-repository marketplace, install version 3.0.0, discover the skills and agents, and pass the repository validation workflow.