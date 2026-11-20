import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from common import *

PID = 'pl-banxia'
G = '#b9cb8c'   # leaf tint
G2 = '#9db46e'  # petiole
o = []
o.append('''<defs>
<linearGradient id="pl-banxia-pet" x1="0" x2="1"><stop offset="0" stop-color="#c4d49a"/><stop offset="1" stop-color="#7f9a55"/></linearGradient>
<radialGradient id="pl-banxia-corm" cx=".38" cy=".35" r=".8"><stop offset="0" stop-color="#f7eedb"/><stop offset=".7" stop-color="#e2cfa6"/><stop offset="1" stop-color="#b8976a"/></radialGradient>
<radialGradient id="pl-banxia-grain" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#f6d2a8"/><stop offset=".6" stop-color="#d0864f"/><stop offset="1" stop-color="#9a4a26"/></radialGradient>
<radialGradient id="pl-banxia-fa" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#f8eab8"/><stop offset="1" stop-color="#d8b55c"/></radialGradient>
<linearGradient id="pl-banxia-spa" x1="0" x2="1"><stop offset="0" stop-color="#cfdca6"/><stop offset=".55" stop-color="#a7bd76"/><stop offset="1" stop-color="#6f8a4a"/></linearGradient>
</defs>''')

# ---------------- Pinellia whole plant -----------------
P = []
cx, cy = 250, 548   # corm centre
# fibrous roots (from upper shoulders of the corm, arching down)
rnd = random.Random(4)
roots = []
for i in range(16):
    side = -1 if i % 2 == 0 else 1
    a0 = (rnd.random() * 0.9 + 0.2) * side
    sx = cx + side * (14 + rnd.random() * 6)
    sy = cy - 10 + rnd.random() * 8
    L = 35 + rnd.random() * 45
    pts_ = [(sx, sy)]
    x, y = sx, sy
    ang = math.radians(90 - side * (40 + rnd.random() * 40))
    for k in range(6):
        ang += (rnd.random() - 0.5) * 0.5 + side * -0.12
        x += math.cos(ang) * L / 6; y += math.sin(ang) * L / 6
        pts_.append((x, y))
    roots.append('<path d="%s" class="ink2" stroke-width="%.2f"/>' % (smooth(pts_), 0.5 + rnd.random() * 0.4))
    # root hairs
    for k in range(2, 6, 2):
        hx, hy = pts_[k]
        roots.append('<path d="M%s %s l%s %s" class="ink2" stroke-width=".3"/>' % (f(hx), f(hy), f(side * 4), f(3)))
P.append('<g>' + ''.join(roots) + '</g>')
# corm
corm = smooth([(cx - 24, cy - 4), (cx - 20, cy - 16), (cx - 8, cy - 21), (cx, cy - 18), (cx + 9, cy - 21), (cx + 21, cy - 15),
               (cx + 24, cy - 2), (cx + 19, cy + 14), (cx + 4, cy + 21), (cx - 12, cy + 19), (cx - 22, cy + 10)], close=True)
P.append('<path d="%s" fill="url(#pl-banxia-corm)"/>' % corm)
P.append('<path d="%s" fill="url(#ink-hatch-l)" clip-path="url(#pl-banxia-cc)"/>' % corm)
P.append('<clipPath id="pl-banxia-cc"><path d="M%d %d h40 v40 h-60z"/></clipPath>' % (cx - 4, cy - 2))
P.append(stipple_ellipse(cx + 4, cy + 4, 20, 15, 60, r=.45, seed=7, bias=(0.6, 0.8)))
P.append('<path d="%s" class="ink3" stroke-width="1.5"/>' % corm)
# corm bud / leaf-base scar on top
P.append('<path d="M%d %d q8 -10 16 0" class="ink" fill="#d9c79a"/>' % (cx - 8, cy - 19))

# petioles: (start, control points..., top)
def petiole(points, w=3.2):
    d = smooth(points)
    return ('<path d="%s" stroke="#2a2018" stroke-width="%.1f" fill="none" stroke-linecap="round"/>'
            '<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" stroke-linecap="round"/>') % (d, w + 1.8, d, G2, w)

leaf1 = [(cx - 6, cy - 20), (cx - 18, cy - 110), (cx - 55, cy - 210), (cx - 95, cy - 280), (cx - 110, cy - 300)]
leaf2 = [(cx + 6, cy - 20), (cx + 20, cy - 100), (cx + 52, cy - 200), (cx + 80, cy - 262), (cx + 90, cy - 285)]
leaf3 = [(cx + 2, cy - 22), (cx + 10, cy - 70), (cx + 40, cy - 115), (cx + 78, cy - 140)]
ped = [(cx, cy - 22), (cx + 2, cy - 130), (cx - 4, cy - 220), (cx - 10, cy - 280), (cx - 12, cy - 300)]
P.append(petiole(leaf1)); P.append(petiole(leaf2)); P.append(petiole(leaf3, 2.4)); P.append(petiole(ped, 2.6))
# sheath at base
P.append('<path d="M%d %d q-6 -30 0 -52 q6 22 4 52z" fill="#c6d49b" class="ink2"/>' % (cx - 4, cy - 18))

# trifoliate leaves
def trifol(tx, ty, ang, Lm, Ll, W, seed):
    s = []
    s.append(leaf(tx, ty, ang - 64, Ll, W * 0.85, p=0.55, q=1.05, bend=0.04, fill=G, veins=7, vein_ang=55))
    s.append(leaf(tx, ty, ang + 64, Ll, W * 0.85, p=0.55, q=1.05, bend=-0.04, fill=G, veins=7, vein_ang=55))
    s.append(leaf(tx, ty, ang, Lm, W, p=0.55, q=1.05, bend=0.03, fill=G, veins=8, vein_ang=55))
    s.append('<circle cx="%s" cy="%s" r="2.6" fill="%s" stroke="#2a2018" stroke-width=".7"/>' % (f(tx), f(ty), G2))
    return ''.join(s)
P.append(trifol(cx - 110, cy - 300, -118, 122, 96, 38, 1))
P.append(trifol(cx + 90, cy - 285, -64, 116, 88, 36, 2))
# young simple ovate-cordate leaf (seedling leaf form)
P.append(leaf(cx + 78, cy - 140, -20, 62, 40, p=0.35, q=1.2, bend=-0.03, fill='#c7d6a0', veins=5, vein_ang=60, base_round=0.9))

# bulbils on petioles (one mid-petiole on leaf 1, one at leaflet junction of leaf 2)
def bulbil(x, y, r=5.5):
    return ('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#pl-banxia-corm)" class="ink"/>'
            '<path d="M%s %s q2 -3 4 0" class="ink2"/>') % (f(x), f(y), f(r), f(r * 0.85), f(x - 2), f(y - 1))
b1 = (cx - 32, cy - 150)
P.append(bulbil(b1[0] - 4, b1[1], 6))
P.append(bulbil(cx + 85, cy - 276, 4.5))

# peduncle + spathe + spadix appendage
sx, sy = cx - 12, cy - 300
spathe_tube = smooth([(sx - 6, sy + 2), (sx - 8, sy - 20), (sx - 5, sy - 36), (sx + 6, sy - 38), (sx + 8, sy - 20), (sx + 6, sy + 2)], close=False)
P.append('<path d="%s Z" fill="url(#pl-banxia-spa)" class="ink"/>' % spathe_tube)
P.append('<path d="M%s %s q6 -18 2 -36" class="ink2"/>' % (f(sx - 1), f(sy)))
blade = smooth([(sx - 6, sy - 34), (sx - 14, sy - 62), (sx - 16, sy - 92), (sx - 8, sy - 118), (sx + 4, sy - 126), (sx + 14, sy - 116),
                (sx + 16, sy - 90), (sx + 12, sy - 58), (sx + 6, sy - 36)], close=True)
P.append('<path d="%s" fill="url(#pl-banxia-spa)"/>' % blade)
P.append('<path d="%s" fill="url(#ink-hatch-l)" clip-path="url(#pl-banxia-bc)"/>' % blade)
P.append('<clipPath id="pl-banxia-bc"><rect x="%s" y="%s" width="20" height="100"/></clipPath>' % (f(sx + 3), f(sy - 130)))
for k in range(-2, 3):
    P.append('<path d="M%s %s q%s -40 %s -86" class="ink2" stroke-width=".4"/>' % (f(sx + k * 3), f(sy - 36), f(k * 5), f(k * 2)))
P.append('<path d="%s" class="ink" stroke="#5b4a6a"/>' % blade)
# hood tip & purplish margin
P.append('<path d="M%s %s q6 -3 9 6" class="ink" stroke="#6b4f72" stroke-width="1.3"/>' % (f(sx + 4), f(sy - 126)))
# appendage (whip) emerging from throat, up and out
app = [(sx + 2, sy - 50), (sx + 4, sy - 110), (sx + 9, sy - 160), (sx + 22, sy - 196), (sx + 40, sy - 216), (sx + 52, sy - 220)]
P.append('<path d="%s" stroke="#2a2018" stroke-width="3.6" fill="none" stroke-linecap="round"/>' % smooth(app))
P.append('<path d="%s" stroke="#8a9a5a" stroke-width="2" fill="none" stroke-linecap="round"/>' % smooth(app))
P.append('<path d="%s" stroke="#7a5a80" stroke-width=".9" fill="none" stroke-dasharray="3 4"/>' % smooth(app[1:]))

body = [o[0], '<g filter="url(#ink-rough)">' + '\n'.join(P) + '</g>']

# ---------- labels for Pinellia ----------
L = []
L.append(label(14, 40, '佛焰花序附屬器', None) + label(14, 54, 'Spadix appendage', None, cls='le halo'))
L.append(leader(130, 47, sx + 18, sy - 192))
L.append(label(14, 100, '佛焰苞', None) + label(14, 114, 'Spathe', None, cls='le halo'))
L.append(leader(64, 96, sx - 14, sy - 85))
L.append(label(14, 362, '三出複葉', None) + label(14, 376, 'Trifoliate leaf', None, cls='le halo'))
L.append(label(14, 390, '小葉橢圓披針形', None, cls='ls halo'))
L.append(leader(70, 350, 84, 262))
L.append(label(14, 420, '珠芽', None) + label(14, 434, 'Bulbil', None, cls='le halo'))
L.append(leader(50, 416, b1[0] - 11, b1[1]))
L.append(label(14, 470, '葉柄', None) + label(14, 484, 'Petiole', None, cls='le halo'))
L.append(leader(50, 466, cx - 16, cy - 98))
L.append(label(342, 528, '塊莖（藥用）', None) + label(342, 542, 'Corm (tuber)', None, cls='le halo'))
L.append(leader(338, 524, cx + 22, cy - 8))
L.append(label(342, 584, '鬚根', None) + label(342, 598, 'Fibrous roots', None, cls='le halo'))
L.append(leader(338, 580, cx + 52, cy + 22))
L.append(label(322, 342, '幼葉：單葉卵狀心形', None, cls='ls halo'))
L.append(label(322, 356, 'juvenile simple leaf', None, cls='le halo'))
L.append(leader(370, 361, cx + 112, cy - 166))

# name block
L.append('<text x="14" y="632" class="lt">半夏</text><text x="54" y="632" class="le" style="font-size:13px">Pinellia ternata (Thunb.) Breit.</text>')
L.append('<text x="14" y="650" class="ls">天南星科 Araceae · 藥用部位：塊莖 Pinelliae Rhizoma</text>')
L.append(scalebar(300, 625, 18, 2))
L.append('<text x="300" y="646" class="ls">全株約 1/2 自然大小</text>')
body.append('\n'.join(L))

# ---------- Sorghum ----------
S = []
ax, ay0, ay1 = 560, 300, 50
# culm and leaf
S.append('<path d="M%d %d L%d %d" stroke="#2a2018" stroke-width="5.4" stroke-linecap="round"/>' % (ax, 340, ax, ay0))
S.append('<path d="M%d %d L%d %d" stroke="#c9c08a" stroke-width="3.4" stroke-linecap="round"/>' % (ax, 340, ax, ay0))
S.append('<path d="M%d 324 h7" class="ink"/>' % (ax - 3.5))
# leaf blade arching to the right
lb = [(ax + 2, 330), (ax + 50, 300), (ax + 110, 288), (ax + 160, 296), (ax + 185, 318)]
lb2 = [(ax + 185, 318), (ax + 158, 306), (ax + 108, 300), (ax + 54, 314), (ax + 2, 340)]
S.append('<path d="%s" fill="#bccb8e" class="ink"/>' % smooth(lb + lb2[1:], close=True))
S.append('<path d="%s" stroke="#f3efd8" stroke-width="2.2" fill="none"/>' % smooth([(ax + 2, 335), (ax + 52, 307), (ax + 110, 294), (ax + 160, 301), (ax + 185, 318)]))
for k in range(1, 5):
    S.append('<path d="%s" class="ink2" stroke-width=".35"/>' % smooth([(ax + 4, 332 - k * 0.6), (ax + 52, 304 - k * 1.2 + 4), (ax + 110, 291 + k * 0.5), (ax + 160, 299 + k * .5)]))
# panicle axis
S.append('<path d="M%d %d C%d %d %d %d %d %d" class="ink" stroke-width="1.6"/>' % (ax, ay0, ax + 2, 220, ax - 2, 120, ax, ay1))
rnd = random.Random(11)
grains = []
branches = []
for i, y in enumerate(range(ay0 - 8, ay1 + 4, -13)):
    t = (ay0 - y) / (ay0 - ay1)
    env = 62 * math.sin(math.pi * (0.12 + 0.8 * t)) ** 0.8
    for side in (-1, 1):
        if (i + (side > 0)) % 1:
            continue
        Lb = env * (0.75 + rnd.random() * 0.3)
        a = math.radians(-90 + side * (38 + 18 * (1 - t)))
        ex, ey = ax + math.cos(a) * Lb, y + math.sin(a) * Lb
        branches.append('<path d="M%d %s Q%s %s %s %s" class="ink2" stroke-width=".6"/>' % (ax, f(y), f(ax + side * Lb * 0.4), f(y - 3), f(ex), f(ey)))
        nseeds = 2 + int(Lb / 18)
        for k in range(nseeds):
            kk = 0.35 + 0.65 * k / max(nseeds - 1, 1)
            gx = ax + (ex - ax) * kk + (rnd.random() - 0.5) * 6
            gy = y + (ey - y) * kk + (rnd.random() - 0.5) * 6 - 3
            ang = math.degrees(a) + 90 + (rnd.random() - 0.5) * 40
            grains.append((gy, '<g transform="translate(%s %s) rotate(%s)"><ellipse rx="4.4" ry="5.4" fill="url(#pl-banxia-grain)" stroke="#2a2018" stroke-width=".55"/>'
                                '<path d="M-3.4 2.4 Q0 8 3.4 2.4 Q0 4.6 -3.4 2.4z" fill="#5a3a24" stroke="#2a2018" stroke-width=".4"/>'
                                '<path d="M0 -4.6 l0 -3" class="ink2" stroke-width=".35"/></g>' % (f(gx), f(gy), f(ang))))
S.append(''.join(branches))
grains.sort(key=lambda g: -g[0])
S.append(''.join(g[1] for g in grains))
body.append('<g filter="url(#ink-rough)">' + '\n'.join(S) + '</g>')
# sorghum labels
L2 = []
L2.append(label(650, 60, '圓錐花序', None) + label(650, 74, 'Panicle', None, cls='le halo'))
L2.append(leader(646, 66, 600, 110))
L2.append(label(650, 120, '穎果（帶穎）', None) + label(650, 134, 'Grain in glumes', None, cls='le halo'))
L2.append(leader(646, 126, 604, 168))
L2.append(label(650, 236, '稈與葉', None) + label(650, 250, 'Culm &amp; leaf', None, cls='le halo'))
L2.append(leader(668, 256, 680, 293))
L2.append('<text x="452" y="372" class="lt">秫米</text><text x="492" y="372" class="le" style="font-size:13px">Sorghum bicolor (L.) Moench</text>')
L2.append('<text x="452" y="390" class="ls">高粱 · 禾本科 Poaceae · 藥用部位：去殼種仁（米）</text>')
L2.append('<text x="452" y="406" class="ls" fill="#a8412c" style="fill:#a8412c">※「秫米」一說為黏粟（糯小米 Setaria italica），待查證</text>')
body.append('\n'.join(L2))

# ---------- detail cells ----------
D = []
D.append('<path d="M440 20 V 650" class="panel"/>')
D.append('<path d="M452 420 H 750" class="panel"/>')
cells = [(452, 428), (552, 428), (652, 428), (452, 540), (552, 540), (652, 540)]
# 1 corm longitudinal section
x0, y0 = 500, 478
sec = smooth([(x0 - 30, y0), (x0 - 26, y0 - 18), (x0 - 10, y0 - 26), (x0, y0 - 22), (x0 + 10, y0 - 26), (x0 + 26, y0 - 18), (x0 + 30, y0), (x0 + 22, y0 + 20), (x0, y0 + 27), (x0 - 22, y0 + 20)], close=True)
D.append('<g filter="url(#ink-rough)"><path d="%s" fill="#f7f1e2"/>' % sec)
D.append(stipple_ellipse(x0, y0 + 2, 24, 20, 120, r=.4, seed=3, op=.45))
D.append('<path d="%s" fill="none" stroke="#b8976a" stroke-width="3"/>' % sec)
D.append('<path d="%s" class="ink"/>' % sec)
D.append('<path d="M%d %d q4 -12 8 0 q-4 -4 -8 0" fill="#c9d6a3" class="ink2"/>' % (x0 - 4, y0 - 23))
for k in range(-2, 3):
    D.append('<path d="M%d %d q%d 14 %d 30" class="ink2" stroke-width=".35" stroke-dasharray="1 2"/>' % (x0 + k * 7, y0 - 16, k * 2, k * 4))
D.append('</g>')
D.append(num(462, 438, 1) + '<text x="474" y="442" class="ls">塊莖縱切</text><text x="462" y="526" class="le">Corm, l.s. ×2</text>')
# 2 spathe opened: female flowers at base, sterile gap, male flowers, appendage
x0, y0 = 600, 526
D.append('<g filter="url(#ink-rough)" transform="translate(600 526) scale(.8) translate(-600 -526)">')
D.append('<path d="M%d %d q-14 -30 -10 -66 q10 -6 20 0 q4 36 -10 66z" fill="#d6e1b1" class="ink"/>' % (x0, y0))
D.append('<path d="M%d %d v-72" stroke="#2a2018" stroke-width="3.2"/>' % (x0, y0 - 4))
D.append('<path d="M%d %d v-72" stroke="#c7cf8e" stroke-width="1.8"/>' % (x0, y0 - 4))
for k in range(5):
    D.append('<ellipse cx="%s" cy="%d" rx="2.6" ry="2.2" fill="#9fbf6a" stroke="#2a2018" stroke-width=".5"/>' % (f(x0 + (-2.5 if k % 2 else 2.5)), y0 - 8 - k * 3))
for k in range(6):
    D.append('<rect x="%s" y="%d" width="3" height="2.4" fill="#e8d98a" stroke="#2a2018" stroke-width=".4"/>' % (f(x0 + (-3.5 if k % 2 else 0.5)), y0 - 34 - k * 3))
D.append('<path d="M%d %d q2 -12 12 -20" stroke="#2a2018" stroke-width="2.4" fill="none"/>' % (x0, y0 - 74))
D.append('<path d="M%d %d q2 -12 12 -20" stroke="#8a9a5a" stroke-width="1.2" fill="none"/></g>' % (x0, y0 - 74))
D.append(num(562, 438, 2) + '<text x="574" y="442" class="ls">佛焰苞剖開</text>')
D.append('<text x="618" y="518" class="ls halo">雌花</text><text x="618" y="494" class="ls halo">雄花</text><text x="618" y="470" class="ls halo">附屬器</text>')
D.append(leader(616, 514, x0 + 3, y0 - 13) + leader(616, 490, x0 + 3, y0 - 38) + leader(616, 466, x0 + 4, y0 - 66))
D.append('<text x="562" y="538" class="le">Spathe opened</text>')
# 3 bulbil enlarged
x0, y0 = 700, 482
D.append('<g filter="url(#ink-rough)"><path d="M%d %d l50 -18" stroke="#2a2018" stroke-width="5.6"/><path d="M%d %d l50 -18" stroke="%s" stroke-width="3.6"/>' % (x0 - 26, y0 + 10, x0 - 26, y0 + 10, G2))
D.append('<ellipse cx="%d" cy="%d" rx="12" ry="10" fill="url(#pl-banxia-corm)" class="ink"/>' % (x0, y0 + 4))
D.append(stipple_ellipse(x0 + 3, y0 + 7, 8, 6, 25, r=.4, seed=9, bias=(.5, .8)))
D.append('<path d="M%d %d q4 -6 8 0" class="ink2"/></g>' % (x0 - 3, y0 - 2))
D.append(num(662, 438, 3) + '<text x="674" y="442" class="ls">珠芽 ×3</text><text x="662" y="526" class="le">Bulbil on petiole</text>')
# 4 法半夏 slice
x0, y0 = 500, 594
D.append('<g filter="url(#ink-rough)"><ellipse cx="%d" cy="%d" rx="30" ry="22" fill="#c9a24c" class="ink"/>' % (x0 + 2, y0 + 4))
D.append('<ellipse cx="%d" cy="%d" rx="30" ry="22" fill="url(#pl-banxia-fa)" class="ink"/>' % (x0, y0))
D.append(stipple_ellipse(x0, y0, 26, 18, 90, r=.45, seed=21, op=.5))
D.append('<ellipse cx="%d" cy="%d" rx="26" ry="18" fill="none" stroke="#a88430" stroke-width=".7" stroke-dasharray="2 2"/>' % (x0, y0))
for k in range(5):
    a = k * 1.3
    D.append('<path d="M%s %s l%s %s" class="ink2" stroke-width=".4"/>' % (f(x0 + math.cos(a) * 8), f(y0 + math.sin(a) * 6), f(math.cos(a) * 9), f(math.sin(a) * 7)))
D.append('</g>')
D.append(num(462, 550, 4) + '<text x="474" y="554" class="ls">法半夏飲片</text><text x="462" y="634" class="le">Processed slice</text>')
D.append('<text x="462" y="647" class="ls">甘草、石灰炮製，色黃</text>')
# 5 sorghum grain enlarged with glumes
x0, y0 = 600, 596
D.append('<g filter="url(#ink-rough)">')
D.append('<path d="M%d %d q-18 -8 -14 -30 q8 10 14 30z" fill="#4a3424" class="ink"/>' % (x0 - 2, y0 + 16))
D.append('<path d="M%d %d q18 -8 14 -30 q-8 10 -14 30z" fill="#5b4030" class="ink"/>' % (x0 + 2, y0 + 16))
D.append('<ellipse cx="%d" cy="%d" rx="14" ry="17" fill="url(#pl-banxia-grain)" class="ink"/>' % (x0, y0 - 6))
D.append('<path d="M%d %d q5 -9 0 -14 q-5 5 0 14z" fill="#f2dcb0" class="ink2"/>' % (x0 - 2, y0 + 8))
D.append('<path d="M%d %d q8 -6 6 -18" stroke="#fff" stroke-opacity=".5" stroke-width="2" fill="none"/></g>' % (x0 - 6, y0 - 6))
D.append(num(562, 550, 5) + '<text x="574" y="554" class="ls">高粱穎果 ×4</text><text x="562" y="634" class="le">Caryopsis</text>')
D.append('<text x="620" y="608" class="ls halo">胚</text>' + leader(618, 604, x0, y0 + 2))
# 6 hulled grains (秫米)
rnd = random.Random(5)
D.append('<g filter="url(#ink-rough)">')
for k in range(14):
    gx = 700 + (rnd.random() - 0.5) * 60; gy = 598 + (rnd.random() - 0.5) * 26 - (abs(gx - 700) < 18) * 6
    D.append('<ellipse cx="%s" cy="%s" rx="5.4" ry="4.6" transform="rotate(%d %s %s)" fill="%s" stroke="#2a2018" stroke-width=".55"/>' % (
        f(gx), f(gy), rnd.randint(0, 180), f(gx), f(gy), rnd.choice(['#e9c9a0', '#dfb88a', '#f0d6b4'])))
D.append('</g>')
D.append(num(662, 550, 6) + '<text x="674" y="554" class="ls">秫米（去殼）</text><text x="662" y="634" class="le">Hulled grains ×1</text>')
body.append('\n'.join(D))

cap = ('<b>圖 9-A　〈邪客〉半夏湯的兩味藥。</b>左：半夏（天南星科）全株——地下的球形<b>塊莖</b>即藥用部位，上部生鬚根；細長葉柄頂生三出複葉，葉柄上可見繁殖用的<b>珠芽</b>；'
       '綠色佛焰苞包住肉穗花序，頂端延伸成鞭狀附屬器。右：秫米，此處以高粱（Sorghum bicolor）繪出；但「秫米」究竟指高粱米，還是黏粟（糯小米），歷代注家說法不一 <span class="ev C">待查證</span>。'
       '半夏降逆化痰、秫米和胃——兩味都在「通」中焦，而不是安神。依植物誌與藥材圖鑑重繪，比例為示意。')
open('/home/user/Insomnia/figs/pl-banxia.html', 'w').write(figure(PID, 'Plate 9·A', '〈邪客〉半夏湯：半夏與秫米', 'Pinellia &amp; sorghum: the first insomnia formula', 660,
                                                         '半夏全株（塊莖、三出複葉、佛焰苞）與秫米（高粱）的植物圖譜', '\n'.join(body), cap))
