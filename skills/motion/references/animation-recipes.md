# Animation Recipes

Eight motion primitives. Between them they cover everything in the reference GIFs.
Every recipe is seekable — it uses CSS `@keyframes` or WAAPI only, so
`capture_frames.py` can set `currentTime` and get a deterministic frame.

## The rules that make a loop look professional

### 1. One loop clock

Define a single duration and derive everything from it.

```css
:root {
  --loop: 4800ms;        /* total loop */
  --steps: 4;            /* number of sequential states */
}
```

Every animation gets `animation-duration: var(--loop)` and expresses its own timing as
percentages inside that one cycle. Animations with different durations produce a
composite loop equal to their least common multiple, which will not close cleanly at
your capture length.

If a sub-animation genuinely needs to be faster, make it an **integer division**:
`calc(var(--loop) / 4)`. Never `1.3s` next to `4.8s`.

### 2. Frame 0 must equal frame N

The value at `0%` and at `100%` must be identical, and the state at `t = --loop` must
equal the state at `t = 0`. `capture_frames.py` samples `[0, loop)` exclusive of the
endpoint, so a keyframe set that ends where it started loops seamlessly.

`build_gif.py` reports the seam as a multiplier against the loop's own biggest frame-to-frame
step, printed as `x<n>`. At or below `x1.25` the seam is indistinguishable from any other
frame boundary. Above `x2.0` something does not close. Usual culprit: a `transform` that
ends at a different value, or an `animation-delay` that is not a clean fraction of the loop.

Judge the multiplier, not the raw seam percentage — the last captured frame sits one step
before the loop point, so a raw percentage flags clean fast loops and passes broken slow
ones. `helper/visual-contract.json` holds the authoritative thresholds.

Pass `--json <path>` to `build_gif.py` when running it directly. The JSON carries the
changed-pixel and seam measurements beside their contract thresholds; `render.sh` creates
that fragment automatically and merges it into `build/render-report.json`.

### 3. Motion budget: measure changed pixels, not area

The intuitive rule is "keep under 20% of the canvas moving". That rule is wrong, and a
fourth reference file proves it.

| Reference | Area that looks like it moves | **Changed pixels per frame** | Bytes per frame | Total |
|---|---|---|---|---|
| Flow Map (light ground) | ~11% | 0.08% | **157 KB** | 4.8 MB / 30 frames |
| Orbit Cycle (light ground) | ~14% | 0.03% | 10 KB | 2.4 MB / 230 frames |
| Specimen Grid (dark ground) | **~85%** | 1.09% | 20 KB | 2.5 MB / 120 frames |

The Specimen Grid runs 42 independent micro-animations at once. Visually the entire
canvas is alive. It still encodes at an eighth of the per-frame cost of the Flow Map,
whose animation is four boxes and four dots.

Two things actually drive file size:

**1. Changed pixels per frame, not bounding-box area.** `diff_mode=rectangle` encodes
only the changed region. Forty-two tiny flat-colour animations touch fewer pixels than
one accent wash sweeping across a 240x90 card. Area is a proxy that fails badly on
dense grids.

**2. Palette pressure from the background.** A dark, flat ground needs very few colours
and dithers to almost nothing. A light ground with a grid texture, soft shadows and
antialiased serif type needs a wide palette, and every changed pixel costs more. That is
the whole reason the Flow Map costs 157 KB a frame while doing less.

So the practical rules are:

- **Dark flat ground:** you can animate almost everything, as long as each animation is
  small and flat-coloured. The Specimen Grid archetype depends on this.
- **Light textured ground:** keep motion tight and localised. The 20% area heuristic is
  a reasonable proxy *here* and nowhere else.
- **Never** animate `filter: blur()`, large `box-shadow` spread, or `backdrop-filter` on
  either. Those rewrite every pixel underneath and defeat rectangle diffing regardless
  of how small the element looks.

`build_gif.py` reports the real number as `motion:` — the mean share of pixels changing
between consecutive frames. Judge against that, not against a bounding box.

| Mean changed pixels / frame | Reading |
|---|---|
| under 0.5% | very cheap, you have room to add motion |
| 0.5 – 2% | healthy for a dense or dark design |
| 2 – 5% | fine only if the ground is dark and flat |
| over 5% | something full-bleed is animating. Find it |

`check_render.py` still reports bounding-box area, which is useful for spotting an
accidental full-canvas fade. Treat it as a smell test, not a gate.

### 4. Static elements must be truly static

Do not put `opacity: 0.999` or a `will-change` on a static element. Any sub-pixel
difference between frames defeats GIF frame-diffing and multiplies file size.
Avoid animating `filter: blur()` and `box-shadow` spread on large areas for the same
reason — they touch every pixel underneath.

Cheap to animate: `transform`, `opacity` on small elements, `stroke-dashoffset`,
`offset-distance`, `border-color`, `background-color` on small elements.

Expensive: `filter`, large `box-shadow`, `backdrop-filter`, anything full-bleed.

---

## Primitive 1 — Sequential Highlight

The reading pointer. An accent outline walks through N sibling elements.
This is the primary animation in the Charlie Hills reference.

```css
:root { --loop: 4800ms; --steps: 4; }

.step {
  border: 2px solid var(--line);
  background: transparent;
  animation: stepOn var(--loop) steps(1, end) infinite;
}
/* Stagger by an exact fraction of the loop. NOTE THE REVERSE ORDER. */
.step:nth-child(1) { animation-delay: calc(var(--loop) * 0 / 4); }
.step:nth-child(2) { animation-delay: calc(var(--loop) * -3 / 4); }
.step:nth-child(3) { animation-delay: calc(var(--loop) * -2 / 4); }
.step:nth-child(4) { animation-delay: calc(var(--loop) * -1 / 4); }

@keyframes stepOn {
   0%   { border-color: var(--accent); background: var(--accent-wash); }
  25%   { border-color: var(--line);   background: transparent; }
 100%   { border-color: var(--line);   background: transparent; }
}
```

### The reverse-delay trap

A negative delay pushes an animation **forward** in its cycle, not backward. So the
element that should light up *last* needs the *smallest* negative offset.

Write it out before you trust it. You want element `i` (1-indexed, N total) to be
active at `t = (i-1) x loop / N`. The animation is active when its progress is near 0.
So the delay you need is:

```
delay(1) = 0
delay(i) = -loop x (N - i + 1) / N     for i > 1
```

For N = 4 that gives `0, -3/4, -2/4, -1/4`. Writing the intuitive
`0, -1/4, -2/4, -3/4` produces the sequence **1 → 4 → 3 → 2**, which looks almost
right in a thumbnail and is obviously wrong once anyone watches it. Verify by
capturing 4 frames at `t = 0, loop/4, loop/2, 3xloop/4` and checking the order.

Negative delays also mean frame 0 already shows the correct state, with no blank
first frame.

`steps(1, end)` gives the hard on/off snap seen in the reference. For a soft version,
use the default easing and widen the transition band to 5% either side.

**Dwell time.** 900–1200ms per step reads as deliberate. Below 600ms it reads as a
flicker and the viewer cannot follow it. That caps you at about 5 steps in a 5s loop.

---

## Primitive 2 — Path Particles

Dots travelling along a connector. The second animation in the Charlie Hills reference,
and what makes a static diagram feel like a system with flow in it.

### SVG method (preferred, works on any path shape)

```html
<svg class="wires" viewBox="0 0 1080 1350">
  <path id="w1" d="M240,470 C240,600 420,620 540,700" fill="none"
        stroke="#F0C9A8" stroke-width="2"/>
  <circle r="5" fill="#D97757">
    <animateMotion dur="4.8s" repeatCount="indefinite" begin="0s">
      <mpath href="#w1"/>
    </animateMotion>
  </circle>
</svg>
```

`<animateMotion>` is SMIL. Chrome exposes SMIL animations through
`document.getAnimations()` in recent versions, but to be safe `capture_frames.py` also
calls `svg.setCurrentTime(t)` on every root SVG, which seeks SMIL deterministically.

### CSS method (offset-path — use for HTML elements, not SVG children)

```css
.particle {
  offset-path: path("M240,470 C240,600 420,620 540,700");
  offset-rotate: 0deg;
  animation: travel var(--loop) linear infinite;
}
@keyframes travel {
  0%   { offset-distance: 0%;   opacity: 0; }
  12%  { opacity: 1; }
  88%  { opacity: 1; }
  100% { offset-distance: 100%; opacity: 0; }
}
```

Fading in and out at the ends hides the teleport back to the start, which is what makes
the loop invisible.

**Staggering multiple wires:** give each particle a negative delay of
`calc(var(--loop) * -N / count)`. Do not use random delays — they will not close.

**Density.** One particle per wire. Two reads as a data stream, which is a different
and busier feeling. Three is noise.

---

## Primitive 3 — Path Draw-On

A connector strokes itself from nothing to full, or a dashed grey line becomes solid
accent. The circle in the FullEnrich reference does this.

```css
.wire {
  stroke-dasharray: var(--len);      /* set --len to the path length */
  stroke-dashoffset: var(--len);
  animation: draw var(--loop) ease-in-out infinite;
}
@keyframes draw {
  0%   { stroke-dashoffset: var(--len); }
  55%  { stroke-dashoffset: 0; }
  90%  { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: var(--len); }
}
```

Get the length in the browser with `path.getTotalLength()` and write it into the CSS
variable, or read it once and hardcode it. A wrong `--len` produces a line that
either never completes or completes early and sits still.

To hold the drawn state and reset invisibly, add a fade at the tail:

```css
90%  { stroke-dashoffset: 0; opacity: 1; }
99%  { stroke-dashoffset: 0; opacity: 0; }
100% { stroke-dashoffset: var(--len); opacity: 0; }
```

---

## Primitive 4 — Orbit

Node markers travelling a circular path. The FullEnrich signature.

```css
.orbiter {
  offset-path: circle(380px at 540px 700px);
  animation: orbit var(--loop) linear infinite;
}
@keyframes orbit {
  from { offset-distance: 0%; }
  to   { offset-distance: 100%; }
}
.orbiter:nth-child(2) { animation-delay: calc(var(--loop) * -1 / 5); }
.orbiter:nth-child(3) { animation-delay: calc(var(--loop) * -2 / 5); }
.orbiter:nth-child(4) { animation-delay: calc(var(--loop) * -3 / 5); }
.orbiter:nth-child(5) { animation-delay: calc(var(--loop) * -4 / 5); }
```

A full 360° rotation over the loop closes perfectly by definition, which is why orbit
animations tolerate high frame rates. Use `linear` — any easing makes the loop point
visible as a hesitation.

If markers should stay upright while orbiting, add `offset-rotate: 0deg`.

---

## Primitive 5 — Staggered Reveal

Cards rising and fading in, in reading order. Use for grids.

```css
.card {
  animation: reveal var(--loop) ease-out infinite;
}
.card:nth-child(n) { animation-delay: calc(var(--loop) * -0.02 * var(--i)); }
/* set --i per card inline: style="--i:3" */

@keyframes reveal {
  0%   { opacity: 0; transform: translateY(14px); }
  14%  { opacity: 1; transform: translateY(0); }
  86%  { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(14px); }
}
```

**Warning.** This is the primitive that most often blows the motion budget. Twelve cards
fading over the whole canvas means the whole canvas is in motion. Use it for a maximum
of 6 elements, or restrict it to a single column.

A safer variant: reveal only the **pills or badges**, and leave the card bodies static.
Same perceived life, a fraction of the moving area.

---

## Primitive 6 — Counter / Bar Growth

Bars growing from zero, for the Spec Sheet archetype.

```css
.bar-fill {
  transform-origin: left center;
  animation: grow var(--loop) cubic-bezier(.2,.8,.2,1) infinite;
}
@keyframes grow {
  0%   { transform: scaleX(0); }
  35%  { transform: scaleX(1); }
  92%  { transform: scaleX(1); }
  100% { transform: scaleX(0); }
}
```

Scale the fill, never animate `width` — width triggers layout on every frame and
produces sub-pixel text reflow in neighbouring elements.

Numeric counters cannot be animated in pure CSS in a seekable way. Either leave the
number static at its final value (recommended) or drive it with a WAAPI animation on a
custom property registered via `@property`.

---

## Primitive 7 — Typewriter

For the Terminal Card archetype.

```css
.type {
  width: 0;
  overflow: hidden;
  white-space: nowrap;
  border-right: 3px solid var(--accent);
  animation: type var(--loop) steps(28, end) infinite,
             caret calc(var(--loop) / 8) steps(1, end) infinite;
}
@keyframes type {
  0%   { width: 0; }
  45%  { width: 28ch; }
  92%  { width: 28ch; }
  100% { width: 0; }
}
@keyframes caret {
  0%, 49%  { border-color: var(--accent); }
  50%,100% { border-color: transparent; }
}
```

`steps(N)` where N is the character count gives the mechanical feel. Requires a
monospace font and `ch` units to line up.

The caret uses an integer division of the loop so it closes with the main cycle.

---

## Primitive 8 — Glow Pulse

For the Node Tree archetype. The most expensive primitive — restrict it to small,
isolated elements.

```css
.node.tier-1 {
  animation: pulse var(--loop) ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 rgba(217,119,87,0); }
  18%      { box-shadow: 0 0 44px rgba(217,119,87,.35); }
  40%      { box-shadow: 0 0 0 rgba(217,119,87,0); }
}
.node.tier-2 { animation-delay: calc(var(--loop) * -0.12); }
.node.tier-3 { animation-delay: calc(var(--loop) * -0.24); }
```

A large blurred shadow rewrites every pixel it covers, so the GIF encoder cannot reuse
frame regions. Keep the shadow radius under 50px and the element under 300px wide, or
the file size triples.

---

---

## Primitive 9 — Ambient Micro-Loops

Many small independent animations running at once, each in its own cell. The engine
behind the Specimen Grid.

The trap is that N independent durations produce a composite loop equal to their least
common multiple, which will not close at your capture length. Every micro-loop must be
an **integer division** of the master loop.

```css
:root { --loop: 6000ms; }

/* Each cell declares how many times its own animation repeats per master loop.
   Set --n inline: style="--n:3"  */
.cell > * {
  animation-duration: calc(var(--loop) / var(--n, 1));
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}
```

With `--loop: 6000ms`, legal values of `--n` are 1, 2, 3, 4, 5, 6, 8, 10, 12. A
count-up that wants to feel slow uses `--n:1`. A glitch that wants to feel frantic uses
`--n:12`. Nothing in between, ever. `--n:7` gives 857.14ms, which does not close.

Desynchronise with negative delays derived from the cell index, so the grid does not
pulse in unison:

```css
.cell:nth-child(n) > * {
  animation-delay: calc(var(--loop) * -0.037 * var(--i));
}
```

`0.037` is arbitrary and that is the point. Any fixed fraction works because the
animation is infinite and the delay only shifts the phase. Do not use `random()` or a
JS-generated value; you need the same phase on every render.

### Two traps that cost me a render each

**The `animation:` shorthand resets `animation-delay` to `0s`.** If a parent rule sets
the phase offset as a longhand and the specimen rule uses the shorthand, whichever wins
the cascade takes everything. `.demo > svg > *` and `.sp-line path` both compute to
specificity (0,1,1) — `*` contributes nothing — so source order decided it and the
shorthand silently cancelled every phase offset. Use longhands in the specimen rules:

```css
/* wrong: kills the inherited delay and duration */
.sp-line path { animation: draw var(--loop) ease-in-out infinite; }

/* right: leaves duration and delay to the parent rule */
.sp-line path { animation-name: draw; animation-timing-function: ease-in-out; }
```

**Phase offsets do not reach inside an SVG.** If the cell's wrapper is an `<svg>` and
the animation lives on a child `<path>` or `<circle>`, a rule targeting `.demo > *` never
touches it. Add a second rule one level deeper:

```css
.demo > svg > * {
  animation-duration: calc(var(--loop) / var(--n, 1));
  animation-delay: calc(var(--loop) * -0.037 * var(--i, 0) - var(--loop) * 0.3);
  animation-iteration-count: infinite;
}
```

Without it, every SVG specimen starts at offset 0 and renders **blank in frame 0**,
which fails the first-frame gate in `qa-gates.md`.

**And set `stroke-dasharray` to the measured length.** A guessed value larger than the
real path means the stroke never appears during the first part of the animation.

```js
document.querySelectorAll('path, circle').forEach(el =>
  console.log(el.getTotalLength().toFixed(0)));
```

### Keeping it cheap

- Flat fills only. No gradients that span a whole cell, no blur, no shadow
- Small elements. A bar 6px tall costs almost nothing to redraw
- Dark flat ground. This primitive is only affordable on one
- Reuse. Author 10–14 distinct miniatures and recolour them per category

### Layering the category sweep on top

The second layer walks a coloured border through the cells of one category at a time:

```css
.cell {
  border: 1px solid var(--line);
  animation: sweep var(--loop) steps(1, end) infinite;
}
/* --cat is the category index, --cats the number of categories.
   Delays run in REVERSE, as always. */
.cell { animation-delay: calc(var(--loop) * -1 * (var(--cats) - var(--cat)) / var(--cats)); }

@keyframes sweep {
  0%   { border-color: var(--cat-color); }
  14%  { border-color: var(--line); }
  100% { border-color: var(--line); }
}
```

Every cell in a category shares one `--cat`, so the whole category lights together. That
reads as a guided tour of the legend rather than a random twinkle.

## Primitive 10 — Mascot Pointer

A character travels a drawn route and the layout reacts to where it lands. This replaces
Primitive 2's abstract dot rather than sitting alongside it: a canvas gets one reading
pointer, and if a mascot is present, the mascot is it.

The motion is generated, not authored. `scripts/bake_mascot.py` wraps
`svg-mascot-animator/scripts/physics.py` and emits the `keyTimes` / `keyPoints` pair, the
landing squash, the contact shadow, the seam fade, and the reversed negative delays the
stage cards need, all expressed against one `--loop`.

```bash
python3 scripts/bake_mascot.py hop --loop 6000 --id mf --stops 5 --apex 40 --dwell .11
```

```xml
<g class="mf-seam">
  <g>
    <animateMotion dur="6s" begin="-3s" repeatCount="indefinite"
                   calcMode="linear" rotate="0"
                   keyTimes="0;0.11;0.2225;…" keyPoints="0;0;0.25;…">
      <mpath href="#mf-rail"/>
    </animateMotion>
    <ellipse class="mf-shadow" rx="15" ry="5" fill="#3A342F" opacity=".22"/>
    <g class="mf-squash"><use href="#mf-body"/></g>
  </g>
</g>
```

`keyPoints` holds a constant value across a dwell window and moves across a travel window,
which is what turns continuous path motion into discrete hops with attention at each stop.

Three things break this primitive and nothing else does:

- **Anime.js.** `requestAnimationFrame` is not seekable, so `capture_frames.py` cannot
  reach it. Use the baked static track only.
- **A mascot clock that is not the artboard clock.** Everything inherits `var(--loop)` or
  an integer division of it.
- **The seam on frame 0.** Shift every mascot track by `calc(var(--loop) * -0.5)` and the
  `<animateMotion>` by `begin="-3s"`, so the fade that hides the teleport happens
  mid-loop instead of on the poster frame.

Full doctrine, including the three mascot roles and the archetype compatibility table:
`references/mascots.md`. Reference build: `assets/template-mascot-flow.html`.

Measured cost of the reference build: **0.21% changed pixels per frame**, seam 0.00%,
0.26 MB at 1080x1350, 6 s, 12.5 fps, on House 0's light ground.

---

## Composition patterns

The reference GIFs each use exactly **two** primitives. That is the right number. A mascot
does not add a third: Primitive 10 *replaces* Primitive 2, and the highlight it drives is
still Primitive 1.

| Archetype | Primitive A | Primitive B |
|---|---|---|
| Flow Map + Verdict | Sequential Highlight (setup row) | Path Particles (converging wires) |
| Orbit Cycle | Orbit (node markers) | Path Draw-On (the ring) |
| Directory Map | Sequential Highlight (tree rows) | Staggered Reveal (pills only) |
| Pipeline Stages | Sequential Highlight (stage cards) | Staggered Reveal (checklist ticks) |
| Node Tree | Glow Pulse (tiers) | Path Particles (dashed connectors) |
| Terminal Card | Typewriter | Glow Pulse (CTA border) |
| Spec Sheet | Bar Growth | Path Particles (timeline dot) |
| Character Flowchart | Path Particles (one token on the full route) | Sequential Highlight (cards it passes) |
| Mascot Flow | Mascot Pointer (the hop) | Sequential Highlight (stages it lands on) |
| Trading Card Grid | Sequential Highlight | — |
| Logo Grid | Staggered Reveal (one column at a time) | — |
| Annotated Blueprint | Path Draw-On (the spine) | Staggered Reveal (branches) |
| Cheat Sheet Poster | Sequential Highlight (panel numbers) | — |

## Timing table

| Loop | fps | Frames | Fits |
|---|---|---|---|
| 3600ms | 8.33 | 30 | 4 discrete states, 900ms dwell |
| 4800ms | 12.5 | 60 | 4 states + particles |
| 6000ms | 12.5 | 75 | 5 states, or a slow draw-on |
| 6000ms | 20 | 120 | ambient micro-loops + category sweep |
| 7680ms | 30 | 230 | orbit + draw-on, smooth |

Pick from this table rather than inventing numbers. Each row divides cleanly and has
been verified to close.

## Debugging a broken loop

| Symptom | Cause | Fix |
|---|---|---|
| Visible jump at the loop point | keyframe `100%` ≠ `0%` | make the endpoints identical |
| One element out of sync | a duration that is not the loop or an integer division of it | derive from `var(--loop)` |
| Jitter on static text | a parent has a `transform` or `will-change` | remove it; animate the child instead |
| GIF is 12 MB | motion budget blown, or `filter`/`box-shadow` on a large area | cut the moving area |
| First frame is blank | animation starts at `opacity: 0` with a positive delay | use a negative delay |
| Particles drift out of the wire | `offset-path` and the SVG path use different coordinate spaces | put the particle inside the same SVG and use `<mpath>` |
| One cell in a grid stutters | its `--n` is not an integer division of the loop | use 1,2,3,4,5,6,8,10,12 only |
| A cell ignores its phase offset | a specimen rule used the `animation:` shorthand | switch to `animation-name` + `animation-timing-function` |
| An SVG specimen is blank in frame 0 | the phase rule targets the `<svg>`, not the animated child | add a `.demo > svg > *` rule |
| The mascot is missing from frame 0 | the seam fade landed on the poster frame | shift every mascot track by `-0.5 * loop`, `begin="-3s"` on the SMIL |
| The mascot tilts as it travels | `animateMotion` banks to the path tangent by default | add `rotate="0"` |
| The mascot renders static across all frames | Anime.js or any rAF driver | bake it to CSS or SMIL |
| A squash happens near the top of the canvas | `transform-box` left at `view-box` | set `transform-box:fill-box` on the scaling group |
| The highlight lights the wrong stage | delays hand-edited away from the baked arrivals | re-run `bake_mascot.py hop` and paste both outputs together |
| A stroke never fully draws | `stroke-dasharray` is longer than the real path | measure with `getTotalLength()` |
| The whole grid pulses in unison | no phase offset per cell | add the `--i` negative delay |
