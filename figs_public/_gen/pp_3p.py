import sys, math, random
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from ppx import *
from lib import fist, capsule

PID = 'pp-3p'
H = 600
D = []
o = []
add = o.append
BARK = ['#8a5a32', '#9c6a3c', '#7a4e2a', '#a87444', '#b07c48']
GRAIN = '#ecd2a0'
GROUND = '#d9c7a0'

D.append('<radialGradient id="%s-glow" cx=".5" cy=".6" r=".5"><stop offset="0" stop-color="#f7c66a" stop-opacity=".75"/><stop offset=".6" stop-color="#f3b45a" stop-opacity=".25"/><stop offset="1" stop-color="#f3b45a" stop-opacity="0"/></radialGradient>' % PID)
for nm, col in (('ar', '#a8412c'), ('ak', INK), ('ab', '#2c5d9c')):
    D.append('<marker id="%s-%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (PID, nm, col))


def stick(x1, y1, x2, y2, w, col, end=True, rnd=None):
    a = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(a), math.cos(a)
    w2 = w * .75
    d = 'M%s %s L%s %s L%s %s L%s %s Z' % (f(x1 + nx * w / 2), f(y1 + ny * w / 2), f(x2 + nx * w2 / 2), f(y2 + ny * w2 / 2),
                                          f(x2 - nx * w2 / 2), f(y2 - ny * w2 / 2), f(x1 - nx * w / 2), f(y1 - ny * w / 2))
    out = ['<path d="%s" fill="%s" stroke="%s" stroke-width=".7" stroke-linejoin="round"/>' % (d, col, INK)]
    # bark line (shadow side)
    out.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-opacity=".45"/>' % (
        f(x1 - nx * w * .25), f(y1 - ny * w * .25), f(x2 - nx * w2 * .25), f(y2 - ny * w2 * .25), INK, f(max(.4, w * .18))))
    out.append('<path d="M%s %s L%s %s" stroke="#e8c08a" stroke-width="%s" stroke-opacity=".6"/>' % (
        f(x1 + nx * w * .22), f(y1 + ny * w * .22), f(x2 + nx * w2 * .22), f(y2 + ny * w2 * .22), f(max(.3, w * .12))))
    if end:
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" fill="%s" stroke="%s" stroke-width=".6"/>' % (
            f(x2), f(y2), f(w2 * .28), f(w2 / 2), f(math.degrees(a)), f(x2), f(y2), GRAIN, INK))
    return ''.join(out)


def log(x, y, L, r, ang=0, col='#8a5a32', label=None, lsize=11.5, char=False):
    """cylinder lying, centre (x,y), length L, radius r; end-grain on the right end"""
    g = ['<g transform="translate(%s,%s) rotate(%s)">' % (f(x), f(y), f(ang))]
    g.append('<path d="M%s %s H%s A%s %s 0 0 1 %s %s H%s A%s %s 0 0 1 %s %sZ" fill="%s" stroke="%s" stroke-width="1"/>' % (
        f(-L / 2), f(-r), f(L / 2), f(r * .4), f(r), f(L / 2), f(r), f(-L / 2), f(r * .4), f(r), f(-L / 2), f(-r), col, INK))
    # bark texture
    rnd = random.Random(int(x * 7 + y))
    bk = ''
    for i in range(int(L / 7)):
        xx = -L / 2 + 4 + i * 7 + rnd.uniform(-2, 2)
        yy = rnd.uniform(-r * .7, r * .7)
        bk += 'M%s %s h%s' % (f(xx), f(yy), f(rnd.uniform(4, 10)))
    g.append('<path d="%s" stroke="%s" stroke-width=".5" stroke-opacity=".6"/>' % (bk, INK))
    g.append('<path d="M%s %s H%s A%s %s 0 0 1 %s %s H%s Z" fill="url(#ink-hatch)" opacity=".55"/>' % (
        f(-L / 2), f(r * .35), f(L / 2), f(r * .4), f(r), f(L / 2), f(r), f(-L / 2)))
    g.append('<path d="M%s %s H%s" stroke="#e2b98a" stroke-width="%s" stroke-opacity=".7"/>' % (f(-L / 2 + 2), f(-r * .55), f(L / 2 - 2), f(r * .25)))
    if char:
        g.append('<path d="M%s %s H%s A%s %s 0 0 1 %s %s H%s Z" fill="#2b2420" opacity=".75"/>' % (
            f(-L / 2), f(-r), f(L / 2), f(r * .4), f(r), f(L / 2), f(r), f(-L / 2)))
    # end grain
    g.append('<ellipse cx="%s" cy="0" rx="%s" ry="%s" fill="%s" stroke="%s" stroke-width=".9"/>' % (f(L / 2), f(r * .42), f(r), GRAIN, INK))
    for k in (.7, .45, .2):
        g.append('<ellipse cx="%s" cy="0" rx="%s" ry="%s" fill="none" stroke="#a87444" stroke-width=".5"/>' % (f(L / 2), f(r * .42 * k), f(r * k)))
    g.append('</g>')
    if label:
        g.append(T(x - 3, y + lsize * .36, label, 'lb', 'middle', size=lsize, halo=True))
    return ''.join(g)


def flame_shape(cx, by, w, h, n, seed, lean=0):
    rnd = random.Random(seed)
    P = [(cx - w / 2, by)]
    for i in range(n):
        t = (i + .5) / n
        xb = cx - w / 2 + w * t
        hh = h * (0.55 + 0.45 * math.sin(math.pi * t)) * rnd.uniform(.85, 1.05)
        P.append((xb - w / n * .45, by - hh * rnd.uniform(.25, .4)))
        P.append((xb + lean * hh * .25 + rnd.uniform(-3, 3), by - hh))
    P.append((cx + w / 2 - w / n * .1, by - h * .2))
    P.append((cx + w / 2, by))
    P.append((cx, by + w * .12))
    return smooth(P, close=True, t=.6)


def fire(cx, by, w, h, seed=1, lean=0):
    out = ['<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s-glow)"/>' % (f(cx), f(by - h * .4), f(w * 1.2), f(h * .9), PID)]
    out.append('<path d="%s" fill="#c8452a" stroke="%s" stroke-width="1"/>' % (flame_shape(cx, by, w, h, 5, seed, lean), INK))
    out.append('<path d="%s" fill="url(#ink-hatch-r)" opacity=".35"/>' % flame_shape(cx, by, w, h, 5, seed, lean))
    out.append('<path d="%s" fill="#ec8c34" stroke="%s" stroke-width=".6"/>' % (flame_shape(cx, by, w * .72, h * .74, 4, seed + 1, lean), INK))
    out.append('<path d="%s" fill="#f6d36a" stroke="%s" stroke-width=".5"/>' % (flame_shape(cx, by, w * .42, h * .46, 3, seed + 2, lean), INK))
    out.append('<path d="%s" fill="#fff4cc"/>' % flame_shape(cx, by, w * .2, h * .22, 2, seed + 3, lean))
    # engraved tongue lines
    rnd = random.Random(seed + 9)
    ln = ''
    for i in range(7):
        x0 = cx - w * .3 + w * .6 * i / 6
        hh = h * (.35 + .35 * math.sin(math.pi * i / 6))
        ln += 'M%s %s Q%s %s %s %s ' % (f(x0), f(by - 4), f(x0 + rnd.uniform(-6, 6)), f(by - hh * .6), f(x0 + lean * hh * .2 + rnd.uniform(-4, 4)), f(by - hh))
    out.append('<path d="%s" fill="none" stroke="#7a2a18" stroke-width=".55" stroke-opacity=".55"/>' % ln)
    # sparks
    for i in range(6):
        sx = cx + rnd.uniform(-w * .5, w * .5) + lean * 10
        sy = by - h - rnd.uniform(4, h * .35)
        out.append('<ellipse cx="%s" cy="%s" rx="1.1" ry="2" fill="#f2a43c" transform="rotate(%s %s %s)"/>' % (f(sx), f(sy), f(rnd.uniform(-30, 30)), f(sx), f(sy)))
    return '\n'.join(out)


def kindling(cx, by, w, h, n, seed):
    """mound of dry twigs"""
    rnd = random.Random(seed)
    out = []
    # dry grass base
    gr = ''
    for i in range(int(w / 2.2)):
        x = cx - w / 2 + rnd.uniform(0, w)
        gr += 'M%s %s q%s %s %s %s' % (f(x), f(by), f(rnd.uniform(-6, 6)), f(-rnd.uniform(4, 10)), f(rnd.uniform(-8, 8)), f(-rnd.uniform(6, 14)))
    out.append('<path d="%s" fill="none" stroke="#b89a4a" stroke-width=".7"/>' % gr)
    for i in range(n):
        t = rnd.random()
        lev = rnd.random() ** .8
        yc = by - lev * h * (1 - abs(t - .5) * 1.4)
        xc = cx - w / 2 + w * t
        L = rnd.uniform(w * .25, w * .5)
        a = math.radians(rnd.uniform(-35, 35) + (180 if rnd.random() < .5 else 0))
        ww = rnd.uniform(2.6, 5.2)
        out.append(stick(xc - L / 2 * math.cos(a), yc - L / 2 * math.sin(a), xc + L / 2 * math.cos(a), yc + L / 2 * math.sin(a), ww, rnd.choice(BARK)))
    gr2 = ''
    for i in range(int(w / 3)):
        x = cx - w / 2 + rnd.uniform(0, w)
        gr2 += 'M%s %s q%s %s %s %s' % (f(x), f(by + 1), f(rnd.uniform(-5, 5)), f(-rnd.uniform(3, 7)), f(rnd.uniform(-7, 7)), f(-rnd.uniform(4, 9)))
    out.append('<path d="%s" fill="none" stroke="#c9ab55" stroke-width=".6"/>' % gr2)
    return '\n'.join(out)


def ground(x, y, w):
    return ('<path d="M%s %s h%s v14 h-%s z" fill="%s"/>' % (x, y, w, w, GROUND) +
            '<path d="M%s %s h%s v14 h-%s z" fill="url(#ink-stipple-l)"/>' % (x, y, w, w) +
            '<path d="M%s %s h%s" stroke="%s" stroke-width="1"/>' % (x, y, w, INK))


def stones(cx, by, w, seed):
    rnd = random.Random(seed)
    out = []
    for i in range(7):
        x = cx - w / 2 + w * i / 6
        rx = rnd.uniform(7, 10); ry = rnd.uniform(5, 7)
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#b9b2a4" stroke="%s" stroke-width=".8"/>' % (f(x), f(by - ry + 3), f(rx), f(ry), INK))
        out.append('<path d="M%s %s a%s %s 0 0 0 %s 0" fill="url(#ink-hatch)" opacity=".6"/>' % (f(x - rx), f(by - ry + 3), f(rx), f(ry), f(2 * rx)))
    return ''.join(out)


def panel(x, y, w, h, tag, zh, en, col):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="5" fill="#fbf3df" stroke="%s" stroke-width="1"/>'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="none" stroke="#c9b48a" stroke-width=".6"/>' % (x, y, w, h, INK, x + 3, y + 3, w - 6, h - 6) +
            '<circle cx="%s" cy="%s" r="11" fill="%s" stroke="%s" stroke-width=".8"/>' % (x + 20, y + 22, col, INK) +
            '<text x="%s" y="%s" text-anchor="middle" style="font-size:12.5px;font-weight:700;fill:#fff;font-family:Georgia,serif">%s</text>' % (x + 20, y + 26.5, tag) +
            T(x + 37, y + 27, zh, 'lb', size=15.5) + T(x + 37, y + 42, en, 'le', size=11))

def grip(x, y, ang, sc=1.0, sleeve='#cfdcef', slen=70):
    """hand gripping a rod that runs along local x through (0,0); forearm goes to local -y"""
    g = ['<g transform="translate(%s,%s) rotate(%s) scale(%s)">' % (f(x), f(y), f(ang), f(sc))]
    # sleeve / forearm
    g.append('<path d="M-13 -28 L-16 %s L16 %s L13 -28 Z" fill="%s" stroke="%s" stroke-width="1"/>' % (-28 - slen, -28 - slen, sleeve, INK))
    g.append('<path d="M4 -30 L6 %s M-7 -32 L-8 %s" stroke="%s" stroke-width=".5" stroke-opacity=".6"/>' % (-24 - slen, -30 - slen * .7, INK))
    g.append('<path d="M3 -28 L13 -28 L16 %s L8 %s Z" fill="url(#ink-hatch)" opacity=".5"/>' % (-28 - slen, -28 - slen))
    g.append('<path d="M-14 -34 h28 v7 h-28z" fill="#fbf6ea" stroke="%s" stroke-width=".8"/>' % INK)
    # back of hand
    g.append('<path d="M-12 -27 C-15 -20 -17 -13 -16 -7 L16 -7 C17 -13 15 -20 12 -27 Z" fill="url(#ink-vol-flesh)" stroke="%s" stroke-width="1"/>' % INK)
    g.append('<path d="M-6 -24 L-8 -10 M0 -25 L-.5 -10 M6 -24 L7 -10" stroke="%s" stroke-width=".45" stroke-opacity=".45"/>' % INK)
    # thumb (behind the rod on the left, tip coming round the front)
    g.append('<path d="M-15 -16 C-22 -12 -24 -2 -20 6 C-17 11 -11 11 -10 6 C-11 1 -13 -4 -11 -9 Z" fill="#efc9b0" stroke="%s" stroke-width=".9"/>' % INK)
    g.append('<path d="M-19 4 C-17 7 -14 8 -12 6" stroke="%s" stroke-width=".5" fill="none"/>' % INK)
    # four curled fingers over the rod
    for i, xx in enumerate((-11.6, -3.9, 3.9, 11.4)):
        ln = 18 if i in (1, 2) else 16
        g.append('<path d="M%s -9 h7 v%s a3.5 3.5 0 0 1 -7 0 z" fill="url(#ink-vol-flesh)" stroke="%s" stroke-width=".9"/>' % (f(xx - 3.5), ln, INK))
        g.append('<path d="M%s -1 q3.5 1.6 7 0 M%s %s q3.5 1.4 7 0" fill="none" stroke="%s" stroke-width=".5"/>' % (f(xx - 3.5), f(xx - 3.5), f(-9 + ln * .82), INK))
        g.append('<path d="M%s -9.5 q3.5 -2.6 7 0" fill="none" stroke="%s" stroke-width=".7"/>' % (f(xx - 3.5), INK))
    g.append('<path d="M8 -9 h7 v16 a3.5 3.5 0 0 1 -7 0z" fill="url(#ink-hatch-l)" opacity=".8"/>')
    g.append('</g>')
    return ''.join(g)

PY0, PH0 = 8, 352
GY = 292   # ground line
# =================== (a) predisposing ===================
AX, AW = 10, 212
add(panel(AX, PY0, AW, PH0, 'a', '體質：柴堆', 'predisposing — the kindling', '#8a6a3a'))
add(ground(AX + 6, GY, AW - 12))
add('<ellipse cx="%s" cy="%s" rx="26" ry="4" fill="%s" opacity=".18"/>' % (AX + 52, GY + 2, INK))
add('<ellipse cx="%s" cy="%s" rx="50" ry="5" fill="%s" opacity=".18"/>' % (AX + 146, GY + 2, INK))
add(kindling(AX + 52, GY, 52, 26, 12, 3))
add(kindling(AX + 146, GY, 104, 110, 56, 5))
add(T(AX + 52, GY - 44, '柴少', 'lb', 'middle', size=14))
add('<path d="M%s %s v10" class="ld" marker-end="url(#ink-dot)"/>' % (AX + 52, GY - 38))
add(T(AX + 146, GY - 128, '柴多', 'lb', 'middle', size=14))
add('<path d="M%s %s v10" class="ld" marker-end="url(#ink-dot)"/>' % (AX + 146, GY - 122))
add(T(AX + 16, GY - 176, '每個人天生的', 'ls', size=12.5))
add(T(AX + 16, GY - 159, '「柴」不一樣多', 'ls', size=12.5))
add(T(AX + 14, GY + 34, '容易緊張、愛擔心、', 'ls', size=11.5))
add(T(AX + 14, GY + 50, '家族有人失眠、年紀漸長', 'ls', size=11.5))

# =================== (b) precipitating ===================
BX0, BW = 230, 222
add(panel(BX0, PY0, BW, PH0, 'b', '誘發：火柴', 'precipitating — the match', '#c8452a'))
add(ground(BX0 + 6, GY, BW - 12))
pcx = BX0 + 170
add('<ellipse cx="%s" cy="%s" rx="44" ry="5" fill="%s" opacity=".18"/>' % (pcx, GY + 2, INK))
add(kindling(pcx, GY, 84, 64, 30, 8))
add(fire(pcx - 4, GY - 22, 30, 34, seed=4))
# falling lit match
mx, my, ma = pcx - 6, 118, 62
add('<g transform="translate(%s,%s) rotate(%s)">' % (mx, my, ma) +
    '<rect x="-30" y="-2.4" width="40" height="4.8" rx="1" fill="#e9cf98" stroke="%s" stroke-width=".7"/>' % INK +
    '<path d="M-30 1 h40" stroke="%s" stroke-width=".4" stroke-opacity=".5"/>' % INK +
    '<ellipse cx="13" cy="0" rx="5.5" ry="4.2" fill="#a8412c" stroke="%s" stroke-width=".8"/></g>' % INK)
add(fire(mx + 14 * math.cos(math.radians(ma)) + 2, my + 14 * math.sin(math.radians(ma)) - 2, 11, 22, seed=11, lean=-.6))
for k in range(3):
    add('<path d="M%s %s l-10 -18" stroke="%s" stroke-width=".8" stroke-opacity=".6"/>' % (mx - 14 + k * 8, my - 24 + k * 3, INK))
add('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="%s" stroke-width=".9" stroke-dasharray="3 3" marker-end="url(#%s-ak)"/>' % (mx + 14, my + 40, mx + 18, my + 70, pcx + 4, GY - 64, INK, PID))
# matchbox in front-left
MBX, MBY, MBW, MBH = BX0 + 10, GY - 42, 150, 52
add('<path d="M%s %s l14 -12 h%s l-14 12z" fill="#e7d3a6" stroke="%s" stroke-width=".9"/>' % (MBX, MBY, MBW, INK))
add('<path d="M%s %s l14 -12 v%s l-14 12z" fill="#7b2f22" stroke="%s" stroke-width=".9"/>' % (MBX + MBW, MBY, MBH, INK))
add('<path d="M%s %s l14 -12 v%s l-14 12z" fill="url(#ink-hatch-d)" opacity=".5"/>' % (MBX + MBW, MBY, MBH))
add('<rect x="%s" y="%s" width="%s" height="%s" fill="#a8412c" stroke="%s" stroke-width="1"/>' % (MBX, MBY, MBW, MBH, INK))
add('<rect x="%s" y="%s" width="%s" height="%s" fill="#fbf3df" stroke="%s" stroke-width=".6"/>' % (MBX + 4, MBY + 4, MBW - 8, MBH - 8, INK))
cells = [(MBX + 4 + (MBW - 8) * (i + .5) / 3) for i in range(3)]
# icon 1: briefcase (life stress)
c = cells[0]; iy = MBY + 17
add('<rect x="%s" y="%s" width="16" height="11" rx="1.5" fill="#8a5a32" stroke="%s" stroke-width=".7"/><path d="M%s %s v-3 h6 v3" fill="none" stroke="%s" stroke-width=".8"/><path d="M%s %s h16" stroke="%s" stroke-width=".5"/>' % (
    f(c - 8), f(iy - 6), INK, f(c - 3), f(iy - 6), INK, f(c - 8), f(iy - 1), INK))
add('<path d="M%s %s l2 -3 M%s %s l-2 -3" stroke="%s" stroke-width=".7"/>' % (f(c + 9), f(iy - 7), f(c - 9), f(iy - 7), TCM))
# icon 2: thermometer (illness)
c = cells[1]
add('<rect x="%s" y="%s" width="4" height="12" rx="2" fill="#fff" stroke="%s" stroke-width=".7"/><circle cx="%s" cy="%s" r="3.2" fill="%s" stroke="%s" stroke-width=".7"/><rect x="%s" y="%s" width="1.6" height="8" fill="%s"/>' % (
    f(c - 2), f(iy - 10), INK, f(c), f(iy + 4), RED, INK, f(c - .8), f(iy - 5), RED))
# icon 3: airplane (jet lag)
c = cells[2]
add('<path d="M%s %s l14 -4 q3 -1 3 1 q0 2 -3 2.5 l-14 2 z M%s %s l5 -1 l-4 7 h-2 z M%s %s l3 -.5 l-3 -4 h-2 z" fill="#cfdcef" stroke="%s" stroke-width=".7"/>' % (
    f(c - 9), f(iy + 1), f(c - 1), f(iy - 1), f(c - 6), f(iy - 1), INK))
for c, t in zip(cells, ('生活壓力', '生病', '時差')):
    add(T(c, MBY + 40, t, 'lb', 'middle', size=11.5, halo=False))
add('<path d="M%s %s h%s" stroke="#3a2a1c" stroke-width="3" stroke-opacity=".7"/>' % (MBX + MBW + 2, MBY + MBH - 6, 10))
add(T(BX0 + 14, GY + 34, '一件事點燃了失眠：', 'ls', size=11.5))
add(T(BX0 + 14, GY + 50, '考試、失業、生病、搭機⋯', 'ls', size=11.5))

# =================== (c) perpetuating ===================
CX0, CW = 460, 290
add(panel(CX0, PY0, CW, PH0, 'c', '維持：一直搧風的手', 'perpetuating — the fanning hand', '#7b2f22'))
add(ground(CX0 + 6, GY, CW - 12))
FX = CX0 + 112
add(stones(FX, GY, 112, 2))
add('<ellipse cx="%s" cy="%s" rx="56" ry="6" fill="%s" opacity=".2"/>' % (FX, GY + 2, INK))
# burning logs (crossed) + charred
add(log(FX - 18, GY - 12, 64, 7, -14, '#6e4426', char=True))
add(log(FX + 18, GY - 12, 64, 7, 194, '#6e4426', char=True))
add(kindling(FX, GY - 6, 70, 24, 14, 12))
add(fire(FX, GY - 10, 78, 142, seed=21, lean=.25))
# smoke
add('<path d="M%s %s c-10 -14 10 -22 0 -36 c-8 -12 8 -18 2 -30 M%s %s c8 -12 -6 -22 4 -34" fill="none" stroke="#8a8478" stroke-width="1.1" stroke-opacity=".55"/>' % (FX + 14, GY - 162, FX - 6, GY - 160))
# burnt-out match on the ground
add('<g transform="translate(%s,%s) rotate(-8)"><rect x="-16" y="-1.6" width="28" height="3.2" fill="#3b302a" stroke="%s" stroke-width=".5"/><ellipse cx="12" cy="0" rx="3.4" ry="2.6" fill="#1c1714"/></g>' % (CX0 + 38, GY - 3, INK))
add(T(CX0 + 20, GY + 32, '火柴早就熄了', 'ls', size=11.5))
add('<path d="M%s %s L%s %s" class="ld" marker-end="url(#ink-dot)"/>' % (CX0 + 40, GY + 21, CX0 + 40, GY - 2))
# fanning hand from left, holding a round fan (團扇)
fx0, fy0 = CX0 + 8, 168
# fan: handle + round leaf
hx0, hy0 = fx0 + 34, fy0 - 2
hx1, hy1 = fx0 + 46, fy0 - 26
add('<path d="M%s %s L%s %s" stroke="%s" stroke-width="3.6" stroke-linecap="round"/><path d="M%s %s L%s %s" stroke="#b98049" stroke-width="2.2" stroke-linecap="round"/>' % (fx0 + 26, fy0 + 14, hx1, hy1, INK, fx0 + 26, fy0 + 14, hx1, hy1))
fcx, fcy = fx0 + 56, fy0 - 52
add('<ellipse cx="%s" cy="%s" rx="22" ry="28" transform="rotate(26 %s %s)" fill="#efe2c2" stroke="%s" stroke-width="1.1"/>' % (fcx, fcy, fcx, fcy, INK))
rib = ''
for k in range(-4, 5):
    a = math.radians(26 + 90 + k * 13)
    rib += 'M%s %s L%s %s' % (f(hx1), f(hy1), f(fcx + 26 * math.cos(math.radians(26 - 90 + k * 14)) * .8), f(fcy + 26 * math.sin(math.radians(26 - 90 + k * 14)) * 1.0))
add('<path d="%s" stroke="#b08a50" stroke-width=".5"/>' % rib)
add('<ellipse cx="%s" cy="%s" rx="22" ry="28" transform="rotate(26 %s %s)" fill="url(#ink-hatch-l)" opacity=".6"/>' % (fcx, fcy, fcx, fcy))
add('<ellipse cx="%s" cy="%s" rx="22" ry="28" transform="rotate(26 %s %s)" fill="none" stroke="%s" stroke-width="1.1"/>' % (fcx, fcy, fcx, fcy, INK))
_ha = math.degrees(math.atan2(hy1 - (fy0 + 14), hx1 - (fx0 + 26)))
add(grip(fx0 + 30, fy0 + 6, _ha + 180, .95, sleeve='#cfdcef', slen=40))
# motion arcs of the fan + wind lines
add('<path d="M%s %s a40 40 0 0 1 22 -30 M%s %s a46 46 0 0 1 26 -32" fill="none" stroke="%s" stroke-width=".8" stroke-dasharray="3 2"/>' % (fcx - 14, fcy + 40, fcx - 6, fcy + 46, INK))
for k in range(3):
    y = fcy + 30 + k * 16
    add('<path d="M%s %s q12 -6 24 0 t24 2" fill="none" stroke="%s" stroke-width="1.1" marker-end="url(#%s-ab)"/>' % (fcx + 8, y, WEST, PID))
# woodpile (labelled habits) on the right
WX = CX0 + 228
habits = ['太早上床', '躺床滑手機', '白天補眠', '怕睡不著']
for i, hb in enumerate(habits):
    add(log(WX, GY - 11 - i * 21, 104, 10, 0, BARK[i % 4], label=hb, lsize=12))
# a hand adding a log (top right) labelled 喝酒助眠
lx, ly = CX0 + 196, 84
add(log(lx, ly, 96, 10, 22, '#9c6a3c', label=None))
add(T(lx - 2, ly + 4, '喝酒助眠', 'lb', 'middle', size=12, extra=' transform="rotate(22 %s %s)"' % (lx, ly)))
add(grip(lx + 26 * math.cos(math.radians(22)), ly + 26 * math.sin(math.radians(22)), 22, .95, sleeve="#e7d3a6", slen=50))
add('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="%s" stroke-width="1.2" marker-end="url(#%s-ar)"/>' % (lx - 30, ly + 34, lx - 50, ly + 54, FX + 34, GY - 128, TCM, PID))
add(T(CX0 + 150, GY + 32, '這些習慣＝添柴、搧風', 'ls', size=11.5))
add(T(CX0 + 150, GY + 48, '→ 火一直燒下去', 'lb', size=12, color=TCM))

# =================== Spielman bars ===================
SY0, SY1 = 392, 512
add(T(14, 382, '三種因素隨時間的變化', 'lb', size=14))
add(T(170, 382, '(Spielman 3P model)', 'le', size=11))
cols = [('還沒失眠', [('p', 34)]), ('剛開始失眠', [('p', 34), ('t', 56)]), ('幾週後', [('p', 34), ('t', 24), ('m', 30)]), ('慢性失眠', [('p', 34), ('m', 48)])]
CF = {'p': ('#c9a77f', 'url(#ink-stipple-l)'), 't': ('#ec8c34', 'url(#ink-hatch-l)'), 'm': ('#a8412c', 'url(#ink-hatch-r)')}
thr = SY1 - 64
for i, (nm, segs) in enumerate(cols):
    x = 60 + i * 96
    y = SY1
    for k, hgt in segs:
        add('<rect x="%s" y="%s" width="44" height="%s" fill="%s" stroke="%s" stroke-width=".8"/>' % (x, y - hgt, hgt, CF[k][0], INK))
        add('<rect x="%s" y="%s" width="44" height="%s" fill="%s" opacity=".6"/>' % (x, y - hgt, hgt, CF[k][1]))
        y -= hgt
    add(T(x + 22, SY1 + 16, nm, 'ls', 'middle', size=11.5))
add('<path d="M40 %s H440" stroke="%s" stroke-width="1.2" stroke-dasharray="6 4"/>' % (thr, TCM))
add(T(44, thr - 6, '失眠門檻', 'lb', size=12, color=TCM))
add('<path d="M40 %s H440" stroke="%s" stroke-width="1"/>' % (SY1, INK))
for k, (zh, (c1, _)) in enumerate((('體質（柴）', CF['p']), ('誘發（火柴）', CF['t']), ('維持（搧風的手）', CF['m']))):
    y = 404 + k * 22
    add('<rect x="460" y="%s" width="16" height="12" fill="%s" stroke="%s" stroke-width=".7"/>' % (y - 10, c1, INK))
    add(T(482, y, zh, 'ls', size=12))
add('<rect x="600" y="390" width="150" height="100" rx="4" fill="#e3ecd7" stroke="%s" stroke-width=".8"/>' % INK)
add(T(610, 410, '所以治療重點：', 'lb', size=12.5, color='#3f6a2a'))
add(T(610, 428, '讓那隻手停下來，', 'ls', size=12))
add(T(610, 445, '把多出來的柴拿走', 'ls', size=12))
add(T(610, 466, '（失眠認知行為治療', 'ls', size=11))
add(T(610, 478, ' CBT-I 的目標）', 'le', size=11))

# =================== message band ===================
add('<rect x="10" y="%s" width="740" height="40" rx="5" fill="#f6dcd4" stroke="%s" stroke-width=".8"/>' % (H - 52, INK))
add('<rect x="13" y="%s" width="734" height="34" rx="4" fill="none" stroke="#a8412c" stroke-width=".6"/>' % (H - 49))
add(T(380, H - 26, '讓你開始失眠的原因，常常不是讓你一直失眠的原因', 'lb', 'middle', size=17, halo=False))

body = '\n'.join(o)
write(PID, '圖 4·A', '失眠像一場火：柴、火柴、和一直搧風的手', 'Insomnia as a fire: kindling, a match, and a fanning hand', H, body,
      '三格營火比喻失眠的 3P 模式：體質如柴堆、誘發事件如火柴、維持因子如一直搧風添柴的手；下方為三種因素隨時間變化的長條圖。',
      '<b>圖 4·A　失眠像一場火。</b>(a) 每個人天生的「柴」多寡不同；(b) 一根火柴（壓力、生病、時差）把火點著；(c) 火柴早就熄了，但太早上床、躺床滑手機、白天補眠、怕睡不著、喝酒助眠這些做法，像一隻手不停搧風添柴，讓火繼續燒。下方長條圖顯示：到了慢性期，誘發事件已經消失，撐住失眠的主要是維持因子，這正是失眠認知行為治療下手的地方。依 Spielman 3P 模式重繪的示意圖。',
      '\n'.join(D))
