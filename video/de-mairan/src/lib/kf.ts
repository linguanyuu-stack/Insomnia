import { Easing, interpolate } from 'remotion';

/** gentle ease used for every move: slow in, slow out */
export const ease = Easing.bezier(0.45, 0, 0.25, 1);

/** keyframes in seconds → value (clamped, eased per segment) */
export const kf = (t: number, times: number[], values: number[]) =>
  interpolate(t, times, values, { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease });

/** 0 → 1 fade starting at `start`, lasting `dur` seconds */
export const fadeIn = (t: number, start: number, dur = 1.6) => kf(t, [start, start + dur], [0, 1]);

/** slow idle sway in degrees (for plants) */
export const sway = (t: number, amp = 0.6, speed = 0.8, phase = 0) => Math.sin(t * speed + phase) * amp;
