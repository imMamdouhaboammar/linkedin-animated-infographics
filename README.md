# linkedin-animated-infographics

A Claude Code plugin marketplace for the animated-infographic post format.

Two plugins. One turns a topic into a LinkedIn post that ships as a caption plus a
1080x1350 looping GIF infographic. The other turns a static SVG mascot into
physics-driven animation.

The marketplace and the repository share a name; the plugins inside are named separately so
the skills you type stay short. Installing looks like this:

```
linkedin-motion @ linkedin-animated-infographics
   ↑ plugin           ↑ marketplace
```

and the skills come out as `/linkedin-motion:new-post`, not
`/linkedin-animated-infographics:new-post`.

## Install

```bash
/plugin marketplace add imMamdouhaboammar/linkedin-animated-infographics
/plugin install linkedin-motion@linkedin-animated-infographics
/plugin install svg-mascot-animator@linkedin-animated-infographics
```

Then, once per machine:

```bash
bash ~/.claude/plugins/cache/linkedin-animated-infographics/linkedin-motion/*/scripts/setup.sh
```

Plugin names are the skill namespace, so `linkedin-motion` is what you type. The marketplace
name is only used at install time.

That installs Playwright and a Chrome binary and checks for ffmpeg. Everything else runs on
plain Python 3.

## Plugins

### `linkedin-motion`

Ship a LinkedIn post end to end. The output is a caption written to one of seven archetypes
and a GIF rendered deterministically from HTML through seeked headless Chrome.

The thesis: these posts are **static infographics with a small fraction of the canvas
moving**, and that motion is a **reading pointer** guiding the eye in the order the author
wants. Everything else is frozen. That is why they look expensive.

**Skills**

| Skill | Covers |
|---|---|
| `post` | the router. Pipeline, non-negotiables, working method |
| `caption` | 7 caption archetypes, the truncation cut, hook and CTA libraries, the ban list |
| `artboard` | 13 layout archetypes, the House 0 palette, type scale, offline fonts |
| `motion` | 10 seekable primitives, the one-loop-clock rule, the reverse-delay trap |
| `mascots` | 3 mascot roles, the seek-safe rig, motion budgeting, archetype compatibility |
| `render` | capture, GIF assembly with size budgeting, every QA gate, publishing |
| `arabic` | RTL mirroring, the Arabic type scale, bidi isolation, caption rhythm |

**Workflows** (user-invoked)

```
/linkedin-motion:new-post    [topic or URL] [--arabic] [--mascot]
/linkedin-motion:render-gif  [path.html] [--duration 6.0] [--fps 12.5]
/linkedin-motion:qa-post     [path.html] [caption.md]
```

**Agents**

| Agent | Does |
|---|---|
| `caption-writer` | writes the caption, enforces the ban list, verifies every number |
| `artboard-builder` | builds the still until it passes `check_render.py` |
| `motion-engineer` | adds exactly two primitives and makes the loop close |
| `render-qa` | renders and judges, read-only, so the render noise stays off the main thread |
| `post-critic` | red-teams the finished post before it ships |

**Hook.** A `PostToolUse` lint runs on any HTML file containing an `#artboard`. It catches the
three failures that otherwise cost a full render: `requestAnimationFrame` motion that cannot be
seeked, a webfont loading over the network, and a missing or wrongly-sized artboard element.

### `svg-mascot-animator`

Static SVG in, animation out, with timing from equations and solvers rather than nudged
keyframes. Anime.js v4 for runtime pages; baked CSS keyframes for README and docs assets, so
both versions of an asset share one motion identity.

## Why physics.py is vendored twice

`linkedin-motion/scripts/physics.py` is a copy of the file in `svg-mascot-animator`. Claude
Code copies each plugin to its own cache directory on install, so a cross-plugin relative path
would not resolve at runtime. `linkedin-motion/scripts/sync_physics.sh` refreshes the copy and
tells you when it had drifted.

## Development

```bash
claude --plugin-dir ./plugins/linkedin-motion
claude plugin validate .
claude plugin validate ./plugins/linkedin-motion
```

Then `/reload-plugins` to pick up edits without restarting.

## Migrating from the standalone skill

This repository previously held `linkedin-animated-infographics` as a single loose skill:
`SKILL.md`, `references/`, `scripts/`, and `assets/` at the root. That layout still works if
you drop it in `~/.claude/skills/`, but it is superseded here.

Remove the old copy from `~/.claude/skills/linkedin-animated-infographics/` after installing
the plugin. Both can load at once, and a stale copy of the reference files is the kind of
thing that costs an hour when the two disagree.

The plugin is the same body of work, split so each stage loads on its own:

| Before | Now |
|---|---|
| one 300-line `SKILL.md` | `post` router plus six focused skills |
| `references/caption-patterns.md` | `skills/caption/` |
| `references/visual-archetypes.md`, `design-systems.md` | `skills/artboard/` |
| `references/animation-recipes.md` | `skills/motion/` |
| `references/mascots.md` | `skills/mascots/` |
| `references/qa-gates.md`, `production-pipeline.md`, `publishing-playbook.md` | `skills/render/` |
| `references/arabic-rtl.md` | `skills/arabic/` |
| running the pipeline by hand | `/linkedin-motion:new-post` plus five agents |

## Renaming later

A plugin's `name` is its stable identifier. Users reference it in `enabledPlugins` and in
`/plugin install`, so changing it after publishing breaks every existing install. If you ever
do need to change one, add a top-level `renames` map to `marketplace.json` mapping the old name
to the new one, and treat that map as append-only history.

Nothing here is published yet, so now is the free moment to settle the names.

## Credits

Built by **Mamdouh Aboammar**, Managing Partner at Momint, founder of PrePilot.cloud and
OpenOps Studio.

The mascot layer takes its physics and rig from
[vibe-svgs](https://github.com/imMamdouhaboammar/vibe-svgs). The seek-safety discipline follows
the same reasoning as HeyGen's HyperFrames keyframe layer: motion a renderer has to seek must
be authored so it can be seeked, not recorded.

The archetypes were derived by analysing publicly posted LinkedIn content. They describe
structure, not content. No third-party text or design is redistributed here.

MIT licensed.
