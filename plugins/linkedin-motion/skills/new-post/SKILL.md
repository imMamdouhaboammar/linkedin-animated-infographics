---
name: new-post
description: Run the full post pipeline end to end, from topic to a delivered GIF plus caption plus first comment.
disable-model-invocation: true
argument-hint: "[topic or URL] [optional: --arabic] [optional: --mascot]"
---

# /linkedin-motion:new-post

Topic: **$ARGUMENTS**

Run the pipeline. Do not skip the approval gates; they exist because animating a layout nobody
approved is the most expensive mistake in this workflow.

## 1. Intake, kept short

Ask only two things, in one message: **what is the one takeaway**, and **what is the CTA**.
Infer everything else. If the argument is a URL, fetch it first and infer from the page.

## 2. Propose, one line each

State the caption archetype and the visual archetype with a one-line reason for each. Wait for
a yes or a redirect. If `--mascot` was passed, also state which mascot roles you will use and
run the budget check now.

## 3. Caption

Delegate to the `caption-writer` agent with the topic, takeaway, archetype, and CTA. Load
`linkedin-motion:caption` yourself only if you are writing it inline.

Show the caption. Get a yes before building anything.

## 4. Still

Delegate to the `artboard-builder` agent with the approved caption and archetype. It returns
`build/post.html` and `build/still.png` already passing `check_render.py`.

Show the still. **This is the approval gate.** Get a yes.

## 5. Motion

Delegate to the `motion-engineer` agent. Two primitives, one `--loop`, nothing in the margin.
If a mascot is in play it runs `bake_mascot.py` and pastes the blocks whole.

## 6. Render and QA

Delegate to the `render-qa` agent. It renders, runs the gates, and reports failures without
changing anything. Fix what it reports and send it back until it passes.

## 7. Deliver

Present, in this order:

1. the GIF
2. the caption in a copyable block
3. the first-comment text
4. two lines on the numbers: `motion:`, seam, and file size

Then stop. No postamble.

If `--arabic` was passed, load `linkedin-motion:arabic` before step 3. The layout mirrors and
the type scale changes; it is not a translation pass.
