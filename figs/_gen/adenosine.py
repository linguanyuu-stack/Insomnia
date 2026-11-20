import sys, os, math, random, re
sys.path.insert(0, os.path.dirname(__file__))
from plib import *
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D

P = 'pl-adenosine'
D = []
O = []
add = O.append
AD = '#2c5d9c'; CAF = '#7a4a2a'; A1C = '#9db8dc'; A2C = '#e6c66a'

PURINE = Chem.MolFromSmarts('[#7]1~[#6]~[#7]~[#6]2~[#6](~[#6]~1)~[#7]~[#6]~[#7]~2')


def mol_aligned(smi, w, h, bond=26):
    """Same drawing style as kit/mol.py (RDKit skeletal formula), but purine cores share one orientation
    and scale; also returns draw coords of the purine atoms for the highlight tint."""
    tm = Chem.MolFromSmiles('c1ncc2[nH]cnc2n1'); AllChem.Compute2DCoords(tm)
    m = Chem.MolFromSmiles(smi)
    AllChem.GenerateDepictionMatching2DStructure(m, tm, refPatt=PURINE)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    o = d.drawOptions()
    o.clearBackground = False; o.bondLineWidth = 1.6; o.fixedFontSize = 13; o.padding = 0.08; o.fixedBondLength = bond
    o.updateAtomPalette({6: (0.165, 0.125, 0.094), 7: (0.17, 0.36, 0.61), 8: (0.66, 0.25, 0.17), 1: (0.165, 0.125, 0.094)})
    d.DrawMolecule(m); d.FinishDrawing()
    s = d.GetDrawingText()
    s = re.sub(r'<\?xml[^>]*\?>\s*', '', s)
    s = re.sub(r"<rect style='opacity:1.0;fill:#FFFFFF[^>]*>\s*</rect>", '', s)
    s = re.sub(r"<!-- END OF HEADER -->", '', s)
    s = re.sub(r'<svg[^>]*>', '', s, count=1).replace('</svg>', '')
    s = re.sub(r"class='[^']*'\s*", '', s)
    match = m.GetSubstructMatch(PURINE)
    pts = [(d.GetDrawCoords(i).x, d.GetDrawCoords(i).y) for i in match]
    allp = [(d.GetDrawCoords(i).x, d.GetDrawCoords(i).y) for i in range(m.GetNumAtoms())]
    return '<g class="mol">' + s.strip() + '</g>', pts, allp


def tint_hull(pts, pad=11):
    # pts in purine order: ring6 = 0..5 ; ring5 = 3,4,6,7,8 -> outline 0,1,2,3,8,7,6,4,5
    order = [0, 1, 2, 3, 8, 7, 6, 4, 5]
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    ring = []
    for i in order:
        x, y = pts[i]
        dx, dy = x - cx, y - cy
        L = math.hypot(dx, dy) or 1
        ring.append((x + dx / L * pad, y + dy / L * pad))
    return cr(ring, True)


# ================= LEFT: synapse scene =================
# extracellular background
add('<rect x="14" y="40" width="440" height="314" rx="6" fill="#f4efe2"/>')


# --- presynaptic bouton ---
bout = [(40, 40), (70, 42), (96, 54), (150, 64), (205, 82), (236, 112), (238, 150), (222, 172), (180, 182), (120, 184), (70, 176), (40, 160)]
add('<path d="M14 40 L40 40" />')
bd = cr([(14, 70), (30, 60), (60, 70)] + bout[2:] + [(40, 150), (14, 140)], False)
bpath = 'M14 52 C40 48 70 52 96 58 C140 66 200 76 230 108 C246 128 244 160 222 174 C190 192 120 192 70 180 C44 174 26 164 14 156 Z'
add('<path d="%s" fill="#f6e4d6"/><path d="%s" fill="url(#ink-stipple-l)"/>' % (bpath, bpath))
add(shade(P + '-m1', bpath, -10, -10, 'ink-hatch-l', 1))
add('<path d="%s" class="ink3" />' % bpath)
# mitochondria
for (cx, cy, rx, ry, rot) in [(70, 100, 30, 13, -8), (150, 92, 24, 11, 12)]:
    add('<g transform="rotate(%s %s %s)"><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#f0cdb8" class="ink"/>' % (rot, cx, cy, cx, cy, rx, ry))
    zz = 'M%s %s' % (cx - rx + 6, cy)
    for k in range(int(rx * 2 / 6) - 1):
        zz += ' L%s %s' % (cx - rx + 9 + k * 6, cy + (-ry + 4 if k % 2 == 0 else ry - 4))
    add('<path d="%s" class="ink2"/><ellipse cx="%s" cy="%s" rx="%s" ry="%s" class="ink2" transform="scale(1)" fill="none" stroke-opacity=".5"/></g>' % (zz, cx, cy, rx - 3, ry - 3))
add('<text x="70" y="128" text-anchor="middle" class="ls halo">粒線體 → ATP</text>')
# synaptic vesicles
rnd = random.Random(3)
for (vx, vy) in [(110, 140), (128, 152), (148, 146), (170, 156), (190, 142), (96, 158), (208, 158), (160, 130), (186, 120)]:
    add('<circle cx="%s" cy="%s" r="7" fill="#fbf7ee" class="ink"/>' % (vx, vy))
    for k in range(3):
        add('<circle cx="%s" cy="%s" r="1" fill="%s"/>' % (f(vx + rnd.uniform(-3, 3)), f(vy + rnd.uniform(-3, 3)), RED))
# fusing vesicle releasing ATP
add('<path d="M140 186 q8 10 16 0" fill="#fbf7ee" class="ink"/>')
add('<text x="30" y="30" class="lb">突觸前終端 <tspan class="le">Presynaptic terminal</tspan></text>')

# --- astrocyte ---
ax, ay = 382, 104


def tapered(pts, w0, w1):
    dense = bez_pts(pts, per=10)
    L = len(dense)
    left, right = [], []
    for i, (x, y) in enumerate(dense):
        a_, b_ = dense[max(0, i - 1)], dense[min(L - 1, i + 1)]
        tx, ty = b_[0] - a_[0], b_[1] - a_[1]
        n = math.hypot(tx, ty) or 1
        nx, ny = -ty / n, tx / n
        w = (w0 + (w1 - w0) * i / (L - 1)) / 2
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w))
    return poly(left + right[::-1], True)


shapes = []
ra = random.Random(8)
for ang, ln in [(-160, 70), (-120, 64), (-75, 60), (-30, 66), (10, 62), (55, 70), (100, 52)]:
    pts = [(ax, ay)]
    for k in range(1, 5):
        t = k / 4
        aa = math.radians(ang + ra.uniform(-14, 14))
        pts.append((ax + ln * t * math.cos(aa), ay + ln * t * math.sin(aa)))
    shapes.append(tapered(pts, 9, .8))
    # side branch
    mx, my = pts[2]
    ab = math.radians(ang + ra.choice([-38, 38]))
    shapes.append(tapered([(mx, my), (mx + 12 * math.cos(ab), my + 12 * math.sin(ab)), (mx + 24 * math.cos(ab + .2), my + 24 * math.sin(ab + .2))], 3.5, .6))
# perisynaptic process: sheath hugging the bouton, ending in the cleft
sheath = [(ax, ay), (330, 118), (284, 124), (254, 142), (246, 176), (250, 206), (262, 228)]
shapes.append(tapered(sheath, 10, 7))
shapes.append(tapered([(262, 226), (276, 236), (292, 238)], 7, 2))
body_d = cr([(ax - 22, ay - 6), (ax - 10, ay - 22), (ax + 10, ay - 20), (ax + 22, ay - 4), (ax + 18, ay + 16), (ax, ay + 22), (ax - 18, ay + 14)], True)
shapes.append(body_d)
add('<g>' + ''.join('<path d="%s" fill="none" stroke="%s" stroke-width="2.2" stroke-linejoin="round"/>' % (d, INK) for d in shapes) + '</g>')
add('<g>' + ''.join('<path d="%s" fill="#dfe9d8"/>' % d for d in shapes) + '</g>')
add('<g opacity=".8">' + ''.join('<path d="%s" fill="url(#ink-stipple-l)"/>' % d for d in shapes) + '</g>')
add('<ellipse cx="%s" cy="%s" rx="11" ry="8" fill="#b9cbb0" class="ink"/><circle cx="%s" cy="%s" r="2.4" fill="%s"/>' % (ax + 2, ay + 1, ax + 5, ay, INK))
add('<text x="372" y="34" text-anchor="middle" class="lb">星狀膠細胞 <tspan class="le">Astrocyte</tspan></text>')

# --- postsynaptic membrane with receptors ---
MY = 352
add('<rect x="14" y="%s" width="440" height="34" fill="url(#ink-membrane)"/>' % MY)
add('<rect x="14" y="%s" width="440" height="112" fill="#f3d9c6" fill-opacity=".55"/>' % (MY + 34))
add('<path d="M14 %s H454" class="ink"/>' % MY)
add('<text x="24" y="%s" class="ls" style="font-style:italic">突觸後神經元 Postsynaptic neuron</text>' % (MY + 120))


def gpcr(x0, col, lig=None, label_zh='', label_en=''):
    o = []
    hel = []
    for i in range(7):
        x = x0 + i * 8.6
        tilt = (-1) ** i * 2.5
        hel.append((x, tilt))
        o.append('<rect x="%s" y="%s" width="8" height="48" rx="4" fill="%s" stroke="%s" stroke-width=".8" transform="rotate(%s %s %s)"/>' % (
            f(x), MY - 7, col, INK, tilt, f(x + 4), MY + 17))
        o.append('<path d="M%s %s v40" stroke="#fff" stroke-width="1.2" stroke-opacity=".5" transform="rotate(%s %s %s)"/>' % (f(x + 2.4), MY - 3, tilt, f(x + 4), MY + 17))
    # loops
    for i in range(6):
        xa, xb = x0 + i * 8.6 + 4, x0 + (i + 1) * 8.6 + 4
        if i % 2 == 0:
            o.append('<path d="M%s %s q%s 14 %s 0" class="ink2" stroke-width="1"/>' % (f(xa), MY + 41, f((xb - xa) / 2), f(xb - xa)))
        else:
            o.append('<path d="M%s %s q%s -12 %s 0" class="ink2" stroke-width="1"/>' % (f(xa), MY - 7, f((xb - xa) / 2), f(xb - xa)))
    cx = x0 + 30
    # binding pocket
    o.append('<path d="M%s %s q8 10 16 0" fill="#f4efe2" class="ink2"/>' % (f(cx - 8), MY - 7))
    # G protein below
    o.append('<ellipse cx="%s" cy="%s" rx="13" ry="9" fill="%s" class="ink"/><ellipse cx="%s" cy="%s" rx="9" ry="7" fill="#efe2cc" class="ink"/><circle cx="%s" cy="%s" r="5" fill="#e3d4bb" class="ink"/>' % (
        f(cx - 8), MY + 60, col, f(cx + 10), MY + 58, f(cx + 22), MY + 52))
    return '\n'.join(o)


def adeno(x, y, r=4.4):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="#fff" stroke-width=".9"/>' % (f(x), f(y), r, AD)


def caff(x, y, r=5.2):
    pts = [(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in range(30, 390, 60)]
    return '<path d="%s" fill="%s" stroke="#fff" stroke-width=".9"/>' % (poly(pts, True), CAF)


RX = [54, 184, 334]
add(gpcr(RX[0], A1C))
add(gpcr(RX[1], A2C))
add(gpcr(RX[2], A2C))
# ligands in pockets
add(adeno(RX[0] + 30, MY - 9, 5))
add(adeno(RX[1] + 30, MY - 9, 5))
add(caff(RX[2] + 30, MY - 9, 6))
# adenosine bouncing off caffeine-blocked receptor
add('<path d="M%s %s q16 0 28 -10" stroke="%s" stroke-width="1" fill="none" stroke-dasharray="2 2" marker-end="url(#ink-arrow)"/>' % (RX[2] + 44, MY - 4, AD))
add(adeno(RX[2] + 86, MY - 18))
add('<path d="M%s %s l8 8 M%s %s l-8 8" stroke="%s" stroke-width="2.2"/>' % (RX[2] + 58, MY - 13, RX[2] + 64, MY - 13, RED))
# receptor names (above, small)
for x, zh, col in [(RX[0], 'A1 受體', '#2c5d9c'), (RX[1], 'A2A 受體', '#8a6a12'), (RX[2], 'A2A + 咖啡因', CAF)]:
    add('<text x="%s" y="%s" text-anchor="middle" class="lb halo" style="fill:%s">%s</text>' % (x + 30, MY - 24, col, zh))
# effects below membrane
eff = [(RX[0] + 30, ['Gi：cAMP ↓', '清醒神經元被抑制']), (RX[1] + 30, ['Gs：cAMP ↑', '促眠神經元被推動']), (RX[2] + 30, ['受體被佔住', '腺苷訊號擋掉 → 不睏'])]
for x, lines in eff:
    for k, t in enumerate(lines):
        add('<text x="%s" y="%s" text-anchor="middle" class="ls halo"%s>%s</text>' % (f(x), MY + 86 + k * 14, ' style="font-weight:600"' if k == 0 else '', t))

# --- ATP -> adenosine conversion chain in the space ---
def atp(x, y, n):
    o = [adeno(x, y, 4.8)]
    for k in range(n):
        o.append('<circle cx="%s" cy="%s" r="3.2" fill="#e7b04a" stroke="%s" stroke-width=".5"/>' % (f(x + 8 + k * 6.5), f(y), INK))
    return ''.join(o)


cy0 = 222
chain = [(40, 'ATP', 3), (104, 'ADP', 2), (162, 'AMP', 1), (214, '腺苷', 0)]
for i, (x, nm, n) in enumerate(chain):
    add(atp(x, cy0, n))
    add('<text x="%s" y="%s" class="ls halo" style="font-weight:600">%s</text>' % (x - 5, cy0 + 18, nm))
    if i < 3:
        xe = chain[i + 1][0] - 9
        xs_ = x + 10 + n * 6.5
        add('<path d="M%s %s H%s" class="ink" marker-end="url(#ink-arrow)"/>' % (f(xs_), cy0, f(xe)))
add('<text x="96" y="%s" class="ls halo" style="font-style:italic">CD39</text><text x="152" y="%s" class="ls halo" style="font-style:italic" text-anchor="end"></text>' % (cy0 - 10, cy0 - 10))
add('<text x="190" y="%s" class="ls halo" style="font-style:italic">CD73</text>' % (cy0 - 10))
add('<path d="M148 190 C140 200 60 196 44 212" stroke="%s" stroke-width=".9" fill="none" stroke-dasharray="3 2" marker-end="url(#ink-arrow)"/>' % INK)
add('<text x="40" y="%s" class="ls halo">釋到細胞外的 ATP 被酵素逐步拆成腺苷</text>' % (cy0 + 38))
# ATP release from astrocyte foot
add('<path d="M290 242 C292 256 296 266 300 274" stroke="%s" stroke-width=".9" fill="none" stroke-dasharray="3 2" marker-end="url(#ink-arrow)"/>' % INK)
add(atp(296, 284, 3))
add('<text x="318" y="262" class="ls halo">膠細胞也釋出 ATP</text>')
add('<text x="26" y="300" class="ls halo" style="font-style:italic">細胞外間隙 Extracellular space</text>')
# scattered adenosine accumulating
rr = random.Random(11)
for k in range(26):
    x = rr.uniform(30, 440); y = rr.uniform(272, 330)
    if (x < 200 and 286 < y < 306) or any(abs(x - (r + 30)) < 52 and y > MY - 44 for r in RX) or (284 < x < 330 and y < 292) or any(abs(x - (r + 30)) < 34 and y > 318 for r in RX) or (360 < x < 420 and y > 300):
        continue
    add(adeno(x, y, 3.4))

# ================= hourglass strip =================
HY = 520
add('<text x="14" y="%s" class="lt">沙漏：醒越久，腺苷越多</text>' % (HY - 6))
# hourglass icon
hx, hy = 34, HY + 34
hg = 'M%s %s h28 M%s %s h28' % (hx - 14, hy - 26, hx - 14, hy + 26)
add('<path d="M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s" fill="#fbf7ee" class="ink"/>' % (
    hx - 11, hy - 24, hx - 11, hy - 6, hx - 2, hy - 4, hx - 2, hy, hx - 2, hy + 4, hx - 11, hy + 6, hx - 11, hy + 24))
add('<path d="M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s" fill="#fbf7ee" class="ink"/>' % (
    hx + 11, hy - 24, hx + 11, hy - 6, hx + 2, hy - 4, hx + 2, hy, hx + 2, hy + 4, hx + 11, hy + 6, hx + 11, hy + 24))
add('<path d="M%s %s L%s %s L%s %s Z" fill="#e2c48a"/>' % (hx - 9, hy - 14, hx + 9, hy - 14, hx, hy - 2))
add('<path d="M%s %s Q%s %s %s %s Z" fill="#e2c48a"/>' % (hx - 10, hy + 23, hx, hy + 8, hx + 10, hy + 23))
add('<path d="M%s %s V%s" stroke="#c9a457" stroke-width="1"/>' % (hx, hy, hy + 16))
add('<path d="%s" class="ink3"/>' % hg)
boxes = [('07:00 起床', 3), ('15:00', 12), ('23:00 上床前', 30)]
for i, (t, n) in enumerate(boxes):
    bx = 70 + i * 130
    add('<rect x="%s" y="%s" width="118" height="52" rx="5" fill="#f4efe2" stroke="#bfae8a" stroke-width=".8"/>' % (bx, HY + 8))
    rb = random.Random(20 + i)
    for k in range(n):
        add(adeno(bx + rb.uniform(8, 110), HY + 16 + rb.uniform(0, 36), 3))
    add('<text x="%s" y="%s" text-anchor="middle" class="ls" style="font-weight:600">%s</text>' % (bx + 59, HY + 76, t))
    if i < 2:
        add('<path d="M%s %s h10" class="ink" marker-end="url(#ink-arrow)"/>' % (bx + 119, HY + 34))
add('<text x="70" y="%s" class="ls">睡著之後腺苷被清除，沙漏翻回來；白天補眠會提早漏掉一部分沙。</text>' % (HY + 96))

# ================= RIGHT: molecules =================
add('<path d="M470 24 V630" stroke="#d8c9a8" stroke-width="1"/>')
add('<text x="486" y="34" class="lt">結構比一比</text><text x="574" y="34" class="le">Adenosine vs caffeine</text>')
ad_svg, ad_pur, ad_all = mol_aligned('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O', 260, 250, 25)
cf_svg, cf_pur, cf_all = mol_aligned('Cn1cnc2c1c(=O)n(C)c(=O)n2C', 260, 210, 25)
D.append('<radialGradient id="%s-pt" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#f6e7b0"/><stop offset="1" stop-color="#f2d98a"/></radialGradient>' % P)
for (svg, pur, ox, oy, zh, en, sub) in [(ad_svg, ad_pur, 486, 48, '腺苷 Adenosine', '嘌呤 + 核糖', '睡眠壓力的訊號分子'),
                                        (cf_svg, cf_pur, 486, 340, '咖啡因 Caffeine', '1,3,7-三甲基黃嘌呤', 'A1／A2A 受體的拮抗劑')]:
    add('<g transform="translate(%s %s)"><path d="%s" fill="url(#%s-pt)" stroke="#d9b53c" stroke-width="1" stroke-dasharray="3 2"/>%s</g>' % (ox, oy, tint_hull(pur, 13), P, svg))
    add('<text x="%s" y="%s" class="lb">%s</text>' % (ox, oy + (258 if svg is ad_svg else 216), zh))
    add('<text x="%s" y="%s" class="le">%s　<tspan class="ls" style="font-style:normal">%s</tspan></text>' % (ox, oy + (272 if svg is ad_svg else 230), en, sub))

body = inline_classes('\n'.join(O))
cap = ('<b>圖 1-C　睡眠壓力的分子：腺苷與咖啡因。</b>醒著時神經元與星狀膠細胞消耗並釋出 ATP，細胞外的酵素（CD39、CD73）把它一路拆成腺苷，腺苷就隨清醒時數累積。'
       '腺苷作用在 A1 受體（抑制清醒神經元）與 A2A 受體（推動促眠迴路）；咖啡因的骨架和腺苷一樣是嘌呤環（右側淡黃色部分），所以能卡進受體口袋，卻不會啟動它，等於把「睏」的訊號擋掉。'
       '示意圖，突觸間隙與分子大小都經放大；腺苷的來源與受體分布在人體仍有不少未定之處。分子結構以 RDKit 依 SMILES 繪製。')
write(P, 'Plate 1·C', '睡眠壓力的分子：腺苷與咖啡因', 'Adenosine, the sleep-pressure molecule, and caffeine', 640, body,
      '突觸示意圖顯示腺苷累積並結合 A1 與 A2A 受體、咖啡因佔住 A2A 受體，右側為腺苷與咖啡因的結構式', cap, defs=''.join(D))
