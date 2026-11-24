import React from 'react';
import { AbsoluteFill } from 'remotion';
import { linearTiming, TransitionSeries } from '@remotion/transitions';
import { S1_SECONDS, S1Year } from './scenes/S1Year';
import { S2_SECONDS, S2Mairan } from './scenes/S2Mairan';
import { S3_SECONDS, S3DayNight } from './scenes/S3DayNight';
import { S4_SECONDS, S4_SUN, S4Wonder } from './scenes/S4Wonder';
import { S5_INTERIOR, S5_SECONDS, S5Cabinet } from './scenes/S5Cabinet';
import { S6_SECONDS, S6Clock } from './scenes/S6Clock';
import { bloom, darkPaper, scribble, torn } from './transitions';

export const FPS = 30;
const f = (s: number) => Math.round(s * FPS);
export const SCENES = [S1_SECONDS, S2_SECONDS, S3_SECONDS, S4_SECONDS, S5_SECONDS, S6_SECONDS].map(f);
/** transition lengths in frames — slow, so each picture can settle */
export const TRANSITIONS = [f(2.0), f(2.2), f(2.6), f(2.4), f(2.0)];
export const TOTAL_FRAMES = SCENES.reduce((a, b) => a + b, 0) - TRANSITIONS.reduce((a, b) => a + b, 0);

/** 1729：含羞草的時鐘 */
export const MimosaClock: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#fbecd8' }}>
    <TransitionSeries>
      <TransitionSeries.Sequence name="1 · 1729" durationInFrames={SCENES[0]}>
        <S1Year />
      </TransitionSeries.Sequence>
      {/* pencil scribble fills in the next page */}
      <TransitionSeries.Transition presentation={scribble(7)} timing={linearTiming({ durationInFrames: TRANSITIONS[0] })} />
      <TransitionSeries.Sequence name="2 · 德梅朗" durationInFrames={SCENES[1]}>
        <S2Mairan />
      </TransitionSeries.Sequence>
      {/* the page is torn away */}
      <TransitionSeries.Transition presentation={torn(11)} timing={linearTiming({ durationInFrames: TRANSITIONS[1] })} />
      <TransitionSeries.Sequence name="3 · 日開夜合" durationInFrames={SCENES[2]}>
        <S3DayNight />
      </TransitionSeries.Sequence>
      {/* morning: the day page blooms out from the sun like wet watercolour */}
      <TransitionSeries.Transition presentation={bloom(S4_SUN)} timing={linearTiming({ durationInFrames: TRANSITIONS[2] })} />
      <TransitionSeries.Sequence name="4 · 看太陽？" durationInFrames={SCENES[3]}>
        <S4Wonder />
      </TransitionSeries.Sequence>
      {/* darkness spreads from the covered sun and shrinks into the cabinet */}
      <TransitionSeries.Transition presentation={darkPaper(S4_SUN, S5_INTERIOR)} timing={linearTiming({ durationInFrames: TRANSITIONS[3] })} />
      <TransitionSeries.Sequence name="5 · 不透光的櫃子" durationInFrames={SCENES[4]}>
        <S5Cabinet />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={scribble(23)} timing={linearTiming({ durationInFrames: TRANSITIONS[4] })} />
      <TransitionSeries.Sequence name="6 · 體內的時鐘" durationInFrames={SCENES[5]}>
        <S6Clock />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  </AbsoluteFill>
);
