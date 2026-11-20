import sys, math
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from pplib import *

PID = "pp-cbti"
RED, BLUE, GOLD = "#a8412c", "#2c5d9c", "#c9962e"
PJ = "#9fb3cf"   # pajama


def bed_side(x, y, s=1.0, blanket="#e8d6ae", person=False):
    """small side-view bed, origin at floor-left (headboard), length 100*s"""
    o = [f'<g transform="translate({x},{y}) scale({s})">',
         '<path d="M0 0 V-46 C0 -52 10 -53 12 -47 V0Z" fill="#a57c55" stroke="#2a2018" stroke-width="1.1"/>',
         '<path d="M10 -22 H100 V-12 H10Z" fill="#f4eee0" stroke="#2a2018" stroke-width=".9"/>',
         '<path d="M10 -12 H100 V-8 H10Z" fill="#a57c55" stroke="#2a2018" stroke-width=".8"/>',
         '<path d="M96 0 V-30 C96 -34 104 -34 104 -30 V0Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>',
         '<path d="M12 -23 C10 -28 14 -31 22 -31 C30 -31 34 -29 34 -25 C33 -22 20 -21 12 -23Z" fill="#fbf6ea" stroke="#2a2018" stroke-width=".8"/>']
    if person:
        o.append(head(26, -31, .2, -90, eye="closed"))
    o.append(f'<path d="M{32 if person else 30} -24 C40 -30 56 -30 70 -28 C82 -27 92 -27 97 -26 L97 -12 L{32 if person else 30} -12Z" fill="{blanket}" stroke="#2a2018" stroke-width=".9"/>'
             '<path d="M52 -29 C50 -22 52 -16 50 -12 M74 -28 C76 -22 74 -16 76 -12" class="ink2"/>')
    o.append('<path d="M14 -8 V0 M92 -8 V0" stroke="#2a2018" stroke-width="2"/></g>')
    return "".join(o)


def walker(x, y, s=1.0):
    """standing person in pyjamas walking to the right; feet at origin, height 110*s"""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    # back arm
    o.append(capsule(-3, -88, -10, -70, 3.6, 3.2, "#8aa0bf", .9))
    o.append(capsule(-10, -70, -12, -56, 3.2, 2.6, "#8aa0bf", .9))
    o.append('<circle cx="-12.5" cy="-54" r="2.8" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width=".7"/>')
    # back leg
    o.append(capsule(-2, -54, -7, -28, 5.8, 4.6, "#8aa0bf", .9))
    o.append(capsule(-7, -28, -15, -5, 4.6, 3.6, "#8aa0bf", .9))
    o.append('<path d="M-20 -6 C-18 -9 -12 -8 -10 -5 C-9 -2 -11 0 -14 0 H-21 C-23 -1 -22 -4 -20 -6Z" fill="#6b4a32" stroke="#2a2018" stroke-width=".8"/>')
    # torso
    o.append(f'<path d="M-6 -93 C-1 -95 6 -95 9 -92 C11 -82 10 -66 9 -54 C3 -51 -5 -51 -8 -54 C-9 -66 -9 -82 -6 -93Z" fill="{PJ}" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M-8 -54 C-9 -66 -9 -82 -6 -93 L-3 -92 C-5 -80 -5 -66 -4 -53Z" fill="url(#ink-hatch-l)"/>'
             '<path d="M2 -92 V-56 M1 -84 h2 M1 -76 h2 M1 -68 h2" class="ink2"/>')
    # front leg
    o.append(capsule(2, -55, 8, -29, 6, 4.8, PJ, 1))
    o.append(capsule(8, -29, 11, -5, 4.8, 3.8, PJ, 1))
    o.append('<path d="M7 -6 C9 -9 15 -8 19 -5 C22 -3 22 0 19 0 H8 C6 -1 6 -4 7 -6Z" fill="#7a5236" stroke="#2a2018" stroke-width=".8"/>')
    o.append('<path d="M6 -40 C8 -36 9 -33 9 -30 M10 -20 C10 -16 11 -12 11 -9" class="ink2"/>')
    # head
    o.append(head(2, -103, .18, 6, eye="open", hair="short"))
    # front arm
    o.append(capsule(3, -88, 9, -71, 3.8, 3.3, PJ, 1))
    o.append(capsule(9, -71, 17, -60, 3.3, 2.7, PJ, 1))
    o.append('<circle cx="18.5" cy="-58.5" r="2.9" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width=".7"/>')
    o.append('</g>')
    return "".join(o)


def sitter(x, y, s=1.0):
    """person seated on a chair facing right, eyes closed, hand on belly. origin = seat front/hip level"""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    # chair back + seat
    o.append('<path d="M-22 -62 L-16 -62 L-14 2 L-20 2Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M-22 2 H34 V8 H-22Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M-18 8 V48 M30 8 V48" stroke="#2a2018" stroke-width="3"/>')
    # thigh + shin
    o.append(capsule(-4, -4, 36, -2, 8.5, 7, "#7d8fa8", 1))
    o.append(capsule(36, -2, 40, 40, 6.5, 5, "#7d8fa8", 1))
    o.append('<path d="M34 40 C36 36 44 36 52 40 C55 42 54 46 50 46 H34Z" fill="#6b4a32" stroke="#2a2018" stroke-width=".9"/>')
    # torso
    o.append('<path d="M-12 -60 C-4 -64 8 -64 12 -58 C14 -46 16 -30 18 -14 C16 -4 4 0 -8 -2 C-14 -16 -16 -40 -12 -60Z" fill="#e3c9a8" stroke="#2a2018" stroke-width="1.1"/>'
             '<path d="M-12 -60 C-16 -40 -14 -16 -8 -2 L-3 -2 C-8 -18 -9 -40 -6 -60Z" fill="url(#ink-hatch-l)"/>'
             '<path d="M2 -62 C4 -56 4 -52 2 -48 M0 -40 C6 -38 10 -36 14 -34" class="ink2"/>')
    # head
    o.append(head(2, -82, .27, 0, eye="closed", hair="long"))
    # arm: shoulder -> elbow -> hand on belly
    o.append(capsule(2, -54, -2, -30, 5, 4.4, "#e3c9a8", 1))
    o.append(capsule(-2, -30, 14, -20, 4.4, 3.6, "#e3c9a8", 1))
    o.append(hand(13, -21, .42, -10))
    o.append('</g>')
    return "".join(o)


def card(i, x, y, title, d1, d2, vign):
    w, h = 140, 222
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>',
         f'<rect x="{x+5}" y="{y+5}" width="{w-10}" height="146" rx="3" fill="#efe6d2" stroke="#bfae8a" stroke-width=".8"/>',
         f'<g>{vign}</g>',
         f'<circle cx="{x+16}" cy="{y+170}" r="9.5" fill="{GOLD}" stroke="#2a2018" stroke-width=".8"/>'
         f'<text x="{x+16}" y="{y+174.5}" text-anchor="middle" style="font-size:12px;font-weight:900;fill:#fbf6ea">{i}</text>',
         f'<text x="{x+30}" y="{y+175}" class="lb" style="font-size:15px">{title}</text>',
         f'<text x="{x+8}" y="{y+196}" class="ls">{d1}</text>',
         f'<text x="{x+8}" y="{y+211}" class="ls">{d2}</text>']
    return "".join(o)


CY = 8
xs = [10 + i * 150 for i in range(5)]
V = []
# ① sleep restriction: time bar with window, bed, hourglass
x = xs[0]
v = []
v.append(f'<text x="{x+70}" y="{CY+24}" class="ls" text-anchor="middle">只在這段時間躺床</text>')
bx0, bx1, by = x + 12, x + 128, CY + 34
X1 = lambda t: bx0 + (t - 22) / 10 * (bx1 - bx0)
v.append(f'<rect x="{bx0}" y="{by}" width="{bx1-bx0}" height="14" fill="#cfd6e2" stroke="#2a2018" stroke-width=".8"/>'
         f'<rect x="{X1(24.5):.1f}" y="{by}" width="{X1(30.5)-X1(24.5):.1f}" height="14" fill="#3f6fa6" stroke="#2a2018" stroke-width=".8"/>')
for t, lb in [(22, "22"), (24.5, "00:30"), (30.5, "06:30")]:
    v.append(f'<line x1="{X1(t):.1f}" y1="{by+14}" x2="{X1(t):.1f}" y2="{by+18}" stroke="#2a2018" stroke-width=".7"/>')
v.append(f'<text x="{X1(24.5):.1f}" y="{by+28}" class="ls" text-anchor="middle" style="font-weight:700;fill:{BLUE}">00:30</text>'
         f'<text x="{X1(30.5):.1f}" y="{by+28}" class="ls" text-anchor="middle" style="font-weight:700;fill:{BLUE}">06:30</text>')
v.append(bed_side(x + 12, CY + 140, .8, person=True))
# hourglass (compressed / squeezed)
hx, hy = x + 112, CY + 112
v.append(f'<g transform="translate({hx},{hy})"><path d="M-14 -26 H14 M-14 26 H14" stroke="#7a5236" stroke-width="3.5" stroke-linecap="round"/>'
         '<path d="M-11 -24 C-11 -10 -3 -4 -2 0 C-3 4 -11 10 -11 24 H11 C11 10 3 4 2 0 C3 -4 11 -10 11 -24Z" fill="#eaf1f8" stroke="#2a2018" stroke-width="1"/>'
         '<path d="M-6 -12 C-3 -8 -1 -4 0 -1 C1 -4 3 -8 6 -12Z" fill="#d9b53c"/><path d="M0 0 V14" stroke="#d9b53c" stroke-width="1"/>'
         '<path d="M-10 24 C-8 15 8 15 10 24Z" fill="#d9b53c" stroke="#2a2018" stroke-width=".5"/>'
         '<path d="M-16 -24 V24 M16 -24 V24" stroke="#7a5236" stroke-width="2"/></g>')
v.append(f'<path d="M{hx-26} {hy-10} l6 4 l-6 4 M{hx+26} {hy-10} l-6 4 l6 4" fill="none" stroke="{RED}" stroke-width="1.4"/>')
V.append(card("①", x, CY, "睡眠限制", "縮短躺床時間，", "讓睡意變濃、睡得更紮實", "".join(v)))

# ② stimulus control: bed on left, person walks out to a lit doorway
x = xs[1]
v = []
v.append(bed_side(x + 8, CY + 140, .62, blanket="#e8d6ae"))
v.append(f'<path d="M{x+8} {CY+92} h0" />')
# moved-back blanket corner
v.append(f'<path d="M{x+26} {CY+124} C{x+32} {CY+118} {x+40} {CY+118} {x+44} {CY+124}" class="ink2"/>')
# doorway with warm light
dx = x + 96
v.append(f'<rect x="{dx}" y="{CY+40}" width="34" height="100" fill="#ffe7a6" stroke="#2a2018" stroke-width="1.2"/>'
         f'<path d="M{dx} {CY+140} L{dx-26} {CY+150} L{dx+8} {CY+150} L{dx+34} {CY+140}Z" fill="#ffe7a6" opacity=".7"/>'
         f'<path d="M{dx+34} {CY+40} L{dx+42} {CY+46} V{CY+146} L{dx+34} {CY+140}" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>'
         f'<path d="M{dx+6} {CY+56} H{dx+28} L{dx+24} {CY+70} H{dx+10}Z" fill="#fff6d8" stroke="#2a2018" stroke-width=".6"/>'
         f'<path d="M{dx+12} {CY+90} H{dx+30} V{CY+140} M{dx+12} {CY+90} V{CY+140}" class="ink2"/>')
v.append(walker(x + 80, CY + 144, .92))
v.append(f'<path d="M{x+46} {CY+70} C{x+56} {CY+60} {x+70} {CY+58} {x+82} {CY+60}" fill="none" stroke="{BLUE}" stroke-width="1.3" marker-end="url(#ink-arrow-blue)"/>')
v.append(f'<text x="{x+12}" y="{CY+28}" class="ls">睡不著？先離開床</text>')
V.append(card("②", x, CY, "刺激控制", "睏了才上床，", "睡不著就起床；床只睡覺", "".join(v)))

# ③ relaxation breathing
x = xs[2]
v = []
v.append(sitter(x + 46, CY + 96, .95))
# belly expansion arcs
v.append(f'<path d="M{x+66} {CY+66} C{x+72} {CY+74} {x+72} {CY+84} {x+66} {CY+92} M{x+72} {CY+62} C{x+80} {CY+72} {x+80} {CY+86} {x+72} {CY+96}" fill="none" stroke="{BLUE}" stroke-width="1.2"/>')
# breath out from nose
v.append(f'<path d="M{x+62} {CY+24} c6 -3 10 3 16 0 c6 -3 10 3 16 0 c6 -3 10 3 16 0" fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="3 2"/>')
v.append(f'<text x="{x+134}" y="{CY+48}" class="ls" text-anchor="end" style="fill:{BLUE}">吸 4 秒</text>'
         f'<text x="{x+134}" y="{CY+64}" class="ls" text-anchor="end" style="fill:{BLUE}">吐 6 秒</text>')
V.append(card("③", x, CY, "放鬆訓練", "慢慢腹式呼吸，", "放鬆肌肉、鬆開油門", "".join(v)))

# ④ cognitive restructuring
x = xs[3]
v = []
v.append(head(x + 30, CY + 112, .4, 0, eye="open", hair="grey", age="old"))
v.append(f'<path d="M{x+30} {CY+128} C{x+20} {CY+134} {x+12} {CY+140} {x+8} {CY+151} H{x+60} C{x+56} {CY+142} {x+48} {CY+134} {x+40} {CY+132}Z" fill="#b8c4a0" stroke="#2a2018" stroke-width="1"/>')
v.append(f'<rect x="{x+12}" y="{CY+14}" width="116" height="28" rx="12" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/>'
         f'<text x="{x+70}" y="{CY+32}" class="ls" text-anchor="middle" style="font-weight:700">今晚一定又睡不著</text>'
         f'<path d="M{x+18} {CY+38} L{x+122} {CY+18}" stroke="{RED}" stroke-width="2"/>')
v.append(f'<path d="M{x+70} {CY+44} V{CY+56}" stroke="#2a2018" stroke-width="1.3" marker-end="url(#ink-arrow)"/>')
v.append(f'<rect x="{x+12}" y="{CY+60}" width="116" height="42" rx="12" fill="#e3ecf7" stroke="{BLUE}" stroke-width="1.1"/>'
         f'<text x="{x+70}" y="{CY+77}" class="ls" text-anchor="middle" style="fill:{BLUE};font-weight:700">就算睡少一點，</text>'
         f'<text x="{x+70}" y="{CY+93}" class="ls" text-anchor="middle" style="fill:{BLUE};font-weight:700">明天還是過得去</text>')
for k, (cx, cy, r) in enumerate([(x + 60, CY + 106, 2), (x + 66, CY + 112, 2.8)]):
    pass
v.append(f'<circle cx="{x+58}" cy="{CY+108}" r="2.4" fill="#e3ecf7" stroke="{BLUE}" stroke-width=".8"/><circle cx="{x+52}" cy="{CY+114}" r="1.7" fill="#e3ecf7" stroke="{BLUE}" stroke-width=".8"/>')
V.append(card("④", x, CY, "認知調整", "換個想法，", "減少對失眠的害怕與擔心", "".join(v)))

# ⑤ sleep hygiene: coffee after 14:00 crossed, dim lamp, regular alarm
x = xs[4]
v = []
cx0, cy0 = x + 36, CY + 58
v.append(f'<g transform="translate({cx0},{cy0})">'
         '<path d="M-16 -14 H14 L11 14 C10 18 -12 18 -13 14Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1.1"/>'
         '<path d="M-14 -10 H12" stroke="#6b4a32" stroke-width="3"/>'
         '<path d="M14 -8 C24 -8 24 6 12 6" fill="none" stroke="#2a2018" stroke-width="1.6"/>'
         '<path d="M-24 18 H22" stroke="#2a2018" stroke-width="1.2"/>'
         '<path d="M-8 -20 c-3 -4 3 -6 0 -10 M0 -20 c-3 -4 3 -6 0 -10" fill="none" stroke="#8a6a3a" stroke-width=".8"/></g>')
v.append(f'<path d="M{cx0-24} {cy0-30} L{cx0+24} {cy0+20} M{cx0+24} {cy0-30} L{cx0-24} {cy0+20}" stroke="{RED}" stroke-width="2.4" opacity=".85"/>')
v.append(f'<text x="{cx0}" y="{CY+96}" class="ls" text-anchor="middle" style="fill:{RED};font-weight:700">14:00 後</text>')
# dim lamp
lx, ly = x + 104, CY + 70
v.append(f'<radialGradient id="{PID}-lg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd98a" stop-opacity=".7"/><stop offset="1" stop-color="#ffd98a" stop-opacity="0"/></radialGradient>'
         f'<circle cx="{lx}" cy="{ly-8}" r="26" fill="url(#{PID}-lg)"/>'
         f'<path d="M{lx-14} {ly} H{lx+14} L{lx+8} {ly-22} H{lx-8}Z" fill="#f6e2b0" stroke="#2a2018" stroke-width="1"/>'
         f'<path d="M{lx} {ly} V{ly+22} M{lx-10} {ly+24} H{lx+10}" stroke="#2a2018" stroke-width="1.8"/>'
         f'<path d="M{lx-4} {ly} L{lx-2} {ly-22} M{lx+3} {ly} L{lx+2} {ly-22}" class="ink2"/>')
v.append(f'<text x="{lx}" y="{CY+110}" class="ls" text-anchor="middle">燈光調暗</text>')
# alarm clock
ax, ay = x + 44, CY + 126
v.append(f'<path d="M{ax-20} {ay-18} a8 8 0 0 1 10 -8 M{ax+20} {ay-18} a8 8 0 0 0 -10 -8" fill="#c9962e" stroke="#2a2018" stroke-width="1"/>'
         f'<path d="M{ax-12} {ay+16} l-4 5 M{ax+12} {ay+16} l4 5" stroke="#2a2018" stroke-width="1.6"/>')
v.append(clock(ax, ay, 15, 7, 0))
v.append(f'<text x="{ax+24}" y="{ay+2}" class="ls" style="font-weight:700">每天</text><text x="{ax+24}" y="{ay+16}" class="ls" style="font-weight:700">同時起床</text>')
V.append(card("⑤", x, CY, "睡眠衛生", "下午後不喝咖啡，", "燈光調暗、固定起床時間", "".join(v)))

# ===== toolbox (carpenter's tote) =====
T = []
FY, BY_ = 392, 492   # front board top / bottom
L0, R0, DX, DY = 196, 556, 34, -26
wood, wood2, wood3 = "#c08a55", "#a87443", "#8c5f36"
# left end board (inner face visible)
T.append(f'<path d="M{L0} {BY_} V{FY} L{L0+DX/2} {FY-74} L{L0+DX} {FY+DY} V{BY_+DY}Z" fill="{wood2}" stroke="#2a2018" stroke-width="1.3"/>'
         f'<path d="M{L0} {BY_} V{FY} L{L0+DX/2} {FY-74} L{L0+DX} {FY+DY} V{BY_+DY}Z" fill="url(#ink-hatch)" opacity=".7"/>')
# back board (inner face)
T.append(f'<path d="M{L0+DX} {FY+DY} H{R0+DX} V{FY+DY+40} H{L0+DX}Z" fill="{wood3}" stroke="#2a2018" stroke-width="1.1"/>'
         f'<path d="M{L0+DX} {FY+DY} H{R0+DX} V{FY+DY+40} H{L0+DX}Z" fill="url(#ink-hatch-d)" opacity=".6"/>')
# interior floor shadow
T.append(f'<path d="M{L0} {FY} L{L0+DX} {FY+DY} H{R0+DX} L{R0} {FY}Z" fill="#5a3d24"/>')
# tools sticking out (behind front board): positions and a tag per tool
tools = []
# hammer
tools.append(f'<path d="M248 {FY+6} L262 {FY-74}" stroke="#a87443" stroke-width="7" stroke-linecap="round"/><path d="M248 {FY+6} L262 {FY-74}" stroke="#2a2018" stroke-width="7.8" stroke-linecap="round" opacity=".0"/>'
             f'<path d="M244 {FY-82} L284 {FY-74} L282 {FY-64} L262 {FY-66} L246 {FY-72}Z" fill="#8e8a84" stroke="#2a2018" stroke-width="1.1"/><path d="M244 {FY-82} C238 {FY-86} 236 {FY-80} 240 {FY-76} L246 {FY-72}" fill="#8e8a84" stroke="#2a2018" stroke-width="1"/>')
# screwdriver
tools.append(f'<path d="M318 {FY+4} L322 {FY-50}" stroke="#9a958c" stroke-width="3"/><path d="M316 {FY-48} L326 {FY-48} L328 {FY-96} C328 {FY-102} 316 {FY-102} 316 {FY-96}Z" fill="#c9473a" stroke="#2a2018" stroke-width="1"/>'
             f'<path d="M319 {FY-56} V{FY-92} M323 {FY-56} V{FY-92}" class="ink2"/>')
# wrench
tools.append(f'<path d="M382 {FY+4} L396 {FY-70}" stroke="#9a958c" stroke-width="8" stroke-linecap="round"/><path d="M382 {FY+4} L396 {FY-70}" stroke="#2a2018" stroke-width=".8" fill="none"/>'
             f'<path d="M386 {FY-66} C380 {FY-80} 388 {FY-94} 400 {FY-92} L398 {FY-84} L404 {FY-80} L410 {FY-86} C414 {FY-74} 404 {FY-62} 396 {FY-66}Z" fill="#b4afa6" stroke="#2a2018" stroke-width="1.1"/>')
# folding ruler
tools.append(f'<path d="M444 {FY+4} L450 {FY-86} L460 {FY-86} L456 {FY+4}Z" fill="#e8cf7a" stroke="#2a2018" stroke-width="1"/>'
             + "".join(f'<path d="M{446+0.07*k*10:.1f} {FY-80+k*10} h5" stroke="#2a2018" stroke-width=".6"/>' for k in range(8)))
# paintbrush
tools.append(f'<path d="M510 {FY+4} L502 {FY-54}" stroke="#a87443" stroke-width="6" stroke-linecap="round"/><path d="M496 {FY-54} L508 {FY-56} L508 {FY-66} L496 {FY-64}Z" fill="#9a958c" stroke="#2a2018" stroke-width=".9"/>'
             f'<path d="M496 {FY-64} C494 {FY-76} 498 {FY-84} 502 {FY-88} C506 {FY-84} 510 {FY-76} 508 {FY-66}Z" fill="#d9b53c" stroke="#2a2018" stroke-width=".9"/>')
T.append('<g transform="translate(0,-26)">' + ''.join(tools) + '</g>')
# handle dowel between end peaks
T.append(f'<path d="M{L0+DX/2} {FY-70} H{R0+DX/2}" stroke="#2a2018" stroke-width="13" stroke-linecap="round"/>'
         f'<path d="M{L0+DX/2} {FY-70} H{R0+DX/2}" stroke="#d9a670" stroke-width="10.5" stroke-linecap="round"/>'
         f'<path d="M{L0+DX/2} {FY-73} H{R0+DX/2}" stroke="#f0cfa0" stroke-width="2" opacity=".8"/>')
# front board
T.append(f'<path d="M{L0} {FY} H{R0} V{BY_} H{L0}Z" fill="{wood}" stroke="#2a2018" stroke-width="1.6"/>')
for k in range(9):
    yy = FY + 10 + k * 10
    amp = 2 + (k % 3)
    T.append(f'<path d="M{L0+4} {yy} C{L0+90} {yy-amp} {L0+170} {yy+amp} {L0+250} {yy-1} S{R0-30} {yy+amp} {R0-4} {yy}" fill="none" stroke="#7a5230" stroke-width=".6" opacity=".7"/>')
T.append(f'<ellipse cx="{L0+120}" cy="{FY+52}" rx="12" ry="5" fill="none" stroke="#7a5230" stroke-width=".7"/><ellipse cx="{L0+120}" cy="{FY+52}" rx="6" ry="2.4" fill="none" stroke="#7a5230" stroke-width=".6"/>')
T.append(f'<path d="M{L0} {BY_-16} H{R0} V{BY_} H{L0}Z" fill="url(#ink-hatch)" opacity=".7"/>')
# right end board (outer face)
T.append(f'<path d="M{R0} {BY_} V{FY} L{R0+DX/2} {FY-74} L{R0+DX} {FY+DY} V{BY_+DY}Z" fill="{wood2}" stroke="#2a2018" stroke-width="1.5"/>'
         f'<path d="M{R0+DX*0.55} {BY_+DY*0.55} V{FY-30} L{R0+DX/2} {FY-74} L{R0+DX} {FY+DY} V{BY_+DY}Z" fill="url(#ink-hatch-d)" opacity=".75"/>'
         f'<circle cx="{R0+DX/2}" cy="{FY-70}" r="6.5" fill="#d9a670" stroke="#2a2018" stroke-width="1"/>')
# metal corner brackets + nails
for cx_ in (L0 + 2, R0 - 18):
    T.append(f'<rect x="{cx_}" y="{BY_-18}" width="16" height="16" fill="#8e8a84" stroke="#2a2018" stroke-width=".9"/><circle cx="{cx_+5}" cy="{BY_-13}" r="1.3" fill="#2a2018"/><circle cx="{cx_+11}" cy="{BY_-7}" r="1.3" fill="#2a2018"/>'
             f'<rect x="{cx_}" y="{FY+2}" width="16" height="16" fill="#8e8a84" stroke="#2a2018" stroke-width=".9"/><circle cx="{cx_+5}" cy="{FY+7}" r="1.3" fill="#2a2018"/><circle cx="{cx_+11}" cy="{FY+13}" r="1.3" fill="#2a2018"/>')
# brass name plate on front
T.append(f'<rect x="{(L0+R0)/2-92}" y="{FY+32}" width="184" height="34" rx="3" fill="#e2c46e" stroke="#2a2018" stroke-width="1"/>'
         f'<rect x="{(L0+R0)/2-88}" y="{FY+36}" width="176" height="26" rx="2" fill="none" stroke="#8a6a3a" stroke-width=".6"/>'
         f'<text x="{(L0+R0)/2}" y="{FY+55}" text-anchor="middle" class="lb" style="font-size:14px">CBT-I 工具箱</text>')
# shadow under box
T.append(f'<ellipse cx="{(L0+R0)/2+20}" cy="{BY_+4}" rx="210" ry="8" fill="#2a2018" opacity=".12"/>')

# strings from card bottoms to tool tips with small tags
tips = [(262, FY - 104), (322, FY - 126), (398, FY - 120), (455, FY - 114), (502, FY - 114)]
S_ = []
for i, (tx, ty) in enumerate(tips):
    cx_ = xs[i] + 70
    S_.append(f'<path d="M{cx_} {CY+222} C{cx_} {CY+262} {tx} {ty-60} {tx} {ty-14}" fill="none" stroke="#8a6a3a" stroke-width="1" stroke-dasharray="1 2.5"/>')
    S_.append(f'<g transform="translate({tx},{ty-14}) rotate({-8 + i*4})"><path d="M-9 -6 H9 V8 L0 13 L-9 8Z" fill="#efdcae" stroke="#2a2018" stroke-width=".8"/>'
              f'<text x="0" y="5.5" text-anchor="middle" style="font-size:10px;font-weight:900;fill:#2a2018">{"①②③④⑤"[i]}</text></g>')

# ===== sleep diary notebook (right)
N = []
nx, ny = 618, 394
N.append(f'<g transform="translate({nx},{ny}) rotate(-6)">'
         '<path d="M0 0 H62 V84 H0Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
         '<path d="M62 0 H124 V84 H62Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
         '<path d="M-4 -3 H128 V88 H-4Z" fill="none" stroke="#3f6fa6" stroke-width="3" opacity=".8"/>'
         '<path d="M62 0 V84" stroke="#2a2018" stroke-width="1.2"/>')
for r in range(7):
    yy = 16 + r * 9.5
    N.append(f'<path d="M6 {yy} H56 M68 {yy} H118" stroke="#8a9bb3" stroke-width=".5"/>')
    a = 8 + (r * 7) % 14
    N.append(f'<rect x="{68+a}" y="{yy-6}" width="{26 - (r%3)*4}" height="4" fill="#3f6fa6" opacity=".8"/>')
    N.append(f'<path d="M8 {yy-2} h{6 + r%3*3}" stroke="#2a2018" stroke-width=".7"/>')
N.append('<path d="M10 8 H44" stroke="#2a2018" stroke-width="1.2"/><path d="M72 8 H112" stroke="#2a2018" stroke-width="1.2"/>')
N.append('</g>')
N.append(f'<g transform="translate({nx+110},{ny+66}) rotate(-40)"><path d="M0 0 H54 L62 3 L54 6 H0Z" fill="#d9b53c" stroke="#2a2018" stroke-width=".8"/><path d="M54 0 L62 3 L54 6Z" fill="#efd9b0" stroke="#2a2018" stroke-width=".6"/><path d="M-6 0 H0 V6 H-6Z" fill="#e7a3a3" stroke="#2a2018" stroke-width=".6"/></g>')
N.append(f'<text x="{nx+6}" y="{ny+112}" class="lb" style="font-size:14px">睡眠日誌</text>'
         f'<text x="{nx+6}" y="{ny+128}" class="ls">每天記下上床、睡著、</text><text x="{nx+6}" y="{ny+142}" class="ls">醒來時間，治療的依據</text>')

# ===== guideline badge (left)
G = []
gx, gy = 96, 420
G.append(f'<path d="M{gx-22} {gy+22} L{gx-30} {gy+62} L{gx-14} {gy+54} L{gx-6} {gy+68} L{gx} {gy+28}Z" fill="{RED}" stroke="#2a2018" stroke-width=".9"/>'
         f'<path d="M{gx+22} {gy+22} L{gx+30} {gy+62} L{gx+14} {gy+54} L{gx+6} {gy+68} L{gx} {gy+28}Z" fill="#8f3524" stroke="#2a2018" stroke-width=".9"/>')
pts = []
for k in range(32):
    r = 34 if k % 2 == 0 else 30
    a = math.pi * 2 * k / 32
    pts.append(f"{gx + r*math.cos(a):.1f} {gy + r*math.sin(a):.1f}")
G.append(f'<path d="M{" L".join(pts)}Z" fill="{GOLD}" stroke="#2a2018" stroke-width="1"/>'
         f'<circle cx="{gx}" cy="{gy}" r="25" fill="#f2d98a" stroke="#2a2018" stroke-width=".8"/>'
         f'<text x="{gx}" y="{gy-3}" text-anchor="middle" class="lb" style="font-size:13px">第一線</text>'
         f'<text x="{gx}" y="{gy+12}" text-anchor="middle" class="ls" style="font-weight:700">治療</text>')
G.append(f'<text x="10" y="{gy-96}" class="lb" style="font-size:14px">各國指引都把 CBT-I</text>'
         f'<text x="10" y="{gy-79}" class="lb" style="font-size:14px">列為慢性失眠的</text>'
         f'<text x="10" y="{gy-62}" class="lb" style="font-size:14px;fill:{RED}">第一線治療</text>')
G.append(f'<text x="10" y="{gy+88}" class="ls">通常每週 1 次、約 4–8 次</text>')

body = "\n".join(["".join(V), "".join(S_), "".join(T), "".join(N), "".join(G)])
cap = ('<b>圖 6·A　失眠認知行為治療 CBT-I 的工具箱。</b>CBT-I 不是單一招式，而是一組搭配使用的工具：睡眠限制、刺激控制、放鬆訓練、認知調整與睡眠衛生，'
       '再加上每天的睡眠日誌，由專業人員依你的狀況逐週調整。各國臨床指引都把它列為慢性失眠的第一線治療；'
       '睡眠限制等步驟最好在醫師或心理師指導下進行。示意圖，時間僅為舉例。')
html = fig(PID, "圖 6·A", "失眠認知行為治療 CBT-I 的工具箱", "The CBT-I toolbox", 562,
           "五張小卡分別描繪睡眠限制（縮短的躺床時段與沙漏）、刺激控制（睡不著起身走向另一個亮燈的房間）、放鬆訓練（坐著做腹式呼吸）、認知調整（把『今晚一定又睡不著』劃掉改成『就算睡少一點，明天還是過得去』）、睡眠衛生（下午不喝咖啡、調暗燈光、固定起床）；下方為木製工具箱、睡眠日誌與第一線治療徽章",
           body, cap)
write(PID, html)
print(len(html))
