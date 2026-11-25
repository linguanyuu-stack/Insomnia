import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Bubble, Caption, HeartBurst, SceneFade, Sprite, SpriteName, Ticks, tw, wave } from "../lib/kit";
import { Bush, Outdoors, Rose } from "../lib/props";
import { Fuling } from "../lib/fuling";
import { Petals3D } from "../three/ThreeBits";

export const S8_DUR = 360;
const G = 930;

const FRIENDS: { name: SpriteName; h: number; dx: number }[] = [
  { name: "qianshi_idle", h: 200, dx: -200 },
  { name: "chuanxiong_idle", h: 220, dx: -95 },
  { name: "danggui_tea", h: 250, dx: 15 },
  { name: "huaishan_calm", h: 240, dx: 125 },
  { name: "gouqi_cup", h: 220, dx: 225 },
];
const CHEER: SpriteName[] = ["qianshi_run", "chuanxiong_point", "danggui_water", "huaishan_herb", "gouqi_cup"];

export const S8Propose: React.FC = () => {
  const f = useCurrentFrame();
  const door = tw(f, [150, 166], [0, 1]);
  // fuling path: pick rose at bush, run to door
  const fx = f < 40 ? 250 : tw(f, [40, 110], [250, 1440]);
  const running = f >= 40 && f < 110;
  const kneel = tw(f, [166, 180], [0, 1]);
  const accepted = f >= 250;
  const burst = 282;
  const bushX = 640;

  // rose position: in fuling's hand → offered → in lianzi's hand
  const roseX = accepted ? tw(f, [250, 262], [1560, 1640]) : fx + 95 + kneel * 40;
  const roseY = accepted ? tw(f, [250, 262], [700, 640]) : G - 190 - (running ? Math.abs(wave(f, 14, 26)) : 0) - kneel * 30 + (f < 32 ? tw(f, [16, 32], [80, 0]) : 0);
  const roseR = accepted ? 10 : 20 + kneel * 40;

  return (
    <SceneFade dur={S8_DUR}>
      <Outdoors sun={1} house doorOpen={door} />
      {/* rose bush where he picks the flower */}
      <Bush x={200} y={G - 10} w={300} />

      {/* lianzi at the door */}
      {f >= 160 ? (
        <Sprite
          name={f < 205 ? "lianzi_surprise" : accepted && f > 268 ? "lianzi_leaf" : "lianzi_idle"}
          x={1670}
          y={812}
          h={f > 268 ? 230 : 210}
          shadow={0.15}
          opacity={tw(f, [160, 168], [0, 1])}
          lift={f > 268 ? Math.abs(wave(f, 22, 30)) : 0}
        />
      ) : null}

      {/* the friends peeking over the hedge */}
      {FRIENDS.map((fr, i) => {
        const out = f >= burst;
        const peek = f > 70 ? tw(f, [70 + i * 4, 82 + i * 4], [0, 1]) : 0;
        const giggle = f > 200 && f < burst ? wave(f, 6, 4, i * 2) : 0;
        const bob = !out ? -60 + peek * (180 + Math.abs(wave(f, 40, 14, i * 9))) : 0;
        const runX = out ? tw(f, [burst, burst + 40], [0, 1]) : 0;
        const x = bushX + fr.dx + runX * (260 + i * 120);
        const y = out ? G + 40 - runX * 40 : G + 40;
        return (
          <Sprite
            key={fr.name}
            name={out ? CHEER[i] : fr.name}
            x={x}
            y={y}
            h={fr.h}
            lift={out ? Math.abs(wave(f, 16, 70, i * 5)) : bob}
            rot={giggle}
            shadow={out ? 0.2 : 0}
          />
        );
      })}
      {f < burst ? <Bush x={bushX} y={G + 70} w={600} flowers={false} /> : null}
      {f >= 200 && f < burst ? <Bubble x={bushX} y={G - 210} text="嘻嘻嘻……" at={200} until={burst - 2} size={36} tail="none" /> : null}

      {/* fuling */}
      <Fuling
        x={fx}
        y={G}
        h={250}
        slim={1}
        muscle={f < 160 ? 0.0 : 0}
        pose={f >= 166 && f < 250 ? "fuling_shy" : "fuling_idle"}
        lift={running ? Math.abs(wave(f, 14, 26)) : kneel * -26}
        rot={kneel * 10}
      />
      <Rose x={roseX} y={roseY} s={0.75} rot={roseR} />
      <Ticks x={250} y={G - 300} at={24} />

      {/* doorbell */}
      <Ticks x={1790} y={640} at={118} dur={30} color="#e0475f" rot={20} />
      <Bubble x={1760} y={580} text="叮咚～♪" at={118} until={152} size={44} tail="right" />

      <HeartBurst x={1600} y={640} from={205} to={330} n={10} spread={260} />

      {f >= burst ? (
        <AbsoluteFill>
          <Petals3D confetti n={120} burstAt={burst} />
        </AbsoluteFill>
      ) : null}
      <Caption
        cues={[
          [6, 62, "茯苓摘下一朵玫瑰，"],
          [66, 150, "一路衝到蓮子家，按下門鈴——"],
          [168, 240, "「蓮子，這朵花……送給妳！」"],
          [244, 288, "蓮子又驚又喜，收下了花！"],
          [292, 358, "躲在一旁偷看的大家，全都衝出來歡呼！"],
        ]}
      />
    </SceneFade>
  );
};
