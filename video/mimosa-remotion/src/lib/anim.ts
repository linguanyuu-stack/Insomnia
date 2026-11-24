// Small timing helpers. All times are in seconds (scene-local).
export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
/** progress 0..1 of t between a and b */
export const P = (t: number, a: number, b: number) => clamp((t - a) / (b - a));
export const io = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
export const out3 = (t: number) => 1 - Math.pow(1 - t, 3);
export const back = (t: number) => {
  const c1 = 1.9;
  const c3 = c1 + 1;
  return t <= 0 ? 0 : 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
};
/** round for compact SVG */
export const f = (n: number) => Math.round(n * 10) / 10;

/** transform + opacity for a "pop in" (overshoot scale) at x,y */
export const pop = (x: number, y: number, p: number, s = 1) => ({
  transform: `translate(${f(x)} ${f(y)}) scale(${Math.max(0.0001, back(p) * s)})`,
  opacity: clamp(p * 3),
});

/** camera push centred on the frame */
export const camera = (s: number, dx = 0, dy = 0) =>
  `translate(${960 + dx} ${540 + dy}) scale(${s}) translate(-960 -540)`;
