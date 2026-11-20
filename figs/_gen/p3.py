import sys, math; sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from lib import *

PID = "pl-rls-rbd"
PJ = "#cfdcef"   # pajama
PJ2 = "#b9cbe4"


def walker(x, y, s=1.0):
    """small walking figure facing right; feet at (x,y)"""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    # far limbs (darker)
    o.append(capsule(-4, -96, 4, -84, 3.2, 2.8, PJ2, .8))
    o.append(capsule(4, -84, 11, -73, 2.8, 2.2, PJ2, .8))
    o.append('<ellipse cx="12.5" cy="-71" rx="2.6" ry="3" fill="#dcae93" stroke="#2a2018" stroke-width=".7"/>')
    o.append(capsule(-2, -64, -10, -34, 5, 4, PJ2, .8))
    o.append(capsule(-10, -34, -18, -6, 4, 3, PJ2, .8))
    o.append('<path d="M-21 -7 C-18 -3 -14 -1 -8 0 C-8 -3 -12 -5 -16 -8Z" fill="#7a5a3e" stroke="#2a2018" stroke-width=".8"/>')
    # torso
    o.append('<path d="M-8 -98 C-2 -101 6 -100 9 -96 C11 -88 10 -76 9 -64 C4 -60 -4 -60 -9 -64 C-10 -76 -11 -88 -8 -98Z" fill="' + PJ + '" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M-6 -66 C-8 -78 -8 -88 -6 -96" class="ink2"/><path d="M-9 -64 C-10 -76 -11 -88 -8 -98 L-5 -97 C-7 -88 -7 -76 -6 -64Z" fill="url(#ink-hatch)"/>')
    # near leg
    o.append(capsule(2, -64, 10, -34, 5.2, 4.2, PJ, 1))
    o.append(capsule(10, -34, 12, -5, 4.2, 3.2, PJ, 1))
    o.append('<path d="M8 -6 C9 -1 14 0 24 0 C24 -3 20 -5 15 -7Z" fill="#7a5a3e" stroke="#2a2018" stroke-width=".8"/>')
    o.append('<path d="M4 -48 C6 -44 8 -40 9 -36" class="ink2"/>')
    # near arm (swings back)
    o.append(capsule(0, -95, -6, -80, 3.4, 3, PJ, 1))
    o.append(capsule(-6, -80, -8, -66, 3, 2.4, PJ, 1))
    o.append('<ellipse cx="-8.5" cy="-63" rx="2.6" ry="3.2" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width=".7"/>')
    o.append('</g>')
    o.append(head(x + 2 * s, y - 108 * s, .15 * s, 0, eye="open", hair="short"))
    return "".join(o)


def rls():
    o = []
    # mattress & blanket edge
    o.append('<path d="M6 262 H372 V286 H6Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M6 286 H372 V294 H6Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>')
    leg = ("M0 196 C30 192 56 190 72 192 C82 192 88 196 92 200 C140 206 210 216 262 224 C280 210 300 190 316 172 "
           "C322 164 330 162 334 168 C336 174 332 182 326 188 C316 200 300 220 290 238 C284 250 278 260 268 264 "
           "C258 266 250 264 246 258 C240 252 232 250 222 252 C200 256 180 262 150 264 C120 266 96 262 80 256 C64 252 40 252 0 254Z")
    # far leg: same outline, knee drawn up a little (restless), behind
    o.append(f'<g transform="translate(-14,-12)"><path d="{leg}" fill="#dcae93" stroke="#2a2018" stroke-width="1"/>'
             f'<path d="{leg}" fill="url(#ink-hatch-l)"/></g>')
    o.append(f'<clipPath id="pl-rls-rbd-leg"><path d="{leg}"/></clipPath>')
    o.append(f'<path d="{leg}" fill="url(#ink-vol-flesh)"/>')
    o.append('<g clip-path="url(#pl-rls-rbd-leg)">')
    # tibia (anterior) and fibula
    o.append('<path d="M84 206 C96 202 108 206 112 208 C160 212 210 220 256 227 C261 230 260 236 254 236 C210 230 160 224 112 220 C100 222 88 218 84 212Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M120 214 C170 218 210 224 250 230" fill="none" stroke="#2a2018" stroke-width=".5" stroke-dasharray="1.5 2"/>'
             '<path d="M104 230 C150 232 200 236 252 242 L253 246 C200 241 150 236 104 234Z" fill="#efe6d2" stroke="#2a2018" stroke-width=".8"/>')
    # soleus (deep)
    o.append('<path d="M100 238 C140 238 180 242 216 248 C226 250 228 254 222 256 C190 258 150 262 120 262 C104 260 96 250 100 238Z" fill="#c46a58" stroke="#2a2018" stroke-width=".9"/>')
    for i in range(8):
        x = 108 + i * 14
        o.append(f'<path d="M{x} 240 C{x+6} 248 {x+12} 254 {x+16} 260" fill="none" stroke="#7a2d22" stroke-width=".5" stroke-opacity=".8"/>')
    # gastrocnemius (superficial) from femoral condyles to Achilles
    o.append('<path d="M60 238 C76 236 92 240 108 248 C130 256 160 258 196 256 C206 255 214 254 222 253 L222 262 C200 264 170 266 140 266 C110 266 86 262 70 256 C60 252 56 244 60 238Z" fill="#b5473a" stroke="#2a2018" stroke-width="1.1"/>')
    for i in range(14):
        x = 64 + i * 11
        o.append(f'<path d="M{x} 242 C{x+10} 250 {x+18} 256 {x+26} 264" fill="none" stroke="#5e1f16" stroke-width=".55" stroke-opacity=".75"/>')
    o.append('<path d="M74 252 C110 260 150 262 200 260" fill="none" stroke="#f4c9bd" stroke-width="1.2" opacity=".8"/>')
    # Achilles tendon & calcaneus
    o.append('<path d="M196 255 C214 252 232 250 250 248 L254 256 C236 258 216 260 196 262Z" fill="#f6e7b0" stroke="#2a2018" stroke-width=".9"/>'
             '<path d="M204 257 H248" class="ink2"/>')
    o.append('<path d="M250 242 C262 238 276 242 280 250 C282 258 276 264 266 264 C256 264 248 256 250 242Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1"/>')
    o.append('<ellipse cx="92" cy="206" rx="9" ry="6" fill="#efe6d2" stroke="#2a2018" stroke-width=".8"/>')
    o.append('<path d="M272 230 C284 214 298 196 314 178 M280 236 C292 220 306 202 320 184" fill="none" stroke="#c9b48a" stroke-width="2" stroke-linecap="round" opacity=".8"/>')
    o.append('</g>')
    o.append(f'<path d="{leg}" class="ink3"/>')
    o.append('<path d="M326 172 C328 168 332 168 333 171 M322 178 C325 175 329 176 330 180" class="ink2"/><path d="M254 236 C258 234 262 236 262 240" class="ink2"/>')
    # creeping sensation - wavy worms inside calf
    import random
    random.seed(4)
    for (cx, cy) in [(96, 254), (134, 258), (172, 256), (120, 246), (158, 248), (196, 250)]:
        d = f"M{cx-12} {cy}"
        for k in range(6):
            d += f" q2 {-3 if k%2==0 else 3} 4 0"
        o.append(f'<path d="{d}" fill="none" stroke="#f6e7b0" stroke-width="2.6" stroke-linecap="round"/>')
        o.append(f'<path d="{d}" fill="none" stroke="#c9962e" stroke-width="1.2" stroke-linecap="round"/>')
    # blanket over thighs (kicked down, bunched)
    o.append('<path d="M-2 160 C14 150 30 156 40 166 C52 160 64 166 66 180 C74 196 70 226 74 258 C76 274 70 292 62 296 L-2 296Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M40 166 C36 190 44 230 40 296 L50 296 C54 250 50 200 52 170Z" fill="url(#ink-hatch)"/>'
             '<path d="M66 180 C60 200 62 240 60 296 L66 296 C72 270 72 220 70 190Z" fill="url(#ink-hatch-d)" opacity=".7"/>'
             '<path d="M14 156 C12 200 18 240 14 296 M26 158 C30 200 24 250 28 296 M44 180 C50 186 58 186 64 182" class="ink2"/>')
    # motion marks for urge to move
    o.append('<path d="M342 160 C350 156 352 166 360 162 M340 178 C348 174 350 184 358 180 M334 196 C342 192 344 202 352 198" fill="none" stroke="#a8412c" stroke-width="1.1"/>')
    return "".join(o)


def rls_chart(x, y):
    """mini chart: symptom intensity over 24h (worse evening/night)"""
    o = [f'<g transform="translate({x},{y})">']
    w, h = 150, 46
    o.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fbf6ea" stroke="#bfae8a" stroke-width=".8"/>')
    o.append(f'<rect x="{w*14/24:.0f}" y="0" width="{w*10/24:.0f}" height="{h}" fill="#cfdcef" opacity=".6"/>')
    pts = []
    for i in range(0, w + 1, 2):
        t = 8 + i / w * 24
        v = math.exp(-((t - 24.5) / 3.6) ** 2)
        pts.append((i, h - 4 - v * (h - 10)))
    o.append('<path d="M' + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + '" fill="none" stroke="#a8412c" stroke-width="1.6"/>')
    for t, lb in [(8, "8"), (14, "14"), (20, "20"), (26, "2"), (32, "8")]:
        xx = (t - 8) / 24 * w
        o.append(f'<line x1="{xx:.1f}" y1="{h}" x2="{xx:.1f}" y2="{h+3}" stroke="#2a2018" stroke-width=".7"/><text x="{xx:.1f}" y="{h+13}" class="ls" text-anchor="middle">{lb}</text>')
    o.append(f'<text x="2" y="-5" class="ls">症狀強度：傍晚、夜間最重 <tspan class="le">circadian</tspan></text>')
    o.append('</g>')
    return "".join(o)


def rbd():
    o = []
    X = 392
    # pillows
    o.append(f'<path d="M{X+8} 214 C{X+2} 200 {X+10} 190 {X+26} 190 C{X+46} 188 {X+70} 188 {X+80} 194 C{X+86} 200 {X+84} 212 {X+78} 216 C{X+58} 220 {X+30} 220 {X+8} 214Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>')
    # headboard, mattress
    o.append(f'<path d="M{X} 296 V138 C{X} 128 {X+22} 124 {X+26} 134 V296" fill="#a57c55" stroke="#2a2018" stroke-width="1.3"/>'
             f'<path d="M{X} 296 V138 C{X} 128 {X+22} 124 {X+26} 134 V296" fill="url(#ink-hatch-l)"/>'
             f'<path d="M{X+20} 262 H760 V286 H{X+20}Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/>'
             f'<path d="M{X+20} 286 H760 V294 H{X+20}Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>')
    # --- partner (behind), propped on elbow, recoiling toward headboard
    o.append(f'<path d="M{X+30} 182 C{X+40} 168 {X+60} 164 {X+76} 170 C{X+88} 182 {X+92} 210 {X+90} 240 L{X+40} 240 C{X+32} 220 {X+28} 198 {X+30} 182Z" fill="#f0c4b8" stroke="#2a2018" stroke-width="1.1"/>'
             f'<path d="M{X+46} 178 C{X+52} 186 {X+62} 188 {X+70} 182" class="ink2"/>'
             f'<path d="M{X+30} 182 C{X+28} 198 {X+32} 220 {X+40} 240 L{X+48} 240 C{X+40} 220 {X+38} 198 {X+40} 184Z" fill="url(#ink-hatch)"/>')
    o.append(head(X + 56, 146, .42, -6, eye="wide", hair="long", mouth="open"))
    # partner raised forearm + open hand (defensive)
    o.append(capsule(X + 74, 178, X + 96, 160, 5, 4, "#f0c4b8", 1))
    o.append(hand(X + 96, 160, .62, -62))
    # --- dreamer (near), lying, head on pillow, eyes closed, mouth open shouting
    o.append(f'<path d="M{X+72} 210 C{X+82} 204 {X+96} 202 {X+112} 202 L{X+118} 262 L{X+70} 262 C{X+66} 246 {X+66} 224 {X+72} 210Z" fill="{PJ}" stroke="#2a2018" stroke-width="1.1"/>')
    o.append(head(X + 52, 218, .46, -96, eye="closed", hair="short", mouth="open"))
    # blanket over dreamer with kicking legs
    top = f"M{X+108} 206 C{X+130} 196 {X+150} 198 {X+170} 206 C{X+190} 212 {X+204} 210 {X+224} 204 C{X+244} 198 {X+262} 186 {X+280} 176 C{X+292} 172 {X+300} 180 {X+304} 190 C{X+320} 196 {X+340} 196 {X+368} 194"
    o.append(f'<path d="{top} L{X+372} 300 C{X+340} 302 {X+300} 296 {X+270} 300 C{X+230} 304 {X+190} 296 {X+150} 300 C{X+130} 302 {X+114} 298 {X+106} 296Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>')
    o.append(f'<path d="M{X+170} 206 C{X+166} 240 {X+172} 270 {X+168} 300 C{X+160} 270 {X+158} 240 {X+162} 208Z" fill="url(#ink-hatch)"/>'
             f'<path d="M{X+280} 176 C{X+270} 220 {X+276} 260 {X+272} 300 C{X+264} 260 {X+262} 220 {X+268} 182Z" fill="url(#ink-hatch)"/>'
             f'<path d="M{X+130} 202 C{X+132} 240 {X+128} 270 {X+132} 300 M{X+220} 206 C{X+216} 240 {X+222} 270 {X+218} 300 M{X+320} 196 C{X+322} 240 {X+318} 270 {X+322} 300" class="ink2"/>')
    o.append(f'<path d="M{X+270} 164 C{X+280} 156 {X+292} 156 {X+300} 162 M{X+266} 154 C{X+280} 144 {X+296} 146 {X+306} 154" fill="none" stroke="#a8412c" stroke-width="1.1"/>')
    # dreamer's punching arm: upper arm up from shoulder, forearm toward partner side / up
    o.append(capsule(X + 100, 212, X + 128, 176, 7, 6, PJ, 1.1))
    o.append(capsule(X + 128, 176, X + 150, 136, 6, 5, PJ, 1.1))
    o.append(f'<path d="M{X+120} 186 C{X+124} 182 {X+126} 178 {X+128} 174 M{X+138} 160 C{X+140} 154 {X+143} 148 {X+146} 144" class="ink2"/>')
    o.append(fist(X + 150, 136, .95, -62))
    o.append(f'<path d="M{X+168} 116 l8 -6 M{X+174} 126 l10 -2 M{X+162} 108 l3 -9" stroke="#a8412c" stroke-width="1.6" stroke-linecap="round"/>')
    o.append(f'<path d="M{X+112} 130 C{X+118} 122 {X+128} 114 {X+140} 110" fill="none" stroke="#a8412c" stroke-width="1" stroke-dasharray="2 2"/>')
    # dream bubble
    bx, by = X + 250, 92
    o.append(f'<path d="M{bx-70} {by} C{bx-74} {by-22} {bx-46} {by-34} {bx-24} {by-28} C{bx-14} {by-44} {bx+18} {by-44} {bx+28} {by-30} '
             f'C{bx+52} {by-36} {bx+74} {by-16} {bx+66} {by+2} C{bx+80} {by+18} {bx+56} {by+36} {bx+34} {by+28} C{bx+20} {by+42} {bx-12} {by+42} {bx-24} {by+30} '
             f'C{bx-48} {by+40} {bx-78} {by+22} {bx-70} {by}Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>')
    for (cx, cy, r) in [(X + 120, 190, 2.5), (X + 140, 172, 0)]:
        pass
    o.append(f'<circle cx="{bx-86}" cy="{by+44}" r="4" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/><circle cx="{bx-98}" cy="{by+60}" r="2.6" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/>')
    o.append(f'<text x="{bx}" y="{by-6}" class="lb" text-anchor="middle">夢裡有人追打</text><text x="{bx}" y="{by+10}" class="ls" text-anchor="middle">→ 揮拳、踢腳、大叫</text>'
             f'<text x="{bx}" y="{by+24}" class="le" text-anchor="middle">dream enactment</text>')
    return "".join(o)


def emg(x, y):
    o = [f'<g transform="translate({x},{y})">']
    w = 150
    import random
    random.seed(7)
    def tr(yy, bursts):
        pts = []
        for i in range(0, w + 1):
            amp = .5
            for (a, b, A) in bursts:
                if a <= i <= b:
                    amp = A
            pts.append((i, yy + random.uniform(-amp, amp)))
        return '<path d="M' + " L".join(f"{a} {b:.1f}" for a, b in pts) + '" fill="none" stroke="#2a2018" stroke-width=".8"/>'
    # REM bar
    o.append(f'<rect x="0" y="0" width="{w}" height="10" fill="#3f6fa6" fill-opacity=".85"/><text x="{w/2}" y="8.5" class="ls" text-anchor="middle" style="fill:#fbf6ea;font-size:9.5px">REM 睡眠期</text>')
    o.append(tr(30, []))
    o.append(tr(66, [(30, 46, 9), (80, 92, 6), (118, 150, 11), (176, 186, 7)]))
    o.append(f'<text x="-6" y="34" class="lb halo" text-anchor="end">正常</text><text x="-6" y="47" class="le halo" text-anchor="end">atonia</text>')
    o.append(f'<text x="-6" y="70" class="lb halo" text-anchor="end" style="fill:#a8412c">RBD</text><text x="-6" y="83" class="le halo" text-anchor="end">no atonia</text>')
    o.append(f'<text x="{w+8}" y="34" class="ls">下巴肌電平坦：</text><text x="{w+8}" y="47" class="ls">肌肉被「關掉」</text>')
    o.append(f'<text x="{w+8}" y="66" class="ls" style="fill:#a8412c">肌電一陣陣爆發：</text><text x="{w+8}" y="79" class="ls" style="fill:#a8412c">夢裡的動作做出來</text>')
    o.append('</g>')
    return "".join(o)


body = []
# titles
body.append('<text x="186" y="18" class="lt" text-anchor="middle">不寧腿症候群 RLS</text><text x="186" y="34" class="le" text-anchor="middle">Restless legs syndrome — awake, evening, at rest</text>')
body.append('<text x="576" y="18" class="lt" text-anchor="middle">REM 睡眠行為障礙 RBD</text><text x="576" y="34" class="le" text-anchor="middle">REM sleep behaviour disorder — asleep, dreaming</text>')
body.append('<line x1="381" y1="8" x2="381" y2="420" class="panel"/>')
body.append(rls())
body.append(rls_chart(14, 62))
body.append('<rect x="214" y="44" width="148" height="100" rx="3" fill="#fbf6ea" stroke="#bfae8a" stroke-width=".8"/>')
body.append('<path d="M222 132 H354" class="ink2"/>')
body.append(walker(276, 132, .82))
body.append('<path d="M300 92 C312 90 318 96 316 104" fill="none" stroke="#2c5d9c" stroke-width="1.2" marker-end="url(#ink-arrow-blue)"/>')
body.append(lab(318, 74, "起來走", None) + '<text x="318" y="88" class="ls halo">就舒服</text><text x="318" y="101" class="le halo">relief</text>')
# leg labels
body.append(lab(8, 322, "腓腸肌", "Gastrocnemius", two=True) + lead([(54, 318), (84, 256)]))
body.append(lab(104, 322, "比目魚肌", "Soleus", two=True) + lead([(150, 318), (150, 250)]))
body.append(lab(198, 322, "阿基里斯腱", "Achilles tendon", two=True) + lead([(250, 318), (226, 256)]))
body.append(lab(296, 322, "脛骨", "Tibia", two=True) + lead([(312, 318), (200, 224)]))
body.append('<text x="8" y="362" class="lb" style="fill:#c9962e">≈≈ 小腿深處「蟲爬、酸麻、說不出的難受」</text>'
            '<text x="8" y="376" class="le">deep creeping / crawling discomfort with an urge to move</text>')
body.append('<text x="8" y="396" class="ls">休息、躺下時加重　·　活動、走路就緩解　·　傍晚夜間最明顯</text>')
body.append('<text x="8" y="410" class="ls">病人是「清醒著」睡不著；抗組織胺會讓它更糟</text>')
# RBD
body.append(rbd())
body.append(lab(398, 66, "伴侶被打到、嚇醒", None) + '<text x="398" y="80" class="le halo">bed partner recoils</text>')
body.append(lead([(430, 84), (446, 120)]))
body.append(lab(600, 244, "閉著眼：人還在睡", None, cls="ls") + lead([(596, 240), (442, 208)]))
body.append(emg(468, 340))
body.append('<text x="468" y="326" class="ls">PSG：REM 期的下巴肌電圖 <tspan class="le">chin EMG during REM</tspan></text>')

cap = ('<b>圖 3-C　兩個長得像失眠的病。</b>左：不寧腿症候群——病人是醒著的，傍晚躺下休息時小腿深處（腓腸肌、比目魚肌一帶）出現蟲爬、酸麻般難以形容的不適與想動的衝動，起來走就緩解；'
       '症狀有明顯的晝夜節律。右：REM 睡眠行為障礙——病人是睡著的，在 REM 期把夢「演」出來，揮拳、踢腳、大叫，常傷到伴侶；'
       'PSG 上可見 REM 期本該消失的肌肉張力仍在（下巴肌電爆發）。RBD 常與神經退化性疾病有關、SSRI/SNRI 也可能誘發，應轉神經科或睡眠中心。示意圖。')

html = fig(PID, "Plate 3·C", "不寧腿與 REM 睡眠行為障礙：長得像失眠的兩個病", "Restless legs & REM sleep behaviour disorder", 432,
           "左為躺在床上的小腿與其肌肉解剖，小腿深處有蟲爬感，插圖為起身走路緩解；右為男子在睡夢中揮拳、伴侶驚嚇退縮，下方為 REM 期下巴肌電比較", "\n".join(body), cap)
write(PID, html)
