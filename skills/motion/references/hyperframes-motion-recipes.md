# HyperFrames Motion Recipes & Blueprint Catalog

A comprehensive catalog of seekable, deterministic motion recipes and scene blueprints adapted from HyperFrames (`https://github.com/heygen-com/hyperframes`) for 1080x1350 LinkedIn animated infographics.

---

## 1. The Core Deterministic Motion Contract

Every animation implemented in this system MUST satisfy:

1. **One Loop Clock**: All durations derive from a single root variable (`--loop: 4800ms` or a paused master timeline). Sub-animations use integer divisions (`--loop / 2`, `--loop / 4`).
2. **Deterministic & Seek-Safe**: No `Math.random()`, `Date.now()`, or `performance.now()`. Use index-derived pseudo-random hashes and finite repeats. Every frame must be a pure function of timeline time `t`.
3. **Transform & Paint Only**: Animate `transform` (`translate`, `scale`, `rotate`), `opacity`, `color`, `background-color`, `stroke-dashoffset`. Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`).
4. **Frame 0 Completeness**: Frame 0 (t = 0) must always present a complete, fully legible static infographic.
5. **Clean Loop Closure**: The visual state at `t = --loop` (or 100%) must seamlessly match `t = 0` (seam ratio ≤ x1.25).
6. **Changed-Pixel Budget Discipline**:
   - Dark flat ground: changed pixels < 2.0% per frame.
   - Light textured ground: changed pixels < 0.5% per frame.
   - Avoid animating `filter: blur()`, `backdrop-filter`, or large `box-shadow` spreads on large surfaces.
7. **Stagger Cap**: Total group stagger duration must be ≤ 0.4s to ensure arrival reads as a unified beat rather than sluggish individual pops.

---

## 2. Atomic Motion Recipes (The Essential Primitives)

### Recipe 1: Kinetic Beat Slam (Typography)
High-impact rhythmic headline arrival where words slam into place with scale-down overshoot and settle.

```css
@keyframes beatSlam {
  0% { opacity: 0; transform: scale(1.6) translateY(-20px); }
  15% { opacity: 1; transform: scale(0.96) translateY(2px); }
  25%, 85% { opacity: 1; transform: scale(1) translateY(0); }
  100% { opacity: 0; transform: scale(1); }
}
.headline-word {
  display: inline-block;
  animation: beatSlam var(--loop) cubic-bezier(0.16, 1, 0.3, 1) infinite;
}
.word-1 { animation-delay: calc(var(--loop) * 0.00); }
.word-2 { animation-delay: calc(var(--loop) * 0.08); }
.word-3 { animation-delay: calc(var(--loop) * 0.16); }
```

### Recipe 2: SVG Path Draw-On (Connectors & Outlines)
Connector lines, pipeline arrows, or icon contours that draw themselves smoothly along a vector path.

```css
.draw-path {
  stroke-dasharray: var(--path-len, 400);
  stroke-dashoffset: var(--path-len, 400);
  animation: pathDraw var(--loop) cubic-bezier(0.25, 1, 0.5, 1) infinite;
}
@keyframes pathDraw {
  0%, 10% { stroke-dashoffset: var(--path-len, 400); }
  40%, 85% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: 0; }
}
```

### Recipe 3: Dynamic Counter & Scale Surge (Data & Metrics)
A numerical stat counts up while subtly scaling to punctuate escalating magnitude.

```html
<div class="stat-container">
  <span class="stat-number" id="kpi-counter">0</span>
  <span class="stat-unit">%</span>
</div>
<script>
  // In deterministic GSAP seekable timeline:
  const counterObj = { val: 0 };
  tl.to(counterObj, {
    val: 98,
    duration: 1.2,
    ease: "power3.out",
    onUpdate: () => {
      document.getElementById("kpi-counter").textContent = Math.round(counterObj.val);
    }
  }, 0.2);
  tl.fromTo(".stat-container", 
    { scale: 0.85, opacity: 0 },
    { scale: 1.08, opacity: 1, duration: 0.6, ease: "back.out(1.6)" },
    0.2
  ).to(".stat-container", { scale: 1.0, duration: 0.6, ease: "power2.out" }, 0.8);
</script>
```

### Recipe 4: Anchored Layout Expand (Cards & Accordions)
Container expands vertically without triggering layout reflow by using scale transforms and synchronous sibling push.

```css
.expandable-panel {
  transform-origin: top center;
  animation: panelExpand var(--loop) cubic-bezier(0.16, 1, 0.3, 1) infinite;
}
@keyframes panelExpand {
  0%, 15% { transform: scaleY(0.4); opacity: 0.8; }
  35%, 85% { transform: scaleY(1.0); opacity: 1.0; }
  100% { transform: scaleY(0.4); opacity: 0.8; }
}
```

### Recipe 5: Spring-Pop Entrance (Feature Cards & Badges)
Elements pop in with clean, crisp `back.out` overshoot.

```css
@keyframes springPop {
  0% { transform: scale(0.3); opacity: 0; }
  25% { transform: scale(1.06); opacity: 1; }
  35%, 85% { transform: scale(1.0); opacity: 1; }
  100% { transform: scale(0.3); opacity: 0; }
}
.badge-item {
  animation: springPop var(--loop) cubic-bezier(0.34, 1.56, 0.64, 1) infinite;
}
```

### Recipe 6: 3D Split-Tilt Cards (Comparison / Before-After)
Paired comparison cards tilt along the Y axis in opposite directions like an open book, creating spatial depth.

```css
.card-perspective-stage {
  perspective: 1200px;
}
.card-left {
  transform: rotateY(12deg) rotateX(4deg);
  animation: floatLeft var(--loop) ease-in-out infinite;
}
.card-right {
  transform: rotateY(-12deg) rotateX(4deg);
  animation: floatRight var(--loop) ease-in-out infinite;
}
@keyframes floatLeft {
  0%, 100% { transform: rotateY(12deg) translateY(0); }
  50% { transform: rotateY(16deg) translateY(-8px); }
}
@keyframes floatRight {
  0%, 100% { transform: rotateY(-12deg) translateY(0); }
  50% { transform: rotateY(-16deg) translateY(-8px); }
}
```

### Recipe 7: Chart Scrub Playhead & Value Tooltip (Interactive Dataviz)
A vertical tracking playhead sweeps across a data polyline while the readout tooltip updates synchronously.

```javascript
// Synchronous scrub along polyline
const scrubProxy = { progress: 0 };
tl.to(scrubProxy, {
  progress: 1,
  duration: 2.0,
  ease: "power2.inOut",
  onUpdate: () => {
    const x = 100 + scrubProxy.progress * 400; // X range across chart
    gsap.set(".playhead-line", { x: x });
    gsap.set(".chart-tooltip", { x: x, y: calculatePolylineY(scrubProxy.progress) });
  }
}, 0.5);
```

### Recipe 8: Deterministic Ballistic Particle Burst (Celebration / Milestone)
Punctuation burst where particles fly outward on pseudo-random deterministic trajectories.

```javascript
function hash(i) {
  let n = i * 374761393;
  n = (n ^ (n >> 13)) * 1274126177;
  return ((n ^ (n >> 16)) & 0x7fffffff) / 0x7fffffff;
}

const particles = [];
for (let i = 0; i < 24; i++) {
  const angle = hash(i * 3 + 1) * Math.PI * 2;
  const distance = 40 + hash(i * 3 + 2) * 80;
  const dx = Math.cos(angle) * distance;
  const dy = Math.sin(angle) * distance;
  
  tl.fromTo(`.particle-${i}`,
    { x: 0, y: 0, scale: 1, opacity: 1 },
    { x: dx, y: dy + 20, scale: 0, opacity: 0, duration: 0.8, ease: "power2.out" },
    1.4
  );
}
```

---

## 3. Narrative Scene Blueprints for Infographics

| Blueprint ID | Story Role | Signature Move | Best Fit Infographic Structure |
|---|---|---|---|
| `kinetic-type-beats` | Hook / Value Prop | Punchy word swap & scale slam | Signal Sheet, Hero Headline, Summary Takeaway |
| `prompt-type-submit-generate` | Workflow / Demo | Terminal prompt typing → live artifact generation | Command Canvas, Working Screen, 1-Prompt Workflow |
| `dataviz-countup` | Hook / Proof | Exploding metric count-up + gauge fill | Stack Ledger, KPI Summary, Impact Proof |
| `constellation-hub` | Architecture | Orbiting satellite tools spring around core hub | Ecosystem Snapshot, Hub & Spoke, Tool Catalog |
| `grid-card-assemble` | Breadth / Features | Staggered 3D cascade into clean aligned grid | Proof Mosaic, Comparison Grid, Feature Specimen |
| `agent-progress-theater` | Key Feature | Step items cycle, check off, and highlight status | Pipeline Stages, Step-by-Step Playbook |
| `comparison-split` | Problem / Comparison | Mirrored 3D book-tilt cards with badge pop | Before/After Workflow, Decision Cards |
| `cta-morph-press` | Call-to-Action | Hero widget condenses into button + cursor tactile press | Cheat Sheet Poster, Final Verdict, Action Footer |

---

## 4. Easing Selection Matrix

| Motion Intent | GSAP Easing | CSS Bezier Equivalent | Feel & Context |
|---|---|---|---|
| **Sharp UI Arrival** | `power3.out` / `power4.out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Crisp, high-end, responsive feel for cards and badges |
| **Tactile Overshoot** | `back.out(1.4 - 1.7)` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful, mechanical spring for icons, chips, and pills |
| **Organic Breathing** | `sine.inOut` | `cubic-bezier(0.37, 0, 0.63, 1)` | Subtle ambient floating, node pulsing, and sheens |
| **Mechanical Step** | `steps(n)` | `steps(n, jump-none)` | Terminal cursor blink, stepped tickers, discrete state swaps |
| **Linear Progression** | `none` | `linear` | Continuous progress bars, SVG dash offsets, radar sweeps |
