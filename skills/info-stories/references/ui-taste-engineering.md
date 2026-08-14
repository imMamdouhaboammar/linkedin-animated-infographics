# UI Taste Engineering and Anti-Slop Interface Standards

A unified specification combining principles from taste-skill and hallmark to engineer high-craft UI mockups, interface cutaways, web/mobile screens, and interactive components

---

## 1 The Four Core Verbs

```
1 Build (Default): Synthesize new UI using the three dials and token-locked palettes
2 Audit: Evaluate existing UI code against anti-patterns and emit a ranked punch list without edits
3 Redesign: Preserve core copy and intent while reconstructing the visual hierarchy and component rhythm
4 Study: Extract Design DNA (macrostructure, typography roles, color anchor) from screenshots or URLs without copying pixels
```

---

## 2 The Three Dials: Core Configuration

Every UI screen, interface mockup, or design layout operates under three explicit dial values:

```
DESIGN_VARIANCE: 1 (Symmetry / Formal) to 10 (Dynamic / Experimental)
MOTION_INTENSITY: 1 (Static) to 10 (Kinetic / Micro-Physics)
VISUAL_DENSITY: 1 (Airy / Minimal) to 10 (Data-Rich / High-Information)
```

### Contextual Dial Presets

| UI Scenario | Variance | Motion | Density | Foundation Direction |
| :--- | :---: | :---: | :---: | :--- |
| SaaS Marketing View | 7 | 6 | 4 | Clean sans + balanced grid + single dominant CTA |
| Developer Platform & Terminal | 6 | 5 | 5 | Monospace accents + code blocks + dark neutral canvas |
| Premium Consumer Interface | 7 | 6 | 3 | High-contrast palette + generous spacing + verified assets |
| UI Storyboard Flow | 8 | 7 | 4 | Multi-state cards + directional indicators + state badges |
| Interface Cutaway | 6 | 5 | 6 | Highlighted component zones + focused callout tags |

---

## 3 The 8-State Interactive Completeness Checklist

Every interactive component and control must define explicit styling across all 8 interaction states:

```
1 Default: Resting neutral state with clear visual affordance
2 Hover: Subtle illumination or elevation shift
3 Focus-Visible: Accessible focus ring with minimum 3 to 1 contrast
4 Active: Tactile feedback with slight translation (-translate-y-[1px]) or scale (0.98)
5 Disabled: Reduced opacity and inert pointer styling
6 Loading: Skeleton or inline state indicator
7 Error: Clear contextual indicator and inline guidance text
8 Success: Confirmation indicator and transient highlight
```

---

## 4 Pre-Emit Six-Axis Self-Critique

Before exporting or publishing any UI artifact, score it from 1 to 5 across these six axes:

```
1 Purpose: Does the screen solve one primary user job with zero ambiguity?
2 Hierarchy: Does one dominant visual anchor command attention within 2 seconds?
3 Execution: Are tokens, spacing scales, and alignment grids mathematically consistent?
4 Specificity: Are metrics, copy, and controls grounded in real product context?
5 Restraint: Have unnecessary decorative cards, borders, and icons been eliminated?
6 Variety: Does the layout avoid repetitive zigzag patterns and cookie-cutter grids?
```

Any score below 3 requires an immediate targeted revision pass before final delivery

---

## 5 Anti-Default Typography and Palette Discipline

### Typography Invariants
- Sans-Serif Primacy: Default display typefaces include Geist, Satoshi, Cabinet Grotesk, and Outfit
- Serif Restrictions: Prohibit default usage of Fraunces and Instrument Serif unless explicitly required by brand heritage
- Roman Headings: Keep display titles in roman style (`font-style: normal`); convey emphasis through weight or accent color rather than italic titles
- Descender Clearance: Maintain minimum 1.1 line height and bottom padding for italic words with descenders (`g`, `j`, `p`, `q`, `y`)

### Palette and Contrast Invariants
- Single Accent Rule: Establish one primary accent tone per screen with saturation under 80%
- Token Locking: Every color and typeface declaration must reference defined design tokens without inline ad-hoc values
- Prohibit Neon Purple Tropes: Eliminate unearned purple glow borders and dark mesh backgrounds
- Contrast Floors: Ensure all text and interactive controls exceed WCAG AA standards (4.5 to 1 for body, 3.0 to 1 for large headings)

---

## 6 Layout Geometry and Evidence Truthfulness

### Hero and Screen Discipline
- Keep headlines under 2 lines and subtext under 20 words for immediate feed comprehension
- Limit hero text blocks to maximum 4 elements: eyebrow label, primary title, concise explanation, action button
- Prohibit fake chrome: Avoid drawing simulated browser bars, fake phone bezels, or artificial traffic light dots
- Bento Grid Integrity: Ensure bento containers have exact cell counts corresponding to real content items with zero empty placeholder tiles
- Logo Wall Restraint: Display authentic SVG logos only without redundant industry subtitle labels

---

## 7 DOM Bounding Box & Collision Prevention

- **Programmatic Geometry Audit**: Always measure computed bounding boxes (`top`, `bottom`, `height`) of major vertical containers via Headless Chrome / Playwright (`getBoundingClientRect()`).
- **Inter-Section Breathing Room**: Maintain a minimum 20px clean gap between the Header bottom and the Main Stage top.
- **Zero Dead-Space Container Sizing**: Avoid oversized hardcoded container heights. Use `display: flex; flex-direction: column; justify-content: space-between;` and exact content-hugging heights to eliminate empty white bands.

---

## 8 Progressive Narrative Motion & Opacity Flow

- **Progressive Opacity Sequencing**: Pipeline and funnel steps start in a resting dimmed state (`opacity: 0.45`). As the traveler puck docks at Step $N$, Step $N$ illuminates to `opacity: 1.0` with active borders and subtle elevation.
- **Elimination of Obscuring Floating Badges**: Never attach floating text badges to a moving puck that can hop across lines and obscure readable copy. Keep moving indicators clean and symbolic (e.g. crisp brand glyphs with pulse rings).
- **Hero Deliverable Ignition**: After the final step completes its transition, the hero deliverable card pulses with accent glow.

---

## 9 Headline Baseline & Asset Self-Containment

- **Baseline Integrity**: Avoid inline boxed button pills inside `h1` sentences. Use seamless inline editorial highlights (`border-bottom` accents with harmonious background tints) to maintain continuous reading rhythm.
- **Deterministic Offline Assets**: Base64-encode all local author portraits and brand marks as Data URIs directly in HTML to ensure 100% offline frame capture without network latency or render flickering.

---

## 10 Ultra-High Quality Render & Visual Crispness

- **High-Fidelity Visual Priority**: Always prioritize crispness, deep contrast, and smooth gradients in final GIF renders. File size allocations up to 5 MB or 6 MB are fully justified to maintain crystal-clear typography on high-DPI LinkedIn feeds.
- **Palette Quantization**: Use 128 to 256 color depth ladders. Avoid aggressive lossy compression or unnecessary downscaling when visual clarity can be preserved within the platform ceiling.


