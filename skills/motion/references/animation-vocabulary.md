# Standardized Animation Vocabulary & Reverse-Lookup Glossary

A reverse-lookup glossary mapping sensations, visual descriptions, and physics behaviors to their authoritative industry motion terms.

---

## 1. Entrances & Exits
- **Scale In**: Element grows from a smaller scale (e.g. `scale(0.95)`) to full size while fading in. Never starts from `scale(0)`.
- **Pop In**: Element appears with a slight `back.out` overshoot and settles into place.
- **Reveal**: Content is uncovered progressively along an axis, typically via `clip-path: inset()`.
- **Slide In**: Element enters along X or Y from an offset position.

## 2. Sequencing & Timing
- **Stagger**: Animating multiple items one after another with a small delay (30–60ms) between each.
- **Orchestration**: Deliberately coordinating timelines, delays, and eases so multiple animations feel like one harmonic movement.
- **Keyframes**: Interpolated boundary states within a single animation loop.

## 3. Physicality & Transforms
- **Origin-Aware Animation**: An element animates out of its trigger anchor (e.g. popover expanding from the clicked button) rather than an arbitrary center.
- **3D Tilt / Flip**: Rotations along the X and Y axes (`rotateX`, `rotateY`) within a `perspective` container.
- **Asymmetric Easing**: Separate acceleration curves for entry vs. exit (e.g. deliberate press, snappy response).

## 4. State Transitions & Morphs
- **Morph**: One shape smoothly transitions into another shape (e.g. pill into menu, button into progress indicator).
- **Shared Element Transition**: An element travels and resizes from one layout position to another.
- **Continuity Transition**: Maintaining spatial awareness between states by animating geometry rather than cutting.

## 5. Physics & Springs
- **Spring**: Motion driven by tension, mass, and damping rather than fixed durations.
- **Damping Ratio ($\zeta$)**: Controls oscillation and bounce (`1.0` = critically damped, `0.8` = subtle bounce).
- **Rubber-Banding**: Resistance and snap-back when dragging past a natural boundary.
- **Momentum Projection**: Projecting velocity forward to determine natural deceleration resting points.
- **Interruptibility**: The ability to redirect an active animation mid-flight from its current presentation value without jumping.

## 6. Ambient & Idle Motion
- **Sine Breathing**: Subtle harmonic oscillation on scale or position simulating breath.
- **Orbit**: An element traveling along an elliptical trajectory around a central anchor.
- **Sheen / Glow Pulse**: Traveling specular sweep or soft radial illumination.
