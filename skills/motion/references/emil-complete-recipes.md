# Emil Kowalski & Apple Design Complete Motion Recipes & Physics Catalog

Authoritative implementations, formulas, and production code patterns covering the complete suite of 14 animation recipes and Apple fluid interface principles from Emil Kowalski's design engineering system (`animations.dev` / `https://github.com/emilkowalski/skills`).

---

## 1. The 14 Canonical UI & Infographic Motion Recipes

### Recipe 1: Tactile Press Feedback (Buttons, Cards, Chips)
Instant physical feedback on touch/click. Scales children (icons, labels) as a unified physical object.

```css
.pressable {
  transition: transform 160ms var(--ease-out-snappy), box-shadow 160ms var(--ease-out-snappy);
}
.pressable:active {
  transform: scale(0.97);
  transition: transform 80ms ease-in;
}
```

### Recipe 2: Origin-Aware Popovers, Menus, Selects & Dropdowns
Scales out of its trigger anchor instead of thin air.

```css
.popover-menu {
  transform-origin: var(--transform-origin, top center);
  transition: opacity 200ms var(--ease-out-snappy), transform 200ms var(--ease-out-snappy);
}
.popover-menu[data-starting-style],
.popover-menu[data-closed] {
  opacity: 0;
  transform: scale(0.95);
}
```

### Recipe 3: High-Perceived-Speed Tooltips & Instant Neighbor Hand-off
Initial delay prevents accidental triggers; subsequent tooltips skip delay and animation for lightning-fast toolbar navigation.

```css
.tooltip {
  transform-origin: var(--transform-origin, bottom center);
  transition: transform 125ms var(--ease-out-snappy), opacity 125ms var(--ease-out-snappy);
}
.tooltip[data-closed] {
  opacity: 0;
  transform: scale(0.97);
}
/* Instant neighboring tooltips */
.tooltip[data-instant] {
  transition-duration: 0ms !important;
}
```

### Recipe 4: Centered Modals & Synchronized Backdrops
Modals are exempt from trigger origin; they scale in centered from `scale(0.96)`.

```css
.modal-dialog {
  transform-origin: center;
  transition: opacity 250ms var(--ease-out-expo), transform 250ms var(--ease-out-expo);
}
.modal-dialog[data-closed] {
  opacity: 0;
  transform: scale(0.96);
}
.modal-backdrop {
  transition: opacity 250ms var(--ease-out-expo);
}
.modal-backdrop[data-closed] {
  opacity: 0;
}
```

### Recipe 5: Bottom Sheet / Drawer Slide
Smooth iOS-style vertical sheet motion using the ionic drawer curve.

```css
.bottom-sheet {
  transform: translateY(0);
  transition: transform 450ms cubic-bezier(0.32, 0.72, 0, 1);
}
.bottom-sheet[data-closed] {
  transform: translateY(100%);
}
```

### Recipe 6: Sonner-Style Elegant Toast Stack
Graceful `ease` timing that balances opacity and reflow height changes.

```css
.toast-card {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 350ms ease, transform 350ms ease;
  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

### Recipe 7: Layout Accordion & Section Collapse
Short duration to prevent layout recalculation stutter.

```css
.accordion-content {
  overflow: hidden;
  transition: height 200ms var(--ease-out-snappy), opacity 200ms var(--ease-out-snappy);
}
```

### Recipe 8: Tight Staggered Group Entrance
Stagger list or grid items by 30–60ms. Total group arrival completes within ≤ 400ms.

```css
.stagger-item {
  opacity: 0;
  transform: translateY(8px);
  animation: staggerFadeIn 300ms var(--ease-out-snappy) forwards;
}
.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 50ms; }
.stagger-item:nth-child(3) { animation-delay: 100ms; }
.stagger-item:nth-child(4) { animation-delay: 150ms; }

@keyframes staggerFadeIn {
  to { opacity: 1; transform: translateY(0); }
}
```

### Recipe 9: Hold-to-Confirm Progress Fill
For destructive actions or verified commits. Linear progress fill during press, snappy snap-back on release.

```css
.confirm-fill {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms var(--ease-out-snappy); /* release: snap back */
}
.confirm-button:active .confirm-fill {
  clip-path: inset(0 0 0 0);
  transition: clip-path 1.8s linear; /* press: deliberate progress */
}
.confirm-button:active {
  transform: scale(0.97);
}
```

### Recipe 10: Tab Indicator with Color-Clipped Duplicate
Zero-desync tab transitions by clipping an overlaid active-state clone.

```css
.tabs-active-overlay {
  clip-path: inset(0 60% 0 20%); /* dynamically driven by active tab bounds */
  transition: clip-path 250ms var(--ease-in-out-smooth);
}
```

### Recipe 11: Scroll / Reveal on Enter
Directional wipe using `clip-path: inset()`.

```css
.scroll-reveal {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 500ms var(--ease-in-out-smooth);
}
.scroll-reveal[data-visible] {
  clip-path: inset(0 0 0 0);
}
```

### Recipe 12: Drag to Dismiss with Momentum Flick & Damping
Dismiss on velocity (`> 0.11`) or distance threshold, settling with a spring.

```javascript
const timeTaken = Date.now() - dragStartTime;
const velocity = Math.abs(dragDistance) / timeTaken;

if (Math.abs(dragDistance) >= THRESHOLD || velocity > 0.11) {
  dismiss();
} else {
  // Settle back to origin
  animateSpring(element, { y: 0 }, { duration: 0.5, bounce: 0.2 });
}
```

### Recipe 13: Masking Crossfades with Micro-Blur
Eliminates awkward visual double-exposure during image or card swaps.

```css
.card-crossfade.transitioning {
  filter: blur(2px);
  opacity: 0.7;
  transition: filter 180ms ease, opacity 180ms ease;
}
```

### Recipe 14: Hardware-Accelerated WAAPI Programmatic Motion
Library-free JS animation executing on the GPU compositor.

```javascript
element.animate(
  [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
  { duration: 600, fill: 'forwards', easing: 'cubic-bezier(0.16, 1, 0.3, 1)' }
);
```

---

## 2. Apple Fluid Interfaces Physics & Formulas

### A. Damping Ratio & Response Defaults

| Interaction Role | Damping Ratio ($\zeta$) | Response ($T_0$) | Feel & Behavior |
|---|---|---|---|
| **Standard Repositioning** | `1.0` (Critically Damped) | `0.40s` | Zero bounce, smooth deceleration |
| **Drawer / Sheet Gesture** | `0.8` (Subtle Spring) | `0.30s` | Snappy, crisp physical feel |
| **Momentum Throw / Flick** | `0.75 - 0.80` | `0.45s` | Natural deceleration carrying momentum |

### B. Apple Momentum Projection Equation
Projects where a dragged/thrown element should come to rest based on release velocity:

$$D_{\text{proj}} = \left(\frac{v_{\text{initial}}}{1000}\right) \times \frac{d_{\text{rate}}}{1 - d_{\text{rate}}}$$

*(where $d_{\text{rate}} \approx 0.998$ for natural scroll feel, or $0.990$ for snappier UI)*.

### C. Rubber-Banding Soft Boundary Formula
Nonlinear resistance when dragging past content limits:

$$x_{\text{rubber}} = \frac{x_{\text{overshoot}} \times L \times c}{L + c \times |x_{\text{overshoot}}|}$$

*(where $L$ is the dimension length and $c \approx 0.55$)*.

---

## 3. Apple Translucent Materials & Depth Tokens

```css
:root {
  /* Translucent floating surface */
  --surface-glass-light: rgba(255, 255, 255, 0.72);
  --surface-glass-dark: rgba(18, 24, 38, 0.75);
  
  /* Backdrop blur filter */
  --blur-material: blur(20px) saturate(180%);
  
  /* Light-catching top border edge */
  --border-light-catch: 1px solid rgba(255, 255, 255, 0.45);
}

.floating-card {
  background: var(--surface-glass-light);
  backdrop-filter: var(--blur-material);
  -webkit-backdrop-filter: var(--blur-material);
  border-top: var(--border-light-catch);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}
```
