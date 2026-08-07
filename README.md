<div align="center">

# LinkedIn Animated Infographics

**Turn imagination into visual stories that stop the scroll and make the idea click**

`Claude Code Plugin 3.0.0` · `1080×1350` · `Info-stories` · `UI stories` · `Exact-SVG mascots` · `Arabic / RTL`

<br>

<a href="./assets/demo_artboard_v4.gif">
  <img src="./assets/demo_artboard_v4.gif" alt="Animated LinkedIn infographic demo generated with the plugin" width="720">
</a>

<sub>Live 1080×1350 demo · click to open full size</sub>

</div>

## WOW first, AHA after

<strong>WOW stops the scroll<br>AHA makes the idea click</strong>

The plugin aims for both

**WOW** is the visual pull: a strong concept, a clear focal point, confident color, smart composition, and motion with a job

**AHA** is the payoff: the reader sees a relationship, comparison, transformation, state change, interface flow, or reveal that makes the idea easier to understand

If the effect looks good but adds no meaning, it is decoration

`creative-director` develops the concept before layout starts, then the rest of the workflow tests whether the idea still works through copy, layout, motion, QA, and final verification

## Demos

Good outputs can live in the repo as working examples, not screenshots buried in a README

There are two shelves:

- **Created by Mamdouh** under `demos/owned/`
- **Created by the community** under `demos/community/<github-user>/`

Every accepted demo is the same portable package: **GIF + HTML + demo.json**

After a finished post reaches final verification `PASS`, the plugin can ask `Share this demo with the community?` If the user says yes, `share-demo` validates the public package and `community-publisher` can prepare a contributor fork, branch, commit, push, and pull request. It stops at the PR. Every contribution still needs maintainer manual review and merge

[Browse the demo gallery](demos/README.md) · [Read the contribution contract](docs/community-demos.md)

## Install from Claude Marketplace

```text
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-animated-infographics@mamdouh-creative-tools
```

Validate a local checkout with

```bash
claude plugin validate .
```

## What it makes

Not a generic stack of cards with movement added at the end

A strong output should have

| Part | Standard |
| --- | --- |
| **Hook** | One opening idea worth stopping for |
| **Visual idea** | One dominant concept readable at feed size |
| **WOW** | A fresh visual or motion move that serves the story |
| **AHA** | A payoff that changes understanding |
| **Story** | A clear shape such as comparison, process, transformation, proof, interface flow, or framework |
| **Color** | Creative and attractive without becoming loud |
| **Composition** | Center-first unless the content reads better another way |
| **Motion** | Deliberate, seekable, deterministic, and tied to meaning |
| **Evidence** | Claims, metrics, product states, logos, and proof tied to supplied material |
| **Finish** | Mechanical QA, critique, and independent verification |

## Creative runtime

Before story architecture starts, `creative-director` creates at least three genuinely different directions in `build/creative-concepts.json`

Each direction defines

- visual hook
- copy hook
- aha mechanic
- story shape
- Visual Style
- Story Archetype
- motion behavior
- evidence dependencies
- risks
- why the idea deserves attention

At least one direction must contain a real visual payoff, not a palette swap or a new card arrangement

The local gates are `hooked-design-copy`, `creative-payoff`, `restrained-palette`, and `center-first-composition`

## Info-stories

Info-stories separates four decisions

1. **Story House** for visual character and palette
2. **Visual Style** for composition grammar
3. **Story Archetype** for information structure
4. **Motion Pattern** for how attention moves

The source of truth is the merged registry returned by `scripts/info_stories.py::load_catalog()`

UI Mockup Stories are first-class options

- UI Storyboard
- Interface Cutaway
- Screen to Outcome
- Inside the Interface
- State Change Story
- Cursor Focus
- State Transition

Real-looking product behavior must be supported by evidence

Concept UI stays clearly identifiable when it could be mistaken for real product proof

## Exact-SVG mascots

If the user asks for a named or official mascot, the plugin uses the **exact SVG supplied by the user or attached to the task**

No silent redraw
No substitute
No lookalike

The mascot path inspects the supplied SVG, finds usable geometry, develops motion around the real asset, preserves identity, and checks the animated result against the untouched source

```bash
python3 scripts/mascot_contract.py directions
python3 scripts/mascot_contract.py check build/mascot-request.json
```

## Connected production path

Read [`helper/GUIDE.md`](helper/GUIDE.md) before choosing a workflow or worker

```text
design-study
  -> evidence-checker
  -> creative-director
  -> story-architect
  -> palette-curator
  -> copy-compressor
  -> layout-composer
  -> caption-writer
  -> artboard-builder
  -> motion-director
  -> optional mascot-animator
  -> motion-engineer
  -> render-qa
  -> post-critic
  -> story-verifier
  -> optional share-demo
```

`new-post` is the production parent workflow. `share-demo` is a separate opt-in parent workflow after verified delivery

Workers return artifacts to their parent instead of coordinating peers through hidden handoffs

## Research that ships as behavior

`research/` is part of production logic, not a reading folder

Current gates

`prose-specificity` · `voice-preservation` · `design-dials` · `structural-originality` · `reference-dna` · `contrast-discipline` · `evidence-traceability` · `bounded-verification`

Each adopted gate keeps source provenance, inspected commit SHA, local behavior, stage, severity, owners, implementation references, and tests

Upstream working copies are research inputs only and are not packaged as runtime dependencies

## Visual defaults

- Palette character: `creative-attractive-restrained`
- Composition: `center-first`
- Text contrast: `4.5:1` minimum
- State contrast: `3:1` minimum
- One dominant visual anchor at feed scale
- Motion intensity comes from the story, not from a need to animate everything

Center-first can be overridden when comprehension or fidelity improves, including tables, UI mockups, terminal surfaces, timelines, Arabic / RTL reading flow, or a documented reference-DNA decision

## Workflows

```text
/linkedin-animated-infographics:new-post    [topic or URL] [--arabic] [--mascot]
/linkedin-animated-infographics:render-gif  [path.html] [--duration 6.0] [--fps 12.5]
/linkedin-animated-infographics:qa-post     [path.html] [caption.md]
/linkedin-animated-infographics:share-demo  [build directory]
```

Programmatic routing

```bash
python3 tools/route_request.py --request "Create an animated LinkedIn infographic"
```

## Strict validation

Disconnected capability means failure

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/demo_gallery.py check
python3 scripts/validate_marketplace.py
claude plugin validate .
```

`scripts/ecosystem_doctor.py` rejects dead, undeclared, unreachable, untested, disconnected, or unsafe public modules and manifest references

CI also registers the checkout as marketplace `mamdouh-creative-tools` and installs `linkedin-animated-infographics@mamdouh-creative-tools` into a clean Claude home

## Public tools

```text
tools/story_scaffold.py
tools/composition_check.py
tools/palette_preview.py
tools/copy_slop_check.py
tools/contrast_check.py
tools/fingerprint_check.py
tools/route_request.py
scripts/demo_gallery.py
scripts/demo_submit.py
```

## Documentation

- [Architecture](docs/ecosystem.md)
- [Routing protocol](docs/routing.md)
- [Agents](docs/agents.md)
- [Skills](docs/skills.md)
- [Community demos](docs/community-demos.md)
- [Demo gallery](demos/README.md)
- [Research gates and provenance](docs/research.md)
- [Claude Marketplace](docs/marketplace.md)
- [Development and validation](docs/development.md)

Coding agents should also read [`AGENTS.md`](AGENTS.md) or [`CLAUDE.md`](CLAUDE.md)

Both point to the same helper, research, module, and validation authority

## License

MIT
