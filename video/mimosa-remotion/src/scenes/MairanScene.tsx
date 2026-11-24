import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Paper, Raw } from '../components/Paper';
import { back, camera, f, io, lerp, out3, P, pop } from '../lib/anim';
import { bust, rot, scrollLabel, sunSVG } from '../lib/draw';
import { C, FONT } from '../lib/theme';

const BUST = bust();
const TAG = scrollLabel(0, 0, 330, 74, '天文學家', 44);

/** Scene 2 — 天文學家德梅朗 */
export const MairanScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pb = out3(P(t, 0, 0.7));
  const po = out3(P(t, 0.4, 0.9));
  const pt = out3(P(t, 0.6, 1.1));
  const [x1, y1] = rot(Math.cos(t * 1.5) * 190, Math.sin(t * 1.5) * 62, 0, 0, -12);
  const [x2, y2] = rot(Math.cos(t * 2.4 + 2) * 120, Math.sin(t * 2.4 + 2) * 38, 0, 0, -12);
  return (
    <Paper defs={<clipPath id="nameClip"><rect x={1180} y={330} width={560 * io(P(t, 0.8, 2.2))} height={260} /></clipPath>}>
      <g transform={camera(1.02 + 0.05 * io(P(t, 0, 4.5)), lerp(10, -14, P(t, 0, 4.5)))}>
        {/* portrait */}
        <Raw svg={BUST} transform={`translate(${f(380 - (1 - pb) * 80)} ${f(232 + (1 - pb) * 40)}) scale(1.5)`} opacity={pb} />
        {/* orbits & sun: an astronomer */}
        <g transform="translate(1420 250)" opacity={po}>
          <ellipse rx={190} ry={62} fill="none" stroke={C.ink} strokeWidth={2.5} transform="rotate(-12)" />
          <ellipse rx={120} ry={38} fill="none" stroke={C.ink} strokeWidth={2} transform="rotate(-12)" strokeDasharray="8 8" />
          <circle r={22} fill="#9aa3b5" stroke={C.ink} strokeWidth={2.5} />
          <circle cx={f(x1)} cy={f(y1)} r={13} fill="#c9a07a" stroke={C.ink} strokeWidth={2.5} />
          <circle cx={f(x2)} cy={f(y2)} r={9} fill="#93a8c9" stroke={C.ink} strokeWidth={2.5} />
        </g>
        <Raw svg={sunSVG(36, t)} transform={`translate(1690 150) scale(${f(back(P(t, 0.45, 0.95)))})`} opacity={po} />
        {/* telescope */}
        <g transform={`translate(${f(1540 + (1 - pt) * 200)} 760)`} opacity={pt}>
          <path d="M0,0L-80,180M0,0L80,180M0,0L0,190" stroke={C.ink} strokeWidth={5} strokeLinecap="round" />
          <g transform={`rotate(${f(-22 + Math.sin(t * 1.4) * 4)})`}>
            <path d="M-150,-6L120,-30L124,10L-150,22Z" fill="#c8a25e" stroke={C.ink} strokeWidth={3} />
            <path d="M-150,-6L120,-30L124,10L-150,22Z" fill="url(#hatch)" opacity={0.35} />
            <rect x={118} y={-40} width={26} height={60} rx={4} fill="#b08240" stroke={C.ink} strokeWidth={3} transform="rotate(-5 130 -10)" />
            <rect x={-190} y={-6} width={44} height={26} rx={4} fill="#7a5630" stroke={C.ink} strokeWidth={3} />
            <path d="M-40,-14L-40,14M40,-22L40,10" stroke={C.gold} strokeWidth={5} />
          </g>
          <circle r={9} fill={C.ink} />
        </g>
        {/* name written by hand */}
        <g clipPath="url(#nameClip)">
          <text x={1200} y={430} fontSize={70} fontFamily={FONT.script} fill={C.ink}>Jean-Jacques</text>
          <text x={1180} y={520} fontSize={70} fontFamily={FONT.script} fill={C.ink}>d&apos;Ortous de Mairan</text>
        </g>
        <path d="M1190,555C1350,540 1500,540 1690,548" fill="none" stroke={C.red} strokeWidth={4} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - io(P(t, 2.1, 2.6))} />
        <Raw svg={TAG} {...pop(1430, 650, P(t, 1.5, 1.9))} />
      </g>
    </Paper>
  );
};
