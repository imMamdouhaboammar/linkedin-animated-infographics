<div align="center">

# LinkedIn Animated Infographics

**Turn evidence into a visual story with a sharp hook, a memorable reveal, and motion that earns its place**

`Claude Code Plugin 3.0.0` · `1080×1350` · `Info-stories` · `UI stories` · `Exact-SVG mascots` · `Arabic / RTL`

<br>

<a href="./assets/demo_artboard_v4.gif">
  <img src="./assets/demo_artboard_v4.gif" alt="Animated LinkedIn infographic demo generated with the plugin" width="720">
</a>

<sub>Live 1080×1350 demo · click the animation to open it full size</sub>

</div>

## The idea

**WOW gets the scroll to stop  
AHA makes the idea click**

This plugin is built to earn both

The **WOW moment** comes from a strong concept, distinctive composition, confident color, a clear visual anchor, and motion with timing and purpose

The **AHA moment** comes when the visual changes understanding through a reveal, comparison, relationship, transformation, state change, interface sequence, or another useful payoff

If an effect looks impressive but does not make the idea clearer, more memorable, or easier to understand, it does not count as the payoff

That principle is enforced before layout by the `creative-director`, then checked again through story, layout, motion, review, and verification

## Install from Claude Marketplace

```text
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-animated-infographics@mamdouh-creative-tools
```

The marketplace and plugin live in this repository

Validate a local checkout with

```bash
claude plugin validate .
```

## What the plugin is trying to make

Not another generic card stack with animated decoration

A finished post should have

| Job | What the plugin looks for |
| --- | --- |
| **Hook** | A headline or opening frame that earns attention through specificity, tension, outcome, recognition, or useful surprise |
| **Visual idea** | One dominant concept that the reader can understand at feed scale |
| **WOW moment** | A visual or motion payoff that feels fresh without becoming excessive |
| **AHA moment** | A reveal that adds understanding instead of simply adding movement |
| **Story shape** | A deliberate sequence such as comparison, transformation, state change, process, interface story, proof view, or framework |
| **Color** | Creative, attractive, restrained palettes with enough character to feel designed |
| **Composition** | Center-first by default, with alignment exceptions only when content, fidelity, or reading order benefits |
| **Motion** | Seekable, deterministic movement tied to meaning rather than constant activity |
| **Evidence** | Claims, product states, metrics, logos, and proof tied back to supplied material |
| **Finish** | Mechanical QA, adversarial critique, and independent verification before delivery |

## Creative runtime

Before story architecture hardens, `creative-director` produces at least three genuinely different directions in `build/creative-concepts.json`

Each direction defines

- visual hook
- copy hook
- aha mechanic
- story shape
- recommended Visual Style
- recommended Story Archetype
- recommended motion behavior
- evidence dependencies
- risks
- why the direction earns attention

At least one direction must contain a useful visual payoff rather than a palette variation or decorative treatment

The local creative gates include `hooked-design-copy`, `creative-payoff`, `restrained-palette`, and `center-first-composition`

## Info-stories

Info-stories separates four decisions that are often mixed together

1. **Story House** for the visual language and palette character
2. **Visual Style** for composition grammar
3. **Story Archetype** for the information structure
4. **Motion Pattern** for how attention moves through the story

The source of truth is the merged registry returned by `scripts/info_stories.py::load_catalog()`

UI Mockup Stories are first-class story options, including

- UI Storyboard
- Interface Cutaway
- Screen to Outcome
- Inside the Interface
- State Change Story
- Cursor Focus
- State Transition

Real-looking product behavior stays evidence-backed, while concept UI is identified when readers could mistake it for documented product behavior

## Exact-SVG mascots

Named or official mascots use the **exact SVG supplied by the user or attached to the task**

The plugin does not silently redraw, approximate, replace, or generate a lookalike

The mascot path inspects the supplied SVG, finds addressable geometry, develops a communication-led motion direction, preserves the source identity, integrates the animation, and checks the result against the untouched asset

```bash
python3 scripts/mascot_contract.py directions
python3 scripts/mascot_contract.py check build/mascot-request.json
```

## The connected production path

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
```

`new-post` is the parent workflow

Workers return bounded artifacts to the parent instead of coordinating peers through hidden handoffs

## Research that actually runs

The `research/` directory is active production guidance rather than background reading

Current runtime gates

`prose-specificity` · `voice-preservation` · `design-dials` · `structural-originality` · `reference-dna` · `contrast-discipline` · `evidence-traceability` · `bounded-verification`

Each adopted gate keeps source provenance, inspected commit SHA, local behavior, stage, severity, real owners, implementation references, and tests

Upstream working copies are research inputs only and are not packaged as runtime dependencies

## Visual defaults

- Palette character: `creative-attractive-restrained`
- Composition: `center-first`
- Text contrast: `4.5:1` minimum for meaningful text
- State-defining contrast: `3:1` minimum
- One dominant visual anchor at feed scale
- Motion intensity resolved from the story rather than added by default

Center-first can be overridden when comprehension or fidelity genuinely improves, including tables, UI mockups, terminal surfaces, timelines, Arabic / RTL reading flow, or a documented reference-DNA decision

## Workflows

```text
/linkedin-animated-infographics:new-post    [topic or URL] [--arabic] [--mascot]
/linkedin-animated-infographics:render-gif  [path.html] [--duration 6.0] [--fps 12.5]
/linkedin-animated-infographics:qa-post     [path.html] [caption.md]
```

Programmatic routing

```bash
python3 tools/route_request.py --request "Create an animated LinkedIn infographic"
```

## Strict validation

The repository treats disconnected capabilities as failures rather than documentation debt

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tools skills/svg-mascot-animator/scripts
python3 scripts/info_stories.py check
python3 scripts/ecosystem_router.py check
python3 scripts/research_gates.py check
python3 scripts/plugin_graph.py check
python3 scripts/ecosystem_doctor.py check
python3 scripts/validate_marketplace.py
claude plugin validate .
```

`scripts/ecosystem_doctor.py` rejects dead, undeclared, unreachable, untested, disconnected, or unsafe public modules and manifest references

CI also registers the checked-out repository as marketplace `mamdouh-creative-tools` and installs `linkedin-animated-infographics@mamdouh-creative-tools` into a clean Claude home

## Public tools

```text
tools/story_scaffold.py
tools/composition_check.py
tools/palette_preview.py
tools/copy_slop_check.py
tools/contrast_check.py
tools/fingerprint_check.py
tools/route_request.py
```

## Documentation

- [Architecture](docs/ecosystem.md)
- [Routing protocol](docs/routing.md)
- [Agents](docs/agents.md)
- [Skills](docs/skills.md)
- [Research gates and provenance](docs/research.md)
- [Claude Marketplace](docs/marketplace.md)
- [Development and validation](docs/development.md)

Coding agents should also read [`AGENTS.md`](AGENTS.md) or [`CLAUDE.md`](CLAUDE.md)

Both point back to the same helper, research, module, and validation authority

## License

MIT
