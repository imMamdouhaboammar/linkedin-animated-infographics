# Agents

The active worker inventory is declared in `helper/modules.json` and the executable order is declared in `architecture/plugin-graph.json`. Every agent returns a bounded artifact or verdict to the parent workflow. Agents do not coordinate peer agents directly.

## Complete workflow agents

### `design-study`

Diagnoses visual references into reusable design DNA before concept generation. It owns `reference-dna` when references are present and returns `build/design-study.json`.

### `evidence-checker`

Defines the factual boundary before creative work begins. It classifies claims, product states, metrics, logos, proof, and UI evidence, then returns `build/evidence.json`. It owns `evidence-traceability` at intake.

### `creative-director`

Generates at least three evidence-safe creative directions before story architecture. Each direction contains a visual hook, copy hook, aha mechanic, story shape, visual/style recommendations, evidence dependencies, risks, and why it earns attention. It returns `build/creative-concepts.json`.

This agent owns the local creative concept layer. It applies `hooked-design-copy` and `creative-payoff` without inventing claims or using spectacle as a substitute for explanation.

### `story-architect`

Turns the selected creative direction into a deterministic Info-stories brief. It resolves Story Archetype, Visual Style, Story House, Motion Patterns, and design dials, then returns `build/story-brief.json`.

### `palette-curator`

Resolves the Story House and semantic token roles. It enforces `creative-attractive-restrained` palette behavior and the `contrast-discipline` research gate. It returns `build/palette-check.json`.

### `copy-compressor`

Compresses source material into infographic-sized design copy while protecting facts, names, numbers, mechanisms, voice, and the approved copy hook. It applies `prose-specificity`, `voice-preservation`, and evidence constraints, then returns `build/artboard-copy.json`.

### `layout-composer`

Turns the selected concept, story brief, copy, palette, and optional reference study into a static hierarchy and topology specification. It applies `center-first-composition`, `design-dials`, `structural-originality`, and `reference-dna` when active. It returns `build/layout-spec.json`.

### `caption-writer`

Writes the LinkedIn caption and first comment. It applies `hooked-design-copy` to the opening, keeps one caption archetype, preserves evidence, and returns `build/caption.md` plus `build/first-comment.md`.

### `artboard-builder`

Builds the approved 1080x1350 HTML still and rendered PNG. It preserves the selected creative payoff, Story House tokens, center-first layout or documented exception, UI fidelity, and contrast. It returns `build/post.html` and `build/still.png`.

### `motion-director`

Chooses zero to two meaning-driven Motion Patterns after the still is approved. Motion must communicate hierarchy, sequence, reveal, state, route, or the selected creative payoff. It returns `build/motion-direction.json`.

### `mascot-animator`

Conditional worker for a named or official mascot. It requires the exact user-supplied or task-attached SVG, inspects the real geometry, preserves identity, selects a communication-led creative direction, and returns `build/mascot/motion-contract.json`. Missing exact SVG is a HOLD.

### `motion-engineer`

Implements the approved seekable motion direction on the approved still. It preserves the resolved story brief, frame-zero completeness, one loop clock, motion budget, and exact mascot identity when present.

### `render-qa`

Produces deterministic static/GIF evidence without editing the artboard. It checks frame 0, feed-scale legibility, contrast, changed-pixel motion, seam, safe zone, duration, and file size. It returns `build/render-report.json`.

### `post-critic`

Performs adversarial review before independent verification. It explicitly checks anti-slop, design-taste, `hooked-design-copy`, `creative-payoff`, `restrained-palette`, `center-first-composition`, UI fidelity, mascot identity, motion meaning, and evidence safety. It returns `build/critic-report.json`.

### `story-verifier`

Read-only independent acceptance worker. It inspects artifact evidence directly, records one evidence row per criterion, enforces `evidence-traceability` and `bounded-verification`, and returns `build/verification-report.json` with `PASS`, `FAIL:fixable`, or `FAIL:escalate`.

## Coordination contract

The canonical complete sequence is declared in `architecture/plugin-graph.json` and mirrored by the `create-post` route. The parent workflow owns sequencing, user approvals, HOLD resolution, and the maximum-two targeted repair loop.

Validate all worker contracts with:

```bash
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 -m unittest tests.test_agent_contracts -v
```
