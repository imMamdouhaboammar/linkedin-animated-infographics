# Design Systems

Four house styles observed across the reference set, plus the type stacks that survive
offline rendering and the spacing scale that holds the layouts together.

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

## House 1 — Warm Paper

The most common in the set. Charlie Hills, Ruben Hassid, ColdIQ. Light, editorial,
grid-paper texture, serif headline with one accent word.

```css
--bg:          #FFFFFF;
--paper:       #FDFCFA;   /* card fills, one step off white */
--ink:         #16202C;
--muted:       #6B7787;
--line:        #E3E6EA;
--accent:      #D9744F;   /* terracotta */
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
--bg:      #FAF7F2;
--card:    #FFFFFF;
--ink:     #1A2333;
--muted:   #6A7385;
--accent:  #E2552B;
--border:  2px solid var(--accent);

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
| Headline line 2 | 44–56 | 400–600 | -0.015em | 14–18 |
| Subline | 19–22 | 400 | 0 | 6–7 |
| Section header | 12–13 | 800 | 0.14em, caps | 4 |
| Card title | 17–20 | 700 | 0 | 6 |
| Card body | 14–15 | 400 | 0 | 4.5 |
| Pill / chip | 13–15 | 600 | 0 | 4.5 |
| Micro label | 10–11 | 800 | 0.11em, caps | 3.5 |
| Footer name | 15 | 800 | 0.09em, caps | 5 |

The micro labels are unreadable in feed by design. They exist for the reader who taps
in. Every piece of information that must land in feed lives in the headline, the
section headers, and the card titles.

**The 22px floor** applies to anything load-bearing. `check_render.py` flags everything
below it; you decide which flags are acceptable.

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

## Attribution footer

Mandatory on every artboard. These images get reposted without the caption, and the
footer is the only thing that survives.

```html
<div class="foot">
  <div class="av"></div>
  <span class="nm">YOUR NAME</span>
  <span class="url">· yoursite.com</span>
</div>
```

Dark bar, 78px, full bleed, centred. Or a light variant with a top border. Either way
it must be visually separated from the content zone, and it must never animate.
