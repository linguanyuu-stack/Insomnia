import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Pencil } from '../components/Pencil';
import { pointOn, Stage } from '../components/Stage';
import { collage, kf, ramp, sketchIn, sway } from '../lib/kf';
import { cut } from '../lib/pieces';

export const S4_SECONDS = 12;
/** where the sun sits — the next transition's darkness starts here */
export const S4_SUN: [number, number] = [330, 235];

const darkScrap = (cx: number, cy: number) => {
  // a torn piece of dark paper, drawn as a rough blob
  let d = '';
  for (let i = 0; i < 28; i++) {
    const a = (i / 28) * Math.PI * 2;
    const r = 170 + Math.sin(i * 2.7) * 14 + Math.cos(i * 5.3) * 9;
    d += `${i ? 'L' : 'M'}${(cx + Math.cos(a) * r * 1.15).toFixed(1)},${(cy + Math.sin(a) * r).toFixed(1)}`;
  }
  return d + 'Z';
};

/** 大家以為植物在「看太陽」… 但如果看不到太陽呢？ */
export const S4Wonder: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const mairan = cut('mairanLens', 1330, 690, 0.78, collage(t, 2.0, { dx: 950, rot: 12 }, 0, 2.2), { z: 50 });
  const [hx, hy] = pointOn(mairan, 300 * 4, 150 * 4);
  const cover = kf(t, [5.8, 7.2], [0, 1]);
  const [sx, sy] = S4_SUN;
  return (
    <Stage
      night={0.35 * cover}
      cam={{ zoom: kf(t, [0, S4_SECONDS], [1.0, 1.07]), x: kf(t, [0, S4_SECONDS], [980, 900]), y: kf(t, [0, S4_SECONDS], [540, 500]) }}
      pieces={[
        { el: 'sun', x: sx, y: sy, s: 0.62, z: -60, rot: t * 4, glow: true }, // already up: the morning blooms out of it
        { el: 'cloud', x: 640 + t * 8, y: 150, s: 0.5, z: -80, ...sketchIn(t, 1.0, 2.0) },
        { el: 'plantOpen', x: 610, y: 610, s: 0.66, z: 10, rot: sway(t, 0.8, 0.9), ...sketchIn(t, 0.9, 2.6) },
        mairan,
      ]}
    >
      <Pencil
        id="s4"
        strokes={[
          // "the plant looks at the sun": a dashed pencil line from the sun to the leaves
          { d: `M${sx + 70},${sy + 80} Q${sx + 260},${sy + 40} ${sx + 330},${sy + 230}`, p: ramp(t, 3.4, 1.3) * (1 - ramp(t, 5.8, 1.0)), dash: '16 14', width: 5, color: '#c58a2a' },
          { d: `M${sx + 305},${sy + 205} L${sx + 330},${sy + 232} L${sx + 345},${sy + 198}`, p: ramp(t, 4.6, 0.4) * (1 - ramp(t, 5.8, 0.6)), width: 5, color: '#c58a2a' },
          // a big hand-drawn question mark next to de Mairan
          { d: `M${hx - 70},${hy - 250} C${hx - 70},${hy - 330} ${hx + 50},${hy - 330} ${hx + 45},${hy - 260} C${hx + 40},${hy - 210} ${hx - 15},${hy - 205} ${hx - 15},${hy - 150}`, p: ramp(t, 7.0, 1.1), width: 11, color: '#b4553f' },
          { d: `M${hx - 16},${hy - 112} l2,4`, p: ramp(t, 8.1, 0.2), width: 14, color: '#b4553f' },
        ]}
      />
      {/* a scrap of dark paper slides over the sun */}
      {cover > 0.001 ? (
      <svg width={1920} height={1080} style={{ position: 'absolute', opacity: Math.min(1, cover * 2) }}>
        <defs>
          <pattern id="s4hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(40)">
            <line x1="0" y1="0" x2="0" y2="9" stroke="#3a3747" strokeWidth="2" />
          </pattern>
          <filter id="s4shadow">
            <feDropShadow dx="10" dy="14" stdDeviation="10" floodColor="#1a120a" floodOpacity="0.4" />
          </filter>
        </defs>
        <g transform={`translate(${(1 - cover) * -520} ${(1 - cover) * -160}) rotate(${(1 - cover) * -20} ${sx} ${sy})`}>
          <path d={darkScrap(sx, sy)} fill="#23212c" filter="url(#s4shadow)" />
          <path d={darkScrap(sx, sy)} fill="url(#s4hatch)" opacity={0.7} />
        </g>
      </svg>
      ) : null}
      <Captions
        items={[
          [1.2, 5.5, '那時，大家都以為那是植物在「看太陽」。'],
          [5.8, 9.8, '但他想知道：如果看不到太陽呢？'],
        ]}
      />
    </Stage>
  );
};
