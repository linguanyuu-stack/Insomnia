import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Pencil } from '../components/Pencil';
import { pointOn, Stage } from '../components/Stage';
import { clamp, collage, kf, ramp, sketchIn, sway } from '../lib/kf';
import { cut } from '../lib/pieces';

export const S6_SECONDS = 12;

const WATCH = { el: 'watch' as const, x: 760, y: 640, s: 0.62 };
const FACE = pointOn(WATCH, 571 * 4, 223 * 4);
const HAND = 27 * 4 * WATCH.s * 0.78;
const REV = 6; // seconds per turn of the red hand: first half day, second half night

/**
 * 植物身體裡的時鐘 — the pocket watch sits in the plant like a heart, glowing. Its red hand
 * goes round, and the leaves fold and open in step with it. Key words: 自己的時鐘.
 */
export const S6Clock: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const run = Math.max(0, t - 2.2);
  const angle = (run / REV) * 360;
  // night while the hand is in the second half of its turn (smoothed)
  const phase = (run / REV) % 1;
  const nightIn = run <= 0 ? 0 : kf(phase, [0.44, 0.56, 0.94, 1], [0, 1, 1, 0], (x) => x);
  const appear = ramp(t, 0.6, 2.2);
  const open = 1 - nightIn;
  const glow = ramp(t, 1.6, 1.6) * (0.85 + 0.15 * Math.sin(t * 3));
  const stamp = collage(t, 5.2, { dx: 700, rot: 18 }, -4, 2.0);
  const [fx, fy] = FACE;
  return (
    <Stage
      night={0.35 * nightIn}
      cam={{ zoom: kf(t, [0, S6_SECONDS], [1.06, 0.98]), y: kf(t, [0, S6_SECONDS], [560, 540]) }}
      under={
        <AbsoluteFill
          style={{
            background: `radial-gradient(circle at ${fx}px ${fy}px, rgba(255,214,130,.75) 0px, rgba(255,214,130,.35) 140px, rgba(255,214,130,0) 330px)`,
            opacity: glow,
          }}
        />
      }
      pieces={[
        { el: 'plantOpen', x: 1010, y: 500, s: 0.86, z: -20, rot: sway(t, 0.7, 0.9), opacity: appear, glow: true, draw: clamp(open * 2) * appear, color: clamp((open - 0.35) / 0.65) * appear },
        { el: 'plantClosed', x: 1060, y: 520, s: 0.9, z: -20, rot: sway(t, 0.6, 0.7, 1), glow: true, draw: clamp(nightIn * 2), color: clamp((nightIn - 0.35) / 0.65) },
        { ...WATCH, z: 40, glow: true, ...sketchIn(t, 0.8, 2.4) },
        cut('kwClock', 1440, 850, 0.95, stamp, { z: 60, glow: true }),
      ]}
    >
      <Pencil
        id="s6"
        strokes={[
          // a red second hand that keeps the plant's time
          { d: `M${fx},${fy} L${(fx + Math.sin((angle * Math.PI) / 180) * HAND).toFixed(1)},${(fy - Math.cos((angle * Math.PI) / 180) * HAND).toFixed(1)}`, p: ramp(t, 2.0, 0.3), width: 4, color: '#c0392b' },
        ]}
      />
      <Captions items={[[1.0, 11.0, '就像植物身體裡，有自己的時鐘。']]} />
      <AbsoluteFill style={{ backgroundColor: '#fbecd8', opacity: kf(t, [11.2, 12], [0, 1]) }} />
    </Stage>
  );
};
