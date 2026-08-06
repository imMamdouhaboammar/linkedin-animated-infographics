#!/usr/bin/env python3
"""
bake_mascot.py — seek-safe mascot motion for animated infographics.

The problem this solves. svg-mascot-animator designs mascot motion for README
assets and runtime pages: one mascot, its own canvas, its own clock. Dropping that
output into a 1080x1350 artboard breaks two things at once. The mascot's duration
is almost never an integer division of the artboard's --loop, so the composite
cycle becomes the least common multiple and the GIF stops closing. And Anime.js
runtime motion is driven by requestAnimationFrame, which capture_frames.py cannot
seek, so the frames come back wrong or blank.

This script bakes the same physics into CSS keyframes expressed as percentages of
the artboard loop, so a mascot inherits the artboard's clock instead of bringing
its own. Timing comes from svg-mascot-animator/scripts/physics.py — the equations
are not reimplemented here.

Three roles, matching references/mascots.md:

  idle    ambient breathing and blinking. Unlimited count, amplitude capped.
  hop     the pointer mascot. One per artboard. Travels a route and lands on each
          stop, which is what the sequential highlight then reacts to.
  payoff  the reaction mascot. One per artboard. Fires once, at the moment the
          pointer arrives.

Usage:
    python3 bake_mascot.py idle   --loop 6000 --id hero --n 2 --amp 3
    python3 bake_mascot.py hop    --loop 6000 --id ptr --stops 5 --apex 46 --dwell .10
    python3 bake_mascot.py payoff --loop 6000 --id win --at .78 --rise 20
    python3 bake_mascot.py budget --w 1080 --h 1350 --mascot 64 --travel 1
"""

import argparse
import math
import sys
from pathlib import Path

# physics.py lives in the sibling skill. Import it rather than copying equations.
# physics.py is vendored into this plugin's scripts/ directory. Plugins are copied
# to a cache location on install, so a cross-plugin relative path would not resolve.
# The other candidates cover running this script straight out of a checkout.
PHYS_CANDIDATES = [
    Path(__file__).resolve().parent,
    Path("/mnt/skills/user/svg-mascot-animator/scripts"),
    Path.home() / ".claude/skills/svg-mascot-animator/scripts",
    Path(__file__).resolve().parent.parent.parent / "svg-mascot-animator/skills/svg-mascot-animator/scripts",
]
for c in PHYS_CANDIDATES:
    if (c / "physics.py").exists():
        sys.path.insert(0, str(c))
        break
else:
    sys.exit(
        "physics.py not found. This script depends on the svg-mascot-animator skill.\n"
        "Looked in:\n  " + "\n  ".join(str(c) for c in PHYS_CANDIDATES)
    )

import physics as P  # noqa: E402


# --------------------------------------------------------------------------
# loop hygiene
# --------------------------------------------------------------------------
LEGAL_DIVISORS = (1, 2, 3, 4, 5, 6, 8, 10, 12)


def check_division(loop_ms, n):
    """A sub-loop must repeat a whole number of times inside the artboard loop.

    Anything else produces a composite cycle equal to the least common multiple,
    which will not close at the capture length. This is the same constraint as
    Primitive 9 in references/animation-recipes.md and it is the single most
    common way a mascot breaks an otherwise clean render.
    """
    if n not in LEGAL_DIVISORS:
        sys.exit(
            f"--n {n} is not a legal divisor. Use one of {LEGAL_DIVISORS}.\n"
            f"At --loop {loop_ms}ms, n={n} gives {loop_ms/n:.2f}ms, which does not close."
        )
    return loop_ms / n / 1000.0


def banner(txt):
    return f"/* {txt} */"


# --------------------------------------------------------------------------
# role: idle
# --------------------------------------------------------------------------
def bake_idle(loop_ms, ident, n, amp, blink):
    """Ambient life. A sine breathe on y plus an optional blink.

    Amplitude is capped deliberately. An idle mascot competes with the reading
    pointer the moment it moves more than a few pixels, and the whole design
    depends on exactly one thing being the loudest moving object.
    """
    if amp > 4:
        sys.exit(f"--amp {amp} exceeds the idle cap of 4px. See references/mascots.md.")

    dur = check_division(loop_ms, n)
    loop_s = loop_ms / 1000.0

    breathe = P.harmonic(0, dur, amp, cycles=1, n=12)
    out = [banner(f"idle '{ident}' — {n} breathe cycles per {loop_ms}ms loop, {amp}px")]
    out.append(P.keyframes(f"{ident}-breathe", breathe, dur,
                           template="translateY({0}px)"))

    if blink:
        # A blink is a scaleY collapse, not an opacity fade. Two per loop reads
        # as alive; more reads as nervous.
        b0, b1 = 0.30, 0.30 + 0.11
        frames = [(0, 1), (b0, 1), (b0 + 0.045, 0.08), (b1, 1), (loop_s, 1)]
        out.append(P.keyframes(f"{ident}-blink", frames, loop_s,
                               template="scaleY({0})"))

    out.append(f""".{ident}-breathe{{
  animation-name:{ident}-breathe;
  animation-duration:calc(var(--loop) / {n});
  animation-timing-function:linear;
  animation-iteration-count:infinite;
}}""")
    if blink:
        out.append(f""".{ident}-blink{{
  transform-box:fill-box; transform-origin:50% 50%;
  animation-name:{ident}-blink;
  animation-duration:var(--loop);
  animation-timing-function:steps(1,end);
  animation-iteration-count:infinite;
}}""")
    return "\n".join(out)


# --------------------------------------------------------------------------
# role: hop  (the pointer)
# --------------------------------------------------------------------------
def bake_hop(loop_ms, ident, stops, apex, dwell, fade, restitution):
    """The pointer mascot: travels a route, dwells at each stop.

    Emits three things that must be used together:
      1. keyTimes / keyPoints for <animateMotion> along the route path
      2. a squash keyframe set that fires on each landing
      3. a contact-shadow keyframe set derived from the same landings

    The route path is authored by hand in the artboard. This script only decides
    when the mascot is where, because that is the part that has to agree with the
    sequential highlight and with the loop boundary.
    """
    loop_s = loop_ms / 1000.0
    legs = stops - 1
    if legs < 1:
        sys.exit("--stops must be at least 2.")

    # Budget: total dwell + total travel = 1. Fade windows sit inside the first
    # and last dwell so the seam teleport is never visible.
    total_dwell = dwell * stops
    if total_dwell >= 0.9:
        sys.exit(f"--dwell {dwell} x {stops} stops = {total_dwell:.2f} of the loop. "
                 "Leave at least 10% for travel.")
    travel_f = (1.0 - total_dwell) / legs      # fraction of the loop, per leg
    travel_s = travel_f * loop_s               # seconds, per leg

    # keyTimes and keyPoints are fractions of the loop. Landings are seconds,
    # because every keyframe block below is built from physics.py in seconds.
    key_times, key_points, land_f = [], [], []
    t = 0.0
    for i in range(stops):
        p = i / legs
        key_times.append(round(t, 4)); key_points.append(round(p, 4))
        t += dwell
        key_times.append(round(t, 4)); key_points.append(round(p, 4))
        if i:
            land_f.append(t - dwell)
        if i < legs:
            t += travel_f
    key_times[-1] = 1.0
    landings = [f * loop_s for f in land_f]

    out = [banner(f"hop pointer '{ident}' — {stops} stops, {int(dwell * loop_ms)}ms dwell, "
                  f"{int(travel_s * 1000)}ms per leg")]

    # implied gravity, printed so a floaty arc gets caught before rendering
    g = P.gravity(apex, travel_s)
    verdict = ("floaty, raise the apex or shorten the leg" if g < 500
               else "ok" if g < 2000 else "snappy, lower the apex or lengthen the leg")
    out.append(banner(f"apex {apex}u over {P.fmt(travel_s,3)}s implies g = {P.fmt(g,0)} u/s^2 "
                      f"({verdict})"))

    out.append(f'''<!-- paste onto the <animateMotion> inside the route SVG -->
  dur="{P.fmt(loop_s,3)}s" repeatCount="indefinite" calcMode="linear" rotate="0"
  keyTimes="{';'.join(P.fmt(k,4) for k in key_times)}"
  keyPoints="{';'.join(P.fmt(k,4) for k in key_points)}"''')

    # squash on each landing, from physics.squash
    sq = [(0.0, 1.0, 1.0)]
    for L in landings:
        sy = 0.80
        sq += [(L - 0.05, 1.0, 1.0), (L, P.squash(sy), sy),
               (L + 0.07, P.squash(1.06), 1.06), (L + 0.16, 1.0, 1.0)]
    sq.append((loop_s, 1.0, 1.0))
    sq = sorted([f for f in sq if 0 <= f[0] <= loop_s], key=lambda f: f[0])
    out.append(P.keyframes(f"{ident}-squash", sq, loop_s, template="scale({0},{1})"))

    # contact shadow: wide and faint at the apex, tight and dark on landing
    sh = [(0.0, 15, .30)]
    for L in landings:
        sh += [(L - travel_s * 0.5, 7, .10), (L, 16, .32), (L + 0.16, 15, .30)]
    sh.append((loop_s, 15, .30))
    sh = sorted([x for x in sh if 0 <= x[0] <= loop_s], key=lambda x: x[0])
    out.append(P.shadow_keyframes(f"{ident}-shadow", sh, loop_s))

    if fade:
        f_in, f_out = dwell * 0.45, 1.0 - dwell * 0.45
        out.append(P.keyframes(
            f"{ident}-seam",
            [(0, 0), (f_in * loop_s, 1), (f_out * loop_s, 1), (loop_s, 0)],
            loop_s, prop="opacity", template="{0}"))
        out.append(banner("the seam fade is what hides the teleport from the last stop "
                          "back to the first. Without it the loop point is visible."))

    out.append(f'''.{ident}-squash{{
  transform-box:fill-box; transform-origin:50% 100%;
  animation-name:{ident}-squash; animation-duration:var(--loop);
  animation-timing-function:linear; animation-iteration-count:infinite;
}}
.{ident}-shadow{{
  animation-name:{ident}-shadow; animation-duration:var(--loop);
  animation-timing-function:linear; animation-iteration-count:infinite;
}}''')

    # the highlight schedule the artboard's cards must follow
    arrivals = [0.0] + land_f
    out.append(banner("sequential highlight: stop i lights at these loop percentages, "
                      "which are the arrival instants above"))
    out.append(banner("  " + "   ".join(f"{i+1}: {P.fmt(a*100,2)}%"
                                        for i, a in enumerate(arrivals))))
    # A negative delay pushes an animation FORWARD in its cycle. To be at progress 0
    # at time A, the offset is -(loop - A), not -A. Writing -A gives the reversed
    # order that looks almost right in a thumbnail and is obviously wrong on playback.
    out.append(banner("  as negative delays, REVERSED (see the reverse-delay trap in "
                      "animation-recipes.md):"))
    out.append(banner("  " + "   ".join(
        f"{i+1}: calc(var(--loop) * {P.fmt(-(1 - a),4)})" for i, a in enumerate(arrivals))))
    out.append(banner(f"  highlight keyframe: 0%{{on}} {P.fmt(dwell*100,2)}%{{off}} 100%{{off}}, "
                      "steps(1,end)"))
    if restitution:
        for a, d in P.restitution_series(apex, e=restitution, bounces=1):
            out.append(banner(f"  rebound: apex {P.fmt(a,1)}u over {P.fmt(d,3)}s"))
    return "\n".join(out)


# --------------------------------------------------------------------------
# role: payoff
# --------------------------------------------------------------------------
def bake_payoff(loop_ms, ident, at, rise, zeta, fn):
    """The reaction. Fires once per loop, at the instant the pointer arrives.

    Uses the underdamped step response rather than an ease, so the mascot
    overshoots and settles instead of gliding into place. That overshoot is the
    entire reason a reaction reads as a reaction.
    """
    loop_s = loop_ms / 1000.0
    t0 = at * loop_s
    dur = 0.52
    if t0 + dur > loop_s:
        sys.exit(f"--at {at} leaves {P.fmt(loop_s - t0,2)}s before the loop closes, "
                 f"and the spring needs {dur}s. Move it earlier.")

    samples = P.step_response(0, -rise, dur, zeta=zeta, fn=fn, n=8)
    frames = [(0.0, 0.0), (t0, 0.0)]
    frames += [(t0 + t, y) for t, y in samples]
    frames += [(t0 + dur + 0.30, 0.0), (loop_s, 0.0)]
    frames = sorted({(round(t, 4), round(y, 3)) for t, y in frames if t <= loop_s})

    out = [banner(f"payoff '{ident}' — fires at {P.fmt(at*100,1)}% of the loop, "
                  f"rise {rise}u, zeta {zeta}, fn {fn}Hz")]
    out.append(banner(f"zeta {zeta} reads as "
                      f"{'rubbery' if zeta < .28 else 'lively' if zeta < .45 else 'businesslike'}"))
    out.append(P.keyframes(f"{ident}-pop", frames, loop_s, template="translateY({0}px)"))
    out.append(f""".{ident}-pop{{
  animation-name:{ident}-pop; animation-duration:var(--loop);
  animation-timing-function:linear; animation-iteration-count:infinite;
}}""")
    return "\n".join(out)


# --------------------------------------------------------------------------
# budget
# --------------------------------------------------------------------------
def budget(w, h, mascot, travel, idles):
    """Estimate changed pixels per frame before building anything.

    A travelling element costs roughly twice its own box per frame: the encoder
    has to erase where it was and draw where it is. Idles cost their box once,
    because only a few rows change. build_gif.py reports the real number as
    motion:; this is the sanity check that stops you building a mascot the
    artboard cannot afford.
    """
    canvas = w * h
    box = mascot * mascot
    moving = box * 2 * travel + box * 0.35 * idles
    pct = moving / canvas * 100
    verdict = ("cheap" if pct < .5 else "healthy" if pct < 2
               else "dark flat grounds only" if pct < 5 else "OVER BUDGET")
    print(f"canvas        {w}x{h} = {canvas:,} px")
    print(f"pointer       {mascot}x{mascot} travelling, ~{box*2:,} px/frame")
    print(f"idles         {idles} x ~{int(box*0.35):,} px/frame")
    print(f"estimate      {pct:.2f}% of pixels per frame — {verdict}")
    if pct >= 2:
        cap = int(math.sqrt(canvas * 0.02 / (2 * travel + 0.35 * idles)))
        print(f"suggestion    drop the pointer to about {cap}px, or move to a dark flat ground")


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="role", required=True)

    def common(p):
        p.add_argument("--loop", type=int, default=6000, help="artboard loop in ms")
        p.add_argument("--id", dest="ident", required=True,
                       help="namespace prefix. Every keyframe and class gets it")

    p = sub.add_parser("idle"); common(p)
    p.add_argument("--n", type=int, default=2, help=f"cycles per loop, one of {LEGAL_DIVISORS}")
    p.add_argument("--amp", type=float, default=3, help="breathe amplitude in px, max 4")
    p.add_argument("--blink", action="store_true")

    p = sub.add_parser("hop"); common(p)
    p.add_argument("--stops", type=int, required=True)
    p.add_argument("--apex", type=float, default=46, help="arc height in user units")
    p.add_argument("--dwell", type=float, default=0.10, help="fraction of loop held at each stop")
    p.add_argument("--fade", action="store_true", default=True)
    p.add_argument("--restitution", type=float, default=0.0)

    p = sub.add_parser("payoff"); common(p)
    p.add_argument("--at", type=float, required=True, help="fraction of loop when it fires")
    p.add_argument("--rise", type=float, default=20)
    p.add_argument("--zeta", type=float, default=0.32)
    p.add_argument("--fn", type=float, default=6.5)

    p = sub.add_parser("budget")
    p.add_argument("--w", type=int, default=1080)
    p.add_argument("--h", type=int, default=1350)
    p.add_argument("--mascot", type=int, default=64)
    p.add_argument("--travel", type=int, default=1)
    p.add_argument("--idles", type=int, default=0)

    a = ap.parse_args()
    if a.role == "idle":
        print(bake_idle(a.loop, a.ident, a.n, a.amp, a.blink))
    elif a.role == "hop":
        print(bake_hop(a.loop, a.ident, a.stops, a.apex, a.dwell, a.fade, a.restitution))
    elif a.role == "payoff":
        print(bake_payoff(a.loop, a.ident, a.at, a.rise, a.zeta, a.fn))
    else:
        budget(a.w, a.h, a.mascot, a.travel, a.idles)


if __name__ == "__main__":
    main()
