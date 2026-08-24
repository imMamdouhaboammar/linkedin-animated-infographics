#!/usr/bin/env python3
"""Fail when exported final-frame motion or required final-state visibility is incomplete."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright is not installed. Run: bash scripts/setup.sh")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.capture_frames import BROWSER_CANDIDATES, PREP_CSS
from scripts.visual_contract import file_sha256

PAUSE_ALL = """
() => {
  document.getAnimations().forEach(a => {
    try { a.pause(); } catch (e) {}
  });
  document.querySelectorAll('svg').forEach(svg => {
    try { svg.pauseAnimations(); } catch (e) {}
  });
}
"""

SEEK_ALL = """
(tMs) => {
  document.getAnimations().forEach(a => {
    try {
      a.pause();
      a.currentTime = tMs;
    } catch (e) {}
  });
  document.querySelectorAll('svg').forEach(svg => {
    try { svg.setCurrentTime(tMs / 1000); } catch (e) {}
  });
}
"""

AUDIT_FINAL = """
({finalSampleMs, selector}) => {
  const violations = [];
  const finite = [];
  const requiredVisible = [];
  const requestedRoot = document.querySelector(selector);
  const root = requestedRoot || document.documentElement;
  const selectorFound = Boolean(requestedRoot);

  function describeTarget(target) {
    if (!target) return '<unknown>';
    const tag = (target.tagName || 'element').toLowerCase();
    if (target.id) return `${tag}#${target.id}`;
    const classes = target.classList && target.classList.length
      ? '.' + [...target.classList].slice(0, 3).join('.')
      : '';
    return `${tag}${classes}`;
  }

  function rounded(value) {
    return Math.round(value * 1000) / 1000;
  }

  function finalHitTest(target, rect, rootRect) {
    const left = Math.max(rect.left, rootRect.left, 0);
    const right = Math.min(rect.right, rootRect.right, window.innerWidth);
    const top = Math.max(rect.top, rootRect.top, 0);
    const bottom = Math.min(rect.bottom, rootRect.bottom, window.innerHeight);
    if (right - left <= 1 || bottom - top <= 1) {
      return {sample_count: 0, visible_samples: 0, blockers: []};
    }

    const xs = [0.2, 0.5, 0.8];
    const ys = [0.2, 0.5, 0.8];
    const fractions = [
      [xs[1], ys[1]],
      [xs[0], ys[0]],
      [xs[2], ys[0]],
      [xs[0], ys[2]],
      [xs[2], ys[2]],
    ];
    const blockers = new Set();
    let visibleSamples = 0;
    const previousPointerEvents = target.style.pointerEvents;
    target.style.pointerEvents = 'auto';
    try {
      for (const [fx, fy] of fractions) {
        const x = left + (right - left) * fx;
        const y = top + (bottom - top) * fy;
        const stack = document.elementsFromPoint(x, y);
        const targetIndex = stack.findIndex(node => node === target || target.contains(node));
        if (targetIndex >= 0) {
          visibleSamples += 1;
        } else if (stack.length) {
          blockers.add(describeTarget(stack[0]));
        }
      }
    } finally {
      target.style.pointerEvents = previousPointerEvents;
    }
    return {
      sample_count: fractions.length,
      visible_samples: visibleSamples,
      blockers: [...blockers].slice(0, 5),
    };
  }

  document.getAnimations().forEach((animation, index) => {
    const effect = animation.effect;
    if (!effect || !effect.getTiming || !effect.getComputedTiming) return;
    const target = effect.target || null;
    if (!(target instanceof Element) || (target !== root && !root.contains(target))) return;

    const timing = effect.getTiming();
    if (timing.iterations === Infinity) return;

    const computed = effect.getComputedTiming();
    const endTime = Number(computed.endTime);
    if (!Number.isFinite(endTime)) return;

    const row = {
      index,
      animation: animation.animationName || animation.id || `animation-${index}`,
      element: describeTarget(target),
      end_time_ms: Math.round(endTime * 1000) / 1000,
      progress: computed.progress,
      current_iteration: computed.currentIteration,
    };
    finite.push(row);

    if (endTime > finalSampleMs + 0.5) {
      violations.push({
        ...row,
        reason: 'finite-animation-incomplete',
        remaining_ms: Math.round((endTime - finalSampleMs) * 1000) / 1000,
      });
    }
  });

  const visibilityTargets = [];
  if (root instanceof Element && root.hasAttribute('data-final-visible')) visibilityTargets.push(root);
  root.querySelectorAll('[data-final-visible]').forEach(node => visibilityTargets.push(node));
  const rootRect = root.getBoundingClientRect();

  visibilityTargets.forEach(target => {
    const style = getComputedStyle(target);
    const rect = target.getBoundingClientRect();
    const opacity = Number.parseFloat(style.opacity);
    const reasons = [];
    const intersectsRoot = rect.right > rootRect.left + 0.5
      && rect.left < rootRect.right - 0.5
      && rect.bottom > rootRect.top + 0.5
      && rect.top < rootRect.bottom - 0.5;
    const fullyInsideRoot = rect.left >= rootRect.left - 0.5
      && rect.right <= rootRect.right + 0.5
      && rect.top >= rootRect.top - 0.5
      && rect.bottom <= rootRect.bottom + 0.5;
    const intersectionWidth = Math.max(0, Math.min(rect.right, rootRect.right) - Math.max(rect.left, rootRect.left));
    const intersectionHeight = Math.max(0, Math.min(rect.bottom, rootRect.bottom) - Math.max(rect.top, rootRect.top));
    const area = Math.max(0, rect.width) * Math.max(0, rect.height);
    const visibleArea = intersectionWidth * intersectionHeight;
    const visibleRatio = area > 0 ? visibleArea / area : 0;
    const clipping = {
      left_px: rounded(Math.max(0, rootRect.left - rect.left)),
      right_px: rounded(Math.max(0, rect.right - rootRect.right)),
      top_px: rounded(Math.max(0, rootRect.top - rect.top)),
      bottom_px: rounded(Math.max(0, rect.bottom - rootRect.bottom)),
    };

    if (style.display === 'none') reasons.push('display-none');
    if (style.visibility === 'hidden' || style.visibility === 'collapse') reasons.push(`visibility-${style.visibility}`);
    if (Number.isFinite(opacity) && opacity <= 0.01) reasons.push('opacity-zero');
    if (rect.width <= 0.5 || rect.height <= 0.5) reasons.push('zero-area');
    if (!intersectsRoot) reasons.push('outside-export-root');
    else if (!fullyInsideRoot) reasons.push('clipped-by-export-root');

    let ancestor = target.parentElement;
    while (ancestor && ancestor !== root.parentElement) {
      const ancestorStyle = getComputedStyle(ancestor);
      const ancestorOpacity = Number.parseFloat(ancestorStyle.opacity);
      if (ancestorStyle.display === 'none') {
        reasons.push('ancestor-display-none');
        break;
      }
      if (ancestorStyle.visibility === 'hidden' || ancestorStyle.visibility === 'collapse') {
        reasons.push(`ancestor-visibility-${ancestorStyle.visibility}`);
        break;
      }
      if (Number.isFinite(ancestorOpacity) && ancestorOpacity <= 0.01) {
        reasons.push('ancestor-opacity-zero');
        break;
      }
      if (ancestor === root) break;
      ancestor = ancestor.parentElement;
    }

    const hitTest = finalHitTest(target, rect, rootRect);
    if (reasons.length === 0 && hitTest.sample_count > 0 && hitTest.visible_samples === 0) {
      reasons.push('occluded');
    }

    const uniqueReasons = [...new Set(reasons)];
    const row = {
      element: describeTarget(target),
      opacity: Number.isFinite(opacity) ? rounded(opacity) : null,
      display: style.display,
      visibility: style.visibility,
      rect: {
        x: rounded(rect.x),
        y: rounded(rect.y),
        width: rounded(rect.width),
        height: rounded(rect.height),
      },
      visible_ratio: rounded(visibleRatio),
      clipping,
      hit_test: hitTest,
      reasons: uniqueReasons,
    };
    requiredVisible.push(row);

    if (uniqueReasons.length) {
      violations.push({
        ...row,
        reason: 'required-final-element-hidden',
      });
    }
  });

  return {finite, requiredVisible, violations, selectorFound};
}
"""


def find_browser(explicit: str | None) -> str | None:
    if explicit:
        if Path(explicit).exists():
            return explicit
        raise ValueError(f"Browser not found at {explicit}")
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html")
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--fps", type=float, default=12.5)
    parser.add_argument("--selector", default="#artboard")
    parser.add_argument("--json", default="build/.render-evidence/final-frame.json")
    parser.add_argument("--browser")
    parser.add_argument("--settle", type=int, default=300)
    args = parser.parse_args(argv)

    html = Path(args.html).resolve()
    report_path = Path(args.json)
    if not html.is_file():
        print(f"No such file: {html}", file=sys.stderr)
        return 2
    if args.duration <= 0 or args.fps <= 0:
        print("duration and fps must be positive", file=sys.stderr)
        return 2

    frames = int(round(args.duration * args.fps))
    if frames < 2:
        print("duration x fps must give at least 2 frames", file=sys.stderr)
        return 2

    loop_ms = args.duration * 1000.0
    step_ms = loop_ms / frames
    final_sample_ms = (frames - 1) * step_ms

    try:
        browser_path = find_browser(args.browser)
        with sync_playwright() as playwright:
            launch = {"args": ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"]}
            if browser_path:
                launch["executable_path"] = browser_path
            browser = playwright.chromium.launch(**launch)
            try:
                page = browser.new_page(viewport={"width": 1080, "height": 1350})
                page.goto(html.as_uri(), wait_until="load")
                page.add_style_tag(content=PREP_CSS)
                try:
                    page.evaluate("() => document.fonts && document.fonts.ready")
                except Exception:
                    pass
                page.wait_for_timeout(args.settle)
                page.evaluate(PAUSE_ALL)
                page.evaluate(SEEK_ALL, final_sample_ms)
                measured = page.evaluate(
                    AUDIT_FINAL,
                    {"finalSampleMs": final_sample_ms, "selector": args.selector},
                )
            finally:
                browser.close()
    except Exception as exc:
        message = str(exc)
        if "Executable doesn't exist" in message or "Failed to launch" in message:
            message = "Chromium could not start. Run: python3 -m playwright install chromium"
        print(message, file=sys.stderr)
        return 2

    violations = measured["violations"]
    report = {
        "schema_version": 1,
        "stage": "final-frame",
        "artifact": str(html),
        "artifact_sha256": file_sha256(html),
        "selector": args.selector,
        "selector_found": measured["selectorFound"],
        "duration_ms": round(loop_ms, 3),
        "fps": args.fps,
        "frames": frames,
        "final_sample_ms": round(final_sample_ms, 3),
        "finite_animations": measured["finite"],
        "required_visible_elements": measured["requiredVisible"],
        "violations": violations,
        "verdict": "FAIL" if violations else "PASS",
    }
    write_report(report_path, report)

    if violations:
        print(f"final-frame audit: FAIL ({len(violations)} final-state violation(s))")
        for row in violations[:8]:
            if row["reason"] == "finite-animation-incomplete":
                print(
                    f"  {row['element']} {row['animation']}: "
                    f"{row['remaining_ms']:.1f}ms remains after last exported frame"
                )
            else:
                print(f"  {row['element']}: invalid final state ({', '.join(row.get('reasons', []))})")
        return 1

    print(
        "final-frame audit: PASS "
        f"({len(measured['finite'])} finite animation(s) complete, "
        f"{len(measured['requiredVisible'])} required final element(s) visible)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
