import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { Captions } from '../components/Captions';
import { LayerStage } from '../components/LayerStage';
import { fadeIn, kf } from '../lib/kf';

export const YEAR_SECONDS = 7;

/** 分鏡 1 — 時間是 1729 年 */
export const YearScene: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  return (
    <LayerStage
      panel="p1"
      cam={{ x: 864, y: kf(t, [0, 7], [480, 430]), zoom: kf(t, [0, 7], [0.9, 1.08]) }}
      anims={{
        banner: { z: 60, opacity: fadeIn(t, 0.2, 2.0), scale: kf(t, [0.2, 2.6], [0.94, 1]) },
        props: { z: 200, opacity: fadeIn(t, 1.4, 1.8), dy: kf(t, [1.4, 3.6], [110, 0]) },
      }}
    >
      <Captions items={[[1.0, 6.6, '時間是 1729 年。']]} />
    </LayerStage>
  );
};
