import sys, math
sys.path.insert(0, '/home/user/Insomnia/figs_public/_gen')
from pplib import *

PID = "pp-perception"
RED, BLUE = "#a8412c", "#2c5d9c"
AX0, AX1 = 150, 740
X = lambda t: AX0 + t * (AX1 - AX0) / 8.0

# ===== Row A: bedroom as she remembers it
SY0, SH = 26, 212
K = 1.25
A = [f'<g transform="translate(10,{SY0})">',
     f'<defs><clipPath id="{PID}-c1"><rect x="0" y="0" width="740" height="{SH}"/></clipPath>'
     f'<radialGradient id="{PID}-lamp" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff2c4" stop-opacity=".7"/><stop offset="1" stop-color="#fff2c4" stop-opacity="0"/></radialGradient></defs>',
     f'<g clip-path="url(#{PID}-c1)">',
     f'<rect x="0" y="0" width="740" height="{SH}" fill="#c3cde0"/><rect x="0" y="0" width="740" height="{SH}" fill="url(#ink-hatch-h)" opacity=".55"/>',
     f'<path d="M0 {SH-16} H740 V{SH} H0Z" fill="#8f9bad"/><path d="M0 {SH-16} H740 V{SH} H0Z" fill="url(#ink-hatch-l)"/><path d="M0 {SH-16} H740" class="ink"/>',
     window(684, 16, 44, 62)]
BW = 420
A.append(f'<g transform="scale({K})">')
A.append(bed_lying(BW / K, 0, (SH - 16) / K, eye="wide", shirt="#e3c9d6", hx=64, hair="long", blanket="#ead9b8", head_s=.46))
A.append('</g>')
# footboard
A.append(f'<path d="M{BW-6} {SH-16} V{SH-84} C{BW-6} {SH-92} {BW+12} {SH-94} {BW+14} {SH-86} V{SH-16}Z" fill="#a57c55" stroke="#2a2018" stroke-width="1.3"/>'
         f'<path d="M{BW-6} {SH-16} V{SH-84} C{BW-6} {SH-92} {BW+12} {SH-94} {BW+14} {SH-86} V{SH-16}Z" fill="url(#ink-hatch-l)"/>')
# nightstand + lamp (off) + alarm clock
NX = 470
A.append(f'<path d="M{NX} {SH-16} V{SH-70} H{NX+84} V{SH-16}" fill="#a57c55" stroke="#2a2018" stroke-width="1.2"/><path d="M{NX} {SH-46} H{NX+84} M{NX+38} {SH-60} h8 M{NX+38} {SH-34} h8" class="ink2"/>'
         f'<path d="M{NX-3} {SH-74} H{NX+87} V{SH-70} H{NX-3}Z" fill="#8a6440" stroke="#2a2018" stroke-width=".8"/>')
A.append(f'<path d="M{NX+62} {SH-74} h14 l-3 -4 h-8Z M{NX+69} {SH-78} V{SH-112}" fill="#8a6440" stroke="#2a2018" stroke-width="1.2"/>'
         f'<path d="M{NX+55} {SH-112} H{NX+83} L{NX+78} {SH-134} H{NX+60}Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1"/><path d="M{NX+60} {SH-112} L{NX+64} {SH-134} M{NX+66} {SH-112} L{NX+67} {SH-134}" class="ink2"/>')
A.append(digital(NX + 6, SH - 96, "05:00", 46, 22))
# armchair silhouette at right with a dressing gown
A.append(f'<path d="M600 {SH-16} V{SH-96} C600 {SH-112} 626 {SH-116} 640 {SH-110} C654 {SH-116} 666 {SH-104} 664 {SH-90} V{SH-16}" fill="#7d8fa8" stroke="#2a2018" stroke-width="1.2"/>'
         f'<path d="M592 {SH-16} V{SH-64} C592 {SH-74} 606 {SH-74} 606 {SH-64} V{SH-48} H660 V{SH-64} C660 {SH-74} 674 {SH-74} 674 {SH-64} V{SH-16}Z" fill="#8a9cb5" stroke="#2a2018" stroke-width="1.2"/>'
         f'<path d="M600 {SH-96} C600 {SH-112} 626 {SH-116} 640 {SH-110} L620 {SH-50} H604Z" fill="url(#ink-hatch-l)"/>')
A.append('</g></g>')
A.append(f'<rect x="10" y="{SY0}" width="740" height="{SH}" fill="none" stroke="#2a2018" stroke-width="1.2"/>')
# thought bubbles (absolute coords)
hx_abs, hy_abs = 10 + 64 * K, SY0 + ((SH - 16) / K - 63) * K
A.append(bubble(178, SY0 + 58, 56, 34, tail=(hx_abs + 8, hy_abs - 26), seed=.2))
A.append(f'<text x="178" y="{SY0+54}" class="ls" text-anchor="middle">明天的報告怎麼辦…</text>'
         f'<text x="178" y="{SY0+70}" class="ls" text-anchor="middle">又要睡不著了</text>')
for t, (hh, mm), txt in [(2, (1, 0), "01:00"), (4, (3, 0), "03:00"), (6, (5, 0), "05:00")]:
    cx, cy = X(t), SY0 + 56
    A.append(bubble(cx, cy, 54, 42, seed=.5 + t))
    A.append(clock(cx, cy - 10, 17, hh, mm))
    A.append(f'<text x="{cx}" y="{cy+24}" class="lb" text-anchor="middle" style="fill:{RED}">{txt} 還醒著</text>')
for a, b in [(2, 4), (4, 6)]:
    for k, r in [(.42, 2), (.5, 2.4), (.58, 2)]:
        A.append(f'<circle cx="{X(a)+(X(b)-X(a))*k:.1f}" cy="{SY0+56}" r="{r}" fill="#fbf6ea" stroke="#2a2018" stroke-width=".7"/>')
A.append(f'<text x="10" y="18" class="lt">她記得的那一夜：「我整晚都沒睡」 <tspan class="le">what she remembers</tspan></text>')

# ===== Row B: hypnogram
HY = {"W": 296, "R": 318, "L": 344, "D": 372}
B = []
B.append(f'<text x="10" y="270" class="lt halo">儀器記錄到的同一夜 <tspan class="le">hypnogram</tspan></text>')
B.append(f'<rect x="{AX0}" y="284" width="{AX1-AX0}" height="100" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/>')
# light-sleep band
B.append(f'<rect x="{AX0}" y="{HY["L"]-9}" width="{AX1-AX0}" height="18" fill="#cfdcef" opacity=".55"/>')
seq = [(0, 1.0, "W"), (1.0, 1.2, "L"), (1.2, 1.6, "L"), (1.6, 1.9, "D"), (1.9, 2.0, "L"), (2.0, 2.25, "W"),
       (2.25, 2.9, "L"), (2.9, 3.2, "D"), (3.2, 3.5, "L"), (3.5, 3.75, "R"), (3.75, 4.0, "L"), (4.0, 4.33, "W"),
       (4.33, 5.2, "L"), (5.2, 5.6, "R"), (5.6, 6.0, "L"), (6.0, 6.33, "W"), (6.33, 7.0, "L"), (7.0, 7.3, "R"),
       (7.3, 7.5, "L"), (7.5, 8.0, "W")]
for a, b, st in seq:
    if st == "W":
        B.append(f'<rect x="{X(a):.1f}" y="284" width="{X(b)-X(a):.1f}" height="100" fill="#e9b04a" opacity=".55"/>'
                 f'<rect x="{X(a):.1f}" y="284" width="{X(b)-X(a):.1f}" height="100" fill="url(#ink-hatch)" opacity=".45"/>')
d = ""
prev = None
for a, b, st in seq:
    y = HY[st]
    d += (f"M{X(a):.1f} {y} " if prev is None else f"L{X(a):.1f} {y} ") + f"L{X(b):.1f} {y} "
    prev = y
B.append(f'<path d="{d}" fill="none" stroke="#2a2018" stroke-width="2" stroke-linejoin="round"/>')
for a, b, st in seq:
    if st == "R":
        B.append(f'<path d="M{X(a):.1f} {HY["R"]} H{X(b):.1f}" stroke="#7a5aa6" stroke-width="4"/>')
    if st == "D":
        B.append(f'<path d="M{X(a):.1f} {HY["D"]} H{X(b):.1f}" stroke="{BLUE}" stroke-width="4"/>')
for name, key, en in [("清醒", "W", "awake"), ("作夢期", "R", "REM"), ("淺睡", "L", "light (N1–N2)"), ("深睡", "D", "deep (N3)")]:
    B.append(f'<text x="{AX0-8}" y="{HY[key]+4}" class="lb" text-anchor="end">{name} <tspan class="le">{en}</tspan></text>')
for i in range(9):
    hh = (23 + i) % 24
    B.append(f'<line x1="{X(i):.1f}" y1="384" x2="{X(i):.1f}" y2="388" stroke="#2a2018" stroke-width=".8"/>'
             f'<text x="{X(i):.1f}" y="399" class="ls" text-anchor="middle">{hh:02d}:00</text>')
# annotations under axis
B.append(f'<text x="{X(0.5):.1f}" y="416" class="ls halo" text-anchor="middle">躺了約 1 小時才睡著</text>')
B.append(f'<text x="{X(5.0):.1f}" y="416" class="ls halo" text-anchor="middle">醒來的片段都很短（約 15–20 分鐘），中間其實大多在<tspan style="font-weight:700;fill:{BLUE}">淺睡</tspan></text>')
# arrows from remembered clocks to wake spikes
for t in (2, 4, 6):
    x = X(t + .14)
    B.append(f'<path d="M{X(t):.1f} {SY0+96} C{X(t):.1f} {SY0+150} {x:.1f} 230 {x:.1f} 288" fill="none" stroke="{RED}" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#ink-arrow-red)"/>')
B.append(f'<text x="{X(6)+10:.1f}" y="256" class="ls halo" style="fill:{RED}">「記得醒著」＝ 這些短暫醒來</text>')

# ===== Row C: bars + message
C = []
CY = 446
C.append(f'<text x="10" y="{CY}" class="lt">兩種「睡了多久」 <tspan class="ls">（示意數字）</tspan></text>')
bx0, bpx = 150, 36
C.append(f'<text x="{bx0-8}" y="{CY+30}" class="lb" text-anchor="end">自己覺得睡了</text>')
C.append(f'<rect x="{bx0}" y="{CY+16}" width="{3*bpx}" height="20" fill="#e9b04a" stroke="#2a2018" stroke-width="1"/><rect x="{bx0}" y="{CY+16}" width="{3*bpx}" height="20" fill="url(#ink-hatch-l)"/>'
         f'<text x="{bx0+3*bpx+8}" y="{CY+31}" class="lb" style="font-size:14px">約 3 小時</text>')
C.append(f'<text x="{bx0-8}" y="{CY+66}" class="lb" text-anchor="end">儀器量到</text>')
C.append(f'<rect x="{bx0}" y="{CY+52}" width="{5.5*bpx}" height="20" fill="#3f6fa6" stroke="#2a2018" stroke-width="1"/><rect x="{bx0}" y="{CY+52}" width="{5.5*bpx}" height="20" fill="url(#ink-hatch-l)"/>'
         f'<text x="{bx0+5.5*bpx+8}" y="{CY+67}" class="lb" style="font-size:14px;fill:{BLUE}">約 5.5 小時</text>')
C.append(f'<path d="M{bx0} {CY+80} H{bx0+8*bpx}" stroke="#2a2018" stroke-width=".8"/>')
for i in range(0, 9, 2):
    C.append(f'<line x1="{bx0+i*bpx}" y1="{CY+80}" x2="{bx0+i*bpx}" y2="{CY+84}" stroke="#2a2018" stroke-width=".8"/><text x="{bx0+i*bpx}" y="{CY+96}" class="ls" text-anchor="middle">{i}</text>')
C.append(f'<text x="{bx0+8*bpx+10}" y="{CY+96}" class="ls">小時</text>')
C.append(f'<text x="{bx0}" y="{CY+116}" class="ls">兩者差距，就是被記成「醒著」的淺睡時間</text>')
MX = 486
C.append(f'<rect x="{MX}" y="{CY-14}" width="264" height="140" rx="6" fill="#f6e7b0" fill-opacity=".45" stroke="#2a2018" stroke-width=".9"/>')
C.append(f'<text x="{MX+16}" y="{CY+14}" class="lt" style="font-size:18px">這不是說謊。</text>')
C.append(f'<text x="{MX+16}" y="{CY+42}" class="lb" style="font-size:14.5px">失眠的人淺睡時，</text>')
C.append(f'<text x="{MX+16}" y="{CY+62}" class="lb" style="font-size:14.5px;fill:{RED}">大腦仍很像醒著，</text>')
C.append(f'<text x="{MX+16}" y="{CY+86}" class="ls">短短幾次醒來，連在一起就被記成</text>')
C.append(f'<text x="{MX+16}" y="{CY+102}" class="ls">「一整晚都沒睡」。醫學上稱為</text>')
C.append(f'<text x="{MX+16}" y="{CY+118}" class="ls">「睡眠狀態感知落差」。</text>')

body = "\n".join(["".join(A), "".join(B), "".join(C)])
cap = ('<b>圖 4·C　「我整晚都沒睡」：感覺和儀器的落差。</b>上圖是她記得的夜晚：一直在擔心、每次看鐘都醒著；下方是同一夜的睡眠檢查，'
       '她其實睡了好幾個小時，只是多半是淺睡，中間夾著幾次短暫醒來——剛好就是她記得看過鐘的那幾刻。這種落差很常見，並不代表失眠是想像出來的，'
       '而是失眠者的大腦在淺睡時仍偏「醒」。時數為示意。')
html = fig(PID, "圖 4·C", "「我整晚都沒睡」：感覺和儀器的落差", "Sleep-state misperception — felt vs. measured sleep", 590,
           "上方為躺在床上睜眼的女子，頭上一串思緒泡泡：擔心明天、時鐘 01:00、03:00、05:00；下方為同一夜的睡眠階段圖，顯示大多為淺睡、只有幾次短暫醒來，紅色箭頭把記得醒著的時刻對到短暫醒來；底部長條比較自覺睡 3 小時與儀器量到約 5.5 小時（示意）",
           body, cap)
write(PID, html)
print(len(html))
