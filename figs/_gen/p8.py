import sys, math; sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from lib import *

PID = "pl-elderly"
SH = "#b9a98c"   # cardigan
W = 368
exec(open('/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad/sofa_part.py').read())


def dusk_window():
    return ('<defs><linearGradient id="pl-elderly-dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5c6f9a"/><stop offset=".6" stop-color="#e9a86a"/><stop offset="1" stop-color="#f6d79a"/></linearGradient></defs>'
            '<rect x="274" y="50" width="76" height="62" fill="#efe6d2" stroke="#2a2018" stroke-width=".9"/>'
            '<rect x="279" y="55" width="66" height="52" fill="url(#pl-elderly-dusk)" stroke="#2a2018" stroke-width=".8"/>'
            '<path d="M279 107 V96 h10 v-6 h8 v8 h14 v-10 h9 v8 h12 v-4 h13 V107Z" fill="#4a3a3a"/>'
            '<path d="M312 55 V107 M279 81 H345" stroke="#efe6d2" stroke-width="2.5"/>')


def bed_scene():
    o = []
    o.append(f'<clipPath id="{PID}-cb"><rect x="0" y="40" width="{W}" height="236"/></clipPath><g clip-path="url(#{PID}-cb)">')
    o.append(f'<rect x="0" y="40" width="{W}" height="236" fill="#c9d3e3"/><rect x="0" y="40" width="{W}" height="236" fill="url(#ink-hatch-h)" opacity=".5"/>')
    o.append(f'<path d="M0 252 H{W} V276 H0Z" fill="#9aa6b6"/><path d="M0 252 H{W}" class="ink"/>')
    o.append('<rect x="276" y="56" width="70" height="72" fill="#1f2d48" stroke="#2a2018" stroke-width="1"/><path d="M311 56 V128 M276 92 H346" stroke="#efe6d2" stroke-width="2.5"/>'
             '<circle cx="290" cy="68" r=".9" fill="#f6e7b0"/><circle cx="332" cy="112" r=".9" fill="#f6e7b0"/><circle cx="296" cy="114" r=".9" fill="#f6e7b0"/><circle cx="336" cy="72" r=".9" fill="#f6e7b0"/>')
    o.append(clock(200, 76, 16, 3, 0) + '<rect x="178" y="98" width="44" height="15" rx="2" fill="#2a2018"/>'
             '<text x="200" y="109.5" text-anchor="middle" style="font-family:monospace;font-size:11.5px;font-weight:700;fill:#f6c96a">03:00</text>')
    o.append('<path d="M8 252 V128 C8 118 30 114 34 124 V252" fill="#a57c55" stroke="#2a2018" stroke-width="1.3"/><path d="M8 252 V128 C8 118 30 114 34 124 V252" fill="url(#ink-hatch-l)"/>'
             f'<path d="M30 212 H{W} V236 H30Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/><path d="M30 236 H{W} V244 H30Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/><path d="M36 244 V252" stroke="#2a2018" stroke-width="3"/>')
    o.append('<path d="M30 210 C24 200 30 192 44 192 C60 190 82 190 92 194 C98 198 96 210 92 214 C74 216 46 216 30 210Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M36 208 C48 212 70 212 88 210" class="ink2"/>')
    o.append(head(58, 189, .46, -90, eye="open", hair="grey", age="old"))
    o.append('<path d="M75 181 C80 178 86 176 92 176 C98 175 102 175 104 176 L104 213 L72 213 C70 204 71 190 75 181Z" fill="#cfdcef" stroke="#2a2018" stroke-width="1"/>')
    top = "M100 178 C110 170 124 168 138 171 C150 174 156 179 166 179 C178 179 186 174 198 175 C212 176 224 181 240 182 C270 180 300 182 368 184"
    o.append(f'<path d="{top} L368 248 C330 250 300 244 270 249 C230 252 200 245 170 249 C140 252 120 245 100 244Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M138 171 C140 196 134 222 138 247 C131 226 130 200 132 172Z" fill="url(#ink-hatch)"/><path d="M198 175 C194 200 200 226 194 247 C202 226 205 200 205 176Z" fill="url(#ink-hatch)"/>'
             '<path d="M166 180 C164 204 168 230 164 249 M240 182 C242 210 238 230 242 250 M300 183 C298 210 302 230 300 248" class="ink2"/>')
    o.append('<path d="M98 180 C102 174 108 170 114 169 C112 196 114 222 112 248 C106 248 101 246 98 244Z" fill="#f7f1e2" stroke="#2a2018" stroke-width="1"/>')
    o.append('<path d="M110 176 C120 172 132 170 144 170 L146 179 C134 180 122 182 112 186Z" fill="#cfdcef" stroke="#2a2018" stroke-width="1"/>')
    o.append(hand(144, 174, .66, 8))
    o.append('<path d="M70 168 C120 140 160 112 184 96" fill="none" stroke="#a8412c" stroke-width=".9" stroke-dasharray="3 3" marker-end="url(#ink-arrow-red)"/>')
    o.append('</g>')
    o.append(f'<rect x=".5" y="40.5" width="{W-1}" height="235" fill="none" stroke="#2a2018" stroke-width="1"/>')
    return "".join(o)


body = []
body.append(f'<g transform="translate(6,0)">{sofa_scene()}{dusk_window()}</g>')
body.append(f'<g transform="translate(386,0)">{bed_scene()}</g>')
body.append('<text x="190" y="20" class="lt" text-anchor="middle">傍晚七點半：沙發上就打起瞌睡</text><text x="190" y="35" class="le" text-anchor="middle">dozing in the armchair in the early evening</text>')
body.append('<text x="570" y="20" class="lt" text-anchor="middle">凌晨三點：清醒，等天亮</text><text x="570" y="35" class="le" text-anchor="middle">awake at 03:00, waiting for dawn</text>')

# ===== 24-h comparison chart
Y0 = 300
x0, w = 120, 610          # 12:00 -> 12:00 next day
def X(h):
    return x0 + (h - 12) / 24 * w
C = []
C.append(f'<text x="8" y="{Y0}" class="lt">相位前移：整段睡眠往前搬</text><text x="196" y="{Y0}" class="le">advanced sleep phase — the whole window moves earlier</text>')
# night shading
C.append(f'<rect x="{X(18.5):.1f}" y="{Y0+10}" width="{X(30.5)-X(18.5):.1f}" height="166" fill="#cfdcef" opacity=".35"/>')
rows = [("年輕成人", "young adult", Y0 + 56, 23.5, 31.5, 3.5, 1.0, "#2c5d9c", None),
        ("長者", "older adult", Y0 + 126, 21.0, 28.0, 1.5, .55, "#a8412c", (19.5, 20.1))]
for zh, en, yb, s0, s1, mpk, amp, col, doze in rows:
    # melatonin curve above bar
    pts = []
    for i in range(0, w + 1, 2):
        h = 12 + i / w * 24
        v = amp * math.exp(-((h - (mpk + 24 if mpk < 12 else mpk)) / 2.6) ** 2)
        pts.append((x0 + i, yb - 2 - v * 34))
    C.append(f'<path d="M{x0} {yb-2} ' + " ".join(f"L{a:.1f} {b:.1f}" for a, b in pts) + f' L{x0+w} {yb-2}Z" fill="{col}" fill-opacity=".14"/>')
    C.append('<path d="M' + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + f'" fill="none" stroke="{col}" stroke-width="1.6"/>')
    # sleep bar
    C.append(f'<rect x="{x0}" y="{yb}" width="{w}" height="12" fill="#efe6d2" stroke="#2a2018" stroke-width=".7"/>')
    C.append(f'<rect x="{X(s0):.1f}" y="{yb}" width="{X(s1)-X(s0):.1f}" height="12" fill="#3f6fa6" fill-opacity=".85"/>')
    if doze:
        C.append(f'<rect x="{X(doze[0]):.1f}" y="{yb}" width="{X(doze[1])-X(doze[0]):.1f}" height="12" fill="#3f6fa6" fill-opacity=".55"/>')
    C.append(f'<rect x="{x0}" y="{yb}" width="{w}" height="12" fill="none" stroke="#2a2018" stroke-width=".8"/>')
    C.append(f'<text x="{x0-8}" y="{yb-10}" class="lb" text-anchor="end" style="fill:{col}">{zh}</text><text x="{x0-8}" y="{yb+3}" class="le" text-anchor="end">{en}</text>')
    pkx = X(mpk + 24)
    C.append(f'<text x="{pkx:.1f}" y="{yb - 2 - amp*34 - 5:.1f}" class="ls halo" text-anchor="middle" style="fill:{col}">褪黑激素高峰</text>')
    C.append(f'<text x="{X(s0):.1f}" y="{yb+25}" class="ls" text-anchor="middle">{int(s0)}:{"30" if s0 % 1 else "00"}</text>'
             f'<text x="{X(s1):.1f}" y="{yb+25}" class="ls" text-anchor="middle">{int(s1 % 24)}:{"30" if s1 % 1 else "00"}</text>')
# elder annotations
C.append(f'<text x="{X(19.8):.1f}" y="{Y0+163}" class="ls" text-anchor="middle">打瞌睡</text>')
C.append(f'<path d="M{X(23.5)+4:.1f} {Y0+88} L{X(21.0)+2:.1f} {Y0+118}" stroke="#a8412c" stroke-width="1" stroke-dasharray="3 2" marker-end="url(#ink-arrow-red)"/>')
C.append(f'<path d="M{X(31.5)-4:.1f} {Y0+88} L{X(28.0)+2:.1f} {Y0+118}" stroke="#a8412c" stroke-width="1" stroke-dasharray="3 2" marker-end="url(#ink-arrow-red)"/>')
# axis
C.append(f'<path d="M{x0} {Y0+176} H{x0+w}" class="ink"/>')
for h, lb in [(12, "12"), (15, "15"), (18, "18"), (21, "21"), (24, "0"), (27, "3"), (30, "6"), (33, "9"), (36, "12")]:
    C.append(f'<line x1="{X(h):.1f}" y1="{Y0+176}" x2="{X(h):.1f}" y2="{Y0+180}" stroke="#2a2018" stroke-width=".7"/><text x="{X(h):.1f}" y="{Y0+191}" class="ls" text-anchor="middle">{lb}</text>')
C.append(f'<text x="{x0-8}" y="{Y0+191}" class="ls" text-anchor="end">時鐘</text>')
C.append(f'<rect x="8" y="{Y0+200}" width="12" height="9" fill="#3f6fa6" fill-opacity=".85"/><text x="24" y="{Y0+209}" class="ls">睡眠時段</text>'
         f'<path d="M92 {Y0+204} h18" stroke="#2a2018" stroke-width="1.6"/><text x="114" y="{Y0+209}" class="ls">褪黑激素（長者：較低、較早）</text>'
         f'<text x="8" y="{Y0+228}" class="ls" style="fill:#a8412c">總睡眠時數其實不少，只是整段往前；叫他更早睡只會更早醒 → 傍晚光照與活動、別太早上床。</text>')
body.append("".join(C))

cap = ('<b>圖 12-B　老人家天沒亮就醒：相位前移。</b>上：同一位長者，傍晚七點半就在沙發上打瞌睡，凌晨三點清醒等天亮。下：與年輕成人相比，長者夜間褪黑激素分泌幅度較低、高峰提早，'
       '睡眠時段整段往前移；總睡眠時間不一定短。處理重點是把時鐘往後推（傍晚光照與活動、避免太早上床），而不是叫他更早睡；長者的睡眠結構本來就會改變（深睡少、夜醒多），也要調整期待。示意圖，曲線為概念示意，非實測資料。')

html = fig(PID, "Plate 12·B", "老人家天沒亮就醒：相位前移", "Early waking in older adults — the advanced sleep phase", 540,
           "左為長者傍晚在沙發看電視打瞌睡，右為凌晨三點躺在床上清醒；下方為年輕成人與長者的 24 小時睡眠時段與褪黑激素曲線比較", "\n".join(body), cap)
write(PID, html)
