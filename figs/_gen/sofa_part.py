def sofa_scene():
    o = []
    # room (warm evening)
    o.append(f'<rect x="0" y="40" width="{W}" height="236" fill="#f1e2c4"/><rect x="0" y="40" width="{W}" height="236" fill="url(#ink-hatch-h)" opacity=".25"/>')
    o.append(f'<path d="M0 248 H{W} V276 H0Z" fill="#c9b48a"/><path d="M0 248 H{W} V276 H0Z" fill="url(#ink-hatch-l)"/><path d="M0 248 H{W}" class="ink"/>')
    # floor lamp glow
    o.append('<radialGradient id="pl-elderly-lamp" cx=".5" cy=".3" r=".6"><stop offset="0" stop-color="#ffe9a8" stop-opacity=".9"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>')
    o.append('<clipPath id="pl-elderly-cl"><rect x="0" y="40" width="368" height="236"/></clipPath><circle cx="18" cy="90" r="70" fill="url(#pl-elderly-lamp)" clip-path="url(#pl-elderly-cl)"/>'
             '<path d="M6 70 L30 70 L24 50 L12 50Z" fill="#e8d6ae" stroke="#2a2018" stroke-width="1"/><path d="M18 70 V246 M8 248 H28" stroke="#2a2018" stroke-width="1.6"/>')
    # TV + cabinet
    o.append('<path d="M262 206 H358 V248 H262Z" fill="#a57c55" stroke="#2a2018" stroke-width="1.1"/><path d="M310 206 V248 M268 226 H304 M316 226 H352" class="ink2"/>')
    o.append('<path d="M286 196 H334 L330 206 H290Z" fill="#3a3a3a"/><rect x="266" y="128" width="88" height="68" rx="3" fill="#2a2f36" stroke="#2a2018" stroke-width="1.2"/>'
             '<rect x="271" y="133" width="78" height="58" fill="#a9c4e6"/><path d="M271 170 C290 160 306 176 324 164 C334 158 342 162 349 160 V191 H271Z" fill="#6e93c2"/>'
             '<circle cx="330" cy="146" r="7" fill="#f6e7b0"/>')
    o.append('<path d="M266 150 L150 110 M266 176 L150 190" stroke="#cfdcef" stroke-width="1" stroke-dasharray="2 4" opacity=".9"/>')
    # wall clock
    o.append(clock(200, 82, 15, 19, 30))
    o.append('<text x="200" y="116" class="ls" text-anchor="middle">19:30</text>')
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
    o.append(head(70, 82, .42, -28, eye="closed", hair="grey", age="old", mouth="open"))
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


