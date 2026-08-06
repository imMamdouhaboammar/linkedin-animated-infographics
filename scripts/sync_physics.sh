#!/usr/bin/env bash
# sync_physics.sh — refresh the vendored copy of physics.py from the
# svg-mascot-animator plugin and report whether it had drifted.
#
# physics.py is vendored rather than imported across plugins because Claude Code
# copies each plugin to its own cache directory on install, so a relative path
# out of this plugin would not resolve at runtime.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="${1:-$HERE/../../svg-mascot-animator/skills/svg-mascot-animator/scripts/physics.py}"
[ -f "$SRC" ] || { echo "source not found: $SRC"; echo "pass the path as an argument"; exit 2; }
if cmp -s "$SRC" "$HERE/physics.py"; then
  echo "physics.py is in sync with $SRC"
else
  cp "$SRC" "$HERE/physics.py"
  echo "physics.py updated from $SRC"
  echo "Re-run any baked keyframes: the equations changed."
fi
