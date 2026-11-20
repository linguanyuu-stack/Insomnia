import sys, math, random; sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from lib import *
from organs import heart, kidney, lateral_brain

PID = "pl-hyperarousal"
P = PID


def mirror_x(d_left):
    return d_left


body = []
body.append(f'<defs><radialGradient id="{P}-pet"><stop offset="0" stop-color="#fff3a0"/><stop offset=".35" stop-color="#f2a93b"/><stop offset=".7" stop-color="#d9473a" stop-opacity=".7"/><stop offset="1" stop-color="#d9473a" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="{P}-fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf6ea" stop-opacity="0"/><stop offset="1" stop-color="#fbf6ea"/></linearGradient></defs>')

# ================= centre figure (frontal, transparent body)
F = []
half_outline = ("M364 132 C350 138 330 140 314 144 C304 148 299 156 298 168 C296 190 294 214 292 240 C290 262 290 284 294 306 "
                "C296 320 298 334 300 344 L310 344 C310 330 312 300 314 270 C316 240 318 210 322 186 "
                "C326 210 330 240 336 268 C338 284 334 304 330 324 C328 340 328 352 328 362 L380 362 L380 132Z")
F.append(f'<path d="{half_outline}" fill="#f3d9c6" fill-opacity=".55"/>')
F.append(f'<path d="{half_outline}" transform="translate(760,0) scale(-1,1)" fill="#f3d9c6" fill-opacity=".55"/>')
F.append('<path d="M380 36 C401 36 410 54 410 74 C410 90 405 102 396 109 C390 114 385 116 380 116 C375 116 370 114 364 109 C355 102 350 90 350 74 C350 54 359 36 380 36Z" fill="#f3d9c6" fill-opacity=".55"/>')
# skeleton hints: clavicles, ribs, sternum
ribs = []
for i in range(7):
    y = 156 + i * 16
    ribs.append(f'M378 {y-3} C362 {y-2} 344 {y+4} {334+i*0.5} {y+18}')
rib_d = " ".join(ribs)
F.append(f'<path d="{rib_d}" fill="none" stroke="#bfae8a" stroke-width="1.6"/><path d="{rib_d}" transform="translate(760,0) scale(-1,1)" fill="none" stroke="#bfae8a" stroke-width="1.6"/>')
F.append('<path d="M374 146 L386 146 L385 226 L375 226Z" fill="#efe6d2" stroke="#bfae8a" stroke-width="1"/>')
F.append('<path d="M334 142 C350 146 364 144 376 140" fill="none" stroke="#bfae8a" stroke-width="3"/><path d="M426 142 C410 146 396 144 384 140" fill="none" stroke="#bfae8a" stroke-width="3"/>')
# lungs
lung = "M372 152 C356 150 342 166 338 196 C334 226 336 250 342 258 C352 256 364 252 372 248Z"
F.append(f'<path d="{lung}" fill="#cfdcef" fill-opacity=".45" stroke="#7d93b3" stroke-width=".8"/><path d="{lung}" transform="translate(760,0) scale(-1,1)" fill="#cfdcef" fill-opacity=".45" stroke="#7d93b3" stroke-width=".8"/>')
F.append('<path d="M336 260 C356 246 372 248 380 254 C390 248 406 246 424 258" fill="none" stroke="#a57c55" stroke-width="1" stroke-dasharray="3 2"/>')
# aorta / IVC down to kidneys
F.append('<path d="M386 236 L386 340" stroke="#b5473a" stroke-width="3.5"/><path d="M375 232 L375 340" stroke="#3f6fa6" stroke-width="3.5"/>')
# heart in situ
F.append(f'<g transform="translate(360,186) scale(.27)">{heart(P, detail=False)}</g>')
# kidneys + adrenals
F.append(f'<g transform="translate(344,272) scale(.32)">{kidney()}</g><g transform="translate(416,272) scale(-.32,.32)">{kidney()}</g>')
# brain in head with PET glow
F.append(f'<clipPath id="{P}-hb"><path d="M357 60 C357 46 368 40 380 40 C392 40 403 46 403 60 C403 68 398 72 390 72 C385 72 382 70 380 70 C378 70 375 72 370 72 C362 72 357 68 357 60Z"/></clipPath>')
F.append('<path d="M357 60 C357 46 368 40 380 40 C392 40 403 46 403 60 C403 68 398 72 390 72 C385 72 382 70 380 70 C378 70 375 72 370 72 C362 72 357 68 357 60Z" fill="#efe1d6" stroke="#2a2018" stroke-width=".9"/>')
F.append(f'<g clip-path="url(#{P}-hb)"><circle cx="368" cy="52" r="14" fill="url(#{P}-pet)"/><circle cx="394" cy="50" r="13" fill="url(#{P}-pet)"/><circle cx="380" cy="66" r="9" fill="url(#{P}-pet)"/></g>')
F.append('<path d="M380 41 L380 70 M362 52 C366 48 370 54 374 50 M386 50 C390 46 394 52 398 48 M362 62 C366 60 370 64 374 60 M386 60 C390 58 394 62 398 60" class="ink2"/>')
# head details
F.append('<path d="M350 70 C348 50 360 34 380 33 C400 34 412 50 410 70 C406 58 400 50 390 48 C380 46 368 48 360 52 C354 56 352 62 350 70Z" fill="#5a4330" fill-opacity=".55" stroke="#2a2018" stroke-width=".8"/>')
F.append('<path d="M380 36 C401 36 410 54 410 74 C410 90 405 102 396 109 C390 114 385 116 380 116 C375 116 370 114 364 109 C355 102 350 90 350 74 C350 54 359 36 380 36Z" class="ink3"/>')
F.append('<path d="M351 72 C345 70 343 78 345 86 C346 92 349 96 352 94 M409 72 C415 70 417 78 415 86 C414 92 411 96 408 94" class="ink"/>')
for ex in (368, 392):
    F.append(f'<path d="M{ex-6} 78 C{ex-3} 74.5 {ex+3} 74.5 {ex+6} 78 C{ex+3} 80.5 {ex-3} 80.5 {ex-6} 78Z" fill="#fff" stroke="#2a2018" stroke-width=".8"/><circle cx="{ex}" cy="77.8" r="2" fill="#3a2a1c"/>'
             f'<path d="M{ex-7} 71 C{ex-3} 69 {ex+3} 69 {ex+7} 71.5" fill="none" stroke="#3b2a1d" stroke-width="1.3"/>')
F.append('<path d="M380 80 C379 87 377 92 376 95 C378 97.5 382 97.5 384 95 M372 105 C376 106.5 384 106.5 388 105 M374 103.5 C378 102.5 382 102.5 386 103.5" class="ink2" stroke-width=".8"/>')
# body outline strokes
outline_stroke = ("M364 110 C366 118 367 126 364 132 C350 138 330 140 314 144 C304 148 299 156 298 168 C296 190 294 214 292 240 C290 262 290 284 294 306 "
                  "C296 320 298 334 300 344 M310 344 C310 330 312 300 314 270 C316 240 318 210 322 186 "
                  "M324 190 C328 210 330 240 336 268 C338 284 334 304 330 324 C328 340 328 352 328 362")
F.append(f'<path d="{outline_stroke}" class="ink3"/><path d="{outline_stroke}" transform="translate(760,0) scale(-1,1)" class="ink3"/>')
F.append(hand(304, 340, .9, 90) + f'<g transform="translate(760,0) scale(-1,1)">{hand(304, 340, .9, 90)}</g>')
F.append('<path d="M326 362 C346 366 362 368 380 366 C398 368 414 366 434 362" fill="none" stroke="#2a2018" stroke-width=".8" stroke-dasharray="3 3"/>')
F.append('<path d="M376 300 C378 304 382 304 384 300" class="ink2"/>')
# BP cuff on patient's left upper arm (viewer right)
F.append('<path d="M440 186 L467 184 L469 222 L438 224Z" fill="#7d93b3" stroke="#2a2018" stroke-width="1"/>'
         '<path d="M444 190 L444 220 M462 188 L463 220" stroke="#e6edf6" stroke-width="1" stroke-dasharray="2 2"/>')
body.append("".join(F))

# ================= callout: brain PET + EEG (top-left)
B = ['<rect x="8" y="28" width="276" height="230" rx="4" class="panel"/>']
B.append(f'<clipPath id="{P}-lb"><path d="M30 110 C26 80 50 50 90 44 C130 38 170 46 196 64 C214 78 222 98 216 116 C212 128 200 136 188 138 C170 140 150 142 132 140 C116 150 96 152 80 146 C64 142 48 132 40 124 C34 120 30 116 30 110Z"/></clipPath>')
lb = lateral_brain(P, pet=False)
pet = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{P}-pet)" opacity="{op}"/>' for (cx, cy, r, op) in
              [(62, 82, 32, .9), (104, 60, 26, .7), (160, 80, 28, .65), (122, 112, 20, .8), (196, 104, 18, .55)])
B.append(f'<g transform="translate(4,-3) scale(.86)">{lb}<g clip-path="url(#{P}-lb)">{pet}</g>'
         '<path d="M30 110 C26 80 50 50 90 44 C130 38 170 46 196 64 C214 78 222 98 216 116 C212 128 200 136 188 138 C170 140 150 142 132 140 C116 150 96 152 80 146 C64 142 48 132 40 124 C34 120 30 116 30 110Z" fill="none" stroke="#2a2018" stroke-width="1.4"/></g>')
B.append('<text x="196" y="46" class="lb halo">腦部代謝 ↑</text><text x="196" y="60" class="le halo">PET glucose</text><text x="196" y="72" class="le halo">metabolism</text>')
B.append('<text x="18" y="168" class="ls halo">睡著時代謝仍偏高；入睡時清醒相關</text><text x="18" y="182" class="ls halo">腦區的代謝下降得比較少</text>')
# EEG traces
def eeg(x0, y0, w, kind):
    random.seed(5 if kind == "d" else 9)
    pts = []
    for i in range(w):
        if kind == "d":
            v = 9 * math.sin(i * .07) + 2 * math.sin(i * .5) + random.uniform(-1, 1)
        else:
            v = 2.5 * math.sin(i * .9) + 2 * math.sin(i * 1.7) + 3 * math.sin(i * .12) + random.uniform(-1.5, 1.5)
        pts.append((x0 + i, y0 - v))
    return '<path d="M' + " L".join(f"{a} {b:.1f}" for a, b in pts) + f'" fill="none" stroke="{"#2c5d9c" if kind == "d" else "#a8412c"}" stroke-width=".9"/>'
B.append(eeg(104, 204, 172, "d") + eeg(104, 238, 172, "b"))
B.append('<text x="18" y="203" class="ls">好睡者深睡</text><text x="18" y="216" class="le">slow δ waves</text>'
         '<text x="18" y="237" class="ls" style="fill:#a8412c">失眠者睡眠中</text><text x="18" y="250" class="le">more fast β / γ</text>')
body.append("".join(B))
body.append('<path d="M357 54 C330 40 300 50 284 70" fill="none" stroke="#8a6a3a" stroke-width=".8" stroke-dasharray="3 2"/>')

# ================= callout: adrenal (left middle)
K = ['<rect x="8" y="268" width="276" height="112" rx="4" class="panel"/>']
K.append(f'<g transform="translate(18,272) scale(.92)">{kidney()}</g>')
K.append('<text x="98" y="290" class="lb halo">腎上腺 <tspan class="le">adrenal gland</tspan></text>'
         '<text x="98" y="306" class="ls">皮質醇 cortisol ↑（HPA 軸）</text>'
         '<text x="98" y="321" class="ls">正腎上腺素 ↑（交感神經）</text>'
         '<text x="98" y="342" class="ls" style="fill:#8a6a3a">下視丘 CRH → 腦下垂體 ACTH</text>'
         '<text x="98" y="356" class="ls" style="fill:#8a6a3a">→ 腎上腺皮質 → 皮質醇</text>')
K.append(lead([(96, 286), (52, 282)]))
K.append('<text x="98" y="372" class="le">adrenal sits on top of the kidney 腎臟</text>')
body.append("".join(K))
body.append('<path d="M346 282 C320 286 300 300 284 316" fill="none" stroke="#8a6a3a" stroke-width=".8" stroke-dasharray="3 2"/>')

# ================= callout: heart (top-right)
H = ['<rect x="476" y="28" width="276" height="230" rx="4" class="panel"/>']
H.append(f'<g transform="translate(490,52) scale(.8)">{heart(P)}</g>')
hl = [("主動脈弓", "Aortic arch", (582, 64), 50),
      ("肺動脈幹", "Pulmonary trunk", (600, 96), 84),
      ("左心室", "Left ventricle", (642, 168), 118),
      ("右心室", "Right ventricle", (588, 170), 152),
      ("冠狀動脈", "Coronary arteries", (611, 180), 186)]
for zh, en, tgt, y in hl:
    H.append(lab(668, y, zh, en, two=True))
    H.append(lead([(666, y - 4), tgt]))
H.append(lab(484, 44, "上腔靜脈", None, cls="ls") + lead([(532, 48), (544, 62)]))
H.append(lab(484, 150, "右心房", None, cls="ls") + lead([(520, 146), (534, 140)]))
# fast ECG
pts = []
for i in range(170):
    ph = i % 24
    v = -12 if ph == 4 else (3 if ph == 5 else (2 * math.sin((ph - 10) / 12 * math.pi) if 10 <= ph <= 22 else 0))
    pts.append((574 + i, 238 + v))
H.append('<path d="M' + " L".join(f"{a} {b:.1f}" for a, b in pts) + '" fill="none" stroke="#a8412c" stroke-width="1"/>')
H.append('<text x="484" y="236" class="lb" style="fill:#a8412c">心跳 ↑</text><text x="484" y="250" class="le">heart rate ↑</text>')
body.append("".join(H))
body.append('<path d="M400 210 C430 190 450 160 476 150" fill="none" stroke="#8a6a3a" stroke-width=".8" stroke-dasharray="3 2"/>')

# ================= BP gauge + thermometer (right middle)
T = ['<rect x="476" y="268" width="276" height="112" rx="4" class="panel"/>']
gx, gy = 520, 318
T.append(f'<path d="M468 214 C474 240 470 262 480 282 C488 296 494 304 {gx-18} {gy+12}" fill="none" stroke="#4a4f57" stroke-width="2"/>')
T.append(f'<circle cx="{gx}" cy="{gy}" r="24" fill="#e6e6e0" stroke="#2a2018" stroke-width="1.4"/><circle cx="{gx}" cy="{gy}" r="20" fill="#fbf6ea" stroke="#2a2018" stroke-width=".7"/>')
for i in range(13):
    a = math.radians(-135 + i * 22.5)
    T.append(f'<line x1="{gx+16*math.sin(a):.1f}" y1="{gy-16*math.cos(a):.1f}" x2="{gx+19.5*math.sin(a):.1f}" y2="{gy-19.5*math.cos(a):.1f}" stroke="#2a2018" stroke-width=".8"/>')
T.append(f'<path d="M{gx-17} {gy+8} A18 18 0 0 1 {gx-8} {gy-16}" fill="none" stroke="#a8412c" stroke-width="2.4" opacity=".0"/>')
T.append(f'<line x1="{gx}" y1="{gy}" x2="{gx+15}" y2="{gy-8}" stroke="#a8412c" stroke-width="1.6" stroke-linecap="round"/><circle cx="{gx}" cy="{gy}" r="2" fill="#2a2018"/>')
T.append(f'<path d="M{gx+6} {gy+40} C{gx+16} {gy+44} {gx+30} {gy+50} {gx+40} {gy+48}" fill="none" stroke="#4a4f57" stroke-width="2"/>'
         f'<ellipse cx="{gx+50}" cy="{gy+46}" rx="12" ry="8" fill="#4a4f57" stroke="#2a2018" stroke-width=".8"/>')
T.append('<text x="552" y="292" class="lb">夜間血壓 ↑</text><text x="552" y="306" class="le">night-time BP</text>')
# thermometer
tx = 660
T.append(f'<rect x="{tx-5}" y="280" width="10" height="72" rx="5" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
         f'<circle cx="{tx}" cy="358" r="9" fill="#d9473a" stroke="#2a2018" stroke-width="1"/>'
         f'<rect x="{tx-2.2}" y="296" width="4.4" height="60" fill="#d9473a"/>' +
         "".join(f'<line x1="{tx+5}" y1="{286+i*7}" x2="{tx+9}" y2="{286+i*7}" stroke="#2a2018" stroke-width=".6"/>' for i in range(9)))
T.append(f'<path d="M{tx-14} 312 V292" stroke="#a8412c" stroke-width="1.4" marker-end="url(#ink-arrow-red)"/>')
T.append('<text x="676" y="300" class="lb">體溫 ↑</text><text x="676" y="314" class="le">core temp</text><text x="676" y="332" class="lb">代謝率 ↑</text><text x="676" y="346" class="le">metabolic rate</text>')
body.append("".join(T))

# ================= limbic inset (bottom-left)
Lm = ['<rect x="8" y="392" width="462" height="196" rx="4" class="panel"/>']
Lm.append('<text x="18" y="410" class="lt">壓力迴路：邊緣系統 → 清醒中樞</text><text x="18" y="425" class="le">limbic projections to arousal centres (medial view; amygdala &amp; hippocampus projected)</text>')
ox, oy, sc = 40, 434, .85
outer = ("M20 90 C14 56 50 16 120 12 C180 10 232 36 244 80 C248 100 240 116 226 122 C214 126 200 124 192 120 C184 112 176 108 166 108 "
         "C150 108 140 114 130 118 C110 124 80 122 60 116 C40 112 22 104 20 90Z")
G = []
G.append(f'<clipPath id="{P}-mb"><path d="{outer}"/></clipPath>')
G.append(f'<path d="{outer}" fill="#efe1d6" stroke="#2a2018" stroke-width="1.4"/>')
G.append(f'<g clip-path="url(#{P}-mb)"><path d="M10 20 L78 20 L72 70 L60 120 L10 120Z" fill="#cfdcef" opacity=".8"/></g>')
G.append(f'<path d="{outer}" fill="none" stroke="#2a2018" stroke-width="1.4"/>')
G.append('<path d="M64 70 C70 50 100 38 132 36 C166 34 196 46 204 66 C206 74 200 78 194 74 C186 58 164 50 136 50 C108 50 86 58 78 72 C74 78 66 78 64 70Z" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/>')
G.append('<path d="M40 40 C48 34 52 42 60 36 M90 22 C96 30 104 24 110 30 M150 20 C156 28 164 22 170 28 M200 36 C204 44 212 42 216 50 M226 70 C230 78 226 86 234 92 M30 70 C38 66 42 72 48 68" class="ink2"/>')
G.append('<ellipse cx="146" cy="80" rx="22" ry="12" fill="#e8d6c8" stroke="#2a2018" stroke-width=".9"/>')
G.append('<path d="M148 96 C160 92 172 96 176 104 C186 112 190 126 186 140 C184 150 186 158 188 168 L174 168 C172 156 168 150 164 142 C154 136 148 126 148 112Z" fill="#e8d6c8" stroke="#2a2018" stroke-width="1"/>')
G.append('<path d="M190 120 C206 112 236 116 242 130 C246 146 232 156 214 156 C200 156 190 146 188 134Z" fill="#e8d6c8" stroke="#2a2018" stroke-width="1"/>'
         '<path d="M196 126 C210 122 230 124 238 132 M196 136 C210 134 226 136 236 142 M200 146 C210 146 222 148 230 150" class="ink2"/>')
G.append('<path d="M112 92 C120 88 132 90 140 96 C138 104 130 108 122 108 C116 106 112 100 112 92Z" fill="#f6e7b0" stroke="#2a2018" stroke-width=".8"/>')
G.append('<circle cx="134" cy="108" r="3" fill="#efe1d6" stroke="#2a2018" stroke-width=".7"/><ellipse cx="118" cy="117" rx="5" ry="4" fill="#f0c4b8" stroke="#2a2018" stroke-width=".7"/>')
# hippocampus & amygdala (projected, dashed)
G.append('<path d="M120 116 C140 124 166 122 178 106 C182 100 180 94 174 96 C166 108 146 114 124 108Z" fill="#d9b53c" fill-opacity=".55" stroke="#2a2018" stroke-width=".9" stroke-dasharray="2.5 2"/>')
G.append('<ellipse cx="108" cy="112" rx="9" ry="6.5" fill="#d9473a" fill-opacity=".75" stroke="#2a2018" stroke-width=".9" stroke-dasharray="2.5 2"/>')
# nuclei
G.append('<circle cx="122" cy="96" r="3.4" fill="#a8412c" stroke="#2a2018" stroke-width=".6"/>')  # PVN
G.append('<circle cx="132" cy="100" r="3.4" fill="#2f7a5f" stroke="#2a2018" stroke-width=".6"/>')  # LH orexin
G.append('<circle cx="180" cy="126" r="3.4" fill="#2c5d9c" stroke="#2a2018" stroke-width=".6"/>')  # LC
# pathways
G.append('<path d="M112 106 C114 102 116 100 119 98" fill="none" stroke="#a8412c" stroke-width="1.8" marker-end="url(#ink-arrow-red)"/>')
G.append('<path d="M114 116 C140 136 162 136 176 128" fill="none" stroke="#a8412c" stroke-width="1.8" marker-end="url(#ink-arrow-red)"/>')
G.append('<path d="M125 96 L128 98" stroke="#a8412c" stroke-width="1.6"/>')
G.append('<path d="M132 96 C132 70 116 52 96 40" fill="none" stroke="#2f7a5f" stroke-width="1.6" marker-end="url(#ink-arrow)"/>')
G.append('<path d="M178 122 C176 90 170 60 156 34" fill="none" stroke="#2c5d9c" stroke-width="1.6" marker-end="url(#ink-arrow-blue)"/>')
G.append('<path d="M50 80 C64 96 84 104 98 110" fill="none" stroke="#2c5d9c" stroke-width="1.4" stroke-dasharray="3 2" marker-end="url(#ink-tee)"/>')
Lm.append(f'<g transform="translate({ox},{oy}) scale({sc})">{"".join(G)}</g>')
# labels for limbic inset (right side column)
def gp(x, y):
    return (round(ox + sc * x, 1), round(oy + sc * y, 1))
lbls = [("前額葉皮質 PFC", "top-down brake (weaker)", gp(40, 64), 446),
        ("下視丘 PVN：CRF", "stress hormone drive", gp(122, 96), 476),
        ("外側下視丘 orexin", "the 'accelerator'", gp(132, 100), 506),
        ("杏仁核 Amygdala", "fear / threat", gp(108, 114), 536),
        ("藍斑核 LC：正腎上腺素", "noradrenaline", gp(180, 126), 566)]
for zh, en, tgt, y in lbls:
    Lm.append(f'<text x="290" y="{y}" class="lb halo">{zh}</text><text x="290" y="{y+12}" class="le halo">{en}</text>')
    Lm.append(lead([(286, y - 4), tgt]))
Lm.append(lab(gp(120, 136)[0] - 60, gp(120, 136)[1] + 10, "海馬迴", "hippocampus", cls="ls"))
Lm.append(lead([(gp(120, 136)[0] - 20, gp(120, 136)[1] + 2), gp(150, 118)]))
body.append("".join(Lm))

# ================= caution box (bottom-right)
C = ['<rect x="476" y="392" width="276" height="196" rx="4" fill="#f6e7b0" fill-opacity=".35" stroke="#c9962e" stroke-width=".9"/>']
C.append('<text x="488" y="414" class="lb" style="fill:#a8412c">注意因果方向</text>')
lines = ["上面這些「熱機」現象多半來自相關性研究，",
         "可能是失眠、睡眠不足或共病（如憂鬱）的",
         "結果，不一定是原因。",
         "",
         "對應第 1 章的開關圖：過度警覺＝油門被踩著。",
         "壓力 → CRF → 刺激 orexin 神經元（小鼠）；",
         "杏仁核等邊緣區投射到清醒中樞。",
         "orexin 拮抗劑的思路：不加強煞車，",
         "而是拿掉一部分油門。"]
for i, t in enumerate(lines):
    C.append(f'<text x="488" y="{434 + i*16}" class="ls">{t}</text>')
body.append("".join(C))

# left/right orientation note
body.append('<text x="380" y="380" class="ls" text-anchor="middle">（圖中人的左側在讀者右側）</text>')

cap = ('<b>圖 4-A　過度警覺：身體哪裡在「熱機」。</b>慢性失眠者在白天與夜間都可測到較高的激發程度：腦部葡萄糖代謝偏高（PET）、睡眠腦波中快波（β、γ）較多、'
       '心跳與代謝率、體溫較高、HPA 軸與交感神經較活躍（皮質醇、正腎上腺素），部分研究見夜間血壓較高。左下為邊緣系統（杏仁核、海馬迴，以虛線投影在正中切面上）投射到下視丘與腦幹清醒中樞的示意，前額葉的「煞車」相對不足。'
       '這些多為相關性發現，因果方向未定。示意圖，依解剖教科書重繪，器官大小與位置已簡化。')

html = fig(PID, "Plate 4·A", "過度警覺：身體哪裡在「熱機」", "Hyperarousal — where the body is 'running hot'", 596,
           "半透明人體正面圖，標出腦部代謝與快波、心臟心跳加快、腎上腺皮質醇升高、體溫與血壓升高，並附邊緣系統投射到清醒中樞的插圖", "\n".join(body), cap)
write(PID, html)
