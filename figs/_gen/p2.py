import sys, math; sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from lib import *

PID = "pl-osa"
S = .8
TY = 52
LX = 100       # left drawing origin
RX = 660       # right drawing origin (mirrored)


def L(x, y):
    return (round(LX + S * x, 1), round(TY + S * y, 1))


def R(x, y):
    return (round(RX - S * x, 1), round(TY + S * y, 1))


SKIN = ("M150 2 C200 0 248 30 264 80 C274 116 270 140 262 156 C258 170 262 190 268 214 C276 260 280 320 282 380 "
        "L104 380 C102 340 100 300 98 276 C96 262 92 250 84 244 C70 240 56 238 46 234 C36 230 30 222 28 214 "
        "C27 206 32 200 36 198 C30 194 26 190 27 186 C29 182 32 181 33 180 C29 178 26 174 26 170 C26 166 28 163 30 161 "
        "C24 160 16 157 10 152 C6 149 8 144 12 140 C22 128 34 116 42 104 C40 96 38 88 40 78 C44 50 80 6 150 2Z")


def vertebrae():
    o = []
    # C1 anterior arch, dens
    o.append('<ellipse cx="193" cy="160" rx="6" ry="8" fill="#efe6d2" stroke="#2a2018" stroke-width="1"/>')
    o.append('<path d="M201 176 C199 162 201 146 207 142 C213 142 215 156 214 176Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1"/>')
    bodies = [(174, 214), (218, 246), (250, 278), (282, 310), (314, 342), (346, 374)]
    for i, (y0, y1) in enumerate(bodies):
        x0 = 188
        o.append(f'<path d="M{x0} {y0+3} C{x0-2} {(y0+y1)/2} {x0-2} {(y0+y1)/2} {x0} {y1-3} C{x0+1} {y1} {x0+4} {y1} {x0+8} {y1} L217 {y1} C220 {y1} 221 {y1-2} 221 {y1-4} '
                 f'L221 {y0+4} C221 {y0+1} 219 {y0} 216 {y0} L{x0+6} {y0} C{x0+3} {y0} {x0} {y0+1} {x0} {y0+3}Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1.1"/>')
        o.append(f'<path d="M{x0+4} {y0+4} L217 {y0+4} L217 {y1-4} L{x0+4} {y1-4}Z" fill="url(#ink-stipple)" opacity=".55"/>')
        if i:
            o.append(f'<path d="M{x0+1} {y0-2} H220" stroke="#c9b48a" stroke-width="3"/>')
    # posterior arch of C1 / spinous processes (C2 bifid & large, C7 prominens)
    o.append('<ellipse cx="250" cy="160" rx="8" ry="6" fill="#efe6d2" stroke="#2a2018" stroke-width="1"/>')
    sp = [(186, 210, 266), (230, 246, 260), (262, 278, 262), (294, 310, 264), (326, 344, 268), (356, 376, 274)]
    for y0, y1, xe in sp:
        o.append(f'<path d="M238 {y0-4} C248 {y0-2} {xe-4} {y0+3} {xe} {y0+8} C{xe+2} {y0+12} {xe-2} {y1} {xe-8} {y1} C250 {y1} 244 {y1+1} 238 {y1+4}Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1"/>'
                 f'<path d="M242 {y0} C250 {y0+2} 256 {y0+6} {xe-4} {(y0+y1)/2}" class="ink2"/>')
    # spinal canal & cord
    o.append('<path d="M223 150 L237 150 L237 392 L223 392Z" fill="#f6e7b0"/>'
             '<path d="M225 150 C226 240 226 320 226 392 M235 150 C236 240 236 320 236 392" class="ink" stroke-width=".9"/>')
    return "".join(o)


def skull_brain():
    o = []
    # calvaria band (ends at opisthion ~ 236,150)
    o.append('<path d="M46 100 C42 60 84 12 150 8 C198 6 244 34 257 80 C264 108 262 132 246 150 L234 150 C248 130 250 108 243 86 '
             'C230 48 194 22 150 24 C96 26 62 64 62 100 C60 102 52 104 46 100Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1.2"/>'
             '<path d="M50 90 C50 60 88 18 150 14 C196 12 240 40 251 84 C256 110 254 130 242 146" fill="none" stroke="#2a2018" stroke-width=".5" stroke-dasharray="1.5 2.5"/>')
    o.append('<path d="M50 78 C52 70 60 68 64 74 C66 84 64 94 58 98 C52 96 49 88 50 78Z" fill="#e3ebf6" stroke="#2a2018" stroke-width=".8"/>')
    # cerebrum (medial surface)
    o.append('<path d="M64 100 C60 64 96 28 150 27 C198 27 236 54 241 94 C242 104 240 110 236 112 C222 106 208 104 196 106 '
             'C186 104 176 100 166 98 C156 96 146 94 136 94 C116 94 96 100 80 104 C72 106 66 104 64 100Z" fill="#efe1d6" stroke="#2a2018" stroke-width="1"/>')
    o.append('<path d="M98 82 C104 66 124 58 148 57 C172 56 192 64 200 80 C202 86 198 90 192 88 C186 76 170 70 150 70 C128 70 114 76 108 86 C104 90 98 88 98 82Z" fill="#fbf6ea" stroke="#2a2018" stroke-width=".8"/>')
    o.append('<path d="M128 84 C136 76 160 76 170 84 C168 92 152 94 140 92 C132 92 128 90 128 84Z" fill="#e8d6c8" stroke="#2a2018" stroke-width=".7"/>')
    o.append('<path d="M78 70 C84 62 92 66 98 58 C104 52 112 56 120 46 M130 40 C138 38 142 44 152 38 C162 34 168 42 178 40 M190 46 C198 48 204 56 212 58 '
             'M220 70 C226 76 224 84 232 92 M70 88 C74 82 78 86 82 80 M206 100 C214 96 222 102 232 98 M80 96 C88 92 96 96 104 90" class="ink2"/>')
    # cerebellum with folia
    o.append('<path d="M200 110 C214 104 236 104 245 114 C252 126 248 140 236 147 C224 152 210 148 202 140 C196 132 196 118 200 110Z" fill="#e8d6c8" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M206 128 C214 124 222 126 228 130 M228 130 C234 122 240 118 246 118 M228 130 C236 132 242 136 246 140 M228 130 C230 138 232 144 230 150 M216 126 C214 118 218 112 224 108 M210 136 C214 142 220 146 226 148" fill="none" stroke="#fbf6ea" stroke-width="2.2"/>'
             '<path d="M206 128 C214 124 222 126 228 130 M228 130 C234 122 240 118 246 118 M228 130 C236 132 242 136 246 140 M228 130 C230 138 232 144 230 150 M216 126 C214 118 218 112 224 108 M210 136 C214 142 220 146 226 148" class="ink2"/>')
    # brainstem: midbrain, pons, medulla -> cord
    o.append('<path d="M158 98 C168 98 178 102 184 110 C194 116 198 124 198 132 C204 140 214 146 224 150 L236 150 '
             'C232 142 222 134 212 128 C206 120 198 110 192 104 C184 98 172 94 160 94Z" fill="#e8d6c8" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M180 108 C188 114 192 122 194 130" class="ink2"/>')
    # sphenoid body + basiocciput (clivus)
    o.append('<path d="M114 100 C122 96 140 96 156 98 C166 108 180 122 192 134 C198 140 202 144 204 148 L194 152 '
             'C184 146 170 140 156 136 C144 134 128 132 116 132 C114 122 113 110 114 100Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1.1"/>'
             '<path d="M120 105 C128 103 140 103 148 106 C152 114 153 122 151 128 C140 129 128 129 121 127 C119 120 119 112 120 105Z" fill="#e3ebf6" stroke="#2a2018" stroke-width=".7"/>'
             '<path d="M158 108 C170 118 182 130 194 144" fill="none" stroke="#2a2018" stroke-width=".5" stroke-dasharray="1 2"/>'
             '<ellipse cx="146" cy="96" rx="6" ry="3.4" fill="#f0c4b8" stroke="#2a2018" stroke-width=".7"/>')
    return "".join(o)


def nose_mouth(osa):
    o = []
    # nasal cavity air
    o.append('<path d="M30 158 C24 150 26 142 34 130 C40 120 44 110 46 104 C70 100 96 98 114 100 L118 156 L36 160Z" fill="#e3ebf6"/>')
    # nasal bone / cartilage line
    o.append('<path d="M44 104 C36 118 24 132 16 144" class="ink" stroke-width=".9"/>'
             '<path d="M46 104 C70 100 96 98 112 100" class="ink" stroke-width=".9"/>')
    # conchae
    o.append('<path d="M56 154 C76 155 96 154 114 152 L114 148 C96 152 76 152 58 151Z M64 136 C80 138 100 137 114 135 L114 131 C100 135 80 135 66 134Z M88 120 C98 121 108 121 116 119 L116 116 C108 119 98 119 90 118Z" fill="url(#ink-hatch-d)"/>')
    for d in ["M50 141 C64 132 94 131 114 137 C118 141 117 148 112 150 C108 151 106 148 108 145 C96 142 74 144 60 149 C52 151 46 147 50 141Z",
              "M62 124 C76 115 100 114 114 120 C118 124 117 131 112 133 C108 134 106 131 108 128 C98 125 80 127 70 132 C62 134 58 129 62 124Z",
              "M86 109 C98 104 110 104 116 108 C118 112 116 117 112 118 C108 118 108 115 110 113 C102 112 96 113 90 116 C86 117 84 112 86 109Z"]:
        o.append(f'<path d="{d}" fill="#f0c4b8" stroke="#2a2018" stroke-width=".9"/>')
    o.append('<path d="M56 140 C72 136 96 136 112 140 M66 123 C80 119 100 119 112 123" class="ink2"/>')
    # hard palate + maxilla, teeth
    o.append('<path d="M30 160 C46 156 80 155 114 155 L116 162 C90 164 62 166 42 168 C38 168 34 166 30 164Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1.1"/>'
             '<path d="M40 160 C60 159 90 158 110 158" fill="none" stroke="#2a2018" stroke-width=".4" stroke-dasharray="1 2"/>')
    o.append('<path d="M33 164 C30 170 30 178 32 184 C34 184 36 182 37 178 C38 172 38 168 38 166Z" fill="#fffaf0" stroke="#2a2018" stroke-width=".9"/>')
    o.append('<path d="M36 206 C34 198 34 190 36 185 C38 185 40 187 41 190 C42 196 42 202 41 206Z" fill="#fffaf0" stroke="#2a2018" stroke-width=".9"/>')
    # mandible symphysis
    o.append('<path d="M37 204 C33 212 30 220 32 226 C34 232 40 235 48 235 C56 235 61 229 61 220 C61 212 55 204 47 196 C44 194 40 196 37 204Z" fill="#efe6d2" stroke="#2a2018" stroke-width="1.2"/>'
             '<path d="M42 210 C40 218 42 226 48 229 C54 228 56 222 55 216 C52 210 48 206 44 206Z" fill="url(#ink-stipple)" stroke="#2a2018" stroke-width=".5"/>')
    return "".join(o)


def tongue_palate(osa):
    o = []
    if not osa:
        tongue = ("M40 186 C42 176 56 167 74 165 C94 163 114 165 130 172 C144 180 152 192 156 206 C159 218 159 230 156 238 "
                  "C146 246 134 250 120 250 C104 248 88 240 74 232 C64 226 58 216 54 208 C50 200 44 194 40 186Z")
        palate = "M114 155 C126 156 140 164 148 176 C153 184 155 194 153 201 C150 205 146 202 145 196 C141 186 131 174 114 166Z"
        epi = "M162 236 C163 228 164 222 166 216 C170 219 170 228 168 240 C165 254 156 264 128 270 L124 266 C148 260 158 250 162 236Z"
        hy = (118, 255)
    else:
        tongue = ("M40 186 C42 176 56 168 74 166 C96 164 120 168 140 178 C158 188 172 200 176 214 C179 226 178 236 174 244 "
                  "C160 252 140 254 122 252 C104 250 88 242 74 234 C64 226 58 216 54 208 C50 200 44 194 40 186Z")
        palate = "M114 155 C130 155 154 162 168 172 C176 180 178 196 175 210 C171 215 165 213 163 205 C158 190 138 176 114 166Z"
        epi = "M171 250 C173 244 175 240 177 236 C180 240 179 248 176 256 C170 264 158 268 128 270 L124 266 C152 262 166 258 171 250Z"
        hy = (120, 258)
    o.append(f'<path d="{tongue}" fill="#e7a796" stroke="#2a2018" stroke-width="1.2"/>')
    # genioglossus fan & striations
    gx, gy = 56, 214
    ends = [(68, 170), (88, 168), (108, 169), (126, 175), (140, 186), (150, 200), (154, 216), (152, 232)] if not osa else \
           [(68, 172), (90, 170), (112, 172), (134, 180), (154, 192), (168, 206), (172, 222), (168, 238)]
    for ex, ey in ends:
        o.append(f'<path d="M{gx} {gy} Q{(gx+ex)/2+4} {(gy+ey)/2+6} {ex} {ey}" fill="none" stroke="#8a3a2c" stroke-width=".55" stroke-opacity=".75"/>')
    o.append(f'<path d="{tongue}" fill="url(#ink-hatch-r)" opacity=".25"/>')
    # geniohyoid & mylohyoid
    o.append(f'<path d="M58 222 C76 232 96 244 {hy[0]-4} {hy[1]-4} L{hy[0]-2} {hy[1]+2} C96 252 74 240 56 230Z" fill="#d98f7e" stroke="#2a2018" stroke-width=".8"/>'
             f'<path d="M50 234 C70 246 92 256 {hy[0]-6} {hy[1]+4}" class="ink2"/>')
    # soft palate
    o.append(f'<path d="{palate}" fill="#e7a796" stroke="#2a2018" stroke-width="1.1"/>')
    # hyoid
    o.append(f'<ellipse cx="{hy[0]}" cy="{hy[1]}" rx="7" ry="5" fill="#efe6d2" stroke="#2a2018" stroke-width="1.1"/>')
    # epiglottis
    o.append(f'<path d="{epi}" fill="#f3e3b0" stroke="#2a2018" stroke-width="1"/>')
    return "".join(o), tongue


def larynx(osa):
    o = []
    # laryngeal + tracheal lumen
    o.append('<path d="M114 262 L160 272 L162 318 L158 380 L112 380 L112 318Z" fill="#cfdcef"/>')
    # aryepiglottic fold from epiglottis to arytenoid
    ep = (164, 246) if not osa else (172, 256)
    o.append(f'<path d="M{ep[0]} {ep[1]} C{ep[0]+4} {ep[1]+12} 168 268 170 280" fill="none" stroke="#c46a58" stroke-width="2.4" stroke-linecap="round"/>')
    # thyroid cartilage
    o.append('<path d="M106 260 C101 272 100 290 104 306 L112 306 C109 290 109 274 114 262Z" fill="#f3e3b0" stroke="#2a2018" stroke-width="1"/>')
    # vestibular & vocal folds
    o.append('<path d="M112 282 C128 280 146 280 160 282 M112 294 C128 291 146 291 162 293" fill="none" stroke="#b5473a" stroke-width="1.6" stroke-linecap="round"/>')
    # cricoid arch + lamina, arytenoid
    o.append('<path d="M106 310 C104 314 104 318 108 320 L114 320 L114 310Z" fill="#f3e3b0" stroke="#2a2018" stroke-width=".9"/>'
             '<path d="M160 290 L170 288 L172 320 L162 320Z" fill="#f3e3b0" stroke="#2a2018" stroke-width=".9"/>'
             '<path d="M160 290 C160 282 164 276 168 274 C170 280 172 284 170 288Z" fill="#f3e3b0" stroke="#2a2018" stroke-width=".9"/>')
    for y in range(328, 380, 11):
        o.append(f'<ellipse cx="111" cy="{y}" rx="3.2" ry="4" fill="#f3e3b0" stroke="#2a2018" stroke-width=".8"/>')
    o.append('<path d="M114 324 L114 380 M160 322 L160 380" class="ink" stroke-width=".9"/>')
    # oesophagus
    o.append('<path d="M162 320 L180 320 L182 380 L162 380Z" fill="#d98f7e" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M171 322 C170 344 172 362 171 380" class="ink2"/><path d="M164 330 V376 M179 330 V376" stroke="#2a2018" stroke-width=".4" stroke-dasharray="1 2"/>')
    return "".join(o)


def drawing(osa, pid_sfx):
    o = []
    o.append(f'<clipPath id="pl-osa-sk{pid_sfx}"><path d="{SKIN}"/></clipPath>')
    o.append(f'<path d="{SKIN}" fill="#f3d9c6"/>')
    o.append(f'<g clip-path="url(#pl-osa-sk{pid_sfx})">')
    # posterior neck muscles shading
    o.append('<path d="M236 170 C250 200 262 260 274 380 L240 380 C236 300 236 240 232 190Z" fill="#e7a796" opacity=".55"/>'
             '<path d="M240 196 C246 240 250 300 252 380 M248 200 C256 250 260 310 264 380" class="ink2" stroke-opacity=".6"/>')
    o.append(skull_brain())
    # pharynx lumen
    o.append('<path d="M116 104 L116 132 C134 132 152 136 166 142 C172 148 176 156 177 166 L177 318 L162 318 L162 280 L150 240 L148 196 L116 160Z" fill="#cfdcef"/>')
    # prevertebral tissue/constrictors
    o.append('<path d="M166 142 C172 148 176 156 177 166 L177 320 L186 320 L186 160 C184 152 182 148 186 146 C180 142 174 140 166 140Z" fill="#d98f7e" stroke="#2a2018" stroke-width=".8"/>')
    # adenoid
    o.append('<path d="M140 133 C152 132 164 136 172 146 C164 148 152 144 142 139Z" fill="#f0c4b8" stroke="#2a2018" stroke-width=".7"/><path d="M140 133 C152 132 164 136 172 146 C164 148 152 144 142 139Z" fill="url(#ink-stipple)"/>')
    o.append(vertebrae())
    o.append(nose_mouth(osa))
    o.append(larynx(osa))
    tp, tongue = tongue_palate(osa)
    o.append(tp)
    if osa:
        # collapse zones
        o.append('<path d="M168 170 C174 176 177 186 177 196 L177 212 C172 214 168 212 166 206 C166 194 166 182 166 172Z" fill="#b5473a" opacity=".6"/>'
                 '<path d="M170 210 C175 218 177 230 177 240 L172 246 C172 234 170 222 166 214Z" fill="#b5473a" opacity=".6"/>')
        for (x1, y1, x2, y2) in [(138, 180, 160, 190), (138, 222, 164, 226)]:
            o.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#a8412c" stroke-width="2.2" fill="none" marker-end="url(#ink-arrow-red)"/>')
    o.append('</g>')
    o.append(f'<path d="{SKIN}" class="ink3"/>')
    # lips line & nostril
    o.append('<path d="M33 180 C38 181 42 181 46 182" class="ink2"/><path d="M14 150 C20 152 24 154 28 156" class="ink2"/>')
    return "".join(o)


body = []
body.append(f'<g transform="translate({LX},{TY}) scale({S})">{drawing(False, "a")}</g>')
body.append(f'<g transform="translate({RX},{TY}) scale(-{S},{S})">{drawing(True, "b")}</g>')
# panel titles
body.append(f'<text x="{LX+100}" y="20" class="lt" text-anchor="middle">清醒・正常</text><text x="{LX+100}" y="35" class="le" text-anchor="middle">Awake — airway open</text>')
body.append(f'<text x="{RX-100}" y="20" class="lt" text-anchor="middle" style="fill:#a8412c">睡眠中・阻塞型呼吸中止</text><text x="{RX-100}" y="35" class="le" text-anchor="middle">Asleep (OSA) — airway collapses</text>')

# left labels (anterior structures of normal drawing)
lefts = [("鼻甲", "Nasal conchae", (90, 128), 76),
         ("鼻腔", "Nasal cavity", (48, 120), 106),
         ("硬顎", "Hard palate", (76, 159), 136),
         ("軟顎", "Soft palate", (132, 170), 166),
         ("懸雍垂", "Uvula", (150, 199), 196),
         ("舌", "Tongue", (96, 184), 226),
         ("頦舌肌", "Genioglossus", (80, 212), 256),
         ("下頜骨", "Mandible", (48, 226), 286),
         ("舌骨", "Hyoid bone", (118, 255), 316),
         ("甲狀軟骨", "Thyroid cartilage", (105, 286), 346)]
for zh, en, (tx, ty), y in lefts:
    gx, gy = L(tx, ty)
    body.append(lab(4, y, zh, en, two=True))
    body.append(lead([(74 if len(zh) < 3 else 4 + 14 * len(zh) + 4, y - 4), (gx, gy)]))
# center labels (shared, leaders to both drawings)
cent = [("鼻咽", "Nasopharynx", (152, 152), 104),
        ("口咽", "Oropharynx", (162, 222), 202),
        ("會厭", "Epiglottis", (167, 232), 236),
        ("下咽", "Hypopharynx", (172, 300), 286),
        ("頸椎", "Cervical vertebrae", (200, 284), 320),
        ("氣管", "Trachea", (130, 352), 360),
        ("食道", "Oesophagus", (171, 352), 394)]
for zh, en, (tx, ty), y in cent:
    body.append(lab(380, y, zh, en, anchor="middle", two=True))
    w = 13 * len(zh) / 2 + 4
    a, b = L(tx, ty), R(tx, ty)
    if zh == "口咽":
        b = R(150, 186)  # OSA: point at closed retropalatal segment
    body.append(lead([(380 - w, y - 4), a]))
    body.append(lead([(380 + w, y - 4), b]))
# right labels (OSA mechanism)
rights = [("① 軟顎後塌", "soft palate falls back", R(171, 192), 150),
          ("② 舌根後倒", "tongue base falls back", R(173, 228), 196),
          ("頦舌肌張力 ↓", "genioglossus tone ↓", R(110, 205), 252),
          ("會厭被推後", "epiglottis pushed back", R(175, 248), 298)]
for zh, en, (gx, gy), y in rights:
    body.append(f'<text x="756" y="{y}" class="lb halo" text-anchor="end" style="fill:#a8412c">{zh}</text>'
                f'<text x="756" y="{y+13}" class="le halo" text-anchor="end">{en}</text>')
    body.append(lead([(756 - 13 * len(zh) - 2, y - 4), (gx, gy)]))

# bottom traces
def trace(x0, y0, w, kind):
    o = []
    pts = []
    for i in range(0, w + 1):
        t = i / w
        if kind == "flow_n":
            v = 7 * math.sin(t * 2 * math.pi * 6)
        elif kind == "flow_o":
            if .3 < t < .72:
                v = .6 * math.sin(t * 90)
            elif t >= .72:
                v = 10 * math.sin((t - .72) * 2 * math.pi * 9) * (1.2 - (t - .72))
            else:
                v = 6 * math.sin(t * 2 * math.pi * 6)
        elif kind == "spo2_n":
            v = -5
        else:
            # desaturation lagging apnea
            if t < .5:
                v = -5
            elif t < .82:
                v = -5 - 12 * (t - .5) / .32
            elif t < .92:
                v = -17 + 12 * (t - .82) / .1
            else:
                v = -5
        pts.append((x0 + i, y0 - v))
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    col = "#2c5d9c" if kind.startswith("flow") else "#a8412c"
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.1"/>')
    return "".join(o)

ty0 = 452
body.append(f'<line x1="0" y1="{ty0-20}" x2="760" y2="{ty0-20}" stroke="#d8c9a8" stroke-width=".8"/>')
body.append(trace(140, ty0 + 6, 200, "flow_n") + trace(140, ty0 + 36, 200, "spo2_n"))
body.append(trace(420, ty0 + 6, 200, "flow_o") + trace(420, ty0 + 36, 200, "spo2_o"))
body.append(lab(380, ty0 + 10, "氣流", "Airflow", anchor="middle"))
body.append(lab(380, ty0 + 40, "血氧", "SpO₂", anchor="middle"))
body.append(f'<text x="136" y="{ty0+10}" class="ls" text-anchor="end">規律呼吸</text><text x="136" y="{ty0+40}" class="ls" text-anchor="end">≈ 97%</text>')
# apnea bracket
ax0, ax1 = 420 + 60, 420 + 144
body.append(f'<path d="M{ax0} {ty0-4} V{ty0-8} H{ax1} V{ty0-4}" class="ld"/><text x="{(ax0+ax1)/2}" y="{ty0-12}" class="ls halo" text-anchor="middle">呼吸中止 ≥ 10 秒 <tspan class="le">apnoea</tspan></text>')
body.append(f'<text x="{420+150}" y="{ty0+66}" class="ls halo" text-anchor="middle" style="fill:#a8412c">血氧下降（落後於呼吸中止）</text>')
body.append(f'<path d="M{420+150} {ty0-8} L{420+150} {ty0-2}" stroke="#a8412c" stroke-width="1.2" marker-end="url(#ink-arrow-red)"/>'
            f'<text x="{626}" y="{ty0+4}" class="ls" style="fill:#a8412c">微覺醒</text><text x="{626}" y="{ty0+17}" class="le">arousal</text>')

cap = ('<b>圖 3-B　阻塞型睡眠呼吸中止（OSA）：氣道在哪裡塌陷。</b>左為清醒時的頭頸正中矢狀切面，空氣（淡藍）從鼻腔經鼻咽、口咽、下咽進入喉與氣管。'
       '右為睡眠中（多為仰躺）：咽部肌肉與頦舌肌張力下降，①軟顎與懸雍垂往後貼到咽後壁、②舌根後倒，口咽段被堵住（紅色）；'
       '胸腹仍在用力，但氣流中斷、血氧下降，直到大腦短暫醒來把氣道撐開——這種一夜數十次的「微覺醒」，病人常只說「睡不好、白天很睏」。'
       '許多安眠藥會讓它惡化，所以打鼾、目擊停止呼吸要先篩檢（STOP-Bang）。示意圖，依解剖教科書重繪，比例簡化；右圖為左圖的鏡像。')

html = fig(PID, "Plate 3·B", "睡眠呼吸中止：氣道在哪裡塌陷", "Obstructive sleep apnoea — where the airway collapses", 526,
           "頭頸正中矢狀切面兩幅：左為清醒時氣道暢通，右為睡眠中軟顎與舌根後倒造成氣道阻塞，下方附氣流與血氧曲線", "\n".join(body), cap)
write(PID, html)
