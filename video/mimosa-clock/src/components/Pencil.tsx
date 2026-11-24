import React from 'react';
import { AbsoluteFill } from 'remotion';

export type Stroke = { d: string; p: number; color?: string; width?: number; dash?: string; opacity?: number };

/**
 * Hand-drawn pencil marks drawn on top of the page (arrows, question marks, scribbles).
 * Each stroke draws itself as p goes 0 → 1; a turbulence filter roughens the line.
 */
export const Pencil: React.FC<{ strokes: Stroke[]; id?: string }> = ({ strokes, id = 'rough' }) => (
  <AbsoluteFill>
    <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: 'absolute' }}>
      <defs>
        <filter id={id} x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={4} />
          <feDisplacementMap in="SourceGraphic" scale={4} xChannelSelector="R" yChannelSelector="G" result="d" />
          <feTurbulence type="fractalNoise" baseFrequency="0.9 0.3" numOctaves={1} seed={9} result="g" />
          <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.2 0 0 0 1.9" result="gm" />
          <feComposite in="d" in2="gm" operator="in" />
        </filter>
      </defs>
      <g filter={`url(#${id})`}>
        {strokes.map((s, i) =>
          s.p <= 0.001 ? null : s.dash ? (
            // dashed strokes: reveal with a clip-like second dash pattern via mask
            <g key={i} opacity={s.opacity ?? 1}>
              <mask id={`${id}-m${i}`}>
                <path d={s.d} fill="none" stroke="#fff" strokeWidth={(s.width ?? 5) + 8} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - s.p} />
              </mask>
              <path d={s.d} fill="none" stroke={s.color ?? '#4a3c32'} strokeWidth={s.width ?? 5} strokeLinecap="round" strokeDasharray={s.dash} mask={`url(#${id}-m${i})`} />
            </g>
          ) : (
            <path key={i} d={s.d} fill="none" stroke={s.color ?? '#4a3c32'} strokeWidth={s.width ?? 5} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - s.p} opacity={s.opacity ?? 1} />
          ),
        )}
      </g>
    </svg>
  </AbsoluteFill>
);
