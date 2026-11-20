#!/usr/bin/env python3
"""Public edition: public/source.html + plates (figs_public/pp-*.html, figs/pl-*.html)
-> 重新認識失眠_民眾版.html.  Marker syntax in source: <!--PLATE:id--> or <!--PLATE:id|plain-language caption-->"""
import re, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
sys.path.insert(0, P('kit'))
from platelib import slim, pack, COMPRESS

s = open(P('public/source.html'), encoding='utf-8').read()
build_src = open(P('kit/build.py'), encoding='utf-8').read()
loader = re.search(r'sub1\(\'</head>\', """(.*?)"""\)', build_src, re.S).group(1)

plate_css = open(P('kit/plate.css'), encoding='utf-8').read()
s = s.replace('</style>', plate_css + '\n</style>', 1)
s = s.replace('<div class="wrap">', '<div class="wrap">\n' + open(P('kit/defs.svg'), encoding='utf-8').read(), 1)
if COMPRESS:
    s = s.replace('</head>', loader, 1)

missing, n = [], 0
def repl(m):
    global n
    pid, cap = m.group(1), m.group(2)
    f = P('figs_public' if pid.startswith('pp-') else 'figs', pid + '.html')
    if not os.path.exists(f):
        missing.append(pid)
        return f'<div class="plate-z">（圖版製作中：{pid}）</div>'
    snip = open(f, encoding='utf-8').read().strip()
    snip = re.sub(r'^<!--.*?-->\s*', '', snip, flags=re.S)
    if cap:
        t = re.search(r'<span class="ptt">(.*?)</span>', snip)
        title = re.sub('<[^>]+>', '', t.group(1)) if t else ''
        snip = re.sub(r'<figcaption>.*?</figcaption>', f'<figcaption><b>{title}。</b>{cap}</figcaption>', snip, flags=re.S)
        # doctors'-edition plate numbers (Plate 3·A) mean nothing here
        snip = re.sub(r'<span class="pn">.*?</span>', '<span class="pn">醫師版圖版</span>', snip, count=1)
    n += 1
    return pack(pid, slim(snip))
s = re.sub(r'<!--PLATE:([\w-]+)(?:\|(.*?))?-->', repl, s, flags=re.S)

out = P('重新認識失眠_民眾版.html')
open(out, 'w', encoding='utf-8').write(s)
size = len(s.encode('utf-8'))
print('wrote', out, size // 1024, 'KB |', n, 'plates | missing:', missing or 'none')
if size > 950_000:
    sys.exit('WARNING: over ~950 KB (app preview truncates near 1 MB)')
