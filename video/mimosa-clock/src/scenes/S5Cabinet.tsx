import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Pencil } from '../components/Pencil';
import { alignTo, Piece, pointOn, Stage } from '../components/Stage';
import { clamp, collage, kf, ramp, sketchIn, span } from '../lib/kf';
import { cut } from '../lib/pieces';

export const S5_SECONDS = 16.5;

const CAB: Piece = { el: 'cabinetBare', x: 1000, y: 565, s: 0.85 };
// the dark opening of the cabinet (storyboard px ×4) — the previous transition lands here
const [ix0, iy0] = pointOn(CAB, 270 * 4, 148 * 4);
const [ix1, iy1] = pointOn(CAB, 363 * 4, 279 * 4);
export const S5_INTERIOR = { x: (ix0 + ix1) / 2, y: (iy0 + iy1) / 2, w: ix1 - ix0, h: iy1 - iy0 };
const POT_HOME = alignTo(CAB, 'pot');
const DOOR = alignTo(CAB, 'door');
const HINGE = [...pointOn(CAB, 366 * 4, 217 * 4)] as [number, number];
const POT_START = { x: 640, y: 770 }; // on the desk, beside de Mairan's book
// the "peek inside" window
const PEEK = { x: 1575, y: 470, r: 215 };

/**
 * 不透光的櫃子 — the plant is carried into the cabinet and the door swings shut (3D hinge).
 * A window then opens onto the dark inside: while sun and moon pass outside, the leaves
 * still open by day and fold at night.
 */
export const S5Cabinet: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  // carry the pot into the cabinet
  const carry = kf(t, [1.8, 3.8], [0, 1]);
  const potX = POT_START.x + (POT_HOME.x - POT_START.x) * carry;
  const potY = POT_START.y + (POT_HOME.y - POT_START.y) * carry - Math.sin(carry * Math.PI) * 130;
  // the door swings shut, then a little settle
  const door = kf(t, [3.9, 5.2, 5.45, 5.65], [118, 0, 3, 0]);
  // outside: day → night → day
  const night = kf(t, [8.6, 9.6, 12.0, 13.0], [0, 1, 1, 0]);
  const arc = (a: number, b: number) => {
    const p = kf(t, [a, b], [0, 1], (x) => x);
    return { x: 640 + p * 640, y: 200 - Math.sin(p * Math.PI) * 95, o: span(t, a, b, 0.8) };
  };
  const sun1 = arc(6.4, 9.4);
  const moon = arc(9.0, 12.8);
  const sun2 = arc(12.4, 16.4);
  // the peek window grows out of the cabinet
  const pk = kf(t, [5.9, 7.3], [0, 1]);
  const peek = {
    x: S5_INTERIOR.x + (PEEK.x - S5_INTERIOR.x) * pk,
    y: S5_INTERIOR.y + (PEEK.y - S5_INTERIOR.y) * pk,
    r: 40 + (PEEK.r - 40) * pk,
  };
  const clip: [number, number, number] = [peek.x, peek.y, peek.r];
  const open = 1 - night; // inside, the leaves follow the day even in the dark
  const inOpen = { draw: clamp(open * 2), color: clamp((open - 0.35) / 0.65) };
  const inClosed = { draw: clamp(night * 2), color: clamp((night - 0.35) / 0.65) };
  const stamp = collage(t, 5.3, { dy: -60, rot: -30 }, -7, 0.7);
  return (
    <Stage
      night={night}
      cam={{ zoom: kf(t, [0, 3.5, 5.6, 6.8], [1.0, 1.05, 1.05, 1.0]), x: kf(t, [0, 3.5, 5.6, 6.8], [960, 990, 990, 960]) }}
      under={
        pk > 0.001 ? (
          <AbsoluteFill>
            <svg width={1920} height={1080} style={{ position: 'absolute' }}>
              <defs>
                <pattern id="peekHatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(40)">
                  <line x1="0" y1="0" x2="0" y2="8" stroke="#45414f" strokeWidth="2" />
                </pattern>
              </defs>
              <circle cx={peek.x} cy={peek.y} r={peek.r} fill="#25222d" />
              <circle cx={peek.x} cy={peek.y} r={peek.r} fill="url(#peekHatch)" opacity={0.6} />
            </svg>
          </AbsoluteFill>
        ) : null
      }
      pieces={[
        { el: 'sun', x: sun1.x, y: sun1.y, s: 0.36, z: -80, rot: t * 6, opacity: sun1.o, glow: true, key: 'sun1' },
        { el: 'nightSky', x: moon.x, y: moon.y, s: 0.42, z: -80, opacity: moon.o, back: 1, shadow: 0.6, glow: true },
        { el: 'sun', x: sun2.x, y: sun2.y, s: 0.36, z: -80, rot: t * 6, opacity: sun2.o, glow: true, key: 'sun2' },
        CAB,
        { el: 'mairanWrite', x: 395, y: 665, s: 0.8, z: 30, ...sketchIn(t, 0.4, 3.0) },
        { el: 'pot', x: potX, y: potY, s: POT_HOME.s, z: 0, rot: Math.sin(carry * Math.PI) * -6, ...sketchIn(t, 0.9, 1.8) },
        { ...DOOR, rotY: door, pivot: HINGE, z: 0 },
        cut('kwDark', DOOR.x, DOOR.y - 40, 1.25, stamp, { z: 5, opacity: stamp.opacity * (1 - ramp(t, 6.6, 0.8)) }),
        // inside the cabinet, seen through the window
        { el: 'plantOpen', x: peek.x - 20, y: peek.y + 30, s: 0.42 * (0.4 + 0.6 * pk), clip, glow: true, ...inOpen, opacity: pk },
        { el: 'plantClosed', x: peek.x - 10, y: peek.y + 40, s: 0.44 * (0.4 + 0.6 * pk), clip, glow: true, ...inClosed, opacity: pk },
      ]}
    >
      <Pencil
        id="s5"
        strokes={[
          // the window's pencil rim and a dashed line back to the cabinet door
          { d: `M${peek.x + peek.r},${peek.y} A${peek.r},${peek.r} 0 1 1 ${peek.x + peek.r - 0.1},${peek.y - 1}`, p: ramp(t, 6.2, 1.2), width: 6, color: '#4a3c32' },
          { d: `M${DOOR.x + 150},${DOOR.y - 60} Q${(DOOR.x + PEEK.x) / 2},${PEEK.y - 120} ${PEEK.x - PEEK.r - 10},${PEEK.y - 30}`, p: ramp(t, 7.0, 1.0), dash: '14 12', width: 4, color: '#6b5a4a' },
        ]}
      />
      <Captions
        items={[
          [0.6, 5.4, '德梅朗把觀察的那一株含羞草，放進不透光的櫃子裡。'],
          [5.8, 9.6, '結果，葉子沒因照不到太陽，'],
          [9.8, 14.6, '照樣在白天張開、在晚上合起來。'],
        ]}
      />
    </Stage>
  );
};
