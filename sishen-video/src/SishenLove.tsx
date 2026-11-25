import React from "react";
import { AbsoluteFill, Series, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import { S1Title, S1_DUR } from "./scenes/S1Title";
import { S2Bedroom, S2_DUR } from "./scenes/S2Bedroom";
import { S3Rescue, S3_DUR } from "./scenes/S3Rescue";
import { S4Humid, S4_DUR } from "./scenes/S4Humid";
import { S5Idea, S5_DUR } from "./scenes/S5Idea";
import { S6Cook, S6_DUR } from "./scenes/S6Cook";
import { S7Transform, S7_DUR } from "./scenes/S7Transform";
import { S8Propose, S8_DUR } from "./scenes/S8Propose";
import { S9End, S9_DUR } from "./scenes/S9End";

export const SCENES = [
  { id: "S1-Title", C: S1Title, d: S1_DUR },
  { id: "S2-Bedroom", C: S2Bedroom, d: S2_DUR },
  { id: "S3-Rescue", C: S3Rescue, d: S3_DUR },
  { id: "S4-Humid", C: S4Humid, d: S4_DUR },
  { id: "S5-Idea", C: S5Idea, d: S5_DUR },
  { id: "S6-Cook", C: S6Cook, d: S6_DUR },
  { id: "S7-Transform", C: S7Transform, d: S7_DUR },
  { id: "S8-Propose", C: S8Propose, d: S8_DUR },
  { id: "S9-End", C: S9End, d: S9_DUR },
];

export const TOTAL = SCENES.reduce((a, s) => a + s.d, 0);

export const SishenLove: React.FC = () => (
  <AbsoluteFill style={{ background: "#f7ead6" }}>
    <Series>
      {SCENES.map(({ id, C, d }) => (
        <Series.Sequence key={id} name={id} durationInFrames={d}>
          <C />
        </Series.Sequence>
      ))}
    </Series>
    <Audio src={staticFile("soundtrack.wav")} />
  </AbsoluteFill>
);
