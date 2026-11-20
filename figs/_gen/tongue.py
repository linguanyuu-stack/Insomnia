import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from common import *

PID = 'pl-tongue'
UID = [0]

def uid():
    UID[0] += 1
    return 'pl-tongue-%d' % UID[0]

BODY = {'pale': ('#f6d4cc', '#e4a49a'), 'normal': ('#f2aaa0', '#d8766c'), 'red': ('#ee8676', '#c53c32'),
        'deep': ('#e0605a', '#a8261f'), 'dark': ('#b07a92', '#6e3a58')}

def tongue(cx, top, W, H, body='normal', fat=0.0, teeth=0, coat=None, red_tip=False, cracks=0, ecchy=0,
           less_coat=False, seed=1, lips=True, sulcus=True, skin=False, lipf=1.0):
    """Front view of a protruded tongue framed by lips. (cx, top) = centre of mouth line."""
    rnd = random.Random(seed)
    g = []
    W = W * (1 + fat)
    def hw(t):
        base = W / 2 * (1 - t ** 3.2) ** 0.5 * (0.9 + 0.12 * math.sin(math.pi * min(t * 1.2, 1)))
        if teeth and 0.18 < t < 0.88:
            base -= teeth * abs(math.sin(t * 22)) ** 0.6
        return base
    N = 60
    left = [(cx - hw(i / N), top + i / N * H) for i in range(N + 1)]
    right = [(cx + hw(i / N), top + i / N * H) for i in range(N + 1)]
    shape = smooth(left + list(reversed(right))[1:], close=True, t=0.4)
    c1, c2 = BODY[body]
    gid = uid(); clip = uid()
    g.append('<defs><radialGradient id="%s" cx=".5" cy=".55" r=".65"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
             '<clipPath id="%s"><path d="%s"/></clipPath></defs>' % (gid, c1, c2, clip, shape))
    Wl = W * lipf
    if lips:
        # skin around mouth
        if skin:
            g.append('<path d="%s" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width=".8"/>' % smooth(
                [(cx - Wl * 1.05, top - 34), (cx, top - 46), (cx + Wl * 1.05, top - 34), (cx + Wl * 1.0, top + H * 0.55), (cx + Wl * 0.7, top + H * 0.95), (cx, top + H * 1.12),
                 (cx - Wl * 0.7, top + H * 0.95), (cx - Wl * 1.0, top + H * 0.55)], close=True))
        # mouth cavity
        g.append('<path d="%s" fill="#4a1a1a" stroke="#2a2018" stroke-width=".8"/>' % smooth(
            [(cx - Wl * 0.78, top - 2), (cx, top - 14), (cx + Wl * 0.78, top - 2), (cx + Wl * 0.6, top + H * 0.32), (cx, top + H * 0.44), (cx - Wl * 0.6, top + H * 0.32)], close=True))
        # lower lip (behind tongue)
        g.append('<path d="%s" fill="#c87a70" stroke="#2a2018" stroke-width=".9"/>' % smooth(
            [(cx - Wl * 0.8, top + 0), (cx - Wl * 0.62, top + H * 0.36), (cx, top + H * 0.5), (cx + Wl * 0.62, top + H * 0.36), (cx + Wl * 0.8, top),
             (cx + Wl * 0.7, top + H * 0.46), (cx, top + H * 0.64), (cx - Wl * 0.7, top + H * 0.46)], close=True))
        # lower teeth
        g.append('<path d="M%s %s Q%s %s %s %s" stroke="#f4efe2" stroke-width="3" fill="none"/>' % (
            f(cx - Wl * 0.6), f(top + H * 0.3), f(cx), f(top + H * 0.46), f(cx + Wl * 0.6), f(top + H * 0.3)))
    # tongue body
    g.append('<path d="%s" fill="url(#%s)"/>' % (shape, gid))
    # filiform texture
    pap = []
    for k in range(int(W * H / 22)):
        t = rnd.random() ** 0.9; s_ = rnd.uniform(-1, 1)
        x = cx + s_ * hw(t) * 0.95; y = top + t * H
        pap.append('<circle cx="%s" cy="%s" r=".45"/>' % (f(x), f(y)))
    g.append('<g fill="#fff" fill-opacity=".45" clip-path="url(#%s)">%s</g>' % (clip, ''.join(pap)))
    # fungiform papillae: red dots, denser at tip & edges
    fp = []
    nred = int(W * H / (60 if not red_tip else 40))
    for k in range(nred):
        t = rnd.random() ** 0.6; s_ = rnd.uniform(-1, 1) * (0.6 + 0.4 * rnd.random())
        x = cx + s_ * hw(t) * 0.92; y = top + t * H
        fp.append('<circle cx="%s" cy="%s" r="%s"/>' % (f(x), f(y), f(0.7 + rnd.random() * 0.5)))
    g.append('<g fill="%s" fill-opacity=".7" clip-path="url(#%s)">%s</g>' % ('#b02a22' if body in ('red', 'deep') else '#c0544a', clip, ''.join(fp)))
    # coat
    if coat:
        col, op, t1, wf, thick = coat
        cpts = []
        for i in range(31):
            t = i / 30 * t1
            j = rnd.uniform(-1, 1) * (3 if thick else 1.5)
            cpts.append((t, hw(t) * wf + j))
        L = [(cx - w, top + t * H) for t, w in cpts]
        R = [(cx + w, top + t * H) for t, w in reversed(cpts)]
        # round the front of the coat
        tip_y = top + t1 * H
        cs = smooth(L + [(cx, tip_y + H * 0.06)] + R, close=True)
        cid = uid()
        g.append('<defs><radialGradient id="%s" cx=".5" cy=".2" r=".9"><stop offset="0" stop-color="%s" stop-opacity="%s"/><stop offset="1" stop-color="%s" stop-opacity="%s"/></radialGradient></defs>' % (
            cid, col, op, col, op * 0.35))
        g.append('<path d="%s" fill="url(#%s)" clip-path="url(#%s)"/>' % (cs, cid, clip))
        if thick:
            g.append('<path d="%s" fill="url(#ink-stipple-l)" opacity=".7" clip-path="url(#%s)"/>' % (cs, clip))
            for k in range(14):
                t = rnd.random() * t1 * 0.9; s_ = rnd.uniform(-1, 1) * wf * 0.8
                g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" fill-opacity=".45"/>' % (f(cx + s_ * hw(t)), f(top + t * H), f(2 + rnd.random() * 3), f(1.5 + rnd.random() * 2), col))
    # red tip with prickles
    if red_tip:
        rid = uid()
        g.append('<defs><radialGradient id="%s" cx=".5" cy="1" r=".6"><stop offset="0" stop-color="#c41e1a" stop-opacity=".95"/><stop offset="1" stop-color="#c41e1a" stop-opacity="0"/></radialGradient></defs>' % rid)
        g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)" clip-path="url(#%s)"/>' % (f(cx - W / 2), f(top + H * 0.55), f(W), f(H * 0.46), rid, clip))
        for k in range(26):
            t = 0.78 + rnd.random() * 0.2; s_ = rnd.uniform(-0.9, 0.9)
            g.append('<circle cx="%s" cy="%s" r="1.1" fill="#8a0e0a" clip-path="url(#%s)"/>' % (f(cx + s_ * hw(t)), f(top + t * H), clip))
    # median sulcus
    if sulcus:
        g.append('<path d="M%s %s Q%s %s %s %s" stroke="#7a2a24" stroke-opacity=".55" stroke-width="1.1" fill="none"/>' % (
            f(cx), f(top + H * 0.06), f(cx + 1), f(top + H * 0.4), f(cx), f(top + H * 0.68)))
    # cracks
    for k in range(cracks):
        x = cx + rnd.uniform(-0.45, 0.45) * W / 2; y = top + H * rnd.uniform(0.2, 0.75)
        d = 'M%s %s' % (f(x), f(y))
        for j in range(4):
            x += rnd.uniform(-6, 6); y += rnd.uniform(3, 7)
            d += ' L%s %s' % (f(x), f(y))
        g.append('<path d="%s" stroke="#6a1610" stroke-width="1.3" fill="none" stroke-linecap="round"/>' % d)
        g.append('<path d="%s" stroke="#f0a090" stroke-width=".4" fill="none" transform="translate(.8 .4)"/>' % d)
    # central longitudinal crack for cracks
    if cracks:
        g.append('<path d="M%s %s l-1 10 l2 10 l-2 12 l1 10" stroke="#6a1610" stroke-width="1.6" fill="none"/>' % (f(cx), f(top + H * 0.15)))
    # ecchymoses (瘀點/瘀斑)
    for k in range(ecchy):
        side = 1 if k % 2 else -1
        t = rnd.uniform(0.3, 0.88)
        x = cx + side * hw(t) * rnd.uniform(0.6, 0.85); y = top + t * H
        g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#3e1a3a" fill-opacity=".8"/>' % (f(x), f(y), f(1.4 + rnd.random() * 2.2), f(1.2 + rnd.random() * 1.6)))
    # shading on one side
    g.append('<path d="%s" fill="url(#ink-hatch-l)" opacity=".5" clip-path="url(#%s)" transform="translate(%s 0)"/>' % (shape, clip, f(W * 0.62)))
    g.append('<path d="%s" fill="none" stroke="#2a2018" stroke-width="1.2"/>' % shape)
    if lips:
        # upper lip over the tongue root
        g.append('<path d="%s" fill="#c87a70" stroke="#2a2018" stroke-width="1"/>' % smooth(
            [(cx - Wl * 0.86, top + 2), (cx - Wl * 0.45, top - 14), (cx - Wl * 0.1, top - 13), (cx, top - 10), (cx + Wl * 0.1, top - 13), (cx + Wl * 0.45, top - 14), (cx + Wl * 0.86, top + 2),
             (cx + Wl * 0.45, top + 1), (cx, top + 3), (cx - Wl * 0.45, top + 1)], close=True))
        g.append('<path d="M%s %s Q%s %s %s %s" stroke="#f4efe2" stroke-width="2.4" fill="none"/>' % (f(cx - Wl * 0.42), f(top + 3), f(cx), f(top + 6), f(cx + Wl * 0.42), f(top + 3)))
        g.append('<path d="M%s %s Q%s %s %s %s" stroke="#fff" stroke-opacity=".35" stroke-width="2" fill="none"/>' % (f(cx - Wl * 0.4), f(top - 9), f(cx - Wl * 0.2), f(top - 12), f(cx - Wl * 0.05), f(top - 9)))
    return '\n'.join(g), hw

def sublingual(cx, top, W, H):
    """underside of tongue with distended veins."""
    g = []
    sh = smooth([(cx - W / 2, top + H), (cx - W / 2 - 2, top + H * 0.4), (cx - W * 0.3, top + 4), (cx, top), (cx + W * 0.3, top + 4), (cx + W / 2 + 2, top + H * 0.4), (cx + W / 2, top + H)], close=True)
    g.append('<path d="%s" fill="#d98a90" stroke="#2a2018" stroke-width="1"/>' % sh)
    g.append('<path d="M%s %s L%s %s" stroke="#f0c0c0" stroke-width="3"/><path d="M%s %s L%s %s" class="ink2"/>' % (f(cx), f(top + H * 0.35), f(cx), f(top + H), f(cx), f(top + H * 0.35), f(cx), f(top + H)))
    for s in (-1, 1):
        v = [(cx + s * 9, top + H), (cx + s * 12, top + H * 0.8), (cx + s * 8, top + H * 0.62), (cx + s * 13, top + H * 0.45), (cx + s * 9, top + H * 0.28), (cx + s * 11, top + H * 0.12)]
        g.append('<path d="%s" stroke="#2a2018" stroke-width="5.4" fill="none" stroke-linecap="round"/><path d="%s" stroke="#4a3a8a" stroke-width="3.8" fill="none" stroke-linecap="round"/>' % (smooth(v), smooth(v)))
        g.append('<path d="%s" stroke="#7a6ac0" stroke-width="1" fill="none" stroke-linecap="round" transform="translate(-.8 -.4)"/>' % smooth(v))
    g.append('<path d="M%s %s q%s 8 %s 0" fill="#c87a70" stroke="#2a2018" stroke-width=".9"/>' % (f(cx - W * 0.7), f(top + H), f(W * 0.7), f(W * 1.4)))
    return '\n'.join(g)

body = []
# ================= tongue map =================
MX, MT, MW, MH = 200, 74, 128, 190
tg, hw = tongue(MX, MT, MW, MH, 'normal', coat=('#fbf8f0', .6, 0.62, 0.62, False), seed=5, skin=False, lipf=0.82)
body.append('<g>%s</g>' % tg)
# region boundaries
def Y(t): return MT + t * MH
reg = []
reg.append('<path d="M%s %s Q%s %s %s %s" class="ink2" stroke-dasharray="4 3" stroke-width=".9"/>' % (f(MX - hw(.26) * .96), f(Y(.26)), f(MX), f(Y(.31)), f(MX + hw(.26) * .96), f(Y(.26))))
reg.append('<path d="M%s %s Q%s %s %s %s" class="ink2" stroke-dasharray="4 3" stroke-width=".9"/>' % (f(MX - hw(.8) * .96), f(Y(.78)), f(MX), f(Y(.72)), f(MX + hw(.8) * .96), f(Y(.78))))
for s in (-1, 1):
    reg.append('<path d="%s" class="ink2" stroke-dasharray="4 3" stroke-width=".9"/>' % smooth([(MX + s * hw(t) * 0.6, Y(t)) for t in [0.28, 0.4, 0.55, 0.7, 0.76]]))
body.append('\n'.join(reg))
# region tags (on tongue, with halo)
tag = lambda x, y, t: '<text x="%s" y="%s" text-anchor="middle" class="lb halo" style="font-size:12px">%s</text>' % (f(x), f(y), t)
body.append(tag(MX, Y(.17), '舌根') + tag(MX, Y(.53), '舌中') + tag(MX, Y(.9), '舌尖') + tag(MX - hw(.5) * .8, Y(.5), '邊') + tag(MX + hw(.5) * .8, Y(.5), '邊'))
L = []
L.append(label(14, 84, '舌根 → 腎', None) + label(14, 98, 'root: Kidney', None, cls='le halo') + leader(100, 88, MX - 40, Y(.15)))
L.append(label(14, 150, '舌邊 → 肝膽', None) + label(14, 164, 'sides: Liver–GB', None, cls='le halo') + leader(104, 154, MX - hw(.5) * .86, Y(.48)))
L.append(label(14, 214, '舌中 → 脾胃', None) + label(14, 228, 'centre: Spleen–St', None, cls='le halo') + leader(118, 218, MX - 16, Y(.6)))
L.append(label(300, 262, '舌尖 → 心肺', None) + label(300, 276, 'tip: Heart–Lung', None, cls='le halo') + leader(298, 258, MX + 22, Y(.92)))
L.append(label(300, 100, '舌中溝', None, cls='ls halo') + label(300, 114, 'median sulcus', None, cls='le halo') + leader(298, 104, MX + 1, Y(.35)))
L.append(label(300, 150, '蕈狀乳頭（紅點）', None, cls='ls halo') + label(300, 164, 'fungiform papillae', None, cls='le halo') + leader(298, 154, MX + 52, Y(.72)))
L.append(label(300, 200, '舌苔', None, cls='ls halo') + label(300, 214, 'coating', None, cls='le halo') + leader(298, 204, MX + 22, Y(.3)))
L.append('<text x="14" y="34" class="lt">舌面分區 <tspan class="le" style="font-size:12px">tongue map (正常：淡紅舌、薄白苔)</tspan></text>')
body.append('\n'.join(L))
# reading guide + colour scale
R = []
R.append('<rect x="440" y="16" width="308" height="270" fill="#fffaf0" stroke="#bfae8a" stroke-width=".8"/>')
R.append('<text x="452" y="38" class="lb">看舌四步 <tspan class="le">how to read</tspan></text>')
rows = [('① 舌色', '淡白 · 淡紅 · 紅 · 絳 · 紫暗'), ('② 舌形', '胖大齒痕 · 瘦薄 · 裂紋 · 點刺'), ('③ 苔色', '白 · 黃 · 灰黑'), ('④ 苔質', '薄厚 · 潤燥 · 膩 · 少苔 / 剝苔')]
for i, (a, b) in enumerate(rows):
    R.append('<text x="452" y="%d" class="ls"><tspan style="font-weight:700">%s</tspan>　%s</text>' % (62 + i * 18, a, b))
R.append('<text x="452" y="146" class="ls" style="font-weight:700">舌色由淡到暗</text>')
chips = [('pale', '淡白'), ('normal', '淡紅'), ('red', '紅'), ('deep', '絳'), ('dark', '紫暗')]
for i, (k, n) in enumerate(chips):
    x = 470 + i * 56
    c1, c2 = BODY[k]
    gid = uid()
    R.append('<defs><radialGradient id="%s" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient></defs>' % (gid, c1, c2))
    R.append('<path d="M%d 156 h36 v20 q0 22 -18 22 q-18 0 -18 -22z" fill="url(#%s)" stroke="#2a2018" stroke-width=".9"/>' % (x - 18, gid))
    R.append('<text x="%d" y="214" text-anchor="middle" class="ls">%s</text>' % (x, n))
R.append('<path d="M460 222 H735" stroke="#2a2018" stroke-width=".7" marker-end="url(#ink-arrow)"/>')
R.append('<text x="452" y="240" class="ls">寒、虛 ←　　　　　　　　→ 熱、瘀</text>')
R.append('<text x="452" y="260" class="ls">自然光下看；伸舌放鬆、不要用力。</text>')
R.append('<text x="452" y="276" class="ls">咖啡、檳榔、糖果可「染苔」，先問再判斷。</text>')
body.append('\n'.join(R))

# ================= six tongues =================
cells = [
    dict(t='舌紅、苔薄黃', z='肝鬱化火', f='丹梔逍遙散、龍膽瀉肝湯', j='柴胡加龍骨牡蠣湯', p='對應：林小姐型', body='red', coat=('#e9c860', .55, 0.6, 0.6, False), seed=11),
    dict(t='舌尖紅（點刺）', z='心火熾盛', f='導赤散', j='梔子豉湯、瀉心湯類', p='急性誘發期常見', body='normal', coat=('#fbf8f0', .5, 0.55, 0.55, False), red_tip=True, seed=12),
    dict(t='舌紅少苔、有裂紋', z='陰虛火旺／心腎不交', f='黃連阿膠湯、天王補心丹、交泰丸', j='黃連阿膠湯', p='更年期常見', body='deep', coat=('#fbf8f0', .25, 0.18, 0.35, False), cracks=5, seed=13),
    dict(t='舌紅、苔黃膩', z='痰熱內擾', f='黃連溫膽湯', j='（非仲景方）', p='先排除逆流、OSA', body='red', coat=('#d4a82a', .92, 0.82, 0.8, True), seed=14),
    dict(t='舌淡胖、有齒痕', z='心脾兩虛（氣血不足）', f='歸脾湯', j='酸棗仁湯', p='對應：陳伯伯型', body='pale', coat=('#fbf8f0', .6, 0.66, 0.66, False), fat=0.18, teeth=2.6, seed=15),
    dict(t='舌暗紫、有瘀點', z='瘀血內阻', f='血府逐瘀湯', j='—', p='＋舌下絡脈怒張', body='dark', coat=('#f3eee6', .45, 0.5, 0.55, False), ecchy=9, seed=16),
]
CW, CH = 246, 178
for i, c in enumerate(cells):
    x0 = 6 + (i % 3) * 250; y0 = 300 + (i // 3) * 184
    body.append('<rect x="%d" y="%d" width="%d" height="%d" class="panel"/>' % (x0, y0, CW, CH))
    kw = {k: c[k] for k in ('coat', 'red_tip', 'cracks', 'ecchy', 'fat', 'teeth', 'seed') if k in c}
    tg, _ = tongue(x0 + 62, y0 + 44, 70, 100, c['body'], lipf=0.78, **kw)
    body.append('<g>%s</g>' % tg)
    body.append(num(x0 + 12, y0 + 14, str(i + 1)))
    tx = x0 + 126
    body.append('<text x="%d" y="%d" class="lb" style="font-size:12.5px">%s</text>' % (tx, y0 + 24, c['t']))
    body.append('<text x="%d" y="%d" class="ls" style="fill:#a8412c;font-weight:700">%s</text>' % (tx, y0 + 46, c['z']))
    def wrap(prefix, txt, n=10):
        toks = txt.split('、'); lines = []; cur = prefix
        for k, tk in enumerate(toks):
            piece = tk + ('、' if k < len(toks) - 1 else '')
            if len(cur) + len(piece) > n and cur not in ('', prefix):
                lines.append(cur); cur = piece
            elif len(cur) + len(piece) > n and cur == prefix:
                lines.append(cur); cur = piece
            else:
                cur += piece
        lines.append(cur)
        return lines
    yy = y0 + 66
    for ln in wrap('常用方：', c['f']):
        body.append('<text x="%d" y="%d" class="ls">%s</text>' % (tx, yy, ln)); yy += 15
    for ln in wrap('經方：', c['j']):
        body.append('<text x="%d" y="%d" class="ls" style="fill:#6a5640">%s</text>' % (tx, yy, ln)); yy += 15
    if i == 5:
        body.append(sublingual(x0 + 200, y0 + 118, 44, 40))
        body.append('<text x="%d" y="%d" class="ls">舌下絡脈</text>' % (tx, y0 + 140))
        body.append('<text x="%d" y="%d" class="ls">怒張</text>' % (tx, y0 + 154))
        body.append(leader(tx + 28, y0 + 150, x0 + 190, y0 + 140))
    else:
        body.append('<text x="%d" y="%d" class="ls" style="font-style:italic">%s</text>' % (tx, y0 + 166, c['p']))
    if i == 5:
        body.append('<text x="%d" y="%d" class="ls" style="font-style:italic">需排除其他疾病</text>' % (x0 + 10, y0 + 170))
body.append('<text x="14" y="292" class="lt">失眠常見六種舌象 <tspan class="le" style="font-size:12px">six tongues often seen in insomnia (證型與常用方依第 11 章)</tspan></text>')

cap = ('<b>圖 11-A　失眠常見的舌象。</b>上：舌面分區（舌尖屬心肺、舌邊屬肝膽、舌中屬脾胃、舌根屬腎）是中醫望診的傳統對應，不是解剖上的神經或血管分區。下：六種舌象各配第 11 章的證型與常用方；顏色與紋理為繪製示意，實際判讀受光源、相機、染苔影響，'
       '需合參脈症。「對應林小姐／陳伯伯型」是本讀本的教學假設，書中並未記錄兩位的舌象 <span class="ev C">示意</span>。')
open('/home/user/Insomnia/figs/pl-tongue.html', 'w').write(figure(PID, 'Plate 11·A', '失眠常見的舌象', 'Tongue atlas for insomnia patterns', 670,
                                                         '舌面分區圖與六種失眠常見舌象：舌紅苔薄黃、舌尖紅、舌紅少苔裂紋、舌紅苔黃膩、舌淡胖齒痕、舌暗紫瘀點與舌下絡脈怒張', '\n'.join(body), cap))
