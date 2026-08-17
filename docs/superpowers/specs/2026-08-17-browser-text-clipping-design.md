# Browser Text Clipping Gate

Date: 2026-08-17

## Problem

The rendered artboard audit already measures canvas size, occupancy, footer detachment, containment depth, typography, contrast, and font fallback, but it does not mechanically detect text that is truncated by a constrained box. The QA guide says no content may be clipped, yet that requirement currently depends on human inspection.

## Decision

Add browser-measured text clipping evidence to `scripts/artboard_audit.py` and make clipping of load-bearing text a blocking visual gate.

A text box is considered clipped when its rendered `scrollWidth` exceeds `clientWidth` or its rendered `scrollHeight` exceeds `clientHeight`, allowing a one-pixel tolerance for browser rounding, and the effective overflow policy on that axis is not `visible`. Visible overflow is not truncation and must not block export.

For ordinary elements, the probe measures direct text nodes to avoid attributing unrelated descendant geometry to a wrapper. For load-bearing roles, it also inspects descendant text so common markup such as `<h1 class="headline"><span>Long title</span></h1>` cannot hide clipping at the headline container.

The probe records the element role, text sample, client dimensions, scroll dimensions, overflow mode, and whether it is load-bearing.

Load-bearing classification uses the same role hints already used by the feed-scale typography audit: headline, hero, title, takeaway, subline, lede, and kicker. Clipping in these roles blocks export. Other clipped text is reported as advisory evidence so intentional micro-copy truncation does not create a false hard failure.

## Contract

The feature adds two thresholds through the merged visual-contract loader:

- `type.max_clipped_load_bearing_nodes = 0`, blocking, gate `text-clipping`
- `type.max_clipped_nodes = 0`, advisory, gate `text-clipping`

The blocking threshold is documented against the existing QA requirement that no content is clipped. Feature-scoped contract fragments may add new threshold and gate ids but cannot replace existing ids or conflict with existing gate definitions.

## Report changes

`artboard_audit.py` adds both findings and exposes clipping measurements in the machine-readable report. Failure evidence names the rendered element, client and scroll dimensions, computed overflow modes, and the amount by which the clipped content exceeds its visible client box.

## Regression coverage

Regression coverage includes:

- a compliant artboard that must report zero clipped text nodes
- a violating artboard where a constrained load-bearing headline wraps its text in a descendant span and must fail `text-clipping`
- a constrained headline using `overflow: visible` that must not be reported as clipped
- the committed ROAS motion example probed at multiple story timestamps to catch state-dependent load-bearing clipping
- render-report fixtures built from the same merged visual contract used by production code

## Scope boundary

This change detects text clipping by the text container's rendered client box. It does not attempt generic element collision detection, ancestor-container cropping outside the measured text role, intentional SVG cropping, or semantic judgments about whether arbitrary non-text overflow is desirable. Those remain separate future initiatives.
