# Animation Opportunities & Restraint Gate

Framework for identifying meaningful motion opportunities while aggressively filtering out decorative slop.

---

## 1. The Four-Question Restraint Gate

Every proposed animation must pass all 4 questions in order:

```
[1. Frequency Check] ➔ [2. Purpose Check] ➔ [3. Speed Budget] ➔ [4. Function Check]
```

### 1. Frequency Check
- **100+ times/day** (Keyboard shortcuts, command palettes, repeated data reading): **REJECT. No animation.**
- **Tens of times/day** (Hover states, lists): Near-imperceptible micro-motion only.
- **Occasional** (Modals, cards, reveals): Standard animation permitted.
- **Rare / Hero / First-time** (Aha moment payoff, milestone celebrations): Full delight budget permitted.

### 2. Purpose Check
The animation MUST serve one of these named jobs:
- **Feedback**: Confirming an interaction occurred (tactile scale on press).
- **Spatial Consistency**: Showing origin and destination (origin-aware scale-out).
- **State Indication**: Making a transformation legible (accordion expand, toggle morph).
- **Preventing Jarring Changes**: Bridging two states smoothly.
- **Explanation**: Demonstrating a workflow or data progression.
- **Payoff Punctuation**: Clarifying the core creative takeaway.

*(If the only purpose is "it looks cool", REJECT).*

### 3. Speed Budget Check
- UI micro-interactions must complete within **≤ 300ms**.
- Group staggers must complete within **≤ 400ms**.

### 4. Function Check
- Functional data charts, dense numbers, and critical body text MUST stay static.
- Motion is applied only to indicators, focus anchors, or flow lines.

---

## 2. The Six Seams to Hunt for Meaningful Motion

1. **Feedback Gaps**: Pressable elements lacking active tactile response → apply `scale(0.97)` on `:active`.
2. **Teleporting States**: Elements appearing or vanishing with hard cuts → apply `scale(0.95)` + `opacity` entrance with `cubic-bezier(0.23, 1, 0.32, 1)`.
3. **Missing Spatial Anchors**: Popovers or tooltips appearing disconnected from triggers → apply origin-aware `transform-origin`.
4. **Group Arrival Flurries**: Grids/lists snapping in all at once → apply 40ms stagger.
5. **Gesture & Flow Seams**: Sliders or indicators jumping between steps → apply smooth spring/ease transitions.
6. **Delight Moments**: Story milestone, final ROI counter, or verified CTA verdict → apply dynamic count-up, particle burst, or spring pop.
