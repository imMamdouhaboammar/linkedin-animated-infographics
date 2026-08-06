"""Keyframe generators for physically grounded SVG animation.

Everything returns (time_seconds, value) sample lists, or a finished CSS keyframe
string via keyframes(). Times are absolute seconds inside one loop; convert to
percentages with the loop duration so several animations stay in sync.
"""

import math

# Easing curves that correspond to real motion. Anything not on this list is a
# stylistic choice and should be justified.
EASING = {
    # displacement of a body under constant acceleration, y proportional to t^2
    "free_fall":   "cubic-bezier(.11,0,.5,0)",
    # deceleration under constant negative acceleration
    "decelerate":  "cubic-bezier(.5,1,.89,1)",
    # sinusoidal velocity profile: pendulum, breathing, any simple harmonic motion
    "sine_inout":  "cubic-bezier(.37,0,.63,1)",
    # settling into a rest position with a small overshoot
    "settle":      "cubic-bezier(.25,.7,.35,1)",
    # explosive release out of anticipation
    "release":     "cubic-bezier(.5,0,.75,1)",
    # arrival that overshoots then comes back
    "overshoot":   "cubic-bezier(.3,.85,.4,1)",
}


def fmt(v, n=2):
    """Trim floats so generated CSS stays small and readable."""
    s = f"{v:.{n}f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def pct(t, duration):
    return fmt(t / duration * 100)


# --------------------------------------------------------------------------
# ballistics
# --------------------------------------------------------------------------
def projectile(t0, t1, apex, n=8):
    """Sampled parabolic arc from t0 to t1 peaking at `apex` units above ground.

    Returns (t, y) with y negative (SVG y grows downward). Emit these as keyframes
    with linear interpolation. Eight samples is enough for a full-frame arc; use
    more for very long hangtimes and fewer for small hops.
    """
    return [(t0 + (t1 - t0) * i / n, -4 * apex * (i / n) * (1 - i / n))
            for i in range(n + 1)]


def gravity(apex, airtime):
    """Implied gravitational constant in user units per second squared.

    Print this when designing a jump. Values far below ~500 read as floaty and far
    above ~2000 read as snappy and weightless. The absolute number only means
    something relative to the subject's height, so also report apex/height.
    """
    return 8 * apex / (airtime ** 2)


def restitution_series(apex, e=0.62, bounces=2, airtime=None):
    """Successive bounce apexes and airtimes for coefficient of restitution e.

    Height scales with e squared, airtime with e. Rigid plastic or metal sits
    around 0.55-0.7; something soft and heavy sits near 0.3.
    """
    if airtime is None:
        airtime = 2 * math.sqrt(2 * apex / 980)
    out = []
    for i in range(1, bounces + 1):
        out.append((apex * e ** (2 * i), airtime * e ** i))
    return out


def bounce_chain(t0, apex, e=0.62, bounces=2, airtime=0.85, n=8, n_decay=2):
    """Full landing sequence: successive arcs with decreasing apex and airtime.

    Returns (t, y) samples starting at t0 on the ground. Later arcs get fewer
    samples since they are shorter on screen.
    """
    out, t = [(t0, 0.0)], t0
    a, d = apex, airtime
    for i in range(bounces):
        a, d = a * e ** 2, d * e
        out += projectile(t, t + d, a, max(4, n - n_decay * i))
        t += d
    return out


# --------------------------------------------------------------------------
# oscillation
# --------------------------------------------------------------------------
def pendulum_period(length, g=980):
    """T = 2*pi*sqrt(L/g). Use length from the pivot to the centre of mass, not
    to the bottom of the artwork. Animate half of T with `alternate` and
    EASING["sine_inout"], which is the correct velocity profile, so the swing
    needs only two keyframes."""
    return 2 * math.pi * math.sqrt(length / g)


def step_response(start, target, duration, zeta=0.32, fn=6.5, n=7):
    """Underdamped second-order step response: overshoot, oscillate, settle.

    y(t) = target + (start-target) * e^(-zeta*wn*t) * [cos(wd*t) + (zeta*wn/wd)*sin(wd*t)]

    zeta 0.2 is loose and rubbery, 0.35 is lively, 0.6 is stiff and businesslike.
    fn is the natural frequency in Hz: small light objects 8-12, heavy bodies 4-6.
    Use this for every arrival, impact, and load change instead of easing to a
    flat value.
    """
    wn = 2 * math.pi * fn
    wd = wn * math.sqrt(1 - zeta ** 2)
    out = []
    for i in range(n + 1):
        t = duration * i / n
        env = math.exp(-zeta * wn * t)
        out.append((t, target + (start - target) * env *
                    (math.cos(wd * t) + (zeta * wn / wd) * math.sin(wd * t))))
    return out


def harmonic(t0, duration, amplitude, cycles=1, n=12, phase=0.0):
    """Plain sine motion for breathing, floating, and hovering. Sample it rather
    than easing between extremes when more than one full cycle is involved."""
    return [(t0 + duration * i / n,
             amplitude * math.sin(2 * math.pi * (cycles * i / n + phase)))
            for i in range(n + 1)]


# --------------------------------------------------------------------------
# secondary motion
# --------------------------------------------------------------------------
def shadow_track(samples, apex, rx_ground=34, rx_apex=15, op_ground=.30, op_apex=.10):
    """Contact shadow driven by the subject's own height samples.

    Feed it the exact list returned by projectile or bounce_chain. Deriving the
    shadow from a separate hand-made curve is the most common way depth stops
    reading, because the shadow drifts out of phase with the body.
    """
    out = []
    for t, y in samples:
        r = min(1.0, abs(y) / apex) if apex else 0.0
        out.append((t, rx_ground + (rx_apex - rx_ground) * r,
                    op_ground + (op_apex - op_ground) * r))
    return out


def squash(sy, preserve=0.55):
    """Horizontal scale for a given vertical scale.

    Strict area preservation is 1/sy, which looks liquid on blocky or rigid
    subjects. preserve=0.55 keeps the read without melting the silhouette;
    push toward 1.0 for soft characters, toward 0.2 for machinery.
    """
    return 1 + (1 - sy) * preserve


# --------------------------------------------------------------------------
# emitting CSS
# --------------------------------------------------------------------------
def keyframes(name, frames, duration, prop="transform", template="translateY({0}px)",
              easing=None, dedupe=True):
    """Build a @keyframes block from (time, *values) samples.

    frames: list of tuples, first element is time in seconds, the rest feed template
    easing: optional dict {time: easing string} applied to the segment starting there
    """
    easing = easing or {}
    seen, parts = set(), []
    for fr in frames:
        t, vals = fr[0], [fmt(v) for v in fr[1:]]
        key = pct(t, duration)
        body = template.format(*vals)
        if dedupe and (key, body) in seen:
            continue
        seen.add((key, body))
        e = easing.get(t) or easing.get(round(t, 4))
        tf = f";animation-timing-function:{e}" if e else ""
        parts.append(f"{key}%{{{prop}:{body}{tf}}}")
    return f"@keyframes {name}{{{''.join(parts)}}}"


def shadow_keyframes(name, tracked, duration):
    """Companion to shadow_track: emits rx and opacity together."""
    parts = [f"{pct(t, duration)}%{{rx:{fmt(rx)}px;opacity:{fmt(op, 3)}}}"
             for t, rx, op in tracked]
    return f"@keyframes {name}{{{''.join(parts)}}}"


# --------------------------------------------------------------------------
# timing reference, printed for convenience during design
# --------------------------------------------------------------------------
TIMING = {
    "anticipation_crouch": (0.25, 0.45),   # slow settle into the crouch
    "release":             (0.04, 0.08),   # explosive, shorter than you expect
    "contact_squash":      (0.04, 0.08),   # longer than this reads as soft
    "recovery_overshoot":  (0.10, 0.18),
    "blink":               (0.08, 0.14),
    "idle_breath_cycle":   (2.2, 3.6),
    "loop_total":          (3.0, 6.0),     # long enough to read, short enough to reread
}

if __name__ == "__main__":
    a, T = 95, 0.85
    print(f"apex {a} over {T}s -> g = {gravity(a, T):.0f} units/s^2")
    print("bounces:", [(round(h, 1), round(d, 2)) for h, d in restitution_series(a)])
    print(f"pendulum L=100 -> T = {pendulum_period(100, 986):.2f}s "
          f"(animate {pendulum_period(100, 986)/2:.2f}s alternate)")
