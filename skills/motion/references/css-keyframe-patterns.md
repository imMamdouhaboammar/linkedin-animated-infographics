# CSS Animations & Keyframe Mechanisms Catalog

A comprehensive guide for authoring pure CSS `@keyframes`, hardware-accelerated compositor animations, CSS variable staggers, and deterministic timing rules adapted for LinkedIn animated infographics.

---

## 1. The CSS Keyframe Deterministic Contract

Pure CSS animations in this system run off the main thread directly on the GPU compositor, providing stutter-free performance during render capture:

1. **One Loop Clock**: All durations derive from root variable `--loop: 4800ms`. Sub-animations use integer fractions (`calc(var(--loop) / 2)`).
2. **Animation Fill Mode**: Always use `animation-fill-mode: both` so initial (0%) and terminal (100%) states are firmly locked.
3. **Finite / Exact Iteration Counts**: For infographics, animations must complete exact cycles within the total duration.
4. **Compositor Properties Only**: Animate `transform`, `opacity`, `filter`, and `clip-path`. Never animate layout properties (`width`, `height`, `margin`, `padding`, `top`, `left`).
5. **No CSS `transition` on Animated Elements**: Never mix CSS `transition` with `@keyframes` on the same element to avoid interpolation desynchronization during frame capture.

---

## 2. CSS Variable-Driven Staggers

Instead of writing separate `@keyframes` for each child, use index variables:

```html
<div class="card-grid">
  <div class="card" style="--i: 0;">1. Input Stage</div>
  <div class="card" style="--i: 1;">2. Core Engine</div>
  <div class="card" style="--i: 2;">3. Artifact Output</div>
</div>

<style>
.card {
  opacity: 0;
  transform: translateY(12px) scale(0.96);
  animation: cardEntrance var(--loop) cubic-bezier(0.16, 1, 0.3, 1) infinite;
  animation-delay: calc(var(--i) * 80ms);
}

@keyframes cardEntrance {
  0%, 10% { opacity: 0; transform: translateY(12px) scale(0.96); }
  25%, 85% { opacity: 1; transform: translateY(0) scale(1); }
  100% { opacity: 0; transform: translateY(12px) scale(0.96); }
}
</style>
```

---

## 3. Pure CSS Micro-Motif Recipes

### Recipe 1: Pulse Ring (Radar / Active Beacon)
Pulsing radar ring behind an active tool icon or focal node:

```css
.pulse-beacon {
  position: relative;
  width: 56px;
  height: 56px;
}
.pulse-beacon::before {
  content: "";
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  animation: beaconPulse var(--loop) cubic-bezier(0.2, 0, 0, 1) infinite;
}
@keyframes beaconPulse {
  0% { transform: scale(0.8); opacity: 0; }
  25% { opacity: 0.8; }
  50%, 100% { transform: scale(1.4); opacity: 0; }
}
```

### Recipe 2: Specular Shimmer Sweep (Premium Glass Header)
Traveling light sheen across a badge or card header without triggering layout redraw:

```css
.shimmer-badge {
  position: relative;
  overflow: hidden;
}
.shimmer-badge::after {
  content: "";
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.25) 50%,
    transparent 100%
  );
  animation: shimmerSweep var(--loop) cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
@keyframes shimmerSweep {
  0%, 20% { transform: translateX(-100%); }
  45%, 100% { transform: translateX(100%); }
}
```

### Recipe 3: Stepped Terminal Cursor Blink
Discrete square-wave cursor blink using `steps(1)`:

```css
.terminal-cursor {
  display: inline-block;
  width: 10px;
  height: 20px;
  background-color: var(--accent);
  animation: cursorBlink 800ms steps(1) infinite;
}
@keyframes cursorBlink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
```

### Recipe 4: Parent/Child Counter-Transform (Anti-Warp Layout Scaling)
Expands a container vertically while maintaining clean aspect ratio of internal icons:

```css
.accordion-wrapper {
  transform-origin: top center;
  animation: wrapperScale var(--loop) cubic-bezier(0.16, 1, 0.3, 1) infinite;
}
.accordion-wrapper .icon-fixed {
  transform-origin: center;
  animation: iconCounterScale var(--loop) cubic-bezier(0.16, 1, 0.3, 1) infinite;
}
@keyframes wrapperScale {
  0%, 15% { transform: scaleY(0.5); opacity: 0.7; }
  35%, 85% { transform: scaleY(1.0); opacity: 1.0; }
  100% { transform: scaleY(0.5); opacity: 0.7; }
}
@keyframes iconCounterScale {
  0%, 15% { transform: scaleY(2.0); } /* Inverse of 0.5 */
  35%, 85% { transform: scaleY(1.0); }
  100% { transform: scaleY(2.0); }
}
```

---

## 4. Keyframe Mechanism Selection Matrix

| Need | Mechanism | Keyframe Channels |
|---|---|---|
| Vector Connector Growth | SVG Dash Offset | `stroke-dashoffset: 400` → `0` |
| Component Reveal | Clip-Path Inset | `clip-path: inset(0 100% 0 0)` → `inset(0 0 0 0)` |
| Card / Badge Pop | Transform Scale | `scale(0.95)` → `scale(1.04)` → `scale(1.0)` |
| Step Hierarchy / Sequence | Indexed CSS Vars | `animation-delay: calc(var(--i) * 60ms)` |
| Active Tool Pulse | Radar Border | `scale(0.8)` → `scale(1.3)` + `opacity: 0` |
| 3D Perspective Card | Preserve-3D Stage | `rotateY(14deg)` → `rotateY(0deg)` |
