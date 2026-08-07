# Design Systems

Five house styles observed across the reference set, plus the type stacks that survive
offline rendering and the spacing scale that holds the layouts together.

**House 0 is the default.** Build in it unless the content is genuinely dark-technical
(House 2, House 3) or the brief names a brand palette. The other four stay documented
because they are what the reference posts actually use.

## Why offline fonts matter

`capture_frames.py` freezes the page and screenshots 60 times. If a webfont is still
loading, some frames render in the fallback and some in the real face, and the GIF
flickers. Three safe options, in order of preference:

1. **System stacks** (below). Zero risk, and every OS in the reference set renders them
   close enough that nobody notices.
2. **Base64-embedded woff2** inside a `@font-face` in the same HTML file. Adds weight to
   the file but the render is deterministic.
3. A local font file referenced with a `file://` path. Works, but the artboard stops
   being portable.

Never `@import` from Google Fonts. The capture script waits on `document.fonts.ready`,
but a network hiccup mid-capture still produces mixed frames.

### System stacks

```css
/* Editorial display — headlines in the Charlie Hills / Ruben Hassid family */
--display: "Iowan Old Style", "Palatino Linotype", Georgia, "Times New Roman", serif;

/* Neutral grotesk — body, cards, labels */
--sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue",
        Inter, Arial, sans-serif;

/* Monospace — commands, paths, code blocks, terminal cards */
--mono: "SF Mono", ui-monospace, "Cascadia Mono", "Roboto Mono", Menlo,
        Consolas, "Liberation Mono", monospace;

/* Condensed display — the pixel/poster headline in the Priyanka family */
--condensed: "Haettenschweiler", "Arial Narrow Bold", "Impact", sans-serif;

/* Arabic — see references/arabic-rtl.md before using */
--arabic: "SF Arabic", "Segoe UI", "Noto Naskh Arabic", "Dubai", Tahoma, sans-serif;
```

---

## House 0 — Muted Reference (the default)

**Use this unless the brief asks for something else.** It is the softest palette in the
set and the only one built for long dwell time: warm off-white ground, near-white panel
fills, nine desaturated section hues, and a single terracotta that carries every active
state. Nothing in it is above about 55% saturation, so it holds up at full brightness on
a phone at night, which is where most of these posts get read.

Sampled from a nine-panel cheat-sheet poster, so the values are observed rather than
invented. Every hue ships in four tiers and you pick the tier by job, never by taste.

### Core

```css
--bg:          #FDFAF5;   /* warm paper ground, faint speckle */
--paper:       #FCFCF9;   /* panel and card fill, one step off the ground */
--ink:         #3A342F;   /* headlines and card titles */
--ink-2:       #4C413D;   /* body copy */
--muted:       #7C736C;   /* sublines, micro labels, dotted leaders */
--line:        #E4DED4;   /* every border and rule */
--accent:      #A85B36;   /* terracotta */
--accent-wash: #F7EAE1;
--accent-deep: #8C4526;   /* accent text on a wash fill */
--foot:        #2E2A26;   /* attribution bar */
```

### The nine section hues

Each hue exists in four tiers. `bar` is the header strip, `wash` is the panel body when
you need the section colour to carry into the content, `mid` is the only tier that takes
white text, and `ink` is the label on a bar or wash.

```css
/* 1 apricot */  --s1-bar:#EACCAE; --s1-wash:#FAF1E7; --s1-mid:#D07418; --s1-ink:#A35508;
/* 2 blush   */  --s2-bar:#DEBAD2; --s2-wash:#F7EBF3; --s2-mid:#AB3D86; --s2-ink:#842765;
/* 3 clay    */  --s3-bar:#D2B4AE; --s3-wash:#F6EEEC; --s3-mid:#A15647; --s3-ink:#7B3C30;
/* 4 mist    */  --s4-bar:#BACCCC; --s4-wash:#EFF3F3; --s4-mid:#5D8C8C; --s4-ink:#426969;
/* 5 lilac   */  --s5-bar:#CCC0D2; --s5-wash:#F2EEF4; --s5-mid:#7D5A8E; --s5-ink:#5D3F6B;
/* 6 mauve   */  --s6-bar:#BA9CB4; --s6-wash:#F4EEF3; --s6-mid:#905885; --s6-ink:#6D3E64;
/* 7 wheat   */  --s7-bar:#D8CC96; --s7-wash:#F8F6EA; --s7-mid:#BCA22C; --s7-ink:#927C19;
/* 8 sage    */  --s8-bar:#C0C6BA; --s8-wash:#F1F3EF; --s8-mid:#748365; --s8-ink:#556249;
/* 9 slate   */  --s9-bar:#909090; --s9-wash:#F1F1F1; --s9-mid:#747474; --s9-ink:#575454;
```

Slate is the closer. In the source poster it carries the final panel, the one holding
limits, checklists and safety rules. Use it for the summary block and nowhere else, and
the reader learns within one scroll that grey means "this is the part you act on".

### Tier discipline

This is the rule that keeps the palette calm, and the one most likely to get broken:

| Tier | Allowed on | Never on |
|---|---|---|
| `bar` | header strips, chips, badge fills behind dark text | body text, large fills over ~30% of a panel |
| `wash` | panel bodies, callout boxes, table row stripes | anything that also carries an accent border |
| `mid` | filled badges with white text, small icon tiles | text, borders, backgrounds larger than 60px |
| `ink` | section labels, list glyphs, the section name | fills of any size |

`bar` and `wash` never touch each other inside one component. A wash body under a bar
header is the exception the layout is designed around; everything else reads as mud.

### Accent discipline in this house

Nine hues plus an accent looks like it breaks the one-accent rule in the section below.
It does not, because the section hues are **static identity** and the accent is **state**:

- Section hues never animate. They are frozen the whole loop.
- The terracotta appears on exactly four things: one word in the headline, the active
  border of whatever the sequential highlight is walking through, the list glyph, and
  the CTA. That is it.

The moment a section hue animates, the reader loses the ability to tell "this is panel
four" from "this is the panel being pointed at", and the reading pointer stops working.

### Assigning hues to sections

Walk the list in order and take the next hue. Do not pick by meaning; the sequence is
the meaning. Two adjacent sections must never share a hue family, which is why the
order runs warm, cool, warm, cool rather than grouping the warms together:

```
apricot → blush → clay → mist → lilac → mauve → wheat → sage → slate
```

Under six sections, drop from the end and keep slate as the closer if you have a summary
block: `apricot, mist, mauve, wheat, sage, slate`.

### Texture

The ground carries a fine speckle, not a grid. It is what stops 1080x1350 of off-white
from banding in a 128-colour GIF.

```css
background-color: var(--bg);
background-image:
  radial-gradient(rgba(58,52,47,.055) .6px, transparent .7px),
  radial-gradient(rgba(58,52,47,.038) .6px, transparent .7px);
background-size: 13px 13px, 21px 21px;
background-position: 0 0, 7px 11px;
```

Two offset layers at coprime sizes so no repeat is visible. Keep the alpha under .06 or
it reads as noise rather than paper. If a GIF comes back over budget in this house, cut
the second layer before you cut anything else — speckle is the single most expensive
thing on a light ground.

### Panel recipe

```css
.panel { background: var(--paper); border: 1px solid var(--line); border-radius: 14px;
         overflow: hidden; }
.panel > .head { background: var(--s4-bar); padding: 11px 18px;
                 display: flex; align-items: center; gap: 11px; }
.panel > .head .num { width: 26px; height: 26px; border-radius: 8px;
                      background: var(--s4-mid); color: #fff;
                      font: 800 14px/26px var(--sans); text-align: center; }
.panel > .head .ttl { color: var(--s4-ink); font: 800 19px var(--sans);
                      letter-spacing: .01em; }
.panel > .body { padding: 18px; }
```

Set one `--s*` group per panel and nothing else changes. The header strip is the whole
identity system.

### Best for

Cheat Sheet Poster, Trading Card Grid, Pipeline Stages, Flow Map, Directory Map,
Annotated Blueprint. Anything with three or more parallel sections.

### Where it fails

- **Dense dark diagrams.** Node Tree and Terminal Card want House 2 or House 3. A glow
  on a cream ground reads as a printing error.
- **Under four sections.** With two or three panels the hue system has nothing to do and
  the post looks like it lost its colour. Use House 1 there.
- **Photography.** Any real image next to these tints makes them look washed out. Keep
  this house to type, rules and flat shapes.

---

## House 1 — Warm Paper

The most common in the set. Charlie Hills, Ruben Hassid, ColdIQ. Light, editorial,
grid-paper texture, serif headline with one accent word.

```css
--bg:          #FFFFFF;
--paper:       #FDFCFA;   /* card fills, one step off white */
--ink:         #16202C;
--ink-2:       #2B3540;   /* body copy */
--muted:       #57626F;
--line:        #D8DCE2;
--accent:      #D9744F;   /* terracotta; fills and active state only */
--accent-deep: #8C3E20;   /* accent-coloured text */
--accent-wash: #FBEDE6;
--footer-bg:   #101B29;

/* quadrant / category colours, used only for small labels */
--c-green:  #2E9E7B;
--c-amber:  #C9862F;
--c-purple: #8B5FBF;
--c-blue:   #2F7FBF;
```

Texture:

```css
background-image:
  linear-gradient(rgba(22,32,44,.028) 1px, transparent 1px),
  linear-gradient(90deg, rgba(22,32,44,.028) 1px, transparent 1px);
background-size: 36px 36px;
```

Best for: Flow Map, Spec Sheet, Cheat Sheet, Character Flowchart, Annotated Blueprint.

---

## House 2 — Deep Glow

Priyanka, navreo, DRIP. Near-black with accent glow on cards. Reads as "technical" and
photographs well against LinkedIn's white feed.

```css
--bg:          #0B0D12;
--card:        #12151C;
--card-2:      #171B24;
--ink:         #F2F4F7;
--muted:       #8C97A8;
--line:        rgba(255,255,255,.09);
--accent:      #E0603A;
--glow:        0 0 40px rgba(224,96,58,.18);
--tile:        #F5F1EA;   /* cream icon tiles, the only light element */
```

Card recipe:

```css
.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 14px;
  box-shadow: var(--glow), inset 0 1px 0 rgba(255,255,255,.04);
}
```

Pastel annotation pills on dark, for the Directory Map:

```css
--p-yellow:#FBE8A6; --p-cyan:#A9E9F0; --p-mint:#A9EBC8;
--p-lilac:#CFC2F5; --p-rose:#F5B7B7;   /* all with #16202C text */
```

Best for: Node Tree, Logo Grid, Directory Map.

---

## House 3 — Terminal

BDOS. Monospace everywhere, terminal green, mac window chrome. Only works when the
content is genuinely developer-facing.

```css
--bg:      #0D0D0D;
--chrome:  #1A1A1A;
--ink:     #E8E8E8;
--muted:   #7A7A7A;
--accent:  #8BE04E;
--accent-bg: rgba(139,224,78,.07);
--dot-red:#FF5F57; --dot-amber:#FEBC2E; --dot-green:#28C840;
```

Everything is `--mono`. One proportional font breaks the illusion.

Best for: Terminal Card only.

---

## House 4 — Editorial Card

Prospeo, HeyOz. Cream ground, serif card titles, saturated accent borders, one mascot
colour per card.

```css
--bg:          #FAF7F2;
--card:        #FFFFFF;
--ink:         #1A2333;
--ink-2:       #2B3540;   /* body copy */
--muted:       #6A7385;
--accent:      #E2552B;   /* fills and borders only */
--accent-deep: #A03318;   /* accent-coloured text */
--border:      2px solid var(--accent);

/* mascot palette — one per card, never reuse within a grid */
--m1:#E2552B; --m2:#5E8B5A; --m3:#3D7EA6;
--m4:#D4A72C; --m5:#B33D3D; --m6:#7B5EA7;
--m7:#2E9E9E; --m8:#3B6B3B; --m9:#2C3E70;
```

Best for: Trading Card Grid, Pipeline Stages, Character Flowchart.

---

## Type scale

Sizes are in artboard px at 1080 wide. The right-hand column is the effective size at
LinkedIn's ~350px feed width, which is the number that decides legibility.

| Role | Size | Weight | Tracking | At 350px |
|---|---|---|---|---|
| Headline | 56–72 | 700 | -0.018em | 18–23 |
| Headline line 2 | 44–56 | 500–600 | -0.015em | 14–18 |
| Subline | 19–22 | 500–600 | 0 | 6–7 |
| Section header | 12–13 | 800 | 0.14em, caps | 4 |
| Card title | 17–20 | 700 | 0 | 6 |
| Card body | 14–15 | 500–600 | 0 | 4.5 |
| Pill / chip | 13–15 | 600 | 0 | 4.5 |
| Micro label | 10–11 | 800 | 0.11em, caps | 3.5 |
| Footer name | 15 | 800 | 0.09em, caps | 5 |

The micro labels are unreadable in feed by design. They exist for the reader who taps
in. Every piece of information that must land in feed lives in the headline, the
section headers, and the card titles.

**The 22px floor** applies to anything load-bearing. `check_render.py` flags everything
below it; you decide which flags are acceptable.

## Contrast floor, every house

Contrast is a token-level constraint, not a final-pass styling preference. Before using a
foreground/background pair, calculate WCAG relative luminance and the contrast ratio:

```text
L = 0.2126 R + 0.7152 G + 0.0722 B
contrast = (Llighter + 0.05) / (Ldarker + 0.05)
```

Convert each sRGB channel to linear light first: divide by `12.92` when the channel is at
or below `0.04045`; otherwise use `((c + 0.055) / 1.055) ** 2.4`.

```python
def relative_luminance(hex_color: str) -> float:
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [
        c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        for c in rgb
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    a = relative_luminance(foreground)
    b = relative_luminance(background)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)
```

Minimums:

- Text under 24px: **4.5:1**, with body-role text at **500 weight or heavier**.
- Borders, badge outlines, and state-defining fills: **3:1** against the adjacent colour.

Two recurring failures:

1. **Raw accent used as text.** `--accent` is for fills, borders, and active state. When
   accent colour carries text, use that house's `--accent-deep` and verify the pair.
2. **Muted text placed on line-colour fills.** `--muted` is a foreground token and `--line`
   is a boundary token. An inactive badge should use `--paper` or a wash as its fill and
   `--muted`, `--ink-2`, or `--ink` for text. If a line-colour fill is unavoidable, verify
   the actual pair instead of assuming the token names make it safe.

## Spacing scale

```
4  8  12  16  20  24  32  40  48  60  80
```

- Artboard margin: 60 left/right, 54 top, footer 78 tall
- Card padding: 18–26
- Gap between grid cards: 14
- Gap between major sections: 34–40
- Border radius: 12 (cards), 14 (panels), 999 (pills)

## Accent discipline

The accent colour appears in exactly four places:

1. One word in the headline
2. Numbered badges
3. The active state of whatever animates
4. The CTA element, if there is one

Everywhere else is ink, muted, or line. The category colours (green/amber/purple/blue)
are for **labels only**, never for fills larger than a chip. The moment a second colour
gets a large fill, the accent stops reading as the accent.

House 0 extends this rather than breaking it: its nine section hues are static identity
and are allowed header strips and panel washes, while the terracotta stays the only
colour that ever changes between frames. See the tier table in House 0.
