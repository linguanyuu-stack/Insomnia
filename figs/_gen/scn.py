import sys, os, math, random, io, contextlib
sys.path.insert(0, os.path.dirname(__file__))
from plib import *
with contextlib.redirect_stdout(io.StringIO()):
    import brain

P = 'pl-scn'
D = []
O = []
add = O.append
s = 0.58
BX, BY = 150, 178


def B(x, y):
    return (BX + (x - 178) * s, BY + (y - 245) * s)


PUR = '#6b4f9a'; ORA = '#d08a1e'; LIGHT = '#e8b923'; MEL = '#2c5d9c'

# ------------- head silhouette -------------
head = [(110, 356), (104, 346), (106, 336), (112, 328), (108, 322), (102, 318), (104, 313), (108, 310), (104, 306), (100, 302), (103, 297), (108, 292),
        (102, 289), (94, 286), (87, 282), (84, 275), (87, 266), (95, 248), (104, 228), (111, 212), (116, 204), (110, 194), (106, 186), (110, 168), (120, 141), (136, 106), (165, 77), (205, 57), (255, 47),
        (305, 49), (352, 63), (392, 93), (416, 133), (426, 176), (422, 220), (408, 258), (392, 282), (382, 306), (378, 340),
        (380, 400), (386, 470), (392, 548), (200, 548), (196, 470), (190, 416), (178, 389), (150, 377), (128, 370), (116, 364)]
head_d = cr(head, True, k=.8)
D.append('<clipPath id="%s-hc"><path d="%s"/></clipPath>' % (P, head_d))
D.append('<linearGradient id="%s-nf" x1="0" y1="0" x2="0" y2="1"><stop offset=".75" stop-color="#f6e4d4"/><stop offset="1" stop-color="#f6e4d4" stop-opacity="0"/></linearGradient>' % P)
add('<path d="%s" fill="url(#%s-nf)"/>' % (head_d, P))
add('<g clip-path="url(#%s-hc)">' % P)
add(shade(P + '-m1', head_d, -14, -4, 'ink-hatch-l', .8))
add('</g>')

# hair: strands following the scalp from hairline to nape
scalp = bez_pts([(122, 136), (136, 106), (165, 77), (205, 57), (255, 47), (305, 49), (352, 63), (392, 93), (416, 133), (426, 176), (422, 220), (410, 252)], per=10)
rnd = random.Random(4)
outer, inner = [], []
for i, (x, y) in enumerate(scalp):
    a, b = scalp[max(0, i - 1)], scalp[min(len(scalp) - 1, i + 1)]
    tx, ty = b[0] - a[0], b[1] - a[1]
    L = math.hypot(tx, ty) or 1
    nx, ny = -ty / L, tx / L      # outward (left of travel direction for this clockwise run)
    th = 9 * min(1, i / 8, (len(scalp) - 1 - i) / 10)
    outer.append((x + nx * th, y + ny * th)); inner.append((x - nx * 1.5, y - ny * 1.5))
hair_d = poly(outer + inner[::-1], True)
add('<path d="%s" fill="#8a6b4e" fill-opacity=".85"/>' % hair_d)
strands = ''
for k in range(70):
    i0 = rnd.randint(0, len(scalp) - 12)
    ln = rnd.randint(6, 14)
    fr = rnd.uniform(.15, .95)
    pts = [(inner[j][0] + (outer[j][0] - inner[j][0]) * fr, inner[j][1] + (outer[j][1] - inner[j][1]) * fr) for j in range(i0, min(len(scalp), i0 + ln))]
    strands += poly(pts)
add('<path d="%s" stroke="#f3e6d0" stroke-width=".5" stroke-opacity=".7" fill="none"/>' % strands)
add('<path d="%s" stroke="%s" stroke-width=".8" fill="none"/>' % (hair_d, INK))

# ------------- skull vault (from brain outline offsets) -------------
cer_m = [B(*p) for p in brain.cer[:16]] + [B(*p) for p in [(609, 330), (613, 355), (607, 382), (591, 405), (565, 424), (528, 434), (490, 438)]]
dense = bez_pts(cer_m, per=8)
o1, o2 = [], []
for i, (x, y) in enumerate(dense):
    a, b = dense[max(0, i - 1)], dense[min(len(dense) - 1, i + 1)]
    tx, ty = b[0] - a[0], b[1] - a[1]
    L = math.hypot(tx, ty) or 1
    nx, ny = ty / L, -tx / L
    o1.append((x + nx * 3, y + ny * 3)); o2.append((x + nx * 11.5, y + ny * 11.5))
sk = poly(o2 + o1[::-1], True)
add('<path d="%s" fill="%s"/><path d="%s" fill="url(#ink-stipple)" opacity=".6"/><path d="%s" class="ink2"/>' % (sk, BONE, sk, sk))
add('<path d="%s" class="ink" />' % poly(o2))
# orbital roof
add('<path d="%s" fill="%s" class="ink2"/>' % (cr([(136, 196), (152, 192), (172, 196), (186, 205), (184, 209), (170, 201), (152, 197), (138, 201)], True), BONE))

# ------------- brain (reused from plate 1-A, nuclei omitted) -------------
G = inline_classes('\n'.join(brain.G[:brain.NUC])).replace('pl-brain', P + '-b')
add('<g transform="translate(%s %s) scale(%s) translate(-178 -245)">%s</g>' % (BX, BY, s, G))
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.3"/>' % (cr([B(*p) for p in brain.cer], True), INK))

# ------------- cervical spine, cord -------------
# vertebral bodies (C2-T1) with discs
for i in range(8):
    y = 316 + i * 28.5
    x = 247 + 3 * math.sin(i / 7 * math.pi)
    h = 23 if i else 30
    yb = y - (8 if i == 0 else 0)
    vb = '<rect x="%s" y="%s" width="27" height="%s" rx="4" fill="%s"/>' % (f(x), f(yb), h, BONE)
    add(vb + '<rect x="%s" y="%s" width="27" height="%s" rx="4" fill="url(#ink-stipple)" opacity=".5"/>' % (f(x), f(yb), h)
        + '<rect x="%s" y="%s" width="27" height="%s" rx="4" class="ink2" stroke-width=".8"/>' % (f(x), f(yb), h))
    add('<rect x="%s" y="%s" width="25" height="4.5" rx="2" fill="#dfe7ee" class="ink2"/>' % (f(x + 1), f(yb + h + .5)))
    # spinous process
    sp = [(298, y + 2), (306, y - 2), (330 + i * 1.5, y + 12), (334 + i * 2, y + 20), (322, y + 18), (302, y + 16)]
    if i == 7:
        sp = [(298, y + 2), (306, y - 2), (345, y + 12), (348, y + 20), (330, y + 18), (302, y + 16)]
    add('<path d="%s" fill="%s"/><path d="%s" fill="url(#ink-stipple)" opacity=".5"/><path d="%s" class="ink2" stroke-width=".8"/>' % (cr(sp, True), BONE, cr(sp, True), cr(sp, True)))
# atlas anterior arch + dens
add('<ellipse cx="256" cy="300" rx="7" ry="5" fill="%s" class="ink2"/>' % BONE)
cord = [(270, 307), (276, 340), (277, 400), (278, 548), (292, 548), (292, 400), (292, 340), (295, 307)]
add('<path d="%s" fill="#f6edd8"/><path d="%s" fill="url(#ink-stipple-l)"/><path d="%s" class="ink"/>' % ((cr(cord, True),) * 3))
add('<path d="M285 312 L285 546" class="ink2" stroke-dasharray="1.5 2"/>')

# ------------- carotid, sympathetic chain, SCG -------------
ica = [(212, 548), (214, 470), (215, 420), (222, 360), (230, 310), (236, 272), (233, 246)]
add('<path d="%s" fill="none" stroke="%s" stroke-width="7.5" stroke-linecap="round"/>' % (cr(ica), INK))
add('<path d="%s" fill="none" stroke="%s" stroke-width="5.6" stroke-linecap="round"/>' % (cr(ica), '#c86454'))
add('<path d="%s" fill="none" stroke="#f4c9bd" stroke-width="1.6" stroke-linecap="round" transform="translate(-1 0)"/>' % cr(ica[:-1]))
eca = [(215, 425), (209, 392), (198, 362), (186, 340)]
add('<path d="%s" fill="none" stroke="%s" stroke-width="5.6" stroke-linecap="round"/><path d="%s" fill="none" stroke="#c86454" stroke-width="3.8" stroke-linecap="round"/>' % (cr(eca), INK, cr(eca)))
chain = [(237, 360), (238, 420), (239, 470), (240, 548)]
add('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round"/>' % (cr(chain), INK, cr(chain), NERVE))
for (cx, cy, rx, ry) in [(237, 343, 5, 18), (238, 440, 3.6, 7), (240, 516, 5, 9)]:
    add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" stroke="%s" stroke-width=".9"/><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#ink-stipple)" opacity=".6"/>' % (cx, cy, rx, ry, NERVE, INK, cx, cy, rx, ry))

# ------------- eye -------------
EC = (152, 218); ER = 19
add('<circle cx="%s" cy="%s" r="%s" fill="#fbf7ef" class="ink"/>' % (EC[0], EC[1], ER))
# choroid / retina layer (back of eye)
add('<path d="M%s %s A%s %s 0 0 1 %s %s" fill="none" stroke="#c86454" stroke-width="2.2" stroke-opacity=".75"/>' % (
    f(EC[0] + ER * math.cos(math.radians(-110)) - 1), f(EC[1] + ER * math.sin(math.radians(-110))), ER - 1.6, ER - 1.6,
    f(EC[0] + ER * math.cos(math.radians(110)) - 1), f(EC[1] + ER * math.sin(math.radians(110)))))
add('<path d="M%s %s A%s %s 0 0 1 %s %s" fill="none" stroke="%s" stroke-width="1.6"/>' % (
    f(EC[0] + (ER - 3) * math.cos(math.radians(-100))), f(EC[1] + (ER - 3) * math.sin(math.radians(-100))), ER - 3, ER - 3,
    f(EC[0] + (ER - 3) * math.cos(math.radians(100))), f(EC[1] + (ER - 3) * math.sin(math.radians(100))), ORA))
# cornea, iris, lens
add('<path d="M136 208 Q127 218 136 228" fill="#eef3f6" class="ink"/>')
add('<path d="M137 207 L139 213 M137 229 L139 223" stroke="%s" stroke-width="2.2"/>' % '#5b7aa0')
add('<ellipse cx="143" cy="218" rx="3.6" ry="6.5" fill="#f3efe3" class="ink2"/>')
add(shade(P + '-m2', 'M%s %s m-%s 0 a%s %s 0 1 0 %s 0 a%s %s 0 1 0 -%s 0' % (EC[0], EC[1], ER, ER, ER, 2 * ER, ER, ER, 2 * ER), 5, -5, 'ink-hatch-l', 1))
# eyelids/brow on the silhouette
add('<path d="M129 206 Q134 200 142 199" class="ink" /><path d="M129 230 Q134 235 141 236" class="ink2"/>')
add('<path d="M120 190 Q132 184 150 186" fill="none" stroke="#6b5440" stroke-width="2.6" stroke-linecap="round"/>')
# face details: nostril, lips line, ear hint none (sagittal)
add('<path d="M95 281 q4 -7 12 -4 q4 3 1 9" class="ink2"/><path d="M104 307 q4 1 8 -1" class="ink2"/><path d="M112 244 q8 12 4 26" class="ink2" stroke-opacity=".5"/><path d="M114 325 q6 2 8 -2" class="ink2" stroke-opacity=".6"/>')
# sternocleidomastoid (faint) and neck shading
add('<path d="%s" fill="none" stroke="%s" stroke-width=".7" stroke-opacity=".45"/>' % (cr([(352, 300), (320, 360), (270, 440), (220, 520), (205, 545)]), INK))
add('<path d="%s" fill="none" stroke="%s" stroke-width=".7" stroke-opacity=".45"/>' % (cr([(372, 318), (340, 380), (290, 460), (240, 540)]), INK))
add(ticks([(352, 300), (320, 360), (270, 440), (220, 520)], side=-1, step=3, l0=2, l1=6, w=.4, op=.35, seed=9))
# optic nerve (eye -> chiasm)
on = [(170, 214), (186, 212), (204, 209), (222, 205)]
add('<path d="%s" fill="none" stroke="%s" stroke-width="6.5" stroke-linecap="round"/><path d="%s" fill="none" stroke="#f2e8cf" stroke-width="4.6" stroke-linecap="round"/>' % (cr(on), INK, cr(on)))
# head contour on top
add('<path d="%s" class="ink3" clip-path="url(#%s-cut)"/>' % (head_d, P))
D.append('<clipPath id="%s-cut"><rect x="0" y="0" width="760" height="545"/></clipPath>' % P)

# ------------- the pathway -------------
SCN = B(321, 283); PVN = B(343, 254); PIN = B(470, 244); IML = (285, 522); SCG = (237, 343)
# light rays
for dy in (-9, 0, 9):
    add('<path d="M22 %s L126 %s" stroke="%s" stroke-width="2" stroke-dasharray="7 4" marker-end="url(#%s-al)"/>' % (f(212 + dy * 1.8), f(218 + dy * .7), LIGHT, P))
D.append('<marker id="%s-al" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 1L9 5L0 9z" fill="%s"/></marker>' % (P, LIGHT))
D.append('<marker id="%s-ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (P, RED))
D.append('<marker id="%s-ao" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (P, ORA))
D.append('<marker id="%s-ap" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (P, PUR))
# 2 RHT along optic nerve, into SCN
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.8" marker-end="url(#%s-ao)"/>' % (cr([(168, 216), (190, 213), (210, 208), (225, 204), (SCN[0] - 2, SCN[1] + 1)]), ORA, P))
# 3 SCN -> PVN
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" marker-end="url(#%s-ap)"/>' % (cr([(SCN[0] + 1, SCN[1] - 4), (SCN[0] + 6, SCN[1] - 12), (PVN[0] - 2, PVN[1] + 4)]), PUR, P))
# 4 PVN -> brainstem -> cord IML
desc = [(PVN[0] + 3, PVN[1] + 2), (258, 200), (268, 240), (276, 280), (282, 320), (283, 420), (284, IML[1] - 4)]
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.7" marker-end="url(#%s-ar)"/>' % (cr(desc), RED, P))
# preganglionic: IML -> stellate -> up the chain -> SCG
pre = [(283, 523), (262, 527), (243, 520), (240, 490), (238, 440), (237, 372)]
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.7" marker-end="url(#%s-ar)"/>' % (cr(pre), RED, P))
# 5 postganglionic: SCG -> along ICA -> pineal
post = [(236, 326), (233, 300), (240, 268), (252, 236), (276, 205), (300, 186), (PIN[0] - 6, PIN[1] + 3)]
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.7" stroke-dasharray="4 2.2" marker-end="url(#%s-ar)"/>' % (cr(post), RED, P))
# nuclei and pineal emphasis
add('<ellipse cx="%s" cy="%s" rx="4.6" ry="3.3" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(SCN[0]), f(SCN[1]), PUR, INK))
add('<ellipse cx="%s" cy="%s" rx="4.2" ry="3.2" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(PVN[0]), f(PVN[1]), RED, INK))
add('<circle cx="%s" cy="%s" r="3" fill="%s" stroke="%s" stroke-width=".7"/>' % (IML[0], IML[1], RED, INK))
# melatonin molecules leaving the pineal
rnd = random.Random(2)
for k in range(9):
    a = rnd.uniform(-60, 80); r = rnd.uniform(9, 22)
    x, y = PIN[0] + r * math.cos(math.radians(a)) + 4, PIN[1] + r * math.sin(math.radians(a)) + 4
    add('<circle cx="%s" cy="%s" r="1.9" fill="%s" stroke="#fff" stroke-width=".5"/>' % (f(x), f(y), MEL))


def num(x, y, n, col=INK):
    return ('<circle cx="%s" cy="%s" r="8" fill="%s" stroke="#fbf6ea" stroke-width="1.5"/>'
            '<text x="%s" y="%s" text-anchor="middle" style="font-size:11px;font-weight:700;fill:#fff;font-family:Georgia,serif">%s</text>') % (f(x), f(y), col, f(x), f(y + 3.8), n)


NUMS = [num(34, 196, 1, '#b8901a'), num(196, 225, 2, ORA), num(219, 172, 3, PUR), num(266, 300, 4, RED), num(258, 222, 5, RED)]

# ------------- retina magnifier (top-left) -------------
MC = (60, 78); MR = 47
D.append('<clipPath id="%s-mc"><circle cx="%s" cy="%s" r="%s"/></clipPath>' % (P, MC[0], MC[1], MR - 1))
R = ['<g clip-path="url(#%s-mc)"><g transform="translate(.34 .26) scale(.904)">' % P, '<rect x="10" y="30" width="120" height="120" fill="#f8efe0"/>']
# layers: (top=vitreous side, ganglion layer) -> (bottom photoreceptors, pigment epithelium)
R.append('<rect x="10" y="110" width="120" height="30" fill="#c86454" fill-opacity=".55"/><rect x="10" y="110" width="120" height="30" fill="url(#ink-hatch)"/>')
for i in range(17):
    x = 16 + i * 6.5
    R.append('<path d="M%s 110 v-14" stroke="%s" stroke-width="2.4" stroke-linecap="round"/><path d="M%s 110 v-14" stroke="#e9dcc0" stroke-width="1.3" stroke-linecap="round"/>' % (f(x), INK, f(x)))
R.append('<path d="M10 92 H130 M10 70 H130" stroke="%s" stroke-width=".5" stroke-dasharray="2 2" opacity=".6"/>' % INK)
for i in range(9):
    x = 18 + i * 12
    R.append('<circle cx="%s" cy="82" r="3" fill="#efe2cc" stroke="%s" stroke-width=".5"/>' % (f(x), INK))
# ordinary RGCs
for x in (30, 92, 110):
    R.append('<circle cx="%s" cy="60" r="4.2" fill="#efe2cc" stroke="%s" stroke-width=".6"/>' % (x, INK))
# ipRGC (gold) with dendrites, axon heading to optic nerve
R.append('<path d="M62 60 C58 66 50 72 44 80 M62 60 C66 68 74 72 80 80 M62 60 C60 70 62 76 60 86" stroke="%s" stroke-width="1.2" fill="none"/>' % GOLD)
R.append('<path d="M62 56 C70 48 90 44 130 42" stroke="%s" stroke-width="1.6" fill="none"/>' % GOLD)
R.append('<circle cx="62" cy="59" r="6" fill="#f2cf6a" stroke="%s" stroke-width=".8"/><circle cx="62.5" cy="59" r="2.2" fill="%s"/>' % (INK, '#7a5a12'))
R.append('<path d="M40 30 L58 54 M70 30 L64 52" stroke="%s" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#%s-al)"/>' % (LIGHT, P))
R.append('</g></g><circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1.6"/>' % (MC[0], MC[1], MR, INK))
R.append('<path d="M%s %s L168 212" class="ld" stroke-dasharray="3 2"/>' % (f(MC[0] + MR * .8), f(MC[1] + MR * .6)))
R.append('<text x="8" y="141" class="lb halo">ipRGC</text><text x="8" y="156" class="lb halo">感光節細胞</text><text x="8" y="170" class="le halo">含 melanopsin</text><text x="8" y="183" class="le halo">對藍光最敏感</text>')
R.append('<text x="22" y="252" class="lb halo" style="fill:#9a7412">光 Light</text>')

# ------------- right column labels -------------
RL = [
    dict(t=(PVN[0] + 1, PVN[1] - 2), zh='③ 室旁核 PVN', en='Paraventricular nucleus'),
    dict(t=(PIN[0] + 3, PIN[1] - 1), zh='⑤ 松果體 Pineal gland', en='→ 褪黑激素 melatonin'),
    dict(t=(SCN[0] + 2, SCN[1] + 1), zh='② 視交叉上核 SCN', en='Suprachiasmatic nucleus'),
    dict(t=(206, 209), zh='視神經・視網膜下視丘徑', en='Optic n. / retinohypothalamic tract', bias=6),
    dict(t=(236, 290), zh='頸內動脈', en='Internal carotid a. + 交感纖維'),
    dict(t=(240, 340), zh='④ 上頸神經節 SCG', en='Superior cervical ganglion'),
    dict(t=(272, 380), zh='頸椎椎體', en='Cervical vertebral body'),
    dict(t=(286, 420), zh='脊髓 Spinal cord', en='下行交感路徑 descending'),
    dict(t=(239, 470), zh='交感神經鏈', en='Sympathetic trunk'),
    dict(t=(IML[0] + 2, IML[1]), zh='④ 中間外側柱 IML', en='Intermediolateral column, T1–T2'),
]
LBL = column('R', 452, RL, 168, 540, gap=34.5)

# ------------- coronal inset (top-right) -------------
CX, CY = 600, 22
C = ['<rect x="456" y="14" width="296" height="138" rx="4" class="panel"/>',
     '<text x="464" y="31" class="lb">冠狀切面 <tspan class="le">Coronal section through the chiasm</tspan></text>']
tissue = [(535, 50), (560, 46), (585, 49), (600, 47), (615, 49), (640, 46), (665, 50), (668, 80), (662, 108), (650, 122), (636, 128), (600, 131), (564, 128), (550, 122), (538, 108), (532, 80)]
td = cr(tissue, True)
C.append('<path d="%s" fill="%s"/><path d="%s" fill="url(#ink-stipple-l)"/>' % (td, FLESH, td))
C.append(shade(P + '-m3', td, -6, -8, 'ink-hatch-l', 1))
C.append('<path d="%s" class="ink"/>' % td)
# wavy cut top edge
C.append('<path d="%s" class="ink2" stroke-dasharray="3 2"/>' % cr([(535, 50), (560, 46), (585, 49), (600, 47), (615, 49), (640, 46), (665, 50)]))
# third ventricle slit
v3 = [(597, 48), (603, 48), (603.5, 80), (602.5, 104), (604, 114), (600, 118), (596, 114), (597.5, 104), (596.5, 80)]
C.append('<path d="%s" fill="%s" class="ink"/>' % (cr(v3, True), '#d9e4ef'))
# PVN wings
for sgn in (-1, 1):
    pv = [(600 + sgn * 5, 60), (600 + sgn * 14, 63), (600 + sgn * 17, 74), (600 + sgn * 10, 82), (600 + sgn * 5, 78)]
    C.append('<path d="%s" fill="#e9a596" stroke="%s" stroke-width=".7"/>' % (cr(pv, True), INK))
    # fornix columns
    C.append('<circle cx="%s" cy="92" r="5.5" fill="#f8f0df" class="ink"/><circle cx="%s" cy="92" r="5.5" fill="url(#ink-hatch-h)" opacity=".6"/>' % (600 + sgn * 29, 600 + sgn * 29))
    # SCN
    C.append('<ellipse cx="%s" cy="112" rx="7.2" ry="6" fill="url(#%s-gp)" stroke="%s" stroke-width=".8"/>' % (600 + sgn * 10, P, INK))
D.append('<radialGradient id="%s-gp" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#d8c8ee"/><stop offset="1" stop-color="#6b4f9a"/></radialGradient>' % P)
# optic chiasm band
ch = [(548, 121), (575, 118), (600, 119), (625, 118), (652, 121), (655, 129), (628, 133), (600, 134), (572, 133), (545, 129)]
C.append('<path d="%s" fill="#f2e8cf"/><path d="%s" fill="url(#ink-hatch-r)" opacity=".6"/><path d="%s" class="ink"/>' % ((cr(ch, True),) * 3))
C.append(label('L', 528, 66, '室旁核 PVN', None, (588, 70), stub=6))
C.append(label('L', 528, 98, '穹窿 Fornix', None, (566, 93), stub=6))
C.append(label('L', 528, 124, '視交叉上核 SCN', None, (590, 112), stub=6))
C.append(label('R', 676, 66, '第三腦室', '3rd ventricle', (603, 72), stub=6))
C.append(label('R', 676, 118, '視交叉', 'Optic chiasm', (650, 126), stub=6))

# ------------- day / night panels -------------
def eye_icon(x, y, closed=False):
    if closed:
        return ('<path d="M%s %s q14 10 28 0" class="ink" stroke-width="1.4"/><path d="M%s %s l-2 5 M%s %s l0 6 M%s %s l2 5" class="ink2"/>'
                % (x - 14, y, x - 8, y + 4, x, y + 5, x + 8, y + 4))
    return ('<path d="M%s %s q14 -13 28 0 q-14 13 -28 0z" fill="#fbf7ef" class="ink" stroke-width="1.2"/><circle cx="%s" cy="%s" r="6" fill="#7d9bbd" class="ink2"/><circle cx="%s" cy="%s" r="2.6" fill="%s"/>'
            % (x - 14, y, x, y, x, y, INK))


def pine(x, y, on):
    d = cr([(x - 12, y), (x - 6, y - 9), (x + 4, y - 10), (x + 14, y - 4), (x + 15, y + 3), (x + 4, y + 9), (x - 7, y + 8)], True)
    g = '<path d="%s" fill="%s"/><path d="%s" fill="url(#ink-stipple)" opacity=".7"/><path d="%s" class="ink" stroke-width="1.2"/>' % (d, '#dcc29a' if on else '#e8dcc6', d, d)
    return g


def gang(x, y, on):
    return '<ellipse cx="%s" cy="%s" rx="11" ry="6" fill="%s" class="ink"/><ellipse cx="%s" cy="%s" rx="11" ry="6" fill="url(#ink-stipple)" opacity=".5"/>' % (x, y, NERVE if on else '#efe6cf', x, y)


def panel(x0, y0, night):
    w, h = 364, 194
    o = ['<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="%s" stroke="#bfae8a" stroke-width=".8"/>' % (x0, y0, w, h, '#e4e9f1' if night else '#fbf1cf')]
    if night:
        o.append('<text x="%s" y="%s" class="lt">夜晚 Night：黑暗 → 褪黑激素上升</text>' % (x0 + 12, y0 + 24))
        o.append('<path d="M%s %s a14 14 0 1 0 12 22 a11 11 0 1 1 -12 -22z" fill="#f3e7b5" stroke="%s" stroke-width="1"/>' % (x0 + 326, y0 + 12, INK))
        for (sx, sy) in [(x0 + 300, y0 + 18), (x0 + 350, y0 + 44), (x0 + 292, y0 + 40)]:
            o.append('<path d="M%s %s l1.2 3 3 1.2 -3 1.2 -1.2 3 -1.2 -3 -3 -1.2 3 -1.2z" fill="%s"/>' % (sx, sy - 4, '#b8901a'))
    else:
        o.append('<text x="%s" y="%s" class="lt">白天 Day：光 → 褪黑激素被關掉</text>' % (x0 + 12, y0 + 24))
        cx, cy = x0 + 332, y0 + 30
        o.append('<circle cx="%s" cy="%s" r="11" fill="#f6d55c" stroke="%s" stroke-width="1"/>' % (cx, cy, INK))
        for a in range(0, 360, 30):
            r1, r2 = 14, 20 if a % 60 == 0 else 17
            o.append('<path d="M%s %s L%s %s" stroke="#c99a1e" stroke-width="1.4" stroke-linecap="round"/>' % (
                f(cx + r1 * math.cos(math.radians(a))), f(cy + r1 * math.sin(math.radians(a))), f(cx + r2 * math.cos(math.radians(a))), f(cy + r2 * math.sin(math.radians(a)))))
    yi = y0 + 78
    xs = [x0 + 36, x0 + 104, x0 + 172, x0 + 240, x0 + 312]
    # icons
    o.append(eye_icon(xs[0], yi, closed=night))
    if not night:
        for dy in (-8, 0, 8):
            o.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="1.6" stroke-dasharray="4 2.5" marker-end="url(#%s-al)"/>' % (x0 + 4, yi - 16 + dy, xs[0] - 15, yi + dy * .4, LIGHT, P))
    o.append('<ellipse cx="%s" cy="%s" rx="7" ry="6" fill="url(#%s-gp)" stroke="%s" stroke-width=".8"/><ellipse cx="%s" cy="%s" rx="7" ry="6" fill="url(#%s-gp)" stroke="%s" stroke-width=".8"/>' % (
        xs[1] - 8, yi, P, INK, xs[1] + 8, yi, P, INK))
    o.append('<ellipse cx="%s" cy="%s" rx="10" ry="7" fill="%s" stroke="%s" stroke-width=".9"/>' % (xs[2], yi, '#e9a596' if night else '#f0e3dc', INK))
    o.append(gang(xs[3], yi, night))
    o.append(pine(xs[4], yi, night))
    # connectors
    col_on = RED
    if night:
        o.append('<path d="M%s %s H%s" stroke="#9a8a70" stroke-width="1.2" stroke-dasharray="2 2"/>' % (xs[0] + 16, yi, xs[1] - 17))
        o.append('<path d="M%s %s H%s" stroke="#9a8a70" stroke-width="1.2" stroke-dasharray="2 2" marker-end="url(#%s-teeg)"/>' % (xs[1] + 17, yi, xs[2] - 13, P))
        for a, b in ((xs[2] + 11, xs[3] - 13), (xs[3] + 12, xs[4] - 14)):
            o.append('<path d="M%s %s H%s" stroke="%s" stroke-width="2" marker-end="url(#%s-ar)"/>' % (a, yi, b, col_on, P))
    else:
        o.append('<path d="M%s %s H%s" stroke="%s" stroke-width="2" marker-end="url(#%s-ao)"/>' % (xs[0] + 16, yi, xs[1] - 17, ORA, P))
        o.append('<path d="M%s %s H%s" stroke="%s" stroke-width="2.2" marker-end="url(#%s-teep)"/>' % (xs[1] + 17, yi, xs[2] - 13, PUR, P))
        for a, b in ((xs[2] + 11, xs[3] - 13), (xs[3] + 12, xs[4] - 14)):
            o.append('<path d="M%s %s H%s" stroke="#a89a80" stroke-width="1.2" stroke-dasharray="2 3"/>' % (a, yi, b))
    names = [('眼', 'retina'), ('SCN', '時鐘'), ('PVN', '室旁核'), ('SCG', '上頸神經節'), ('松果體', 'pineal')]
    for (zh, en), x in zip(names, xs):
        o.append('<text x="%s" y="%s" text-anchor="middle" class="ls" style="font-weight:600">%s</text><text x="%s" y="%s" text-anchor="middle" class="le">%s</text>' % (x, yi + 25, zh, x, yi + 38, en))
    for i, x in enumerate([(xs[0] + xs[1]) / 2, (xs[1] + xs[2]) / 2, (xs[2] + xs[3]) / 2, (xs[3] + xs[4]) / 2]):
        o.append(num(x, yi - 16, '②③④⑤'[i] and i + 2, [ORA, PUR, RED, RED][i]).replace('r="8"', 'r="7"'))
    o.append(num(xs[0] - 20, yi - 18, 1, '#b8901a').replace('r="8"', 'r="7"') if not night else '')
    # capillary with melatonin
    vy = y0 + 140
    o.append('<path d="M%s %s H%s M%s %s H%s" stroke="%s" stroke-width="1.1"/>' % (x0 + 18, vy, x0 + w - 18, x0 + 18, vy + 18, x0 + w - 18, INK))
    o.append('<rect x="%s" y="%s" width="%s" height="18" fill="#f3d3c9" fill-opacity=".7"/>' % (x0 + 18, vy, w - 36))
    rr = random.Random(5)
    for k in range(9):
        o.append('<ellipse cx="%s" cy="%s" rx="4" ry="2.3" fill="#d9705f" fill-opacity=".55" stroke="#a8412c" stroke-width=".4"/>' % (f(x0 + 30 + k * 36 + rr.uniform(-6, 6)), f(vy + 9 + rr.uniform(-4, 4))))
    nmel = 22 if night else 2
    for k in range(nmel):
        mx = x0 + 26 + rr.uniform(0, w - 52) if night else x0 + 250 + k * 40
        o.append('<circle cx="%s" cy="%s" r="2.4" fill="%s" stroke="#fff" stroke-width=".5"/>' % (f(mx), f(vy + 9 + rr.uniform(-5, 5)), MEL))
    if night:
        o.append('<path d="M%s %s V%s" stroke="%s" stroke-width="1.8" fill="none" marker-end="url(#%s-ab)"/>' % (xs[4] + 24, yi + 6, vy - 2, MEL, P))
    o.append('<text x="%s" y="%s" class="ls" style="fill:%s;font-weight:600">%s</text>' % (x0 + 22, vy - 5, MEL, '血中褪黑激素 ↑↑（凌晨 2–4 點最高）' if night else '血中褪黑激素 ≈ 0'))
    txt = ('SCN 放開 PVN → 交感神經 → 松果體釋放褪黑激素' if night else '光經 ipRGC → SCN 興奮 → 壓住 PVN → 交感訊號關閉')
    o.append('<text x="%s" y="%s" class="ls">%s</text>' % (x0 + 18, y0 + h - 10, txt))
    return '\n'.join(o)


D.append('<marker id="%s-teep" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M5 0V10" stroke="%s" stroke-width="2.6"/></marker>' % (P, PUR))
D.append('<marker id="%s-teeg" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M5 0V10" stroke="#9a8a70" stroke-width="2"/></marker>' % P)
D.append('<marker id="%s-ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (P, MEL))
PAN = [panel(12, 562, False), panel(384, 562, True)]

body = inline_classes('\n'.join(O) + '\n' + '\n'.join(NUMS) + '\n' + '\n'.join(R) + '\n' + LBL + '\n' + '\n'.join(C) + '\n' + '\n'.join(PAN))
cap = ('<b>圖 1-B　視交叉上核：身體的主時鐘。</b>①光進入眼睛，被含 melanopsin 的視網膜感光節細胞（ipRGC）接收；②訊號沿視神經中的視網膜下視丘徑送到緊貼視交叉上方的 SCN；'
       '③SCN 把時間訊號交給室旁核 PVN；④PVN 經腦幹、脊髓下行到上胸段的中間外側柱，再出到交感神經鏈、往上到上頸神經節；⑤節後纖維沿頸內動脈回到顱內支配松果體。'
       '白天光線讓 SCN 壓住這條路，褪黑激素幾乎不分泌；天黑後路徑打開，褪黑激素才上升。示意圖，依解剖與生理教科書重繪；眼睛與交感神經鏈其實在中線外側，這裡投影到同一個矢狀面。')
write(P, 'Plate 1·B', '視交叉上核：身體的主時鐘', "The suprachiasmatic nucleus — the body's master clock", 766, body,
      '頭部側面剖面圖，顯示光線經視網膜、視交叉上核、室旁核、脊髓與上頸神經節到松果體的路徑，並比較白天與夜晚的褪黑激素分泌', cap, defs=''.join(D))
