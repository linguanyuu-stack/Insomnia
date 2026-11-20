import sys, math
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from pplib import *

PID = "pp-redflags"
RED, BLUE = "#a8412c", "#2c5d9c"
CW, VH = 240, 168


def room(bg="#c9d3e3", floor="#9aa6b6", fy=VH - 14, hatch=.5):
    return (f'<rect x="0" y="0" width="{CW}" height="{VH}" fill="{bg}"/><rect x="0" y="0" width="{CW}" height="{VH}" fill="url(#ink-hatch-h)" opacity="{hatch}"/>'
            f'<path d="M0 {fy} H{CW} V{VH} H0Z" fill="{floor}"/><path d="M0 {fy} H{CW} V{VH} H0Z" fill="url(#ink-hatch-l)"/><path d="M0 {fy} H{CW}" class="ink"/>')


def edge_sitter(x, y, s=1.0, pose="despair", shirt="#b9c3d6", pants="#6e7d96", hair="short"):
    """person sitting on the edge of a bed, facing right. origin = hip on mattress edge"""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    # back arm (behind body)
    if pose == "despair":
        o.append(capsule(12, -42, 30, -14, 4.6, 4, shirt, .9, ' opacity=".9"'))
        o.append(capsule(30, -14, 40, -40, 4, 3.4, shirt, .9))
    # legs
    o.append(capsule(0, -4, 40, -4, 8.5, 7, pants, 1))
    if pose == "rub":
        o.append(capsule(40, -4, 52, 34, 6.6, 5, pants, 1))
        o.append('<path d="M47 33 C50 29 60 30 66 35 C68 38 66 41 62 41 H48 C46 39 46 36 47 33Z" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width=".9"/>')
    else:
        o.append(capsule(40, -4, 42, 36, 6.6, 5, pants, 1))
        o.append('<path d="M38 36 C40 32 50 33 56 37 C58 40 56 43 52 43 H38 C36 41 36 38 38 36Z" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width=".9"/>')
    o.append('<path d="M6 -8 C16 -6 26 -6 36 -8" class="ink2"/>')
    # torso leaning forward
    o.append(f'<path d="M-10 -2 C-14 -18 -8 -38 4 -52 C10 -56 20 -56 26 -50 C26 -38 22 -22 16 -4 C8 2 -4 2 -10 -2Z" fill="{shirt}" stroke="#2a2018" stroke-width="1.1"/>'
             '<path d="M-10 -2 C-14 -18 -8 -38 4 -52 L8 -50 C0 -36 -4 -18 -3 0Z" fill="url(#ink-hatch-l)"/>'
             '<path d="M10 -30 C14 -26 16 -20 16 -14 M0 -20 C4 -16 6 -10 6 -4" class="ink2"/>')
    if pose == "despair":
        o.append(head(33, -62, .3, 42, eye="closed", hair=hair))
        o.append(capsule(16, -44, 34, -12, 4.8, 4.2, shirt, 1))
        o.append(capsule(34, -12, 44, -42, 4.2, 3.6, shirt, 1))
        o.append(hand(44, -42, .5, -100))
    else:  # rub calf, looking down at legs
        o.append(head(30, -64, .3, 28, eye="open", hair=hair))
        o.append(capsule(16, -44, 34, -18, 4.8, 4.2, shirt, 1))
        o.append(capsule(34, -18, 46, 12, 4.2, 3.6, shirt, 1))
        o.append(hand(46, 12, .5, 70))
    o.append('</g>')
    return "".join(o)


def cell(i, gx, gy, vign, title, hint, hint_col="#5d4b38"):
    o = [f'<g transform="translate({gx},{gy})">',
         f'<defs><clipPath id="{PID}-c{i}"><rect x="0" y="0" width="{CW}" height="{VH}" rx="4"/></clipPath></defs>',
         f'<g clip-path="url(#{PID}-c{i})">{vign}</g>',
         f'<rect x="0" y="0" width="{CW}" height="{VH}" rx="4" fill="none" stroke="#2a2018" stroke-width="1.2"/>',
         # red flag icon
         f'<path d="M4 {VH+8} V{VH+30}" stroke="#2a2018" stroke-width="1.4"/><path d="M4.5 {VH+9} C9 {VH+6} 13 {VH+12} 19 {VH+9} V{VH+19} C13 {VH+22} 9 {VH+16} 4.5 {VH+19}Z" fill="#c9473a" stroke="#2a2018" stroke-width=".7"/>',
         f'<text x="24" y="{VH+21}" class="lb" style="font-size:14.5px">{title}</text>',
         f'<text x="24" y="{VH+39}" class="ls" style="fill:{hint_col}">{hint}</text>',
         '</g>']
    return "".join(o)


cells = []
# ---------- 1. snoring / apnoea, bed partner watching
v = [room()]
v.append(window(186, 14, 40, 46))
v.append(bed_lying(CW, 0, VH - 14, eye="closed", shirt="#cfdcef", hx=52, hair="short", head_s=.44, mouth="open"))
# partner sitting up on elbow behind, looking at sleeper (faces left)
v.append(f'<path d="M110 {VH-62} C112 {VH-88} 120 {VH-100} 134 {VH-102} C148 {VH-102} 156 {VH-92} 158 {VH-70} L160 {VH-56} L112 {VH-56}Z" fill="#e3c9d6" stroke="#2a2018" stroke-width="1"/>'
         f'<path d="M150 {VH-96} C156 {VH-86} 158 {VH-74} 158 {VH-62} L152 {VH-58} C152 {VH-72} 150 {VH-84} 146 {VH-94}Z" fill="url(#ink-hatch-l)"/>')
v.append(head(134, VH - 118, .36, -12, eye="wide", hair="long", flip=True))
# arm propping
v.append(capsule(118, VH - 92, 104, VH - 66, 4.6, 4, "#e3c9d6", 1))
v.append(capsule(104, VH - 66, 92, VH - 54, 4, 3.4, "#e3c9d6", 1))
# re-draw blanket front edge over partner hips
v.append(f'<path d="M96 {VH-58} C120 {VH-64} 150 {VH-62} 180 {VH-60} C200 {VH-60} 220 {VH-62} {CW} {VH-60} L{CW} {VH-26} L96 {VH-26}Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.1"/>'
         f'<path d="M140 {VH-62} C142 {VH-50} 138 {VH-38} 142 {VH-27} M196 {VH-60} C194 {VH-48} 198 {VH-36} 194 {VH-27}" class="ink2"/>')
# snore marks + pause
v.append(f'<path d="M48 {VH-108} l6 -5 l6 5 l6 -5 l6 5 M44 {VH-122} l7 -6 l7 6 l7 -6 l7 6" fill="none" stroke="#3f6fa6" stroke-width="1.6" stroke-linejoin="round"/>')
v.append(f'<rect x="20" y="10" width="92" height="24" rx="10" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/>'
         f'<path d="M98 34 L106 46 L90 34" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/><path d="M91 33.5 H97" stroke="#fbf6ea" stroke-width="2"/>'
         f'<text x="66" y="27" class="ls" text-anchor="middle" style="font-weight:700;fill:{RED}">呼吸…停了？</text>')
cells.append((v, "大聲打鼾、睡眠中停止呼吸", "可能是睡眠呼吸中止症"))

# ---------- 2. dozing at the wheel
v = []
v.append(f'<rect x="0" y="0" width="{CW}" height="{VH}" fill="#d8e3ec"/>')
# road through windscreen
v.append(f'<path d="M120 0 H{CW} V92 H120Z" fill="#cfe0ee"/><path d="M120 70 C170 66 200 66 {CW} 68 V92 H120Z" fill="#9fb39a"/>'
         f'<path d="M150 92 L196 66 L206 66 L188 92Z" fill="#8e8a84"/><path d="M190 70 l-4 4 M182 80 l-5 5" stroke="#fbf6ea" stroke-width="1.4"/>'
         f'<path d="M120 64 C140 60 160 56 176 58 C184 50 200 50 208 56 C220 54 232 56 {CW} 58" fill="none" stroke="#7d9a7a" stroke-width="1"/>')
# car body interior: roof, A-pillar, door, dashboard
v.append(f'<path d="M0 0 H{CW} V12 C180 14 140 20 112 30 L100 26 C60 18 30 14 0 14Z" fill="#5d564e" stroke="#2a2018" stroke-width="1.1"/>')
v.append(f'<path d="M112 30 L150 96 L140 98 L102 30Z" fill="#6a625a" stroke="#2a2018" stroke-width="1.1"/>')
v.append(f'<path d="M140 96 C170 88 210 88 {CW} 90 V128 H150 C142 118 138 106 140 96Z" fill="#45403a" stroke="#2a2018" stroke-width="1.2"/>'
         f'<path d="M140 96 C170 88 210 88 {CW} 90 V100 C210 98 170 100 142 106Z" fill="url(#ink-hatch-d)" opacity=".8"/>')
v.append(f'<path d="M0 108 H150 L170 {VH} H0Z" fill="#6e665c"/><path d="M0 108 H150 L170 {VH} H0Z" fill="url(#ink-hatch-r)" opacity=".5"/>')
# seat
v.append(f'<path d="M30 40 C24 40 20 46 22 56 L34 128 L46 128 L40 56 C40 46 36 40 30 40Z" fill="#3e4656" stroke="#2a2018" stroke-width="1.1"/>'
         f'<path d="M30 126 H110 C116 126 116 138 110 138 H34Z" fill="#3e4656" stroke="#2a2018" stroke-width="1.1"/>'
         f'<path d="M24 26 C22 18 36 16 38 24 L40 40 L28 42Z" fill="#3e4656" stroke="#2a2018" stroke-width="1"/>')
# driver: legs
v.append(capsule(50, 120, 112, 118, 9, 8, "#4d5a6e", 1))
v.append(capsule(112, 118, 128, 154, 7, 5.5, "#4d5a6e", 1))
v.append(f'<path d="M122 152 C126 148 138 150 146 154 C148 158 144 160 140 160 H124Z" fill="#3a2a1c" stroke="#2a2018" stroke-width=".8"/>')
# torso
v.append(f'<path d="M40 64 C46 58 62 58 70 64 C76 84 78 104 74 124 C64 130 50 130 42 124 C36 104 36 84 40 64Z" fill="#e6e1d6" stroke="#2a2018" stroke-width="1.1"/>'
         f'<path d="M40 64 C36 84 36 104 42 124 L48 124 C44 104 44 84 46 64Z" fill="url(#ink-hatch-l)"/>'
         f'<path d="M54 62 L60 72 L66 62" stroke="#2a2018" stroke-width="1" fill="none"/><path d="M60 74 V122" class="ink2"/>')
# head drooping forward, eyes closed
v.append(head(62, 40, .36, 34, eye="closed", hair="short"))
# arms to wheel
v.append(capsule(60, 70, 82, 100, 5.8, 5, "#e6e1d6", 1))
v.append(capsule(82, 100, 118, 90, 5, 4.2, "#e6e1d6", 1))
v.append(hand(116, 90, .5, -12))
# steering wheel (side, ellipse) + column
v.append(f'<path d="M132 104 L150 112" stroke="#2a2018" stroke-width="6"/>'
         f'<ellipse cx="128" cy="86" rx="7" ry="28" transform="rotate(-22 128 86)" fill="none" stroke="#2a2018" stroke-width="5"/>'
         f'<ellipse cx="128" cy="86" rx="7" ry="28" transform="rotate(-22 128 86)" fill="none" stroke="#5d564e" stroke-width="2.6"/>')
v.append(f'<text x="94" y="30" class="lt" style="fill:{BLUE}">z</text><text x="104" y="22" class="lt" style="fill:{BLUE};font-size:18px">Z</text>')
cells.append((v, "開車或開會時打瞌睡", "白天嚴重嗜睡，可能不只是失眠"))

# ---------- 3. restless legs: sitting on bed edge rubbing calf
v = [room("#c3cde0", "#8f9bad")]
v.append(window(160, 14, 52, 50))
# bed (side) on left
v.append(f'<path d="M0 {VH-14} V{VH-110} C0 {VH-118} 18 {VH-120} 20 {VH-112} V{VH-14}Z" fill="#a57c55" stroke="#2a2018" stroke-width="1.2"/>'
         f'<path d="M0 {VH-64} H104 V{VH-40} H0Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/>'
         f'<path d="M0 {VH-40} H104 V{VH-32} H0Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/><path d="M98 {VH-32} V{VH-14}" stroke="#2a2018" stroke-width="3"/>'
         f'<path d="M14 {VH-66} C30 {VH-80} 52 {VH-78} 70 {VH-70} C64 {VH-62} 40 {VH-60} 14 {VH-62}Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1"/>')
v.append(edge_sitter(84, VH - 66, 1.05, pose="rub", shirt="#cfdcef", pants="#cfdcef", hair="grey"))
# tingling marks on the shin + motion arcs
v.append(f'<path d="M128 {VH-60} c3 -3 5 3 8 0 c3 -3 5 3 8 0 M132 {VH-48} c3 -3 5 3 8 0 c3 -3 5 3 8 0 M140 {VH-36} c3 -3 5 3 8 0 c3 -3 5 3 8 0" fill="none" stroke="#e0413a" stroke-width="1.3"/>')
v.append(f'<path d="M158 {VH-26} C164 {VH-30} 166 {VH-20} 160 {VH-14} M166 {VH-32} C176 {VH-30} 178 {VH-16} 168 {VH-10}" fill="none" stroke="#2a2018" stroke-width="1"/>')
v.append(f'<text x="160" y="{VH-82}" class="ls halo" style="fill:{RED};font-weight:700">又酸又麻</text><text x="160" y="{VH-68}" class="ls halo" style="fill:{RED};font-weight:700">動一動才好</text>')
cells.append((v, "晚上腿很不舒服、一定要動", "可能是不寧腿症候群"))

# ---------- 4. REM sleep behaviour disorder: punching / kicking in sleep
v = [room()]
# nightstand + toppling lamp
v.append(f'<path d="M196 {VH-14} V{VH-70} H{CW} V{VH-14}" fill="#a57c55" stroke="#2a2018" stroke-width="1.1"/>'
         f'<g transform="rotate(28 214 {VH-72})"><path d="M206 {VH-72} h16 M214 {VH-72} V{VH-100}" stroke="#2a2018" stroke-width="2"/><path d="M202 {VH-100} H226 L220 {VH-120} H208Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1"/></g>'
         f'<path d="M196 {VH-110} l-6 -6 M204 {VH-118} l-2 -8 M232 {VH-118} l4 -6" stroke="#2a2018" stroke-width="1.2"/>')
v.append(bed_lying(190, 0, VH - 14, eye="closed", shirt="#cfdcef", hx=50, hair="grey", head_s=.44, blanket="#e0cfa4"))
# punching arm thrust upward-right + fist
v.append(capsule(76, VH - 74, 96, VH - 104, 5.2, 4.6, "#cfdcef", 1))
v.append(capsule(96, VH - 104, 124, VH - 118, 4.6, 4, "#cfdcef", 1))
v.append(fist(124, VH - 118, .62, -24))
v.append(f'<path d="M140 {VH-136} l10 -8 M144 {VH-124} l12 -2 M142 {VH-112} l11 4" stroke="#2a2018" stroke-width="1.3"/>')
# kicking foot out from under blanket at the foot end
v.append(capsule(188, VH - 44, 206, VH - 60, 5.4, 4.6, "#cfdcef", 1))
v.append(f'<path d="M203 {VH-58} C201 {VH-66} 204 {VH-76} 210 {VH-78} C214 {VH-78} 216 {VH-74} 214 {VH-68} C213 {VH-62} 211 {VH-58} 208 {VH-56}Z" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width=".9"/>'
         f'<path d="M184 {VH-70} c4 -4 10 -4 14 -2 M180 {VH-60} c3 -3 8 -3 11 -1" fill="none" stroke="#2a2018" stroke-width="1"/>')
# dream bubble: running away
v.append(bubble(40, 30, 32, 22, tail=(54, VH - 98), seed=.3))
v.append(f'<text x="40" y="35" class="ls" text-anchor="middle" style="font-weight:700">（夢裡打架）</text>')
cells.append((v, "睡覺時把夢演出來、揮拳踢人", "可能是快速動眼期睡眠行為障礙"))

# ---------- 5. low mood, thoughts of self-harm (handled gently)
v = [room("#aeb8cc", "#7f8a9d", hatch=.6)]
v.append(f'<radialGradient id="{PID}-soft" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff2c4" stop-opacity=".55"/><stop offset="1" stop-color="#fff2c4" stop-opacity="0"/></radialGradient>')
v.append(window(170, 18, 50, 54, moon=True, sky="#2e3d5c"))
v.append(f'<ellipse cx="160" cy="{VH-40}" rx="70" ry="30" fill="url(#{PID}-soft)"/>')
v.append(f'<path d="M0 {VH-14} V{VH-110} C0 {VH-118} 18 {VH-120} 20 {VH-112} V{VH-14}Z" fill="#8f6a48" stroke="#2a2018" stroke-width="1.2"/>'
         f'<path d="M0 {VH-64} H112 V{VH-40} H0Z" fill="#e8e2d4" stroke="#2a2018" stroke-width="1"/>'
         f'<path d="M0 {VH-40} H112 V{VH-32} H0Z" fill="#8f6a48" stroke="#2a2018" stroke-width="1"/><path d="M104 {VH-32} V{VH-14}" stroke="#2a2018" stroke-width="3"/>'
         f'<path d="M12 {VH-66} C30 {VH-82} 56 {VH-80} 76 {VH-70} C70 {VH-62} 40 {VH-60} 12 {VH-62}Z" fill="#c9bfa8" stroke="#2a2018" stroke-width="1"/>')
v.append(edge_sitter(92, VH - 66, 1.05, pose="despair", shirt="#9aa7bd", pants="#5f6b80", hair="long"))
# a phone on the bed, glowing softly, suggesting reaching out
v.append(f'<rect x="38" y="{VH-72}" width="22" height="9" rx="2" fill="#2a2f36" stroke="#2a2018" stroke-width=".8" transform="rotate(-6 49 {VH-68})"/><rect x="40" y="{VH-71}" width="18" height="6" rx="1" fill="#e6f1ff" transform="rotate(-6 49 {VH-68})"/>')
cells.append((v, "情緒低落、想傷害自己", "請馬上找人談：安心專線 1925（24 小時）", RED))

# ---------- 6. long-term sleeping pills, wanting to stop
v = [f'<rect x="0" y="0" width="{CW}" height="{VH}" fill="#efe3c8"/><rect x="0" y="0" width="{CW}" height="{VH}" fill="url(#ink-hatch-h)" opacity=".3"/>']
# wall calendar
cx0, cy0 = 112, 10
v.append(f'<rect x="{cx0}" y="{cy0}" width="118" height="100" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/><rect x="{cx0}" y="{cy0}" width="118" height="16" fill="#c9473a" stroke="#2a2018" stroke-width="1"/>'
         f'<circle cx="{cx0+30}" cy="{cy0}" r="2.4" fill="#2a2018"/><circle cx="{cx0+88}" cy="{cy0}" r="2.4" fill="#2a2018"/>'
         f'<text x="{cx0+59}" y="{cy0+12.5}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:#fbf6ea">減藥計畫</text>')
for r in range(5):
    for c in range(7):
        x = cx0 + 4 + c * 16
        y = cy0 + 20 + r * 16
        v.append(f'<rect x="{x}" y="{y}" width="14" height="14" fill="none" stroke="#bfae8a" stroke-width=".6"/>')
        k = r * 7 + c
        if k < 23:
            v.append(f'<path d="M{x+3} {y+3} l8 8 M{x+11} {y+3} l-8 8" stroke="#6a5640" stroke-width=".9"/>')
# step-down dose bars on calendar weeks (right margin): 1, 3/4, 1/2, 1/4
for r, frac in enumerate([1, .75, .5, .25, 0]):
    pass
# table
v.append(f'<path d="M0 124 H{CW} V{VH} H0Z" fill="#b48a5e"/><path d="M0 124 H{CW} V{VH} H0Z" fill="url(#ink-hatch-l)"/><path d="M0 124 H{CW}" class="ink"/>')
# pill bottle (amber) + cap + blank label
bx, by = 40, 124
v.append(f'<path d="M{bx-18} {by} V{by-56} C{bx-18} {by-62} {bx+18} {by-62} {bx+18} {by-56} V{by}Z" fill="#c9862e" stroke="#2a2018" stroke-width="1.2"/>'
         f'<path d="M{bx+8} {by} V{by-56} C{bx+12} {by-58} {bx+16} {by-58} {bx+18} {by-56} V{by}Z" fill="url(#ink-hatch)" opacity=".7"/>'
         f'<path d="M{bx-12} {by-50} V{by-6}" stroke="#fff" stroke-width="2" opacity=".35"/>'
         f'<rect x="{bx-20}" y="{by-74}" width="40" height="16" rx="2" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
         + "".join(f'<path d="M{bx-18+k*4} {by-73} V{by-59}" stroke="#2a2018" stroke-width=".5"/>' for k in range(10)) +
         f'<rect x="{bx-15}" y="{by-46}" width="30" height="26" fill="#fbf6ea" stroke="#2a2018" stroke-width=".7"/>'
         f'<text x="{bx}" y="{by-34}" text-anchor="middle" style="font-size:8px;font-weight:700">安眠藥</text>'
         f'<path d="M{bx-10} {by-28} H{bx+10} M{bx-10} {by-24} H{bx+6}" stroke="#2a2018" stroke-width=".5"/>')
# loose tablets incl. a halved one
for (px, py) in [(76, 134), (90, 140), (70, 146)]:
    v.append(f'<ellipse cx="{px}" cy="{py}" rx="5" ry="3" fill="#fbf6ea" stroke="#2a2018" stroke-width=".8"/><path d="M{px-3} {py} H{px+3}" stroke="#2a2018" stroke-width=".4"/>')
v.append(f'<path d="M104 140 a5 3 0 0 1 0 6 Z" fill="#fbf6ea" stroke="#2a2018" stroke-width=".8"/><path d="M110 138 a5 3 0 0 0 0 6 Z" fill="#fbf6ea" stroke="#2a2018" stroke-width=".8"/>')
# glass of water
v.append(f'<path d="M150 98 H174 L170 134 H154Z" fill="#e3ecf7" fill-opacity=".8" stroke="#2a2018" stroke-width="1"/><path d="M152 110 H172" stroke="#3f6fa6" stroke-width=".7"/>')
# step-down taper sketch on table (paper)
v.append(f'<g transform="rotate(-4 205 145)"><rect x="180" y="128" width="54" height="34" fill="#fbf6ea" stroke="#2a2018" stroke-width=".8"/>'
         f'<path d="M184 134 H196 V142 H208 V149 H220 V155 H230" fill="none" stroke="{BLUE}" stroke-width="1.6"/></g>')
cells.append((v, "長期吃安眠藥，想停藥", "別自己突然停，和醫師一起慢慢減"))

out = []
for k, item in enumerate(cells):
    v, t, h = item[0], item[1], item[2]
    col = item[3] if len(item) > 3 else "#5d4b38"
    gx = 10 + (k % 3) * 250
    gy = 8 + (k // 3) * 228
    out.append(cell(k, gx, gy, "".join(v), t, h, col))

body = "\n".join(out)
cap = ('<b>圖 7·A　這些情況，請找醫師。</b>失眠有時只是表面，背後可能是需要另外治療的睡眠疾病或身心問題：打鼾合併呼吸暫停、白天嚴重嗜睡、腿部不適一定要動、睡夢中拳打腳踢、'
       '情緒低落甚至想傷害自己，以及長期使用安眠藥想停藥。出現這些情況，請先就醫評估，不要只靠自己調整。若有傷害自己的念頭，請立即撥打安心專線 1925（24 小時免付費）或 119。人物為示意。')
html = fig(PID, "圖 7·A", "這些情況，請找醫師", "Red flags — when to see a doctor", 460,
           "六格插圖：枕邊人看著大聲打鼾、呼吸暫停的伴侶；駕駛在方向盤前打瞌睡；坐在床邊揉小腿的長者；睡夢中揮拳踢腿、撞倒檯燈的長者；坐在床邊雙手掩面的人，旁邊有手機；安眠藥瓶、水杯與畫滿記號的減藥月曆",
           body, cap)
write(PID, html)
print(len(html))
