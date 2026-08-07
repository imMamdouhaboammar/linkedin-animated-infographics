# Demos

The gallery has two namespaces and one package contract.

Every entry is **GIF + HTML + demo.json**. No extra files live inside a demo directory.

`demos/catalog.json` is generated from the manifests. Do not edit it by hand.

## Created by Mamdouh

Maintainer demos live at:

```text
demos/owned/<slug>/
  demo.gif
  index.html
  demo.json
```

Owned demos use the same schema, export checks, and gallery validation as community work. There is no maintainer bypass.

The existing README hero animation remains at `assets/demo_artboard_v4.gif`. It is not copied into `demos/owned/` until its matching final HTML is available and the complete three-file package passes the gallery validator.

## Created by the community

Community demos live at:

```text
demos/community/<github-user>/<slug>/
  demo.gif
  index.html
  demo.json
```

The GitHub username in the path must match `demo.json.author`. Each demo keeps its own attribution, story type, language, tags, plugin version, license, and explicit rights confirmation.

Browse the machine-readable index in [`catalog.json`](catalog.json).

## Share a demo from the plugin

After a finished infographic passes independent verification, the plugin can ask:

`Share this demo with the community?`

Nothing is published until the user explicitly says yes.

If accepted, `share-demo` checks the final GIF and HTML, collects public metadata and rights confirmation, prepares the three-file package, validates it, and delegates GitHub contribution mechanics to `community-publisher`.

The publisher prepares a contributor fork, fresh branch, commit, push, and pull request. It stops at the PR. Every submission requires maintainer **manual review** and merge.

## Contribute manually

Create a package under your GitHub namespace, regenerate the catalog, then run:

```bash
python3 scripts/demo_submit.py check demos/community/<github-user>/<slug>
python3 scripts/demo_gallery.py build
python3 scripts/demo_gallery.py check
```

Commit the three demo files plus the regenerated root `demos/catalog.json`, then open a pull request against `main`.

Do not include prompts unless you intend to publish them. Do not include credentials, local paths, private URLs, evidence files, build reports, source documents, or assets you cannot redistribute.

The complete contribution and privacy contract is in [`../docs/community-demos.md`](../docs/community-demos.md).
