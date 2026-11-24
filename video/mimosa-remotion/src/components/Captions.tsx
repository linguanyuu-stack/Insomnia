import React from 'react';
import { AbsoluteFill, Easing, Interactive, interpolate, Sequence, useCurrentFrame } from 'remotion';
import { C, FONT } from '../lib/theme';
import { CAPTIONS } from '../timeline';

const Caption: React.FC<{ text: string; duration: number }> = ({ text, duration }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center' }}>
      <Interactive.Div
        name="Caption"
        style={{
          marginBottom: 44,
          fontFamily: FONT.kai,
          fontWeight: 700,
          fontSize: 52,
          letterSpacing: 2,
          color: C.ink,
          textAlign: 'center',
          maxWidth: 1680,
          opacity: interpolate(frame, [0, 5, duration - 4, duration], [0, 1, 1, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
          translate: interpolate(frame, [0, 6], ['0px 12px', '0px 0px'], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        {text}
      </Interactive.Div>
    </AbsoluteFill>
  );
};

/** Subtitle track: a soft paper band + one Sequence per line */
export const Captions: React.FC = () => (
  <AbsoluteFill>
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        height: 160,
        background: `linear-gradient(to bottom, rgba(244,232,210,0), rgba(244,232,210,.88) 45%, rgba(244,232,210,.95))`,
      }}
    />
    {CAPTIONS.map(([from, to, text]) => (
      <Sequence key={from} name={text.slice(0, 12)} from={from} durationInFrames={to - from}>
        <Caption text={text} duration={to - from} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
