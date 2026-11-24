// Procedural colored-pencil drawings, returned as SVG markup strings.
// Rendered through <Raw/> so that hundreds of leaflets stay cheap per frame.
import { back, clamp, f, lerp, out3 } from './anim';
import { C, FONT } from './theme';

type Pt = [number, number];

export function rng(seed: number) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function rot(dx: number, dy: number, x: number, y: number, deg: number): Pt {
  const a = (deg * Math.PI) / 180;
  const c = Math.cos(a);
  const s = Math.sin(a);
  return [x + dx * c - dy * s, y + dx * s + dy * c];
}

/** Catmull-Rom spline through points → SVG path */
export function cr(pts: Pt[], close = false) {
  const p = close ? [pts[pts.length - 1], ...pts, pts[0], pts[1]] : [pts[0], ...pts, pts[pts.length - 1]];
  let d = `M${f(p[1][0])},${f(p[1][1])}`;
  for (let i = 1; i < p.length - 2; i++) {
    const [x0, y0] = p[i - 1];
    const [x1, y1] = p[i];
    const [x2, y2] = p[i + 1];
    const [x3, y3] = p[i + 2];
    d += `C${f(x1 + (x2 - x0) / 6)},${f(y1 + (y2 - y0) / 6)} ${f(x2 - (x3 - x1) / 6)},${f(y2 - (y3 - y1) / 6)} ${f(x2)},${f(y2)}`;
  }
  return d + (close ? 'Z' : '');
}

export const tf = (x: number, y: number, s = 1, r = 0) => `translate(${f(x)} ${f(y)}) rotate(${f(r)}) scale(${s})`;

// ───────── mimosa ─────────
function leaflet(px: number, py: number, a: number, l: number, w: number) {
  const c1 = rot(l * 0.45, -w * 1.35, px, py, a);
  const tip = rot(l, 0, px, py, a);
  const c2 = rot(l * 0.45, w * 1.35, px, py, a);
  return `M${f(px)},${f(py)}Q${f(c1[0])},${f(c1[1])} ${f(tip[0])},${f(tip[1])}Q${f(c2[0])},${f(c2[1])} ${f(px)},${f(py)}Z`;
}

/** Fern-like frond as in the storyboard. k: 1 = open … 0 = folded & drooping */
export function frond(x: number, y: number, ang: number, len: number, k: number, s = 1) {
  const droopDir = Math.cos((ang * Math.PI) / 180) >= 0 ? 1 : -1;
  const A = ang + droopDir * (1 - k) * 38;
  const n = 15;
  const bend = 0.1 * len * droopDir * (1 + (1 - k) * 1.2);
  let dL = '';
  let dR = '';
  const pts: Pt[] = [];
  for (let i = 0; i <= 8; i++) {
    const t = i / 8;
    pts.push(rot(len * t, bend * Math.sin(Math.PI * t), x, y, A));
  }
  for (let i = 0; i < n; i++) {
    const t = 0.1 + (0.88 * i) / (n - 1);
    const [px, py] = rot(len * t, bend * Math.sin(Math.PI * t), x, y, A);
    const ta = A + (Math.atan2(bend * Math.PI * Math.cos(Math.PI * t), len) * 180) / Math.PI;
    const taper = 0.5 + 0.5 * Math.sin(Math.PI * Math.min(1, t * 1.08));
    const l = Math.min(44, len * 0.17) * s * taper;
    const w = l * 0.21 * lerp(0.7, 1, k);
    const spread = lerp(20, 70, k);
    dL += leaflet(px, py, ta - spread, l, w);
    dR += leaflet(px, py, ta + spread, l, w);
  }
  return (
    `<path d="${dR}" fill="${C.leaf2}" stroke="${C.leafD}" stroke-width="1.5"/>` +
    `<path d="${dL}" fill="${C.leaf}" stroke="${C.leafD}" stroke-width="1.5"/>` +
    `<path d="${cr(pts)}" fill="none" stroke="#5b6a2c" stroke-width="${f(2.6 * s)}" stroke-linecap="round"/>`
  );
}

export function pompom(x: number, y: number, r: number, seed = 1) {
  const R = rng(seed);
  let lines = '';
  let dots = '';
  for (let i = 0; i < 46; i++) {
    const a = R() * Math.PI * 2;
    const rr = r * (0.55 + R() * 0.5);
    const x2 = x + Math.cos(a) * rr;
    const y2 = y + Math.sin(a) * rr;
    lines += `M${f(x + Math.cos(a) * r * 0.2)},${f(y + Math.sin(a) * r * 0.2)}L${f(x2)},${f(y2)}`;
    dots += `<circle cx="${f(x2)}" cy="${f(y2)}" r="${f(r * 0.07 + 1)}" fill="#f7d36a"/>`;
  }
  return `<circle cx="${x}" cy="${y}" r="${f(r * 0.5)}" fill="#f2b6d2"/><path d="${lines}" stroke="${C.pink}" stroke-width="2" stroke-linecap="round"/>${dots}`;
}

function bud(x: number, y: number, a: number, s = 1) {
  const [bx, by] = rot(16 * s, 0, x, y, a);
  return (
    `<ellipse cx="${f(bx)}" cy="${f(by)}" rx="${f(9 * s)}" ry="${f(7 * s)}" fill="#c9a2a8" stroke="${C.ink}" stroke-width="1.4" transform="rotate(${a} ${f(bx)} ${f(by)})"/>` +
    `<path d="M${f(bx - 4 * s)},${f(by - 3 * s)}l2,-3M${f(bx + 2 * s)},${f(by - 5 * s)}l3,-2M${f(bx - s)},${f(by + 5 * s)}l-1,3" stroke="${C.ink}" stroke-width="1.2"/>`
  );
}

function thorns(pts: Pt[], seed: number) {
  const R = rng(seed);
  let d = '';
  for (let i = 0; i < pts.length - 1; i++) {
    const [x1, y1] = pts[i];
    const [x2, y2] = pts[i + 1];
    for (let j = 0; j < 3; j++) {
      const t = (j + 0.3 + R() * 0.4) / 3;
      const x = lerp(x1, x2, t);
      const y = lerp(y1, y2, t);
      const a = Math.atan2(y2 - y1, x2 - x1) + (j % 2 ? 1 : -1) * 1.9;
      d += `M${f(x)},${f(y)}l${f(Math.cos(a) * 9)},${f(Math.sin(a) * 9)}`;
    }
  }
  return `<path d="${d}" stroke="${C.stem}" stroke-width="2" stroke-linecap="round"/>`;
}

export type PlantSpec = {
  stem: Pt[];
  fronds: [number, number, number, number][]; // x, y, angle, length
  flowers?: [number, number, number, number, number][]; // x, y, r, fromX, fromY
  buds?: [number, number, number][];
};

/** k: leaf openness, grow: 0..1 growth-in animation */
export function plant(spec: PlantSpec, k: number, grow = 1, s = 1) {
  const dash = 1 - clamp(grow * 1.6);
  let o = `<path d="${cr(spec.stem)}" fill="none" stroke="${C.stem}" stroke-width="${7 * s}" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="${dash}"/>`;
  o += `<path d="${cr(spec.stem)}" fill="none" stroke="${C.ink}" stroke-width="${1.2 * s}" opacity=".6" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="${dash}"/>`;
  if (grow > 0.55) o += thorns(spec.stem, 4);
  (spec.flowers || []).forEach(([x, y, r, fx, fy], i) => {
    const g = clamp((grow - 0.45 - i * 0.06) * 3);
    if (g <= 0) return;
    o += `<path d="M${fx},${fy}Q${f((fx + x) / 2 - 10)},${f((fy + y) / 2)} ${x},${y}" stroke="${C.stem}" stroke-width="${3 * s}" fill="none"/>`;
    o += `<g transform="translate(${x} ${y}) scale(${back(g)}) translate(${-x} ${-y})">${pompom(x, y, r * s, i + 3)}</g>`;
  });
  spec.fronds.forEach(([x, y, a, l], i) => {
    const g = clamp((grow - 0.3 - i * 0.05) * 2.6);
    if (g <= 0) return;
    o += frond(x, y, a, l * out3(g), k, s * lerp(0.5, 1, g));
  });
  (spec.buds || []).forEach(([x, y, a]) => {
    if (grow > 0.7) o += bud(x, y, a, s);
  });
  return o;
}

/** small mimosa in a terracotta pot; origin = pot bottom centre */
export function pottedPlant(k: number) {
  const spec: PlantSpec = {
    stem: [[0, -70], [-4, -130], [6, -190], [0, -235]],
    fronds: [[-2, -120, -150, 95], [3, -150, -30, 100], [4, -185, -140, 85], [2, -210, -45, 80]],
    flowers: [[-30, -260, 18, -1, -225]],
    buds: [[0, -235, -70]],
  };
  return (
    plant(spec, k, 1, 0.85) +
    `<path d="M-48,-72H48L36,0H-36Z" fill="#c9714d" stroke="${C.ink}" stroke-width="3"/><rect x="-54" y="-84" width="108" height="16" rx="4" fill="#d9845e" stroke="${C.ink}" stroke-width="3"/>` +
    `<path d="M-30,-60L-26,-8" stroke="#e7a481" stroke-width="5" opacity=".7"/>`
  );
}

// ───────── sky ─────────
export function sunSVG(r: number, t: number) {
  let rays = '';
  for (let i = 0; i < 16; i++) {
    const a = i * 22.5 + t * 18;
    const L = i % 2 ? r * 0.45 : r * 0.8;
    const [x1, y1] = rot(r * 1.25, 0, 0, 0, a);
    const [x2, y2] = rot(r * 1.25 + L, 0, 0, 0, a);
    rays += `M${f(x1)},${f(y1)}L${f(x2)},${f(y2)}`;
  }
  return (
    `<path d="${rays}" stroke="#e7a93a" stroke-width="5" stroke-linecap="round"/>` +
    `<circle r="${r}" fill="${C.sun}" stroke="#d9952f" stroke-width="3"/><circle r="${r}" fill="url(#hatchSun)" opacity=".7"/>`
  );
}

export function moonSVG(r: number) {
  return `<path d="M0,${-r}A${r},${r} 0 1 0 ${f(r * 0.6)},${f(r * 0.8)}A${f(r * 0.82)},${f(r * 0.82)} 0 1 1 0,${-r}Z" fill="#f4dc8c" stroke="#c9a346" stroke-width="3"/>`;
}

export function star(x: number, y: number, r: number, a = 0) {
  let d = '';
  for (let i = 0; i < 10; i++) {
    const rr = i % 2 ? r * 0.42 : r;
    const [px, py] = rot(0, -rr, x, y, i * 36 + a);
    d += (i ? 'L' : 'M') + f(px) + ',' + f(py);
  }
  return `<path d="${d}Z" fill="#f4dc8c" stroke="#c9a346" stroke-width="1.5"/>`;
}

export function cloud(x: number, y: number, s: number, fill = '#fdfaf2', stroke = '#a9b6d6') {
  return `<path transform="${tf(x, y, s)}" d="M-80,20C-110,20 -110,-15 -80,-15C-80,-45 -35,-50 -22,-28C-10,-60 45,-55 45,-20C80,-30 100,15 70,20Z" fill="${fill}" stroke="${stroke}" stroke-width="3"/>`;
}

// ───────── UI-ish drawings ─────────
/** Scroll label with curled ends, like the storyboard */
export function scrollLabel(cx: number, cy: number, w: number, h: number, text: string, size: number) {
  const x0 = cx - w / 2;
  const x1 = cx + w / 2;
  const y0 = cy - h / 2;
  const y1 = cy + h / 2;
  return (
    `<path d="M${x0 + 14},${y0}H${x1 - 14}Q${x1},${y0} ${x1},${y0 + 12}Q${x1 + 14},${cy} ${x1},${y1 - 12}Q${x1},${y1} ${x1 - 14},${y1}H${x0 + 14}Q${x0},${y1} ${x0},${y1 - 12}Q${x0 - 14},${cy} ${x0},${y0 + 12}Q${x0},${y0} ${x0 + 14},${y0}Z" fill="${C.cream}" stroke="${C.ink}" stroke-width="3"/>` +
    `<path d="M${x0 - 6},${cy - 10}q-12,10 0,20M${x1 + 6},${cy - 10}q12,10 0,20" fill="none" stroke="${C.ink}" stroke-width="2.5"/>` +
    `<text x="${cx}" y="${cy + size * 0.36}" text-anchor="middle" font-size="${size}" font-family="${FONT.kai}" font-weight="700" fill="${C.ink}" letter-spacing="4">${text}</text>`
  );
}

export function pocketWatch(r: number, hourDeg: number, minDeg: number) {
  let ticks = '';
  for (let i = 0; i < 12; i++) {
    const [x1, y1] = rot(0, -r * 0.78, 0, 0, i * 30);
    const [x2, y2] = rot(0, -r * (i % 3 ? 0.7 : 0.62), 0, 0, i * 30);
    ticks += `M${f(x1)},${f(y1)}L${f(x2)},${f(y2)}`;
  }
  const [hx, hy] = rot(0, -r * 0.45, 0, 0, hourDeg);
  const [mx, my] = rot(0, -r * 0.68, 0, 0, minDeg);
  return (
    `<path d="M-14,${-r - 4}a14,14 0 1 1 28,0" fill="none" stroke="${C.gold}" stroke-width="7"/><rect x="-12" y="${-r - 14}" width="24" height="16" rx="4" fill="${C.gold}" stroke="${C.ink}" stroke-width="2.5"/>` +
    `<circle r="${r + 10}" fill="${C.gold}" stroke="${C.ink}" stroke-width="3"/><circle r="${r}" fill="#fdf8ec" stroke="${C.ink}" stroke-width="2.5"/>` +
    `<path d="${ticks}" stroke="${C.ink}" stroke-width="3" stroke-linecap="round"/>` +
    `<path d="M0,0L${f(hx)},${f(hy)}" stroke="${C.ink}" stroke-width="7" stroke-linecap="round"/><path d="M0,0L${f(mx)},${f(my)}" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>` +
    `<circle r="6" fill="${C.ink}"/>`
  );
}

/** Jean-Jacques d'Ortous de Mairan — stylised bust (frame ≈ 0..420 × 0..525), facing right */
export function bust() {
  const R = rng(17);
  let backMass = '';
  let front = '';
  const curl = (x: number, y: number, r: number) => {
    let sp = '';
    for (let i = 0; i <= 24; i++) {
      const t = i / 24;
      const a = t * 1.6 * Math.PI * 2 + R() * 0.2;
      const rr = r * (0.85 - 0.7 * t);
      sp += (i ? 'L' : 'M') + f(x + Math.cos(a) * rr) + ',' + f(y + Math.sin(a) * rr * 0.9);
    }
    return `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(r)}" ry="${f(r * 0.9)}" fill="#efe7da" stroke="${C.ink}" stroke-width="2.4"/><path d="${sp}" fill="none" stroke="#8d8276" stroke-width="2"/>`;
  };
  const cl: [number, number, number][] = [];
  for (let a = 170; a <= 345; a += 17) {
    const [x, y] = rot(96, 0, 212, 170, a);
    cl.push([x, y, 30]);
  }
  for (let y = 190; y <= 430; y += 34) {
    cl.push([128 + R() * 12, y, 30]);
    cl.push([168 + R() * 12, y + 14, 28]);
  }
  for (let y = 250; y <= 380; y += 32) cl.push([272 + R() * 14, y, 26]);
  backMass += `<path d="M120,120C140,60 280,40 312,120L318,250 300,390 150,450 105,420Z" fill="#e6dccb" stroke="${C.ink}" stroke-width="2.5"/>`;
  cl.sort((p, q) => p[1] - q[1]).forEach(([x, y, r]) => (backMass += curl(x, y, r)));
  const coat =
    `<path d="M30,525C40,420 80,352 160,322L262,318C330,336 382,410 398,525Z" fill="${C.blue}" stroke="${C.ink}" stroke-width="3"/>` +
    `<path d="M30,525C40,420 80,352 160,322L200,330 C180,420 150,470 140,525Z" fill="url(#hatch)" opacity=".45"/>` +
    `<path d="M160,322C176,390 196,440 204,525M262,320C258,390 252,440 248,525" fill="none" stroke="${C.blueD}" stroke-width="5"/>` +
    `<path d="M285,336C300,405 305,465 300,525" fill="none" stroke="${C.ink}" stroke-width="2.5"/>` +
    [372, 412, 452, 492].map((y) => `<circle cx="${f(312 - (y - 372) * 0.05)}" cy="${y}" r="7" fill="${C.gold}" stroke="${C.ink}" stroke-width="2"/>`).join('');
  const neck = `<path d="M192,248L198,322L254,320L258,256Z" fill="${C.skin}" stroke="${C.ink}" stroke-width="2.5"/>`;
  let jab = 'M206,312';
  for (let i = 0; i < 7; i++) {
    const y = 320 + i * 17;
    jab += `Q${f(190 - i * 1.5)},${y + 6} ${f(204 - i)},${y + 14}`;
  }
  jab += 'L246,430';
  for (let i = 6; i >= 0; i--) {
    const y = 320 + i * 17;
    jab += `Q${f(262 + i * 1.5)},${y + 8} ${f(250 + i * 0.5)},${y}`;
  }
  jab += 'Z';
  const jabot = `<path d="${jab}" fill="#fbf7ef" stroke="${C.ink}" stroke-width="2.2"/><path d="M215,330q12,8 26,0M213,360q14,8 30,0M214,392q14,8 30,0" fill="none" stroke="#9a8f82" stroke-width="1.8"/>`;
  const facePts: Pt[] = [[200, 96], [238, 104], [256, 134], [254, 150], [263, 168], [281, 194], [268, 204], [267, 211], [273, 217], [263, 224], [268, 231], [261, 242], [257, 256], [238, 270], [210, 268], [190, 238], [185, 170], [190, 118]];
  const face =
    `<path d="${cr(facePts, true)}" fill="${C.skin}" stroke="${C.ink}" stroke-width="3"/>` +
    `<path d="M196,200C196,240 214,262 238,268C214,262 200,250 196,200Z" fill="url(#hatchFine)" opacity=".5"/>` +
    `<ellipse cx="232" cy="203" rx="17" ry="10" fill="#e79c97" opacity=".45"/>` +
    `<path d="M224,160Q237,151 249,159Q238,166 224,160Z" fill="#fff" stroke="${C.ink}" stroke-width="2"/><circle cx="241" cy="159.5" r="4.2" fill="#3a2c22"/>` +
    `<path d="M221,154Q236,148 251,154" fill="none" stroke="${C.ink}" stroke-width="2.4"/>` +
    `<path d="M220,143Q237,133 255,141" fill="none" stroke="#7d6a5a" stroke-width="4" stroke-linecap="round"/>` +
    `<path d="M266,198q-6,4 -12,1" fill="none" stroke="${C.ink}" stroke-width="2"/>` +
    `<path d="M256,222Q263,225 270,220" fill="none" stroke="#a0524c" stroke-width="2.6"/>` +
    `<path d="M246,236q10,6 16,0" fill="none" stroke="#c48d76" stroke-width="1.6"/>`;
  ([[184, 112, 24], [210, 96, 20], [236, 93, 15], [170, 150, 24], [176, 192, 25], [182, 234, 24], [186, 272, 22], [160, 300, 24]] as [number, number, number][]).forEach(
    ([x, y, r]) => (front += curl(x, y, r)),
  );
  return `<g>${backMass}${coat}${neck}${jabot}${face}${front}</g>`;
}

/** sleeve + hand reaching right from the bust (bust coordinates) */
export const armReach = (hx: number, hy: number) =>
  `<path d="M330,400C380,${hy + 30} ${hx - 70},${hy + 20} ${hx - 30},${hy - 16}L${hx - 14},${hy + 22}C${hx - 60},${hy + 42} 400,410 352,448Z" fill="${C.blue}" stroke="${C.ink}" stroke-width="3"/>` +
  `<path d="M${hx - 36},${hy - 20}q14,-6 24,6q-6,14 -2,30q-14,8 -24,4" fill="#fbf7ef" stroke="${C.ink}" stroke-width="2.2"/>` +
  `<ellipse cx="${hx}" cy="${hy}" rx="20" ry="16" fill="${C.skin}" stroke="${C.ink}" stroke-width="2.6"/>`;
