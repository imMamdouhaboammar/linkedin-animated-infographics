#!/usr/bin/env python3
"""Validate a finished animation against the asset contract.

Usage:
  python3 check_asset.py <file.svg> [more.svg ...]   static track
  python3 check_asset.py --runtime <scene.html>      runtime track (Anime.js)

Exits non-zero if any FAIL is reported. WARN items are judgement calls worth a
second look rather than hard errors.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"


def check(path):
    stem = os.path.basename(path).rsplit(".", 1)[0]
    src = open(path).read()
    fails, warns, oks = [], [], []

    try:
        root = ET.fromstring(src)
    except ET.ParseError as e:
        return [f"XML does not parse: {e}"], [], []

    # accessibility
    if root.get("role") == "img":
        oks.append('role="img"')
    else:
        fails.append('root svg is missing role="img"')

    labelled = root.get("aria-labelledby", "")
    tids = [t.get("id") for t in root.iter(f"{NS}title")]
    dids = [d.get("id") for d in root.iter(f"{NS}desc")]
    if tids and dids and all(i and i in labelled for i in tids[:1] + dids[:1]):
        oks.append("title and desc wired through aria-labelledby")
    else:
        fails.append("needs <title> and <desc> with ids referenced by aria-labelledby")

    if not root.get("viewBox"):
        fails.append("missing viewBox, the file will not scale")
    else:
        oks.append("viewBox present")

    # motion accessibility
    if "prefers-reduced-motion" in src:
        oks.append("prefers-reduced-motion fallback present")
    else:
        fails.append("no @media (prefers-reduced-motion:reduce) block")

    if "prefers-color-scheme" in src:
        oks.append("dark mode block present")
    else:
        warns.append("no prefers-color-scheme block; confirm neutrals read on both themes")

    # animation actually exists
    kfs = re.findall(r"@keyframes\s+([\w-]+)", src)
    smil = re.search(r"<(animate|animateTransform|animateMotion)\b", src)
    if not kfs and not smil:
        fails.append("no CSS keyframes and no SMIL; nothing will move")
    else:
        oks.append(f"{len(kfs)} keyframe blocks" + (" plus SMIL" if smil else ""))

    # id and keyframe namespacing
    ids = [el.get("id") for el in root.iter() if el.get("id")]
    bad_ids = [i for i in ids if not i.startswith(stem)]
    if bad_ids:
        fails.append(f"ids not prefixed with '{stem}': {', '.join(bad_ids[:6])}"
                     " (they will collide when several files are inlined on one page)")
    elif ids:
        oks.append(f"all {len(ids)} ids namespaced")

    bad_kf = [k for k in kfs if not k.startswith(stem)]
    if bad_kf:
        warns.append(f"keyframe names not prefixed with '{stem}': {', '.join(bad_kf[:6])}")
    elif kfs:
        oks.append("keyframe names namespaced")

    # img-context hazards
    if "<script" in src:
        fails.append("contains <script>; it will not execute inside <img>")
    if "@font-face" in src or "fonts.googleapis" in src:
        fails.append("loads an external font; it will not resolve inside <img>")
    ext = [u for u in re.findall(r'(?:href|src)="(https?://[^"]+)"', src)]
    if ext:
        fails.append(f"external reference will be blocked: {ext[0]}")
    if "xlink:href" in src and "xmlns:xlink" not in src:
        fails.append("uses xlink:href without declaring the xlink namespace")

    # scaling traps
    scaled = re.findall(r"transform:\s*scale", src) + re.findall(r"scaleX|scaleY", src)
    if scaled and "transform-box" not in src:
        warns.append("scales or rotates without transform-box; origins will resolve against "
                     "the viewport rather than the element and drift")

    # size sanity
    kb = len(src.encode()) / 1024
    if kb > 60:
        warns.append(f"{kb:.0f}KB is heavy for a README asset; reduce sample counts")
    else:
        oks.append(f"{kb:.1f}KB")

    return fails, warns, oks


def check_runtime(path):
    """Runtime track: Anime.js drives the page, so the rules differ. Scripting is
    expected; what matters is that the engine is pinned, the API is v4, motion
    preference is honoured, and the scene still describes itself."""
    src = open(path).read()
    fails, warns, oks = [], [], []

    imports = re.findall(r"from\s+['\"]([^'\"]*animejs[^'\"]*)['\"]", src)
    if not imports:
        fails.append("no animejs import found; the runtime track expects the engine")
    else:
        oks.append(f"imports {imports[0]}")
        remote = [i for i in imports if i.startswith("http")]
        if remote and not re.search(r"animejs@\d+\.\d+", remote[0]):
            fails.append("CDN import is unpinned; a future release can change the motion")
        elif remote:
            oks.append("engine version pinned")

    if re.search(r"\banime\s*\(\s*\{", src) or "anime.timeline(" in src \
            or "anime.path(" in src or "easing:" in src:
        fails.append("v3 syntax detected (anime({targets}), anime.timeline, anime.path, "
                     "easing:); none of it runs on v4")
    if "createSpring(" in src:
        warns.append("createSpring() is deprecated in 4.5; use spring()")

    if "<script" in src and 'type="module"' not in src and "type='module'" not in src:
        fails.append("Anime.js v4 is ESM only; the script tag needs type=\"module\"")
    else:
        oks.append("module script")

    if "prefers-reduced-motion" in src:
        oks.append("reduced-motion handled")
    else:
        fails.append("no prefers-reduced-motion handling; guard with matchMedia and seek "
                     "the timeline to its resting pose")

    if "prefers-color-scheme" in src:
        oks.append("dark mode block present")
    else:
        warns.append("no prefers-color-scheme block")

    if 'role="img"' in src and "<title" in src and "<desc" in src:
        oks.append("scene describes itself")
    else:
        warns.append("inline svg should carry role=\"img\" with title and desc, since a "
                     "screen reader cannot watch the motion")

    if "duration:" in src and "ease: spring(" in src.replace("ease:spring(", "ease: spring("):
        warns.append("check that no spring() sits next to an explicit duration; overriding "
                     "it discards the settling time the solver computed")

    if "createScope(" in src or ".revert()" in src:
        oks.append("cleanup path present")
    else:
        warns.append("no createScope or revert(); animations will leak if the host unmounts")

    return fails, warns, oks


def main(paths):
    runtime = "--runtime" in paths
    paths = [p for p in paths if not p.startswith("--")]
    bad = 0
    for p in paths:
        fails, warns, oks = check_runtime(p) if runtime else check(p)
        print(f"\n{os.path.basename(p)}")
        for o in oks:
            print(f"  ok    {o}")
        for w in warns:
            print(f"  warn  {w}")
        for f in fails:
            print(f"  FAIL  {f}")
        bad += len(fails)
    print(f"\n{'contract satisfied' if not bad else str(bad) + ' failures'}")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
