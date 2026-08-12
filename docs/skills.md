# Skills

The active skill inventory is declared in `helper/modules.json`. Every public skill follows the v3 contract: Purpose, Use when, Inputs, Outputs, Procedure, HOLD conditions, Related components, and Research gates.

## Visual intelligence contracts

`tools/story_retrieve.py` returns deterministic, stage-specific, bounded UTF-8 capsules. References influence only selected structure/motion/typography IDs; screenshot fonts are never treated as exact identification.

## Workflow and routing skills

### `post`

Public routing entrypoint. It reads `helper/GUIDE.md`, resolves the request, and routes complete creation to `new-post` or focused work to QA, render, design-study, mascot-animation, Info-stories, or verified community publishing.

### `new-post`

Canonical complete parent workflow. It owns evidence, creative concept approval, story, copy, layout, still, motion, mascot condition, render QA, adversarial review, independent verification, HOLD resolution, and final delivery.

### `qa-post`

Focused QA parent workflow for an existing artifact. It runs deterministic render evidence, local creative gates, adversarial critique, and independent verification.

### `render-gif`

Focused rendering workflow for approved HTML. It renders and reports motion, seam, and file-size evidence without redesigning the artifact.

### `share-demo`

Focused opt-in parent workflow for publishing a finished verified GIF/HTML result to the repository gallery. It requires explicit consent, final verification PASS, rights confirmation, a clean public-export preflight, and the exact `demo.gif + index.html + demo.json` package. Source-prompt publication is separately opt-in. It delegates only fork/branch/commit/push/PR mechanics to `community-publisher`; every PR requires maintainer manual review and merge.

## Domain skills

### `info-stories`

Resolves Story House, Visual Style, Story Archetype, Motion Patterns, design dials, UI story behavior, creative payoff, and reference-informed structure. The authoritative registry is the merged result of `scripts/info_stories.py::load_catalog()`.

### `caption`

Defines evidence-safe LinkedIn caption archetypes, opening hooks, truncation discipline, CTA behavior, and anti-slop review. It uses `hooked-design-copy` for attention-bearing openings.

### `artboard`

Defines static 1080x1350 composition, visual hierarchy, Story House token usage, structural originality, feed-scale legibility, contrast, UI mockup behavior, `creative-attractive-restrained` palettes, and `center-first` composition.

### `motion`

Defines deterministic seekable animation, one-loop-clock behavior, frame-zero completeness, meaning-driven Motion Patterns, changed-pixel restraint, and loop closure.

### `mascots`

Defines the infographic mascot communication role, exact-SVG identity rule, motion budget, and interaction with reading order. A named or official mascot without its exact SVG is a HOLD.

### `svg-mascot-animator`

Inspects and animates the exact supplied SVG. It covers riggability, identity preservation, physics/timing, creative directions, deterministic delivery, and validation.

### `render`

Defines frame capture, GIF assembly, static/mobile evidence, seam measurement, motion percentage, file-size budgets, and render acceptance.

### `arabic`

Defines Arabic and bilingual adaptation, RTL reading order, bidi isolation, Arabic typography, natural hook adaptation, and alignment exceptions when centered treatment would reduce comprehension.

## Creative defaults

The visual production skills inherit these plugin-local defaults from `helper/capabilities.json` and `helper/quality-gates.json`:

- palette: `creative-attractive-restrained`
- composition: `center-first`
- attention-bearing copy: `hooked-design-copy`
- complete story concept: `creative-payoff`

These defaults are blocking unless an approved brief or valid comprehension/fidelity exception applies.

## Research integration

Skills name the research gates they own or consume. The runtime gate registry lives in `research/capability-notes/gates.json`; research notes do not independently redefine production behavior. `share-demo` inherits `bounded-verification` as a publication prerequisite and does not create new claims.

Validate skill contracts with:

```bash
python3 -m unittest tests.test_skill_contracts -v
python3 scripts/ecosystem_doctor.py check
```
