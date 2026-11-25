import React from "react";
import faces from "../faces.json";

export type Expr =
  | "smile"
  | "happy"
  | "laugh"
  | "angry"
  | "shout"
  | "strain"
  | "tired"
  | "sleep"
  | "sad"
  | "disappointed"
  | "surprised"
  | "love"
  | "shy"
  | "determined"
  | "dizzy"
  | "giggle"
  | "nervous"
  | "proud";

export type FaceSpec = {
  e: Expr;
  look?: number; // -1 (left) .. 1 (right): gaze + slight head-turn
  lookY?: number; // -1 up .. 1 down
  blush?: number; // extra blush 0..1
  tear?: boolean;
  talk?: number; // 0..1 mouth open amount (lip-flap)
};

export const hasFace = (name: string) => name in faces;

const INKF = "#3b2414";
const MOUTH = "#b8453c";
const TONGUE = "#f08c8c";

type Pt = [number, number];

export const Face: React.FC<{ name: string; spec: FaceSpec }> = ({ name, spec }) => {
  const F = (faces as unknown as Record<string, { w: number; h: number; eyeL: Pt; eyeR: Pt; mouth: Pt }>)[name];
  if (!F) return null;
  const { e, look = 0, lookY = 0, blush = 0, tear = false, talk = 0 } = spec;
  const d = Math.hypot(F.eyeR[0] - F.eyeL[0], F.eyeR[1] - F.eyeL[1]);
  const turn = look * d * 0.12;
  const eL: Pt = [F.eyeL[0] + turn, F.eyeL[1] + lookY * d * 0.04];
  const eR: Pt = [F.eyeR[0] + turn, F.eyeR[1] + lookY * d * 0.04];
  const m: Pt = [F.mouth[0] + turn * 1.1, F.mouth[1] + d * 0.02];
  const sw = d * 0.06;
  const px = look * d * 0.06;
  const py = lookY * d * 0.05;

  const stroke = { stroke: INKF, strokeWidth: sw, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, fill: "none" };

  // ---------- eyes
  const dot = (c: Pt, s = 1, hl = true, squash = 1) => (
    <g>
      <ellipse cx={c[0] + px} cy={c[1] + py} rx={d * 0.1 * s} ry={d * 0.145 * s * squash} fill={INKF} />
      {hl ? <circle cx={c[0] + px - d * 0.025 * s} cy={c[1] + py - d * 0.045 * s * squash} r={d * 0.032 * s} fill="#fff" /> : null}
    </g>
  );
  const arcUp = (c: Pt) => <path d={`M${c[0] - d * 0.12} ${c[1] + d * 0.04} Q ${c[0]} ${c[1] - d * 0.12} ${c[0] + d * 0.12} ${c[1] + d * 0.04}`} {...stroke} />;
  const arcDown = (c: Pt) => <path d={`M${c[0] - d * 0.12} ${c[1] - d * 0.02} Q ${c[0]} ${c[1] + d * 0.1} ${c[0] + d * 0.12} ${c[1] - d * 0.02}`} {...stroke} />;
  const chevron = (c: Pt, dir: 1 | -1) => (
    <path
      d={`M${c[0] - dir * d * 0.1} ${c[1] - d * 0.09} L ${c[0] + dir * d * 0.08} ${c[1]} L ${c[0] - dir * d * 0.1} ${c[1] + d * 0.09}`}
      {...stroke}
      strokeWidth={sw * 1.1}
    />
  );
  const halfLid = (c: Pt, droop = 0) => (
    <g>
      <clipPath id={`lid-${name}-${c[0].toFixed(0)}`}>
        <rect x={c[0] - d * 0.2} y={c[1] - d * 0.01} width={d * 0.4} height={d * 0.3} />
      </clipPath>
      <ellipse cx={c[0] + px} cy={c[1] + py * 0.5} rx={d * 0.085} ry={d * 0.115} fill={INKF} clipPath={`url(#lid-${name}-${c[0].toFixed(0)})`} />
      <path d={`M${c[0] - d * 0.13} ${c[1] - d * 0.01 + droop * d * 0.03} L ${c[0] + d * 0.13} ${c[1] - d * 0.01 - droop * d * 0.03}`} {...stroke} />
    </g>
  );
  const heart = (c: Pt) => (
    <path
      transform={`translate(${c[0]} ${c[1]}) scale(${d / 220})`}
      d="M0 22 C -24 6 -26 -14 -12 -20 C -4 -23 0 -16 0 -12 C 0 -16 4 -23 12 -20 C 26 -14 24 6 0 22 Z"
      fill="#e8505f"
      stroke={INKF}
      strokeWidth={4}
    />
  );
  const spiral = (c: Pt) => (
    <path
      d={`M${c[0]} ${c[1]} m ${d * 0.02} 0 a ${d * 0.02} ${d * 0.02} 0 1 0 ${-d * 0.04} 0 a ${d * 0.05} ${d * 0.05} 0 1 0 ${d * 0.09} 0 a ${d * 0.08} ${d * 0.08} 0 1 0 ${-d * 0.15} 0`}
      {...stroke}
      strokeWidth={sw * 0.8}
    />
  );

  // ---------- brows (a = angle: +angry inward-down, -worried inward-up)
  const brows = (a: number, lift = 0) => {
    const y = -d * (0.27 + lift);
    const mk = (c: Pt, side: -1 | 1) => {
      const inner: Pt = [c[0] - side * d * 0.09, c[1] + y + a * d * 0.07];
      const outer: Pt = [c[0] + side * d * 0.11, c[1] + y - a * d * 0.07];
      return <path d={`M${inner[0]} ${inner[1]} L ${outer[0]} ${outer[1]}`} {...stroke} strokeWidth={sw * 1.15} />;
    };
    return (
      <>
        {mk(eL, -1)}
        {mk(eR, 1)}
      </>
    );
  };

  // ---------- mouths
  const W = d * 0.42;
  const smileM = (k = 1) => <path d={`M${m[0] - W * 0.4 * k} ${m[1] - d * 0.02} Q ${m[0]} ${m[1] + d * 0.12 * k} ${m[0] + W * 0.4 * k} ${m[1] - d * 0.02}`} {...stroke} />;
  const frownM = (k = 1) => <path d={`M${m[0] - W * 0.35 * k} ${m[1] + d * 0.06} Q ${m[0]} ${m[1] - d * 0.06 * k} ${m[0] + W * 0.35 * k} ${m[1] + d * 0.06}`} {...stroke} />;
  const openD = (k = 1) => (
    <g>
      <path
        d={`M${m[0] - W * 0.5 * k} ${m[1] - d * 0.04} Q ${m[0]} ${m[1] - d * 0.01} ${m[0] + W * 0.5 * k} ${m[1] - d * 0.04} Q ${m[0] + W * 0.35 * k} ${m[1] + d * 0.24 * k} ${m[0]} ${m[1] + d * 0.25 * k} Q ${m[0] - W * 0.35 * k} ${m[1] + d * 0.24 * k} ${m[0] - W * 0.5 * k} ${m[1] - d * 0.04} Z`}
        fill={MOUTH}
        stroke={INKF}
        strokeWidth={sw * 0.8}
        strokeLinejoin="round"
      />
      <ellipse cx={m[0]} cy={m[1] + d * 0.16 * k} rx={W * 0.25 * k} ry={d * 0.06 * k} fill={TONGUE} />
    </g>
  );
  const oM = (k = 1) => <ellipse cx={m[0]} cy={m[1] + d * 0.04} rx={d * 0.07 * k} ry={d * 0.1 * k} fill={MOUTH} stroke={INKF} strokeWidth={sw * 0.8} />;
  const shoutM = (k = 1) => (
    <path
      d={`M${m[0] - W * 0.4 * k} ${m[1] + d * 0.12 * k} Q ${m[0]} ${m[1] - d * 0.1 * k} ${m[0] + W * 0.4 * k} ${m[1] + d * 0.12 * k} Q ${m[0]} ${m[1] + d * 0.2 * k} ${m[0] - W * 0.4 * k} ${m[1] + d * 0.12 * k} Z`}
      fill={MOUTH}
      stroke={INKF}
      strokeWidth={sw * 0.8}
      strokeLinejoin="round"
    />
  );
  const teethM = () => (
    <g>
      <rect x={m[0] - W * 0.42} y={m[1] - d * 0.04} width={W * 0.84} height={d * 0.13} rx={d * 0.05} fill="#fff" stroke={INKF} strokeWidth={sw * 0.8} />
      <path d={`M${m[0] - W * 0.42} ${m[1] + d * 0.025} L ${m[0] + W * 0.42} ${m[1] + d * 0.025} M ${m[0] - W * 0.14} ${m[1] - d * 0.04} L ${m[0] - W * 0.14} ${m[1] + d * 0.09} M ${m[0] + W * 0.14} ${m[1] - d * 0.04} L ${m[0] + W * 0.14} ${m[1] + d * 0.09}`} stroke={INKF} strokeWidth={sw * 0.5} />
    </g>
  );
  const wavyM = () => (
    <path
      d={`M${m[0] - W * 0.4} ${m[1] + d * 0.03} q ${W * 0.1} ${-d * 0.05} ${W * 0.2} 0 t ${W * 0.2} 0 t ${W * 0.2} 0 t ${W * 0.2} 0`}
      {...stroke}
      strokeWidth={sw * 0.85}
    />
  );
  const catM = () => (
    <path d={`M${m[0] - W * 0.36} ${m[1]} q ${W * 0.18} ${d * 0.1} ${W * 0.36} 0 q ${W * 0.18} ${d * 0.1} ${W * 0.36} 0`} {...stroke} />
  );

  let eyes: React.ReactNode = null;
  let mouth: React.ReactNode = null;
  let br: React.ReactNode = null;
  let extra: React.ReactNode = null;

  switch (e) {
    case "smile":
      eyes = [dot(eL), dot(eR)];
      mouth = smileM();
      break;
    case "happy":
      eyes = [arcUp(eL), arcUp(eR)];
      mouth = openD(0.8);
      break;
    case "laugh":
      eyes = [arcUp(eL), arcUp(eR)];
      mouth = openD(1.15);
      br = brows(-0.4, 0.06);
      break;
    case "proud":
      eyes = [arcUp(eL), arcUp(eR)];
      mouth = openD(0.95);
      br = brows(0.3, 0.06);
      break;
    case "angry":
      eyes = [dot(eL, 0.95, true, 0.85), dot(eR, 0.95, true, 0.85)];
      br = brows(1);
      mouth = frownM(1.1);
      break;
    case "shout":
      eyes = [dot(eL, 0.95, true, 0.85), dot(eR, 0.95, true, 0.85)];
      br = brows(1.1);
      mouth = shoutM(1.2);
      break;
    case "strain":
      eyes = [chevron(eL, 1), chevron(eR, -1)];
      br = brows(0.9);
      mouth = teethM();
      break;
    case "tired":
      eyes = [halfLid(eL, -1), halfLid(eR, 1)];
      br = brows(-0.5, -0.02);
      mouth = wavyM();
      extra = (
        <g opacity={0.5}>
          {arcDown([eL[0], eL[1] + d * 0.1])}
          {arcDown([eR[0], eR[1] + d * 0.1])}
        </g>
      );
      break;
    case "sleep":
      eyes = [arcDown(eL), arcDown(eR)];
      mouth = oM(0.6);
      break;
    case "sad":
      eyes = [dot(eL, 1.05), dot(eR, 1.05)];
      br = brows(-1);
      mouth = frownM();
      break;
    case "disappointed":
      eyes = [halfLid(eL, -1), halfLid(eR, 1)];
      br = brows(-1.1);
      mouth = frownM(0.8);
      break;
    case "surprised":
      eyes = [dot(eL, 1.25), dot(eR, 1.25)];
      br = brows(-0.2, 0.12);
      mouth = oM(1.2 + talk * 0.3);
      break;
    case "love":
      eyes = [heart(eL), heart(eR)];
      mouth = openD(0.75);
      break;
    case "shy":
      eyes = [arcUp(eL), arcUp(eR)];
      mouth = wavyM();
      br = brows(-0.6, 0.02);
      break;
    case "determined":
      eyes = [dot(eL), dot(eR)];
      br = brows(0.75);
      mouth = talk > 0 ? shoutM(0.6 + talk * 0.6) : smileM(0.7);
      break;
    case "dizzy":
      eyes = [spiral(eL), spiral(eR)];
      mouth = wavyM();
      break;
    case "giggle":
      eyes = [arcUp(eL), arcUp(eR)];
      mouth = catM();
      break;
    case "nervous":
      eyes = [dot(eL, 0.85), dot(eR, 0.85)];
      br = brows(-0.8, 0.04);
      mouth = talk > 0 ? oM(0.6 + talk * 0.6) : wavyM();
      break;
  }

  // generic talking override for open-mouth friendly expressions
  if (talk > 0 && (e === "smile" || e === "angry" || e === "sad")) {
    mouth = e === "angry" ? shoutM(0.6 + talk * 0.6) : e === "sad" ? oM(0.5 + talk * 0.5) : openD(0.4 + talk * 0.5);
  }

  const blushN = Math.max(blush, e === "shy" || e === "love" ? 0.8 : 0);
  return (
    <g>
      {blushN > 0 ? (
        <g opacity={blushN}>
          {[eL, eR].map((c, i) => (
            <g key={i}>
              <ellipse cx={c[0] + (i ? 1 : -1) * d * 0.12} cy={c[1] + d * 0.2} rx={d * 0.15} ry={d * 0.08} fill="#f08a96" opacity={0.6} />
              <path
                d={`M${c[0] + (i ? 1 : -1) * d * 0.12 - d * 0.08} ${c[1] + d * 0.24} l ${d * 0.04} ${-d * 0.08} m ${d * 0.03} ${d * 0.08} l ${d * 0.04} ${-d * 0.08} m ${d * 0.03} ${d * 0.08} l ${d * 0.04} ${-d * 0.08}`}
                stroke="#d4566a"
                strokeWidth={sw * 0.6}
                strokeLinecap="round"
              />
            </g>
          ))}
        </g>
      ) : null}
      {extra}
      {br}
      {eyes}
      {mouth}
      {tear ? (
        <path
          d={`M${eR[0] + d * 0.05} ${eR[1] + d * 0.1} c ${d * 0.04} ${d * 0.08} ${d * 0.07} ${d * 0.11} ${d * 0.07} ${d * 0.15} a ${d * 0.07} ${d * 0.07} 0 0 1 ${-d * 0.14} 0 c 0 ${-d * 0.04} ${d * 0.03} ${-d * 0.07} ${d * 0.07} ${-d * 0.15} Z`}
          fill="#9fd3f0"
          stroke="#4d8fb8"
          strokeWidth={sw * 0.5}
        />
      ) : null}
    </g>
  );
};
