import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { CabinetStage } from '../components/CabinetStage';
import { Paper, Raw } from '../components/Paper';
import { camera, io, P, pop } from '../lib/anim';
import { pocketWatch } from '../lib/draw';
import { C, FONT } from '../lib/theme';
import { SCENES } from '../timeline';

/** Scene 6 — "an inner clock" title card over the frozen cabinet scene */
export const ClockScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const end = SCENES.cabinet / fps;
  const fc = P(t, 0.15, 0.7);
  const card = pop(960, 470, fc);
  return (
    <Paper>
      <g transform={camera(1.03 + 0.02 * io(P(t, 0, 4.6)))}>
        <CabinetStage lt={end} clock={end + t} />
      </g>
      <rect width={1920} height={1080} fill={C.paper} opacity={0.62 * io(fc)} />
      <g {...card}>
        <rect x={-560} y={-150} width={1120} height={300} rx={26} fill="#f8e6b4" stroke={C.gold} strokeWidth={8} />
        <rect x={-540} y={-130} width={1080} height={260} rx={18} fill="none" stroke={C.ink} strokeWidth={3} />
        <text x={110} y={-82} textAnchor="middle" fontSize={32} fontFamily={FONT.kai} fill={C.muted} letterSpacing={4}>生理節律．生物時鐘</text>
        <text x={110} y={10} textAnchor="middle" fontSize={92} fontFamily={FONT.kai} fontWeight={700} fill={C.ink} letterSpacing={6}>植物身體裡</text>
        <text x={110} y={100} textAnchor="middle" fontSize={64} fontFamily={FONT.kai} fontWeight={700} fill="#b0473c" letterSpacing={6}>有自己的時鐘</text>
        <path d="M-40,118C60,110 200,110 270,116" stroke="#f0c23e" strokeWidth={10} strokeLinecap="round" opacity={0.8} fill="none" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - io(P(t, 0.9, 1.4))} />
        <Raw svg={pocketWatch(95, 300 + t * 40, t * 240)} transform="translate(-370 0)" />
      </g>
    </Paper>
  );
};
