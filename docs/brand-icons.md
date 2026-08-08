# Brand icons

Official AI and LLM marks, fetched from a pinned upstream set instead of drawn from memory.

## Why this exists

The repository already had a rule for named and official marks: the exact SVG is mandatory, and a lookalike is never acceptable. What it did not have was a way to *get* one. The only available answer was `HOLD: exact SVG required`, which stops a build even when the vendor's own artwork is a fetch away.

Tracing a logo from memory produces a mark that is subtly wrong in a way most reviewers will not catch and the brand owner will. This tool removes the temptation by making the correct asset the easy one.

## Source

| | |
|---|---|
| Package | `@lobehub/icons-static-svg` |
| Version | pinned in `assets/brand-icons/manifest.json` |
| Upstream | https://github.com/lobehub/lobe-icons |
| Gallery | https://lobehub.com/icons |
| Licence | MIT |

**The MIT licence covers the packaging of the set. It does not carry any right in the marks themselves.** Every logo remains the trademark of its owner. Use one nominatively, to identify that product where it genuinely appears in the story, and nothing else. Do not use a mark as decoration, do not imply endorsement, do not recolour or restyle it, and do not place it so the reader would infer a partnership or an integration that does not exist.

## Scope, and where it ends

This is an **AI and LLM** set. It covers OpenAI, Claude, Gemini, Perplexity, Mistral, Google, Meta and several hundred more.

It does **not** cover general social, advertising or analytics platforms. TikTok, LinkedIn, Reddit, YouTube, Google Analytics and Looker Studio are not in it.

Asking for one of those is not an error to route around. The tool reports the gap and stops:

```console
$ python3 tools/brand_icon.py fetch tiktok
'tiktok' is not in @lobehub/icons-static-svg@1.94.0. This set covers AI and LLM
brands... Supply the exact SVG yourself, or keep the literal product name.
```

That is the same doctrine as the mascot gate. A missing mark is a HOLD, never a substitution.

### The mixed-set trap

If a zone names six platforms and this set only carries two of them, do not give those two real logos and leave the other four as text. A half-branded row reads as a mistake rather than a decision. Either every member of a zone gets its real mark, or the whole zone uses literal product names. Record which rule you applied.

## Use

```bash
# what exists
python3 tools/brand_icon.py list --query claude

# fetch one, sanitise it, record where it came from
python3 tools/brand_icon.py fetch claude --variant color
python3 tools/brand_icon.py fetch openai            # falls back to the mono mark

# verify nothing in the cache drifted
python3 tools/brand_icon.py check
```

Variants are `color`, `mono`, `text` and `brand`. A colour request falls back to the vendor's monochrome mark when that is the only one shipped, which is still that vendor's own artwork rather than a substitution.

Marks land in `assets/brand-icons/` and every one gets a row in `assets/brand-icons/provenance.json` carrying the resolved name, source URL, pinned version, licence, trademark note, SHA-256 and fetch date.

## What the sanitiser rejects

A fetched mark is remote input. It is parsed and inspected before it is ever written, and rejected outright if it contains:

- a `<script>`, `<foreignObject>`, `<iframe>`, `<audio>` or `<video>` element
- any `on*` event handler attribute
- an `href` or `src` pointing at `http:`, `https:`, `//`, `javascript:` or `data:text/html`
- a `style` attribute pulling an external `url()`
- a `<!DOCTYPE>` or `<!ENTITY>` declaration, which is the XXE vector
- more than 256 KB, or anything that does not parse as XML with an `<svg>` root

`check` re-runs the same inspection over the cache and compares each file against its recorded hash, so a mark that is edited after the fact fails rather than shipping quietly.

## Using a mark on an artboard

Inline the SVG into the artboard rather than linking it. A fixed 1080x1350 artboard is captured by headless Chrome, and an external reference is a network dependency in the middle of a deterministic render.

Keep the vendor's own geometry and colours. If the mark needs to sit on a coloured surface, change the surface, not the mark.

Every logo on an artboard still inherits `evidence-traceability`: it must identify a real source or destination in the story. A logo wall with no story job fails the gate regardless of how official the artwork is.
