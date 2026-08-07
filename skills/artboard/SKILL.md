---
name: artboard
description: >-
  Choose a visual layout and build the 1080x1350 still. Use when picking a visual archetype for
  an infographic, laying out cards, panels, nodes, or a route, choosing colours, type, or
  spacing for a LinkedIn visual, or building the HTML artboard before any animation. Covers 13
  layout archetypes, the House 0 default palette with its nine section hues, offline-safe font
  stacks, the type scale, and the mandatory attribution footer.
---

# Artboard

The still is the approval gate. Build it, show it, get a yes, then animate.

## Pick the layout from the shape of the content

| Content shape | Archetype |
|---|---|
| A hierarchy of files or modules | Directory Map |
| A linear process with stages | Pipeline Stages |
| A cyclical process with no start | Orbit Cycle |
| Many inputs converging on one output | Flow Map + Verdict |
| A flat catalogue of third-party tools | Logo Grid |
| N independent items of equal weight | Trading Card Grid |
| A branching dependency graph | Node Tree |
| One product or integration announcement | Terminal Card |
| Dense reference material meant to be saved | Cheat Sheet Poster |
| A benchmark, spec, or timeline | Spec Sheet |
| A sequential how-to | Annotated Blueprint |
| A sequence made friendly, with a character | Character Flowchart |
| A catalogue you can *show* running | Specimen Grid |

Caption archetype and visual archetype are chosen independently.
`references/visual-archetypes.md` has the structural spec, what to animate, and the failure
mode for each, plus a table for choosing between adjacent ones.

## Colour: House 0 is the default

Warm paper ground, nine desaturated section hues in four tiers each, one terracotta carrying
every active state. Build in it unless the content is genuinely dark-technical (House 2 or 3)
or the brief names a brand palette, and say which house you switched to and why.

Drop-in token sheet: `${CLAUDE_PLUGIN_ROOT}/assets/house0-tokens.css`.
Rendered swatches: `${CLAUDE_PLUGIN_ROOT}/assets/house0-swatches.html`.

Tier discipline is what keeps it calm. `bar` for header strips, `wash` for panel bodies, `mid`
for filled badges with white text, `ink` for label text. Never a `mid` on a background larger
than 60px, never an `ink` as a fill. Full rules in `references/design-systems.md`.

Section hues are **static identity**. The accent is **state**. The moment a section hue
animates, the reader loses the ability to tell "this is panel four" from "this is the panel
being pointed at".

## Hard constraints

1. Exactly one `#artboard` element, `width:1080px; height:1350px`. The capture script
   screenshots that element, not the viewport.
2. Fonts are system-safe or base64-embedded in the same file. A webfont that loads over the
   network renders as a fallback in some frames and not others, and the GIF flickers.
3. Nothing in the outer 48px margin may ever move. That band holds the title and the footer.
4. **The attribution footer is mandatory.** Avatar, name, one URL. These images get reposted
   stripped of the caption, and the footer is the only thing that survives.
5. Anything load-bearing stays at or above 22px in artboard units, which is about 7px at
   LinkedIn's 350px feed width.
6. Text must reach **4.5:1 contrast** and body-role text must use **500 weight or heavier**.
   Use each house's `--accent-deep` for accent-coloured text, never the raw accent token.
   See `references/design-systems.md#contrast-floor-every-house` for the calculation and
   token rules.

## Templates

`${CLAUDE_PLUGIN_ROOT}/assets/` holds `template-flow-map.html`, `template-orbit-cycle.html`,
`template-directory-map.html`, `template-specimen-grid.html`, and `template-mascot-flow.html`.
Start from one rather than from an empty file.

## Check the still

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py build/post.html --out build/still.png
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py build/post.html --mobile
```

The mobile downscale is the one to judge legibility on. Micro labels below 22px are
unreadable in feed by design; every flag is a judgement call, not an automatic failure.