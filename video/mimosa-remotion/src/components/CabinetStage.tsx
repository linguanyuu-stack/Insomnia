import React from 'react';
import { Raw } from './Paper';
import { clamp, f, io, lerp, out3, P, pop } from '../lib/anim';
import { armReach, bust, moonSVG, pocketWatch, pottedPlant, scrollLabel, sunSVG } from '../lib/draw';
import { C, FONT } from '../lib/theme';

const MAIRAN = bust() + armReach(536, 488);
const LBL_OPEN = scrollLabel(0, 0, 360, 80, '葉片張開', 46);
const LBL_CLOSED = scrollLabel(0, 0, 360, 80, '葉片合起來', 46);
const STAMP = `<rect x="-120" y="-40" width="240" height="80" rx="10" fill="${C.cream}" stroke="${C.red}" stroke-width="5" transform="rotate(-6)"/><text y="16" text-anchor="middle" font-size="48" font-family="${FONT.kai}" font-weight="700" fill="${C.red}" transform="rotate(-6)" letter-spacing="6">不透光</text>`;

/** Key moments of the cabinet experiment, in seconds from the start of scene 5 */
export const CAB = {
  slide: [0.8, 2.0],
  door: [2.0, 2.6],
  reveal: [2.9, 3.3],
  cycles: [3.3, 9.3], // two full days outside the cabinet
};

/** night amount 0..1 outside the cabinet at time lt (sharpened cosine, 2 cycles) */
export const nightAt = (lt: number) => {
  if (lt < CAB.cycles[0]) return 0;
  const c = P(lt, CAB.cycles[0], CAB.cycles[1]);
  const n = 0.5 - 0.5 * Math.cos(c * Math.PI * 4);
  return clamp((n - 0.5) * 3 + 0.5);
};

/** The dark-cabinet composition as a pure function of time (shared by scenes 5 and 6) */
export const CabinetStage: React.FC<{ lt: number; clock: number }> = ({ lt, clock }) => {
  const mp = out3(P(lt, 0, 0.6));
  const slide = io(P(lt, CAB.slide[0], CAB.slide[1]));
  const px = lerp(750, 1190, slide);
  const py = lerp(880, 826, slide) - Math.sin(slide * Math.PI) * 50;
  const night = nightAt(lt);
  const k = 1 - night;
  // door hinged on the right edge, swinging shut
  const th = (lerp(118, 0, io(P(lt, CAB.door[0], CAB.door[1]))) * Math.PI) / 180;
  const L0 = 1012, R0 = 1368, T0 = 318, B0 = 830, w = R0 - L0;
  const fx = R0 - w * Math.cos(th);
  const ex = Math.sin(th) * 34;
  const ix1 = lerp(R0, fx, 0.12);
  const ix2 = lerp(R0, fx, 0.88);
  const xr = P(lt, CAB.reveal[0], CAB.reveal[1]); // door becomes an x-ray outline
  const show = P(lt, CAB.reveal[0] - 0.1, CAB.reveal[1]);
  const qx = 530 + Math.sin(lt * 9) * 14 + (lt % 1) * 30;
  const qy = 866 + Math.sin(lt * 23) * 3;
  // hands race through the hours once the days start passing
  const hr = lt < CAB.cycles[0] ? clock * 30 : 45 + P(lt, CAB.cycles[0], CAB.cycles[1]) * 1440 + (clock - lt) * 30;
  return (
    <g>
      {/* outside sky: day / night */}
      <g opacity={show}>
        <text x={1190} y={92} textAnchor="middle" fontSize={30} fontFamily={FONT.kai} fill={C.muted}>櫃子外面</text>
        <rect x={990} y={110} width={400} height={130} rx={16} fill="#f8e6a8" stroke={C.ink} strokeWidth={3} />
        <rect x={990} y={110} width={400} height={130} rx={16} fill={C.night} stroke={C.ink} strokeWidth={3} opacity={night} />
        <rect x={990} y={110} width={400} height={130} rx={16} fill="url(#hatchBlue)" opacity={night * 0.5} />
        <Raw svg={night > 0.5 ? moonSVG(40) : sunSVG(32, lt)} transform={`translate(1070 175) rotate(${night > 0.5 ? -15 : 0})`} />
        <text x={1250} y={190} textAnchor="middle" fontSize={50} fontFamily={FONT.kai} fontWeight={700} fill={night > 0.5 ? C.cream : C.ink} letterSpacing={6}>
          {night > 0.5 ? '晚上' : '白天'}
        </text>
      </g>
      {/* cabinet */}
      <rect x={960} y={270} width={460} height={610} rx={6} fill={C.wood} stroke={C.ink} strokeWidth={4} />
      <rect x={960} y={270} width={460} height={610} rx={6} fill="url(#hatch)" opacity={0.25} />
      <path d="M940,270H1440L1420,246H960Z" fill={C.woodD} stroke={C.ink} strokeWidth={3.5} />
      <rect x={1012} y={318} width={356} height={512} fill="#2b2633" stroke={C.ink} strokeWidth={3} />
      <rect x={1012} y={318} width={356} height={512} fill="url(#hatchDark)" opacity={0.7} />
      <rect x={980} y={880} width={40} height={34} fill={C.woodD} stroke={C.ink} strokeWidth={3} />
      <rect x={1360} y={880} width={40} height={34} fill={C.woodD} stroke={C.ink} strokeWidth={3} />
      <Raw svg={pottedPlant(k)} transform={`translate(${f(px)} ${f(py)}) scale(1.15)`} />
      <rect x={1012} y={318} width={356} height={512} fill="#1c1824" opacity={0.12 * xr} />
      <g>
        <path d={`M${R0},${T0}L${f(fx)},${f(T0 - ex)}L${f(fx)},${f(B0 + ex)}L${R0},${B0}Z`} fill="#a87245" fillOpacity={1 - xr * 0.9} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" strokeDasharray={xr > 0.5 ? '14 10' : undefined} />
        <path
          d={`M${f(ix1)},${f(T0 + 30 - ex * 0.12)}L${f(ix2)},${f(T0 + 30 - ex * 0.88)}L${f(ix2)},${f(560 - ex * 0.1)}L${f(ix1)},560ZM${f(ix1)},600L${f(ix2)},600L${f(ix2)},${f(B0 - 30 + ex * 0.88)}L${f(ix1)},${f(B0 - 30 + ex * 0.12)}Z`}
          fill="none"
          stroke={C.woodD}
          strokeWidth={4}
          opacity={1 - xr * 0.7}
        />
        <circle cx={f(lerp(R0, fx, 0.9))} cy={574} r={9} fill={C.gold} stroke={C.ink} strokeWidth={2.5} />
      </g>
      <Raw svg={STAMP} {...pop(1190, 300, P(lt, CAB.door[1] - 0.1, CAB.door[1] + 0.25))} />
      {/* de Mairan at his desk, writing */}
      <Raw svg={MAIRAN} transform={`translate(${f(150 - (1 - mp) * 140)} 545) scale(.72)`} opacity={mp} />
      <g transform={`translate(${f(qx)} ${f(qy)}) rotate(-38)`} opacity={mp}>
        <path d="M0,0C20,-30 60,-70 120,-90C90,-50 50,-18 0,0Z" fill="#fdfaf2" stroke={C.ink} strokeWidth={2.5} />
        <path d="M0,0L100,-80" stroke={C.ink} strokeWidth={1.5} />
      </g>
      <path d="M40,880H930V960H40Z" fill={C.wood} stroke={C.ink} strokeWidth={4} />
      <path d="M40,880H930V900H40Z" fill="#b57c48" stroke={C.ink} strokeWidth={3} />
      <path d="M380,876C430,850 500,850 545,872C590,850 660,850 710,876L705,884H385Z" fill="#fbf5e6" stroke={C.ink} strokeWidth={3} />
      <path d="M545,872V884M410,868q50,-14 110,-2M420,858q50,-12 100,0M570,866q50,-14 110,0M575,856q45,-12 95,0" fill="none" stroke="#9a8f82" strokeWidth={2} />
      <path d="M800,880h60l-6,-46h-48Z" fill="#3a3340" stroke={C.ink} strokeWidth={3} />
      {/* pocket watch + what the leaves do inside */}
      <Raw svg={pocketWatch(110, hr, hr * 6)} {...pop(1660, 400, P(lt, CAB.reveal[0], CAB.reveal[1] + 0.1))} />
      <g transform={`translate(0 ${f((1 - show) * 30)})`} opacity={show}>
        <text x={1660} y={640} textAnchor="middle" fontSize={34} fontFamily={FONT.kai} fill={C.muted}>櫃子裡的含羞草</text>
        <Raw svg={k > 0.5 ? LBL_OPEN : LBL_CLOSED} transform="translate(1660 730)" />
      </g>
    </g>
  );
};
