import sys, math; sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from lib import *

PID = "pl-hotflash"
NG = "#d8cfe6"   # nightwear
W = 374


def scene():
    o = []
    o.append(f'<clipPath id="{PID}-c"><rect x="0" y="40" width="{W}" height="236"/></clipPath><g clip-path="url(#{PID}-c)">')
    o.append(f'<rect x="0" y="40" width="{W}" height="236" fill="#c9d3e3"/><rect x="0" y="40" width="{W}" height="236" fill="url(#ink-hatch-h)" opacity=".5"/>')
    o.append(f'<path d="M0 254 H{W} V276 H0Z" fill="#9aa6b6"/><path d="M0 254 H{W}" class="ink"/>')
    # window still dark
    o.append('<rect x="276" y="58" width="70" height="72" fill="#24334f" stroke="#2a2018" stroke-width="1"/><path d="M311 58 V130 M276 94 H346" stroke="#efe6d2" stroke-width="2.5"/>'
             '<circle cx="290" cy="70" r=".9" fill="#f6e7b0"/><circle cx="330" cy="110" r=".9" fill="#f6e7b0"/><circle cx="296" cy="118" r=".9" fill="#f6e7b0"/>'
             '<path d="M330 68 a7 7 0 1 0 5 11 a5.5 5.5 0 1 1 -5 -11Z" fill="#f6e7b0"/>')
    # clock
    o.append(clock(200, 76, 16, 3, 40) + '<rect x="178" y="98" width="44" height="15" rx="2" fill="#2a2018"/>'
             '<text x="200" y="109.5" text-anchor="middle" style="font-family:monospace;font-size:11.5px;font-weight:700;fill:#f6c96a">03:40</text>')
    # bed
    o.append('<path d="M8 254 V128 C8 118 30 114 34 124 V254" fill="#a57c55" stroke="#2a2018" stroke-width="1.3"/><path d="M8 254 V128 C8 118 30 114 34 124 V254" fill="url(#ink-hatch-l)"/>'
             f'<path d="M30 212 H{W} V236 H30Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/><path d="M30 236 H{W} V244 H30Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/><path d="M36 244 V254" stroke="#2a2018" stroke-width="3"/>'
             '<path d="M40 214 C120 218 220 216 374 216" stroke="#2a2018" stroke-width=".5" fill="none" stroke-dasharray="2 2" opacity=".5"/>')
    # damp patch on sheet
    o.append('<ellipse cx="74" cy="214" rx="34" ry="4" fill="#9fb4d4" opacity=".6"/>')
    o.append('<path d="M30 210 C24 200 30 192 44 192 C60 190 82 190 92 194 C98 198 96 210 92 214 C74 216 46 216 30 210Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>')
    # far arm propping on mattress
    o.append(capsule(64, 130, 50, 176, 6, 5, "#c7bcd9", 1))
    o.append(capsule(50, 176, 46, 206, 5, 4, "#e2b9a2", 1))
    # legs (pajama pants), knees slightly bent, feet up
    o.append(capsule(92, 204, 154, 190, 13, 10, NG, 1.1))
    o.append(capsule(154, 190, 216, 204, 9.5, 7, NG, 1.1))
    o.append('<path d="M212 206 C214 196 218 186 224 178 C228 174 234 176 233 182 C232 192 228 204 226 212 C222 214 214 212 212 206Z" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M226 180 C228 178 231 178 232 180" class="ink2"/>')
    o.append('<path d="M110 200 C130 196 146 192 156 192 M170 194 C186 198 200 200 210 202" class="ink2"/>')
    # blanket kicked to the foot end
    o.append('<path d="M250 212 C246 196 254 178 270 172 C282 166 296 172 304 166 C318 160 336 166 346 176 C360 172 374 180 374 192 L374 248 C350 252 320 246 296 250 C276 252 258 248 250 244Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M270 172 C266 196 274 226 268 250 C262 226 260 196 264 176Z M304 166 C300 190 310 220 304 250 C298 222 294 190 298 168Z M346 176 C340 200 350 226 344 248 C338 224 336 200 340 178Z" fill="url(#ink-hatch)"/>'
             '<path d="M256 200 C270 190 290 188 310 196 C326 202 340 198 354 190 M260 222 C280 214 300 216 320 222" class="ink2"/>')
    o.append('<path d="M236 168 C246 162 256 162 262 168 M232 154 C246 146 262 146 272 154" fill="none" stroke="#a8412c" stroke-width="1.2"/>')
    # torso upright
    o.append(head(80, 86, .46, 8, eye="open", hair="long", sweat=True))
    o.append(f'<path d="M68 108 C60 116 56 130 55 150 C54 172 55 196 60 213 L112 213 C106 196 100 180 98 164 C97 150 100 134 98 122 C96 114 92 110 88 108 C82 112 74 112 68 108Z" fill="{NG}" stroke="#2a2018" stroke-width="1.2"/>'
             '<path d="M68 108 C60 116 56 130 55 150 C54 172 55 196 60 213 L68 213 C63 196 61 166 64 130Z" fill="url(#ink-hatch)"/>'
             '<path d="M70 109 C76 120 84 120 88 109 M86 124 C92 130 96 138 98 148" class="ink2"/>')
    # flush on face / neck / upper chest
    o.append(f'<radialGradient id="{PID}-fl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e0533f" stop-opacity=".55"/><stop offset="1" stop-color="#e0533f" stop-opacity="0"/></radialGradient>')
    o.append(f'<ellipse cx="88" cy="100" rx="26" ry="30" fill="url(#{PID}-fl)"/>')
    # near arm: hand fanning face
    o.append(capsule(80, 120, 102, 156, 7, 6, NG, 1.1))
    o.append(capsule(102, 156, 118, 118, 6, 5, "#e2b9a2", 1.1))
    o.append(hand(118, 118, .62, -100))
    o.append('<path d="M134 96 C138 100 138 106 134 110 M140 92 C146 98 146 108 140 114" fill="none" stroke="#2a2018" stroke-width=".9"/>')
    # heat waves
    for x0 in (58, 100, 150):
        o.append(f'<path d="M{x0} 70 C{x0-6} 62 {x0+6} 56 {x0} 48" fill="none" stroke="#d9473a" stroke-width="1.3" opacity=".8"/>' if x0 != 100 else '')
    o.append('<path d="M150 150 C144 142 156 136 150 128 M170 156 C164 148 176 142 170 134" fill="none" stroke="#d9473a" stroke-width="1.2" opacity=".75"/>')
    o.append('</g>')
    o.append(f'<rect x=".5" y="40.5" width="{W-1}" height="235" fill="none" stroke="#2a2018" stroke-width="1"/>')
    return "".join(o)


body = []
body.append(f'<g transform="translate(6,0)">{scene()}</g>')
body.append('<text x="193" y="20" class="lt" text-anchor="middle">凌晨三、四點：熱醒、流汗、踢被子</text><text x="193" y="35" class="le" text-anchor="middle">a 54-year-old woman woken by a hot flash</text>')
# labels on scene
body.append(lab(128, 150, "臉頸胸潮紅、出汗", None, cls="ls") )
body.append(lead([(126, 146), (96, 112)]))
body.append(lab(250, 150, "被子踢開", None, cls="ls") + lead([(276, 152), (290, 172)]))
body.append(lab(52, 268, "床單汗濕", None, cls="ls") + lead([(84, 262), (80, 216)]))
# night strip
body.append('<text x="6" y="298" class="ls">一夜的樣子 <tspan class="le">one night</tspan></text>')
body.append(strip(6, 304, 374, [(23, 23.3, "wake"), (23.3, 26.1, "sleep"), (26.1, 26.4, "wake"), (26.4, 27.6, "sleep"), (27.6, 28.3, "wake"), (28.3, 28.9, "sleep"), (28.9, 29.4, "wake"), (29.4, 30.5, "sleep")],
                  22, 31, [(22, "22"), (24, "0"), (26, "2"), (28, "4"), (30, "6")], h=13))
for t in (26.1, 27.6, 28.9):
    x = 6 + (t - 22) / 9 * 374
    body.append(f'<path d="M{x:.1f} 300 l-3 -6 h6Z" fill="#d9473a" stroke="#2a2018" stroke-width=".5"/>')
body.append('<text x="380" y="344" class="ls" text-anchor="end"><tspan style="fill:#d9473a">▼</tspan> 熱潮紅 → 醒來（下半夜多）</text>')

# ===== mechanism: hypothalamus inset
X0 = 396
M = [f'<rect x="{X0}" y="40" width="358" height="132" rx="4" class="panel"/>']
M.append(f'<text x="{X0+10}" y="58" class="lb">下視丘的體溫恆定器 <tspan class="le">hypothalamic thermostat</tspan></text>')
# small medial brain (scaled)
bx, by, bs = X0 + 6, 62, .62
outer = ("M20 90 C14 56 50 16 120 12 C180 10 232 36 244 80 C248 100 240 116 226 122 C214 126 200 124 192 120 C184 112 176 108 166 108 "
         "C150 108 140 114 130 118 C110 124 80 122 60 116 C40 112 22 104 20 90Z")
G = [f'<path d="{outer}" fill="#efe1d6" stroke="#2a2018" stroke-width="1.4"/>',
     '<path d="M64 70 C70 50 100 38 132 36 C166 34 196 46 204 66 C206 74 200 78 194 74 C186 58 164 50 136 50 C108 50 86 58 78 72 C74 78 66 78 64 70Z" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/>',
     '<ellipse cx="146" cy="80" rx="22" ry="12" fill="#e8d6c8" stroke="#2a2018" stroke-width=".9"/>',
     '<path d="M148 96 C160 92 172 96 176 104 C186 112 190 126 186 140 C184 150 186 158 188 168 L174 168 C172 156 168 150 164 142 C154 136 148 126 148 112Z" fill="#e8d6c8" stroke="#2a2018" stroke-width="1"/>',
     '<path d="M190 120 C206 112 236 116 242 130 C246 146 232 156 214 156 C200 156 190 146 188 134Z" fill="#e8d6c8" stroke="#2a2018" stroke-width="1"/>',
     '<path d="M108 88 C118 84 132 86 140 94 C138 104 130 110 120 110 C112 108 106 98 108 88Z" fill="#f6e7b0" stroke="#2a2018" stroke-width=".9"/>',
     '<ellipse cx="118" cy="120" rx="6" ry="4.5" fill="#f0c4b8" stroke="#2a2018" stroke-width=".7"/>',
     '<circle cx="112" cy="92" r="4.2" fill="#2c5d9c" stroke="#2a2018" stroke-width=".6"/>',
     '<circle cx="128" cy="104" r="4.2" fill="#d9473a" stroke="#2a2018" stroke-width=".6"/>',
     '<path d="M126 101 C122 98 118 96 116 95" fill="none" stroke="#d9473a" stroke-width="1.8" marker-end="url(#ink-arrow-red)"/>',
     '<path d="M40 40 C48 34 52 42 60 36 M90 22 C96 30 104 24 110 30 M150 20 C156 28 164 22 170 28 M200 36 C204 44 212 42 216 50" class="ink2"/>']
M.append(f'<g transform="translate({bx},{by}) scale({bs})">{"".join(G)}</g>')
def gp(x, y):
    return (round(bx + bs * x, 1), round(by + bs * y, 1))
M.append(lab(X0 + 172, 80, "視前區 體溫調節中樞", None, cls="ls") + f'<text x="{X0+172}" y="93" class="le halo">preoptic thermoregulatory centre</text>' + lead([(X0 + 170, 77), gp(112, 92)]))
M.append(lab(X0 + 172, 112, "弓狀核 KNDy 神經元", None, cls="ls") + f'<text x="{X0+172}" y="125" class="le halo">kisspeptin / neurokinin B / dynorphin</text>' + lead([(X0 + 170, 109), gp(128, 104)]))
M.append(f'<text x="{X0+172}" y="146" class="ls" style="fill:#a8412c">雌激素 ↓ → KNDy 過度活化</text>'
         f'<text x="{X0+172}" y="160" class="ls" style="fill:#a8412c">→ 把「舒適溫度帶」收窄</text>')
M.append(lab(X0 + 10, 164, "腦下垂體", None, cls="ls") + lead([(X0 + 58, 160), gp(118, 122)]))
body.append("".join(M))

# ===== graph: thermoneutral zone & core temperature
gx0, gy0, gw, gh = X0 + 36, 196, 300, 120
Gr = [f'<rect x="{X0}" y="180" width="358" height="190" rx="4" class="panel"/>']
Gr.append(f'<text x="{X0+10}" y="196" class="lb">舒適溫度帶變窄 <tspan class="le">narrowed thermoneutral zone</tspan></text>')
top, bot = gy0 + 10, gy0 + gh
# premenopause wide zone (dashed)
Gr.append(f'<rect x="{gx0}" y="{top+12}" width="{gw}" height="{gh-36}" fill="#cfdcef" opacity=".35" stroke="#3f6fa6" stroke-width=".8" stroke-dasharray="4 3"/>')
# postmenopause narrow zone
nz_hi, nz_lo = top + 46, top + 62
Gr.append(f'<rect x="{gx0}" y="{nz_hi}" width="{gw}" height="{nz_lo-nz_hi}" fill="#f6e7b0" opacity=".85" stroke="#c9962e" stroke-width=".9"/>')
Gr.append(f'<path d="M{gx0} {nz_hi} H{gx0+gw}" stroke="#d9473a" stroke-width="1.2"/><path d="M{gx0} {nz_lo} H{gx0+gw}" stroke="#2c5d9c" stroke-width="1.2"/>')
# core temp trace
pts = []
peaks = [0.35, 0.56, 0.74]
for i in range(gw + 1):
    t = i / gw
    v = 6 * math.sin(t * 2 * math.pi * 3.2) - 6 * t
    for p in peaks:
        v += 16 * math.exp(-((t - p) / .025) ** 2)
    pts.append((gx0 + i, nz_lo - 12 - v))
Gr.append('<path d="M' + " L".join(f"{a} {b:.1f}" for a, b in pts) + '" fill="none" stroke="#2a2018" stroke-width="1.5"/>')
for p in peaks:
    x = gx0 + p * gw
    Gr.append(f'<path d="M{x:.1f} {nz_hi-22} c-4 -6 0 -10 2 -14 c1 4 6 6 4 12 c-1 3 -4 4 -6 2Z" fill="#d9473a" stroke="#2a2018" stroke-width=".5"/>')
    Gr.append(f'<path d="M{x:.1f} {bot+2} V{bot+12}" stroke="#a8412c" stroke-width="1.2" marker-end="url(#ink-arrow-red)"/>')
Gr.append(f'<path d="M{gx0} {top} V{bot} H{gx0+gw}" class="ink"/>')
Gr.append(f'<text x="{gx0-6}" y="{top+6}" class="ls" text-anchor="end">核心</text><text x="{gx0-6}" y="{top+19}" class="ls" text-anchor="end">體溫</text>')
Gr.append(f'<text x="{gx0+4}" y="{nz_hi-4}" class="ls halo" style="fill:#d9473a">出汗閾值 sweating</text>')
Gr.append(f'<text x="{gx0+4}" y="{nz_lo+12}" class="ls halo" style="fill:#2c5d9c">發抖閾值 shivering</text>')
Gr.append(f'<text x="{gx0+gw-4}" y="{bot-22}" class="ls halo" text-anchor="end" style="fill:#3f6fa6">虛線框＝停經前的舒適帶（寬）</text>')
Gr.append(f'<text x="{gx0+gw-4}" y="{bot-8}" class="ls halo" text-anchor="end" style="fill:#8a6a3a">黃色帶＝停經後（很窄）</text>')
Gr.append(f'<text x="{gx0+gw/2}" y="{bot+26}" class="ls" text-anchor="middle" style="fill:#a8412c">體溫小小上升就越過出汗閾值 → 熱潮紅 → 醒來</text>')
Gr.append(f'<text x="{gx0+gw/2}" y="{bot+42}" class="le" text-anchor="middle">small rises cross the lowered threshold → flush → awakening</text>')
body.append("".join(Gr))

cap = ('<b>圖 12-A　更年期的下半夜醒：熱潮紅。</b>停經前後雌激素下降，下視丘弓狀核的 KNDy 神經元失去抑制而過度活化，使視前區體溫調節中樞的「舒適溫度帶」（出汗與發抖閾值之間）變得很窄；'
       '夜裡核心體溫只要小幅上升就越過出汗閾值，引發血管擴張、潮紅、出汗，人也跟著醒來。熱潮紅在圍停經期可同時是失眠的誘發與維持因子，處理它本身就是治療的一部分。示意圖，溫度帶寬度為誇張化表示。')

html = fig(PID, "Plate 12·A", "更年期下半夜醒：熱潮紅", "Menopausal night waking — the hot flash", 378,
           "左為約五十四歲女性凌晨三點四十分熱醒、出汗、踢開被子；右為下視丘 KNDy 神經元與舒適溫度帶變窄、核心體溫越過出汗閾值引發熱潮紅與醒來的示意", "\n".join(body), cap)
write(PID, html)
