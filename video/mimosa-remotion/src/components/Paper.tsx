import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, H, W } from '../lib/theme';

/** Inline SVG markup (procedural drawings from lib/draw.ts) */
export const Raw: React.FC<{ svg: string } & React.SVGProps<SVGGElement>> = ({ svg, ...rest }) => (
  <g {...rest} dangerouslySetInnerHTML={{ __html: svg }} />
);

/**
 * Parchment page + colored-pencil filter.
 * Everything passed as children is drawn in a 1920×1080 SVG space and gets:
 * wobbling "boiling" lines (new seed every 3 frames) and streaky pencil grain.
 */
export const Paper: React.FC<{ children: React.ReactNode; defs?: React.ReactNode }> = ({ children, defs }) => {
  const frame = useCurrentFrame();
  const seed = 1 + (Math.floor(frame / 3) % 6);
  return (
    <AbsoluteFill style={{ backgroundColor: C.paper }}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: 'absolute', inset: 0 }}>
        <defs>
          <filter id="pencil" filterUnits="userSpaceOnUse" x="0" y="0" width={W} height={H} colorInterpolationFilters="sRGB">
            <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves={2} seed={seed} result="warp" />
            <feDisplacementMap in="SourceGraphic" in2="warp" scale={5} xChannelSelector="R" yChannelSelector="G" result="wob" />
            <feTurbulence type="fractalNoise" baseFrequency="0.95 0.28" numOctaves={2} seed={11} result="grain" />
            <feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.6 0 0 0 2.15" result="gmask" />
            <feComposite in="wob" in2="gmask" operator="in" />
          </filter>
          <filter id="paperTex" filterUnits="userSpaceOnUse" x="0" y="0" width={W} height={H}>
            <feTurbulence type="fractalNoise" baseFrequency="0.0035" numOctaves={3} seed={5} result="blot" />
            <feColorMatrix in="blot" type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.4  0 0 0 0 0.22  1.1 0 0 0 -0.45" result="b" />
            <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves={1} seed={9} result="fib" />
            <feColorMatrix in="fib" type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0 0.25  0.5 0 0 0 -0.18" result="fb" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="fb" />
            </feMerge>
          </filter>
          <radialGradient id="vig" cx="50%" cy="48%" r="72%">
            <stop offset="62%" stopColor="#6b4a2a" stopOpacity="0" />
            <stop offset="100%" stopColor="#6b4a2a" stopOpacity=".30" />
          </radialGradient>
          <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
            <line x1="0" y1="0" x2="0" y2="8" stroke={C.ink} strokeWidth="1.3" />
          </pattern>
          <pattern id="hatchFine" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(-32)">
            <line x1="0" y1="0" x2="0" y2="5" stroke={C.ink} strokeWidth=".9" />
          </pattern>
          <pattern id="hatchBlue" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(28)">
            <line x1="0" y1="0" x2="0" y2="9" stroke="#33427a" strokeWidth="2.2" />
          </pattern>
          <pattern id="hatchSun" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(-20)">
            <line x1="0" y1="0" x2="0" y2="10" stroke="#e9b93c" strokeWidth="2" />
          </pattern>
          <pattern id="hatchDark" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="6" stroke="#15121c" strokeWidth="2" />
          </pattern>
          {defs}
        </defs>
        <rect width={W} height={H} filter="url(#paperTex)" opacity={0.55} />
        <g filter="url(#pencil)">{children}</g>
        <rect width={W} height={H} fill="url(#vig)" />
      </svg>
    </AbsoluteFill>
  );
};
