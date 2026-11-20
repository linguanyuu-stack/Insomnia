"""reusable organ drawings (local coords)"""


def heart(pfx, detail=True):
    """anterior view of the heart, local ~ (30..200, -12..226); patient's left = +x"""
    o = []
    # great vessels behind: descending aorta & pulmonary arteries
    o.append('<path d="M140 30 C156 30 166 40 166 56 L166 120 L152 120 L152 58 C152 48 148 44 140 44Z" fill="#c46a58" stroke="#2a2018" stroke-width="1.1"/>')
    # right pulmonary artery (passes behind ascending aorta)
    o.append('<path d="M124 60 C112 58 100 60 90 64 L88 56 C100 52 114 50 126 54Z" fill="#7d9cc6" stroke="#2a2018" stroke-width="1"/>')
    # SVC
    o.append('<path d="M60 -10 L82 -10 L84 76 L62 80Z" fill="url(#ink-vol-blue)" stroke="#2a2018" stroke-width="1.2"/>'
             '<path d="M66 -6 C68 20 68 50 68 74" class="ink2" stroke-opacity=".6"/>')
    # aortic arch + branches
    o.append('<path d="M84 100 C82 70 84 40 98 26 C112 12 140 12 154 26 C162 34 166 44 166 56 L152 58 C152 46 144 36 132 34 C118 32 108 40 104 56 C102 70 104 86 106 100Z" fill="url(#ink-vol-red)" stroke="#2a2018" stroke-width="1.3"/>')
    for (x1, y1, x2, y2, w) in [(100, 24, 90, -10, 7), (118, 16, 116, -12, 5), (136, 18, 144, -10, 5)]:
        o.append(f'<path d="M{x1-w} {y1+4} L{x2-w} {y2} L{x2+w} {y2} L{x1+w} {y1+4}Z" fill="#d97a68" stroke="#2a2018" stroke-width="1"/>')
    o.append('<path d="M92 90 C90 66 92 44 104 32" class="ink2"/><path d="M84 100 C82 70 84 40 98 26 L104 32 C94 44 92 70 94 100Z" fill="url(#ink-hatch)" opacity=".6"/>')
    # pulmonary trunk (blue in plate convention) & branches
    o.append('<path d="M108 112 C108 92 112 72 124 60 C132 52 146 50 160 52 L196 48 L198 62 L164 66 C150 66 140 70 136 80 C132 92 132 104 132 116Z" fill="url(#ink-vol-blue)" stroke="#2a2018" stroke-width="1.2"/>'
             '<path d="M118 108 C118 90 122 76 130 68" class="ink2" stroke-opacity=".6"/>')
    # left auricle
    o.append('<path d="M160 86 C172 76 188 80 190 92 C184 92 182 98 176 98 C170 100 164 96 160 94Z" fill="#c46a58" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M168 86 l3 4 M176 84 l2 5 M183 86 l0 5" class="ink2"/>')
    # right atrium + auricle
    o.append('<path d="M84 76 C66 74 50 86 46 104 C42 126 48 146 62 158 C70 164 80 164 88 158 L96 110Z" fill="url(#ink-vol-red)" stroke="#2a2018" stroke-width="1.3"/>'
             '<path d="M84 76 C90 70 102 74 106 84 C104 92 96 96 92 102 C86 100 80 92 84 76Z" fill="#c46a58" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M90 80 l3 4 M96 78 l2 5" class="ink2"/>'
             '<path d="M46 104 C42 126 48 146 62 158 L68 152 C56 140 52 124 54 106Z" fill="url(#ink-hatch)" opacity=".7"/>')
    # ventricles: RV (anterior) and LV (left border + apex)
    o.append('<path d="M88 158 C92 120 104 106 132 108 C150 108 166 96 184 98 C198 104 204 124 202 148 C200 180 186 206 160 222 '
             'C150 226 140 222 130 214 C110 198 92 180 88 158Z" fill="url(#ink-vol-red)" stroke="#2a2018" stroke-width="1.5"/>')
    o.append('<path d="M184 98 C198 104 204 124 202 148 C200 180 186 206 160 222 L156 214 C178 200 190 176 192 148 C194 126 190 110 180 102Z" fill="url(#ink-hatch)" opacity=".75"/>')
    o.append('<path d="M100 170 C110 190 126 206 148 216" fill="url(#ink-hatch-l)" stroke="none"/>')
    # fat in grooves
    o.append('<path d="M150 108 C156 140 156 180 154 218" fill="none" stroke="#f6e7b0" stroke-width="7" stroke-linecap="round" opacity=".9"/>'
             '<path d="M90 106 C82 124 82 146 92 166 C100 180 112 194 124 206" fill="none" stroke="#f6e7b0" stroke-width="6" stroke-linecap="round" opacity=".9"/>')
    # coronary arteries (red) & veins (blue)
    o.append('<path d="M104 102 C94 112 88 130 90 150 C92 168 104 186 120 200" fill="none" stroke="#2a2018" stroke-width="3.4"/>'
             '<path d="M104 102 C94 112 88 130 90 150 C92 168 104 186 120 200" fill="none" stroke="#d9473a" stroke-width="2.2"/>')
    o.append('<path d="M140 100 C150 112 152 140 152 170 C152 192 152 206 150 218" fill="none" stroke="#2a2018" stroke-width="3.4"/>'
             '<path d="M140 100 C150 112 152 140 152 170 C152 192 152 206 150 218" fill="none" stroke="#d9473a" stroke-width="2.2"/>')
    if detail:
        for d in ["M152 132 C162 140 172 150 180 166", "M152 160 C164 168 172 178 178 192", "M152 186 C160 194 166 200 170 208",
                  "M150 140 C142 150 134 158 124 164", "M92 140 C102 146 110 154 114 164", "M140 100 C152 96 166 96 178 100"]:
            o.append(f'<path d="{d}" fill="none" stroke="#2a2018" stroke-width="2.4"/><path d="{d}" fill="none" stroke="#d9473a" stroke-width="1.3"/>')
        o.append('<path d="M158 112 C162 140 162 176 158 214" fill="none" stroke="#3f6fa6" stroke-width="1.8"/>'
                 '<path d="M86 118 C80 138 82 156 96 176" fill="none" stroke="#3f6fa6" stroke-width="1.5"/>')
    return "".join(o)


def kidney(adrenal_hot=True):
    """left kidney with adrenal on top, local ~ (0..70, 0..110)"""
    o = []
    o.append('<path d="M34 22 C14 22 4 42 4 62 C4 86 16 108 36 108 C50 108 58 100 58 90 C58 82 50 78 48 70 C46 62 50 56 56 50 C60 44 60 22 34 22Z" fill="url(#ink-vol-red)" stroke="#2a2018" stroke-width="1.3"/>')
    o.append('<path d="M14 56 C12 70 16 88 26 98" class="ink2"/><path d="M48 70 C56 72 66 72 72 70 M50 76 C58 80 66 84 72 86" fill="none" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M48 66 C58 64 66 62 72 60" fill="none" stroke="#b5473a" stroke-width="3"/><path d="M50 80 C58 82 66 84 72 84" fill="none" stroke="#3f6fa6" stroke-width="3"/>'
             '<path d="M50 86 C52 96 50 104 54 116" fill="none" stroke="#e8cf7a" stroke-width="3"/>')
    fill = "#e9b04a" if adrenal_hot else "#f6e7b0"
    o.append(f'<path d="M14 26 C16 10 30 0 44 4 C54 8 58 18 54 30 C44 24 28 22 14 26Z" fill="{fill}" stroke="#2a2018" stroke-width="1.2"/>'
             '<path d="M22 22 C30 14 40 12 48 18" fill="none" stroke="#a8412c" stroke-width="1.4"/>'
             '<path d="M14 26 C16 10 30 0 44 4 C54 8 58 18 54 30 C44 24 28 22 14 26Z" fill="url(#ink-stipple)" opacity=".6"/>')
    return "".join(o)


def lateral_brain(pfx, pet=True):
    """left lateral brain, frontal pole at left, local ~ (26..222, 38..182)"""
    o = []
    outline = ("M30 110 C26 80 50 50 90 44 C130 38 170 46 196 64 C214 78 222 98 216 116 C212 128 200 136 188 138 "
               "C170 140 150 142 132 140 C116 150 96 152 80 146 C64 142 48 132 40 124 C34 120 30 116 30 110Z")
    o.append('<path d="M156 140 C170 134 196 136 208 144 C214 156 202 168 184 168 C168 168 158 160 156 150Z" fill="#e8d6c8" stroke="#2a2018" stroke-width="1"/>'
             '<path d="M162 146 C176 142 196 144 204 150 M164 154 C176 152 192 154 202 158 M170 162 C180 160 190 162 196 164" class="ink2"/>')
    o.append('<path d="M138 140 C140 152 144 166 148 182 L160 182 C158 168 156 152 156 140Z" fill="#e8d6c8" stroke="#2a2018" stroke-width="1"/>')
    o.append(f'<path d="{outline}" fill="#efe1d6" stroke="#2a2018" stroke-width="1.4"/>')
    o.append('<path d="M78 112 C100 100 126 96 150 98 M126 46 C122 66 118 86 112 100 M60 62 C70 70 66 82 78 88 C86 92 84 102 92 106 '
             'M44 96 C54 92 60 100 70 96 M150 50 C146 64 154 72 148 86 M176 60 C170 72 178 84 172 96 M196 82 C188 92 196 102 188 112 '
             'M96 52 C92 66 100 74 96 86 M104 120 C116 116 128 124 140 120 M88 132 C100 128 110 136 122 132 M160 112 C170 108 176 116 186 112 '
             'M136 50 C134 60 140 70 136 82 M110 46 C106 58 112 66 108 78" class="ink2"/>')
    if pet:
        for (cx, cy, r, op) in [(62, 82, 30, .85), (104, 62, 24, .7), (160, 80, 26, .6), (120, 112, 18, .75), (196, 104, 16, .5)]:
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{pfx}-pet)" opacity="{op}"/>')
        o.append(f'<path d="{outline}" fill="none" stroke="#2a2018" stroke-width="1.4"/>')
    return "".join(o)
