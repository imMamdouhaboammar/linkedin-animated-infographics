#!/usr/bin/env python3
"""Fail when rendered text is clipped or escapes the artboard."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.render_probe import open_artboard

PROBE_JS = r"""
() => {
  const board = document.querySelector('#artboard');
  if (!board) return {error: 'no #artboard element', violations: []};
  const br = board.getBoundingClientRect();
  const violations = [];
  const visible = el => {
    const cs = getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden' &&
           parseFloat(cs.opacity || '1') > 0.01;
  };
  const label = el => `<${el.tagName.toLowerCase()} class="${
    (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className || '')
      .toString().slice(0, 50)}">`;
  const clips = (el, axis) => {
    const cs = getComputedStyle(el);
    const value = axis === 'x' ? cs.overflowX : cs.overflowY;
    return value === 'hidden' || value === 'clip';
  };
  const outside = (inner, outer, axis) => axis === 'x'
    ? inner.left < outer.left - 1 || inner.right > outer.right + 1
    : inner.top < outer.top - 1 || inner.bottom > outer.bottom + 1;

  board.querySelectorAll('*').forEach(el => {
    if (!visible(el)) return;
    const textNodes = [...el.childNodes]
      .filter(n => n.nodeType === 3 && n.textContent.trim().length > 0);
    if (!textNodes.length) return;

    const range = document.createRange();
    range.setStartBefore(textNodes[0]);
    range.setEndAfter(textNodes[textNodes.length - 1]);
    const tr = range.getBoundingClientRect();
    if (!tr.width || !tr.height) return;

    const reasons = [];
    if (outside(tr, br, 'x') || outside(tr, br, 'y')) reasons.push('outside-artboard');

    for (let ancestor = el; ancestor && ancestor !== board.parentElement;
         ancestor = ancestor.parentElement) {
      if (!visible(ancestor)) continue;
      const ar = ancestor.getBoundingClientRect();
      if (clips(ancestor, 'x') && outside(tr, ar, 'x')) {
        reasons.push(`clipped-x:${label(ancestor)}`);
      }
      if (clips(ancestor, 'y') && outside(tr, ar, 'y')) {
        reasons.push(`clipped-y:${label(ancestor)}`);
      }
      if (ancestor === board) break;
    }

    if (reasons.length) {
      const text = textNodes.map(n => n.textContent).join('').trim();
      violations.push({
        element: label(el),
        sample: text.slice(0, 70),
        reasons: [...new Set(reasons)],
        text_rect: {
          left: Math.round((tr.left - br.left) * 10) / 10,
          top: Math.round((tr.top - br.top) * 10) / 10,
          right: Math.round((tr.right - br.left) * 10) / 10,
          bottom: Math.round((tr.bottom - br.top) * 10) / 10,
        },
      });
    }
  });
  return {error: null, violations};
}
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html')
    ap.add_argument('--json', dest='json_out', default=None)
    ap.add_argument('--browser', default=None)
    ap.add_argument('--at', type=float, default=0.0)
    args = ap.parse_args(argv)

    with open_artboard(args.html, width=1080, height=1350, at=args.at,
                       browser=args.browser) as (page, capture):
        result = page.evaluate(PROBE_JS)

    if result.get('error'):
        print(result['error'], file=sys.stderr)
        return 2

    violations = result['violations']
    report = {
        'schema_version': 1,
        'stage': 'text-overflow',
        'artifact': str(Path(args.html).resolve()),
        'capture': capture,
        'verdict': 'FAIL' if violations else 'PASS',
        'violations': violations,
    }
    if args.json_out:
        target = Path(args.json_out)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')

    print('── text overflow audit ──────────────────────')
    if not violations:
        print('  ok    no clipped or overflowing text detected')
        return 0
    print(f'  FAIL  {len(violations)} text node(s) clipped or outside the artboard')
    for row in violations[:8]:
        print(f"        {row['element']} {row['sample']!r}: {', '.join(row['reasons'])}")
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
