import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from common import *

PID = 'pl-herbs'
G = '#b9cb8c'
BR = '#8a6a3a'
defs = '''<defs>
<radialGradient id="pl-herbs-seed" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#d98a6a"/><stop offset=".6" stop-color="#8e3a26"/><stop offset="1" stop-color="#5a2216"/></radialGradient>
<radialGradient id="pl-herbs-drupe" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#e8a07a"/><stop offset=".7" stop-color="#a8412c"/><stop offset="1" stop-color="#6a2618"/></radialGradient>
<radialGradient id="pl-herbs-gard" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#f7c27a"/><stop offset=".7" stop-color="#e0702c"/><stop offset="1" stop-color="#a8411c"/></radialGradient>
<radialGradient id="pl-herbs-rhiz" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#e2c27a"/><stop offset="1" stop-color="#9a7030"/></radialGradient>
<radialGradient id="pl-herbs-bone" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#f6f0e2"/><stop offset="1" stop-color="#c8bca2"/></radialGradient>
<radialGradient id="pl-herbs-yolk" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffe58a"/><stop offset=".7" stop-color="#f0a820"/><stop offset="1" stop-color="#c47a10"/></radialGradient>
<linearGradient id="pl-herbs-jiao" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a4422"/><stop offset=".5" stop-color="#3a2014"/><stop offset="1" stop-color="#22140c"/></linearGradient>
<linearGradient id="pl-herbs-amber" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8a858"/><stop offset="1" stop-color="#8a4a1a"/></linearGradient>
<linearGradient id="pl-herbs-pearl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbf8f2"/><stop offset=".6" stop-color="#e6e2ea"/><stop offset="1" stop-color="#c9c0d0"/></linearGradient>
</defs>'''

def stem(points, w=3, col=BR):
    d = smooth(points)
    return ('<path d="%s" stroke="#2a2018" stroke-width="%s" fill="none" stroke-linecap="round"/>'
            '<path d="%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>') % (d, f(w + 1.6), d, col, f(w))

def trinerved(x, y, ang, L, W, fill=G, crenate=10):
    """ovate leaf with 3 basal veins (Ziziphus)."""
    N = 40; out = []
    def wf(t): return (t ** 0.45) * ((1 - t) ** 0.9)
    mx = max(wf(i / N) for i in range(N + 1))
    up, dn = [], []
    for i in range(N + 1):
        t = i / N
        w = W / 2 * wf(t) / mx * (1 + (0.04 * math.sin(t * crenate * 2 * math.pi) if 0.1 < t < 0.95 else 0))
        up.append(rot(t * L, -w, x, y, ang)); dn.append(rot(t * L, w, x, y, ang))
    d = smooth(up + list(reversed(dn))[1:], close=True)
    out.append('<path d="%s" fill="%s" fill-opacity=".9"/>' % (d, fill))
    out.append('<path d="%s" fill="url(#ink-hatch-l)"/>' % smooth([rot(t / N * L, 0, x, y, ang) for t in range(N + 1)] + list(reversed(dn))[1:], close=True))
    out.append('<path d="%s" class="ink2" stroke-width=".7"/>' % pts([rot(0, 0, x, y, ang), rot(L * .95, 0, x, y, ang)]))
    for s in (-1, 1):
        P = [rot(L * k / 6 * 0.85, s * W / 2 * 0.62 * math.sin(math.pi * k / 6 * 0.95) ** 0.8, x, y, ang) for k in range(7)]
        out.append('<path d="%s" class="ink2" stroke-width=".5"/>' % smooth(P))
    out.append('<path d="%s" class="ink"/>' % d)
    return ''.join(out)

def cell_frame(x, y, w, h, n, zh, lat, part, partl):
    return ('<rect x="%d" y="%d" width="%d" height="%d" class="panel"/>' % (x, y, w, h) +
            '<text x="%d" y="%d" class="lt">%s　%s</text>' % (x + 8, y + 20, n, zh) +
            '<text x="%d" y="%d" class="le">%s</text>' % (x + 8, y + 35, lat) +
            '<text x="%d" y="%d" class="ls">藥用部位：<tspan style="font-weight:700">%s</tspan> <tspan class="le">%s</tspan></text>' % (x + 8, y + h - 8, part, partl))

body = [defs]
CW, CH = 246, 316
cells = [(6, 6), (257, 6), (508, 6), (6, 330), (257, 330), (508, 330)]

# ================= 1 酸棗 =================
x0, y0 = cells[0]
C = ['<g filter="url(#ink-rough)">']
nodes = [(26, 262), (62, 226), (96, 214), (118, 172), (156, 152), (172, 112), (206, 86)]
C.append(stem([(x0 + x, y0 + y) for x, y in nodes], 2.6, '#7a4a2a'))
for i, (x, y) in enumerate(nodes[1:-1], 1):
    X, Y = x0 + x, y0 + y
    sg = 1 if i % 2 else -1
    # paired stipular spines: one long straight, one short recurved
    C.append('<path d="M%s %s l%s %s" stroke="#4a2a18" stroke-width="1.4" stroke-linecap="round"/>' % (f(X), f(Y), f(sg * 9), f(-11)))
    C.append('<path d="M%s %s q%s 2 %s 6" stroke="#4a2a18" stroke-width="1.2" fill="none" stroke-linecap="round"/>' % (f(X), f(Y), f(-sg * 5), f(-sg * 6)))
for i, (x, y, a, L) in enumerate([(62, 226, 150, 44), (96, 214, 30, 46), (118, 172, 200, 42), (156, 152, 20, 44), (172, 112, 230, 38), (206, 86, -20, 34)]):
    C.append(trinerved(x0 + x, y0 + y, a, L, L * 0.55))
# flower clusters (small, 5-merous, yellow-green)
for (x, y) in [(100, 222), (122, 180), (160, 160)]:
    for k in range(3):
        fx, fy = x0 + x + k * 5 - 4, y0 + y + (k % 2) * 4
        petals = ''.join('<ellipse cx="%s" cy="%s" rx="1.5" ry="1" transform="rotate(%d %s %s)" fill="#e2e08a" stroke="#2a2018" stroke-width=".3"/>' % (
            f(fx + 2 * math.cos(a)), f(fy + 2 * math.sin(a)), math.degrees(a), f(fx + 2 * math.cos(a)), f(fy + 2 * math.sin(a))) for a in [j * 2 * math.pi / 5 for j in range(5)])
        C.append(petals + '<circle cx="%s" cy="%s" r=".9" fill="#c9962e"/>' % (f(fx), f(fy)))
# drupes
for (x, y) in [(70, 240), (180, 128)]:
    C.append('<path d="M%d %d v7" class="ink2"/><circle cx="%d" cy="%d" r="8.5" fill="url(#pl-herbs-drupe)" class="ink"/><ellipse cx="%d" cy="%d" rx="2.4" ry="1.6" fill="#fff" fill-opacity=".6"/>' % (
        x0 + x, y0 + y - 8, x0 + x, y0 + y + 7, x0 + x - 3, y0 + y + 4))
# seed detail (酸棗仁) enlarged
sx, sy = x0 + 190, y0 + 232
C.append('<ellipse cx="%d" cy="%d" rx="18" ry="24" fill="url(#pl-herbs-seed)" class="ink"/>' % (sx, sy))
C.append('<path d="M%d %d q2 22 0 44" class="ink2" stroke="#f0c0a0"/>' % (sx, sy - 22))
C.append('<path d="M%d %d q-2 -4 0 -6 q2 2 0 6" fill="#2a1a10"/>' % (sx, sy + 24))
C.append('<ellipse cx="%d" cy="%d" rx="4" ry="9" fill="#fff" fill-opacity=".35" transform="rotate(-15 %d %d)"/>' % (sx - 7, sy - 8, sx - 7, sy - 8))
# side view (flat lens)
C.append('<ellipse cx="%d" cy="%d" rx="5" ry="22" fill="url(#pl-herbs-seed)" class="ink"/>' % (sx + 34, sy))
C.append('</g>')
C.append(num(sx - 26, sy - 26, 'a'))
C.append(label(x0 + 150, y0 + 274, '酸棗仁 ×3', None, cls='ls halo') + label(x0 + 128, y0 + 288, '扁橢圓、紫紅有光澤', None, cls='ls halo'))
C.append(label(x0 + 168, y0 + 196, '正面', None, cls='ls halo') + label(x0 + 214, y0 + 196, '側面', None, cls='ls halo'))
C.append(label(x0 + 8, y0 + 64, '托葉刺（一直一彎）', None, cls='ls halo') + leader(x0 + 90, y0 + 70, x0 + 148, y0 + 142))
C.append(label(x0 + 8, y0 + 98, '三出基脈', None, cls='ls halo') + leader(x0 + 58, y0 + 100, x0 + 90, y0 + 166))
C.append(label(x0 + 8, y0 + 186, '核果', None, cls='ls halo') + label(x0 + 8, y0 + 200, 'drupe', None, cls='le halo') + leader(x0 + 34, y0 + 190, x0 + 64, y0 + 236))
C.append(scalebar(x0 + 10, y0 + 280, 20, 1))
C.append(cell_frame(x0, y0, CW, CH, '酸棗', '', 'Ziziphus jujuba var. spinosa', '種子', 'Ziziphi Spinosae Semen'))
body.append('\n'.join(C))

# ================= 2 黃連 =================
x0, y0 = cells[1]
C = ['<g filter="url(#ink-rough)">']
# fibrous roots
rnd = random.Random(3)
for k in range(22):
    bx = x0 + 70 + rnd.random() * 90; by = y0 + 262 + rnd.random() * 8
    C.append('<path d="M%s %s q%s %s %s %s" class="ink2" stroke-width=".45"/>' % (f(bx), f(by), f(rnd.uniform(-6, 6)), f(10), f(rnd.uniform(-10, 10)), f(18 + rnd.random() * 10)))
# clustered rhizomes ("chicken claw")
claws = [(-36, -8, -30), (-18, -24, -12), (0, -30, 4), (18, -22, 18), (34, -10, 34)]
bx, by = x0 + 112, y0 + 262
C.append('<path d="M%d %d q50 -18 96 0 q-8 10 -48 10 q-40 0 -48 -10z" fill="url(#pl-herbs-rhiz)" class="ink"/>' % (bx - 48, by))
for dx, dy, lean in claws:
    p0 = (bx + dx * 0.8, by - 2); p1 = (bx + dx + lean * 0.3, by + dy - 20)
    L_, R_ = [], []
    n = 6
    for i in range(n + 1):
        t = i / n
        cx_ = p0[0] + (p1[0] - p0[0]) * t; cy_ = p0[1] + (p1[1] - p0[1]) * t - math.sin(t * math.pi) * 3
        w = 6.5 - t * 1.6 + (0.8 if i % 2 else 0)
        L_.append((cx_ - w, cy_)); R_.append((cx_ + w, cy_))
    C.append('<path d="%s" fill="url(#pl-herbs-rhiz)" class="ink"/>' % smooth(L_ + list(reversed(R_)), close=True))
    for i in range(1, n):
        a, b = L_[i], R_[i]
        C.append('<path d="M%s %s Q%s %s %s %s" class="ink2" stroke-width=".5"/>' % (f(a[0]), f(a[1]), f((a[0] + b[0]) / 2), f(a[1] + 2.5), f(b[0]), f(b[1])))
    C.append('<path d="M%s %s l-3 -2 M%s %s l3 -1" class="ink2" stroke-width=".4"/>' % (f(L_[3][0]), f(L_[3][1]), f(R_[2][0]), f(R_[2][1])))
# petioles and ternate leaves with incised lobes
def lobed(x, y, ang, L, W):
    N = 60; up = []; dn = []
    for i in range(N + 1):
        t = i / N
        base = (t ** 0.5) * ((1 - t) ** 0.8)
        lobe = 1 + 0.28 * math.cos(t * 3 * 2 * math.pi) if t > 0.15 else 1
        tooth = 1 + (0.12 if i % 3 == 0 else 0)
        w = W / 2 * base / 0.38 * lobe * tooth
        up.append(rot(t * L, -w, x, y, ang)); dn.append(rot(t * L, w, x, y, ang))
    d = pts(up + list(reversed(dn))[1:], close=True)
    s = '<path d="%s" fill="#a9c07a" fill-opacity=".95" class="ink" stroke-linejoin="miter"/>' % d
    s += '<path d="%s" fill="url(#ink-hatch-l)"/>' % pts([rot(t / N * L, 0, x, y, ang) for t in range(N + 1)] + list(reversed(dn))[1:], close=True)
    s += '<path d="%s" class="ink2"/>' % pts([rot(0, 0, x, y, ang), rot(L * .9, 0, x, y, ang)])
    for k in range(1, 4):
        t = k / 3.6
        for sg in (-1, 1):
            s += '<path d="%s" class="ink2" stroke-width=".4"/>' % pts([rot(t * L * 0.8, 0, x, y, ang), rot(t * L + 6, sg * W * 0.32, x, y, ang)])
    return s
tops = [((x0 + 70, y0 + 92), [(x0 + 98, y0 + 238), (x0 + 84, y0 + 170)], 0),
        ((x0 + 170, y0 + 82), [(x0 + 120, y0 + 236), (x0 + 150, y0 + 160)], 1),
        ((x0 + 122, y0 + 128), [(x0 + 112, y0 + 238), (x0 + 118, y0 + 190)], 2)]
for (tx, ty), mids, k in tops:
    C.append(stem([mids[0], mids[1], (tx, ty)], 1.6, '#8a7a4a'))
for (tx, ty), mids, k in tops:
    base_ang = [-115, -60, -90][k]
    C.append(lobed(tx, ty, base_ang - 62, 34, 26))
    C.append(lobed(tx, ty, base_ang + 62, 34, 26))
    C.append(lobed(tx, ty, base_ang, 44, 30))
# rhizome cross-section detail
cx_, cy_ = x0 + 206, y0 + 196
C.append('<circle cx="%d" cy="%d" r="20" fill="#8a6a2a" class="ink"/>' % (cx_, cy_))
C.append('<circle cx="%d" cy="%d" r="16.5" fill="#f2c21e"/>' % (cx_, cy_))
for k in range(16):
    a = k * math.pi / 8
    C.append('<path d="M%s %s L%s %s" stroke="#c9871a" stroke-width="1.1"/>' % (f(cx_ + 4 * math.cos(a)), f(cy_ + 4 * math.sin(a)), f(cx_ + 15 * math.cos(a)), f(cy_ + 15 * math.sin(a))))
C.append('<circle cx="%d" cy="%d" r="4" fill="#e9a43a" stroke="#2a2018" stroke-width=".4"/>' % (cx_, cy_))
C.append('<circle cx="%d" cy="%d" r="11" fill="none" stroke="#a86a10" stroke-width=".6" stroke-dasharray="2 1.5"/>' % (cx_, cy_))
C.append('</g>')
C.append(num(cx_ - 24, cy_ - 24, 'a'))
C.append(label(x0 + 180, y0 + 232, '斷面鮮黃', None, cls='ls halo') + label(x0 + 180, y0 + 246, '放射紋 ×2', None, cls='ls halo'))
C.append(label(x0 + 8, y0 + 236, '根莖簇生', None, cls='ls halo') + label(x0 + 8, y0 + 250, '如雞爪', None, cls='ls halo') + leader(x0 + 52, y0 + 244, x0 + 82, y0 + 246))
C.append(label(x0 + 8, y0 + 290, '鬚根', None, cls='ls halo') + leader(x0 + 32, y0 + 286, x0 + 74, y0 + 278))
C.append(label(x0 + 190, y0 + 126, '三全裂', None, cls='ls halo') + label(x0 + 190, y0 + 140, '羽狀深裂', None, cls='ls halo') + leader(x0 + 206, y0 + 114, x0 + 198, y0 + 88))
C.append(scalebar(x0 + 150, y0 + 284, 20, 1))
C.append(cell_frame(x0, y0, CW, CH, '黃連', '', 'Coptis chinensis Franch.', '根莖', 'Coptidis Rhizoma'))
body.append('\n'.join(C))

# ================= 3 梔子 =================
x0, y0 = cells[2]
C = ['<g filter="url(#ink-rough)">']
main = [(x0 + 40, y0 + 296), (x0 + 60, y0 + 240), (x0 + 88, y0 + 180), (x0 + 116, y0 + 120), (x0 + 140, y0 + 84)]
C.append(stem(main, 2.6, '#6a5a3a'))
C.append(stem([(x0 + 62, y0 + 236), (x0 + 120, y0 + 220), (x0 + 168, y0 + 196)], 2, '#6a5a3a'))
# opposite leaf pairs
for (x, y, a) in [(60, 240, -10), (88, 180, -40), (116, 120, -60)]:
    C.append(leaf(x0 + x, y0 + y, a + 70, 50, 22, p=0.6, q=0.9, fill='#8fae6a', veins=8, vein_ang=60, marginal=False))
    C.append(leaf(x0 + x, y0 + y, a - 110 + 180 + 180, 50, 22, p=0.6, q=0.9, fill='#8fae6a', veins=8, vein_ang=60, marginal=False))
C.append(leaf(x0 + 120, y0 + 220, 100, 44, 20, p=0.6, q=0.9, fill='#8fae6a', veins=7, vein_ang=60, marginal=False))
# white flower (6 spirally overlapping obovate lobes) at top
fx, fy = x0 + 150, y0 + 70
for k in range(6):
    a = k * 60 + 10
    pp = [rot(u, v, fx, fy, a) for u, v in [(2, 0), (8, -7), (20, -9), (26, -2), (22, 6), (8, 5)]]
    C.append('<path d="%s" fill="#fbf8ef" class="ink"/>' % smooth(pp, close=True))
    C.append('<path d="%s" class="ink2" stroke-width=".4"/>' % smooth([rot(4, 0, fx, fy, a), rot(16, -2, fx, fy, a), rot(22, 0, fx, fy, a)]))
C.append('<circle cx="%d" cy="%d" r="4" fill="#f0d070" class="ink"/>' % (fx, fy))
C.append('<path d="M%d %d l-6 18" stroke="#9fb46e" stroke-width="5"/><path d="M%d %d l-6 18" class="ink2"/>' % (fx - 4, fy + 8, fx - 4, fy + 8))
# fruit with ribs + persistent calyx lobes
gx, gy = x0 + 178, y0 + 206
fr = smooth([(gx, gy - 26), (gx + 12, gy - 18), (gx + 15, gy + 2), (gx + 10, gy + 20), (gx, gy + 26), (gx - 10, gy + 20), (gx - 15, gy + 2), (gx - 12, gy - 18)], close=True)
C.append('<path d="%s" fill="url(#pl-herbs-gard)" class="ink"/>' % fr)
for k in (-8, -3, 3, 8):
    C.append('<path d="M%d %d q%d 22 %d 50" class="ink2" stroke="#7a2a10"/>' % (gx + k * 0.6, gy - 24, k * 1.4, k * 0.2))
for k in range(6):
    a = -90 + (k - 2.5) * 16
    C.append('<path d="M%s %s q%s %s %s %s" stroke="#5a7a3a" stroke-width="1.6" fill="none"/>' % (f(gx), f(gy - 25), f(math.cos(math.radians(a)) * 8), f(math.sin(math.radians(a)) * 10), f(math.cos(math.radians(a)) * 12 + (k - 2.5) * 2), f(-20)))
C.append('<ellipse cx="%d" cy="%d" rx="3" ry="6" fill="#fff" fill-opacity=".4"/>' % (gx - 6, gy - 4))
# cross-section detail
cx_, cy_ = x0 + 200, y0 + 268
C.append('<circle cx="%d" cy="%d" r="17" fill="#e0702c" class="ink"/><circle cx="%d" cy="%d" r="13" fill="#f6a24a"/>' % (cx_, cy_, cx_, cy_))
rs = random.Random(2)
for k in range(26):
    a = rs.random() * 2 * math.pi; r = rs.random() * 10
    C.append('<ellipse cx="%s" cy="%s" rx="1.8" ry="1.2" fill="#8a2a10" transform="rotate(%d %s %s)"/>' % (f(cx_ + r * math.cos(a)), f(cy_ + r * math.sin(a)), rs.randint(0, 180), f(cx_ + r * math.cos(a)), f(cy_ + r * math.sin(a))))
for k in range(3):
    a = k * 2 * math.pi / 3
    C.append('<path d="M%d %d L%s %s" stroke="#c45a20" stroke-width=".8"/>' % (cx_, cy_, f(cx_ + 13 * math.cos(a)), f(cy_ + 13 * math.sin(a))))
C.append('</g>')
C.append(num(cx_ + 2, cy_ - 26, 'a'))
C.append(label(x0 + 134, y0 + 262, '果實橫切', None, cls='ls halo') + label(x0 + 134, y0 + 276, '種子多數', None, cls='ls halo'))
C.append(label(x0 + 186, y0 + 112, '花白色', None, cls='ls halo') + label(x0 + 186, y0 + 126, '六裂、芳香', None, cls='ls halo') + leader(x0 + 184, y0 + 108, x0 + 166, y0 + 84))
C.append(label(x0 + 176, y0 + 152, '宿存萼片', None, cls='ls halo') + leader(x0 + 196, y0 + 156, x0 + 180, y0 + 184))
C.append(label(x0 + 8, y0 + 260, '果實具縱稜', None, cls='ls halo') + label(x0 + 8, y0 + 274, '橙紅色', None, cls='ls halo') + leader(x0 + 72, y0 + 256, gx - 14, gy + 4))
C.append(scalebar(x0 + 92, y0 + 290, 20, 1))
C.append(cell_frame(x0, y0, CW, CH, '梔子', '', 'Gardenia jasminoides J.Ellis', '果實', 'Gardeniae Fructus'))
body.append('\n'.join(C))

# ================= 4 柴胡 =================
x0, y0 = cells[3]
C = ['<g filter="url(#ink-rough)">']
# taproot
root = [(x0 + 104, y0 + 236), (x0 + 112, y0 + 236), (x0 + 114, y0 + 252), (x0 + 112, y0 + 272), (x0 + 106, y0 + 294), (x0 + 102, y0 + 272), (x0 + 101, y0 + 252)]
C.append('<path d="%s" fill="#9a6a3a" class="ink"/>' % smooth(root, close=True))
C.append('<path d="%s" fill="url(#ink-hatch)"/>' % smooth(root[3:] + [root[0]], close=True))
for (a, b, c, d) in [(112, 258, 128, 278), (103, 264, 86, 284), (110, 276, 118, 296)]:
    C.append('<path d="M%d %d Q%d %d %d %d" stroke="#2a2018" stroke-width="1.3" fill="none"/>' % (x0 + a, y0 + b, x0 + (a + c) / 2, y0 + d - 6, x0 + c, y0 + d))
for k in range(5):
    C.append('<path d="M%d %d q5 1 9 0" class="ink2" stroke-width=".5"/>' % (x0 + 103, y0 + 244 + k * 8))
# stems
st = [(x0 + 108, y0 + 236), (x0 + 110, y0 + 180), (x0 + 106, y0 + 130), (x0 + 112, y0 + 90)]
C.append(stem(st, 2.2, '#7a9a4a'))
C.append(stem([(x0 + 108, y0 + 150), (x0 + 80, y0 + 110), (x0 + 60, y0 + 78)], 1.6, '#7a9a4a'))
C.append(stem([(x0 + 110, y0 + 130), (x0 + 140, y0 + 100), (x0 + 168, y0 + 74)], 1.6, '#7a9a4a'))
C.append(stem([(x0 + 112, y0 + 90), (x0 + 112, y0 + 70)], 1.4, '#7a9a4a'))
# linear-lanceolate leaves with parallel veins
def linleaf(x, y, ang, L, W):
    up, dn = [], []
    for i in range(31):
        t = i / 30
        w = W / 2 * math.sin(math.pi * min(t * 1.15, 1)) ** 0.7 * (1 - t) ** 0.3
        up.append(rot(t * L, -w, x, y, ang)); dn.append(rot(t * L, w, x, y, ang))
    d = smooth(up + list(reversed(dn))[1:], close=True)
    s = '<path d="%s" fill="#a9c07a"/>' % d
    for k in (-0.6, -0.3, 0, 0.3, 0.6):
        s += '<path d="%s" class="ink2" stroke-width=".35"/>' % smooth([rot(t / 10 * L, k * W / 2 * math.sin(math.pi * min(t / 10 * 1.15, 1)) ** 0.7 * (1 - t / 10) ** 0.3, x, y, ang) for t in range(1, 10)])
    return s + '<path d="%s" class="ink"/>' % d
for (x, y, a, L) in [(109, 200, -150, 70), (110, 190, -30, 66), (108, 160, -160, 58), (110, 150, -20, 60), (108, 118, 200, 44), (111, 112, -10, 46)]:
    C.append(linleaf(x0 + x, y0 + y, a, L, 8))
# compound umbels
def umbel(cx, cy, n=6, r=18):
    s = ''
    for k in range(n):
        a = math.radians(-90 + (k - (n - 1) / 2) * 22)
        ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        s += '<path d="M%s %s L%s %s" class="ink2" stroke-width=".55"/>' % (f(cx), f(cy), f(ex), f(ey))
        for j in range(6):
            b = math.radians(-90 + (j - 2.5) * 26)
            fx, fy = ex + 5 * math.cos(b), ey + 5 * math.sin(b)
            s += '<path d="M%s %s L%s %s" class="ink2" stroke-width=".35"/><circle cx="%s" cy="%s" r="1.5" fill="#e8c83a" stroke="#2a2018" stroke-width=".3"/>' % (f(ex), f(ey), f(fx), f(fy), f(fx), f(fy))
    # bracts
    s += '<path d="M%s %s l-5 -4 M%s %s l5 -4" class="ink2"/>' % (f(cx), f(cy), f(cx), f(cy))
    return s
C.append(umbel(x0 + 60, y0 + 78)); C.append(umbel(x0 + 168, y0 + 74)); C.append(umbel(x0 + 112, y0 + 70, 7, 20))
# single flower detail
dx, dy = x0 + 206, y0 + 150
for k in range(5):
    a = k * 72
    C.append('<path d="%s" fill="#f0d04a" class="ink2"/>' % smooth([rot(u, v, dx, dy, a) for u, v in [(0, 0), (6, -4), (11, -1), (9, 2), (6, 1)]], close=True))
C.append('<circle cx="%d" cy="%d" r="3" fill="#c9962e" class="ink2"/>' % (dx, dy))
C.append('</g>')
C.append(num(dx - 20, dy - 18, 'a'))
C.append(label(x0 + 184, y0 + 180, '小花 ×6', None, cls='ls halo') + label(x0 + 184, y0 + 194, '黃色 5 瓣', None, cls='ls halo'))
C.append(label(x0 + 8, y0 + 120, '複繖形花序', None, cls='ls halo') + leader(x0 + 30, y0 + 108, x0 + 52, y0 + 72))
C.append(label(x0 + 8, y0 + 222, '葉線狀披針形', None, cls='ls halo') + label(x0 + 8, y0 + 236, '平行脈', None, cls='ls halo') + leader(x0 + 50, y0 + 226, x0 + 60, y0 + 175))
C.append(label(x0 + 150, y0 + 266, '主根', None, cls='ls halo') + label(x0 + 150, y0 + 280, '質硬、褐色', None, cls='ls halo') + leader(x0 + 148, y0 + 262, x0 + 114, y0 + 262))
C.append(scalebar(x0 + 10, y0 + 284, 20, 1))
C.append(cell_frame(x0, y0, CW, CH, '柴胡', '', 'Bupleurum chinense DC.', '根', 'Bupleuri Radix'))
body.append('\n'.join(C))

# ================= 5 龍骨 & 牡蠣 =================
x0, y0 = cells[4]
C = ['<g filter="url(#ink-rough)">']
# fossil bone shaft fragment, oblique
bone = smooth([(x0 + 30, y0 + 72), (x0 + 120, y0 + 56), (x0 + 168, y0 + 54), (x0 + 172, y0 + 66), (x0 + 176, y0 + 92), (x0 + 168, y0 + 100), (x0 + 120, y0 + 104), (x0 + 36, y0 + 118), (x0 + 28, y0 + 100)], close=True)
C.append('<path d="%s" fill="url(#pl-herbs-bone)"/>' % bone)
C.append('<path d="M%d %d L%d %d L%d %d L%d %d z" fill="url(#ink-hatch-l)"/>' % (x0 + 36, y0 + 100, x0 + 166, y0 + 86, x0 + 168, y0 + 100, x0 + 36, y0 + 118))
for k in range(9):
    xx = x0 + 50 + k * 13
    C.append('<path d="M%d %d l%d %d l3 6" class="ink2" stroke-width=".45"/>' % (xx, y0 + 66 + k % 3 * 6, 4, 10))
rr = random.Random(4)
for k in range(10):
    xx = x0 + 50 + rr.random() * 110; yy = y0 + 70 + rr.random() * 28
    C.append('<path d="M%s %s l2 -3 l2 2 l2 -4" stroke="#5a4a3a" stroke-width=".5" fill="none"/>' % (f(xx), f(yy)))
C.append('<path d="%s" class="ink3" stroke-width="1.4"/>' % bone)
# broken end cross-section (left end): compact ring + cancellous
ex, ey = x0 + 32, y0 + 95
C.append('<ellipse cx="%d" cy="%d" rx="11" ry="23" fill="#e9dfc6" class="ink"/>' % (ex, ey))
C.append('<ellipse cx="%d" cy="%d" rx="6" ry="15" fill="#d6c8a6" stroke="#2a2018" stroke-width=".5"/>' % (ex, ey))
C.append('<ellipse cx="%d" cy="%d" rx="6" ry="15" fill="url(#ink-stipple-d)"/>' % (ex, ey))
# sponge pattern
for k in range(12):
    C.append('<circle cx="%s" cy="%s" r="1.3" fill="none" stroke="#2a2018" stroke-width=".35"/>' % (f(ex + rr.uniform(-4, 4)), f(ey + rr.uniform(-12, 12))))
# oyster shells: outer (layered) + inner (pearly with muscle scar)
ox, oy = x0 + 70, y0 + 200
outer = [(ox - 28, oy - 52), (ox - 6, oy - 58), (ox + 18, oy - 40), (ox + 30, oy - 6), (ox + 30, oy + 30), (ox + 20, oy + 56), (ox - 6, oy + 62), (ox - 28, oy + 44), (ox - 34, oy + 6), (ox - 34, oy - 30)]
C.append('<path d="%s" fill="#b8b0b8" class="ink"/>' % smooth(outer, close=True))
umbo = (ox - 18, oy - 50)
for k in range(1, 8):
    s_ = 1 - k * 0.12
    P = [(umbo[0] + (x - umbo[0]) * s_ + rr.uniform(-1.5, 1.5), umbo[1] + (y - umbo[1]) * s_ + rr.uniform(-1.5, 1.5)) for x, y in outer]
    C.append('<path d="%s" fill="%s" stroke="#2a2018" stroke-width=".5"/>' % (smooth(P, close=True), ['#c9c0c6', '#a89aa6', '#d6ced2', '#9a8a98', '#cfc6cc', '#b0a2ae', '#ddd6da'][k - 1]))
    # frilly edge marks
    for (x, y) in P[3:7]:
        C.append('<path d="M%s %s l2 3" class="ink2" stroke-width=".35"/>' % (f(x), f(y)))
ix, iy = x0 + 170, y0 + 200
inner = [(ix - 26, iy - 50), (ix - 2, iy - 54), (ix + 22, iy - 34), (ix + 30, iy + 2), (ix + 28, iy + 34), (ix + 14, iy + 56), (ix - 10, iy + 58), (ix - 30, iy + 38), (ix - 34, iy + 0), (ix - 32, iy - 32)]
C.append('<path d="%s" fill="#a89aa6" class="ink"/>' % smooth(inner, close=True))
C.append('<path d="%s" fill="url(#pl-herbs-pearl)" stroke="#2a2018" stroke-width=".6"/>' % smooth([(x + (ix - x) * 0.12, y + (iy - y) * 0.12) for x, y in inner], close=True))
C.append('<ellipse cx="%d" cy="%d" rx="9" ry="7" fill="#7a5a8a" fill-opacity=".75" stroke="#2a2018" stroke-width=".5"/>' % (ix + 6, iy + 12))
C.append('<path d="M%d %d q4 -6 10 -4" class="ink2"/>' % (ix - 22, iy - 44))
C.append('</g>')
C.append(label(x0 + 70, y0 + 140, '龍骨', None) + label(x0 + 104, y0 + 140, 'Os Draconis', None, cls='le halo'))
C.append(label(x0 + 70, y0 + 154, '古代哺乳類骨骼化石', None, cls='ls halo'))
C.append(label(x0 + 132, y0 + 50, '斷端：緻密骨＋海綿骨', None, cls='ls halo') + leader(x0 + 130, y0 + 46, x0 + 38, y0 + 84))
C.append(label(x0 + 8, y0 + 276, '牡蠣', None) + label(x0 + 42, y0 + 276, 'Ostrea gigas', None, cls='le halo'))
C.append(label(x0 + 8, y0 + 290, '外面：層層疊疊的鱗片', None, cls='ls halo'))
C.append(label(x0 + 140, y0 + 276, '內面珍珠光澤', None, cls='ls halo') + label(x0 + 140, y0 + 290, '紫色＝閉殼肌痕', None, cls='ls halo') + leader(x0 + 190, y0 + 280, ix + 8, iy + 18))
C.append('<rect x="%d" y="%d" width="%d" height="%d" class="panel"/>' % (x0, y0, CW, CH))
C.append('<text x="%d" y="%d" class="lt">龍骨・牡蠣</text>' % (x0 + 8, y0 + 20))
C.append('<text x="%d" y="%d" class="le">Fossil bone &amp; oyster shell</text>' % (x0 + 8, y0 + 35))
C.append('<text x="%d" y="%d" class="ls">藥用部位：<tspan style="font-weight:700">化石・貝殼</tspan>（重鎮安神）</text>' % (x0 + 8, y0 + CH - 8))
body.append('\n'.join(C))

# ================= 6 阿膠 + 雞子黃 =================
x0, y0 = cells[5]
C = ['<g filter="url(#ink-rough)">']
# gelatin block (isometric slab)
bx, by = x0 + 30, y0 + 80
top = [(bx, by), (bx + 70, by - 18), (bx + 112, by), (bx + 42, by + 18)]
front = [(bx, by), (bx + 42, by + 18), (bx + 42, by + 32), (bx, by + 14)]
side = [(bx + 42, by + 18), (bx + 112, by), (bx + 112, by + 14), (bx + 42, by + 32)]
C.append('<path d="%s" fill="url(#pl-herbs-jiao)" class="ink"/>' % pts(top, True))
C.append('<path d="%s" fill="#2a160c" class="ink"/>' % pts(front, True))
C.append('<path d="%s" fill="#3a2014" class="ink"/>' % pts(side, True))
C.append('<path d="M%d %d l46 -12" stroke="#fff" stroke-opacity=".45" stroke-width="3" stroke-linecap="round"/>' % (bx + 20, by - 2))
# second piece held to light (translucent amber), broken edge
px, py = x0 + 150, y0 + 70
C.append('<path d="M%d %d l56 -10 l6 30 l-8 4 l4 6 l-50 10z" fill="url(#pl-herbs-amber)" fill-opacity=".85" class="ink"/>' % (px, py))
C.append('<path d="M%d %d l46 -8" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>' % (px + 4, py + 6))
C.append('<circle cx="%d" cy="%d" r="11" fill="#f6e7b0" stroke="#c9962e" stroke-width=".8"/>' % (px + 70, py - 26))
for k in range(8):
    a = k * math.pi / 4
    C.append('<path d="M%s %s l%s %s" stroke="#c9962e" stroke-width=".8"/>' % (f(px + 70 + 13 * math.cos(a)), f(py - 26 + 13 * math.sin(a)), f(4 * math.cos(a)), f(4 * math.sin(a))))
# dish with egg yolk + cracked shell
dx, dy = x0 + 80, y0 + 196
C.append('<ellipse cx="%d" cy="%d" rx="52" ry="14" fill="#efe6d2" class="ink"/>' % (dx, dy))
C.append('<path d="M%d %d q52 40 104 0" fill="#e2d6bc" class="ink"/>' % (dx - 52, dy))
C.append('<path d="M%d %d q52 30 104 0" fill="url(#ink-hatch-l)"/>' % (dx - 52, dy))
C.append('<ellipse cx="%d" cy="%d" rx="34" ry="8" fill="#fbf8ef" fill-opacity=".85" stroke="#2a2018" stroke-width=".4"/>' % (dx, dy))
C.append('<ellipse cx="%d" cy="%d" rx="14" ry="10" fill="url(#pl-herbs-yolk)" class="ink"/>' % (dx, dy - 3))
C.append('<ellipse cx="%d" cy="%d" rx="4" ry="2.4" fill="#fff" fill-opacity=".7"/>' % (dx - 5, dy - 7))
ex, ey = x0 + 180, y0 + 186
C.append('<path d="M%d %d q2 -26 20 -28 q18 2 20 28 l-5 -5 -5 6 -5 -7 -5 6 -5 -6 -5 6 -5 -5z" fill="#f3e7d2" class="ink"/>' % (ex - 20, ey))
C.append('<path d="M%d %d q2 18 20 20 q18 -2 20 -20 l-5 4 -5 -5 -5 6 -5 -5 -5 5 -5 -6 -5 5z" fill="#efe0c6" class="ink"/>' % (ex - 18, ey + 14))
C.append('</g>')
C.append(label(x0 + 8, y0 + 128, '阿膠', None) + label(x0 + 42, y0 + 128, 'Asini Corii Colla', None, cls='le halo'))
C.append(label(x0 + 8, y0 + 142, '驢皮熬製的膠塊；黑褐有光澤', None, cls='ls halo'))
C.append(label(x0 + 8, y0 + 156, '對光照視呈棕色半透明', None, cls='ls halo') + leader((x0 + 124, y0 + 152), (x0 + 200, y0 + 152), (x0 + 186, y0 + 92)))
C.append(label(x0 + 8, y0 + 238, '雞子黃', None) + label(x0 + 56, y0 + 238, 'egg yolk', None, cls='le halo'))
C.append(label(x0 + 8, y0 + 252, '湯稍冷後才加入攪勻', None, cls='ls halo'))
C.append(label(x0 + 8, y0 + 268, '「內膠烊盡，小冷，內雞子黃，攪令相得」', None, cls='ls halo'))
C.append(label(x0 + 8, y0 + 284, '黃連阿膠湯：黃連、黃芩、芍藥、阿膠、雞子黃', None, cls='ls halo'))
C.append('<rect x="%d" y="%d" width="%d" height="%d" class="panel"/>' % (x0, y0, CW, CH))
C.append('<text x="%d" y="%d" class="lt">阿膠・雞子黃</text>' % (x0 + 8, y0 + 20))
C.append('<text x="%d" y="%d" class="le">Donkey-hide gelatin &amp; egg yolk</text>' % (x0 + 8, y0 + 35))
C.append('<text x="%d" y="%d" class="ls">用於：<tspan style="font-weight:700">黃連阿膠湯</tspan>（少陰病，心中煩，不得臥）</text>' % (x0 + 8, y0 + CH - 8))
body.append('\n'.join(C))

cap = ('<b>圖 10-A　經方安神藥材圖譜。</b>依植物誌與《中國藥典》藥材性狀重繪，比例尺為約略值。酸棗仁湯用的是<b>酸棗的種子</b>（扁平、紫紅、有光澤），不是果肉；黃連的根莖簇生如雞爪、斷面鮮黃；梔子的果實帶縱稜與宿萼；柴胡用根。'
       '龍骨、牡蠣是礦物與貝殼類的「重鎮」藥，出現在柴胡加龍骨牡蠣湯與桂枝加龍骨牡蠣湯；阿膠與雞子黃是黃連阿膠湯的兩味血肉有情之品，雞子黃要等湯稍冷才下。')
open('/home/user/Insomnia/figs/pl-herbs.html', 'w').write(figure(PID, 'Plate 10·A', '經方裡的安神藥材長什麼樣', 'Materia medica of the classical sleep formulas', 652,
                                                        '六格藥材圖譜：酸棗與酸棗仁、黃連根莖、梔子花果、柴胡、龍骨與牡蠣、阿膠與雞子黃', '\n'.join(body), cap))
