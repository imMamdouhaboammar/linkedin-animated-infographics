# Quality Gates

Run these before returning a caption

## Gate 1: Mobile hook

PASS when line 1

- is understandable alone
- contains a real tension, claim, object, or behavior
- earns attention without fake suspense
- is compact enough to survive mobile truncation when practical

FAIL when it begins with generic context or requires line 2 to explain what line 1 means

## Gate 2: Named specificity

PASS when the caption uses real names, mechanisms, categories, commands, metrics, or use cases where available

FAIL when generic nouns such as `tool`, `solution`, `platform`, or `workflow` replace the real thing without a reason

## Gate 3: Mechanism

PASS when the reader can explain what happens

FAIL when the caption only explains how to feel about the product

## Gate 4: Evidence

PASS when every number, benchmark, star count, price, license, compatibility claim, and performance claim is supplied or verified

FAIL when precision was invented to make the post stronger

## Gate 5: Narrative movement

PASS when every section advances the idea

FAIL when the body repeatedly restates the opening tension

## Gate 6: Visual alignment

PASS when caption and visual have distinct communication jobs

FAIL when the caption narrates every frame or describes something that is not present

## Gate 7: First comment

PASS when link-heavy or setup-heavy detail is separated when separation improves readability

FAIL when the first comment merely repeats the post

## Gate 8: Anti-slop

Hard fail on

- generic motivational close
- fake urgency
- empty superlatives
- repeated `not X, but Y` constructions
- mechanical paragraph symmetry
- performative phrases such as `here's the game changer`
- dramatic punctuation with no information
- generic CTA such as `Thoughts?`
- em dash when the active house style forbids it or when a simpler punctuation choice works

## Gate 9: Sayability

Read the caption aloud mentally

If a sentence sounds like it belongs in a brand deck instead of something the writer would actually say, rewrite it

## Gate 10: House style

User-specific rules outrank this Skill

Examples

- banned punctuation
- banned vocabulary
- required dialect
- no terminal periods
- no em dash
- specific capitalization
- preferred code-switching

Treat explicit house-style instructions as hard constraints

## Gate 11: URL integrity

PASS when every supplied URL is preserved exactly unless the user asks to shorten or replace it

FAIL when a link is rewritten, reordered incorrectly, duplicated accidentally, or attached to the wrong item

## Gate 12: Visual claim safety

PASS when the visual is described as an illustration, map, sequence, or example when that is what it is

FAIL when an example visual is described as a client result, benchmark proof, or real product state without evidence

## Release threshold

A caption is ready only when all hard gates pass

Do not ship a draft with a known house-style violation, unsupported claim, wrong URL, wrong product name, or visual mismatch
