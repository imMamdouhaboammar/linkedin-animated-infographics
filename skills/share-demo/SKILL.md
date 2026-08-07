---
name: share-demo
description: Package a verified infographic demo for the public gallery and, after explicit user opt-in, prepare a community pull request without merging it.
disable-model-invocation: true
argument-hint: "[build directory] [optional metadata]"
---

# /linkedin-animated-infographics:share-demo

## Purpose

Run the focused parent workflow for publishing a finished infographic to the repository community gallery. This is a public data-export boundary, not part of normal delivery. Read `helper/GUIDE.md` before execution and keep all GitHub writes behind explicit opt-in.

The public demo contract is exactly `demo.gif + index.html + demo.json`. `demos/catalog.json` is generated separately and is never a fourth file inside a demo directory.

## Use when

Use this focused workflow only when a user explicitly agrees to share a finished demo with the community, or directly asks to publish a previously verified result. The normal `new-post` parent workflow may offer this after delivery only when final verification PASS has already been recorded.

Do not invoke this workflow merely because a GIF was generated. Declining the offer, giving no consent, or asking only for local output causes no GitHub write.

## Inputs

Required inputs:

- explicit opt-in to public community sharing
- `build/post.html` or another explicitly selected final verified HTML artifact
- `build/post.gif` or another explicitly selected final verified GIF artifact
- `build/verification-report.json` with final verdict `PASS`
- GitHub username and matching public author URL
- demo title and short description
- language, story type, and tags
- explicit rights confirmation covering the submitted HTML, GIF, and redistributable assets
- chosen public license

Optional inputs:

- source prompt, only when the user separately consents to publishing it
- source repository URL
- short public notes

## Outputs

The parent workflow produces:

- `build/community-demo.json` containing the approved public metadata
- `build/community-demo-package` containing the staged three-file package
- on successful GitHub publication, a pull request URL against `imMamdouhaboammar/linkedin-animated-infographics:main`
- on unavailable GitHub write access, a precise HOLD plus the validated local contribution package and manual commands when the host can prepare them safely

A PR URL is required before reporting GitHub publication as successful. Creating files locally is not equivalent to opening a pull request.

## Procedure

1. Confirm **explicit opt-in**. Ask one direct question if consent is not already explicit. Do not infer consent from enthusiasm, prior GitHub use, or the fact that the user created the work.
2. Read `build/verification-report.json`. Community publication requires **verification PASS**. Any other verdict returns a HOLD.
3. Resolve the exact final HTML and GIF. Do not publish drafts, stills, evidence files, build reports, attachments, or unrelated files.
4. Collect publication metadata: title, author, author URL, description, language, story type, tags, date, plugin version, and license.
5. Obtain explicit **rights confirmation**. Do not infer ownership or redistribution rights.
6. Treat the **source prompt** as private by default. Include it only after a separate explicit yes to publishing the prompt itself.
7. Write the approved metadata input used by the deterministic preflight. Keep control fields such as prompt-consent flags outside the final public schema.
8. Prepare the contribution package with `scripts/demo_submit.py prepare`, for example:

```bash
python3 scripts/demo_submit.py prepare \
  --build-dir build \
  --stage-root build/community-submission \
  --author <github-user> \
  --slug <slug> \
  --metadata build/community-demo.json
```

9. Validate the staged package with `scripts/demo_submit.py check`:

```bash
python3 scripts/demo_submit.py check build/community-submission/community/<github-user>/<slug>
```

10. Run the gallery validator against the contribution checkout before GitHub publication. The required gate is `scripts/demo_gallery.py check`; regenerate `demos/catalog.json` deterministically with `scripts/demo_gallery.py build` only after the three-file package is placed in the contribution checkout.
11. Confirm the contribution changes only `demos/community/<github-user>/<slug>/{demo.gif,index.html,demo.json}` plus the root generated `demos/catalog.json` when its content changes.
12. Delegate the validated contribution to `community-publisher`. That worker owns fork, branch, commit, push, and pull-request mechanics. It returns control to this parent workflow and never merges.
13. Return the PR URL, demo ID/path, validation summary, and the explicit reminder that maintainer manual review and merge are still required.

## HOLD conditions

Return HOLD instead of guessing or partially publishing when any of these is unresolved:

- explicit opt-in is missing
- final verification PASS is missing
- final GIF or HTML is missing, empty, or ambiguous
- rights confirmation is missing or false
- public metadata is incomplete
- secret, local-path, signed-URL, or unsafe remote-script findings appear in export preflight
- the destination demo already exists
- GitHub username cannot be resolved safely
- GitHub authentication cannot create/reuse a fork, push a fresh branch, or open a pull request
- the target upstream repository cannot be verified exactly
- deterministic catalog validation fails

A HOLD must state the blocking requirement. Never weaken export checks, publish extra files, or claim success without a returned PR URL.

## Related components

- routing authority: `helper/GUIDE.md`
- route registry: `helper/router.json`
- demo schema: `schemas/demo.schema.json`
- package preflight: `scripts/demo_submit.py`
- gallery validator: `scripts/demo_gallery.py`
- gallery index: `demos/catalog.json`
- publisher worker: `agents/community-publisher.md`
- final creation parent workflow: `skills/new-post/SKILL.md`
- artifact registry: `helper/artifacts.json`

## Research gates

`bounded-verification` remains the relevant research gate because a demo cannot cross this export boundary until the independent final verdict is PASS. Existing evidence and creative gates govern the artifact before publication; this workflow does not create new claims, redesign the post, or reinterpret evidence.
