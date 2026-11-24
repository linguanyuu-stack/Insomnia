"""Paper backdrop (public/paper.jpg) + caption font chunks (Noto Sans TC, SIL OFL 1.1).

Only the @fontsource unicode-range chunks containing characters used in src/ are
copied; src/font-manifest.json lists them. Re-run after changing caption text.
"""
import json, pathlib, re, shutil
import numpy as np, cv2
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
rng = np.random.default_rng(7)
H, W = 1080, 1920
base = np.array([251, 236, 216], np.float32)  # storyboard paper colour
blot = cv2.GaussianBlur(rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32), (0, 0), 6)
blot = cv2.resize(blot / blot.std(), (W, H), interpolation=cv2.INTER_CUBIC)
fib = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.7)
img = base + blot[..., None] * np.array([2.2, 2.6, 3.4]) + fib[..., None] * 2.4
yy, xx = np.mgrid[0:H, 0:W]
vig = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
img -= (np.clip(vig - 0.5, 0, None) * 22)[..., None] * np.array([0.8, 1.0, 1.3])
(ROOT / 'public').mkdir(exist_ok=True)
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(ROOT / 'public' / 'paper.jpg', quality=92)

src_text = ''.join(p.read_text('utf8') for p in (ROOT / 'src').rglob('*.ts*'))
cps = {ord(c) for c in src_text if ord(c) > 0x7e} | set(range(0x20, 0x7f))
out = ROOT / 'public' / 'fonts'
shutil.rmtree(out, ignore_errors=True)
out.mkdir(parents=True)
manifest = []
pkg = ROOT / 'node_modules' / '@fontsource' / 'noto-sans-tc'
for weight in ('500',):
    css = (pkg / f'{weight}.css').read_text()
    for block in css.split('@font-face')[1:]:
        ur = re.search(r'unicode-range:\s*([^;]+);', block).group(1)
        rs = []
        for part in ur.split(','):
            a, _, b = part.strip()[2:].partition('-')
            rs.append((int(a, 16), int(b or a, 16)))
        if not any(a <= cp <= b for cp in cps for a, b in rs):
            continue
        fn = re.search(r"url\(\./files/([^)]+\.woff2)\)", block).group(1)
        shutil.copy(pkg / 'files' / fn, out / fn)
        manifest.append({'file': 'fonts/' + fn, 'weight': weight, 'unicodeRange': ur.strip()})
(ROOT / 'src' / 'font-manifest.json').write_text(json.dumps(manifest, indent=1))
print(len(manifest), 'font chunks')
