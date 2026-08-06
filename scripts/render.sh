#!/usr/bin/env bash
# render.sh — one command from HTML artboard to LinkedIn-ready GIF.
#
#   bash scripts/render.sh build/post.html build/post.gif --duration 4.8 --fps 12.5
#
# Extra flags are passed through: --max-mb, --colors, --selector, --scale, --browser
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

while [[ $# -gt 0 ]]; do
  case "$1" in
    --duration) DURATION="$2"; shift 2 ;;
    --fps)      FPS="$2";      shift 2 ;;
    --max-mb)   MAXMB="$2";    shift 2 ;;
    --colors)   COLORS="$2";   shift 2 ;;
    --selector) SELECTOR="$2"; shift 2 ;;
    --scale)    SCALE="$2";    shift 2 ;;
    --browser)  BROWSER="$2";  shift 2 ;;
    *) echo "unknown flag: $1" >&2; exit 1 ;;
  esac
done

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMES="$(dirname "$OUT")/.frames"

BROWSER_ARG=()
[[ -n "$BROWSER" ]] && BROWSER_ARG=(--browser "$BROWSER")

echo "── capture ──────────────────────────────────"
python3 "$HERE/capture_frames.py" "$HTML" \
  --out "$FRAMES" --duration "$DURATION" --fps "$FPS" \
  --selector "$SELECTOR" --scale "$SCALE" "${BROWSER_ARG[@]}"

echo
echo "── assemble ─────────────────────────────────"
python3 "$HERE/build_gif.py" "$FRAMES" \
  --out "$OUT" --fps "$FPS" --max-mb "$MAXMB" --colors "$COLORS"
