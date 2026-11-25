import React from "react";
import { useCurrentFrame } from "remotion";
import { Caption, Heart, SceneFade, Sprite, tw, usePop, wave, Zzz, Bubble } from "../lib/kit";
import { Bedroom, BedBack, BedBlanket, DampCloud, Rose } from "../lib/props";

export const S2_DUR = 390;

/** Thought cloud with content */
const Thought: React.FC<{ x: number; y: number; s: number; children: React.ReactNode }> = ({ x, y, s, children }) => (
  <div style={{ position: "absolute", left: x, top: y, transform: `translate(-50%,-50%) scale(${s})` }}>
    <svg width={560} height={420} viewBox="-280 -210 560 420" style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
      <circle cx={-330} cy={190} r={16} fill="#fffaf0" stroke="#5a3b22" strokeWidth={4} />
      <circle cx={-270} cy={150} r={26} fill="#fffaf0" stroke="#5a3b22" strokeWidth={4} />
      <path
        d="M-200 120 C -290 120 -290 20 -230 0 C -280 -90 -170 -170 -90 -130 C -50 -210 90 -210 120 -130 C 210 -170 290 -80 240 0 C 290 50 250 140 170 120 C 130 190 -150 190 -200 120 Z"
        fill="#fffaf0"
        stroke="#5a3b22"
        strokeWidth={5}
      />
    </svg>
    <div style={{ position: "absolute", left: 0, top: 0, width: 560, height: 420 }}>{children}</div>
  </div>
);

export const S2Bedroom: React.FC = () => {
  const f = useCurrentFrame();
  const thinking = f >= 95 && f < 268;
  const bubbleS = Math.min(usePop(95, 12), f < 262 ? 1 : tw(f, [262, 268], [1, 0]));
  const roseMode = f >= 190;
  const cloudP = usePop(222, 9);
  const tryUp = tw(f, [205, 235], [0, 50]) - tw(f, [252, 266], [0, 50], (t) => t * t);
  const squash = f >= 252 && f < 290 ? 1 - Math.max(0, Math.sin(((f - 252) / 38) * Math.PI)) * 0.15 : 1;
  const pose = "fuling_idle";
  const talkA = (a: number, b: number) => (f >= a && f < b ? Math.abs(Math.sin(f / 2.6)) : 0);
  const face =
    f < 95
      ? { e: "sleep" as const }
      : f < 128
        ? { e: "smile" as const, look: 0.3, lookY: -1, blush: 0.6 }
        : f < 200
          ? { e: "love" as const, look: 0.6 }
          : f < 240
            ? { e: "determined" as const, look: 0.7, talk: talkA(202, 236) }
            : f < 266
              ? { e: "surprised" as const, lookY: -1 }
              : f < 300
                ? { e: "tired" as const, talk: talkA(270, 296) }
                : f < 330
                  ? { e: "disappointed" as const, look: -0.8, lookY: -0.6 }
                  : { e: "sleep" as const };
  return (
    <SceneFade dur={S2_DUR}>
      <Bedroom />
      <div style={{ position: "absolute", left: 735, top: 170, width: 130, height: 150, background: "#fff6e4", border: "8px solid #b07a4c", borderRadius: 10, boxShadow: "0 4px 0 rgba(90,59,34,0.3)", transform: `rotate(${-4 + (f > 128 && f < 200 ? wave(f, 30, 1) : 0)}deg)`, overflow: "hidden" }}>
        <Sprite name="lianzi_idle" x={65} y={150} h={130} shadow={0} face={{ e: "smile", look: 0.2 }} />
      </div>
      <Heart x={870} y={170 - (f > 128 && f < 200 ? Math.abs(wave(f, 30, 12)) : 0)} s={0.45} opacity={f > 128 && f < 200 ? 1 : 0.6} />
      <BedBack />
      <Sprite
        name={pose}
        x={735}
        y={745 - tryUp}
        h={230}
        sy={(1 + wave(f, 70, 0.02)) * squash}
        sx={2 - squash}
        shadow={0}
        rot={f >= 266 && f < 300 ? wave(f, 8, 3) : 0}
        face={face}
      />
      <BedBlanket lift={tryUp * 0.3} />
      <Zzz x={820} y={520} to={95} />
      <Zzz x={820} y={520} from={305} />
      {thinking ? (
        <Thought x={1160} y={320} s={bubbleS}>
          {!roseMode ? (
            <>
              <Sprite name="lianzi_idle" x={280} y={350} h={240} shadow={0} lift={Math.abs(wave(f, 30, 10))} />
              <Heart x={130} y={140 + wave(f, 30, 8)} s={0.9} />
              <Heart x={430} y={120 + wave(f, 30, 8, 10)} s={0.7} />
            </>
          ) : (
            <>
              <Rose x={280} y={170} s={1.2} rot={wave(f, 40, 6)} />
              <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center", fontFamily: "inherit" }} />
            </>
          )}
        </Thought>
      ) : null}
      <Bubble x={980} y={560} text="去買花送她！" at={200} until={240} size={40} />
      {f >= 222 && f < 300 ? (
        <DampCloud x={760} y={tw(f, [222, 240, 250, 262], [180, 300, 300, 420])} s={cloudP * 1.1} opacity={tw(f, [285, 300], [1, 0])} />
      ) : null}
      <Bubble x={900} y={560} text="唉……好累……" at={268} until={300} size={40} />
      <Caption
        cues={[
          [12, 92, "白茯苓，偷偷喜歡著隔壁的蓮子。"],
          [98, 195, "好想買一朵花，送給她……"],
          [205, 298, "可是濕氣太重，全身沉甸甸、懶洋洋……"],
          [305, 385, "「算了……明天再說吧～」"],
        ]}
      />
    </SceneFade>
  );
};
