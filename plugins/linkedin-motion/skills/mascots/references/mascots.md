# Mascots

How to put a character on a 1080x1350 artboard without losing the thing that makes
these posts work.

- [Why this needs rules](#why-this-needs-rules)
- [The three roles](#the-three-roles)
- [Seek-safety: what changes versus svg-mascot-animator](#seek-safety-what-changes-versus-svg-mascot-animator)
- [The rig](#the-rig)
- [Baking the motion](#baking-the-motion)
- [The seam](#the-seam)
- [Motion budget with a mascot](#motion-budget-with-a-mascot)
- [Drawing the mascot](#drawing-the-mascot)
- [Archetype compatibility](#archetype-compatibility)
- [Failure modes](#failure-modes)

---

## Why this needs rules

The skill's whole thesis is in `SKILL.md`: these are static infographics with a small
fraction of the canvas moving, and that motion is a **reading pointer** telling the eye
what order to read in. A mascot is the loudest moving object anyone can put on a page.
Dropped in casually it stops being decoration and starts competing with the pointer, and
the reader loses the thread the layout was built to carry.

So the mascot does not get added *next to* the reading pointer. Where a mascot exists,
**the mascot becomes the reading pointer**, and the abstract dot from Primitive 2 is
deleted. One pointer, always. Everything else on the canvas either idles within a few
pixels or stays frozen.

Handled that way a character earns its place, because a token travelling a route is a
stronger pointer than a dot: the reader tracks a body with a face and a direction, and
the dwell at each stop reads as attention rather than as a timing gap.

## The three roles

Every mascot on the artboard is exactly one of these. If you cannot say which, it does
not belong on the artboard.

| Role | Count | Amplitude | Job |
|---|---|---|---|
| **Pointer** | exactly 1 | travels the full route | is the reading pointer. Cards light as it lands |
| **Payoff** | 0 or 1 | one spring, ~20px | reacts at the last stop. The visual full stop |
| **Idle** | 0 to about 6 | 3px, hard cap 4px | ambient life in a panel, node, or footer group |

The counts are not stylistic. Two pointers means two reading orders and the post has no
reading order at all. Two payoffs means the eye does not know where the sentence ended.

Idles are cheap and safe because their amplitude is capped below the threshold where
peripheral vision registers them as motion worth turning toward. `bake_mascot.py` refuses
an `--amp` above 4 for that reason.

## Seek-safety: what changes versus svg-mascot-animator

The sibling skill `svg-mascot-animator` designs the motion. This skill renders it into a
GIF through seeked headless Chrome. Three of its defaults do not survive that trip.

| svg-mascot-animator default | Here | Why |
|---|---|---|
| Anime.js runtime track | **forbidden** | `requestAnimationFrame` cannot be seeked. `capture_frames.py` pauses `document.getAnimations()` and sets `currentTime`; a rAF loop is not in that set and renders frame 0 seventy-five times, or garbage |
| The mascot owns its own duration | **inherits `var(--loop)`** | Two clocks produce a composite cycle equal to their least common multiple, which will not close at the capture length. Same constraint as Primitive 9 |
| `360 x 240` own canvas | **artboard coordinates** | The mascot lives inside the artboard's SVG so `<mpath>` and the route share one coordinate space |
| `prefers-reduced-motion` fallback | **keep it anyway** | Headless Chrome does not set the preference, so it never fires during capture. Keep it for the artboard opened directly in a browser, and because the reduced-motion pose is a useful check on whether frame 0 reads on its own |

What carries over unchanged: the physics, the rig, the namespacing discipline, and the
asset contract's `role="img"` / `<title>` / `<desc>` block. Use the **static track** of
that skill, never the runtime track.

`bake_mascot.py` imports `svg-mascot-animator/scripts/physics.py` directly rather than
reimplementing the equations, so a fix there reaches both skills. If that skill is not
installed, the script says so and stops.

## The rig

Identical to `svg-mascot-animator/references/rigging.md`, with one addition: the
travelling group is owned by `<animateMotion>` and must carry no transform of its own.

```xml
<defs>
  <!-- normalized so the feet sit at (0,0) -->
  <g id="mf-body" transform="translate(-23,-52)">…artwork…</g>
  <path id="mf-rail" d="M 118 490 C 152 470, 152 610, 118 650 …"/>
</defs>

<use href="#mf-rail" class="rail"/>          <!-- the route, drawn, static -->

<g class="mf-seam">                          <!-- opacity: hides the loop teleport -->
  <g>                                        <!-- animateMotion owns this transform -->
    <animateMotion dur="6s" begin="-3s" repeatCount="indefinite"
                   calcMode="linear" rotate="0"
                   keyTimes="…" keyPoints="…"><mpath href="#mf-rail"/></animateMotion>
    <ellipse class="mf-shadow" cx="0" cy="3" rx="15" ry="5" fill="#3A342F" opacity=".22"/>
    <g class="mf-squash"><use href="#mf-body"/></g>
  </g>
</g>
```

Four things in that snippet are load-bearing:

- **`rotate="0"`.** Without it `animateMotion` banks the mascot to the path tangent, which
  on a hop rail means it arrives at each stop tilted.
- **`<mpath>` rather than a CSS `offset-path`.** Same coordinate space as the drawn route,
  so the mascot cannot drift off the line it is supposed to be following. This is the fix
  in the debugging table in `animation-recipes.md`.
- **The shadow rides inside the travelling group.** Physically a contact shadow stays on
  the ground while the body arcs. At a 30px bow that difference is invisible and the
  attached version costs one animated element instead of two. On a full-width ballistic
  arc, split it out and drive it with `physics.shadow_track()` from the body's own samples.
- **`transform-box: fill-box`** on `.mf-squash`. The default resolves `transform-origin`
  against the whole viewport, so a squash meant to happen at the feet happens somewhere
  near the top of the canvas.

## Baking the motion

```bash
python3 scripts/bake_mascot.py budget --mascot 64 --travel 1 --idles 4
python3 scripts/bake_mascot.py hop    --loop 6000 --id mf  --stops 5 --apex 40 --dwell .11
python3 scripts/bake_mascot.py idle   --loop 6000 --id amb --n 2 --amp 3 --blink
python3 scripts/bake_mascot.py payoff --loop 6000 --id win --at .89 --rise 18 --zeta .30
```

Run `budget` first. It costs nothing and it is the difference between finding out the
mascot is too big now or after a five-minute render.

`hop` prints four things you need and one you should read:

1. the `keyTimes` / `keyPoints` pair for `<animateMotion>`
2. squash keyframes, one landing per stop, from `physics.squash()`
3. shadow keyframes phased to the same landings
4. **the arrival instants**, already converted to the reversed negative delays the stage
   cards need, so the highlight and the mascot cannot drift apart
5. the implied gravity, e.g. `apex 40u over 0.674s implies g = 705 u/s^2 (ok)`

That last line is the one to actually read. Below about 500 the mascot floats; above 2000
it snaps. Fixing it is a matter of changing `--apex` or `--dwell`, not of nudging
keyframes, which is the entire point of generating the numbers.

Never hand-edit the baked output. Change the arguments and re-run, then paste. The
generated block is the record of what the motion is, and once it has been touched by hand
nobody can tell which numbers are physics and which are taste.

## The seam

A route with a start and an end has a teleport at the loop point: the mascot is at the
last stop at 100% and at the first stop at 0%. Two things handle it together.

**The fade.** `bake_mascot.py hop` emits a `-seam` opacity track that fades out inside the
last dwell and back in inside the first. The mascot disappears while standing still and
reappears while standing still, which is invisible.

**The half-loop shift.** Frame 0 of a GIF is the poster frame LinkedIn shows before
playback starts, and it must be a complete readable infographic. With no shift, frame 0
lands exactly on the fade and the pointer is missing from the poster. Add
`animation-delay: calc(var(--loop) * -0.5)` to every mascot track and `begin="-3s"` to the
`<animateMotion>`, and the seam moves to the middle of the loop where nobody sees it.

The stage delays then shift with it. The formula becomes:

```
|delay_i| = (0.5 - arrival_i) mod 1
```

For five stops at 11% dwell that is `0.5, 0.2775, 0.055, 0.8325`. Getting this wrong
produces a highlight that runs in a plausible but wrong order, which is the failure the
reverse-delay trap in `animation-recipes.md` describes.

## Motion budget with a mascot

A travelling element costs roughly **twice its own bounding box per frame**: the encoder
erases where it was and draws where it is. An idle costs about a third of its box, because
only a few rows of pixels change.

| Configuration | Measured `motion:` | Reading |
|---|---|---|
| Border highlight + typewriter, no mascot | 0.06% | very cheap |
| Border highlight + one 52px pointer + 1 payoff + 2 idles | **0.21%** | cheap, room to spare |
| Same with a 120px pointer | ~1.1% | healthy, still fine |
| Two travelling mascots | ~2.2% | dark flat grounds only, and the reading order is already broken |

So the budget is almost never what stops you. On House 0's light ground a 64px pointer at
12.5 fps lands around 0.25 MB for a 6 s loop. What actually caps mascot size is
legibility: below about 40px in the artboard the face is a smudge at LinkedIn's 350px feed
width, and above about 140px the mascot starts reading as the subject of the image rather
than as a pointer into it.

**40 to 90px is the working range.** Verify on `check_render.py --mobile`.

## Drawing the mascot

Flat fills only. No gradients, no blur, no `box-shadow`, no `filter`. Those defeat
rectangle diffing and a mascot that would have cost 20 KB a frame costs 200.

Pull the fills from House 0: `--accent` for the pointer, a section `--mid` for each idle,
`--accent-deep` for details. Using a section `mid` is what makes an idle read as belonging
to its panel rather than as a sticker.

Three parts is enough to be alive: a body, two eyes with pupils that can blink, and one
detail on top that gives the silhouette a direction. Eyes are what make a shape read as a
character, and a blink costs four keyframes.

Keep it under about 12 shapes. Everything else is detail nobody sees at 350px wide.

**Namespace every id and every `@keyframes`** with the mascot's `--id`. Six mascots inline
in one artboard share one document, and a second `@keyframes breathe` silently overrides
the first. `bake_mascot.py` does this automatically; artwork ids are on you.

## Archetype compatibility

| Archetype | Mascot fit | Notes |
|---|---|---|
| Character Flowchart | **native** | the archetype was already built around this |
| Pipeline Stages | **native** | the pointer walks the stages, which is what the archetype's sweep was faking |
| Annotated Blueprint | **native** | the spine is already a rail. Replace the draw-on with a hop |
| Flow Map + Verdict | good | pointer travels the converging wires, payoff sits on the verdict panel |
| Orbit Cycle | good | the pointer orbits; no payoff, because a cycle has no end |
| Trading Card Grid | idles only | one small idle per card. A pointer here fights the grid |
| Node Tree | idles only | the glow already is the pointer |
| Directory Map | idles only | the tree is the structure; a mascot hopping a file tree reads as clutter |
| Specimen Grid | **none** | 42 things already move. A mascot is invisible in it |
| Cheat Sheet Poster | **none** | this archetype exists to be saved and zoomed, and it is read on the still frame |
| Terminal Card | **none** | breaks the monospace illusion |
| Logo Grid, Spec Sheet | **none** | third-party brands and benchmark data. A character undercuts both |

## Failure modes

- **Two things claiming to be the pointer.** A mascot travelling while an accent border
  also sweeps independently. Delete one. If the mascot exists, the border reacts to it.
- **The mascot missing from frame 0.** The seam landed on the poster frame. Apply the
  half-loop shift.
- **Highlight and mascot out of sync.** Somebody hand-edited one of the two. Re-run
  `bake_mascot.py hop` and paste both outputs from the same run.
- **A sub-loop that is not an integer division.** An idle at `--n 7` gives 857.14ms inside
  a 6000ms loop and the composite cycle never closes. Legal values are 1, 2, 3, 4, 5, 6,
  8, 10, 12. The script refuses the rest.
- **Idles breathing in unison.** No phase offset. Give each a different negative delay;
  any fixed fraction works, and it must be fixed rather than random so every render is
  identical.
- **A mascot inside the 48px margin.** The title block and footer stay dead still. Note
  that `check_render.py` reports a **false positive** for animated groups that live inside
  `<defs>`: a defs child has a zero-size rect at the origin, which reads as a margin
  violation. Check whether the flagged element is a template before chasing it.
- **Anime.js left in the page.** The render comes back static or blank. Bake it.
- **The mascot doing something the diagram does not say.** A character celebrating at a
  stage that is described as a review pass reads as a lie. The payoff fires at the payoff,
  and nowhere else.
