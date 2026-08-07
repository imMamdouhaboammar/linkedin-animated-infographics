# Upstream capability experiment report

Date: 2026-08-07
Branch: `feat/info-stories`

## Question

Do the adapted capabilities from stop-slop, no-ai-slop, taste-skill, Hallmark, and COG-second-brain add useful constraints without replacing the existing deterministic artboard and motion pipeline?

## Experiment A: categorically different story compositions

Two acceptance briefs were resolved from the same local registry.

### Ember Signal

- House: Ember Paper
- Style: Signal Sheet
- Archetype: Framework in One Page
- Motion: Sequential Highlight + Chip / Badge Pulse
- Design dials: variance 5, motion 4, density 8
- Composition check: PASS

### Midnight Command

- House: Midnight Operator
- Style: Command Canvas
- Archetype: One Prompt, Full Workflow
- Motion: Type-On Terminal + Soft Zoom Focus
- Design dials: variance 6, motion 7, density 5
- Composition check: PASS

Result: the registry can produce a dense editorial board and a dark terminal-led composition without sharing a surface or structural grammar.

## Experiment B: deterministic scaffold

The Ember Signal brief was generated twice from identical inputs.

Both files produced SHA256:

`cc62c3c1601107928b48a4a8e2645836300085607916b0dd46347143703ef117`

`cmp` result: byte-identical.

Result: the selection/scaffold layer is deterministic. Visual variety comes from explicit registry choices and content shape, not random output.

## Experiment C: anti-slop gate

Baseline copy:

`Here's the thing: it's not just automation, it's a revolution. In conclusion, this changes everything.`

Detected findings:

1. `throat-clearing`
2. `binary-contrast`
3. `importance-puffery`
4. `recap-ending`

Revised factual copy:

`The verifier reads the rendered artifact and records evidence for each acceptance criterion.`

Detected findings: none.

Result: the detector identifies named structural writing patterns without classifying authorship and leaves a specific plain sentence untouched.

## Experiment D: structural variety

Previous and candidate compositions were compared across six fingerprint axes.

A palette-only reskin changed 0/6 axes and failed with:

`Structural fingerprint changes only 0/6 axes; change at least 2.`

A candidate that changed topology, card grammar, and divider language passed.

Result: visual variety is now measurable at structure level rather than inferred from colour changes.

## Experiment E: reference study contract

The user-attached `Claude Code for Outbound` reference was converted into a structured study report covering surface, type roles, structure, rhythm, motion, visual anchor, local recommendations, and copy boundaries.

`validate_study_report()` result: PASS.

The uploaded reference contains 100 frames over 10.0 seconds. Motion recommendations were limited to observable restrained local state changes; the study does not invent motion for one-frame uploads.

## What each upstream contributed

- stop-slop: directness, rhythm, named formula detection
- no-ai-slop: voice preservation, portability check, detect/edit separation
- taste-skill: design variance, motion intensity, visual density, mechanical pre-flight
- Hallmark: structural fingerprinting, design-DNA study, token discipline, anti-reskin rule
- COG-second-brain: independent verifier, evidence rows, bounded repair loop

## What was deliberately excluded

- React/Next/Tailwind implementation rules
- website navigation, forms, dark-mode, responsive-browser gates
- mandatory GSAP or scroll hijacking
- random aesthetic selection
- copying marketplace templates or signature work
- shipping any upstream working copy inside the plugin

## Current conclusion

The imported ideas are useful when translated into local invariants. They now strengthen story selection, copy diagnosis, structural variety, reference study, and acceptance verification while leaving the existing HTML/GIF execution pipeline authoritative.

## Render-environment smoke

A real `check_render.py` smoke was attempted on `assets/template-flow-map.html`.

1. Initial attempt reported Playwright missing.
2. Python Playwright, Pillow, bundled Chromium, and Playwright FFmpeg were installed without elevated privileges.
3. Browser launch then stopped because the Codespace image lacks the OS library `libatk-1.0.so.0`.

The missing library requires an operating-system package installation that is outside the permissions available in this session. No privileged workaround was attempted.

Status: browser screenshot/mobile-render verification is **environment-blocked** in this Codespace. The feature did not modify `check_render.py`, `capture_frames.py`, `build_gif.py`, or `render.sh`; static lint and all non-browser tests remain available and are run in the final gate.


## Final non-browser gate

- Unit tests: 40 passed, 0 failed
- Python compile: passed for `scripts/` and `tools/`
- Catalog validation: passed
- Upstream inventory snapshot: passed
- Both acceptance composition checks: passed
- Reference study schema: passed
- Stale `linkedin-motion` namespace scan: no matches in core skills/agents
- `git diff --check`: passed
