# Research Capability Gates

Research under `research/` is an active input to production quality, not a passive archive. The repository preserves source provenance, independently-worded local adoption rules, runtime gate ownership, and tests without packaging upstream working copies.

## Provenance sources

The tracked snapshot in `research/capability-notes/sources.json` records five inspected MIT repositories and exact commits:

- COG-second-brain
- hallmark
- no-ai-slop
- stop-slop
- taste-skill

The ignored `research/upstreams/` clones are local study material only and never ship with the plugin.

## Runtime gates

`research/capability-notes/gates.json` is the machine-readable adoption contract.

### `prose-specificity`

Informed by stop-slop and no-ai-slop. Detect named low-information prose patterns by slot, preserve literal labels, and block generic filler or unsupported rhetorical setup before delivery.

### `voice-preservation`

Informed primarily by no-ai-slop. Preserve specific facts, mechanisms, names, numbers, and deliberate voice while applying the minimum effective edit.

### `design-dials`

Informed by taste-skill. Resolve design variance, visual density, and motion intensity as explicit bounded decisions rather than random aesthetic choice.

### `structural-originality`

Informed by taste-skill and hallmark. Require meaningful variation in topology, card grammar, connectors, visual anchor, density, or motion grammar. Palette-only reskins fail.

### `reference-dna`

Informed by hallmark. When a visual reference is supplied, extract reusable rhythm, topology, card/connector grammar, token roles, density, motion grammar, attribution, and visual anchor without cloning distinctive work.

### `contrast-discipline`

Informed by taste-skill and hallmark. Keep one coherent semantic token set and enforce the repository text/state contrast floors before approval.

### `evidence-traceability`

Informed by COG-second-brain, hallmark, and no-ai-slop. Trace factual claims, product states, metrics, logos, proof, and acceptance rows to supplied evidence.

### `bounded-verification`

Informed by COG-second-brain. Keep verification independent, evidence-backed, read-only, and limited to two targeted repair attempts before escalation.

## Adoption chain

A research idea is not considered integrated merely because a note mentions it. The shipping chain is:

1. `sources.json` records repository, inspected commit, and license
2. individual capability notes record Adopt, Adapt, Reject, and local targets
3. `gates.json` declares stable runtime gate IDs, stage, severity, owners, and implementation references
4. `helper/capabilities.json` maps repository capabilities to those gate IDs
5. `scripts/ecosystem_router.py` returns applicable research gates for a request
6. named shipping agents execute the gate behavior
7. `scripts/research_gates.py` and `scripts/ecosystem_doctor.py` reject dead provenance, owners, or implementation references

## Local-native behavior

Not every good repository rule needs upstream provenance. The following are explicitly local product behavior rather than research-source claims:

- exact official mascot SVG identity
- `hooked-design-copy`
- `creative-payoff`
- `creative-attractive-restrained` palette default
- `center-first` composition default

These live under helper capabilities/local quality gates and are kept separate from research attribution.

## Deliberate exclusions

The plugin does not import frontend-framework prescriptions, mandatory GSAP/scroll behavior, random aesthetic selection, paid-template cloning, signature-work cloning, or upstream repositories as runtime dependencies.

## Validation

```bash
python3 scripts/audit_upstreams.py check
python3 scripts/research_gates.py check
python3 scripts/ecosystem_doctor.py check
python3 -m unittest tests.test_research_gates tests.test_upstream_capabilities -v
```
