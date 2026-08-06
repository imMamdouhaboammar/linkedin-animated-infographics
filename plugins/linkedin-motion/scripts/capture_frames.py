#!/usr/bin/env python3
"""
capture_frames.py — deterministic frame capture for animated infographics.

Loads an HTML artboard in headless Chrome, pauses every animation, then seeks
each one to an exact timestamp and screenshots. Because the animations are
*seeked* rather than recorded in real time, every frame is pixel-exact and the
loop closes perfectly.

Handles three animation systems:
  1. CSS @keyframes and WAAPI  -> document.getAnimations()
  2. SVG SMIL (<animateMotion>) -> svgRoot.setCurrentTime()
  3. CSS transitions            -> disabled entirely (they are not seekable)

Usage:
    python3 capture_frames.py post.html --out frames/ --duration 4.8 --fps 12.5
    python3 capture_frames.py post.html --out frames/ --duration 4.8 --fps 12.5 \
            --selector "#artboard" --scale 1 --browser /usr/bin/google-chrome
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright is not installed. Run: bash scripts/setup.sh")


# Chrome/Chromium binaries we will try, in order, if --browser is not given.
BROWSER_CANDIDATES = [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/opt/google/chrome/chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]

# Injected before the page renders. Kills transitions (unseekable) and any
# animation that would otherwise start on a timer we do not control.
PREP_CSS = """
* {
  transition: none !important;
  -webkit-transition: none !important;
}
"""

# Pause everything, once, after load.
PAUSE_ALL = """
() => {
  document.getAnimations().forEach(a => {
    try { a.pause(); } catch (e) {}
  });
  document.querySelectorAll('svg').forEach(svg => {
    try { svg.pauseAnimations(); } catch (e) {}
  });
  return document.getAnimations().length;
}
"""

# Seek everything to time t (milliseconds).
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

# Report anything that cannot be seeked, so the user gets a warning instead of
# a silently broken render.
AUDIT = """
() => {
  const report = { animations: 0, infinite: 0, durations: [], rafDetected: false };
  document.getAnimations().forEach(a => {
    report.animations++;
    const t = a.effect && a.effect.getTiming ? a.effect.getTiming() : {};
    if (t.iterations === Infinity) report.infinite++;
    if (typeof t.duration === 'number') report.durations.push(Math.round(t.duration));
  });
  report.rafDetected = !!window.__rafUsed;
  return report;
}
"""

# Flag any use of requestAnimationFrame, which cannot be seeked.
RAF_TRAP = """
(() => {
  const orig = window.requestAnimationFrame;
  window.__rafUsed = false;
  window.requestAnimationFrame = function (cb) {
    window.__rafUsed = true;
    return orig.call(window, cb);
  };
})();
"""


def find_browser(explicit=None):
    if explicit:
        if Path(explicit).exists():
            return explicit
        sys.exit(f"Browser not found at {explicit}")
    for c in BROWSER_CANDIDATES:
        if Path(c).exists():
            return c
    # Fall back to Playwright's own bundled Chromium.
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", help="path to the HTML artboard")
    ap.add_argument("--out", default="frames", help="output directory for PNG frames")
    ap.add_argument("--duration", type=float, required=True,
                    help="loop duration in seconds (must match --loop in the CSS)")
    ap.add_argument("--fps", type=float, default=12.5, help="frames per second")
    ap.add_argument("--selector", default="#artboard",
                    help="element to screenshot; falls back to full page if missing")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--scale", type=float, default=1.0,
                    help="device scale factor; 2 renders retina then downsample")
    ap.add_argument("--browser", default=None, help="path to a Chrome/Chromium binary")
    ap.add_argument("--settle", type=int, default=600,
                    help="ms to wait after load for fonts and images")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    html_path = Path(args.html).resolve()
    if not html_path.exists():
        sys.exit(f"No such file: {html_path}")

    out_dir = Path(args.out)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    n_frames = int(round(args.duration * args.fps))
    if n_frames < 2:
        sys.exit("duration x fps must give at least 2 frames")

    def log(*a):
        if not args.quiet:
            print(*a, flush=True)

    log(f"artboard : {html_path.name}")
    log(f"loop     : {args.duration}s @ {args.fps} fps -> {n_frames} frames")

    exe = find_browser(args.browser)
    launch_args = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        "--force-color-profile=srgb",
        "--disable-lcd-text",          # grayscale AA -> fewer colours -> smaller GIF
        "--font-render-hinting=none",  # identical text rasterisation every frame
        "--disable-gpu",
    ]

    with sync_playwright() as p:
        launch_kwargs = {"args": launch_args}
        if exe:
            launch_kwargs["executable_path"] = exe
            log(f"browser  : {exe}")
        browser = p.chromium.launch(**launch_kwargs)

        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        page.add_init_script(RAF_TRAP)
        page.goto(html_path.as_uri(), wait_until="load")
        page.add_style_tag(content=PREP_CSS)

        # Let webfonts and images settle before we freeze anything.
        try:
            page.evaluate("() => document.fonts && document.fonts.ready")
        except Exception:
            pass
        page.wait_for_timeout(args.settle)

        count = page.evaluate(PAUSE_ALL)
        report = page.evaluate(AUDIT)
        log(f"animations: {count} found, {report['infinite']} infinite")

        if report["rafDetected"]:
            log("  WARNING: requestAnimationFrame detected. rAF motion cannot be "
                "seeked and will render frozen. Convert it to CSS keyframes.")

        durations = sorted(set(report["durations"]))
        loop_ms = args.duration * 1000
        odd = [d for d in durations
               if d and abs((loop_ms / d) - round(loop_ms / d)) > 0.001]
        if odd:
            log(f"  WARNING: durations that do not divide the loop cleanly: {odd}ms")
            log(f"           loop is {int(loop_ms)}ms. These will not close seamlessly.")

        target = page.query_selector(args.selector)
        if target is None:
            log(f"  NOTE: '{args.selector}' not found, capturing the full viewport")

        step_ms = loop_ms / n_frames
        for i in range(n_frames):
            t = i * step_ms
            page.evaluate(SEEK_ALL, t)
            path = out_dir / f"f{i:04d}.png"
            if target is not None:
                target.screenshot(path=str(path))
            else:
                page.screenshot(path=str(path))
            if not args.quiet and (i % 10 == 0 or i == n_frames - 1):
                log(f"  frame {i + 1}/{n_frames}")

        browser.close()

    meta = {
        "html": str(html_path),
        "frames": n_frames,
        "fps": args.fps,
        "duration": args.duration,
        "width": args.width,
        "height": args.height,
        "scale": args.scale,
    }
    (out_dir / "capture.json").write_text(json.dumps(meta, indent=2))
    log(f"done     : {n_frames} frames in {out_dir}/")


if __name__ == "__main__":
    main()
