#!/usr/bin/env bash
# render.sh — one command from HTML artboard to LinkedIn-ready GIF.
#
#   bash scripts/render.sh build/post.html build/post.gif --duration 4.8 --fps 12.5
#
# Supported flags: --max-mb, --colors, --selector, --scale, --browser, --mobile
set -euo pipefail

HTML="${1:?usage: render.sh <artboard.html> <out.gif> [--duration S] [--fps N] ...}"
OUT="${2:?usage: render.sh <artboard.html> <out.gif> [--duration S] [--fps N] ...}"
shift 2

DURATION=4.8
FPS=12.5
MAXMB=5
COLORS=128
SELECTOR="#artboard"
SCALE=1
BROWSER=""
MOBILE_ARG=(--mobile)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --duration) DURATION="$2"; shift 2 ;;
    --fps)      FPS="$2";      shift 2 ;;
    --max-mb)   MAXMB="$2";    shift 2 ;;
    --colors)   COLORS="$2";   shift 2 ;;
    --selector) SELECTOR="$2"; shift 2 ;;
    --scale)    SCALE="$2";    shift 2 ;;
    --browser)  BROWSER="$2";  shift 2 ;;
    --mobile)   MOBILE_ARG=(--mobile); shift ;;
    --no-mobile) MOBILE_ARG=(--no-mobile); shift ;;
    *) echo "unknown flag: $1" >&2; exit 1 ;;
  esac
done

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$(dirname "$OUT")"
EVIDENCE="$OUT_DIR/.render-evidence"
FRAMES="$EVIDENCE/frames"
STILL="$OUT_DIR/still.png"
REPORT="$OUT_DIR/render-report.json"
ARTBOARD_JSON="$EVIDENCE/artboard.json"
STILL_JSON="$EVIDENCE/still.json"
GIF_JSON="$EVIDENCE/gif.json"
mkdir -p "$EVIDENCE"

echo "── lint ─────────────────────────────────────"
bash "$HERE/lint_artboard.sh" "$HTML"

echo
echo "── artboard audit ───────────────────────────"
set +e
ARTBOARD_CMD=(python3 "$HERE/artboard_audit.py" "$HTML" --json "$ARTBOARD_JSON")
[[ -n "$BROWSER" ]] && ARTBOARD_CMD+=(--browser "$BROWSER")
"${ARTBOARD_CMD[@]}"
ARTBOARD_STATUS=$?
set -e
[[ "$ARTBOARD_STATUS" -le 1 ]] || exit "$ARTBOARD_STATUS"

echo
echo "── still ────────────────────────────────────"
set +e
STILL_CMD=(python3 "$HERE/check_render.py" "$HTML" --out "$STILL" \
  --json "$STILL_JSON" --selector "$SELECTOR" "${MOBILE_ARG[@]}")
[[ -n "$BROWSER" ]] && STILL_CMD+=(--browser "$BROWSER")
"${STILL_CMD[@]}"
STILL_STATUS=$?
set -e
[[ "$STILL_STATUS" -le 1 ]] || exit "$STILL_STATUS"

echo
echo "── capture ──────────────────────────────────"
CAPTURE_CMD=(python3 "$HERE/capture_frames.py" "$HTML" \
  --out "$FRAMES" --duration "$DURATION" --fps "$FPS" \
  --selector "$SELECTOR" --scale "$SCALE")
[[ -n "$BROWSER" ]] && CAPTURE_CMD+=(--browser "$BROWSER")
"${CAPTURE_CMD[@]}"

echo
echo "── assemble ─────────────────────────────────"
set +e
python3 "$HERE/build_gif.py" "$FRAMES" \
  --out "$OUT" --fps "$FPS" --max-mb "$MAXMB" --colors "$COLORS" \
  --json "$GIF_JSON"
GIF_STATUS=$?
set -e
[[ "$GIF_STATUS" -le 1 ]] || exit "$GIF_STATUS"

echo
echo "── merge evidence ───────────────────────────"
python3 "$HERE/render_report.py" merge \
  --artboard "$ARTBOARD_JSON" --still "$STILL_JSON" --gif "$GIF_JSON" \
  --input "$HTML" --output "$OUT" --out "$REPORT"
