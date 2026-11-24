import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { Stage } from '../components/Stage';
import { collage, kf, sketchIn } from '../lib/kf';
import { cut } from '../lib/pieces';

export const S1_SECONDS = 8.5;

/** 時間是 1729 年 — the year is sketched in pencil, coloured, then globe & books are laid on the page */
export const S1Year: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  return (
    <Stage
      cam={{ zoom: kf(t, [0, S1_SECONDS], [1.0, 1.07]), y: kf(t, [0, S1_SECONDS], [540, 515]) }}
      pieces={[
        { el: 'banner', x: 960, y: 350, s: 0.78, ...sketchIn(t, 0.3, 3.6) },
        cut('globe', 790, 735, 0.82, collage(t, 2.8, { dy: 700, rot: -28 }, -4, 2.0), { z: 70 }),
        cut('books', 1110, 790, 0.9, collage(t, 3.3, { dy: 700, dx: 120, rot: 24 }, 3, 2.0), { z: 90 }),
      ]}
    >
      <Captions items={[[1.0, 6.3, '時間是 1729 年。']]} />
    </Stage>
  );
};
