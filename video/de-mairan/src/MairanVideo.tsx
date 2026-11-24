import React from 'react';
import { AbsoluteFill } from 'remotion';
import { linearTiming, TransitionSeries } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { CabinetScene, CABINET_SECONDS } from './scenes/CabinetScene';
import { MairanScene, MAIRAN_SECONDS } from './scenes/MairanScene';
import { MimosaScene, MIMOSA_SECONDS } from './scenes/MimosaScene';
import { WonderScene, WONDER_SECONDS } from './scenes/WonderScene';
import { YearScene, YEAR_SECONDS } from './scenes/YearScene';

export const FPS = 30;
/** slow crossfade between storyboard frames (1.5 s) */
export const FADE_FRAMES = 45;
export const SCENE_FRAMES = [YEAR_SECONDS, MAIRAN_SECONDS, MIMOSA_SECONDS, WONDER_SECONDS, CABINET_SECONDS].map((s) => Math.round(s * FPS));
export const TOTAL_FRAMES = SCENE_FRAMES.reduce((a, b) => a + b, 0) - FADE_FRAMES * (SCENE_FRAMES.length - 1);

// TransitionSeries only accepts its own element types as direct children
const crossfade = () => <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: FADE_FRAMES })} />;

/** 1729：德梅朗與含羞草的時鐘 */
export const MairanVideo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#fbe9d4' }}>
    <TransitionSeries>
      <TransitionSeries.Sequence name="1 · 1729" durationInFrames={SCENE_FRAMES[0]}>
        <YearScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="2 · 德梅朗" durationInFrames={SCENE_FRAMES[1]}>
        <MairanScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="3 · 含羞草日夜" durationInFrames={SCENE_FRAMES[2]}>
        <MimosaScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="4 · 看太陽？" durationInFrames={SCENE_FRAMES[3]}>
        <WonderScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="5 · 不透光的櫃子" durationInFrames={SCENE_FRAMES[4]}>
        <CabinetScene />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  </AbsoluteFill>
);
