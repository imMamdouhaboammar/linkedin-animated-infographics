# Community Demos

Community publishing is an optional public-export workflow for finished work. It is not part of normal delivery and it never writes to GitHub without explicit user consent.

## Package contract

A demo directory contains exactly:

```text
demo.gif
index.html
demo.json
```

Community path:

```text
demos/community/<github-user>/<slug>/
```

Owned maintainer demos use `demos/owned/<slug>/` and follow the same validation rules.

The root `demos/catalog.json` is generated deterministically from all accepted `demo.json` files.

## `demo.json`

Every manifest validates against `schemas/demo.schema.json`.

Required public fields include identity, title, author attribution, description, plugin version, language, story type, tags, fixed local GIF/HTML paths, creation date, license, and `rights_confirmed: true`.

`source_prompt` is optional. It is private by default and is included only after separate explicit consent to publish the prompt itself.

Paths inside the manifest may not escape the demo directory. Community author names must match the GitHub namespace in the directory path.

## When the plugin may offer publishing

`new-post` may offer community sharing only after delivery and independent verification `PASS`.

If the user declines or gives no answer, there is no GitHub write.

If the user explicitly accepts, the focused `share-demo` parent workflow collects public metadata and rights confirmation, selects the verified final GIF and HTML, and runs the export preflight.

## Export boundary

The publisher is a data-export boundary and fails closed.

Automatic packaging rejects common credential markers, bearer credentials, local absolute paths, signed URLs, and remote executable script resources that require maintainer inspection. It copies only the approved final HTML and GIF. It never recursively publishes `build/`.

Do not publish evidence files, build reports, source documents, private attachments, local paths, signed/private URLs, secrets, or assets the contributor cannot redistribute.

The workflow never infers rights. `rights_confirmed` is an explicit assertion from the user.

## Prepare and validate

Typical preparation:

```bash
python3 scripts/demo_submit.py prepare \
  --build-dir build \
  --stage-root build/community-submission \
  --author <github-user> \
  --slug <slug> \
  --metadata build/community-demo.json
```

Validate the staged package:

```bash
python3 scripts/demo_submit.py check build/community-submission/community/<github-user>/<slug>
```

After placing the package in a contribution checkout:

```bash
python3 scripts/demo_gallery.py build
python3 scripts/demo_gallery.py check
```

`demo_gallery.py check` validates package shape, metadata, safe paths, namespace attribution, duplicate IDs, and catalog drift.

## GitHub publication

`community-publisher` is the narrow contribution worker. It may create or reuse the authenticated contributor's fork, create a fresh `community/<user>/<slug>` branch, add the three demo files, regenerate the root catalog, commit, push, and open a pull request against upstream `main`.

The worker must **Never merge** the pull request. It must never enable auto-merge, push directly to upstream `main`, force-push unrelated history, or claim success without a real PR URL.

Every submission remains open for maintainer manual review and merge.

## HOLD states

Publishing returns HOLD when final verification is not PASS, rights confirmation is missing, GIF/HTML artifacts are missing or ambiguous, export scanning finds unsafe material, GitHub identity or write access is unavailable, the upstream target cannot be verified, the contribution path already exists, catalog validation fails, or pull-request creation does not return a URL.

A publication HOLD does not invalidate the already delivered infographic.
