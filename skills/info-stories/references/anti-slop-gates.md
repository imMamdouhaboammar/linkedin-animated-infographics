# Anti-slop gates

These gates apply to visible infographic copy: title, subline, card body, labels, CTA, caption, and explanatory annotations. They diagnose patterns, not authorship.

## Protect before editing

Record names, numbers, mechanisms, product terms, qualifications, source claims, and any sentence whose wording is part of the author's recognisable voice. Compression is not permission to generalise a fact.

## Mechanical scan

Run `detect_copy_slop()` from `scripts/info_stories.py` or apply the same named checks manually.

Fail or revise when a load-bearing copy slot contains:

- **Throat-clearing:** setup such as "here's the thing" or "let's be clear" before the actual point
- **Binary contrast:** formulaic negative setup plus positive reveal framing (e.g., "not X, it's Y", "not a... but a...", "this is not... this is...", "ده مش ... ده ...", "هذا ليس ... بل ...", "مش مجرد ... لكنه ...", "الفرق مش ...")
- **Forbidden terminology:** terms like `system`, `systems`, `layer`, `layers`, `machine`, `machines`, `gear`, `gears`, `occupy`, `difference`, or Arabic equivalents (`نظام`, `سيستم`, `طبقة`, `طبقات`, `ماكينة`, `ترس`, `احتلال`, `الفرق`)
- **Faux insight:** "the deeper truth" or "what most people get wrong" without a concrete mechanism
- **Importance puffery:** claims such as "changes everything" or generic superlatives
- **Recap ending:** an ending that repeats the poster instead of giving the reader a next action
- **Rhetorical setup:** a question whose only job is to delay the answer
- **Dash crutch:** em/en dash (`—`, `–`) used as sentence glue in final visible copy
- **Trailing punctuation:** period marks at the end of titles, cards, or bullet items

## Direct declaration protocol

When structuring copy for products, tools, and visual cards, apply the four-part sequence:
1. Explicit Definition: Say what the thing is directly
2. Target Role: Say who it serves
3. Operational Context: Say when it is used
4. Practical Outcome: Say what decision or action it enables

## Human judgement gates

- **Portability:** could the sentence move unchanged to another product or creator? If yes, make it specific or cut it
- **Evidence:** does a claim become stronger than its source after compression? If yes, restore the qualification
- **Voice:** did the edit remove a useful irregularity just to make every card sound the same? If yes, restore the voice
- **Rhythm:** do three adjacent cards start or end with the same sentence shape? If yes, vary structure rather than synonym-cycling
- **Density:** if a card needs two paragraphs, split the information architecture instead of shrinking type

## Detect mode

When asked only to diagnose, return `slot`, `pattern`, `evidence`, and `fix direction`. Do not rewrite without permission.

## Edit mode

Make the minimum effective edit. Never invent an example, metric, testimonial, or mechanism to make a weak line sound more specific.

