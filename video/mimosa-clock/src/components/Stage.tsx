import React, { useEffect, useMemo, useState } from 'react';
import * as THREE from 'three';
import { useThree } from '@react-three/fiber';
import { ThreeCanvas } from '@remotion/three';
import { AbsoluteFill, cancelRender, continueRender, delayRender, Img, staticFile, useVideoConfig } from 'remotion';
import elements from '../elements.json';

export type ElName = keyof typeof elements;

/**
 * One drawing from the storyboard placed on stage.
 * x, y: centre in screen px (1920×1080) · s: scale of the 4× cut-out · z: depth (+ = closer)
 * draw: 0→1 graphite pencil lines scribble in · color: 0→1 the coloured drawing washes in
 * back: paper cut-out margin (collage) · shadow: cast shadow of the cut-out
 */
export type Piece = {
  el: ElName;
  x: number;
  y: number;
  s: number;
  rot?: number;
  z?: number;
  draw?: number;
  color?: number;
  back?: number;
  shadow?: number;
  opacity?: number;
  seed?: number;
  /** ignore the scene's night tint */
  glow?: boolean;
  key?: string;
};

export type Cam = { x?: number; y?: number; zoom?: number; rot?: number };

const FOV = 30;
const D0 = 540 / Math.tan(((FOV / 2) * Math.PI) / 180); // z=0 plane maps 1:1 to screen px

// ───────────── textures: preloaded once, stage mounts only when ready ─────────────
const cache = new Map<string, Promise<THREE.Texture>>();
const loadTexture = (file: string) => {
  if (!cache.has(file)) {
    cache.set(
      file,
      new THREE.TextureLoader().loadAsync(staticFile(file)).then((t) => {
        t.colorSpace = THREE.NoColorSpace; // pass the artwork's colours through untouched
        t.anisotropy = 8;
        return t;
      }),
    );
  }
  return cache.get(file)!;
};

function useTextures(files: string[]) {
  const key = files.join('|');
  const [map, setMap] = useState<Record<string, THREE.Texture> | null>(null);
  const [handle] = useState(() => delayRender(`textures ${files.length}`));
  useEffect(() => {
    Promise.all(files.map(loadTexture))
      .then((ts) => setMap(Object.fromEntries(files.map((f, i) => [f, ts[i]]))))
      .catch((e) => cancelRender(e));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);
  // release only after the canvas has mounted (it then holds its own delayRender until drawn)
  useEffect(() => {
    if (!map) return;
    const id = requestAnimationFrame(() => continueRender(handle));
    return () => cancelAnimationFrame(id);
  }, [map, handle]);
  return map;
}

// ───────────── shaders ─────────────
const VERT = /* glsl */ `
varying vec2 vUv;
void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;

const NOISE = /* glsl */ `
float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}
vec2 rot2(vec2 p, float a) { float c = cos(a), s = sin(a); return vec2(c * p.x - s * p.y, s * p.x + c * p.y); }`;

const FRAG = /* glsl */ `
uniform sampler2D map; uniform sampler2D backMap;
uniform float uDraw, uColor, uBack, uOpacity, uSeed;
uniform vec2 uSize; uniform vec3 uTint;
varying vec2 vUv;
${NOISE}
void main() {
  vec4 art = texture2D(map, vUv);
  float back = texture2D(backMap, vUv).r;
  vec2 q = vUv * uSize / 260.0;
  // pencil hatching: long diagonal streaks, revealed roughly from top-left to bottom-right
  vec2 h1 = rot2(q, 0.62);
  float streak = noise(vec2(h1.x * 1.3, h1.y * 16.0) + uSeed) * 0.7 + noise(q * 3.0 + uSeed) * 0.3;
  float order = vUv.x * 0.55 + (1.0 - vUv.y) * 0.45;
  float thrD = order * 0.5 + streak * 0.5;
  float sk = smoothstep(thrD, thrD + 0.07, uDraw * 1.12);
  // colour washes in along a different hatch angle
  vec2 h2 = rot2(q, -0.5);
  float wash = noise(vec2(h2.x * 1.1, h2.y * 9.0) + uSeed * 1.7) * 0.6 + noise(q * 2.0 - uSeed) * 0.4;
  float thrC = order * 0.45 + wash * 0.55;
  float col = smoothstep(thrC, thrC + 0.16, uColor * 1.2);
  float lum = dot(art.rgb, vec3(0.299, 0.587, 0.114));
  float line = art.a * smoothstep(0.80, 0.40, lum);
  vec3 graphite = vec3(0.33, 0.30, 0.28);
  float aS = line * sk * 0.9 * (1.0 - col);
  float aC = art.a * col;
  float a = aC + aS * (1.0 - aC);
  vec3 rgb = (art.rgb * aC + graphite * aS * (1.0 - aC)) / max(a, 1e-4);
  // scissor-cut paper backing
  float bA = back * uBack;
  vec3 paper = vec3(1.0, 0.982, 0.955) - 0.035 * noise(q * 18.0);
  float A = a + bA * (1.0 - a);
  vec3 RGB = (rgb * a + paper * bA * (1.0 - a)) / max(A, 1e-4);
  gl_FragColor = vec4(RGB * uTint, A * uOpacity);
}`;

const SHADOW_FRAG = /* glsl */ `
uniform sampler2D map; uniform sampler2D backMap; uniform float uBack, uAmt;
varying vec2 vUv;
void main() {
  float b = texture2D(backMap, vUv, 3.0).r * uBack;
  float a = texture2D(map, vUv, 3.0).a * (1.0 - uBack);
  gl_FragColor = vec4(0.23, 0.16, 0.10, (b + a) * uAmt * 0.32);
}`;

const PieceMesh: React.FC<{ p: Piece; tex: Record<string, THREE.Texture>; order: number; night: number }> = ({ p, tex, order, night }) => {
  const info = elements[p.el];
  const mat = useMemo(
    () =>
      new THREE.ShaderMaterial({
        uniforms: {
          map: { value: tex[info.file] },
          backMap: { value: tex[info.back] },
          uDraw: { value: 1 },
          uColor: { value: 1 },
          uBack: { value: 0 },
          uOpacity: { value: 1 },
          uSeed: { value: 0 },
          uSize: { value: new THREE.Vector2(info.w, info.h) },
          uTint: { value: new THREE.Vector3(1, 1, 1) },
        },
        vertexShader: VERT,
        fragmentShader: FRAG,
        transparent: true,
        depthTest: false,
        depthWrite: false,
      }),
    [info, tex],
  );
  const shadowMat = useMemo(
    () =>
      new THREE.ShaderMaterial({
        uniforms: { map: { value: tex[info.file] }, backMap: { value: tex[info.back] }, uBack: { value: 0 }, uAmt: { value: 0 } },
        vertexShader: VERT,
        fragmentShader: SHADOW_FRAG,
        transparent: true,
        depthTest: false,
        depthWrite: false,
      }),
    [info, tex],
  );
  const u = mat.uniforms;
  u.uDraw.value = p.draw ?? 1;
  u.uColor.value = p.color ?? 1;
  u.uBack.value = p.back ?? 0;
  u.uOpacity.value = p.opacity ?? 1;
  u.uSeed.value = p.seed ?? (p.el.length * 7.13) % 10;
  const nt = p.glow ? 0 : night;
  (u.uTint.value as THREE.Vector3).set(1 - 0.26 * nt, 1 - 0.2 * nt, 1 - 0.02 * nt);
  shadowMat.uniforms.uBack.value = p.back ?? 0;
  shadowMat.uniforms.uAmt.value = (p.shadow ?? 0) * (p.opacity ?? 1) * Math.min(1, (p.color ?? 1) * 1.5 + (p.back ?? 0));

  const z = p.z ?? 0;
  const k = (D0 - z) / D0;
  const s = p.s * k;
  const lift = 1 + 0.02 * (p.shadow ?? 0);
  return (
    <group position={[(p.x - 960) * k, -(p.y - 540) * k, z]} rotation={[0, 0, (-(p.rot ?? 0) * Math.PI) / 180]}>
      {(p.shadow ?? 0) > 0.001 ? (
        <mesh position={[14 * k, -20 * k, 0]} scale={[s * lift, s * lift, 1]} renderOrder={order * 2} material={shadowMat}>
          <planeGeometry args={[info.w, info.h]} />
        </mesh>
      ) : null}
      <mesh scale={[s, s, 1]} renderOrder={order * 2 + 1} material={mat}>
        <planeGeometry args={[info.w, info.h]} />
      </mesh>
    </group>
  );
};

const CameraRig: React.FC<{ cam: Cam }> = ({ cam }) => {
  const camera = useThree((s) => s.camera);
  const x = (cam.x ?? 960) - 960;
  const y = -((cam.y ?? 540) - 540);
  camera.position.set(x, y, D0 / (cam.zoom ?? 1));
  camera.up.set(Math.sin(((cam.rot ?? 0) * Math.PI) / 180), Math.cos(((cam.rot ?? 0) * Math.PI) / 180), 0);
  camera.lookAt(x, y, 0);
  camera.updateProjectionMatrix();
  return null;
};

/**
 * A paper page filmed by a gently moving camera. Pieces are Three.js planes at different
 * depths (parallax). `night` tints the page blue. Children render as a DOM overlay
 * (hand-drawn pencil marks, captions).
 */
export const Stage: React.FC<{ pieces: Piece[]; cam?: Cam; night?: number; children?: React.ReactNode }> = ({ pieces, cam = {}, night = 0, children }) => {
  const { width, height } = useVideoConfig();
  const files = useMemo(() => [...new Set(pieces.flatMap((p) => [elements[p.el].file, elements[p.el].back]))].sort(), [pieces]);
  const tex = useTextures(files);
  const list = pieces
    .map((p, i) => ({ p, i }))
    .filter(({ p }) => (p.opacity ?? 1) > 0.001 && ((p.draw ?? 1) > 0.001 || (p.color ?? 1) > 0.001 || (p.back ?? 0) > 0.001))
    .sort((a, b) => (a.p.z ?? 0) - (b.p.z ?? 0) || a.i - b.i);
  return (
    <AbsoluteFill>
      <Img src={staticFile('paper.jpg')} style={{ position: 'absolute', width: '100%', height: '100%' }} />
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 70% 20%, #7f93d6, #4a5aa0)', mixBlendMode: 'multiply', opacity: 0.5 * night }} />
      {tex ? (
        <ThreeCanvas width={width} height={height} flat gl={{ antialias: true, alpha: true, preserveDrawingBuffer: true }} camera={{ fov: FOV, near: 10, far: 20000, position: [0, 0, D0] }}>
          <CameraRig cam={cam} />
          <ambientLight intensity={1} />
          {list.map(({ p, i }, n) => (
            <PieceMesh key={p.key ?? `${p.el}-${i}`} p={p} tex={tex} order={n} night={night} />
          ))}
        </ThreeCanvas>
      ) : null}
      {children}
    </AbsoluteFill>
  );
};

/** screen position of a point given in the element's storyboard panel px (x4) */
export const pointOn = (p: Pick<Piece, 'el' | 'x' | 'y' | 's'>, panelX: number, panelY: number) => {
  const e = elements[p.el];
  return [p.x + (panelX - (e.x0 + e.w / 2)) * p.s, p.y + (panelY - (e.y0 + e.h / 2)) * p.s] as const;
};
