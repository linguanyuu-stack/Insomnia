import React from 'react';
import { Composition, Folder } from 'remotion';
import './lib/fonts';
import { FPS, H, W } from './lib/theme';
import { MimosaVideo } from './MimosaVideo';
import { CabinetScene } from './scenes/CabinetScene';
import { ClockScene } from './scenes/ClockScene';
import { MairanScene } from './scenes/MairanScene';
import { MimosaScene } from './scenes/MimosaScene';
import { WonderScene } from './scenes/WonderScene';
import { YearScene } from './scenes/YearScene';
import { SCENES, TOTAL_FRAMES } from './timeline';

const size = { width: W, height: H, fps: FPS };

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Mimosa1729" component={MimosaVideo} durationInFrames={TOTAL_FRAMES} {...size} />
    <Folder name="Scenes">
      <Composition id="S1-Year" component={YearScene} durationInFrames={SCENES.year} {...size} />
      <Composition id="S2-Mairan" component={MairanScene} durationInFrames={SCENES.mairan} {...size} />
      <Composition id="S3-Mimosa" component={MimosaScene} durationInFrames={SCENES.mimosa} {...size} />
      <Composition id="S4-Wonder" component={WonderScene} durationInFrames={SCENES.wonder} {...size} />
      <Composition id="S5-Cabinet" component={CabinetScene} durationInFrames={SCENES.cabinet} {...size} />
      <Composition id="S6-Clock" component={ClockScene} durationInFrames={SCENES.clock} {...size} />
    </Folder>
  </>
);
