import { loadFont } from '@remotion/fonts';
import { staticFile } from 'remotion';
import { FONT } from './theme';
import wenkai from './wenkai-manifest.json';

// WenKai files are subsets of LXGW WenKai TC (SIL OFL 1.1) containing only the glyphs
// used in src/ — run `npm run fonts` after changing any Chinese text.
export const fontsReady = Promise.all([
  ...wenkai.map((c) => loadFont({ family: FONT.kai, url: staticFile(c.file), weight: c.weight, unicodeRange: c.unicodeRange })),
  loadFont({ family: FONT.fell, url: staticFile('fonts/fell-400.woff2'), weight: '400' }),
  loadFont({ family: FONT.fell, url: staticFile('fonts/fell-400-italic.woff2'), weight: '400', style: 'italic' }),
  loadFont({ family: FONT.script, url: staticFile('fonts/pinyon-400.woff2'), weight: '400' }),
]);
