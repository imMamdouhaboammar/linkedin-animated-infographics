# GIF library and retrieval validation

Date: 2026-08-11

Runtime: `/opt/homebrew/bin/python3` (Python 3.14.6)

Scope: the user-supplied 37-GIF corpus, ignored local reference state, canonical mechanism retrieval, and representative scaffold/retrieval outputs

## Result

The real corpus and all seven retrieval briefs passed the checks that the current deterministic paths can perform. The corpus resolved to 31 canonical assets and six aliases, repeated ingestion produced a byte-identical manifest, every cached GIF and sampled frame opened successfully, and the seven briefs selected seven distinct leading mechanisms and seven distinct primary references.

Representative JSON generation is supported and was exercised. Representative HTML render inspection was not performed because the repository has no deterministic story/layout/motion-JSON-to-HTML generator: `scripts/render.sh` starts from an already-authored HTML artboard. Creating HTML by hand would introduce unvalidated content and layout decisions rather than test the scaffold/retrieval path.

## Observed machine facts

### Corpus and ignored state

| Check | Observed result |
| --- | ---: |
| Source GIF files | 37 |
| Unique source SHA-256 values | 31 |
| Canonical manifest references | 31 |
| Manifest aliases | 6 |
| Deprecated ID aliases | `REF-003`, `REF-008`, `REF-031`, `REF-032` |
| Filename-only aliases | 2 |
| Cached GIFs opened through Pillow | 31 |
| Sampled PNGs opened through Pillow | 124 (first, middle, pre-seam, final for each canonical reference) |
| Cached GIF bytes | 67,998,232 |
| Manifest bytes | 52,161 |
| Repeated-ingest manifest SHA-256 | `b6048b78b42eb320d0c2b4ba8d0cab80a5621dce55904ed202a80b7a74d713d0` |

Two consecutive invocations of the canonical ingest command returned `31 canonical, 6 aliases`; `cmp` found no byte difference between their manifests. The canonical `check` command returned `Reference library: OK`. Independent Pillow reads reached the last frame of every cached GIF and verified all 124 PNG samples.

### Seven retrieval briefs

The executable inputs are in `examples/info-stories/reference-retrieval-briefs.json`. Each case was run twice through `tools/story_retrieve.py`. The outputs were byte-identical between runs. The mechanism list was also shuffled with 12 fixed seeds per case; every shuffled run preserved the complete ranked slug order.

| Brief | Leading mechanism | Primary reference | Ranked mechanisms | concept | story | palette/type | layout | motion | review |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Maturity ladder | `capability-ladder` | `REF-005` | `capability-ladder`, `evidence-ladder` | 1,303 | 1,950 | 1,183 | 1,928 | 1,871 | 1,275 |
| Model selection | `decision-spectrum` | `REF-018` | `decision-spectrum`, `threshold-dial` | 1,380 | 1,906 | 1,261 | 1,989 | 1,914 | 1,338 |
| Radial ecosystem | `radial-tool-constellation` | `REF-021` | `radial-tool-constellation`, `agent-ring` | 1,394 | 2,019 | 1,229 | 1,847 | 1,872 | 1,346 |
| Layered stack | `readiness-layer-reveal` | `REF-015` | `readiness-layer-reveal`, `anatomy-cutaway`, `terminal-stack-cutaway` | 1,810 | 2,748 | 1,578 | 2,707 | 2,585 | 1,741 |
| Editorial comparison | `editorial-thesis-contrast` | `REF-029` | `editorial-thesis-contrast` | 789 | 1,104 | 722 | 1,087 | 1,095 | 779 |
| Human/AI handoff | `dual-actor-decision-flow` | `REF-033` | `dual-actor-decision-flow` | 798 | 1,080 | 719 | 1,159 | 1,074 | 774 |
| Local-tool setup | `local-setup-command-rail` | `REF-035` | `local-setup-command-rail` | 835 | 1,152 | 737 | 1,133 | 1,132 | 821 |

Values in the six stage columns are compact UTF-8 JSON byte counts. All 42 projections were below their declared 8,000-byte budget. The largest was the layered-stack story projection at 2,748 bytes.

### Representative generated artifacts

The real public scaffold/retrieval CLIs produced nine output artifacts under ignored `build/task-6-validation/`:

| Case | Story brief | Layout context | Motion context |
| --- | ---: | ---: | ---: |
| Maturity ladder | 1,122 bytes | 1,929 bytes | 1,872 bytes |
| Editorial comparison | 1,118 bytes | 1,088 bytes | 1,096 bytes |
| Local-tool setup | 1,128 bytes | 1,134 bytes | 1,133 bytes |

The directory contains those nine outputs plus six stage query inputs (15 files, 60 KiB on disk). The combined SHA-256 evidence digest for the nine sorted output records is `3014fc52ee6dba844e361df4153d26e2e6c0fc8de7d6fe6b4e4cf4d33bf576c8`. `git check-ignore` confirmed the outputs are excluded by the repository's `build/` rule.

## Semantic curation observations

These are human observations from the first, middle, pre-seam, and final cached samples for three representative references. They are not pixel-derived facts or claims about exact fonts.

- `REF-005` supports a capability-ladder abstraction: all six levels remain visible while motion changes emphasis among a small number of level-specific diagrams. The reusable lesson is the ordered hierarchy and one-level-at-a-time focus, not its source copy, mascot, portrait, palette, or exact measurements.
- `REF-029` supports an editorial-thesis contrast: the large paired terms share one explicit inequality and one evidence area; the middle sample highlights a contribution route while the surrounding thesis stays readable. The reusable lesson is thesis-first hierarchy and paired evidence on one axis, not the wording, colors, or illustration geometry.
- `REF-035` supports a local-setup command rail: commands and explanations occupy distinct columns, a numbered central sequence defines reading order, and sampled motion highlights bounded steps without removing the complete guide. Its measured seam ratio is `0.835205`, so it must not be treated as proof of a seamless loop despite the sampled frames retaining the same broad structure.

These observations support the selected mechanism labels, but final layout, copy, typography, and motion decisions still belong to the established downstream artifacts and reviewers.

## Render-inspection boundary

No representative HTML was produced by the scaffold/retrieval commands. The available paths have these boundaries:

- `tools/story_scaffold.py` emits a story brief.
- `tools/story_retrieve.py` emits stage-specific context capsules.
- `scripts/render.sh` requires an authored HTML artboard and does not consume either JSON output.

Consequently, still/mobile clipping, resolved-font evidence, generated middle/final/seam frames, generic-AI pattern review, and originality review of a newly rendered artifact remain **not verified**. The cached source-frame inspection above validates reference accessibility and semantic fit only; it is not a substitute for output render QA.

## Rights and provenance limits

All 31 canonical records remain `provenance_state: unverified`, `rights_state: unverified`, and `confidence: unreviewed`. This validation does not grant reuse permission or establish authorship, licensing, factual accuracy, or exact font identity.

The source GIFs, cached assets, sampled frames, and temporary representative artifacts remain ignored and are not packaged. Only abstract structure, hierarchy, density, and motion principles may inform new work. Source wording, commands, claims, logos, portraits, mascots, illustrations, and exact visual measurements remain excluded unless separately verified and authorized.

## Commands

The external corpus path is intentionally represented by an environment variable so a private workstation path is not committed.

```bash
REFERENCE_CORPUS=<user-supplied-corpus-directory>
/opt/homebrew/bin/python3 scripts/reference_intelligence.py ingest --library "$REFERENCE_CORPUS"
/opt/homebrew/bin/python3 scripts/reference_intelligence.py ingest --library "$REFERENCE_CORPUS"
/opt/homebrew/bin/python3 scripts/reference_intelligence.py check
```

Each query from `examples/info-stories/reference-retrieval-briefs.json` was extracted to a temporary JSON file and exercised through:

```bash
/opt/homebrew/bin/python3 tools/story_retrieve.py --query <temporary-query.json>
```

Representative story briefs were produced through `tools/story_scaffold.py --out`; their layout and motion capsules were produced through `tools/story_retrieve.py` with `stage` set to `layout` and `motion` respectively.
