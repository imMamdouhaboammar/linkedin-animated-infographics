# Impeccable Motion Craft & Authoring Standards

A comprehensive design engineering and craft discipline guide adapted from Paul Bakaus's `pbakaus/impeccable` suite.

---

## 1. The Motion Thesis Principle

Every animated infographic or interactive UI surface must declare a clear **Motion Thesis** before writing keyframes:

```
[1. The Authored Focal Moment] + [2. Continuity & State] + [3. Feedback & Acknowledgement]
```

- **One Authored Focal Moment**: Exactly ONE rehearsed hero sequence that carries the story payoff (e.g. data progression, architecture breakthrough, comparative payoff). Do NOT scatter uniform entrance fades across every container.
- **Continuity & State**: Layout and state changes explain where elements came from using FLIP, clip-paths, or origin-aware transforms.
- **Feedback & Acknowledgement**: Micro-interactions provide instant tactile confirmation (100–150ms) without making the user wait.

---

## 2. Visitor Mode Discipline

| Visitor Mode | Primary Motion Role | Interaction Constraint |
|---|---|---|
| **Persuade / Experience** (Hero Infographics, Marketing) | Motion carries the narrative voice; one primary rehearsed focal loop. | Keep the loop seamless and frame 0 100% readable. |
| **Operate / Read** (Dense Charts, Code Blocks, Metrics) | Motion serves state, feedback, and continuity only. | Data and text remain static; no decorative distraction. |

---

## 3. Asymmetric Timing & Easing Calibration

Arrivals should feel confident; exits must feel snappy and never block the user:

```css
:root {
  /* Confident arrival deceleration (Paul Bakaus / Impeccable standard) */
  --ease-arrival: cubic-bezier(0.16, 1, 0.3, 1);
  
  /* Snappy exit acceleration */
  --ease-exit: cubic-bezier(0.7, 0, 0.84, 0);
  
  /* Natural physical spring */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Durations by Consequence:
- **100–150 ms**: Immediate tactile feedback (button press, toggle click).
- **150–250 ms**: Routine state changes (dropdown reveal, badge update).
- **300–450 ms**: Layout expands, modal overlays, tab switches.
- **500–800 ms**: Authored focal moment hero animations.

---

## 4. Impeccable Craft Floor & Visual Anti-Patterns

### Strict Bans (Design Debt Refusal):
1. **No Section Eyebrows by Habit**: Do not put a tiny biscuit badge or kicker above every single heading. Let strong headings speak.
2. **No Identical Lazy Card Grids**: Avoid repeating identical icon+title+body card boxes unless repetition is the core story.
3. **No Gradient Text Keywords**: Avoid CSS gradient fills on headline text; create contrast through weight, scale, and color harmony.
4. **No Colored Side-Stripe Borders**: Avoid `border-left: 4px solid var(--accent)` on callout cards.
5. **No Zero-Blur Hard Offset Shadows**: Avoid `box-shadow: 4px 4px 0 #000` unless executing strict neobrutalism. Use soft, layered, offset shadows.
6. **No Sketchy SVG Doodles**: Avoid low-quality pseudo-hand-drawn SVG curves. Use precise mathematical geometry and authored vector paths.

### Browser Surfaces Styling:
Always style native browser elements so the interface feels crafted from ground up:

```css
/* Styled text selection matching palette */
::selection {
  background: var(--accent-subtle, rgba(59, 130, 246, 0.2));
  color: var(--accent-ink, #1e40af);
}

/* Styled focus rings with explicit offset */
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

---

## 5. Reduced Motion Graceful Degradation

Always provide an intentional alternative under `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  
  /* Preserve meaningful opacity and color state transitions */
  .state-transition {
    transition: opacity 150ms ease, background-color 150ms ease !important;
  }
}
```
