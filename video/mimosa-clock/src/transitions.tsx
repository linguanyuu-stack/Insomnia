import React from 'react';
import { AbsoluteFill, interpolate } from 'remotion';
import type { TransitionPresentation, TransitionPresentationComponentProps } from '@remotion/transitions';

const W = 1920;
const H = 1080;
const ease = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const rnd = (seed: number) => {
  let s = seed;
  return () => {
    s = (s * 16807) % 2147483647;
    return s / 2147483647;
  };
};

// ───────────────────────── 1. pencil-hatching reveal ─────────────────────────
// The new page is shaded in with slanted pencil strokes, sweeping left → right.
type ScribbleProps = { seed: number };

const SLANT = 520; // horizontal run of each stroke from top to bottom
const GAP = 13;
const hatchLines = (seed: number) => {
  const r = rnd(seed);
  const lines: { x: number; order: number; wob: number }[] = [];
  for (let x = -40; x < W + SLANT + 40; x += GAP) {
    lines.push({ x, order: x / (W + SLANT) + (r() - 0.5) * 0.09, wob: (r() - 0.5) * 30 });
  }
  return lines;
};
const lineD = (l: { x: number; wob: number }) => `M${l.x},-60 Q${l.x - SLANT / 2 + l.wob},${H / 2} ${l.x - SLANT},${H + 60}`;
const lineProgress = (p: number, order: number) => Math.min(1, Math.max(0, (p * 1.3 - order) / 0.3));

const ScribbleComp: React.FC<TransitionPresentationComponentProps<ScribbleProps>> = ({ children, presentationDirection, presentationProgress, passedProps }) => {
  if (presentationDirection === 'exiting') return <AbsoluteFill>{children}</AbsoluteFill>;
  const p = ease(presentationProgress);
  const lines = hatchLines(passedProps.seed);
  const body = lines
    .map((l) => {
      const q = lineProgress(p, l.order);
      return q <= 0 ? '' : `<path d='${lineD(l)}' pathLength='1' stroke-dasharray='1 1' stroke-dashoffset='${(1 - q).toFixed(3)}'/>`;
    })
    .join('');
  const mask = `<svg xmlns='http://www.w3.org/2000/svg' width='${W}' height='${H}' viewBox='0 0 ${W} ${H}'><g fill='none' stroke='white' stroke-width='${GAP * 2.1}' stroke-linecap='round'>${body}</g></svg>`;
  const url = `url("data:image/svg+xml;utf8,${encodeURIComponent(mask)}")`;
  const active = lines.filter((l) => {
    const q = lineProgress(p, l.order);
    return q > 0 && q < 1;
  });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ maskImage: url, WebkitMaskImage: url, maskSize: '100% 100%', WebkitMaskSize: '100% 100%' }}>{children}</AbsoluteFill>
      {/* graphite: the strokes still being drawn */}
      <svg width={W} height={H} style={{ position: 'absolute', opacity: 0.45 }}>
        {active.map((l) => {
          const q = lineProgress(p, l.order);
          return <path key={l.x} d={lineD(l)} fill="none" stroke="#4a3f36" strokeWidth={1.8} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - q} opacity={Math.sin(q * Math.PI)} />;
        })}
      </svg>
    </AbsoluteFill>
  );
};
export const scribble = (seed = 7): TransitionPresentation<ScribbleProps> => ({ component: ScribbleComp, props: { seed } });

// ───────────────────────── 2. torn page ─────────────────────────
type TornProps = { seed: number };

const tearEdge = (p: number, seed: number) => {
  const r = rnd(seed);
  const base = interpolate(p, [0, 1], [-420, W + 420]);
  const pts: [number, number][] = [];
  let jag = 0;
  for (let y = -40; y <= H + 40; y += 18) {
    jag = jag * 0.55 + (r() - 0.5) * 34;
    pts.push([base + (y - H / 2) * 0.32 + jag + Math.sin(y * 0.011 + seed) * 26, y]);
  }
  return pts;
};

const TornComp: React.FC<TransitionPresentationComponentProps<TornProps>> = ({ children, presentationDirection, presentationProgress, passedProps }) => {
  if (presentationDirection === 'entering') return <AbsoluteFill style={{ zIndex: 1 }}>{children}</AbsoluteFill>;
  if (presentationProgress <= 0) return <AbsoluteFill>{children}</AbsoluteFill>;
  const p = ease(presentationProgress);
  const edge = tearEdge(p, passedProps.seed);
  const poly = [...edge.map(([x, y]) => `${x.toFixed(1)}px ${y}px`), `${W + 600}px ${H + 40}px`, `${W + 600}px -40px`].join(',');
  const line = 'M' + edge.map(([x, y]) => `${x.toFixed(1)},${y}`).join(' L');
  const lift = Math.sin(Math.PI * Math.min(1, presentationProgress * 1.2)) * 6;
  return (
    <AbsoluteFill style={{ zIndex: 2 }}>
      <AbsoluteFill style={{ clipPath: `polygon(${poly})`, translate: `${lift}px ${-lift * 0.4}px` }}>{children}</AbsoluteFill>
      <svg width={W} height={H} style={{ position: 'absolute', translate: `${lift}px ${-lift * 0.4}px` }}>
        <defs>
          <filter id="tornBlur">
            <feGaussianBlur stdDeviation={10} />
          </filter>
          <filter id="fibres">
            <feTurbulence type="fractalNoise" baseFrequency="0.25" numOctaves={2} seed={passedProps.seed} />
            <feDisplacementMap in="SourceGraphic" scale={9} xChannelSelector="R" yChannelSelector="G" />
          </filter>
        </defs>
        {/* shadow of the lifted page on the new page, then the white torn fibres */}
        <path d={line} fill="none" stroke="#3a2a1c" strokeOpacity={0.35} strokeWidth={26} filter="url(#tornBlur)" transform="translate(-14 6)" />
        <path d={line} fill="none" stroke="#fffaf1" strokeWidth={13} filter="url(#fibres)" />
        <path d={line} fill="none" stroke="#e8dcc6" strokeWidth={2} transform="translate(5 0)" filter="url(#fibres)" />
      </svg>
    </AbsoluteFill>
  );
};
export const torn = (seed = 11): TransitionPresentation<TornProps> => ({ component: TornComp, props: { seed } });

// ───────────────────────── 3. a new collage sheet slides over ─────────────────────────
type SlideProps = { fromX: number; fromY: number; rot: number };

const SlideComp: React.FC<TransitionPresentationComponentProps<SlideProps>> = ({ children, presentationDirection, presentationProgress, passedProps }) => {
  const p = ease(presentationProgress);
  if (presentationDirection === 'exiting') {
    return (
      <AbsoluteFill style={{ scale: `${1 - 0.03 * p}` }}>
        {children}
        <AbsoluteFill style={{ backgroundColor: '#2b1d10', opacity: 0.22 * p }} />
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill
      style={{
        translate: `${passedProps.fromX * (1 - p)}px ${passedProps.fromY * (1 - p)}px`,
        rotate: `${passedProps.rot * (1 - p)}deg`,
        boxShadow: `0 ${30 * (1 - p) + 4}px ${70 * (1 - p) + 10}px rgba(40,25,10,${0.45 * (1 - p * 0.8)})`,
        overflow: 'hidden',
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
export const sheetSlide = (fromX = 1300, fromY = 500, rot = 9): TransitionPresentation<SlideProps> => ({ component: SlideComp, props: { fromX, fromY, rot } });

// ───────────────────────── 4. dark paper swallows the light, becomes the cabinet ─────────────────────────
type IrisProps = { from: [number, number]; to: { x: number; y: number; w: number; h: number }; seed: number };

const roughRect = (cx: number, cy: number, w: number, h: number, seed: number, jag: number) => {
  const r = rnd(seed);
  const pts: string[] = [];
  const n = 26;
  const side = (x0: number, y0: number, x1: number, y1: number) => {
    for (let i = 0; i < n; i++) {
      const t = i / n;
      pts.push(`${(x0 + (x1 - x0) * t + (r() - 0.5) * jag).toFixed(1)},${(y0 + (y1 - y0) * t + (r() - 0.5) * jag).toFixed(1)}`);
    }
  };
  const l = cx - w / 2;
  const rr = cx + w / 2;
  const t = cy - h / 2;
  const b = cy + h / 2;
  side(l, t, rr, t);
  side(rr, t, rr, b);
  side(rr, b, l, b);
  side(l, b, l, t);
  return 'M' + pts.join(' L') + 'Z';
};

const DarkPaper: React.FC<{ d: string; opacity?: number }> = ({ d, opacity = 1 }) => (
  <svg width={W} height={H} style={{ position: 'absolute' }} opacity={opacity}>
    <defs>
      <pattern id="irisHatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(40)">
        <line x1="0" y1="0" x2="0" y2="9" stroke="#3a3747" strokeWidth="2" />
      </pattern>
      <filter id="irisShadow">
        <feDropShadow dx="0" dy="6" stdDeviation="10" floodColor="#1a120a" floodOpacity="0.45" />
      </filter>
    </defs>
    <path d={d} fill="#23212c" filter="url(#irisShadow)" />
    <path d={d} fill="url(#irisHatch)" opacity={0.7} />
  </svg>
);

const IrisComp: React.FC<TransitionPresentationComponentProps<IrisProps>> = ({ children, presentationDirection, presentationProgress, passedProps }) => {
  const p = presentationProgress;
  const { from, to, seed } = passedProps;
  if (presentationDirection === 'exiting') {
    // a scene is wrapped in its next transition for its whole length (progress 0): draw nothing extra then
    if (p <= 0) return <AbsoluteFill>{children}</AbsoluteFill>;
    if (p >= 0.5) return null;
    const g = ease(p / 0.5);
    const size = interpolate(g, [0, 1], [10, 4200]);
    return (
      <AbsoluteFill>
        {children}
        <DarkPaper d={roughRect(from[0], from[1], size, size * 0.92, seed, 8 + g * 60)} />
      </AbsoluteFill>
    );
  }
  if (p < 0.5) return null;
  const g = ease((p - 0.5) / 0.5);
  const cx = interpolate(g, [0, 1], [W / 2, to.x]);
  const cy = interpolate(g, [0, 1], [H / 2, to.y]);
  const w = interpolate(g, [0, 1], [W * 2.2, to.w]);
  const h = interpolate(g, [0, 1], [H * 2.2, to.h]);
  return (
    <AbsoluteFill>
      {children}
      <DarkPaper d={roughRect(cx, cy, w, h, seed + 1, 8 + (1 - g) * 50)} opacity={interpolate(p, [0.86, 1], [1, 0], { extrapolateLeft: 'clamp' })} />
    </AbsoluteFill>
  );
};
export const darkPaper = (from: [number, number], to: IrisProps['to'], seed = 5): TransitionPresentation<IrisProps> => ({ component: IrisComp, props: { from, to, seed } });
