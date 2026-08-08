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
python3 scripts/check_render.py deliverables/ai-decision-latency/post.html --out /tmp/still.png
bash scripts/render.sh deliverables/ai-decision-latency/post.html /tmp/post.gif --duration 7.68 --fps 12.5
```

Requires a Chromium-family browser and an ffmpeg build that includes the `image2` demuxer.

## Numbers

| Gate | Measured | Ceiling |
|---|---|---|
| file size | 0.39 MB | 5 MB |
| motion per frame | 0.14% | 2% |
| loop seam | 0.78% | 8% |
| duration | 7.68s | 8s |
| contrast pairs passing | 26 / 26 | all |

## Two things a reader should know

**No numbers.** Nothing on the artboard is measured. States are qualitative on purpose: `STRONG SIGNAL`, `NEEDS MORE DATA`, `LOSING MOMENTUM`. The three example insights sit under an `EXAMPLE OUTPUT` label because they are illustrative, not findings.

**No traced logos.** No official SVG was supplied for any platform or AI vendor, so none was redrawn from memory. Platforms appear as correctly spelled name tokens in each vendor's brand colour. The token slots take real SVGs without any layout change.
