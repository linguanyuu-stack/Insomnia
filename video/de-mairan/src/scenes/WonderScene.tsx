import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { LayerStage } from '../components/LayerStage';
import { fadeIn, kf, sway } from '../lib/kf';

export const WONDER_SECONDS = 11.5;

/** 分鏡 4 — 大家以為植物在「看太陽」；如果看不到太陽呢？ */
export const WonderScene: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const dim = kf(t, [6.2, 8.4], [1, 0.72]); // the sun "goes away" for the question
  return (
    <LayerStage
      panel="p4"
      cam={{ x: kf(t, [0, 3.2, 10], [1172, 1172, 1190]), y: kf(t, [0, 3.2, 10], [600, 600, 690]), zoom: kf(t, [0, 3.2, 10], [1.0, 1.0, 1.7]) }}
      anims={{
        skyDay: { z: -160, opacity: kf(t, [6.2, 8.4], [1, 0.18]) },
        skyNight: { z: -160, opacity: dim },
        plantL: { z: 40, opacity: dim, rot: sway(t, 0.6, 0.9), pivot: [60, 860] },
        plantR: { z: 40, opacity: dim, rot: sway(t, 0.5, 0.7, 1.5), pivot: [1390, 820] },
        title: { z: 60, opacity: dim },
        arrows: { z: 70, opacity: dim, rot: sway(t, 6, 0.6) },
        labelL: { z: 90, opacity: dim },
        labelR: { z: 90, opacity: dim },
        mairan: { z: 230, opacity: fadeIn(t, 0.6, 2.2), dy: kf(t, [0.6, 3.4], [220, 0]) },
      }}
    >
      <Captions
        items={[
          [0.8, 5.6, '那時，大家都以為那是植物在「看太陽」。'],
          [6.0, 11.0, '但他想知道：如果看不到太陽呢？'],
        ]}
      />
    </LayerStage>
  );
};
