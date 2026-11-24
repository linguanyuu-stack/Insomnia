import { FPS } from './lib/theme';

/** Scene lengths in frames (30 fps). Edit here to re-time the video. */
export const SCENES = {
  year: 105, // 1729
  mairan: 135, // the astronomer
  mimosa: 165, // leaves open by day, fold at night
  wonder: 195, // "is it watching the sun?"
  cabinet: 285, // the dark cabinet experiment
  clock: 140, // an inner clock
};
/** crossfade between scenes, in frames */
export const TRANSITION = 15;

const order = ['year', 'mairan', 'mimosa', 'wonder', 'cabinet', 'clock'] as const;
export const SCENE_START: Record<(typeof order)[number], number> = {} as never;
let acc = 0;
for (const k of order) {
  SCENE_START[k] = acc;
  acc += SCENES[k] - TRANSITION;
}
export const TOTAL_FRAMES = acc + TRANSITION;

const s = (scene: (typeof order)[number], sec: number) => SCENE_START[scene] + Math.round(sec * FPS);

/** Narration / subtitles: [from frame, to frame, text] on the main timeline */
export const CAPTIONS: [number, number, string][] = [
  [s('year', 0.3), s('year', 3.0), '時間是 1729 年。'],
  [s('mairan', 0.2), s('mairan', 4.2), '天文學家德梅朗（Jean-Jacques d’Ortous de Mairan）'],
  [s('mimosa', 0.2), s('mimosa', 5.0), '他注意到，含羞草的葉子在白天張開、晚上合起來。'],
  [s('wonder', 0.2), s('wonder', 3.05), '那時，大家都以為那是植物在「看太陽」。'],
  [s('wonder', 3.2), s('wonder', 6.3), '但他想知道：如果看不到太陽呢？'],
  [s('cabinet', 0.2), s('cabinet', 3.9), '德梅朗把觀察的那一株含羞草，放進不透光的櫃子裡。'],
  [s('cabinet', 4.05), s('cabinet', 9.3), '結果，葉子沒因照不到太陽，照樣在白天張開、在晚上合起來。'],
  [s('clock', 0.3), s('clock', 4.5), '就像植物身體裡，有自己的時鐘。'],
];
