import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Pencil } from '../components/Pencil';
import { Stage } from '../components/Stage';
import { collage, kf, ramp, sketchIn, sketchOut, sway } from '../lib/kf';
import { both, cut } from '../lib/pieces';

export const S3_SECONDS = 13;

/**
 * 白天張開、晚上合起來 — sunlight falls on the open leaves; then the sun sinks, a night-sky
 * scrap slides in, the page turns blue, and the plant is erased back to pencil and redrawn folded.
 */
export const S3DayNight: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const night = kf(t, [6.0, 8.6], [0, 1]);
  const light = ramp(t, 2.6, 1.4) * (1 - ramp(t, 5.6, 1.2));
  const [sx, sy] = [320, 250];
  // warm rays from the sun towards the leaves ("受光")
  const rays = [-14, -4, 6, 16].map((a, i) => {
    const r = (a * Math.PI) / 180 + 0.62;
    const [x0, y0] = [sx + Math.cos(r) * 130, sy + Math.sin(r) * 130];
    const [x1, y1] = [sx + Math.cos(r) * (390 + i * 30), sy + Math.sin(r) * (390 + i * 30)];
    return { d: `M${x0.toFixed(0)},${y0.toFixed(0)} L${x1.toFixed(0)},${y1.toFixed(0)}`, p: ramp(t, 2.6 + i * 0.15, 1.0) * light, color: '#e8b13f', width: 4, opacity: 0.8 };
  });
  return (
    <Stage
      night={night}
      cam={{ zoom: kf(t, [0, S3_SECONDS], [1.0, 1.06]), x: kf(t, [0, 6, S3_SECONDS], [930, 950, 1000]) }}
      pieces={[
        { el: 'sun', x: sx, y: sy + kf(t, [6.0, 8.4], [0, 900]), s: 0.62, z: -80, rot: t * 4, glow: true, opacity: 1 - ramp(t, 7.3, 1.0), ...sketchIn(t, 0.3, 2.4) },
        { el: 'cloud', x: 610 + t * 9, y: 170, s: 0.6, z: -90, opacity: 1 - 0.7 * night, ...sketchIn(t, 0.9, 2.2) },
        cut('nightSky', 1400, 235, 0.82, collage(t, 6.2, { dx: 1100, rot: 14 }, 2, 2.4), { z: -60, glow: true }),
        cut('title', 1000, 140, 0.58, collage(t, 1.4, { dy: -420, rot: -14 }, -2), { z: 60 }),
        { el: 'plantOpen', x: 920, y: 590, s: 0.86, z: 20, rot: sway(t, 0.8, 0.9), ...both(sketchIn(t, 1.0, 3.2), sketchOut(t, 6.8, 2.4)) },
        { el: 'plantClosed', x: 970, y: 610, s: 0.9, z: 20, rot: sway(t, 0.6, 0.7, 1), ...sketchIn(t, 7.8, 3.0) },
      ]}
    >
      <Pencil id="s3" strokes={rays} />
      <Captions
        items={[
          [1.0, 5.8, '注意到，含羞草的葉子在白天張開、'],
          [6.4, 10.8, '晚上合起來。'],
        ]}
      />
    </Stage>
  );
};
