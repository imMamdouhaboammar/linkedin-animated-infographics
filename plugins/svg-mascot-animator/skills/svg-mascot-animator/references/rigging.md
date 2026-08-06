# Rigging reference

How to prepare the artwork and structure the transforms so keyframes stay simple.

- [Normalize the artwork](#normalize-the-artwork)
- [One concern per group](#one-concern-per-group)
- [transform-box and origins](#transform-box-and-origins)
- [Single-path artwork](#single-path-artwork)
- [Splitting a path for articulation](#splitting-a-path-for-articulation)
- [Reduced-motion poses](#reduced-motion-poses)
- [Multiple instances](#multiple-instances)

## Normalize the artwork

Put the artwork in `<defs>` once, translated so the origin sits at its natural pivot, then
place instances with `<use>`:

```xml
<defs><g id="mascot-jump-m" transform="translate(-12,-20)">…artwork…</g></defs>
…
<use href="#mascot-jump-m" transform="translate(180,152) scale(2.6)"/>
```

For a grounded character the pivot is bottom centre: `translate(-(x0+x1)/2, -y1)`. For
something hanging it is top centre: `translate(-(x0+x1)/2, -y0)`. `inspect_svg.py` prints
both.

This matters because every later transform is expressed relative to that origin. With the
feet at `(0,0)`, a squash is `scale(1.14, .8)` and needs no origin correction; without it,
every scale drags the subject through the floor and you end up compensating with translate
values that have to be recomputed whenever anything changes.

The base scale belongs on the `<use>` element, outside the animated groups, so the animated
values stay in scene units and remain readable.

## One concern per group

Nest one transform per concern, outermost first:

```xml
<g class="x">        <!-- horizontal position -->
  <g class="y">      <!-- vertical position -->
    <g class="r">    <!-- rotation -->
      <g class="s">  <!-- scale: squash and stretch -->
        <use href="#mascot-jump-m" transform="translate(0,152) scale(2.6)"/>
```

CSS `transform` replaces the whole value, so two concerns in one group means every keyframe
has to restate both. Rotation and scale each need a different origin, which makes the
combination genuinely unworkable rather than merely tedious.

Separate groups also let each concern carry its own timing function. Horizontal travel is
linear, the vertical arc is linear between samples, and the squash is eased per segment.
One group cannot express that.

## transform-box and origins

The default `transform-box: view-box` resolves `transform-origin` against the SVG viewport,
not the element, so `transform-origin: 50% 100%` points at the bottom centre of the whole
canvas. On a nested, already-translated group the behaviour is easy to get wrong and varies
in the details between engines.

Set it explicitly on anything that scales or rotates:

```css
.s { transform-box: fill-box; transform-origin: 50% 100%; }  /* feet */
.r { transform-box: fill-box; transform-origin: 50% 50%; }   /* body centre */
.swing { transform-box: fill-box; transform-origin: 50% 0%; }  /* pivot at the top */
```

`fill-box` uses the element's own bounding box, computed before its own transform, which is
stable and predictable. Groups that only translate need no origin at all.

Two traps:

- A `<line>` has a zero-area bounding box, so `fill-box` on it is unreliable. Use a thin
  `<rect>` for anything that needs to scale, such as a rope under tension.
- A group's bounding box includes everything inside it. If a swing group holds a rope plus
  the body, its top centre is the pivot only when the rope starts exactly at the pivot and
  the body is centred on it. Check the numbers rather than assuming.

## Single-path artwork

Many icon-style mascots are one path with holes cut by `fill-rule="evenodd"`. Nothing inside
can move independently: no blinking, no limbs, no reactions.

What still works, and works well:

- Whole-body squash, stretch, rotation, and arcs
- Shadow, dust, sparks, and props drawn as separate elements around it
- Environment motion: scrolling ground, falling objects, filling meters, rotating scenery
- Silhouette-level acting, where the pose and timing carry the performance

Tell the user this at the start. Promising a walk cycle and delivering a hop is worse than
proposing a hop that fits the artwork.

## Splitting a path for articulation

When the user wants real articulation, the split is mechanical:

1. Identify the sub-shapes in the path data. Blocky mascots usually decompose into
   axis-aligned rectangles that are trivial to restate as `<rect>` elements.
2. Rebuild the body without the parts that need to move, keeping the same fill rule.
3. Emit each moving part as its own element with its own pivot, positioned to overlap the
   body slightly so no seam appears during rotation.
4. Verify the reassembled static version matches the original pixel for pixel before
   animating anything.

With separate legs, a four-legged gait uses diagonal pairs in antiphase, the body bobs at
twice the stride frequency, and a treadmill ground must scroll at exactly stride length
divided by cycle time or the feet visibly slip.

## Reduced-motion poses

Presentation attributes act as the lowest-priority style, so an element can carry
`transform="translate(78,0)"` as an attribute while a CSS animation overrides it during
playback. Setting `animation: none` in the reduced-motion block falls back to that attribute
value, which is a clean way to define the resting pose once.

Choose the pose that carries the story rather than the first frame. A jump asset should show
the subject landed with the check mark visible; an overload asset should show the full stack
and the red meter. A reduced-motion viewer should learn the same thing everyone else does.

## Multiple instances

`<use>` referencing one `<defs>` entry keeps the file small when a scene needs several
copies. Each instance can carry its own class, delay, and custom properties, so a crowd of
identical subjects with staggered timing costs almost nothing:

```xml
<use href="#m" class="hop" style="--delay:.12s" transform="translate(120,152) scale(2)"/>
<use href="#m" class="hop" style="--delay:.24s" transform="translate(190,152) scale(2)"/>
```

Referenced content inherits `currentColor` and CSS custom properties from the instance, so
recolouring per instance works without duplicating the geometry.
