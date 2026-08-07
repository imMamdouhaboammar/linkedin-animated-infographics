# Ecosystem v3 Creative Runtime Addendum

This addendum extends the approved Ecosystem Routing Kernel v3 design with four plugin-local production requirements requested during implementation.

## 1. Creative director as a first-class worker

Add `agents/creative-director.md` before `story-architect` on the complete `new-post` shipping path.

The worker receives source material, `build/evidence.json`, optional `build/design-study.json`, product constraints, language, format, and any approved brand limits. It returns `build/creative-concepts.json` to the parent workflow.

The artifact contains at least three bounded directions. Every direction must include:

- `concept_name`
- `visual_hook`
- `copy_hook`
- `aha_mechanic`
- `story_shape`
- `recommended_visual_style`
- `recommended_story_archetype`
- `recommended_motion_behavior`
- `evidence_dependencies`
- `risk_notes`
- `why_it_earns_attention`

At least one direction must create a clear visual payoff or aha moment without relying on novelty for its own sake. The creative director may recombine structures, reveal relationships, transform states, stage comparisons, or use UI/mascot moments, but it may not invent claims, metrics, product behavior, or evidence.

The parent workflow selects or approves one direction. `story-architect`, `copy-compressor`, `layout-composer`, and `motion-director` consume the selected direction rather than independently inventing competing concepts.

## 2. Hook-driven design copy

Infographic design copy must not default to neutral reporting language when the slot is responsible for attention or progression.

Create a local quality gate `hooked-design-copy` with these rules:

- hero headline must earn attention through specificity, tension, useful surprise, strong framing, a concrete outcome, or a recognisable problem
- section openers may use micro-hooks when they advance the story, but labels, table headers, commands, and UI controls remain literal when clarity requires it
- hooks cannot manufacture stakes, facts, urgency, social proof, or numbers
- ban generic declarative openings that could move unchanged to another product or topic
- preserve the user's own language and specific evidence
- one strong hook is better than every label trying to sound clever

`creative-director`, `copy-compressor`, `caption-writer`, and `post-critic` own this gate.

## 3. Plugin-local creative quality gates

Add `helper/quality-gates.json` as the machine-readable registry for local product behavior that is not attributed to upstream research.

Required gates:

- `hooked-design-copy`: blocking
- `creative-payoff`: blocking for complete post creation and Info-story composition
- `restrained-palette`: blocking unless the approved brief explicitly requests a louder treatment
- `center-first-composition`: blocking unless the layout artifact records a valid alignment exception

The existing helper defaults `creative-attractive-restrained` and `center-first` become enforcement inputs rather than prose-only guidance.

A wow or aha moment means the content produces a useful visual payoff, reveal, state change, comparison, relationship, or interaction that makes the idea easier to understand or remember. It does not mean glow, 3D decoration, extreme saturation, excessive motion, or arbitrary spectacle.

## 4. Strict module reality validator

Add `helper/modules.json` as the public module manifest and `scripts/ecosystem_doctor.py` as the strict cross-repository validator.

The manifest records active public modules by type: skills, agents, and tools. Every entry records its path, role, test contract, and one or more reachability links.

The doctor must fail when any of these conditions is true:

- declared module path does not exist
- public skill exists but is absent from the manifest
- public agent exists but is absent from the manifest
- public tool in `tools/*.py` exists but is absent from the manifest
- active skill is unreachable from a router route/condition or an agent preload
- active agent is unreachable from a workflow sequence or conditional edge
- active tool is not referenced by a skill, agent, helper guide, or declared validator contract
- module test contract does not exist
- helper capability owner is not a declared active agent
- artifact producer/consumer is not a declared active participant
- quality gate owner is not a declared active agent
- research gate owner or implementation reference is dead
- workflow sequence differs between router and plugin graph
- complete-post route omits the creative director, post critic, or independent verifier

`python3 scripts/ecosystem_doctor.py check` becomes the strict repository doctor and is required in CI before official Claude plugin validation.

## 5. Updated complete-post sequence

The canonical shipping sequence becomes:

1. `design-study`
2. `evidence-checker`
3. `creative-director`
4. `story-architect`
5. `palette-curator`
6. `copy-compressor`
7. `layout-composer`
8. `caption-writer`
9. `artboard-builder`
10. `motion-director`
11. optional `mascot-animator` between still construction and motion implementation
12. `motion-engineer`
13. `render-qa`
14. `post-critic`
15. `story-verifier`

Static output may skip motion-specific workers after the approved still, but it still requires adversarial critique and independent verification.

## 6. Success criteria added by this addendum

A complete route is only considered integrated when:

- the creative director is reachable and produces its declared artifact
- design copy exposes a real hook rather than merely restating source material
- the selected concept contains a useful visual payoff or documented reason to stay intentionally plain
- palette execution follows `creative-attractive-restrained`
- composition follows `center-first` or records a valid exception
- every public module is declared, reachable, tested, and referenced by the strict doctor
- local quality gates and research-derived gates are both visible in the route result and enforced by shipping owners
