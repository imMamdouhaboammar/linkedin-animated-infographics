---
name: masterone
description: Start LinkedIn infographic work by onboarding reusable project preferences, resolving only route-relevant missing inputs, and selecting the correct OpenAI production or focused skill. Use first when a ChatGPT or Codex user starts or resumes infographic work.
---

# MasterOne

## Purpose

Act as the OpenAI front door for LinkedIn Animated Infographics. Reuse project preferences, avoid repeated setup questions, classify the current request, then hand execution to the narrowest installed skill that owns the job.

MasterOne does not duplicate production logic from downstream skills.

## Project profile

When workspace writes are available, store reusable preferences in `.linkedin-infographics/profile.json` using the repository profile contract. If writes are unavailable, keep the same normalized fields in working context and do not claim they were persisted.

Reusable fields include default language and audience, copyright and footer rules, fonts and local font paths, approved logos and brand assets, references and reference intent, mascot identities and assets, static or animated output, motion preferences, approval rules, and output defaults.

Never infer user-confirmed brand or identity choices from filenames alone.

## Onboarding

Inspect the current request, project context, and saved profile before asking anything. Ask only for missing inputs that materially block the selected route.

For complete creation, reusable blockers are language, audience, and output mode. Exact footer text is additionally blocking only when the saved preference requires a footer. Fonts, logos, mascots, and references become blocking only when the current task or downstream skill requires them.

Current explicit user instructions override saved defaults for the current request. Persist them as new defaults only when the user indicates that intent.

## Routing

Choose the narrowest installed OpenAI skill:

- complete creation, redesign, animation, or tool-aware multi-stage execution -> `linkedin-infographic-autopilot`
- full production without explicit autopilot orchestration -> `linkedin-infographic-studio`
- finished-output QA -> `linkedin-infographic-review`
- protected named mascot or exact SVG work -> `exact-svg-mascot`
- verified community publishing after explicit consent -> `share-community-demo`
- focused visual-reference or Info-story work -> use the relevant focused path in `linkedin-infographic-studio` or `linkedin-infographic-autopilot`

If a named downstream skill is not exposed by the host, apply its documented boundary locally and state that it was not invoked.

## HOLD

Return `HOLD` instead of guessing when a route-relevant reusable input is missing, required footer text is unknown, a requested identity asset cannot satisfy the downstream verification gate, explicit reference evidence cannot be inspected, or the requested final artifact cannot be executed with observed host capabilities.

## Completion

Before handoff, report the selected route, reusable values applied, current-request overrides, and unresolved blockers. Then let the selected downstream skill own production and verification.
