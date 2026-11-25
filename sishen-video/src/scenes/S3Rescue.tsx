import React from "react";
import { useCurrentFrame } from "remotion";
import { Bubble, Caption, SceneFade, Sprite, Sweat, Ticks, tw, wave } from "../lib/kit";
import { Bedroom, BedBack, BedBlanket } from "../lib/props";

export const S3_DUR = 450;
const G = 930; // floor line for characters

const Rope: React.FC<{ x1: number; y1: number; x2: number; y2: number }> = ({ x1, y1, x2, y2 }) => (
  <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}>
    <path d={`M${x1} ${y1} Q ${(x1 + x2) / 2} ${Math.max(y1, y2) + 14} ${x2} ${y2}`} stroke="#9b6b3e" strokeWidth={8} fill="none" strokeLinecap="round" />
    <path d={`M${x1} ${y1} Q ${(x1 + x2) / 2} ${Math.max(y1, y2) + 14} ${x2} ${y2}`} stroke="#d9b27c" strokeWidth={3} fill="none" strokeDasharray="8 8" />
  </svg>
);

export const S3Rescue: React.FC = () => {
  const f = useCurrentFrame();
  const door = tw(f, [0, 12], [0, 1]);
  const shake = wave(f, 5, 3);

  // --- entrance (0-60)
  const enterQ = tw(f, [8, 40], [1650, 1180]);
  const enterC = tw(f, [14, 46], [1680, 1420]);
  const hop = (s: number) => Math.abs(wave(f - s, 16, 30));

  // --- beat 1: pull (60-170)
  const pullX = tw(f, [70, 165], [820, 900]);

  // --- beat 2: drag (170-290)
  const dragX = tw(f, [175, 285], [620, 1000]);

  // --- beat 3: carry (290-450)
  const carryX = tw(f, [295, 440], [900, 1700]);
  const exitO = tw(f, [400, 440], [1, 0]);

  return (
    <SceneFade dur={S3_DUR}>
      <div style={{ position: "absolute", inset: 0, transformOrigin: "62% 88%", transform: `scale(${tw(f, [50, 80], [1, 1.18])})` }}>
      <Bedroom doorOpen={door} />
      <BedBack />
      {f < 66 ? (
        <>
          <Sprite name="fuling_shy" x={735} y={745 - tw(f, [56, 66], [0, 60])} h={230} shadow={0} sy={1 + wave(f, 70, 0.02)} />
          <BedBlanket />
        </>
      ) : (
        <BedBlanket />
      )}

      {/* entrance */}
      {f < 66 ? (
        <>
          <Sprite name="qianshi_angry" x={enterQ} y={G} h={220} lift={f < 40 ? hop(8) : 0} />
          <Sprite name="chuanxiong_point" x={enterC} y={G} h={240} flip lift={f < 46 ? hop(14) : 0} />
          <Ticks x={enterQ - 20} y={G - 230} at={40} />
          <Bubble x={1280} y={640} text="茯苓！快起來！" at={36} until={66} size={44} />
        </>
      ) : null}

      {/* beat 1: 拉 */}
      {f >= 66 && f < 172 ? (
        <>
          <Sprite name="chuanxiong_walk" x={pullX - 190} y={G} h={230} rot={14 + shake * 0.5} />
          <Sprite name="fuling_idle" x={pullX} y={G} h={220} sx={1.18 + wave(f, 10, 0.04)} sy={0.9} rot={shake} lift={tw(f, [66, 76], [80, 0])} />
          <Rope x1={pullX + 90} y1={G - 110} x2={pullX + 290} y2={G - 120} />
          <Sprite name="qianshi_run" x={pullX + 360} y={G} h={220} rot={-16 + shake} />
          <Sweat x={pullX + 400} y={G - 230} at={90} />
          <Sweat x={pullX - 220} y={G - 250} at={100} />
          <Bubble x={pullX + 360} y={G - 250} text="嘿——咻！" at={84} until={160} size={40} />
        </>
      ) : null}

      {/* beat 2: 拖 */}
      {f >= 172 && f < 292 ? (
        <>
          <svg width={1920} height={1080} style={{ position: "absolute" }}>
            <g transform={`translate(${dragX - 190} ${G - 40})`}>
              <rect x={0} y={0} width={380} height={50} rx={10} fill="#c9b8e6" stroke="#5a3b22" strokeWidth={5} />
              {Array.from({ length: 8 }).map((_, i) => (
                <line key={i} x1={20 + i * 46} y1={0} x2={20 + i * 46} y2={50} stroke="#fff" strokeWidth={10} opacity={0.6} />
              ))}
              <line x1={0} y1={25} x2={380} y2={25} stroke="#fff" strokeWidth={10} opacity={0.6} />
            </g>
          </svg>
          <Sprite name="fuling_shy" x={dragX - 10} y={G - 10} h={210} rot={-88 + wave(f, 9, 2)} shadow={0} style={{ transformOrigin: "50% 75%" }} />
          <Rope x1={dragX + 190} y1={G - 20} x2={dragX + 360} y2={G - 110} />
          <Sprite name="qianshi_run" x={dragX + 420} y={G} h={220} rot={-14 + shake} />
          <Rope x1={dragX + 190} y1={G - 20} x2={dragX + 560} y2={G - 120} />
          <Sprite name="chuanxiong_walk" x={dragX + 640} y={G} h={230} rot={-12 - shake} />
          <Sweat x={dragX + 470} y={G - 240} at={190} />
          <Sweat x={dragX + 690} y={G - 250} at={200} />
          <Bubble x={dragX + 560} y={G - 270} text="重～死～了～" at={200} until={285} size={40} />
        </>
      ) : null}

      {/* beat 3: 背 */}
      {f >= 292 ? (
        <>
          <Sprite name="qianshi_run" x={carryX - 260} y={G} h={210} rot={10 + shake} opacity={exitO} lift={Math.abs(wave(f, 14, 8))} />
          <Sprite name="chuanxiong_walk" x={carryX} y={G} h={230} rot={shake} sy={0.92} opacity={exitO} lift={Math.abs(wave(f, 14, 6))} />
          <Sprite
            name="fuling_shy"
            x={carryX + 10}
            y={G - 190 - Math.abs(wave(f, 14, 6))}
            h={200}
            rot={-70 + wave(f, 14, 6)}
            shadow={0}
            opacity={exitO}
          />
          <Sweat x={carryX + 70} y={G - 250} at={300} period={22} />
          <Bubble x={carryX - 60} y={G - 340} text="一、二！一、二！" at={310} until={400} size={40} />
        </>
      ) : null}

      </div>
      <Caption
        cues={[
          [6, 64, "芡實和川芎，實在看不下去了！"],
          [72, 168, "用拉的——"],
          [176, 288, "用拖的——"],
          [296, 380, "用背的——"],
          [384, 448, "千辛萬苦，總算把茯苓弄出門！"],
        ]}
      />
    </SceneFade>
  );
};
