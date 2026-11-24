import React from 'react';
import { AbsoluteFill, Easing, Interactive, interpolate, Sequence, useCurrentFrame, useVideoConfig } from 'remotion';
import { CAPTION_FONT } from '../lib/fonts';

/** [start s, end s, text] in scene-local seconds */
export type CaptionItem = [number, number, string];

const Line: React.FC<{ text: string; frames: number }> = ({ text, frames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center' }}>
      <Interactive.Div
        name="Caption"
        style={{
          marginBottom: 58,
          padding: '10px 34px',
          fontFamily: CAPTION_FONT,
          fontWeight: 500,
          fontSize: 50,
          letterSpacing: 3,
          color: '#3b332d',
          textAlign: 'center',
          maxWidth: 1640,
          opacity: interpolate(frame, [0, 0.5 * fps, frames - 0.5 * fps, frames], [0, 1, 1, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
          translate: interpolate(frame, [0, 0.7 * fps], ['0px 10px', '0px 0px'], {
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

/** Subtitle track over a soft paper band, like the captions under the storyboard frames */
export const Captions: React.FC<{ items: CaptionItem[] }> = ({ items }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          bottom: 0,
          height: 200,
          background: 'linear-gradient(to bottom, rgba(251,233,212,0), rgba(251,236,216,.85) 45%, rgba(251,236,216,.93))',
        }}
      />
      {items.map(([a, b, text]) => (
        <Sequence key={a} name={text.slice(0, 10)} from={Math.round(a * fps)} durationInFrames={Math.round((b - a) * fps)}>
          <Line text={text} frames={Math.round((b - a) * fps)} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
