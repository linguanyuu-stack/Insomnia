import sys, math, random; sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from lib import *

PID = "pl-psg"
HX, HY, HS = 100, 224, .62
SH = "#e3e9f2"  # t-shirt


def hp(lx, ly):
    """head local -> global (rot -90)"""
    return (round(HX + ly * HS, 1), round(HY - lx * HS, 1))


def electrode(x, y, r=3.2, col="#d9b53c"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="#2a2018" stroke-width=".8"/><circle cx="{x}" cy="{y}" r="{r*.4}" fill="#fbf6ea"/>'


def wire(p0, p1, c1, c2, col="#6a5640", w=.9):
    return f'<path d="M{p0[0]} {p0[1]} C{c1[0]} {c1[1]} {c2[0]} {c2[1]} {p1[0]} {p1[1]}" fill="none" stroke="{col}" stroke-width="{w}"/>'


o = []
# ---------- bed
o.append('<path d="M22 300 V150 C22 140 44 136 48 146 V300" fill="#bfc6cf" stroke="#2a2018" stroke-width="1.3"/>'
         '<path d="M22 300 V150 C22 140 44 136 48 146 V300" fill="url(#ink-hatch-l)"/>'
         '<path d="M44 248 H514 V272 H44Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/>'
         '<path d="M44 272 H514 V282 H44Z" fill="#9aa3ad" stroke="#2a2018" stroke-width="1"/>'
         '<path d="M60 282 V300 M500 282 V300" stroke="#2a2018" stroke-width="3"/>'
         '<path d="M0 300 H516" class="ink"/>')
# pillow
o.append('<path d="M50 246 C44 234 52 226 68 226 C90 224 118 224 130 230 C136 236 134 246 128 250 C104 252 72 252 50 246Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
         '<path d="M56 244 C76 248 104 248 126 246 M58 232 C64 236 68 240 70 244" class="ink2"/>')
# ---------- body
o.append(head(HX, HY, HS, -90, eye="closed", hair="short"))
# torso (t-shirt)
torso = ("M128 214 C134 206 146 202 160 199 C180 196 204 198 224 201 C244 204 260 206 274 210 L276 250 L128 250 C124 240 124 224 128 214Z")
o.append(f'<path d="{torso}" fill="{SH}" stroke="#2a2018" stroke-width="1.2"/>'
         '<path d="M132 214 C138 220 146 222 152 220" class="ink2"/><path d="M128 214 C124 224 124 240 128 250 L136 250 C132 238 132 224 134 216Z" fill="url(#ink-hatch-l)"/>'
         '<path d="M180 200 C186 206 190 214 192 222 M226 202 C230 210 232 220 232 230" class="ink2" stroke-opacity=".6"/>')
# RIP belts (chest, abdomen) with coil zigzag
for bx, top in [(168, 197), (238, 203)]:
    o.append(f'<path d="M{bx} {top} L{bx+10} {top+1} L{bx+10} 250 L{bx} 250Z" fill="#7d93b3" stroke="#2a2018" stroke-width=".9"/>')
    zz = f"M{bx+5} {top+2}"
    yy = top + 2
    k = 0
    while yy < 248:
        yy += 3
        zz += f" L{bx+2 if k%2==0 else bx+8} {yy}"
        k += 1
    o.append(f'<path d="{zz}" fill="none" stroke="#e6edf6" stroke-width=".7"/>')
    o.append(f'<rect x="{bx-1}" y="{top+14}" width="12" height="8" rx="1.5" fill="#2a2018"/>')
# ECG electrodes on chest
o.append(electrode(150, 204, 3.4, "#e9e2d0") + electrode(214, 200, 3.4, "#e9e2d0"))
# blanket over hips/thighs
o.append('<path d="M262 206 C276 196 300 192 322 196 C344 200 362 198 382 204 C390 206 394 216 392 226 L398 290 C380 292 360 288 340 292 C316 294 290 288 266 292 C262 270 258 240 262 206Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>'
         '<path d="M322 196 C318 230 324 260 320 292 C312 262 310 230 314 198Z" fill="url(#ink-hatch)"/>'
         '<path d="M292 196 C294 230 288 262 292 290 M356 200 C352 236 360 262 356 290" class="ink2"/>'
         '<path d="M382 204 C390 206 394 216 392 226 L398 290 L388 290 C386 260 384 230 380 206Z" fill="url(#ink-hatch-d)" opacity=".7"/>')
# lower legs (reuse lateral leg outline): knee ~386, heel on mattress
leg = ("M0 196 C30 192 56 190 72 192 C82 192 88 196 92 200 C140 206 210 216 262 224 C280 210 300 190 316 172 "
       "C322 164 330 162 334 168 C336 174 332 182 326 188 C316 200 300 220 290 238 C284 250 278 260 268 264 "
       "C258 266 250 264 246 258 C240 252 232 250 222 252 C200 256 180 262 150 264 C120 266 96 262 80 256 C64 252 40 252 0 254Z")
o.append(f'<g transform="translate(330,104) scale(.56)"><g transform="translate(-12,-10)"><path d="{leg}" fill="#dcae93" stroke="#2a2018" stroke-width="1.6"/></g>'
         f'<path d="{leg}" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width="2.2"/>'
         '<path d="M100 214 C150 220 200 226 250 232 M326 172 C328 168 332 168 333 171 M322 178 C325 175 329 176 330 180 M254 236 C258 234 262 236 262 240" fill="none" stroke="#2a2018" stroke-width="1" stroke-opacity=".6"/></g>')
# blanket re-drawn over thighs (on top of leg root)
o.append('<path d="M262 206 C276 196 300 192 322 196 C344 200 362 198 382 204 C390 206 394 216 392 226 L398 290 C380 292 360 288 340 292 C316 294 290 288 266 292 C262 270 258 240 262 206Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>'
         '<path d="M322 196 C318 230 324 260 320 292 C312 262 310 230 314 198Z" fill="url(#ink-hatch)"/>'
         '<path d="M292 196 C294 230 288 262 292 290 M356 200 C352 236 360 262 356 290" class="ink2"/>'
         '<path d="M382 204 C390 206 394 216 392 226 L398 290 L388 290 C386 260 384 230 380 206Z" fill="url(#ink-hatch-d)" opacity=".7"/>')
# leg EMG electrodes on tibialis anterior (lateral to tibial crest)
o.append(electrode(420, 223, 3) + electrode(446, 226, 3))
# near arm lying along body with hand + pulse oximeter
o.append(capsule(146, 232, 206, 240, 9, 8, SH, 1.1))
o.append(capsule(206, 240, 262, 242, 7.5, 6, "#f3d9c6", 1.1))
o.append(hand(262, 242, .78, 4))
o.append('<path d="M282 236 h14 a4 4 0 0 1 4 4 v6 a4 4 0 0 1 -4 4 h-14Z" fill="#3a3a3a" stroke="#2a2018" stroke-width=".8"/><circle cx="292" cy="243" r="2" fill="#e34a3a"/>')
# head electrodes (10-20): local coords on scalp of profile head
eeg = {"Fp": (31, -20), "F": (22, -36), "Cz": (2, -45), "C": (-6, -30), "P": (-20, -40), "O": (-33, -14)}
eegp = {k: hp(*v) for k, v in eeg.items()}
mast = hp(-11, 12)
eog = hp(19, -1)
chin = [hp(26, 39), hp(18, 41)]
cann = hp(36, 13)
therm = hp(34, 18)
for k, (x, y) in eegp.items():
    o.append(electrode(x, y, 2.8))
o.append(electrode(*mast, 2.8, "#b7c6dc"))
o.append(electrode(*eog, 2.6, "#e9e2d0"))
for c in chin:
    o.append(electrode(*c, 2.4, "#e9e2d0"))
# nasal cannula: prongs at nostril, tubing over ear
o.append(f'<path d="M{cann[0]} {cann[1]} C{cann[0]+10} {cann[1]+2} {mast[0]+8} {mast[1]-8} {mast[0]+2} {mast[1]-2} C{mast[0]-6} {mast[1]+6} {mast[0]-12} {mast[1]+18} {mast[0]-24} {mast[1]+22}" fill="none" stroke="#7fb0a0" stroke-width="2.2"/>')
o.append(f'<path d="M{therm[0]} {therm[1]} C{therm[0]+6} {therm[1]-6} {therm[0]+16} {therm[1]-6} {therm[0]+22} {therm[1]-2}" fill="none" stroke="#c46a58" stroke-width="1.2"/>'
         f'<circle cx="{therm[0]}" cy="{therm[1]}" r="1.8" fill="#c46a58" stroke="#2a2018" stroke-width=".5"/>')
# head box on headboard + wires
o.append('<rect x="14" y="156" width="28" height="40" rx="3" fill="#4a4f57" stroke="#2a2018" stroke-width="1"/>'
         '<g fill="#d9b53c">' + "".join(f'<circle cx="{20+(i%3)*8}" cy="{164+(i//3)*8}" r="1.6"/>' for i in range(12)) + '</g>')
wires = []
for (x, y) in list(eegp.values()) + [mast, eog] + chin:
    wires.append(wire((x, y), (40, 176), (x - 10, y - 30), (60, 170), "#8a6a3a", .7))
for (x, y) in [(150, 204), (214, 200), (173, 214), (243, 220), (420, 223), (446, 226), (300, 243)]:
    wires.append(wire((x, y), (42, 190), (x - 10, y + 40), (90, 262), "#6a7a90", .7))
o.append('<g opacity=".85">' + "".join(wires) + '</g>')
# redraw electrodes on top of wires
for k, (x, y) in eegp.items():
    o.append(electrode(x, y, 2.8))
o.append(electrode(*mast, 2.8, "#b7c6dc") + electrode(*eog, 2.6, "#e9e2d0") + "".join(electrode(*c, 2.4, "#e9e2d0") for c in chin))
o.append(electrode(150, 204, 3.4, "#e9e2d0") + electrode(214, 200, 3.4, "#e9e2d0") + electrode(420, 223, 3) + electrode(446, 226, 3))
body = ['<g>' + "".join(o) + '</g>']

# ---------- labels (top row, two tiers) & bottom
L = []
def tl(x, y, zh, en, tgt, anchor="middle"):
    L.append(lab(x, y, zh, en, anchor=anchor, two=True))
    L.append(lead([(x, y + 17), tgt]))

tl(60, 40, "腦波 EEG", "10–20 scalp sites", eegp["Cz"])
tl(150, 40, "眼動 EOG", "outer canthus", eog)
tl(244, 40, "心電圖 ECG", "chest leads", (214, 200))
tl(340, 40, "腹部呼吸帶", "abdominal RIP belt", (243, 206))
tl(440, 40, "腿動 EMG", "tibialis anterior", (446, 226))
tl(108, 92, "鼻壓力導管", "nasal pressure cannula", (cann[0] + 2, cann[1] - 4))
tl(204, 92, "下巴肌電", "chin EMG", chin[0])
tl(290, 120, "胸部呼吸帶", "thoracic RIP belt", (173, 199))
# bottom labels
def bl(x, y, zh, en, tgt, anchor="middle"):
    L.append(lab(x, y, zh, en, anchor=anchor, two=True))
    L.append(lead([(x, y - 13), tgt]))
bl(44, 330, "電極盒", "head box", (28, 196))
bl(150, 330, "口鼻溫度感測", "thermistor", therm)
bl(270, 330, "乳突參考電極", "mastoid ref. M1/M2", mast)
bl(400, 330, "指尖血氧", "pulse oximeter SpO₂", (292, 250))
body.append("".join(L))
body.append('<text x="6" y="372" class="ls">每條線各量一件事：腦波＋眼動＋下巴肌電 → 判讀睡眠分期；</text><text x="6" y="387" class="ls">氣流＋呼吸帶＋血氧 → 呼吸事件；腿部肌電 → 週期性肢體抽動；心電圖 → 心律。</text>')

# ---------- monitor (top right)
mx, my, mw, mh = 520, 24, 232, 214
M = [f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="6" fill="#3b3f46" stroke="#2a2018" stroke-width="1.2"/>',
     f'<rect x="{mx+8}" y="{my+8}" width="{mw-16}" height="{mh-24}" fill="#fbf6ea" stroke="#2a2018" stroke-width=".8"/>',
     f'<path d="M{mx+mw/2-20} {my+mh} L{mx+mw/2-26} {my+mh+8} H{mx+mw/2+26} L{mx+mw/2+20} {my+mh}" fill="#3b3f46" stroke="#2a2018" stroke-width=".8"/>']
chans = [("EEG", "eeg"), ("EOG", "eog"), ("Chin", "emg"), ("Leg", "leg"), ("ECG", "ecg"), ("Flow", "flow"),
         ("Therm", "flow2"), ("Chest", "eff"), ("Abd", "eff2"), ("SpO₂", "spo2")]
random.seed(3)
x0 = mx + 52
x1 = mx + mw - 12
for i, (nm, kind) in enumerate(chans):
    yy = my + 24 + i * 17.5
    M.append(f'<text x="{mx+14}" y="{yy+4}" class="ls" style="font-size:10px;font-weight:600">{nm}</text>')
    pts = []
    n = int(x1 - x0)
    for j in range(n):
        t = j / n
        if kind == "eeg":
            v = 2.6 * math.sin(j * .9) + random.uniform(-2, 2) + 2.5 * math.sin(j * .21)
        elif kind == "eog":
            v = 5 * math.tanh(math.sin(j * .05) * 3) if .55 < t < .8 else random.uniform(-.6, .6)
        elif kind == "emg":
            v = random.uniform(-3, 3) if t < .5 else random.uniform(-.6, .6)
        elif kind == "leg":
            v = random.uniform(-4, 4) if (.2 < t < .24 or .6 < t < .64) else random.uniform(-.4, .4)
        elif kind == "ecg":
            ph = (j % 22)
            v = -6 if ph == 3 else (2 if ph == 4 else (1.2 * math.sin(ph / 22 * math.pi) if ph > 8 else 0))
        elif kind in ("flow", "flow2"):
            v = 4.5 * math.sin(j * .16)
        elif kind in ("eff", "eff2"):
            v = 4 * math.sin(j * .16 + (0 if kind == "eff" else .3))
        else:
            v = 2
        pts.append((x0 + j, yy - v))
    col = {"eeg": "#2c5d9c", "eog": "#2c5d9c", "emg": "#2a2018", "leg": "#2a2018", "ecg": "#a8412c", "spo2": "#a8412c"}.get(kind, "#2f7a5f")
    M.append('<path d="M' + " L".join(f"{a} {b:.1f}" for a, b in pts) + f'" fill="none" stroke="{col}" stroke-width=".8"/>')
M.append(f'<text x="{mx+mw/2}" y="{my+mh-5}" class="ls" text-anchor="middle" style="fill:#e8dcc2;font-size:10px">30 秒一頁（epoch）判讀</text>')
body.append("".join(M))
body.append(f'<text x="{mx}" y="{my+mh+24}" class="lb">多導睡眠檢查 <tspan class="le">Polysomnography (PSG)</tspan></text>')

# ---------- actigraphy inset (bottom right)
ax, ay = 520, 282
A = [f'<rect x="{ax}" y="{ay}" width="232" height="118" rx="4" class="panel"/>']
# forearm + watch
A.append(capsule(ax + 12, ay + 40, ax + 70, ay + 34, 11, 9, "#f3d9c6", 1.1))
A.append(hand(ax + 74, ay + 34, .7, -6))
A.append(f'<path d="M{ax+38} {ay+22} h14 v26 h-14Z" fill="#4a4f57" stroke="#2a2018" stroke-width=".9"/>'
         f'<rect x="{ax+36}" y="{ay+28}" width="18" height="14" rx="3" fill="#2a2f36" stroke="#2a2018" stroke-width=".9"/>'
         f'<rect x="{ax+38.5}" y="{ay+30.5}" width="13" height="9" rx="1.5" fill="#cfdcef"/>')
A.append(f'<text x="{ax+108}" y="{ay+20}" class="lb">腕動計 <tspan class="le">wrist actigraphy</tspan></text>'
         f'<text x="{ax+108}" y="{ay+35}" class="ls">只量「動不動」</text>'
         f'<text x="{ax+108}" y="{ay+49}" class="ls">靜止＝推估為睡著</text>')
# activity bars over 24 h (12:00 -> 12:00)
bx0, by0, bw = ax + 10, ay + 98, 212
random.seed(11)
for i in range(0, 96):
    t = 12 + i * .25
    hr = t % 24
    night = (hr >= 23.5 or hr < 6.5)
    lying_awake = 23.5 <= hr or hr < 1.2
    h = random.uniform(1, 4) if night else random.uniform(8, 30)
    if lying_awake:
        h = random.uniform(0.5, 3)
    col = "#3f6fa6" if night else "#8a6a3a"
    A.append(f'<rect x="{bx0 + i*bw/96:.1f}" y="{by0-h:.1f}" width="{bw/96*.75:.2f}" height="{h:.1f}" fill="{col}"/>')
A.append(f'<path d="M{bx0} {by0} H{bx0+bw}" class="ink2"/>')
for t, lb in [(12, "12"), (18, "18"), (24, "0"), (30, "6"), (36, "12")]:
    xx = bx0 + (t - 12) / 24 * bw
    A.append(f'<text x="{xx:.1f}" y="{by0+11}" class="ls" text-anchor="middle" style="font-size:9.5px">{lb}</text>')
A.append(f'<path d="M{bx0 + (23.5-12)/24*bw:.1f} {ay+80} H{bx0 + (25.2-12)/24*bw:.1f}" stroke="#a8412c" stroke-width="1" marker-end="url(#ink-arrow-red)" marker-start="url(#ink-arrow-red)"/>'
         f'<text x="{bx0 + (24.4-12)/24*bw:.1f}" y="{ay+74}" class="ls halo" text-anchor="middle" style="fill:#a8412c;font-size:10px">躺著沒睡也算「睡」</text>')
body.append("".join(A))

cap = ('<b>圖 2-A　儀器怎麼量睡眠。</b>多導睡眠檢查（PSG）在睡眠實驗室整夜同時記錄：頭皮腦波（依國際 10–20 系統定位）、眼角的眼動、下巴與小腿脛前肌的肌電、'
       '鼻壓力導管與口鼻溫度感測的氣流、胸腹呼吸帶、心電圖與指尖血氧；技師每 30 秒判讀一頁，算出客觀的入睡時間、總睡眠時間與呼吸事件。'
       '右下的腕動計只量手腕動不動，躺著清醒但不動時會被當成睡著，因此在失眠者常高估睡眠。主觀與客觀的落差，正是本節要談的。示意圖，電極數量已簡化。')

html = fig(PID, "Plate 2·A", "多導睡眠檢查 PSG 與手環：儀器量的睡眠", "Polysomnography and actigraphy — sleep as the instruments see it", 410,
           "病人躺在睡眠實驗室床上，接上腦波、眼動、肌電、氣流、呼吸帶、心電圖、血氧與腿部肌電；右上為 PSG 監視畫面，右下為腕動計與活動量長條圖", "\n".join(body), cap)
write(PID, html)
