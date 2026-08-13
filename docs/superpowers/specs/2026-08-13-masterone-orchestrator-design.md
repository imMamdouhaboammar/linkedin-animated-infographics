# MasterOne Orchestrator Design

## Goal

Add `MasterOne` as the repository front-door experience for Claude and other agent clients. MasterOne owns first-run onboarding, persistent project preferences, brief completeness, and deterministic route selection. Existing parent workflows such as `new-post`, `qa-post`, and `render-gif` continue to own production sequencing.

## Architecture

MasterOne has two cooperating surfaces:

1. `skills/masterone/SKILL.md` is the public parent entrypoint. It performs onboarding and route selection, then transfers control to the canonical workflow selected by `helper/router.json`.
2. `agents/masterone.md` is the bounded context worker. It normalizes reusable project preferences, inspects available context, reports missing blocking inputs, and returns a route decision to the invoking parent workflow. It never coordinates peer agents.

This preserves the repository rule that workers do not orchestrate peer workers while still making MasterOne the first user-facing experience.

## Persistent profile

The canonical project preference file is `.linkedin-infographics/profile.json`. It is generated from `schemas/masterone-profile.schema.json` and stores reusable preferences rather than transient post facts.

Preference groups include project identity, content language and audience defaults, copyright and footer rules, typography and local font paths, approved logos, visual references, mascot identities and policy, LinkedIn canvas/output defaults, motion defaults, and approval preferences.

MasterOne asks only for unresolved fields that materially affect the requested route. Missing optional preferences never block unrelated focused work.

## Onboarding

On first run MasterOne reads `helper/GUIDE.md`, checks the profile, inspects supplied context before asking questions, records only explicit or safely observed values, computes readiness for the requested route, reports only missing blocking inputs, syncs a bounded managed section in `CLAUDE.md`, then transfers control to the canonical route.

MasterOne never invents copyright ownership, attribution, fonts, identity assets, mascot identities, or reference intent.

## CLAUDE.md contract

`CLAUDE.md` remains an instruction index, not a preference database. The managed `MASTERONE` section points to the profile and requires clients to honor copyright/footer ownership, selected fonts, approved logos and identity assets, mascot policy, visual reference intent, language/RTL preference, audience, and output defaults.

The managed section is idempotent and replaces only content between explicit markers.

## Routing

`helper/router.json` gains a top-level `front_door` contract naming `masterone`, the profile path, and supported downstream intents. MasterOne classifies requests into existing intents: `create-post`, `qa`, `render`, `design-study`, `mascot-animation`, `info-story`, and `share-demo`. It is not added to the `new-post` worker sequence.

## Public interfaces and test seams

`scripts/masterone_profile.py` exposes `init`, `status`, `set`, `sync-claude`, and `check` commands. Tests exercise these commands as public behavior.

Routing tests assert that the helper router names MasterOne as the front door while preserving current `create-post` worker order. Contract tests assert that MasterOne is registered in module and graph inventories and that the public skill can reach every supported downstream intent.

## Readiness

For `create-post`, blocking reusable fields are content language, audience, and output mode. Copyright/footer information blocks only when the profile marks a footer as required. Existing verified-identity, reference, evidence, typography, and HOLD contracts remain authoritative.

Focused routes require only their route-specific inputs. For example, `render` does not require audience or copyright metadata.

## Performance

MasterOne reduces repeated context collection rather than adding another full prompt layer. Reusable preferences are loaded once from the profile; transient post facts remain in the existing runtime-context request; downstream caching and HOLD semantics remain unchanged; MasterOne does not preload every skill or duplicate existing quality gates.

## Failure handling

Invalid profile JSON, unsupported schema versions, invalid enum values, or malformed dotted updates fail without rewriting the existing profile. `sync-claude` edits only the managed marker region and preserves all other content.

## Documentation

Update `CLAUDE.md`, `AGENTS.md`, `helper/GUIDE.md`, `docs/agents.md`, and `docs/routing.md` with concise pointers so MasterOne is discoverable without duplicating the full profile schema in always-loaded instructions.
