import React from 'react';
import { Composition, Folder } from 'remotion';
import './lib/fonts';
import { FPS, MimosaClock, SCENES, TOTAL_FRAMES } from './MimosaClock';
import { S1Year } from './scenes/S1Year';
import { S2Mairan } from './scenes/S2Mairan';
import { S3DayNight } from './scenes/S3DayNight';
import { S4Wonder } from './scenes/S4Wonder';
import { S5Cabinet } from './scenes/S5Cabinet';
import { S6Clock } from './scenes/S6Clock';

const size = { width: 1920, height: 1080, fps: FPS };

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="MimosaClock" component={MimosaClock} durationInFrames={TOTAL_FRAMES} {...size} />
    <Folder name="Scenes">
      <Composition id="S1-Year" component={S1Year} durationInFrames={SCENES[0]} {...size} />
      <Composition id="S2-Mairan" component={S2Mairan} durationInFrames={SCENES[1]} {...size} />
      <Composition id="S3-DayNight" component={S3DayNight} durationInFrames={SCENES[2]} {...size} />
      <Composition id="S4-Wonder" component={S4Wonder} durationInFrames={SCENES[3]} {...size} />
      <Composition id="S5-Cabinet" component={S5Cabinet} durationInFrames={SCENES[4]} {...size} />
      <Composition id="S6-Clock" component={S6Clock} durationInFrames={SCENES[5]} {...size} />
    </Folder>
  </>
);
