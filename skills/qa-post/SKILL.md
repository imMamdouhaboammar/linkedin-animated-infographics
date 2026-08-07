---
name: qa-post
description: Run deterministic render checks, local creative gates, adversarial critique, and independent evidence-backed acceptance against a built infographic before shipment.
disable-model-invocation: true
argument-hint: "[path/to/artboard.html] [optional: path/to/caption.md]"
---

# /linkedin-animated-infographics:qa-post

Arguments: **$ARGUMENTS**

## Purpose

Act as the focused **parent workflow** for QA. Report evidence and route targeted fixes; do not silently edit the artifact or let the producing worker grade its own result.

Read `helper/GUIDE.md` before checking the artifact.

## Use when

Use for a finished or nearly finished artboard/GIF that needs shipping acceptance, regression review, visual/caption red-teaming, or verification after a targeted fix.

## Inputs

- artboard HTML and rendered static/GIF evidence
- optional caption and first comment
- story brief, selected creative concept, evidence table, and layout spec when available
- optional mascot identity/motion contract
- explicit acceptance criteria when supplied

## Outputs

Return `build/render-report.json`, `build/critic-report.json`, `build/verification-report.json`, and one final verdict: `SHIP` or `HOLD: <the one thing to fix first>`.

## Procedure

1. Run deterministic render checks:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py <path> --out /tmp/qa-still.png
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py <path> --mobile
bash ${CLAUDE_PLUGIN_ROOT}/scripts/lint_artboard.sh <path>
```

2. Walk the `render` skill and `references/qa-gates.md`. Inspect frame 0 and feed-width output. For GIFs, capture seam, changed-pixel motion, duration, and file-size evidence.
3. If a caption exists, apply the `caption` skill and `hooked-design-copy`. Check truncation, one archetype, factual support, CTA discipline, and anti-slop findings.
4. Delegate adversarial review to `post-critic`. It must evaluate `creative-payoff`, `restrained-palette`, `center-first-composition`, UI fidelity, mascot identity when present, motion meaning, and evidence safety.
5. Any must-fix item produces a HOLD until corrected or proven not applicable.
6. Delegate independent acceptance to `story-verifier`. The verifier reads the actual artifacts and evidence, not a worker summary.
7. Respect the maximum-two targeted fix attempts before escalation.

## HOLD conditions

Return HOLD for a failed render gate, unsupported factual claim, generic/unsupported hero hook, missing promised creative payoff, excessive or unjustified palette treatment, invalid alignment exception, UI/mascot fidelity failure, or independent verifier failure.

## Related components

- routing authority: `helper/GUIDE.md`
- local quality gates: `helper/quality-gates.json`
- render skill: `skills/render/SKILL.md`
- caption skill: `skills/caption/SKILL.md`
- adversarial worker: `agents/post-critic.md`
- independent verifier: `agents/story-verifier.md`
- verification reference: `skills/info-stories/references/verification-loop.md`

## Research gates

QA enforces applicable `prose-specificity`, `voice-preservation`, `structural-originality`, `contrast-discipline`, and `evidence-traceability` gates. `bounded-verification` is always active for final acceptance and prevents unbounded repair loops.
