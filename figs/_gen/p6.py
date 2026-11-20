import sys, math; sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from lib import *

PID = "pl-conditioning"
SH = "#9fb7a0"   # same green sweater both scenes: same person
W = 368


def sofa_scene():
    o = []
    # room (warm evening)
    o.append(f'<rect x="0" y="40" width="{W}" height="236" fill="#f1e2c4"/><rect x="0" y="40" width="{W}" height="236" fill="url(#ink-hatch-h)" opacity=".25"/>')
    o.append(f'<path d="M0 248 H{W} V276 H0Z" fill="#c9b48a"/><path d="M0 248 H{W} V276 H0Z" fill="url(#ink-hatch-l)"/><path d="M0 248 H{W}" class="ink"/>')
    # floor lamp glow
    o.append('<radialGradient id="pl-conditioning-lamp" cx=".5" cy=".3" r=".6"><stop offset="0" stop-color="#ffe9a8" stop-opacity=".9"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>')
    o.append('<clipPath id="pl-conditioning-cl"><rect x="0" y="40" width="368" height="236"/></clipPath><circle cx="18" cy="90" r="70" fill="url(#pl-conditioning-lamp)" clip-path="url(#pl-conditioning-cl)"/>'
             '<path d="M6 70 L30 70 L24 50 L12 50Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1"/><path d="M18 70 V246 M8 248 H28" stroke="#2a2018" stroke-width="1.6"/>')
    # TV + cabinet
    o.append('<path d="M262 206 H358 V248 H262Z" fill="#a57c55" stroke="#2a2018" stroke-width="1.1"/><path d="M310 206 V248 M268 226 H304 M316 226 H352" class="ink2"/>')
    o.append('<path d="M286 196 H334 L330 206 H290Z" fill="#3a3a3a"/><rect x="266" y="128" width="88" height="68" rx="3" fill="#2a2f36" stroke="#2a2018" stroke-width="1.2"/>'
             '<rect x="271" y="133" width="78" height="58" fill="#a9c4e6"/><path d="M271 170 C290 160 306 176 324 164 C334 158 342 162 349 160 V191 H271Z" fill="#6e93c2"/>'
             '<circle cx="330" cy="146" r="7" fill="#f6e7b0"/>')
    o.append('<path d="M266 150 L150 110 M266 176 L150 190" stroke="#cfdcef" stroke-width="1" stroke-dasharray="2 4" opacity=".9"/>')
    # wall clock
    o.append(clock(200, 82, 15, 21, 30))
    o.append('<text x="200" y="116" class="ls" text-anchor="middle">21:30</text>')
    # sofa back & seat (behind person)
    o.append('<path d="M30 248 V120 C30 100 44 92 58 96 C66 100 68 110 66 122 L60 190 L196 190 C206 190 208 204 200 208 L190 210 L190 248Z" fill="#b5473a" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M30 248 V120 C30 100 44 92 58 96 L50 100 C40 104 38 116 38 130 V248Z" fill="url(#ink-hatch)" opacity=".8"/>'
             '<path d="M62 190 C100 186 150 186 196 190" class="ink2"/><path d="M56 110 C54 140 54 170 58 188" class="ink2"/>')
    # person: legs
    o.append(capsule(100, 188, 158, 184, 13, 10, "#5c6f8a", 1.1))
    o.append(capsule(158, 184, 166, 236, 9.5, 7, "#5c6f8a", 1.1))
    o.append('<path d="M158 236 C158 244 166 248 186 247 C188 242 182 238 172 236Z" fill="#e8dcc2" stroke="#2a2018" stroke-width="1"/>')
    # torso leaning back on sofa
    o.append(f'<path d="M64 108 C78 102 92 104 98 116 C104 136 108 160 112 182 C112 196 100 202 88 200 C74 198 66 188 62 172 C58 150 58 126 64 108Z" fill="{SH}" stroke="#2a2018" stroke-width="1.2"/>'
             '<path d="M64 108 C58 126 58 150 62 172 C66 188 74 198 82 200 L78 196 C70 184 68 160 70 128Z" fill="url(#ink-hatch-l)"/>'
             '<path d="M72 112 C78 116 86 116 92 112" class="ink2"/>')
    # head resting back, dozing
    o.append(head(70, 82, .42, -28, eye="closed", hair="short", mouth="open"))
    # arm: upper arm down, forearm on lap, hand with remote drooping
    o.append(capsule(84, 116, 98, 160, 7, 6, SH, 1.1))
    o.append(capsule(98, 160, 132, 172, 6, 5, SH, 1.1))
    o.append(hand(132, 172, .6, 40))
    o.append('<rect x="138" y="190" width="18" height="6" rx="2" transform="rotate(30 147 193)" fill="#3a3a3a" stroke="#2a2018" stroke-width=".7"/>')
    # near armrest of sofa (occludes hips)
    o.append('<path d="M24 248 V176 C24 164 34 160 46 160 L112 160 C124 160 128 170 124 180 L120 186 L120 248Z" fill="#c46a58" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M24 176 C24 164 34 160 46 160 L112 160 C124 160 128 170 124 180 C110 176 60 174 30 180Z" fill="#d98f7e" stroke="#2a2018" stroke-width=".8"/>'
             '<path d="M120 186 L120 248 L110 248 L112 186Z" fill="url(#ink-hatch)"/><path d="M40 190 C60 192 90 192 110 190" class="ink2"/>'
             '<path d="M30 248 V256 M114 248 V256" stroke="#2a2018" stroke-width="3"/>')
    # Zzz
    o.append('<text x="100" y="96" class="lt" style="fill:#2c5d9c">z</text><text x="112" y="84" class="lt" style="fill:#2c5d9c;font-size:18px">Z</text><text x="128" y="70" class="lt" style="fill:#2c5d9c;font-size:22px">Z</text>')
    o.append(f'<rect x=".5" y="40.5" width="{W-1}" height="235" fill="none" stroke="#2a2018" stroke-width="1"/>')
    return "".join(o)


def bed_scene():
    o = []
    o.append(f'<rect x="0" y="40" width="{W}" height="236" fill="#c9d3e3"/><rect x="0" y="40" width="{W}" height="236" fill="url(#ink-hatch-h)" opacity=".5"/>')
    o.append(f'<path d="M0 252 H{W} V276 H0Z" fill="#9aa6b6"/><path d="M0 252 H{W} V276 H0Z" fill="url(#ink-hatch-l)"/><path d="M0 252 H{W}" class="ink"/>')
    # window dark
    o.append('<rect x="290" y="56" width="56" height="64" fill="#24334f" stroke="#2a2018" stroke-width="1"/><path d="M318 56 V120 M290 88 H346" stroke="#efe6d2" stroke-width="2.5"/>'
             '<circle cx="300" cy="66" r=".9" fill="#f6e7b0"/><circle cx="336" cy="102" r=".9" fill="#f6e7b0"/><circle cx="330" cy="70" r=".9" fill="#f6e7b0"/>')
    # headboard, mattress
    o.append('<path d="M8 252 V128 C8 118 30 114 34 124 V252" fill="#a57c55" stroke="#2a2018" stroke-width="1.3"/><path d="M8 252 V128 C8 118 30 114 34 124 V252" fill="url(#ink-hatch-l)"/>'
             f'<path d="M30 212 H{W} V236 H30Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/><path d="M30 236 H{W} V244 H30Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/><path d="M36 244 V252" stroke="#2a2018" stroke-width="3"/>')
    # bedside table with clock
    # pillow
    o.append('<path d="M30 210 C24 200 30 192 44 192 C60 190 82 190 92 194 C98 198 96 210 92 214 C74 216 46 216 30 210Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M36 208 C48 212 70 212 88 210" class="ink2"/>')
    # phone glow
    o.append('<radialGradient id="pl-conditioning-ph" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e6f1ff" stop-opacity=".95"/><stop offset="1" stop-color="#e6f1ff" stop-opacity="0"/></radialGradient>')
    o.append('<ellipse cx="78" cy="150" rx="46" ry="34" fill="url(#pl-conditioning-ph)"/>')
    # head on pillow, wide awake
    o.append(head(58, 189, .46, -90, eye="wide", hair="short"))
    o.append(f'<path d="M75 181 C80 178 86 176 92 176 C98 175 102 175 104 176 L104 213 L72 213 C70 204 71 190 75 181Z" fill="{SH}" stroke="#2a2018" stroke-width="1"/>')
    # blanket
    top = "M100 178 C110 170 124 168 138 171 C150 174 156 179 166 179 C178 179 186 174 198 175 C212 176 224 181 240 182 C270 180 300 182 368 184"
    o.append(f'<path d="{top} L368 248 C330 250 300 244 270 249 C230 252 200 245 170 249 C140 252 120 245 100 244Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M138 171 C140 196 134 222 138 247 C131 226 130 200 132 172Z" fill="url(#ink-hatch)"/><path d="M198 175 C194 200 200 226 194 247 C202 226 205 200 205 176Z" fill="url(#ink-hatch)"/>'
             '<path d="M166 180 C164 204 168 230 164 249 M240 182 C242 210 238 230 242 250 M300 183 C298 210 302 230 300 248" class="ink2"/>')
    # arms raised holding phone above face
    o.append(capsule(98, 186, 104, 150, 7, 6, SH, 1.1))
    o.append(capsule(104, 150, 82, 134, 6, 5, SH, 1.1))
    o.append(hand(82, 134, .6, 200))
    o.append('<rect x="56" y="118" width="26" height="14" rx="2.5" fill="#2a2f36" stroke="#2a2018" stroke-width="1" transform="rotate(-8 69 125)"/>'
             '<rect x="59" y="120.5" width="20" height="9" rx="1" fill="#e6f1ff" transform="rotate(-8 69 125)"/>')
    o.append('<path d="M66 134 L64 160 M74 134 L72 160" stroke="#e6f1ff" stroke-width="1" opacity=".8"/>')
    # thought bubble: clock + work papers
    bx, by = 222, 96
    o.append(f'<path d="M{bx-78} {by} C{bx-84} {by-26} {bx-50} {by-42} {bx-26} {by-34} C{bx-14} {by-52} {bx+22} {by-52} {bx+34} {by-36} '
             f'C{bx+60} {by-42} {bx+86} {by-18} {bx+76} {by+4} C{bx+90} {by+22} {bx+62} {by+42} {bx+38} {by+32} C{bx+22} {by+48} {bx-14} {by+48} {bx-28} {by+34} '
             f'C{bx-54} {by+44} {bx-88} {by+24} {bx-78} {by}Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>')
    o.append(f'<circle cx="{bx-92}" cy="{by+42}" r="5" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/><circle cx="{bx-110}" cy="{by+54}" r="3" fill="#fbf6ea" stroke="#2a2018" stroke-width=".9"/>')
    o.append(clock(bx - 40, by - 4, 17, 1, 30))
    # papers / laptop
    o.append(f'<g transform="translate({bx+2},{by-24})"><path d="M0 4 L30 0 L34 36 L4 40Z" fill="#fff" stroke="#2a2018" stroke-width=".9"/><path d="M6 4 L36 0 L40 36 L10 40Z" fill="#fff" stroke="#2a2018" stroke-width=".9"/>'
             '<path d="M14 8 L34 6 M14 14 L36 12 M15 20 L36 18 M16 26 L30 25" class="ink2"/><path d="M16 30 L24 34 L36 22" fill="none" stroke="#a8412c" stroke-width="1.2"/></g>')
    o.append(f'<text x="{bx+56}" y="{by-6}" class="lb" style="fill:#a8412c">!?</text>')
    o.append(f'<text x="{bx}" y="{by+30}" class="ls" text-anchor="middle">「只剩五小時…報告還沒寫…」</text>')
    o.append(f'<rect x=".5" y="40.5" width="{W-1}" height="235" fill="none" stroke="#2a2018" stroke-width="1"/>')
    return "".join(o)


def bed_icon(x, y, s=1.0, col="#e8d6ae"):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<path d="M0 30 V4 C0 0 6 -1 7 3 V30" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>'
            '<path d="M6 18 H52 V26 H6Z" fill="#f4eee0" stroke="#2a2018" stroke-width=".9"/>'
            '<path d="M8 17 C8 13 12 12 18 12 C22 12 24 14 23 18Z" fill="#fbf6ea" stroke="#2a2018" stroke-width=".8"/>'
            f'<path d="M22 18 C26 12 34 12 40 13 C46 14 50 15 52 18 L52 28 L22 28Z" fill="{col}" stroke="#2a2018" stroke-width=".9"/>'
            '<path d="M6 26 V31 M50 26 V31" stroke="#2a2018" stroke-width="1.6"/></g>')


body = []
body.append(f'<g transform="translate(6,0)">{sofa_scene()}</g>')
body.append(f'<g transform="translate(386,0)">{bed_scene()}</g>')
body.append('<text x="190" y="20" class="lt" text-anchor="middle">客廳沙發：看著電視就睡著</text><text x="190" y="35" class="le" text-anchor="middle">on the sofa — drifts off easily</text>')
body.append('<text x="570" y="20" class="lt" text-anchor="middle" style="fill:#a8412c">一躺上床：反而清醒</text><text x="570" y="35" class="le" text-anchor="middle">in bed — wide awake, phone, worrying</text>')

# ===== conditioning diagram
Y = 300
D = []
D.append(f'<text x="8" y="{Y}" class="lt">古典制約：床怎麼變成「清醒的訊號」</text><text x="262" y="{Y}" class="le">classical conditioning of the bed</text>')
boxes = [(8, "① 原本", "床 → 睡意", "bed → sleepiness", "#cfdcef"),
         (196, "② 反覆配對（數十個夜晚）", "床 ＋ 翻來覆去、滑手機、擔心", "bed + wakefulness, worry", "#f6e7b0"),
         (384, "③ 制約形成", "床 → 清醒、焦慮", "bed alone → arousal", "#f0c4b8"),
         (572, "④ 刺激控制：重新配對", "床 → 睡意", "bed → sleep again", "#cfdcef")]
for i, (x, t, zh, en, col) in enumerate(boxes):
    D.append(f'<rect x="{x}" y="{Y+12}" width="180" height="104" rx="5" fill="{col}" fill-opacity=".45" stroke="#2a2018" stroke-width=".9"/>')
    D.append(f'<text x="{x+90}" y="{Y+30}" class="lb" text-anchor="middle">{t}</text>')
    D.append(bed_icon(x + 12, Y + 42, 1.0))
    D.append(f'<text x="{x+90}" y="{Y+98}" class="ls" text-anchor="middle">{zh}</text><text x="{x+90}" y="{Y+111}" class="le" text-anchor="middle">{en}</text>')
    if i < 3:
        D.append(f'<path d="M{x+181} {Y+64} H{x+194}" stroke="#2a2018" stroke-width="1.4" marker-end="url(#ink-arrow)"/>')
# icons right of beds
# 1: Zzz
D.append(f'<text x="96" y="{Y+70}" class="lt" style="fill:#2c5d9c">z Z</text>')
# 2: phone + worry
D.append(f'<rect x="270" y="{Y+46}" width="14" height="24" rx="2.5" fill="#2a2f36" stroke="#2a2018" stroke-width=".8"/><rect x="272" y="{Y+49}" width="10" height="17" fill="#e6f1ff"/>'
         f'<text x="296" y="{Y+64}" class="lt" style="fill:#a8412c">?!</text>'
         f'<text x="322" y="{Y+56}" class="ls">× N 夜</text>')
# 3: arousal: heart + eye
D.append(f'<path d="M466 {Y+52} c-6 -8 -18 -2 -12 8 l12 12 l12 -12 c6 -10 -6 -16 -12 -8Z" fill="#d9473a" stroke="#2a2018" stroke-width=".8"/>'
         f'<path d="M488 {Y+58} C494 {Y+50} 506 {Y+50} 512 {Y+58} C506 {Y+66} 494 {Y+66} 488 {Y+58}Z" fill="#fff" stroke="#2a2018" stroke-width=".9"/><circle cx="500" cy="{Y+58}" r="3.4" fill="#3a2a1c"/>'
         f'<text x="520" y="{Y+56}" class="ls">心跳↑</text><text x="520" y="{Y+70}" class="ls">腦子轉</text>')
# 4: stimulus control rules
D.append(f'<text x="652" y="{Y+50}" class="ls">睏了才上床</text><text x="652" y="{Y+64}" class="ls">睡不著就</text><text x="652" y="{Y+78}" class="ls" style="fill:#2c5d9c;font-weight:700">起身離床</text>')
D.append(f'<path d="M640 {Y+82} C630 {Y+92} 616 {Y+90} 610 {Y+80}" fill="none" stroke="#2c5d9c" stroke-width="1.2" marker-end="url(#ink-arrow-blue)"/>')
D.append(f'<path d="M662 {Y+122} C560 {Y+146} 300 {Y+146} 290 {Y+122}" fill="none" stroke="#2c5d9c" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#ink-arrow-blue)"/>')
D.append(f'<text x="476" y="{Y+164}" class="ls halo" text-anchor="middle" style="fill:#2c5d9c">拆掉「床＝清醒」的連結，讓床只和睡覺配對 <tspan class="le">extinction &amp; re-pairing</tspan></text>')
body.append("".join(D))

cap = ('<b>圖 4-B　床變成「清醒的地方」。</b>同一個人，在客廳沙發看電視會打瞌睡，一走進臥室躺上床卻清醒：反覆在床上翻來覆去、看手機、擔心明天，大腦把「床」學成了「開始焦慮」的訊號（古典制約）。'
       '刺激控制法——只在想睡時上床、睡不著就起身離床、床只用來睡覺——就是把這個連結重新訓練回來，是 CBT-I 的核心零件之一。示意圖。')

html = fig(PID, "Plate 4·B", "床變成清醒的地方：制約", "Conditioned arousal — when the bed becomes a cue for wakefulness", 472,
           "左圖男子在客廳沙發看電視打瞌睡，右圖同一人躺在床上滑手機、清醒擔憂；下方為古典制約與刺激控制的四格示意", "\n".join(body), cap)
write(PID, html)
