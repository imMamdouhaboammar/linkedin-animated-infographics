---
name: linkedin-animated-infographics
description: Produce LinkedIn posts in the high-save "animated infographic" format — a structured caption plus a 1080x1350 looping GIF infographic rendered from HTML/CSS/SVG via headless Chrome and ffmpeg. Use this skill EVERY TIME the user wants a LinkedIn post, a carousel-killer single visual, an animated infographic, a GIF for LinkedIn, a "system map", "stack map", "workflow diagram", "cheat sheet" visual, or asks how creators make those looping Claude/AI/GTM infographics. Also trigger on Arabic requests like "اعملي بوست لينكدإن", "انفوجرافيك متحرك", "GIF للينكدإن", "خريطة نظام", "بوست فيه فيجوال", or when the user pastes a topic, repo, tool, playbook, or skill and wants it turned into a LinkedIn visual. Covers 7 caption archetypes, 13 visual archetypes, a motion vocabulary of 9 animation primitives, deterministic frame capture, GIF size budgeting under LinkedIn's limits, and full RTL/Arabic adaptation. Even for a small ask like "make me a hook" or "animate this diagram", use this skill.
license: MIT
metadata:
  version: 1.0.0
  author: Mamdouh Aboammar (@imMamdouhaboammar)
  homepage: https://github.com/imMamdouhaboammar/linkedin-animated-infographics
---

# LinkedIn Animated Infographics

A production system for the post format that dominates AI/GTM LinkedIn right now: a
tightly structured caption paired with a single 1080x1350 looping GIF that reads as a
designed infographic, not a slide.

## The one insight that makes this work

These GIFs are **static infographics with 10–15% of the canvas moving**.

Forensics on two reference files confirms it:

| | Charlie Hills "Board of Advisers" | FullEnrich "Agent Orbit" |
|---|---|---|
| Size | 1080x1350 | 1080x1350 |
| Frames | 30 | 230 |
| Frame delay | 120ms (8.3 fps) | 30–40ms (~30 fps) |
| Duration | 3.6s | 7.67s |
| Loop | infinite | infinite |
| File size | 4.8 MB | 2.4 MB |
| What actually moves | An accent outline stepping through 4 setup boxes + dots travelling down 4 curved connectors | Mascot nodes orbiting a dashed circle + the circle drawing itself solid + one arrow reveal |

Everything else — headline, body cards, quotes, verdict panel, footer — is frozen.
That is why they look expensive. Motion is used as a **reading pointer**, guiding the
eye through the diagram in the order the author wants it read.

If more than ~20% of the canvas is moving, the design has failed. Reduce before rendering.

## Pipeline

```
topic  →  archetype pick  →  caption  →  HTML/CSS/SVG artboard  →  deterministic
          (§1 + §2)          (§3)        (§4, 1080x1350)          frame capture (§5)
                                                                        ↓
                                          publish (§7)  ←  QA (§6)  ←  GIF assembly
```

The renderer is headless Chrome driven by Playwright. Animations are **seeked**, not
recorded in real time — `document.getAnimations()` is paused and `currentTime` is set
per frame. That gives pixel-identical, jitter-free frames and a mathematically exact
loop close. Real-time screen recording produces the wobbly output that reads as amateur.

---

## §1 — Choose the caption archetype

Read `references/caption-patterns.md` for the full anatomy of each, with line-by-line
skeletons and real examples. Quick router:

| Archetype | Use when | Signature move |
|---|---|---|
| **A. Numbered Inventory** | You have N discrete items (skills, tools, prompts) | "My 9 X." then 9 one-line entries |
| **B. Result Case Study** | You have a real before/after metric | Metric in line 1, system in the middle, metric again at the end |
| **C. Bundle Manifest** | You're gating a free resource | "Here's what you'll get" + `▫️` list + comment keyword |
| **D. Setup Walkthrough** | The value is a procedure with exact clicks | Numbered steps, no theory, a time claim ("live in 24 minutes") |
| **E. Operating Story** | You made a real decision at your company | First-person, concrete before/after, no CTA at all |
| **F. Belief Correction** | You have a POV and no product to push | Short declarative lines, aphoristic close, follow/repost CTA |

Do not blend archetypes. Blending is the most common failure — a manifest with a case
study bolted on reads as a pitch deck.

## §2 — Choose the visual archetype

Read `references/visual-archetypes.md` for the full catalogue with structural specs.
Thirteen archetypes, reverse-engineered from the reference set. Quick router:

| Content shape | Archetype |
|---|---|
| A hierarchy of files/modules | **Directory Map** |
| A linear process with stages | **Pipeline Stages** |
| A cyclical process, no start | **Orbit Cycle** |
| Many inputs converging on one output | **Flow Map + Verdict** |
| A flat catalogue of tools | **Logo Grid** |
| N independent items of equal weight | **Trading Card Grid** |
| A branching decision or dependency graph | **Node Tree** |
| One product/tool announcement | **Terminal Card** |
| Dense reference material | **Cheat Sheet Poster** |
| A spec, benchmark or timeline | **Spec Sheet** |
| A sequential how-to | **Annotated Blueprint** |
| A mascot-led flowchart | **Character Flowchart** |
| A catalogue you can *show* running | **Specimen Grid** |

Caption archetype and visual archetype are chosen independently. B pairs well with
Pipeline Stages; C with Directory Map or Trading Card Grid; D with Annotated Blueprint.

## §3 — Write the caption

Full rules in `references/caption-patterns.md`. Non-negotiables:

- **Line 1 must survive the truncation cut.** LinkedIn shows roughly the first 140
  characters on mobile before "…see more". Line 1 alone should make the click worth it.
- **One idea per line. Blank line between almost every line.** These captions are
  90% whitespace by area. That is the format.
- **Specific numbers and specific product names.** "275+ clients", "$7M ARR",
  "1.8% to 4.3%", "300+ hours", "24 minutes". Categories are invisible; names are proof.
- **One CTA, at the end.** Pick one: comment keyword, repost, newsletter, or question.
- **No em dashes.** Use a period and a line break.
- Never use the denial-then-reveal contrast pattern ("not X, this is Y" / "ده مش X، ده Y").
  State the thing directly. See the ban list in `references/caption-patterns.md`.

## §4 — Build the artboard

Start from a template in `assets/`:

- `template-flow-map.html` — converging flow with a verdict panel (Charlie Hills family)
- `template-orbit-cycle.html` — nodes orbiting a centre artifact (FullEnrich family)
- `template-directory-map.html` — monospace tree with annotation pills (DRIP family)
- `template-specimen-grid.html` — 25 live micro-demos in one grid (catalogue family)

Each is a single self-contained HTML file, no external requests, fixed 1080x1350
artboard. Read `references/animation-recipes.md` before touching the CSS — it holds the
eight animation primitives and the rules that keep a loop seamless.

Hard constraints for the artboard:

1. Exactly one `#artboard` element, `width:1080px; height:1350px;` — the capture script
   screenshots that element, not the viewport.
2. All animations must be **CSS animations or WAAPI**, `infinite`, and share one
   `--loop` duration or an integer division of it. JS-driven `requestAnimationFrame`
   motion cannot be seeked and will break capture.
3. All fonts must be embedded or system-safe. A font that loads over the network will
   render as a fallback in some frames and not others. `references/design-systems.md`
   lists the safe stacks and the four house palettes.
4. Nothing may move in the outer 48px margin. That band holds the title and the
   attribution footer and must stay dead still.

Sanity-check the still frame before animating:

```bash
python3 scripts/check_render.py build/post.html --out build/still.png
```

## §5 — Render the GIF

One command:

```bash
bash scripts/render.sh build/post.html build/post.gif --duration 4.8 --fps 12.5
```

That wraps two steps you can also run separately:

```bash
python3 scripts/capture_frames.py build/post.html --out build/frames \
        --duration 4.8 --fps 12.5 --selector "#artboard"

python3 scripts/build_gif.py build/frames --out build/post.gif \
        --fps 12.5 --max-mb 5 --colors 128
```

`build_gif.py` runs a two-pass ffmpeg palette (`palettegen` + `paletteuse` with
Bayer dithering) and then automatically steps down colours, then fps, then scale until
the file lands under the size budget. It prints every attempt so you can see the
trade it made.

**Choosing duration and fps.** These two numbers decide file size more than anything else.

| Motion style | fps | Duration | Frames |
|---|---|---|---|
| Stepped highlight, discrete states | 10–12.5 | 3.5–5s | 35–60 |
| Smooth orbit or path draw | 25–30 | 6–8s | 150–240 |
| Single reveal, then hold | 12.5 | 3s | ~38 |

Start at the low end. A 12.5 fps stepped animation at 1080x1350 with 128 colours lands
around 2–4 MB, which is comfortable. Smooth 30 fps only survives if the moving region
is small and the background is flat.

## §6 — QA before you export

Run through `references/qa-gates.md`. The gates that catch the most failures:

- **Loop close.** Frame 0 and frame N-1 must be visually identical. `build_gif.py`
  reports the pixel delta between them; anything above 0.5% means an animation
  doesn't divide evenly into the loop duration.
- **Mobile legibility.** LinkedIn renders the image at roughly 350px wide in feed.
  Any text below 22px in the 1080px artboard is unreadable. `check_render.py --mobile`
  produces the 350px downscale so you can look at it honestly.
- **Motion budget.** Judge on `build_gif.py`'s `motion:` line, the mean share of pixels
  changing per frame. Under 2% is healthy. Bounding-box area is a misleading proxy: one
  reference file animates 85% of its canvas and still encodes cheaper than a file that
  animates 11%. See `references/animation-recipes.md`.
- **First-frame integrity.** LinkedIn shows a static poster frame before the GIF plays
  for some users. Frame 0 must be a complete, readable infographic on its own.
- **Autoplay reality.** LinkedIn plays GIFs uploaded as images, but converts large ones.
  Keep under 5 MB and under 8 seconds.

## §7 — Publish

`references/publishing-playbook.md` covers upload mechanics, the first-comment link
strategy, comment-gate wording, and posting windows. Two things people get wrong:

- Upload the GIF as an **image**, not a document or video. LinkedIn autoplays image GIFs.
- Put links in the first comment, not the caption, and say so in the caption.

---

## When to use something else

If the deliverable is a video rather than a post, use **HyperFrames**
(`heygen-com/hyperframes`). It shares this skill's architecture — HTML in, seeked frames
in headless Chrome, ffmpeg out — but outputs MP4 with audio, captions and a much larger
animation runtime surface. This skill stays the better choice when the deliverable is a
LinkedIn post, because the caption and archetype layers are most of the work and
HyperFrames does not cover them. The two compose; see
`references/production-pipeline.md`.

## Arabic and bilingual output

Read `references/arabic-rtl.md` before producing any Arabic version. It is not a
translation job. The layout mirrors, the numeral system changes, the typographic scale
changes (Arabic needs roughly 12% more leading and one size up for the same optical
weight), and English technical terms stay LTR inside RTL runs. The file covers the
font stack, the bidi isolation markers, and the caption rhythm differences — Arabic
LinkedIn captions carry longer lines than English ones and break at different points.

## Reference index

| File | Read it when |
|---|---|
| `references/caption-patterns.md` | Writing or editing any caption |
| `references/visual-archetypes.md` | Choosing or building a layout |
| `references/animation-recipes.md` | Writing any animation CSS |
| `references/design-systems.md` | Picking colours, fonts, spacing |
| `references/production-pipeline.md` | Renderer setup, troubleshooting, HyperFrames interop |
| `references/arabic-rtl.md` | Any Arabic or bilingual output |
| `references/qa-gates.md` | Before every export |
| `references/publishing-playbook.md` | Before posting |

## Scripts

| Script | Does |
|---|---|
| `scripts/capture_frames.py` | Seeks WAAPI animations and screenshots N deterministic frames |
| `scripts/build_gif.py` | Two-pass palette GIF assembly with automatic size budgeting |
| `scripts/check_render.py` | Still-frame render, mobile downscale, contrast and safe-zone audit |
| `scripts/render.sh` | Runs capture then build in one command |
| `scripts/setup.sh` | Installs Playwright, a Chrome binary, and checks ffmpeg |

## Credits

Built by **Mamdouh Aboammar** — Managing Partner at Momint, founder of
PrePilot.cloud and OpenOps Studio. Brand strategist and vibe coder working
across Egypt, KSA, UAE, Qatar and Canada.

- GitHub: [@imMamdouhaboammar](https://github.com/imMamdouhaboammar)
- PrePilot: [prepilot.cloud](https://prepilot.cloud)

The archetypes were derived by analysing publicly posted LinkedIn content.
They describe structure, not content. No third-party text or design is
redistributed here. Everything in `assets/` is original.

MIT licensed. See `LICENSE`.

## Working method

When the user brings a topic:

1. Ask only what you cannot infer — usually just: what is the one takeaway, and what is
   the CTA. Do not run a long intake.
2. Propose the caption archetype and visual archetype together, in one line each, and
   get a yes before building.
3. Write the caption first. The caption decides what the visual has to carry.
4. Build the artboard as a still. Show it. Get a yes.
5. Animate last, and animate less than feels right.
6. Render, QA, deliver the GIF plus the caption plus the first-comment text.

Animating a layout the user has not approved wastes the most time of anything in this
workflow. The still is the approval gate.
