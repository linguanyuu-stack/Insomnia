import math, random

def f(v):
    s = ('%.1f' % v)
    return s[:-2] if s.endswith('.0') else s

def pts(points, close=False):
    d = 'M' + ' L'.join(f(x) + ' ' + f(y) for x, y in points)
    return d + ('Z' if close else '')

def smooth(points, close=False, t=0.5):
    """Catmull-Rom -> cubic bezier path through points."""
    P = list(points)
    n = len(P)
    if n < 3:
        return pts(P, close)
    if close:
        P2 = [P[-1]] + P + [P[0], P[1]]
    else:
        P2 = [P[0]] + P + [P[-1]]
    d = 'M%s %s' % (f(P[0][0]), f(P[0][1]))
    rng = n if close else n - 1
    for i in range(rng):
        p0, p1, p2, p3 = P2[i], P2[i + 1], P2[i + 2], P2[i + 3]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += ' C%s %s %s %s %s %s' % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return d + ('Z' if close else '')

def rot(u, v, x, y, ang):
    a = math.radians(ang)
    return (x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a))

def leaf(x, y, ang, L, W, p=0.6, q=1.0, bend=0.0, fill='#c9d6a3', veins=7,
         vein_ang=50, marginal=True, hatch='url(#ink-hatch-l)', serrate=0, tipcurl=0.0,
         midrib_w=0.9, cls='ink', extra_shade=True, seed=1, base_round=0.0):
    """Generic simple leaf. (x,y) = base, ang = direction degrees (0 = +x, 90 = down)."""
    N = 40
    ts = [i / N for i in range(N + 1)]
    def wf(t):
        val = (t ** p) * ((1 - t) ** q)
        return val
    mx = max(wf(t) for t in ts)
    def mid(t):
        return (t * L, bend * L * math.sin(math.pi * t) + tipcurl * L * t ** 3)
    def side(t, s):
        u, v = mid(t)
        w = W / 2 * wf(t) / mx
        if base_round and t < 0.15:
            w = max(w, W / 2 * base_round * math.sin(t / 0.15 * math.pi / 2))
        if serrate and 0.08 < t < 0.97:
            k = int(t * serrate * 2)
            w *= 1 + (0.06 if k % 2 == 0 else -0.02)
        return (u, v + s * w)
    up = [side(t, -1) for t in ts]
    dn = [side(t, 1) for t in reversed(ts)]
    g = lambda P: [rot(u, v, x, y, ang) for (u, v) in P]
    outline = smooth(g(up) + g(dn)[1:], close=True)
    half_dn = smooth(g([mid(t) for t in ts]) + g(dn)[1:], close=True)
    out = []
    out.append('<path d="%s" fill="%s" fill-opacity=".85"/>' % (outline, fill))
    if extra_shade and hatch:
        out.append('<path d="%s" fill="%s"/>' % (half_dn, hatch))
    # midrib
    out.append('<path d="%s" class="ink2" stroke-width="%s"/>' % (smooth(g([mid(t) for t in ts[:-1]])), midrib_w))
    # lateral veins
    for i in range(veins):
        t0 = 0.08 + 0.82 * i / max(veins - 1, 1)
        for s in (-1, 1):
            u0, v0 = mid(t0)
            w = W / 2 * wf(min(t0 + 0.08, 0.99)) / mx
            va = math.radians(vein_ang)
            l1 = w * 0.85
            P = [(u0, v0)]
            for k in range(1, 6):
                kk = k / 5
                du = l1 * kk / math.tan(va) * 0.9 + l1 * 0.6 * kk ** 2
                P.append((u0 + du, v0 + s * l1 * (kk - 0.15 * kk ** 2)))
            out.append('<path d="%s" class="ink2" stroke-width=".45"/>' % smooth(g(P)))
    if marginal:
        for s in (-1, 1):
            P = [side(t, s * 0.86) for t in ts[3:-3]]
            P = [(u, mid(t)[1] + (v - mid(t)[1]) * 0.86) for (u, v), t in zip([side(t, s) for t in ts[3:-3]], ts[3:-3])]
            out.append('<path d="%s" class="ink2" stroke-width=".35" stroke-opacity=".8"/>' % smooth(g(P)))
    out.append('<path d="%s" class="%s"/>' % (outline, cls))
    return '\n'.join(out)

def stipple_ellipse(cx, cy, rx, ry, n, r=0.5, seed=1, bias=None, color='#2a2018', op=0.8):
    rnd = random.Random(seed)
    out = []
    i = 0
    while len(out) < n and i < n * 20:
        i += 1
        a = rnd.random() * 2 * math.pi
        rr = math.sqrt(rnd.random())
        x = cx + rr * rx * math.cos(a); y = cy + rr * ry * math.sin(a)
        if bias:  # bias=(dx,dy) direction where dots concentrate
            dot = (math.cos(a) * bias[0] + math.sin(a) * bias[1]) * rr
            if rnd.random() > 0.25 + 0.75 * max(0, dot):
                continue
        out.append('<circle cx="%s" cy="%s" r="%s"/>' % (f(x), f(y), f(r * (0.7 + 0.6 * rnd.random()))))
    return '<g fill="%s" fill-opacity="%s">%s</g>' % (color, op, ''.join(out))

def label(x, y, zh, en=None, anchor='start', two_line=False, cls='lb halo', ecls='le'):
    a = '' if anchor == 'start' else ' text-anchor="%s"' % anchor
    if en and two_line:
        return ('<text x="%s" y="%s" class="%s"%s>%s</text>' % (f(x), f(y), cls, a, zh) +
                '<text x="%s" y="%s" class="%s halo"%s>%s</text>' % (f(x), f(y + 14), ecls, a, en))
    if en:
        return '<text x="%s" y="%s" class="%s"%s>%s <tspan class="%s">%s</tspan></text>' % (f(x), f(y), cls, a, zh, ecls, en)
    return '<text x="%s" y="%s" class="%s"%s>%s</text>' % (f(x), f(y), cls, a, zh)

def leader(*P, dot_end=True):
    if P and not isinstance(P[0], (tuple, list)):
        P = [(P[i], P[i + 1]) for i in range(0, len(P), 2)]
    d = pts(P)
    m = ' marker-end="url(#ink-dot)"' if dot_end else ''
    return '<path d="%s" class="ld"%s/>' % (d, m)

import re
def fixfill(body):
    # class .ink* sets fill:none in CSS, which beats a fill="" attribute; move fill into style
    def rep(m):
        tag = m.group(0)
        if re.search(r'class="ink[23]?"', tag) and ' fill="' in tag and 'style=' not in tag:
            tag = re.sub(r' fill="([^"]*)"', r' style="fill:\1"', tag, count=1)
        return tag
    return re.sub(r'<(path|ellipse|circle|rect|polygon)\b[^>]*>', rep, body)

def figure(pid, pn, zh, en, H, aria, body, caption):
    body = fixfill(body)
    return ('<figure class="plate" id="%s">\n  <div class="pt"><span class="pn">%s</span><span class="ptt">%s</span><span class="pte">%s</span></div>\n'
            '  <svg viewBox="0 0 760 %d" role="img" aria-label="%s">\n%s\n  </svg>\n  <figcaption>%s</figcaption>\n</figure>\n') % (pid, pn, zh, en, H, aria, body, caption)

def scalebar(x, y, px_per_cm, cm=2, label_txt=None):
    w = px_per_cm * cm
    out = ['<g>']
    for i in range(cm):
        out.append('<rect x="%s" y="%s" width="%s" height="4" fill="%s" stroke="#2a2018" stroke-width=".6"/>' % (
            f(x + i * px_per_cm), f(y), f(px_per_cm), '#2a2018' if i % 2 == 0 else '#fbf6ea'))
    out.append('<text x="%s" y="%s" class="ls">%s</text>' % (f(x + w + 6), f(y + 5), label_txt or '%d cm' % cm))
    out.append('</g>')
    return ''.join(out)

def num(x, y, n, r=7):
    return ('<circle cx="%s" cy="%s" r="%s" fill="#fbf6ea" stroke="#2a2018" stroke-width=".7"/>'
            '<text x="%s" y="%s" text-anchor="middle" style="font-size:10px;font-weight:700">%s</text>') % (f(x), f(y), r, f(x), f(y + 3.5), n)
