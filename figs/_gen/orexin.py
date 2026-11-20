import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
from plib import *

P = 'pl-orexin'
D = []
O = []
add = O.append
OX = '#c9962e'; OXS = '#f6e7b0'
rnd = random.Random(21)

D.append('<marker id="%s-ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (P, TCM))
D.append('<marker id="%s-tb" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M5 0V10" stroke="%s" stroke-width="2.4"/></marker>' % (P, WEST))
D.append('<radialGradient id="%s-so" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="#fbeec4"/><stop offset="1" stop-color="#e2bd5c"/></radialGradient>' % P)

# =============== the orexin neuron ===============
S = (300, 214)
shapes = []          # filled cell parts (merged silhouette)
spines = ''


def branch(p0, ang, length, w, depth, seed):
    global spines
    r = random.Random(seed)
    pts = [p0]
    a = ang
    x, y = p0
    for k in range(4):
        a += r.uniform(-12, 12)
        x += length / 4 * math.cos(math.radians(a)); y += length / 4 * math.sin(math.radians(a))
        pts.append((x, y))
    shapes.append(tapered(pts, w, max(.9, w * .35)))
    # spines
    dense = resample(bez_pts(pts, per=8), 5)
    for i, (sx, sy) in enumerate(dense[2:-1]):
        sa = math.radians(a + (90 if i % 2 else -90) + r.uniform(-25, 25))
        ln = 2.5 + r.random() * 1.5
        spines += 'M%s %s l%s %s ' % (f(sx), f(sy), f(ln * math.cos(sa)), f(ln * math.sin(sa)))
    tips = [pts[-1]]
    if depth > 0:
        for db in (-28, 26):
            mid = pts[2] if db < 0 else pts[3]
            tips += branch(mid, a + db, length * .62, w * .55, depth - 1, seed * 7 + db)
    return tips


dend = [(-178, 92), (-148, 96), (-205, 80), (-115, 78), (140, 72), (-238, 70), (112, 60)]
tips = []
for i, (a, L) in enumerate(dend):
    p0 = (S[0] + 16 * math.cos(math.radians(a)), S[1] + 14 * math.sin(math.radians(a)))
    tips += branch(p0, a, L, 9, 2 if i < 4 else 1, 100 + i)
soma = [(S[0] - 26, S[1] - 4), (S[0] - 16, S[1] - 20), (S[0] + 2, S[1] - 26), (S[0] + 20, S[1] - 16), (S[0] + 30, S[1] - 4),
        (S[0] + 38, S[1] + 2), (S[0] + 24, S[1] + 14), (S[0] + 6, S[1] + 24), (S[0] - 14, S[1] + 20)]
soma_d = cr(soma, True)
# axon (thin, unmyelinated) to branch point
AX = [(S[0] + 36, S[1] + 2), (S[0] + 70, S[1] + 4), (S[0] + 120, S[1]), (S[0] + 160, S[1] + 2)]
shapes.append(tapered(AX, 4.5, 2.4))
add('<g>' + ''.join('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (d, INK) for d in shapes + [soma_d]) + '</g>')
add('<g>' + ''.join('<path d="%s" fill="%s"/>' % (d, OXS) for d in shapes) + '<path d="%s" fill="url(#%s-so)"/></g>' % (soma_d, P))
add('<g opacity=".7">' + ''.join('<path d="%s" fill="url(#ink-stipple-l)"/>' % d for d in shapes) + '</g>')
add(shade(P + '-m1', soma_d, -6, -6, 'ink-hatch', .7))
add('<path d="%s" stroke="%s" stroke-width=".8" fill="none" stroke-linecap="round"/>' % (spines, INK))
# nucleus, nucleolus, Nissl bodies
add('<ellipse cx="%s" cy="%s" rx="12" ry="9.5" fill="#efe0b8" stroke="%s" stroke-width=".9"/><ellipse cx="%s" cy="%s" rx="12" ry="9.5" fill="url(#ink-stipple)" opacity=".5"/>' % (S[0] - 1, S[1] - 2, INK, S[0] - 1, S[1] - 2))
add('<circle cx="%s" cy="%s" r="2.8" fill="%s"/>' % (S[0] + 2, S[1] - 3, INK))
for k in range(16):
    a = rnd.uniform(0, 6.28); r = rnd.uniform(14, 20)
    add('<ellipse cx="%s" cy="%s" rx="1.8" ry="1" fill="#8a6418" transform="rotate(%s %s %s)"/>' % (
        f(S[0] + r * math.cos(a)), f(S[1] + r * .75 * math.sin(a)), int(rnd.uniform(0, 180)), f(S[0] + r * math.cos(a)), f(S[1] + r * .75 * math.sin(a))))

# axon collaterals with varicosities to targets
TG = [('cortex', 74), ('TMN', 146), ('DR', 216), ('LDT', 286), ('LC', 356)]
BP = (S[0] + 160, S[1] + 2)
TX = 588
var = ''
for name, ty in TG:
    pts = [BP, (BP[0] + 40, BP[1] + (ty - BP[1]) * .2), (BP[0] + 90, ty + (BP[1] - ty) * .15), (TX - 30, ty)]
    add('<path d="%s" fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round"/>' % (cr(pts), INK, cr(pts), OXS))
    dense = resample(bez_pts(pts, per=12), 9)
    for (vx, vy) in dense[6:-1]:
        var += '<ellipse cx="%s" cy="%s" rx="2.8" ry="2.2" fill="%s" stroke="%s" stroke-width=".6"/>' % (f(vx), f(vy), '#e2bd5c', INK)
    # terminal bouton
    var += '<circle cx="%s" cy="%s" r="4.2" fill="#e2bd5c" stroke="%s" stroke-width=".8"/>' % (TX - 28, ty, INK)
    for k in range(4):
        var += '<circle cx="%s" cy="%s" r="1.1" fill="%s"/>' % (f(TX - 22 + rnd.uniform(0, 6)), f(ty + rnd.uniform(-5, 5)), OX)
add(var)


# =============== targets ===============
def cluster(cx, cy, col, n=4, seed=1):
    r = random.Random(seed)
    o = ['<ellipse cx="%s" cy="%s" rx="26" ry="17" fill="%s" fill-opacity=".18" stroke="%s" stroke-width=".7" stroke-dasharray="2 2"/>' % (cx, cy, col, col)]
    for k in range(n):
        x = cx - 14 + k * 9 + r.uniform(-2, 2); y = cy + r.uniform(-7, 7)
        a = r.uniform(-40, 40)
        o.append('<path d="M%s %s l%s %s" stroke="%s" stroke-width="1" />' % (f(x), f(y), f(10 * math.cos(math.radians(a + 90))), f(10 * math.sin(math.radians(a + 90))), INK))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".7" transform="rotate(%s %s %s)"/>' % (
            cr([(x - 4, y + 3), (x, y - 5), (x + 4, y + 3)], True), col, INK, int(a), f(x), f(y)))
    return '\n'.join(o)


tcol = {'TMN': RED, 'DR': RED, 'LDT': RED, 'LC': RED}
for name, ty in TG[1:]:
    add(cluster(TX + 4, ty, '#c86454', seed=hash(name) % 50))
# cortex strip with pyramidal cells
cy = TG[0][1]
add('<path d="M%s %s h96 v40 h-96z" fill="%s"/><path d="M%s %s h96 v40 h-96z" fill="url(#ink-stipple-l)"/>' % (TX - 22, cy - 26, '#efd3c6', TX - 22, cy - 26))
add('<path d="M%s %s q48 -8 96 0" class="ink"/><path d="M%s %s h96" class="ink2" stroke-dasharray="3 2"/>' % (TX - 22, cy - 26, TX - 22, cy + 14))
for k in range(4):
    x = TX - 10 + k * 22; y = cy + 4 - (k % 2) * 6
    add('<path d="M%s %s L%s %s L%s %s Z" fill="#d98a7a" stroke="%s" stroke-width=".7"/><path d="M%s %s V%s M%s %s l-5 5 M%s %s l5 5" stroke="%s" stroke-width=".8"/>' % (
        x - 4, y + 4, x, y - 6, x + 4, y + 4, INK, x, y - 6, cy - 22, x - 3, y + 4, x + 3, y + 4, INK))
TL = [('大腦皮質', 'Cortex', '廣泛提高警覺'), ('結節乳頭核 TMN', 'Tuberomammillary n.', '組織胺'), ('背側縫核 DR', 'Dorsal raphe', '血清素'),
      ('LDT/PPT', 'Pons–midbrain tegmentum', '乙醯膽鹼'), ('藍斑核 LC', 'Locus coeruleus', '正腎上腺素')]
for (name, ty), (zh, en, nt) in zip(TG, TL):
    add('<text x="%s" y="%s" class="lb halo">%s</text>' % (TX + 82 if name == 'cortex' else TX + 36, ty - 6 if name != 'cortex' else ty - 34, zh))
    add('<text x="%s" y="%s" class="le halo">%s</text>' % (TX + 82 if name == 'cortex' else TX + 36, ty + 8 if name != 'cortex' else ty - 21, en))
    add('<text x="%s" y="%s" class="ls halo" style="fill:%s">%s</text>' % (TX + 82 if name == 'cortex' else TX + 36, ty + 21 if name != 'cortex' else ty - 8, TCM, nt))

# =============== inputs (left) ===============
IN = []
# limbic: amygdala almond
icons = []
alm = cr([(-22, 2), (-10, -14), (10, -15), (22, -2), (10, 14), (-12, 14)], True)
icons.append('<path d="%s" fill="#e9a596" stroke="%s" stroke-width="1"/><path d="%s" fill="url(#ink-hatch-l)"/>' % (alm, INK, alm))
icons.append('<circle cx="0" cy="0" r="18" fill="#f6e7b0" stroke="%s" stroke-width="1"/><circle cx="-2" cy="-1" r="14" fill="#fbf3d0" stroke="%s" stroke-width=".6"/><circle cx="-2" cy="-1" r="14" fill="url(#ink-stipple-l)"/><path d="M10 12 q7 -4 5 -12" fill="#c9a457" stroke="%s" stroke-width=".7"/>' % (INK, INK, INK))
st = [(-22, -12), (-12, -18), (-6, -13), (-8, -2), (2, 6), (16, 4), (22, 12), (14, 22), (-6, 22), (-20, 12), (-24, 0)]
icons.append('<path d="M-14 -16 l-3 -9" stroke="%s" stroke-width="5" stroke-linecap="round"/><path d="M-14 -16 l-3 -9" stroke="#e9b4a2" stroke-width="3" stroke-linecap="round"/><path d="%s" fill="#e9b4a2" stroke="%s" stroke-width="1"/><path d="%s" fill="url(#ink-hatch-r)" opacity=".5"/><path d="M-14 0 q8 12 24 14" class="ink2"/>' % (INK, cr(st, True), INK, cr(st, True)))
glu = mol('OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O', 150, 110)
icons.append('<g transform="translate(-40 -30) scale(.54)">%s</g>' % glu)
YB = [46, 138, 236, 336]
for ic, y0 in zip(icons, YB):
    add('<g transform="translate(46 %s)">%s</g>' % (y0, ic))
INL = [
    ('邊緣系統・杏仁核', 'Limbic input', '情緒、恐懼、興奮 → ＋', TCM),
    ('瘦素 leptin（脂肪）', 'Leptin, high when fed', '吃飽時多 → 抑制 −', WEST),
    ('飢餓素 ghrelin（胃）', 'Ghrelin', '空腹時升高 → ＋', TCM),
    ('血糖 glucose', 'Glucose', '血糖低 → ＋；血糖高 → −', TCM),
]
for (zh, en, eff, col), y0 in zip(INL, YB):
    y = y0 + 38
    add('<text x="14" y="%s" class="lb halo">%s</text><text x="14" y="%s" class="le halo">%s</text><text x="14" y="%s" class="ls halo" style="fill:%s;font-weight:600">%s</text>' % (y, zh, y + 13.5, en, y + 27, col, eff))
arr = [((72, YB[0]), (205, 132), 'ag'), ((70, YB[1]), (196, 190), 'tb'), ((74, YB[2]), (196, 240), 'ag'), ((82, YB[3]), (214, 290), 'ag')]
for (a, b, m) in arr:
    col = WEST if m == 'tb' else TCM
    add('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" marker-end="url(#%s-%s)"/>' % (cr([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 8), b]), col, P, m))
# VLPO inhibitory input at top (sleep)
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="4 2.5" marker-end="url(#%s-tb)"/>' % (cr([(250, 30), (270, 80), (286, 176)]), WEST, P))
add('<text x="170" y="22" class="lb halo" style="fill:%s">VLPO（睡眠時）</text><text x="170" y="36" class="ls halo">GABA 抑制 −</text>' % WEST)
# labels for the neuron
add(label('R', 352, 290, 'Orexin 神經元', 'Lateral hypothalamus, 約數萬個', (S[0] + 10, S[1] + 16), stub=6))
add(label('R', 352, 124, '樹突與棘', 'Dendrites with spines', (S[0] + 60, S[1] - 50), stub=6))
add('<text x="%s" y="%s" class="ls halo" style="font-style:italic">軸突 axon</text>' % (S[0] + 70, S[1] - 6))
add('<text x="%s" y="%s" class="ls halo" style="font-style:italic">膨體 varicosities：釋出 orexin</text>' % (BP[0] - 4, 412))
add('<path d="M%s 402 Q%s 380 %s 372" class="ld" marker-end="url(#ink-dot)"/>' % (BP[0] + 50, BP[0] + 60, BP[0] + 76))
add('<text x="352" y="252" class="ls halo">細胞核 nucleus</text><path d="M350 248 L%s %s" class="ld" marker-end="url(#ink-dot)"/>' % (S[0] + 6, S[1] + 2))

# =============== narcolepsy inset ===============
NY = 428
N = ['<rect x="12" y="%s" width="736" height="214" rx="6" fill="#f3ece0" stroke="#bfae8a" stroke-width=".8"/>' % NY,
     '<text x="24" y="%s" class="lt">小插圖：第一型猝睡症 Narcolepsy type 1</text>' % (NY + 22)]


def hypo_disc(cx, cy, n_alive, n_dead, seed):
    r = random.Random(seed)
    o = ['<circle cx="%s" cy="%s" r="40" fill="#f2d0c3"/><circle cx="%s" cy="%s" r="40" fill="url(#ink-stipple-l)"/><circle cx="%s" cy="%s" r="40" class="ink"/>' % (cx, cy, cx, cy, cx, cy)]
    pos = []
    while len(pos) < n_alive + n_dead:
        x, y = cx + r.uniform(-30, 30), cy + r.uniform(-30, 30)
        if math.hypot(x - cx, y - cy) < 31 and all(math.hypot(x - a, y - b) > 11 for a, b in pos):
            pos.append((x, y))
    for i, (x, y) in enumerate(pos):
        a = r.uniform(0, 360)
        if i < n_alive:
            o.append('<path d="M%s %s l%s %s M%s %s l%s %s" stroke="%s" stroke-width=".8"/>' % (f(x), f(y), f(8 * math.cos(math.radians(a))), f(8 * math.sin(math.radians(a))), f(x), f(y), f(-7 * math.cos(math.radians(a + 40))), f(-7 * math.sin(math.radians(a + 40))), INK))
            o.append('<circle cx="%s" cy="%s" r="3.6" fill="#e2bd5c" stroke="%s" stroke-width=".7"/>' % (f(x), f(y), INK))
        else:
            o.append('<circle cx="%s" cy="%s" r="3.6" fill="none" stroke="#8a7a60" stroke-width=".7" stroke-dasharray="1.5 1.2"/>' % (f(x), f(y)))
    return '\n'.join(o)


N.append(hypo_disc(70, NY + 92, 14, 0, 3))
N.append(hypo_disc(170, NY + 92, 2, 12, 4))
N.append('<text x="70" y="%s" text-anchor="middle" class="ls" style="font-weight:600">正常</text>' % (NY + 148))
N.append('<text x="170" y="%s" text-anchor="middle" class="ls" style="font-weight:600">猝睡症：約九成消失</text>' % (NY + 148))
N.append('<path d="M112 %s h14" class="ink" marker-end="url(#ink-arrow)"/>' % (NY + 92))
N.append('<text x="24" y="%s" class="ls">外側下視丘的 orexin 神經元</text><text x="24" y="%s" class="ls">多半被自體免疫破壞</text>' % (NY + 170, NY + 184))

# switch traces
tx0, tw = 250, 190
N.append('<text x="%s" y="%s" class="lb">開關失去穩定器</text>' % (tx0, NY + 48))
for k, (lab, unstable) in enumerate([('正常', False), ('猝睡症', True)]):
    y0 = NY + 66 + k * 54
    x1 = tx0 + 74
    N.append('<text x="%s" y="%s" class="ls" style="font-weight:600">%s</text>' % (tx0, y0 + 17, lab))
    N.append('<path d="M%s %s H%s M%s %s H%s" stroke="#bfae8a" stroke-width=".6" stroke-dasharray="2 2"/>' % (x1, y0, tx0 + tw, x1, y0 + 26, tx0 + tw))
    N.append('<text x="%s" y="%s" class="ls" style="font-size:9.5px" text-anchor="end">醒</text><text x="%s" y="%s" class="ls" style="font-size:9.5px" text-anchor="end">REM</text>' % (x1 - 4, y0 + 3, x1 - 4, y0 + 29))
    if not unstable:
        d = 'M%s %s H%s' % (x1, y0, tx0 + tw)
    else:
        xs = [0, 14, 18, 30, 34, 60, 64, 70, 74, 92, 96, 108]
        d = 'M%s %s' % (x1, y0)
        st = 0
        for x in xs[1:]:
            d += ' H%s V%s' % (x1 + x, y0 + (26 if st == 0 else 0))
            st = 1 - st
        d += ' H%s' % (tx0 + tw)
    N.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (d, OX if not unstable else RED))
N.append('<text x="%s" y="%s" class="ls">REM 片段闖入清醒：猝倒、</text><text x="%s" y="%s" class="ls">睡眠癱瘓、入睡幻覺、白天嗜睡</text>' % (tx0, NY + 180, tx0, NY + 194))

# cataplexy figure (kneeling collapse while laughing), facing left
FX, FY = 560, NY + 200


def T(pts):
    return [(FX + x, FY + y) for x, y in pts]


fig = []
ground = 'M%s %s H%s' % (FX - 90, FY + 1, FX + 150)
fig.append('<path d="%s" stroke="%s" stroke-width="1"/>' % (ground, INK))
fig.append('<path d="%s" stroke="%s" stroke-width=".5" opacity=".6"/>' % (''.join('M%s %s l-6 6 ' % (FX - 86 + k * 10, FY + 1) for k in range(24)), INK))
# far arm (limp, behind torso)
farm = T([(18, -100), (30, -76), (40, -54), (46, -44)])
fig.append('<path d="%s" fill="#6b7f99" stroke="%s" stroke-width="1"/>' % (tapered(farm, 13, 10), INK))
fig.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".9"/>' % (cr(T([(42, -48), (52, -44), (56, -34), (50, -28), (44, -34)]), True), FLESH, INK))
# trousers: thigh + shin (kneeling)
tr = T([(-8, -1), (-12, -14), (-4, -34), (10, -52), (24, -66), (44, -70), (60, -60), (62, -44), (58, -28), (68, -18), (82, -14), (88, -6), (86, 0)])
trd = cr(tr, True, k=.8)
fig.append('<path d="%s" fill="#4a5568"/><path d="%s" fill="url(#ink-hatch)" opacity=".55"/>' % (trd, trd))
fig.append('<path d="%s" fill="none" stroke="#2f3846" stroke-width=".8" opacity=".9"/>' % cr(T([(10, -40), (26, -40), (44, -30), (58, -24)])))
fig.append('<path d="%s" fill="none" stroke="#2f3846" stroke-width=".8"/>' % cr(T([(-6, -18), (2, -24), (8, -20)])))
fig.append('<path d="%s" class="ink"/>' % trd)
# shoe (sole up, toes on the floor)
sh = T([(80, -16), (94, -16), (110, -8), (114, -1), (84, 0)])
fig.append('<path d="%s" fill="#3a2f28" stroke="%s" stroke-width="1"/><path d="%s" stroke="#7a6a5a" stroke-width=".8" fill="none"/>' % (cr(sh, True, k=.7), INK, cr(T([(86, -13), (104, -9)]))))
# torso (shirt), slumped forward
to = T([(22, -64), (46, -70), (56, -86), (50, -110), (32, -128), (8, -134), (-12, -124), (-20, -104), (-8, -86), (6, -72)])
tod = cr(to, True)
fig.append('<path d="%s" fill="#c9d6e3"/><path d="%s" fill="url(#ink-hatch-l)"/>' % (tod, tod))
fig.append(shade(P + '-m2', tod, -8, 8, 'ink-hatch', .7))
fig.append('<path d="%s" fill="none" stroke="%s" stroke-width=".7"/>' % (cr(T([(30, -122), (36, -100), (42, -80)])), INK))  # fold
fig.append('<path d="%s" fill="none" stroke="%s" stroke-width=".7"/>' % (cr(T([(-6, -96), (8, -90), (20, -80)])), INK))
fig.append('<path d="%s" class="ink"/>' % tod)
fig.append('<path d="%s" fill="none" stroke="%s" stroke-width="1"/>' % (cr(T([(20, -66), (34, -70), (48, -72)])), INK))  # belt line
# neck + head hanging forward/down
fig.append('<path d="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (cr(T([(-8, -126), (-18, -132), (-26, -124), (-16, -114)]), True), FLESH, INK))
head = T([(-22, -128), (-30, -140), (-44, -142), (-56, -134), (-62, -120), (-64, -110), (-58, -100), (-50, -96), (-40, -100), (-30, -110)])
hd = cr(head, True)
fig.append('<path d="%s" fill="%s"/>' % (hd, FLESH))
# hair
hair = T([(-22, -128), (-28, -142), (-44, -146), (-58, -138), (-63, -126), (-56, -126), (-48, -134), (-36, -132), (-28, -122)])
fig.append('<path d="%s" fill="#5a4636"/><path d="%s" fill="url(#ink-hatch-d)" opacity=".5"/>' % (cr(hair, True), cr(hair, True)))
fig.append('<path d="%s" class="ink"/>' % hd)
# ear
fig.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".8"/>' % (cr(T([(-34, -124), (-28, -122), (-28, -114), (-34, -114)]), True), FLESH_D, INK))
# laughing face: closed eyes (arcs), open mouth, cheek line
fig.append('<path d="%s" fill="none" stroke="%s" stroke-width="1"/>' % (cr(T([(-55, -120), (-52, -117), (-48, -119)])), INK))
fig.append('<path d="%s" fill="#7a2f24" stroke="%s" stroke-width=".9"/>' % (cr(T([(-60, -106), (-54, -104), (-52, -100), (-58, -99), (-62, -102)]), True), INK))
fig.append('<path d="%s" fill="none" stroke="%s" stroke-width=".7"/>' % (cr(T([(-50, -112), (-46, -106), (-48, -100)])), INK))
# near arm: sleeve to wrist, hand flat on floor
arm = T([(-6, -122), (-18, -100), (-26, -74), (-30, -48), (-34, -22)])
fig.append('<path d="%s" fill="#b9c8d8" stroke="%s" stroke-width="1"/>' % (tapered(arm, 15, 11), INK))
fig.append('<path d="%s" fill="none" stroke="%s" stroke-width=".7"/>' % (cr(T([(-22, -78), (-28, -70), (-26, -62)])), INK))
handp = T([(-40, -24), (-28, -24), (-24, -12), (-22, -2), (-30, 0), (-40, 0), (-50, -1), (-52, -4), (-46, -8), (-44, -16)])
fig.append('<path d="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (cr(handp, True, k=.8), FLESH, INK))
fig.append('<path d="%s" fill="none" stroke="%s" stroke-width=".6"/>' % (' '.join(cr(T([(-46 + 5 * k, -6), (-48 + 5 * k, -1)])) for k in range(4)), INK))
# motion / sudden-collapse marks and laughter
for k in range(3):
    fig.append('<path d="%s" fill="none" stroke="%s" stroke-width=".9" opacity=".7" marker-end="url(#ink-arrow)"/>' % (cr(T([(4 + k * 18, -176), (6 + k * 18, -158), (4 + k * 18, -146)])), INK))
fig.append('<text x="%s" y="%s" class="ls" style="font-style:italic;fill:%s">哈哈哈…</text>' % (FX - 104, FY - 138, TCM))
N.append('\n'.join(fig))
N.append('<text x="%s" y="%s" class="lb">猝倒 cataplexy</text>' % (FX + 66, NY + 48))
N.append('<text x="%s" y="%s" class="ls">大笑或驚喜時，</text><text x="%s" y="%s" class="ls">全身肌肉突然無力，</text><text x="%s" y="%s" class="ls">人是清醒的。</text>' % (
    FX + 66, NY + 66, FX + 66, NY + 80, FX + 66, NY + 94))

body = inline_classes('\n'.join(O) + '\n' + '\n'.join(N))
cap = ('<b>圖 1-E　Orexin 神經元：開關上的穩定器。</b>外側下視丘的 orexin 神經元只有數萬個，軸突卻投射到藍斑核、結節乳頭核、背側縫核、LDT/PPT 與大腦皮質，沿途膨體釋出 orexin，把清醒中樞穩定在「開」。'
       '它同時收到情緒（邊緣系統）與代謝訊號：空腹時 leptin 低、ghrelin 高、血糖低都會推它一把，所以餓、怕、興奮時特別難睡。'
       '下方小圖：第一型猝睡症的人約九成 orexin 神經元消失，開關不穩，REM 的肌肉無力會闖入清醒，大笑時突然腿軟跌坐（猝倒）。示意圖，神經元形態與數量比例為教學簡化。')
write(P, 'Plate 1·E', 'Orexin 神經元：開關上的穩定器', 'The orexin neuron — stabiliser of the switch', 652, body,
      'orexin 神經元的形態、輸入訊號與投射目標，以及猝睡症時神經元消失與猝倒的示意', cap, defs=''.join(D))
