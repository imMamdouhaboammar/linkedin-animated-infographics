---
name: new-post
description: Run the full post pipeline end to end, from topic to a delivered GIF plus caption plus first comment.
disable-model-invocation: true
argument-hint: "[topic or URL] [optional: --arabic] [optional: --mascot]"
---

# /linkedin-animated-infographics:new-post

Topic: **$ARGUMENTS**

Run the pipeline. Do not skip approval gates.

## 1. Intake

Ask only two things in one message: **what is the one takeaway**, and **what is the CTA**. Infer everything else from the topic or supplied source. If the source contains facts or numbers, mark them for `evidence-checker` before compression.

## 2. Resolve the Info-stories brief

Delegate to `story-architect`. It loads `linkedin-animated-infographics:info-stories` and resolves:

- Story Archetype
- Visual Style
- Story House
- zero to two Motion Patterns
- the Visual Style design dials

If references or previous designs were supplied, run `design-study` first and pass the accepted design DNA into `story-architect`.

Save the resolved scaffold as `build/story-brief.json`. State the four choices and the caption archetype with one short reason each. If `--mascot` was passed, state the mascot role too. Wait for a yes or redirect before writing the caption.

## 3. Caption and compressed artboard copy

Delegate caption writing to `caption-writer`. Use `copy-compressor` for artboard slots when the source is too dense, and `evidence-checker` for any claim that will appear visually. Load `linkedin-animated-infographics:caption` only if writing inline.

Show the caption. Get a yes before building anything.

## 4. Still

Delegate to `artboard-builder` with the approved caption, compressed artboard copy, and `build/story-brief.json`. The story brief owns the Story House tokens, Visual Style, and preferred existing artboard archetype. The builder returns `build/post.html` and `build/still.png` already passing `check_render.py`.

Show the still. **This is the approval gate.** Get a yes before motion.

## 5. Motion

Delegate to `motion-engineer` with `build/story-brief.json`. It implements the resolved Motion Patterns using the existing seekable primitives. If output mode is static, skip this step. If a mascot is in play, the mascot pointer replaces any competing pointer primitive rather than becoming a third motion.

## 6. Render and independent QA

Delegate render mechanics to `render-qa`. Fix render failures and re-run until the existing QA gates pass.

Then delegate final acceptance to `story-verifier`. It reads the artifact directly and uses `skills/info-stories/references/verification-loop.md`. A `FAIL:fixable` may trigger a targeted fix and re-check. Maximum two targeted fix attempts. A third unresolved failure escalates instead of looping.

## 7. Deliver

Present, in this order:

1. the GIF or static artifact
2. the caption in a copyable block
3. the first-comment text
4. the resolved Info-stories four-axis selection
5. render numbers: motion, seam, and file size when applicable

Then stop. No postamble.

If `--arabic` was passed, load `linkedin-animated-infographics:arabic` before step 3. Arabic changes layout and type behavior; it is not a translation pass.
