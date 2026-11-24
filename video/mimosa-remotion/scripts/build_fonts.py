"""Build small font subsets into public/fonts from the @fontsource packages.

LXGW WenKai TC is shipped by fontsource as ~100 unicode-range chunks; this subsets
the chunks we need to the characters actually used in src/.
Run: npm run fonts   (requires: pip install fonttools brotli)
"""
import json, pathlib, re, shutil
from fontTools.ttLib import TTFont
from fontTools import subset

ROOT = pathlib.Path(__file__).resolve().parent.parent
NM = ROOT / 'node_modules' / '@fontsource'
OUT = ROOT / 'public' / 'fonts'
OUT.mkdir(parents=True, exist_ok=True)

text = ''.join(p.read_text('utf8') for p in (ROOT / 'src').rglob('*.ts*'))
chars = sorted(set(c for c in text if ord(c) > 0x7e) | set(chr(c) for c in range(0x20, 0x7f)))
codepoints = [ord(c) for c in chars]

def ranges(css_block):
    m = re.search(r'unicode-range:\s*([^;]+);', css_block)
    out = []
    for part in m.group(1).split(','):
        part = part.strip()[2:]
        a, _, b = part.partition('-')
        out.append((int(a, 16), int(b or a, 16)))
    return out

manifest = []
for old in OUT.glob('wenkai-*.woff2'):
    old.unlink()
for weight in ('400', '700'):
    css = (NM / 'lxgw-wenkai-tc' / f'{weight}.css').read_text()
    for block in css.split('@font-face')[1:]:
        rs = ranges(block)
        used = [cp for cp in codepoints if any(a <= cp <= b for a, b in rs)]
        if not used or all(cp < 0x7f for cp in used) and 'latin' not in block:
            continue
        src = re.search(r"url\(\./files/([^)]+\.woff2)\)", block).group(1)
        ft = TTFont(NM / 'lxgw-wenkai-tc' / 'files' / src)
        opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['*']
        sub = subset.Subsetter(opts); sub.populate(unicodes=used); sub.subset(ft)
        name = f'wenkai-{weight}-{len([m for m in manifest if m["weight"] == weight])}.woff2'
        ft.flavor = 'woff2'; ft.save(OUT / name)
        manifest.append({'file': 'fonts/' + name, 'weight': weight,
                         'unicodeRange': ','.join('U+%04X' % cp for cp in used)})
    print('wenkai', weight, len([m for m in manifest if m['weight'] == weight]), 'files')
(ROOT / 'src' / 'lib' / 'wenkai-manifest.json').write_text(json.dumps(manifest, indent=1))

shutil.copy(NM / 'im-fell-english/files/im-fell-english-latin-400-normal.woff2', OUT / 'fell-400.woff2')
shutil.copy(NM / 'im-fell-english/files/im-fell-english-latin-400-italic.woff2', OUT / 'fell-400-italic.woff2')
shutil.copy(NM / 'pinyon-script/files/pinyon-script-latin-400-normal.woff2', OUT / 'pinyon-400.woff2')
print('done')
