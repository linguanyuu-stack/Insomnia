/* insomnia.js: the series' own pieces for 重新認識失眠 shorts, loaded after shorts.js.
   A pocket watch drawn in code (its hands are groups to turn), sun and moon, a slow push on a plate piece, a struck-out
   word, the series card. Colours follow the public edition's plates. */
'use strict';
const NIGHT = '#1f2a44', GOLD = '#c9962e', CREAM = '#f6efe0', INK = '#2a2018', LEAF = '#6f8a3f', BLUE = '#3f6fa6';
const SERIES = ['身體裡的時鐘', '為什麼會想睡', '什麼才叫失眠'];

// a pocket watch at (x, y), radius r. Returns { g, hour, minute, ghost }: hands point up at r 0, turned by state r
// (degrees). ghost is a red minute hand (the true time), hidden until shown.
function watch(p, x, y, r, { t0, face = '#fffaf0', ghost = false } = {}) {
  const g = G(p, { x, y, o: t0 === undefined ? 1 : 0, s: t0 === undefined ? 1 : .6 });
  mk('circle', { cx: 0, cy: -r - r * .16, r: r * .1, fill: 'none', stroke: GOLD, 'stroke-width': r * .045 }, g);   // the bow
  rect(g, -r * .08, -r - r * .12, r * .16, r * .14, { fill: GOLD, stroke: INK, 'stroke-width': 3, rx: 4 });        // the crown
  mk('circle', { r: r * 1.04, fill: GOLD, stroke: INK, 'stroke-width': r * .03 }, g);
  mk('circle', { r: r * .92, fill: face, stroke: INK, 'stroke-width': r * .015 }, g);
  for (let i = 0; i < 60; i++) {
    const a = i * Math.PI / 30, big = i % 5 === 0, r0 = r * (big ? .76 : .83), r1 = r * .88;
    path(g, `M${r0 * Math.sin(a)} ${-r0 * Math.cos(a)}L${r1 * Math.sin(a)} ${-r1 * Math.cos(a)}`, { stroke: INK, 'stroke-width': big ? r * .028 : r * .01 });
  }
  const hand = (len, w, col) => { const h = G(g, {}); path(h, `M0 ${r * .12}L0 ${-len}`, { stroke: col, 'stroke-width': w }); return h; };
  const gh = hand(r * .74, r * .028, RED); put(gh, { o: ghost ? 1 : 0 });
  const hour = hand(r * .48, r * .06, INK), minute = hand(r * .74, r * .04, INK);
  mk('circle', { r: r * .06, fill: INK }, g);
  if (t0 !== undefined) tw(g, { o: 1, s: 1 }, t0, .4, back);
  return { g, hour, minute, ghost: gh };
}
// a watch's time: minutes since 12:00 put on both hands
const setTime = (w, min) => { put(w.minute, { r: min * 6 }); put(w.hour, { r: min * .5 }); };

// a sun or a moon drawn in ink
function sun(p, x, y, r, t0) {
  const g = G(p, { x, y, o: t0 === undefined ? 1 : 0, s: t0 === undefined ? 1 : .4 });
  mk('circle', { r: r * 1.9, fill: '#f6d77a', opacity: .35 }, g);
  for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; path(g, `M${r * 1.25 * Math.cos(a)} ${r * 1.25 * Math.sin(a)}L${r * 1.65 * Math.cos(a)} ${r * 1.65 * Math.sin(a)}`, { stroke: GOLD, 'stroke-width': r * .12 }); }
  mk('circle', { r, fill: '#f0c84a', stroke: INK, 'stroke-width': r * .07 }, g);
  if (t0 !== undefined) tw(g, { o: 1, s: 1 }, t0, .45, back);
  return g;
}
function moon(p, x, y, r, t0) {
  const g = G(p, { x, y, o: t0 === undefined ? 1 : 0, s: t0 === undefined ? 1 : .4 });
  path(g, `M${r * .2} ${-r}A${r} ${r} 0 1 0 ${r * .2} ${r}A${r * .78} ${r * .78} 0 1 1 ${r * .2} ${-r}Z`, { fill: '#f6e7b0', stroke: INK, 'stroke-width': r * .07 });
  if (t0 !== undefined) tw(g, { o: 1, s: 1 }, t0, .45, back);
  return g;
}

// a plate piece (img/<name>.webp, size from ART) h or w px, centred on (x, y), pushed from s0 to s1 over t0..t1
function piece(p, name, x, y, t0, t1, { h, w, s0 = 1, s1 = 1.08, dx = 0, dy = 0, enter } = {}) {
  const g = G(p, { x, y, s: s0 });
  const e = plate(g, name, 0, 0, { h, w, t0: enter });
  tw(g, { s: s1, x: x + dx, y: y + dy }, t0, Math.max(.01, t1 - t0), lin);
  return g;
}

// a red line struck through a word drawn with word() (its width in e._w)
function strike(p, e, x, y, t0, size) {
  const w = e._w + 30;
  const l = path(p, `M${x - w / 2} ${y - size * .3}L${x + w / 2} ${y - size * .42}`, { stroke: RED, 'stroke-width': size / 9 }, { d: 0 });
  draw(l, t0, .25, out);
  sfx(BEAT_ID, t0, 'whoosh', .4);
  return l;
}

// a soft dark veil over a shot, faded in at t0
function veil(p, t0, o = .6, dur = .35, colour = '#000') {
  const v = rect(p, -20, -20, W + 40, H + 40, { fill: colour });
  put(v, { o: 0 }); tw(v, { o }, t0, dur, lin);
  return v;
}

// the series card: the name, then each episode, this one lit
function seriesCard(s, t0, n, { lead } = {}) {
  rect(s, -20, -20, W + 40, H + 40, { fill: NIGHT });
  moon(s, 700, 300, 46, t0);
  for (let i = 0; i < 26; i++) { const R = seeded(i + 3); mk('circle', { cx: 60 + R() * 780, cy: 160 + R() * 260, r: 1.5 + R() * 2.5, fill: '#f6e7b0', opacity: .7 }, s); }
  word(s, '重新認識失眠', CX, 560, t0, { size: 116, fill: CREAM });
  T(s, '給睡不好的你和家人', { x: CX, y: 650, size: 44, fill: '#b9b2a2', font: SANS, weight: 500, anchor: 'middle' });
  SERIES.forEach((str, i) => {
    const on = i + 1 === n, y = 820 + i * 130;
    const e = G(s, { x: CX, y, o: 0 });
    rect(e, -330, -62, 660, 100, { fill: on ? RED : 'none', stroke: on ? RED : '#55607a', 'stroke-width': 3, rx: 10 });
    T(e, `${i + 1}`, { x: -290, y: 10, size: 52, fill: on ? CREAM : '#7d869c', font: SANS, weight: 600 });
    T(e, str, { x: -220, y: 10, size: 52, fill: on ? CREAM : '#7d869c', font: SANS, weight: 600 });
    tw(e, { o: 1 }, t0 + .15 + i * .12, .25, out);
    if (on) { put(e, { s: .96 }); tw(e, { s: 1.06 }, (lead ?? t0) + .5, .3, back); }
  });
  if (lead === undefined) T(s, '…', { x: CX, y: 1250, size: 60, fill: '#7d869c', font: SANS, weight: 600, anchor: 'middle' });
}

// the fonts must be in before words are measured: Oswald and EB Garamond (the kit's) and the Chinese chunks this page uses
const startSeries = () => {
  const text = [...document.querySelectorAll('script')].map(s => s.textContent).join('') + JSON.stringify(TIMINGS) + SERIES.join('');
  const zh = [...new Set(text.match(/[　-鿿＀-￯]/g) || [])].join('');
  return Promise.all(['600 40px Oswald', '500 40px Oswald', 'italic 400 40px "EB Garamond"', '400 40px "EB Garamond"']
    .map(f => document.fonts.load(f)).concat(['500', '600'].map(w => document.fonts.load(`${w} 40px "Noto Sans TC"`, zh))))
    .then(boot);
};
