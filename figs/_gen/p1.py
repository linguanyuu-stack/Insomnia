import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from lib import *

PID = "pl-patterns"
W = 236  # panel width


def room(variant):
    """room background, window, bed frame (panel local coords)"""
    o = []
    # wall
    o.append(f'<rect x="0" y="44" width="{W}" height="222" fill="#d5dce8"/>')
    o.append(f'<rect x="0" y="44" width="{W}" height="222" fill="url(#ink-hatch-h)" opacity=".55"/>')
    # floor
    o.append(f'<path d="M0 252 H{W} V266 H0Z" fill="#b8a98c"/><path d="M0 252 H{W} V266 H0Z" fill="url(#ink-hatch-l)"/>'
             f'<path d="M0 252 H{W}" class="ink"/>')
    # window (right upper)
    wx, wy, ww, wh = (150, 58, 70, 74)
    o.append(f'<rect x="{wx-6}" y="{wy-6}" width="{ww+12}" height="{wh+14}" fill="#efe6d2" stroke="#2a2018" stroke-width=".9"/>')
    sky = "#24334f" if variant != "c" else "#1f2d48"
    o.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="{sky}" stroke="#2a2018" stroke-width="1"/>')
    # stars / moon
    for sx, sy in [(160, 70), (178, 64), (205, 76), (168, 96), (212, 110), (190, 92), (157, 120)]:
        o.append(f'<circle cx="{sx}" cy="{sy}" r=".9" fill="#f6e7b0"/>')
    mx, my = {"a": (200, 78), "b": (184, 70), "c": (168, 112)}[variant]
    o.append(f'<path d="M{mx} {my-8} a8 8 0 1 0 6 13 a6.5 6.5 0 1 1 -6 -13Z" fill="#f6e7b0" stroke="#2a2018" stroke-width=".6"/>')
    if variant == "c":  # still dark: faint horizon of rooftops
        o.append(f'<path d="M{wx} {wy+wh} V{wy+wh-10} h10 v-6 h8 v8 h14 v-12 h9 v10 h12 v-5 h17 V{wy+wh}Z" fill="#141c2c"/>')
    o.append(f'<path d="M{wx+ww/2} {wy} V{wy+wh} M{wx} {wy+wh/2} H{wx+ww}" stroke="#efe6d2" stroke-width="3"/>'
             f'<path d="M{wx+ww/2} {wy} V{wy+wh} M{wx} {wy+wh/2} H{wx+ww}" class="ink2"/>')
    # curtains
    o.append(f'<path d="M{wx-12} {wy-10} C{wx-4} {wy+20} {wx-10} {wy+60} {wx-2} {wy+92} L{wx-16} {wy+92} C{wx-20} {wy+50} {wx-16} {wy+20} {wx-20} {wy-10}Z" fill="#c9a77f" stroke="#2a2018" stroke-width=".8"/>'
             f'<path d="M{wx-15} {wy-6} C{wx-12} {wy+30} {wx-14} {wy+60} {wx-9} {wy+90}" class="ink2"/>'
             f'<path d="M{wx+ww+12} {wy-10} C{wx+ww+4} {wy+20} {wx+ww+10} {wy+60} {wx+ww+2} {wy+92} L{wx+ww+16} {wy+92} C{wx+ww+20} {wy+50} {wx+ww+16} {wy+20} {wx+ww+20} {wy-10}Z" fill="#c9a77f" stroke="#2a2018" stroke-width=".8"/>'
             f'<path d="M{wx+ww+15} {wy-6} C{wx+ww+12} {wy+30} {wx+ww+14} {wy+60} {wx+ww+9} {wy+90}" class="ink2"/>'
             f'<path d="M{wx-24} {wy-10} H{wx+ww+24}" stroke="#2a2018" stroke-width="2"/>')
    # headboard
    o.append('<path d="M8 252 V128 C8 118 30 114 34 124 V252" fill="#a57c55" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M8 252 V128 C8 118 30 114 34 124 V252" fill="url(#ink-hatch-l)"/>'
             '<path d="M14 136 V246 M28 136 V246" class="ink2"/>')
    # mattress + frame
    o.append(f'<path d="M30 212 H{W+10} V236 H30Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/>'
             f'<path d="M30 236 H{W+10} V244 H30Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>'
             f'<path d="M36 244 V252" stroke="#2a2018" stroke-width="3"/>')
    return "".join(o)


def pillow():
    return ('<path d="M30 210 C24 200 30 192 44 192 C60 190 82 190 92 194 C98 198 96 210 92 214 C74 216 46 216 30 210Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
            '<path d="M36 208 C48 212 70 212 88 210 M40 197 C46 200 50 204 52 206 M84 196 C80 200 79 204 80 208" class="ink2"/>'
            '<path d="M30 210 C46 216 74 216 92 214 C80 212 52 212 38 206Z" fill="url(#ink-hatch-l)"/>')


def lying(variant):
    o = []
    o.append(pillow())
    rot = {"a": -90, "c": -76}[variant]
    hx, hy = (58, 189)
    o.append(head(hx, hy, .46, rot, eye="open", hair="short" if variant == "a" else "long"))
    # pajama shoulder / collar area
    o.append('<path d="M75 181 C80 178 86 176 92 176 C98 175 102 175 104 176 L104 213 L72 213 C70 204 71 190 75 181Z" fill="#cfdcef" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M78 182 C84 188 90 189 98 188 M76 196 C80 200 84 206 84 213" class="ink2"/><path d="M72 213 C72 204 74 198 80 194 L82 213Z" fill="url(#ink-hatch-l)"/>')
    # blanket (runs out of frame to the right)
    top = "M100 178 C110 170 124 168 138 171 C150 174 156 179 166 179 C178 179 186 174 198 175 C212 176 224 181 240 182"
    o.append(f'<path d="{top} L240 248 C220 250 200 244 180 249 C160 252 140 245 120 249 C110 250 104 247 100 244Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>')
    o.append('<path d="M138 171 C140 196 134 222 138 247 C131 226 130 200 132 172Z" fill="url(#ink-hatch)"/>'
             '<path d="M198 175 C194 200 200 226 194 247 C202 226 205 200 205 176Z" fill="url(#ink-hatch)"/>'
             '<path d="M166 180 C164 204 168 230 164 249" class="ink2"/>'
             '<path d="M120 249 C122 230 116 210 118 186 M152 177 C154 200 150 226 154 250 M182 177 C184 200 180 224 182 248 M216 178 C218 200 214 226 218 248" class="ink2"/>'
             '<path d="M104 213 C130 216 170 214 240 214" stroke="#2a2018" stroke-width=".5" stroke-dasharray="2 2" fill="none" opacity=".45"/>')
    # turned-down sheet edge (narrow band)
    o.append('<path d="M98 180 C102 174 108 170 114 169 C112 196 114 222 112 248 C106 248 101 246 98 244Z" fill="#f7f1e2" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M106 174 C104 200 107 224 105 246" class="ink2"/><path d="M98 180 C100 206 98 230 98 244 L103 246 C104 222 102 200 103 176Z" fill="url(#ink-hatch-l)"/>')
    # forearm resting on top of blanket, hand on abdomen
    o.append('<path d="M110 176 C120 172 132 170 144 170 L146 179 C134 180 122 182 112 186Z" fill="#cfdcef" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M116 180 C126 177 134 176 142 175" class="ink2"/>')
    o.append(hand(144, 174, .66, 8))
    return "".join(o)


def sitting():
    o = [pillow()]
    o.append(head(80, 86, .46, 16, eye="open", hair="short"))
    # torso upright, slightly slumped, back on pillow
    o.append('<path d="M68 108 C60 116 56 130 55 150 C54 172 55 196 60 213 L112 213 C106 196 100 180 98 164 C97 150 100 134 98 122 C96 114 92 110 88 108 C82 112 74 112 68 108Z" fill="#cfdcef" stroke="#2a2018" stroke-width="1.2"/>'
             '<path d="M68 108 C60 116 56 130 55 150 C54 172 55 196 60 213 L68 213 C63 196 61 166 64 130Z" fill="url(#ink-hatch)"/>'
             '<path d="M70 109 C76 118 84 118 88 109 M79 116 L80 132 M86 122 C92 128 96 136 98 146" class="ink2"/>'
             '<circle cx="80" cy="124" r=".9" fill="#2a2018"/><circle cx="80.6" cy="138" r=".9" fill="#2a2018"/>')
    # blanket over legs, knees raised
    o.append('<path d="M86 200 C100 190 116 156 140 148 C156 144 166 160 182 182 C194 196 214 196 240 194 L240 248 C220 250 200 244 180 249 C160 252 140 245 120 249 C104 251 92 247 86 244Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M140 148 C134 180 130 214 128 248 C124 216 124 182 136 150Z" fill="url(#ink-hatch)"/>'
             '<path d="M164 164 C172 196 174 226 180 248 C168 226 164 196 158 158Z" fill="url(#ink-hatch-l)"/>'
             '<path d="M150 148 C152 180 152 214 150 248 M206 196 C208 214 204 232 208 246 M112 176 C108 200 112 224 108 246 M226 196 C228 214 224 232 228 246" class="ink2"/>')
    # near arm: upper arm down from shoulder, forearm across knees
    o.append('<path d="M70 116 C82 112 92 120 92 134 C92 148 94 158 98 166 C110 160 124 152 136 146 L141 156 C128 164 114 174 100 178 C90 180 84 174 80 162 C76 148 72 134 74 120Z" fill="#cfdcef" stroke="#2a2018" stroke-width="1.1"/>'
             '<path d="M82 138 C84 150 88 162 94 170 M106 170 C116 164 126 158 136 152" class="ink2"/>')
    o.append(hand(137, 149, .64, 34))
    o.append(hand(146, 140, .58, 58, fill="#dcae93"))
    return "".join(o)


def panel(px, variant, title_zh, title_en, hh, mm, tlabel, segs, quote):
    o = [f'<g transform="translate({px},0)">']
    o.append(f'<text x="{W/2}" y="18" class="lt" text-anchor="middle">{title_zh}</text>'
             f'<text x="{W/2}" y="34" class="le" text-anchor="middle">{title_en}</text>')
    o.append(f'<clipPath id="pl-patterns-c{variant}"><rect x="0" y="44" width="{W}" height="222"/></clipPath><g clip-path="url(#pl-patterns-c{variant})"><g filter="url(#ink-rough)">{room(variant)}</g>')
    if variant == "b":
        o.append(sitting())
    else:
        o.append(lying(variant))
    o.append('</g>')
    # gaze line
    if variant == "a":
        o.append('<path d="M66 164 C70 140 80 120 96 64" fill="none" stroke="#a8412c" stroke-width=".9" stroke-dasharray="3 3" marker-end="url(#ink-arrow-red)"/>')
    if variant == "c":
        o.append('<path d="M74 168 C104 146 126 124 146 100" fill="none" stroke="#a8412c" stroke-width=".9" stroke-dasharray="3 3" marker-end="url(#ink-arrow-red)"/>')
    # clock on wall
    cx, cy = (40, 70)
    o.append(clock(cx, cy, 17, hh, mm))
    o.append(f'<rect x="{cx-23}" y="{cy+22}" width="46" height="15" rx="2" fill="#2a2018"/>'
             f'<text x="{cx}" y="{cy+33.5}" text-anchor="middle" style="font-family:monospace;font-size:11.5px;font-weight:700;fill:#f6c96a">{tlabel}</text>')
    o.append(f'<rect x=".5" y="44.5" width="{W-1}" height="221" fill="none" stroke="#2a2018" stroke-width="1"/>')
    # timeline strip
    o.append(strip(8, 282, W - 16, segs, 22, 31, [(22, "22"), (24, "0"), (26, "2"), (28, "4"), (30, "6")], h=13))
    o.append(f'<text x="{W/2}" y="326" class="ls" text-anchor="middle" font-style="italic">{quote}</text>')
    o.append('</g>')
    return "".join(o)


body = []
body.append(panel(8, "a", "(a) 入睡困難", "Sleep-onset insomnia", 0, 40, "00:40",
                  [(23, 25, "wake"), (25, 30.5, "sleep")], "「躺了快兩個小時還醒著」"))
body.append(panel(262, "b", "(b) 睡眠維持困難", "Sleep-maintenance insomnia", 3, 10, "03:10",
                  [(23, 23.4, "wake"), (23.4, 27, "sleep"), (27, 28.6, "wake"), (28.6, 30.5, "sleep")], "「半夜醒來，就很難再睡著」"))
body.append(panel(516, "c", "(c) 早醒", "Early-morning awakening", 4, 30, "04:30",
                  [(23, 23.4, "wake"), (23.4, 28.5, "sleep"), (28.5, 30.5, "wake")], "「天還沒亮就醒，再也睡不回去」"))
# legend
body.append('<g transform="translate(160,348)">'
            '<rect x="0" y="0" width="22" height="11" fill="#3f6fa6" fill-opacity=".85" stroke="#2a2018" stroke-width=".7"/>'
            '<text x="28" y="10" class="ls">睡著 <tspan class="le">asleep</tspan></text>'
            '<rect x="120" y="0" width="22" height="11" fill="#e9b04a" stroke="#2a2018" stroke-width=".7"/>'
            '<rect x="120" y="0" width="22" height="11" fill="url(#ink-hatch)" opacity=".7"/>'
            '<text x="148" y="10" class="ls">躺在床上卻清醒 <tspan class="le">awake in bed</tspan></text>'
            '<text x="330" y="10" class="ls">橫軸：晚上 22 點 → 早上 7 點 <tspan class="le">clock time</tspan></text>'
            '</g>')

cap = ('<b>圖 3-A　三種症狀型態。</b>同樣說「睡不好」，病人躺在床上的樣子不一樣：(a) 上床後遲遲睡不著；(b) 睡著了，但半夜醒來很久睡不回去；'
       '(c) 比預定時間早醒、窗外還是黑的，就再也睡不著。下方時間條用藍色表示睡著、橘色斜線表示清醒躺在床上。'
       '型態影響選藥（短半衰期 vs 維持型藥物）與鑑別（凌晨醒要想到相位前移、酒精、憂鬱、夜尿、呼吸中止、熱潮紅）；實際上混合型最多，型態也會隨時間改變。示意圖。')

html = fig(PID, "Plate 3·A", "入睡困難、睡眠維持困難、早醒", "Three symptom patterns of insomnia", 368,
           "三格插圖：病人在夜裡躺在床上，分別是入睡困難、半夜醒來坐起、清晨早醒，下方附時間條", "\n".join(body), cap)
write(PID, html)
