import sys, math, random
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from ppx import *

PID = 'pp-forces'
H = 684
D = []
o = []
add = o.append
SAND = '#e3c27a'; SAND_D = '#c99f4e'
SEA = '#5f86b5'; SEA_S = '#cfdcef'
NIGHT = '#dfe4ef'

for nm, col in (('ab', '#2c5d9c'), ('ar', '#a8412c'), ('ag', '#8a6418'), ('ak', INK)):
    D.append('<marker id="%s-%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 1L9 5L0 9L2.5 5z" fill="%s"/></marker>' % (PID, nm, col))
D.append('<linearGradient id="%s-sky" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fbeec9"/><stop offset=".55" stop-color="#f8e3c0"/><stop offset=".68" stop-color="#c9cfe0"/><stop offset="1" stop-color="#aeb8d2"/></linearGradient>' % PID)
D.append('<linearGradient id="%s-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb9d8"/><stop offset="1" stop-color="#4f73a0"/></linearGradient>' % PID)
D.append('<radialGradient id="%s-brass" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#fff1c2"/><stop offset=".45" stop-color="#e2b04a"/><stop offset="1" stop-color="#8a5f1c"/></radialGradient>' % PID)
D.append('<radialGradient id="%s-glass" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#ffffff" stop-opacity=".7"/><stop offset="1" stop-color="#d9e4ee" stop-opacity=".35"/></radialGradient>' % PID)


def panel(x, y, w, h, fill='#fbf3df'):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="5" fill="%s" stroke="%s" stroke-width="1"/>'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="none" stroke="#c9b48a" stroke-width=".6"/>') % (x, y, w, h, fill, INK, x + 3, y + 3, w - 6, h - 6)


def numc(x, y, n, col):
    return ('<circle cx="%s" cy="%s" r="10" fill="%s" stroke="%s" stroke-width=".8"/>'
            '<text x="%s" y="%s" text-anchor="middle" style="font-size:12.5px;font-weight:700;fill:#fff;font-family:Georgia,serif">%s</text>') % (x, y, col, INK, x, y + 4.3, n)

# ======================= PANEL 1: HOURGLASS =======================
add(panel(10, 8, 240, 322))
add(numc(30, 30, '1', '#b8862a'))
add(T(46, 35, '睡意沙漏', 'lb', size=16))
add(T(124, 35, 'sleep-pressure hourglass', 'le', size=11))

HX, HY = 78, 152
def hg(x, y):
    return (HX + x, HY + y)
prof = [(21, -80), (31, -70), (35, -50), (31, -28), (16, -9), (3.2, 0)]
R = [hg(x, y) for x, y in prof] + [hg(x, -y) for x, y in reversed(prof[:-1])]
Lft = [hg(-x, -y) for x, y in prof] + [hg(-x, y) for x, y in reversed(prof[:-1])]
glass = cr(R + Lft, True, k=.9)
D.append('<clipPath id="%s-gl"><path d="%s"/></clipPath>' % (PID, glass))
# columns behind
for sx in (-44, 44):
    add('<path d="%s" fill="#a8743e" stroke="%s" stroke-width=".9"/>' % (cr([hg(sx - 3, -80), hg(sx - 4, -60), hg(sx - 2.5, -30), hg(sx - 4.5, 0), hg(sx - 2.5, 30), hg(sx - 4, 60), hg(sx - 3, 80),
                                                                          hg(sx + 3, 80), hg(sx + 4, 60), hg(sx + 2.5, 30), hg(sx + 4.5, 0), hg(sx + 2.5, -30), hg(sx + 4, -60), hg(sx + 3, -80)], True, k=.8), INK))
    add('<path d="M%s %s V%s" stroke="#e0b47c" stroke-width="1" opacity=".7"/>' % (f(HX + sx - 1.5), f(HY - 78), f(HY + 78)))
    add('<path d="M%s %s V%s" stroke="%s" stroke-width="2" opacity=".35"/>' % (f(HX + sx + 2), f(HY - 78), f(HY + 78), INK))
# sand inside
sandB = ('<path d="%s" fill="%s"/>' % (cr([hg(-36, 82), hg(-36, 4), hg(-6, 4), hg(-1, 2), hg(1, 2), hg(6, 4), hg(36, 4), hg(36, 82)], True), SAND))
mound = cr([hg(-34, 42), hg(-20, 34), hg(-6, 22), hg(0, 18), hg(6, 22), hg(20, 34), hg(34, 42), hg(34, 84), hg(-34, 84)], True, k=.8)
add('<g clip-path="url(#%s-gl)">' % PID)
add('<path d="%s" fill="%s" stroke="%s" stroke-width=".7"/>' % (mound, SAND, INK))
add('<path d="%s" fill="url(#ink-stipple)" opacity=".75"/>' % mound)
add('<path d="%s" fill="url(#ink-hatch)" opacity=".35"/>' % cr([hg(14, 30), hg(24, 36), hg(34, 42), hg(34, 84), hg(20, 84)], True))
# a little sand left on top
topS = cr([hg(-14, -12), hg(-6, -16), hg(0, -17), hg(6, -16), hg(14, -12), hg(6, -6), hg(0, -2), hg(-6, -6)], True)
add('<path d="%s" fill="%s" stroke="%s" stroke-width=".5"/><path d="%s" fill="url(#ink-stipple)" opacity=".6"/>' % (topS, SAND, INK, topS))
add('<path d="M%s %s V%s" stroke="%s" stroke-width="1.6" stroke-dasharray="1.5 1.2"/>' % (f(HX), f(HY - 2), f(HY + 19), SAND_D))
add('</g>')
add('<path d="%s" fill="url(#%s-glass)" stroke="%s" stroke-width="1.3"/>' % (glass, PID, INK))
add('<path d="%s" fill="none" stroke="#fff" stroke-width="2" stroke-opacity=".8"/>' % cr([hg(-26, -64), hg(-29, -48), hg(-24, -30)]))
add('<path d="%s" fill="none" stroke="#fff" stroke-width="2" stroke-opacity=".8"/>' % cr([hg(-25, 30), hg(-29, 48), hg(-26, 64)]))
# wooden plates
for yy in (-80, 80):
    sgn = -1 if yy < 0 else 1
    y1 = HY + yy + sgn * 1
    add('<path d="M%s %s h104 v%s h-104z" fill="#b98049" stroke="%s" stroke-width="1"/>' % (f(HX - 52), f(y1 if sgn > 0 else y1 - 9), 9, INK))
    add('<path d="M%s %s h104" stroke="#e7c08c" stroke-width="1"/>' % (f(HX - 52), f((y1 if sgn > 0 else y1 - 9) + 2)))
    add('<path d="M%s %s h104 v%s h-104z" fill="url(#ink-hatch-h)" opacity=".6"/>' % (f(HX - 52), f((y1 if sgn > 0 else y1 - 9) + 5), 4))
    add('<ellipse cx="%s" cy="%s" rx="56" ry="3.6" fill="#9a6535" stroke="%s" stroke-width=".9"/>' % (f(HX), f(y1 + sgn * 9 if sgn > 0 else y1 - 9), INK))
# gauge on the right
GX = 132
for (yy, txt1, txt2, col) in ((76, '07:00 起床', '沙子幾乎是空的', '#5d4b38'), (22, '23:00', '沙滿了 → 很睏', TCM)):
    y = HY + yy
    add('<path d="M%s %s H%s" stroke="%s" stroke-width=".7" stroke-dasharray="2 2"/>' % (f(HX + 36), f(y), f(GX - 2), INK))
    add(T(GX, y + 1, txt1, 'lb', size=12.5, color=col))
    add(T(GX, y + 15, txt2, 'ls', size=11.5))
add('<path d="M%s %s V%s" stroke="%s" stroke-width="1.6" marker-end="url(#%s-ar)"/>' % (f(GX - 8), f(HY + 82), f(HY + 30), TCM, PID))
add(T(GX, HY - 62, '醒著越久', 'lb', size=12.5))
add(T(GX, HY - 47, '下半部沙子越多', 'ls', size=11.5))
add(T(GX, HY - 22, '睡著時', 'lb', size=12.5, color=WEST))
add(T(GX, HY - 7, '沙子被慢慢清空', 'ls', size=11.5))
# texts bottom
add('<path d="M22 262 H238" stroke="#c9b48a" stroke-width=".6"/>')
add(T(22, 282, '學名：恆定睡眠驅力', 'lb', size=12.5))
add(T(22, 298, '（Process S）', 'le', size=11.5))
add(T(22, 316, '沙子＝腦中累積的腺苷 adenosine', 'ls', size=11.5))

# ======================= PANEL 2: TIDE =======================
add(panel(260, 8, 240, 322))
add(numc(280, 30, '2', '#3f6fa6'))
add(T(296, 35, '生理時鐘潮汐', 'lb', size=16))
add(T(296, 51, 'the circadian tide', 'le', size=11))

# alertness control points (clock hour, 0..1)
CP = [(4, 0.0), (7, 0.24), (10, 0.52), (12, 0.6), (14, 0.54), (16, 0.66), (18, 0.82), (20.5, 0.98), (22, 0.86), (23, 0.66), (24.5, 0.4), (26.5, 0.13), (28, 0.0), (31, 0.24)]
CPD = bez_pts(CP, per=24)


def Cval(c):
    if c < 6.99:
        c += 24
    for (a, b), (d, e) in zip(CPD, CPD[1:]):
        if a <= c <= d:
            return b + (e - b) * (c - a) / max(d - a, 1e-9)
    return CPD[-1][1]

TX0, TX1, TYB, TAMP = 272, 488, 214, 122
def tx(h):   # h: hours since 07:00
    return TX0 + (TX1 - TX0) * h / 24
def ty(v):
    return TYB - v * TAMP
D.append('<clipPath id="%s-tc"><rect x="%d" y="60" width="%d" height="190"/></clipPath>' % (PID, TX0 - 4, TX1 - TX0 + 8))
add('<g clip-path="url(#%s-tc)">' % PID)
add('<rect x="%d" y="60" width="%d" height="190" fill="url(#%s-sky)"/>' % (TX0 - 4, TX1 - TX0 + 8, PID))
wave = [(tx(i / 4), ty(Cval(7 + i / 4))) for i in range(0, 97)]
wd = poly([(TX0 - 4, wave[0][1])] + wave + [(TX1 + 4, wave[-1][1]), (TX1 + 4, 252), (TX0 - 4, 252)], True)
add('<path d="%s" fill="url(#%s-sea)"/>' % (wd, PID))
add('<path d="%s" fill="url(#ink-hatch-h)" opacity=".8"/>' % wd)
# little wavelets on water
rnd = random.Random(7)
wl = ''
for i in range(70):
    h = rnd.uniform(0, 24); v = Cval(7 + h)
    yy = ty(v) + rnd.uniform(8, 210 - ty(v) if ty(v) < 200 else 12)
    if yy > 246:
        continue
    x = tx(h)
    wl += 'M%s %s q2.5 -2.2 5 0 q2.5 2.2 5 0' % (f(x - 5), f(yy))
add('<path d="%s" fill="none" stroke="#e8eef6" stroke-width=".7" stroke-opacity=".8"/>' % wl)
# foam crests along the surface
crest = ''
for i in range(0, 96, 5):
    x, y = wave[i]
    crest += 'M%s %s q3 -4 6 -1 q-2 0 -2.5 2' % (f(x - 3), f(y + 1))
add('<path d="%s" fill="none" stroke="#fff" stroke-width="1"/>' % crest)
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.6"/>' % (poly(wave), INK))
add('</g>')
add('<rect x="%d" y="60" width="%d" height="190" fill="none" stroke="%s" stroke-width=".8"/>' % (TX0 - 4, TX1 - TX0 + 8, INK))
# sun & moon
sx_, sy_ = tx(6), 80
add('<circle cx="%s" cy="%s" r="10" fill="#f6d36a" stroke="%s" stroke-width=".9"/>' % (f(sx_), f(sy_), INK))
sr = ''
for i in range(12):
    a = math.radians(i * 30)
    sr += 'M%s %sL%s %s' % (f(sx_ + 13 * math.cos(a)), f(sy_ + 13 * math.sin(a)), f(sx_ + 18 * math.cos(a)), f(sy_ + 18 * math.sin(a)))
add('<path d="%s" stroke="#b8862a" stroke-width="1.1"/>' % sr)
mx_, my_ = tx(20.5), 108
add('<path d="M%s %s a13 13 0 1 0 11 19 a10 10 0 1 1 -11 -19z" fill="#f4ecc8" stroke="%s" stroke-width=".9"/>' % (f(mx_ - 2), f(my_ - 12), INK))
for (x, y) in ((tx(22.8), 74), (tx(17.6), 128), (tx(23), 140)):
    add('<path d="M%s %s l1.2 3 3 .3 -2.3 2 .8 3 -2.7 -1.6 -2.7 1.6 .8 -3 -2.3 -2 3 -.3z" fill="#f4ecc8" stroke="%s" stroke-width=".45"/>' % (f(x), f(y - 4), INK))
# annotations
pk = (tx(13.5), ty(.98))
add(T(pk[0] - 4, 74, '晚上 8–9 點', 'lb', 'middle', size=12, color=TCM))
add(T(pk[0] - 4, 88, '第二波清醒', 'lb', 'middle', size=12, color=TCM))
add('<path d="M%s %s L%s %s" stroke="%s" stroke-width=".8" marker-end="url(#%s-ar)"/>' % (f(pk[0] - 4), f(92), f(pk[0]), f(pk[1] - 4), TCM, PID))
add(T(tx(18.6), 226, '凌晨 3–5 點', 'lb', 'middle', size=12, color='#fff', halo=False))
add(T(tx(18.6), 242, '最低潮', 'lb', 'middle', size=11, color='#fff', halo=False))
# ticks
for h, lb in ((0, '07'), (5, '12'), (11, '18'), (17, '24'), (20, '03'), (24, '07')):
    x = tx(h)
    add('<path d="M%s 250 v4" stroke="%s" stroke-width=".8"/>' % (f(x), INK))
    add(T(x, 265, lb, 'ls', 'middle', size=11))
add(T(TX0 - 6, 265, '', 'ls'))
add('<path d="M272 278 H490" stroke="#c9b48a" stroke-width=".6"/>')
add(T(272, 296, '浪越高＝時鐘給的清醒力越強', 'ls', size=12))
add(T(272, 314, '學名：晝夜節律（Process C）', 'lb', size=12.5))

# ======================= PANEL 3: ALARM BELL =======================
add(panel(510, 8, 240, 322))
add(numc(530, 30, '3', '#a8412c'))
add(T(546, 35, '壓力警報器', 'lb', size=16))
add(T(546, 51, 'the stress alarm', 'le', size=11))
BX, BY = 604, 150
# wall plaque (wood) behind
add('<path d="%s" fill="#a8412c" stroke="%s" stroke-width="1.1"/>' % (cr([(BX - 30, BY - 72), (BX + 30, BY - 72), (BX + 36, BY - 60), (BX + 36, BY + 66), (BX + 30, BY + 78), (BX - 30, BY + 78), (BX - 36, BY + 66), (BX - 36, BY - 60)], True, k=.6), INK))
add('<path d="%s" fill="url(#ink-hatch)" opacity=".5"/>' % cr([(BX + 18, BY - 72), (BX + 30, BY - 72), (BX + 36, BY - 60), (BX + 36, BY + 66), (BX + 30, BY + 78), (BX + 18, BY + 78)], True, k=.6))
for yy in (-62, 68):
    add('<circle cx="%s" cy="%s" r="3" fill="#d9c08a" stroke="%s" stroke-width=".7"/><path d="M%s %s h4" stroke="%s" stroke-width=".7"/>' % (BX, BY + yy, INK, BX - 2, BY + yy, INK))
# striker mechanism box below bell
add('<rect x="%s" y="%s" width="30" height="22" rx="3" fill="#7b2f22" stroke="%s" stroke-width="1"/>' % (BX - 15, BY + 34, INK))
add('<rect x="%s" y="%s" width="30" height="22" rx="3" fill="url(#ink-hatch-r)" opacity=".5"/>' % (BX - 15, BY + 34))
# bell dome
add('<circle cx="%s" cy="%s" r="44" fill="url(#%s-brass)" stroke="%s" stroke-width="1.4"/>' % (BX, BY - 6, PID, INK))
for rr, op in ((36, .7), (24, .6), (12, .6)):
    add('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width=".7" stroke-opacity="%s"/>' % (BX, BY - 6, rr, INK, op))
D.append('<clipPath id="%s-bc"><circle cx="%s" cy="%s" r="44"/></clipPath>' % (PID, BX, BY - 6))
add('<path d="%s" fill="url(#ink-hatch)" opacity=".55" clip-path="url(#%s-bc)"/>' % (cr([(BX + 10, BY - 52), (BX + 50, BY - 20), (BX + 46, BY + 30), (BX + 10, BY + 44), (BX + 30, BY + 10), (BX + 30, BY - 22)], True), PID))
add('<path d="M%s %s a30 30 0 0 1 22 -12" fill="none" stroke="#fff8dc" stroke-width="3" stroke-linecap="round" opacity=".9"/>' % (BX - 30, BY - 22))
add('<circle cx="%s" cy="%s" r="5" fill="#8a5f1c" stroke="%s" stroke-width=".8"/>' % (BX, BY - 6, INK))
# hammer arm striking the rim
add('<path d="M%s %s L%s %s" stroke="%s" stroke-width="3.6" stroke-linecap="round"/><path d="M%s %s L%s %s" stroke="#c9c2b0" stroke-width="2" stroke-linecap="round"/>' % (BX, BY + 40, BX + 26, BY + 32, INK, BX, BY + 40, BX + 26, BY + 32))
add('<circle cx="%s" cy="%s" r="5.5" fill="#5a5048" stroke="%s" stroke-width=".9"/>' % (BX + 28, BY + 31, INK))
# vibration marks
for k, rr in enumerate((54, 62, 70)):
    for a0, a1 in ((-150, -115), (-65, -30), (150, 185)):
        a0r, a1r = math.radians(a0), math.radians(a1)
        add('<path d="M%s %s A%d %d 0 0 1 %s %s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-opacity="%s"/>' % (
            f(BX + rr * math.cos(a0r)), f(BY - 6 + rr * math.sin(a0r)), rr, rr, f(BX + rr * math.cos(a1r)), f(BY - 6 + rr * math.sin(a1r)), TCM, 1.6 - k * .3, 1 - k * .25))
# tags wired into the bell
for k, (txt, en) in enumerate((('壓力', 'stress'), ('焦慮', 'worry'), ('疼痛', 'pain'))):
    yy = BY - 20 + k * 40
    x0 = 684
    add('<path d="M%s %s C%s %s %s %s %s %s" fill="none" stroke="%s" stroke-width="1" stroke-dasharray="3 2"/>' % (
        x0, yy, x0 - 20, yy, BX + 50, BY + 46, BX + 15, BY + 46, INK))
    add('<rect x="%s" y="%s" width="56" height="30" rx="3" fill="#fbf6ea" stroke="%s" stroke-width=".9"/>' % (x0, yy - 15, INK))
    add('<circle cx="%s" cy="%s" r="2" fill="none" stroke="%s" stroke-width=".7"/>' % (x0 + 5, yy, INK))
    add(T(x0 + 30, yy - 1, txt, 'lb', 'middle', size=13, color=TCM, halo=False))
    add(T(x0 + 30, yy + 11, en, 'le', 'middle', size=10.5, halo=False))
add('<path d="M522 262 H738" stroke="#c9b48a" stroke-width=".6"/>')
add(T(522, 282, '壓力、焦慮、疼痛會讓大腦留在清醒', 'ls', size=12))
add(T(522, 299, '警報一響，可以蓋過沙漏和潮汐', 'lb', size=12.5, color=TCM))
add(T(522, 316, '學名：過度警醒 hyperarousal', 'ls', size=11.5))

# ======================= COMBINED CHART =======================
CY0, CY1 = 382, 590
CXa, CXb = 92, 610
def X(h):     # hours since 07:00
    return CXa + (CXb - CXa) * h / 24
def Y(v):
    return CY1 - v * (CY1 - CY0)
add(T(14, 356, '把三者放在一起：一天 24 小時', 'lb', size=15))
add(T(238, 356, 'the three forces over 24 hours', 'le', size=11.5))

# simulate sand
def sim(nap=None, bed=None):
    out = []
    s = 0.12; t = 7.0; dt = 0.05
    asleep_from = None
    while t <= 31.0001:
        c = Cval(t if t < 31 else 31)
        if nap and nap[0] <= t < nap[1]:
            s *= math.exp(-dt / 4.0)
        elif t >= 21.5 and (asleep_from is not None or s >= c):
            if asleep_from is None:
                asleep_from = t
            s *= math.exp(-dt / 4.0)
        else:
            s = 1 - (1 - s) * math.exp(-dt / 12)
        out.append((t, s))
        t += dt
    return out, asleep_from
SN, on_n = sim()
SP_, on_p = sim(nap=(13.5, 16.0))
# wake time: when s < c after 04:00
def wake_of(S):
    for t, s in S:
        if t > 28 and s < Cval(t):
            return t
    return 31
wk = wake_of(SN)
# night background & gate
add('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(X(on_n - 7)), CY0, f(X(wk - 7) - X(on_n - 7)), CY1 - CY0, '#dde4f1'))
add('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#ink-hatch-l)" opacity=".5"/>' % (f(X(on_n - 7)), CY0, f(X(wk - 7) - X(on_n - 7)), CY1 - CY0))
add(T((X(on_n - 7) + X(wk - 7)) / 2 + 10, CY0 + 70, '睡眠之門打開 → 睡著', 'lb', 'middle', size=13, color=WEST))
add(T((X(on_n - 7) + X(wk - 7)) / 2 + 10, CY0 + 85, 'sleep gate open', 'le', 'middle', size=11))
# axes
add('<path d="M%s %s V%s H%s" fill="none" stroke="%s" stroke-width="1"/>' % (CXa, CY0 - 6, CY1, CXb + 4, INK))
for h in range(0, 25, 1):
    add('<path d="M%s %s v%s" stroke="%s" stroke-width="%s"/>' % (f(X(h)), CY1, 5 if h % 3 == 0 else 2.5, INK, .8 if h % 3 == 0 else .5))
    if h % 3 == 0:
        add(T(X(h), CY1 + 17, '%02d' % ((7 + h) % 24), 'ls', 'middle', size=11))
add(T(CXb + 12, CY1 + 17, '時', 'ls', size=11))
add(T(CXa - 8, CY0 + 2, '高', 'ls', 'end', size=11))
add(T(CXa - 8, CY1 - 2, '低', 'ls', 'end', size=11))
# tide curve (filled water)
tide = [(X(i / 4), Y(Cval(7 + i / 4))) for i in range(0, 97)]
add('<path d="%s" fill="%s" fill-opacity=".55"/>' % (poly(tide + [(X(24), CY1), (X(0), CY1)], True), SEA_S))
add('<path d="%s" fill="url(#ink-hatch-h)" opacity=".5"/>' % poly(tide + [(X(24), CY1), (X(0), CY1)], True))
add('<path d="%s" fill="none" stroke="%s" stroke-width="2.2"/>' % (poly(tide), SEA))
# sand curves
def spath(S):
    return poly([(X(t - 7), Y(s)) for t, s in S[::2]])
add('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="5 3.5"/>' % (spath(SP_), '#b8862a'))
add('<path d="%s" fill="none" stroke="%s" stroke-width="4.6" stroke-linecap="round"/>' % (spath(SN), INK))
add('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (spath(SN), SAND))
# small sand grains along line
# door icon at the crossing
dx_, dy_ = X(on_n - 7), Y(Cval(on_n))
add('<g transform="translate(%s,%s)">' % (f(dx_ + 6), f(dy_ - 46)) +
    '<rect x="0" y="0" width="24" height="38" fill="#3b4a66" stroke="%s" stroke-width="1"/>' % INK +
    '<path d="M24 0 L36 -4 L36 42 L24 38Z" fill="#b98049" stroke="%s" stroke-width="1"/>' % INK +
    '<path d="M27 4 L33 2 V16 L27 18Z M27 22 L33 21 V36 L27 34Z" fill="none" stroke="%s" stroke-width=".6"/>' % INK +
    '<circle cx="26.5" cy="20" r="1.2" fill="%s"/>' % INK +
    '<path d="M2 36 L22 36 L18 30 L6 30Z" fill="#f6e7b0" opacity=".7"/></g>')
add('<circle cx="%s" cy="%s" r="4" fill="%s" stroke="%s" stroke-width="1"/>' % (f(dx_), f(dy_), PAPER, INK))
add(T(dx_ + 48, dy_ - 30, '沙子壓過潮水', 'lb', size=12.5))
add(T(dx_ + 48, dy_ - 15, '→ 門打開', 'lb', size=12.5, color=WEST))
# second wind annotation
pkx, pky = X(13.5), Y(Cval(20.5))
add(T(pkx - 26, CY0 - 2, '第二波清醒：沙子還壓不過潮水', 'ls', 'end', size=11.5, color=TCM))
add('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="%s" stroke-width=".8" marker-end="url(#%s-ar)"/>' % (f(pkx - 30), f(CY0 - 6), f(pkx - 14), f(CY0 - 10), f(pkx - 4), f(pky - 4), TCM, PID))
# wake annotation
wx, wy = X(wk - 7), Y(Cval(wk))
add('<circle cx="%s" cy="%s" r="3.5" fill="%s" stroke="%s" stroke-width="1"/>' % (f(wx), f(wy), PAPER, INK))
# nap crossing (door opens later)
npx = X(on_p - 7); npy = Y(Cval(on_p))
add('<circle cx="%s" cy="%s" r="3.2" fill="#b8862a" stroke="%s" stroke-width=".8"/>' % (f(npx), f(npy), INK))
add(T(npx - 10, npy + 34, '有午睡：門較晚才開', 'ls', 'end', size=11.5, color='#8a6418'))
add('<path d="M%s %s L%s %s" class="ld"/>' % (f(npx - 10), f(npy + 28), f(npx - 2), f(npy + 4)))
# curve labels
add(T(X(4.5), Y(0.38) + 30, '睡意沙子', 'lb', 'middle', size=13, color='#8a6418'))
add(T(X(4.6), Y(Cval(11.6)) - 10, '清醒潮汐', 'lb', 'middle', size=13, color=SEA))
add(T(X(10.6), Y(0.18), '午睡太久', 'lb', 'middle', size=12, color='#8a6418'))
add('<path d="M%s %s L%s %s" class="ld" marker-end="url(#ink-dot)"/>' % (f(X(10.6)), f(Y(.18) - 14), f(X(8.8)), f(Y(0.30))))

# right-side notes
NX = 626
add(T(NX, CY0 + 2, '圖例', 'lb', size=12.5))
add('<path d="M%s %s h24" stroke="%s" stroke-width="4.6"/><path d="M%s %s h24" stroke="%s" stroke-width="3"/>' % (NX, CY0 + 20, INK, NX, CY0 + 20, SAND))
add(T(NX + 30, CY0 + 24, '睡意沙子', 'ls', size=11.5))
add('<path d="M%s %s h24" stroke="%s" stroke-width="2.2"/>' % (NX, CY0 + 40, SEA))
add(T(NX + 30, CY0 + 44, '清醒潮汐', 'ls', size=11.5))
add('<path d="M%s %s h24" stroke="#b8862a" stroke-width="1.6" stroke-dasharray="5 3.5"/>' % (NX, CY0 + 60))
add(T(NX + 30, CY0 + 64, '有睡午覺', 'ls', size=11.5))
# nap box
add('<rect x="%s" y="%s" width="126" height="92" rx="4" fill="#f6e7b0" stroke="%s" stroke-width=".8"/>' % (NX - 4, CY0 + 82, INK))
add(T(NX + 4, CY0 + 102, '午睡太久', 'lb', size=13.5, color=TCM))
add(T(NX + 4, CY0 + 119, '＝提前漏掉沙子', 'lb', size=13.5, color=TCM))
add(T(NX + 4, CY0 + 138, '晚上沙子不夠，', 'ls', size=11.5))
add(T(NX + 4, CY0 + 154, '門開得比較晚', 'ls', size=11.5))
add(T(NX + 4, CY0 + 168, '（短於 20–30 分較無妨）', 'ls', size=10))

# alarm note under chart
AY = CY1 + 34
add('<rect x="14" y="%s" width="732" height="54" rx="5" fill="#f6dcd4" stroke="%s" stroke-width=".8"/>' % (AY, INK))
add('<g transform="translate(40,%s) scale(.42)">' % (AY + 27) +
    '<circle r="44" fill="url(#%s-brass)" stroke="%s" stroke-width="2.4"/><circle r="30" fill="none" stroke="%s" stroke-width="1.4"/><circle r="8" fill="#8a5f1c"/>' % (PID, INK, INK) +
    '<path d="M-58 -30 a62 62 0 0 1 0 60 M58 -30 a62 62 0 0 0 0 60" fill="none" stroke="%s" stroke-width="3"/></g>' % TCM)
add(T(74, AY + 23, '③ 警報器響時：就算沙子已滿、潮水已退，門也會被卡住', 'lb', size=13.5, color=TCM))
add(T(74, AY + 42, '所以「很累卻睡不著」常常不是睡意不夠，而是警報器沒關。', 'ls', size=12))

body = '\n'.join(o)
write(PID, '圖 2·A', '讓你想睡的兩股力量，和一個警報器', 'Two forces that make you sleepy — and one alarm', H, body,
      '三個比喻：睡意沙漏、生理時鐘潮汐、壓力警報器；下方為二十四小時合併圖，沙子高過潮水時睡眠之門打開。',
      '<b>圖 2·A　兩股力量和一個警報器。</b>醒著越久，「睡意沙漏」積的沙子越多；「生理時鐘潮汐」則像海浪，傍晚到睡前反而有一波最高的清醒浪，凌晨三到五點最低。等沙子壓過潮水，睡眠之門才會打開；午睡太久會先漏掉沙子，晚上門就開得晚。壓力、焦慮、疼痛像警報器，一響就能把門卡住。曲線為示意，非實際測量值。',
      '\n'.join(D))
