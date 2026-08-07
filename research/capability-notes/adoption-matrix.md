# Upstream capability adoption matrix

The upstream repositories are research inputs, not bundled runtime dependencies. Their working copies live under ignored `research/upstreams/`. Product-facing rules are independently worded and tested locally. Runtime adoption is declared in `gates.json`; prose notes explain why each gate exists but do not replace the machine-readable contract.

| Runtime gate | stop-slop | no-ai-slop | taste-skill | Hallmark | COG | Local implementation |
|---|---|---|---|---|---|---|
| `prose-specificity` | strong | strong | - | - | - | anti-slop gates + copy-compressor + caption-writer + post-critic |
| `voice-preservation` | supporting | strong | - | - | - | anti-slop gates + copy-compressor + caption-writer |
| `design-dials` | - | - | strong | - | - | story brief design dials + story-architect + layout-composer + motion-director |
| `structural-originality` | - | - | strong | strong | - | design-taste gates + layout-composer + artboard-builder + fingerprint checker |
| `reference-dna` | - | - | - | strong | - | design-study + study protocol + layout-composer |
| `contrast-discipline` | - | - | strong | strong | - | semantic Story House tokens + palette-curator + contrast checker |
| `evidence-traceability` | - | supporting | - | strong | strong | evidence-checker + protected fact slots + verifier evidence rows |
| `bounded-verification` | - | - | - | - | strong | render-qa + post-critic + read-only story-verifier + max-two repair loop |

## How the gates ship

1. `sources.json` records the inspected upstream repository, commit, and license
2. Individual capability notes record Adopt / Adapt / Reject decisions
3. `gates.json` records stable runtime gate IDs, source names, stages, severity, owners, local behavior, and implementation references
4. `helper/capabilities.json` connects repository capabilities to those gate IDs
5. `scripts/ecosystem_router.py` returns the applicable gate IDs with a route
6. Shipping agents execute the gate behavior and return evidence to the parent workflow
7. `scripts/research_gates.py check` and unit tests reject missing provenance, dead owners, broken implementation references, or unconnected gates

## Deliberate exclusions

- No frontend framework prescriptions are imported
- No mandatory GSAP, scroll hijacking, dark mode, navigation, form, or responsive-site rules are imported
- No random aesthetic selection is used
- No paid-template or signature-work cloning is supported
- No upstream repository is packaged with the plugin
- No upstream prose is copied as a runtime prompt; local rules remain independently worded
