import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
from plib import *

P = 'pl-brain'
D = []          # defs
G = []          # main reusable drawing group (also used by inset)
M = []          # main-only overlay
add = G.append

CORTEX = '#f1e2d2'; CUT = '#f8f0df'; VENT = '#d9e4ef'; HYPO = '#f2d0c3'; THAL = '#ecd5c2'

# ---------------- cerebrum (medial surface) ----------------
cer = [(178, 245), (182, 205), (198, 165), (226, 126), (262, 97), (306, 77), (356, 64), (408, 61), (457, 68), (503, 86),
       (545, 113), (578, 148), (600, 190), (612, 232), (611, 265), (597, 287), (566, 295), (532, 296), (500, 294),
       (472, 312), (432, 330), (398, 342), (368, 350), (346, 346), (336, 334), (330, 312), (310, 302), (275, 298),
       (240, 290), (205, 276), (186, 262)]
cer_d = cr(cer, closed=True)
add('<path d="%s" fill="%s"/>' % (cer_d, CORTEX))
add('<path d="%s" fill="url(#ink-stipple-l)" opacity=".55"/>' % cer_d)
add(shade(P + '-m1', cer_d, -16, -14, 'ink-hatch', .55))
add(shade(P + '-m2', cer_d, -6, -5, 'ink-hatch-d', .6))

# sulci (main line + engraved ticks on one side)
sulci = [
    # cingulate sulcus with marginal ramus
    ([(305, 252), (284, 228), (274, 198), (283, 166), (308, 141), (350, 127), (400, 122), (440, 124), (461, 116), (469, 95), (471, 70)], 1, 1.3),
    # paracentral sulcus
    ([(372, 124), (369, 104), (374, 84), (372, 64)], -1, 1.0),
    # central sulcus notch
    ([(428, 62), (433, 75), (429, 88)], 1, 1.0),
    # parieto-occipital
    ([(560, 120), (551, 150), (538, 186), (522, 218), (508, 238)], 1, 1.3),
    # calcarine
    ([(606, 262), (580, 254), (548, 246), (520, 240), (498, 238)], 1, 1.3),
    # subparietal
    ([(476, 142), (496, 152), (516, 146), (526, 132)], -1, 1.0),
    # frontal medial tertiary sulci
    ([(200, 212), (222, 222), (246, 218), (262, 226)], 1, .9),
    ([(206, 168), (230, 178), (254, 172), (268, 160)], 1, .9),
    ([(248, 118), (262, 133), (288, 130), (304, 120)], 1, .9),
    ([(318, 92), (332, 104), (352, 100)], 1, .9),
    # superior rostral
    ([(206, 255), (236, 262), (266, 262), (292, 268)], -1, .9),
    # precuneus / cuneus / lingual minor
    ([(492, 120), (506, 132), (512, 112)], 1, .8),
    ([(526, 190), (546, 198), (560, 214)], -1, .8),
    ([(572, 196), (586, 214), (596, 238)], 1, .8),
    ([(548, 274), (570, 272), (592, 278)], 1, .8),
    ([(522, 276), (532, 286)], 1, .8),
    ([(190, 236), (208, 241), (224, 250)], 1, .8),
    ([(228, 142), (244, 150), (242, 166)], -1, .8),
    ([(396, 84), (410, 95), (406, 110)], 1, .8),
    ([(486, 182), (500, 193), (513, 180)], 1, .8),
    ([(330, 76), (322, 90)], 1, .7),
    ([(574, 160), (586, 178)], -1, .7),
]
for i, (pts, side, w) in enumerate(sulci):
    add(ticks(pts, side=side, step=2.6, l0=2, l1=6.5, w=.45, op=.6, seed=i))
    add('<path d="%s" class="ink" stroke-width="%s"/>' % (cr(pts), w))
add('<path d="%s" class="ink3"/>' % cer_d)

# ---------------- septum pellucidum ----------------
sept = [(430, 176), (380, 172), (340, 177), (316, 190), (308, 206), (313, 221), (322, 233), (332, 216), (356, 201), (392, 195), (430, 199), (452, 205)]
add('<path d="%s" fill="#ece3d6"/><path d="%s" fill="url(#ink-stipple-l)"/>' % (cr(sept, True), cr(sept, True)))

# ---------------- corpus callosum (cut) ----------------
cc_out = [(318, 233), (302, 222), (289, 203), (292, 182), (308, 166), (335, 156), (380, 150), (430, 151), (470, 158), (497, 173), (507, 194), (501, 214), (486, 224), (470, 222)]
cc_in = [(463, 211), (456, 192), (432, 176), (380, 171), (340, 176), (315, 189), (307, 205), (312, 220), (320, 230)]
cc = cc_out + cc_in
cc_d = cr(cc, True)
add('<path d="%s" fill="%s"/>' % (cc_d, CUT))
# fibre lines parallel to the arch
for k in range(1, 5):
    t = k / 5
    pts = [(a[0] * (1 - t) + b[0] * t, a[1] * (1 - t) + b[1] * t) for a, b in zip(
        [(305, 214), (296, 196), (306, 172), (336, 160), (380, 154), (430, 155), (468, 162), (492, 178), (500, 196)],
        [(315, 212), (310, 200), (318, 186), (342, 174), (380, 169), (430, 172), (455, 182), (466, 196), (480, 214)])]
    add('<path d="%s" class="ink2" stroke-opacity=".35"/>' % cr(pts))
add('<path d="%s" class="ink"/>' % cc_d)
# callosal sulcus
add('<path d="%s" class="ink2"/>' % cr([(300, 228), (284, 205), (286, 180), (305, 160), (335, 150), (380, 145), (430, 146), (472, 152), (500, 168), (512, 193), (506, 216)]))

# ---------------- diencephalon ----------------
v3 = [(311, 287), (314, 266), (316, 248), (322, 234), (338, 232), (362, 214), (400, 209), (440, 212), (458, 222), (455, 238),
      (450, 252), (420, 266), (390, 282), (362, 297), (350, 300), (336, 302), (329, 303), (318, 290)]
add('<path d="%s" fill="%s"/>' % (cr(v3, True), VENT))
thal = [(340, 234), (350, 221), (378, 213), (415, 212), (446, 217), (457, 230), (452, 245), (442, 254), (415, 252), (385, 249), (358, 244)]
thal_d = cr(thal, True)
add('<path d="%s" fill="%s"/>' % (thal_d, THAL))
add(shade(P + '-m3', thal_d, -5, -6, 'ink-hatch-l', 1))
add('<path d="%s" class="ink"/>' % thal_d)
# interthalamic adhesion (cut)
add('<ellipse cx="398" cy="232" rx="9" ry="6.5" fill="%s" class="ink2"/><ellipse cx="398" cy="232" rx="9" ry="6.5" fill="url(#ink-hatch-h)"/>' % CUT)
# stria medullaris + habenula
add('<path d="%s" class="ink2"/>' % cr([(352, 223), (390, 215), (430, 216), (452, 226)]))
add('<ellipse cx="452" cy="233" rx="4" ry="3.2" fill="#e6c9b2" class="ink2"/>')
hypo = [(316, 250), (338, 241), (366, 247), (396, 255), (410, 262), (390, 281), (362, 296), (350, 300), (336, 302), (329, 303), (318, 290), (313, 270)]
hypo_d = cr(hypo, True)
add('<path d="%s" fill="%s"/>' % (hypo_d, HYPO))
add(shade(P + '-m4', hypo_d, -4, -6, 'ink-hatch-l', 1))
add('<path d="%s" class="ink2"/>' % hypo_d)
# hypothalamic sulcus
add('<path d="%s" class="ink" stroke-dasharray="0"/>' % cr([(338, 238), (366, 246), (400, 253), (430, 257), (447, 258)]))
# lamina terminalis
add('<path d="%s" class="ink"/>' % cr([(321, 236), (316, 252), (313, 270), (311, 285)]))
# post-commissural fornix through hypothalamus (dashed)
add('<path d="%s" class="ink2" stroke-dasharray="2 2"/>' % cr([(334, 238), (338, 258), (344, 278), (349, 292)]))
# choroid plexus on roof
cp = []
for i in range(30):
    x = 352 + i * 3.4
    cp.append((x, 214 + (i % 2) * 2.4 + (x - 352) * 0.02))
add('<path d="%s" fill="none" stroke="#a8412c" stroke-width=".7" stroke-opacity=".7"/>' % cr(cp))

# fornix
fx_top = [(470, 216), (440, 199), (392, 194), (356, 199), (333, 214), (323, 232)]
fx_bot = [(331, 238), (340, 222), (360, 210), (392, 205), (436, 209), (462, 222)]
fx_d = cr(fx_top + fx_bot, True)
add('<path d="%s" fill="%s"/><path d="%s" fill="url(#ink-hatch-h)" opacity=".5"/><path d="%s" class="ink"/>' % (fx_d, '#f3ead6', fx_d, fx_d))
# anterior & posterior commissure
add('<ellipse cx="319" cy="241" rx="4.6" ry="4" fill="%s" class="ink"/><ellipse cx="319" cy="241" rx="4.6" ry="4" fill="url(#ink-hatch-d)" opacity=".6"/>' % CUT)

# ---------------- brainstem (cut) ----------------
bs = [(362, 297), (367, 306), (362, 313), (347, 328), (341, 350), (347, 372), (363, 388), (371, 402), (377, 432), (383, 470),
      (428, 470), (434, 442), (440, 420), (447, 404), (452, 385), (457, 360), (462, 335), (466, 315), (469, 304),
      (482, 297), (487, 286), (483, 276), (485, 265), (478, 255), (466, 252), (452, 252), (420, 266), (390, 282)]
bs_d = cr(bs, True)
add('<path d="%s" fill="%s"/>' % (bs_d, CUT))
add('<path d="%s" fill="url(#ink-stipple-l)" opacity=".8"/>' % bs_d)
# basilar pons transverse fibres
pons = [(364, 312), (347, 328), (341, 350), (347, 372), (363, 388), (392, 384), (398, 350), (393, 316)]
add('<clipPath id="%s-cp1"><path d="%s"/></clipPath>' % (P, cr(pons, True)))
pf = ''
for i in range(26):
    y = 309 + i * 3.1
    pf += 'M340 %s q30 %s 64 %s ' % (f(y), f(-2 + (i % 3)), f(1.5))
add('<path clip-path="url(#%s-cp1)" d="%s" stroke="%s" stroke-width=".5" stroke-opacity=".55" fill="none"/>' % (P, pf, INK))
add('<path d="%s" class="ink2" stroke-opacity=".6"/>' % cr([(367, 312), (392, 318), (398, 350), (392, 384), (370, 390)]))
# longitudinal fibres in medulla & tegmentum
for k in range(5):
    x0 = 380 + k * 9
    add('<path d="%s" class="ink2" stroke-opacity=".3"/>' % cr([(x0 - 4, 388), (x0, 420), (x0 + 3, 468)]))
for k in range(4):
    add('<path d="%s" class="ink2" stroke-opacity=".3"/>' % cr([(372 + k * 10, 300 - k * 4), (395 + k * 12, 310), (410 + k * 10, 360), (412 + k * 6, 385)]))
# medullary cut end
add('<ellipse cx="405.5" cy="470" rx="22.5" ry="4.5" fill="#efe3c9" class="ink"/>')
add('<path d="M403 467 l1 6 M408 467 l-1 6" class="ink2"/>')
add('<path d="%s" class="ink2" stroke-dasharray="2 2"/>' % cr([(405, 470), (408, 420), (448, 404)]))
# tectum: colliculi divisions
add('<path d="M482 276 q-6 -2 -10 2" class="ink2"/>')
add(shade(P + '-m5', bs_d, -5, 0, 'ink-hatch-l', .8))
add('<path d="%s" class="ink"/>' % bs_d)
# cerebral aqueduct
aq1 = [(446, 257), (454, 268), (461, 283), (467, 300)]
aq2 = [(450, 255), (458, 266), (465, 281), (472, 298)]
add('<path d="%s" fill="%s" class="ink2"/>' % (poly(bez_pts(aq1) + list(reversed(bez_pts(aq2))), True), VENT))
# 4th ventricle
v4 = [(468, 303), (478, 311), (490, 324), (500, 336), (494, 350), (484, 368), (470, 388), (452, 402), (452, 385), (457, 360), (462, 335), (466, 315)]
v4_d = cr(v4, True)
add('<path d="%s" fill="%s"/><path d="%s" class="ink"/>' % (v4_d, VENT, v4_d))
cp2 = [(492, 352), (488, 360), (484, 366), (480, 374), (474, 382)]
add('<path d="%s" fill="none" stroke="#a8412c" stroke-width="1.1" stroke-dasharray="1.5 1.2" stroke-opacity=".7"/>' % cr(cp2))

# ---------------- pineal ----------------
pin = [(452, 240), (464, 236), (476, 239), (484, 244), (477, 249), (463, 251), (454, 249)]
pin_d = cr(pin, True)
add('<path d="%s" fill="#dcc29a"/><path d="%s" fill="url(#ink-stipple)" opacity=".7"/><path d="%s" class="ink"/>' % (pin_d, pin_d, pin_d))
add('<ellipse cx="450" cy="253" rx="3.6" ry="3" fill="%s" class="ink2"/>' % CUT)

# ---------------- cerebellum ----------------
cb = [(476, 303), (488, 299), (512, 299), (542, 298), (571, 302), (595, 312), (609, 330), (613, 355), (607, 382), (591, 405),
      (565, 421), (535, 428), (510, 424), (494, 415), (482, 405), (476, 395), (484, 376), (492, 356), (500, 338), (490, 325), (480, 312)]
dense = bez_pts(cb, closed=True, per=14)
C = (522, 352)
# scalloped (folia) outer contour except the ventricular face
out = []
acc = 0
for i, (x, y) in enumerate(dense):
    a, b = dense[i - 1], dense[(i + 1) % len(dense)]
    tx, ty = b[0] - a[0], b[1] - a[1]
    L = math.hypot(tx, ty) or 1
    nx, ny = ty / L, -tx / L   # outward for clockwise contour
    acc += math.dist(dense[i - 1], (x, y)) if i else 0
    free = not (x < 503 and 300 < y < 412)
    amp = 1.6 * abs(math.sin(acc / 4.2 * math.pi)) if free else 0
    out.append((x + nx * amp, y + ny * amp))
cb_d = poly(out, True)
add('<path d="%s" fill="#ead4c2"/><path d="%s" fill="url(#ink-stipple-l)"/>' % (cb_d, cb_d))
add(shade(P + '-m6', cb_d, -12, -10, 'ink-hatch', .6))
# arbor vitae
rnd = random.Random(7)
wm_ink, wm_fill, fiss = [], [], []
prim = [-150, -128, -104, -80, -56, -32, -8, 16, 40, 64, 90, 116]
for ai, a in enumerate(prim):
    R = ray_hit(out, C, a)
    L1 = R * 0.5
    p1 = (C[0] + L1 * math.cos(math.radians(a)), C[1] + L1 * math.sin(math.radians(a)))
    segs = [(C, p1, 5.2)]
    for b in (-14, 0, 13) if R > 55 else (-11, 11):
        aa = a + b + rnd.uniform(-3, 3)
        R2 = ray_hit(out, p1, aa)
        L2 = R2 * 0.62
        p2 = (p1[0] + L2 * math.cos(math.radians(aa)), p1[1] + L2 * math.sin(math.radians(aa)))
        segs.append((p1, p2, 2.6))
        for cdel in (-9, 9):
            R3 = ray_hit(out, p2, aa + cdel)
            L3 = R3 * 0.6
            p3 = (p2[0] + L3 * math.cos(math.radians(aa + cdel)), p2[1] + L3 * math.sin(math.radians(aa + cdel)))
            segs.append((p2, p3, 1.2))
    for (u, v, w) in segs:
        d = 'M%s %sL%s %s' % (f(u[0]), f(u[1]), f(v[0]), f(v[1]))
        wm_ink.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (d, INK, f(w + 1.3)))
        wm_fill.append('<path d="%s" stroke="#fbf3e2" stroke-width="%s" stroke-linecap="round"/>' % (d, f(w)))
    # fissure between this primary and next
    if ai < len(prim) - 1:
        am = (a + prim[ai + 1]) / 2
        Rm = ray_hit(out, C, am)
        deep = 0.62 if ai in (2, 6, 9) else 0.3
        q0 = (C[0] + Rm * math.cos(math.radians(am)), C[1] + Rm * math.sin(math.radians(am)))
        q1 = (C[0] + Rm * (1 - deep) * math.cos(math.radians(am)), C[1] + Rm * (1 - deep) * math.sin(math.radians(am)))
        fiss.append('<path d="M%s %sL%s %s" class="ink2" stroke-opacity=".8"/>' % (f(q0[0]), f(q0[1]), f(q1[0]), f(q1[1])))
add('<g fill="none">' + ''.join(wm_ink) + '<ellipse cx="%s" cy="%s" rx="15" ry="11" fill="%s"/>' % (C[0] - 2, C[1], INK) + ''.join(wm_fill)
    + '<ellipse cx="%s" cy="%s" rx="13.8" ry="9.8" fill="#fbf3e2"/></g>' % (C[0] - 2, C[1]))
add(''.join(fiss))
add('<path d="%s" class="ink"/>' % cb_d)
# tentorium cerebelli (dura) line
add('<path d="%s" fill="none" stroke="%s" stroke-width=".8" stroke-dasharray="5 2 1 2" opacity=".7"/>' % (cr([(488, 297), (530, 297), (575, 299), (606, 312)]), INK))

# ---------------- optic chiasm & nerve, pituitary, sella ----------------
add('<path d="%s" fill="#f2e8cf" class="ink"/>' % cr([(304, 289), (284, 298), (262, 305), (260, 313), (285, 307), (306, 298)], True))
add('<ellipse cx="261" cy="309" rx="3" ry="4.2" fill="#e5d6b2" class="ink2"/>')
add('<g transform="rotate(-22 311 291)"><ellipse cx="311" cy="291" rx="9.5" ry="5.5" fill="%s" class="ink"/><ellipse cx="311" cy="291" rx="9.5" ry="5.5" fill="url(#ink-hatch-r)" opacity=".7"/></g>' % CUT)
# sella turcica (sphenoid bone)
sel = [(290, 316), (294, 336), (308, 349), (328, 351), (343, 342), (347, 324), (349, 308), (343, 307), (340, 322), (334, 338), (320, 343), (305, 337), (298, 318)]
sel_d = cr(sel, True)
add('<path d="%s" fill="%s"/><path d="%s" fill="url(#ink-cross)" opacity=".5"/><path d="%s" class="ink"/>' % (sel_d, BONE, sel_d, sel_d))
# infundibulum + pituitary
add('<path d="%s" fill="%s" class="ink2"/>' % (cr([(327, 301), (333, 301), (330, 314), (326, 322), (321, 320), (324, 310)], True), HYPO))
ant = [(301, 323), (308, 316), (318, 316), (324, 322), (324, 333), (316, 339), (306, 337), (300, 331)]
pos = [(323, 320), (330, 317), (337, 322), (337, 332), (330, 338), (322, 336)]
add('<path d="%s" fill="#e9b4a2"/><path d="%s" fill="url(#ink-stipple)" opacity=".6"/><path d="%s" class="ink"/>' % ((cr(ant, True),) * 3))
add('<path d="%s" fill="#f1dfc0"/><path d="%s" fill="url(#ink-hatch-l)"/><path d="%s" class="ink"/>' % ((cr(pos, True),) * 3))
# mammillary body
add('<circle cx="350" cy="297" r="6.2" fill="#ecc9b6" class="ink"/><path d="M346 299 a4 4 0 0 0 7 0" class="ink2"/>')

# ---------------- nuclei ----------------
NUC = len(G)
N = {
    'MnPO': ((324, 252), BLUE), 'VLPO': ((318, 269), BLUE), 'SCN': ((321, 283), '#7a5aa6'),
    'ORX': ((344, 266), GOLD), 'TMN': ((363, 285), RED),
    'DR': ((446, 289), RED), 'LDT': ((452, 306), RED), 'LC': ((457, 326), RED),
}
D.append('<radialGradient id="%s-gb" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#a9c3e6"/><stop offset="1" stop-color="#2c5d9c"/></radialGradient>' % P)
D.append('<radialGradient id="%s-gr" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#f1b4a6"/><stop offset="1" stop-color="#a8412c"/></radialGradient>' % P)
D.append('<radialGradient id="%s-gg" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#fbe6a6"/><stop offset="1" stop-color="#c9962e"/></radialGradient>' % P)
D.append('<radialGradient id="%s-gp" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#d8c8ee"/><stop offset="1" stop-color="#6b4f9a"/></radialGradient>' % P)
grad = {BLUE: P + '-gb', RED: P + '-gr', GOLD: P + '-gg', '#7a5aa6': P + '-gp'}
for k, ((x, y), c) in N.items():
    rx, ry = (6.5, 4.6) if k not in ('LC', 'DR') else (5.5, 4.4)
    add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)" stroke="%s" stroke-width=".7"/>' % (x, y, rx, ry, grad[c], INK))

# ---------------- main-only overlay: ascending arousal + zoom box ----------------
asc = [
    [(452, 312), (436, 282), (420, 256), (404, 236)],
    [(447, 316), (420, 296), (388, 288), (352, 270), (318, 226), (276, 196)],
]
for pts in asc:
    M.append('<path d="%s" fill="none" stroke="%s" stroke-width="7" stroke-opacity=".22" stroke-linecap="round"/>' % (cr(pts), RED))
    M.append('<path d="%s" fill="none" stroke="%s" stroke-width=".9" stroke-dasharray="3 2.5" marker-end="url(#ink-arrow-red)"/>' % (cr(pts), TCM))

ZX, ZY, ZW, ZH = 296, 229, 182, 112
M.append('<rect x="%s" y="%s" width="%s" height="%s" class="panel" stroke="#8a6a3a"/>' % (ZX, ZY, ZW, ZH))

# lobe names inside the cortex
M.append('<text x="282" y="106" class="ls halo" font-style="italic">額葉</text>')
M.append('<text x="414" y="104" class="ls halo" font-style="italic">頂葉</text>')
M.append('<text x="560" y="230" class="ls halo" font-style="italic" text-anchor="middle">枕葉</text>')
M.append('<text x="196" y="44" class="ls">前 Anterior</text><path d="M190 40 h-20" class="ink" marker-end="url(#ink-arrow)"/>')
M.append('<text x="540" y="44" class="ls" text-anchor="end">後 Posterior</text><path d="M546 40 h20" class="ink" marker-end="url(#ink-arrow)"/>')

# ---------------- labels: main ----------------
L = [
    dict(t=(330, 143), zh='扣帶迴', en='Cingulate gyrus'),
    dict(t=(296, 196), zh='胼胝體（膝部）', en='Corpus callosum'),
    dict(t=(322, 203), zh='透明中隔', en='Septum pellucidum'),
    dict(t=(356, 204), zh='穹窿', en='Fornix'),
    dict(t=(318, 241), zh='前連合', en='Anterior commissure'),
    dict(t=(305, 293), zh='視交叉', en='Optic chiasm'),
    dict(t=(272, 305), zh='視神經', en='Optic nerve'),
    dict(t=(310, 330), zh='腦下垂體', en='Pituitary (hypophysis)', bias=10),
    dict(t=(352, 300), zh='乳頭體', en='Mammillary body', bias=12),
    dict(t=(362, 352), zh='橋腦', en='Pons'),
]
R = [
    dict(t=(549, 160), zh='頂枕溝', en='Parieto-occipital sulcus'),
    dict(t=(424, 222), zh='視丘', en='Thalamus'),
    dict(t=(476, 243), zh='松果體', en='Pineal gland'),
    dict(t=(586, 256), zh='距狀溝', en='Calcarine sulcus'),
    dict(t=(426, 262), zh='第三腦室', en='Third ventricle'),
    dict(t=(484, 268), zh='中腦頂蓋', en='Tectum (colliculi)'),
    dict(t=(464, 289), zh='中腦導水管', en='Cerebral aqueduct'),
    dict(t=(487, 346), zh='第四腦室', en='Fourth ventricle'),
    dict(t=(566, 372), zh='小腦（活樹）', en='Cerebellum, arbor vitae'),
    dict(t=(408, 445), zh='延腦', en='Medulla oblongata'),
]
M.append(column('L', 152, L, 92, 452, gap=33))
M.append(column('R', 626, R, 128, 470, gap=33))

# legend (top-left)
def sw(x, y, g, zh, en):
    return ('<ellipse cx="%s" cy="%s" rx="7" ry="5" fill="url(#%s)" stroke="%s" stroke-width=".7"/>'
            '<text x="%s" y="%s" class="lb">%s</text><text x="%s" y="%s" class="le">%s</text>') % (x, y, g, INK, x + 13, y + 4.5, zh, x + 13, y + 18, en)

# ---------------- inset (magnified diencephalon & brainstem) ----------------
S = 1.7
IX, IY = 302, 498
def T(p):
    return (IX + (p[0] - ZX) * S, IY + (p[1] - ZY) * S)
I = []
D.append('<clipPath id="%s-zc"><rect x="%s" y="%s" width="%s" height="%s"/></clipPath>' % (P, ZX, ZY, ZW, ZH))
I.append('<g transform="translate(%s %s) scale(%s) translate(%s %s)"><g clip-path="url(#%s-zc)"><use href="#%s-g"/></g></g>' % (IX, IY, S, -ZX, -ZY, P, P))
I.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="#8a6a3a" stroke-width="1"/>' % (IX, IY, ZW * S, ZH * S))
I.append('<text x="%s" y="%s" class="ls halo" text-anchor="end">放大 ×1.7　Magnified</text>' % (IX + ZW * S - 6, IY + ZH * S - 7))
# connector lines from zoom box to inset
I.append('<path d="M%s %s L%s %s M%s %s L%s %s" class="ld" stroke-dasharray="3 3" stroke="#8a6a3a"/>' % (ZX, ZY + ZH, IX, IY, ZX + ZW, ZY + ZH, IX + ZW * S, IY))
# inhibitory projections from VLPO in the inset (blue dashed, tee)
D.append('<marker id="%s-teeb" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M5 0V10" stroke="#2c5d9c" stroke-width="2.4"/></marker>' % P)
v = T(N['VLPO'][0])
for tgt in ('TMN', 'DR', 'LC'):
    t = T(N[tgt][0])
    ang = math.atan2(t[1] - v[1], t[0] - v[0])
    e = (t[0] - 13 * math.cos(ang), t[1] - 13 * math.sin(ang))
    mid = ((v[0] + e[0]) / 2, (v[1] + e[1]) / 2 + (18 if tgt != 'TMN' else 10))
    I.append('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="%s" stroke-width="1.1" stroke-dasharray="4 2.5" marker-end="url(#%s-teeb)"/>' % (
        f(v[0] + 9), f(v[1] + 3), f(mid[0]), f(mid[1]), f(e[0]), f(e[1]), WEST, P))
IL = [
    dict(t=T(N['MnPO'][0]), zh='正中視前核 <tspan style="fill:#2c5d9c">MnPO</tspan>', en='Median preoptic n.'),
    dict(t=T(N['VLPO'][0]), zh='腹外側視前核 <tspan style="fill:#2c5d9c">VLPO</tspan>', en='Ventrolateral preoptic n.'),
    dict(t=T(N['SCN'][0]), zh='視交叉上核 <tspan style="fill:#6b4f9a">SCN</tspan>', en='Suprachiasmatic n.'),
    dict(t=T(N['ORX'][0]), zh='外側下視丘 <tspan style="fill:#a8781a">orexin</tspan>', en='Lateral hypothalamus', bias=-30, elbow=T(N['ORX'][0])[0]),
    dict(t=T(N['TMN'][0]), zh='結節乳頭核 <tspan style="fill:#a8412c">TMN</tspan>', en='Tuberomammillary n.', bias=40),
]
IR = [
    dict(t=T(N['DR'][0]), zh='背側縫核 <tspan style="fill:#a8412c">DR</tspan>', en='Dorsal raphe（血清素）'),
    dict(t=T(N['LDT'][0]), zh='<tspan style="fill:#a8412c">LDT/PPT</tspan>', en='Laterodorsal / pedunculo-', sub='pontine tegm.（乙醯膽鹼）'),
    dict(t=T(N['LC'][0]), zh='藍斑核 <tspan style="fill:#a8412c">LC</tspan>', en='Locus coeruleus（正腎）'),
]
for d, yy in zip([IL[0], IL[3], IL[1], IL[2], IL[4]], [518, 555.5, 591.5, 627.5, 663.5]):
    el = None
    if d is IL[3]:
        el = 368
    I.append(label('L', 290, yy, d['zh'], d['en'], d['t'], elbow=el))

I.append('<text x="431" y="553" class="ls halo" style="font-weight:600">下視丘 <tspan class="le">Hypothalamus</tspan></text>')
I.append(column('R', IX + ZW * S + 14, IR, 560, 690, gap=48))

# legend bottom-left
LG = ['<text x="12" y="520" class="lt">圖例 Legend</text>']
LG.append(sw(20, 542, P + '-gb', '睡眠中樞（煞車）', 'Sleep-promoting, GABA'))
LG.append(sw(20, 578, P + '-gr', '清醒中樞（油門）', 'Arousal, monoamine/ACh'))
LG.append(sw(20, 614, P + '-gg', '穩定器 orexin', 'Wake stabiliser'))
LG.append(sw(20, 650, P + '-gp', '生理時鐘 SCN', 'Master clock'))
LG.append('<path d="M12 684 h22" stroke="%s" stroke-width="7" stroke-opacity=".22" stroke-linecap="round"/><text x="40" y="688" class="ls">上行激活（往皮質）</text>' % RED)
LG.append('<path d="M12 704 h18" stroke="%s" stroke-width="1.1" stroke-dasharray="4 2.5" marker-end="url(#%s-teeb)"/><text x="40" y="708" class="ls">VLPO 抑制投射</text>' % (WEST, P))

body = ('<g id="%s-g">\n' % P) + inline_classes('\n'.join(G)) + '\n</g>\n' + '\n'.join(M) + '\n' + '\n'.join(I) + '\n' + '\n'.join(LG)
cap = ('<b>圖 1-A　睡眠開關在腦的哪裡。</b>人腦正中矢狀切面（右半腦內側面，臉朝左）。藍色的 VLPO／MnPO 位在視交叉正上方的前視丘下部，是「煞車」；'
       '紅色的 TMN、背側縫核、LDT/PPT、藍斑核沿著下視丘後部到腦幹背側排成一列，是「油門」，透過上行激活系統叫醒皮質；金色的 orexin 神經元夾在中間當穩定器。'
       '下方放大圖的藍色虛線是 VLPO 對清醒中樞的抑制。示意圖，依解剖教科書重繪；VLPO、外側下視丘、PPT 等其實位在中線兩側，這裡投影到正中面上，大小也經放大以便辨認。')
if __name__ == '__main__':
    write(P, 'Plate 1·A', '睡眠開關在腦的哪裡', 'Where the sleep switch sits — midsagittal brain', 720, body,
          '人腦正中矢狀切面，標出睡眠與清醒中樞的位置', cap, defs=''.join(D))
