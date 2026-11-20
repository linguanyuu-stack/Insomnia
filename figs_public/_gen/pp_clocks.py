import sys, math, random
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from ppx import *
from body import outline, details, right_half

PID = 'pp-clocks'
H = 668
CX, TOP, S = 240, 84, 1.15
D = []   # defs
o = []
add = o.append


def P(x, y):
    return (CX + x * S, TOP + y * S)


def SP(pts_, close=False):
    return smooth([P(x, y) for x, y in pts_], close)


D.append('<radialGradient id="%s-skin" cx=".45" cy=".3" r=".9"><stop offset="0" stop-color="#fbe8da" stop-opacity=".8"/><stop offset="1" stop-color="#e2b89c" stop-opacity=".8"/></radialGradient>' % PID)
D.append('<radialGradient id="%s-sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff3c4"/><stop offset=".55" stop-color="#f6d97a"/><stop offset="1" stop-color="#f6d97a" stop-opacity="0"/></radialGradient>' % PID)
D.append('<linearGradient id="%s-beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f3cf5c" stop-opacity=".15"/><stop offset="1" stop-color="#e7b52e" stop-opacity=".75"/></linearGradient>' % PID)
D.append('<clipPath id="%s-mag"><circle cx="585" cy="168" r="104"/></clipPath>' % PID)
D.append('<marker id="%s-ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="#b8862a"/></marker>' % PID)
for nm, col in (('am', '#a8412c'), ('ab', '#2c5d9c'), ('aq', '#4f7a3a')):
    D.append('<marker id="%s-%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (PID, nm, col))

# ---------------- sun + light beams ----------------
SX, SY = 62, 76
add('<circle cx="%d" cy="%d" r="44" fill="url(#%s-sun)"/>' % (SX, SY, PID))
rays = ''
for i in range(16):
    a = math.radians(i * 22.5 + 6)
    r0, r1 = 22, (34 if i % 2 else 40)
    rays += 'M%s %sL%s %s' % (f(SX + r0 * math.cos(a)), f(SY + r0 * math.sin(a)), f(SX + r1 * math.cos(a)), f(SY + r1 * math.sin(a)))
add('<path d="%s" stroke="#c9962e" stroke-width="1.3" stroke-linecap="round"/>' % rays)
add('<circle cx="%d" cy="%d" r="18" fill="#f6d36a" stroke="%s" stroke-width="1.1"/>' % (SX, SY, INK))
add('<circle cx="%d" cy="%d" r="18" fill="url(#ink-hatch-l)" mask="none" opacity=".5"/>' % (SX, SY))
add('<circle cx="%d" cy="%d" r="13" fill="none" stroke="#b8862a" stroke-width=".6" stroke-dasharray="1.5 2"/>' % (SX, SY))
ex_l, ex_r = P(-10.3, 28.3), P(10.3, 28.3)
for (ex, ey), w in ((ex_l, 1), (ex_r, 1)):
    # tapered golden beam sun -> eye
    a = math.atan2(ey - SY, ex - SX)
    nx, ny = -math.sin(a), math.cos(a)
    x0, y0 = SX + 20 * math.cos(a), SY + 20 * math.sin(a)
    add('<path d="M%s %s L%s %s L%s %s Z" fill="url(#%s-beam)"/>' % (
        f(x0 + nx * 9), f(y0 + ny * 9), f(ex - 3), f(ey), f(x0 - nx * 9), f(y0 - ny * 9), PID))
    add('<path d="M%s %s L%s %s" stroke="#b8862a" stroke-width="1.2" stroke-dasharray="5 3" marker-end="url(#%s-ag)"/>' % (
        f(x0), f(y0), f(ex - 5 * math.cos(a)), f(ey - 5 * math.sin(a)), PID))

# ---------------- body ----------------
bd = outline(CX, TOP, S)
B = ['<g>']
B.append('<path d="%s" fill="url(#%s-skin)"/>' % (bd, PID))
D.append('<clipPath id="%s-rs"><rect x="%s" y="0" width="200" height="700"/></clipPath>' % (PID, f(CX + 16 * S)))
B.append('<path d="%s" fill="url(#ink-hatch-l)" clip-path="url(#%s-rs)" opacity=".8"/>' % (bd, PID))

# faint lungs & ribs for orientation
RL = [(-6, 92), (-14, 87), (-24, 93), (-31, 110), (-34, 135), (-34, 160), (-22, 156), (-11, 160), (-5, 150), (-4, 118)]
LL = [(6, 92), (14, 87), (24, 93), (31, 110), (34, 135), (33, 162), (22, 160), (17, 154), (15, 142), (9, 132), (6, 115)]
for Lp in (RL, LL):
    B.append('<path d="%s" fill="#eec3bb" fill-opacity=".45" stroke="%s" stroke-width=".6" stroke-opacity=".55"/>' % (SP(Lp, True), INK))
    B.append('<path d="%s" fill="url(#ink-stipple-l)" opacity=".5"/>' % SP(Lp, True))
for k in range(6):
    yy = 100 + k * 11
    for sg in (1, -1):
        B.append('<path d="%s" class="ink2" stroke-opacity=".28"/>' % SP([(sg * 4, yy), (sg * 18, yy - 1), (sg * 30, yy + 6), (sg * 33, yy + 13)]))

# fat (subcutaneous, viewer's left flank/hip)
FAT = [(-31, 190), (-33, 206), (-37, 226), (-41, 246), (-36, 246), (-31, 228), (-27, 208), (-27, 192)]
B.append('<path d="%s" fill="#f3d97c" stroke="%s" stroke-width=".7"/>' % (SP(FAT, True), INK))
rnd = random.Random(4)
for k in range(16):
    t = k / 15
    yy = 192 + 52 * t
    xx = -29 - 9 * t + rnd.uniform(-1.6, 1.6)
    x2, y2 = P(xx, yy)
    B.append('<circle cx="%s" cy="%s" r="%s" fill="#f8e7a6" stroke="%s" stroke-width=".4"/>' % (f(x2), f(y2), f(1.9 + rnd.random()), INK))

# muscle (viewer's left thigh, quadriceps)
MU = [(-37, 262), (-30, 255), (-20, 260), (-15, 284), (-16, 312), (-21, 334), (-30, 334), (-36, 314), (-39, 286)]
B.append('<path d="%s" fill="#c9705c" fill-opacity=".85" stroke="%s" stroke-width=".8"/>' % (SP(MU, True), INK))
for k in range(9):
    t = k / 8
    B.append('<path d="%s" class="ink2" stroke-width=".45" stroke-opacity=".7"/>' % SP([(-36 + 19 * t, 262 - 4 * math.sin(t * 3)), (-37 + 20 * t, 290), (-31 + 10 * t, 330)]))
B.append('<path d="%s" fill="url(#ink-hatch)" opacity=".45"/>' % SP([(-37, 262), (-33, 258), (-34, 290), (-29, 333), (-36, 314), (-39, 286)], True))

# skin patch (viewer's left forearm)
def aoff(y):
    return max(0, (y - 92)) * 0.13
SK = [(-56 - aoff(196), 196), (-61 - aoff(196), 194), (-62 - aoff(230), 230), (-55 - aoff(232), 232)]
# heart
HT = [(-6, 128), (3, 123), (13, 128), (20, 140), (18, 152), (9, 158), (1, 155), (-5, 147), (-8, 137)]
B.append('<path d="%s" fill="url(#ink-vol-red)" stroke="%s" stroke-width=".9"/>' % (SP(HT, True), INK))
B.append('<path d="%s" class="ink2"/>' % SP([(2, 126), (6, 140), (9, 156)]))
B.append('<path d="%s" fill="url(#ink-hatch)" opacity=".5"/>' % SP([(13, 128), (20, 140), (18, 152), (9, 158), (12, 146), (14, 134)], True))
B.append('<path d="%s" fill="none" stroke="%s" stroke-width="3.6"/>' % (SP([(-1, 128), (-1, 112), (5, 105), (10, 112)]), INK))
B.append('<path d="%s" fill="none" stroke="#c4594a" stroke-width="2.2"/>' % SP([(-1, 128), (-1, 112), (5, 105), (10, 112)]))
# diaphragm
B.append('<path d="%s" class="ink2" stroke-dasharray="3 2" stroke-opacity=".6"/>' % SP([(-34, 162), (-18, 152), (0, 160), (18, 155), (34, 164)]))
# pancreas (behind stomach)
PA = [(-8, 197), (-2, 192), (10, 193), (22, 188), (30, 187), (31, 192), (24, 196), (12, 200), (2, 203), (-7, 203)]
B.append('<path d="%s" fill="#ecc27a" stroke="%s" stroke-width=".8"/>' % (SP(PA, True), INK))
for k in range(8):
    x2, y2 = P(-4 + k * 4.4, 197 - k * .9)
    B.append('<path d="M%s %s q1.5 -2 3 0 q1.5 2 3 0" class="ink2" stroke-width=".4"/>' % (f(x2 - 3), f(y2)))
# liver
LV = [(-35, 163), (-22, 158), (-6, 161), (10, 163), (21, 167), (14, 173), (0, 179), (-14, 187), (-28, 190), (-35, 180)]
B.append('<path d="%s" fill="#a95c48" stroke="%s" stroke-width=".9"/>' % (SP(LV, True), INK))
B.append('<path d="%s" fill="url(#ink-hatch-l)"/>' % SP(LV, True))
B.append('<path d="%s" fill="url(#ink-hatch)" opacity=".6"/>' % SP([(-35, 180), (-28, 190), (-14, 187), (0, 179), (-14, 182), (-28, 184)], True))
B.append('<path d="%s" class="ink2" stroke="#fbe8da" stroke-opacity=".6"/>' % SP([(-30, 166), (-18, 162), (-4, 164)]))
B.append('<path d="%s" class="ink2"/>' % SP([(-4, 162), (-2, 172), (-6, 182)]))
# stomach (in front of left lobe)
ST = [(9, 164), (15, 159), (23, 160), (29, 167), (30, 180), (25, 190), (15, 195), (4, 194), (-4, 188), (-1, 183), (7, 185), (14, 182), (17, 174), (12, 168)]
B.append('<path d="%s" fill="#e3a08a" stroke="%s" stroke-width=".9"/>' % (SP(ST, True), INK))
B.append('<path d="%s" fill="url(#ink-hatch-l)"/>' % SP([(29, 167), (30, 180), (25, 190), (15, 195), (20, 186), (25, 176)], True))
for k in range(4):
    B.append('<path d="%s" class="ink2" stroke-width=".4"/>' % SP([(13 + k * 3, 162 + k), (19 + k * 2, 176), (12 + k * 2, 190 - k)]))
B.append('<path d="%s" fill="none" stroke="%s" stroke-width="3"/>' % (SP([(12, 152), (11, 160)]), INK))
# intestines: colon frame + small intestine coils
colon = [(-22, 238), (-25, 222), (-24, 206), (-14, 203), (0, 206), (14, 204), (24, 206), (25, 222), (22, 236), (12, 241)]
B.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (SP(colon), INK, f(8.2 * S)))
B.append('<path d="%s" fill="none" stroke="#d9a58a" stroke-width="%s" stroke-linecap="round"/>' % (SP(colon), f(6.6 * S)))
hd = ''
for t in [i / 26 for i in range(27)]:
    pass
dense = bez_pts([P(x, y) for x, y in colon], per=8)
for i in range(4, len(dense) - 2, 4):
    (x1, y1), (x2, y2) = dense[i - 1], dense[i + 1]
    a = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(a) * 4 * S, math.cos(a) * 4 * S
    x, y = dense[i]
    hd += 'M%s %sL%s %s' % (f(x + nx), f(y + ny), f(x - nx), f(y - ny))
B.append('<path d="%s" stroke="%s" stroke-width=".5" stroke-opacity=".7"/>' % (hd, INK))
SI = [(-14, 212), (12, 212), (14, 218), (-12, 219), (-14, 225), (14, 225), (15, 231), (-10, 232), (-6, 238), (8, 238)]
B.append('<path d="%s" fill="%s" fill-opacity=".9" stroke="none"/>' % (SP([(-17, 210), (17, 210), (19, 240), (-17, 242)], True), '#efc2ad'))
B.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (SP(SI), INK, f(5.4 * S)))
B.append('<path d="%s" fill="none" stroke="#f1c8b4" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (SP(SI), f(4.1 * S)))
B.append('<path d="%s" fill="none" stroke="%s" stroke-width=".4" stroke-opacity=".5"/>' % (SP([(x, y + 1.2) for x, y in SI]), INK))

# brain inside the head (front view, faint)
for sg in (1, -1):
    bh = [(sg * 1.2, 4.5), (sg * 12, 3), (sg * 21, 8), (sg * 24, 16), (sg * 23, 23), (sg * 15, 24), (sg * 6, 24.5), (sg * 1.2, 26)]
    d_ = SP(bh, True)
    B.append('<path d="%s" fill="#efd3c6" fill-opacity=".85"/><path d="%s" fill="url(#ink-stipple-l)"/><path d="%s" class="ink" stroke-width=".8"/>' % (d_, d_, d_))
    for g in [[(sg * 5, 8), (sg * 11, 13), (sg * 8, 19)], [(sg * 16, 7), (sg * 20, 15), (sg * 15, 21)], [(sg * 6, 20), (sg * 13, 21), (sg * 20, 19)]]:
        B.append('<path d="%s" class="ink2" stroke-opacity=".6"/>' % SP(g))
B.append(details(CX, TOP, S, eyes='open'))
# modern short hair
HR = [(-26.5, 27), (-27.5, 14), (-23, 4), (-13, -2.5), (0, -3.6), (13, -2.5), (23, 4), (27.5, 14), (26.5, 27), (24.5, 19), (21, 11), (12, 9.5), (2, 11), (-9, 9.5), (-19, 11), (-24.5, 19)]
B.append('<path d="%s" fill="#3d2c1f" fill-opacity=".92" stroke="%s" stroke-width=".9"/>' % (SP(HR, True), INK))
B.append('<path d="%s" fill="none" stroke="#9c7a58" stroke-width=".5" stroke-opacity=".8"/>' % ' '.join(
    SP(s_) for s_ in [[(-20, 6), (-8, 0), (6, -1)], [(-24, 14), (-14, 6), (0, 3)], [(4, 2), (14, 3), (22, 10)], [(8, 6), (18, 7), (24, 16)]]))
B.append('<path d="%s" class="ink3" stroke-width="1.5"/>' % bd)
B.append('</g>')
add('\n'.join(B))

# eyes -> SCN optic path (retinohypothalamic)
SCN = P(0, 31)
for ex, ey in (ex_l, ex_r):
    add('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="#c9962e" stroke-width="1.6"/>' % (f(ex), f(ey + 1), f((ex + SCN[0]) / 2), f(ey + 5), f(SCN[0]), f(SCN[1])))
add('<circle cx="%s" cy="%s" r="3.4" fill="#6a4c9c" stroke="%s" stroke-width=".8"/>' % (f(SCN[0]), f(SCN[1]), INK))
add('<circle cx="%s" cy="%s" r="7" fill="none" stroke="%s" stroke-width=".7"/>' % (f(SCN[0]), f(SCN[1]), INK))

# ---------------- conductor's cue lines SCN -> clocks ----------------
CL = {  # name: local coords of clock
    'heart': (7, 140), 'liver': (-19, 171), 'stomach': (22, 174), 'pancreas': (3, 199),
    'gut': (-3, 224), 'fat': (-35, 222), 'muscle': (-27, 296), 'skin': (-60 - aoff(214), 214),
}
HUB = P(0, 104)
cues = ['<path d="%s" fill="none" stroke="#b8862a" stroke-width="1.6" stroke-dasharray="4 2.5"/>' % smooth([SCN, P(0, 50), P(0, 76), HUB])]
for k, (x, y) in CL.items():
    if k == 'skin':
        path = [HUB, P(-24, 112), P(-44, 130), P(-52, 170), P(x + 3, y - 9)]
    elif k == 'muscle':
        path = [HUB, P(-14, 130), P(-24, 200), P(-26, 250), P(x, y - 9)]
    elif k == 'fat':
        path = [HUB, P(-14, 130), P(-26, 180), P(x + 2, y - 9)]
    else:
        path = [HUB, P(x * .4, (y + 104) / 2), P(x, y - 9)]
    cues.append('<path d="%s" fill="none" stroke="#b8862a" stroke-width=".9" stroke-dasharray="3 2.4" stroke-opacity=".85"/>' % smooth(path))
add('\n'.join(cues))
for k, (x, y) in CL.items():
    cx_, cy_ = P(x, y)
    add(clockface(cx_, cy_, 7.2, 7, 0))

# ---------------- magnified hypothalamus with conductor ----------------
MX, MY, MR = 585, 168, 104
# cone from SCN to lens
a1, a2 = math.radians(-118), math.radians(118)
add('<path d="M%s %s L%s %s M%s %s L%s %s" stroke="%s" stroke-width=".7" stroke-dasharray="4 3" fill="none"/>' % (
    f(SCN[0] + 7), f(SCN[1] - 2), f(MX - MR * .93), f(MY - MR * .36), f(SCN[0] + 7), f(SCN[1] + 2), f(MX - MR * .82), f(MY + MR * .57), INK))
M = ['<g clip-path="url(#%s-mag)">' % PID]
M.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#f4e2d6"/>' % (MX - MR, MY - MR, 2 * MR, 2 * MR))
M.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#ink-stipple-l)" opacity=".8"/>' % (MX - MR, MY - MR, 2 * MR, 2 * MR))
# corpus callosum arc (top) & fornix
M.append('<path d="%s" fill="#efe3cf" stroke="%s" stroke-width="1"/>' % (cr([(MX - 110, MY - 70), (MX - 40, MY - 96), (MX + 40, MY - 98), (MX + 110, MY - 84), (MX + 110, MY - 66), (MX + 40, MY - 80), (MX - 40, MY - 78), (MX - 110, MY - 52)], True), INK))
M.append('<path d="%s" fill="url(#ink-hatch-h)" opacity=".8"/>' % cr([(MX - 110, MY - 70), (MX - 40, MY - 96), (MX + 40, MY - 98), (MX + 110, MY - 84), (MX + 110, MY - 66), (MX + 40, MY - 80), (MX - 40, MY - 78), (MX - 110, MY - 52)], True))
# third ventricle (blue cavity)
V3 = [(MX - 62, MY - 60), (MX + 20, MY - 66), (MX + 70, MY - 50), (MX + 74, MY - 10), (MX + 54, MY + 30), (MX + 44, MY + 48), (MX + 36, MY + 58),
      (MX + 30, MY + 38), (MX - 6, MY + 22), (MX - 36, MY + 40), (MX - 44, MY + 30), (MX - 46, MY - 10)]
M.append('<path d="%s" fill="#d7e2f0" stroke="%s" stroke-width=".9"/>' % (cr(V3, True), INK))
M.append('<path d="%s" fill="url(#ink-hatch-h)" opacity=".35"/>' % cr(V3, True))
# thalamus (massa intermedia) & anterior commissure
M.append('<ellipse cx="%d" cy="%d" rx="34" ry="22" fill="#ead2c4" stroke="%s" stroke-width=".9"/>' % (MX + 30, MY - 30, INK))
M.append('<ellipse cx="%d" cy="%d" rx="34" ry="22" fill="url(#ink-stipple)" opacity=".5"/>' % (MX + 30, MY - 30))
M.append('<circle cx="%d" cy="%d" r="8" fill="#efe3cf" stroke="%s" stroke-width=".9"/>' % (MX - 40, MY - 20, INK))
M.append('<path d="M%d %d q4 -3 8 0 M%d %d q4 3 8 0" class="ink2"/>' % (MX - 44, MY - 22, MX - 44, MY - 17))
# lamina terminalis + hypothalamic floor tissue
M.append('<path d="%s" fill="#efcdbf" stroke="%s" stroke-width=".9"/>' % (cr([(MX - 46, MY - 10), (MX - 44, MY + 30), (MX - 36, MY + 40), (MX - 6, MY + 22), (MX + 30, MY + 38), (MX + 36, MY + 58),
                                                                                  (MX + 40, MY + 70), (MX + 20, MY + 66), (MX - 30, MY + 62), (MX - 60, MY + 50), (MX - 70, MY + 20)], True), INK))
# optic nerve from the eye (anterior, left) to chiasm
ON = [(MX - 120, MY + 74), (MX - 80, MY + 66), (MX - 40, MY + 60), (MX - 12, MY + 58)]
M.append('<path d="%s" fill="#f1dc8e" stroke="%s" stroke-width="1"/>' % (tapered(ON, 26, 20), INK))
M.append('<path d="%s" fill="url(#ink-hatch-h)" opacity=".7"/>' % tapered(ON, 26, 20))
# chiasm knot
CH = [(MX - 20, MY + 50), (MX + 8, MY + 46), (MX + 30, MY + 52), (MX + 36, MY + 64), (MX + 26, MY + 76), (MX - 4, MY + 78), (MX - 24, MY + 72)]
M.append('<path d="%s" fill="#f1dc8e" stroke="%s" stroke-width="1.1"/>' % (cr(CH, True), INK))
M.append('<path d="%s" fill="url(#ink-hatch)" opacity=".5"/>' % cr([(MX - 4, MY + 78), (MX + 26, MY + 76), (MX + 36, MY + 64), (MX + 20, MY + 70)], True))
for k in range(5):
    M.append('<path d="%s" class="ink2" stroke-width=".45"/>' % cr([(MX - 18 + k * 3, MY + 54 + k * 4), (MX + 6, MY + 62), (MX + 30, MY + 58 + k * 3)]))
# infundibulum + pituitary (behind chiasm)
M.append('<path d="%s" fill="#e8b4a2" stroke="%s" stroke-width="1"/>' % (cr([(MX + 34, MY + 58), (MX + 48, MY + 62), (MX + 52, MY + 84), (MX + 66, MY + 92), (MX + 72, MY + 108), (MX + 30, MY + 108), (MX + 36, MY + 90), (MX + 40, MY + 78)], True), INK))
M.append('<path d="%s" fill="url(#ink-hatch)" opacity=".4"/>' % cr([(MX + 48, MY + 62), (MX + 52, MY + 84), (MX + 66, MY + 92), (MX + 72, MY + 108), (MX + 58, MY + 104), (MX + 46, MY + 82)], True))
# light signal along optic nerve
M.append('<path d="%s" fill="none" stroke="#c9962e" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#%s-ag)"/>' % (cr([(MX - 104, MY + 70), (MX - 60, MY + 62), (MX - 26, MY + 56), (MX - 8, MY + 44)]), PID))
# SCN = podium
M.append('<ellipse cx="%d" cy="%d" rx="27" ry="9" fill="#8a6bb8" stroke="%s" stroke-width="1.1"/>' % (MX + 2, MY + 42, INK))
M.append('<ellipse cx="%d" cy="%d" rx="27" ry="9" fill="url(#ink-stipple)" opacity=".7"/>' % (MX + 2, MY + 42))
M.append('<path d="M%d %d q27 7 54 0" fill="none" stroke="%s" stroke-width=".6"/>' % (MX - 25, MY + 43, INK))
M.append('<ellipse cx="%d" cy="%d" rx="18" ry="3.2" fill="#b9a2dd" opacity=".8"/>' % (MX - 2, MY + 37))

# conductor (feet at fx,fy; faces right), ~74 px tall
fx, fy = MX + 2, MY + 36
def C(pts_, close=True):
    return cr([(fx + x, fy + y) for x, y in pts_], close)
COAT = '#2f2a35'
cd = []
# legs / trousers
cd.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".8"/>' % (C([(-8, -32), (-1, -32), (-2, -16), (-4, -1), (-9, -1), (-9, -16)]), COAT, INK))
cd.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".8"/>' % (C([(0, -32), (7, -32), (8, -16), (9, -1), (4, -1), (2, -16)]), '#3b3542', INK))
cd.append('<path d="%s" fill="#111" stroke="%s" stroke-width=".6"/>' % (C([(-10, -2), (-3, -2), (-1, 0.5), (-11, 0.5)]), INK))
cd.append('<path d="%s" fill="#111" stroke="%s" stroke-width=".6"/>' % (C([(3, -2), (10, -2), (14, 0.5), (3, 0.5)]), INK))
# coat tails (behind, to the left)
cd.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".8"/>' % (C([(-9, -38), (-12, -26), (-15, -12), (-11, -12), (-6, -26)]), COAT, INK))
# torso
cd.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".9"/>' % (C([(-9, -57), (-2, -60), (6, -58), (9, -50), (8, -36), (5, -30), (-8, -30), (-10, -42)]), COAT, INK))
# shirt front & bow tie
cd.append('<path d="%s" fill="#fbf6ea" stroke="%s" stroke-width=".5"/>' % (C([(-1, -58), (5, -58), (5, -44), (2, -38)]), INK))
cd.append('<path d="M%s %s l3 -2 v4 z M%s %s l3 2 v-4 z" fill="#111"/>' % (f(fx), f(fy - 56), f(fx + 6), f(fy - 58)))
cd.append('<path d="%s" class="ink2" stroke="#6d6578"/>' % C([(-6, -54), (-5, -40), (-3, -31)], False))
# left (far) arm forward, open palm
cd.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".8"/>' % (C([(-5, -56), (4, -50), (12, -46), (16, -45), (16, -41), (10, -41), (2, -45), (-6, -50)]), COAT, INK))
cd.append('<path d="%s" fill="#f1cdb4" stroke="%s" stroke-width=".6"/>' % (C([(16, -46), (21, -48), (24, -47.5), (21, -45), (24, -44), (20, -42.5), (16, -41)]), INK))
# head (profile right)
cd.append('<path d="%s" fill="#f1cdb4" stroke="%s" stroke-width=".8"/>' % (C([(-2, -61), (-1, -64), (-4, -68), (-3, -74), (2, -77), (7, -75), (8.5, -71), (10.5, -68), (8.5, -67.5), (8.5, -65), (6, -63), (3, -62.5), (2, -60)]), INK))
cd.append('<path d="%s" fill="#5b5f66" stroke="%s" stroke-width=".6"/>' % (C([(-4.5, -68), (-4, -75), (1, -78.5), (7, -76.5), (8, -73.5), (3, -73.5), (1, -71), (-1, -66)]), INK))
cd.append('<path d="M%s %s h2.2" stroke="%s" stroke-width=".8"/>' % (f(fx + 5.4), f(fy - 70.5), INK))
# raised right arm with baton
cd.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".8"/>' % (C([(4, -58), (10, -64), (16, -72), (19, -70), (14, -60), (8, -51)]), '#3b3542', INK))
cd.append('<circle cx="%s" cy="%s" r="2.4" fill="#f1cdb4" stroke="%s" stroke-width=".6"/>' % (f(fx + 18), f(fy - 72.5), INK))
cd.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="2.2" stroke-linecap="round"/><path d="M%s %s L%s %s" stroke="#fbf6ea" stroke-width="1.1" stroke-linecap="round"/>' % (
    f(fx + 18), f(fy - 73), f(fx + 34), f(fy - 90), INK, f(fx + 18.5), f(fy - 73.5), f(fx + 33.5), f(fy - 89.5)))
# cue arcs from baton
for k, rr in enumerate((8, 14, 20)):
    cd.append('<path d="M%s %s a%d %d 0 0 1 %s %s" fill="none" stroke="#c9962e" stroke-width="1.1" stroke-opacity="%s"/>' % (
        f(fx + 36 + rr * .2), f(fy - 92 - rr * .9), rr, rr, f(rr * 1.1), f(rr * 1.2), f(1 - k * .25)))
M.append('\n'.join(cd))
M.append('</g>')
add('\n'.join(M))
# lens rim
add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#8a6a3a" stroke-width="5"/>' % (MX, MY, MR + 2))
add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="1"/><circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="1.2"/>' % (MX, MY, MR - .5, INK, MX, MY, MR + 4.5, INK))

# magnifier labels
L = []
L.append(T(MX, 44, '腦中的總指揮', 'lb', 'middle', size=15, color='#5b3f8c'))
L.append(T(MX, 58, '視交叉上核 SCN（下視丘）', 'le', 'middle', size=12))
L.append(lab2(MX - 2, 296, '視神經交叉', 'optic chiasm', anchor='middle', size=13, ensize=11))
L.append(lead([(MX - 2, 282), (MX - 2, MY + 80)]))
L.append(lab2(700, 268, '腦下垂體', 'pituitary', size=13, ensize=11))
L.append(lead([(698, 264), (684, 264), (MX + 56, MY + 92)]))
L.append(lab2(474, 252, '光訊號', 'from the eyes', anchor='end', size=13, ensize=11, color='#8a6418'))
L.append(lead([(478, 248), (MX - 78, MY + 66)]))
L.append(lab2(700, 120, '指揮台', 'SCN podium', size=13, ensize=11, color='#5b3f8c'))
L.append(lead([(698, 116), (686, 116), (MX + 26, MY + 40)]))
add('\n'.join(L))

# ---------------- labels: light ----------------
add('<g transform="translate(18,150)">'
    '<path d="M6 0 v26 q0 10 10 10 q10 0 10 -10 v-26" fill="none" stroke="%s" stroke-width="4.4" stroke-linecap="round"/>'
    '<path d="M6 0 v26 q0 10 10 10 q10 0 10 -10 v-26" fill="none" stroke="#e6c35a" stroke-width="2.6" stroke-linecap="round"/>'
    '<path d="M16 36 v18" stroke="%s" stroke-width="4.4" stroke-linecap="round"/><path d="M16 36 v18" stroke="#c9a03a" stroke-width="2.6" stroke-linecap="round"/>'
    '<path d="M-2 6 q-4 6 0 12 M34 6 q4 6 0 12 M-7 2 q-6 10 0 20 M39 2 q6 10 0 20" fill="none" stroke="#b8862a" stroke-width=".9"/></g>' % (INK, INK))
add(T(64, 160, '光線＝校音叉', 'lb', size=15, color='#8a6418'))
add(T(64, 176, '最主要的對時訊號', 'ls', size=12))
add(T(64, 191, 'light: the main', 'le', size=11.5))
add(T(64, 205, 'time-setter', 'le', size=11.5))

# ---------------- organ labels ----------------
def olabel(side, xcol, y, zh, en, key, color=INK):
    tx, ty = P(*CL[key])
    anc = 'end' if side == 'L' else 'start'
    out = lab2(xcol, y, zh, en, anc, size=14, color=color)
    sx = xcol + 4 if side == 'L' else xcol - 4
    tx2 = tx + (-9 if side == 'R' else 9)
    out = lead([(sx, y - 5), (sx + (10 if side == 'L' else -10), y - 5), (tx2, ty)]) + out
    return out

add(olabel('L', 140, 262, '肝臟的時鐘', 'liver', 'liver'))
add(olabel('L', 140, 312, '皮膚的時鐘', 'skin', 'skin'))
add(olabel('L', 140, 362, '脂肪的時鐘', 'fat', 'fat'))
add(olabel('L', 140, 418, '肌肉的時鐘', 'muscle', 'muscle'))
add(olabel('R', 368, 210, '心臟的時鐘', 'heart', 'heart'))
add(olabel('R', 368, 330, '胃的時鐘', 'stomach', 'stomach'))
add(olabel('R', 368, 372, '胰臟的時鐘', 'pancreas', 'pancreas'))
add(olabel('R', 368, 414, '腸道的時鐘', 'gut', 'gut'))
# cue line legend near body
add(T(368, 452, '金色虛線：總指揮把「現在幾點」', 'ls', size=11.5, color='#8a6418'))
add(T(368, 466, '透過神經與荷爾蒙傳到各器官', 'ls', size=11.5, color='#8a6418'))

# ---------------- secondary cues panel (right bottom) ----------------
PX, PY, PW, PH = 556, 336, 194, 156
cue = []
cue.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" class="panel"/>' % (PX, PY, PW, PH))
cue.append(T(PX + 10, PY + 18, '其他對時訊號（力量較小）', 'lb', size=12.5))
cue.append(T(PX + 10, PY + 32, 'secondary time cues', 'le', size=11))
# meal: rice bowl + chopsticks
bx, by = PX + 28, PY + 60
cue.append('<path d="M%d %d h28 q-2 16 -14 17 q-12 -1 -14 -17z" fill="#e9eef5" stroke="%s" stroke-width=".9"/>' % (bx - 14, by, INK))
cue.append('<path d="M%d %d q14 -9 28 0" fill="#fbf6ea" stroke="%s" stroke-width=".8"/>' % (bx - 14, by, INK))
cue.append('<path d="M%d %d h28" stroke="%s" stroke-width=".6"/><path d="M%d %d q2 6 -2 9 M%d %d q-2 6 2 9" stroke="%s" stroke-width=".6" fill="none"/>' % (bx - 12, by + 6, BLUE, bx - 6, by + 6, bx + 6, by + 6, BLUE))
cue.append('<path d="M%d %d l22 -14 M%d %d l22 -12" stroke="#8a5a2a" stroke-width="1.6" stroke-linecap="round"/>' % (bx + 2, by - 2, bx + 5, by - 1))
cue.append('<path d="M%d %d h10 v3 h-10z" fill="#e3d9c2" stroke="%s" stroke-width=".5"/>' % (bx - 5, by + 17, INK))
cue.append(T(PX + 64, PY + 56, '吃飯時間', 'lb', size=13))
cue.append(T(PX + 64, PY + 70, '→ 肝、胃、腸、胰臟', 'ls', size=11.5, color=TCM))
# exercise: running shoe
sx_, sy_ = PX + 34, PY + 100
cue.append('<path d="M%d %d q2 -8 8 -9 l6 6 q8 3 14 4 q6 1 6 6 v3 h-34 z" fill="#d6dfe9" stroke="%s" stroke-width=".9"/>' % (sx_ - 16, sy_ + 8, INK))
cue.append('<path d="M%d %d h34 v3 h-34z" fill="#fbf6ea" stroke="%s" stroke-width=".7"/>' % (sx_ - 16, sy_ + 14, INK))
cue.append('<path d="M%d %d l3 3 M%d %d l3 3 M%d %d l3 3" class="ink2"/>' % (sx_ - 6, sy_ + 1, sx_ - 3, sy_ + 2, sx_, sy_ + 3))
cue.append('<path d="M%d %d h-8 M%d %d h-12 M%d %d h-8" stroke="%s" stroke-width=".8"/>' % (sx_ - 20, sy_ + 4, sx_ - 20, sy_ + 9, sx_ - 20, sy_ + 14, INK))
cue.append(T(PX + 64, PY + 100, '運動時間', 'lb', size=13))
cue.append(T(PX + 64, PY + 114, '→ 肌肉、心臟', 'ls', size=11.5, color='#4f7a3a'))
# temperature: thermometer
tx_, ty_ = PX + 28, PY + 124
cue.append('<rect x="%d" y="%d" width="7" height="20" rx="3.5" fill="#fbf6ea" stroke="%s" stroke-width=".9"/>' % (tx_ - 3.5, ty_, INK))
cue.append('<circle cx="%d" cy="%d" r="5.5" fill="%s" stroke="%s" stroke-width=".9"/><rect x="%d" y="%d" width="3" height="14" fill="%s"/>' % (tx_, ty_ + 22, RED, INK, tx_ - 1.5, ty_ + 8, RED))
cue.append('<path d="M%d %d h3 M%d %d h3 M%d %d h3" class="ink2"/>' % (tx_ + 4, ty_ + 5, tx_ + 4, ty_ + 9, tx_ + 4, ty_ + 13))
cue.append(T(PX + 64, PY + 136, '冷熱變化', 'lb', size=13))
cue.append(T(PX + 64, PY + 150, '→ 皮膚、全身', 'ls', size=11.5, color=WEST))
add('\n'.join(cue))
# small coloured arrows (secondary cues) pointing at the clocks they tune
def sarrow(key, ang, col, L_=17, off=11):
    x, y = P(*CL[key])
    a = math.radians(ang)
    x1, y1 = x + (off + L_) * math.cos(a), y + (off + L_) * math.sin(a)
    x2, y2 = x + off * math.cos(a), y + off * math.sin(a)
    return '<path d="M%s %sL%s %s" stroke="%s" stroke-width="2" marker-end="url(#%s-%s)"/>' % (f(x1), f(y1), f(x2), f(y2), {'am': '#a8412c', 'aq': '#4f7a3a', 'ab': '#2c5d9c'}[col], PID, col)
for key, ang, col in (('liver', 140, 'am'), ('stomach', -20, 'am'), ('gut', 20, 'am'), ('pancreas', 10, 'am'),
                      ('muscle', 160, 'aq'), ('heart', -30, 'aq'), ('skin', 100, 'ab')):
    add(sarrow(key, ang, col))
# ---------------- desync inset (left bottom) ----------------
IX, IY = 12, 470
ins = ['<rect x="%d" y="%d" width="132" height="128" rx="4" class="panel"/>' % (IX, IY)]
ins.append(T(IX + 8, IY + 18, '對準時', 'lb', size=12.5, color='#4f7a3a'))
for k in range(4):
    ins.append(clockface(IX + 20 + k * 30, IY + 36, 8, 7, 0))
ins.append(T(IX + 8, IY + 70, '熬夜、輪班、時差', 'lb', size=12.5, color=TCM))
for k, (h_, m_) in enumerate(((7, 0), (3, 15), (10, 40), (1, 30))):
    ins.append(clockface(IX + 20 + k * 30, IY + 88, 8, h_, m_, face='#fbe9e3'))
ins.append(T(IX + 8, IY + 116, '→ 各器官時鐘不同步', 'ls', size=11.5))
add('\n'.join(ins))

# ---------------- message band ----------------
add('<rect x="10" y="%d" width="740" height="40" rx="5" fill="#f6e7b0" stroke="%s" stroke-width=".8"/>' % (H - 50, INK))
add('<rect x="13" y="%d" width="734" height="34" rx="4" fill="none" stroke="#c9962e" stroke-width=".6"/>' % (H - 47))
add(T(380, H - 25, '光線校正總指揮，總指揮再讓全身的時鐘對時', 'lb', 'middle', size=17, halo=False))

body = '\n'.join(o)
write(PID, '圖 1·D', '全身都是時鐘，腦裡有一位總指揮', 'Clocks everywhere, one conductor in the brain', H, body,
      '站立人體半透明示意：腦部下視丘的視交叉上核以指揮家表示，肝、心、胃、胰、腸、肌肉、皮膚、脂肪各有小時鐘；光線經眼睛校正總指揮。',
      '<b>圖 1·D　全身都是時鐘。</b>不只腦袋，肝臟、心臟、腸胃、胰臟、肌肉、皮膚、脂肪細胞裡都有自己的小時鐘。坐鎮在眼睛後方、視神經交叉正上方的「視交叉上核」像樂團指揮：早上的光線從眼睛進來替它校時，它再把時間傳給全身；吃飯、運動、冷熱也能微調部分器官的時鐘，但力量較小。示意圖，器官位置與大小經簡化。',
      '\n'.join(D))
