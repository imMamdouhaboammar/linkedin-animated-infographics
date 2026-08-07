#!/usr/bin/env python3
import argparse
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.info_stories import load_catalog  # noqa: E402


def render(catalog):
    cards = []
    for house in catalog["houses"]:
        t = house["tokens"]
        swatches = "".join(
            f'<div class="swatch"><span style="background:{html.escape(value)}"></span><b>{html.escape(name)}</b><code>{html.escape(value)}</code></div>'
            for name, value in t.items()
        )
        cards.append(
            f'<article style="--bg:{t["bg"]};--surface:{t["surface"]};--ink:{t["ink"]};--line:{t["line"]};--accent:{t["accent"]};--accent-deep:{t["accent_deep"]}">'
            f'<header><div><h2>{html.escape(house["name"])}</h2><p>{html.escape(house["tone"])}</p></div><span>{html.escape(house["slug"])}</span></header>'
            f'<div class="sample"><strong>Headline with <em>accent</em></strong><small>Body text stays readable on the selected paper.</small></div>'
            f'<div class="swatches">{swatches}</div></article>'
        )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Info-stories Story Houses</title><style>
*{{box-sizing:border-box}} body{{margin:0;padding:40px;background:#eef1f4;color:#1e2933;font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1180px;margin:auto}} h1{{font-size:38px;margin:0 0 8px}} .intro{{margin:0 0 28px;color:#53606d}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}} article{{background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:18px;padding:22px}}
header{{display:flex;justify-content:space-between;gap:16px;align-items:start}} h2{{margin:0;font-size:26px}} p{{margin:4px 0 0}} header span{{font:600 12px ui-monospace,monospace;border:1px solid var(--line);padding:5px 8px;border-radius:999px}}
.sample{{background:var(--surface);border:1px solid var(--line);padding:18px;border-radius:12px;margin:18px 0;display:grid;gap:6px}} .sample strong{{font-size:21px}} .sample em{{font-style:normal;color:var(--accent-deep)}}
.swatches{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}} .swatch{{display:grid;gap:4px;min-width:0}} .swatch span{{height:36px;border:1px solid rgba(0,0,0,.12);border-radius:8px}} .swatch b{{font-size:11px}} code{{font-size:10px;overflow:hidden}}
@media(max-width:800px){{.grid{{grid-template-columns:1fr}}.swatches{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body><main><h1>Info-stories Story Houses</h1><p class="intro">Choose the palette family first, then use semantic tokens rather than freehand colours.</p><section class="grid">{''.join(cards)}</section></main></body></html>'''


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render all Info-stories Story Houses as a standalone HTML preview")
    parser.add_argument("--out", type=Path, default=ROOT / "build" / "info-stories-palettes.html")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args(argv)
    output = render(load_catalog())
    if args.stdout:
        print(output)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output)
        print(args.out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
