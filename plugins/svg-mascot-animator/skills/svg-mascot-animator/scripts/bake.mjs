#!/usr/bin/env node
/**
 * bake.mjs — turn Anime.js easing and spring solvers into static CSS @keyframes.
 *
 * The point: an asset destined for a README cannot run JavaScript, but it can
 * still be timed by the same solver that drives the interactive version. Sample
 * the solver here, emit keyframes, and both tracks share one motion identity.
 *
 * Library use:
 *   import { sampleEase, sampleSpring, keyframes, springKeyframes } from './bake.mjs';
 *
 * CLI:
 *   node bake.mjs spring --from 1 --to .64 --stiffness 90 --damping 8 --name press \
 *        --template "scale({sx},{v})" --loop 5000 --at 350
 *   node bake.mjs ease --name drop --ease outBounce --from -160 --to 0 \
 *        --template "translateY({v}px)" --loop 5000 --at 0 --dur 700
 *   node bake.mjs list
 */

import { eases, spring } from 'animejs';

const fmt = (v, n = 3) => {
  const s = v.toFixed(n).replace(/0+$/, '').replace(/\.$/, '');
  return s === '' || s === '-0' ? '0' : s;
};

/** Sample a named Anime.js ease into [progress0to1, easedValue] pairs. */
export function sampleEase(name, samples = 12) {
  const fn = typeof name === 'function' ? name : eases[name];
  if (!fn) throw new Error(`unknown ease "${name}". run: node bake.mjs list`);
  return Array.from({ length: samples + 1 }, (_, i) => {
    const u = i / samples;
    return [u, fn(u)];
  });
}

/**
 * Sample Anime.js's spring solver. Returns its own settling duration in ms,
 * which is the physically correct length for those parameters — use it instead
 * of picking a duration by feel.
 */
export function sampleSpring(opts = {}, samples = 14) {
  const s = spring({ stiffness: 100, damping: 10, mass: 1, velocity: 0, ...opts });
  return {
    duration: s.duration,
    samples: Array.from({ length: samples + 1 }, (_, i) => {
      const u = i / samples;
      return [u, s.ease(u)];
    }),
  };
}

/**
 * Emit a @keyframes block.
 *  progressSamples: [[u, easedProgress]]
 *  from/to:         the value range the progress drives
 *  at/dur/loop:     placement in milliseconds inside the loop
 *  template:        "{v}" is the value, "{sx}" is the companion squash width,
 *                   "{u}" is raw progress
 */
export function keyframes(name, progressSamples, {
  from = 0, to = 1, at = 0, dur = 1000, loop = 1000,
  prop = 'transform', template = 'translateY({v}px)',
  squashPreserve = 0.55, decimals = 3,
} = {}) {
  const seen = new Set();
  const parts = [];
  for (const [u, p] of progressSamples) {
    const v = from + (to - from) * p;
    const pct = fmt(((at + dur * u) / loop) * 100, 3);
    const body = template
      .replaceAll('{v}', fmt(v, decimals))
      .replaceAll('{u}', fmt(p, decimals))
      .replaceAll('{sx}', fmt(1 + (1 - v) * squashPreserve, decimals));
    const key = `${pct}|${body}`;
    if (seen.has(key)) continue;
    seen.add(key);
    parts.push(`${pct}%{${prop}:${body}}`);
  }
  return `@keyframes ${name}{${parts.join('')}}`;
}

/** Convenience: spring parameters straight to a keyframe block. */
export function springKeyframes(name, springOpts, placement = {}) {
  const { duration, samples } = sampleSpring(springOpts, placement.samples ?? 14);
  return {
    duration,
    css: keyframes(name, samples, { dur: duration, ...placement }),
  };
}

/** Anime.js ease name that matches a physical motion, for the static track. */
export const PHYSICAL_EASES = {
  freeFall: 'inQuad',        // displacement under constant acceleration
  decelerate: 'outQuad',
  pendulum: 'inOutSine',     // exact velocity profile of simple harmonic motion
  settle: 'outQuart',
  release: 'inCubic',
  overshoot: 'outBack',
  bounce: 'outBounce',       // built-in restitution chain, e fixed by the curve
  elastic: 'outElastic',
};

// ---------------------------------------------------------------- CLI
const argv = process.argv.slice(2);
if (argv.length) {
  const cmd = argv[0];
  const arg = (k, d) => {
    const i = argv.indexOf(`--${k}`);
    return i === -1 ? d : argv[i + 1];
  };
  const num = (k, d) => (arg(k) === undefined ? d : parseFloat(arg(k)));

  if (cmd === 'list') {
    console.log('anime.js eases:\n  ' + Object.keys(eases).sort().join(' '));
    console.log('\nphysical mapping:');
    for (const [k, v] of Object.entries(PHYSICAL_EASES)) console.log(`  ${k.padEnd(12)} ${v}`);
  } else if (cmd === 'spring') {
    const { duration, css } = springKeyframes(
      arg('name', 'spring-bake'),
      { stiffness: num('stiffness', 100), damping: num('damping', 10),
        mass: num('mass', 1), velocity: num('velocity', 0) },
      { from: num('from', 0), to: num('to', 1), at: num('at', 0),
        loop: num('loop', 1000), prop: arg('prop', 'transform'),
        template: arg('template', 'translateY({v}px)'),
        samples: num('samples', 14) },
    );
    console.error(`solver settling duration: ${duration}ms`);
    console.log(css);
  } else if (cmd === 'ease') {
    const css = keyframes(
      arg('name', 'ease-bake'),
      sampleEase(arg('ease', 'outQuad'), num('samples', 12)),
      { from: num('from', 0), to: num('to', 1), at: num('at', 0),
        dur: num('dur', 1000), loop: num('loop', 1000),
        prop: arg('prop', 'transform'),
        template: arg('template', 'translateY({v}px)') },
    );
    console.log(css);
  } else {
    console.error('commands: list | spring | ease');
    process.exit(1);
  }
}
