"""pp-nobel  圖 1·C  Fruit fly, period mutants, PER/TIM loop, 2017 Nobel Prize."""
import sys, math, random
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from clk_lib import write, T, lead, f, cr, poly, rot, sun, moon, L, INK, tapered, num

PID = 'pp-nobel'
H = 682
o, defs = [], []

defs.append('<pattern id="%s-hex" width="3.2" height="2.8" patternUnits="userSpaceOnUse"><circle cx=".8" cy=".7" r=".75" fill="#7a1c14" fill-opacity=".55"/><circle cx="2.4" cy="2.1" r=".75" fill="#7a1c14" fill-opacity=".55"/></pattern>' % PID)
defs.append('<radialGradient id="%s-eye" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#ef6a55"/><stop offset=".6" stop-color="#c0392b"/><stop offset="1" stop-color="#7a1c14"/></radialGradient>' % PID)
defs.append('<radialGradient id="%s-gold" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#fff2b8"/><stop offset=".45" stop-color="#e2b54a"/><stop offset="1" stop-color="#9a6b14"/></radialGradient>' % PID)
defs.append('<radialGradient id="%s-tan" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#e6bd84"/><stop offset="1" stop-color="#a87238"/></radialGradient>' % PID)


def panel_title(x, y, s, anchor='start'):
    return T(x, y, s, 'lt', anchor, halo=False)


def pframe(x, y, w, h):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="4" class="panel"/>' % (x, y, w, h)


# =============================================================== (a) the fly
o.append(pframe(10, 30, 368, 278))
o.append(panel_title(22, 52, '(a) 果蠅 <tspan class="le" style="font-size:13px">Drosophila melanogaster</tspan>'))
FX, FY, FS = 196, 160, 1.0
G = lambda u, v: (FX + u * FS, FY + v * FS)


def wing(side):
    """wing in local coords (base 0,0 -> tip 150,0), anterior = -y"""
    outline = [(0, -4), (30, -13), (80, -21), (124, -22), (147, -12), (153, 0), (148, 10), (126, 22), (86, 30), (46, 27), (20, 17), (6, 8), (0, 4)]
    g = ['<path d="%s" fill="#eef4f7" fill-opacity=".72" stroke="%s" stroke-width=".9"/>' % (cr(outline, True), INK)]
    # faint iridescent tint
    g.append('<path d="%s" fill="url(#ink-hatch-l)" opacity=".35"/>' % cr(outline, True))
    veins = [([(4, -6), (40, -15), (88, -21), (124, -22), (147, -12), (153, 0)], 1.1),   # costa
             ([(4, -5), (30, -12), (58, -18)], .8),                                    # L1
             ([(16, -6), (60, -12), (100, -17), (126, -21)], .75),                     # L2
             ([(8, -2), (60, -3), (110, -3), (152, -2)], .75),                         # L3
             ([(8, 2), (60, 4), (110, 7), (146, 9)], .75),                             # L4
             ([(6, 6), (50, 13), (90, 20), (116, 25)], .75),                           # L5
             ([(4, 8), (20, 14), (38, 20)], .6)]                                       # L6
    for P, w in veins:
        g.append('<path d="%s" fill="none" stroke="#5a4630" stroke-width="%s"/>' % (cr(P), w))
    g.append('<path d="M56 -3 L56 4 M92 6.5 L91 20" stroke="#5a4630" stroke-width=".8"/>')
    # marginal fringe
    fr = ''
    for t in range(14):
        x = 128 + t * 2.2
        fr += 'M%s %sl1 1.6' % (f(x), f(14 - t * 1.0 if t < 12 else 2))
    g.append('<path d="%s" stroke="%s" stroke-width=".35" fill="none"/>' % (fr, INK))
    if side < 0:
        return '<g transform="translate(%s %s) rotate(118) scale(%s %s)">%s</g>' % (f(G(-24, -12)[0]), f(G(-24, -12)[1]), FS, -FS, ''.join(g))
    return '<g transform="translate(%s %s) rotate(62) scale(%s)">%s</g>' % (f(G(24, -12)[0]), f(G(24, -12)[1]), FS, ''.join(g))


def leg(P, w0=4.2):
    """P: [coxa, knee, ankle, tip] in local; tarsus segmented"""
    g = []
    Pg = [G(*p) for p in P]
    g.append('<path d="%s" fill="#b98448" stroke="%s" stroke-width=".8"/>' % (tapered([Pg[0], Pg[1]], w0, w0 * .8), INK))
    g.append('<path d="%s" fill="#c49058" stroke="%s" stroke-width=".8"/>' % (tapered([Pg[1], Pg[2]], w0 * .7, w0 * .55), INK))
    # tarsus 5 segments
    ax, ay = Pg[2]; tx, ty = Pg[3]
    d = ''
    for k in range(5):
        x0 = ax + (tx - ax) * k / 5; y0 = ay + (ty - ay) * k / 5
        x1 = ax + (tx - ax) * (k + .9) / 5; y1 = ay + (ty - ay) * (k + .9) / 5
        d += 'M%s %sL%s %s' % (f(x0), f(y0), f(x1), f(y1))
    g.append('<path d="%s" stroke="#8a5a2a" stroke-width="1.8" stroke-linecap="round" fill="none"/>' % d)
    # claws
    ang = math.atan2(ty - ay, tx - ax)
    for s_ in (-1, 1):
        a2 = ang + s_ * .6
        g.append('<path d="M%s %s l%s %s" stroke="%s" stroke-width=".6"/>' % (f(tx), f(ty), f(math.cos(a2) * 3), f(math.sin(a2) * 3), INK))
    # tiny leg bristles
    bd = ''
    for seg in ((Pg[0], Pg[1]), (Pg[1], Pg[2])):
        (x0, y0), (x1, y1) = seg
        for k in range(1, 5):
            x = x0 + (x1 - x0) * k / 5; y = y0 + (y1 - y0) * k / 5
            a = math.atan2(y1 - y0, x1 - x0) + .5
            bd += 'M%s %sl%s %s' % (f(x), f(y), f(math.cos(a) * 3), f(math.sin(a) * 3))
    g.append('<path d="%s" stroke="%s" stroke-width=".4" fill="none"/>' % (bd, INK))
    return ''.join(g)


def bristle(u, v, ang, ln, w=1.1):
    x, y = G(u, v)
    a = math.radians(ang)
    ex, ey = x + math.cos(a) * ln, y + math.sin(a) * ln
    mx, my = (x + ex) / 2 + math.cos(a + 1.57) * ln * .06, (y + ey) / 2 + math.sin(a + 1.57) * ln * .06
    return '<path d="%s" fill="#1d140e"/>' % tapered([(x, y), (mx, my), (ex, ey)], w, .15)


fly = ['<g>']
for sgn in (-1, 1):
    fly.append(leg([(sgn * 16, -28), (sgn * 40, -42), (sgn * 50, -74), (sgn * 58, -96)]))
    fly.append(leg([(sgn * 24, -6), (sgn * 60, -16), (sgn * 86, 8), (sgn * 104, 24)]))
    fly.append(leg([(sgn * 20, 12), (sgn * 52, 34), (sgn * 64, 74), (sgn * 74, 102)]))
# abdomen
abd = (0, 72, 27, 47)
ax_, ay_ = G(abd[0], abd[1])
fly.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s-tan)" stroke="%s" stroke-width="1.4"/>' % (f(ax_), f(ay_), f(abd[2] * FS), f(abd[3] * FS), PID, INK))
defs.append('<clipPath id="%s-abd"><ellipse cx="%s" cy="%s" rx="%s" ry="%s"/></clipPath>' % (PID, f(ax_), f(ay_), f(abd[2] * FS), f(abd[3] * FS)))
bands = ['<g clip-path="url(#%s-abd)">' % PID]
for k, (yt, hh) in enumerate([(40, 6), (54, 7), (68, 8), (82, 9), (96, 10), (108, 14)]):
    x0, y0 = G(-30, yt)
    bands.append('<path d="M%s %s q%s %s %s 0 v%s q-%s %s -%s 0Z" fill="#4a3020" fill-opacity=".9"/>' % (
        f(x0), f(y0), f(30 * FS), f(5 * FS), f(60 * FS), f(hh * FS), f(30 * FS), f(5 * FS), f(60 * FS)))
    bands.append('<path d="M%s %s q%s %s %s 0" fill="none" stroke="%s" stroke-width=".6"/>' % (f(x0), f(y0 - 6 * FS), f(30 * FS), f(5 * FS), f(60 * FS), INK))
bands.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#ink-hatch)" transform="translate(%s 0)" opacity=".7"/>' % (f(ax_), f(ay_), f(abd[2] * FS), f(abd[3] * FS), f(13 * FS)))
bands.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#ink-stipple-l)"/>' % (f(ax_), f(ay_), f(abd[2] * FS), f(abd[3] * FS)))
bands.append('</g>')
fly.extend(bands)
fly.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="1.4"/>' % (f(ax_), f(ay_), f(abd[2] * FS), f(abd[3] * FS), INK))
# thorax
tx_, ty_ = G(0, -8)
fly.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s-tan)" stroke="%s" stroke-width="1.5"/>' % (f(tx_), f(ty_), f(29 * FS), f(34 * FS), PID, INK))
fly.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#ink-stipple)" opacity=".7"/>' % (f(tx_), f(ty_), f(29 * FS), f(34 * FS)))
fly.append('<path d="M%s %s A%s %s 0 0 1 %s %s" fill="url(#ink-hatch)" opacity=".8"/>' % (f(G(18, -32)[0]), f(G(18, -32)[1]), f(29 * FS), f(34 * FS), f(G(18, 18)[0]), f(G(18, 18)[1])))
# faint stripes (acrostichal rows)
for u in (-9, -3, 3, 9):
    fly.append('<path d="M%s %s Q%s %s %s %s" stroke="#7a4f22" stroke-width=".5" stroke-dasharray="1 2" fill="none"/>' % (
        f(G(u * .8, -36)[0]), f(G(u, -36)[1]), f(G(u * 1.1, -10)[0]), f(G(u, -10)[1]), f(G(u * .9, 18)[0]), f(G(u, 18)[1])))
# scutellum
sx_, sy_ = G(0, 25)
fly.append('<path d="M%s %s Q%s %s %s %s Z" fill="#c4904f" stroke="%s" stroke-width="1.1"/>' % (f(G(-15, 20)[0]), f(G(-15, 20)[1]), f(sx_), f(G(0, 40)[1]), f(G(15, 20)[0]), f(G(15, 20)[1]), INK))
# halteres
for sgn in (-1, 1):
    hx_, hy_ = G(sgn * 24, 18)
    fly.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="1"/><circle cx="%s" cy="%s" r="3" fill="#e6d3a8" stroke="%s" stroke-width=".8"/>' % (
        f(G(sgn * 18, 14)[0]), f(G(sgn * 18, 14)[1]), f(hx_), f(hy_), INK, f(hx_), f(hy_), INK))
# wings
fly.append(wing(-1))
fly.append(wing(1))
# head
hx_, hy_ = G(0, -50)
fly.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#b98448" stroke="%s" stroke-width="1.4"/>' % (f(hx_), f(hy_), f(28 * FS), f(16 * FS), INK))
for sgn in (-1, 1):
    ex_, ey_ = G(sgn * 18, -51)
    fly.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s-eye)" stroke="%s" stroke-width="1.2" transform="rotate(%s %s %s)"/>' % (
        f(ex_), f(ey_), f(13 * FS), f(16.5 * FS), PID, INK, sgn * 18, f(ex_), f(ey_)))
    fly.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s-hex)" transform="rotate(%s %s %s)"/>' % (
        f(ex_), f(ey_), f(13 * FS), f(16.5 * FS), PID, sgn * 18, f(ex_), f(ey_)))
    fly.append('<ellipse cx="%s" cy="%s" rx="3.4" ry="2" fill="#fff" fill-opacity=".7" transform="rotate(-30 %s %s)"/>' % (f(ex_ - 4), f(ey_ - 7), f(ex_ - 4), f(ey_ - 7)))
    # antenna (aristate)
    a0 = G(sgn * 5, -64)
    a1 = G(sgn * 8, -72)
    fly.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (f(a0[0]), f(a0[1]), f(a1[0]), f(a1[1]), '#8a5a2a'))
    fly.append('<ellipse cx="%s" cy="%s" rx="3" ry="4.2" fill="#a46c34" stroke="%s" stroke-width=".7"/>' % (f(a1[0]), f(a1[1] - 2), INK))
    ar = [G(sgn * 9, -76), G(sgn * 16, -88), G(sgn * 26, -94)]
    fly.append('<path d="%s" fill="none" stroke="%s" stroke-width=".7"/>' % (cr(ar), INK))
    br = ''
    for k in range(1, 7):
        t = k / 7
        bx = ar[0][0] + (ar[2][0] - ar[0][0]) * t; by = ar[0][1] + (ar[2][1] - ar[0][1]) * t - 2 * math.sin(math.pi * t)
        br += 'M%s %sl%s %s' % (f(bx), f(by), f(sgn * 1.5), -4)
        br += 'M%s %sl%s %s' % (f(bx), f(by), f(sgn * 3), 2.5)
    fly.append('<path d="%s" stroke="%s" stroke-width=".4" fill="none"/>' % (br, INK))
# ocelli + head bristles
for u, v in [(0, -60), (-3, -56), (3, -56)]:
    x, y = G(u, v)
    fly.append('<circle cx="%s" cy="%s" r="1.3" fill="#fbe9a0" stroke="%s" stroke-width=".5"/>' % (f(x), f(y), INK))
fly.append(bristle(-6, -58, -100, 13, .9)); fly.append(bristle(6, -58, -80, 13, .9))
fly.append(bristle(-9, -45, 105, 10, .8)); fly.append(bristle(9, -45, 75, 10, .8))
# thoracic macrochaetae (point backwards)
for sgn in (-1, 1):
    fly.append(bristle(sgn * 10, -18, 90 - sgn * 8, 20))
    fly.append(bristle(sgn * 10, 2, 90 - sgn * 8, 20))
    fly.append(bristle(sgn * 24, -28, 90 - sgn * 50, 14))
    fly.append(bristle(sgn * 27, -6, 90 - sgn * 40, 14))
    fly.append(bristle(sgn * 6, 32, 90 + sgn * 22, 24))
    fly.append(bristle(sgn * 12, 26, 90 - sgn * 5, 18))
fly.append('</g>')
o.extend(fly)
# labels (a)
o.append(lead([(84, 82), (96, 82), G(-21, -58)]))
o.append(T(80, 80, '紅色複眼', 'lb', 'end'))
o.append(T(80, 94, 'compound eye', 'le', 'end'))
o.append(lead([(296, 76), (284, 76), G(22, -92)]))
o.append(T(300, 74, '觸角', 'lb', 'start'))
o.append(T(300, 88, 'antenna', 'le', 'start'))
o.append(lead([(298, 130), (286, 130), G(12, -1)]))
o.append(T(302, 128, '剛毛', 'lb', 'start'))
o.append(T(302, 142, 'bristles', 'le', 'start'))
o.append(lead([(84, 250), (96, 250), (122, 244)]))
o.append(T(80, 248, '翅脈', 'lb', 'end'))
o.append(T(80, 262, 'wing veins', 'le', 'end'))
# scale bar (body ~ 2.5–3 mm; drawn ~ 200 px)
o.append('<path d="M150 296 h66 M150 292 v8 M216 292 v8" stroke="%s" stroke-width="1"/>' % INK)
o.append(T(222, 300, '= 1 公釐', 'ls', 'start'))
o.append(T(22, 300, '真實身長約 2.5 公釐', 'ls', 'start', halo=True, style='font-weight:700'))

# =============================================================== (b) period mutants
BX = 392
o.append(pframe(BX - 4, 30, 362, 278))
o.append(panel_title(BX + 8, 52, '(b) 1971 年：「時鐘壞掉」的突變果蠅'))
o.append(T(BX + 8, 68, 'Konopka &amp; Benzer：全黑中記錄活動，每列一天（畫兩天）', 'ls', 'start', halo=False))


def fly_acto(x, y, w, tau, title, sub, col, arr=False, seed=1):
    g = [T(x, y - 6, title, 'lb', 'start', halo=False, style='font-size:13px;fill:%s' % col),
         T(x + w, y - 6, sub, 'ls', 'end', halo=False, style='font-weight:700')]
    nd, rh = 6, 7
    pxh = w / 48
    rnd = random.Random(seed)
    g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#e6e0d4"/>' % (x, y, w, nd * rh))
    for d in range(nd):
        yy = y + d * rh
        dd = ''
        for t10 in range(0, 480, 4):
            t = t10 / 10
            if arr:
                act = rnd.random() < .35
            else:
                # activity bouts start at onset_j = 7 + j*tau (absolute h), duration 11 h
                absT = 24 * d + t
                j = math.floor((absT - 7) / tau)
                ph = absT - 7 - j * tau
                act = ph < 11
            if act:
                hgt = rnd.uniform(.3, 1) * (rh - 1)
                dd += 'M%s %sv-%s' % (f(x + t * pxh), f(yy + rh - .4), f(hgt))
        g.append('<path d="%s" stroke="%s" stroke-width=".9" fill="none"/>' % (dd, INK))
    g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width=".8"/>' % (x, y, w, nd * rh, INK))
    g.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width=".7"/>' % (f(x + w / 2), y, f(x + w / 2), y + nd * rh, INK))
    if not arr:
        # guide along onsets
        x0 = x + 7 * pxh
        x1 = x + (7 + (nd - .5) * (tau - 24)) * pxh
        if tau < 24:
            x0 += 24 * pxh; x1 += 24 * pxh
        g.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.6" stroke-dasharray="3 2"/>' % (f(x0), y - 1, f(x1), y + nd * rh + 1, col))
    return ''.join(g)


AW = 160
o.append(fly_acto(BX + 8, 96, AW, 24.0, '正常 per⁺', '約 24 小時', '#2c5d9c', seed=2))
o.append(fly_acto(BX + 184, 96, AW, 19.0, '短週期 perˢ', '約 19 小時', '#a8412c', seed=3))
o.append(fly_acto(BX + 8, 176, AW, 28.0, '長週期 perᴸ', '約 28 小時', '#8a6a1a', seed=4))
o.append(fly_acto(BX + 184, 176, AW, 24, '無節律 per⁰', '亂成一團', '#5d4b38', arr=True, seed=5))
o.append(T(BX + 8, 236, '黑色短線＝果蠅在動；斜線愈斜，代表一天愈偏離 24 小時', 'ls', 'start', halo=False))
# 1984 note with DNA glyph
dna = ''
for k in range(0, 60, 2):
    x = BX + 14 + k
    dna += 'M%s %sL%s %s' % (f(x), f(270 + 6 * math.sin(k / 6)), f(x), f(270 - 6 * math.sin(k / 6)))
o.append('<path d="%s" stroke="#8a6a3a" stroke-width=".6"/>' % dna)
o.append('<path d="%s" fill="none" stroke="#2c5d9c" stroke-width="1.6"/><path d="%s" fill="none" stroke="#a8412c" stroke-width="1.6"/>' % (
    poly([(BX + 14 + k, 270 + 6 * math.sin(k / 6)) for k in range(0, 61)]), poly([(BX + 14 + k, 270 - 6 * math.sin(k / 6)) for k in range(0, 61)])))
o.append(T(BX + 84, 266, '三種突變都落在同一個基因：period（週期）', 'lb', 'start', halo=False, style='font-size:12.5px'))
o.append(T(BX + 84, 282, '1984 年，Hall、Rosbash 與 Young 兩個團隊', 'ls', 'start', halo=False))
o.append(T(BX + 84, 296, '把 period 基因找了出來', 'ls', 'start', halo=False))

# =============================================================== (c) PER/TIM loop drawn as a 24-h clock
o.append(pframe(10, 318, 470, 374))
o.append(panel_title(22, 340, '(c) 時鐘基因怎麼「數」出 24 小時'))
CX, CY = 245, 512
RC, RN = 112, 50
R1, R2 = 120, 138


def P(h, r):
    a = math.radians(h / 24 * 360 - 90)
    return (CX + r * math.cos(a), CY + r * math.sin(a))


def arc(h0, h1, r0, r1):
    a0, b0 = P(h0, r1), P(h1, r1)
    a1, b1 = P(h1, r0), P(h0, r0)
    large = 1 if (h1 - h0) % 24 > 12 else 0
    return 'M%s %s A%s %s 0 %d 1 %s %s L%s %s A%s %s 0 %d 0 %s %s Z' % (f(a0[0]), f(a0[1]), r1, r1, large, f(b0[0]), f(b0[1]), f(a1[0]), f(a1[1]), r0, r0, large, f(b1[0]), f(b1[1]))


# dial ring: night (18->6) dark, day (6->18) light
o.append('<path d="%s" fill="#f6e2a0" stroke="%s" stroke-width=".8"/>' % (arc(6, 18, R1, R2), INK))
o.append('<path d="%s" fill="#2f3f63" stroke="%s" stroke-width=".8"/>' % (arc(18, 30, R1, R2), INK))
td = ''
for h in range(24):
    a, b = P(h, R2 - (6 if h % 6 == 0 else 3.5)), P(h, R2)
    td += 'M%s %sL%s %s' % (f(a[0]), f(a[1]), f(b[0]), f(b[1]))
o.append('<path d="%s" stroke="%s" stroke-width=".8"/>' % (td, INK))
for h, lab in [(0, '0 時'), (6, '6'), (12, '12'), (18, '18')]:
    x, y = P(h, R2 + 11)
    o.append(T(x, y + 4, lab, 'ls', 'middle', halo=True, style='font-weight:700'))
o.append(moon(*P(0, (R1 + R2) / 2), r=6.5))
o.append(sun(*P(12, (R1 + R2) / 2), r=4.6))
# cell
o.append('<circle cx="%s" cy="%s" r="%s" fill="#f8ead8" stroke="%s" stroke-width="2"/>' % (CX, CY, RC, INK))
o.append('<circle cx="%s" cy="%s" r="%s" fill="url(#ink-stipple-l)"/>' % (CX, CY, RC))
o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width=".6"/>' % (CX, CY, RC - 3.5, INK))
# nucleus
o.append('<circle cx="%s" cy="%s" r="%s" fill="#e8dcf0" stroke="%s" stroke-width="1.5"/>' % (CX, CY, RN, INK))
o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width=".6"/>' % (CX, CY, RN - 3, INK))
o.append('<circle cx="%s" cy="%s" r="%s" fill="url(#ink-stipple-l)"/>' % (CX, CY, RN - 3))
for h in (3, 9, 15.5, 21):
    x, y = P(h, RN - 1.5)
    o.append('<circle cx="%s" cy="%s" r="2.6" fill="#f8ead8" stroke="%s" stroke-width=".7"/>' % (f(x), f(y), INK))
o.append(T(CX, CY - 30, '細胞核', 'ls', 'middle', halo=True, style='font-weight:700'))
# gene (double helix) in lower nucleus
gx0, gx1, gy = CX - 34, CX + 30, CY + 18
h1 = [(gx0 + k, gy + 4 * math.sin(k / 4.2)) for k in range(0, gx1 - gx0 + 1)]
h2 = [(gx0 + k, gy - 4 * math.sin(k / 4.2)) for k in range(0, gx1 - gx0 + 1)]
rung = ''.join('M%s %sL%s %s' % (f(x), f(y), f(x2), f(y2)) for (x, y), (x2, y2) in list(zip(h1, h2))[::3])
o.append('<path d="%s" stroke="#8a6a3a" stroke-width=".5"/>' % rung)
o.append('<path d="%s" fill="none" stroke="#5d4b38" stroke-width="1.3"/><path d="%s" fill="none" stroke="#5d4b38" stroke-width="1.3"/>' % (poly(h1), poly(h2)))
o.append('<rect x="%s" y="%s" width="26" height="12" rx="2" fill="#a8412c" fill-opacity=".25" stroke="#a8412c" stroke-width="1"/>' % (gx0 + 18, gy - 6))
o.append(T(CX - 2, gy + 20, 'period 基因', 'ls', 'middle', halo=True, style='font-weight:700;fill:#a8412c'))

# mRNA leaving through lower-left pore (~15:30) to ribosomes (~18 h)
pm = [(gx0 + 28, gy - 2), P(15.6, RN - 8), P(15.6, RN + 6), P(16.6, 74), P(17.6, 84), P(18.6, 86)]
mr = []
dense = []
from plib import bez_pts
pts = bez_pts(pm, per=8)
for i, (x, y) in enumerate(pts):
    if i == 0:
        continue
    x0, y0 = pts[i - 1]
    nx, ny = -(y - y0), (x - x0)
    nl = math.hypot(nx, ny) or 1
    w = 2.2 * math.sin(i * 1.3)
    dense.append((x + nx / nl * w, y + ny / nl * w))
o.append('<path d="%s" fill="none" stroke="#c0392b" stroke-width="1.5"/>' % cr(dense))
# ribosomes on mRNA
for h in (17.7, 18.6):
    x, y = P(h, 85)
    o.append('<ellipse cx="%s" cy="%s" rx="7" ry="5" fill="#d9c08a" stroke="%s" stroke-width=".8"/><ellipse cx="%s" cy="%s" rx="5" ry="3.6" fill="#e9d6a6" stroke="%s" stroke-width=".8"/>' % (
        f(x - 1), f(y - 3), INK, f(x + 1), f(y + 3), INK))


def per(x, y, s=1.0):
    return '<path d="M%s %s c%s %s %s %s %s %s c%s %s %s %s %s %sZ" fill="#5b8ac2" stroke="%s" stroke-width=".9"/>' % (
        f(x - 7 * s), f(y), f(0), f(-6 * s), f(14 * s), f(-7 * s), f(14 * s), f(0), f(0), f(7 * s), f(-14 * s), f(6 * s), f(-14 * s), f(0), INK)


def tim(x, y, s=1.0):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#7fb069" stroke="%s" stroke-width=".9"/>' % (f(x), f(y), f(6.2 * s), f(5.4 * s), INK)


def pair(x, y, s=1.0):
    return per(x - 4 * s, y, s) + tim(x + 7 * s, y + 1 * s, s)


# PER and TIM made at dusk; accumulate and pair through the night
for h, r in [(19.6, 72), (20.4, 92)]:
    o.append(per(*P(h, r)))
for h, r in [(19.9, 98), (20.8, 74)]:
    o.append(tim(*P(h, r)))
for h, r in [(21.6, 82), (22.3, 98), (22.6, 68), (23.3, 86), (0.1, 98), (0.2, 72), (1.0, 86)]:
    o.append(pair(*P(h, r)))
# a pair entering the nucleus through the upper-right pore (~2-3 h)
xa, ya = P(2.0, 82)
xb, yb_ = P(2.9, RN + 4)
o.append('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="%s" stroke-width="1.2" marker-end="url(#ink-arrow)"/>' % (f(xa), f(ya), f((xa + xb) / 2 + 8), f((ya + yb_) / 2 - 2), f(xb), f(yb_), INK))
xi, yi = P(3.2, 30)
o.append(pair(xi, yi, .95))
# repression bar onto the gene
o.append('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="#a8412c" stroke-width="1.8" marker-end="url(#ink-tee)"/>' % (f(xi - 2), f(yi + 6), f(CX + 14), f(CY + 2), f(gx0 + 34), f(gy - 8)))
# morning: DBT + light break PER/TIM down (~6-10 h)
xd, yd = P(7.0, 84)
o.append(per(xd - 6, yd))
o.append('<circle cx="%s" cy="%s" r="10" fill="#e39b4f" stroke="%s" stroke-width=".9"/><path d="M%s %s l10 -5 v10 Z" fill="#f8ead8" stroke="%s" stroke-width=".9"/>' % (
    f(xd + 14), f(yd), INK, f(xd + 14), f(yd), INK))
o.append(T(xd + 16, yd + 22, 'DBT 酵素', 'ls', 'middle', halo=True, style='font-size:10px;font-weight:700;fill:#b06a1e'))
for k, (dx, dy) in enumerate([(-10, -10), (-2, -12), (6, -10)]):
    o.append('<circle cx="%s" cy="%s" r="2.6" fill="#f6e7b0" stroke="%s" stroke-width=".6"/><text x="%s" y="%s" class="ls" text-anchor="middle" style="font-size:4.5px;font-weight:700">P</text>' % (
        f(xd + dx), f(yd + dy), INK, f(xd + dx), f(yd + dy + 1.6)))
# fragments
for h, r, ang in [(8.8, 92, 20), (9.5, 76, -30), (10.1, 96, 60), (10.6, 82, 10)]:
    x, y = P(h, r)
    o.append('<path d="M%s %s l4 -3 l3 4 l-2 3 l-5 -1Z" fill="#5b8ac2" fill-opacity=".55" stroke="%s" stroke-width=".6" transform="rotate(%s %s %s)"/>' % (f(x - 3), f(y), INK, ang, f(x), f(y)))
    o.append('<path d="M%s %s l3 -2 l2 3 l-3 2Z" fill="#7fb069" fill-opacity=".55" stroke="%s" stroke-width=".6"/>' % (f(x + 5), f(y + 3), INK))
# light ray striking from outside at ~6 h
lx0, ly0 = P(5.2, R2 + 4)
lx1, ly1 = P(6.2, 100)
o.append('<path d="M%s %s L%s %s" stroke="#e0a526" stroke-width="2.2" stroke-dasharray="5 3" marker-end="url(#ink-arrow)"/>' % (f(lx0), f(ly0), f(lx1), f(ly1)))
# big circular flow arrow inside the cytoplasm ring (clockwise)
o.append('<path d="%s" fill="none" stroke="#8a6a3a" stroke-width="1.1" stroke-dasharray="2 3" marker-end="url(#ink-arrow)"/>' % (
    'M%s %s A%s %s 0 0 1 %s %s' % (f(P(11.2, 104)[0]), f(P(11.2, 104)[1]), 104, 104, f(P(14.6, 104)[0]), f(P(14.6, 104)[1]))))
# step badges on the ring + corner texts
steps = [
    (14.5, '①', '白天：period 基因開工，', '抄出 mRNA（製造說明書）', (22, 650), 'start'),
    (20.5, '②', '入夜：做出 PER 蛋白，', '和 TIM 配對，越積越多', (22, 360), 'start'),
    (2.0, '③', '半夜：PER＋TIM 進入細胞核，', '把自己的基因關掉', (468, 360), 'end'),
    (8.5, '④', '早上：DBT 和光把它們分解，', '基因重新開工 → 回到 ①', (468, 650), 'end'),
]
cols = ['#a8412c', '#2c5d9c', '#5b3f8a', '#b06a1e']
for (h, n, l1, l2, (tx, ty), anc), col in zip(steps, cols):
    x, y = P(h, (R1 + R2) / 2)
    o.append(num(x, y, n.replace('①', '1').replace('②', '2').replace('③', '3').replace('④', '4'), col=col, r=8.5))
    o.append(T(tx, ty, n + ' ' + l1, 'lb', anc, style='font-size:12.5px;fill:%s' % col))
    o.append(T(tx if anc == 'start' else tx, ty + 15, l2, 'ls', anc, style='font-weight:700'))
# small legend for molecules
lgx, lgy = 22, 400
o.append(per(lgx + 8, lgy))
o.append(T(lgx + 20, lgy + 4, 'PER', 'ls', 'start', style='font-weight:700;fill:#2c5d9c'))
o.append(tim(lgx + 8, lgy + 18))
o.append(T(lgx + 20, lgy + 22, 'TIM', 'ls', 'start', style='font-weight:700;fill:#4f7a3a'))
o.append('<path d="M%s %s q4 -4 8 0 q4 4 8 0" fill="none" stroke="#c0392b" stroke-width="1.5"/>' % (lgx, lgy + 36))
o.append(T(lgx + 20, lgy + 40, 'mRNA', 'ls', 'start', style='font-weight:700;fill:#a8412c'))

# =============================================================== (d) Nobel
o.append(pframe(490, 318, 260, 374))
o.append(panel_title(502, 340, '(d) 2017 年諾貝爾獎'))
MX, MY, MR = 620, 450, 62
# ribbon
o.append('<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="#2c5d9c" stroke="%s" stroke-width="1"/>' % (MX - 34, 352, MX - 8, 352, MX + 6, MY - 50, MX - 18, MY - 50, INK))
o.append('<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="#a8412c" stroke="%s" stroke-width="1"/>' % (MX + 34, 352, MX + 8, 352, MX - 6, MY - 50, MX + 18, MY - 50, INK))
o.append('<path d="M%s %s L%s %s L%s %s Z" fill="url(#ink-hatch)" opacity=".6"/>' % (MX + 34, 352, MX + 18, MY - 50, MX + 8, 352))
o.append('<circle cx="%s" cy="%s" r="%s" fill="url(#%s-gold)" stroke="%s" stroke-width="1.6"/>' % (MX, MY, MR, PID, INK))
o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#8a5a0a" stroke-width="1"/>' % (MX, MY, MR - 6))
o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#fff2b8" stroke-width=".8" stroke-opacity=".7"/>' % (MX, MY, MR - 7.5))
# laurel wreath: two branches of leaves along an arc
for sgn in (-1, 1):
    pts = []
    for k in range(11):
        th = math.radians(90 + sgn * (25 + k * 13))  # from bottom up each side
        x, y = MX + (MR - 18) * math.cos(th), MY + (MR - 18) * math.sin(th)
        pts.append((x, y))
        ang = math.degrees(th) + sgn * 90 + 180
        for side in (-1, 1):
            la = ang + side * 38 - sgn * 0
            lx2, ly2 = x + math.cos(math.radians(la)) * 9, y + math.sin(math.radians(la)) * 9
            mxl, myl = (x + lx2) / 2, (y + ly2) / 2
            nx, ny = -(ly2 - y) * .32, (lx2 - x) * .32
            o.append('<path d="M%s %sQ%s %s %s %sQ%s %s %s %sZ" fill="#c99a2e" stroke="#6a4a0a" stroke-width=".6"/>' % (
                f(x), f(y), f(mxl + nx), f(myl + ny), f(lx2), f(ly2), f(mxl - nx), f(myl - ny), f(x), f(y)))
    o.append('<path d="%s" fill="none" stroke="#6a4a0a" stroke-width="1"/>' % cr(pts))
o.append('<text x="%s" y="%s" text-anchor="middle" style="font-family:Georgia,serif;font-size:24px;font-weight:700;fill:#5a3d08">2017</text>' % (MX, MY + 8))
o.append('<path d="M%s %s a%s %s 0 0 1 %s %s" fill="none" stroke="#fff6d0" stroke-width="3" stroke-opacity=".55" stroke-linecap="round"/>' % (MX - 40, MY - 26, MR - 12, MR - 12, 36, -18))
o.append(T(620, 538, '諾貝爾生理學或醫學獎', 'lb', 'middle', style='font-size:15px'))
o.append(T(620, 562, 'Jeffrey C. Hall', 'le', 'middle', style='font-size:13px;font-style:normal;font-weight:600;fill:#2a2018'))
o.append(T(620, 578, 'Michael Rosbash', 'le', 'middle', style='font-size:13px;font-style:normal;font-weight:600;fill:#2a2018'))
o.append(T(620, 594, 'Michael W. Young', 'le', 'middle', style='font-size:13px;font-style:normal;font-weight:600;fill:#2a2018'))
o.append('<rect x="504" y="610" width="232" height="44" rx="5" fill="#f6e7b0" stroke="#c9962e" stroke-width="1"/>')
o.append(T(620, 629, '「發現控制晝夜節律的', 'lb', 'middle', halo=False, style='font-size:14px'))
o.append(T(620, 647, '分子機制」', 'lb', 'middle', halo=False, style='font-size:14px'))
o.append(T(620, 676, '從一株含羞草到一個基因：約 290 年', 'ls', 'middle', halo=False, style='font-weight:700;fill:#8a6a3a'))

caption = ('<b>圖 1·C　果蠅、時鐘基因與 2017 年諾貝爾獎。</b>(a) 只有約 2.5 公釐長的果蠅，是研究生理時鐘的主角。'
           '(b) 1971 年科學家找到「時鐘壞掉」的突變果蠅：有的一天約 19 小時、有的約 28 小時、有的完全沒節律，問題都出在同一個 period 基因。'
           '(c) 這個基因白天開工，做出的 PER 蛋白在夜裡累積、和 TIM 配對後回到細胞核把自己關掉，早上再被分解——一圈剛好約 24 小時。'
           '(d) 解開這個機制的三位美國科學家獲得 2017 年諾貝爾獎。示意圖，分子與細胞比例未依實際大小；獎牌為通用示意，非實物設計。')
write(PID, '圖 1·C', '果蠅、時鐘基因與 2017 年諾貝爾獎', 'Fruit flies, clock genes and the 2017 Nobel Prize',
      H, '<g transform="translate(0 -18)">' + '\n'.join(x for x in o if x) + '</g>', '四格圖：(a) 果蠅背面精細圖，紅色複眼、翅脈與剛毛；(b) 正常、短週期、長週期與無節律突變果蠅的活動紀錄；(c) 以 24 小時鐘面呈現的 PER／TIM 負回饋循環；(d) 2017 年諾貝爾生理學或醫學獎通用金牌與三位得獎者姓名。',
      caption, ''.join(defs))
