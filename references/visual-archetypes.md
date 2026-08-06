# Visual Archetypes

Twelve layout families, reverse-engineered from the reference set. Each entry gives the
structural spec, the content shape it fits, what to animate, and the failure mode.

All specs assume a **1080 x 1350** artboard (4:5, LinkedIn's tallest in-feed image).
The Cheat Sheet Poster is the exception and runs taller.

## Shared frame

Every archetype in the set shares the same outer frame:

```
┌─ 48–64px margin ──────────────────────────────┐
│  EYEBROW           (10–12px, letterspaced,    │
│                     uppercase, muted)         │
│  HEADLINE          (52–72px, one accent word) │
│  SUBLINE           (18–22px, muted)           │
│                                               │
│  ── content zone ──────────────────────────   │
│                                               │
│  ── content zone ──────────────────────────   │
│                                               │
├───────────────────────────────────────────────┤
│  avatar + NAME · handle/url    (footer bar)   │
└───────────────────────────────────────────────┘
```

Rules that hold across all twelve:

- **One accent colour**, used on: one word in the headline, the numbered badges, and
  the active state of whatever animates. Nowhere else.
- **Two type families maximum.** A display face for the headline, a monospace or grotesk
  for everything technical.
- **Footer attribution is mandatory.** Avatar, name, one URL. These images get reposted
  stripped of the caption; the footer is the only thing that survives.
- **Nothing in the outer margin moves.**

---

## 1. Directory Map

**Content shape:** a hierarchy of files, modules, or skills.
**Reference:** DRIP `.cro-bundle/ fully mapped` — 10 skills + 5 agents.

### Structure

```
folder-icon  root-name/
└── folder/                    ┈┈┈┈┈┈┈┈▸  [ pill: summary ]
    ├── 📄 item-name           ┈┈┈┈┈┈┈┈▸  [ pill: what it does ]
    ├── 📄 item-name           ┈┈┈┈┈┈┈┈▸  [ pill ]
    └── 📄 item-name           ┈┈┈┈┈┈┈┈▸  [ pill ]
```

- Monospace throughout, 20–24px, tree glyphs `├── └── │` as literal characters
- Left column: the tree, left-aligned at a fixed indent of 36px per level
- Right column: pills, **right-aligned to a common edge** so the ragged left creates
  the visual rhythm
- Dotted leader `┈┈┈▸` connects the two columns
- Each group gets its own pill colour, pastel on dark or saturated on light
- Group headers carry a `(N)` count

### Animate

Sequential highlight walking down the tree, one item at a time, 400ms dwell. Or a
staggered fade-in of the pills only, left column static.

### Fails when

More than 20 leaf items. The tree becomes a wall. Split into two posts.

---

## 2. Flow Map + Verdict

**Content shape:** many inputs converging on one synthesised output.
**Reference:** Charlie Hills `How to build a board of AI advisers`.

### Structure

```
[ SETUP ROW: 4 numbered boxes, equal width, connected by ›  ]

              [ the question, in a rounded pill ]
                          │
        ┌────────┬────────┼────────┬────────┐   ← curved bezier connectors
      [card]   [card]   [card]   [card]         ← 4 persona/input cards
        └────────┴────────┼────────┴────────┘   ← curves converging
                   [ THE SYNTHESISER ]
                          │
┌──────────────────────────────────────────────┐
│ VERDICT PANEL — 2x2 labelled quadrants        │
│ + a single full-width "first move" line       │
└──────────────────────────────────────────────┘

[ invoke it:  chip   chip   chip ]
```

- Setup row boxes: 1px border, number badge in accent circle top-left
- Connectors: SVG cubic beziers, 2px, each a different pastel, low opacity
- Cards: avatar circle 44px, name bold, role in accent caps 10px, quote in italic
- Verdict panel quadrants: coloured label caps + body with **selective bolding**
  of the payoff clause
- A faint oversized brand glyph watermark sits behind the convergence point

### Animate

This is the reference GIF. Two primitives only:
1. Accent outline steps through the 4 setup boxes, ~900ms each
2. Dots travel down each bezier from card to synthesiser, staggered

30 frames at 8.3 fps, 3.6s.

### Fails when

More than 5 input cards. The convergence angle gets too shallow to read.

---

## 3. Orbit Cycle

**Content shape:** a cyclical process where no stage is "first".
**Reference:** FullEnrich `Claude code /newpage` — 5 agents around a screenshot.

### Structure

```
        [ Node 5 ]        CENTRE TITLE        [ Node 1 ]
              ╲          [ centre glyph ]         ╱
               ○ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ ○
              ╱     [ centre artifact:        ╲
        [ Node 4 ]     product screenshot ]   [ Node 2 ]
               ○ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ ○
                          [ Node 3 ]
```

- 5–6 nodes evenly spaced on a circle, radius ~380px
- Each node: a badge pill (`Agent-N`) + bold title + 3–4 lines of description
- Node markers sit **on** the circle path as white circles with a mascot/icon inside
- The circle itself is a dashed stroke that becomes solid as the animation runs
- An output artifact sits outside the ring with a solid arrow pointing to it

### Animate

Reference GIF, 230 frames at 30 fps, 7.67s:
1. Node markers travel around the dashed circle using `offset-path`
2. The circle strokes itself solid via `stroke-dashoffset`
3. The output arrow reveals last

### Fails when

Node descriptions exceed 4 lines. They collide with neighbours at the diagonals.

---

## 4. Pipeline Stages

**Content shape:** a linear process, 4–6 stages, each with sub-items.
**Reference:** HeyOz `AI Creative Framework`.

### Structure

```
[ eyebrow chip ]
HEADLINE with accent phrase
[ ⚡ claim ]  |  [ 📈 claim ]

        [ product UI mock, centred, with a real prompt in it ]
                          ↓
                  [ ROLE LABEL ]
   ┌──────┬──────┬──────┬──────┬──────┐
   │ 1.   │ 2.   │ 3.   │ 4.   │ 5.   │  ← stage cards, each a different
   │ NAME │ NAME │ NAME │ NAME │ NAME │    border colour
   │ ☑ …  │ ☑ …  │ ☑ …  │ ☑ …  │ ☑ …  │  ← 4 checklist rows each
   │  ●   │  ●   │  ●   │  ●   │  ●   │  ← coloured icon circle
   └──────┴──────┴──────┴──────┴──────┘
   [ output ][ output ][ output ][ output ]  ← real sample outputs
   platform   platform  platform  platform    ← platform logos
   ┌────────────────────────────────────┐
   │ offer + CTA        │  author card  │
   └────────────────────────────────────┘
```

- Stage cards: numbered, coloured 1px border matching the icon circle
- Arrows between cards, `→`, small and muted
- The output row underneath is what sells it — real artefacts, not placeholders

### Animate

Accent sweep left to right across the stage cards, checklist ticks appearing in
sequence within the active card.

### Fails when

Sample outputs are obviously fake. This archetype lives on the output row being real.

---

## 5. Logo Grid

**Content shape:** a flat catalogue of tools with no hierarchy.
**Reference:** navreo `1,000+ connectors. One Claude Code system.`

### Structure

```
BRAND WORDMARK                                        [ mascot ]

HEADLINE line one
HEADLINE line two in accent
subline, 2 lines, with 3 bolded keywords

● COL A HEADER  (08)   ● COL B HEADER  (08)   ● COL C HEADER  (08)
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ [logo] Name   │      │ [logo] Name   │      │ [logo] Name   │
│        tagline│      │        tagline│      │        tagline│
└───────────────┘      └───────────────┘      └───────────────┘
   × 8 rows               × 8 rows               × 8 rows

              muted one-line positioning statement
```

- 3 columns × 8 rows = 24 cells. Column headers carry a dot in accent + a count badge
- Each cell: 40px logo tile, name 17px semibold, tagline 13px muted
- Dark background makes the logos pop. This archetype rarely works on light

### Animate

Staggered fade+rise of cells, column by column. Keep total under 2s or it drags.

### Fails when

Logos have inconsistent padding. Normalise every logo into a 40px rounded tile first.

---

## 6. Trading Card Grid

**Content shape:** N independent items of equal weight, 6–9 of them.
**Reference:** Prospeo `Signal-Based Outbound Playbook`.

### Structure

```
[01 FOUNDATION]        BRAND MARKS          [02 MARKET INTEL]
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│  [mascot]    │    │  CENTRE TITLE │    │  [mascot]    │
│  SKILL /name │    │  SUBTITLE     │    │  SKILL /name │
│  Card Title  │    │  one-line     │    │  Card Title  │
│  desc line   │    │  promise      │    │  desc line   │
│ RUNS ON [pill]│   └───────────────┘    │ RUNS ON [pill]│
└──────────────┘                          └──────────────┘

┌──────┬──────┬──────┬──────┐    ← row of 4
┌───────┬───────┬───────┐        ← row of 3
      [ closing italic line ]
[ chip ][ chip ][ chip ]  [ CTA button ]
```

- Cards: 2px accent border, number badge in a filled corner tab with a category label
- Each card carries a distinctly coloured mascot — colour is the only differentiator
- Serif display for card titles gives this family its editorial feel
- Bottom row: 3 attribute chips + one filled CTA button with an arrow

### Animate

Cards flip or scale-in in reading order. Or one accent glow travelling card to card.

### Fails when

Mascots are all the same colour. The whole grid flattens.

---

## 7. Node Tree

**Content shape:** a branching dependency or capability graph.
**Reference:** Priyanka `Claude Code for GTM Engineers`.

### Structure

```
     DISPLAY HEADLINE (pixel/condensed face)
     Sub-headline, three lines, accent on line 3

              ┌────────────────────┐
              │ [logos] ROOT NODE  │   ← glowing card
              │        [ pill ]    │
              └─────────┬──────────┘
        ┌───────────────┼───────────────┐   ← dashed orthogonal connectors
   ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
   │ [icon]  │     │ [icon]  │     │ [icon]  │
   │ Name    │     │ Name    │     │ Name    │
   │ [pill]  │     │ [pill]  │     │ [pill]  │
   └────┬────┘     └────┬────┘     └────┬────┘
   ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
   │ leaf    │     │ leaf    │     │ leaf    │
   └─────────┘     └─────────┘     └─────────┘

   ┌═══════ FULL WIDTH BANNER ═══════┐
   ┌─────────────────┬───────────────┐
   │ What You'll     │ N Core        │
   │ Build           │ Workflows     │
   │ • item + desc   │ • item + desc │
   └─────────────────┴───────────────┘
```

- Near-black background with a subtle noise or grid texture
- Every card has an outer accent glow (`box-shadow: 0 0 40px rgba(accent,.18)`)
- Icon tiles are cream-coloured squares — the only light elements, so they lead the eye
- Connectors are dashed 1px, low opacity

### Animate

Glow pulse cascading root → branches → leaves. Or dashes flowing along the connectors
via `stroke-dashoffset`.

### Fails when

Glow is applied to everything. Glow only the active tier.

---

## 8. Terminal Card

**Content shape:** a single tool, integration, or announcement.
**Reference:** BDOS `Google Ads + Claude Code`.

### Structure

```
┌─ ● ● ●          window-title          ─┐
│                                        │
│  → the one-line positioning            │
│                                        │
│      [LOGO A]     +     [LOGO B]       │
│       Name             Name            │
│       sublabel         sublabel        │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ 📩 FREE GUIDE                    │  │
│  │ The offer, large                 │  │
│  │ the qualifier, smaller           │  │
│  └──────────────────────────────────┘  │
│                                        │
│  >>> domain.com                        │
└────────────────────────────────────────┘
```

- Monospace everywhere. Near-black `#0D0D0D`, terminal green `#8BE04E` accent
- Mac window chrome dots at 14px in the classic red/amber/green
- The CTA box is a 2px accent-bordered rectangle with a transparent tinted fill
- `>>>` prompt prefix on the domain line

### Animate

Typewriter reveal on the positioning line and the domain. Blinking cursor block.
Optionally a soft pulse on the CTA border.

### Fails when

Anything is not monospace. One proportional font breaks the illusion.

---

## 9. Cheat Sheet Poster

**Content shape:** dense reference material meant to be saved and zoomed.
**Reference:** ColdIQ `How to run multichannel outreach like the top 1%`.

### Structure

A 3-column masonry of 9 numbered panels, each with its own pastel section colour, on a
textured off-white ground. Runs taller than 4:5 — around 1280 x 1900.

```
      [ avatar + author pill ]
  HEADLINE with accent tail
  [chip] [chip] [chip] [chip]

┌─ 1 Panel ─┐ ┌─ 2 Panel ─┐ ┌─ 3 Panel ─┐
│ mixed     │ │ a flow    │ │ bullet    │
│ content   │ │ diagram   │ │ list      │
└───────────┘ └───────────┘ └───────────┘
┌─ 4 ───────┐ ┌─ 5 ───────┐ ┌─ 6 ───────┐
└───────────┘ └───────────┘ └───────────┘
┌─ 7 ─────────────┐ ┌─ 8 ─────────────┐
└─────────────────┘ └─────────────────┘
┌─ 9 full width ───────────────────────┐
└──────────────────────────────────────┘
```

- Numbered square badge, filled, top-left of each panel header bar
- Panel header bar takes the section colour at ~35% tint; body is white
- Mixed content types inside panels: mini-flows, chip rows, checklists, quote blocks

### Animate

Barely. One accent sweep through the panel numbers, 300ms each. This archetype is for
saving, and saving happens on the still frame.

### Fails when

Body text drops below 22px. At 350px feed width this becomes an unreadable texture —
which is acceptable only if the caption explicitly says "save and zoom".

---

## 10. Spec Sheet

**Content shape:** a benchmark, timeline, or versioned comparison plus use cases.
**Reference:** Charlie Hills `Fable 5: The Complete Guide`.

### Structure

```
[ decorative numeral ]  HEADLINE: Accent Subtitle
                        subline · url

┌── BAR CHART PANEL ──────┐  ┌── TIMELINE PANEL ────────────┐
│ Label ████████ 95.0%    │  │ ●────●────●────◉             │
│ Label ████     88.6%    │  │ date date date date          │
│ Label ███      85.2%    │  │ ┌──────────┐ ┌────────────┐  │
└─────────────────────────┘  │ │ variant A│ │ variant B  │  │
                             │ └──────────┘ └────────────┘  │
                             └──────────────────────────────┘
TOP N USE CASES
┌ 01 │ Title                                    ┌─────────┐ ┐
│      one-line description                     │ mini    │ │
│    ┌──────────────────────────────────────┐   │ visual  │ │
│    │ monospace prompt with [PLACEHOLDERS] │   └─────────┘ │
│    └──────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────┘
   × 5
```

- Numbered use-case cards, each with a coloured index chip, a monospace code block, and
  a small abstract mini-illustration on the right
- Placeholders in the code blocks rendered in accent `[X]` — this is what makes people
  screenshot it
- Grid-paper background texture at very low opacity

### Animate

Bars growing from zero. Timeline dot travelling left to right. Nothing else.

### Fails when

The code blocks are not literally copy-pasteable. This archetype's entire value is that
the reader can use the text directly.

---

## 11. Annotated Blueprint

**Content shape:** N items, each with sub-attributes, connected to a spine.
**Reference:** Ruben Hassid `The 3 Claude Skills to Replace 500+ Prompts`.

### Structure

```
 HEADLINE in serif display
 with an underlined accent phrase
 │
 ├─[01]─ SECTION LABEL
 │       ┌──────────┐   ┌──────────┐   ┌───────────────────┐
 │       │ the name │───│ What it  │───│ → attribute       │
 │       └──────────┘   │ is:      │   ├───────────────────┤
 │       ┌──────────┐   └──────────┘   │ → attribute       │
 │       │ How to   │                  ├───────────────────┤
 │       │ create:  │                  │ → attribute       │
 │       └──────────┘                  └───────────────────┘
 ├─[02]─ ...
 └─[03]─ ...
```

- A single vertical accent spine on the left, branching orthogonally into each section
- Alternating dark boxes (definitions) and accent-tinted boxes (attributes)
- All connectors are 1.5px orthogonal lines with rounded corners, accent-coloured
- Attribution line bottom-left and bottom-right

### Animate

The spine draws itself top to bottom, branches drawing as it passes each section.
Single continuous 4s draw.

### Fails when

More than 3 top-level sections. The spine runs out of vertical room.

---

## 12. Character Flowchart

**Content shape:** a sequence with optional branches, made friendly.
**Reference:** Ruben Hassid `9 Claude Skills that write your prompts for you`.

### Structure

```
[glyph] HEADLINE IN SERIF DISPLAY
        second line lighter weight

    START
  Messy Idea  ──────▶ ┌──────────┐ ──────┐
   [scribble]         │ [mascot] │       │
                      │ 01. Name │       │
                      │ /command │       │
                      └──────────┘       │
   ┌──────────────────────────────────────┘
   ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ [mascot] │──│ [mascot] │──│ [mascot] │
│ 02. Name │  │ 03. Name │  │ 04. Name │
└──────────┘  └──────────┘  └──────────┘
                                    ... boustrophedon (snake) reading order
                              FINISH
                              Outcome
                              • bullet
```

- Cream ground `#FAF7F2`, cards in off-white with soft rounded corners and no border
- One pixel-art mascot per card, each a different colour, 8-bit style
- Connectors are thick 3px black orthogonal lines with hard 90° corners and arrowheads
- Serif display headline, monospace for the `/command` line, sans for descriptions
- Snake layout: row 1 left-to-right, row 2 right-to-left. Follow the arrows.

### Animate

A token travelling the full path start to finish, cards lighting as it passes.
This is the most engaging animation in the set and the most expensive to build.

### Fails when

Mascots are inconsistent in style. Generate all of them in one pass with one prompt.

---

## 13. Specimen Grid

**Content shape:** a catalogue of N capabilities where each one can be *shown* rather
than described.
**Reference:** Charlie Hills `Every Motion Claude Can Make` — 42 motion types.

The most demanding archetype in the set and the highest-ceiling one. Each cell contains
a working miniature of the thing it names. The reader does not read a list of features,
they watch 42 of them run at once.

### Structure

```
[glyph]  HEADLINE with one accent word
         N types. One install. Free.
● Cat A  ● Cat B  ● Cat C  ● Cat D  ● Cat E     ← legend, dot per category

┌─────────────┬──────┬──────┬──────┬──────┐    ← variable-width masonry
│   SPECIMEN  │ spec │ spec │ spec │ spec │      cell width follows the demo,
│   label     │ label│ label│ label│ label│      not a fixed column count
├──────┬──────┼──────┴──┬───┴──┬───┴──┬───┤
│ spec │ spec │ specimen│ spec │ spec │...│
└──────┴──────┴─────────┴──────┴──────┴───┘
   × 8 rows

        [ avatar  NAME · url ]  ← pill-shaped footer
```

- Near-black ground `#081020`, cells one step lighter with a 1px border
- Each cell: the live miniature on top, label bottom-left at 13–15px
- **Cell width varies with the demo.** A bar race needs width, a countdown ring does
  not. Fixed columns waste the space and make the grid read as a spreadsheet
- Category is carried by the **accent colour of the miniature**, matched to the legend
  dot. No category labels on the cells themselves
- Footer is a rounded pill floating on the ground, not a full-width bar

### Animate

Two layers running together:

1. **Ambient Micro-Loops** — every cell runs its own independent loop, continuously
2. **Category Sweep** — a coloured border walks through the cells of one category at a
   time, in legend order, tinted to that category's colour

Reference file: 1080x1350, 120 frames at 20 fps, 6s, 2.5 MB. Roughly 85% of the canvas
is visibly moving and it still encodes at 20 KB a frame, because the ground is dark and
flat and every individual animation is tiny. See the motion budget table in
`animation-recipes.md`.

### Fails when

- The miniatures are static illustrations of motion rather than the motion itself. The
  entire premise is that they run
- The ground is light. On a light textured ground the same grid costs three to four
  times the file size
- Cells are a fixed grid. The variable widths are what make it read as a specimen sheet
  instead of a table
- More than about 45 cells. Below roughly 90x90px a miniature stops being legible

### Build note

Author one cell at a time as an isolated component with its own `--loop` that is an
integer division of the master loop. Forty-two hand-tuned animations is a large build;
budget accordingly and reuse aggressively. Twelve distinct miniatures recoloured across
five categories reads as 42 to anyone scrolling.

## Choosing between adjacent archetypes

| If you're torn between | Pick | Because |
|---|---|---|
| Directory Map vs Trading Card Grid | Directory Map | if the items have a real parent-child structure |
| Node Tree vs Flow Map | Flow Map | if things converge; Node Tree if they diverge |
| Pipeline Stages vs Annotated Blueprint | Pipeline | if the stages are sequential in time |
| Logo Grid vs Trading Card Grid | Logo Grid | if the items are third-party brands |
| Spec Sheet vs Cheat Sheet | Spec Sheet | if there is one hero comparison |
| Character Flowchart vs Orbit Cycle | Orbit | if the process has no beginning |
| Specimen Grid vs Logo Grid | Specimen | if you can *show* each item working |
| Specimen Grid vs Trading Card Grid | Trading Card | if each item needs a sentence of explanation |
