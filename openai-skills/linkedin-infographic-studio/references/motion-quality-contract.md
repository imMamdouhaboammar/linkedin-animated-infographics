# Motion quality contract

Motion starts only after the still passes `visual-quality-contract.md`.

## Story job

Every animation must explain at least one of these:

- what should I read next?
- what changed?
- where did this item travel?
- which state is active?

If an animation cannot answer one of those questions, remove it.

## Preserve the approved composition

- Do not use animation as a reason to redesign a passing still.
- Do not hide critical meaning in a state that appears for only a brief moment.
- Frame zero must be coherent and intentional.
- The final resting state must remain coherent.
- Keep the useful relationship visible long enough to understand at normal feed viewing speed.

## Motion hierarchy

Use a small number of motion behaviors with clear roles. Prefer coordinated sequencing over many independent micro-animations.

Acceptable examples include:
- staged reveal that controls reading order
- highlight shift that shows which source or state is active
- connector travel that explains movement or attribution
- comparison transition that makes a relationship easier to understand
- state change that supports the aha moment

Reject:
- constant floating or pulsing without a story job
- decorative bounce on every label
- unrelated entrance effects on every component
- motion that adds clutter to an already dense layout
- movement that distracts from the primary takeaway

## Timing and pacing

- Give the hook enough time to register before the first meaningful change.
- Do not make all elements enter at once.
- Avoid long inactive tails that make the GIF feel unfinished.
- Keep repeated loops deterministic and visually clean at the seam.
- Use easing consistently unless a specific physical or editorial effect requires another behavior.

## Final motion critique

Before delivery, inspect:
- whether motion improves comprehension
- whether reading order is clear
- whether any text becomes harder to read while moving
- whether the visual anchor remains dominant
- whether the loop seam is distracting
- whether the animation duration feels proportionate to the amount of information

Return `motion-on-weak-still` as FAIL if the composition should have been redesigned before animation.
Return `decorative-motion` as FAIL when the majority of motion has no explanatory role.

Maximum two targeted motion repair attempts before HOLD or FAIL.
