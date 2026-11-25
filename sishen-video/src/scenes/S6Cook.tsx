import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { BRUSH, INK, ROUND, Bubble, Caption, SceneFade, Sprite, Ticks, tw, wave, Wash } from "../lib/kit";
import { ChefHat, Steam } from "../lib/props";
import { INGREDIENTS, SoupPot3D } from "../three/ThreeBits";

export const S6_DUR = 420;

const AMOUNT: Record<string, string> = {
  當歸: "1.5 錢",
  川芎: "1 錢",
  淮山: "6 錢",
  蓮子: "5 錢",
  茯苓: "5 錢",
  芡實: "4 錢",
  枸杞: "1.5 錢",
};

const TAG_POS: [number, number][] = [
  [560, 210],
  [1360, 220],
  [500, 360],
  [1420, 370],
  [620, 120],
  [1300, 110],
  [960, 90],
];

export const S6Cook: React.FC = () => {
  const f = useCurrentFrame();
  const done = tw(f, [330, 350], [0, 1]);
  return (
    <SceneFade dur={S6_DUR}>
      {/* warm kitchen */}
      <AbsoluteFill style={{ background: "linear-gradient(#f6e6c8, #efd2a4)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {Array.from({ length: 8 }).map((_, i) => (
          <rect key={i} x={i * 250 - 20} y={-10} width={8} height={760} fill="#e2c193" />
        ))}
        <rect x={0} y={760} width={1920} height={320} fill="#b98656" />
        <line x1={0} y1={760} x2={1920} y2={760} stroke={INK} strokeWidth={6} />
        {Array.from({ length: 6 }).map((_, i) => (
          <line key={i} x1={0} y1={800 + i * 50} x2={1920} y2={800 + i * 50} stroke="#a3734a" strokeWidth={3} />
        ))}
        {/* little stove flames under the pot */}
        {[0, 1, 2, 3, 4].map((i) => (
          <path
            key={i}
            d={`M${880 + i * 40} 905 C ${870 + i * 40} ${880 - Math.abs(wave(f, 10, 16, i * 3))}, ${900 + i * 40} ${860 - Math.abs(wave(f, 8, 22, i * 5))}, ${900 + i * 40} 905 Z`}
            fill={i % 2 ? "#ff9f43" : "#ffcf5c"}
            stroke="#c4622d"
            strokeWidth={3}
          />
        ))}
      </svg>
      <Wash x={960} y={560} w={1100} h={700} color="#fff4dc" opacity={0.6 + done * 0.4} blur={60} />
      <AbsoluteFill style={{ top: 40 }}>
        <SoupPot3D width={1920} height={1080} />
      </AbsoluteFill>

      <Steam x={960} y={560} from={0} n={14} spread={380} size={170} rise={420} period={70} />

      {/* chefs */}
      <Sprite
        name="danggui_water"
        x={330}
        y={1000}
        h={430}
        lift={Math.abs(wave(f, 40, 8))}
        rot={f > 30 && f < 110 ? 6 : 0}
        face={done > 0 ? { e: "laugh", look: 1 } : f < 110 ? { e: "smile", look: 1, lookY: 0.6 } : { e: "determined", look: 1, lookY: 0.4 }}
      />
      <ChefHat x={320 + (f > 30 && f < 110 ? 30 : 0)} y={610 - Math.abs(wave(f, 40, 8))} w={140} rot={-6} />
      <Sprite
        name={(f >= 240 && f < 280) || done > 0 ? "gouqi_jump" : "gouqi_point"}
        x={1400}
        y={1010}
        h={300}
        flip
        lift={(f >= 240 && f < 280) || done > 0 ? Math.abs(wave(f, 22, 40, 5)) : Math.abs(wave(f, 26, 6, 5))}
        face={
          done > 0
            ? { e: "laugh", look: -0.5 }
            : f >= 240 && f < 280
              ? { e: "happy", look: -1, talk: Math.abs(Math.sin(f / 2.4)) }
              : { e: "smile", look: -1, lookY: 0.4 }
        }
      />
      <ChefHat x={1392} y={748 - ((f >= 240 && f < 280) || done > 0 ? Math.abs(wave(f, 22, 40, 5)) : Math.abs(wave(f, 26, 6, 5)))} w={100} rot={-10} />
      <Sprite
        name="huaishan_herb"
        x={1700}
        y={1000}
        h={420}
        flip
        lift={Math.abs(wave(f, 40, 8, 13))}
        face={done > 0 ? { e: "proud", look: -1 } : f >= 110 && f < 240 ? { e: "determined", look: -1, lookY: 0.5, talk: f > 118 && f < 150 ? Math.abs(Math.sin(f / 2.4)) : 0 } : { e: "smile", look: -1, lookY: 0.5 }}
      />
      <ChefHat x={1690} y={630 - Math.abs(wave(f, 40, 8, 13))} w={120} rot={8} />
      <Bubble x={1500} y={700} text="枸杞來囉～" at={244} until={282} size={38} tail="right" />
      <Bubble x={1640} y={520} text="四神，下鍋！" at={118} until={160} size={38} tail="right" />
      <Bubble x={420} y={520} text="先放當歸、川芎～" at={20} until={70} size={38} tail="left" />

      {/* ingredient tags */}
      {INGREDIENTS.map((ing, i) => {
        const t = f - ing.at;
        if (t < 0) return null;
        const p = Math.min(1, t / 8);
        const pop = t < 14 ? 1 + Math.sin((t / 14) * Math.PI) * 0.25 : 1;
        const [x, y] = TAG_POS[i];
        const four = ["淮山", "蓮子", "茯苓", "芡實"].includes(ing.key);
        return (
          <div
            key={ing.key}
            style={{
              position: "absolute",
              left: x,
              top: y,
              transform: `translate(-50%,-50%) scale(${p * pop})`,
              fontFamily: ROUND,
              fontSize: 40,
              color: INK,
              background: four ? "#fff2b8" : "#fffaf0",
              border: `4px solid ${four ? "#d9a23a" : INK}`,
              borderRadius: 999,
              padding: "6px 26px 8px",
              whiteSpace: "nowrap",
              opacity: 1 - done,
            }}
          >
            {ing.key} <span style={{ fontSize: 30, color: "#8a6a48" }}>{AMOUNT[ing.key]}</span>
          </div>
        );
      })}

      {/* done banner */}
      {f >= 330 ? (
        <div
          style={{
            position: "absolute",
            top: 120,
            width: "100%",
            textAlign: "center",
            fontFamily: BRUSH,
            fontWeight: 700,
            fontSize: 140,
            color: "#b8452f",
            letterSpacing: 20,
            transform: `scale(${0.6 + done * 0.4})`,
            opacity: done,
            textShadow: "0 0 30px #fff6d8, 0 6px 0 rgba(255,210,120,0.6)",
          }}
        >
          四神湯 完成！
        </div>
      ) : null}
      <Ticks x={620} y={180} at={340} dur={40} scale={1.6} rot={-30} />
      <Ticks x={1300} y={180} at={344} dur={40} scale={1.6} rot={30} />
      <Caption
        cues={[
          [6, 112, "三位廚神出手：當歸、川芎先下鍋！"],
          [118, 244, "再加入「四神」——淮山、蓮子、茯苓、芡實"],
          [250, 326, "最後撒上枸杞，小火慢慢燉……"],
          [336, 416, "香噴噴的四神湯，完成啦！"],
        ]}
      />
    </SceneFade>
  );
};
