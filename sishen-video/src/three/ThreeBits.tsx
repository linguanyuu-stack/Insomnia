import React, { useLayoutEffect, useMemo } from "react";
import * as THREE from "three";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

const INK3 = "#4a2f1a";

/** deterministic pseudo random */
export const rnd = (i: number, salt = 0) => {
  const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
  return x - Math.floor(x);
};

const LookAt: React.FC<{ target: [number, number, number] }> = ({ target }) => {
  const camera = useThree((s) => s.camera);
  useLayoutEffect(() => {
    camera.lookAt(...target);
    camera.updateProjectionMatrix();
  });
  return null;
};

/** Toon-shaded mesh with an inverted-hull ink outline, to match the hand-drawn sheets */
const Inked: React.FC<{
  geometry: THREE.BufferGeometry;
  color: string;
  outline?: number;
  position?: [number, number, number];
  rotation?: [number, number, number];
  scale?: number | [number, number, number];
  gradient: THREE.Texture;
}> = ({ geometry, color, outline = 0.06, position, rotation, scale = 1, gradient }) => {
  const s: [number, number, number] = typeof scale === "number" ? [scale, scale, scale] : scale;
  return (
    <group position={position} rotation={rotation} scale={s}>
      <mesh geometry={geometry}>
        <meshToonMaterial color={color} gradientMap={gradient} />
      </mesh>
      <mesh geometry={geometry} scale={1 + outline}>
        <meshBasicMaterial color={INK3} side={THREE.BackSide} />
      </mesh>
    </group>
  );
};

const useToonGradient = () =>
  useMemo(() => {
    const data = new Uint8Array([150, 150, 150, 255, 215, 215, 215, 255, 255, 255, 255, 255]);
    const t = new THREE.DataTexture(data, 3, 1, THREE.RGBAFormat);
    t.minFilter = THREE.NearestFilter;
    t.magFilter = THREE.NearestFilter;
    t.needsUpdate = true;
    return t;
  }, []);

/* ------------------------------------------------------------------ */
/* Soup pot                                                            */
/* ------------------------------------------------------------------ */

export type Ingredient = {
  key: string;
  at: number; // frame it drops in
  color: string;
  kind: "slice" | "ball" | "cube" | "goji" | "lump" | "flat";
  count: number;
};

export const INGREDIENTS: Ingredient[] = [
  { key: "當歸", at: 40, color: "#e8cf98", kind: "flat", count: 3 },
  { key: "川芎", at: 70, color: "#b98a52", kind: "lump", count: 2 },
  { key: "淮山", at: 120, color: "#f6eedd", kind: "slice", count: 4 },
  { key: "蓮子", at: 150, color: "#f3e6c6", kind: "ball", count: 4 },
  { key: "茯苓", at: 180, color: "#fbf7ee", kind: "cube", count: 4 },
  { key: "芡實", at: 210, color: "#a8584a", kind: "ball", count: 4 },
  { key: "枸杞", at: 250, color: "#e0412f", kind: "goji", count: 6 },
];

export const SoupPot3D: React.FC<{ width: number; height: number; stirFrom?: number }> = ({ width, height, stirFrom = 280 }) => {
  const frame = useCurrentFrame();
  const gradient = useToonGradient();

  const geo = useMemo(() => {
    const pts: THREE.Vector2[] = [];
    // pot profile (radius, height)
    const prof: [number, number][] = [
      [0, -1.2],
      [1.5, -1.2],
      [2.05, -0.9],
      [2.35, -0.3],
      [2.4, 0.3],
      [2.3, 0.85],
      [2.45, 1.0],
      [2.38, 1.08],
      [2.15, 0.95],
    ];
    prof.forEach(([r, y]) => pts.push(new THREE.Vector2(r, y)));
    return {
      pot: new THREE.LatheGeometry(pts, 48),
      soup: new THREE.CircleGeometry(2.12, 48),
      slice: new THREE.CylinderGeometry(0.32, 0.32, 0.09, 20),
      ball: new THREE.SphereGeometry(0.22, 18, 14),
      cube: new THREE.BoxGeometry(0.34, 0.34, 0.34),
      goji: new THREE.SphereGeometry(0.12, 14, 10),
      lump: new THREE.DodecahedronGeometry(0.3, 0),
      flat: new THREE.BoxGeometry(0.62, 0.05, 0.28),
      handle: new THREE.TorusGeometry(0.36, 0.11, 10, 24, Math.PI),
      spoon: new THREE.CylinderGeometry(0.07, 0.07, 3.2, 10),
      flower: new THREE.CircleGeometry(0.22, 5),
    };
  }, []);

  // soup colour: clear water → amber broth
  const brew = interpolate(frame, [40, 300], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const soupColor = new THREE.Color("#cfe3e6").lerp(new THREE.Color("#d29a4e"), brew);
  const stir = Math.max(0, frame - stirFrom);
  const swirl = frame * 0.012 + stir * 0.05;

  const pieces: React.ReactNode[] = [];
  INGREDIENTS.forEach((ing, gi) => {
    for (let k = 0; k < ing.count; k++) {
      const start = ing.at + k * 4;
      const t = frame - start;
      if (t < 0) continue;
      const seed = gi * 10 + k;
      const r = 0.45 + rnd(seed, 1) * 1.35;
      const a0 = rnd(seed, 2) * Math.PI * 2;
      const fall = interpolate(t, [0, 16], [5.5, 0.95], { extrapolateRight: "clamp", easing: Easing.in(Easing.quad) });
      const bob = t > 16 ? Math.sin((frame + seed * 7) / 14) * 0.04 : 0;
      const ang = a0 + (t > 16 ? swirl * (1.4 - r * 0.3) : 0);
      const x = Math.cos(ang) * r;
      const z = Math.sin(ang) * r;
      const geom = geo[ing.kind];
      const sc: [number, number, number] = ing.kind === "goji" ? [1, 1, 1.9] : [1, 1, 1];
      pieces.push(
        <Inked
          key={`${gi}-${k}`}
          geometry={geom}
          color={ing.color}
          gradient={gradient}
          outline={0.12}
          position={[x, fall + bob, z]}
          rotation={[rnd(seed, 3) * 3 + t * 0.02, ang + rnd(seed, 4) * 2, rnd(seed, 5) * 0.6]}
          scale={sc}
        />,
      );
      // splash ring
      if (t >= 16 && t < 34 && k === 0) {
        const p = (t - 16) / 18;
        pieces.push(
          <mesh key={`sp-${gi}`} position={[x, 0.97, z]} rotation={[-Math.PI / 2, 0, 0]}>
            <ringGeometry args={[0.2 + p * 0.8, 0.28 + p * 0.8, 32]} />
            <meshBasicMaterial color="#ffffff" transparent opacity={1 - p} />
          </mesh>,
        );
      }
    }
  });

  const spoonAng = stir > 0 ? stir * 0.12 : 0.6;

  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 7.4, 9.2], fov: 40 }}>
      <LookAt target={[0, 0.6, 0]} />
      <ambientLight intensity={1.4} />
      <directionalLight position={[4, 8, 5]} intensity={2.2} />
      <group rotation={[0, Math.sin(frame / 90) * 0.08, 0]}>
        <mesh geometry={geo.pot}>
          <meshToonMaterial color="#f4ead6" gradientMap={gradient} side={THREE.DoubleSide} />
        </mesh>
        <mesh geometry={geo.pot} scale={[1.035, 1.02, 1.035]}>
          <meshBasicMaterial color={INK3} side={THREE.BackSide} />
        </mesh>
        {/* painted lotus band */}
        {Array.from({ length: 6 }).map((_, i) => {
          const a = (i / 6) * Math.PI * 2 + 0.3;
          return (
            <mesh key={i} geometry={geo.flower} position={[Math.cos(a) * 2.41, 0.05, Math.sin(a) * 2.41]} rotation={[0, -a + Math.PI / 2, 0]}>
              <meshBasicMaterial color="#ee9aac" side={THREE.DoubleSide} />
            </mesh>
          );
        })}
        {/* handles */}
        <group position={[2.45, 0.55, 0]} rotation={[0, 0, -Math.PI / 2]}>
          <Inked geometry={geo.handle} color="#f4ead6" gradient={gradient} outline={0.1} />
        </group>
        <group position={[-2.45, 0.55, 0]} rotation={[0, 0, Math.PI / 2]}>
          <Inked geometry={geo.handle} color="#f4ead6" gradient={gradient} outline={0.1} />
        </group>
        {/* soup */}
        <mesh geometry={geo.soup} position={[0, 0.92, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <meshToonMaterial color={soupColor} gradientMap={gradient} />
        </mesh>
        {pieces}
        {/* ladle */}
        <group position={[Math.cos(spoonAng) * 1.1, 1.9, Math.sin(spoonAng) * 1.1]} rotation={[0.25, 0, -0.35]}>
          <Inked geometry={geo.spoon} color="#b07a4c" gradient={gradient} outline={0.25} />
        </group>
      </group>
    </ThreeCanvas>
  );
};

/* ------------------------------------------------------------------ */
/* Falling petals / confetti                                           */
/* ------------------------------------------------------------------ */

const PETAL_COLORS = ["#f6b3c2", "#f8c9d3", "#f2a0b4", "#fde3e8", "#f9d77e", "#b9e09a"];
const CONFETTI_COLORS = ["#f07f95", "#ffd36e", "#8fc4e3", "#9cc477", "#c9a6d4", "#ff9f6b", "#ffffff"];

export const Petals3D: React.FC<{ n?: number; from?: number; confetti?: boolean; burstAt?: number }> = ({
  n = 50,
  from = 0,
  confetti = false,
  burstAt = 0,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const gradient = useToonGradient();
  const geos = useMemo(() => {
    const shape = new THREE.Shape();
    shape.moveTo(0, -0.22);
    shape.bezierCurveTo(0.2, -0.1, 0.18, 0.18, 0, 0.24);
    shape.bezierCurveTo(-0.18, 0.18, -0.2, -0.1, 0, -0.22);
    const heart = new THREE.Shape();
    heart.moveTo(0, -0.2);
    heart.bezierCurveTo(-0.3, 0, -0.25, 0.25, 0, 0.12);
    heart.bezierCurveTo(0.25, 0.25, 0.3, 0, 0, -0.2);
    return {
      petal: new THREE.ShapeGeometry(shape, 8),
      rect: new THREE.PlaneGeometry(0.16, 0.3),
      heart: new THREE.ShapeGeometry(heart, 8),
    };
  }, []);
  const t = frame - from;
  if (t < 0) return null;
  const items: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    let x: number, y: number, z: number;
    if (confetti) {
      // two cannons from bottom corners
      const side = i % 2 === 0 ? -1 : 1;
      const tt = Math.max(0, frame - burstAt - (i % 7)) / 30;
      const vx = -side * (1.5 + rnd(i, 1) * 4.5);
      const vy = 6 + rnd(i, 2) * 6;
      x = side * 7 + vx * tt + Math.sin(tt * 3 + i) * 0.3;
      y = -4.5 + vy * tt - 0.5 * 7.5 * tt * tt;
      y = Math.max(y, -4.8 - tt * 0.6);
      z = (rnd(i, 3) - 0.5) * 4;
      if (frame < burstAt) continue;
    } else {
      const speed = 0.012 + rnd(i, 1) * 0.012;
      const cy = ((rnd(i, 2) * 12 + t * speed * 30) % 12) - 6;
      x = (rnd(i, 3) - 0.5) * 18 + Math.sin(t / 30 + i) * 0.6;
      y = -cy;
      z = (rnd(i, 4) - 0.5) * 6;
    }
    const colors = confetti ? CONFETTI_COLORS : PETAL_COLORS;
    const geom = confetti ? (i % 5 === 0 ? geos.heart : geos.rect) : i % 9 === 0 ? geos.heart : geos.petal;
    const s = confetti ? 1 + rnd(i, 6) * 0.6 : 0.8 + rnd(i, 6) * 0.7;
    items.push(
      <mesh
        key={i}
        geometry={geom}
        position={[x, y, z]}
        rotation={[t * (0.03 + rnd(i, 7) * 0.06) + i, t * (0.02 + rnd(i, 8) * 0.05), t * 0.02 + i]}
        scale={[s, s, s]}
      >
        <meshToonMaterial color={confetti ? colors[i % colors.length] : i % 9 === 0 ? "#f07f95" : colors[i % colors.length]} gradientMap={gradient} side={THREE.DoubleSide} />
      </mesh>,
    );
  }
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 0, 10], fov: 50 }} style={{ position: "absolute", inset: 0 }}>
      <ambientLight intensity={1.6} />
      <directionalLight position={[3, 5, 6]} intensity={1.8} />
      {items}
    </ThreeCanvas>
  );
};
