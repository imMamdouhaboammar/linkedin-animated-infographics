# svg-mascot-animator

Static SVG in, animation out, with the timing coming from equations and solvers rather than
from nudged keyframes.

Anime.js v4 is the default engine for runtime contexts. Where JavaScript cannot run, the same
solvers are sampled ahead of time and baked into CSS keyframes, so both versions of an asset
share one motion identity.

## Install

```bash
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install svg-mascot-animator@linkedin-animated-infographics
```

## Note on the two tracks

**Runtime track** for docs sites, landing pages, product UI, and anything reacting to scroll,
hover, or state.

**Static track** for README images, badges, and anything loaded through `<img>`, where
scripting never executes.

If you are animating a mascot for a **LinkedIn infographic**, use the static track only, and
install `linkedin-motion` alongside this. That plugin's renderer seeks animations frame by
frame, and runtime motion cannot be seeked.

MIT licensed.
