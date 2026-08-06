---
name: arabic
description: >-
  Produce the Arabic or bilingual version of a LinkedIn infographic and caption. Use for any
  Arabic or mixed Arabic-English post, artboard, or caption, and whenever a layout needs to
  mirror to RTL. Trigger on "النسخة العربية", "اعملي نسخة بالعربي", "RTL version", "bilingual
  post", or an Arabic brief for a visual. Covers layout mirroring, the numeral system, the
  Arabic type scale, bidi isolation for LTR technical terms, the font stack, and how Arabic
  caption rhythm differs from English.
---

# Arabic and bilingual output

**This is not a translation job.** Running the English artboard through a translator and
flipping `direction: rtl` produces something that reads as a machine artifact to any native
reader, and the type will be visibly too small.

Four things change, and all four are structural:

1. **The layout mirrors.** Reading order runs right to left, so the eyebrow, headline, number
   badges, and dotted leaders all move, and any sequential highlight runs the other way.
2. **The typographic scale changes.** Arabic needs roughly 12% more leading and one size step
   up for the same optical weight. An Arabic headline set at the English size looks thin and
   cramped.
3. **The numeral system is a decision.** Pick one and hold it across the whole artboard.
4. **English technical terms stay LTR inside RTL runs.** `Claude`, `ChatGPT`, `MCP`, `CTR`,
   version strings, and commands need bidi isolation or the punctuation around them jumps to
   the wrong side.

## Caption rhythm

Arabic LinkedIn captions carry longer lines than English ones and break at different points.
The truncation cut still applies but lands at a different character count, so line 1 has to be
measured rather than assumed.

The ban list applies identically in Arabic: no `ده مش X، ده Y`, no `مش مجرد X`, no
`هذا ليس X، بل Y`, no em dashes.

## Full reference

`references/arabic-rtl.md` has the font stack, the bidi isolation markers, the mirrored
spacing scale, and the caption rhythm differences. Read it before producing any Arabic output.
