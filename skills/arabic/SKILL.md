---
name: arabic
description: Produce Arabic or bilingual LinkedIn infographic copy and layout with native RTL reading order, bidi-safe technical terms, Arabic-aware typography, and evidence-safe hooks.
---

# Arabic and bilingual output

## Purpose

Adapt an approved infographic story and caption for Arabic or mixed Arabic-English use without treating the work as word-for-word translation. Preserve meaning, evidence, hierarchy, and native reading behavior.

Read `helper/GUIDE.md` first. Arabic/RTL is a conditional route that changes copy, typography, reading order, motion direction, and alignment decisions.

## Use when

Use for Arabic briefs, Arabic captions, bilingual posts, RTL artboards, or any story that mixes Arabic with LTR technical terms such as product names, commands, acronyms, or version strings.

## Inputs

- approved source/evidence and story direction
- Arabic source copy or approved meaning to adapt
- product/brand spellings that must remain exact
- selected Story House and layout when already resolved
- numeral preference when the brief requires one
- static or animated output mode

## Outputs

Return Arabic/bilingual copy, RTL layout instructions, bidi-isolation notes for LTR technical terms, numeral decision, typography adjustments, and any evidence/meaning issue to the parent workflow.

## Procedure

1. Read `references/arabic-rtl.md` in full.
2. Preserve the source meaning and protected facts before rewriting for Arabic rhythm.
3. Mirror reading order where sequence or hierarchy depends on direction. Do not mechanically mirror product UI or diagrams whose native direction is part of the evidence.
4. Use Arabic-aware type sizing and leading. Arabic usually needs more vertical breathing room and may need a larger optical size than the English equivalent.
5. Pick one numeral convention and hold it across the artifact unless the evidence itself contains a different literal number format.
6. Isolate English product names, commands, acronyms, version strings, URLs, and code so punctuation does not jump in RTL runs.
7. Apply `hooked-design-copy` to the Arabic hero/opening when the slot is attention-bearing. Use natural Arabic framing, not literal translation of an English hook.
8. Preserve `center-first` as the default composition, but Arabic/RTL reading flow is an explicit alignment exception when centered treatment reduces comprehension.
9. Recheck the mobile truncation cut and feed-width typography after adaptation.

## HOLD conditions

Return a HOLD when a protected product/brand spelling is unknown, a factual hook cannot be preserved truthfully in Arabic, a bilingual UI state would require inventing untranslated product behavior, or the chosen numeral/terminology convention is genuinely ambiguous and materially affects the artifact.

## Related components

- routing authority: `helper/GUIDE.md`
- caption rules: `skills/caption/SKILL.md`
- design copy hooks: `skills/info-stories/references/hook-driven-design-copy.md`
- Arabic reference: `references/arabic-rtl.md`
- full parent workflow: `skills/new-post/SKILL.md`

## Research gates

When active in the route, apply `prose-specificity`, `voice-preservation`, and `evidence-traceability`. Arabic adaptation may change rhythm and phrasing, but it may not erase specific facts or create unsupported emphasis.
