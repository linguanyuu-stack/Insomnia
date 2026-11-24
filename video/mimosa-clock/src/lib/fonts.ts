import { loadFont } from '@remotion/fonts';
import { staticFile } from 'remotion';
import chunks from '../font-manifest.json';

export const CAPTION_FONT = 'NotoSansTC';

// Noto Sans TC (SIL OFL 1.1) — only the unicode-range chunks used by the captions.
// Run `npm run assets` after changing caption text.
export const fontsReady = Promise.all(
  chunks.map((c) => loadFont({ family: CAPTION_FONT, url: staticFile(c.file), weight: c.weight, unicodeRange: c.unicodeRange })),
);
