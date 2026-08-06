# Anime.js reference

Verified against **v4.5.0**. Run `node scripts/bake.mjs list` to confirm the easing names
against whatever version is actually installed, since the API moves.

- [Install](#install)
- [Which track needs it](#which-track-needs-it)
- [The exports that matter here](#the-exports-that-matter-here)
- [Physics domain to Anime.js feature](#physics-domain-to-animejs-feature)
- [Timelines](#timelines)
- [Springs](#springs)
- [SVG helpers](#svg-helpers)
- [Baking to CSS](#baking-to-css)
- [Version traps](#version-traps)

## Install

```bash
npm install animejs          # project use, ESM only
```

Browser without a build step, pinned so a future release cannot silently change the motion:

```js
import { animate, createTimeline, spring, svg, utils } from 'https://esm.sh/animejs@4.5.0';
```

`https://cdn.jsdelivr.net/npm/animejs@4.5.0/+esm` works the same way. Both hosts are usually
reachable from sandboxed preview environments; pin the version either way.

## Which track needs it

Anime.js is the default engine for anything that runs in a page: docs sites, landing pages,
product UI, artifacts, interactive explainers, demos, anything responding to scroll, hover,
pointer, or state.

It cannot be the delivery mechanism for a README asset, because an SVG loaded through `<img>`
is an isolated document with no scripting. That does not remove Anime.js from that track, it
moves it earlier: `scripts/bake.mjs` samples the same easing and spring solvers in Node and
emits CSS keyframes. The static file and the interactive file then share one motion identity
rather than being two independent guesses.

Ask which context the asset is for before choosing. When the answer is both, design once and
emit twice.

## The exports that matter here

Everything below is a named export of `animejs`, with subpath modules available
(`animejs/svg`, `animejs/utils`, `animejs/timeline`, `animejs/easings`, and others).

| Export | Use |
|---|---|
| `animate(targets, params)` | the single-animation workhorse |
| `createTimeline(params)` | sequencing, which is where character animation lives |
| `spring({stiffness, damping, mass, velocity})` | physical settling, solver picks its own duration |
| `stagger(value, opts)` | offsets across many elements, also usable as a timeline position |
| `svg.createMotionPath(path)` | travel along a path with automatic rotation |
| `svg.createDrawable(sel)` | stroke drawing through the `draw: '0 1'` property |
| `svg.morphTo(target, precision)` | shape morphing with point extrapolation |
| `utils.$ / get / set / remove / lerp / clamp / mapRange / random / snap / damp` | reading and writing values mid-animation |
| `createScope({root, mediaQueries})` | selector isolation and one cleanup handle |
| `onScroll({sync, enter, leave})` | scroll-linked or scroll-triggered playback |
| `createDraggable(el, {releaseEase})` | pointer dragging with a spring release |
| `createAnimatable(el, params)` | per-property setters for cursor-following and continuous input |
| `createTimer({duration, onUpdate})` | a frame loop without a target |
| `splitText / scrambleText` | text effects, useful for captions inside a scene |
| `waapi.animate` | native WAAPI path when the animation can run off the main thread |
| `eases`, `cubicBezier`, `linear`, `steps`, `irregular` | the easing surface |
| `engine.defaults`, `engine.timeUnit`, `engine.speed` | global configuration |

Ease names dropped the `ease` prefix in v4: `inOutSine`, `outQuad`, `outElastic`,
`outBounce`, plus the parameterized `in(power)`, `out(power)`, `inOut(power)`. The default is
`out(2)`.

## Physics domain to Anime.js feature

| Domain | Anime.js | Note |
|---|---|---|
| Projectile arc | `svg.createMotionPath` on a quadratic path | the path carries the parabola, so `ease: 'linear'` is correct |
| Bounce chain | `spring()` per landing, or `outBounce` for one call | a spring per impact gives control over restitution feel |
| Pendulum | `ease: 'inOutSine'` with `alternate: true` | exact velocity profile, two keyframes |
| Damped spring | `spring({stiffness, damping, mass})` | solver reports its own settling duration |
| Free fall | `ease: 'inQuad'` | displacement proportional to t² |
| Stacking / queue | `stagger()` as both delay and timeline position | one call, many objects |
| Line drawing | `svg.createDrawable` with `draw: ['0 0','0 1','1 1']` | draw in then out |
| Shape change | `svg.morphTo` | needs comparable point counts, tune `precision` |
| Follow-through | second `.add()` at `'<'` with a small offset | shares the timeline clock |
| Continuous input | `createAnimatable` + `utils.damp` | for cursor and scroll following |

## Timelines

Timelines are where a motion story stops being a list of effects. Positions are the whole
feature:

```js
const tl = createTimeline({ loop: true, defaults: { duration: 600, ease: 'outQuad' } });
tl.add('#body', { scaleY: .8 }, 400)   // absolute ms
  .add('#body', { scaleY: 1.22 })      // right after the previous
  .add('#pos',  { x: 300 }, '<')       // start together with the previous
  .add('#dust', { opacity: 0 }, '<+=120')
  .add('.tok',  { y: 0 }, stagger(90));
```

`'<'` starts with the previous animation, `'<<'` with the one before that, `'+=n'` and
`'-=n'` offset from the end, and a bare number is absolute time. Reach for `tl.duration`
rather than adding the beats up by hand.

`tl.seek()`, `tl.speed`, `tl.reverse()`, and `tl.stretch()` make the timeline scrubbable,
which is how to tune timing: build the scene, then scrub it slowly and watch where the weight
goes wrong.

## Springs

```js
const s = spring({ stiffness: 140, damping: 9, mass: 1, velocity: 0 });
animate('#body', { scaleY: 1, ease: s });   // duration comes from the solver
```

`stiffness` raises frequency, `damping` kills overshoot, `mass` slows everything and adds
weight, `velocity` seeds an entry speed for a handoff from a previous move. The returned
object exposes `.duration` in milliseconds and `.ease(t)` normalized over that duration,
which is what makes headless baking possible.

Do not set an explicit `duration` alongside a spring. Overriding it discards the settling
time the solver computed, which is the reason to use a spring in the first place.

Starting ranges: light and comic `stiffness: 120–180, damping: 6–9`; heavy and grounded
`stiffness: 60–100, damping: 12–18, mass: 1.5–3`.

## SVG helpers

```js
animate('#pos', { ...svg.createMotionPath('#route'), duration: 850, ease: 'linear' });
```

`createMotionPath` returns `{translateX, translateY, rotate}`, so it spreads into the
parameter object and drives all three at once. `rotate` follows the tangent, which is exactly
right for a subject that should bank into its arc and wrong for one that should stay upright,
in which case drop that key.

```js
animate(svg.createDrawable('.line'), { draw: ['0 0', '0 1', '1 1'], delay: stagger(80) });
```

`draw` is a `'start end'` pair in path-length fractions. `'0 0' → '0 1'` draws in,
`'0 1' → '1 1'` wipes out, and the pair together gives a stroke that travels.

```js
animate($shape, { d: svg.morphTo('#target', 0.5) });
```

Morphing extrapolates points to match the two shapes. Lower `precision` means fewer generated
points and a coarser interpolation, `0` disables extrapolation entirely and requires the
shapes to already correspond.

## Baking to CSS

```bash
node scripts/bake.mjs list
node scripts/bake.mjs spring --name mascot-press --from 1 --to .88 \
     --stiffness 90 --damping 7 --template "scale({sx},{v})" --at 350 --loop 5000
node scripts/bake.mjs ease --name mascot-drop --ease inQuad --from -160 --to 0 \
     --dur 350 --loop 5000 --template "translateY({v}px)"
```

The spring command prints the solver's settling duration to stderr and the keyframes to
stdout, so it pipes cleanly into a generator. Import the module instead of shelling out when
building a whole scene:

```js
import { sampleSpring, keyframes, springKeyframes } from './scripts/bake.mjs';
```

`{v}` is the value, `{sx}` the companion squash width, `{u}` raw progress. Eight to fourteen
samples covers a spring; a long arc wants more.

## Version traps

- **`createSpring()` is deprecated in 4.5** in favour of `spring()`. The old name still works
  and prints a warning. Use `spring()`.
- **v3 syntax does not run.** `anime({targets, ...})`, `easing:`, `anime.timeline()`,
  `anime.path()`, and `anime.setDashoffset()` are all gone. If a snippet looks like that, it
  predates v4.
- **ESM only.** No global `anime` object from a plain `<script src>`. Use
  `<script type="module">` with an `esm.sh` or jsdelivr URL, or bundle it.
- **Check the installed version before writing code**, since exports keep arriving.
  `node -e "import('animejs').then(m => console.log(Object.keys(m).sort().join(' ')))"`
  lists what is actually there, and 4.5 added surface that older references do not mention.
