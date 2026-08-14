# Project Learnings: LinkedIn Animated Infographics Multi-Agent Engine

**Date:** 2026-08-14  
**Author:** AI Systems Engineer & Master Orchestrator  
**Status:** Canonical & Active

---

## 1. Executive Summary
This document synthesizes the architectural decisions, design physics, model delegation strategies, and watchdog supervision patterns established for the **LinkedIn Animated Infographics** ecosystem. It serves as the durable knowledge base for building, reviewing, and automating high-impact visual infographics.

---

## 2. Key Decisions & Rationale

| Architectural Decision | Chosen Implementation | Core Rationale |
| :--- | :--- | :--- |
| **Front-Door Protocol** | Mandatory `masterone` first-pass | Prevents repeated onboarding questions; keeps project preferences (`.linkedin-infographics/profile.json`) persistent and clean. |
| **Model Tier Delegation** | `pro` / GPT-5.6 Sol for high-reasoning tasks; `flash` for microcopy & QA | Optimizes token cost and execution latency while providing deep cognitive reasoning for concepting, layout geometry, physics, and verification. |
| **Liveness Supervision** | 30-Second Watchdog Heartbeat (`schedule`) | Prevents silent hanging or infinite repair loops in multi-agent pipelines; enforces a 2-attempt bounded repair cap. |
| **Visual Geometry** | Strictly 1080 × 1350 px (4:5 vertical) | Captures maximum vertical screen real estate on mobile LinkedIn feeds without banner clipping. |
| **Brand Identity** | Lobe-first verified vector marks (`@lobehub/icons`) | Eliminates AI logo hallucination; missing trademarks trigger an immediate, non-negotiable `HOLD`. |
| **Typography Engine** | Embedded Base64 WOFF2 & System UI | Eliminates render-time network latency, CORS blocks, and blank frames during headless Puppeteer capture. |
| **Animation Engine** | Pure CSS `@keyframes` on a single master `--loop` | Guarantees deterministic frame seeking, zero-seam looping (`x1.0` - `x1.25`), and changed-pixel economy (<0.5%). |

---

## 3. Discovered Patterns & Engineering Techniques

### 3.1 Ghost Trail vs Blur Filters (Pixel Budgeting)
* **Problem:** Standard `filter: blur(12px)` touches every pixel under the element, causing the GIF encoder to redraw the entire canvas every frame (ballooning file sizes to 10 MB+).
* **Solution:** Create layered duplicate DOM elements (`.trail.t1`, `.trail.t2`) with reduced opacity (0.20, 0.10), reduced scale (0.86, 0.72), and negative animation delays (`-70ms`, `-150ms`).
* **Result:** Silky smooth kinetic comet trail at **0 additional GPU pixel recalculation cost** and file sizes under 400 KB.

### 3.2 Ballistic Hop & Secondary Motion Physics
A professional kinetic feel requires coordinating four simultaneous animation properties:
1. **Trajectory (`routePos`)**: Combines vertical leap (`translateY`) with horizontal sway (`translateX`) and waddling tilt (`rotate: -7deg` to `+6deg`).
2. **Inertia Squash/Stretch (`podSquash`)**: Anticipation squash (`scale: 1.14, 0.82`) -> In-flight stretch (`scale: 0.86, 1.20`) -> Impact compression (`scale: 1.24, 0.70`) -> Rebound settling (`scale: 0.93, 1.09`).
3. **Contact Rings (`ringPulse`)**: Instant shockwave expansion (`scale: 0.5 -> 1.8`) exactly upon landing.
4. **Card Illumination (`r1Bg` - `r5Bg`)**: Synchronized 3px glow outline (`box-shadow: 0 0 0 3px var(--accent-tint)`) active exclusively during the puck dwell window.

---

## 4. Anti-Patterns & Lessons Learned

| Anti-Pattern Encountered | Why It Fails | Mandatory Corrective Pattern |
| :--- | :--- | :--- |
| **Skipping MasterOne** | Loses persistent profile context and risks inconsistent footers/languages. | Always execute `masterone` first to inspect `.linkedin-infographics/profile.json`. |
| **Remote Font `@import`** | Causes blank/flaky text in headless browser capture. | Embed Base64 WOFF2 strings directly in CSS or use native system fonts. |
| **Multiple Unrelated Animation Clocks** | Causes loop desynchronization and visible seam glitches. | Derive all sub-animation timings as integer divisions of a single `--loop` clock. |
| **Unbounded Subagent Execution** | Subagents can stall or repeat failing repair loops. | The 30s Watchdog detects stalls (>60s) and caps repairs at max 2 iterations. |
| **Drawing or Tracing Logos Manually** | Hallucinates incorrect trademark geometry. | Resolve exact vector assets via user upload or Lobe Hub. Otherwise, issue a `HOLD`. |

---

## 5. Multi-Agent Production Sequence Checklist

```
[ ] 00. MasterOne Onboarding (Check .linkedin-infographics/profile.json)
[ ] 01. design-study (Extract Reference DNA)
[ ] 02. evidence-checker (Validate Facts & Anti-Hallucination)
[ ] 03. asset-curator (Resolve Lobe-First Brand Assets)
[ ] 04. creative-director [Sol/Pro] (Generate Visual Hook, Copy Hook & Aha Moment)
[ ] 05. story-architect (Map 5-Step Story Progression & Tokens)
[ ] 06. palette-curator (Check WCAG Contrast Floors)
[ ] 07. type-curator (Specify Offline Render-Safe Fonts)
[ ] 08. copy-compressor [Flash] (Compress Hooked Microcopy into Slot Budget)
[ ] 09. layout-composer [Sol/Pro] (Build 1080x1350 Spatial Geometry)
[ ] 10. caption-writer [Flash] (Draft Truncation-Proof LinkedIn Caption)
[ ] 11. artboard-builder (Generate Static HTML & Frame 0 Still)
[ ] 12. motion-director [Sol/Pro] (Choreograph Single-Clock Motion Plan)
[ ] 13. mascot-animator [Optional] (Rig Vector Character Motion)
[ ] 14. motion-engineer (Implement Seekable CSS @keyframes)
[ ] 15. render-qa [Flash] (Capture Frames & Audit Seam/Pixels)
[ ] 16. post-critic [Sol/Pro] (Adversarial Multi-Axis Quality Critique)
[ ] 17. story-verifier [Sol/Pro] (Certify Deliverable for Release)
```
