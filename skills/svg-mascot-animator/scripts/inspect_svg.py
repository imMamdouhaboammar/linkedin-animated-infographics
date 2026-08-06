#!/usr/bin/env python3
"""Report the geometry and riggability of a source SVG.

Usage: python inspect_svg.py <file.svg>

Prints the viewBox, the drawable elements, a coarse bounding box read from path
and shape coordinates, and the pivot translations to use when normalizing the
artwork into <defs>.
"""

import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
SHAPES = ("path", "rect", "circle", "ellipse", "polygon", "polyline", "line", "text", "g")
NUM = re.compile(r"-?\d*\.?\d+(?:e-?\d+)?")


def path_extent(d):
    """Coarse extent from absolute commands. Relative-heavy paths are reported as
    approximate; when precision matters, confirm against the viewBox instead."""
    xs, ys, cx, cy = [], [], 0.0, 0.0
    for cmd, args in re.findall(r"([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)", d):
        n = [float(v) for v in NUM.findall(args)]
        up = cmd.isupper()
        if cmd in "Mm" or cmd in "Ll" or cmd in "Tt":
            for i in range(0, len(n) - 1, 2):
                cx, cy = (n[i], n[i + 1]) if up else (cx + n[i], cy + n[i + 1])
                xs.append(cx); ys.append(cy)
        elif cmd in "Hh":
            for v in n:
                cx = v if up else cx + v
                xs.append(cx); ys.append(cy)
        elif cmd in "Vv":
            for v in n:
                cy = v if up else cy + v
                xs.append(cx); ys.append(cy)
        elif cmd in "CcSsQqAa":
            step = {"C": 6, "S": 4, "Q": 4, "A": 7}[cmd.upper()]
            for i in range(0, len(n) - step + 1, step):
                seg = n[i:i + step]
                cx, cy = (seg[-2], seg[-1]) if up else (cx + seg[-2], cy + seg[-1])
                xs.append(cx); ys.append(cy)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def main(p):
    src = open(p).read()
    root = ET.fromstring(src)
    vb = root.get("viewBox", "(none)")
    print(f"file      {p}")
    print(f"viewBox   {vb}")
    print(f"size attr width={root.get('width')} height={root.get('height')}")

    drawn = {}
    for el in root.iter():
        tag = el.tag.replace(NS, "")
        if tag in SHAPES and tag != "g":
            drawn[tag] = drawn.get(tag, 0) + 1
    total = sum(drawn.values())
    print(f"elements  {drawn or '(none)'}  total={total}")

    box = None
    for el in root.iter(f"{NS}path"):
        e = path_extent(el.get("d", ""))
        if e:
            box = e if box is None else (min(box[0], e[0]), min(box[1], e[1]),
                                         max(box[2], e[2]), max(box[3], e[3]))
    if box:
        x0, y0, x1, y1 = box
        print(f"bbox      x {x0:g}..{x1:g}   y {y0:g}..{y1:g}   "
              f"({x1-x0:g} x {y1-y0:g} units)")
        print(f"pivots    grounded: translate({-(x0+x1)/2:g},{-y1:g})   "
              f"hanging: translate({-(x0+x1)/2:g},{-y0:g})")

    print()
    if total <= 1:
        print("RIG       single shape. Limbs, eyes and mouth cannot move independently.")
        print("          Work at body level: squash, stretch, arcs, rotation, plus")
        print("          shadow, dust and props drawn as separate elements.")
        print("          Offer the user a split into separate paths to unlock articulation.")
    else:
        print(f"RIG       {total} shapes are separately addressable. Check which map to")
        print("          limbs, eyes or props before choosing a motion story.")

    for warn, msg in [("<script", "contains script; strip it, it will not run inside <img>"),
                      ("xlink:href", "uses xlink; prefer plain href"),
                      ("@font-face", "loads a font; web fonts do not resolve inside <img>"),
                      ("http://", "has an external reference"),
                      ("https://", "has an external reference")]:
        if warn in src and warn not in ("http://", "https://") or \
           (warn in ("http://", "https://") and src.count(warn) > 1):
            print(f"WARN      {msg}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
