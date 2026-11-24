import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Stage } from '../components/Stage';
import { collage, kf, sketchIn, sway } from '../lib/kf';
import { cut } from '../lib/pieces';

export const S2_SECONDS = 10;

/** 天文學家德梅朗 — the portrait is drawn line by line, his world of orbits & telescopes gathers around him */
export const S2Mairan: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  return (
    <Stage
      cam={{ zoom: kf(t, [0, S2_SECONDS], [1.0, 1.06]), x: kf(t, [0, S2_SECONDS], [985, 945]) }}
      pieces={[
        { el: 'portrait', x: 570, y: 600, s: 0.72, z: 40, ...sketchIn(t, 0.2, 3.8) },
        { el: 'orbit', x: 1390, y: 235, s: 0.72, z: -60, rot: sway(t, 2, 0.5), ...sketchIn(t, 2.2, 2.6) },
        { el: 'name', x: 1405, y: 485, s: 0.82, z: 10, ...sketchIn(t, 3.3, 2.4) },
        cut('telescope', 1480, 790, 0.78, collage(t, 4.8, { dx: 800, dy: 120, rot: 22 }, -2, 2.0), { z: 80 }),
      ]}
    >
      <Captions items={[[1.2, 7.6, '天文學家德梅朗（Jean-Jacques d’Ortous de Mairan）']]} />
    </Stage>
  );
};
