# Emil Kowalski Animation Craft Standards & Review Guide

Authoritative motion craft rules, easing curves, spring parameters, duration budgets, and review checklists distilled from Emil Kowalski's animation engineering philosophy (`animations.dev`), adapted for deterministic LinkedIn animated infographics.

---

## 1. The Ten Non-Negotiable Craft Standards

Every animation in this system is reviewed and built against these 10 standards:

1. **Justified Motion**: Every animation must serve a clear cognitive purpose: hierarchy, reading sequence, state transition, reveal, or creative payoff. "It looks cool" is never a justification.
2. **Frequency & Pacing Appropriate**: Infographic loops must feel deliberate and calm. Avoid hyperactive pulsing or rapid frantic loops.
3. **Responsive Custom Easing**:
   - **Never use `ease-in` on UI entrances/exits** (it delays the exact moment the eye is watching).
   - Built-in CSS easings (`ease`, `linear`) are too weak for high-end craft.
   - Use strong custom cubic-beziers that start fast and decelerate smoothly.
4. **Sub-300ms Micro-Interactions**:
   - Button press / Click feedback: **100–160ms**
   - Tooltips, small badges: **125–200ms**
   - Dropdowns, card expands: **150–250ms**
   - Modals / Full-stage reveals: **200–400ms**
5. **Physicality & Origin Correctness**:
   - **Never animate from `scale(0)`** (nothing appears from nowhere; start from `scale(0.90–0.96)` + `opacity: 0`).
   - Set `transform-origin` to the trigger anchor (e.g. `top left`, `bottom center`) so popovers and chips expand from their origin rather than a disconnected center.
6. **Interruptibility & Determinism**:
   - In live web UIs, use transitions or springs.
   - In rendered infographic loops, ensure keyframe states are pure deterministic functions of timeline time `t`.
7. **GPU-Only Properties**:
   - Animate `transform` (`translate`, `scale`, `rotate`) and `opacity` only.
   - **Never** animate `width`, `height`, `margin`, `padding`, `top`, or `left`.
8. **Asymmetric Enter/Exit Timing**:
   - Deliberate actions (user typing, press) take longer; system responses snap.
   - Example: Press down is deliberate (`160ms`), release and trigger response is snappy (`100ms`).
9. **Tight Stagger Discipline**:
   - Stagger group items with **30–80ms** intervals.
   - Total group entrance must complete within **≤ 400ms** so it reads as one coordinated beat.
10. **Accessibility & Hover Gating**:
    - Gate hover states behind `@media (hover: hover) and (pointer: fine)`.
    - Support `prefers-reduced-motion` by reducing spatial translations to opacity/color transitions.

---

## 2. Master Easing Palette

```css
:root {
  /* Snappy, responsive UI entrance (starts fast, lands smoothly) */
  --ease-out-snappy: cubic-bezier(0.23, 1, 0.32, 1);
  
  /* Ultra-crisp modern card / modal arrival */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  
  /* On-screen movement & continuous morphs */
  --ease-in-out-smooth: cubic-bezier(0.77, 0, 0.175, 1);
  
  /* Natural drawer / accordion slide curve */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
  
  /* Spring overshoot for chips, pills, and badges */
  --ease-spring-pop: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 3. Tactile Button & Card Press Pattern

Subtle scale compression on `:active` with asymmetric release:

```css
.pressable-card {
  transform: scale(1);
  transition: transform 140ms var(--ease-out-snappy), box-shadow 140ms ease-out;
}

.pressable-card:active {
  transform: scale(0.97);
  transition: transform 80ms ease-in;
}
```

---

## 4. Clip-Path Directional Reveals (Without Layout Thrashing)

Using `clip-path: inset(t r b l)` enables wipe reveals, comparison sliders, and tab highlighting without touching `width` or `height`:

```css
/* Reveal from bottom to top */
.clip-reveal-up {
  clip-path: inset(100% 0 0 0);
  transition: clip-path 350ms var(--ease-out-expo);
}
.clip-reveal-up.active {
  clip-path: inset(0 0 0 0);
}

/* Tab highlight underline / background wipe */
.tab-indicator {
  clip-path: inset(0 100% 0 0);
  animation: tabWipe var(--loop) var(--ease-out-snappy) infinite;
}
@keyframes tabWipe {
  0%, 15% { clip-path: inset(0 100% 0 0); }
  35%, 85% { clip-path: inset(0 0 0 0); }
  100% { clip-path: inset(0 0 0 100%); }
}
```

---

## 5. Masking Imperfect Crossfades

When transitioning between two states or swapping images/cards, avoid an awkward double-exposure by applying a micro-blur during the swap:

```css
@keyframes smoothCardSwap {
  0% { opacity: 1; filter: blur(0px); }
  45% { opacity: 0; filter: blur(2px); transform: scale(0.97); }
  55% { opacity: 0; filter: blur(2px); transform: scale(0.97); }
  100% { opacity: 1; filter: blur(0px); transform: scale(1); }
}
```
*(Keep blur ≤ 2px and duration ≤ 200ms to avoid GIF payload inflation).*

---

## 6. Reviewer Checklist & Escalation Triggers

When auditing motion implementation in `render-qa` or `post-critic`, immediately flag:

| Trigger / Anti-Pattern | Severity | Remediation |
|---|---|---|
| `scale(0)` initial state | **BLOCK** | Change to `scale(0.95)` + `opacity: 0` |
| `ease-in` on UI entrance | **BLOCK** | Change to `cubic-bezier(0.23, 1, 0.32, 1)` or `ease-out` |
| Animating `width`/`height`/`top`/`left` | **BLOCK** | Replace with `transform: translate()` or `clip-path` |
| Group stagger > 400ms total | **FLAG** | Tighten per-item delay to 40–60ms |
| `transform-origin: center` on popover/tooltip | **FLAG** | Anchor origin to trigger source (`top left`, etc.) |
| Unbounded `transition: all` | **FLAG** | Explicitly name `transform, opacity` |
