// Render index.html frame-by-frame to MP4 (or stills).
//   node render.js                 -> mimosa-1729.mp4
//   node render.js --stills 1,3.5  -> stills/t1.png, stills/t3.5.png
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

(async () => {
  const args = process.argv.slice(2);
  const stillsArg = args.includes('--stills') ? args[args.indexOf('--stills') + 1] : null;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'index.html') + '?render=1');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  await page.evaluate(() => document.fonts.ready);
  const svg = await page.$('#stage');

  if (stillsArg) {
    fs.mkdirSync(path.join(__dirname, 'stills'), { recursive: true });
    for (const t of stillsArg.split(',').map(Number)) {
      await page.evaluate(t => window.render(t), t);
      await svg.screenshot({ path: path.join(__dirname, 'stills', `t${t}.png`) });
    }
    await browser.close();
    return;
  }

  const fps = await page.evaluate(() => window.FPS);
  const dur = await page.evaluate(() => window.DURATION);
  const out = path.join(__dirname, 'mimosa-1729.mp4');
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'ignore', 'inherit'] });
  const n = Math.round(fps * dur);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.render(t), i / fps);
    const buf = await svg.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 30 === 0) process.stderr.write(`frame ${i}/${n}\n`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('wrote', out);
})();
