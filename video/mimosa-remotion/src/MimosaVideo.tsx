import React from 'react';
import { AbsoluteFill } from 'remotion';
import { linearTiming, TransitionSeries } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { Captions } from './components/Captions';
import { CabinetScene } from './scenes/CabinetScene';
import { ClockScene } from './scenes/ClockScene';
import { MairanScene } from './scenes/MairanScene';
import { MimosaScene } from './scenes/MimosaScene';
import { WonderScene } from './scenes/WonderScene';
import { YearScene } from './scenes/YearScene';
import { SCENES, TRANSITION } from './timeline';

// TransitionSeries only accepts its own element types as children, so this returns the element itself
const crossfade = () => <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: TRANSITION })} />;

/** 1729：含羞草的時鐘 — full video (scenes + subtitle track) */
export const MimosaVideo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#f4e8d2' }}>
    <TransitionSeries>
      <TransitionSeries.Sequence name="1729" durationInFrames={SCENES.year}>
        <YearScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="德梅朗" durationInFrames={SCENES.mairan}>
        <MairanScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="含羞草 日夜" durationInFrames={SCENES.mimosa}>
        <MimosaScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="看太陽？" durationInFrames={SCENES.wonder}>
        <WonderScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="不透光的櫃子" durationInFrames={SCENES.cabinet}>
        <CabinetScene />
      </TransitionSeries.Sequence>
      {crossfade()}
      <TransitionSeries.Sequence name="體內時鐘" durationInFrames={SCENES.clock}>
        <ClockScene />
      </TransitionSeries.Sequence>
    </TransitionSeries>
    <Captions />
  </AbsoluteFill>
);
