import type { ElName, Piece } from '../components/Stage';
import { collage } from './kf';

/** place a collage cut-out (see kf.collage) */
export const cut = (el: ElName, x: number, y: number, s: number, c: ReturnType<typeof collage>, extra: Partial<Piece> = {}): Piece => ({
  el,
  x: x + c.dx,
  y: y + c.dy,
  s: s * c.press,
  rot: c.rot,
  opacity: c.opacity,
  back: c.back,
  shadow: c.shadow,
  ...extra,
});

/** combine a sketch-in and a sketch-out (takes the smaller of each) */
export const both = (a: { draw: number; color: number }, b: { draw: number; color: number }) => ({
  draw: Math.min(a.draw, b.draw),
  color: Math.min(a.color, b.color),
});
