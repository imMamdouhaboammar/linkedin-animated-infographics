# Physics and timing reference

Read this before writing keyframes. Import the functions from `scripts/physics.py`
rather than reimplementing the equations.

- [The one rule that matters most](#the-one-rule-that-matters-most)
- [Easing map](#easing-map)
- [Ballistics](#ballistics)
- [Oscillation](#oscillation)
- [Squash and stretch](#squash-and-stretch)
- [Secondary motion](#secondary-motion)
- [Timing values](#timing-values)
- [Loop construction](#loop-construction)

## The one rule that matters most

**Sample the curve, interpolate linearly.** An easing function between two keyframes is a
guess about the shape of the motion. For anything under acceleration, sample the real curve
at eight or more points and let the browser interpolate linearly between them.

A jump written as `0% {y:0} 50% {y:-95px} 100% {y:0}` with `ease-in-out` decelerates into the
apex and accelerates out of it in roughly the right way, but the middle of each half is
wrong: it spends too long at mid-height and not enough at the top. The result reads as
floating. Nine samples of `y = -4h·u(1-u)` with `linear` between them reads as gravity,
because it is gravity.

The exception is motion whose real velocity profile happens to match a named easing. A
pendulum is exactly sinusoidal, so `cubic-bezier(.37,0,.63,1)` between two keyframes is not
an approximation, it is the correct answer, and sampling would only add bytes.

## Easing map

| Motion | Curve | Why |
|---|---|---|
| Free fall, anything accelerating from rest | `cubic-bezier(.11,0,.5,0)` | approximates displacement proportional to t² |
| Deceleration to a stop under constant force | `cubic-bezier(.5,1,.89,1)` | mirror of the above |
| Pendulum, breathing, hovering, any simple harmonic motion | `cubic-bezier(.37,0,.63,1)` | sinusoidal velocity, zero at the extremes and maximum at the centre |
| Settling into rest | `cubic-bezier(.25,.7,.35,1)` | fast approach, soft arrival |
| Explosive release out of anticipation | `cubic-bezier(.5,0,.75,1)` | slow build then sharp exit |
| Arrival with overshoot | `cubic-bezier(.3,.85,.4,1)` | passes the target and comes back |

`ease`, `ease-in-out`, and `linear` on their own are not motion decisions. `linear` is
correct only between samples of a curve you already computed, and for constant-velocity
horizontal travel during flight, where there is no horizontal force.

## Ballistics

Apex `h` reached in airtime `T` implies `g = 8h/T²` in user units per second squared.
Print this while designing. Below roughly 500 the subject reads as floating in low gravity;
above roughly 2000 it reads weightless and snappy. What actually matters is the ratio of
apex to subject height: jumping two body-heights is athletic, six is cartoon.

Horizontal travel during flight is linear. Nothing pushes the subject sideways in the air,
so any easing on the x axis is a mistake that shows up as a subtle slide.

Bounces follow the coefficient of restitution `e`: each apex is `e²` of the previous one and
each airtime is `e` of the previous one. Rigid plastic and metal live around 0.55 to 0.70,
soft heavy bodies near 0.30. One visible rebound is usually enough; two if the subject is
light and comic. `restitution_series()` and `bounce_chain()` handle the arithmetic.

Rotation in the air is constant angular velocity, so linear between the launch angle and the
landing angle. A subject that speeds up its spin mid-flight looks wrong even when nobody can
say why.

## Oscillation

**Pendulum.** `T = 2π√(L/g)`, with `L` measured from the pivot to the centre of mass rather
than to the bottom of the artwork. Animate half of `T` with `alternate` and sinusoidal
easing. Deriving the duration from the visible rope length is what makes a long rope feel
heavy and a short one feel twitchy, which no amount of eyeballing reproduces reliably.

Rope tension peaks at the lowest point of the arc, which the pendulum passes twice per
period. Any tension effect therefore runs at double the swing frequency: a 2 s swing gets a
1 s tension cycle.

**Damped spring.** Every arrival, impact, and load change should overshoot and settle rather
than easing flatly into its target:

```
y(t) = target + (start - target)·e^(-ζωₙt)·[cos(ω_d t) + (ζωₙ/ω_d)·sin(ω_d t)]
where ωₙ = 2πfₙ  and  ω_d = ωₙ√(1-ζ²)
```

`ζ` (damping ratio) sets the character: 0.2 is loose and rubbery, 0.32 is lively, 0.6 is
stiff and corporate. `fₙ` (natural frequency, Hz) tracks mass: small light objects 8 to 12,
heavy bodies 4 to 6. Seven samples over 0.3 s is enough for a single impact. Use
`step_response()`.

**Breathing and hovering.** Plain sine at 0.3 to 0.45 Hz, amplitude 2 to 4 percent of the
subject's height. Sample it with `harmonic()` when more than one cycle is involved, since
chaining eased extremes accumulates error.

## Squash and stretch

Tie the deformation to velocity, not to a schedule:

- Stretch on launch, when vertical velocity is highest
- Neutral at the apex, where vertical velocity is zero
- Stretch again just before impact
- Squash on contact, briefly
- Overshoot slightly on recovery, then settle

Strict area preservation means `sx = 1/sy`, which looks liquid on rigid or blocky subjects.
`squash(sy, preserve)` interpolates: 0.55 keeps the read without melting the silhouette,
near 1.0 suits soft characters, near 0.2 suits machinery.

Typical magnitudes: anticipation crouch `sy` 0.78 to 0.84, launch stretch `sy` 1.18 to 1.25,
contact squash `sy` 0.68 to 0.75. Push past those and the subject stops looking like itself.

## Secondary motion

**Contact shadow.** Radius and opacity read from the same height samples as the body, via
`shadow_track()`. A shadow driven by its own hand-made curve drifts out of phase and quietly
destroys the sense of depth. A grounded shadow at radius 34 and opacity 0.30 shrinking to 15
and 0.10 at the apex is a good starting range for a subject around 60 units wide.

**Lag and follow-through.** Trailing parts move on the same period as their driver with a
phase offset of 6 to 10 percent and roughly 20 percent of the amplitude. In CSS this is a
negative `animation-delay` on the same duration, which keeps the two permanently in step.

**Anticipation.** Any committed move needs a preparatory move in the opposite direction. The
crouch takes 0.25 to 0.45 s and settles slowly; the release takes 0.04 to 0.08 s. The
asymmetry is the whole effect.

**Impact debris.** Two or three small circles expanding and fading over 0.25 to 0.4 s, each
with a slightly different scale and start time. Uniform debris reads as a graphic; varied
debris reads as an event.

## Timing values

| Beat | Duration |
|---|---|
| Anticipation crouch | 0.25 to 0.45 s, slow settle |
| Release from crouch | 0.04 to 0.08 s |
| Contact squash | 0.04 to 0.08 s, longer reads as soft |
| Recovery overshoot | 0.10 to 0.18 s |
| Blink | 0.08 to 0.14 s |
| Idle breath cycle | 2.2 to 3.6 s |
| Full loop | 3 to 6 s |

Loops under 3 s become annoying in a README that stays on screen while someone reads. Loops
over 6 s mean most viewers never see the payoff.

## Loop construction

A scene that ends where it began loops silently. When the subject has to end up somewhere
else, fade the actor across the last three to five percent, reset its position while it is
invisible, and fade back in over the first two percent. Keep the static set pieces (ground,
labels, frames) outside the fading group so only the actor resets.

When several elements share a loop, give them one duration and offset them with
`animation-delay`. Different durations drift apart over time and the scene desynchronises
after a few minutes on a page that nobody reloads.

Per-element variation inside one shared keyframe block comes from custom properties:
`transform: translateY(var(--drop))` inside `@keyframes` resolves per element, so ten falling
objects with different starting heights need one keyframe block and ten inline `--drop`
values.
