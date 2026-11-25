import React from "react";
import { useCurrentFrame } from "remotion";
import { BRUSH, INK, ROUND, Bubble, Caption, SceneFade, Sprite, SpriteName, Ticks, tw, usePop, wave } from "../lib/kit";
import { ChefHat, Lightbulb, Outdoors } from "../lib/props";
import { Fuling } from "../lib/fuling";

export const S5_DUR = 180;
const G = 930;

const CHEFS: { name: SpriteName; label: string; sub: string; hatX: number; hatY: number; hatW: number; color: string }[] = [
  { name: "danggui_tea", label: "當歸大廚", sub: "補血活血", hatX: 0.47, hatY: 0.1, hatW: 150, color: "#e9b7c3" },
  { name: "huaishan_herb", label: "淮山大廚", sub: "健脾益氣", hatX: 0.52, hatY: 0.12, hatW: 130, color: "#c9dcae" },
  { name: "gouqi_cup", label: "枸杞大廚", sub: "滋補明目", hatX: 0.6, hatY: 0.1, hatW: 120, color: "#f3b39b" },
];

export const S5Idea: React.FC = () => {
  const f = useCurrentFrame();
  const bulb = usePop(14, 8);
  const panel = tw(f, [70, 88], [1, 0]);
  return (
    <SceneFade dur={S5_DUR}>
      <Outdoors humid={0.8} sun={0} />
      <Fuling x={560} y={G} h={240} inflate={1} />
      <Sprite name="qianshi_angry" x={260} y={G + 10} h={200} rot={-88} style={{ transformOrigin: "50% 90%" }} />
      <Sprite name="chuanxiong_point" x={1200} y={G} h={260} lift={f < 30 ? tw(f, [0, 12, 24], [0, 60, 0]) : 0} />
      <Lightbulb x={1230} y={520 + wave(f, 30, 6)} s={bulb} glow={0.6 + wave(f, 12, 0.4)} />
      <Ticks x={1150} y={480} at={16} />
      <Ticks x={1320} y={470} at={18} rot={40} />
      <Bubble x={1440} y={640} text="對了！" at={20} until={70} size={52} />

      {/* chef reveal panel */}
      {f >= 70 ? (
        <div
          style={{
            position: "absolute",
            inset: 0,
            transform: `translateY(${panel * 1100}px)`,
            background: "linear-gradient(#fbf1dd, #f3e0bf)",
          }}
        >
          <div style={{ position: "absolute", top: 60, width: "100%", textAlign: "center", fontFamily: BRUSH, fontWeight: 700, fontSize: 96, color: INK, letterSpacing: 12 }}>
            藥膳三大廚神
          </div>
          {CHEFS.map((c, i) => {
            const p = usePopAt(f, 86 + i * 16);
            const cx = 420 + i * 540;
            const h = 420;
            return (
              <div key={c.name} style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, opacity: Math.min(1, p * 1.5) }}>
                <div
                  style={{
                    position: "absolute",
                    left: cx - 220,
                    top: 220,
                    width: 440,
                    height: 690,
                    borderRadius: 40,
                    background: c.color,
                    border: `5px solid ${INK}`,
                    transform: `scale(${p}) rotate(${(i - 1) * 2}deg)`,
                  }}
                />
                <div style={{ transform: `translateY(${(1 - p) * 80}px)` }}>
                  <Sprite name={c.name} x={cx} y={730} h={h} lift={Math.abs(wave(f, 30, 10, i * 10))} shadow={0.15} />
                  <ChefHat x={cx - 210 + c.hatX * 420} y={730 - h + c.hatY * h - Math.abs(wave(f, 30, 10, i * 10))} w={c.hatW} rot={(i - 1) * 8} />
                </div>
                <div
                  style={{
                    position: "absolute",
                    left: cx - 200,
                    width: 400,
                    top: 748,
                    textAlign: "center",
                    fontFamily: ROUND,
                    transform: `scale(${p})`,
                  }}
                >
                  <div style={{ fontSize: 58, color: INK }}>{c.label}</div>
                  <div style={{ fontSize: 34, color: "#8a6a48" }}>{c.sub}</div>
                </div>
              </div>
            );
          })}
        </div>
      ) : null}
      <Caption
        cues={[
          [8, 68, "「對了！去找三位藥膳廚神幫忙！」"],
          [130, 178, "當歸、淮山、枸杞——廚神登場！"],
        ]}
      />
    </SceneFade>
  );
};

// spring-like pop usable inside loops (no hooks)
const usePopAt = (f: number, at: number) => {
  const t = Math.max(0, f - at) / 14;
  if (t <= 0) return 0;
  if (t >= 1.6) return 1;
  return 1 - Math.cos(t * 4.2) * Math.exp(-t * 3.2);
};
