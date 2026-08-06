#!/usr/bin/env bash
# lint_artboard.sh — cheap grep-level checks that catch the failures which
# otherwise only show up after a five-minute render. No browser, no ffmpeg.
#
#   bash lint_artboard.sh build/post.html
#
# Exit 0 = clean or warnings only. Exit 1 = at least one hard error.
set -u
F="${1:-}"
[ -z "$F" ] && { echo "usage: lint_artboard.sh <artboard.html>"; exit 2; }
[ -f "$F" ] || { echo "not found: $F"; exit 2; }

ERR=0; WARN=0
err()  { printf '  ERROR  %s\n' "$1"; ERR=$((ERR+1)); }
warn() { printf '  warn   %s\n' "$1"; WARN=$((WARN+1)); }
ok()   { printf '  ok     %s\n' "$1"; }

printf '── lint %s ──\n' "$F"

# 1. exactly one #artboard at the right size
N=$(grep -c 'id="artboard"' "$F" || true)
case "$N" in
  1) ok "one #artboard element" ;;
  0) err "no id=\"artboard\" element. capture_frames.py screenshots that element, not the viewport" ;;
  *) err "$N elements with id=\"artboard\". There must be exactly one" ;;
esac
grep -q '1080px' "$F" && grep -q '1350px' "$F" \
  && ok "1080x1350 present" \
  || err "artboard is not 1080px x 1350px"

# 2. unseekable motion
if grep -qE 'requestAnimationFrame|anime\(|createTimeline|from *[\x27"]https://esm\.sh/animejs' "$F"; then
  err "requestAnimationFrame or Anime.js runtime found. capture_frames.py cannot seek it; the render comes back static or blank"
else
  ok "no rAF or Anime.js runtime"
fi

# 3. network fonts
if grep -qE '@import[^;]*fonts\.(googleapis|gstatic)|<link[^>]*fonts\.(googleapis|gstatic)' "$F"; then
  err "webfont loaded over the network. Some frames render in the fallback and the GIF flickers. Use a system stack or base64-embed it"
else
  ok "no network fonts"
fi

# 4. expensive properties
if grep -qE 'animation[^;]*(filter|backdrop-filter)|@keyframes[^}]*filter: *blur' "$F"; then
  warn "an animated filter or backdrop-filter. These rewrite every pixel underneath and defeat rectangle diffing"
fi

# 5. one loop clock
if grep -q -- '--loop' "$F"; then
  BAD=$(grep -oE 'animation-duration: *[0-9.]+m?s' "$F" | grep -v 'var(--loop)' | sort -u | head -5)
  if [ -n "$BAD" ]; then
    warn "hard-coded animation-duration values found; everything should derive from --loop or an integer division of it:"
    printf '           %s\n' $BAD
  else
    ok "all durations derive from --loop"
  fi
else
  grep -q '@keyframes' "$F" && warn "animations present but no --loop custom property defined"
fi

# 6. the nth-of-type trap
grep -q ':nth-of-type' "$F" && warn ":nth-of-type counts siblings by tag, so it silently matches the wrong element when the artboard has mixed children. Use explicit classes"

# 7. attribution footer
grep -qE 'class="foot"|class="footer"' "$F" \
  && ok "attribution footer present" \
  || err "no attribution footer. These images get reposted stripped of the caption and the footer is all that survives"

# 8. em dash in visible copy
grep -q '—' "$F" && warn "em dash found. Use a period and a line break"

# 9. denial-then-reveal
if grep -qiE 'this is not (a|an|just)|not just a|ده مش|مش مجرد|هذا ليس' "$F"; then
  err "denial-then-reveal contrast found. State the thing directly"
fi

printf '── %d error(s), %d warning(s) ──\n' "$ERR" "$WARN"
[ "$ERR" -gt 0 ] && exit 1
exit 0
