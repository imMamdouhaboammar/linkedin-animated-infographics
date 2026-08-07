---
name: caption
description: Write or edit evidence-safe LinkedIn captions, opening hooks, CTAs, and first comments using one caption archetype, mobile truncation discipline, and the repository anti-slop rules.
---

# Caption

## Purpose

Write or evaluate the post caption and opening hook without weakening evidence or turning the copy into generic marketing language. Attention-bearing copy should earn the click; literal information should remain literal when clarity is the job.

Read `helper/GUIDE.md` first. For Info-stories, also read `skills/info-stories/references/hook-driven-design-copy.md`.

## Use when

Use for a new caption, hook, opening line, CTA, first comment, caption rewrite, or caption QA. Use the `caption-writer` worker inside the full parent workflow.

## Inputs

- approved facts/evidence
- audience and one primary takeaway
- selected creative concept and story brief when available
- CTA or explicitly CTA-free intent
- language and any brand/voice constraints

## Outputs

Return finished caption copy, first-comment copy when applicable, selected caption archetype, hook mechanism, and any unsupported claim that prevents a safe final version.

## Procedure

1. Read `references/caption-patterns.md` and the active helper gates.
2. Pick one caption archetype and stay in it: Numbered Inventory, Result Case Study, Bundle Manifest, Setup Walkthrough, Operating Story, Belief Correction, or Catalogue Tease.
3. Apply `hooked-design-copy` to line 1. Use specificity, supported tension, concrete outcome, recognizable problem, useful surprise, or strong framing. A portable generic opening fails.
4. Keep line 1 compact enough to survive the mobile truncation cut; under roughly 55 characters is a strong default when the language allows it.
5. Keep one idea per line and use deliberate whitespace. Do not let a short-form caption collapse into dense paragraphs.
6. Use specific names and numbers only when evidence supports them. Unsupported precision is removed, not approximated.
7. Use one CTA at the end unless the chosen archetype intentionally has none.
8. Run anti-slop checks. Reject denial-then-reveal constructions, generic puffery, faux insight, repetitive recap, and buzzword substitution. No em dashes.
9. Preserve useful voice and concrete mechanisms. Do not make every line clever; one strong opening and a clear progression are enough.
10. For Arabic/bilingual output, use the `arabic` skill before finalizing rhythm, bidi, and truncation behavior.

## HOLD conditions

Return a HOLD when the requested hook, result, price, metric, testimonial, product claim, or CTA premise cannot be supported from the available evidence and cannot be rewritten truthfully without changing the approved idea.

## Related components

- routing authority: `helper/GUIDE.md`
- local hook gate: `helper/quality-gates.json`
- design-copy reference: `skills/info-stories/references/hook-driven-design-copy.md`
- detailed patterns: `references/caption-patterns.md`
- worker: `agents/caption-writer.md`
- copy compression: `agents/copy-compressor.md`

## Research gates

Apply `prose-specificity` and `voice-preservation` to all visible prose. Apply `evidence-traceability` whenever the caption contains numbers, product behavior, proof, or other checkable factual claims.
