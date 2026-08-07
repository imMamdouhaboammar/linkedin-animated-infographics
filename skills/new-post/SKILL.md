---
name: new-post
description: Run the full post pipeline end to end, from topic to a delivered GIF or static infographic plus caption and first comment.
disable-model-invocation: true
argument-hint: "[topic or URL] [optional: --arabic] [optional: --mascot]"
---

# /linkedin-animated-infographics:new-post

Topic: **$ARGUMENTS**

The parent workflow owns orchestration. Workers return artifacts to this workflow; do not ask one worker to coordinate its peers.

## 1. Reference diagnosis

If the user supplied screenshots, GIFs, previous designs, or visual references, delegate to `design-study` and save the structured result as `build/design-study.json`. If there is no visual reference, record that this stage is not applicable and continue.

## 2. Evidence inventory

Delegate to `evidence-checker` with the source material and all claims, numbers, product names, proof slots, and logos likely to appear. Save `build/evidence.json`. Unsupported proof is blocked before copy or layout work begins. A source with no external factual claims still gets a short evidence record saying so.

## 3. Story contract

Delegate to `story-architect` with the topic, one takeaway, CTA, language, output mode, `build/design-study.json` when present, and `build/evidence.json`. Save the deterministic result as `build/story-brief.json`.

State the four Info-stories choices and one reason per choice. If the user explicitly chose an axis, preserve it unless a hard compatibility or contrast rule fails.

## 4. Palette contract

Delegate to `palette-curator` with `build/story-brief.json` and any brand colours. Save the complete verified token block and contrast result as `build/palette-check.json`. A failing text or state pair holds the build.

## 5. Artboard copy

Delegate to `copy-compressor` with the source, evidence record, Story Archetype, and target story beats. Save slot-keyed copy and protected facts as `build/artboard-copy.json`. Keep intentional short labels; remove generic filler and unsupported claims.

## 6. Static layout specification

Delegate to `layout-composer` with the story brief, palette check, artboard copy, and optional design study. Save `build/layout-spec.json`, including zone order, visual anchor, hierarchy, structural fingerprint, and asset requirements.

## 7. Caption

Delegate to `caption-writer` with the approved facts, one takeaway, CTA, and narrative context. Save the caption as `build/caption.md` and first-comment text as `build/first-comment.md`.

Show the caption and the resolved story direction. Get approval before building the still.

## 8. Still construction

Delegate to `artboard-builder` with `build/story-brief.json`, `build/palette-check.json`, `build/artboard-copy.json`, `build/layout-spec.json`, and the approved caption. It returns `build/post.html` and `build/still.png` after static checks.

Show the still. This is the visual approval gate. Get approval before motion.

## 9. Motion direction

For animated output, delegate to `motion-director` with the approved still, layout spec, story brief, and mascot role when applicable. Save `build/motion-direction.json`. Static output records this stage as skipped.

## 10. Motion implementation

For animated output, delegate to `motion-engineer` with the approved still, story brief, and motion-direction artifact. It returns the animated `build/post.html`. Static output skips this stage.

## 11. Render mechanics and gates

Delegate to `render-qa`. Save its gate-by-gate evidence as `build/render-report.json`. A `HOLD` returns control to this parent workflow for a targeted fix and re-run.

## 12. Adversarial review

Delegate to `post-critic` with the rendered artifact, caption, evidence record, structural fingerprint, and render report. Save `build/critic-report.json`. Resolve every must-fix item or record why it is not applicable before independent verification.

## 13. Independent acceptance

Delegate to `story-verifier` with the artifact paths, story brief, evidence record, render report, critic report, and explicit acceptance criteria. Save `build/verification-report.json`. `FAIL:fixable` may trigger a targeted fix and re-check. Maximum two targeted fix attempts; a third unresolved failure escalates.

## 14. Deliver

Deliver, in this order:

1. GIF or static artifact
2. caption
3. first-comment text
4. resolved Story House, Visual Style, Story Archetype, and Motion Patterns
5. render numbers when applicable
6. final verification verdict

If `--arabic` is present, apply `linkedin-animated-infographics:arabic` before copy/layout production. If `--mascot` is present, the exact-SVG mascot gate defined by the mascot skills must pass before any mascot animation is attempted.
