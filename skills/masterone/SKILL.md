---
name: masterone
description: Front-door onboarding and routing parent for LinkedIn Animated Infographics. Establishes project preferences once, asks only for materially missing inputs, then delegates to the canonical focused or production workflow.
argument-hint: "[request, topic, URL, or setup instruction]"
---

# /linkedin-animated-infographics:masterone

Request: **$ARGUMENTS**

## Purpose

Act as the front-door onboarding and routing entrypoint for the plugin. Make user/project preferences explicit, reusable, and machine-readable in `.linkedin-infographics/profile.json`, then hand control to the existing route selected from `helper/router.json`.

## Use when

Use MasterOne before production to establish reusable project defaults (project name, default language, audience, footer/copyright text, primary font) or to route onboarding requests before delegating to specialist workflows.

## Inputs

- user request, topic, URL, or setup instruction
- optional `.linkedin-infographics/profile.json`
- `helper/GUIDE.md`
- `helper/router.json`

## Outputs

- resolved or updated project profile `.linkedin-infographics/profile.json`
- compact routing capsule containing profile state, missing blocking fields, confirmed preferences, discovered candidates, classified intent, and recommended route

## Procedure

1. Inspect `.linkedin-infographics/profile.json` when present in the workspace.
2. Read `helper/GUIDE.md` and `helper/router.json`.
3. Resolve request classification and recommended route with the deterministic router:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/route_request.py --request "$ARGUMENTS"
```

4. Delegate profile diagnosis to the `masterone` agent when a compact assessment is useful.
5. Ask only for blocking fields that cannot be inferred safely from explicit user input or discovered files.
6. Never invent copyright text, ownership, attribution, fonts, official logos, mascot identities, or reference intent.
7. Route to the selected workflow from `helper/router.json`.

## HOLD conditions

Return a HOLD when blocking project fields (`project.name`, `content.default_language`, `content.audience`, `copyright.footer_text`, `typography.primary_font`) remain unresolved and cannot be safely inferred. Do not start a production route while blocking profile fields remain unresolved.

## Related components

- router guide: `helper/GUIDE.md`
- router registry: `helper/router.json`
- profile schema: `schemas/masterone-profile.schema.json`
- deterministic router CLI: `tools/route_request.py`
- masterone agent: `agents/masterone.md`
- public router skill: `skills/post/SKILL.md`

## Research gates

MasterOne enforces preference clarity and identity safety. It inherits `voice-preservation`, `evidence-traceability`, and `bounded-verification` without replacing production quality gates.
