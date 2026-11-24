import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Stage } from '../components/Stage';
import { collage, kf, ramp, sketchIn, sway } from '../lib/kf';
import { cut } from '../lib/pieces';

export const S6_SECONDS = 11;

/** 植物身體裡的時鐘 — the pocket watch, with a sun and a night sky circling it; the little plant opens and folds in time */
export const S6Clock: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const [cx, cy] = [760, 470];
  const a = t * 0.55 - 1.2;
  const orbit = (ph: number) => ({ x: cx + Math.cos(a + ph) * 310, y: cy + Math.sin(a + ph) * 230, front: Math.sin(a + ph) > 0 });
  const sun = orbit(0);
  const moon = orbit(Math.PI);
  const appear = ramp(t, 1.6, 1.6);
  const dayW = kf(-Math.sin(a), [-0.35, 0.35], [0, 1]); // sun in the upper half → day
  return (
    <Stage
      night={0.45 * (1 - dayW) * appear}
      cam={{ zoom: kf(t, [0, S6_SECONDS], [1.04, 0.98]) }}
      pieces={[
        { el: 'sun', x: sun.x, y: sun.y, s: 0.3, z: sun.front ? 80 : -80, rot: t * 8, opacity: appear, glow: true },
        { el: 'nightSky', x: moon.x, y: moon.y, s: 0.32, z: moon.front ? 80 : -80, opacity: appear, back: 1, shadow: 0.5, glow: true },
        { el: 'watch', x: cx, y: cy, s: 1.15, z: 0, rot: sway(t, 2.5, 1.5), glow: true, ...sketchIn(t, 0.2, 2.8) },
        { el: 'plantOpen', x: 330, y: 820, s: 0.34, z: 30, rot: sway(t, 1, 0.9), opacity: dayW * ramp(t, 3.0, 1.4) },
        { el: 'plantClosed', x: 345, y: 830, s: 0.36, z: 30, rot: sway(t, 1, 0.9), opacity: (1 - dayW) * ramp(t, 3.0, 1.4) },
        cut('note', 1420, 520, 0.8, collage(t, 2.8, { dx: 950, rot: 16 }, 2, 2.2), { z: 50 }),
      ]}
    >
      <Captions items={[[1.0, 10.0, '像植物身體裡，有自己的時鐘。']]} />
      <AbsoluteFill style={{ backgroundColor: '#fbecd8', opacity: kf(t, [10.2, 11], [0, 1]) }} />
    </Stage>
  );
};
