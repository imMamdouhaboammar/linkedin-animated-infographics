# Upstream capability adoption matrix

The upstream repositories are research inputs, not bundled runtime dependencies. Their working copies live under ignored `research/upstreams/`. Product-facing rules are independently worded and tested locally.

| Capability | stop-slop | no-ai-slop | taste-skill | Hallmark | COG | Local implementation |
|---|---|---|---|---|---|---|
| Named prose-pattern detection | strong | strong | medium | medium | - | anti-slop gates + copy-compressor |
| Voice preservation | medium | strong | medium | medium | - | copy-compressor |
| Structural diversity | - | - | strong | strong | - | story-architect + layout-composer |
| Explicit density/motion/variance | - | - | strong | medium | - | story brief design dials |
| Reference DNA study | - | - | medium | strong | - | design-study + study protocol |
| Token discipline and contrast | - | - | strong | strong | - | palette-curator + catalog validator |
| Honest facts / no fake metrics | medium | strong | strong | strong | medium | evidence-checker + post-critic |
| Independent verifier | - | - | - | medium | strong | story-verifier |
| Bounded fix loop | - | - | - | medium | strong | verification-loop |
| Evidence traceability | - | - | - | medium | strong | verifier evidence rows |

## Deliberate exclusions

- No frontend framework prescriptions are imported
- No mandatory GSAP, scroll hijacking, dark mode, navigation, form, or responsive-site rules are imported
- No random aesthetic selection is used
- No paid-template or signature-work cloning is supported
- No upstream repository is packaged with the plugin
