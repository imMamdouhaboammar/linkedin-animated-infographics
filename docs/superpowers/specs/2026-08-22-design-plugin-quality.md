# Design and OpenAI Plugin Quality Upgrade Specification

## Goal

Improve the repository's design judgment and the public ChatGPT/Codex Skills-only package without changing the product into an MCP-backed plugin or weakening the existing evidence, identity, typography, still-first, motion, and render gates.

## Product decision

Keep the public OpenAI distribution Skills-only. The recurring user job is to turn evidence-backed material into a distinctive static or animated LinkedIn visual story, then review it rigorously before publishing. External apps are optional host capabilities, not mandatory dependencies for the core job.

The public Skill portfolio stays intentionally compact:

- `masterone` for onboarding and route selection
- `linkedin-infographic-autopilot` for capability-aware end-to-end execution
- `linkedin-infographic-studio` for full production
- `linkedin-infographic-review` for bounded pre-publish critique
- `exact-svg-mascot` for exact protected mascot work
- `share-community-demo` for explicit post-verification community sharing

Do not add duplicate public Skills for internal agent roles.

## Design-quality upgrade

### 1. Perception preflight

Before still construction, require a compact perception preflight with:

- exactly one primary focal anchor; reject three or more equal-emphasis anchors
- one-second hierarchy test
- thumbnail test at approximately 100x100 pixels
- squint or blur value-mass test
- grayscale hierarchy test
- negative-space audit that distinguishes intentional negative space from accidental dead space
- edge, crop, and tangency audit
- brand-off specificity test: after hiding logos, the composition should still feel specific to the story rather than generic UI
- effect-subtraction test: removing glow, shadows, 3D, or decorative motion must not remove the concept itself

A failing preflight routes only the failing dimension back for revision. It does not restart unrelated evidence, asset, or typography work.

### 2. Reference transfer protocol

When visual references exist, analyze each reference through:

1. Evidence: what is visibly present
2. Observation: the structural/aesthetic pattern
3. Transferable rule: a general principle safe to reuse
4. Anti-rule: what must not be copied or over-applied

Assign non-overlapping jobs to references when multiple references exist, such as composition, type hierarchy, color harmony, texture, pacing, or motion. Do not blend references indiscriminately and do not copy distinctive subject matter, identity, or proprietary composition signatures.

### 3. Visual-slop pressure

Continue the existing named blocking taxonomy and add severity-aware aggregation for non-hard-gate defects:

- critical: always blocks
- major: pressure 3
- minor: pressure 1
- block when there is any critical finding, two or more major findings, four or more minor findings, or cumulative pressure is at least 6

Hard gates remain independently blocking regardless of the aggregate score.

### 4. Targeted revision routing

Every failed visual review must identify the smallest responsible dimension:

- concept/message
- hierarchy/composition
- typography
- Arabic/RTL when applicable
- brand/identity
- copy density
- motion
- render/runtime

Retry from the last approved artifact for that dimension. Do not chain repairs onto a known-bad visual state when doing so would compound drift.

## OpenAI package behavior

Both `linkedin-infographic-studio` and `linkedin-infographic-autopilot` must carry the same design-quality contract while remaining self-contained. `linkedin-infographic-review` must expose the perception checks and severity-aware findings to users reviewing existing work.

Capability negotiation remains truthful. Shell, Python, sandbox writes, image inspection, delegation, connected apps, and publishing tools may be used only when observed in the current host.

## Release decision

The current public package is still `prepared-not-submitted`, so this work strengthens the existing `3.7.0` release candidate instead of creating version churn before first submission.

All host manifests, compatibility registries, marketplace metadata, validators, tests, and submission metadata remain aligned on `3.7.0`. A future published snapshot can cut a new version when there is an actual distribution boundary that requires it.

## Submission boundary

Prepare updated Skills-only submission metadata and reviewer cases from repository-supported behavior. Keep status `prepared-not-submitted`. Do not claim OpenAI portal submission, review, approval, or publication.

## Verification

Required gates:

- repository unit tests
- Python compileall gate
- Info-stories validation
- ecosystem router validation
- research-gates validation
- plugin graph validation
- ecosystem doctor
- demo gallery validation
- marketplace validation
- Codex/OpenAI plugin validation
- Antigravity plugin validation
- GitHub Security Gates
- Plugin Scanner
- CodeRabbit and QLTY status when available on the pull request

A merge requires exact-head verification and no unresolved high-severity review findings.
