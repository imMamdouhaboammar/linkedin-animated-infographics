# Routing Guide

The repository routes requests through `helper/` before choosing production workers. The human-readable entry is [`../helper/GUIDE.md`](../helper/GUIDE.md); `helper/router.json` is the machine-readable route registry.

## Intents

| Intent | Execution |
|---|---|
| `create-post` | Full `new-post` parent workflow |
| `qa` | Focused `qa-post` parent workflow |
| `render` | Focused `render-gif` workflow |
| `design-study` | Reference diagnosis through `design-study` |
| `mascot-animation` | Focused exact-SVG mascot path |
| `info-story` | Focused Info-stories concept/story composition |

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

QA applies the relevant review variants. Rendering applies mechanical and verification gates rather than creative rewriting.

## Research gates

Research gates are selected from capability ownership and route context. `reference-dna`, for example, only activates when visual references are actually present.

Validate the router:

```bash
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/ecosystem_doctor.py check
```
