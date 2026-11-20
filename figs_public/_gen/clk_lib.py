"""Shared helpers for the circadian-history plates (pp-mimosa, pp-cave, pp-nobel). Reuses figs/_gen helpers read-only."""
import sys, os, re, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(1, os.path.join(ROOT, 'figs', '_gen'))
from plib import f, cr, poly, bez_pts, resample, ticks, tapered, num, INK, PAPER, RED, RED_S, BLUE, BLUE_S, YEL, YEL_S, FLESH, FLESH_D, BONE, GOLD  # noqa
import lib as L  # noqa  (head, hand, clock)


def write(pid, pn, ptt, pte, H, body, aria, caption, defs=''):
    html = ('<figure class="plate" id="%s">\n<div class="pt"><span class="pn">%s</span><span class="ptt">%s</span><span class="pte">%s</span></div>\n'
            '<svg viewBox="0 0 760 %d" role="img" aria-label="%s">\n%s%s\n</svg>\n<figcaption>%s</figcaption>\n</figure>\n') % (
        pid, pn, ptt, pte, H, aria, ('<defs>' + defs + '</defs>\n') if defs else '', body, caption)
    for m in re.finditer(r'\sid="([^"]+)"', html):
        assert m.group(1).startswith(pid), m.group(1)
    p = os.path.join(ROOT, 'figs_public', pid + '.html')
    open(p, 'w').write(html)
    print('wrote', p, len(html), 'bytes')


def T(x, y, s, cls='lb', anchor='start', halo=True, style=''):
    a = '' if anchor == 'start' else ' text-anchor="%s"' % anchor
    st = ' style="%s"' % style if style else ''
    return '<text x="%s" y="%s" class="%s%s"%s%s>%s</text>' % (f(x), f(y), cls, ' halo' if halo else '', a, st, s)


def lead(pts, dot=True):
    return '<path class="ld" d="%s"%s/>' % (poly(pts), ' marker-end="url(#ink-dot)"' if dot else '')


def rot(u, v, x, y, ang):
    a = math.radians(ang)
    return (x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a))


def sun(x, y, r, col='#f0b64a'):
    o = ['<g>']
    for i in range(12):
        a = math.radians(i * 30)
        o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.4" stroke-linecap="round"/>' % (
            f(x + math.cos(a) * r * 1.35), f(y + math.sin(a) * r * 1.35), f(x + math.cos(a) * r * 1.8), f(y + math.sin(a) * r * 1.8), INK))
    o.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="1.1"/>' % (f(x), f(y), f(r), col, INK))
    o.append('</g>')
    return ''.join(o)


def moon(x, y, r, col='#f6e7b0'):
    d = 'M%s %s A%s %s 0 1 0 %s %s A%s %s 0 1 1 %s %s Z' % (
        f(x + r * .35), f(y - r * .94), f(r), f(r), f(x + r * .35), f(y + r * .94), f(r * .78), f(r * .78), f(x + r * .35), f(y - r * .94))
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (d, col, INK)
