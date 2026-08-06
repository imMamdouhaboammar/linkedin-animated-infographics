---
name: post
description: >-
  Router for building a LinkedIn post as a caption plus a 1080x1350 looping GIF infographic.
  Use EVERY TIME the user wants a LinkedIn post, an animated infographic, a GIF for LinkedIn,
  a carousel-killer single visual, a system map, stack map, workflow diagram, or cheat sheet
  visual, or asks how creators make those looping Claude/AI/GTM infographics. Also trigger on
  Arabic requests like "اعملي بوست لينكدإن", "انفوجرافيك متحرك", "GIF للينكدإن", "خريطة نظام",
  "بوست فيه فيجوال", or when the user pastes a topic, repo, tool, playbook, or skill and wants
  it turned into a LinkedIn visual. Even for a small ask like "make me a hook" or "animate this
  diagram", start here.
---

# LinkedIn Motion

The post format that dominates AI and GTM LinkedIn: a tightly structured caption paired with
a single 1080x1350 looping GIF that reads as a designed infographic rather than a slide.

## The one insight that makes this work

These GIFs are **static infographics with a small fraction of the canvas moving**, and that
motion is a **reading pointer** guiding the eye through the diagram in the order the author
wants it read. Everything else is frozen. That is why they look expensive.

Judge the moving fraction on `build_gif.py`'s reported `motion:` figure, not on how much of
the canvas looks busy. Under 2% is healthy.

## Pipeline

```
topic  →  archetype pick  →  caption  →  artboard  →  motion  →  render  →  QA  →  publish
```

Each stage has its own skill. Load the one you are in, not all of them.

| Stage | Skill | Load it when |
|---|---|---|
| Caption | `linkedin-motion:caption` | writing or editing any caption. Seven archetypes, the truncation cut, the ban list |
| Layout | `linkedin-motion:artboard` | choosing a visual archetype, picking colours, building the still |
| Motion | `linkedin-motion:motion` | writing any animation CSS. Ten seekable primitives and the loop rules |
| Mascots | `linkedin-motion:mascots` | putting a character on the artboard. Three roles, seek-safety, budget |
| Render | `linkedin-motion:render` | capturing frames, assembling the GIF, running the gates, publishing |
| Arabic | `linkedin-motion:arabic` | any Arabic or bilingual output. It is not a translation job |

Three workflow skills run the whole thing end to end: `linkedin-motion:new-post`,
`linkedin-motion:render-gif`, `linkedin-motion:qa-post`.

## Agents

Delegate rather than doing everything on the main thread. The render loop in particular
produces a lot of output that does not belong in the conversation.

| Agent | Give it |
|---|---|
| `caption-writer` | the topic and the CTA. Returns a caption that has already passed the ban list |
| `artboard-builder` | the approved caption and archetype. Returns a still that passes `check_render.py` |
| `motion-engineer` | an approved still. Returns the animated artboard with a clean loop |
| `render-qa` | a built artboard. Runs the render, reports gate failures, changes nothing |

## Non-negotiables

1. Exactly one `#artboard` element at `width:1080px; height:1350px`.
2. All animation is CSS or WAAPI or SMIL, `infinite`, sharing one `--loop` or an integer
   division of it. `requestAnimationFrame` cannot be seeked and will not render.
3. Fonts are system-safe or base64-embedded. Never `@import` from a network.
4. Colour comes from **House 0 — Muted Reference**, the default palette. Do not invent one
   and do not raise the saturation.
5. Nothing moves in the outer 48px margin.
6. If there is a mascot, the mascot **is** the reading pointer and the abstract particle is
   deleted.
7. No em dashes and no denial-then-reveal contrast in the caption, English or Arabic.

## Working method

1. Ask only what you cannot infer: the one takeaway, and the CTA. No long intake.
2. Propose the caption archetype and visual archetype in one line each. Get a yes.
3. Write the caption first. It decides what the visual has to carry.
4. Build the still. Show it. Get a yes. **This is the approval gate.**
5. Animate last, and animate less than feels right.
6. Render, QA, deliver the GIF plus the caption plus the first-comment text.

Animating a layout nobody has approved wastes more time than anything else in this workflow.

## Setup

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh
```

Installs Playwright, a Chrome binary, and checks for ffmpeg. Everything else in
`${CLAUDE_PLUGIN_ROOT}/scripts/` runs on plain Python 3.
