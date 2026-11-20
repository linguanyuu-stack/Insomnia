import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from common import *
from body import outline, details, hair, pt, right_half

PID = 'pl-weiqi'
S = 0.8
TOP = 92
CXD, CXN = 194, 566
RED = '#a8412c'; GOLD = '#c9962e'; BLUE = '#2c5d9c'
o = []
o.append('''<defs>
<radialGradient id="pl-weiqi-skin" cx=".45" cy=".3" r=".9"><stop offset="0" stop-color="#fbe8da"/><stop offset="1" stop-color="#e2b89c"/></radialGradient>
<radialGradient id="pl-weiqi-skinn" cx=".45" cy=".3" r=".9"><stop offset="0" stop-color="#f3e6dc"/><stop offset="1" stop-color="#cdb4a6"/></radialGradient>
<linearGradient id="pl-weiqi-night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9deeb"/><stop offset="1" stop-color="#eef0f3"/></linearGradient>
<linearGradient id="pl-weiqi-day" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbeec9"/><stop offset="1" stop-color="#fbf6ea"/></linearGradient>
</defs>''')

def P(cx, x, y):
    return pt(cx, TOP, S, x, y)

def panel(x, y, w, h, fill):
    return ('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#2a2018" stroke-width="1.4"/>'
            '<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#2a2018" stroke-width=".5"/>') % (x, y, w, h, fill, x + 4, y + 4, w - 8, h - 8)

def cartouche(x, y, w, big, small):
    return ('<rect x="%d" y="%d" width="%d" height="30" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
            '<rect x="%d" y="%d" width="%d" height="26" fill="none" stroke="#2a2018" stroke-width=".4"/>'
            '<text x="%d" y="%d" class="lt">%s</text><text x="%d" y="%d" class="ls">%s</text>') % (
        x, y, w, x + 2, y + 2, w - 4, x + 10, y + 21, big, x + 40, y + 20, small)

def body_fig(cx, eyes, skin):
    d = outline(cx, TOP, S)
    out = ['<path d="%s" fill="url(#%s)"/>' % (d, skin)]
    # shading hatch on viewer-right side of body (light from upper left)
    out.append('<clipPath id="pl-weiqi-c%s"><rect x="%s" y="0" width="200" height="600"/></clipPath>' % (cx, f(cx + 14 * S)))
    out.append('<path d="%s" fill="url(#ink-hatch-l)" clip-path="url(#pl-weiqi-c%s)"/>' % (d, cx))
    out.append(details(cx, TOP, S, eyes=eyes))
    out.append(hair(cx, TOP, S))
    out.append('<path d="%s" class="ink3" stroke-width="1.4"/>' % d)
    return '\n'.join(out)

def qiao(cx, kind, bold):
    if kind == 'yang':   # lateral, viewer's left leg, to inner canthus
        L = [(-27, 446), (-31, 425), (-36, 380), (-40, 310), (-44, 255), (-38, 200), (-38, 150), (-46, 100), (-30, 80), (-14, 64), (-8, 50), (-5, 29)]
        col = '#b8732a'
    else:                # medial, viewer's right leg
        L = [(11, 446), (14, 420), (15, 380), (15, 340), (12, 290), (6, 250), (8, 220), (11, 180), (12, 130), (18, 86), (11, 66), (12, 46), (5, 29)]
        col = '#2f8a7e'
    pts_ = [P(cx, x, y) for x, y in L]
    w = 2.6 if bold else 1.4
    op = 1 if bold else .6
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-dasharray=".1 %s" stroke-linecap="round" stroke-opacity="%s"/>' % (smooth(pts_), col, w, 4.2 if bold else 3.4, op)

body = [o[0]]
# ===== panels =====
body.append(panel(12, 12, 364, 490, 'url(#pl-weiqi-day)'))
body.append(panel(384, 12, 364, 490, 'url(#pl-weiqi-night)'))
body.append(cartouche(24, 24, 170, '晝', '衛氣行於陽 · 目張'))
body.append(cartouche(396, 24, 170, '夜', '衛氣入於陰 · 目瞑'))
# sun
sx, sy = 340, 52
rays = ''.join('<path d="M%s %s L%s %s" stroke="%s" stroke-width="1.1"/>' % (f(sx + 17 * math.cos(a)), f(sy + 17 * math.sin(a)), f(sx + 25 * math.cos(a)), f(sy + 25 * math.sin(a)), GOLD)
               for a in [k * math.pi / 8 for k in range(16)])
body.append('<g>%s<circle cx="%d" cy="%d" r="13" fill="#f2cf6a" stroke="#2a2018" stroke-width="1"/>'
            '<circle cx="%d" cy="%d" r="8" fill="none" stroke="#2a2018" stroke-width=".4" stroke-dasharray="1 2"/></g>' % (rays, sx, sy, sx, sy))
# moon & stars
mx, my = 712, 52
body.append('<path d="M%d %d a16 16 0 1 0 14 22 a12 12 0 1 1 -14 -22z" fill="#f4ecc8" stroke="#2a2018" stroke-width="1"/>' % (mx - 4, my - 16))
for (x, y) in [(660, 40), (682, 74), (640, 66), (700, 92)]:
    body.append('<path d="M%d %d l1.4 3.4 3.6 .3 -2.8 2.3 1 3.5 -3.2 -2 -3.2 2 1 -3.5 -2.8 -2.3 3.6 -.3z" fill="#f4ecc8" stroke="#2a2018" stroke-width=".5"/>' % (x, y - 5))

# ===== DAY figure =====
day = ['<g filter="url(#ink-rough)">', body_fig(CXD, 'open', 'pl-weiqi-skin'), '</g>']
day.append(qiao(CXD, 'yang', True)); day.append(qiao(CXD, 'yin', False))
# wei-qi arrows on the exterior: down the outer arms & legs, both sides
for sg in (1, -1):
    arm = [(sg * 33, 34), (sg * 46, 74), (sg * 68, 100), (sg * 75, 150), (sg * 72, 210), (sg * 70, 262)]
    leg = [(sg * 49, 232), (sg * 50, 280), (sg * 45, 330), (sg * 42, 380), (sg * 37, 425)]
    for L in (arm, leg):
        day.append('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="7 4" marker-end="url(#ink-arrow-red)"/>' % (smooth([P(CXD, x, y) for x, y in L]), RED))
# eyes -> head arcs (目張則氣上行於頭)
for sg in (1, -1):
    day.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.4" marker-end="url(#ink-arrow-red)"/>' % (
        smooth([P(CXD, sg * 12, 25), P(CXD, sg * 22, 6), P(CXD, sg * 30, 20)]), GOLD))
body.append('\n'.join(day))
D = []
D.append(label(22, 120, '目張', None) + label(22, 134, 'eyes open', None, cls='le halo'))
D.append(leader(54, 124, CXD - 8 * S - 6, TOP + 28 * S))
D.append(label(22, 76, '陽氣出於目', None, cls='ls halo') + label(22, 90, '上行於頭', None, cls='ls halo'))
D.append(leader(82, 80, CXD - 23 * S, TOP + 7 * S))
D.append(label(22, 348, '陽蹻脈', None) + label(22, 362, 'Yangqiao vessel', None, cls='le halo'))
D.append(label(22, 376, '外踝→體側→目內眥', None, cls='ls halo'))
D.append(leader(120, 353, CXD - 39 * S, TOP + 330 * S))
D.append(label(288, 196, '衛氣', None) + label(288, 210, 'Wei-qi', None, cls='le halo'))
D.append(label(288, 224, '行於陽分', None, cls='ls halo'))
D.append(leader(286, 202, CXD + 74 * S, TOP + 150 * S))
D.append(label(288, 300, '體表 · 四肢', None, cls='ls halo') + label(288, 314, 'skin &amp; limbs', None, cls='le halo'))
D.append(leader(286, 304, CXD + 49 * S, TOP + 290 * S))
D.append(label(288, 116, '目內眥', None) + label(288, 130, '睛明 BL1', None, cls='le halo'))
D.append(leader(286, 120, CXD + 5 * S, TOP + 29 * S))
D.append(label(288, 400, '陰蹻脈', None, cls='ls halo') + label(288, 414, '（晝弱）', None, cls='ls halo'))
D.append(leader(286, 404, CXD + 14 * S, TOP + 380 * S))
D.append('<text x="24" y="486" class="ls">「平旦陰盡，陽氣出於目，目張則氣上行於頭」《靈樞·衛氣行》</text>')
body.append('\n'.join(D))

# ===== NIGHT figure =====
N = ['<g filter="url(#ink-rough)">', body_fig(CXN, 'closed', 'pl-weiqi-skinn')]
def org(pts_, fill, extra=''):
    return '<path d="%s" fill="%s" stroke="#2a2018" stroke-width=".9"%s/>' % (smooth([P(CXN, x, y) for x, y in pts_], close=True), fill, extra)
# kidneys (retroperitoneal, drawn dashed = behind)
N.append(org([(-12, 194), (-17, 189), (-25, 192), (-28, 206), (-25, 220), (-17, 222), (-13, 214), (-15, 207)], '#c98a70', ' stroke-dasharray="2 1.5"'))
N.append(org([(12, 188), (17, 183), (25, 186), (28, 200), (25, 214), (17, 216), (13, 208), (15, 201)], '#c98a70', ' stroke-dasharray="2 1.5"'))
# lungs
RL = [(-6, 92), (-14, 87), (-24, 93), (-31, 110), (-34, 135), (-34, 160), (-22, 156), (-11, 160), (-5, 150), (-4, 118)]
LL = [(6, 92), (14, 87), (24, 93), (31, 110), (34, 135), (33, 162), (22, 160), (17, 154), (15, 142), (9, 132), (6, 115)]
N.append(org(RL, '#e7b3aa')); N.append(org(LL, '#e7b3aa'))
for sg, Lp in ((-1, RL), (1, LL)):
    N.append('<path d="%s" fill="url(#ink-stipple-l)"/>' % smooth([P(CXN, x, y) for x, y in Lp], close=True))
    N.append('<path d="%s" class="ink2" stroke-width=".45"/>' % smooth([P(CXN, sg * 6, 100), P(CXN, sg * 18, 112), P(CXN, sg * 30, 122)]))
# heart
N.append(org([(-6, 128), (3, 123), (13, 128), (20, 140), (18, 152), (9, 158), (1, 155), (-5, 147), (-8, 137)], '#c4594a'))
N.append('<path d="%s" class="ink2"/>' % smooth([P(CXN, 2, 126), P(CXN, 6, 140), P(CXN, 9, 156)]))
N.append('<path d="%s" fill="none" stroke="#2a2018" stroke-width="2.4"/>' % smooth([P(CXN, -1, 128), P(CXN, -1, 112), P(CXN, 5, 105), P(CXN, 9, 112)]))
N.append('<path d="%s" fill="none" stroke="#c4594a" stroke-width="1.2"/>' % smooth([P(CXN, -1, 128), P(CXN, -1, 112), P(CXN, 5, 105), P(CXN, 9, 112)]))
# diaphragm
N.append('<path d="%s" class="ink2" stroke-dasharray="3 2"/>' % smooth([P(CXN, -34, 162), P(CXN, -18, 152), P(CXN, 0, 160), P(CXN, 18, 155), P(CXN, 34, 164)]))
# liver
LV = [(-35, 163), (-22, 158), (-6, 161), (10, 163), (21, 167), (14, 173), (0, 179), (-14, 187), (-28, 190), (-35, 180)]
N.append(org(LV, '#a95c48'))
N.append('<path d="%s" fill="url(#ink-hatch-l)"/>' % smooth([P(CXN, x, y) for x, y in LV], close=True))
N.append('<path d="%s" class="ink2"/>' % smooth([P(CXN, -4, 162), P(CXN, -2, 172), P(CXN, -6, 182)]))
# spleen
N.append(org([(24, 162), (32, 165), (35, 176), (30, 186), (23, 181), (21, 170)], '#8f5f7a'))
N.append('</g>')
# yin qiao bold, yang qiao faint
N.append(qiao(CXN, 'yin', True)); N.append(qiao(CXN, 'yang', False))
# night circuit: foot (足少陰) -> kidney -> heart -> lung -> liver -> spleen -> kidney
def arr(a, b, bend=0.25, col=BLUE, w=1.6):
    (x1, y1), (x2, y2) = P(CXN, *a), P(CXN, *b)
    mx_, my_ = (x1 + x2) / 2 + (y2 - y1) * bend, (y1 + y2) / 2 - (x2 - x1) * bend
    return '<path d="M%s %s Q%s %s %s %s" fill="none" stroke="%s" stroke-width="%s" marker-end="url(#ink-arrow-blue)"/>' % (
        f(x1), f(y1), f(mx_), f(my_), f(x2), f(y2), col, w)
N.append('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="7 4" marker-end="url(#ink-arrow-blue)"/>' % (
    smooth([P(CXN, 6, 440), P(CXN, 8, 380), P(CXN, 8, 300), P(CXN, 4, 250), P(CXN, 14, 222)]), BLUE))
seq = [((20, 190), (12, 158)), ((-4, 136), (-22, 128)), ((-26, 150), (-22, 172)), ((-2, 172), (24, 170)), ((28, 186), (25, 198))]
for (a, b), bend in zip(seq, [0.3, 0.3, 0.4, -0.25, -0.5]):
    N.append(arr(a, b, bend))
body.append('\n'.join(N))
NL = []
nums = [(26, 176, '1'), (5, 124, '2'), (-34, 140, '3'), (10, 178, '4'), (36, 194, '5')]
for x, y, n in []:
    X, Y = P(CXN, x, y)
    NL.append('<circle cx="%s" cy="%s" r="5.4" fill="#fbf6ea" stroke="%s" stroke-width=".7"/><text x="%s" y="%s" text-anchor="middle" style="font-size:8.5px;font-weight:700;fill:%s">%s</text>' % (
        f(X), f(Y), BLUE, f(X), f(Y + 3), BLUE, n))
# organ labels
def ol(lx, ly, zh, en, tx, ty, anchor='start'):
    X, Y = P(CXN, tx, ty)
    a = ' text-anchor="end"' if anchor == 'end' else ''
    x2 = lx - 3 if anchor == 'start' else lx + 3
    return ('<text x="%d" y="%d" class="lb halo"%s>%s <tspan class="le">%s</tspan></text>' % (lx, ly, a, zh, en) + leader(x2, ly - 4, X, Y))
NL.append(ol(662, 150, '肺', 'Lung', 28, 120))
NL.append(ol(662, 174, '心', 'Heart', 15, 145))
NL.append(ol(662, 198, '脾', 'Spleen', 30, 176))
NL.append(ol(662, 222, '腎', 'Kidney', 25, 205))
NL.append(ol(474, 222, '肝', 'Liver', -28, 182, anchor='end'))
NL.append(label(662, 262, '腎→心→肺', None, cls='ls halo') + label(662, 276, '→肝→脾→腎', None, cls='ls halo'))
NL.append(label(662, 290, '一周', None, cls='ls halo'))
NL.append(label(394, 120, '目瞑', None) + label(394, 134, 'eyes closed', None, cls='le halo'))
NL.append(leader(424, 124, CXN - 10 * S, TOP + 30 * S))
NL.append(label(662, 348, '陰蹻脈', None) + label(662, 362, 'Yinqiao vessel', None, cls='le halo'))
NL.append(label(662, 376, '內踝→腹胸', None, cls='ls halo') + label(662, 390, '→目內眥', None, cls='ls halo'))
NL.append(leader(660, 352, CXN + 15 * S, TOP + 340 * S))
NL.append(label(394, 410, '衛氣從足少陰', None, cls='ls halo') + label(394, 424, '入腎 · 行於陰分', None, cls='ls halo'))
NL.append(leader(470, 415, CXN + 7 * S, TOP + 360 * S))

NL.append('<text x="396" y="472" class="ls">「其始入於陰，常從足少陰注於腎，腎注於心，心注於肺，</text>')
NL.append('<text x="396" y="488" class="ls">肺注於肝，肝注於脾，脾復注於腎為周」《靈樞·衛氣行》</text>')
body.append('\n'.join(NL))

# ===== bottom strip: gate schematic =====
B = []
B.append('<text x="14" y="532" class="lt">病機示意：衛氣的「門」 <tspan class="le" style="font-size:12px">the gate between yang (exterior) and yin (interior)</tspan></text>')
cells = [(14, '① 常', '夜則衛氣入陰 → 目瞑', 'open'), (264, '② 邪客', '厥氣客於五藏六府 → 路被堵住', 'blocked'), (514, '③ 半夏湯', '「陰陽已通，其臥立至」', 'open2')]
rnd = random.Random(2)
for x0, t1, t2, st in cells:
    y0 = 544
    B.append('<rect x="%d" y="%d" width="232" height="100" fill="#fbf6ea" stroke="#bfae8a" stroke-width=".8" stroke-dasharray="3 3"/>' % (x0, y0))
    B.append('<text x="%d" y="%d" class="lb">%s</text><text x="%d" y="%d" class="ls">%s</text>' % (x0 + 8, y0 + 18, t1, x0 + 8, y0 + 92, t2))
    # zones
    B.append('<rect x="%d" y="%d" width="84" height="46" fill="#f6e7b0" stroke="#2a2018" stroke-width=".7"/>' % (x0 + 10, y0 + 28))
    B.append('<rect x="%d" y="%d" width="84" height="46" fill="#cfdcef" stroke="#2a2018" stroke-width=".7"/>' % (x0 + 138, y0 + 28))
    B.append('<text x="%d" y="%d" class="ls">陽 · 外</text><text x="%d" y="%d" class="ls">陰 · 內（五藏）</text>' % (x0 + 14, y0 + 40, x0 + 142, y0 + 40))
    # gate posts
    gx = x0 + 116
    B.append('<rect x="%d" y="%d" width="5" height="50" fill="#8a6a3a" stroke="#2a2018" stroke-width=".6"/><rect x="%d" y="%d" width="5" height="50" fill="#8a6a3a" stroke="#2a2018" stroke-width=".6"/>' % (gx - 20, y0 + 26, gx + 15, y0 + 26))
    B.append('<path d="M%d %d h44" stroke="#2a2018" stroke-width="2.4"/><path d="M%d %d h44" stroke="#a8412c" stroke-width="1.2"/>' % (gx - 22, y0 + 26, gx - 22, y0 + 26))
    if st == 'blocked':
        # closed doors + dark turbulent qi
        B.append('<rect x="%d" y="%d" width="30" height="40" fill="#6b4a2a" stroke="#2a2018" stroke-width=".8"/><path d="M%d %d v40" class="ink2"/>' % (gx - 15, y0 + 32, gx, y0 + 32))
        B.append('<path d="M%d %d l30 40 M%d %d l-30 40" stroke="#2a2018" stroke-width="1"/>' % (gx - 15, y0 + 32, gx + 15, y0 + 32))
        for k in range(3):
            B.append('<path d="M%d %d c-6 -6 6 -12 10 -4 s-2 10 -8 6" fill="none" stroke="#3a3040" stroke-width="1.2"/>' % (x0 + 160 + k * 18, y0 + 58 + (k % 2) * 6))
        # piled-up qi on the yang side
        for k in range(14):
            B.append('<circle cx="%s" cy="%s" r="2.6" fill="%s" stroke="#2a2018" stroke-width=".4"/>' % (f(x0 + 60 + rnd.random() * 30), f(y0 + 48 + rnd.random() * 22), RED))
        B.append('<path d="M%d %d h22" stroke="%s" stroke-width="1.6" marker-end="url(#ink-tee)"/>' % (gx - 40, y0 + 60, RED))
        B.append('<text x="%d" y="%d" class="ls" style="fill:%s">陽蹻盛 → 目不瞑</text>' % (x0 + 120, y0 + 18, RED))
    else:
        # open doors swung aside + qi passing
        B.append('<path d="M%d %d l-6 -3 v38 l6 3z" fill="#6b4a2a" stroke="#2a2018" stroke-width=".6"/><path d="M%d %d l6 -3 v38 l-6 3z" fill="#6b4a2a" stroke="#2a2018" stroke-width=".6"/>' % (gx - 15, y0 + 34, gx + 15, y0 + 34))
        B.append('<path d="M%d %d C%d %d %d %d %d %d" fill="none" stroke="%s" stroke-width="1.8" stroke-dasharray="6 3" marker-end="url(#ink-arrow-blue)"/>' % (
            x0 + 50, y0 + 60, x0 + 90, y0 + 66, x0 + 140, y0 + 66, x0 + 190, y0 + 60, BLUE))
        for k in range(4):
            B.append('<circle cx="%d" cy="%d" r="2.6" fill="%s" stroke="#2a2018" stroke-width=".4"/>' % (x0 + 158 + k * 14, y0 + 50 + (k % 2) * 8, BLUE))
        if st == 'open2':
            B.append('<text x="%d" y="%d" class="ls" style="fill:%s">半夏＋秫米：通</text>' % (x0 + 136, y0 + 18, RED))
body.append('\n'.join(B))

cap = ('<b>圖 9-B　衛氣的晝夜路線。</b>依《靈樞》〈衛氣行〉〈邪客〉〈大惑論〉重繪的<b>中醫理論示意圖，不是解剖圖</b>：白天衛氣行於體表與四肢（陽），目張；夜裡從足少陰入腎，依腎→心→肺→肝→脾的順序在五藏間周行（陰），目瞑。'
       '陽蹻、陰蹻兩脈各單側繪出，都上行到目內眥（睛明）。下排：〈邪客〉說的病不是陽多或陰少，而是「厥氣客於五藏六府」把門堵住，衛氣只能留在陽分、陽蹻盛而目不瞑；半夏湯的用意是把門打開。五藏位置為簡化示意。')
open('/home/user/Insomnia/figs/pl-weiqi.html', 'w').write(figure(PID, 'Plate 9·B', '衛氣晝行於陽、夜行於陰', 'Wei-qi by day and by night (TCM theory)', 652,
                                                        '白天衛氣行於體表、夜間入於五藏的中醫理論示意圖，以及厥氣堵住入陰之路的病機', '\n'.join(body), cap))
