import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Pencil } from '../components/Pencil';
import { Piece, pointOn, Stage } from '../components/Stage';
import { collage, kf, ramp, sketchIn, span } from '../lib/kf';
import { cut } from '../lib/pieces';

export const S5_SECONDS = 16;

const CABINET: Piece = { el: 'cabinet', x: 960, y: 590, s: 0.8, z: 0 };
// the dark inside of the cabinet (storyboard panel px ×4) — the previous transition lands here
const [ix0, iy0] = pointOn(CABINET, 270 * 4, 148 * 4);
const [ix1, iy1] = pointOn(CABINET, 362 * 4, 288 * 4);
export const S5_INTERIOR = { x: (ix0 + ix1) / 2, y: (iy0 + iy1) / 2, w: ix1 - ix0, h: iy1 - iy0 };

const ellipse = (cx: number, cy: number, rx: number, ry: number) =>
  `M${cx - rx},${cy} C${cx - rx},${cy - ry * 1.1} ${cx + rx},${cy - ry * 1.05} ${cx + rx},${cy} C${cx + rx},${cy + ry * 1.1} ${cx - rx * 0.9},${cy + ry} ${cx - rx * 1.04},${cy - ry * 0.1}`;

/** 不透光的櫃子 — outside the days pass (sun, then night, then sun); the result cards show the leaves keep their rhythm */
export const S5Cabinet: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const night = kf(t, [7.8, 8.9, 11.0, 12.1], [0, 1, 1, 0]);
  const arc = (a: number, b: number) => {
    const p = kf(t, [a, b], [0, 1], (x) => x);
    return { x: 780 + p * 600, y: 205 - Math.sin(p * Math.PI) * 90, o: span(t, a, b, 0.8) };
  };
  const sun1 = arc(5.4, 8.8);
  const moon = arc(8.2, 11.6);
  const sun2 = arc(11.0, 14.6);
  const dayCard = collage(t, 6.6, { dx: 760, rot: -12 }, 1.5);
  const nightCard = collage(t, 9.2, { dx: 760, rot: 12 }, -1.5);
  return (
    <Stage
      night={night}
      cam={{ zoom: kf(t, [0, S5_SECONDS], [1.0, 1.04]), x: kf(t, [0, 5, S5_SECONDS], [940, 960, 1010]) }}
      pieces={[
        { el: 'sun', x: sun1.x, y: sun1.y, s: 0.36, z: -80, rot: t * 6, opacity: sun1.o, glow: true, key: 'sun1' },
        { el: 'nightSky', x: moon.x, y: moon.y, s: 0.42, z: -80, opacity: moon.o, back: 1, shadow: 0.6, glow: true },
        { el: 'sun', x: sun2.x, y: sun2.y, s: 0.36, z: -80, rot: t * 6, opacity: sun2.o, glow: true, key: 'sun2' },
        CABINET,
        { el: 'mairanWrite', x: 395, y: 665, s: 0.8, z: 30, ...sketchIn(t, 0.6, 3.0) },
        cut('bubble', 600, 300, 0.68, collage(t, 2.4, { dy: -520, rot: -16 }, -3), { z: 60 }),
        cut('resultHead', 1560, 185, 0.46, collage(t, 5.8, { dx: 700, rot: 12 }, -2), { z: 40 }),
        cut('resultDay', 1560, 415, 0.5, dayCard, { z: 40, opacity: dayCard.opacity * (1 - 0.5 * night), glow: true }),
        cut('resultNight', 1560, 640, 0.5, nightCard, { z: 40, opacity: nightCard.opacity * (0.5 + 0.5 * night), glow: true }),
      ]}
    >
      <Pencil
        id="s5"
        strokes={[
          { d: ellipse(1560, 415, 250, 95), p: ramp(t, 7.4, 1.0) * (1 - ramp(t, 9.0, 0.6)), width: 6, color: '#c0573f' },
          { d: ellipse(1560, 640, 250, 95), p: ramp(t, 9.9, 1.0) * (1 - ramp(t, 11.6, 0.6)), width: 6, color: '#4f63a8' },
          { d: ellipse(1560, 415, 250, 95), p: ramp(t, 12.2, 1.0), width: 6, color: '#c0573f' },
        ]}
      />
      <Captions
        items={[
          [0.6, 5.4, '德梅朗把觀察的那一株含羞草，放進不透光的櫃子裡。'],
          [5.8, 9.4, '結果，葉子沒因照不到太陽，'],
          [9.6, 13.8, '照樣在白天張開、在晚上合起來。'],
        ]}
      />
    </Stage>
  );
};
