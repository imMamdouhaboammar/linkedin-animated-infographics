---
name: qa-post
description: Run every quality gate against a built post before it ships, red-team the post, and independently verify acceptance evidence.
disable-model-invocation: true
argument-hint: "[path/to/artboard.html] [optional: path/to/caption.md]"
---

# /linkedin-animated-infographics:qa-post

Arguments: **$ARGUMENTS**

This workflow reports evidence. It does not silently edit the artifact.

## 1. Deterministic render gates

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py <path> --out /tmp/qa-still.png
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_render.py <path> --mobile
bash ${CLAUDE_PLUGIN_ROOT}/scripts/lint_artboard.sh <path>
```

Walk `linkedin-animated-infographics:render` and `references/qa-gates.md` in full. Open frame 0 and the 350px preview. For GIFs, include seam, motion, duration, and file-size evidence.

## 2. Caption checks

Use `linkedin-animated-infographics:caption` when a caption is supplied. Check the truncation cut, one archetype, factual support, exactly one CTA, anti-slop rules, and banned constructions.

## 3. Adversarial review

Delegate to `post-critic` with the artifact, caption, render evidence, story brief if present, and evidence record if present. Report must-fix, improvement, and leave-alone findings. Any must-fix item produces `HOLD` until resolved or explicitly shown not applicable.

## 4. Independent verification

When an Info-stories brief or acceptance criteria exist, delegate to `story-verifier` with direct artifact paths, render evidence, post-critic findings, and criteria. Do not substitute a worker summary for artifact evidence. Respect the maximum-two-fix-attempt rule.

## Verdict

End with one line: `SHIP` or `HOLD: <the one thing to fix first>`.
