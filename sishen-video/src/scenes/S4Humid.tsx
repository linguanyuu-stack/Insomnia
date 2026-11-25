import React from "react";
import { useCurrentFrame } from "remotion";
import { Bubble, Caption, SceneFade, Sprite, Sweat, Ticks, tw, wave, lin } from "../lib/kit";
import { Drop, Outdoors } from "../lib/props";
import { Fuling } from "../lib/fuling";
import { rnd } from "../three/ThreeBits";

export const S4_DUR = 300;
const G = 930;

export const S4Humid: React.FC = () => {
  const f = useCurrentFrame();
  const humid = tw(f, [0, 70], [0.35, 1]);
  const walkX = tw(f, [0, 50], [-150, 860]);
  const inflate = tw(f, [70, 190], [0, 1], (t) => t * t * (3 - 2 * t));
  const fx = 960;
  const collapse = tw(f, [246, 262], [0, 1]);
  const push = f >= 200 && f < 246;
  const shake = wave(f, 5, 3);

  // converging droplets
  const drops: React.ReactNode[] = [];
  for (let i = 0; i < 40; i++) {
    const start = 60 + i * 3.2;
    const t = (f - start) / 26;
    if (t < 0 || t > 1) continue;
    const ang = rnd(i, 1) * Math.PI * 2;
    const r0 = 700 + rnd(i, 2) * 300;
    const sx = fx + Math.cos(ang) * r0;
    const sy = 600 + Math.sin(ang) * r0 * 0.6;
    const ex = fx + (rnd(i, 3) - 0.5) * 120;
    const ey = G - 160 + (rnd(i, 4) - 0.5) * 80;
    drops.push(<Drop key={i} x={sx + (ex - sx) * t} y={sy + (ey - sy) * t} s={1.4 - t * 0.6} opacity={lin(t, [0, 0.2, 0.85, 1], [0, 1, 1, 0])} />);
  }

  return (
    <SceneFade dur={S4_DUR}>
      <Outdoors humid={humid} sun={0} />
      {f < 52 ? (
        <>
          <Sprite name="qianshi_run" x={walkX - 260} y={G} h={210} rot={16} lift={Math.abs(wave(f, 14, 8))} face={{ e: "determined", look: 1 }} />
          <Sprite name="chuanxiong_walk" x={walkX} y={G} h={230} sy={0.92} lift={Math.abs(wave(f, 14, 6))} face={{ e: "tired", look: 1, lookY: 0.5 }} />
          <Sprite name="fuling_idle" x={walkX + 10} y={G - 190} h={200} rot={-70 + wave(f, 14, 6)} shadow={0} face={{ e: "tired", lookY: -0.5 }} />
        </>
      ) : (
        <>
          {/* helpers */}
          <Sprite
            name={push ? "qianshi_run" : "qianshi_idle"}
            x={push ? tw(f, [200, 215], [620, 680]) : 620}
            y={G + collapse * 10}
            h={210}
            rot={push ? 20 + shake : collapse * -88}
            style={{ transformOrigin: collapse > 0 ? "50% 90%" : "50% 100%" }}
            face={
              collapse > 0
                ? { e: "dizzy" }
                : push
                  ? { e: "strain", look: 1 }
                  : f < 100
                    ? { e: "smile", look: 1 }
                    : { e: "surprised", look: 1, lookY: -0.6 }
            }
          />
          <Sprite
            name={push ? "chuanxiong_walk" : "chuanxiong_idle"}
            x={push ? tw(f, [200, 215], [1320, 1260]) : 1320}
            y={G + collapse * 10}
            h={230}
            flip
            rot={push ? -20 - shake : collapse * 88}
            style={{ transformOrigin: collapse > 0 ? "50% 90%" : "50% 100%" }}
            face={
              collapse > 0
                ? { e: "dizzy" }
                : push
                  ? { e: "strain", look: -1 }
                  : f < 110
                    ? { e: "tired", look: -1 }
                    : { e: "surprised", look: -1, lookY: -0.6 }
            }
          />
          <Fuling
            x={fx}
            y={G}
            h={240}
            pose="fuling_idle"
            inflate={inflate}
            lift={tw(f, [52, 62], [190, 0])}
            face={
              f < 75
                ? { e: "tired" }
                : f < 125
                  ? { e: "surprised", look: Math.sin(f / 9) }
                  : f < 200
                    ? { e: "sad", lookY: 0.7, tear: true, talk: f > 128 && f < 190 ? Math.abs(Math.sin(f / 2.5)) : 0 }
                    : f < 246
                      ? { e: "nervous", look: Math.sin(f / 6) }
                      : { e: "disappointed", lookY: 1, tear: true }
            }
          />
          {drops}
          <Ticks x={fx - 230} y={G - 380} at={150} dur={40} color="#4d8fb8" rot={-20} scale={1.3} />
          <Ticks x={fx + 230} y={G - 380} at={160} dur={40} color="#4d8fb8" rot={20} scale={1.3} />
          {push ? (
            <>
              <Sweat x={700} y={G - 240} at={200} period={20} />
              <Sweat x={1260} y={G - 250} at={205} period={20} />
            </>
          ) : null}
          <Bubble x={fx + 60} y={G - 420} text="咦？身體好重……" at={120} until={196} size={42} />
          <Bubble x={980} y={G - 470} text="推～不～動～啦～" at={262} until={299} size={44} tail="none" />
          {collapse >= 1 ? (
            <>
              <Sweat x={560} y={G - 120} at={262} />
              <Sweat x={1380} y={G - 120} at={268} />
            </>
          ) : null}
        </>
      )}
      <Caption
        cues={[
          [6, 64, "沒想到，外頭的濕氣更重……"],
          [70, 196, "茯苓吸飽了水氣，腫成一大團！"],
          [204, 296, "芡實和川芎，再也拖不動了……"],
        ]}
      />
    </SceneFade>
  );
};
