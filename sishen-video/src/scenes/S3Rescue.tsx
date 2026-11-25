import React from "react";
import { useCurrentFrame } from "remotion";
import { Bubble, Caption, SceneFade, Sprite, Sweat, Ticks, tw, wave, Zzz } from "../lib/kit";
import { Bedroom, BedBack, BedBlanket } from "../lib/props";

export const S3_DUR = 450;
const G = 930; // floor line for characters

const Rope: React.FC<{ x1: number; y1: number; x2: number; y2: number; taut?: boolean }> = ({ x1, y1, x2, y2, taut = true }) => {
  const sag = taut ? 6 : 30;
  const d = `M${x1} ${y1} Q ${(x1 + x2) / 2} ${Math.max(y1, y2) + sag} ${x2} ${y2}`;
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}>
      <path d={d} stroke="#9b6b3e" strokeWidth={9} fill="none" strokeLinecap="round" />
      <path d={d} stroke="#d9b27c" strokeWidth={3} fill="none" strokeDasharray="8 8" />
    </svg>
  );
};

const talk = (f: number, a: number, b: number) => (f >= a && f < b ? Math.abs(Math.sin(f / 2.4)) : 0);

export const S3Rescue: React.FC = () => {
  const f = useCurrentFrame();
  const door = tw(f, [0, 8], [0, 1], (t) => 1 - Math.pow(1 - t, 3));
  const shake = wave(f, 5, 3);

  // --- entrance (0-66): helpers burst in from the right, facing left toward the bed
  const enterQ = tw(f, [6, 36], [1650, 1180]);
  const enterC = tw(f, [12, 42], [1700, 1400]);
  const hop = (s: number) => Math.abs(wave(f - s, 16, 30));

  // --- beat 1: tug-of-war (66-172)
  const pullX = tw(f, [76, 165], [800, 880]);
  // --- beat 2: drag on the rug (172-292)
  const dragX = tw(f, [178, 286], [600, 980]);
  // --- beat 3: piggy-back (292-450)
  const carryX = tw(f, [296, 440], [880, 1690]);
  const exitO = tw(f, [405, 440], [1, 0]);

  return (
    <SceneFade dur={S3_DUR}>
      <div style={{ position: "absolute", inset: 0, transformOrigin: "62% 88%", transform: `scale(${tw(f, [50, 80], [1, 1.18])})` }}>
        <Bedroom doorOpen={door} />
        <BedBack />
        {f < 66 ? (
          <>
            {/* startled awake, then burrows back under the covers */}
            <Sprite
              name="fuling_idle"
              x={735}
              y={745 - (f < 14 ? tw(f, [2, 8, 14], [0, 40, 0]) : 0) - tw(f, [56, 66], [0, 60])}
              h={230}
              shadow={0}
              sy={1 + wave(f, 70, 0.02)}
              face={
                f < 6
                  ? { e: "sleep" }
                  : f < 30
                    ? { e: "surprised", look: 1 }
                    : f < 56
                      ? { e: "tired", look: 0.8, talk: talk(f, 40, 56) }
                      : { e: "surprised", look: 1 }
              }
            />
            <BedBlanket lift={f >= 30 && f < 56 ? -16 : 0} />
            <Bubble x={640} y={540} text="再睡五分鐘……" at={38} until={58} size={36} tail="right" />
          </>
        ) : (
          <BedBlanket />
        )}

        {/* entrance */}
        {f < 66 ? (
          <>
            <Sprite name="qianshi_angry" x={enterQ} y={G} h={220} flip lift={f < 36 ? hop(6) : 0} face={{ e: "shout", look: -1, talk: talk(f, 30, 62) }} />
            <Sprite name="chuanxiong_point" x={enterC} y={G} h={240} flip lift={f < 42 ? hop(12) : 0} face={{ e: f < 44 ? "angry" : "disappointed", look: -1 }} />
            <Ticks x={enterQ - 30} y={G - 240} at={34} />
            <Bubble x={1220} y={640} text="茯苓！快起來！" at={28} until={52} size={44} tail="right" />
            <Bubble x={1420} y={600} text="又在睡……" at={50} until={66} size={38} tail="right" />
          </>
        ) : null}

        {/* beat 1: 拉 — tug of war, helpers face Fuling and lean back */}
        {f >= 66 && f < 172 ? (
          <>
            <Sprite
              name="chuanxiong_walk"
              x={pullX - 200}
              y={G}
              h={230}
              rot={16 + shake * 0.5}
              face={{ e: "strain", look: 1 }}
            />
            <Sprite
              name="fuling_idle"
              x={pullX}
              y={G}
              h={220}
              sx={1.12 + wave(f, 10, 0.04)}
              sy={0.92}
              rot={-8 + shake}
              lift={tw(f, [66, 76], [80, 0])}
              face={{ e: f < 120 ? "tired" : "sad", look: -0.4, lookY: 0.6, talk: talk(f, 96, 150), tear: f >= 120 }}
            />
            <Rope x1={pullX + 95} y1={G - 110} x2={pullX + 290} y2={G - 125} />
            <Sprite name="qianshi_idle" x={pullX + 360} y={G} h={220} flip rot={16 + shake} face={{ e: "strain", look: -1 }} />
            <Sweat x={pullX + 400} y={G - 240} at={90} period={22} />
            <Sweat x={pullX - 240} y={G - 250} at={100} period={24} />
            <Bubble x={pullX + 380} y={G - 260} text="嘿——咻！" at={80} until={110} size={40} tail="left" />
            <Bubble x={pullX - 40} y={G - 250} text="不要嘛～好睏……" at={98} until={150} size={36} tail="left" />
          </>
        ) : null}

        {/* beat 2: 拖 — Fuling fell asleep again on the rug */}
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
              {/* dust puffs behind the rug */}
              {[0, 1, 2].map((i) => {
                const t = ((f + i * 9) % 27) / 27;
                return <circle key={i} cx={dragX - 210 - t * 60} cy={G - 10 - t * 30 - i * 8} r={10 + t * 16} fill="#e9d6b8" opacity={(1 - t) * 0.8} />;
              })}
            </svg>
            <Sprite
              name="fuling_idle"
              x={dragX - 10}
              y={G - 10}
              h={210}
              rot={-86 + wave(f, 9, 2)}
              shadow={0}
              style={{ transformOrigin: "50% 75%" }}
              face={{ e: "sleep" }}
            />
            <Zzz x={dragX - 80} y={G - 140} from={180} />
            <Rope x1={dragX + 190} y1={G - 20} x2={dragX + 370} y2={G - 110} />
            <Sprite name="qianshi_run" x={dragX + 430} y={G} h={220} rot={14 + shake} face={{ e: "strain", look: 0.6 }} />
            <Rope x1={dragX + 190} y1={G - 20} x2={dragX + 580} y2={G - 120} />
            <Sprite
              name="chuanxiong_walk"
              x={dragX + 660}
              y={G}
              h={230}
              rot={12 - shake}
              face={f < 230 ? { e: "strain", look: 0.6 } : { e: "angry", look: -1, talk: talk(f, 232, 280) }}
            />
            <Sweat x={dragX + 480} y={G - 240} at={190} period={22} />
            <Sweat x={dragX + 700} y={G - 250} at={200} period={20} />
            <Bubble x={dragX + 640} y={G - 280} text="他居然又睡著了！" at={232} until={286} size={40} tail="left" />
          </>
        ) : null}

        {/* beat 3: 背 — Chuanxiong carries, Qianshi pushes */}
        {f >= 292 ? (
          <>
            <Sprite
              name="qianshi_run"
              x={carryX - 250}
              y={G}
              h={210}
              rot={18 + shake}
              opacity={exitO}
              lift={Math.abs(wave(f, 14, 6))}
              face={{ e: "determined", look: 1, talk: talk(f, 300, 340) }}
            />
            <Sprite
              name="chuanxiong_walk"
              x={carryX}
              y={G}
              h={230}
              rot={shake}
              sy={0.9 + wave(f, 14, 0.02)}
              opacity={exitO}
              lift={Math.abs(wave(f, 14, 5))}
              face={{ e: "tired", look: 1, lookY: 0.6 }}
            />
            <Sprite
              name="fuling_idle"
              x={carryX + 10}
              y={G - 190 - Math.abs(wave(f, 14, 6))}
              h={200}
              rot={-70 + wave(f, 14, 6)}
              shadow={0}
              opacity={exitO}
              face={{ e: "disappointed", lookY: 1 }}
            />
            <Sweat x={carryX + 70} y={G - 250} at={300} period={18} />
            <Sweat x={carryX + 20} y={G - 230} at={309} period={18} />
            <Bubble x={carryX - 250} y={G - 270} text="加油！一、二！" at={300} until={350} size={38} tail="left" />
            <Bubble x={carryX + 60} y={G - 400} text="呼……好重……" at={350} until={405} size={38} tail="left" />
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
