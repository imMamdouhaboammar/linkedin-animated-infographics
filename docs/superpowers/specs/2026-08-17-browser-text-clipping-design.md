# Browser Text Clipping Gate

Date: 2026-08-17

## Problem

The rendered artboard audit already measures canvas size, occupancy, footer detachment, containment depth, typography, contrast, and font fallback, but it does not mechanically detect text that is truncated by a constrained box. The QA guide says no content may be clipped, yet that requirement currently depends on human inspection.

## Decision

Add browser-measured text clipping evidence to `scripts/artboard_audit.py` and make clipping of load-bearing text a blocking visual gate.

A text node is considered clipped when its rendered `scrollWidth` exceeds `clientWidth` or its rendered `scrollHeight` exceeds `clientHeight`, allowing a one-pixel tolerance for browser rounding. The probe records the element role, text sample, client dimensions, scroll dimensions, overflow mode, and whether it is load-bearing.

Load-bearing classification uses the same role hints already used by the feed-scale typography audit: headline, hero, title, takeaway, subline, lede, and kicker. Clipping in these roles blocks export. Other clipped text is reported as advisory evidence so intentional micro-copy truncation does not create a false hard failure.

## Contract

Add two thresholds:

- `type.max_clipped_load_bearing_nodes = 0`, blocking, gate `text-clipping`
- `type.max_clipped_nodes = 0`, advisory, gate `text-clipping`

The blocking threshold is documented against the existing QA requirement that no content is clipped.

## Report changes

`artboard_audit.py` will add both findings and expose clipping measurements in the machine-readable report. Failure evidence names the rendered element and the amount by which its scroll box exceeds its client box.

## Regression coverage

The violating browser fixture will include one deliberately clipped headline. Tests will require the new blocking threshold to fail with evidence. The compliant fixture must remain warning-free and failure-free.

## Scope boundary

This change detects text clipping only. It does not attempt generic element collision detection, intentional SVG cropping, or semantic judgments about whether arbitrary non-text overflow is desirable. Those remain separate future initiatives.
