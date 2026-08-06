# Asset contract

Every delivered file satisfies all of this. `scripts/check_asset.py` verifies most of it
automatically; the judgement items are marked.

- [Accessibility](#accessibility)
- [Namespacing](#namespacing)
- [Motion accessibility](#motion-accessibility)
- [Colour and themes](#colour-and-themes)
- [The img context](#the-img-context)
- [File size](#file-size)
- [Delivery notes](#delivery-notes)
- [QA checklist](#qa-checklist)

## Accessibility

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 200" width="460" height="200"
     role="img" aria-labelledby="mascot-jump-t mascot-jump-d">
  <title id="mascot-jump-t">Mascot launching from local to prod</title>
  <desc id="mascot-jump-d">The mascot crouches, launches along an arc, lands with a squash
  and one smaller rebound, then a check mark appears.</desc>
```

`role="img"` tells assistive technology to treat the whole graphic as one image rather than
walking its internals. The `<title>` is the short name and the `<desc>` describes what
happens over time, which is the part a static alt text cannot carry. Both need ids, and both
ids belong in `aria-labelledby` in that order.

Keep `width` and `height` on the root alongside `viewBox` so the file has an intrinsic size
when used as an image and does not collapse or stretch to fill its container.

## Namespacing

Prefix every `id` and every `@keyframes` name with the filename stem. Two files inlined on
the same page share one document, so a second `#m` or a second `@keyframes drop` silently
overrides the first. The symptom is one graphic rendering with another's gradient or timing,
which is nearly impossible to diagnose from the outside.

This costs nothing when the file is used as `<img>` and saves the user when it is not.

## Motion accessibility

```css
@media (prefers-reduced-motion:reduce){
  .x,.y,.r,.s{animation:none}
  .x{transform:translateX(382px)}
  .tick{opacity:1}
}
```

Stopping the animation is half the job. The other half is leaving a pose that still
communicates, chosen from the payoff of the story rather than its first frame. Vestibular
sensitivity is common and the setting is a real request, not a formality.

## Colour and themes

Brand colours stay fixed. Neutrals (ground lines, labels, shadows, frames) need a dark
variant, since a graphic that reads on a white README disappears on a dark one:

```css
svg{--ink:#6E6C66;--dim:#C8C5BD}
@media (prefers-color-scheme:dark){svg{--ink:#A9A69D;--dim:#46443F}}
```

Custom properties declared on the root `svg` work inside a file used as an image, and the
media query evaluates against the viewer's system preference.

Judgement item: check that any colour carrying meaning (a red overload state, a green
success mark) still reads at both extremes, and that nothing relies on colour alone to
communicate.

## The img context

An SVG loaded through `<img>`, a README, or a `background-image` is an isolated document
with no scripting and no network:

- `<script>` never executes. Everything is CSS animation or SMIL.
- External fonts never load. Use generic families (`ui-monospace`, `sans-serif`) and expect
  the metrics to shift between machines, so leave slack around text or convert critical
  lettering to paths.
- External images, stylesheets, and any absolute URL are blocked.
- CSS custom properties, media queries, and `@keyframes` all work normally.
- SMIL (`<animate>`, `<animateMotion>`, `<mpath>`) works and is a good fit for motion along
  a path, since the motion updates automatically when the path changes.

## File size

A README asset should stay well under 30KB. Sample counts drive the size: nine samples per
arc and seven per spring impact are plenty. If a file crosses 60KB, reduce the sampling
before reducing the animation.

Run SVGO with `removeViewBox` disabled and with `<title>`, `<desc>`, `id` attributes, and
`@keyframes` preserved. A default SVGO preset strips several of those and quietly breaks both
the accessibility contract and the animation.

## Delivery notes

When the asset is destined for a repository README, the markdown snippet is part of the
deliverable:

```markdown
![Mascot shipping](https://raw.githubusercontent.com/<user>/<repo>/main/svgs/mascot-ship-it.svg)
```

Two things worth telling the user:

- Image hosts commonly proxy and cache repository images aggressively, so an updated file may
  take a while to appear for viewers. Changing the filename forces the update.
- Different themes can be served with `<picture>` and a `media` attribute where the platform
  supports it, which is an alternative to the in-file dark mode block when the two versions
  need to differ more than colour.

## QA checklist

Run `check_asset.py`, then confirm by eye:

- The loop restarts without a visible jump
- Contact frames are short enough that impacts feel solid
- The shadow stays in phase with the subject at every height
- Nothing crosses the viewBox edge at any point in the cycle, including at the apex and at
  maximum stretch
- Text stays inside its container with substituted fonts
- The reduced-motion pose still tells the story
- Neutrals read on both a white and a near-black background
- The subject's silhouette stays recognisable at the extremes of squash and stretch
