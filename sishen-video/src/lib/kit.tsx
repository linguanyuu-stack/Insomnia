import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/fonts";
import sizes from "../sprites.json";
import { Face, FaceSpec, hasFace } from "./face";
export type { FaceSpec, Expr } from "./face";

// Glyph-subset copies of Huninn (jf 粉圓) and LXGW WenKai TC, fetched by tools/fonts.py
export const ROUND = "Huninn";
export const BRUSH = "WenKaiTC";
loadFont({ family: ROUND, url: staticFile("fonts/huninn.woff2") });
loadFont({ family: BRUSH, url: staticFile("fonts/wenkai.woff2"), weight: "700" });

export const INK = "#5a3b22";
export const PAPER = "#f7ead6";

export type SpriteName = keyof typeof sizes;

const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

/** interpolate with clamping and a soft ease by default */
export const tw = (
  f: number,
  input: number[],
  output: number[],
  easing: (t: number) => number = Easing.inOut(Easing.cubic),
) => interpolate(f, input, output, { ...clamp, easing });

export const lin = (f: number, input: number[], output: number[]) =>
  interpolate(f, input, output, clamp);

export const wave = (f: number, period: number, amp: number, phase = 0) =>
  Math.sin(((f + phase) / period) * Math.PI * 2) * amp;

/** 0 → 1 springy pop starting at `at` */
export const usePop = (at: number, damping = 11) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: f - at, fps, config: { damping, mass: 0.6 } });
};

type SpriteProps = {
  name: SpriteName;
  x: number;
  y: number; // ground (bottom-centre)
  h: number;
  flip?: boolean;
  rot?: number;
  sx?: number;
  sy?: number;
  opacity?: number;
  tint?: { color: string; amount: number };
  shadow?: number; // shadow opacity
  lift?: number; // jump height (shadow stays on ground)
  style?: React.CSSProperties;
  children?: React.ReactNode; // overlay in a 0..100 box that follows the sprite
  face?: FaceSpec; // redraw the face with this expression (look is in world space)
};

export const Sprite: React.FC<SpriteProps> = ({
  name,
  x,
  y,
  h,
  flip,
  rot = 0,
  sx = 1,
  sy = 1,
  opacity = 1,
  tint,
  shadow = 0.22,
  lift = 0,
  style,
  children,
  face,
}) => {
  const [iw, ih] = sizes[name];
  const w = (iw / ih) * h;
  const withFace = face && hasFace(name);
  const src = staticFile(`sprites/${name}${withFace ? "__nf" : ""}.png`);
  return (
    <>
      {shadow > 0 ? (
        <div
          style={{
            position: "absolute",
            left: x - w * 0.36 * sx,
            top: y - 14,
            width: w * 0.72 * sx,
            height: 26,
            borderRadius: "50%",
            background: "rgba(110,72,40,1)",
            opacity: shadow * opacity * Math.max(0.3, 1 - lift / 300),
            filter: "blur(6px)",
          }}
        />
      ) : null}
      <div
        style={{
          position: "absolute",
          left: x - w / 2,
          top: y - h - lift,
          width: w,
          height: h,
          opacity,
          transformOrigin: "50% 100%",
          transform: `rotate(${rot}deg) scale(${flip ? -sx : sx}, ${sy})`,
          ...style,
        }}
      >
        <Img src={src} style={{ width: "100%", height: "100%" }} />
        {tint && tint.amount > 0 ? (
          <div
            style={{
              position: "absolute",
              inset: 0,
              background: tint.color,
              opacity: tint.amount,
              mixBlendMode: "multiply",
              WebkitMaskImage: `url(${src})`,
              WebkitMaskSize: "100% 100%",
              maskImage: `url(${src})`,
              maskSize: "100% 100%",
            }}
          />
        ) : null}
        {withFace ? (
          <svg viewBox={`0 0 ${iw} ${ih}`} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", overflow: "visible" }}>
            <Face name={name} spec={{ ...face, look: (face.look ?? 0) * (flip ? -1 : 1) }} />
          </svg>
        ) : null}
        {children ? (
          <svg viewBox="0 0 100 100" preserveAspectRatio="none" style={{ position: "absolute", inset: 0, width: "100%", height: "100%", overflow: "visible" }}>
            {children}
          </svg>
        ) : null}
      </div>
    </>
  );
};

/** Warm paper grain multiplied over everything */
export const PaperGrain: React.FC<{ opacity?: number }> = ({ opacity = 0.55 }) => (
  <AbsoluteFill style={{ mixBlendMode: "multiply", opacity, pointerEvents: "none" }}>
    <Img src={staticFile("paper.jpg")} style={{ width: "100%", height: "100%" }} />
  </AbsoluteFill>
);

/** Dip-to-paper fade at the head and tail of a scene */
export const SceneFade: React.FC<{ dur: number; children: React.ReactNode; inF?: number; outF?: number }> = ({
  dur,
  children,
  inF = 10,
  outF = 10,
}) => {
  const f = useCurrentFrame();
  const o = Math.min(lin(f, [0, inF], [0, 1]), lin(f, [dur - outF, dur], [1, 0]));
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <AbsoluteFill style={{ opacity: inF === 0 && outF === 0 ? 1 : o }}>{children}</AbsoluteFill>
      <PaperGrain />
    </AbsoluteFill>
  );
};

/** Subtitle bar on a soft paper ribbon */
export const Caption: React.FC<{ cues: [number, number, string][] }> = ({ cues }) => {
  const f = useCurrentFrame();
  const cue = cues.find(([a, b]) => f >= a && f < b);
  if (!cue) return null;
  const [a, b, text] = cue;
  const o = Math.min(lin(f, [a, a + 8], [0, 1]), lin(f, [b - 8, b], [1, 0]));
  const y = tw(f, [a, a + 10], [16, 0]);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: 46,
        display: "flex",
        justifyContent: "center",
        opacity: o,
        transform: `translateY(${y}px)`,
      }}
    >
      <div
        style={{
          fontFamily: ROUND,
          fontSize: 54,
          color: INK,
          padding: "14px 46px 16px",
          background: "rgba(255,248,236,0.9)",
          borderRadius: 999,
          boxShadow: "0 4px 0 rgba(150,110,70,0.25)",
          border: "3px solid rgba(150,105,60,0.35)",
          letterSpacing: 2,
          whiteSpace: "nowrap",
        }}
      >
        {text}
      </div>
    </div>
  );
};

/** Hand-drawn speech / thought text above a character */
export const Bubble: React.FC<{
  x: number;
  y: number;
  text: string;
  at: number;
  until: number;
  size?: number;
  tail?: "left" | "right" | "none";
  color?: string;
}> = ({ x, y, text, at, until, size = 46, tail = "left", color = "#fffaf0" }) => {
  const f = useCurrentFrame();
  const p = usePop(at, 10);
  if (f < at || f > until) return null;
  const o = lin(f, [until - 6, until], [1, 0]);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translate(-50%, -100%) scale(${p})`,
        transformOrigin: tail === "right" ? "85% 110%" : "15% 110%",
        opacity: o,
      }}
    >
      <div
        style={{
          fontFamily: ROUND,
          fontSize: size,
          color: INK,
          background: color,
          border: `4px solid ${INK}`,
          borderRadius: 40,
          padding: "10px 30px 12px",
          whiteSpace: "nowrap",
          position: "relative",
        }}
      >
        {text}
        {tail !== "none" ? (
          <div
            style={{
              position: "absolute",
              bottom: -22,
              [tail === "left" ? "left" : "right"]: 40,
              width: 0,
              height: 0,
              borderLeft: "16px solid transparent",
              borderRight: "16px solid transparent",
              borderTop: `24px solid ${INK}`,
            }}
          />
        ) : null}
      </div>
    </div>
  );
};

/** Floating "Zzz" */
export const Zzz: React.FC<{ x: number; y: number; from?: number; to?: number }> = ({ x, y, from = 0, to = 99999 }) => {
  const f = useCurrentFrame();
  if (f < from || f > to) return null;
  return (
    <>
      {[0, 1, 2].map((i) => {
        const t = ((f - from + i * 22) % 66) / 66;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x + t * 70 + i * 6,
              top: y - t * 120,
              fontFamily: ROUND,
              fontSize: 34 + i * 12,
              color: "#7d6aa8",
              opacity: Math.sin(t * Math.PI),
            }}
          >
            Z
          </div>
        );
      })}
    </>
  );
};

/** Little impact ticks like the reference sheets */
export const Ticks: React.FC<{ x: number; y: number; at: number; dur?: number; color?: string; rot?: number; scale?: number }> = ({
  x,
  y,
  at,
  dur = 24,
  color = "#e6a531",
  rot = 0,
  scale = 1,
}) => {
  const f = useCurrentFrame();
  if (f < at || f > at + dur) return null;
  const p = lin(f, [at, at + 6, at + dur - 6, at + dur], [0, 1, 1, 0]);
  return (
    <svg
      style={{ position: "absolute", left: x - 40, top: y - 40, overflow: "visible", opacity: p }}
      width={80}
      height={80}
    >
      <g transform={`translate(40 40) rotate(${rot}) scale(${scale * (0.7 + p * 0.3)})`} stroke={color} strokeWidth={6} strokeLinecap="round">
        <line x1={-26} y1={-6} x2={-40} y2={-14} />
        <line x1={-8} y1={-22} x2={-12} y2={-40} />
        <line x1={12} y1={-20} x2={22} y2={-36} />
      </g>
    </svg>
  );
};

export const Heart: React.FC<{ x: number; y: number; s?: number; color?: string; opacity?: number; rot?: number }> = ({
  x,
  y,
  s = 1,
  color = "#f07f95",
  opacity = 1,
  rot = 0,
}) => (
  <svg
    width={60}
    height={56}
    viewBox="0 0 60 56"
    style={{ position: "absolute", left: x - 30, top: y - 28, transform: `scale(${s}) rotate(${rot}deg)`, opacity, overflow: "visible" }}
  >
    <path
      d="M30 52 C 10 38 2 28 2 17 C 2 8 9 2 17 2 C 23 2 27 5 30 10 C 33 5 37 2 43 2 C 51 2 58 8 58 17 C 58 28 50 38 30 52 Z"
      fill={color}
      stroke="#b9506a"
      strokeWidth={3}
    />
    <ellipse cx={17} cy={14} rx={6} ry={4} fill="#fff" opacity={0.6} />
  </svg>
);

/** Rising hearts emitter */
export const HeartBurst: React.FC<{ x: number; y: number; from: number; to: number; n?: number; spread?: number }> = ({
  x,
  y,
  from,
  to,
  n = 6,
  spread = 160,
}) => {
  const f = useCurrentFrame();
  if (f < from || f > to + 60) return null;
  const out: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    const start = from + i * ((to - from) / n);
    const t = (f - start) / 60;
    if (t < 0 || t > 1) continue;
    const dx = Math.sin(i * 2.3) * spread * 0.5 + wave(f, 40, 14, i * 9);
    out.push(
      <Heart key={i} x={x + dx} y={y - t * 220} s={0.5 + Math.sin(t * Math.PI) * 0.6} opacity={Math.sin(t * Math.PI)} rot={dx / 8} />,
    );
  }
  return <>{out}</>;
};

export const Sweat: React.FC<{ x: number; y: number; at: number; period?: number }> = ({ x, y, at, period = 30 }) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  const t = ((f - at) % period) / period;
  return (
    <svg width={30} height={40} style={{ position: "absolute", left: x, top: y + t * 40, opacity: 1 - t }}>
      <path d="M15 2 C 22 16 28 22 28 28 A 13 13 0 0 1 2 28 C 2 22 8 16 15 2 Z" fill="#9fd3f0" stroke="#4d8fb8" strokeWidth={2.5} />
    </svg>
  );
};

/** Watercolour wash blob */
export const Wash: React.FC<{ x: number; y: number; w: number; h: number; color: string; opacity?: number; blur?: number }> = ({
  x,
  y,
  w,
  h,
  color,
  opacity = 1,
  blur = 30,
}) => (
  <div
    style={{
      position: "absolute",
      left: x - w / 2,
      top: y - h / 2,
      width: w,
      height: h,
      borderRadius: "50%",
      background: color,
      opacity,
      filter: `blur(${blur}px)`,
    }}
  />
);
