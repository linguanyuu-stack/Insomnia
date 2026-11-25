import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { INK, ROUND, wave, Wash } from "./kit";

const S = { stroke: INK, strokeWidth: 4, strokeLinejoin: "round" as const, strokeLinecap: "round" as const };

export const Rose: React.FC<{ x: number; y: number; s?: number; rot?: number; opacity?: number }> = ({
  x,
  y,
  s = 1,
  rot = 0,
  opacity = 1,
}) => (
  <svg
    width={120}
    height={220}
    viewBox="-60 -60 120 220"
    style={{ position: "absolute", left: x - 60, top: y - 60, overflow: "visible", opacity, transform: `rotate(${rot}deg) scale(${s})`, transformOrigin: "50% 27%" }}
  >
    <path d="M0 20 C 4 70 -6 110 2 150" fill="none" {...S} stroke="#4f7a3a" strokeWidth={6} />
    <path d="M1 80 C 20 62 40 66 44 74 C 32 86 14 88 1 80 Z" fill="#8fbf6a" {...S} strokeWidth={3} />
    <path d="M0 108 C -18 92 -38 96 -42 104 C -30 116 -12 116 0 108 Z" fill="#8fbf6a" {...S} strokeWidth={3} />
    <path d="M-34 0 C -40 -30 -14 -48 0 -40 C 14 -48 40 -30 34 0 C 30 26 -30 26 -34 0 Z" fill="#e0475f" {...S} />
    <path d="M-18 -8 C -20 -26 -4 -34 4 -26 C 16 -30 22 -14 14 -4 C 6 6 -12 6 -18 -8 Z" fill="#c92f4a" {...S} strokeWidth={3} />
    <path d="M-6 -14 C -2 -22 8 -20 6 -12" fill="none" {...S} strokeWidth={3} />
    <path d="M-34 0 C -20 14 20 14 34 0 C 30 26 -30 26 -34 0 Z" fill="#d23a54" {...S} strokeWidth={3} />
  </svg>
);

export const ChefHat: React.FC<{ x: number; y: number; w?: number; rot?: number }> = ({ x, y, w = 120, rot = 0 }) => (
  <svg
    width={w}
    height={w}
    viewBox="0 0 120 120"
    style={{ position: "absolute", left: x - w / 2, top: y - w, transform: `rotate(${rot}deg)`, transformOrigin: "50% 100%", overflow: "visible" }}
  >
    <path
      d="M24 92 L 22 62 C 4 60 0 34 18 28 C 22 10 44 6 54 18 C 64 4 90 8 92 26 C 114 26 118 56 98 62 L 96 92 Z"
      fill="#fffdf8"
      {...S}
    />
    <path d="M24 92 L 96 92 L 97 112 L 23 112 Z" fill="#fffdf8" {...S} />
    <path d="M44 64 L 46 90 M 76 64 L 74 90" fill="none" {...S} strokeWidth={3} opacity={0.5} />
  </svg>
);

export const Bowl: React.FC<{ x: number; y: number; s?: number; rot?: number; steam?: boolean; fill?: number }> = ({
  x,
  y,
  s = 1,
  rot = 0,
  steam = true,
  fill = 1,
}) => {
  const f = useCurrentFrame();
  return (
    <svg
      width={160}
      height={160}
      viewBox="-80 -100 160 160"
      style={{ position: "absolute", left: x - 80, top: y - 100, transform: `rotate(${rot}deg) scale(${s})`, transformOrigin: "50% 62%", overflow: "visible" }}
    >
      {steam
        ? [0, 1, 2].map((i) => (
            <path
              key={i}
              d={`M${-24 + i * 24} -20 C ${-34 + i * 24 + wave(f, 30, 8, i * 10)} -45, ${-14 + i * 24} -60, ${-24 + i * 24 + wave(f, 26, 10, i * 7)} -88`}
              fill="none"
              stroke="#e9dccb"
              strokeWidth={6}
              strokeLinecap="round"
              opacity={0.8}
            />
          ))
        : null}
      <ellipse cx={0} cy={-8} rx={62} ry={14} fill="#fbf4e6" {...S} />
      {fill > 0 ? <ellipse cx={0} cy={-8} rx={54 * fill} ry={10 * fill} fill="#d9a45a" /> : null}
      <path d="M-62 -8 C -60 34 -30 50 0 50 C 30 50 60 34 62 -8 C 40 4 -40 4 -62 -8 Z" fill="#fbf4e6" {...S} />
      <path d="M-20 30 C -14 22 -6 22 0 30 C 6 22 14 22 20 30" fill="none" stroke="#e98aa0" strokeWidth={4} />
      <path d="M-36 14 C -30 18 -24 18 -18 14 M 18 14 C 24 18 30 18 36 14" fill="none" stroke="#7aa35b" strokeWidth={4} />
    </svg>
  );
};

export const Lightbulb: React.FC<{ x: number; y: number; s?: number; glow?: number }> = ({ x, y, s = 1, glow = 1 }) => (
  <svg width={120} height={160} viewBox="-60 -80 120 160" style={{ position: "absolute", left: x - 60, top: y - 80, transform: `scale(${s})`, overflow: "visible" }}>
    <circle cx={0} cy={-14} r={70} fill="#ffe27a" opacity={0.35 * glow} />
    <path d="M0 -60 C 32 -60 44 -34 36 -12 C 30 4 20 10 18 28 L -18 28 C -20 10 -30 4 -36 -12 C -44 -34 -32 -60 0 -60 Z" fill="#ffe680" {...S} />
    <path d="M-16 34 L 16 34 M -14 44 L 14 44 M -8 54 L 8 54" {...S} />
    <path d="M-10 18 L -4 -10 L 4 0 L 10 -18" fill="none" {...S} strokeWidth={3} stroke="#c98a2a" />
  </svg>
);

/** Grey damp cloud with "濕氣" label */
export const DampCloud: React.FC<{ x: number; y: number; s?: number; opacity?: number; label?: boolean }> = ({
  x,
  y,
  s = 1,
  opacity = 1,
  label = true,
}) => {
  const f = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: x, top: y, transform: `translate(-50%,-50%) scale(${s})`, opacity }}>
      <svg width={360} height={220} viewBox="-180 -110 360 220" style={{ overflow: "visible" }}>
        <path
          d="M-140 40 C -180 40 -180 -20 -130 -24 C -140 -80 -60 -96 -30 -60 C -10 -110 80 -100 84 -46 C 140 -60 170 0 136 30 C 160 60 120 80 90 64 C 60 90 -40 92 -70 64 C -100 84 -150 72 -140 40 Z"
          fill="#a9b7bd"
          {...S}
          stroke="#56656c"
        />
        <path d="M-50 10 C -46 2 -38 2 -34 10 M 30 10 C 34 2 42 2 46 10" fill="none" stroke="#56656c" strokeWidth={4} strokeLinecap="round" />
        <path d="M-12 34 C -4 26 4 26 12 34" fill="none" stroke="#56656c" strokeWidth={4} strokeLinecap="round" />
        {[-90, -20, 50, 110].map((dx, i) => {
          const t = ((f + i * 13) % 40) / 40;
          return (
            <path
              key={i}
              d={`M${dx} ${80 + t * 70} c 5 9 9 13 9 18 a 9 9 0 0 1 -18 0 c 0 -5 4 -9 9 -18 Z`}
              fill="#8fc4e3"
              stroke="#4d8fb8"
              strokeWidth={2}
              opacity={1 - t}
            />
          );
        })}
      </svg>
      {label ? (
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: 40,
            transform: "translateX(-50%)",
            fontFamily: ROUND,
            fontSize: 40,
            color: "#fff",
            textShadow: "0 0 6px #56656c, 0 0 2px #56656c",
          }}
        >
          濕氣
        </div>
      ) : null}
    </div>
  );
};

/** Moisture droplet */
export const Drop: React.FC<{ x: number; y: number; s?: number; opacity?: number }> = ({ x, y, s = 1, opacity = 1 }) => (
  <svg width={30} height={40} viewBox="0 0 30 40" style={{ position: "absolute", left: x - 15, top: y - 20, transform: `scale(${s})`, opacity }}>
    <path d="M15 2 C 22 16 28 22 28 28 A 13 13 0 0 1 2 28 C 2 22 8 16 15 2 Z" fill="#a8d6ef" stroke="#4d8fb8" strokeWidth={2.5} />
    <ellipse cx={10} cy={26} rx={3} ry={5} fill="#fff" opacity={0.7} />
  </svg>
);

/* ------------------------------------------------------------------ */
/* Backgrounds                                                         */
/* ------------------------------------------------------------------ */

export const Bedroom: React.FC<{ doorOpen?: number; rain?: boolean }> = ({ doorOpen = 0, rain = true }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      {/* wall */}
      <AbsoluteFill style={{ background: "linear-gradient(#efe0c8, #e8d4b4)" }} />
      <Wash x={500} y={300} w={900} h={500} color="#f6ead5" opacity={0.8} blur={60} />
      {/* wainscot + floor */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 760, bottom: 0, background: "linear-gradient(#c99a6a, #b8865a)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {Array.from({ length: 9 }).map((_, i) => (
          <line key={i} x1={i * 240 - 40} y1={760} x2={i * 260 - 160} y2={1080} stroke="#9e7048" strokeWidth={3} opacity={0.5} />
        ))}
        <line x1={0} y1={760} x2={1920} y2={760} stroke={INK} strokeWidth={5} />
        {/* window */}
        <g transform="translate(250 170)">
          <rect x={0} y={0} width={420} height={330} rx={16} fill="#9fb3b8" stroke={INK} strokeWidth={6} />
          <rect x={14} y={14} width={392} height={302} rx={8} fill="#b6c5c6" />
          {rain
            ? Array.from({ length: 26 }).map((_, i) => {
                const px = 20 + ((i * 53) % 380);
                const py = ((f * 9 + i * 71) % 300) + 14;
                return <line key={i} x1={px} y1={py} x2={px - 6} y2={Math.min(py + 26, 316)} stroke="#e8f0f2" strokeWidth={3} opacity={0.8} />;
              })
            : null}
          <path d="M14 230 C 80 200 150 240 220 214 C 300 190 360 226 406 210 L 406 316 L 14 316 Z" fill="#8a9c94" opacity={0.7} />
          <line x1={210} y1={0} x2={210} y2={330} stroke={INK} strokeWidth={6} />
          <line x1={0} y1={165} x2={420} y2={165} stroke={INK} strokeWidth={6} />
          {/* curtains */}
          <path d="M-30 -20 C -10 120 -40 240 -20 360 L 60 360 C 30 240 70 120 40 -20 Z" fill="#c9a6d4" stroke={INK} strokeWidth={4} />
          <path d="M450 -20 C 430 120 460 240 440 360 L 360 360 C 390 240 350 120 380 -20 Z" fill="#c9a6d4" stroke={INK} strokeWidth={4} />
        </g>
        {/* little shelf with plant */}
        <g transform="translate(830 330)">
          <rect x={0} y={60} width={220} height={16} rx={6} fill="#b07a4c" stroke={INK} strokeWidth={4} />
          <path d="M40 60 L 46 24 L 86 24 L 92 60 Z" fill="#e9c9a3" stroke={INK} strokeWidth={4} />
          <path d="M66 24 C 50 0 40 -10 30 -20 M 66 24 C 70 -6 80 -20 96 -26" fill="none" stroke="#5f8b48" strokeWidth={5} strokeLinecap="round" />
          <ellipse cx={30} cy={-22} rx={14} ry={8} fill="#8fbf6a" stroke={INK} strokeWidth={3} />
          <ellipse cx={98} cy={-28} rx={14} ry={8} fill="#8fbf6a" stroke={INK} strokeWidth={3} />
          <rect x={130} y={20} width={22} height={40} rx={4} fill="#e6a5a5" stroke={INK} strokeWidth={3} />
          <rect x={156} y={28} width={20} height={32} rx={4} fill="#a5c3e6" stroke={INK} strokeWidth={3} />
        </g>
        {/* door frame on the right */}
        <g transform="translate(1500 300)">
          <rect x={0} y={0} width={300} height={462} fill="#6d4a2f" stroke={INK} strokeWidth={6} />
          <rect x={10} y={10} width={280} height={452} fill="#f3e3b8" />
          <path d="M10 10 L 150 10 L 150 462 L 10 462 Z" fill="#fff1c8" opacity={doorOpen} />
          <g transform={`translate(10 10) scale(${1 - doorOpen * 0.85} 1)`}>
            <rect x={0} y={0} width={280} height={452} fill="#b07a4c" stroke={INK} strokeWidth={5} />
            <rect x={30} y={30} width={220} height={170} rx={10} fill="none" stroke={INK} strokeWidth={4} opacity={0.6} />
            <rect x={30} y={240} width={220} height={180} rx={10} fill="none" stroke={INK} strokeWidth={4} opacity={0.6} />
            <circle cx={240} cy={230} r={12} fill="#e6c25a" stroke={INK} strokeWidth={4} />
          </g>
        </g>
      </svg>
    </AbsoluteFill>
  );
};

/** Bed with blanket overlay rendered separately so a character can lie "inside" */
export const BedBack: React.FC = () => (
  <svg width={1920} height={1080} style={{ position: "absolute" }}>
    <g transform="translate(560 520)">
      <rect x={0} y={0} width={60} height={330} rx={14} fill="#a8724a" stroke={INK} strokeWidth={6} />
      <rect x={600} y={120} width={50} height={210} rx={12} fill="#a8724a" stroke={INK} strokeWidth={6} />
      <rect x={40} y={190} width={590} height={110} rx={20} fill="#f3e7d4" stroke={INK} strokeWidth={6} />
      <ellipse cx={170} cy={186} rx={110} ry={46} fill="#fffaf0" stroke={INK} strokeWidth={5} />
    </g>
  </svg>
);

export const BedBlanket: React.FC<{ lift?: number }> = ({ lift = 0 }) => (
  <svg width={1920} height={1080} style={{ position: "absolute" }}>
    <g transform={`translate(560 ${520 - lift})`}>
      <path
        d="M150 196 C 260 150 470 160 640 200 L 640 300 C 470 316 260 316 120 300 C 110 260 120 220 150 196 Z"
        fill="#b9a2d6"
        stroke={INK}
        strokeWidth={6}
      />
      {[0, 1, 2, 3, 4].map((i) => (
        <path key={i} d={`M${200 + i * 90} 190 L ${190 + i * 90} 300`} stroke="#fff" strokeWidth={8} opacity={0.5} />
      ))}
      <path d="M150 196 C 260 150 470 160 640 200" fill="none" stroke="#fff" strokeWidth={6} opacity={0.5} />
    </g>
  </svg>
);

/** Outdoor village path. humid 0..1 = foggy overcast, sun 0..1 = clear */
export const Outdoors: React.FC<{ humid?: number; sun?: number; house?: boolean; doorOpen?: number }> = ({
  humid = 0,
  sun = 1,
  house = false,
  doorOpen = 0,
}) => {
  const f = useCurrentFrame();
  const sky = `linear-gradient(rgb(${180 + sun * 30},${205 + sun * 25},${210 + sun * 20}), rgb(${236},${228},${200}))`;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: sky }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {/* sun */}
        <g opacity={sun}>
          <circle cx={1580} cy={180} r={110} fill="#ffe9a8" opacity={0.5} />
          <circle cx={1580} cy={180} r={70} fill="#ffd36e" stroke="#e5a83c" strokeWidth={5} />
        </g>
        {/* hills */}
        <path d="M0 560 C 250 430 450 470 700 520 C 950 420 1250 430 1500 510 C 1700 450 1850 470 1920 500 L 1920 760 L 0 760 Z" fill="#a9c88f" stroke="#6f8f5c" strokeWidth={4} />
        <path d="M0 640 C 300 560 600 600 900 640 C 1200 580 1600 590 1920 630 L 1920 800 L 0 800 Z" fill="#c2d89e" stroke="#7d9a62" strokeWidth={4} />
        {/* willow */}
        <g transform="translate(160 260)">
          <path d="M40 520 C 50 380 30 260 60 120" stroke="#7a5536" strokeWidth={22} fill="none" strokeLinecap="round" />
          {Array.from({ length: 9 }).map((_, i) => (
            <path
              key={i}
              d={`M${60 + i * 12} ${120 + i * 6} C ${100 + i * 18 + wave(f, 90, 6, i * 7)} 200, ${80 + i * 22} 330, ${90 + i * 20 + wave(f, 80, 10, i * 5)} 430`}
              stroke="#7fae5a"
              strokeWidth={8}
              fill="none"
              strokeLinecap="round"
            />
          ))}
          <ellipse cx={90} cy={110} rx={130} ry={70} fill="#9cc477" stroke="#6f8f5c" strokeWidth={4} />
        </g>
        {/* ground path */}
        <path d="M0 780 C 400 740 1400 740 1920 780 L 1920 1080 L 0 1080 Z" fill="#e9d6a8" stroke="#b99a62" strokeWidth={4} />
        <path d="M0 840 C 500 810 1300 810 1920 850" stroke="#d5bd86" strokeWidth={6} fill="none" />
        {/* grass tufts */}
        {[90, 420, 760, 1120, 1380, 1760].map((gx, i) => (
          <path key={i} d={`M${gx} 790 l 8 -34 l 6 30 l 10 -40 l 4 42 l 12 -28 l 2 30`} stroke="#6f9a52" strokeWidth={5} fill="none" strokeLinejoin="round" />
        ))}
        {house ? <LotusHouse doorOpen={doorOpen} /> : null}
      </svg>
      {/* humidity fog */}
      {humid > 0 ? (
        <AbsoluteFill style={{ opacity: humid }}>
          <AbsoluteFill style={{ background: "rgba(150,170,175,0.45)" }} />
          {[0, 1, 2, 3].map((i) => (
            <Wash key={i} x={((i * 620 + f * (1.4 + i * 0.3)) % 2600) - 340} y={420 + i * 130} w={900} h={160} color="#e4ecee" opacity={0.75} blur={40} />
          ))}
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};

/** Lianzi's house, sits right of frame (inside an <svg>) */
export const LotusHouse: React.FC<{ doorOpen?: number }> = ({ doorOpen = 0 }) => (
  <g transform="translate(1290 290)">
    <rect x={40} y={190} width={480} height={330} fill="#fbf1de" stroke={INK} strokeWidth={6} />
    {/* lotus-leaf roof */}
    <path d="M-30 210 C 60 40 200 0 280 0 C 360 0 500 40 590 210 C 500 180 380 196 280 186 C 180 196 60 180 -30 210 Z" fill="#8fbf6a" stroke={INK} strokeWidth={6} />
    <path d="M280 186 L 280 20 M 280 186 L 130 70 M 280 186 L 430 70 M 280 186 L 40 160 M 280 186 L 520 160" stroke="#6f9a52" strokeWidth={4} />
    <path d="M250 -10 C 250 -50 270 -70 280 -80 C 290 -70 310 -50 310 -10 C 300 0 260 0 250 -10 Z" fill="#f4a7b6" stroke={INK} strokeWidth={4} />
    {/* window */}
    <circle cx={140} cy={330} r={56} fill="#cfe3e6" stroke={INK} strokeWidth={5} />
    <path d="M84 330 L 196 330 M 140 274 L 140 386" stroke={INK} strokeWidth={4} />
    {/* doorway */}
    <rect x={300} y={300} width={160} height={220} rx={70} fill="#5b3a24" stroke={INK} strokeWidth={5} />
    <g transform={`translate(300 300) scale(${1 - doorOpen * 0.9} 1)`}>
      <rect x={0} y={0} width={160} height={220} rx={70} fill="#e6b980" stroke={INK} strokeWidth={5} />
      <circle cx={130} cy={130} r={9} fill="#e6c25a" stroke={INK} strokeWidth={3} />
      <path d="M50 60 C 60 40 100 40 110 60" fill="none" stroke={INK} strokeWidth={3} opacity={0.5} />
    </g>
    {/* doorbell */}
    <rect x={476} y={350} width={28} height={40} rx={8} fill="#f6d77a" stroke={INK} strokeWidth={4} />
    <circle cx={490} cy={370} r={7} fill="#e0475f" />
    {/* nameplate */}
    <rect x={160} y={220} width={130} height={46} rx={10} fill="#fffaf0" stroke={INK} strokeWidth={4} />
    <text x={225} y={254} textAnchor="middle" fontFamily={ROUND} fontSize={30} fill={INK}>
      蓮子家
    </text>
  </g>
);

export const Bush: React.FC<{ x: number; y: number; w?: number; flowers?: boolean }> = ({ x, y, w = 360, flowers = true }) => (
  <svg width={w} height={w * 0.6} viewBox="0 0 360 216" style={{ position: "absolute", left: x - w / 2, top: y - w * 0.6, overflow: "visible" }}>
    <path
      d="M10 214 C -10 150 40 110 80 120 C 80 50 170 30 200 80 C 240 30 330 60 320 130 C 370 140 370 210 340 214 Z"
      fill="#86b46a"
      stroke="#557a42"
      strokeWidth={6}
    />
    <path d="M80 160 C 100 140 120 140 140 160 M 200 140 C 220 120 250 120 270 140" fill="none" stroke="#557a42" strokeWidth={4} />
    {flowers
      ? [
          [70, 150],
          [160, 90],
          [250, 110],
          [300, 170],
          [120, 190],
        ].map(([fx, fy], i) => (
          <g key={i} transform={`translate(${fx} ${fy})`}>
            <circle r={13} fill="#e0475f" stroke="#8f2234" strokeWidth={3} />
            <path d="M-5 -2 C -2 -8 6 -6 5 2" fill="none" stroke="#8f2234" strokeWidth={2.5} />
          </g>
        ))
      : null}
  </svg>
);

export const Steam: React.FC<{ x: number; y: number; from: number; n?: number; spread?: number; size?: number; rise?: number; period?: number }> = ({
  x,
  y,
  from,
  n = 8,
  spread = 200,
  size = 90,
  rise = 300,
  period = 50,
}) => {
  const f = useCurrentFrame();
  if (f < from) return null;
  return (
    <>
      {Array.from({ length: n }).map((_, i) => {
        const t = ((f - from + (i * period) / n) % period) / period;
        const dx = Math.sin(i * 1.7) * spread * 0.5 + wave(f, 40, 12, i * 5);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x + dx - size / 2,
              top: y - t * rise - size / 2,
              width: size * (0.6 + t),
              height: size * (0.6 + t),
              borderRadius: "50%",
              background: "radial-gradient(circle, rgba(255,255,255,0.95), rgba(255,255,255,0))",
              opacity: Math.sin(t * Math.PI) * 0.9,
            }}
          />
        );
      })}
    </>
  );
};
