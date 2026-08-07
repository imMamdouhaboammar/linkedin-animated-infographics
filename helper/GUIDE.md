# LLM Routing Guide

Read this file before choosing a production skill or worker.

## Authority

The machine-readable routing authority is split across:

- `helper/router.json` for intent and conditional routing
- `helper/capabilities.json` for capability ownership and research-gate linkage
- `helper/artifacts.json` for handoff artifacts
- `research/capability-notes/sources.json` for inspected upstream provenance
- `research/capability-notes/gates.json` for adopted runtime research gates
- `architecture/plugin-graph.json` for executable worker order and required skill preloads
- `scripts/info_stories.py::load_catalog()` for the merged Info-stories registry

If prose conflicts with one of those contracts, stop and repair the drift instead of guessing.

## Decision protocol

1. Classify the user intent.
   - create or redesign a post: `create-post`
   - inspect a finished post: `qa`
   - render an approved HTML artboard: `render`
   - study a visual reference: `design-study`
   - animate an SVG mascot as a focused task: `mascot-animation`
   - compose an Info-story without running the whole post pipeline: `info-story`
2. Load the route from `router.json`.
3. Resolve capability owners from `capabilities.json`.
4. Apply the route's research gates from `research/capability-notes/gates.json`.
5. Apply conditional asset/language/UI/reference gates before generation.
6. Confirm required assets and evidence.
7. Invoke the selected workflow or focused skill.
8. Workers return artifacts to the parent workflow. They do not coordinate peers through hidden handoffs.
9. Stop on a blocking `HOLD`; do not improvise around it.

## Research gates

Research is active production guidance, not background reading. The current adopted gate IDs are:

- `prose-specificity`: reject named filler and low-information copy patterns per slot
- `voice-preservation`: protect facts, mechanisms, names, numbers, and deliberate voice while editing
- `design-dials`: require explicit design variance, visual density, and motion intensity decisions
- `structural-originality`: reject palette-only reskins and require meaningful structural variation
- `reference-dna`: when a reference exists, diagnose reusable structure without cloning distinctive work
- `contrast-discipline`: enforce the established semantic-token and contrast floors
- `evidence-traceability`: tie factual claims, product states, metrics, logos, and acceptance rows to evidence
- `bounded-verification`: keep verification independent and allow at most two targeted repair attempts

The gate registry records source provenance, stage, severity, owners, local behavior, and implementation references. Upstream repositories are research inputs only; their working copies are not runtime dependencies and are not packaged with the plugin.

Validate this layer with:

```bash
python3 scripts/research_gates.py check
```

## Conditional gates

### Arabic or RTL

Add the `arabic` skill before copy and layout work. Preserve bidi isolation, RTL ordering, Arabic typography, and the existing render constraints.

### Named or official mascot

The exact user-supplied or task-attached SVG is mandatory. If it is missing, return `HOLD: exact SVG required`.

The main model asks the user to attach the exact SVG. A subagent returns the HOLD to its parent workflow. Never redraw, approximate, substitute, or generate a lookalike automatically.

### UI mockup story

Enable the `ui-mockup-fidelity` capability. Product states, features, metrics, integrations, logos, and proof that appear real must be evidence-backed. Clearly label concept UI or fictional data when it could be mistaken for documented product behavior. The route applies `structural-originality`, `contrast-discipline`, and `evidence-traceability` where applicable.

### Visual references

Use `design-study` to extract reusable design DNA. Do not copy a reference pixel-for-pixel or treat its palette as the only source of variation. When a reference is present, activate `reference-dna` before layout production.

### Static versus animated output

Static work stops after still QA and final verification. Animated work adds motion direction, optional mascot animation, motion implementation, and render QA.

## Parent workflow rule

`new-post` is the canonical parent workflow for complete post creation. It owns user approvals, HOLD resolution, repair loops, and final delivery. Every worker returns a bounded artifact to the parent workflow.

## HOLD semantics

A HOLD means a required input or blocking quality gate is missing. Common cases:

- exact official mascot SVG missing
- unsupported factual proof
- unreadable contrast
- incompatible Info-stories composition
- unresolved blocking research-gate finding
- required render evidence unavailable

Do not convert a HOLD into invented content. State the missing requirement and wait for the parent workflow or user to resolve it.

## Final verification

A complete post is not ready because generation finished. The shipping path ends with render evidence, adversarial review, and independent verification. The final verifier may request at most two targeted repair attempts before escalation.
