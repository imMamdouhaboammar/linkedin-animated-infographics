# LLM Routing Guide

Read this file before choosing a production skill or worker.

## Authority

The machine-readable routing authority is split across:

- `helper/router.json` for intent and conditional routing
- `helper/capabilities.json` for capability ownership
- `helper/artifacts.json` for handoff artifacts
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
3. Apply conditional gates before generation.
4. Confirm required assets and evidence.
5. Invoke the selected workflow or focused skill.
6. Workers return artifacts to the parent workflow. They do not coordinate peers through hidden handoffs.
7. Stop on a blocking `HOLD`; do not improvise around it.

## Conditional gates

### Arabic or RTL

Add the `arabic` skill before copy and layout work. Preserve bidi isolation, RTL ordering, Arabic typography, and the existing render constraints.

### Named or official mascot

The exact user-supplied or task-attached SVG is mandatory. If it is missing, return `HOLD: exact SVG required`.

The main model asks the user to attach the exact SVG. A subagent returns the HOLD to its parent workflow. Never redraw, approximate, substitute, or generate a lookalike automatically.

### UI mockup story

Enable the `ui-mockup-fidelity` capability. Product states, features, metrics, integrations, logos, and proof that appear real must be evidence-backed. Clearly label concept UI or fictional data when it could be mistaken for documented product behavior.

### Visual references

Use `design-study` to extract reusable design DNA. Do not copy a reference pixel-for-pixel or treat its palette as the only source of variation.

### Static versus animated output

Static work stops after still QA and final verification. Animated work adds motion direction, optional mascot animation, motion implementation, and render QA.

## Parent workflow rule

`new-post` is the canonical parent workflow for complete post creation. It owns user approvals, HOLD resolution, repair loops, and final delivery. Every worker returns a bounded artifact to the parent workflow.

## HOLD semantics

A HOLD means a required input or quality gate is missing. Common cases:

- exact official mascot SVG missing
- unsupported factual proof
- unreadable contrast
- incompatible Info-stories composition
- required render evidence unavailable

Do not convert a HOLD into invented content. State the missing requirement and wait for the parent workflow or user to resolve it.

## Final verification

A complete post is not ready because generation finished. The shipping path ends with render evidence, adversarial review, and independent verification. The final verifier may request at most two targeted repair attempts before escalation.
