#!/usr/bin/env python3
"""Shared browser probes for the render engine.

``check_render.py``, ``artboard_audit.py`` and ``capture_frames.py`` all need the same
three things: find a real Chrome, open an artboard deterministically, and measure the
DOM. That logic lives here once so the numbers cannot diverge between scripts.

Determinism notes that matter for measurement:

* Fonts are awaited before anything is measured, otherwise a fallback face is measured
  and every type number is wrong.
* Animations are paused and seeked, never left running, so two runs of the same file
  produce identical numbers.
* Measurements are taken from the browser's computed style, not from the source CSS,
  so cascade, inheritance and fallbacks are accounted for.

The JS probes intentionally return raw measurements only. Every threshold comparison
happens in Python against ``helper/visual-contract.json``.
"""

from __future__ import annotations

import contextlib
import os
import shlex
from pathlib import Path

BROWSER_CANDIDATES = [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/opt/google/chrome/chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_browser(explicit: str | None = None) -> str | None:
    """Locate a system Chrome. Returns None when none of the known paths exist."""
    if explicit:
        return explicit
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def resolve_browser(playwright, explicit: str | None = None) -> tuple[str | None, str]:
    """Decide which Chrome build to launch, and name it for the record.

    Returns ``(executable_path_or_None, label)``. ``None`` means "let Playwright use its
    own bundled build", which is the preferred case.

    Preference order is bundled-before-system on purpose. Playwright pins one Chromium
    revision; a system Chrome is whatever the machine happens to have installed that
    week. Font availability, text rasterisation and ``document.fonts.check()`` results
    all differ between builds, so the same artboard measured in two different Chromes
    produces two different numbers — which defeats the point of measuring. A system
    Chrome is still used when no bundled build is present, because a measurement from a
    named browser beats no measurement, and the label records which one it was.
    """
    if explicit:
        return explicit, explicit
    try:
        bundled = playwright.chromium.executable_path
    except Exception:
        bundled = None
    if bundled and Path(bundled).exists():
        # .../ms-playwright/chromium-1234/chrome-mac/Chromium.app/... -> "chromium-1234"
        revision = next((p.name for p in Path(bundled).parents
                         if p.name.startswith("chromium")), "bundled")
        return None, f"playwright {revision}"
    system = find_browser()
    if system:
        return system, f"system {system}"
    raise SystemExit(
        "No Chrome build available. Run: bash scripts/setup.sh "
        "(or pass --browser <path> to a Chrome/Chromium binary)")


# Pause every animation and hold it at a fixed time so measurement is repeatable.
SEEK_JS = """
(t) => {
  document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; });
  document.querySelectorAll('svg').forEach(s => {
    try { s.pauseAnimations(); s.setCurrentTime(t / 1000); } catch (e) {}
  });
}
"""

# Geometry: vertical occupancy, footer detachment, bordered containment depth.
#
# occupancy is the vertical span of real content over the artboard height. With the
# sanctioned 48px outer margins the arithmetic ceiling is (1350-96)/1350 = 92.9%, which
# is why the contract's documented band tops out around 92.
#
# A "surface" is an element that draws a container: a visible border, a background that
# differs from its parent, or a shadow, AND that holds at least one child element. Text
# chips and pills hold only text, so they do not inflate containment depth.
GEOMETRY_JS = """
() => {
  const board = document.querySelector('#artboard');
  const out = { board: null, content: null, footer: null, containment: 0,
                deepest: '', surfaces: 0, error: null };
  if (!board) { out.error = 'no #artboard element'; return out; }
  const br = board.getBoundingClientRect();
  out.board = { w: Math.round(br.width), h: Math.round(br.height) };
  if (!br.height) { out.error = 'artboard has zero height'; return out; }

  const area = r => Math.max(0, r.width) * Math.max(0, r.height);
  const boardArea = area(br);
  const visible = el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    return parseFloat(cs.opacity || '1') > 0.01;
  };
  const hasOwnText = el => [...el.childNodes].some(
    n => n.nodeType === 3 && n.textContent.trim().length > 0);
  const alpha = c => {
    const m = /rgba?\\(([^)]+)\\)/.exec(c || '');
    if (!m) return 0;
    const parts = m[1].split(',').map(s => parseFloat(s));
    return parts.length > 3 ? parts[3] : 1;
  };
  const borderedSides = cs => ['Top', 'Right', 'Bottom', 'Left'].filter(side =>
    parseFloat(cs['border' + side + 'Width']) >= 1 &&
    cs['border' + side + 'Style'] !== 'none' &&
    alpha(cs['border' + side + 'Color']) > 0.02).length;

  // Content elements: anything that draws ink and is not a full-bleed wrapper.
  const all = [...board.querySelectorAll('*')];
  const contentEls = all.filter(el => {
    if (!visible(el)) return false;
    const tag = el.tagName.toLowerCase();
    if (tag === 'style' || tag === 'script' || tag === 'defs') return false;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return false;
    if (area(r) > boardArea * 0.94) return false;   // background wrapper, not content
    const cs = getComputedStyle(el);
    return hasOwnText(el) || tag === 'img' || tag === 'svg' ||
           borderedSides(cs) > 0 || alpha(cs.backgroundColor) > 0.02;
  });
  if (!contentEls.length) { out.error = 'no content elements found'; return out; }

  let top = Infinity, bottom = -Infinity;
  contentEls.forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.top < top) top = r.top;
    if (r.bottom > bottom) bottom = r.bottom;
  });
  out.content = {
    top: Math.round(top - br.top),
    bottom: Math.round(bottom - br.top),
    span: Math.round(bottom - top),
    occupancy_pct: Math.round(1000 * (bottom - top) / br.height) / 10,
  };

  // Footer: the lowest text-bearing block. The gap that matters is between the end of
  // the primary composition (everything not in the footer) and the footer's top edge.
  const textEls = contentEls.filter(hasOwnText);
  if (textEls.length) {
    let footer = null, footerBottom = -Infinity;
    textEls.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.bottom > footerBottom) { footerBottom = r.bottom; footer = el; }
    });
    // Climb to the outermost block whose bottom matches, so a footer's inner span
    // does not count as the footer while its parent row counts as composition.
    let node = footer;
    while (node.parentElement && node.parentElement !== board) {
      const pr = node.parentElement.getBoundingClientRect();
      if (Math.abs(pr.bottom - footerBottom) <= 2) node = node.parentElement; else break;
    }
    const fr = node.getBoundingClientRect();
    let primaryBottom = -Infinity;
    contentEls.forEach(el => {
      if (node === el || node.contains(el)) return;
      const r = el.getBoundingClientRect();
      if (r.bottom > primaryBottom) primaryBottom = r.bottom;
    });
    out.footer = {
      tag: node.tagName.toLowerCase(),
      cls: (node.className && node.className.baseVal !== undefined
            ? node.className.baseVal : node.className || '').toString().slice(0, 60),
      top: Math.round(fr.top - br.top),
      bottom: Math.round(fr.bottom - br.top),
      gap_px: primaryBottom > -Infinity ? Math.round(fr.top - primaryBottom) : null,
      below_footer_px: Math.round(br.bottom - fr.bottom),
    };
  }

  // Bordered containment depth along every ancestor chain inside the artboard.
  const isSurface = el => {
    const cs = getComputedStyle(el);
    if (!el.children.length) return false;              // a chip is not a container
    const r = el.getBoundingClientRect();
    if (area(r) > boardArea * 0.94) return false;        // the page ground itself
    if (borderedSides(cs) >= 2) return true;
    if (cs.boxShadow && cs.boxShadow !== 'none') return true;
    const parent = el.parentElement;
    const parentBg = parent ? getComputedStyle(parent).backgroundColor : '';
    return alpha(cs.backgroundColor) > 0.02 && cs.backgroundColor !== parentBg;
  };
  let deepest = 0, deepestPath = '';
  all.forEach(el => {
    if (el.children.length) return;                     // measure from leaves upward
    let depth = 0;
    const path = [];
    for (let node = el.parentElement; node && node !== board.parentElement;
         node = node.parentElement) {
      if (node === board) break;
      if (isSurface(node)) {
        depth++;
        path.push(node.tagName.toLowerCase() +
          (node.className ? '.' + node.className.toString().trim().split(/\\s+/)[0] : ''));
      }
    }
    if (depth > deepest) { deepest = depth; deepestPath = path.reverse().join(' > '); }
  });
  out.containment = deepest;
  out.deepest = deepestPath;
  out.surfaces = all.filter(el => el.children.length && isSurface(el)).length;
  return out;
}
"""

# Type and rendered contrast on every text-bearing leaf.
#
# Contrast is computed on colours as they actually render, compositing alpha down the
# ancestor chain. The catalog validator only ever sees declared token pairs, so a token
# used at 60% opacity, or a light token landing on a light surface through a cascade
# mistake, is invisible to it and visible here.
TYPE_JS = """
() => {
  const board = document.querySelector('#artboard');
  const out = { nodes: [], error: null };
  if (!board) { out.error = 'no #artboard element'; return out; }
  const br = board.getBoundingClientRect();

  const parse = c => {
    const m = /rgba?\\(([^)]+)\\)/.exec(c || '');
    if (!m) return null;
    const p = m[1].split(',').map(s => parseFloat(s));
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const over = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a),
    g: fg.g * fg.a + bg.g * (1 - fg.a),
    b: fg.b * fg.a + bg.b * (1 - fg.a),
    a: 1,
  });
  const hex = c => '#' + [c.r, c.g, c.b]
    .map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0'))
    .join('');

  // Effective background: composite every translucent ancestor background down onto
  // white, which is what the browser paints against at the root.
  const effectiveBg = el => {
    const stack = [];
    for (let n = el; n; n = n.parentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0.001) stack.push(c);
      if (c && c.a >= 0.999) break;
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
    return base;
  };

  board.querySelectorAll('*').forEach(el => {
    const text = [...el.childNodes]
      .filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    if (!text) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const opacity = parseFloat(cs.opacity || '1');
    if (opacity <= 0.01) return;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;

    const bg = effectiveBg(el);
    let fg = parse(cs.color) || { r: 0, g: 0, b: 0, a: 1 };
    if (opacity < 1) fg = { ...fg, a: fg.a * opacity };
    const composited = over(fg, bg);

    out.nodes.push({
      size: Math.round(parseFloat(cs.fontSize) * 10) / 10,
      weight: cs.fontWeight,
      family: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(),
      fg: hex(composited),
      bg: hex(bg),
      chars: text.length,
      sample: text.slice(0, 48),
      top: Math.round(r.top - br.top),
      tag: el.tagName.toLowerCase(),
      cls: (el.className && el.className.baseVal !== undefined
            ? el.className.baseVal : el.className || '').toString().slice(0, 40),
    });
  });
  return out;
}
"""

# Animated elements: moving area and safe-margin intrusions.
MOTION_JS = """
(margin) => {
  const board = document.querySelector('#artboard');
  const out = { motionArea: 0, anims: 0, marginMotion: [], minClearance: null,
                error: null };
  if (!board) { out.error = 'no #artboard element'; return out; }
  const br = board.getBoundingClientRect();
  const animated = new Set();
  document.getAnimations().forEach(a => {
    if (a.effect && a.effect.target) animated.add(a.effect.target);
    out.anims++;
  });
  animated.forEach(el => {
    if (!el.getBoundingClientRect) return;
    const r = el.getBoundingClientRect();
    out.motionArea += Math.max(0, r.width) * Math.max(0, r.height);
    const clearance = Math.min(r.top - br.top, r.left - br.left,
                               br.right - r.right, br.bottom - r.bottom);
    if (out.minClearance === null || clearance < out.minClearance) {
      out.minClearance = Math.round(clearance * 10) / 10;
    }
    if (clearance < margin) {
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

# Which font families actually resolved. A named family that is not available falls
# back silently, so the same HTML renders with different typography on macOS and CI.
FONT_JS = """
() => {
  const board = document.querySelector('#artboard');
  const out = { stacks: [], error: null };
  if (!board) { out.error = 'no #artboard element'; return out; }
  const seen = new Set();
  const check = (family, weight) => {
    try { return document.fonts.check(`${weight} 16px ${family}`); }
    catch (e) { return null; }
  };
  const consider = el => {
    const cs = getComputedStyle(el);
    const stack = cs.fontFamily;
    const key = stack + '|' + cs.fontWeight;
    if (!stack || seen.has(key)) return;
    seen.add(key);
    const families = stack.split(',').map(s => s.replace(/["']/g, '').trim());
    const generics = new Set(['serif', 'sans-serif', 'monospace', 'cursive',
                              'fantasy', 'system-ui', 'ui-serif', 'ui-sans-serif',
                              'ui-monospace', 'ui-rounded']);
    const resolved = families.find(f => generics.has(f.toLowerCase()) ||
                                        check(JSON.stringify(f), cs.fontWeight));
    out.stacks.push({
      stack,
      weight: cs.fontWeight,
      first: families[0] || '',
      first_available: families.length
        ? (generics.has(families[0].toLowerCase()) ||
           check(JSON.stringify(families[0]), cs.fontWeight))
        : null,
      resolved: resolved || null,
    });
  };
  consider(board);
  board.querySelectorAll('*').forEach(el => {
    const hasText = [...el.childNodes].some(
      n => n.nodeType === 3 && n.textContent.trim().length > 0);
    if (hasText) consider(el);
  });
  return out;
}
"""


# Flags that make rasterisation reproducible across machines. Subpixel antialiasing and
# font hinting are display-dependent, and the GPU path introduces driver-dependent
# rounding, so all three are switched off before anything is measured or captured.
DETERMINISM_ARGS = [
    "--disable-lcd-text",
    "--font-render-hinting=none",
    "--force-color-profile=srgb",
    "--disable-gpu",
]

# Some sandboxes deny the Mach port / ProcessSingleton socket that Chromium's default
# multi-process launch needs. Collapsing to one process is the documented workaround. It
# keeps Blink identical — same layout, same rasteriser, same font stack — and only gives
# up process isolation, so measurements stay comparable. It is never the first choice,
# and when it is used the report says so.
CONSTRAINED_ARGS = ["--single-process", "--no-zygote"]


def _launch(playwright, executable: str | None):
    """Launch Chromium, preferring the isolated multi-process default.

    Returns ``(browser, launch_mode)``. ``launch_mode`` is recorded in the capture info so
    a reader can tell whether the measurement came from a standard launch or a degraded
    one. Extra flags can be appended through ``RENDER_CHROME_ARGS`` (space-separated) for
    environments that need them without the engine hardcoding a local workaround.
    """
    extra = shlex.split(os.environ.get("RENDER_CHROME_ARGS", ""))
    base = {"args": DETERMINISM_ARGS + extra}
    if executable:
        base["executable_path"] = executable

    try:
        return playwright.chromium.launch(**base), "standard"
    except Exception as first_error:
        constrained = dict(base, args=base["args"] + CONSTRAINED_ARGS)
        try:
            return playwright.chromium.launch(**constrained), "single-process"
        except Exception:
            raise SystemExit(
                "Chromium could not start. Run: bash scripts/setup.sh\n"
                f"  {str(first_error).strip().splitlines()[0]}"
            ) from first_error


@contextlib.contextmanager
def open_artboard(html_path, *, width=1080, height=1350, at=0.0, browser=None,
                  settle=600):
    """Open an artboard paused at ``at`` seconds and yield ``(page, info)``.

    ``info`` records the conditions the measurement was taken under — browser build,
    launch mode, viewport, seek time — because a number without its capture conditions is
    not evidence. Raises SystemExit with an actionable message when Playwright or Chrome
    is absent, matching how the existing render scripts report a missing toolchain.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("playwright is not installed. Run: bash scripts/setup.sh")

    target = Path(html_path)
    if not target.is_file():
        raise SystemExit(f"No such file: {target}")

    with sync_playwright() as p:
        executable, label = resolve_browser(p, browser)
        instance, mode = _launch(p, executable)
        page = instance.new_page(viewport={"width": width, "height": height})
        try:
            page.goto(target.resolve().as_uri(), wait_until="load")
            try:
                page.evaluate("() => document.fonts && document.fonts.ready")
            except Exception:
                pass
            page.wait_for_timeout(settle)
            page.evaluate(SEEK_JS, at * 1000)
            yield page, {
                "browser": label,
                "browser_version": instance.version,
                "launch_mode": mode,
                "viewport": {"width": width, "height": height},
                "seeked_at_s": at,
                "settle_ms": settle,
            }
        finally:
            instance.close()
