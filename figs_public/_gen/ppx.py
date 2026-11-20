"""Helpers for pp-clocks / pp-forces / pp-3p (public edition plates)."""
import sys, os, re, math, random
sys.path.insert(0, '/home/user/Insomnia/figs/_gen')
from common import smooth, f, pts, rot  # noqa
from plib import cr, shade, tapered, poly, bez_pts, resample  # noqa

INK = '#2a2018'; PAPER = '#fbf6ea'
RED = '#b5473a'; RED_S = '#f0c4b8'; BLUE = '#3f6fa6'; BLUE_S = '#cfdcef'
YEL = '#d9b53c'; YEL_S = '#f6e7b0'; FLESH = '#f3d9c6'; FLESH_D = '#dcae93'
TCM = '#a8412c'; WEST = '#2c5d9c'; GOLD = '#c9962e'
OUT = '/home/user/Insomnia/figs_public'


def T(x, y, txt, cls='lb', anchor='start', size=None, color=None, weight=None, halo=True, extra=''):
    st = []
    if size: st.append('font-size:%spx' % size)
    if color: st.append('fill:%s' % color)
    if weight: st.append('font-weight:%s' % weight)
    s = ' style="%s"' % ';'.join(st) if st else ''
    a = '' if anchor == 'start' else ' text-anchor="%s"' % anchor
    h = ' halo' if halo else ''
    return '<text x="%s" y="%s" class="%s%s"%s%s%s>%s</text>' % (f(x), f(y), cls, h, a, s, extra, txt)


def lab2(x, y, zh, en=None, anchor='start', size=14, color=None, ensize=12, gap=15):
    o = T(x, y, zh, 'lb', anchor, size=size, color=color)
    if en:
        o += T(x, y + gap, en, 'le', anchor, size=ensize)
    return o


def lead(P, dot=True, extra=''):
    m = ' marker-end="url(#ink-dot)"' if dot else ''
    return '<path class="ld" d="%s"%s%s/>' % (poly(P), m, extra)


def clockface(x, y, r, hh=7, mm=0, face='#fffaf0', bezel='#c9962e', ticks=True):
    s = ['<g transform="translate(%s,%s)">' % (f(x), f(y)),
         '<circle r="%s" fill="%s" stroke="%s" stroke-width=".9"/>' % (f(r + r * .22), bezel, INK),
         '<circle r="%s" fill="%s" stroke="%s" stroke-width=".6"/>' % (f(r), face, INK)]
    if ticks:
        d = ''
        for i in range(12):
            a = math.radians(i * 30)
            l0 = r * .92; l1 = r * (.7 if i % 3 == 0 else .8)
            d += 'M%s %sL%s %s' % (f(l0 * math.sin(a)), f(-l0 * math.cos(a)), f(l1 * math.sin(a)), f(-l1 * math.cos(a)))
        s.append('<path d="%s" stroke="%s" stroke-width="%s"/>' % (d, INK, f(max(.5, r * .07))))
    ha = math.radians((hh % 12 + mm / 60) * 30); ma = math.radians(mm * 6)
    s.append('<path d="M0 0L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
        f(r * .5 * math.sin(ha)), f(-r * .5 * math.cos(ha)), INK, f(max(1, r * .15))))
    s.append('<path d="M0 0L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
        f(r * .78 * math.sin(ma)), f(-r * .78 * math.cos(ma)), INK, f(max(.7, r * .09))))
    s.append('<circle r="%s" fill="%s"/></g>' % (f(max(.9, r * .1)), INK))
    return ''.join(s)


_CLS = {'ink': '1.1', 'ink2': '.6', 'ink3': '1.8'}


def fixfill(body):
    def rep(m):
        tag = m.group(0)
        if re.search(r'class="ink[23]?"', tag) and ' fill="' in tag and 'style=' not in tag:
            tag = re.sub(r' fill="([^"]*)"', r' style="fill:\1"', tag, count=1)
        return tag
    return re.sub(r'<(path|ellipse|circle|rect|polygon)\b[^>]*>', rep, body)


def write(pid, pn, ptt, pte, H, body, aria, caption, defs=''):
    body = fixfill(body)
    html = ('<figure class="plate" id="%s">\n<div class="pt"><span class="pn">%s</span><span class="ptt">%s</span><span class="pte">%s</span></div>\n'
            '<svg viewBox="0 0 760 %d" role="img" aria-label="%s">\n%s%s\n</svg>\n<figcaption>%s</figcaption>\n</figure>\n') % (
        pid, pn, ptt, pte, H, aria, ('<defs>' + defs + '</defs>\n') if defs else '', body, caption)
    for m in re.finditer(r'\sid="([^"]+)"', html):
        assert m.group(1).startswith(pid), m.group(1)
    p = os.path.join(OUT, pid + '.html')
    open(p, 'w').write(html)
    print('wrote', p, len(html), 'bytes')
