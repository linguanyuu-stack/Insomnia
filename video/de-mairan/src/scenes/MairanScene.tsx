import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { LayerStage } from '../components/LayerStage';
import { fadeIn, kf } from '../lib/kf';

export const MAIRAN_SECONDS = 8.5;

/** 分鏡 2 — 天文學家德梅朗 */
export const MairanScene: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  return (
    <LayerStage
      panel="p2"
      cam={{ x: kf(t, [0, 8.5], [690, 840]), y: kf(t, [0, 8.5], [760, 720]), zoom: kf(t, [0, 8.5], [1.0, 1.12]) }}
      anims={{
        person: { z: 140, opacity: fadeIn(t, 0, 2.0), dx: kf(t, [0, 2.8], [-90, 0]) },
        orbit: { z: -120, opacity: fadeIn(t, 2.0, 1.8), rot: kf(t, [2.0, 8.5], [-4, 2]) },
        name: { z: 40, opacity: fadeIn(t, 3.0, 1.8), dx: kf(t, [3.0, 5.0], [50, 0]) },
        telescope: { z: 70, opacity: fadeIn(t, 3.8, 1.8), dy: kf(t, [3.8, 5.8], [70, 0]) },
      }}
    >
      <Captions items={[[1.2, 8.0, '天文學家德梅朗（Jean-Jacques d’Ortous de Mairan）']]} />
    </LayerStage>
  );
};
