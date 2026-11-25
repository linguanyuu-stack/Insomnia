import React from "react";
import { useCurrentFrame } from "remotion";
import { Sprite, SpriteName, wave } from "./kit";

/**
 * 茯苓 with body states:
 *  inflate 0..1  waterlogged & puffy (blue-tinted, jiggly)
 *  slim    0..1  slender after the soup
 *  muscle  0..1  abs + flexing arms drawn on top
 */
export const Fuling: React.FC<{
  x: number;
  y: number;
  h?: number;
  pose?: SpriteName;
  inflate?: number;
  slim?: number;
  muscle?: number;
  lift?: number;
  rot?: number;
  flip?: boolean;
  opacity?: number;
}> = ({ x, y, h = 300, pose = "fuling_idle", inflate = 0, slim = 0, muscle = 0, lift = 0, rot = 0, flip, opacity = 1 }) => {
  const f = useCurrentFrame();
  const jig = inflate > 0.05 ? wave(f, 22, 0.04 * inflate) : 0;
  const breathe = wave(f, 60, 0.012);
  const sx = (1 + inflate * 0.95 + jig) * (1 - slim * 0.2);
  const sy = (1 + inflate * 0.5 - jig * 0.8 + breathe) * (1 + slim * 0.1);
  const stroke = "#6b4426";
  return (
    <Sprite
      name={pose}
      x={x}
      y={y}
      h={h}
      sx={sx}
      sy={sy}
      lift={lift}
      rot={rot}
      flip={flip}
      opacity={opacity}
      shadow={0.25}
      tint={{ color: "#9cc9ea", amount: inflate * 0.5 }}
    >
      {inflate > 0.2 ? (
        <g opacity={(inflate - 0.2) / 0.8}>
          <ellipse cx={30} cy={22} rx={9} ry={5} fill="#fff" opacity={0.55} transform="rotate(-25 30 22)" />
          <ellipse cx={22} cy={34} rx={3} ry={2} fill="#fff" opacity={0.5} />
        </g>
      ) : null}
      {muscle > 0 ? (
        <g opacity={muscle} fill="none" stroke={stroke} strokeWidth={2.4} strokeLinecap="round">
          {/* pecs */}
          <path d="M36 60 C 42 64 48 64 50 60 M 50 60 C 52 64 58 64 64 60" />
          {/* abs */}
          <path d="M50 70 L 50 88" />
          <path d="M42 72 C 45 74 47 74 49 72 M 51 72 C 53 74 55 74 58 72" />
          <path d="M42 79 C 45 81 47 81 49 79 M 51 79 C 53 81 55 81 58 79" />
          <path d="M43 86 C 45 88 47 88 49 86 M 51 86 C 53 88 55 88 57 86" />
          {/* flexing arms */}
          <g transform={`translate(0 ${(1 - muscle) * 12})`} strokeWidth={2.2} strokeLinejoin="round">
            <path d="M22 64 C 10 66 -6 60 -10 46 C -14 34 -12 22 -6 16 C -2 10 6 10 8 16 C 10 22 6 26 2 28 C 4 36 8 42 14 44 C 18 40 24 38 28 44 C 30 50 28 58 22 64 Z" fill="#f4e9d2" />
            <path d="M-2 40 C 2 32 10 30 14 36" />
            <path d="M78 64 C 90 66 106 60 110 46 C 114 34 112 22 106 16 C 102 10 94 10 92 16 C 90 22 94 26 98 28 C 96 36 92 42 86 44 C 82 40 76 38 72 44 C 70 50 72 58 78 64 Z" fill="#f4e9d2" />
            <path d="M102 40 C 98 32 90 30 86 36" />
          </g>
        </g>
      ) : null}
    </Sprite>
  );
};
