import React from 'react';
import { Composition, Folder } from 'remotion';
import './lib/fonts';
import { FPS, MairanVideo, SCENE_FRAMES, TOTAL_FRAMES } from './MairanVideo';
import { CabinetScene } from './scenes/CabinetScene';
import { MairanScene } from './scenes/MairanScene';
import { MimosaScene } from './scenes/MimosaScene';
import { WonderScene } from './scenes/WonderScene';
import { YearScene } from './scenes/YearScene';

const size = { width: 1920, height: 1080, fps: FPS };

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="DeMairan1729" component={MairanVideo} durationInFrames={TOTAL_FRAMES} {...size} />
    <Folder name="Scenes">
      <Composition id="S1-Year" component={YearScene} durationInFrames={SCENE_FRAMES[0]} {...size} />
      <Composition id="S2-Mairan" component={MairanScene} durationInFrames={SCENE_FRAMES[1]} {...size} />
      <Composition id="S3-Mimosa" component={MimosaScene} durationInFrames={SCENE_FRAMES[2]} {...size} />
      <Composition id="S4-Wonder" component={WonderScene} durationInFrames={SCENE_FRAMES[3]} {...size} />
      <Composition id="S5-Cabinet" component={CabinetScene} durationInFrames={SCENE_FRAMES[4]} {...size} />
    </Folder>
  </>
);
