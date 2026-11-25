import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { BRUSH, INK, ROUND, SceneFade, Sprite, SpriteName, tw, usePop, wave, Wash } from "../lib/kit";
import { Petals3D } from "../three/ThreeBits";

export const S9_DUR = 150;

const LINEUP: { name: SpriteName; h: number }[] = [
  { name: "fuling_idle", h: 150 },
  { name: "lianzi_leaf", h: 150 },
  { name: "qianshi_run", h: 140 },
  { name: "chuanxiong_point", h: 150 },
  { name: "danggui_tea", h: 170 },
  { name: "huaishan_herb", h: 170 },
  { name: "gouqi_cup", h: 160 },
];

export const S9End: React.FC = () => {
  const f = useCurrentFrame();
  const pk = tw(f, [0, 26], [0, 1], (t) => 1 - Math.pow(1 - t, 3));
  const t1 = usePop(18, 9);
  const t2 = usePop(36, 12);
  const t3 = usePop(50, 12);
  return (
    <SceneFade dur={S9_DUR} outF={18}>
      <AbsoluteFill style={{ background: "linear-gradient(#f3ecd6, #e7dcbc)" }} />
      <Wash x={520} y={560} w={800} h={900} color="#cfe0b4" opacity={0.7} blur={70} />
      <Wash x={1300} y={420} w={1000} h={600} color="#fff6e2" opacity={0.9} blur={60} />
      <Img
        src={staticFile("package_front.png")}
        style={{
          position: "absolute",
          left: 130,
          top: 70,
          height: 900,
          transform: `translateY(${(1 - pk) * 900}px) rotate(${-4 + wave(f, 90, 1.2)}deg)`,
          filter: "drop-shadow(0 20px 24px rgba(90,60,30,0.35))",
        }}
      />
      <div style={{ position: "absolute", left: 900, right: 60, top: 170, textAlign: "center" }}>
        <div
          style={{
            fontFamily: ROUND,
            fontSize: 46,
            color: "#7aa35b",
            letterSpacing: 8,
            transform: `scale(${t3})`,
          }}
        >
          宜康中醫
        </div>
        <div
          style={{
            fontFamily: BRUSH,
            fontWeight: 700,
            fontSize: 172,
            color: INK,
            letterSpacing: 14,
            transform: `scale(${t1})`,
            textShadow: "0 8px 0 rgba(122,163,91,0.3)",
          }}
        >
          四神藥膳包
        </div>
        <div
          style={{
            display: "inline-block",
            marginTop: 20,
            fontFamily: ROUND,
            fontSize: 52,
            color: "#fff",
            background: "#b8452f",
            padding: "8px 44px 12px",
            borderRadius: 999,
            border: `4px solid ${INK}`,
            transform: `scale(${t2})`,
          }}
        >
          健脾祛濕・找回好元氣
        </div>
      </div>
      {LINEUP.map((c, i) => {
        const p = Math.max(0, Math.min(1, (f - 60 - i * 5) / 10));
        return (
          <Sprite
            key={c.name}
            name={c.name}
            x={1010 + i * 135}
            y={930}
            h={c.h}
            opacity={p}
            lift={Math.abs(wave(f, 20, 22, i * 4)) + (1 - p) * 60}
          />
        );
      })}
      <Petals3D n={40} />
    </SceneFade>
  );
};
