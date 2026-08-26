# QA Gates

Run every gate before export. Each one catches a failure that is invisible on your own
screen and obvious in someone else's feed.

## Gate 1 — Artboard integrity

```bash
python3 scripts/artboard_audit.py build/post.html --json build/artboard-audit.json
python3 scripts/check_render.py build/post.html --out build/still.png --mobile --json build/still-audit.json
```

- [ ] Size reports exactly `1080x1350`
- [ ] No content clipped at any edge
- [ ] The footer bar is present with name and URL
- [ ] Nothing overlaps

A size other than 1080x1350 usually means `#artboard` is missing `flex: none` and got
squeezed by a flex parent.

## Gate 2 — Mobile legibility

Open `build/still_mobile350.png` and look at it honestly, at 100%.

- [ ] The headline is readable
- [ ] Section headers are readable
- [ ] Card titles are readable
- [ ] Nothing looks pale, thin, or washed out
- [ ] The single takeaway lands without zooming

Everything below 22px in the artboard is texture at this size. That is acceptable for
micro labels and card body copy. It is not acceptable for anything the post depends on.

If text is large enough but still looks pale, thin, or washed out, diagnose **contrast and
weight before size**. Verify a minimum 4.5:1 text contrast ratio and use 500 weight or
heavier for body-role text. Increasing font size is not the default fix for a weak colour
pair or a weight that disappears after downscaling.

If the takeaway does not land, the artboard has too much content. Cut, do not shrink.

## Gate 3 — Motion budget

The number that matters is `build_gif.py`'s `motion:` line — the mean share of pixels
changing between consecutive frames.

- [ ] Mean change per frame under 2% (under 5% is acceptable on a dark flat ground)
- [ ] No animated element inside the 48px safe margin
- [ ] Nothing full-bleed is animating

`check_render.py` reports bounding-box area instead. That number over-reports badly for
stroke animations and for dense grids of tiny loops, so treat it as a smell test for an
accidental full-canvas fade, not as a pass/fail gate.

The safe-margin rule exists because the title block and the footer are the two things a
reader's eye returns to. Movement there makes the whole image feel unstable.

Two primitives is the norm for a single-focus layout. The Specimen Grid archetype is the
exception and runs one ambient loop per cell plus a category sweep.

## Gate 4 — Loop close

From `build_gif.py`:

- [ ] `loop:` seam multiplier at or below 1.25 (`x1.25` in the printed line)
- [ ] never above 2.0

The number that gates is the **ratio**, printed as `x<n>`: the seam change divided by the
largest change between any two consecutive frames in the loop.

Do not gate on the raw seam percentage. The last captured frame legitimately sits one step
of motion *before* the loop point, so it is never identical to frame 0, and on a stepped
animation one step can be a large visual change that also occurs at several other points
in the loop. An absolute percentage therefore fails in both directions: it flags clean
fast loops and passes broken slow ones. The ratio normalises the seam against the loop's
own biggest step, so at or below 1.25 the seam is indistinguishable from any other frame
boundary — which is exactly what a clean loop means.

Above 2.0 means something genuinely does not close: a keyframe whose `100%` differs from
its `0%`, or a duration that is not an integer division of the loop.

Then watch the GIF loop five times in a row. If your eye catches a jump, it will catch
it in feed too.

## Gate 5 — Animation order

Capture four frames across the loop and confirm the sequence reads in the intended
direction:

```bash
ffmpeg -v error -i build/post.gif \
  -vf "select='eq(n\,0)+eq(n\,15)+eq(n\,30)+eq(n\,45)'" -vsync 0 /tmp/order%d.png
```

- [ ] Sequential Highlight runs 1, 2, 3, 4 (or right to left in RTL)
- [ ] Particles travel toward the convergence point, not away from it
- [ ] Reveals happen in reading order

The reverse-delay trap produces 1, 4, 3, 2 and is easy to miss.

## Gate 6 — First-frame integrity

LinkedIn shows a static poster before the GIF plays for some users, and every
screenshot anyone takes of your post is a single frame.

- [ ] Frame 0 is a complete, readable infographic on its own
- [ ] No element is mid-fade, half-drawn, or at `opacity: 0` in frame 0
- [ ] The first highlighted element is the one you want seen first

## Gate 7 — Final-frame visibility

Elements marked `data-final-visible` are required to remain substantially visible at the
last exported frame. The browser hit-test samples five points inside each element; at least
60% of those samples must remain visible. Full occlusion and severe partial occlusion are
blocking failures.

- [ ] Required headlines and CTAs are visible at the final sampled frame
- [ ] No overlay covers more than two of the five hit-test samples
- [ ] `final-frame.json` records the threshold id and sampled visibility ratio

## Gate 8 — File

```bash
ffprobe -v error -show_entries stream=width,height,nb_frames,duration \
  -of default=noprint_wrappers=1 build/post.gif
ls -la build/post.gif
```

- [ ] Under 5 MB
- [ ] Under 8 seconds
- [ ] 1080x1350
- [ ] Loops infinitely (open it in a browser and watch it repeat)

## Gate 9 — Content

- [ ] Every number on the artboard is real and verifiable
- [ ] Every product name is spelled the way the company spells it
- [ ] Any code, prompt, or command is literally copy-pasteable and correct
- [ ] The attribution footer is right
- [ ] No placeholder text survived (`YOUR NAME`, `Adviser One`, `yoursite.com`)

Search the HTML for the template placeholders before you export. This is the most
embarrassing failure and the easiest to prevent.

## Gate 10 — Caption

- [ ] Line 1 is under 60 characters and works alone
- [ ] Every line has a blank line after it unless it is a tight list
- [ ] No em dashes
- [ ] No banned buzzwords
- [ ] No denial-then-reveal construction in any line
- [ ] Exactly one CTA, at the end
- [ ] Links are in the first comment, not the caption
- [ ] Specific numbers and specific product names throughout

Read the caption top to bottom out loud. Anything you would not say out loud, cut.

## Gate 11 — RTL, if applicable

See `references/arabic-rtl.md` for the full list.

- [ ] Arabic joins intact at 200% zoom
- [ ] Mixed English terms wrapped in `<bdi>` and reading in the right order
- [ ] SVG wires re-measured after mirroring
- [ ] One numeral system throughout
- [ ] Highlight runs right to left
- [ ] One dialect, matched to the market

---

## The five-minute version

When you are shipping fast:

1. Look at `still_mobile350.png`. Does the takeaway land?
2. Is mean changed-pixel motion under 5%?
3. Watch the loop five times. Any jump?
4. Search the HTML for `YOUR NAME` and `yoursite.com`.
5. Read line 1 of the caption. Would you stop for it?

## Mascot gates

Only when the artboard carries a character. Full doctrine in `references/mascots.md`.

- [ ] **One pointer.** Exactly one mascot travels. If an accent sweep also runs
      independently of it, one of the two has to go.
- [ ] **Frame 0 shows the pointer.** The seam fade must not land on the poster frame.
      Symptom: a complete-looking still with the character missing.
- [ ] **Highlight matches arrival.** Step through four frames at the baked arrival
      instants and check the lit stage is the one the mascot is standing on.
- [ ] **Every sub-loop is an integer division** of `--loop`: 1, 2, 3, 4, 5, 6, 8, 10, 12.
- [ ] **Idle amplitude at or under 4px**, and every idle carries a different phase offset.
- [ ] **No rAF, no Anime.js runtime** anywhere in the page. Baked CSS or SMIL only.
- [ ] **`rotate="0"`** on every `<animateMotion>` unless banking is deliberate.
- [ ] **Mascot between 40px and 90px** in artboard units. Confirm the face still reads on
      `check_render.py --mobile`.
- [ ] **Flat fills only.** No gradient, blur, or shadow spread on the character.
- [ ] **Ids and keyframe names namespaced** with the mascot's `--id`.

Known false positive: `check_render.py` flags animated groups living inside `<defs>` as
safe-zone violations, because a defs child reports a zero-size rect at the origin. Confirm
whether the flagged element is a template before moving anything.

## Machine-readable verdict

`render.sh` writes artboard, still, and GIF JSON fragments, then merges them into
`build/render-report.json`. Every finding carries its measured value, threshold, unit,
severity, status, and evidence. Missing or `NA` blocking evidence fails the merge; the
report also records SHA-256 digests for the input HTML, output GIF, and source fragments.
