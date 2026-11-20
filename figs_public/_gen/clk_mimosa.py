"""pp-mimosa  圖 1·A  de Mairan's 1729 Mimosa experiment."""
import sys, math, random
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from clk_lib import write, T, lead, f, cr, poly, rot, sun, moon, L, INK
from clk_mimosa_lib import plant, pinna_defs

PID = 'pp-mimosa'
H = 508
o = []
defs = []
defs.append(pinna_defs())

# ------------------------------------------------------------------ panel titles
o.append(T(190, 21, '① 放在窗台：看得到日夜', 'lt', 'middle'))
o.append(T(570, 21, '② 1729 年，德梅朗把它關進黑櫃子', 'lt', 'middle'))

# ------------------------------------------------------------------ LEFT: two halves of a windowsill
defs.append('<clipPath id="%s-cl"><rect x="10" y="32" width="360" height="300" rx="3"/></clipPath>' % PID)
defs.append('<linearGradient id="%s-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cc0e3"/><stop offset="1" stop-color="#e3eef6"/></linearGradient>' % PID)
defs.append('<linearGradient id="%s-nsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16213c"/><stop offset="1" stop-color="#2f3f63"/></linearGradient>' % PID)
defs.append('<linearGradient id="%s-ray" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff2b8" stop-opacity=".8"/><stop offset="1" stop-color="#fff2b8" stop-opacity="0"/></linearGradient>' % PID)
defs.append('<radialGradient id="%s-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd77a" stop-opacity=".75"/><stop offset=".45" stop-color="#f3b44c" stop-opacity=".28"/><stop offset="1" stop-color="#f3b44c" stop-opacity="0"/></radialGradient>' % PID)


def window_half(x0, night):
    g = []
    w = 180
    wall = '#ead9b8' if not night else '#b7b0b8'
    g.append('<rect x="%s" y="32" width="%s" height="300" fill="%s"/>' % (x0, w, wall))
    g.append('<rect x="%s" y="32" width="%s" height="300" fill="url(#ink-hatch-l)" opacity="%s"/>' % (x0, w, .5 if not night else .9))
    # window opening
    wx0, wx1, wy0, wy1 = x0 + 26, x0 + w - 26, 50, 214
    g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#8a6542" stroke="%s" stroke-width="1.2"/>' % (wx0 - 8, wy0 - 8, wx1 - wx0 + 16, wy1 - wy0 + 12, INK))
    g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#ink-hatch)" opacity=".35"/>' % (wx0 - 8, wy0 - 8, wx1 - wx0 + 16, wy1 - wy0 + 12))
    g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s-%s)"/>' % (wx0, wy0, wx1 - wx0, wy1 - wy0, PID, 'nsky' if night else 'sky'))
    if night:
        rnd = random.Random(4)
        for i in range(16):
            sx, sy = rnd.uniform(wx0 + 4, wx1 - 4), rnd.uniform(wy0 + 4, wy0 + 70)
            g.append('<circle cx="%s" cy="%s" r="%s" fill="#f6e7b0"/>' % (f(sx), f(sy), f(rnd.uniform(.5, 1.2))))
        g.append(moon(wx1 - 30, wy0 + 26, 13))
    else:
        g.append(sun(wx1 - 30, wy0 + 26, 11))
        # distant hills / roofs
        g.append('<path d="M%s %s Q%s %s %s %s T%s %s V%s H%s Z" fill="#b9cfa0" stroke="%s" stroke-width=".6"/>' % (
            wx0, wy1 - 34, wx0 + 40, wy1 - 52, wx0 + 80, wy1 - 38, wx1, wy1 - 44, wy1, wx0, INK))
    # glazing bars (small 18th-c panes)
    for k in (1, 2):
        xx = wx0 + (wx1 - wx0) * k / 3
        g.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#7a5638" stroke-width="3"/>' % (f(xx), wy0, f(xx), wy1))
    for k in (1, 2, 3):
        yy = wy0 + (wy1 - wy0) * k / 4
        g.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#7a5638" stroke-width="3"/>' % (wx0, f(yy), wx1, f(yy)))
    g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="1"/>' % (wx0, wy0, wx1 - wx0, wy1 - wy0, INK))
    # sill
    g.append('<path d="M%s 214 H%s L%s 226 H%s Z" fill="#b48a5e" stroke="%s" stroke-width="1"/>' % (x0 + 8, x0 + w - 8, x0 + w - 2, x0 + 2, INK))
    g.append('<rect x="%s" y="226" width="%s" height="8" fill="#9a7048" stroke="%s" stroke-width="1"/>' % (x0 + 2, w - 4, INK))
    g.append('<rect x="%s" y="226" width="%s" height="8" fill="url(#ink-hatch)" opacity=".6"/>' % (x0 + 2, w - 4))
    # wainscot panel under sill
    g.append('<rect x="%s" y="250" width="%s" height="70" fill="none" stroke="#8a6a3a" stroke-width=".8"/>' % (x0 + 16, w - 32))
    if not night:
        g.append('<path d="M%s %s L%s %s L%s 226 L%s 226 Z" fill="url(#%s-ray)"/>' % (wx1 - 30, wy0 + 26, wx1 - 10, wy0 + 30, x0 + 150, x0 + 40, PID))
    g.append(plant(x0 + 92, 214 - 40 * .62 - 1, .62, night, seed=3 if night else 5, lk=1.3))
    if night:
        g.append('<rect x="%s" y="32" width="%s" height="300" fill="#1d2440" opacity=".22"/>' % (x0, w))
    return ''.join(g)


o.append('<g clip-path="url(#%s-cl)">' % PID)
o.append(window_half(10, False))
o.append(window_half(190, True))
o.append('</g>')
o.append('<line x1="190" y1="32" x2="190" y2="332" stroke="%s" stroke-width="2.4"/>' % INK)
o.append('<line x1="190" y1="32" x2="190" y2="332" stroke="#fbf6ea" stroke-width=".8"/>')
o.append('<rect x="10" y="32" width="360" height="300" rx="3" fill="none" stroke="%s" stroke-width="1.4"/>' % INK)
# labels in the wainscot area
o.append(T(100, 272, '白天：葉子張開', 'lb', 'middle', style='font-size:14px'))
o.append(T(100, 288, 'leaflets open', 'le', 'middle'))
o.append(T(280, 272, '夜晚：葉子合起', 'lb', 'middle', style='font-size:14px'))
o.append(T(280, 288, 'leaflets fold, stalks droop', 'le', 'middle'))
o.append(T(100, 316, '含羞草 Mimosa pudica', 'ls', 'middle'))
o.append(T(280, 316, '（同一株植物）', 'ls', 'middle'))

# ------------------------------------------------------------------ RIGHT: cabinet + 18th-century observer
defs.append('<clipPath id="%s-cr"><rect x="390" y="32" width="360" height="300" rx="3"/></clipPath>' % PID)
defs.append('<clipPath id="%s-cin"><rect x="532" y="82" width="148" height="210"/></clipPath>' % PID)
defs.append('<linearGradient id="%s-wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5a36"/><stop offset=".5" stop-color="#a5714a"/><stop offset="1" stop-color="#7a4d2e"/></linearGradient>' % PID)
r = ['<g clip-path="url(#%s-cr)">' % PID]
r.append('<rect x="390" y="32" width="360" height="300" fill="#e6d6b6"/>')
r.append('<rect x="390" y="32" width="360" height="300" fill="url(#ink-hatch-l)" opacity=".7"/>')
# floor boards
r.append('<rect x="390" y="306" width="360" height="26" fill="#a98559" stroke="%s" stroke-width="1"/>' % INK)
r.append('<rect x="390" y="306" width="360" height="26" fill="url(#ink-hatch-h)"/>')
for xx in range(400, 750, 46):
    r.append('<line x1="%s" y1="306" x2="%s" y2="332" stroke="%s" stroke-width=".6"/>' % (xx, xx - 14, INK))
# --- cabinet
r.append('<rect x="522" y="74" width="168" height="226" fill="url(#%s-wood)" stroke="%s" stroke-width="1.4"/>' % (PID, INK))
r.append('<path d="M514 62 H698 L694 70 H518 Z" fill="#9b6a43" stroke="%s" stroke-width="1.2"/><rect x="518" y="70" width="176" height="6" fill="#7a4d2e" stroke="%s" stroke-width="1"/>' % (INK, INK))
r.append('<path d="M516 300 H696 V310 H516 Z" fill="#7a4d2e" stroke="%s" stroke-width="1.2"/>' % INK)
r.append('<path d="M524 310 h10 l-2 8 h-6Z M678 310 h10 l-2 8 h-6Z" fill="#5f3a22" stroke="%s" stroke-width=".9"/>' % INK)
# interior (dark) + candle glow
r.append('<rect x="532" y="82" width="148" height="210" fill="#2d241d" stroke="%s" stroke-width="1"/>' % INK)
r.append('<rect x="532" y="82" width="148" height="210" fill="url(#ink-cross)" opacity=".55"/>')
r.append('<g clip-path="url(#%s-cin)"><ellipse cx="560" cy="180" rx="150" ry="140" fill="url(#%s-glow)"/>' % (PID, PID))
r.append('<rect x="532" y="236" width="148" height="7" fill="#6a4429" stroke="%s" stroke-width=".9"/>' % INK)
r.append(plant(604, 236 - 40 * .6 - 1, .6, False, seed=11, lk=1.25))
r.append('</g>')
# door swung open on the right hinge
r.append('<path d="M690 78 L738 94 L738 290 L690 302 Z" fill="#9a6a44" stroke="%s" stroke-width="1.3"/>' % INK)
r.append('<path d="M697 94 L731 105 L731 184 L697 180 Z M697 190 L731 192 L731 280 L697 290 Z" fill="none" stroke="%s" stroke-width=".9"/>' % INK)
r.append('<path d="M690 78 L738 94 L738 290 L690 302 Z" fill="url(#ink-hatch)" opacity=".6"/>')
r.append('<path d="M690 96 h-4 v14 h4 M690 252 h-4 v14 h4" fill="#c9962e" stroke="%s" stroke-width=".7"/>' % INK)
# wood grain on stiles
for xx in (525, 528, 684, 687):
    r.append('<path d="M%s 80 C%s 130 %s 200 %s 298" stroke="#5f3a22" stroke-width=".4" fill="none"/>' % (xx, xx + 1.5, xx - 1.5, xx))

# --- observer (generic 18th-century gentleman, not a likeness)
hx, hy, hs = 452, 178, .8
P = lambda u, v: (hx + u * hs, hy + v * hs)
coat = '#56688a'
body = []
# coat torso
body.append('<path d="M440 220 C430 226 418 236 414 252 C408 276 406 300 404 334 L490 334 C490 306 490 276 484 254 C480 238 472 226 466 220 Z" fill="%s" stroke="%s" stroke-width="1.4"/>' % (coat, INK))
body.append('<path d="M414 252 C408 276 406 300 404 334 L424 334 C424 300 424 272 428 250 Z" fill="url(#ink-hatch)" opacity=".9"/>')
# waistcoat & buttons
body.append('<path d="M468 232 C476 246 480 270 481 300 L481 334 L470 334 C470 300 468 262 462 240 Z" fill="#c9962e" stroke="%s" stroke-width="1"/>' % INK)
for k in range(5):
    body.append('<circle cx="%s" cy="%s" r="1.5" fill="#f1d27a" stroke="%s" stroke-width=".5"/>' % (f(474 + k * 1.2), 252 + k * 15, INK))
# coat fold lines
body.append('<path d="M440 260 C438 285 437 310 436 334 M452 266 C454 290 455 312 455 334" class="ink2"/>')
o_head = L.head(hx, hy, hs, hair='grey')
# wig: side curls + queue ribbon (powdered)
wig = []
wig.append('<path d="%s" fill="#ece7dd" stroke="%s" stroke-width=".9"/>' % (cr([P(u, v) for u, v in [(17, -31), (8, -44), (-14, -48), (-30, -34), (-36, -16), (-34, 2), (-27, 14), (-21, 4), (-19, -8), (-12, -17), (0, -24)]], True), INK))
wig.append('<path d="%s" fill="none" stroke="#a49a88" stroke-width=".6"/>' % ''.join('M%.1f %.1f Q%.1f %.1f %.1f %.1f' % (P(u, -40 + k)[0], P(u, -40 + k)[1], P(u - 12, -44 + k)[0], P(u - 12, -44 + k)[1], P(u - 24, -36 + k)[0], P(u - 24, -36 + k)[1]) for u, k in [(10, 0), (6, 6), (2, 12), (-4, 18)]))
for k, (u, v) in enumerate([(-9, -4), (-10, 6)]):
    cx, cy = P(u, v)
    wig.append('<ellipse cx="%s" cy="%s" rx="8" ry="4.2" fill="#f1ece2" stroke="%s" stroke-width=".8"/>' % (f(cx), f(cy), INK))
    wig.append('<path d="M%s %s a3 2.2 0 1 1 -4 1.5" fill="none" stroke="%s" stroke-width=".5"/>' % (f(cx + 4), f(cy - 1), INK))
qx, qy = P(-26, 20)
wig.append('<path d="M%s %s C%s %s %s %s %s %s" fill="none" stroke="#e8e2d6" stroke-width="4" stroke-linecap="round"/>' % (f(qx + 4), f(qy - 8), f(qx - 2), f(qy), f(qx - 4), f(qy + 10), f(qx - 2), f(qy + 22)))
wig.append('<path d="M%s %s l-7 -5 l1 10 Z M%s %s l7 -5 l-1 10Z" fill="#2a2018"/>' % (f(qx - 2), f(qy + 4), f(qx - 2), f(qy + 4)))
# jabot (lace cravat)
jab = '<path d="M462 214 C470 220 474 228 472 240 C468 238 466 236 464 238 C462 232 458 226 456 220 Z" fill="#fbf8f0" stroke="%s" stroke-width=".8"/><path d="M464 222 c3 3 4 7 4 12" class="ink2"/>' % INK
# arm (sleeve) reaching forward with candle
arm = []
arm.append('<path d="M446 228 C462 236 472 256 478 270 C486 268 496 262 504 254 L512 262 C502 274 490 284 476 288 C466 288 460 278 452 262 C446 250 440 240 446 228Z" fill="%s" stroke="%s" stroke-width="1.3"/>' % (coat, INK))
arm.append('<path d="M452 262 C460 278 466 288 476 288 C470 280 462 268 458 256 Z" fill="url(#ink-hatch)"/>')
# turned-back cuff + lace
arm.append('<path d="M498 252 L510 246 L520 262 L508 270 Z" fill="#3f4f6c" stroke="%s" stroke-width="1"/>' % INK)
arm.append('<path d="M510 246 c3 2 5 6 4 9 c3 1 6 4 6 7" fill="none" stroke="#fbf8f0" stroke-width="2.2"/>')
# hand holding the candlestick
hand = '<path d="M515 250 C520 246 526 246 528 250 C530 254 528 258 524 260 C520 262 516 259 515 256 Z" fill="url(#ink-vol-flesh)" stroke="%s" stroke-width=".9"/><path d="M520 250 c2 1 3 3 3 5 M523 249 c2 1 3 3 2.6 5.4" class="ink2"/>' % INK
cand = []
cand.append('<ellipse cx="520" cy="256" rx="160" ry="150" fill="url(#%s-glow)"/>' % PID)
cand.append('<ellipse cx="522" cy="246" rx="11" ry="3" fill="#d9b53c" stroke="%s" stroke-width=".9"/>' % INK)
cand.append('<path d="M519 246 V214 h6 V246 Z" fill="#fbf6ea" stroke="%s" stroke-width=".9"/>' % INK)
cand.append('<path d="M522 214 v-3" stroke="%s" stroke-width=".8"/>' % INK)
cand.append('<path d="M522 196 C526 202 527 207 522 211 C517 207 518 202 522 196 Z" fill="#f6c24a" stroke="#b5473a" stroke-width=".8"/>')
cand.append('<path d="M522 202 C523.5 205 523.5 207 522 209 C520.5 207 520.5 205 522 202Z" fill="#fff6d0"/>')
r.append('<g>' + cand[0] + '</g>')
r.extend(body)
r.append(jab)
r.append(o_head)
r.extend(wig)
r.extend(arm)
r.append(hand)
r.extend(cand[1:])
# sight line from eye into cabinet
ex, ey = P(26, -5)
r.append('<path d="M%s %s L586 168" stroke="#b5473a" stroke-width=".9" stroke-dasharray="3 3" fill="none" marker-end="url(#ink-arrow-red)"/>' % (f(ex + 4), f(ey)))
r.append('</g>')
o.extend(r)
o.append('<rect x="390" y="32" width="360" height="300" rx="3" fill="none" stroke="%s" stroke-width="1.4"/>' % INK)

# --- night inset (same cabinet, 10 pm)
cx, cy, cr_ = 438, 82, 42
defs.append('<clipPath id="%s-ci"><circle cx="%s" cy="%s" r="%s"/></clipPath>' % (PID, cx, cy, cr_))
o.append('<circle cx="%s" cy="%s" r="%s" fill="#fbf6ea" stroke="%s" stroke-width="1"/>' % (cx, cy, cr_ + 4, INK))
o.append('<g clip-path="url(#%s-ci)"><rect x="%s" y="%s" width="%s" height="%s" fill="#2d241d"/><ellipse cx="%s" cy="%s" rx="60" ry="60" fill="url(#%s-glow)"/>' % (PID, cx - cr_, cy - cr_, 2 * cr_, 2 * cr_, cx - 18, cy + 8, PID))
o.append('<rect x="%s" y="%s" width="%s" height="5" fill="#6a4429"/>' % (cx - cr_, cy + 30, 2 * cr_))
o.append(plant(cx + 4, cy + 30 - 40 * .36, .36, True, seed=21, flowers=True, lk=2.1))
o.append('</g><circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1.6"/>' % (cx, cy, cr_, INK))
o.append(moon(cx - 30, cy - 34, 8))
o.append(T(492, 52, '晚上 10 點再打開看：', 'lb', 'start', style='font-size:13.5px'))
o.append(T(624, 52, '葉子照樣合起', 'lb', 'start', style='font-size:13.5px;fill:#2c5d9c'))
o.append('<path class="ld" d="M489 48 C484 50 482 54 479 58" marker-end="url(#ink-dot)"/>')
# bottom label for the day view
o.append('<rect x="536" y="312" width="194" height="17" rx="3" fill="#fbf6ea" stroke="%s" stroke-width=".6"/>' % INK)
o.append(T(633, 325, '白天打開看：葉子照樣張開', 'lb', 'middle', halo=False, style='font-size:13px;fill:#a8412c'))

# ------------------------------------------------------------------ 24-h strips
def strip(x0, y0, w, dark_always):
    g = []
    X = lambda t: x0 + t / 48 * w
    # row 1: light
    g.append(T(x0 - 6, y0 + 12, '光線', 'ls', 'end', halo=False, style='font-weight:700'))
    for a, b in [(0, 6), (6, 18), (18, 30), (30, 42), (42, 48)]:
        day = 6 <= a % 24 < 18
        col = '#2e2a35' if dark_always else ('#f6e2a0' if day else '#24305a')
        g.append('<rect x="%s" y="%s" width="%s" height="16" fill="%s"/>' % (f(X(a)), y0, f(X(b) - X(a)), col))
        if not dark_always:
            mx = (X(a) + X(b)) / 2
            if day:
                g.append(sun(mx, y0 + 8, 3.6))
            elif b - a > 6:
                g.append(moon(mx, y0 + 8, 5))
    if dark_always:
        g.append(T(X(24), y0 + 12, '櫃子裡始終一片漆黑', 'ls', 'middle', halo=False, style='fill:#f6e7b0'))
    g.append('<rect x="%s" y="%s" width="%s" height="16" fill="none" stroke="%s" stroke-width=".8"/>' % (x0, y0, w, INK))
    # row 2: leaf glyphs
    y1 = y0 + 22
    g.append(T(x0 - 6, y1 + 13, '葉子', 'ls', 'end', halo=False, style='font-weight:700'))
    g.append('<rect x="%s" y="%s" width="%s" height="18" fill="#fbf6ea" stroke="%s" stroke-width=".8"/>' % (x0, y1, w, INK))
    for a in [6, 30]:
        g.append('<rect x="%s" y="%s" width="%s" height="18" fill="#e4ecd0"/>' % (f(X(a)), y1, f(X(a + 12) - X(a))))
    g.append('<rect x="%s" y="%s" width="%s" height="18" fill="none" stroke="%s" stroke-width=".8"/>' % (x0, y1, w, INK))
    for k in range(16):
        t = 1.5 + 3 * k
        open_ = 6 <= t % 24 < 18
        cx_, cy_ = X(t), y1 + 9
        if open_:
            d = 'M%s %sH%s' % (f(cx_ - 7), f(cy_ + 2), f(cx_ + 7))
            for j in range(6):
                xx = cx_ - 5 + j * 2.2
                d += 'M%s %sl1.6 -4.2M%s %sl1.6 4.2' % (f(xx), f(cy_ + 2), f(xx), f(cy_ + 2))
            g.append('<path d="%s" stroke="#5f7a2e" stroke-width=".9" fill="none" stroke-linecap="round"/>' % d)
        else:
            d = 'M%s %sQ%s %s %s %s' % (f(cx_ - 6), f(cy_ - 5), f(cx_ - 2), f(cy_ - 4), f(cx_ + 3), f(cy_ + 5))
            d += 'M%s %sQ%s %s %s %s' % (f(cx_ - 5), f(cy_ - 5.6), f(cx_ - 1), f(cy_ - 3.6), f(cx_ + 4), f(cy_ + 4))
            g.append('<path d="%s" stroke="#4e5e2a" stroke-width="1.4" fill="none" stroke-linecap="round"/>' % d)
    # time axis
    ya = y1 + 18
    for t in range(0, 49, 6):
        g.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width=".7"/>' % (f(X(t)), ya, f(X(t)), ya + 3, INK))
        g.append(T(X(t), ya + 13, str(t % 24) if t != 48 else '24', 'ls', 'middle', halo=False))
    return ''.join(g)


o.append(strip(52, 346, 316, False))
o.append(strip(432, 346, 316, True))
o.append(T(210, 414, '時鐘時間（連續兩天）clock time, 2 days', 'ls', 'middle', halo=False))
o.append(T(590, 414, '沒有日夜，葉子仍然準時開、合', 'ls', 'middle', halo=False, style='font-weight:700;fill:#a8412c'))

# ------------------------------------------------------------------ message band
by = 430
o.append('<rect x="10" y="%s" width="740" height="56" rx="8" fill="#f6e7b0" stroke="#c9962e" stroke-width="1.4"/>' % by)
o.append('<rect x="14" y="%s" width="732" height="48" rx="6" fill="none" stroke="#c9962e" stroke-width=".6"/>' % (by + 4))
# small clock glyph with a leaf
o.append(L.clock(214, by + 28, 17, 10, 10))
o.append(T(244, by + 26, '植物身體裡有自己的時鐘', 'lt', 'start', halo=False, style='font-size:21px'))
o.append(T(246, by + 45, 'The plant carries its own inner clock — it keeps time even in the dark.', 'le', 'start', halo=False, style='font-size:12.5px'))
o.append(T(380, H - 6, '示意圖：植物大小、櫃子與人物皆為示意；人物為示意，非肖像。', 'ls', 'middle', halo=False, style='font-size:10.5px;fill:#8a6a3a'))

caption = ('<b>圖 1·A　黑暗中仍「記得時間」的含羞草。</b>含羞草白天把小葉張開，天黑後合起來、葉柄垂下。'
           '1729 年，法國天文學家德梅朗（de Mairan）把它放進不見天日的櫃子裡，發現它照樣在白天張開、夜裡合起——'
           '可見節律不是陽光「推」出來的，而是植物體內自己有個時鐘。人物為示意，非肖像。')
write(PID, '圖 1·A', '1729 年，在黑暗櫃子裡仍「記得時間」的含羞草', "De Mairan's mimosa — a plant that keeps time in the dark",
      H, '\n'.join(o), '左：窗台上的含羞草白天葉子張開、夜晚合起；右：關進黑暗櫃子後，十八世紀的天文學家拿著蠟燭查看，含羞草仍照時間開合；下方為兩天的光線與葉子開合時間條。',
      caption, ''.join(defs))
