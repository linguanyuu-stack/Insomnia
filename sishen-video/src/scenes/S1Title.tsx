import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { BRUSH, ROUND, INK, Heart, SceneFade, Sprite, tw, usePop, wave, Wash } from "../lib/kit";
import { Outdoors } from "../lib/props";
import { Petals3D } from "../three/ThreeBits";

export const S1_DUR = 150;

export const S1Title: React.FC = () => {
  const f = useCurrentFrame();
  const t1 = usePop(12, 9);
  const t2 = usePop(34, 12);
  const hp = usePop(55, 8);
  return (
    <SceneFade dur={S1_DUR} inF={12}>
      <Outdoors sun={1} />
      <Wash x={960} y={330} w={1300} h={420} color="#fff8ea" opacity={0.85} blur={50} />
      <Sprite name="fuling_idle" x={tw(f, [0, 40], [-200, 600])} y={930} h={300} lift={Math.abs(wave(f, 24, 18))} face={f < 45 ? { e: "determined", look: 1 } : { e: "shy", look: 1 }} />
      <Sprite name="lianzi_idle" x={tw(f, [10, 50], [2120, 1320])} y={930} h={300} flip lift={Math.abs(wave(f, 24, 18, 12))} face={f < 55 ? { e: "smile", look: -1 } : { e: "happy", look: -1, blush: 0.6 }} />
      <Heart x={960} y={720 + wave(f, 40, 10)} s={hp * (1.6 + wave(f, 20, 0.12))} />
      <AbsoluteFill style={{ alignItems: "center", top: 140 }}>
        <div
          style={{
            fontFamily: BRUSH,
            fontWeight: 700,
            fontSize: 170,
            color: INK,
            letterSpacing: 18,
            transform: `scale(${t1}) rotate(${(1 - t1) * -6}deg)`,
            textShadow: "0 6px 0 rgba(240,127,149,0.35)",
          }}
        >
          茯苓的告白
        </div>
        <div
          style={{
            marginTop: 16,
            fontFamily: ROUND,
            fontSize: 54,
            color: "#fff",
            background: "#7aa35b",
            padding: "8px 40px 10px",
            borderRadius: 999,
            border: `4px solid ${INK}`,
            transform: `scale(${t2})`,
          }}
        >
          四神藥膳小劇場
        </div>
      </AbsoluteFill>
      <Petals3D n={45} />
    </SceneFade>
  );
};
