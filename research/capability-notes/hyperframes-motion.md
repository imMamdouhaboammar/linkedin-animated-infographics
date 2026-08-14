# HyperFrames Motion Capability & Adoption Note

## Overview

HyperFrames (`https://github.com/heygen-com/hyperframes`) provides a production-grade motion framework based on single paused GSAP timelines, deterministic frame-by-frame rendering, and atomic motion rules.

This note documents how HyperFrames animation techniques, atomic motion recipes, and multi-phase scene blueprints are adopted and adapted into the LinkedIn Animated Infographics plugin ecosystem.

---

## Architectural Alignment

| HyperFrames Principle | LinkedIn Animated Infographics Adaptation | Status |
|---|---|---|
| **Single Paused Timeline** | Uses single `--loop` clock in CSS / single seekable timeline in GSAP / WAAPI | **ADOPTED** |
| **Deterministic Rendering** | Zero `Math.random()`, zero `Date.now()`, pseudo-random hash functions, quantized time sampling | **ADOPTED** |
| **Transform & Paint Only** | Spatial movement strictly via `transform` (`x`, `y`, `scale`, `rotate`); layout properties (`top`, `left`, `width`, `height`) forbidden | **ADOPTED** |
| **Frame 0 Completeness** | Frame 0 must always be a complete, readable still infographic before motion begins | **ADOPTED** |
| **Loop Closure (Seam ≤ x1.25)** | 0% and 100% states must be identical; seam ratio measured by `build_gif.py` | **ADOPTED** |
| **Changed-Pixel Budget Discipline** | Mean changed pixels per frame < 2.0% (dark ground) or < 0.5% (light ground); avoid large blur / backdrop-filter | **ADOPTED** |
| **1080x1350 Vertical Aspect Ratio** | Infographic canvas fixed at 1080x1350 with 48px outer safe margin | **ADOPTED** |

---

## Adopted Capabilities

### 1. Atomic Motion Recipes (48 Rules)
- **Kinetic Typography**: `kinetic-beat-slam`, `hacker-flip-3d` (character decryption), `gradient-text-sweep` (`background-clip: text`), `context-sensitive-cursor`, `vertical-spring-ticker`.
- **Data & Analytics**: `counting-dynamic-scale` (counter scale growth with value), `stat-bars-and-fills` (scaleY/scaleX stagger), `chart-scrub-readout` (tracking line + dynamic tooltip).
- **Layout & Structure**: `center-outward-expansion`, `anchored-layout-expand` (container expansion without layout reflow), `split-tilt-cards` (3D perspective book-tilt), `avatar-cloud-network`.
- **SVG & Micro-Animation**: `svg-path-draw` (`stroke-dasharray` / `stroke-dashoffset`), `svg-icon-enrichment` (explicit center rotations via `setAttribute('transform', 'rotate(deg cx cy)')`).
- **Tactile Physics**: `spring-pop-entrance` (`back.out` overshoot), `press-release-spring` (tactile button compression & recovery), `control-target-sync`.
- **Ambient & Punctuation**: `sine-wave-loop` (breathing idle loops), `particle-burst` (deterministic ballistic confetti/dots).

### 2. Multi-Phase Scene Blueprints (22 Blueprints)
Mapped to LinkedIn infographic narrative roles:
- **Hook**: `kinetic-type-beats`, `prompt-type-submit-generate`, `dataviz-countup`, `typewriter-reveal`.
- **Problem / Pain Point**: `overwhelm-surround`, `comparison-split`, `ticker-takeover`.
- **Product Intro / Architecture**: `constellation-hub`, `grid-card-assemble`, `device-surface-showcase`.
- **Workflow / Key Feature**: `agent-progress-theater`, `panel-edit-live-sync`, `transcript-scroll-artifact-reveal`.
- **Payoff & CTA**: `cta-morph-press`, `logo-assemble-lockup`, `titlecard-reveal`.

---

## Deliberate Exclusions & Adaptations

1. **No Unbounded Video / Audio Sync**: Audio-reactive motion is adapted to pre-baked deterministic visual rhythm curves rather than live microphone/audio feeds.
2. **No Layout Property Tweens**: Tweens on `width`, `height`, `top`, `left`, `margin` are strictly blocked. Use scale/translate proxies or `anchored-layout-expand`.
3. **No Heavy Full-Canvas Blur Filters**: Large `filter: blur()` or `backdrop-filter` animations defeat GIF frame diffing and multiply payload size; replaced by opacity fades and localized transform masks.
