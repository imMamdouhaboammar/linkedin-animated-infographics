#!/usr/bin/env bash
# setup.sh — install everything the render pipeline needs.
# Safe to re-run. Prints a final readiness report.
set -uo pipefail

if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
  echo "Python 3.11 or newer is required (resolved: $(python3 --version 2>&1))." >&2
  exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)"
RUNTIME_REQUIREMENTS="$REPO_ROOT/requirements-runtime.txt"

if [[ ! -f "$RUNTIME_REQUIREMENTS" ]]; then
  echo "Missing runtime dependency lock: $RUNTIME_REQUIREMENTS" >&2
  exit 1
fi

echo "── python deps ──────────────────────────────"
python3 -m pip install --quiet --break-system-packages -r "$RUNTIME_REQUIREMENTS" 2>/dev/null \
  || python3 -m pip install --quiet -r "$RUNTIME_REQUIREMENTS"

echo "── browser ──────────────────────────────────"
BROWSER=""
for c in /usr/bin/google-chrome /usr/bin/google-chrome-stable /usr/bin/chromium \
         "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; do
  [[ -x "$c" ]] && BROWSER="$c" && break
done

if [[ -z "$BROWSER" ]]; then
  echo "  no Chrome found, trying Playwright's bundled Chromium..."
  python3 -m playwright install chromium 2>/dev/null

  if [[ ! -d "$HOME/.cache/ms-playwright" && "$(uname)" == "Linux" ]]; then
    echo "  Playwright CDN unavailable. Installing Google Chrome from dl.google.com..."
    TMP="$(mktemp -d)"
    curl -sSL -o "$TMP/chrome.deb" \
      https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
      && (sudo apt-get install -y "$TMP/chrome.deb" 2>/dev/null \
          || apt-get install -y "$TMP/chrome.deb")
    rm -rf "$TMP"
    BROWSER="$(command -v google-chrome || true)"
  fi
fi

echo "── ffmpeg ───────────────────────────────────"
if ! command -v ffmpeg >/dev/null; then
  echo "  installing ffmpeg..."
  (sudo apt-get install -y ffmpeg 2>/dev/null \
    || apt-get install -y ffmpeg 2>/dev/null \
    || brew install ffmpeg 2>/dev/null) >/dev/null
fi

echo
echo "── readiness ────────────────────────────────"
python3 -c "import playwright" 2>/dev/null \
  && echo "  playwright   ok" || echo "  playwright   MISSING"
python3 -c "import PIL" 2>/dev/null \
  && echo "  pillow       ok" || echo "  pillow       MISSING"
command -v ffmpeg >/dev/null \
  && echo "  ffmpeg       ok ($(ffmpeg -version | head -1 | cut -d' ' -f3))" \
  || echo "  ffmpeg       MISSING"

FOUND=""
for c in /usr/bin/google-chrome /usr/bin/google-chrome-stable /usr/bin/chromium \
         "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; do
  [[ -x "$c" ]] && FOUND="$c" && break
done
if [[ -n "$FOUND" ]]; then
  echo "  browser      ok ($FOUND)"
elif [[ -d "$HOME/.cache/ms-playwright" ]]; then
  echo "  browser      ok (Playwright bundled Chromium)"
else
  echo "  browser      MISSING — install Google Chrome and pass --browser <path>"
fi
