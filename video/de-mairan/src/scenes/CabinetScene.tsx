import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { LayerStage } from '../components/LayerStage';
import { fadeIn, kf } from '../lib/kf';

export const CABINET_SECONDS = 23;

/** 分鏡 5 — 不透光的櫃子：葉子照樣日開夜合 → 體內的時鐘 */
export const CabinetScene: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  // camera tour: de Mairan → cabinet → results → inner-clock note → whole page
  const k = [0, 3.0, 6.2, 7.4, 10.2, 14.2, 17.2, 19.2, 22.0];
  return (
    <LayerStage
      panel="p5"
      cam={{
        x: kf(t, k, [700, 720, 1320, 1320, 2090, 2100, 2200, 2210, 1290]),
        y: kf(t, k, [860, 850, 830, 830, 430, 420, 1000, 1000, 650]),
        zoom: kf(t, k, [1.6, 1.62, 1.75, 1.78, 1.85, 1.95, 1.75, 1.78, 1.0]),
      }}
      anims={{
        mairan: { z: 160, opacity: fadeIn(t, 0, 1.8) },
        bubble: { z: 120, opacity: fadeIn(t, 1.4, 1.8), scale: kf(t, [1.4, 3.2], [0.9, 1]), pivot: [1020, 980] },
        cabinet: { z: 60, opacity: fadeIn(t, 2.8, 2.0) },
        arrowR: { z: 80, opacity: fadeIn(t, 7.2, 1.4) },
        results: { z: 40, opacity: fadeIn(t, 7.8, 2.2) },
        note: { z: 60, opacity: fadeIn(t, 14.4, 2.0) },
        watch: { z: 150, opacity: fadeIn(t, 15.0, 2.0), rot: Math.sin(t * 1.7) * 3, pivot: [2360, 730] },
        recap: { z: -40, opacity: fadeIn(t, 18.6, 2.2) },
        title: { z: 20, opacity: fadeIn(t, 19.0, 2.2) },
      }}
    >
      <Captions
        items={[
          [0.8, 6.8, '德梅朗把觀察的那一株含羞草，放進不透光的櫃子裡。'],
          [7.4, 11.0, '結果，葉子沒因照不到太陽，'],
          [11.2, 14.8, '照樣在白天張開、在晚上合起來。'],
          [15.3, 22.4, '像植物身體裡，有自己的時鐘。'],
        ]}
      />
    </LayerStage>
  );
};
