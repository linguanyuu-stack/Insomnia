import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Paper } from '../components/Paper';
import { back, camera, f, io, lerp, out3, P, pop } from '../lib/anim';
import { cr, tf } from '../lib/draw';
import { C, FONT } from '../lib/theme';

const LAUREL_STEM: [number, number][] = [[360, 560], [300, 470], [290, 360], [330, 260], [400, 200]];
const LAUREL_LEAVES = Array.from({ length: 9 }).flatMap((_, i) => {
  const t = i / 8;
  const idx = Math.min(3, Math.floor(t * 4));
  const u = t * 4 - idx;
  const [x1, y1] = LAUREL_STEM[idx];
  const [x2, y2] = LAUREL_STEM[Math.min(4, idx + 1)];
  const a = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;
  return [-1, 1].map((sd) => ({ x: lerp(x1, x2, u), y: lerp(y1, y2, u), a: a + sd * 50, i, sd }));
});

const Laurel: React.FC<{ t: number; mirror?: boolean }> = ({ t, mirror }) => (
  <g transform={mirror ? 'translate(1920 0) scale(-1 1)' : undefined}>
    <path d={cr(LAUREL_STEM)} fill="none" stroke="#6f7d3a" strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - out3(P(t, 0.3, 0.9))} />
    {LAUREL_LEAVES.map((o, k) => {
      const p = P(t, 0.4 + o.i * 0.08, 0.75 + o.i * 0.08);
      return (
        <g key={k} transform={tf(o.x, o.y, back(p) * 0.9 + 0.001, o.a)} opacity={Math.min(1, p * 4)}>
          <path d="M0,0C14,-14 40,-14 56,0C40,12 14,12 0,0Z" fill={o.sd < 0 ? '#9db45c' : '#87a24a'} stroke="#566b2a" strokeWidth={2} />
          <path d="M4,0L48,0" stroke="#566b2a" strokeWidth={1.3} />
        </g>
      );
    })}
  </g>
);

const Globe: React.FC<{ t: number }> = ({ t }) => {
  const ph = t * 1.6;
  let md = '';
  for (let i = 0; i < 4; i++) {
    const rx = Math.abs(Math.cos(ph + (i * Math.PI) / 4)) * 86;
    md += `M0,-86A${f(rx)},86 0 0 1 0,86A${f(rx)},86 0 0 1 0,-86`;
  }
  const off = ((t * 60) % 260) - 130;
  const land = [0, 260]
    .map((o) => `M${f(off + o - 40)},-50c30,-20 60,-10 50,20c-10,25 20,40 -10,60c-30,10 -50,-30 -40,-80zM${f(off + o - 150)},10c20,-10 40,0 35,25c-5,30 -40,20 -35,-25z`)
    .join('');
  return (
    <g transform="translate(860 735)">
      <path d="M-60,140L60,140L40,124L-40,124Z" fill={C.wood} stroke={C.ink} strokeWidth={3} />
      <path d="M0,96L0,124" stroke={C.ink} strokeWidth={6} />
      <circle r={86} fill="#cfd9cf" stroke={C.ink} strokeWidth={3} />
      <g clipPath="url(#globeClip)">
        <path d={land} fill="#b9a46c" stroke="#7d6a3c" strokeWidth={2} opacity={0.9} />
      </g>
      <path d={md} fill="none" stroke="#6d7f86" strokeWidth={1.6} />
      <path d="M-86,0H86M-74,-44H74M-74,44H74" stroke="#6d7f86" strokeWidth={1.6} />
      <path d="M-104,40A108,108 0 0 0 104,40" fill="none" stroke={C.gold} strokeWidth={8} transform="rotate(-20)" />
    </g>
  );
};

/** Scene 1 — 時間是 1729 年 */
export const YearScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const b = out3(P(t, 0, 0.5));
  const props = out3(P(t, 0.7, 1.25));
  return (
    <Paper defs={<clipPath id="globeClip"><circle r={86} /></clipPath>}>
      <g transform={camera(1 + 0.06 * io(P(t, 0, 3.5)))}>
        <Laurel t={t} />
        <Laurel t={t} mirror />
        {/* ribbon tails */}
        <g opacity={P(t, 0.3, 0.55)}>
          <path d="M470,395L300,405L350,480L300,560L470,548Z" fill="#efcf98" stroke={C.ink} strokeWidth={3} />
          <path d="M1450,395L1620,405L1570,480L1620,560L1450,548Z" fill="#efcf98" stroke={C.ink} strokeWidth={3} />
          <path d="M470,520L430,548L470,548ZM1450,520L1490,548L1450,548Z" fill="#c9a06a" stroke={C.ink} strokeWidth={2.5} />
        </g>
        {/* ribbon unfurls from the centre */}
        <g transform={`translate(960 425) scale(${lerp(0.05, 1, b)} 1) translate(-960 -425)`} opacity={Math.min(1, b * 4)}>
          <path d="M430,330C700,290 1220,290 1490,330L1490,520C1220,480 700,480 430,520Z" fill="#f6deb0" stroke={C.ink} strokeWidth={3.5} />
          <path d="M430,330C700,290 1220,290 1490,330L1490,360C1220,322 700,322 430,360Z" fill="url(#hatch)" opacity={0.35} />
          <path d="M430,490C700,450 1220,450 1490,490L1490,520C1220,480 700,480 430,520Z" fill="#e4b977" opacity={0.6} />
        </g>
        {'1729'.split('').map((d, i) => {
          const p = pop(720 + i * 160, 500, P(t, 0.35 + i * 0.14, 0.75 + i * 0.14));
          return (
            <g key={i} {...p}>
              <text textAnchor="middle" fontSize={250} fontFamily={FONT.fell} fill="#5a4636" stroke={C.ink} strokeWidth={3}>{d}</text>
              <text textAnchor="middle" fontSize={250} fontFamily={FONT.fell} fill="url(#hatch)" opacity={0.5}>{d}</text>
            </g>
          );
        })}
        <g transform={`translate(0 ${f((1 - props) * 180)})`} opacity={props}>
          <Globe t={t} />
          <g transform="translate(1060 790)">
            <rect x={-130} y={40} width={260} height={44} rx={5} fill="#7d5a8c" stroke={C.ink} strokeWidth={3} />
            <rect x={-116} y={-4} width={240} height={44} rx={5} fill={C.blue} stroke={C.ink} strokeWidth={3} />
            <rect x={-104} y={-44} width={214} height={40} rx={5} fill="#a5643f" stroke={C.ink} strokeWidth={3} />
            <path d="M-90,40V84M-80,-4V40M90,-44V-4M100,40V84" stroke={C.gold} strokeWidth={4} />
            <rect x={-130} y={40} width={260} height={44} rx={5} fill="url(#hatch)" opacity={0.3} />
          </g>
        </g>
      </g>
    </Paper>
  );
};
