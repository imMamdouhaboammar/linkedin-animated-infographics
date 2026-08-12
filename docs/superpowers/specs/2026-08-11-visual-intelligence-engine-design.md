# Visual Intelligence Engine Design

## Status

Accepted for execution by the user's explicit no-approval, continue-through-completion instruction.

## Problem

The plugin has strong prose guidance, a canonical `design-study` worker, deterministic
Info-stories axes, and a render pipeline. It does not have a durable reference library,
content-aware retrieval, compact stage-specific reference context, or traceable visual
review evidence. The supplied corpus contains 37 GIF files: 31 unique animations and six
duplicate filenames. All decode successfully; rights and provenance remain unverified.

The existing upgrade plan correctly identified weak measured render enforcement, but it
does not implement the requested reference-intelligence loop. Its clean-checkout and clone
path assumptions are also stale. The useful measured-render work already present in this
feature branch will be completed first and then reused.

## Observable success

The implementation is accepted only when all of the following are observed:

1. All 37 GIF files ingest successfully, preserving 31 canonical assets and six aliases.
2. Existing IDs remain stable, the missing unique animation becomes `REF-035`, and a
   repeated ingest produces byte-equivalent canonical metadata.
3. Every canonical asset retains a usable local GIF path plus sampled frames in ignored
   plugin state; Git contains metadata and rules, not unlicensed source binaries.
4. Each shipped mechanism is schema-valid, reusable, searchable, reference-aware, and
   declares its originality boundaries.
5. Seven representative briefs retrieve materially different primary references and
   mechanism sets; repeated and shuffled-input runs return the same ranked IDs.
6. Retrieval enforces output mode, language, evidence, density, and content-shape hard
   constraints, explains scores, and stays within a measured UTF-8 context budget.
7. `build/design-study.json` carries ranked evidence and focused projections for concept,
   story, palette/type, layout, motion, and review without duplicating the canonical
   `story-brief`, `layout-spec`, or `motion-direction` artifacts.
8. Taste review covers Purpose, Hierarchy, Execution, Specificity, Restraint, and Variety;
   an applicable score below 3 blocks and every score has evidence.
9. Render evidence records requested/resolved fonts, layout measurements, motion purpose,
   GIF integrity, and originality checks; blocking failures exit non-zero.
10. Focused tests, repository validators, host parity checks, real corpus validation, and
    representative render checks pass freshly on the final worktree.

## Existing architecture retained

```text
brief
  -> design-study (ingest/retrieve/diagnose)
  -> evidence-checker
  -> creative-director
  -> story-architect
  -> palette-curator
  -> copy-compressor
  -> layout-composer
  -> caption-writer
  -> artboard-builder
  -> motion-director
  -> motion-engineer
  -> render-qa
  -> post-critic
  -> story-verifier
```

The worker sequence stays unchanged. `build/design-study.json` remains the reference
handoff. `build/story-brief.json`, `build/layout-spec.json`, and
`build/motion-direction.json` remain the authorities for final design decisions.

## Options considered

### A. Extend `design-study` with deterministic structured retrieval — selected

Use Pillow and the Python standard library for ingestion and measurements. Merge a
curated `mechanisms` axis through the existing catalog loader. Rank by fixed weighted
overlap and hard filters, with slug tie-breaking. Store local assets and sampled frames
under ignored `.plugin-state/reference-studies/`.

Benefits: explainable, testable, no new service or dependency, direct reuse of the
current workflow and validators. Cost: semantic observations still require curated
judgment rather than pretending pixels reveal intent.

### B. Embeddings/vector retrieval — rejected

It adds a model, index lifecycle, nondeterminism, prompt/version drift, and dependency
surface for a corpus capped at 150 records. It is justified only if measured retrieval
misses show structured ranking cannot separate a much larger corpus.

### C. A separate visual-intelligence workflow and design-spec artifact — rejected

It would duplicate `design-study`, `story-brief`, `layout-spec`, and
`motion-direction`, causing drift and bypassing the canonical parent workflow.

## Domain model

### Reference asset

A canonical animation identified by immutable `REF-NNN` plus SHA-256. Duplicate files
remain aliases. The local state record contains the copied asset path and sampled frames;
the shipped record contains basenames, hashes, measurements, observations, confidence,
provenance state, rights state, and Adopt/Adapt/Reject boundaries.

### Mechanism

A reusable creative decision, not a template. It declares origin (`extracted` or `new`),
story jobs, content shapes, compatible catalog axes, layout logic, hierarchy, typography,
motion job, loop strategy, constraints, anti-patterns, implementation hints, and reference
IDs when derived from the corpus.

### Retrieval query

Only fields needed by current callers are supported: story jobs, content shape, output
mode, language, density, evidence mode, explicit reference IDs, `top_k`, and UTF-8 byte
budget. Hard constraints filter first; weighted overlap ranks second; slug resolves ties.

### Focused context

The retrieval result is projected by consumer:

- concept: story jobs, hook mechanism, originality boundaries;
- story: beats, information shape, density, accepted/rejected traits;
- palette/type: semantic roles, type classes, language/font policy;
- layout: topology, zones, proportions, hierarchy, negative space;
- motion: communication job, sequence, timing family, static regions, loop strategy;
- review: source IDs, score reasons, adopted traits, rejected traits, anti-patterns.

No projection receives the full corpus or the whole mechanism library.

## Analysis boundary

Machine extraction records facts it can support: dimensions, bytes, frame count, duration,
loop metadata, hashes, palette distribution, first/last delta, changed-pixel statistics,
sampled frames, and basic spatial occupancy. Semantic composition, typography class,
storytelling, motion grammar, and taste are curated observations with confidence. Exact
font identification is never inferred from pixels.

## Originality and rights

- One structural primary reference; at most one motion and one typography secondary.
- Every selected reference declares the axis it influences.
- Source copy, logos, screenshots, portraits, photography, signature mascots, and
  distinctive illustrations are blocked unless rights are explicitly verified.
- The recurring orange/navy Claude starburst and pixel robot are treated as signature
  styling, not generic tokens.
- Review compares first, middle, final, and seam frames and records adopted and rejected
  traits. Similarity is directional evidence, never permission to clone.

## Typography and motion

Typography roles declare family class, stack ID, supported scripts, weights, and either
`fallback-accepted` or `exact-required`. Render evidence records requested and resolved
families. Exact-required output fails on fallback or missing glyph coverage.

Every motion declares one communication job, a target, order, duration/easing family,
hold, reset, and static regions. Simultaneous independent motion is rejected. Static
output cannot carry motion selections.

## Taste and review

The system does not calculate a fictional automatic taste score from pixels. Agents score
the established six axes from 1–5 with concrete evidence and actionable findings. The
validator checks completeness, evidence, taxonomy, and blocking rules. Objective render
measurements are copied from machine artifacts and protected by content digests.

## Performance and storage

Ingestion hashes each source and reuses cached analysis when the hash is unchanged. Source
GIFs and derived frames stay under ignored plugin state. Shipped JSON remains compact.
Retrieval is an in-memory scan over at most 150 mechanisms; no index service is warranted.

## Known boundary

The corpus's provenance and reuse rights are unverified. The implementation may learn and
retrieve abstract principles locally, but it must not publish or package the source media.
