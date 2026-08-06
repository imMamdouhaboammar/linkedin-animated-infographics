#!/usr/bin/env bash
# setup.sh — install everything the render pipeline needs.
# Safe to re-run. Prints a final readiness report.
set -uo pipefail

echo "── python deps ──────────────────────────────"
pip install --quiet --break-system-packages playwright pillow 2>/dev/null \
  || pip install --quiet playwright pillow

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
