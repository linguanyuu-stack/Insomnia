import React from "react";
import { AbsoluteFill } from "remotion";
import { Sprite, SpriteName, Expr, ROUND } from "./lib/kit";
const EX: Expr[] = ["smile","happy","angry","shout","strain","tired","sleep","sad","disappointed","surprised","love","shy","determined","dizzy","giggle","nervous","proud","laugh"];
export const FaceTest: React.FC<{ name: string }> = ({ name }) => (
  <AbsoluteFill style={{ background: "#3c8c5a" }}>
    {EX.map((e, i) => (
      <React.Fragment key={e}>
        <Sprite name={name as SpriteName} x={160 + (i % 6) * 320} y={330 + Math.floor(i / 6) * 350} h={280} face={{ e, look: i % 3 === 0 ? 0 : i % 3 === 1 ? 1 : -1 }} shadow={0} />
        <div style={{ position: "absolute", left: 60 + (i % 6) * 320, top: 335 + Math.floor(i / 6) * 350, fontFamily: ROUND, fontSize: 22, color: "#fff" }}>{e}</div>
      </React.Fragment>
    ))}
  </AbsoluteFill>
);
