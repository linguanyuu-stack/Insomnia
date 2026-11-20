import sys, math
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from pplib import *

PID = "pp-pedals"
RED, BLUE = "#a8412c", "#2c5d9c"
X0, Y0, X1, Y1 = 176, 44, 584, 396   # main scene frame

def P(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def gauge(cx, cy, r, vmax, val, red_from=None, labels=None, unit="", title=""):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="#b9b2a6" stroke="#2a2018" stroke-width="1.2"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r+3}" fill="#6d665c" stroke="#2a2018" stroke-width=".6"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1f1d1a" stroke="#2a2018" stroke-width=".8"/>']
    th = lambda v: 135 + v / vmax * 270
    if red_from is not None:
        a0, a1 = th(red_from), th(vmax)
        p0, p1 = P(cx, cy, r - 5, a0), P(cx, cy, r - 5, a1)
        o.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{r-5} {r-5} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="#e0413a" stroke-width="7"/>')
    steps = int(vmax * 2) if vmax <= 8 else int(vmax / 10)
    for i in range(steps + 1):
        v = vmax * i / steps
        major = (i % 2 == 0)
        a = th(v)
        q0, q1 = P(cx, cy, r - 2, a), P(cx, cy, r - (11 if major else 7), a)
        o.append(f'<line x1="{q0[0]:.1f}" y1="{q0[1]:.1f}" x2="{q1[0]:.1f}" y2="{q1[1]:.1f}" stroke="#f3ead6" stroke-width="{1.6 if major else .8}"/>')
    if labels:
        for v, t in labels:
            q = P(cx, cy, r - (19 if r > 38 else 15), th(v))
            o.append(f'<text x="{q[0]:.1f}" y="{q[1]+3.2:.1f}" text-anchor="middle" style="font-family:sans-serif;font-size:{9.5 if r > 38 else 7.5}px;font-weight:700;fill:#f3ead6">{t}</text>')
    o.append(f'<text x="{cx}" y="{cy+r*.42:.1f}" text-anchor="middle" style="font-family:sans-serif;font-size:7.5px;fill:#cfc6b2">{unit}</text>')
    a = th(val)
    tip = P(cx, cy, r - 4, a); tail = P(cx, cy, 9, a + 180)
    o.append(f'<line x1="{tail[0]:.1f}" y1="{tail[1]:.1f}" x2="{tip[0]:.1f}" y2="{tip[1]:.1f}" stroke="#ff6a3d" stroke-width="2.6" stroke-linecap="round"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#3a3632" stroke="#cfc6b2" stroke-width=".8"/>')
    # glass reflection
    o.append(f'<path d="M{cx-r*.7:.1f} {cy-r*.45:.1f} A{r*.85:.1f} {r*.85:.1f} 0 0 1 {cx+r*.2:.1f} {cy-r*.83:.1f}" fill="none" stroke="#fff" stroke-width="2" opacity=".18"/>')
    return "".join(o)


SHOE = ("M0 -62 C14 -62 24 -48 25 -30 C26 -14 20 0 18 14 C17 30 20 46 16 56 C12 64 -12 64 -16 56 "
        "C-20 46 -18 30 -18 14 C-19 0 -25 -14 -24 -30 C-23 -48 -14 -62 0 -62Z")


def foot(x, y, rot, mirror=False, pid="a"):
    """top-down/behind view of a leather shoe with ankle + trouser leg heading toward the viewer (+y)"""
    m = " scale(-1,1)" if mirror else ""
    o = [f'<g transform="translate({x},{y}) rotate({rot}){m}">']
    # trouser leg (comes toward viewer, widening)
    leg = "M-21 22 C-24 60 -34 110 -40 170 L46 170 C40 110 26 60 22 22 C10 16 -10 16 -21 22Z"
    # shoe sole rim + upper
    o.append(f'<path d="{SHOE}" fill="#2e211a" stroke="#2a2018" stroke-width="1.4"/>')
    o.append(f'<path d="{SHOE}" transform="scale(.9) translate(0,-1)" fill="url(#{PID}-leather)" stroke="#2a2018" stroke-width=".9"/>')
    # shading on outer side of upper
    o.append(f'<clipPath id="{PID}-sc{pid}"><path d="{SHOE}" transform="scale(.9) translate(0,-1)"/></clipPath>'
             f'<g clip-path="url(#{PID}-sc{pid})"><path d="M10 -70 C24 -40 20 0 20 70 L40 70 L40 -70Z" fill="url(#ink-hatch)" opacity=".9"/>'
             f'<path d="M-22 -10 C-24 10 -20 40 -16 70 L-40 70 L-40 -10Z" fill="url(#ink-hatch-l)"/></g>')
    # toe-cap seam with brogue dots
    o.append('<path d="M-19 -33 C-9 -27 9 -27 20 -33" class="ink2" stroke="#f0d2b0" stroke-width=".8"/>'
             '<path d="M-19 -35.5 C-9 -29.5 9 -29.5 20 -35.5" class="ink2" stroke-dasharray="1 2"/>')
    o.append('<path d="M-6 -56 C-2 -58 4 -58 8 -55" fill="none" stroke="#fff" stroke-width="1.6" opacity=".35"/>')
    # vamp / tongue / laces
    o.append('<path d="M-10 -22 C-6 -26 6 -26 10 -22 L12 20 L-12 20Z" fill="#6b4a32" stroke="#2a2018" stroke-width=".8"/>'
             '<path d="M-4 -24 C-2 -25 2 -25 4 -24 L5 18 L-5 18Z" fill="#4e3424"/>')
    for i in range(5):
        yy = -18 + i * 7.5
        o.append(f'<circle cx="-8" cy="{yy}" r="1.3" fill="#d9c79f" stroke="#2a2018" stroke-width=".4"/><circle cx="8" cy="{yy}" r="1.3" fill="#d9c79f" stroke="#2a2018" stroke-width=".4"/>')
        if i < 4:
            o.append(f'<path d="M-8 {yy} L8 {yy+7.5} M8 {yy} L-8 {yy+7.5}" stroke="#efe2c4" stroke-width="1.4"/>'
                     f'<path d="M-8 {yy} L8 {yy+7.5} M8 {yy} L-8 {yy+7.5}" stroke="#2a2018" stroke-width=".3"/>')
    o.append('<path d="M-8 -18 L8 -18" stroke="#efe2c4" stroke-width="1.4"/>')
    # quarter seam
    o.append('<path d="M-17 2 C-12 -2 -10 -10 -10 -20 M17 2 C12 -2 10 -10 10 -20" class="ink2"/>')
    # sock band
    o.append('<path d="M-17 18 C-10 12 10 12 17 18 L19 30 L-19 30Z" fill="#3e4656" stroke="#2a2018" stroke-width=".8"/>'
             '<path d="M-14 20 V28 M-9 17 V28 M-4 16 V28 M1 16 V28 M6 16 V28 M11 17 V28 M15 19 V28" stroke="#2a2018" stroke-width=".4" opacity=".6"/>')
    # trouser
    o.append(f'<path d="{leg}" fill="#55607a" stroke="#2a2018" stroke-width="1.3"/>')
    o.append('<path d="M14 26 C26 70 34 110 40 170 L46 170 C40 110 26 60 22 22Z" fill="url(#ink-hatch-d)"/>'
             '<path d="M-21 22 C-24 60 -34 110 -40 170 L-30 170 C-24 110 -16 60 -14 24Z" fill="url(#ink-hatch-l)"/>'
             '<path d="M-21 22 C-10 30 12 30 22 22 M-19 34 C-8 40 10 40 20 33" class="ink2"/>'
             '<path d="M2 40 C0 80 2 120 4 170 M-8 60 C-10 70 -12 80 -16 92 M12 70 C16 84 18 96 18 110" class="ink2"/>')
    o.append('</g>')
    return "".join(o)


def press_marks(x, y, col, rot=0):
    o = [f'<g transform="translate({x},{y}) rotate({rot})">']
    for a in (-60, -35, -10, 15):
        p0, p1 = P(0, 0, 70, a - 90), P(0, 0, 84, a - 90)
        o.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>')
    o.append('</g>')
    return "".join(o)


S = []  # scene
S.append(f'<defs><linearGradient id="{PID}-leather" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9a6a45"/><stop offset=".6" stop-color="#7a5236"/><stop offset="1" stop-color="#5a3a26"/></linearGradient>'
         f'<radialGradient id="{PID}-gr" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e0413a" stop-opacity=".55"/><stop offset="1" stop-color="#e0413a" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="{PID}-gb" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3f6fa6" stop-opacity=".5"/><stop offset="1" stop-color="#3f6fa6" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="{PID}-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffb347" stop-opacity=".85"/><stop offset=".55" stop-color="#ff8a3d" stop-opacity=".35"/><stop offset="1" stop-color="#ff8a3d" stop-opacity="0"/></radialGradient>'
         f'<clipPath id="{PID}-clip"><rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}"/></clipPath></defs>')
S.append(f'<g clip-path="url(#{PID}-clip)">')
# floor / carpet
S.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="#7d746a"/>')
S.append(f'<path d="M{X0} 196 C300 204 460 204 {X1} 196 V{Y1} H{X0}Z" fill="#8f867a"/><path d="M{X0} 196 C300 204 460 204 {X1} 196 V{Y1} H{X0}Z" fill="url(#ink-stipple-l)"/>')
# rubber floor mat
S.append(f'<path d="M206 236 C300 230 460 230 548 236 L572 {Y1+4} H190Z" fill="#4a4540" stroke="#2a2018" stroke-width="1.2"/>')
for i in range(12):
    yy = 248 + i * 13
    S.append(f'<path d="M{208 - i*1.3:.0f} {yy} H{550 + i*1.6:.0f}" stroke="#2a2018" stroke-width="1" opacity=".55"/>')
# firewall (front wall of footwell)
S.append(f'<path d="M{X0} 150 C300 160 460 160 {X1} 150 V198 C460 206 300 206 {X0} 198Z" fill="#5d564e"/>'
         f'<path d="M{X0} 150 C300 160 460 160 {X1} 150 V198 C460 206 300 206 {X0} 198Z" fill="url(#ink-hatch)" opacity=".8"/>'
         f'<path d="M{X0} 198 C300 206 460 206 {X1} 198" class="ink"/>')
# side panels: door kick panel (left), centre tunnel (right)
S.append(f'<path d="M{X0} 150 L206 170 L198 {Y1} H{X0}Z" fill="#6a625a" stroke="#2a2018" stroke-width="1.2"/><path d="M{X0} 150 L206 170 L198 {Y1} H{X0}Z" fill="url(#ink-hatch-r)" opacity=".7"/>')
S.append(f'<path d="M{X1} 146 L548 168 L566 {Y1} H{X1}Z" fill="#5a534b" stroke="#2a2018" stroke-width="1.2"/><path d="M{X1} 146 L548 168 L566 {Y1} H{X1}Z" fill="url(#ink-hatch-d)" opacity=".8"/>')
# ---- brake pedal (suspended), blue glow
S.append(f'<ellipse cx="262" cy="244" rx="70" ry="44" fill="url(#{PID}-gb)"/>')
S.append('<path d="M258 156 L266 156 L268 226 L258 226Z" fill="#9a958c" stroke="#2a2018" stroke-width="1"/><path d="M264 158 L268 226 L264 226Z" fill="url(#ink-hatch-d)"/>')
S.append('<path d="M262 252 h0" />')
# ghost rest position
S.append('<rect x="226" y="222" width="74" height="40" rx="7" fill="#3a3733" stroke="#2a2018" stroke-width="1.3"/>')
for i in range(6):
    S.append(f'<path d="M232 {228+i*6} H294" stroke="#7a756c" stroke-width="1.3"/>')
# ---- accelerator (floor hinged organ pedal), red glow
S.append(f'<ellipse cx="470" cy="262" rx="64" ry="66" fill="url(#{PID}-gr)"/>')
S.append('<path d="M450 206 L490 206 L494 320 L448 320Z" fill="#2f2c29" stroke="#2a2018" stroke-width="1.3"/>')
for i in range(15):
    S.append(f'<path d="M{453+0.0*i:.0f} {212+i*7} H{489+0.2*i:.1f}" stroke="#77716a" stroke-width="1.2"/>')
S.append('<path d="M446 318 H496 V328 H446Z" fill="#8e897f" stroke="#2a2018" stroke-width="1"/><circle cx="452" cy="323" r="2" fill="#2a2018"/><circle cx="490" cy="323" r="2" fill="#2a2018"/>')
# ---- feet
S.append(foot(258, 262, -6, mirror=True, pid="l"))
S.append(foot(470, 252, 5, mirror=False, pid="r"))
S.append(press_marks(258, 262, "#3f6fa6", -6))
S.append(press_marks(470, 252, "#e0413a", 5))
# ---- dashboard (top)
S.append(f'<path d="M{X0} {Y0} H{X1} V146 C460 166 300 166 {X0} 146Z" fill="#45403a" stroke="#2a2018" stroke-width="1.6"/>'
         f'<path d="M{X0} 128 C300 150 460 150 {X1} 128 V146 C460 166 300 166 {X0} 146Z" fill="url(#ink-hatch-d)" opacity=".8"/>')
S.append(f'<path d="M232 {Y0} V96 C232 128 252 136 290 138 H474 C512 136 530 128 530 96 V{Y0}" fill="#2a2724" stroke="#2a2018" stroke-width="1.3"/>')
S.append('<path d="M240 52 C300 46 460 46 522 52" fill="none" stroke="#6d665c" stroke-width="1"/>')
S.append(f'<ellipse cx="452" cy="96" rx="80" ry="58" fill="url(#{PID}-glow)" opacity=".75"/>')
S.append(gauge(310, 96, 33, 200, 0, None, [(40, "40"), (80, "80"), (120, "120"), (160, "160")], "km/h"))
S.append(gauge(452, 94, 42, 8, 7.7, 6, [(i, str(i)) for i in range(1, 8)], "×1000"))
# warning light between gauges
S.append('<path d="M381 72 l7 12 h-14Z" fill="#f2b33d" stroke="#2a2018" stroke-width=".7"/><text x="381" y="83" text-anchor="middle" style="font-family:sans-serif;font-size:8px;font-weight:700;fill:#2a2018">!</text>')
S.append('</g>')
S.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="none" stroke="#2a2018" stroke-width="1.4"/>')

L = []
# labels left column
L.append(f'<text x="10" y="82" class="lb halo" style="font-size:14px">車速卻是 0</text>'
         f'<text x="10" y="99" class="ls halo">引擎狂轉，車子沒前進：</text><text x="10" y="113" class="ls halo">整晚躺著，卻休息不到</text>')
L.append(lead([(150, 96), (168, 96), (276, 96)]))
L.append(f'<text x="10" y="236" class="lb halo" style="font-size:15px;fill:{BLUE}">煞車 ＝ 睡眠系統</text>'
         f'<text x="10" y="254" class="ls halo">睡意、夜晚、</text><text x="10" y="268" class="ls halo">一整天累積的「想睡壓力」</text>')
L.append(lead([(160, 244), (226, 244)]))
# right column
L.append(f'<text x="598" y="70" class="lb halo" style="font-size:14px;fill:{RED}">轉速衝上紅線</text>'
         f'<text x="598" y="87" class="ls halo">大腦在高速空轉</text><text x="598" y="101" class="le halo">hyperarousal 過度警覺</text>')
L.append(lead([(594, 78), (500, 70)]))
L.append(f'<text x="598" y="228" class="lb halo" style="font-size:15px;fill:{RED}">油門 ＝ 清醒系統</text>'
         f'<text x="598" y="246" class="ls halo">壓力、焦慮、警覺、</text><text x="598" y="260" class="ls halo">心跳快、腦子停不下來</text>')
L.append(lead([(594, 236), (494, 236)]))
L.append(f'<text x="598" y="340" class="ls halo">兩腳同時踩到底：</text><text x="598" y="354" class="ls halo">睡意其實有，</text><text x="598" y="368" class="ls halo">只是被油門蓋過去</text>')
L.append(f'<text x="380" y="30" class="lb" text-anchor="middle" style="font-size:14px">一個比喻：駕駛座下的兩個踏板 <tspan class="le">a metaphor for the over-aroused brain</tspan></text>')

# ===== inset: bed, exhausted but wide awake
IX, IY, IW, IH = 10, 420, 380, 190
I = [f'<g transform="translate({IX},{IY})">',
     f'<defs><clipPath id="{PID}-ic"><rect x="0" y="0" width="{IW}" height="{IH}"/></clipPath></defs><g clip-path="url(#{PID}-ic)">',
     f'<rect x="0" y="0" width="{IW}" height="{IH}" fill="#c9d3e3"/><rect x="0" y="0" width="{IW}" height="{IH}" fill="url(#ink-hatch-h)" opacity=".5"/>',
     f'<path d="M0 {IH-18} H{IW} V{IH} H0Z" fill="#9aa6b6"/><path d="M0 {IH-18} H{IW} V{IH} H0Z" fill="url(#ink-hatch-l)"/><path d="M0 {IH-18} H{IW}" class="ink"/>',
     window(300, 18, 56, 60)]
# bedside clock on a shelf
I.append(f'<path d="M196 58 H266 V64 H196Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>' + digital(208, 36, "03:12", 46, 22))
K = 1.3
I.append(f'<g transform="scale({K})">')
BH = (IH - 18) / K
I.append(f'<ellipse cx="62" cy="{BH-66}" rx="50" ry="40" fill="url(#{PID}-glow)"/>')
I.append(bed_lying(IW / K, 0, BH, eye="wide", shirt="#cfdcef", hx=64, head_s=.5))
# glowing brain overlay over cranium (head rotated -90: cranium centre at (64, by-63))
hy = BH - 63
I.append(brain_glyph(64, hy + 1, .42, fill="#ffb26b", op=.75, stroke="#a8412c").replace('translate(64', 'translate(64').replace(f'scale(.36)', 'rotate(-90) scale(.36)'))
# under-eye dark circle (eye at local (25,-4) rotated -90 -> (x-4*s, y-25*s)) and tired sweat-free lines
s = .5
ex, ey = 64 + (-4.8) * s, hy - 25.3 * s
I.append(f'<path d="M{ex+3.4:.1f} {ey-3.5:.1f} C{ex+5.5:.1f} {ey-1:.1f} {ex+5.5:.1f} {ey+2:.1f} {ex+3.4:.1f} {ey+4.5:.1f}" fill="none" stroke="#7a5a6a" stroke-width="1.4" opacity=".6"/>')
# arousal squiggles above head
for k, (ax, ay) in enumerate([(34, 40), (58, 30), (84, 40)]):
    I.append(f'<path d="M{ax} {ay} l3 -6 l3 6 l3 -6" fill="none" stroke="#e0413a" stroke-width="1.3" stroke-linecap="round"/>')
I.append('</g></g>')
I.append(f'<rect x="0" y="0" width="{IW}" height="{IH}" fill="none" stroke="#2a2018" stroke-width="1.2"/>')
I.append('</g>')
I.append(f'<text x="{IX}" y="{IY-7}" class="lb halo" style="font-size:14px">身體累壞了，大腦卻還在「加班」</text>')
# labels inside inset (top, clear sky area)
I.append(f'<text x="{IX+128}" y="{IY+28}" class="ls halo">眼睛睜大、腦中轉個不停</text>')
I.append(lead([(IX + 124, IY + 24), (IX + 112, IY + 24), (IX + 92, IY + 76)]))

# ===== message panel
MX, MY = 410, 420
M = [f'<rect x="{MX}" y="{MY}" width="340" height="190" rx="6" fill="#f6e7b0" fill-opacity=".45" stroke="#2a2018" stroke-width=".9"/>',
     f'<text x="{MX+18}" y="{MY+36}" class="lt" style="font-size:20px">很累，卻睡不著——</text>',
     f'<text x="{MX+18}" y="{MY+66}" class="lt" style="font-size:18px">不是不想睡，</text>',
     f'<text x="{MX+18}" y="{MY+94}" class="lt" style="font-size:18px;fill:{RED}">是大腦的油門沒放開。</text>',
     f'<path d="M{MX+18} {MY+110} H{MX+322}" class="ink2"/>',
     f'<text x="{MX+18}" y="{MY+132}" class="ls">所以越「用力想睡」通常越清醒；</text>',
     f'<text x="{MX+18}" y="{MY+150}" class="ls">先學會<tspan style="font-weight:700;fill:{RED}">鬆開油門</tspan>（放鬆、別硬逼自己睡），</text>',
     f'<text x="{MX+18}" y="{MY+168}" class="ls">本來就有的<tspan style="font-weight:700;fill:{BLUE}">煞車（睡意）</tspan>才踩得住。</text>']

body = "\n".join(["".join(S), "".join(L), "".join(I), "".join(M)])
cap = ('<b>圖 4·B　油門和煞車同時踩。</b>失眠的人並不是缺少睡意，而是「清醒系統」（壓力、焦慮、警覺）的油門一直沒放開，蓋過了「睡眠系統」的煞車：'
       '引擎轉速衝上紅線，車子卻原地不動——躺了一整晚，身體卻休息不到。治療的重點因此是鬆開油門，而不是更用力地逼自己睡。比喻示意圖。')
html = fig(PID, "圖 4·B", "油門和煞車同時踩", "Hyperarousal — accelerator and brake pressed together", 620,
           "汽車駕駛座腳踏區特寫：一隻腳踩煞車（睡眠系統），另一隻腳踩油門（清醒系統），儀表板轉速表衝上紅線、車速為零；下方小圖為疲倦卻睜大眼睛躺在床上的人，頭部發出光暈",
           body, cap)
write(PID, html)
print(len(html))
