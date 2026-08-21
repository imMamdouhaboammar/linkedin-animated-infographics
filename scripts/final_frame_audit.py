#!/usr/bin/env python3
"""Fail when finite browser animations are still in progress on the last exported frame."""

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
(finalSampleMs) => {
  const violations = [];
  const finite = [];

  function describeTarget(target) {
    if (!target) return '<unknown>';
    const tag = (target.tagName || 'element').toLowerCase();
    if (target.id) return `${tag}#${target.id}`;
    const classes = target.classList && target.classList.length
      ? '.' + [...target.classList].slice(0, 3).join('.')
      : '';
    return `${tag}${classes}`;
  }

  document.getAnimations().forEach((animation, index) => {
    const effect = animation.effect;
    if (!effect || !effect.getTiming || !effect.getComputedTiming) return;
    const timing = effect.getTiming();
    if (timing.iterations === Infinity) return;

    const computed = effect.getComputedTiming();
    const endTime = Number(computed.endTime);
    if (!Number.isFinite(endTime)) return;

    const target = effect.target || null;
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

  return {finite, violations};
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
                measured = page.evaluate(AUDIT_FINAL, final_sample_ms)
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
        "duration_ms": round(loop_ms, 3),
        "fps": args.fps,
        "frames": frames,
        "final_sample_ms": round(final_sample_ms, 3),
        "finite_animations": measured["finite"],
        "violations": violations,
        "verdict": "FAIL" if violations else "PASS",
    }
    write_report(report_path, report)

    if violations:
        print(f"final-frame audit: FAIL ({len(violations)} unfinished finite animation(s))")
        for row in violations[:8]:
            print(
                f"  {row['element']} {row['animation']}: "
                f"{row['remaining_ms']:.1f}ms remains after last exported frame"
            )
        return 1

    print(f"final-frame audit: PASS ({len(measured['finite'])} finite animation(s) complete)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
