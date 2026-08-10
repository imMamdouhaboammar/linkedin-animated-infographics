# AI doesn't buy the media — Signal to Decision

A LinkedIn animated infographic on where AI actually helps a media buyer: not in running the buy, in shortening the distance between a signal and a decision.

Produced end to end through the `new-post` parent workflow.

## Files

| File | What it is |
|---|---|
| `post.html` | the animated artboard, the source of truth |
| `post.gif` | 1080x1350, 7.68s, 96 frames, 0.39 MB, loops infinitely |
| `still.png` | frame 0 at full size |
| `still-feed-350.png` | the same frame at LinkedIn feed width, for the legibility gate |
| `motion-qa-mid.png` | frame 48, the loop midpoint |
| `motion-qa-final.png` | frame 95, the last frame before the seam |
| `caption.md` | the post caption |
| `first-comment.md` | the first comment, carrying the link and the evidence note |
| `pipeline/` | every artifact the workflow produced, in stage order |

## Info-story contract

| Axis | Choice |
|---|---|
| Story House | `signal-desk` (added as a first-party extension for this build) |
| Visual Style | `funnel-board` |
| Story Archetype | `raw-input-to-final-output` |
| Motion Patterns | `connector-draw` (primary) + `node-pulse` (secondary) |
| Design dials | variance 7, motion 6, density 7 |
| Alignment | center-first, with a recorded lateral exception for the hero band |

## Rebuild

```bash
D=deliverables/ai-decision-latency

# writes still.png, and alongside it still_mobile350.png
python3 scripts/check_render.py $D/post.html --out $D/still.png
mv $D/still_mobile350.png $D/still-feed-350.png

bash scripts/render.sh $D/post.html $D/post.gif --duration 7.68 --fps 12.5

# the two motion QA frames come from the capture, not a second render
cp $D/.frames/f0048.png $D/motion-qa-mid.png
cp $D/.frames/f0095.png $D/motion-qa-final.png
```

Requires a Chromium-family browser and an ffmpeg build that includes the `image2` demuxer.
The ffmpeg bundled with Playwright does not have it and fails at `palettegen`.

## Numbers

| Gate | Measured | Ceiling |
|---|---|---|
| file size | 0.39 MB | 5 MB |
| motion per frame | 0.14% | 2% |
| loop seam | 0.79% | 8% |
| duration | 7.68s | 8s |
| contrast pairs passing | 32 / 32 | all |

## Two things a reader should know

**No numbers.** Nothing on the artboard is measured. States are qualitative on purpose: `STRONG SIGNAL`, `NEEDS MORE DATA`, `LOSING MOMENTUM`. The three example insights sit under an `EXAMPLE OUTPUT` label because they are illustrative, not findings.

**Real marks where they exist, literal names where they do not.** Nothing is traced from memory anywhere on this artboard.

The three AI tools carry their owners' own artwork, resolved from a pinned release of `@lobehub/icons-static-svg` and inlined unmodified. Source URL, package version and SHA-256 for each are in `pipeline/evidence.json`. MIT covers the packaging of that set and carries no right in the marks; each one identifies the product it names inside a zone captioned "These tools do not run the buy."

The six signal-source platforms stay literal name tokens. That upstream set is an AI/LLM set: it has Google and Meta but no TikTok, LinkedIn, Reddit or Google Analytics. Giving two of six real logos while four siblings stayed as text would read as a mistake rather than a decision, so the whole zone keeps one treatment. The rule: **a zone uses vendor artwork only when every member of that zone has a real mark.**

Supplying the four missing SVGs turns that zone over without a layout change.
