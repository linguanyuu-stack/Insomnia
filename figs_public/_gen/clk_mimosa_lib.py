"""Mimosa pudica drawing: bipinnate leaves (2 pairs of digitate pinnae), pink pom-pom heads."""
import math, random
from clk_lib import f, cr, tapered, rot, INK

LEAF_G = '#93ad5c'; LEAF_D = '#6f8a3f'; STEM = '#8d4a36'


def leaflet(cx, cy, ang, l, w):
    """compact oblong leaflet sub-path (base at cx,cy, pointing along ang)"""
    a = rot(l * .5, -w * 1.05, cx, cy, ang); t = rot(l, 0, cx, cy, ang); b = rot(l * .55, w * 1.0, cx, cy, ang)
    return 'M%s %sQ%s %s %s %sQ%s %s %s %sZ' % (f(cx), f(cy), f(a[0]), f(a[1]), f(t[0]), f(t[1]), f(b[0]), f(b[1]), f(cx), f(cy))


def pinna(x, y, ang, R, s, closed, rnd, n=11):
    out = []
    bend = rnd.uniform(-6, 6)
    mid = [rot(R * t, bend * math.sin(math.pi * t) * s, x, y, ang) for t in (0, .33, .66, 1)]
    dA, dB = '', ''
    for i in range(n):
        t = .1 + .86 * i / (n - 1)
        # point on rachis + local tangent
        px, py = rot(R * t, bend * math.sin(math.pi * t) * s, x, y, ang)
        ta = ang + math.degrees(math.atan2(bend * math.pi * math.cos(math.pi * t) * s, R))
        taper = .62 + .38 * math.sin(math.pi * min(1, t * 1.15))
        l = 7.2 * s * taper
        w = 2.5 * s * taper
        if closed:
            # pairs folded upward face to face: seen as one narrow leaflet pressed forward
            dA += leaflet(px, py, ta - 16, l * 1.02, w * .6)
        else:
            dA += leaflet(px, py, ta - 68, l, w)
            dB += leaflet(px, py, ta + 68, l, w)
    if dA:
        out.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".38"/>' % (dA, LEAF_D if closed else LEAF_G, INK))
    if dB:
        out.append('<path d="%s" fill="#a9c172" stroke="%s" stroke-width=".38"/>' % (dB, INK))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (cr(mid), '#5f6e32', f(.75 * s + .2)))
    return ''.join(out)


def leaf(x, y, ang, s, closed, seed=1):
    """Bipinnate leaf: petiole from (x,y) direction ang (deg, SVG), 4 digitate pinnae."""
    rnd = random.Random(seed)
    right = math.cos(math.radians(ang)) >= 0
    if closed:
        ang = ang + (42 if right else -42)
    P = 26 * s
    tip = rot(P, 0, x, y, ang)
    out = ['<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
        cr([(x, y), rot(P * .5, -2 * s, x, y, ang), tip]), '#6c5a2c', f(1.1 * s + .3))]
    # pulvinus swelling at base
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#7d8a42" stroke="%s" stroke-width=".4" transform="rotate(%s %s %s)"/>' % (
        f(x), f(y), f(3 * s), f(1.8 * s), INK, f(ang), f(x), f(y)))
    spread = [-8, -3, 3, 8] if closed else [-36, -12, 12, 36]
    for i, sp in enumerate(spread):
        R = 46 * s * (.86 if i in (0, 3) else 1)
        out.append(pinna(tip[0], tip[1], ang + sp, R, s, closed, rnd))
    return ''.join(out)


def pompom(x, y, r, seed=3):
    rnd = random.Random(seed)
    o = ['<circle cx="%s" cy="%s" r="%s" fill="#e9a9c6" stroke="none"/>' % (f(x), f(y), f(r * .45))]
    d = ''
    dots = []
    for i in range(46):
        a = rnd.uniform(0, 2 * math.pi)
        rr = r * rnd.uniform(.7, 1.0)
        ex, ey = x + math.cos(a) * rr, y + math.sin(a) * rr
        d += 'M%s %sL%s %s' % (f(x + math.cos(a) * r * .25), f(y + math.sin(a) * r * .25), f(ex), f(ey))
        dots.append('<circle cx="%s" cy="%s" r="%s" fill="#f7e3a0"/>' % (f(ex), f(ey), f(max(.45, r * .07))))
    o.append('<path d="%s" stroke="#c4568a" stroke-width=".55" fill="none"/>' % d)
    o.extend(dots)
    o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#c4568a" stroke-width=".4" stroke-dasharray="1.5 2" opacity=".7"/>' % (f(x), f(y), f(r * .55)))
    return ''.join(o)


def bud(x, y, r):
    return '<circle cx="%s" cy="%s" r="%s" fill="#d98fb2" stroke="%s" stroke-width=".5"/><circle cx="%s" cy="%s" r="%s" fill="url(#ink-stipple-l)"/>' % (
        f(x), f(y), f(r), INK, f(x), f(y), f(r))


def prickles(pts, s, seed=2):
    from plib import bez_pts, resample
    rnd = random.Random(seed)
    P = resample(bez_pts(pts, per=10), 9 * s)
    d = ''
    for i in range(1, len(P) - 1):
        a, b = P[i - 1], P[i + 1]
        tx, ty = b[0] - a[0], b[1] - a[1]
        Lh = math.hypot(tx, ty) or 1
        sd = 1 if i % 2 else -1
        nx, ny = -ty / Lh * sd, tx / Lh * sd
        x, y = P[i]
        d += 'M%s %sL%s %s' % (f(x), f(y), f(x + nx * 2.4 * s - tx / Lh * 1.4 * s), f(y + ny * 2.4 * s - ty / Lh * 1.4 * s))
    return '<path d="%s" stroke="%s" stroke-width=".6" fill="none"/>' % (d, INK)


def pot(x, y, s):
    """Terracotta pot, rim top centre at (x,y)."""
    w0, w1, h = 46 * s, 34 * s, 40 * s
    body = 'M%s %s L%s %s Q%s %s %s %s L%s %s Z' % (f(x - w0 * .92), f(y + 7 * s), f(x - w1), f(y + h), f(x), f(y + h + 3 * s), f(x + w1), f(y + h), f(x + w0 * .92), f(y + 7 * s))
    o = ['<path d="%s" fill="#c8785a" stroke="%s" stroke-width="1.2"/>' % (body, INK)]
    sh = 'M%s %s L%s %s L%s %s L%s %s Z' % (f(x + w0 * .35), f(y + 7 * s), f(x + w1 * .4), f(y + h), f(x + w1), f(y + h), f(x + w0 * .92), f(y + 7 * s))
    o.append('<path d="%s" fill="url(#ink-hatch)"/>' % sh)
    o.append('<path d="M%s %s L%s %s" stroke="#f3c7a8" stroke-width="%s" stroke-linecap="round" opacity=".7"/>' % (f(x - w0 * .55), f(y + 11 * s), f(x - w1 * .62), f(y + h - 4 * s), f(2.2 * s)))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#d48a68" stroke="%s" stroke-width="1.2"/>' % (f(x - w0), f(y - 2 * s), f(2 * w0), f(10 * s), f(2 * s), INK))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#ink-hatch-l)"/>' % (f(x + w0 * .4), f(y - 2 * s), f(w0 * .6), f(10 * s)))
    o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#5b4330" stroke="%s" stroke-width=".7"/>' % (f(x), f(y - 1.5 * s), f(w0 * .9), f(3 * s), INK))
    o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#ink-stipple-d)"/>' % (f(x), f(y - 1.5 * s), f(w0 * .9), f(3 * s)))
    return ''.join(o)


def plant(x, y, s, closed, seed=7, flowers=True):
    """Potted Mimosa pudica; (x,y) = pot rim centre."""
    def g(P):
        return [(x + u * s, y + v * s) for u, v in P]
    stems = [
        ([(0, 0), (-4, -40), (2, -90), (-5, -140), (-1, -172)], 4.2, 1.4),
        ([(-4, -48), (-28, -74), (-56, -96)], 2.6, 1.0),
        ([(2, -96), (28, -118), (52, -134)], 2.4, 1.0),
        ([(-2, -26), (26, -42), (54, -50)], 2.4, 1.0),
    ]
    # nodes: (point, angle, seed)
    nodes = [((-56, -96), -168), ((-30, -76), -122), ((52, -134), -20), ((30, -120), -72),
             ((54, -50), -8), ((-1, -172), -86), ((-5, -142), -154), ((-2, -26), -150)]
    o = []
    for P, w0, w1 in stems:
        GP = g(P)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".7"/>' % (tapered(GP, w0 * s + .6, w1 * s + .4), STEM, INK))
        o.append(prickles(GP, s))
    # flowers behind leaves partially
    fl = []
    if flowers:
        for (bx, by), (fx, fy), r in [((2, -96), (20, -150), 11), ((-28, -74), (-50, -128), 10), ((26, -42), (64, -84), 10)]:
            A, B = g([(bx, by)])[0], g([(fx, fy)])[0]
            mid = ((A[0] + B[0]) / 2 + 3 * s, (A[1] + B[1]) / 2)
            fl.append('<path d="%s" fill="none" stroke="#7a5b3a" stroke-width="%s"/>' % (cr([A, mid, B]), f(.9 * s + .2)))
            fl.append(pompom(B[0], B[1], r * s, seed=int(fx)))
        bb = g([(-12, -158)])[0]
        fl.append('<path d="%s" fill="none" stroke="#7a5b3a" stroke-width=".7"/>' % cr([g([(-4, -140)])[0], bb]))
        fl.append(bud(bb[0], bb[1], 3.2 * s))
    for i, ((u, v), a) in enumerate(nodes):
        X, Y = g([(u, v)])[0]
        o.append(leaf(X, Y, a, s, closed, seed=seed + i))
    return pot(x, y, s) + ''.join(o) + ''.join(fl)
