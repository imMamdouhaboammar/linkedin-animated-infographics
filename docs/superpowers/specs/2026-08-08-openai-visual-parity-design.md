# OpenAI Visual Parity Design

## Goal

Bring the ChatGPT/Codex plugin to the same quality discipline as the existing Claude experience while allowing each host to produce a different visual direction.

The target is parity of process and acceptance criteria, not pixel parity.

## Non-negotiable constraint

The existing Claude path is a regression baseline. Do not remove, rename, or repurpose `.claude-plugin/`, `agents/`, Claude worker routing, or Claude-specific execution behavior to improve the OpenAI distribution.

## Root cause

The Claude runtime can execute the repository's worker graph and agent roles directly. The published OpenAI package is skills-only, so a skill that says `delegate to creative-director`, `delegate to layout-composer`, or reads repository files outside the packaged skill bundle can degrade into one-model, one-pass execution.

That failure mode produces visually valid but weak work: top-heavy compositions, large unexplained dead zones, nested card stacks, generic UI grammar, weak macro rhythm, and motion added to a still that never passed a serious visual gate.

## Architecture

Create an OpenAI-specific distribution at `openai-skills/` and point `.codex-plugin/plugin.json` to it. Claude continues using the existing canonical `skills/` plus `agents/` graph.

The OpenAI distribution is a compiled, self-contained workflow. It does not pretend unavailable workers exist. Instead, it executes the same roles as explicit sequential passes with bounded artifacts:

1. evidence inventory
2. creative directions
3. story architecture
4. palette contract
5. copy compression
6. macro layout
7. still construction
8. still critique and repair
9. motion direction
10. motion implementation
11. render QA
12. adversarial visual critique
13. final verification

The OpenAI workflow may produce a different composition, palette, archetype, or motion treatment than Claude. It must satisfy the same quality intent.

## OpenAI package

Create:

- `openai-skills/linkedin-infographic-studio/SKILL.md`
- `openai-skills/linkedin-infographic-studio/references/openai-runtime.md`
- `openai-skills/linkedin-infographic-studio/references/visual-quality-contract.md`
- `openai-skills/linkedin-infographic-studio/references/role-passes.md`
- `openai-skills/linkedin-infographic-studio/references/motion-quality-contract.md`

The package must be self-contained for the workflow it claims to support. It must not require `.claude-plugin/`, `agents/`, `${CLAUDE_PLUGIN_ROOT}`, `helper/`, or `architecture/` at runtime.

## Visual quality contract

The OpenAI still gate is blocking. Motion cannot begin until the still passes.

Required checks:

- one dominant visual anchor readable within two seconds at feed scale
- macro zones defined before styling details
- primary composition uses roughly 82-92% of usable vertical canvas unless the approved concept intentionally uses a sparse composition
- no unexplained vertical gap greater than 120px between the end of the main composition and the footer/takeaway zone
- no more than two levels of bordered containment
- repeated cards are allowed for true comparison, but generic card stacking cannot become the page's primary visual language
- pills, badges, tiny uppercase labels, mini status chips, and dashboard-like UI require a semantic job; decorative use is rejected
- copy density is solved through hierarchy and editing, not smaller type or more nested containers
- footer has an explicit reserved zone and the main composition terminates intentionally near it
- static visual payoff must work before animation
- animation must explain sequence, change, travel, or active state; decorative motion alone fails

## Repair loop

The OpenAI workflow must render or inspect the still, identify the top three visual defects, repair them, and re-check before motion.

After animation, perform a second critique for balance, legibility, pacing, seam quality, and whether motion improves comprehension.

Maximum two targeted repair attempts before returning a precise HOLD/FAIL instead of shipping weak output.

## Generic visual failure taxonomy

The critic must explicitly test for:

- `top-heavy-composition`
- `bottom-dead-zone`
- `nested-card-density`
- `generic-ui-grammar`
- `weak-macro-rhythm`
- `weak-visual-anchor`
- `footer-detachment`
- `motion-on-weak-still`
- `decorative-motion`
- `feed-scale-legibility`

## Manifest and versioning

Change the OpenAI manifest skills path from `./skills/` to `./openai-skills/` and bump the plugin version from `3.2.0` to `3.2.1`.

Keep Claude's version metadata in sync where required by existing repository parity tests, but do not change Claude behavior.

Update OpenAI submission metadata and compatibility metadata to describe the isolated distribution accurately.

## Tests

Repository tests must prove:

1. the OpenAI manifest points to `./openai-skills/`
2. the OpenAI skill bundle exists and is self-contained
3. the OpenAI workflow does not reference Claude-only paths or unavailable worker delegation
4. the visual quality contract contains the blocking failure taxonomy and measurable layout gates
5. Claude plugin/agent files remain present and unchanged in behavior contracts
6. version metadata remains internally consistent
7. directory compliance remains valid: at most three default prompts, square logo/composer icon, no screenshots field

## Release outcome

The repository should end with a publish-ready `3.2.1` OpenAI package. Updating the GitHub repository does not itself republish the already-listed directory version; the new package still requires the platform's update/publish step.
