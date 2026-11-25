import React from "react";
import { useCurrentFrame } from "remotion";
import { BRUSH, Bubble, Caption, SceneFade, Sprite, Ticks, tw, wave } from "../lib/kit";
import { Bowl, Outdoors, Steam } from "../lib/props";
import { Fuling } from "../lib/fuling";

export const S7_DUR = 300;
const G = 930;

export const S7Transform: React.FC = () => {
  const f = useCurrentFrame();
  const humid = tw(f, [115, 220], [0.8, 0]);
  const sun = tw(f, [140, 240], [0, 1]);
  const gx = tw(f, [0, 45], [1900, 1290]);
  // deflate with a wobbly overshoot, then slim down
  const deflate = f < 115 ? 1 : f < 170 ? tw(f, [115, 170], [1, 0]) + Math.sin((f - 115) / 3) * 0.08 * (1 - (f - 115) / 55) : 0;
  const slim = tw(f, [165, 195], [0, 1]);
  const muscle = tw(f, [190, 215], [0, 1]);
  const drink = tw(f, [62, 108], [0, 1]);
  const flexLift = f > 205 ? Math.abs(wave(f, 30, 16)) : 0;
  return (
    <SceneFade dur={S7_DUR}>
      <Outdoors humid={humid} sun={sun} />
      {/* tired helpers perk up later */}
      <Sprite
        name={f < 215 ? "qianshi_angry" : "qianshi_run"}
        x={330}
        y={G}
        h={200}
        rot={f < 215 ? -10 : 0}
        lift={f >= 215 ? Math.abs(wave(f, 18, 40)) : 0}
      />
      <Sprite name={f < 215 ? "chuanxiong_idle" : "chuanxiong_point"} x={560} y={G} h={220} lift={f >= 215 ? Math.abs(wave(f, 18, 40, 9)) : 0} />

      <Fuling
        x={960}
        y={G}
        h={f < 190 ? 250 : tw(f, [190, 210], [250, 290])}
        pose={f < 190 ? (f < 60 ? "fuling_shy" : "fuling_idle") : "fuling_idle"}
        inflate={Math.max(0, deflate)}
        slim={slim}
        muscle={muscle}
        lift={flexLift}
      />

      {/* goji brings soup */}
      <Sprite name={f < 56 ? "gouqi_cup" : "gouqi_cup"} x={gx} y={G} h={260} lift={f < 45 ? Math.abs(wave(f, 14, 16)) : 0} />
      {f >= 50 && f < 118 ? (
        <Bowl x={f < 60 ? tw(f, [50, 60], [1190, 1080]) : 1080} y={tw(f, [50, 60], [720, 640]) - drink * 40} s={0.9} rot={-drink * 55} fill={1 - drink} />
      ) : null}
      <Bubble x={1120} y={480} text="咕嚕咕嚕～" at={66} until={112} size={44} />

      {/* evaporation */}
      {f >= 112 && f < 200 ? <Steam x={960} y={G - 260} from={112} n={18} spread={420} size={150} rise={520} period={40} /> : null}
      <Ticks x={760} y={560} at={120} dur={40} color="#8fc4e3" scale={1.5} rot={-30} />
      <Ticks x={1160} y={560} at={124} dur={40} color="#8fc4e3" scale={1.5} rot={30} />

      {/* power-up */}
      {f >= 195 ? (
        <>
          {[0, 1, 2, 3, 4, 5].map((i) => {
            const a = (i / 6) * Math.PI * 2 + f / 30;
            const r = 230 + wave(f, 20, 14, i * 4);
            return (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: 960 + Math.cos(a) * r - 18,
                  top: G - 170 + Math.sin(a) * r * 0.7 - 18,
                  fontSize: 36,
                  color: "#f2b632",
                  opacity: tw(f, [195, 210], [0, 1]),
                }}
              >
                ✦
              </div>
            );
          })}
          <div
            style={{
              position: "absolute",
              top: 150,
              width: "100%",
              textAlign: "center",
              fontFamily: BRUSH,
              fontWeight: 700,
              fontSize: 130,
              color: "#c2602f",
              letterSpacing: 16,
              transform: `scale(${tw(f, [205, 220], [0.3, 1], (t) => 1 - Math.pow(1 - t, 3))}) rotate(-3deg)`,
              opacity: tw(f, [205, 215], [0, 1]),
              textShadow: "0 6px 0 rgba(255,210,120,0.7)",
            }}
          >
            元氣滿滿！
          </div>
        </>
      ) : null}
      <Caption
        cues={[
          [6, 58, "枸杞端來熱騰騰的四神湯——"],
          [62, 110, "「咕嚕咕嚕……」"],
          [116, 188, "身上的水氣，咻地一下全蒸發了！"],
          [196, 296, "茯苓變得苗條又精實，渾身是勁！"],
        ]}
      />
    </SceneFade>
  );
};
