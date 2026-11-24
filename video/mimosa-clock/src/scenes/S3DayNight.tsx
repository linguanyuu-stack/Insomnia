import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Stage } from '../components/Stage';
import { collage, kf, ramp, sketchIn, sketchOut, sway } from '../lib/kf';
import { both, cut } from '../lib/pieces';

export const S3_SECONDS = 13;

/**
 * 白天張開、晚上合起來 — one plant on the page. The sun sinks, a night-sky scrap slides in,
 * the page turns blue, and the open plant is erased back to pencil and redrawn folded.
 */
export const S3DayNight: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const night = kf(t, [6.0, 8.6], [0, 1]);
  const dayLabel = collage(t, 3.8, { dx: 900, rot: 18 }, -3);
  const dayLabelOut = kf(t, [7.0, 8.4], [0, 1]);
  return (
    <Stage
      night={night}
      cam={{ zoom: kf(t, [0, S3_SECONDS], [1.0, 1.06]), x: kf(t, [0, 6, S3_SECONDS], [930, 950, 1000]) }}
      pieces={[
        { el: 'sun', x: 320, y: 250 + kf(t, [6.0, 8.4], [0, 900]), s: 0.62, z: -80, rot: t * 4, glow: true, opacity: 1 - ramp(t, 7.3, 1.0), ...sketchIn(t, 0.3, 2.4) },
        { el: 'cloud', x: 610 + t * 9, y: 170, s: 0.6, z: -90, opacity: 1 - 0.7 * night, ...sketchIn(t, 0.9, 2.2) },
        cut('nightSky', 1400, 235, 0.82, collage(t, 6.2, { dx: 1100, rot: 14 }, 2, 2.4), { z: -60, glow: true }),
        cut('title', 985, 140, 0.58, collage(t, 1.4, { dy: -420, rot: -14 }, -2), { z: 60 }),
        { el: 'plantOpen', x: 900, y: 575, s: 0.8, z: 20, rot: sway(t, 0.8, 0.9), ...both(sketchIn(t, 1.0, 3.2), sketchOut(t, 6.8, 2.4)) },
        { el: 'plantClosed', x: 950, y: 600, s: 0.84, z: 20, rot: sway(t, 0.6, 0.7, 1), ...sketchIn(t, 7.8, 3.0) },
        cut('labelDay', 1500, 730, 0.52, dayLabel, {
          z: 90,
          y: 730 + dayLabel.dy + dayLabelOut * 700,
          rot: dayLabel.rot + dayLabelOut * 25,
          opacity: dayLabel.opacity * (1 - kf(t, [7.6, 8.4], [0, 1])),
        }),
        cut('labelNight', 1500, 730, 0.52, collage(t, 10.0, { dy: 800, rot: -16 }, 2), { z: 90, glow: true }),
      ]}
    >
      <Captions
        items={[
          [1.0, 5.8, '注意到，含羞草的葉子在白天張開、'],
          [6.4, 11.0, '晚上合起來。'],
        ]}
      />
    </Stage>
  );
};
