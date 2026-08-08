---
name: linkedin-infographic-review
description: Review a finished static or animated LinkedIn infographic before publishing. Check hierarchy, visual balance, dead space, generic UI patterns, copy, evidence, motion, rendering, and feed-scale legibility without redesigning unrelated content.
---

# LinkedIn Infographic Review

## Purpose

Run a focused pre-publish critique on an existing LinkedIn infographic. Diagnose what is blocking publication, separate required fixes from optional polish, and avoid turning review into an unrelated redesign.

## Inputs

Use the finished HTML, GIF, PNG, screenshots, caption, source material, or evidence the user provides.

If evidence required to validate a factual claim is unavailable, mark that claim as unverified instead of inventing support.

## Review order

### 1. Static composition

Inspect the full artboard before looking at small details.

Check:

- one dominant visual anchor is obvious within two seconds
- the page has a clear macro rhythm from hook to visual relationship to takeaway
- the composition is not top-heavy
- there is no unexplained dead zone near the footer
- the footer belongs to the composition instead of floating far below it
- text remains readable at feed scale
- copy density is solved through hierarchy and editing rather than tiny type

For a 1080x1350 artboard, treat an unexplained vertical gap greater than 120px between the main composition and footer/takeaway as a blocking warning unless negative space has an intentional visual job.

### 2. Component grammar

Reject generic component patterns when they replace art direction.

Check:

- no more than two bordered containment levels
- repeated cards exist only when repetition is meaningful
- pills, badges, status chips, and tiny uppercase labels have semantic jobs
- no fake dashboards, fake analytics, fake proof bars, or invented metrics
- visual structure fits the story rather than the easiest HTML pattern

### 3. Copy and evidence

Check:

- one primary message
- hook is specific to the subject
- body copy adds mechanism, evidence, comparison, consequence, or action
- takeaway completes the idea instead of repeating the headline
- claims, numbers, logos, product states, and proof are supported by supplied material
- no generic filler or exaggerated marketing language

### 4. Motion when animated

Every meaningful animation must explain at least one of:

- what should I read next?
- what changed?
- where did this item travel?
- which state is active?

Fail decorative motion when it dominates the explanatory motion.
Fail `motion-on-weak-still` when the composition itself should be repaired before animation.

Inspect frame zero, a representative mid-state, the final state, and the loop seam.

### 5. Failure taxonomy

Return PASS or FAIL for each:

- `top-heavy-composition`
- `bottom-dead-zone`
- `nested-card-density`
- `generic-ui-grammar`
- `weak-macro-rhythm`
- `weak-visual-anchor`
- `footer-detachment`
- `motion-on-weak-still`
- `decorative-motion`
- `feed-scale-legibility`

## Output

Return:

1. verdict: `PASS`, `FAIL:fixable`, or `HOLD`
2. blocking findings
3. top three repair actions in priority order
4. advisory polish, if any
5. evidence limitations
6. motion/render notes when applicable

Do not return PASS while a severe blocking finding remains.
