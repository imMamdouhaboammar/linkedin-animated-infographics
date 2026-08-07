---
name: post
description: Route LinkedIn infographic requests to the correct complete or focused workflow using the repository helper, capability gates, creative defaults, and artifact contracts.
---

# LinkedIn Animated Infographics

## Purpose

Act as the lightweight **routing entrypoint** for the plugin. Do not duplicate the complete workflow here. Read `helper/GUIDE.md`, classify the request, inspect the route, then invoke the correct workflow or focused skill.

## Use when

Start here for a LinkedIn infographic, post, GIF, cheat sheet, workflow visual, stack map, UI story, design direction, hook, mascot request, render request, or QA request when the correct specialist path is not already explicit.

## Inputs

- user request and source material
- optional intent override
- language/output mode
- optional visual references, UI mockup flag, brand assets, or mascot requirement

## Outputs

Return a resolved route containing workflow, skills, agents, capabilities, asset gates, research gates, and local quality gates. For creation requests, hand control to the `new-post` parent workflow.

## Procedure

1. Read `helper/GUIDE.md`.
2. Resolve the request through the deterministic helper when structured routing is useful:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/route_request.py --request "<request>"
```

3. Use the route intent:
   - `create-post` → `new-post`
   - `qa` → `qa-post`
   - `render` → `render-gif`
   - `design-study` → focused `design-study` worker/Info-stories references
   - `mascot-animation` → `mascots` + `svg-mascot-animator`
   - `info-story` → focused `linkedin-animated-infographics:info-stories` composition path
4. When Info-stories is active, the resolved Story House from the merged registry is authoritative. Do not silently replace it with legacy House 0; House 0 is only a legacy fallback when there is no resolved story brief.
5. Apply conditional gates before production: Arabic/RTL, UI fidelity, visual-reference diagnosis, and exact official mascot SVG.
6. For complete creation, require the `creative-director` concept stage before `story-architect`. The concept should provide evidence-safe visual/copy hooks and a useful aha mechanic rather than a generic topic restatement.
7. Keep plugin-local defaults active: `creative-attractive-restrained` palettes and `center-first` composition with documented exceptions.
8. Do not silently bypass `post-critic` or `story-verifier` on complete shipping paths.

## HOLD conditions

Return a HOLD when the helper reports a blocking asset or gate, especially a missing exact mascot SVG, unsupported evidence, incompatible Story House/Style choice, or a render/verification blocker. Do not invent a route around a blocking gate.

## Related components

- routing authority: `helper/GUIDE.md`
- router registry: `helper/router.json`
- capability registry: `helper/capabilities.json`
- local quality gates: `helper/quality-gates.json`
- artifact contracts: `helper/artifacts.json`
- research gates: `research/capability-notes/gates.json`
- Info-stories skill: `linkedin-animated-infographics:info-stories`
- complete workflow: `skills/new-post/SKILL.md`
- focused QA: `skills/qa-post/SKILL.md`
- focused render: `skills/render-gif/SKILL.md`

## Research gates

The post router does not reinterpret research rules. It passes through the gate IDs returned by the helper, including `prose-specificity`, `voice-preservation`, `design-dials`, `structural-originality`, `reference-dna`, `contrast-discipline`, `evidence-traceability`, and `bounded-verification` where applicable.
