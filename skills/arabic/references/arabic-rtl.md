# Arabic and RTL Adaptation

Producing the Arabic version is not a translation pass over the English artboard. The
layout mirrors, the type scale changes, the caption rhythm changes, and mixed-script
runs need explicit handling or they render in the wrong order.

## Contents

- [Artboard mirroring](#artboard-mirroring)
- [Type](#type)
- [Mixed-script runs](#mixed-script-runs)
- [Numerals](#numerals)
- [Animation direction](#animation-direction)
- [Caption differences](#caption-differences)
- [Dialect](#dialect)
- [Banned patterns in Arabic](#banned-patterns-in-arabic)
- [QA additions for RTL](#qa-additions-for-rtl)

---

## Artboard mirroring

```html
<div id="artboard" dir="rtl" lang="ar">
```

Setting `dir="rtl"` on the artboard root flips the CSS logical properties. That is why
the templates use logical properties throughout. If you write physical properties, the
mirror breaks.

| Use | Not |
|---|---|
| `padding-inline-start` | `padding-left` |
| `margin-inline-end` | `margin-right` |
| `border-inline-start` | `border-left` |
| `inset-inline-start` | `left` |
| `text-align: start` | `text-align: left` |

Things that must **not** mirror:

- Logos and brand wordmarks
- Code blocks, file paths, terminal output, URLs
- Anything inside a Terminal Card
- Chart axes where the data has a natural left-to-right time order
- Numbers in a benchmark bar chart

Wrap those in `dir="ltr"`:

```html
<code dir="ltr">~/.claude/skills/</code>
<div class="terminal" dir="ltr">…</div>
```

### SVG wires do not mirror

`dir="rtl"` has no effect on SVG path coordinates. If the layout mirrors, the wires
will point the wrong way and connect to nothing. Two options:

```css
/* Option A: flip the whole SVG layer */
[dir="rtl"] .wires { transform: scaleX(-1); }
```

Option A is fine for symmetrical converging diagrams. For asymmetric paths, rewrite the
`d` attributes with `x' = 1080 - x`. Then re-measure with the snippet in
`references/production-pipeline.md` and confirm the endpoints land on the new card
centres.

Particles travelling a flipped path keep their direction relative to the path, so an
`animateMotion` on a mirrored wire automatically flows right-to-left. That is correct.

---

## Type

Arabic needs more vertical room and reads smaller at the same nominal size.

```css
[lang="ar"] {
  font-family: "SF Arabic", "Segoe UI", "Noto Naskh Arabic", "Dubai",
               "Geeza Pro", Tahoma, sans-serif;
  line-height: 1.65;        /* vs 1.42 for Latin */
  letter-spacing: 0;        /* never letterspace Arabic, it breaks the joins */
  font-feature-settings: "liga" 1, "calt" 1;
}
```

### Rules

- **No letter-spacing, ever.** It disconnects the glyph joins and the text becomes
  unreadable to a native reader while looking merely "airy" to a non-reader.
- **No fake bold.** `font-weight: 700` on a face without a real bold produces synthetic
  bolding that smears the joins. Use a real weight or use colour for emphasis.
- **No all-caps.** Arabic has no case. `text-transform: uppercase` does nothing to
  Arabic and will silently uppercase any Latin mixed into the same run.
- **Size up one step.** Arabic at 15px reads like Latin at 13px. Add roughly 10–12%.
- **Leading up.** Arabic ascenders and descenders are taller. 1.6–1.7 line-height.

### Adjusted type scale

| Role | Latin | Arabic |
|---|---|---|
| Headline | 60 | 56 (Arabic runs wider; drop the size, raise the leading) |
| Subline | 20 | 22 |
| Card title | 18 | 20 |
| Card body | 14 | 16 |
| Micro label | 10 | 12 |

The headline is the one place Arabic goes *down*, because the same sentence occupies
more horizontal space and will wrap badly at 60px in a 960px column. Write shorter
Arabic headlines rather than shrinking the type further.

---

## Mixed-script runs

Almost every post in this niche mixes Arabic prose with English technical terms. Left
alone, the bidi algorithm produces confusing results with punctuation and adjacent
numbers.

```html
<!-- Right: the Latin term is isolated -->
<p>الـ <bdi dir="ltr">Claude Code</bdi> بيشتغل كـ <bdi dir="ltr">GTM operator</bdi>.</p>

<!-- Also right, for a whole element -->
<code dir="ltr" style="unicode-bidi:isolate">/prompt-master</code>
```

`<bdi>` is the correct element. `unicode-bidi: isolate` on a span does the same job in
CSS. Without isolation, a trailing period or a bracket after an English term jumps to
the wrong side of the phrase.

Terms to always isolate: product names, commands, file paths, URLs, version numbers,
metric units, hashtags.

---

## Numerals

Two systems, and mixing them inside one artboard looks broken.

| | Western | Eastern Arabic |
|---|---|---|
| Glyphs | 0123456789 | ٠١٢٣٤٥٦٧٨٩ |
| Used in | Gulf, Egypt (business and tech contexts), all of LinkedIn | Formal print, Quranic, some Levant editorial |

**Default to Western numerals.** Every Arabic-language business post in the reference
niche uses them, and every metric, percentage, price, and version number the reader
already knows is written that way.

Force it if a font substitutes automatically:

```css
[lang="ar"] { font-feature-settings: "lnum" 1; }
```

Percentages, currency, and dates keep their Latin ordering:

```html
<bdi dir="ltr">1.8% → 4.3%</bdi>
<bdi dir="ltr">$7M ARR</bdi>
```

Without the isolation, `1.8% → 4.3%` renders with the arrow pointing the wrong way
inside an RTL paragraph.

---

## Animation direction

A Sequential Highlight in an RTL layout must run **right to left**, following the
reading order. The DOM order does not change — `dir="rtl"` reverses the visual order of
the grid — so `nth-child(1)` is now the rightmost box, and the reverse-delay formula in
`animation-recipes.md` still applies unchanged.

Verify it. Capture at `t = 0, loop/4, loop/2, 3×loop/4` and confirm the highlight starts
on the right.

Path particles converging on a synthesiser are direction-neutral. Orbit animations
should reverse to counter-clockwise for RTL, which reads as "forward":

```css
[dir="rtl"] .orbiter { animation-direction: reverse; }
```

Typewriter animations need the caret on the left:

```css
[dir="rtl"] .type { border-right: 0; border-left: 3px solid var(--accent); }
```

---

## Caption differences

Arabic LinkedIn captions do not behave like English ones.

**Longer lines survive.** English captions break at 6–9 words. Arabic reads comfortably
at 10–14 words per line because the script is denser. Forcing English line lengths onto
Arabic produces a caption that looks chopped.

**The truncation cut is shorter in words.** LinkedIn counts characters, and Arabic packs
more meaning per character, so the visible pre-truncation zone actually carries *more*
content. Line 1 can be a full thought rather than a fragment.

**Numbers still lead.** `من 1.8% لـ 4.3% في شهرين` works exactly as well as the English
equivalent, and the Western numerals give the eye an anchor in the block of script.

**English terms stay English.** Do not translate `Paid Media`, `funnel`, `landing page`,
`lead`, `dashboard`, `retargeting`, `conversion rate`. The audience uses the English
term. Translating it signals that the writer is not in the industry.

Correct: `الـ funnel كله بيقع في الخطوة دي.`
Wrong: `مسار التحويل كله يقع في هذه الخطوة.`

**Punctuation.** Use Arabic comma `،` and Arabic question mark `؟`. Keep the Latin period
`.` — the Arabic full stop is not used in modern digital Arabic.

**Emoji and glyph bullets** work identically. `→` in an RTL paragraph will visually
render as pointing left, which is correct. If you need it to point right, isolate it.

---

## Dialect

Match the market. The reference posts that perform in the Gulf and Egypt are written in
dialect, not Modern Standard Arabic. MSA reads as a press release.

| Market | Register | Marker words |
|---|---|---|
| Egypt | Egyptian colloquial | ده، دي، بيشتغل، عشان، كده، إزاي |
| Saudi / Gulf | Light Gulf, close to white dialect | هذا، يشتغل، عشان، كذا، كيف |
| UAE / Qatar | White dialect, more MSA-leaning | leans formal, keeps English terms |
| Pan-Arab | White dialect | avoid strong Egyptian or Gulf markers |

One dialect per post. Mixing Egyptian `ده` with Gulf `كذا` in the same caption is the
single most obvious tell that the text was machine-assembled.

**On the artboard**, lean more formal than the caption. The visual is a reference
artefact and gets saved and reshared. White dialect or light MSA on the visual, full
dialect in the caption, is the combination that works.

---

## Banned patterns in Arabic

The denial-then-reveal construction is even more conspicuous in Arabic than English
because it does not occur in natural Arabic business writing at all. It is a direct
calque from English ad copy.

Never write:

- `ده مش X. ده Y.`
- `دي مش مجرد X، دي Y.`
- `هذا ليس X، بل Y.`
- `ليس فقط X بل Y.`
- `لا نتحدث عن X، نحن نتحدث عن Y.`

Write the thing directly:

- Instead of `ده مش dashboard، ده غرفة تحكم` →
  `الداشبورد بتجمع المؤشرات اللي بتخليك تاخد قرار أسرع.`
- Instead of `مش مجرد إعلان، دي ماكينة طلبات` →
  `الإعلان ده معمول عشان يجيب طلبات قابلة للقياس.`

Also avoid in Arabic:

- `في عالم اليوم السريع` and any variant of the hedged opener
- `دعنا نتعمق` / `خلينا نغوص`
- Chains of rhetorical questions before the CTA
- The em dash `—`. Arabic typography does not use it; use a period and a line break.

---

## QA additions for RTL

Beyond the standard gates in `qa-gates.md`:

1. **Join integrity.** Zoom to 200% and check that no Arabic word has broken joins.
   Broken joins mean a font substitution happened mid-render or letter-spacing leaked in.
2. **Mixed-run order.** Read every line containing an English term out loud. If the
   punctuation or the term lands on the wrong side, add `<bdi>`.
3. **Wire alignment.** After mirroring, re-measure the endpoints. This is the most
   common RTL failure and it is invisible until you look at the still at full size.
4. **Numeral consistency.** One system across the whole artboard.
5. **Highlight direction.** Confirm the Sequential Highlight starts on the right.
6. **Native read.** Have a native speaker of the target dialect read the caption. Not a
   speaker of a different dialect. The markers are the whole point.

## Bilingual output

Producing an English and an Arabic version of the same post is worth it when the
audience spans both. Two working approaches:

**Two artboards, one design.** Same layout, two HTML files, two GIFs, two posts. Post
them 48 hours apart, not on the same day. This is the recommended approach.

**One artboard, split.** Arabic headline, English technical labels. Works only for the
Terminal Card and Directory Map archetypes where the content is genuinely code-like.
Do not attempt it for prose-heavy archetypes; the result reads as unfinished in both
languages.
