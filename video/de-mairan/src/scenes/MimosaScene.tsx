import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { LayerStage } from '../components/LayerStage';
import { fadeIn, kf, sway } from '../lib/kf';

export const MIMOSA_SECONDS = 10.5;

/** 分鏡 3 — 白天葉子張開（左），晚上合起來（右） */
export const MimosaScene: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const k = [0, 3.4, 7.0, 10.0];
  return (
    <LayerStage
      panel="p3"
      // start on the day side, glide to the night side, then pull back to the whole panel
      cam={{ x: kf(t, k, [740, 760, 1950, 1342]), y: kf(t, k, [690, 690, 660, 690]), zoom: kf(t, k, [1.7, 1.78, 1.72, 1.0]) }}
      anims={{
        skyDay: { z: -160, opacity: fadeIn(t, 0, 1.8) },
        plantL: { z: 50, opacity: fadeIn(t, 0.4, 2.0), rot: sway(t, 0.7, 0.9), pivot: [80, 960] },
        labelL: { z: 100, opacity: fadeIn(t, 1.8, 1.6), dy: kf(t, [1.8, 3.4], [30, 0]) },
        skyNight: { z: -160, opacity: fadeIn(t, 3.8, 2.2) },
        plantR: { z: 50, opacity: fadeIn(t, 4.4, 2.0), rot: sway(t, 0.5, 0.7, 1.5), pivot: [1490, 960] },
        labelR: { z: 100, opacity: fadeIn(t, 5.8, 1.6), dy: kf(t, [5.8, 7.4], [30, 0]) },
        title: { z: 70, opacity: fadeIn(t, 7.2, 1.8) },
        arrows: { z: 80, opacity: fadeIn(t, 7.8, 1.6), rot: kf(t, [7.8, 10.5], [-25, 0]) },
      }}
    >
      <Captions
        items={[
          [1.0, 5.0, '注意到，含羞草的葉子在白天張開、'],
          [5.3, 10.0, '晚上合起來。'],
        ]}
      />
    </LayerStage>
  );
};
