# Mandatory Browser Pixel-by-Pixel Inspection & Auto-Repair Rule

This rule is a non-negotiable quality gate for every generated LinkedIn infographic and visual story.

---

## 1. Core Principle: Visual Reality Over Code Assumptions

Code that compiles or passes static linting is **NOT** finished until it has been rendered in a live browser engine, inspected pixel-by-pixel at full 1080x1350 resolution and 350px mobile feed scale, and verified free of visual defects.

Never claim completion based on raw HTML/CSS strings or theoretical markup.

---

## 2. End-of-Pipeline Browser Inspection Protocol

At the end of every post generation, the pipeline MUST execute the browser inspection pass:

```bash
# Step 1: DOM & layout geometry audit via browser CDP
python3 scripts/artboard_audit.py build/post.html --json build/artboard-audit.json

# Step 2: High-res 1080x1350 still capture + 350px mobile feed downscale
python3 scripts/check_render.py build/post.html --out build/still.png --mobile --json build/still-audit.json

# Step 3: When animated, render seekable frames, check seam ratio & motion budget
bash scripts/render.sh build/post.html build/post.gif --duration 6.0 --fps 12.5
```

---

## 3. The 7 Pixel-by-Pixel Visual Defect Checks

The agent must inspect the rendered browser artifacts (`build/still.png`, `build/still_mobile350.png`, and `build/post.gif`) against these 7 failure categories:

| Check # | Visual Defect Category | What to Look For | Pass Criteria |
|---|---|---|---|
| **1** | **Clipping & Text Overflow** | Text spilling out of cards, truncated copy, clipped descenders (g, y, p, q, j), horizontal scrollbars | Zero clipping; all text comfortably contained within parent bounds |
| **2** | **Safe Margin Clearance** | Content touching or invading the outer 48px/60px perimeter | 100% clearance; title block and footer respect margins |
| **3** | **Alignment & Flex Squishing** | Asymmetric card gaps, distorted icons, squished flex items | Equal margins, crisp vector proportions, `flex: none` on fixed elements |
| **4** | **Contrast & Washed-out Text** | Thin light text on light backgrounds or dark muted text on dark cards | Strict WCAG AA compliance (≥ 4.5:1 text, ≥ 3.0:1 UI states); weight ≥ 500 for body |
| **5** | **Mobile 350px Feed Legibility** | Headline disappearing, takeaway chip illegible, muddy details | Core message & hero takeaway readable instantly without zooming |
| **6** | **Frame 0 Completeness** | Blank containers or half-loaded elements at t = 0 | Frame 0 is a 100% complete, readable static infographic poster |
| **7** | **Loop Seam & Motion Stability** | Visual jump at loop boundary, full-canvas flickering | Seam multiplier ≤ x1.25; mean changed pixels < 2.0% (dark) / < 0.5% (light) |

---

## 4. Closed-Loop Auto-Repair Cycle

When any visual flaw is detected during the browser inspection:

```
[Render in Browser] ➔ [Detect Pixel Flaws] ➔ [Surgical CSS/DOM Fix] ➔ [Re-render & Verify]
```

1. **Diagnose Root Cause**: Identify the exact CSS selector or DOM node causing the visual defect (e.g. `line-height`, `padding`, `flex-shrink: 0`, `font-weight`, `stroke-width`, or `color`).
2. **Apply Surgical Fix**: Modify only the offending properties without rewriting layout architecture.
3. **Re-Run Browser Inspection**: Re-execute `check_render.py` / `render.sh` to capture fresh visual evidence.
4. **Iterate**: Repeat until all 7 checks achieve a clean **PASS** (maximum 2 targeted repair attempts before escalation).
