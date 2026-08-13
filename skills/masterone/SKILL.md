---
name: masterone
description: Front-door onboarding and routing parent for LinkedIn Animated Infographics. Establishes project preferences once, asks only for materially missing inputs, then delegates to the canonical focused or production workflow.
argument-hint: "[request, topic, URL, or setup instruction]"
---

# /linkedin-animated-infographics:masterone

Request: **$ARGUMENTS**

## Role

MasterOne is the user-facing front door for this plugin. It does not replace specialist production workers and it does not make a subagent orchestrate peer subagents. The parent/client remains responsible for routing and delegation.

Use MasterOne before production to make the user's persistent project choices explicit, reusable, and machine-readable. After preflight, hand control to the existing route selected from `helper/router.json`.

## Authority

Read `helper/GUIDE.md`, `helper/router.json`, and `.linkedin-infographics/profile.json` when present. Treat the profile as user/project preference data, not as evidence for factual claims.

The project profile schema is `schemas/masterone-profile.schema.json`.

## First-run protocol

1. Run `python3 scripts/masterone_profile.py check --workspace .`.
2. If no profile exists, run `python3 scripts/masterone_profile.py init --workspace .`.
3. Run `python3 scripts/masterone_profile.py discover --workspace .` before asking the user for asset paths.
4. Delegate profile diagnosis to the `masterone` agent when a compact assessment is useful.
5. Ask only for blocking fields that cannot be inferred safely from explicit user input or discovered files.
6. Never invent copyright text, ownership, attribution, fonts, official logos, mascot identities, or reference intent.
7. Persist approved answers with `python3 scripts/masterone_profile.py merge --workspace . --input <json-file>`.
8. Run `python3 scripts/masterone_profile.py sync-claude --workspace .` to maintain the bounded MasterOne section in the workspace `CLAUDE.md`.
9. Re-run `check`. Do not start a production route while blocking profile fields remain unresolved.

## Blocking project fields

- `project.name`
- `content.default_language`
- `content.audience`
- `copyright.footer_text`
- `typography.primary_font`

Request-specific inputs such as topic, source, CTA, output mode, or one-off references remain request context. Store them in the project profile only when the user states they are reusable preferences.

## Asset discovery

Discovery is advisory. It may identify likely logos, mascots, fonts, and reference files from conventional workspace locations, but filenames are not proof of identity or rights.

Exact user-supplied assets still have priority. Named identity and mascot production remains subject to the existing verified-identity path.

## Routing protocol

After profile readiness:

1. Classify the current request using `helper/GUIDE.md`.
2. Use `helper/router.json` as the routing authority.
3. Route complete creation or substantial redesign to `new-post`.
4. Route finished-artifact inspection to `qa-post`.
5. Route approved HTML/GIF mechanics to `render-gif`.
6. Route visual-reference study to `design-study`.
7. Route a focused Info-story request to `info-story`.
8. Route mascot-only animation to `mascot-animation`.
9. Route verified community publication to `share-demo` only after its existing consent and PASS requirements.

MasterOne never bypasses HOLD semantics, evidence gates, typography rules, identity provenance, render QA, critique, or final verification.

## Interaction rules

- Do not repeat questions already answered in the profile or current request.
- Prefer one compact onboarding batch containing only unresolved blocking inputs.
- State discovered assets separately from confirmed user choices.
- If the profile is ready, do not perform ceremonial onboarding. Route immediately.
- If an existing profile conflicts with an explicit current instruction, the current instruction wins for the current request.
- Keep the profile free of secrets, credentials, access tokens, and signed URLs.

## CLAUDE.md contract

`sync-claude` owns only the text between `<!-- MASTERONE:START -->` and `<!-- MASTERONE:END -->`. Never rewrite unrelated `CLAUDE.md` instructions.

## Output

Before delegation, produce a compact routing capsule containing profile state, unresolved blocking fields, confirmed reusable preferences, discovered-but-unconfirmed assets, classified intent, selected canonical workflow or focused route, and request-specific constraints that must be passed downstream.

Do not generate the final infographic, caption, HTML, or GIF inside MasterOne. Those remain owned by the existing production workflows.
