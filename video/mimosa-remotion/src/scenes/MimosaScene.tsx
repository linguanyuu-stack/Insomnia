import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { MimosaStage } from '../components/MimosaStage';
import { Paper } from '../components/Paper';
import { back, camera, f, io, out3, P, pop } from '../lib/anim';

/** Scene 3 — leaves open by day, fold at night */
export const MimosaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const ap = P(t, 1.5, 1.9);
  return (
    <Paper>
      <g transform={camera(1.03 - 0.03 * io(P(t, 0, 5.5)))}>
        <MimosaStage
          clipId="nightClip3"
          s={{
            t,
            grow: io(P(t, 0, 1.4)),
            growR: io(P(t, 0.15, 1.5)),
            sun: out3(P(t, 0.1, 0.9)),
            // night creeps over the right half, then the right plant folds
            night: io(P(t, 1.6, 2.6)),
            moon: out3(P(t, 1.8, 2.8)),
            kRight: 1 - io(P(t, 2.2, 3.4)),
            plantsOpacity: 1,
            title: pop(960, 128, P(t, 0.15, 0.6)),
            arrows: {
              transform: `translate(960 430) scale(${f(Math.max(0.0001, back(ap)))}) rotate(${f(Math.sin(t * 3) * 6)})`,
              opacity: Math.min(1, ap * 3),
            },
            labels: [pop(600, 790, P(t, 0.9, 1.3)), pop(600, 885, P(t, 1.1, 1.5)), pop(1560, 790, P(t, 2.6, 3.0)), pop(1560, 885, P(t, 3.2, 3.6))],
          }}
        />
      </g>
    </Paper>
  );
};
