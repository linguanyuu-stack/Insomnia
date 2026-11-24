import React, { useEffect, useMemo, useState } from 'react';
import * as THREE from 'three';
import { useThree } from '@react-three/fiber';
import { ThreeCanvas } from '@remotion/three';
import { AbsoluteFill, cancelRender, continueRender, delayRender, Img, staticFile, useVideoConfig } from 'remotion';
import layers from '../layers.json';

export type PanelId = keyof typeof layers;

/** Per-layer animation state. Offsets are in storyboard-panel pixels (x4). */
export type LayerAnim = {
  z?: number; // depth: + towards camera, - away. Creates parallax when the camera moves.
  opacity?: number;
  dx?: number;
  dy?: number;
  scale?: number;
  rot?: number; // degrees, around pivot
  pivot?: [number, number]; // panel px (x4); defaults to the layer centre
};

/** Camera framing: look at (x, y) in panel px; zoom 1 = whole panel fits the frame */
export type Cam = { x: number; y: number; zoom: number };

const FOV = 30;
const T = Math.tan(((FOV / 2) * Math.PI) / 180);

// Textures are loaded once (module cache) and the stage is only mounted when all of a
// panel's layers are ready, so the very first rendered frame already has every texture.
const cache = new Map<string, Promise<THREE.Texture>>();
const loadTexture = (file: string) => {
  if (!cache.has(file)) {
    cache.set(
      file,
      new THREE.TextureLoader().loadAsync(staticFile(file)).then((t) => {
        t.colorSpace = THREE.SRGBColorSpace;
        t.anisotropy = 8;
        return t;
      }),
    );
  }
  return cache.get(file)!;
};

function usePanelTextures(files: string[]) {
  const [map, setMap] = useState<Record<string, THREE.Texture> | null>(null);
  const [handle] = useState(() => delayRender(`textures ${files[0]}`));
  useEffect(() => {
    Promise.all(files.map(loadTexture))
      .then((ts) => {
        setMap(Object.fromEntries(files.map((f, i) => [f, ts[i]])));
        continueRender(handle);
      })
      .catch((e) => cancelRender(e));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [handle]);
  return map;
}

type LayerInfo = (typeof layers)[PanelId]['layers'][number];

const Plane: React.FC<{ info: LayerInfo; tex: THREE.Texture; anim: LayerAnim; W: number; H: number; D1: number; order: number }> = ({ info, tex, anim, W, H, D1, order }) => {
  const z = anim.z ?? 0;
  // scale positions/sizes by (D1 - z) / D1 so the composition matches the storyboard at rest
  const k = (D1 - z) / D1;
  const cx = info.x + info.w / 2 + (anim.dx ?? 0);
  const cy = info.y + info.h / 2 + (anim.dy ?? 0);
  const [px, py] = anim.pivot ?? [cx, cy];
  const s = anim.scale ?? 1;
  return (
    <group position={[(px - W / 2) * k, -(py - H / 2) * k, z]} rotation={[0, 0, (-(anim.rot ?? 0) * Math.PI) / 180]} scale={[s * k, s * k, 1]}>
      <mesh position={[cx - px, -(cy - py), 0]} renderOrder={order}>
        <planeGeometry args={[info.w, info.h]} />
        <meshBasicMaterial map={tex} transparent opacity={anim.opacity ?? 1} depthWrite={false} depthTest={false} toneMapped={false} />
      </mesh>
    </group>
  );
};

/**
 * One storyboard panel as a 2.5D scene: paper backdrop + each cut-out layer on its own
 * plane in a Three.js perspective space, filmed by a slowly moving camera.
 */
export const LayerStage: React.FC<{ panel: PanelId; cam: Cam; anims: Record<string, LayerAnim>; children?: React.ReactNode }> = ({ panel, cam, anims, children }) => {
  const { width, height } = useVideoConfig();
  const P = layers[panel];
  const [W, H] = P.size;
  const aspect = width / height;
  const D1 = useMemo(() => Math.max(W / (2 * T * aspect), H / (2 * T)) * 1.08, [W, H, aspect]);
  const dist = D1 / cam.zoom;
  const textures = usePanelTextures(P.layers.map((l) => l.file));
  // draw back-to-front by depth, then by the order in layers.json (reversed: later = further back)
  const list = P.layers
    .map((info, i) => ({ info, anim: anims[info.name] ?? { opacity: 0 }, i }))
    .filter((l) => (l.anim.opacity ?? 1) > 0.001)
    .sort((a, b) => (a.anim.z ?? 0) - (b.anim.z ?? 0) || b.i - a.i);
  return (
    <AbsoluteFill>
      <Img src={staticFile('paper.jpg')} style={{ position: 'absolute', width: '100%', height: '100%' }} />
      {textures ? (
      <ThreeCanvas width={width} height={height} flat linear={false} gl={{ antialias: true, alpha: true, preserveDrawingBuffer: true }} camera={{ fov: FOV, near: 10, far: 20000, position: [cam.x - W / 2, -(cam.y - H / 2), dist] }}>
        <CameraRig x={cam.x - W / 2} y={-(cam.y - H / 2)} z={dist} />
        <ambientLight intensity={1} />
        {list.map((l, n) => (
          <Plane key={l.info.name} info={l.info} tex={textures[l.info.file]} anim={l.anim} W={W} H={H} D1={D1} order={n} />
        ))}
      </ThreeCanvas>
      ) : null}
      {children}
    </AbsoluteFill>
  );
};

// keeps the default R3F camera in sync with props every frame (no useFrame: driven by render)
const CameraRig: React.FC<{ x: number; y: number; z: number }> = ({ x, y, z }) => {
  const camera = useThree((s) => s.camera);
  camera.position.set(x, y, z);
  camera.lookAt(x, y, 0);
  camera.updateProjectionMatrix();
  return null;
};
