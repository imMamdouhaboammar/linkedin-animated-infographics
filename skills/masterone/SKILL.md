---
name: masterone
description: Front-door onboarding and routing parent workflow for LinkedIn Animated Infographics. Use first when a user starts or resumes infographic work so reusable project preferences are loaded, missing blockers are resolved, and the correct canonical workflow is selected.
argument-hint: "[request, topic, URL, file, or focused task]"
---

# /linkedin-animated-infographics:masterone

Request: **$ARGUMENTS**

## Purpose

MasterOne is the first user-facing parent workflow for this plugin. It prepares reusable project context, resolves only the missing blockers that matter to the current request, then transfers control to the canonical production or focused workflow.

Read `helper/GUIDE.md` and `helper/router.json` before making a routing decision. Machine-readable contracts remain authoritative.

MasterOne does not replace `new-post`. Complete post production still belongs to the existing `new-post` parent workflow and its worker sequence.

## Use when

Use MasterOne when:

- this is the first LinkedIn Animated Infographics request in a project
- the user wants to create, redesign, inspect, render, study, animate, or share infographic work
- the project has reusable preferences such as footer copy, fonts, references, logos, or mascots
- an AI client needs one entrypoint before selecting a plugin skill or worker
- a prior profile exists and should be reused instead of asking the same setup questions again

A client may invoke a focused workflow directly only when the request is already unambiguous and no reusable project context is missing.

## Inputs

MasterOne may consume:

- the user's current request
- `.linkedin-infographics/profile.json` when present
- current `CLAUDE.md` / `AGENTS.md` instructions
- explicit user-provided logos, mascots, fonts, references, files, URLs, and brand assets
- safely observable project paths and existing files
- the route registry in `helper/router.json`

Reusable profile fields include:

- project name and brand
- default language and audience
- copyright owner, attribution, footer text, and whether a footer is required
- primary, secondary, and Arabic fonts plus local font paths
- approved logo and brand-asset paths
- visual references, reference directories, and whether references are inspiration, strict direction, or ask-first
- mascot identities, asset paths, and automatic-use policy
- static or animated output preference
- motion defaults
- approval and output-directory preferences

## Outputs

MasterOne returns or maintains:

- `.linkedin-infographics/profile.json`
- an onboarding/readiness summary with `READY` or the exact missing blocking fields
- one normalized route decision from the supported intent set
- a bounded `MASTERONE` managed section in `CLAUDE.md` when the client has file-write capability
- the canonical downstream parent or focused workflow selection

Supported downstream intents are:

- `create-post`
- `qa`
- `render`
- `design-study`
- `mascot-animation`
- `info-story`
- `share-demo`

## Procedure

### 1. Read authority before onboarding

Read `helper/GUIDE.md`, then `helper/router.json`.

If `.linkedin-infographics/profile.json` exists, read it before asking setup questions. Treat it as reusable project preference context, not as evidence for claims inside a post.

### 2. Inspect before asking

Inspect the user's request and available project context for explicit or safely observable values.

Examples of safely observable context:

- a logo file the user attached or explicitly named
- a local font file already supplied
- a reference directory the user explicitly pointed to
- an existing footer string already recorded in the project profile

Do not infer ownership, rights, attribution, identity, or creative intent from a filename alone.

### 3. Initialize the profile when missing

When the profile does not exist and file-write capability is available, create `.linkedin-infographics/profile.json` using `schemas/masterone-profile.schema.json` as the shape contract.

Start unknown preferences as `null`, empty arrays, or conservative defaults. Never fabricate values to make the profile look complete.

When file-write capability is unavailable, keep the same profile shape in working context and tell the parent client that persistence is unavailable for this run.

### 4. Resolve only route-relevant blockers

For `create-post`, reusable blocking preferences are:

- `content.default_language`
- `content.audience`
- `linkedin.output_mode`

When `copyright.footer_required` is true, `copyright.footer_text` is also blocking.

Fonts, references, logos, mascots, and other fields become blocking only when the request or an active downstream gate requires them.

Focused intents do not inherit unrelated onboarding requirements. A render-only request must not be blocked because audience is missing.

Ask one compact onboarding turn containing only the unresolved blocking fields. If the user provides multiple answers together, record all of them and do not ask again.

### 5. Persist reusable answers

Write reusable answers back to `.linkedin-infographics/profile.json` when file-write capability exists.

Keep transient post facts out of the profile. Topic-specific claims, one-off metrics, current URLs, and post-specific CTA wording belong to the existing runtime request and downstream evidence artifacts.

### 6. Keep CLAUDE.md bounded

When file-write capability exists, maintain one marker-bounded section:

`<!-- MASTERONE:START -->`

The managed section should point to `.linkedin-infographics/profile.json` and require clients to honor copyright/footer rules, fonts, approved identity assets, mascot policy, reference intent, language/RTL defaults, audience, and output mode.

End the section with:

`<!-- MASTERONE:END -->`

Replace only text inside those markers. Preserve all other `CLAUDE.md` content.

Do not copy the full profile JSON into `CLAUDE.md`.

### 7. Classify the request

Map the request to one existing intent:

- complete new post or substantial redesign -> `create-post`
- inspect a finished artifact -> `qa`
- render an approved HTML artboard -> `render`
- analyze a visual reference -> `design-study`
- animate a verified mascot SVG as a focused task -> `mascot-animation`
- compose or resolve an Info-story without the full post pipeline -> `info-story`
- publish a verified completed demo after explicit consent -> `share-demo`

Use the current router contract instead of guessing when route prose and registry data differ.

### 8. Transfer control

After onboarding is `READY`, transfer control to the route's existing parent or focused workflow.

For `create-post`, invoke `new-post` and preserve its complete production sequence.

MasterOne remains the user-facing coordinator for onboarding and route selection, but downstream workers return to their own parent workflow. MasterOne does not sequence peer workers inside `new-post`.

### 9. Re-onboard only when needed

On later requests, reuse the profile automatically.

Ask again only when:

- a required field is still missing
- the user explicitly changes a preference
- a route activates a new blocking requirement
- a stored path is no longer usable
- the stored preference conflicts with an explicit current request

Current explicit user instructions override reusable defaults for the current request. Persist the override only when the user indicates it should become the new default.

## HOLD conditions

Return a precise HOLD before route transfer when:

- a route-relevant blocking profile field is missing after inspection
- the profile is structurally invalid and cannot be safely repaired without user input
- a required footer is enabled but its exact text is unknown
- a requested font is required but unavailable under the existing render-safe typography contract
- a requested named logo or mascot cannot pass the existing verified-identity contract
- a requested reference has no usable evidence under the existing reference gate
- routing intent remains genuinely ambiguous after using the request and current profile

Do not invent a value to clear a HOLD.

## Related components

- routing authority: `helper/router.json`
- routing guide: `helper/GUIDE.md`
- profile schema: `schemas/masterone-profile.schema.json`
- complete production parent: `skills/new-post/SKILL.md`
- public deterministic routing helper: `skills/post/SKILL.md`
- plugin graph: `architecture/plugin-graph.json`
- module registry: `helper/modules.json`
- runtime request and caching: `scripts/runtime_context.py`

## Research gates

MasterOne does not add new research claims or quality gates. It activates the route already defined by the helper and preserves that route's existing research gates, local quality gates, verified-identity rules, typography rules, reference behavior, HOLD semantics, and bounded verification requirements.

For complete post creation, downstream `new-post` continues to apply `evidence-traceability` and `bounded-verification` with the rest of its active gate set.
