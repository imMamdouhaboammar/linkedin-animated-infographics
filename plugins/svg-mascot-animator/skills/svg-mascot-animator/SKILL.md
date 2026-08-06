---
name: svg-mascot-animator
description: >-
  Turn any static SVG mascot, logo, icon, or character into physics-driven animation, using Anime.js v4 as the default engine for interactive contexts and baked CSS keyframes for README and docs assets. Use this skill EVERY TIME the user wants to animate an SVG, add motion to a mascot or logo, build animated README or docs assets, create an animated badge or banner, mentions Anime.js or animejs, asks for "SVG animation", "حرك الـ mascot دي", "اعملي أنيميشن للـ SVG", "animate this logo", "motion for my icon", "README animation", or shares an SVG file and asks for movement, life, or a collection of poses. Also use when the user asks for believable motion physics on the web such as bounce, jump, swing, fall, squash and stretch, spring, motion path, line drawing, morph, stagger, walk cycle, floating, or inertia. Even for a single small request like "خليها تنط" or "make it bounce", use this skill.
license: MIT
---

# SVG Mascot Animator

Static SVG in, animation out, with the timing coming from equations and solvers rather than
from nudged keyframes. Anime.js v4 is the default engine. Where JavaScript cannot run, the
same Anime.js solvers are sampled ahead of time and baked into CSS keyframes, so both
versions of an asset share one motion identity.

What separates convincing motion from generic motion is not more keyframes. It is that the
timing comes from somewhere real: a parabola carried by a motion path, a pendulum whose
period follows from its length, a spring whose settling duration is computed by a solver
rather than picked by feel.

## Setup

Install the engine first, before writing any animation code:

```bash
bash scripts/setup.sh          # npm install animejs, verifies the version and exports
```

In a browser without a build step, import pinned so a future release cannot change the
motion under the user:

```js
import { animate, createTimeline, spring, svg, utils } from 'https://esm.sh/animejs@4.5.0';
```

The API moved substantially at v4 and keeps growing, so confirm the installed surface rather
than trusting a remembered snippet. `setup.sh` prints it, and `node scripts/bake.mjs list`
prints the easing names.

## Pick the track first

**Runtime track — Anime.js drives the page.** Docs sites, landing pages, product UI,
artifacts, demos, anything reacting to scroll, hover, pointer, or state. Timelines, springs,
motion paths, drawables, morphs, stagger, draggables. Start from
`assets/runtime-scene.html`.

**Static track — baked CSS inside a self-contained SVG.** README images, badges, anything
loaded through `<img>`, where scripting never executes. Anime.js still designs the motion;
`scripts/bake.mjs` samples its easings and spring solver in Node and emits the keyframes.

Ask which one the asset is for. When the answer is both, design the timeline once on the
runtime track, then bake it, since going the other direction loses the interactivity that
made the runtime version worth building.

## Workflow

### 1. Read the source and find the rig

```bash
python3 scripts/inspect_svg.py <path-to-svg>
```

Reports the viewBox, the bounding box, how many separately addressable shapes exist, and the
pivot translations to use when normalizing.

**A single path cannot articulate.** If the mascot is one path, limbs and eyes cannot move
independently and every idea has to live at body level: squash, stretch, arcs, rotation, and
secondary elements drawn outside the path. Say this early rather than promising a walk cycle
you cannot deliver, and offer the split as an option, since separating the parts unlocks gait
and reactions.

### 2. Pick stories, one physical domain each

A collection reads as a collection when the pieces do not repeat the same trick.

| Domain | Feels like | Story hooks | Anime.js |
|---|---|---|---|
| Projectile + restitution | committed, weighty | shipping, deploying, jumping a gap | `svg.createMotionPath` then `spring()` on landing |
| Pendulum | rhythmic, hypnotic | swinging between branches, hanging | `ease:'inOutSine'`, `alternate:true` |
| Damped spring | comic, reactive | load, pressure, overflow | `spring({stiffness, damping, mass})` |
| Free fall + stacking | escalating | queue building, backlog, tokens piling | `ease:'inQuad'` + `stagger()` |
| Hop cycle + treadmill | patient, looping | long build, endless progress | looping timeline, ground offset matched to stride |
| Orbit + drift | calm, ambient | idle, thinking, waiting | `createTimer` or a sine-eased loop |
| Inertia drag | mechanical | being pushed, dragging weight | `createDraggable` with `releaseEase: spring()` |
| Reveal / construction | deliberate | building, compiling, assembling | `svg.createDrawable` with `draw:['0 0','0 1']` |
| Transformation | surprising | switching modes, evolving | `svg.morphTo` |

Propose three with one-line stories and let the user pick or redirect. Serious brands may
want the calm end of that table rather than the comic end.

Read `references/animejs.md` for the API and `references/physics.md` for the equations,
easing map, and timing values before writing anything.

### 3. Rig the transform stack

Normalize the artwork once in `<defs>` so the origin sits at the natural pivot, then nest one
transform per concern, outermost first: horizontal position, vertical position, rotation,
scale. Mixing two concerns in one group forces hand-tuning, because CSS `transform` and
Anime.js both replace the whole value rather than composing it.

The rig is identical on both tracks. That is deliberate: it is what lets one motion design
ship twice.

`references/rigging.md` covers `transform-box`, the origin traps that silently break scaling,
splitting a path for articulation, and reduced-motion poses.

### 4. Build the timeline

On the runtime track, `createTimeline` with explicit positions. The positions carry the
performance: `'<'` to start with the previous beat, `'<+=120'` for a lag, `stagger()` as a
position for a cascade. Let springs set their own durations.

On the static track, generate the SVG from a script that imports `scripts/bake.mjs` for
spring and easing samples, or `scripts/physics.py` when the scene is pure ballistics and
Node is unavailable. Print the computed constants and check them before writing the file.
Reporting "apex 95 units over 0.85s implies g = 1052 units/s²" is how you catch a floaty arc
before rendering it.

Two rules carry most of the quality:

- **Sample curves, interpolate linearly.** A parabola becomes eight or nine samples with
  `linear` between them. An `ease-in-out` between two points always reads as floating. On the
  runtime track a motion path does this for you, which is why `createMotionPath` plus
  `ease:'linear'` beats easing a straight translate.
- **Use easing only where the real motion is genuinely eased.** A pendulum is the clean case:
  `inOutSine` is sinusoidal velocity, which is exactly correct, so two keyframes suffice.

### 5. Layer the secondary motion

The primary motion is the least interesting half of the work:

- **Contact shadow driven by the subject's own height**, read from the same samples or, at
  runtime, from the live transform in `onUpdate`. A shadow on its own curve drifts out of
  phase and quietly destroys the sense of depth.
- **Squash and stretch tied to velocity**: stretch at launch and before impact, neutral at
  the apex where vertical velocity is zero, squash on contact.
- **Short contact frames.** A landing squash beyond roughly 0.08s reads as soft.
- **Follow-through and lag**: trailing parts on the same period, offset 6 to 10 percent, at
  roughly 20 percent of the amplitude.
- **Anticipation** before any committed move, slow in and fast out.
- **Overshoot on arrival**, which is what `spring()` gives for free.

### 6. Apply the asset contract

Both tracks satisfy all of this. `references/contract.md` explains why each item matters:

- `role="img"` with `<title>` and `<desc>` wired through `aria-labelledby`
- every `id` and every keyframe name prefixed with the filename stem, so several assets can
  be inlined on one page without collisions
- a reduced-motion path: `@media (prefers-reduced-motion:reduce)` on the static track, a
  `matchMedia` guard that seeks the timeline to its payoff on the runtime track
- a dark variant for neutral colours, with brand colours left alone
- static track only: zero JavaScript, zero external references, zero web fonts

### 7. Verify before delivering

```bash
python3 scripts/check_asset.py <output.svg>              # static track
python3 scripts/check_asset.py --runtime <scene.html>    # runtime track
```

Fix everything it reports, then deliver and explain the physics behind each piece: the
constants, why that easing, what the secondary motion is doing. The explanation is part of
the deliverable, since it is what lets the user judge and adjust the result.

## Output conventions

Name files `<subject>-<verb>`, lowercase and hyphenated: `claudecode-ship-it.svg`. Loops run
3 to 6 seconds; shorter becomes irritating on a page someone is reading, longer means most
viewers never see the payoff. When a scene cannot loop positionally, fade the actor across
the last few percent and reset its position while it is invisible.

Keep each scene in a viewBox sized to its content, typically 320 to 480 units wide.

## Reference files

- `references/animejs.md` — v4 API surface, install, physics-to-feature mapping, springs,
  SVG helpers, baking, and the version traps. Read this before writing engine code.
- `references/physics.md` — equations, easing map, timing tables, secondary motion.
- `references/rigging.md` — transform stack, `transform-box`, origin traps, articulation.
- `references/contract.md` — accessibility, namespacing, `<img>` limits, QA checklist.
- `scripts/setup.sh` — installs Anime.js and prints the installed export surface.
- `scripts/bake.mjs` — samples Anime.js easings and springs into CSS keyframes.
- `scripts/physics.py` — closed-form generators for ballistics and oscillation without Node.
- `scripts/inspect_svg.py` — geometry and riggability report for a source file.
- `scripts/check_asset.py` — contract validator for both tracks.
- `assets/runtime-scene.html` — working starting point for the runtime track.
