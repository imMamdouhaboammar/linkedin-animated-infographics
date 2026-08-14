# Pixel-Perfect Browser Inspection & Visual QA Guide

A comprehensive operational guide for end-of-pipeline browser rendering, CDP inspection, visual defect diagnosis, and automated repair for 1080x1350 LinkedIn animated infographics.

---

## 1. Why Browser Inspection is Mandatory

Browser rendering engines (Chromium/CDP) process font rasterization, sub-pixel antialiasing, CSS flexbox/grid layout trees, text wraps, and CSS animation clocks in ways static code linting cannot simulate.

Every post MUST be opened and inspected in a real browser session before approval.

---

## 2. Browser Inspection Workflow

```
1. Open HTML in Browser at 1080x1350 Viewport
   └─ Run CDP DOM & Geometry Probe (artboard_audit.py)
2. Capture High-Res 1080x1350 Still & Mobile 350px Downscale (check_render.py)
3. If Animated: Capture Seeked Frames & Assemble GIF (render.sh)
4. Audit 7 Visual Quality Pillars
   ├─ [PASS] ──> Proceed to Final Verification (story-verifier)
   └─ [FAIL] ──> Apply Targeted Surgical Fix ──> Re-render in Browser
```

---

## 3. Common Visual Defects & Instant Repair Recipes

### Defect 1: Text Descender Clipping / Card Overflow
- **Symptom**: Letters like `g, y, p, q, j` get their bottoms clipped, or the last line of a paragraph spills out of a card.
- **Root Cause**: `line-height` too tight (e.g. `line-height: 1.0`), fixed container height (`height: 200px`), or `overflow: hidden` without internal padding.
- **Repair Recipe**:
  ```css
  /* Increase line-height and ensure flex auto-sizing */
  .card-body {
    line-height: 1.45;
    min-height: 0;
    padding-bottom: 8px; /* breathing room for descenders */
  }
  ```

### Defect 2: Asymmetric Margins & Edge Hugging
- **Symptom**: Content is squeezed against the top/bottom canvas edge, invading the 48px/60px safe margin.
- **Root Cause**: Missing `#artboard` padding or unconstrained container growth.
- **Repair Recipe**:
  ```css
  #artboard {
    width: 1080px;
    height: 1350px;
    padding: 60px 56px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  ```

### Defect 3: Washed-Out Text at 350px Mobile Feed Scale
- **Symptom**: Body copy looks faint or unreadable on phone screens.
- **Root Cause**: Font weight too light (`font-weight: 300`/`400`) or low contrast ratio against the card ground.
- **Repair Recipe**:
  ```css
  .card-text {
    font-weight: 500; /* boost weight for mobile legibility */
    color: var(--ink); /* use primary ink token, not muted */
  }
  ```

### Defect 4: Flex Item Squishing & Icon Distortion
- **Symptom**: Vector icons, badges, or avatar nodes get squished into ovals when text content expands.
- **Root Cause**: Missing `flex-shrink: 0` on fixed-dimension elements.
- **Repair Recipe**:
  ```css
  .icon-wrapper, .badge, .status-pill {
    flex-shrink: 0;
    width: 44px;
    height: 44px;
  }
  ```

### Defect 5: Loop Seam Jump (GIF Stutter)
- **Symptom**: The animation jumps abruptly every loop cycle.
- **Root Cause**: Keyframe at `100%` does not match `0%`, or animation duration is not an integer division of `--loop`.
- **Repair Recipe**:
  ```css
  :root {
    --loop: 4800ms;
  }
  /* Sub-animations must divide cleanly */
  .sub-anim {
    animation: rotateLoop calc(var(--loop) / 2) linear infinite;
  }
  @keyframes rotateLoop {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); } /* Ends exactly at start point */
  }
  ```

---

## 4. Automation Commands Reference

```bash
# Audit DOM geometry, bounding boxes, containment depth, and fonts
python3 scripts/artboard_audit.py build/post.html --json build/artboard-audit.json

# Capture still, create mobile 350px preview, measure area & clearance
python3 scripts/check_render.py build/post.html --out build/still.png --mobile --json build/still-audit.json

# Render complete deterministic GIF with loop seam & changed-pixel diffing
bash scripts/render.sh build/post.html build/post.gif --duration 6.0 --fps 12.5
```
