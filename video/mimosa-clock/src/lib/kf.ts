import { Easing, interpolate } from 'remotion';

/** slow-in / slow-out used for every move */
export const ease = Easing.bezier(0.45, 0, 0.25, 1);

/** keyframes in seconds → value (clamped, eased per segment) */
export const kf = (t: number, times: number[], values: number[], easing = ease) =>
  interpolate(t, times, values, { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing });

/** 0 → 1 between start and start + dur seconds */
export const ramp = (t: number, start: number, dur = 1.6) => kf(t, [start, start + dur], [0, 1]);

/** 0 → 1 → 0 window */
export const span = (t: number, a: number, b: number, fade = 1) => Math.min(ramp(t, a, fade), 1 - ramp(t, b - fade, fade));

/** idle sway (degrees) */
export const sway = (t: number, amp = 0.8, speed = 0.8, phase = 0) => Math.sin(t * speed + phase) * amp;

/** sketch-then-colour reveal: pencil lines over `dur`, colour starts halfway */
export const sketchIn = (t: number, start: number, dur = 2.6) => ({
  draw: ramp(t, start, dur * 0.6),
  color: ramp(t, start + dur * 0.4, dur * 0.6),
});

/** colour fades back to pencil, then the pencil is erased */
export const sketchOut = (t: number, start: number, dur = 2.0) => ({
  color: 1 - ramp(t, start, dur * 0.6),
  draw: 1 - ramp(t, start + dur * 0.4, dur * 0.6),
});

/**
 * Collage: a paper cut-out slides in from an offset, turning, and settles like it is
 * pressed onto the page (tiny overshoot), with its paper margin and shadow.
 */
export const collage = (t: number, start: number, from: { dx?: number; dy?: number; rot?: number }, settleRot = 0, dur = 1.8) => {
  const p = ramp(t, start, dur);
  const press = kf(t, [start + dur * 0.8, start + dur, start + dur + 0.35], [1, 1.025, 1]);
  return {
    dx: (from.dx ?? 0) * (1 - p),
    dy: (from.dy ?? 0) * (1 - p),
    rot: settleRot + (from.rot ?? 0) * (1 - p),
    opacity: Math.min(1, p * 3),
    press,
    back: 1,
    shadow: 1,
  };
};
