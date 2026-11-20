import sys, os, math, random, io, contextlib
sys.path.insert(0, os.path.dirname(__file__))
from plib import *
with contextlib.redirect_stdout(io.StringIO()):
    import brain

P = 'pl-hpa'
D = []
O = []
add = O.append
CX = 140
ACTH = '#b5473a'; CORT = '#c9962e'; ADR = '#8a3a2a'; ORXC = '#c9962e'
SK = '#f6e3d3'


def mir(pts):
    return [(2 * CX - x, y) for x, y in pts]


def num(x, y, n, col=INK, r=7.5):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="#fbf6ea" stroke-width="1.4"/>'
            '<text x="%s" y="%s" text-anchor="middle" style="font-size:10.5px;font-weight:700;fill:#fff;font-family:Georgia,serif">%s</text>') % (f(x), f(y), r, col, f(x), f(y + 3.7), n)


D.append('<marker id="%s-ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (P, ACTH))
D.append('<marker id="%s-ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (P, CORT))
D.append('<marker id="%s-ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (P, ADR))
D.append('<marker id="%s-ny" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="#a8872a"/></marker>' % P)
D.append('<marker id="%s-tb" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M5 0V10" stroke="%s" stroke-width="2.4"/></marker>' % (P, WEST))

# =============== BODY (front view, semi-transparent) ===============
half = [(CX + 21, 120), (CX + 21, 136), (CX + 24, 150), (CX + 46, 159), (CX + 74, 166), (CX + 91, 180), (CX + 97, 204),
        (CX + 98, 240), (CX + 100, 278), (CX + 101, 300), (CX + 104, 338), (CX + 104, 378), (CX + 100, 408),
        (CX + 105, 426), (CX + 107, 446), (CX + 104, 466), (CX + 99, 477), (CX + 93, 481), (CX + 87, 475), (CX + 85, 458),
        (CX + 80, 454), (CX + 79, 444), (CX + 82, 426), (CX + 83, 410),
        (CX + 81, 372), (CX + 78, 332), (CX + 78, 298), (CX + 74, 254), (CX + 67, 220),
        (CX + 65, 246), (CX + 61, 284), (CX + 56, 318), (CX + 63, 356), (CX + 70, 398), (CX + 68, 450), (CX + 62, 520),
        (CX + 8, 520), (CX + 5, 470), (CX + 2, 428)]
body = half + mir(half)[::-1]
body_d = cr(body, True, k=.85)
D.append('<linearGradient id="%s-fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".9" stop-color="%s" stop-opacity=".9"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>' % (P, SK, SK))
add('<path d="%s" fill="url(#%s-fade)"/>' % (body_d, P))
add(shade(P + '-m1', body_d, 8, 0, 'ink-hatch-l', .7))
D.append('<clipPath id="%s-cut"><rect x="0" y="0" width="290" height="514"/></clipPath>' % P)
# head
head = [(CX, 26), (CX + 22, 30), (CX + 33, 46), (CX + 36, 70), (CX + 34, 92), (CX + 28, 108), (CX + 18, 120), (CX, 126)]
head_all = head + mir(head)[::-1][1:-1]
hd = cr(head_all, True)
add('<path d="%s" fill="%s" fill-opacity=".9"/>' % (hd, SK))
# ears
for sg in (1, -1):
    e = [(CX + sg * 34, 72), (CX + sg * 40, 68), (CX + sg * 42, 80), (CX + sg * 39, 94), (CX + sg * 34, 98)]
    add('<path d="%s" fill="%s" class="ink"/>' % (cr(e), SK))
    add('<path d="M%s 75 q%s 6 0 16" class="ink2"/>' % (CX + sg * 37, sg * 3))
# brain silhouette (front view) inside head
for sg in (1, -1):
    bh = [(CX + sg * 1.5, 34), (CX + sg * 16, 33), (CX + sg * 27, 42), (CX + sg * 31, 58), (CX + sg * 30, 74), (CX + sg * 24, 84), (CX + sg * 12, 80), (CX + sg * 4, 82), (CX + sg * 1.5, 70)]
    bd = cr(bh, True)
    add('<path d="%s" fill="#efd3c6" fill-opacity=".9"/><path d="%s" fill="url(#ink-stipple-l)"/><path d="%s" class="ink" stroke-width=".9"/>' % (bd, bd, bd))
    for g in [[(CX + sg * 6, 40), (CX + sg * 14, 46), (CX + sg * 10, 54)], [(CX + sg * 20, 40), (CX + sg * 24, 52), (CX + sg * 18, 60)],
              [(CX + sg * 8, 60), (CX + sg * 16, 66), (CX + sg * 24, 64)], [(CX + sg * 26, 70), (CX + sg * 18, 76)]]:
        add('<path d="%s" class="ink2" stroke-opacity=".7"/>' % cr(g))
add('<circle cx="%s" cy="84" r="3" fill="%s" stroke="%s" stroke-width=".6"/>' % (CX, '#e9b4a2', INK))   # pituitary
add('<circle cx="%s" cy="76" r="2.6" fill="%s" stroke="%s" stroke-width=".6"/>' % (CX, ACTH, INK))      # PVN/hypothalamus
# face features (fine lines)
for sg in (1, -1):
    add('<path d="M%s 92 q%s -4 %s 0 q%s 3 %s 0" class="ink2"/>' % (CX + sg * 7, sg * 6, sg * 12, -sg * 6, -sg * 12))
    add('<path d="M%s 86 q%s -4 %s 1" class="ink" stroke-width=".9"/>' % (CX + sg * 6, sg * 7, sg * 15))
add('<path d="M%s 94 l-2 12 q2 3 5 0" class="ink2"/><path d="M%s 113 q5 3 10 0" class="ink2"/>' % (CX + 1, CX - 5))
add('<path d="%s" class="ink3"/>' % hd)
# hairline hint


# surface anatomy lines
L2 = []
for sg in (1, -1):
    sgp = lambda pts: [(CX + sg * x, y) for x, y in pts]
    L2.append(cr(sgp([(6, 160), (30, 163), (60, 166)])))           # clavicle
    L2.append(cr(sgp([(21, 120), (14, 142), (6, 158)])))           # sternocleidomastoid
    L2.append(cr(sgp([(8, 224), (34, 228), (58, 214), (67, 196)])))  # pectoral
    L2.append(cr(sgp([(4, 250), (28, 268), (50, 290)])))           # costal margin
    L2.append(cr(sgp([(58, 352), (34, 392), (10, 414)])))          # inguinal
    L2.append(cr(sgp([(80, 210), (84, 250), (86, 286)])))          # biceps
    L2.append(cr(sgp([(85, 298), (92, 302), (98, 300)])))          # elbow crease
    for k in range(3):                                            # fingers
        L2.append(cr(sgp([(90 + k * 4.5, 446), (91 + k * 4.3, 462), (92 + k * 4, 474)])))
    L2.append(cr(sgp([(88, 428), (84, 440), (82, 448)])))          # thumb
    L2.append(cr(sgp([(88, 444), (96, 442), (104, 446)])))         # knuckles
    add('<circle cx="%s" cy="218" r="1.6" fill="none" stroke="%s" stroke-width=".6"/>' % (CX + sg * 34, INK))
L2.append('M%s 250 V312' % CX)
add('<path d="%s" class="ink2" stroke-opacity=".75"/>' % ' '.join(L2))
add('<path d="M%s 320 q2 3 0 5" class="ink2"/>' % CX)

# internal: spine, aorta, IVC, heart, kidneys, adrenals
G = []
for k in range(16):
    y = 152 + k * 15
    G.append('<rect x="%s" y="%s" width="14" height="11" rx="2.5" fill="%s" fill-opacity=".55" stroke="%s" stroke-width=".5" stroke-opacity=".5"/>' % (CX - 7, y, BONE, INK))
heart = [(CX + 2, 206), (CX + 18, 204), (CX + 28, 216), (CX + 22, 236), (CX + 6, 248), (CX - 10, 236), (CX - 12, 218)]
G.append('<path d="%s" fill="#d9705f" fill-opacity=".25" stroke="%s" stroke-width=".6" stroke-opacity=".6"/>' % (cr(heart, True), INK))
G.append('<path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-opacity=".7"/>' % (cr([(CX + 4, 210), (CX + 2, 196), (CX + 10, 190), (CX + 8, 204), (CX + 5, 260), (CX + 4, 330)]), '#c86454'))
G.append('<path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-opacity=".55"/>' % (cr([(CX - 6, 214), (CX - 7, 260), (CX - 6, 330)]), '#5c82b5'))
for sg, dy in ((-1, 6), (1, 0)):
    kc = (CX + sg * 31, 292 + dy)
    kid = [(kc[0] - sg * 4, kc[1] - 22), (kc[0] + sg * 8, kc[1] - 20), (kc[0] + sg * 11, kc[1]), (kc[0] + sg * 8, kc[1] + 20), (kc[0] - sg * 4, kc[1] + 22),
           (kc[0] - sg * 9, kc[1] + 10), (kc[0] - sg * 6, kc[1]), (kc[0] - sg * 9, kc[1] - 10)]
    G.append('<path d="%s" fill="#b9675a" fill-opacity=".75" stroke="%s" stroke-width=".9"/>' % (cr(kid, True), INK))
    ad = [(kc[0] - sg * 8, kc[1] - 22), (kc[0] - sg * 2, kc[1] - 33), (kc[0] + sg * 6, kc[1] - 30), (kc[0] + sg * 10, kc[1] - 21), (kc[0], kc[1] - 23)]
    G.append('<path d="%s" fill="#e8c35a" stroke="%s" stroke-width=".8"/>' % (cr(ad, True), INK))
    G.append('<path d="M%s %s H%s" stroke="#c86454" stroke-width="2.4" stroke-opacity=".8"/>' % (CX + sg * 4, kc[1], kc[0] - sg * 6))
    G.append('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="#e8cf7a" stroke-width="1.6"/>' % (kc[0] - sg * 3, kc[1] + 20, kc[0] - sg * 8, kc[1] + 60, CX + sg * 14, 400))
add('<g>%s</g>' % ''.join(G))
add('<path d="%s" class="ink3" clip-path="url(#%s-cut)"/>' % (body_d, P))
# re-draw head/neck junction cover


# --- pathway on body ---
RA = (CX + 31, 262)   # viewer-right adrenal (figure's left)
LA = (CX - 31, 268)
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#%s-ar)"/>' % (cr([(CX + 3, 88), (CX + 12, 130), (CX + 20, 196), (CX + 18, 236), RA]), ACTH, P))
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.8" marker-end="url(#%s-ag)"/>' % (cr([(LA[0] - 2, LA[1] - 8), (CX - 52, 230), (CX - 46, 160), (CX - 26, 110), (CX - 12, 82)]), CORT, P))
add('<path d="%s" fill="none" stroke="#a8872a" stroke-width="1.4" stroke-dasharray="1.5 2" marker-end="url(#%s-ny)"/>' % (cr([(CX + 6, 236), (CX + 16, 250), (RA[0] - 4, RA[1] + 4)]), P))
add(num(CX + 22, 160, 3, ACTH))
add(num(CX - 54, 200, 5, CORT))
add('<text x="%s" y="150" class="ls halo" style="fill:%s;font-weight:600">ACTH</text>' % (CX + 26, ACTH))
add('<text x="%s" y="150" class="ls halo" text-anchor="end" style="fill:#8a6418;font-weight:600">皮質醇</text>' % (CX - 60))
add('<text x="%s" y="164" class="ls halo" text-anchor="end" style="fill:#8a6418;font-weight:600">腎上腺素</text>' % (CX - 60))

# body labels (left margin)
BL = [
    dict(t=(CX - 31, 296), zh='腎臟', en='Kidney'),
    dict(t=(LA[0] - 2, LA[1] - 2), zh='腎上腺', en='Adrenal gland'),
    dict(t=(CX - 10, 222), zh='心臟', en='Heart'),
]
add(label('L', 46, 262, '腎上腺', 'Adrenal', (LA[0] - 5, LA[1] - 3), stub=4))
add(label('L', 46, 304, '腎臟', 'Kidney', (CX - 34, 300), stub=4))

# =============== BRAIN INSET (sagittal, reuse plate 1-A) ===============
s = .55
BX0, BY0 = 400, 44


def Bm(x, y):
    return (BX0 + (x - 178) * s, BY0 + (y - 61) * s)


I = ['<rect x="292" y="14" width="460" height="318" rx="5" class="panel"/>',
     '<text x="302" y="34" class="lb">腦（正中切面放大）<tspan class="le">Brain, midsagittal</tspan></text>']
Gb = inline_classes('\n'.join(brain.G[:brain.NUC])).replace('pl-brain', P + '-b')
D.append('<clipPath id="%s-bc"><rect x="170" y="50" width="460" height="392"/></clipPath>' % P)
I.append('<g transform="translate(%s %s) scale(%s) translate(-178 -61)"><g clip-path="url(#%s-bc)">%s</g></g>' % (BX0, BY0, s, P, Gb))
PVN = Bm(336, 250); ORX = Bm(353, 268); AMY = Bm(362, 332); APIT = Bm(311, 327); LC = Bm(457, 326); ME = Bm(330, 302)
# amygdala projected (dashed)
I.append('<ellipse cx="%s" cy="%s" rx="10" ry="6.5" fill="#c86454" fill-opacity=".35" stroke="%s" stroke-width="1" stroke-dasharray="2.5 1.5" transform="rotate(-20 %s %s)"/>' % (
    f(AMY[0]), f(AMY[1]), RED, f(AMY[0]), f(AMY[1])))
I.append('<ellipse cx="%s" cy="%s" rx="4.4" ry="3.3" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(PVN[0]), f(PVN[1]), ACTH, INK))
I.append('<ellipse cx="%s" cy="%s" rx="4.4" ry="3.3" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(ORX[0]), f(ORX[1]), ORXC, INK))
I.append('<ellipse cx="%s" cy="%s" rx="3.6" ry="3" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(LC[0]), f(LC[1]), RED, INK))
# portal vessels hint
I.append('<path d="M%s %s q-2 6 -6 10 M%s %s q2 6 -2 11" stroke="#c86454" stroke-width=".9" fill="none"/>' % (f(ME[0]), f(ME[1]), f(ME[0] - 2), f(ME[1] + 1)))
# arrows: 1 amygdala -> PVN
I.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" marker-end="url(#%s-ar)"/>' % (cr([(AMY[0] + 6, AMY[1] - 5), (AMY[0] + 14, AMY[1] - 24), (PVN[0] + 12, PVN[1] + 6), (PVN[0] + 4, PVN[1] + 2)]), ACTH, P))
# 2 PVN -> median eminence -> anterior pituitary (CRH)
I.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="4 2" marker-end="url(#%s-ab)"/>' % (cr([(PVN[0] - 2, PVN[1] + 3), (PVN[0] - 3, PVN[1] + 14), (ME[0] - 1, ME[1] + 4), (APIT[0] + 3, APIT[1] - 4)]), ADR, P))
# 6 PVN (CRH) -> orexin
I.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" marker-end="url(#%s-ag)"/>' % (cr([(PVN[0] + 4, PVN[1] - 3), (PVN[0] + 16, PVN[1] - 4), (ORX[0] + 4, ORX[1] - 4)]), CORT, P))
# orexin -> LC (arousal)
I.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.3" stroke-dasharray="3 2" marker-end="url(#%s-ag)"/>' % (cr([(ORX[0] + 5, ORX[1] + 2), (ORX[0] + 30, ORX[1] + 8), (LC[0] - 6, LC[1] - 3)]), CORT, P))
# 5 cortisol feedback (tee) to PVN & pituitary, coming from the blood (below)
fb0 = (Bm(250, 430)[0], 300)
I.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.3" stroke-dasharray="4 2.5" marker-end="url(#%s-tb)"/>' % (cr([fb0, (fb0[0] + 10, APIT[1] + 30), (APIT[0] - 9, APIT[1] + 6)]), WEST, P))
I.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.3" stroke-dasharray="4 2.5" marker-end="url(#%s-tb)"/>' % (cr([fb0, (fb0[0] - 4, PVN[1] + 30), (PVN[0] - 9, PVN[1] + 1)]), WEST, P))
I.append('<text x="%s" y="%s" class="ls halo" style="fill:%s;font-weight:600">皮質醇負回饋</text>' % (f(fb0[0] - 30), 314, WEST))
I.append(num(AMY[0] + 22, AMY[1] - 14, 1, ACTH))
I.append(num(PVN[0] - 14, PVN[1] + 18, 2, ADR))
I.append(num(PVN[0] + 18, PVN[1] - 14, 6, CORT))
I.append(num(fb0[0] - 40, 302, 5, WEST))
# labels
IL = [
    dict(t=(PVN[0] - 3, PVN[1] - 1), zh='室旁核 PVN', en='分泌 CRH'),
    dict(t=(APIT[0] - 2, APIT[1]), zh='腦下垂體前葉', en='Ant. pituitary → ACTH'),
    dict(t=(AMY[0] - 6, AMY[1] + 3), zh='杏仁核（投影）', en='Amygdala, lateral'),
]
I.append(column('L', 392, IL, 120, 290, gap=46))
IR = [
    dict(t=(ORX[0] + 4, ORX[1]), zh='外側下視丘 orexin', en='CRH 直接刺激它'),
    dict(t=(LC[0] + 3, LC[1]), zh='藍斑核 LC', en='清醒中樞（油門）'),
]
I.append(column('R', 646, IR, 140, 260, gap=40))

# connector head -> brain inset
I.append('<path d="M%s 56 L292 70 M%s 96 L292 300" class="ld" stroke-dasharray="3 3" stroke="#8a6a3a"/>' % (CX + 36, CX + 36))

# =============== ADRENAL / KIDNEY INSET ===============
K = ['<rect x="292" y="342" width="460" height="306" rx="5" class="panel"/>',
     '<text x="302" y="362" class="lb">腎上腺與腎臟（剖面）<tspan class="le">Adrenal on the kidney, cut</tspan></text>']
kc = (530, 532)
kid = [(kc[0] - 30, kc[1] - 92), (kc[0] + 20, kc[1] - 98), (kc[0] + 52, kc[1] - 66), (kc[0] + 62, kc[1] - 10), (kc[0] + 52, kc[1] + 56),
       (kc[0] + 18, kc[1] + 96), (kc[0] - 28, kc[1] + 90), (kc[0] - 48, kc[1] + 52), (kc[0] - 40, kc[1] + 22), (kc[0] - 30, kc[1] + 4),
       (kc[0] - 40, kc[1] - 16), (kc[0] - 50, kc[1] - 48)]
kd = cr(kid, True)
K.append('<path d="%s" fill="#c8705f"/><path d="%s" fill="url(#ink-stipple)" opacity=".5"/>' % (kd, kd))
K.append(shade(P + '-m2', kd, -10, -8, 'ink-hatch', .6))
# medulla region (inner) and pyramids
cxk, cyk = kc[0] + 6, kc[1]
inner = [(cxk + (x - cxk) * .74, cyk + (y - cyk) * .78) for x, y in kid]
sinus = [(kc[0] - 34, kc[1] - 40), (kc[0] + 2, kc[1] - 50), (kc[0] + 20, kc[1] - 10), (kc[0] + 18, kc[1] + 34), (kc[0] - 6, kc[1] + 52), (kc[0] - 36, kc[1] + 38), (kc[0] - 30, kc[1] + 4)]
pyr_c = []
for ang in [-118, -82, -48, -14, 20, 54, 88, 122]:
    a = math.radians(ang)
    bx, by = cxk + 46 * math.cos(a), cyk + 70 * math.sin(a)
    tx, ty = cxk + 14 * math.cos(a) - 4, cyk + 26 * math.sin(a)
    px, py = -math.sin(a), math.cos(a)
    w = 15
    p = [(bx + px * w, by + py * w * .8), (bx - px * w, by - py * w * .8), (tx, ty)]
    pd = 'M%s %s Q%s %s %s %s L%s %s Z' % (f(p[0][0]), f(p[0][1]), f(bx + math.cos(a) * 4), f(by + math.sin(a) * 4), f(p[1][0]), f(p[1][1]), f(p[2][0]), f(p[2][1]))
    K.append('<path d="%s" fill="#9a4a3e"/><path d="%s" fill="url(#ink-hatch-r)" opacity=".7"/><path d="%s" class="ink2"/>' % (pd, pd, pd))
sd = cr(sinus, True)
K.append('<path d="%s" fill="#f2e2a8"/><path d="%s" fill="url(#ink-stipple-l)"/><path d="%s" class="ink2"/>' % (sd, sd, sd))
# pelvis & calyces & ureter
pel = 'M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s C%s %s %s %s %s %s Z' % (
    kc[0] - 52, kc[1] + 6, kc[0] - 30, kc[1] - 14, kc[0] - 4, kc[1] - 30, kc[0] + 8, kc[1] - 24,
    kc[0] + 2, kc[1], kc[0] + 8, kc[1] + 26, kc[0] - 2, kc[1] + 32, kc[0] - 20, kc[1] + 28, kc[0] - 36, kc[1] + 16, kc[0] - 52, kc[1] + 16)
K.append('<path d="%s" fill="#f7f1e2" class="ink"/>' % pel)
K.append('<path d="M%s %s C%s %s %s %s %s 640" fill="none" stroke="%s" stroke-width="7"/><path d="M%s %s C%s %s %s %s %s 640" fill="none" stroke="#f7f1e2" stroke-width="5"/>' % (
    kc[0] - 50, kc[1] + 12, kc[0] - 62, kc[1] + 30, kc[0] - 58, kc[1] + 70, kc[0] - 64, INK, kc[0] - 50, kc[1] + 12, kc[0] - 62, kc[1] + 30, kc[0] - 58, kc[1] + 70, kc[0] - 64))
# renal artery & vein
K.append('<path d="M452 %s C470 %s 480 %s %s %s" fill="none" stroke="%s" stroke-width="7"/><path d="M452 %s C470 %s 480 %s %s %s" fill="none" stroke="#c86454" stroke-width="5"/>' % (
    kc[1] - 14, kc[1] - 18, kc[1] - 18, kc[0] - 40, kc[1] - 14, INK, kc[1] - 14, kc[1] - 18, kc[1] - 18, kc[0] - 40, kc[1] - 14))
K.append('<path d="M452 %s C470 %s 480 %s %s %s" fill="none" stroke="%s" stroke-width="8"/><path d="M452 %s C470 %s 480 %s %s %s" fill="none" stroke="#5c82b5" stroke-width="6"/>' % (
    kc[1] + 4, kc[1] + 6, kc[1] + 4, kc[0] - 44, kc[1] + 2, INK, kc[1] + 4, kc[1] + 6, kc[1] + 4, kc[0] - 44, kc[1] + 2))
K.append('<path d="%s" class="ink3"/>' % kd)
K.append('<ellipse cx="452" cy="%s" rx="2" ry="3.6" fill="#e9a596" class="ink2"/><ellipse cx="452" cy="%s" rx="2.2" ry="4" fill="#a9c3e6" class="ink2"/>' % (kc[1] - 14, kc[1] + 4))
# capsule fat hint
# adrenal (cut) on the upper pole
adr = [(kc[0] - 62, kc[1] - 98), (kc[0] - 30, kc[1] - 132), (kc[0] + 6, kc[1] - 156), (kc[0] + 34, kc[1] - 140), (kc[0] + 62, kc[1] - 104),
       (kc[0] + 46, kc[1] - 92), (kc[0] + 10, kc[1] - 98), (kc[0] - 26, kc[1] - 92)]
acx, acy = kc[0] + 2, kc[1] - 112
def scl(pts, k):
    return [(acx + (x - acx) * k, acy + (y - acy) * k) for x, y in pts]
ad0 = cr(adr, True); ad1 = cr(scl(adr, .9), True); ad2 = cr(scl(adr, .52), True); ad3 = cr(scl(adr, .4), True)
K.append('<path d="%s" fill="#f6e3a0" class="ink"/>' % ad0)            # glomerulosa
K.append('<path d="%s" fill="#e8c35a"/>' % ad1)                        # fasciculata
# fasciculata cords (radial)
cords = ''
for t in range(48):
    a = 2 * math.pi * t / 48
    cords += 'M%s %s L%s %s ' % (f(acx + 9 * math.cos(a)), f(acy + 6 * math.sin(a)), f(acx + 70 * math.cos(a)), f(acy + 50 * math.sin(a)))
D.append('<clipPath id="%s-fz"><path d="%s"/></clipPath>' % (P, ad1))
K.append('<path d="%s" stroke="#a8872a" stroke-width=".6" clip-path="url(#%s-fz)"/>' % (cords, P))
K.append('<path d="%s" fill="#c98a4a"/><path d="%s" fill="url(#ink-hatch-d)" opacity=".5"/>' % (ad2, ad2))   # reticularis
K.append('<path d="%s" fill="#8a3a2a"/><path d="%s" fill="url(#ink-stipple)" opacity=".7"/><path d="%s" class="ink2"/>' % (ad3, ad3, ad3))  # medulla
K.append('<path d="%s" class="ink2"/>' % ad1)
K.append('<path d="%s" class="ink3"/>' % ad0)
# splanchnic nerve into medulla
K.append('<path d="M752 456 C700 452 620 446 %s %s" fill="none" stroke="%s" stroke-width="3.4"/><path d="M752 456 C700 452 620 446 %s %s" fill="none" stroke="#e8cf7a" stroke-width="2"/>' % (
    f(acx + 16), f(acy + 2), INK, f(acx + 16), f(acy + 2)))
# ACTH arriving, outputs leaving
K.append('<path d="M396 400 C430 396 450 404 %s %s" fill="none" stroke="%s" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#%s-ar)"/>' % (f(acx - 50), f(acy + 2), ACTH, P))
K.append('<text x="300" y="398" class="lb halo" style="fill:%s">③ ACTH</text><text x="300" y="412" class="le halo">經血液而來</text>' % ACTH)
K.append('<path d="M%s %s C%s %s %s 380 %s 376" fill="none" stroke="%s" stroke-width="2" marker-end="url(#%s-ag)"/>' % (f(acx - 22), f(acy - 18), f(acx - 30), f(acy - 50), f(acx - 70), 600, CORT, P))
K.append('<path d="M%s %s C%s %s %s %s %s %s" fill="none" stroke="%s" stroke-width="2" marker-end="url(#%s-ab)"/>' % (f(acx + 6), f(acy - 6), f(acx + 30), f(acy - 50), f(acx + 70), 392, 690, 392, ADR, P))
K.append('<text x="606" y="380" class="lb halo" style="fill:#8a6418">④ 皮質醇 cortisol</text>')
K.append('<text x="644" y="410" class="lb halo" style="fill:%s">腎上腺素</text><text x="644" y="424" class="le halo">adrenaline</text>' % ADR)
KL = [
    dict(t=(acx - 54, acy + 6), zh='球狀帶', en='Zona glomerulosa'),
    dict(t=(acx - 34, acy + 16), zh='束狀帶 → 皮質醇', en='Zona fasciculata'),
    dict(t=(acx - 12, acy + 18), zh='網狀帶', en='Zona reticularis'),
    dict(t=(acx - 6, acy + 8), zh='髓質 → 腎上腺素', en='Adrenal medulla'),
]
for d, yy in zip(KL, [440, 472, 504, 536]):
    K.append(label('L', 438, yy, d['zh'], d['en'], d['t'], elbow=446))
KR = [
    dict(t=(614, 444), zh='④ 內臟神經（交感）', en='Splanchnic nerve → medulla'),
    dict(t=(kc[0] + 50, kc[1] - 30), zh='腎皮質', en='Renal cortex'),
    dict(t=(kc[0] + 36, kc[1] + 30), zh='腎錐體（髓質）', en='Renal pyramid'),
    dict(t=(kc[0] - 6, kc[1] + 48), zh='腎盂・輸尿管', en='Pelvis / ureter'),
]
for d, yy in zip(KR, [484, 530, 572, 614]):
    K.append(label('R', 618, yy, d['zh'], d['en'], d['t']))
K.append(label('L', 438, 572, '腎動脈・靜脈', 'Renal artery &amp; vein', (456, kc[1] - 4), elbow=446))
K.append('<path d="M%s 268 L292 470" class="ld" stroke-dasharray="3 3" stroke="#8a6a3a"/>' % (RA[0] + 6))

# =============== step list (left-bottom) ===============
S = ['<text x="12" y="548" class="lt">壓力軸的路線</text>']
steps = [(1, ACTH, '壓力／情緒經杏仁核啟動'), (2, ADR, 'PVN 分泌 CRH → 門脈'), (3, ACTH, '腦下垂體前葉 ACTH 進血液'),
         (4, CORT, '腎上腺皮質 → 皮質醇；交感 → 髓質 → 腎上腺素'), (5, WEST, '回到腦：負回饋 PVN／腦下垂體'), (6, CORT, 'CRH 同時推動 orexin → 清醒（Saper）')]
for i, (n, c, t) in enumerate(steps):
    y = 568 + i * 14.5
    S.append(num(20, y - 4, n, c, r=6))
    S.append('<text x="31" y="%s" class="ls">%s</text>' % (y, t))

body = inline_classes('\n'.join(O) + '\n' + '\n'.join(I) + '\n' + '\n'.join(K)) + '\n' + '\n'.join(S)
cap = ('<b>圖 1-D　第三股力量：壓力軸（HPA axis）與交感神經。</b>情緒與威脅經杏仁核送到下視丘室旁核（PVN），PVN 分泌 CRH，經下視丘–腦下垂體門脈讓前葉釋出 ACTH；'
       'ACTH 隨血流到腎臟上方的腎上腺，促使皮質（束狀帶）分泌皮質醇；同一時間交感神經直接讓髓質釋出腎上腺素。皮質醇回到腦負回饋 PVN 與腦下垂體。'
       'Saper 等指出 CRH 神經元也直接推動 orexin 神經元，所以壓力會把「油門」踩住。示意圖，依解剖教科書重繪；腎上腺比例放大，杏仁核位在顳葉內側，圖中為投影位置。')
write(P, 'Plate 1·D', '第三股力量：壓力軸與交感神經', 'The HPA axis and the sympathetic arm', 656, body,
      '半透明人體正面圖，顯示從腦的室旁核、腦下垂體到腎上腺的壓力軸，以及腎上腺與腎臟剖面放大', cap, defs=''.join(D))
