#!/usr/bin/env python3
"""
check_render.py — render the still frame and audit it before you animate.

Produces:
  - the full 1080x1350 still (frame 0 of the loop)
  - a 350px-wide downscale, which is roughly how LinkedIn renders it in feed
  - a text audit: artboard size, smallest rendered text, safe-zone violations,
    and how much of the canvas is animated

Run this before writing any animation CSS. The still is the approval gate.

Usage:
    python3 check_render.py build/post.html --out build/still.png
    python3 check_render.py build/post.html --out build/still.png --at 2.4
"""

import argparse
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright is not installed. Run: bash scripts/setup.sh")

BROWSER_CANDIDATES = [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/opt/google/chrome/chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

AUDIT = """
(margin) => {
  const board = document.querySelector('#artboard');
  const out = { board: null, smallText: [], marginMotion: [], motionArea: 0, anims: 0 };
  if (!board) return out;
  const br = board.getBoundingClientRect();
  out.board = { w: Math.round(br.width), h: Math.round(br.height) };

  // Smallest rendered text, walking leaf nodes that actually contain characters.
  const seen = new Map();
  document.querySelectorAll('#artboard *').forEach(el => {
    const hasText = [...el.childNodes].some(
      n => n.nodeType === 3 && n.textContent.trim().length > 0);
    if (!hasText) return;
    const cs = getComputedStyle(el);
    const size = parseFloat(cs.fontSize);
    const sample = el.textContent.trim().slice(0, 42);
    if (!seen.has(size)) seen.set(size, sample);
  });
  out.smallText = [...seen.entries()]
    .sort((a, b) => a[0] - b[0]).slice(0, 5)
    .map(([size, sample]) => ({ size: Math.round(size * 10) / 10, sample }));

  // Animated elements: total moving area, and anything inside the safe margin.
  const animated = new Set();
  document.getAnimations().forEach(a => {
    if (a.effect && a.effect.target) animated.add(a.effect.target);
    out.anims++;
  });
  animated.forEach(el => {
    const r = el.getBoundingClientRect();
    out.motionArea += Math.max(0, r.width) * Math.max(0, r.height);
    const inMargin =
      r.top    < br.top + margin    ||
      r.left   < br.left + margin   ||
      r.right  > br.right - margin  ||
      r.bottom > br.bottom - margin;
    if (inMargin) {
      out.marginMotion.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className && el.className.baseVal !== undefined
              ? el.className.baseVal : el.className || '').toString().slice(0, 40),
      });
    }
  });
  return out;
}
"""


def find_browser(explicit=None):
    if explicit:
        return explicit
    for c in BROWSER_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--out", default="still.png")
    ap.add_argument("--at", type=float, default=0.0,
                    help="seek all animations to this time in seconds before capture")
    ap.add_argument("--selector", default="#artboard")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--margin", type=int, default=48,
                    help="safe margin in px that nothing should animate inside")
    ap.add_argument("--browser", default=None)
    args = ap.parse_args()

    html = Path(args.html).resolve()
    if not html.exists():
        sys.exit(f"No such file: {html}")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars",
                       "--force-color-profile=srgb", "--disable-lcd-text",
                       "--font-render-hinting=none", "--disable-gpu"]}
        exe = find_browser(args.browser)
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.goto(html.as_uri(), wait_until="load")
        try:
            page.evaluate("() => document.fonts && document.fonts.ready")
        except Exception:
            pass
        page.wait_for_timeout(600)
        page.evaluate(
            "(t) => { document.getAnimations().forEach(a => { a.pause(); "
            "a.currentTime = t; }); "
            "document.querySelectorAll('svg').forEach(s => { "
            "try { s.pauseAnimations(); s.setCurrentTime(t/1000); } catch(e){} }); }",
            args.at * 1000,
        )
        report = page.evaluate(AUDIT, args.margin)
        el = page.query_selector(args.selector)
        (el or page).screenshot(path=str(out))
        browser.close()

    # Mobile preview.
    mobile = out.with_name(out.stem + "_mobile350.png")
    try:
        from PIL import Image
        im = Image.open(out)
        w = 350
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(mobile)
    except ImportError:
        mobile = None

    canvas = args.width * args.height
    pct = 100.0 * report["motionArea"] / canvas if canvas else 0

    print("── artboard ─────────────────────────────────")
    if report["board"]:
        b = report["board"]
        ok = "ok" if (b["w"], b["h"]) == (1080, 1350) else "expected 1080x1350"
        print(f"  size            {b['w']}x{b['h']}  ({ok})")
    else:
        print(f"  '{args.selector}' not found — captured the viewport instead")

    print("── type ─────────────────────────────────────")
    for t in report["smallText"]:
        flag = "  TOO SMALL for feed" if t["size"] < 22 else ""
        print(f"  {t['size']:>5}px   {t['sample']!r}{flag}")
    print("  (below 22px is unreadable at LinkedIn's ~350px feed width)")

    print("── motion ───────────────────────────────────")
    print(f"  animations      {report['anims']}")
    print(f"  moving area     {pct:.1f}% of canvas"
          f"   {'ok' if pct <= 20 else 'OVER BUDGET, target under 20%'}")
    if pct > 20:
        print("  Note: this counts each animated element's full bounding box. A stroked"
              "\n        circle or path reports its whole box while only the stroke moves,"
              "\n        so ring and wire animations overstate here. Judge those on the"
              "\n        final GIF size instead.")
    if report["marginMotion"]:
        print(f"  SAFE-ZONE VIOLATION: {len(report['marginMotion'])} animated element(s) "
              f"inside the {args.margin}px margin:")
        for m in report["marginMotion"][:6]:
            print(f"    <{m['tag']} class=\"{m['cls']}\">")
        print("  The title block and footer must stay still.")
    else:
        print(f"  margin          clean ({args.margin}px)")

    print("── output ───────────────────────────────────")
    print(f"  still           {out}")
    if mobile:
        print(f"  mobile preview  {mobile}   <- judge legibility on this one")


if __name__ == "__main__":
    main()
