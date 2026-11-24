import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { MimosaStage, settled } from '../components/MimosaStage';
import { Paper, Raw } from '../components/Paper';
import { back, camera, clamp, f, io, lerp, out3, P } from '../lib/anim';
import { armReach, bust, cloud, pottedPlant, sunSVG } from '../lib/draw';
import { C, FONT } from '../lib/theme';

const LENS =
  `<path d="M500,346L548,300" stroke="#6b4a2a" stroke-width="12" stroke-linecap="round"/>` +
  `<circle cx="590" cy="258" r="62" fill="#dbe8ee" fill-opacity=".55" stroke="${C.ink}" stroke-width="10"/><circle cx="590" cy="258" r="62" fill="none" stroke="${C.gold}" stroke-width="5"/>` +
  `<path d="M556,232q14,-20 38,-24" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none"/>`;
const MAIRAN = bust() + armReach(498, 346) + LENS;
const POT = pottedPlant(1);
const BUBBLE =
  `<path d="M-200,-70C-210,-110 -120,-130 -80,-100C-50,-140 60,-140 90,-100C150,-130 230,-90 210,-40C260,-10 230,70 170,66C150,110 40,110 10,80C-30,110 -140,110 -160,66C-230,76 -250,-30 -200,-70Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="3.5"/>` +
  `<circle cx="-90" cy="118" r="18" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/><circle cx="-112" cy="158" r="10" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>`;
const DARK_CLOUD = 'M-62,22C-84,22 -84,-6 -62,-8C-62,-34 -26,-40 -14,-22C-4,-46 40,-42 40,-14C64,-22 78,14 56,22Z';

/** Scene 4 — everyone thought the plant "watches the sun"; what if it can't? */
export const WonderScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const arrowsOut = 1 - P(t, 0.1, 0.4);
  const mp = out3(P(t, 0.25, 1.0));
  const bp = P(t, 1.0, 1.45);
  const q2 = P(t, 3.3, 3.8); // the sun gets covered
  const qm = P(t, 3.7, 4.1);
  return (
    <Paper>
      <g transform={camera(1, 0, -10 * io(P(t, 0, 1)))}>
        <MimosaStage
          clipId="nightClip4"
          s={{
            t: t + 5.5,
            grow: 1,
            growR: 1,
            sun: 1,
            night: 1,
            moon: 1,
            kRight: 0,
            plantsOpacity: 1 - 0.25 * P(t, 0.25, 0.8),
            title: settled(960, 128),
            arrows: { transform: `translate(960 430) scale(${Math.max(0.0001, arrowsOut)})`, opacity: arrowsOut },
            labels: [settled(600, 790), settled(600, 885), settled(1560, 790), settled(1560, 885)],
          }}
        />
        {/* a grey cloud drifts over the real sun too */}
        <Raw svg={cloud(lerp(-160, 205, io(P(t, 3.4, 4.4))), 180, 1.9, '#8d8899', C.ink)} opacity={P(t, 3.4, 3.6)} />
        <Raw svg={POT} transform={`translate(1200 ${f(948 + (1 - mp) * 300)})`} />
        <Raw svg={MAIRAN} transform={`translate(820 ${f(560 + (1 - mp) * 420)}) scale(.64)`} opacity={clamp(mp * 2)} />
        {/* thought bubble */}
        <g transform={`translate(1000 385) scale(${f(Math.max(0.0001, back(bp) * 1.2))})`} opacity={clamp(bp * 3)}>
          <Raw svg={BUBBLE} />
          <Raw svg={sunSVG(32, t)} transform="translate(-106 0) scale(.9)" />
          <path d={DARK_CLOUD} fill="#6d6878" stroke={C.ink} strokeWidth={3} transform={`translate(${f(lerp(-330, -106, io(q2)))} 4)`} opacity={clamp(q2 * 4)} />
          <text x={40} y={18} textAnchor="middle" fontSize={40} fontFamily={FONT.kai} fontWeight={700} fill={C.ink} opacity={1 - clamp(q2 * 3)}>在看太陽？</text>
          <text x={75} y={18} textAnchor="middle" fontSize={38} fontFamily={FONT.kai} fontWeight={700} fill={C.ink} opacity={clamp(q2 * 3 - 1)}>看不到的話？</text>
          <text textAnchor="middle" fontSize={120} fontFamily={FONT.kai} fontWeight={700} fill={C.red} opacity={clamp(qm * 8)} transform={`translate(250 -60) scale(${f(Math.max(0.0001, back(qm)))}) rotate(${f(Math.sin(t * 6) * 6)})`}>？</text>
        </g>
      </g>
    </Paper>
  );
};
