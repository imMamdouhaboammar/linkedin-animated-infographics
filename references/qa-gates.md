# QA Gates

Run every gate before export. Each one catches a failure that is invisible on your own
screen and obvious in someone else's feed.

## Gate 1 — Artboard integrity

```bash
python3 scripts/check_render.py build/post.html --out build/still.png
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
- [ ] The single takeaway lands without zooming

Everything below 22px in the artboard is texture at this size. That is acceptable for
micro labels and card body copy. It is not acceptable for anything the post depends on.

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

- [ ] `loop:` delta reported under 8%

That number is the share of pixels differing between the first and last captured frame.
For a smoothly moving animation a few percent is expected — the last frame is one step
before the loop point, not identical to the first. Above 8% means something genuinely
does not close: a keyframe whose `100%` differs from its `0%`, or a duration that is not
an integer division of the loop.

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

## Gate 7 — File

```bash
ffprobe -v error -show_entries stream=width,height,nb_frames,duration \
  -of default=noprint_wrappers=1 build/post.gif
ls -la build/post.gif
```

- [ ] Under 5 MB
- [ ] Under 8 seconds
- [ ] 1080x1350
- [ ] Loops infinitely (open it in a browser and watch it repeat)

## Gate 8 — Content

- [ ] Every number on the artboard is real and verifiable
- [ ] Every product name is spelled the way the company spells it
- [ ] Any code, prompt, or command is literally copy-pasteable and correct
- [ ] The attribution footer is right
- [ ] No placeholder text survived (`YOUR NAME`, `Adviser One`, `yoursite.com`)

Search the HTML for the template placeholders before you export. This is the most
embarrassing failure and the easiest to prevent.

## Gate 9 — Caption

- [ ] Line 1 is under 60 characters and works alone
- [ ] Every line has a blank line after it unless it is a tight list
- [ ] No em dashes
- [ ] No banned buzzwords
- [ ] No denial-then-reveal construction in any line
- [ ] Exactly one CTA, at the end
- [ ] Links are in the first comment, not the caption
- [ ] Specific numbers and specific product names throughout

Read the caption top to bottom out loud. Anything you would not say out loud, cut.

## Gate 10 — RTL, if applicable

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
2. Is the moving area under 20%?
3. Watch the loop five times. Any jump?
4. Search the HTML for `YOUR NAME` and `yoursite.com`.
5. Read line 1 of the caption. Would you stop for it?
