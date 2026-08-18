#!/usr/bin/env python3
"""Fail when rendered text is clipped or overflows a bounded container."""

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

  board.querySelectorAll('*').forEach(el => {
    if (!visible(el)) return;
    const text = [...el.childNodes]
      .filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    if (!text) return;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;

    const horizontal = el.scrollWidth > el.clientWidth + 1;
    const vertical = el.scrollHeight > el.clientHeight + 1;
    const clipsX = ['hidden', 'clip'].includes(cs.overflowX);
    const clipsY = ['hidden', 'clip'].includes(cs.overflowY);
    const outsideBoard = r.left < br.left - 1 || r.right > br.right + 1 ||
                         r.top < br.top - 1 || r.bottom > br.bottom + 1;

    if ((horizontal && clipsX) || (vertical && clipsY) || outsideBoard) {
      violations.push({
        element: label(el),
        sample: text.slice(0, 70),
        horizontal, vertical, outsideBoard,
        client: [el.clientWidth, el.clientHeight],
        scroll: [el.scrollWidth, el.scrollHeight],
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
        print(f"        {row['element']} {row['sample']!r}")
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
