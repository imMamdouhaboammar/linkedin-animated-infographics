---
name: qa-post
description: Run every quality gate against a built post before it ships, and red-team the caption.
disable-model-invocation: true
argument-hint: "[path/to/artboard.html] [optional: path/to/caption.md]"
---

# /linkedin-motion:qa-post

Arguments: **$ARGUMENTS**

Run the gates in this order and report pass or fail per gate with the specific line or element
that failed. Do not fix anything unless asked; this skill reports.

## Artboard

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py <path> --out /tmp/qa-still.png
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py <path> --mobile
bash ${CLAUDE_PLUGIN_ROOT}/scripts/lint_artboard.sh <path>
```

Then walk `linkedin-motion:render` → `references/qa-gates.md` in full, including the mascot
gates if a character is present.

## Frame 0

Open the first captured frame on its own. It is LinkedIn's poster frame. If it does not read as
a complete infographic without motion, that is a fail regardless of how the loop looks.

## Caption

Load `linkedin-motion:caption` and check:

- line 1 at or under 60 characters
- one archetype, not two blended
- every generic noun replaced by a specific name or number
- exactly one CTA, at the end
- **zero** denial-then-reveal constructions in any language
- zero em dashes, zero buzzwords from the ban list

## Verdict

End with a single line: `SHIP` or `HOLD: <the one thing to fix first>`.
