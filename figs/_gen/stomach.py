import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from common import *
from head import head

PID = 'pl-stomach'
RED = '#a8412c'

def tube(center, w0, w1=None):
    w1 = w0 if w1 is None else w1
    n = len(center)
    L, R = [], []
    for i, (x, y) in enumerate(center):
        a = center[max(i - 1, 0)]; b = center[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
    return L, R

o = ['''<defs>
<radialGradient id="pl-stomach-g" cx=".55" cy=".35" r=".8"><stop offset="0" stop-color="#f6d6c8"/><stop offset=".7" stop-color="#e3a998"/><stop offset="1" stop-color="#c47f6c"/></radialGradient>
<radialGradient id="pl-stomach-muc" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#f0b2a4"/><stop offset="1" stop-color="#c9685a"/></radialGradient>
<linearGradient id="pl-stomach-acid" x1="0" x2="1"><stop offset="0" stop-color="#d9d36a"/><stop offset="1" stop-color="#b9b24a"/></linearGradient>
</defs>''']

# ---------- stomach outline ----------
oes_c = [(214, 22), (217, 60), (222, 100), (229, 130), (233, 150)]
oL, oR = tube(oes_c, 24, 26)   # oL = viewer-right wall? check sign
# make sure 'right' wall has larger x
if oL[0][0] < oR[0][0]:
    oL, oR = oR, oL
greater = [(262, 118), (292, 103), (325, 111), (347, 140), (357, 186), (353, 240), (337, 295), (307, 344), (263, 379), (213, 393), (172, 387), (143, 371), (126, 359), (114, 354)]
lesser = [(118, 333), (140, 324), (166, 317), (193, 317), (216, 305), (230, 279), (232, 238), (227, 190), (222, 160)]
outline_pts = oL + [(246, 152), (250, 140)] + greater + lesser + list(reversed(oR))[:-0 or None]
st = smooth(oL[:-1] + [(247, 150), (252, 134)] + greater + lesser + [oR[-1]] + list(reversed(oR[:-1])), close=True, t=0.45)
# duodenum
du_c = [(118, 345), (96, 340), (74, 348), (64, 378), (63, 414), (72, 440), (98, 452), (136, 456)]
dL, dR = tube(du_c, 26, 24)
du = smooth(dL + list(reversed(dR)), close=True)

S = []
S.append('<clipPath id="pl-stomach-clip"><path d="%s"/></clipPath>' % st)
# diaphragm (behind)
diaU = [(132, 112), (180, 92), (240, 80), (300, 72), (360, 74), (400, 86)]
diaD = [(400, 96), (360, 84), (300, 82), (240, 90), (180, 102), (132, 122)]
S.append('<path d="%s" fill="#d79a86"/>' % smooth(diaU + diaD, close=True))
S.append('<path d="%s" fill="url(#ink-hatch-r)"/>' % smooth(diaU + diaD, close=True))
S.append('<path d="%s" class="ink"/>' % smooth(diaU + diaD, close=True))
# duodenum
S.append('<path d="%s" fill="url(#pl-stomach-g)"/><path d="%s" fill="url(#ink-hatch-l)"/><path d="%s" class="ink3" stroke-width="1.4"/>' % (du, du, du))
for k in range(1, 7):
    a, b = dL[k], dR[k]
    S.append('<path d="M%s %s Q%s %s %s %s" class="ink2" stroke-opacity=".45"/>' % (f(a[0]), f(a[1]), f((a[0] + b[0]) / 2 + 3), f((a[1] + b[1]) / 2 + 3), f(b[0]), f(b[1])))
# stomach body
S.append('<path d="%s" fill="url(#pl-stomach-g)"/>' % st)
# surface muscle-fibre striations: scaled copies of greater curvature
g2 = greater[:-2]
for k in range(1, 9):
    s_ = 1 - k * 0.085
    cx0, cy0 = 205, 250
    P = [(cx0 + (x - cx0) * s_, cy0 + (y - cy0) * s_) for x, y in g2]
    S.append('<path d="%s" class="ink2" stroke-width=".4" stroke-opacity=".35" clip-path="url(#pl-stomach-clip)"/>' % smooth(P))
# oblique fibres near cardia
for k in range(6):
    S.append('<path d="M%d %d q30 20 40 70" class="ink2" stroke-width=".4" stroke-opacity=".35" clip-path="url(#pl-stomach-clip)"/>' % (238 + k * 6, 150 - k * 4))
# shade lower-right
S.append('<path d="M250 420 L380 220 L380 420Z" fill="url(#ink-hatch)" clip-path="url(#pl-stomach-clip)" opacity=".8"/>')
S.append('<path d="M150 400 L250 330 L330 400Z" fill="url(#ink-hatch-l)" clip-path="url(#pl-stomach-clip)"/>')
# oesophagus longitudinal lines
for k in (-6, 0, 6):
    S.append('<path d="%s" class="ink2" stroke-opacity=".5"/>' % smooth([(x + k * (1 - i * 0.05), y) for i, (x, y) in enumerate(oes_c[:-1])]))
# pyloric sphincter ring
S.append('<path d="M118 333 Q109 344 114 355" stroke="#2a2018" stroke-width="5" fill="none"/><path d="M118 333 Q109 344 114 355" stroke="#c47f6c" stroke-width="3" fill="none"/>')
S.append('<path d="%s" class="ink3"/>' % st)
# top cut end of oesophagus
S.append('<ellipse cx="%s" cy="%s" rx="12.5" ry="4" fill="#c9685a" stroke="#2a2018" stroke-width="1"/>' % (f((oL[0][0] + oR[0][0]) / 2), f((oL[0][1] + oR[0][1]) / 2)))
S.append('<ellipse cx="%s" cy="%s" rx="5" ry="1.6" fill="#7a2f22"/>' % (f((oL[0][0] + oR[0][0]) / 2), f((oL[0][1] + oR[0][1]) / 2)))
# LES cut-away window on oesophagus
S.append('<path d="M222 118 q8 -3 16 0 v26 q-8 3 -16 0z" fill="#f0b2a4" stroke="#2a2018" stroke-width=".8"/>')
for k in range(7):
    S.append('<path d="M222 %d q8 -2 16 0" stroke="#a8412c" stroke-width="1.6" fill="none"/>' % (121 + k * 3.4))
# vessels: gastro-epiploic arcade along greater curvature; left/right gastric along lesser
gea = [(126, 372), (168, 398), (215, 404), (266, 390), (314, 354), (345, 300), (362, 240), (365, 190)]
S.append('<path d="%s" fill="none" stroke="#2a2018" stroke-width="3.4"/><path d="%s" fill="none" stroke="#b5473a" stroke-width="2"/>' % (smooth(gea), smooth(gea)))
for (x, y), (x2, y2) in zip(gea[1:-1], greater[9:1:-1]):
    pass
for i in range(1, len(gea) - 1):
    x, y = gea[i]
    # branch toward stomach centre
    tx, ty = 240, 260
    d = math.hypot(tx - x, ty - y)
    ux, uy = (tx - x) / d, (ty - y) / d
    S.append('<path d="M%s %s q%s %s %s %s" fill="none" stroke="#b5473a" stroke-width="1" />' % (f(x), f(y), f(ux * 10 + uy * 4), f(uy * 10 - ux * 4), f(ux * 22), f(uy * 22)))
lga = [(225, 168), (224, 200), (227, 240), (224, 280), (208, 304), (180, 312), (148, 318), (124, 326)]
S.append('<path d="%s" fill="none" stroke="#2a2018" stroke-width="3"/><path d="%s" fill="none" stroke="#b5473a" stroke-width="1.7"/>' % (smooth(lga), smooth(lga)))
for i in range(1, len(lga) - 1, 1):
    x, y = lga[i]
    S.append('<path d="M%s %s l%s %s" stroke="#b5473a" stroke-width=".9"/>' % (f(x), f(y), f(10 if i < 4 else 4), f(4 if i < 4 else 12)))

# cut-away window with rugae
wc = (292, 255)
def ell(cx, cy, rx, ry, ang, n=36):
    a = math.radians(ang)
    return [(cx + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a), cy + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a))
            for t in [2 * math.pi * k / n for k in range(n)]]
wobble = random.Random(3)
W0 = [(x + wobble.uniform(-2, 2), y + wobble.uniform(-2, 2)) for x, y in ell(wc[0], wc[1], 44, 76, -28)]
def inset(P, k):
    cx_ = sum(p[0] for p in P) / len(P); cy_ = sum(p[1] for p in P) / len(P)
    return [(cx_ + (x - cx_) * k, cy_ + (y - cy_) * k) for x, y in P]
S.append('<path d="%s" fill="#f7efe2" stroke="#2a2018" stroke-width="1.1"/>' % smooth(W0, close=True))            # serosa cut edge
S.append('<path d="%s" fill="#c9705a"/>' % smooth(inset(W0, .93), close=True))                                   # muscularis
S.append('<path d="%s" fill="url(#ink-hatch-h)"/>' % smooth(inset(W0, .93), close=True))
S.append('<path d="%s" fill="#f3dccb" stroke="#2a2018" stroke-width=".5"/>' % smooth(inset(W0, .84), close=True))  # submucosa
W3 = inset(W0, .79)
S.append('<clipPath id="pl-stomach-w"><path d="%s"/></clipPath>' % smooth(W3, close=True))
S.append('<path d="%s" fill="url(#pl-stomach-muc)" stroke="#2a2018" stroke-width=".7"/>' % smooth(W3, close=True))
# rugae: wavy longitudinal folds running along the long axis (-28deg from vertical)
rg = random.Random(8)
a = math.radians(-28)
for k in range(-6, 7):
    pts_ = []
    for j in range(-9, 10):
        u = k * 7 + math.sin(j * 0.9 + k) * 2.4 + rg.uniform(-.8, .8)
        v = j * 9
        pts_.append((wc[0] + u * math.cos(a) - v * math.sin(a), wc[1] + u * math.sin(a) + v * math.cos(a)))
    d = smooth(pts_)
    S.append('<path d="%s" fill="none" stroke="#f8d4c8" stroke-width="3" clip-path="url(#pl-stomach-w)"/>' % d)
    S.append('<path d="%s" fill="none" stroke="#7a2f22" stroke-width=".7" clip-path="url(#pl-stomach-w)"/>' % d)
# inner shadow (depth) at upper rim
S.append('<path d="%s" fill="none" stroke="#5a1f15" stroke-opacity=".35" stroke-width="7" clip-path="url(#pl-stomach-w)" transform="translate(3 4)"/>' % smooth(W3, close=True))

body = [o[0], '<g filter="url(#ink-rough)">' + '\n'.join(S) + '</g>']

# ---------- stomach labels ----------
L = []
def lab(x, y, zh, en, tx, ty, side='L'):
    out = label(x, y, zh, None) + label(x, y + 14, en, None, cls='le halo')
    if side == 'L':
        out += leader(x + 4 + 13 * len(zh), y - 4, tx, ty)
    else:
        out += leader(x - 4, y - 4, tx, ty)
    return out
L.append(lab(14, 40, '食道', 'Oesophagus', 207, 50))
L.append(lab(14, 92, '橫膈', 'Diaphragm', 160, 106))
L.append(lab(14, 144, '下食道括約肌', 'Lower oesophageal sphincter (LES)', 223, 131))
L.append(lab(14, 210, '賁門', 'Cardia', 228, 166))
L.append(lab(14, 262, '小彎', 'Lesser curvature', 230, 255))
L.append(label(14, 314, '幽門', None) + label(14, 328, 'Pylorus', None, cls='le halo') + leader(60, 324, 112, 346))
L.append(lab(372, 44, '胃底', 'Fundus', 312, 118, 'R'))
L.append(lab(372, 100, 'His 角', 'Angle of His', 251, 140, 'R'))
L.append(lab(372, 150, '胃體', 'Body', 348, 190, 'R'))
L.append(lab(372, 200, '黏膜皺襞', 'Rugae', 300, 240, 'R'))
L.append(lab(372, 250, '黏膜下層', 'Submucosa', 323, 300, 'R'))
L.append(lab(372, 300, '肌層', 'Muscularis', 333, 314, 'R'))
L.append(lab(372, 350, '大彎', 'Greater curvature', 330, 330, 'R'))
L.append(lab(372, 400, '胃網膜動脈', 'Gastro-epiploic a.', 300, 368, 'R'))
L.append(label(200, 432, '胃竇', None) + label(200, 446, 'Antrum', None, cls='le halo') + leader(214, 417, 184, 366))
L.append(label(14, 498, '十二指腸', None) + label(14, 512, 'Duodenum', None, cls='le halo') + leader(50, 486, 66, 452))
body.append('\n'.join(L))

# ---------- wall layer block (bottom-left) ----------
Bk = ['<g filter="url(#ink-rough)">']
bx, by = 160, 496
layers = [('#f7efe2', '漿膜', 'Serosa', 6, None), ('#d9826a', '縱走肌', 'Longitudinal', 12, 'h'),
          ('#c9705a', '環走肌', 'Circular', 14, 'v'), ('#b8604c', '斜走肌', 'Oblique (胃特有)', 10, 'd'),
          ('#f3dccb', '黏膜下層', 'Submucosa', 10, None), ('#e9a093', '黏膜', 'Mucosa', 14, 'pits')]
y = by
for i, (col, zh, en, h, pat) in enumerate(layers):
    off = i * 14   # stepped peel: each deeper layer extends further right
    x0, x1 = bx, bx + 84 + i * 10
    Bk.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#2a2018" stroke-width=".6"/>' % (x0, y, x1 - x0, h, col))
    if pat == 'h':
        for yy in range(y + 3, y + h, 3):
            Bk.append('<path d="M%d %d H%d" class="ink2" stroke-width=".35"/>' % (x0, yy, x1))
    elif pat == 'v':
        for xx in range(x0 + 2, x1, 3):
            Bk.append('<path d="M%d %d V%d" class="ink2" stroke-width=".35"/>' % (xx, y, y + h))
    elif pat == 'd':
        for xx in range(x0, x1, 4):
            Bk.append('<path d="M%d %d l%d %d" class="ink2" stroke-width=".35"/>' % (xx, y + h, min(h, x1 - xx), -min(h, x1 - xx)))
    elif pat == 'pits':
        for xx in range(x0 + 4, x1 - 2, 7):
            Bk.append('<path d="M%d %d v-8 q2 -3 4 0 v8" fill="#c9685a" stroke="#2a2018" stroke-width=".4"/>' % (xx, y + h))
    Bk.append('<path d="M%d %d h%d" class="ld"/>' % (x1 + 2, y + h / 2, 236 + 6 * 14 - x1 + 4))
    Bk[-1] = '<path d="M%d %s H%d" class="ld"/>' % (x1 + 2, f(y + h / 2), 342)
    y += h
Bk.append('</g>')
y = by
for i, (col, zh, en, h, pat) in enumerate(layers):
    pass
ys = [by + 3, by + 14, by + 31, by + 46, by + 58, by + 72]
yy = 500
for i, (col, zh, en, h, pat) in enumerate(layers):
    Bk.append('<text x="318" y="%d" class="ls halo">%s <tspan class="le">%s</tspan></text>' % (yy + 14 * i + 2, zh, en))
# fix leaders to text rows
Bk2 = []
y = by
for i, (col, zh, en, h, pat) in enumerate(layers):
    Bk2.append('<path d="M%d %s L%d %s L314 %d" class="ld"/>' % (bx + 84 + i * 10 + 2, f(y + h / 2), 300, f(y + h / 2), yy + 14 * i - 2))
    y += h
Bk = [b for b in Bk if 'class="ld"' not in b] + Bk2
Bk.append('<text x="160" y="488" class="lb">胃壁分層 <tspan class="le">Gastric wall layers</tspan></text>')
Bk.append('<text x="160" y="590" class="ls">胃多一層斜走肌，負責攪拌；</text><text x="160" y="604" class="ls">幽門、LES 都是環走肌增厚形成的括約肌。</text>')
body.append('\n'.join(Bk))

# ---------- right column: lying flat vs orthopnea ----------
R = ['<path d="M478 20 V 604" class="panel"/>']
# panel A header
R.append('<text x="490" y="36" class="lb">A　躺不平：逆流 <tspan class="le">supine reflux</tspan></text>')
# bed A
R.append('<g filter="url(#ink-rough)">')
R.append('<rect x="496" y="226" width="252" height="22" rx="3" fill="#efe6d2" stroke="#2a2018" stroke-width="1.1"/>')
R.append('<rect x="490" y="248" width="264" height="8" fill="#8a6a3a" stroke="#2a2018" stroke-width="1"/>')
R.append('<path d="M490 256 v18 M754 256 v18" stroke="#2a2018" stroke-width="3"/>')
R.append('<path d="M500 226 q-2 -18 8 -20 q30 -4 56 0 q8 4 4 20z" fill="#f7f1e2" stroke="#2a2018" stroke-width="1"/>')
R.append('<path d="M510 214 q24 -3 48 0" class="ink2" stroke-opacity=".6"/>')
R.append(head(522, 196, 0.62, -90, eyes='open'))
# blanket over supine body
blA = [(556, 226), (560, 204), (576, 190), (610, 186), (652, 192), (690, 198), (716, 196), (730, 186), (742, 192), (746, 226)]
R.append('<path d="%s" fill="#cfdcef" stroke="#2a2018" stroke-width="1.2"/>' % smooth(blA, close=True))
R.append('<path d="%s" fill="url(#ink-hatch-l)"/>' % smooth(blA, close=True))
for k, (x, y) in enumerate([(590, 196), (630, 194), (668, 200), (700, 204)]):
    R.append('<path d="M%d %d q6 12 2 24" class="ink2"/>' % (x, y))
R.append('<path d="M560 206 q10 -8 22 -8" class="ink" stroke-width="1"/>')
R.append('</g>')
# inset magnifier: flat stomach with acid rising
ix, iy = 628, 104
R.append('<circle cx="%d" cy="%d" r="58" fill="#fbf6ea" stroke="#2a2018" stroke-width="1.1"/>' % (ix, iy))
R.append('<path d="M%d %d L586 186 M%d %d L656 186" class="ld" stroke-dasharray="3 2"/>' % (ix - 40, iy + 42, ix + 36, iy + 45))
R.append('<clipPath id="pl-stomach-ic"><circle cx="%d" cy="%d" r="57"/></clipPath>' % (ix, iy))
I = ['<g clip-path="url(#pl-stomach-ic)" filter="url(#ink-rough)">']
# horizontal oesophagus (to the left = toward mouth) and stomach lying
I.append('<path d="M560 98 L612 98 L612 116 L560 116z" fill="#f0c4b8" stroke="#2a2018" stroke-width="1"/>')
stA = smooth([(610, 96), (626, 80), (656, 76), (684, 86), (690, 106), (680, 128), (650, 140), (620, 134), (612, 118)], close=True)
I.append('<path d="%s" fill="url(#pl-stomach-g)" stroke="#2a2018" stroke-width="1.2"/>' % stA)
# acid layer at the bottom (gravity = down in the inset, patient supine => posterior)
I.append('<clipPath id="pl-stomach-ac"><path d="%s"/></clipPath>' % stA)
I.append('<rect x="600" y="112" width="100" height="40" fill="url(#pl-stomach-acid)" clip-path="url(#pl-stomach-ac)" opacity=".9"/>')
I.append('<path d="M612 109 L566 109 L566 116 L612 116z" fill="url(#pl-stomach-acid)"/>')
for k in range(3):
    I.append('<circle cx="%d" cy="%d" r="1.6" fill="#f7f3c8" stroke="#2a2018" stroke-width=".3"/>' % (640 + k * 14, 124 + (k % 2) * 5))
I.append('<path d="M604 106 L572 106" stroke="%s" stroke-width="2" marker-end="url(#ink-arrow-red)"/>' % RED)
I.append('</g>')
R.append(''.join(I))
R.append('<text x="628" y="176" text-anchor="middle" class="ls halo">胃酸沿食道往上流</text>')
R.append(label(498, 64, '胃酸', None, cls='ls halo') + label(498, 78, 'acid', None, cls='le halo') + leader(526, 74, 600, 124))
R.append(label(498, 120, 'LES 鬆', None, cls='ls halo') + leader(538, 116, 610, 107))
R.append('<text x="500" y="280" class="ls">胸口灼熱、酸水、夜咳；平躺或飯後更明顯</text>')
R.append('<text x="500" y="295" class="ls" style="fill:#a8412c">→ 胃食道逆流 GERD：先處理逆流</text>')
R.append('<path d="M484 312 H754" class="panel"/>')

# panel B: orthopnea, propped up sitting
R.append('<text x="490" y="334" class="lb">B　躺不平：端坐呼吸 <tspan class="le">orthopnea</tspan></text>')
R.append('<g filter="url(#ink-rough)">')
R.append('<rect x="496" y="530" width="252" height="22" rx="3" fill="#efe6d2" stroke="#2a2018" stroke-width="1.1"/>')
R.append('<rect x="490" y="552" width="264" height="8" fill="#8a6a3a" stroke="#2a2018" stroke-width="1"/>')
R.append('<path d="M490 560 v18 M754 560 v18 M494 552 V400" stroke="#2a2018" stroke-width="3"/>')
# stacked pillows behind back
for k, (x, y, w, h, r) in enumerate([(500, 500, 70, 28, -8), (502, 466, 64, 30, -18), (506, 432, 56, 30, -28)]):
    R.append('<g transform="rotate(%d %d %d)"><rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="#f7f1e2" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M%d %d q%d -4 %d 0" class="ink2" stroke-opacity=".6"/></g>' % (r, x + w / 2, y + h / 2, x, y, w, h, x + 8, y + h / 2, w / 2, w - 16))
# torso (pyjama)
torso = [(560, 452), (574, 444), (592, 446), (606, 456), (612, 490), (614, 530), (556, 530), (552, 490)]
R.append('<path d="%s" fill="#e6d3e8" stroke="#2a2018" stroke-width="1.2"/>' % smooth(torso, close=True))
R.append('<path d="%s" fill="url(#ink-hatch-l)"/>' % smooth([(552, 470), (566, 462), (568, 530), (556, 530)], close=True))
for x in (574, 588, 600):
    R.append('<path d="M%d 470 q-3 30 0 58" class="ink2" stroke-opacity=".6"/>' % x)
# legs under blanket
blB = [(600, 530), (604, 506), (630, 500), (676, 498), (700, 490), (714, 482), (734, 488), (746, 530)]
R.append('<path d="%s" fill="#cfdcef" stroke="#2a2018" stroke-width="1.2"/>' % smooth(blB, close=True))
R.append('<path d="%s" fill="url(#ink-hatch-l)"/>' % smooth(blB, close=True))
for x in (640, 672, 704):
    R.append('<path d="M%d 502 q8 12 2 26" class="ink2"/>' % x)
R.append('</g>')
R.append(head(566, 386, 0.78, 6, eyes='open'))
# arm: upper arm down, forearm across chest, hand on sternum
R.append('<g filter="url(#ink-rough)"><path d="M600 458 q12 20 10 44 q-2 6 -8 4 q-22 -8 -30 -20 q2 -6 8 -4 q12 10 20 14 q0 -18 -10 -32z" fill="#e6d3e8" stroke="#2a2018" stroke-width="1.1"/>')
R.append('<path d="M580 478 q-6 -2 -12 2 q-4 4 -2 8 q4 4 12 2 q6 -4 8 -8z" fill="#f3d9c6" stroke="#2a2018" stroke-width=".9"/>')
R.append('<path d="M570 482 l-6 -1 M570 485 l-6 0 M571 488 l-6 1" class="ink2" stroke-width=".4"/></g>')
# breath marks
for k in range(3):
    R.append('<path d="M%d %d q6 -4 12 0" fill="none" stroke="#2c5d9c" stroke-width="1.2"/>' % (594 + k * 7, 418 + k * 5 - 8))
R.append(label(660, 380, '張口喘', None, cls='ls halo') + label(660, 394, 'breathless', None, cls='le halo') + leader(656, 386, 616, 412))
R.append(label(660, 430, '坐起才緩', None, cls='ls halo') + label(660, 444, 'relieved upright', None, cls='le halo') + leader(656, 436, 604, 470))
R.append(label(498, 384, '多個枕頭', None, cls='ls halo') + label(498, 398, 'pillows', None, cls='le halo') + leader(520, 404, 520, 440))
R.append('<text x="500" y="580" class="ls">平躺就喘、要墊高或坐起才能呼吸</text>')
R.append('<text x="500" y="595" class="ls" style="fill:#a8412c">→ 心衰竭、氣喘、COPD：先轉內科排除</text>')
body.append('\n'.join(R))

cap = ('<b>圖 9-C　「臥不安」可能是躺不平。</b>左：胃的前面觀，依 Gray 解剖圖譜重繪並簡化——食道穿過橫膈，在賁門接胃；胃底在賁門左上方，His 角與下食道括約肌（LES）是防逆流的閥門；前壁開窗可見黏膜皺襞與分層胃壁，胃比腸多一層斜走肌。'
       '右：〈逆調論〉的「不得臥」原指不能平躺——A 平躺時胃酸越過鬆弛的 LES 逆流；B 端坐呼吸是心衰竭或氣喘的警訊。問診先分清「睡不著」還是「躺不平」，後者要先排除內科問題。')
open('/home/user/Insomnia/figs/pl-stomach.html', 'w').write(figure(PID, 'Plate 9·C', '胃不和則臥不安：睡不著，還是躺不平？', 'The stomach, reflux and orthopnoea', 610,
                                                          '胃的解剖（食道、下食道括約肌、賁門、胃底、胃體、大小彎、胃竇、幽門、十二指腸、黏膜皺襞與胃壁分層），以及平躺逆流與端坐呼吸兩種躺不平的情形', '\n'.join(body), cap))
