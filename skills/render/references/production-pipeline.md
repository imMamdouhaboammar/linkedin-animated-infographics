# Production Pipeline

Setup, mechanics, troubleshooting, and the alternatives worth knowing about.

## Requirements

| Component | Why |
|---|---|
| Python 3.9+ | drives the capture |
| `playwright` (python package) | browser automation |
| A Chrome or Chromium binary | the renderer |
| `ffmpeg` | GIF assembly with two-pass palette |
| `pillow` | loop-delta check and mobile preview |

```bash
bash scripts/setup.sh
```

### The browser problem

Playwright normally downloads its own Chromium on `playwright install chromium`. On
locked-down networks that CDN is often unreachable, and the command exits 0 having
downloaded nothing, which is confusing. `setup.sh` detects this and falls back to
installing Google Chrome from `dl.google.com`.

If both fail, install Chrome by hand and pass the path:

```bash
python3 scripts/capture_frames.py post.html --browser /path/to/chrome ...
```

Any Chromium-family browser works. Firefox and WebKit do not: `offset-path`, SMIL
seeking, and `document.getAnimations()` coverage all differ.

### Chrome flags that matter

`capture_frames.py` sets these and you should not remove them:

| Flag | Why |
|---|---|
| `--disable-lcd-text` | subpixel antialiasing puts coloured fringes on every glyph, which adds hundreds of colours to the palette and inflates the GIF |
| `--font-render-hinting=none` | guarantees identical glyph rasterisation across frames so static text diffs to zero |
| `--force-color-profile=srgb` | without it, colours shift between machines |
| `--disable-gpu` | GPU rasterisation is non-deterministic between frames |
| `--hide-scrollbars` | a scrollbar would appear in the screenshot |

---

## How seeking works

Real-time recording samples whatever the compositor happened to produce, which drifts.
Seeking asks the browser for the exact state at time `t`.

```js
document.getAnimations().forEach(a => { a.pause(); a.currentTime = tMs; });
document.querySelectorAll('svg').forEach(s => s.setCurrentTime(tMs / 1000));
```

The first line covers CSS `@keyframes` and WAAPI. The second covers SVG SMIL
(`<animateMotion>`, `<animate>`), which lives in a separate timeline.

### What cannot be seeked

- `requestAnimationFrame` loops. `capture_frames.py` traps `rAF` and warns you.
  Convert the motion to CSS keyframes.
- CSS `transition`. There is no timeline to seek. The script disables transitions
  entirely via injected CSS.
- Canvas or WebGL drawn per-frame from a clock. Rewrite as SVG, or drive the canvas
  from an explicit `t` parameter you can set from `page.evaluate`.
- GIF or video elements embedded in the page. They play on their own clock. Replace
  them with a still.

---

## Measuring element positions for SVG wires

The most common build problem is wires that do not land on card edges. Measure rather
than guess:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome",
                          args=["--no-sandbox", "--disable-gpu"])
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.goto(Path("post.html").resolve().as_uri())
    pg.wait_for_timeout(400)
    print(pg.evaluate("""() => {
      const ab = document.querySelector('#artboard').getBoundingClientRect();
      const g = s => [...document.querySelectorAll(s)].map(e => {
        const r = e.getBoundingClientRect();
        return { cx: Math.round(r.left - ab.left + r.width / 2),
                 top: Math.round(r.top - ab.top),
                 bot: Math.round(r.bottom - ab.top) };
      });
      return { cards: g('.cards .card'), synth: g('.synthbox')[0] };
    }"""))
    b.close()
```

Feed the numbers straight into the `d` attributes. Re-measure after any layout change.

---

## GIF encoding

Two passes. Pass one builds an optimal palette from the actual frames; pass two applies
it. Single-pass encoding uses a generic 256-colour web palette and looks visibly worse
at twice the size.

```bash
ffmpeg -framerate 12.5 -i f%04d.png \
  -vf "palettegen=max_colors=128:stats_mode=diff" palette.png

ffmpeg -framerate 12.5 -i f%04d.png -i palette.png \
  -lavfi "paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle" \
  -loop 0 out.gif
```

| Option | Effect |
|---|---|
| `stats_mode=diff` | weights the palette toward pixels that actually change, so moving elements get the colour budget |
| `dither=bayer:bayer_scale=4` | ordered dithering. Produces a stable pattern across frames, so static areas compress. `sierra2_4a` looks better on photos but its error diffusion changes every frame and doubles file size on flat art |
| `diff_mode=rectangle` | encodes only the changed rectangle per frame. This is what makes a small motion budget pay off |
| `-loop 0` | infinite loop |

### Palette size

Flat vector art needs far less than 256. Start at 128. Drop to 96 or 64 if you need
size; on flat art the difference is invisible. Below 48 you start seeing banding in
gradients and soft shadows.

`build_gif.py` walks this ladder automatically and prints each attempt.

### Size budget

Target under 5 MB. LinkedIn accepts larger but transcodes them, and the transcode is
worse than anything you would produce yourself.

The three levers, in the order you should pull them:

1. **Moving area.** By far the biggest. Halving it roughly halves the file.
2. **Palette.** 128 → 64 typically saves 25–35% with no visible change.
3. **Frame rate.** 30 → 15 halves the frames. Only acceptable for stepped animation.

Resolution last. Dropping below 1080 wide is visible in feed and defeats the point.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Every frame identical | animations use `rAF`, or `--duration` does not match `--loop` | check the warning from `capture_frames.py` |
| Text shimmers between frames | subpixel AA, or a webfont loaded mid-capture | flags are set by default; embed the font |
| GIF is 15 MB | motion budget blown | read `animation-recipes.md`, "Motion budget" |
| Artboard captured at 1040 wide | `body` padding squeezing a flex child | add `flex: none` to `#artboard` |
| Visible seam at the loop point | keyframes do not close | `build_gif.py` reports the delta; fix the endpoints |
| Particles float off the wire | `offset-path` in a different coordinate space | put the particle inside the SVG and use `<mpath>` |
| Colours look washed out | missing `--force-color-profile=srgb` | it is set by default; check you did not override the args |
| Highlight order is 1-4-3-2 | the reverse-delay trap | see `animation-recipes.md` |
| Blank first frame | animation starts at `opacity:0` with a positive delay | use a negative delay |

---

## Alternatives

Worth knowing, though the HTML pipeline is what this skill is built on.

**HyperFrames** (`heygen-com/hyperframes`, Apache 2.0, ~37k stars as of August 2026).
The closest thing to this skill, and worth knowing well because it validates the
architecture: HyperFrames also writes HTML, also seeks each frame in headless Chrome,
and also encodes with ffmpeg. Same bet, different output.

|  | This skill | HyperFrames |
|---|---|---|
| Output | looping GIF, 1080x1350 | MP4 (and WebM with alpha) |
| Audio | none | voiceover, music, captions, TTS |
| Animation runtimes | CSS keyframes, WAAPI, SMIL | plus GSAP, Lottie, Three.js, Anime.js, custom adapters |
| Length | 3–8 seconds | minutes |
| Scope | one LinkedIn post, caption included | video production generally |
| Install | one skill | 19 skills, a CLI, a block registry |

**Use HyperFrames when** the deliverable is a video: a product launch clip, a PR
walkthrough, a narrated explainer, anything with audio, anything over ten seconds.
Its `/motion-graphics` workflow covers short unnarrated design-led pieces and overlaps
directly with what this skill produces, except it hands you an MP4.

**Use this skill when** the deliverable is a LinkedIn post. The GIF is only half of it;
the caption archetypes, the visual archetypes and the RTL layer are the other half, and
HyperFrames does not cover any of that. It is a video framework, not a post system.

**Composing the two.** The artboards in `assets/` are plain HTML with CSS keyframes, so
they port to a HyperFrames composition with modest work: wrap the artboard in a
`data-composition-id` stage, add `data-start` and `data-duration`, and the CSS adapter
handles the rest. That gets you an MP4 of the same design when you want one. Going the
other way, a HyperFrames composition can be captured by `capture_frames.py` if it uses
seekable animation, which it is designed to.

```bash
npx skills add heygen-com/hyperframes --full-depth
npx hyperframes init my-video && npx hyperframes render
```

Requires Node 22+ and ffmpeg.

**On GIF versus video for LinkedIn.** Do not assume one beats the other. A GIF uploaded
through the image path loops silently and forever with no play affordance, which suits a
reference diagram people scroll past three times. Native video suits anything with
narration or a story arc. Test it on your own audience rather than trusting a general
claim, including this one.

**Remotion.** React components rendered to video, frame-by-frame, deterministically.
Source-available under the Remotion License rather than a permissive one, so check the
terms for commercial use. HyperFrames is explicitly inspired by it and ships a
`/remotion-to-hyperframes` porting workflow.

**Rive.** State-machine vector animation with a real editor. Excellent motion, exports
to video. The right tool for a mascot with a walk cycle. Not the right tool for a
diagram, because the layout work is much slower than CSS.

**After Effects + Lottie.** Best-in-craft motion. Requires a motion designer and a
licence. The reference posts are almost certainly not made this way; the tells are the
CSS-native easing curves and the pixel-snapped step timing.

**Canva / Figma export.** Fine for a single reveal. No control over loop close, palette,
or frame timing, and the GIF export is usually 3–4× larger than necessary.

**gifski** instead of ffmpeg. Higher quality per byte on gradients, slower, and you
lose `diff_mode=rectangle`. On flat vector art ffmpeg wins.

---

## Batch rendering

Rendering a set of posts:

```bash
for f in build/*.html; do
  name="$(basename "$f" .html)"
  bash scripts/render.sh "$f" "out/$name.gif" --duration 4.8 --fps 12.5
done
```

Each render launches its own browser, which is slow but keeps the runs independent.
A 60-frame capture takes roughly 20–40 seconds on a laptop.
