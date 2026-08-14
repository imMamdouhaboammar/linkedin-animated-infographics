# Mblode Complete CSS Transition Recipes & UI Motion Engine

Authoritative implementation catalog containing 14 production CSS transition patterns, container morphing, odometer rolling, text state swaps, and micro-interactions adapted from `mblode/agent-skills` (`blode.co`).

---

## 1. Global Custom Properties Token Block

```css
:root {
  /* Container Morph */
  --morph-open-dur: 580ms;
  --morph-close-dur: 300ms;
  --morph-open-ease: linear(0, 0.45, 0.78, 1, 1.17, 1.21, 1.18, 1.12, 1.05, 1.02, 1);
  --morph-close-ease: cubic-bezier(0.32, 0.72, 0, 1);
  --morph-content-dur: 140ms;
  --morph-content-blur: 3px;

  /* Card Resize */
  --resize-dur: 300ms;
  --resize-ease: cubic-bezier(0.22, 1, 0.36, 1);

  /* Odometer Digit Roll */
  --odo-dur: 260ms;
  --odo-ease: cubic-bezier(0.22, 1, 0.36, 1);
  --odo-dir: 1; /* 1 = increase, -1 = decrease */

  /* Number Pop-in */
  --digit-dur: 500ms;
  --digit-dist: 12px;
  --digit-stagger: 70ms;
  --digit-blur: 6px;
  --digit-ease: cubic-bezier(0.22, 1, 0.36, 1);

  /* Notification Badge */
  --badge-slide-dur: 260ms;
  --badge-pop-dur: 500ms;
  --badge-blur: 2px;
  --badge-offset-x: -8px;
  --badge-offset-y: 12px;
  --badge-ease: cubic-bezier(0.22, 1, 0.36, 1);

  /* Text State Swap */
  --text-swap-dur: 150ms;
  --text-swap-y: 4px;
  --text-swap-blur: 2px;
  --text-swap-ease: ease-in-out;

  /* Icon Swap */
  --icon-swap-dur: 200ms;
  --icon-swap-blur: 2px;
  --icon-swap-start-scale: 0.25;
  --icon-swap-ease: ease-in-out;

  /* Success Celebration */
  --success-opacity-dur: 550ms;
  --success-rotate-dur: 550ms;
  --success-bob-dur: 550ms;
  --success-blur-dur: 400ms;
  --success-rotate-from: 80deg;
  --success-bob-y: 40px;
  --success-blur-from: 10px;
  --success-ease: cubic-bezier(0.22, 1, 0.36, 1);

  /* Error State Shake */
  --shake-dist: 4px;
  --shake-overshoot: 2px;
  --shake-dur: 280ms;
  --shake-ease: cubic-bezier(0.36, 0.07, 0.19, 0.97);
}
```

---

## 2. The 14 Mblode Transition Recipes

### 1. Container Morph (The Trigger Becomes The Surface)
Pill or button expands into an expanded container with linear overshoot settling and content cross-blur:

```css
.t-morph {
  position: relative;
  overflow: hidden;
  border-radius: 999px;
  transition: width var(--morph-close-dur) var(--morph-close-ease),
              height var(--morph-close-dur) var(--morph-close-ease);
  will-change: width, height;
}
.t-morph[data-open="true"] {
  transition-duration: var(--morph-open-dur);
  transition-timing-function: var(--morph-open-ease);
}
.t-morph-face {
  transition: opacity var(--morph-content-dur) ease, filter var(--morph-content-dur) ease;
}
.t-morph-face[data-face="open"] { position: absolute; inset: 0; }
.t-morph[data-open="false"] [data-face="open"],
.t-morph[data-open="true"] [data-face="closed"] {
  opacity: 0;
  filter: blur(var(--morph-content-blur));
  pointer-events: none;
}
```

### 2. Odometer Directional Digit Roll
Rolls numbers up or down according to the delta with `font-variant-numeric: tabular-nums`:

```css
.t-odo {
  display: inline-flex;
  font-variant-numeric: tabular-nums;
}
.t-odo-slot {
  display: inline-block;
  overflow: hidden;
  height: 1em;
  line-height: 1em;
}
@keyframes odo-roll {
  from {
    transform: translateY(calc(var(--odo-dir) * 1em));
    opacity: 0;
  }
}
.t-odo-digit[data-rolling] {
  display: block;
  animation: odo-roll var(--odo-dur) var(--odo-ease) both;
}
```

### 3. Vertical Text State Swap
Swaps status copy ("Analyzing..." ➔ "Verified PASS") with a vertical blurred drift:

```css
.t-text-swap {
  display: inline-block;
  transition: opacity var(--text-swap-dur) var(--text-swap-ease),
              transform var(--text-swap-dur) var(--text-swap-ease),
              filter var(--text-swap-dur) var(--text-swap-ease);
}
.t-text-swap.is-exit {
  opacity: 0;
  transform: translateY(calc(-1 * var(--text-swap-y)));
  filter: blur(var(--text-swap-blur));
}
.t-text-swap.is-enter {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
}
```

### 4. Icon Swap in Same Grid Slot
Cross-fades two icons (e.g. Lock ➔ Unlock, Check ➔ Copy) in an overlapping CSS grid:

```css
.t-icon-swap { display: inline-grid; }
.t-icon {
  grid-area: 1 / 1;
  opacity: 0;
  transform: scale(var(--icon-swap-start-scale));
  filter: blur(var(--icon-swap-blur));
  transition: opacity var(--icon-swap-dur) var(--icon-swap-ease),
              transform var(--icon-swap-dur) var(--icon-swap-ease),
              filter var(--icon-swap-dur) var(--icon-swap-ease);
}
.t-icon-swap[data-state="active"] .t-icon-active {
  opacity: 1; transform: scale(1); filter: blur(0);
}
```

### 5. Multi-Phase Success Celebration
SVG checkmark stroke draw with simultaneous rotate, vertical bob, and blur clearing:

```css
.t-success-badge {
  opacity: 1;
  transform: translateY(0) rotate(0deg);
  filter: blur(0);
  transition: opacity var(--success-opacity-dur) var(--success-ease),
              transform var(--success-bob-dur) var(--success-ease),
              filter var(--success-blur-dur) var(--success-ease);
}
.t-success-badge[data-starting-style] {
  opacity: 0;
  transform: translateY(var(--success-bob-y)) rotate(var(--success-rotate-from));
  filter: blur(var(--success-blur-from));
}
```

### 6. Asymmetric Error State Shake
Physical recoil shake for invalid inputs or failed claims:

```css
@keyframes errorShake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(calc(-1 * var(--shake-dist))); }
  40% { transform: translateX(var(--shake-dist)); }
  60% { transform: translateX(calc(-1 * var(--shake-overshoot))); }
  80% { transform: translateX(var(--shake-overshoot)); }
}
.t-error-shake {
  animation: errorShake var(--shake-dur) var(--shake-ease);
}
```

### 7. Notification Badge Slide & Pop
Badge translates into position and then pops its dot:

```css
.t-badge {
  position: absolute;
  opacity: 0;
  transform: translate(var(--badge-offset-x), var(--badge-offset-y));
  filter: blur(var(--badge-blur));
  transition: opacity var(--badge-slide-dur) var(--badge-ease),
              transform var(--badge-slide-dur) var(--badge-ease),
              filter var(--badge-slide-dur) var(--badge-ease);
}
.t-badge[data-open="true"] { opacity: 1; transform: translate(0, 0); filter: blur(0); }
.t-badge-dot {
  transform: scale(0);
  transition: transform var(--badge-pop-dur) var(--badge-ease);
}
.t-badge[data-open="true"] .t-badge-dot {
  transform: scale(1);
  transition-delay: calc(var(--badge-slide-dur) * 0.5);
}
```

### 8. Panel Reveal with Distance-Based Blur
```css
.t-panel {
  opacity: 0;
  transform: translateY(12px);
  filter: blur(4px);
  transition: opacity 400ms cubic-bezier(0.22, 1, 0.36, 1),
              transform 400ms cubic-bezier(0.22, 1, 0.36, 1),
              filter 400ms cubic-bezier(0.22, 1, 0.36, 1);
}
.t-panel[data-open="true"] {
  opacity: 1; transform: translateY(0); filter: blur(0);
}
```

### 9. Page Side-by-Side Directional Slide
Adjacent views sliding with matching horizontal direction and edge blurring.

### 10. Number Pop-in with Digit Staggers
Counters and prices entering character-by-character with 70ms stagger.

### 11. Avatar Group Hover Distance Falloff
Interactive avatar stacks lifting with proximity attenuation.

### 12. Card Dimension Tween (CSS Card Resize)
Smooth container dimensions tweening with zero Javascript.

### 13. Origin-Aware Menu Dropdown
Scaling out cleanly from the 6 possible anchor points (`top-left`, `top-center`, `top-right`, etc.).

### 14. Centered Modal with Soft Exit
Scale-up from `0.96` on entry, soft deceleration on exit.
