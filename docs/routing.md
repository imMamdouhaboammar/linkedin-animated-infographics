# Routing Guide

The repository routes requests through `helper/` before choosing production workers. The human-readable entry is [`../helper/GUIDE.md`](../helper/GUIDE.md); `helper/router.json` is the machine-readable route registry.

## Visual reference contract

Reference studies record ranked evidence, confidence, provenance, rights, and focused contexts. Missing or invalid requested evidence returns HOLD; no supplied reference returns SKIP.

## Intents

| Intent | Execution |
|---|---|
| `create-post` | Full `new-post` parent workflow |
| `qa` | Focused `qa-post` parent workflow |
| `render` | Focused `render-gif` workflow |
| `design-study` | Reference diagnosis through `design-study` |
| `mascot-animation` | Focused exact-SVG mascot path |
| `info-story` | Focused Info-stories concept/story composition |
| `share-demo` | Opt-in verified public demo export through `share-demo` + `community-publisher` |

Inspect a route:

```bash
python3 tools/route_request.py --request "Create an animated LinkedIn infographic"
```

Or use the richer script directly:

```bash
python3 scripts/ecosystem_router.py explain \
  --request "Turn this product workflow into a UI story" \
  --ui-mockup
```

The returned contract includes status, workflow, skills, agents, conditional agents, capabilities, asset gates, research gates, and local quality gates.

## Conditional gates

### Arabic / RTL

Adds the `arabic` skill. RTL reading flow may justify an alignment exception when `center-first` would reduce comprehension.

### UI mockup

Adds UI fidelity and evidence ownership. Real-looking product states, features, metrics, integrations, and proof need evidence. Concept/sample UI must be identifiable when readers could confuse it with real product behavior.

### Visual reference

Adds `design-study` and activates `reference-dna`. References are diagnosed into reusable design behavior, not copied as signature work.

### Named / official mascot

Adds the mascot path only when the exact SVG exists. Missing asset returns `HOLD: exact SVG required`. A main conversational model asks the user for the exact SVG; a worker returns the HOLD to its parent workflow.

### Static output

Static work can skip motion-specific workers after still approval, but it does not skip adversarial critique or independent verification.

## Community publishing route

`share-demo` is separate from `create-post`. It is not inserted into the critical creation graph.

`new-post` may offer sharing only after final verification `PASS` and after delivery. Explicit acceptance transfers control to the `share-demo` parent workflow. A decline or no answer stops with no GitHub write.

The focused route resolves to:

- workflow: `share-demo`
- skill: `share-demo`
- agent: `community-publisher`
- capability: `verification-loop`

The parent workflow owns consent, rights confirmation, metadata, source-prompt consent, packaging, and export preflight. The worker owns only fork, fresh branch, scoped commit, push, and pull-request creation. Publication ends at the PR and requires maintainer manual review and merge.

## Creative route behavior

Complete creation runs evidence before concepting. `creative-director` then produces several evidence-safe concept directions with:

- visual hook
- copy hook
- aha mechanic
- story shape
- recommended Visual Style / Story Archetype / motion behavior
- evidence dependencies and risks

The selected concept feeds `story-architect`, copy, layout, and motion planning. Downstream workers should not invent separate competing concepts.

## Local gates

Complete creation and Info-story composition apply:

- `hooked-design-copy`
- `creative-payoff`
- `restrained-palette`
- `center-first-composition`

QA applies the relevant review variants. Rendering applies mechanical and verification gates rather than creative rewriting. Community publishing applies its own consent/export boundary after verification rather than reopening creative production.

## Research gates

Research gates are selected from capability ownership and route context. `reference-dna`, for example, only activates when visual references are actually present. `share-demo` inherits `bounded-verification` as a prerequisite and cannot publish a non-PASS artifact.

Validate the router:

```bash
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
```

## MasterOne front door

The plugin exposes `helper/router.json::front_door` for the first interaction. `masterone` performs project-profile readiness and then hands the request to one of the existing intents: `create-post`, `qa`, `render`, `design-study`, `mascot-animation`, `info-story`, or `share-demo`.

`create-post` still resolves to `new-post`; its worker sequence is unchanged. Persistent preferences live in `.linkedin-infographics/profile.json`. Request-specific topic, source, CTA, output mode, and one-off references remain request context unless the user explicitly makes them reusable defaults.
