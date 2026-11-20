"""pp-cave  圖 1·B  Kleitman & Richardson in Mammoth Cave (1938) + free-running actogram."""
import sys, math, random
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from clk_lib import write, T, lead, f, cr, poly, rot, sun, moon, L, INK, tapered

PID = 'pp-cave'
H = 494
o, defs = [], []

o.append(T(190, 21, '① 1938 年，住進肯塔基州的猛瑪洞', 'lt', 'middle'))
o.append(T(570, 21, '② 沒有陽光，睡覺時間一天天往後飄', 'lt', 'middle'))

# =============================================================== LEFT: cave chamber
X0, Y0, W, HH = 10, 32, 360, 364
defs.append('<clipPath id="%s-cl"><rect x="%s" y="%s" width="%s" height="%s" rx="3"/></clipPath>' % (PID, X0, Y0, W, HH))
defs.append('<radialGradient id="%s-lit" cx="%s" cy="%s" r="230" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f1dfb4"/><stop offset=".35" stop-color="#cdb48c"/><stop offset=".75" stop-color="#7e6a55"/><stop offset="1" stop-color="#4a3e34"/></radialGradient>' % (PID, 190, 175))
defs.append('<radialGradient id="%s-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffe08a" stop-opacity=".85"/><stop offset=".4" stop-color="#f7b955" stop-opacity=".3"/><stop offset="1" stop-color="#f7b955" stop-opacity="0"/></radialGradient>' % PID)
c = ['<g clip-path="url(#%s-cl)">' % PID]
c.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#3d332c"/>' % (X0, Y0, W, HH))
c.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#ink-hatch-d)" opacity=".7"/>' % (X0, Y0, W, HH))
# chamber (lit rock surface)
arch = [(X0, 400), (16, 250), (22, 170), (52, 110), (110, 74), (190, 62), (270, 70), (330, 104), (362, 160), (370, 240), (372, 400)]
c.append('<path d="%s" fill="url(#%s-lit)" stroke="%s" stroke-width="1.6"/>' % (cr(arch), PID, INK))
# limestone strata (curved bedding planes) on the chamber wall
rnd = random.Random(5)
for k, yy in enumerate([96, 122, 150, 182, 214, 246]):
    pts = []
    for i in range(9):
        x = 14 + i * 45
        pts.append((x, yy + 10 * math.sin(i * .9 + k) + abs(x - 190) * -.08 + 20))
    c.append('<path d="%s" fill="none" stroke="%s" stroke-width=".7" stroke-opacity=".55"/>' % (cr(pts), INK))
    pts2 = [(x, y + 4) for x, y in pts]
    c.append('<path d="%s" fill="none" stroke="%s" stroke-width=".35" stroke-opacity=".45" stroke-dasharray="6 3 2 4"/>' % (cr(pts2), INK))
# shadow near the arch edge (engraved)
edge = [(16, 250), (22, 170), (52, 110), (110, 74), (190, 62), (270, 70), (330, 104), (362, 160), (370, 240)]
inner = [(x + (190 - x) * .12, y + (220 - y) * .14) for x, y in edge]
c.append('<path d="%s" fill="url(#ink-hatch)" opacity=".75"/>' % (cr(edge) + cr(inner[::-1])[0:].replace('M', 'L', 1) + 'Z'))
# stalactites
for sx, sy, ln in [(70, 98, 16), (84, 90, 9), (250, 68, 14), (300, 86, 20), (312, 92, 10), (140, 70, 8)]:
    c.append('<path d="M%s %s L%s %s L%s %s Z" fill="#b9a382" stroke="%s" stroke-width=".8"/>' % (sx - 4, sy - 4, sx, sy + ln, sx + 4, sy - 4, INK))
    c.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width=".4"/>' % (sx + 1, sy - 2, sx + .5, sy + ln - 4, INK))
# floor
floor = [(X0, 322), (60, 318), (130, 324), (200, 320), (270, 326), (330, 320), (372, 324), (372, 392), (X0, 392)]
c.append('<path d="%s" fill="#a08a6b" stroke="%s" stroke-width="1.1"/>' % (cr(floor[:7]) + ' L372 400 L10 400 Z', INK))
c.append('<path d="%s Z" fill="url(#ink-stipple)" opacity=".6"/>' % (cr(floor[:7]) + ' L372 400 L10 400'))
for rx_, ry_, rr in [(30, 372, 9), (348, 378, 11), (190, 384, 6), (100, 386, 5)]:
    c.append('<path d="M%s %s q%s %s %s 0 q-%s %s -%s 0Z" fill="#8d7658" stroke="%s" stroke-width=".8"/>' % (rx_ - rr, ry_, rr, -rr * 1.2, 2 * rr, rr, rr * .3, 2 * rr, INK))


def bucket(x, y, s=1.0):
    """pail, rim centre (x,y); bed leg enters it"""
    w0, w1, h = 12 * s, 9 * s, 20 * s
    g = ['<path d="M%s %s L%s %s Q%s %s %s %s L%s %s Z" fill="#9aa3a6" stroke="%s" stroke-width="1"/>' % (
        f(x - w0), f(y), f(x - w1), f(y + h), f(x), f(y + h + 2), f(x + w1), f(y + h), f(x + w0), f(y), INK)]
    g.append('<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="url(#ink-hatch)"/>' % (f(x + 2), f(y), f(x + 2), f(y + h + 1), f(x + w1), f(y + h), f(x + w0), f(y)))
    g.append('<path d="M%s %s H%s M%s %s H%s" stroke="%s" stroke-width=".6"/>' % (f(x - w0 + .8), f(y + 5), f(x + w0 - .8), f(x - w1 - .5), f(y + h - 5), f(x + w1 + .5), INK))
    g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#6f9cc8" stroke="%s" stroke-width=".9"/>' % (f(x), f(y), f(w0), f(3 * s), INK))
    g.append('<path d="M%s %s C%s %s %s %s %s %s" fill="none" stroke="%s" stroke-width=".8"/>' % (f(x - w0), f(y + 1), f(x - w0), f(y - 12 * s), f(x + w0), f(y - 12 * s), f(x + w0), f(y + 1), INK))
    return ''.join(g)


def bed(x0, x1, top, legs, back_off=(7, -5)):
    """wooden camp bed side view; legs stand in water buckets; top = mattress top y"""
    g = []
    bx, by = back_off
    floor_y = top + 64
    # back legs + buckets (seen slightly behind)
    for lx in legs:
        g.append(bucket(lx + bx, floor_y - 20 + by, .85))
        g.append('<rect x="%s" y="%s" width="5" height="%s" fill="#6d4a2e" stroke="%s" stroke-width=".8"/>' % (f(lx + bx - 2.5), top + 18 + by, floor_y - 20 + by - top - 18 + 2, INK))
    # frame + mattress
    g.append('<rect x="%s" y="%s" width="%s" height="7" fill="#7f5534" stroke="%s" stroke-width="1"/>' % (x0, top + 14, x1 - x0, INK))
    g.append('<path d="M%s %s Q%s %s %s %s H%s Q%s %s %s %s V%s H%s Z" fill="#e8dfcb" stroke="%s" stroke-width="1.1"/>' % (
        x0, top + 14, x0, top, x0 + 8, top, x1 - 8, x1, top, x1, top + 6, top + 14, x0, INK))
    g.append('<path d="M%s %s H%s" stroke="%s" stroke-width=".5" stroke-dasharray="2 3"/>' % (x0 + 4, top + 10, x1 - 4, INK))
    for lx in legs:
        g.append('<rect x="%s" y="%s" width="6" height="%s" fill="#7f5534" stroke="%s" stroke-width=".9"/>' % (f(lx - 3), top + 20, floor_y - 20 - top - 20 + 6, INK))
        g.append('<rect x="%s" y="%s" width="3" height="%s" fill="url(#ink-hatch-d)"/>' % (f(lx), top + 20, floor_y - 20 - top - 20 + 6))
        g.append(bucket(lx, floor_y - 20))
    return ''.join(g)


# hanging kerosene lantern (behind people)
lx, ly = 190, 150
c.append('<ellipse cx="%s" cy="%s" rx="150" ry="130" fill="url(#%s-glow)"/>' % (lx, ly + 10, PID))
c.append('<path d="M%s 62 V%s" stroke="%s" stroke-width=".9"/>' % (lx, ly - 22, INK))


def lantern(x, y, s=1.0):
    g = []
    g.append('<path d="M%s %s C%s %s %s %s %s %s" fill="none" stroke="%s" stroke-width="1"/>' % (f(x - 9 * s), f(y - 8 * s), f(x - 9 * s), f(y - 24 * s), f(x + 9 * s), f(y - 24 * s), f(x + 9 * s), f(y - 8 * s), INK))
    g.append('<path d="M%s %s h%s l-%s -%s h-%s Z" fill="#7b6a4a" stroke="%s" stroke-width=".9"/>' % (f(x - 7 * s), f(y - 6 * s), f(14 * s), f(3 * s), f(5 * s), f(8 * s), INK))
    g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff1c2" stroke="%s" stroke-width=".9"/>' % (f(x), f(y + 6 * s), f(7.5 * s), f(12 * s), INK))
    g.append('<path d="M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s Z" fill="#f6b84a"/>' % (
        f(x), f(y - 1 * s), f(x + 3 * s), f(y + 4 * s), f(x + 3 * s), f(y + 9 * s), f(x), f(y + 10 * s), f(x - 3 * s), f(y + 9 * s), f(x - 3 * s), f(y + 4 * s), f(x), f(y - 1 * s)))
    g.append('<path d="M%s %s V%s M%s %s V%s" stroke="%s" stroke-width=".7"/>' % (f(x - 8 * s), f(y - 4 * s), f(y + 17 * s), f(x + 8 * s), f(y - 4 * s), f(y + 17 * s), INK))
    g.append('<path d="M%s %s h%s v%s h-%s Z" fill="#6a5a3e" stroke="%s" stroke-width=".9"/>' % (f(x - 10 * s), f(y + 17 * s), f(20 * s), f(7 * s), f(20 * s), INK))
    g.append('<path d="M%s %s h%s v%s h-%s Z" fill="url(#ink-hatch)"/>' % (f(x + 2 * s), f(y + 17 * s), f(8 * s), f(7 * s), f(8 * s)))
    return ''.join(g)


c.append(lantern(lx, ly))

# --- back bed (left) with seated Kleitman (generic 1930s scientist)
c.append(bed(24, 176, 254, [40, 120]))
# folded blanket + pillow at left end
c.append('<ellipse cx="44" cy="250" rx="17" ry="6" fill="#f6f1e4" stroke="%s" stroke-width=".9"/>' % INK)
c.append('<path d="M66 254 h40 v-8 q-20 -4 -40 0Z" fill="#9b7a5a" stroke="%s" stroke-width=".9"/><path d="M68 249 h36" class="ink2"/>' % INK)

# seated man: hips at (138,252)
hs = .4
hx, hy = 146, 158
sm = []
# legs (thigh to the right, shin down)
sm.append('<path d="M126 238 C140 236 170 238 194 240 C200 241 202 250 198 256 C176 258 150 258 130 258 Z" fill="#6b6152" stroke="%s" stroke-width="1.1"/>' % INK)
sm.append('<path d="M182 242 C188 262 190 290 192 312 L204 312 C204 290 202 266 198 246 Z" fill="#6b6152" stroke="%s" stroke-width="1.1"/>' % INK)
sm.append('<path d="M196 248 C200 268 202 290 204 312 L198 312 C198 290 196 268 192 250Z" fill="url(#ink-hatch)"/>')
sm.append('<path d="M190 312 C190 318 196 320 214 320 C216 316 212 312 204 310 Z" fill="#2f2620" stroke="%s" stroke-width="1"/>' % INK)
sm.append('<path d="M136 252 C150 254 168 254 186 250" class="ink2"/>')
# torso: shirt + waistcoat
sm.append('<path d="M128 182 C122 196 120 220 124 246 L160 248 C162 226 162 200 158 184 C150 178 136 178 128 182Z" fill="#efe9da" stroke="%s" stroke-width="1.1"/>' % INK)
sm.append('<path d="M140 182 C136 200 134 224 136 248 L160 248 C162 226 162 200 158 184 C152 180 146 180 140 182Z" fill="#59564c" stroke="%s" stroke-width="1"/>' % INK)
sm.append('<path d="M148 184 L150 206 L146 214 L144 206 Z" fill="#8a3a2c" stroke="%s" stroke-width=".6"/>' % INK)
for k in range(4):
    sm.append('<circle cx="%s" cy="%s" r="1" fill="#d9cfb8"/>' % (f(153 - k * .4), 212 + k * 9))
sm.append('<path d="M124 200 C122 220 122 236 124 246 L132 246 C130 230 130 214 132 200Z" fill="url(#ink-hatch)"/>')
# head (glasses, short hair)
sm.append(L.head(hx, hy, hs, hair='short'))
ex, ey = hx + 24 * hs, hy - 5 * hs
sm.append('<circle cx="%s" cy="%s" r="3.2" fill="none" stroke="%s" stroke-width=".8"/><path d="M%s %s L%s %s" stroke="%s" stroke-width=".7"/>' % (
    f(ex), f(ey), INK, f(ex - 3), f(ey - .5), f(hx - 1), f(hy - 2), INK))
# arm holding a notebook on the lap
sm.append('<path d="M134 188 C142 200 146 218 150 232 C160 236 174 236 184 232 L186 240 C172 246 156 246 144 242 C138 228 128 206 128 192Z" fill="#efe9da" stroke="%s" stroke-width="1.1"/>' % INK)
sm.append('<path d="M128 194 C132 210 138 228 144 240 L150 238 C144 226 138 210 134 196Z" fill="url(#ink-hatch-l)"/>')
sm.append('<path d="M170 222 L198 214 L204 232 L176 240 Z" fill="#f6f1e4" stroke="%s" stroke-width="1"/>' % INK)
sm.append('<path d="M176 226 L196 220 M177 230 L197 224 M178 234 L198 228" class="ink2"/>')
sm.append('<path d="M184 234 c3 -3 7 -4 9 -2 c2 2 0 5 -3 6 c-3 1 -6 0 -6 -4Z" fill="url(#ink-vol-flesh)" stroke="%s" stroke-width=".8"/>' % INK)
sm.append('<path d="M190 230 L204 210" stroke="#b08a3a" stroke-width="1.6" stroke-linecap="round"/>')
c.extend(sm)

# --- front bed (right) with sleeping Richardson
c.append(bed(206, 410, 286, [224, 352], back_off=(8, -6)))
c.append('<ellipse cx="226" cy="282" rx="18" ry="6.5" fill="#f6f1e4" stroke="%s" stroke-width=".9"/>' % INK)
c.append(L.head(229, 273, .34, rot=-90, eye='closed', hair='short'))
blanket = [(238, 288), (240, 272), (256, 264), (290, 265), (320, 272), (350, 270), (380, 276), (400, 288)]
c.append('<path d="%s Z" fill="#8f6f8a" stroke="%s" stroke-width="1.2"/>' % (cr(blanket), INK))
c.append('<path d="%s" fill="none" stroke="%s" stroke-width=".6"/>' % (cr([(258, 266), (266, 286)]) + cr([(296, 268), (300, 287)]) + cr([(334, 272), (340, 287)]), INK))
c.append('<path d="M238 288 C276 286 316 284 400 288 L400 280 C330 276 300 284 240 282Z" fill="url(#ink-hatch)"/>')
c.append('<path d="M238 272 c4 -2 9 -2 12 0 v6 h-12Z" fill="#efe9da" stroke="%s" stroke-width=".8"/>' % INK)
c.append('</g>')
o.extend(c)
o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="none" stroke="%s" stroke-width="1.4"/>' % (X0, Y0, W, HH, INK))

# labels on the cave
o.append(T(20, 52, '洞裡終年漆黑、恆溫約 12°C', 'ls', 'start', halo=False, style='fill:#f3e6c6;font-size:12px'))
o.append('<rect x="238" y="40" width="126" height="40" rx="2" fill="#fbf6ea" stroke="%s" stroke-width=".8" transform="rotate(2 300 60)"/>' % INK)
o.append('<g transform="rotate(2 300 60)">' + T(301, 56, '試過一天 28 小時：', 'lb', 'middle', halo=False, style='font-size:12.5px') +
         T(301, 72, '醒 19 小時＋睡 9 小時', 'ls', 'middle', halo=False, style='font-size:11.5px;fill:#a8412c;font-weight:700') + '</g>')
o.append(T(206, 132, '煤油燈', 'ls', 'start', style='font-weight:700'))
o.append(T(96, 124, '克萊特曼', 'lb', 'middle'))
o.append(T(96, 138, 'N. Kleitman', 'le', 'middle'))
o.append(T(300, 246, '理查森（睡著）', 'lb', 'middle'))
o.append(T(300, 260, 'B. Richardson', 'le', 'middle'))
o.append(lead([(246, 376), (232, 376), (225, 348)]))
o.append(T(250, 375, '床腳泡在水桶裡', 'lb', 'start', style='font-size:13px'))
o.append(T(250, 390, '防老鼠爬上床', 'ls', 'start', style='font-weight:700'))
o.append(T(24, 388, '兩人在洞裡共住了 32 天', 'ls', 'start', style='font-weight:700'))

# =============================================================== RIGHT: double-plotted actogram
AX0, AX1 = 446, 744
AY0 = 76
ND = 28
RH = 8.4
NENT = 8
TAU = 24.2
SLEEP = 8.0
px = (AX1 - AX0) / 48.0
X = lambda t: AX0 + t * px
rnd = random.Random(11)
a = []
a.append(T((AX0 + AX1) / 2, 41, '活動紀錄圖 actogram：每一列畫連續兩天（中午到中午）', 'ls', 'middle', halo=False, style='font-weight:700'))
labs = ['12', '18', '0', '6', '12', '18', '0', '6', '12']
for i, t in enumerate(range(0, 49, 6)):
    a.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width=".7"/>' % (f(X(t)), AY0 - 4, f(X(t)), AY0, INK))
    a.append(T(X(t), AY0 - 7, labs[i], 'ls', 'middle', halo=False))
a.append(T(X(12), AY0 - 21, '第 n 天的夜晚', 'ls', 'middle', halo=False, style='fill:#8a6a3a'))
a.append(T(X(36), AY0 - 21, '第 n+1 天的夜晚', 'ls', 'middle', halo=False, style='fill:#8a6a3a'))
a.append(T(AX0 - 6, AY0 - 21, '第幾天', 'ls', 'end', halo=False, style='fill:#8a6a3a'))

rnd_on = [random.Random(d * 7 + 1).uniform(-.22, .22) for d in range(ND + 4)]


def onset(k):
    """clock hour of sleep onset on night k (may exceed 24)"""
    if k < NENT:
        return 23.0 + rnd_on[k]
    return 23.0 + (k - NENT + 1) * (TAU - 24) + rnd_on[k]


for d in range(ND):
    y = AY0 + d * RH
    ent = d < NENT
    w0 = 24 * d + 12           # absolute hour at left edge of this row
    if ent:
        a.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#dfe3ee"/>' % (AX0, f(y), f(48 * px), f(RH)))
        for j in range(d - 1, d + 3):
            s0, s1 = 24 * j + 6.5 - w0, 24 * j + 18.5 - w0
            a0, a1 = max(0, s0), min(48, s1)
            if a1 > a0:
                a.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#f7e7b0"/>' % (f(X(a0)), f(y), f((a1 - a0) * px), f(RH)))
    else:
        a.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#e6e0d4"/>' % (AX0, f(y), f(48 * px), f(RH)))
    eps = []
    for k in range(d - 1, d + 3):
        if k < 0:
            continue
        s0 = 24 * k + onset(k) - w0
        eps.append((s0, s0 + SLEEP))
    for s0, s1 in eps:
        a0, a1 = max(0, s0), min(48, s1)
        if a1 > a0:
            a.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#3f6fa6" fill-opacity=".85"/>' % (f(X(a0)), f(y + 1.2), f((a1 - a0) * px), f(RH - 2.4)))
    dd = ''
    t = 0.3
    while t < 48:
        if not any(s0 - .2 <= t < s1 + .2 for s0, s1 in eps):
            h = rnd.uniform(.2, 1.0) * (RH - 1.4)
            dd += 'M%s %sv-%s' % (f(X(t)), f(y + RH - .5), f(h))
        t += .6
    a.append('<path d="%s" stroke="%s" stroke-width="1" stroke-opacity=".85" fill="none"/>' % (dd, INK))
    if d % 3 == 0 or d == ND - 1:
        a.append(T(AX0 - 4, y + RH - 1, str(d + 1), 'ls', 'end', halo=False, style='font-size:9.5px'))
a.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width=".9"/>' % (AX0, AY0, f(48 * px), f(ND * RH), INK))
a.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width=".9"/>' % (f(X(24)), AY0, f(X(24)), f(AY0 + ND * RH), INK))
a.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#a8412c" stroke-width="1.4"/>' % (AX0 - 34, f(AY0 + NENT * RH), AX1, f(AY0 + NENT * RH)))
# guide lines along sleep onsets (both plotted nights)
for off in (0, 24):
    a.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#c9962e" stroke-width="2.2" stroke-dasharray="4 2.5"/>' % (
        f(X(11 + off)), f(AY0 - 1), f(X(11 + off)), f(AY0 + NENT * RH)))
    a.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#a8412c" stroke-width="2.2" stroke-dasharray="4 2.5"/>' % (
        f(X(11 + off + (TAU - 24))), f(AY0 + NENT * RH), f(X(11 + off + (ND - NENT + .5) * (TAU - 24))), f(AY0 + ND * RH + 1)))
# brackets with vertical text in the left margin
def bracket(y0, y1, txt, col):
    xb = 424
    g = '<path d="M%s %s h-4 V%s h4" fill="none" stroke="%s" stroke-width="1.1"/>' % (xb + 4, f(y0 + 1), f(y1 - 1), col)
    n = len(txt)
    ys = (y0 + y1) / 2 - (n - 1) * 7 + 4.5
    g += '<text x="%s" y="%s" class="lb halo" style="font-size:12.5px;fill:%s" text-anchor="middle">%s</text>' % (xb - 9, f(ys), col,
        ''.join('<tspan x="%s" dy="%s">%s</tspan>' % (xb - 9, 0 if i == 0 else 14, ch) for i, ch in enumerate(txt)))
    return g
a.append(bracket(AY0, AY0 + NENT * RH, '有日光', '#8a6a1a'))
a.append(bracket(AY0 + NENT * RH, AY0 + ND * RH, '沒有日光也沒有時鐘', '#a8412c'))
yb = AY0 + ND * RH
# annotation under the plot
a.append(lead([(600, yb + 22), (606, yb + 22), (X(11 + 24 + 19.5 * .2) - 2, yb - 3)], dot=True))
a.append(T(748, yb + 18, '入睡每天晚約 10–15 分鐘', 'lb', 'end', halo=True, style='font-size:12.5px;fill:#a8412c'))
a.append(T(748, yb + 33, '三週後晚了約 4 小時', 'ls', 'end', halo=True, style='font-weight:700'))
a.append(T(AX0, yb + 18, '金色虛線：有日光時，', 'ls', 'start', halo=True, style='font-weight:700;fill:#8a6a1a'))
a.append(T(AX0, yb + 33, '每晚同一時間入睡', 'ls', 'start', halo=True, style='font-weight:700;fill:#8a6a1a'))
ylg = yb + 50
a.append('<rect x="%s" y="%s" width="12" height="7" fill="#3f6fa6" fill-opacity=".85"/>' % (AX0, f(ylg - 7)))
a.append(T(AX0 + 16, ylg, '睡眠 sleep', 'ls', 'start', halo=False))
a.append('<path d="M%s %sv-7 m3 7v-5 m3 5v-8 m3 8v-4" stroke="%s" stroke-width="1"/>' % (f(AX0 + 90), f(ylg + .5), INK))
a.append(T(AX0 + 104, ylg, '清醒活動 activity', 'ls', 'start', halo=False))
a.append('<rect x="%s" y="%s" width="12" height="7" fill="#f7e7b0" stroke="%s" stroke-width=".4"/>' % (AX0 + 206, f(ylg - 7), INK))
a.append(T(AX0 + 222, ylg, '白天日光', 'ls', 'start', halo=False))
o.extend(a)

# =============================================================== message band
by = 410
o.append('<rect x="10" y="%s" width="740" height="52" rx="8" fill="#f6e7b0" stroke="#c9962e" stroke-width="1.4"/>' % by)
o.append('<rect x="14" y="%s" width="732" height="44" rx="6" fill="none" stroke="#c9962e" stroke-width=".6"/>' % (by + 4))
o.append(L.clock(44, by + 26, 15, 0, 12))
o.append(T(74, by + 24, '沒有陽光校正，生理時鐘一天大約 24 小時又十幾分鐘，會慢慢往後飄', 'lt', 'start', halo=False, style='font-size:17.5px'))
o.append(T(76, by + 42, "Without daylight to reset it, the human clock runs about 24.2 h a day and slowly drifts later (Czeisler et al., 1999).", 'le', 'start', halo=False, style='font-size:12px'))
o.append(T(380, H - 8, '示意圖：人物為示意，非肖像；右側活動紀錄依現代實驗室研究的典型結果重繪，並非 1938 年洞穴原始資料。', 'ls', 'middle', halo=False, style='font-size:10.5px;fill:#8a6a3a'))

caption = ('<b>圖 1·B　把人關進沒有時鐘的地方。</b>1938 年，睡眠研究先驅克萊特曼和學生理查森在肯塔基州猛瑪洞住了 32 天，'
           '想把一天拉長成 28 小時；床腳泡在水桶裡防老鼠。結果身體很難跟著改，尤其年紀較長的克萊特曼。'
           '後來在完全隔絕時間線索的實驗室裡看得更清楚：右圖每一列是一天，藍色是睡眠——有日光時每晚準時入睡（上段），'
           '看不到日光後，入睡時間每天往後挪一點，排成一條斜線（下段）。人物為示意，非肖像。')
write(PID, '圖 1·B', '把人關進沒有時鐘的地方', 'Living without clocks: the cave experiment and the free-running clock',
      H, '\n'.join(o), '左：1938 年猛瑪洞內兩位研究者，床腳泡在水桶裡，牆上寫著 28 小時作息；右：雙重繪圖活動紀錄，有日光時每天同時入睡，失去日光後入睡時間逐日往後移成斜線。',
      caption, ''.join(defs))
