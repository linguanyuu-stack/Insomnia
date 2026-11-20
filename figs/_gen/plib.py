"""Small helpers for hand-built engraving-style plates (chapter 1).
Each plate script imports this and writes figs/<id>.html."""
import math, os, subprocess, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INK = '#2a2018'; PAPER = '#fbf6ea'
RED = '#b5473a'; RED_S = '#f0c4b8'; BLUE = '#3f6fa6'; BLUE_S = '#cfdcef'
YEL = '#d9b53c'; YEL_S = '#f6e7b0'; FLESH = '#f3d9c6'; FLESH_D = '#dcae93'
NERVE = '#e8cf7a'; BONE = '#efe6d2'; TCM = '#a8412c'; WEST = '#2c5d9c'; GOLD = '#c9962e'


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def cr(pts, closed=False, k=1.0):
    """Catmull-Rom spline through pts -> SVG path d (cubic Beziers)."""
    n = len(pts)
    if n < 2:
        return ''
    P = list(pts)
    d = 'M%s %s' % (f(P[0][0]), f(P[0][1]))
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = P[(i - 1) % n] if (closed or i > 0) else P[i]
        p1 = P[i]
        p2 = P[(i + 1) % n]
        p3 = P[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        d += 'C%s %s %s %s %s %s' % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    if closed:
        d += 'Z'
    return d


def poly(pts, closed=False):
    d = 'M' + ' L'.join('%s %s' % (f(x), f(y)) for x, y in pts)
    return d + ('Z' if closed else '')


def resample(pts, step, closed=False):
    """Linear resample of a polyline at roughly equal spacing."""
    P = list(pts) + ([pts[0]] if closed else [])
    out = [P[0]]
    acc = 0
    for a, b in zip(P, P[1:]):
        L = math.dist(a, b)
        if L == 0:
            continue
        t = step - acc
        while t <= L:
            out.append((a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L))
            t += step
        acc = L - (t - step)
    return out


def bez_pts(pts, closed=False, per=10):
    """Sample the Catmull-Rom curve into a dense polyline."""
    n = len(pts)
    out = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        for s in range(per):
            t = s / per
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(pts[-1])
    return out


def ticks(pts, side=1, step=3.2, l0=3, l1=7, w=.45, op=.55, seed=1, smooth=True, color=INK):
    """Engraving ticks perpendicular to a curve (on one side) to model a sulcus/fold shadow."""
    import random
    rnd = random.Random(seed)
    dense = bez_pts(pts, per=12) if smooth else pts
    P = resample(dense, step)
    d = ''
    n = len(P)
    for i in range(1, n - 1):
        a, b = P[i - 1], P[i + 1]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L * side, tx / L * side
        fade = min(1, i / 3, (n - 1 - i) / 3)
        ln = (l0 + (l1 - l0) * rnd.random()) * fade
        x, y = P[i]
        d += 'M%s %s l%s %s' % (f(x), f(y), f(nx * ln), f(ny * ln))
    return '<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s" fill="none"/>' % (d, color, w, op)


def shade(pid, d, dx, dy, pat='ink-hatch', op=1, extra=''):
    """Crescent shadow: fill shape with pattern, masked to the side opposite (dx,dy)."""
    return ('<mask id="%s"><path d="%s" fill="#fff"/><path d="%s" transform="translate(%s %s)" fill="#000"/></mask>'
            '<path d="%s" fill="url(#%s)" mask="url(#%s)" opacity="%s" %s/>') % (pid, d, d, f(dx), f(dy), d, pat, pid, op, extra)


def label(side, xcol, y, zh, en=None, target=None, en_inline=False, color=None, stub=10, elbow=None, cls='lb', dot=True, sub=None):
    """Column label. side 'L' -> text-anchor end at xcol, 'R' -> start at xcol.
    Leader from column edge to target (with optional elbow x)."""
    anc = 'end' if side == 'L' else 'start'
    out = []
    fill = ' style="fill:%s"' % color if color else ''
    if en and en_inline:
        out.append('<text x="%s" y="%s" text-anchor="%s" class="%s halo"%s>%s <tspan class="le">%s</tspan></text>' % (f(xcol), f(y), anc, cls, fill, zh, en))
    else:
        out.append('<text x="%s" y="%s" text-anchor="%s" class="%s halo"%s>%s</text>' % (f(xcol), f(y), anc, cls, fill, zh))
        if en:
            out.append('<text x="%s" y="%s" text-anchor="%s" class="le halo">%s</text>' % (f(xcol), f(y + 13.5), anc, en))
    if sub:
        out.append('<text x="%s" y="%s" text-anchor="%s" class="ls halo">%s</text>' % (f(xcol), f(y + (27 if en and not en_inline else 13.5)), anc, sub))
    if target:
        sx = xcol + 4 if side == 'L' else xcol - 4
        sy = y - 4.5
        pts = [(sx, sy)]
        ex = elbow if elbow is not None else (sx + stub if side == 'L' else sx - stub)
        pts.append((ex, sy))
        pts.append(target)
        mk = ' marker-end="url(#ink-dot)"' if dot else ''
        out.insert(0, '<path class="ld" d="%s"%s/>' % (poly(pts), mk))
    return '\n'.join(out)


def mol(smiles, w, h):
    s = subprocess.run(['python3', os.path.join(ROOT, 'kit', 'mol.py'), smiles, str(w), str(h)], capture_output=True, text=True).stdout
    s = '\n'.join(l for l in s.splitlines() if not l.startswith('<!--'))
    return s


def write(pid, pn, ptt, pte, H, body, aria, caption, defs=''):
    html = ('<figure class="plate" id="%s">\n<div class="pt"><span class="pn">%s</span><span class="ptt">%s</span><span class="pte">%s</span></div>\n'
            '<svg viewBox="0 0 760 %d" role="img" aria-label="%s">\n%s%s\n</svg>\n<figcaption>%s</figcaption>\n</figure>\n') % (
        pid, pn, ptt, pte, H, aria, ('<defs>' + defs + '</defs>\n') if defs else '', body, caption)
    # sanity: every id must be prefixed
    for m in re.finditer(r'\sid="([^"]+)"', html):
        assert m.group(1).startswith(pid), m.group(1)
    p = os.path.join(ROOT, 'figs', pid + '.html')
    open(p, 'w').write(html)
    print('wrote', p, len(html), 'bytes')


def distribute(ys, ymin, ymax, gap):
    """Given desired label y's (sorted), push apart to min gap within [ymin,ymax]."""
    out = list(ys)
    for i in range(len(out)):
        out[i] = max(out[i], ymin if i == 0 else out[i - 1] + gap)
    if out and out[-1] > ymax:
        out[-1] = ymax
        for i in range(len(out) - 2, -1, -1):
            out[i] = min(out[i], out[i + 1] - gap)
    return out


def column(side, xcol, items, ymin, ymax, gap=30, **kw):
    """items: list of dict(t=(x,y), zh=, en=, dy=offset, color=)"""
    items = sorted(items, key=lambda d: d['t'][1] + d.get('bias', 0))
    ys = distribute([d['t'][1] + d.get('dy', 0) for d in items], ymin, ymax, gap)
    out = []
    for d, y in zip(items, ys):
        out.append(label(side, xcol, y, d['zh'], d.get('en'), d['t'], color=d.get('color'), elbow=d.get('elbow'), sub=d.get('sub'), **kw))
    return '\n'.join(out)


def ray_hit(poly_pts, c, ang):
    """Distance from c along angle (deg) to first polygon edge."""
    dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    best = 1e9
    n = len(poly_pts)
    for i in range(n):
        (x1, y1), (x2, y2) = poly_pts[i], poly_pts[(i + 1) % n]
        ex, ey = x2 - x1, y2 - y1
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = ((x1 - c[0]) * ey - (y1 - c[1]) * ex) / den
        u = ((x1 - c[0]) * dy - (y1 - c[1]) * dx) / den
        if t > 0 and 0 <= u <= 1:
            best = min(best, t)
    return best


_CLS = {
    'ink': dict(fill='none', stroke=INK, **{'stroke-width': '1.1', 'stroke-linecap': 'round', 'stroke-linejoin': 'round'}),
    'ink2': dict(fill='none', stroke=INK, **{'stroke-width': '.6', 'stroke-linecap': 'round', 'stroke-linejoin': 'round'}),
    'ink3': dict(fill='none', stroke=INK, **{'stroke-width': '1.8', 'stroke-linecap': 'round', 'stroke-linejoin': 'round'}),
    'ld': dict(fill='none', stroke=INK, **{'stroke-width': '.7'}),
}


def inline_classes(s):
    """Replace drawing classes by presentation attributes (explicit attributes win),
    so the markup also renders inside <use> and lets fill= / stroke-width= attributes take effect."""
    def fix(m):
        tag = m.group(0)
        cm = re.search(r'\sclass="(ink|ink2|ink3|ld)"', tag)
        if not cm:
            return tag
        attrs = _CLS[cm.group(1)]
        tag = tag.replace(cm.group(0), '')
        add = ''
        for k, v in attrs.items():
            if not re.search(r'\s%s="' % re.escape(k), tag):
                add += ' %s="%s"' % (k, v)
        return re.sub(r'^<(\w+)', lambda mm: '<' + mm.group(1) + add, tag)
    return re.sub(r'<(path|ellipse|circle|rect|line|polyline|polygon)\b[^>]*>', fix, s)
