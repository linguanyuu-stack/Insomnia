import React from 'react';
import { Raw } from './Paper';
import { back, f, lerp } from '../lib/anim';
import { cloud, moonSVG, plant, PlantSpec, scrollLabel, star, sunSVG } from '../lib/draw';
import { C, FONT } from '../lib/theme';

export const SPEC_L: PlantSpec = {
  stem: [[230, 960], [320, 790], [420, 650], [545, 510], [680, 400], [790, 330]],
  fronds: [[335, 765, -105, 260], [420, 650, -8, 270], [500, 560, -100, 250], [600, 465, 8, 250], [690, 392, -72, 210], [780, 336, 18, 170]],
  flowers: [[205, 560, 42, 330, 775], [380, 420, 36, 470, 600]],
  buds: [[790, 330, -40]],
};
const DX = 1060;
const DY = 10;
export const SPEC_R: PlantSpec = {
  stem: SPEC_L.stem.map(([x, y]) => [x + DX, y + DY]),
  fronds: SPEC_L.fronds.map(([x, y, a, l]) => [x + DX, y + DY, a, l * 0.92]),
  flowers: SPEC_L.flowers!.map(([x, y, r, fx, fy]) => [x + DX, y + DY, r, fx + DX, fy + DY]),
  buds: SPEC_L.buds!.map(([x, y, a]) => [x + DX, y + DY, a]),
};

const NIGHT_SHAPE = 'M1060,0H1920V960H1000C1060,700 990,350 1060,0Z';
const STARS: [number, number, number][] = [[1240, 90, 14], [1380, 240, 10], [1860, 110, 16], [1820, 330, 11], [1290, 380, 9], [1520, 70, 9], [1760, 470, 8]];

const LBL_DAY = scrollLabel(0, 0, 320, 70, '白天（受光）', 40);
const LBL_NIGHT = scrollLabel(0, 0, 320, 70, '晚上（無光）', 40);
const underline = (txt: string, col: string) =>
  `<text y="0" text-anchor="middle" font-size="50" font-family="${FONT.kai}" font-weight="700" fill="${C.ink}" letter-spacing="6">${txt}</text>` +
  `<path d="M-115,18C-40,12 40,12 115,16" stroke="${col}" stroke-width="9" stroke-linecap="round" fill="none" opacity=".85"/>` +
  `<path d="M135,-30l26,-14M140,-8h30M135,14l26,14" stroke="${col}" stroke-width="5" stroke-linecap="round"/>`;
const OPEN = underline('葉片張開', '#f0c23e');
const CLOSED = underline('葉片合起來', '#6f86c9');

type Pop = { transform: string; opacity: number };
export type StageState = {
  t: number; // seconds, for idle motion
  grow: number; // left plant growth 0..1
  growR: number; // right plant growth 0..1
  night: number; // 0..1 how far night has spread on the right half
  moon: number; // 0..1 moon rise
  sun: number; // 0..1 sun rise
  kRight: number; // right plant leaf openness
  plantsOpacity: number;
  title: Pop;
  arrows: Pop;
  labels: [Pop, Pop, Pop, Pop];
};

/** The day / night mimosa composition shared by scenes 3 and 4 */
export const MimosaStage: React.FC<{ s: StageState; clipId: string }> = ({ s, clipId }) => {
  let stars = '';
  STARS.forEach(([x, y, r], i) => (stars += star(x, y, r * (1 + 0.25 * Math.sin(s.t * 5 + i * 2)), s.t * 20)));
  return (
    <g>
      <defs>
        <clipPath id={clipId}>
          <rect x={f(lerp(1920, 960, s.night))} y={0} width={1100} height={1080} />
        </clipPath>
      </defs>
      <path d="M0,0H900C860,300 900,600 860,960H0Z" fill="#f8e3a6" opacity={0.45} />
      <g clipPath={`url(#${clipId})`}>
        <path d={NIGHT_SHAPE} fill={C.night} opacity={0.55} />
        <path d={NIGHT_SHAPE} fill="url(#hatchBlue)" opacity={0.55} />
        <Raw svg={stars} />
      </g>
      <Raw svg={sunSVG(62, s.t)} transform={`translate(200 ${f(lerp(380, 175, s.sun))})`} />
      <Raw svg={cloud(520 + s.t * 14, 150, 0.9)} />
      <Raw svg={moonSVG(62)} transform={`translate(1600 ${f(lerp(420, 165, s.moon))}) rotate(-15)`} opacity={Math.min(1, s.moon * 2)} />
      <g opacity={s.plantsOpacity}>
        <Raw svg={plant(SPEC_L, 1, s.grow)} />
        <Raw svg={plant(SPEC_R, s.kRight, s.growR)} />
      </g>
      <g transform={s.title.transform} opacity={s.title.opacity}>
        <path d="M-190,-62H190Q210,-62 206,-40Q226,0 206,40Q210,62 190,62H-190Q-210,62 -206,40Q-226,0 -206,-40Q-210,-62 -190,-62Z" fill={C.cream} stroke={C.ink} strokeWidth={3.5} />
        <path d="M-222,-10q-14,10 0,22M222,-10q14,10 0,22" fill="none" stroke={C.ink} strokeWidth={3} />
        <text y={4} textAnchor="middle" fontSize={64} fontFamily={FONT.kai} fontWeight={700} fill={C.ink} letterSpacing={10}>含羞草</text>
        <text y={46} textAnchor="middle" fontSize={30} fontFamily={FONT.fell} fontStyle="italic" fill={C.ink}>Mimosa pudica</text>
        <path transform="translate(232 -40) rotate(30)" d="M0,0C10,-10 30,-10 40,0C30,8 10,8 0,0Z" fill={C.leaf} stroke={C.leafD} strokeWidth={2} />
      </g>
      <g transform={s.arrows.transform} opacity={s.arrows.opacity}>
        <path d="M-60,-14C-30,-44 30,-44 60,-14M48,-26L60,-14 42,-8" fill="none" stroke={C.ink} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" />
        <path d="M60,14C30,44 -30,44 -60,14M-48,26L-60,14 -42,8" fill="none" stroke={C.ink} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" />
      </g>
      <Raw svg={LBL_DAY} {...s.labels[0]} />
      <Raw svg={OPEN} {...s.labels[1]} />
      <Raw svg={LBL_NIGHT} {...s.labels[2]} />
      <Raw svg={CLOSED} {...s.labels[3]} />
    </g>
  );
};

export const settled = (x: number, y: number): Pop => ({ transform: `translate(${x} ${y}) scale(${back(1)})`, opacity: 1 });
