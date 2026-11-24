import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { CabinetStage } from '../components/CabinetStage';
import { Paper } from '../components/Paper';
import { camera, io, P } from '../lib/anim';

/** Scene 5 — the plant goes into a light-proof cabinet; leaves keep their rhythm */
export const CabinetScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  return (
    <Paper>
      <g transform={camera(1 + 0.03 * io(P(t, 0, 9.5)))}>
        <CabinetStage lt={t} clock={t} />
      </g>
    </Paper>
  );
};
