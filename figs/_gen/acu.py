import sys, math, random
sys.path.insert(0, '/tmp/claude-0/-home-user-Insomnia/fe5a893d-7d06-5639-9e11-3b1ca5211939/scratchpad')
from common import *
from head import head

PID = 'pl-acupoints'
RED = '#a8412c'
body = []

def pt(x, y, main=True):
    if main:
        return ('<circle cx="%s" cy="%s" r="5.2" fill="#fbf6ea" stroke="%s" stroke-width="1.6"/><circle cx="%s" cy="%s" r="2.4" fill="%s"/>' % (f(x), f(y), RED, f(x), f(y), RED))
    return '<circle cx="%s" cy="%s" r="3.4" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/><circle cx="%s" cy="%s" r="1.3" fill="#2a2018"/>' % (f(x), f(y), f(x), f(y))

def plab(x, y, zh, code, en, note=None, anchor='start', red=True):
    a = ' text-anchor="end"' if anchor == 'end' else ''
    s = '<text x="%s" y="%s" class="lb halo"%s style="fill:%s">%s <tspan class="le">%s</tspan></text>' % (f(x), f(y), a, RED if red else '#2a2018', zh + ' ' + code, en)
    if note:
        for i, ln in enumerate(note.split('|')):
            s += '<text x="%s" y="%s" class="ls halo"%s>%s</text>' % (f(x), f(y + 14 + 13 * i), a, ln)
    return s

# ================= (a) palmar forearm =================
A = ['<g transform="translate(624 -33) rotate(90)"><g filter="url(#ink-rough)">']
WR = 250   # distal wrist crease y
CUN = 28.3
EL = WR + 12 * CUN
hand = [(118, 254), (110, 228), (104, 200), (104, 184), (96, 174), (84, 158), (75, 138), (73, 122), (78, 113), (88, 116), (95, 130), (104, 148), (113, 160),
        (114, 140), (112, 100), (112, 74), (117, 64), (124, 66), (127, 80), (128, 146), (130, 100), (129, 64), (132, 52), (139, 50), (144, 58), (145, 100), (146, 146),
        (148, 104), (148, 70), (152, 60), (159, 61), (163, 72), (164, 148), (166, 120), (168, 92), (172, 84), (178, 85), (182, 96), (183, 128), (185, 160), (187, 192), (186, 226), (182, 254)]
arm = [(182, 254), (187, 290), (192, 360), (197, 450), (202, 530), (205, 590), (206, 606), (98, 606), (98, 590), (101, 530), (106, 450), (110, 360), (114, 290), (118, 254)]
outline = smooth(hand + arm[1:-1], close=True, t=0.42)
A.append('<path d="%s" fill="url(#ink-vol-flesh)"/>' % outline)
# shading ulnar side
A.append('<clipPath id="pl-acupoints-a"><path d="%s"/></clipPath>' % outline)
A.append('<path d="M176 40 L230 40 L230 610 L186 610 Q180 400 170 260z" fill="url(#ink-hatch-l)" clip-path="url(#pl-acupoints-a)"/>')
# thenar / hypothenar eminences
A.append('<path d="M108 230 Q120 190 112 165 Q130 180 132 230z" fill="#e2b49a" fill-opacity=".5"/>')
A.append('<path d="M184 232 Q170 200 180 168 Q166 190 166 236z" fill="#e2b49a" fill-opacity=".5"/>')
# palmar creases
A.append('<path d="M126 152 Q112 190 128 242" class="ink2" stroke-width=".8"/>')
A.append('<path d="M114 168 Q136 170 162 186" class="ink2" stroke-width=".8"/>')
A.append('<path d="M140 158 Q160 160 184 170" class="ink2" stroke-width=".8"/>')
# finger flexion creases
for (x0, x1, ys) in [(113, 127, (126, 104, 84)), (129, 145, (124, 98, 72)), (147, 163, (126, 102, 80)), (166, 182, (134, 114, 98))]:
    for y in ys:
        A.append('<path d="M%d %d q%s 3 %d 0" class="ink2" stroke-width=".6"/>' % (x0 + 1, y, f((x1 - x0) / 2), x1 - x0 - 2))
A.append('<path d="M84 138 q6 4 12 0 M90 154 q6 3 10 -1" class="ink2" stroke-width=".6"/>')
# wrist creases
for k, yy in enumerate([WR, WR + 7, WR + 13]):
    A.append('<path d="M%d %d Q150 %d %d %d" class="ink2" stroke-width="%s"/>' % (116 + k, yy, yy + 4, 184 - k, yy, '.9' if k == 0 else '.5'))
# tendons: FCR (radial), PL (centre), FCU (ulnar)
def tendon(xw, xe, w, yb, col='#f3e3d6'):
    L = [(xw - w / 2, WR - 4), (xw - w / 2 - 1, WR + 60), (xe - w, yb)]
    R = [(xe + w, yb), (xw + w / 2 + 1, WR + 60), (xw + w / 2, WR - 4)]
    d = smooth(L + R, close=False)
    return ('<path d="%s Z" fill="%s" fill-opacity=".8"/>' % (d, col) +
            '<path d="%s" class="ink2" stroke-width=".8"/>' % smooth(L) + '<path d="%s" class="ink2" stroke-width=".8"/>' % smooth(R))
A.append(tendon(133, 128, 7, 360))
A.append(tendon(150, 150, 4.5, 350))
A.append(tendon(176, 180, 8, 370))
# muscle bellies (proximal)
for (x, w) in [(126, 16), (150, 12), (180, 16)]:
    A.append('<path d="M%d 360 q%d 70 %d 200" class="ink2" stroke-opacity=".5"/>' % (x, -w / 2, -w / 4))
    A.append('<path d="M%d 360 q%d 70 %d 200" class="ink2" stroke-opacity=".5"/>' % (x + 6, w / 2, w / 4))
# radial artery
A.append('<path d="M120 %d Q116 380 112 470" stroke="#b5473a" stroke-width="1.4" fill="none" stroke-dasharray="4 2"/>' % (WR - 6))
# pisiform (beneath skin)
A.append('<ellipse cx="180" cy="%d" rx="7" ry="6" fill="#efe6d2" fill-opacity=".8" stroke="#2a2018" stroke-width=".8" stroke-dasharray="2 1.5"/>' % (WR - 4))
# cubital crease
A.append('<path d="M100 %s Q150 %s 204 %s" class="ink2" stroke-width=".9"/>' % (f(EL), f(EL + 8), f(EL)))
A.append('<path d="%s" class="ink3" stroke-width="1.5"/>' % outline)
A.append('</g>')
# ruler (寸) along the ulnar side (drawn in the rotated frame)
RX = 226
A.append('<path d="M%d %d V%s" stroke="#2a2018" stroke-width=".9"/>' % (RX, WR, f(EL)))
for k in range(13):
    y = WR + k * CUN
    A.append('<path d="M%d %s h%d" stroke="#2a2018" stroke-width=".8"/>' % (RX - (6 if k % 2 == 0 else 3), f(y), 6 if k % 2 == 0 else 3))
A.append('<path d="M%d %d L%d %d" class="ld" stroke-dasharray="2 2"/>' % (186, WR, RX, WR))
A.append('<path d="M%d %s L%d %s" class="ld" stroke-dasharray="2 2"/>' % (146, f(WR + 2 * CUN), RX, f(WR + 2 * CUN)))
A.append('</g>')
def T(x, y): return (624 - y, -33 + x)
HT7 = T(170, WR + 1); PC6 = T(141, WR + 2 * CUN); PC7 = T(141, WR + 1)
A.append(pt(*HT7)); A.append(pt(*PC6)); A.append(pt(*PC7, main=False))
for k in (0, 2, 12):
    X, Y_ = T(RX, WR + k * CUN)
    A.append('<text x="%s" y="%s" text-anchor="middle" class="ls">%s</text>' % (f(X), f(Y_ + 16), '%d 寸' % k if k != 2 else '2'))
A.append('<text x="14" y="226" class="ls">腕橫紋→肘橫紋 ＝ 12 寸（骨度分寸）</text>')
# above-row labels (targets ordered left→right)
A.append(label(14, 22, '橈動脈', None, cls='ls halo') + label(14, 35, 'radial a.', None, cls='le halo') + leader(40, 40, *T(118, 420)))
A.append(label(92, 22, '橈側腕屈肌腱', None, cls='ls halo') + label(92, 35, 'FCR tendon', None, cls='le halo') + leader(130, 40, *T(131, 330)))
A.append(plab(196, 22, '內關', 'PC6', 'Neiguan', '腕橫紋上 2 寸，|掌長肌腱與 FCR 之間'))
A.append(leader(300, 60, PC6[0] - 3, PC6[1] - 5))
A.append(label(360, 22, '大陵 PC7', None, cls='ls halo') + label(360, 35, '（參考）', None, cls='ls halo') + leader(372, 40, PC7[0], PC7[1] - 4))
# below-row labels
A.append(label(330, 246, '掌長肌腱', None, cls='ls halo') + label(330, 259, 'palmaris longus', None, cls='le halo') + leader(346, 234, *T(150, 320)))
A.append(label(226, 246, '尺側腕屈肌腱', None, cls='ls halo') + label(226, 259, 'FCU tendon', None, cls='le halo') + leader(250, 234, *T(178, 380)))
A.append(plab(400, 204, '神門', 'HT7', 'Shenmen', '腕橫紋尺側端，|尺側腕屈肌腱橈側凹陷'))
A.append(leader(398, 200, HT7[0] + 2, HT7[1] + 5))
A.append(label(560, 196, '豌豆骨', None, cls='ls halo') + label(560, 209, 'pisiform', None, cls='le halo') + leader(558, 192, *T(182, WR - 5)))
A.append(label(470, 22, '腕橫紋', None, cls='ls halo') + leader(486, 26, *T(118, WR)))
# right side notes
A.append(label(600, 70, '(a) 右前臂掌側', None, cls='lb') + label(600, 84, 'right forearm, palmar', None, cls='le'))
A.append('<text x="600" y="112" class="ls">上緣＝橈側（拇指側）</text><text x="600" y="126" class="ls">下緣＝尺側（小指側）</text>')
body.append('\n'.join(A))
body.append('<path d="M10 270 H750" class="panel"/><path d="M292 278 V 652" class="panel"/><path d="M546 278 V 652" class="panel"/>')

def nlab(x, y, zh, en, notes, red=True, w=None):
    s_ = '<text x="%s" y="%s" class="lb halo" style="fill:%s">%s</text>' % (f(x), f(y), RED if red else '#2a2018', zh)
    s_ += '<text x="%s" y="%s" class="le halo">%s</text>' % (f(x), f(y + 14), en)
    for i, ln in enumerate(notes.split('|') if notes else []):
        s_ += '<text x="%s" y="%s" class="ls halo">%s</text>' % (f(x), f(y + 28 + 13 * i), ln)
    return s_

# ================= (c) head profile =================
Hs, HX, HY = 2.2, 150, 330
C = ['<g filter="url(#ink-rough)">', head(HX, HY, Hs, 0, eyes='closed', hair='#5a4232')]
C.append('<path d="M%s %s q-4 30 -20 44 M%s %s q2 26 26 40" class="ink" />' % (f(HX - 9.5 * Hs), f(HY + 72 * Hs), f(HX + 8.5 * Hs), f(HY + 72 * Hs)))
C.append('<path d="%s" class="ink2" stroke-opacity=".7"/>' % smooth([(HX - 3 * Hs, HY + 44 * Hs), (HX + 1 * Hs, HY + 56 * Hs), (HX + 7 * Hs, HY + 70 * Hs)]))
C.append('<path d="%s" class="ink2" stroke-opacity=".7"/>' % smooth([(HX - 14 * Hs, HY + 47 * Hs), (HX - 12 * Hs, HY + 58 * Hs), (HX - 10 * Hs, HY + 72 * Hs)]))
C.append('</g>')
def H(x, y): return (HX + x * Hs, HY + y * Hs)
GV20 = H(1, -3.2); TE17 = H(-4.8, 42.5); GB20 = H(-13, 45); AM = ((TE17[0] + GB20[0]) / 2, (TE17[1] + GB20[1]) / 2); YT = H(20.3, 22)
apex = H(0, 25.5)
C.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="1" stroke-dasharray="3 3"/>' % (f(apex[0]), f(apex[1]), f(GV20[0]), f(GV20[1] + 5), RED))
C.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="1" stroke-dasharray="2 2"/>' % (f(TE17[0]), f(TE17[1]), f(GB20[0]), f(GB20[1]), RED))
for p in (GV20, AM, YT):
    C.append(pt(*p))
C.append(pt(*TE17, main=False)); C.append(pt(*GB20, main=False))
C.append(label(14, 292, '(c) 頭側面', None, cls='lb') + label(14, 306, 'head, lateral', None, cls='le'))
C.append(nlab(196, 296, '百會 GV20', 'Baihui', '頭頂正中，|兩耳尖連線中點'))
C.append(leader(194, 292, GV20[0] + 5, GV20[1] - 2))
C.append(nlab(206, 372, '印堂 GV29', 'Yintang', '兩眉頭中點|舊編號 EX-HN3'))
C.append(leader(204, 368, YT[0] + 5, YT[1] + 2))
C.append(nlab(14, 478, '風池 GB20', 'Fengchi', '枕骨下凹陷', red=False))
C.append(leader(84, 474, GB20[0] - 3, GB20[1] + 3))
C.append(nlab(14, 540, '安眠', 'Anmian', '翳風–風池中點|經外奇穴，|無 WHO 代碼'))
C.append(leader(46, 536, AM[0] - 1, AM[1] + 4))
C.append(nlab(150, 560, '翳風 TE17', 'Yifeng', '耳垂後凹陷', red=False))
C.append(leader(176, 546, TE17[0] + 2, TE17[1] + 4))
body.append('\n'.join(C))

# ================= (b) medial lower leg =================
DX, DY = 2, 12
B = ['<g transform="translate(%d %d)"><g filter="url(#ink-rough)">' % (DX, DY)]
MT = 586
KN = 334
CB = (MT - KN) / 13.0
leg = [(352, 318), (356, 360), (362, 420), (368, 480), (373, 540), (376, 574), (372, 596), (350, 606), (322, 614), (304, 620), (300, 628), (318, 632), (360, 632),
       (420, 632), (446, 628), (450, 614), (440, 596), (428, 574), (424, 540), (430, 490), (446, 440), (460, 392), (458, 350), (448, 318)]
lg = smooth(leg, close=False, t=0.45)
B.append('<path d="%s" fill="url(#ink-vol-flesh)"/>' % lg)
B.append('<clipPath id="pl-acupoints-b"><path d="%s"/></clipPath>' % lg)
B.append('<path d="M420 300 L470 300 L470 640 L430 640 Q420 520 440 440z" fill="url(#ink-hatch-l)" clip-path="url(#pl-acupoints-b)"/>')
tib = [(366, 334), (378, 400), (386, 470), (392, 530), (398, 568)]
B.append('<path d="%s" stroke="#8a6a3a" stroke-width="1.2" fill="none" stroke-dasharray="5 3"/>' % smooth(tib))
B.append('<path d="M450 344 Q440 420 430 500" class="ink2" stroke-opacity=".6"/>')
B.append('<path d="M434 512 Q428 560 436 600" class="ink2"/><path d="M424 520 Q420 560 426 598" class="ink2" stroke-opacity=".6"/>')
B.append('<ellipse cx="402" cy="%d" rx="13" ry="11" fill="#efd2bc" stroke="#2a2018" stroke-width="1"/>' % (MT - 9))
B.append('<path d="M394 %d q8 -6 16 0" class="ink2"/>' % (MT - 12))
B.append('<path d="M330 628 Q370 616 420 628" class="ink2" stroke-opacity=".6"/>')
B.append('<path d="M304 620 q4 -6 12 -4" class="ink2"/>')
B.append('<path d="%s" class="ink3" stroke-width="1.5"/>' % lg)
B.append('</g>')
SP6 = (397, MT - 3 * CB); KI3 = (414, MT - 2); KI7 = (424, MT - 2 - 2 * CB)
RX = 344
B.append('<path d="M402 %d H%d M%s %s H%d" class="ld" stroke-dasharray="2 2"/>' % (MT, RX, f(SP6[0]), f(SP6[1]), RX))
B.append('<path d="M%d %d V%s" stroke="#2a2018" stroke-width=".9"/>' % (RX, MT, f(MT - 3 * CB)))
for k in range(4):
    B.append('<path d="M%d %s h6" stroke="#2a2018" stroke-width=".8"/>' % (RX - 3, f(MT - k * CB)))
B.append('<text x="%d" y="%s" class="ls halo" text-anchor="end">3 寸</text>' % (RX - 5, f(MT - 1.5 * CB + 4)))
B.append(pt(*SP6)); B.append(pt(*KI7, main=False)); B.append(pt(*KI3, main=False))
B.append('</g>')
def Lg(p): return (p[0] + DX, p[1] + DY)
B.append(label(300, 292, '(b) 右小腿內側', None, cls='lb') + label(300, 306, 'right leg, medial', None, cls='le'))
B.append('<text x="300" y="322" class="ls">內踝尖→陰陵泉 ＝ 13 寸</text>')
B.append(nlab(470, 372, '三陰交', 'SP6 Sanyinjiao', '內踝尖上 3 寸|脛骨內側緣|後方'))
B.append(leader(468, 368, Lg(SP6)[0] + 5, Lg(SP6)[1] - 3))
B.append(nlab(470, 466, '復溜 KI7', 'Fuliu', '太溪上 2 寸|第 13 章用穴', red=False))
B.append(leader(468, 462, Lg(KI7)[0] + 3, Lg(KI7)[1] - 2))
B.append(label(470, 560, '內踝', None, cls='ls halo') + label(470, 573, 'med. malleolus', None, cls='le halo') + leader(468, 556, 412 + DX, MT - 12 + DY))
B.append(label(470, 616, '太溪 KI3', None, cls='ls halo') + leader(468, 612, Lg(KI3)[0] + 3, Lg(KI3)[1] + 2))
B.append(label(300, 410, '脛骨', None, cls='ls halo') + label(300, 423, '內側緣', None, cls='ls halo') + leader(336, 420, 384 + DX, 470 + DY))
body.append('\n'.join(B))

# ================= (d) ear =================
E = ['<g filter="url(#ink-rough)">']
ES, EX, EY = 1.3, 556, 318
def e(x, y): return (EX + x * ES, EY + y * ES)
ear = [(78, 30), (66, 8), (44, 0), (22, 8), (8, 30), (6, 58), (12, 86), (22, 108), (24, 126), (32, 144), (46, 151), (58, 144), (62, 128), (64, 114),
       (70, 104), (78, 92), (82, 80), (78, 68), (74, 58), (76, 44)]
ed = smooth([e(*p) for p in ear], close=True)
E.append('<path d="%s" fill="#f0cdb6"/>' % ed)
# helix rim (scapha inner edge)
E.append('<path d="%s" class="ink" stroke-width=".9"/>' % smooth([e(*p) for p in [(70, 22), (50, 10), (30, 14), (17, 32), (15, 60), (20, 86), (30, 106), (36, 112)]]))
E.append('<path d="%s" fill="url(#ink-hatch-l)"/>' % smooth([e(*p) for p in [(66, 8), (44, 0), (22, 8), (8, 30), (6, 58), (12, 86), (22, 108), (30, 106), (20, 86), (15, 60), (17, 32), (30, 14), (50, 10), (70, 22)]], close=True))
# antihelix body & crura (Y shape)
E.append('<path d="%s" stroke="#2a2018" stroke-width="1" fill="none"/>' % smooth([e(*p) for p in [(46, 112), (38, 94), (34, 72), (38, 52)]]))
E.append('<path d="%s" stroke="#2a2018" stroke-width="1" fill="none"/>' % smooth([e(*p) for p in [(38, 52), (40, 34), (50, 18)]]))     # superior crus
E.append('<path d="%s" stroke="#2a2018" stroke-width="1" fill="none"/>' % smooth([e(*p) for p in [(38, 52), (54, 44), (70, 40)]]))     # inferior crus
E.append('<path d="%s" class="ink2" stroke-opacity=".6"/>' % smooth([e(*p) for p in [(52, 108), (44, 92), (42, 72), (46, 56)]]))
# triangular fossa (shaded)
E.append('<path d="%s" fill="#dcae93" fill-opacity=".7"/>' % smooth([e(*p) for p in [(42, 48), (44, 32), (52, 22), (66, 24), (70, 36), (56, 42)]], close=True))
# concha (cymba + cavum)
E.append('<path d="%s" fill="#d79a86" fill-opacity=".75" stroke="#2a2018" stroke-width=".7"/>' % smooth([e(*p) for p in [(44, 58), (60, 48), (74, 54), (72, 66), (58, 64)]], close=True))
E.append('<path d="%s" fill="#c98a76" fill-opacity=".8" stroke="#2a2018" stroke-width=".7"/>' % smooth([e(*p) for p in [(44, 74), (60, 68), (74, 72), (76, 92), (66, 106), (52, 104), (44, 92)]], close=True))
E.append('<path d="%s" fill="#3a2018" fill-opacity=".8"/>' % smooth([e(*p) for p in [(66, 78), (72, 76), (72, 88), (66, 88)]], close=True))
# helix crus
E.append('<path d="%s" stroke="#2a2018" stroke-width="1.2" fill="none"/>' % smooth([e(*p) for p in [(78, 52), (68, 60), (54, 66)]]))
# tragus & antitragus
E.append('<path d="%s" fill="#f0cdb6" stroke="#2a2018" stroke-width=".9"/>' % smooth([e(*p) for p in [(78, 70), (84, 78), (80, 92), (74, 86)]], close=True))
E.append('<path d="%s" fill="#f0cdb6" stroke="#2a2018" stroke-width=".9"/>' % smooth([e(*p) for p in [(46, 106), (54, 104), (60, 112), (50, 116)]], close=True))
E.append('<path d="%s" class="ink3" stroke-width="1.4"/>' % ed)
E.append('</g>')
SM = e(48, 36)
E.append(pt(*SM))
E.append(label(552, 292, '(d) 右耳', None, cls='lb') + label(552, 306, 'right auricle', None, cls='le'))
E.append(nlab(552, 560, '耳穴神門 TF4', 'ear Shenmen', '三角窩後 1/3 上部|耳穴國標 GB/T 13734'))
E.append(leader(580, 548, SM[0] - 2, SM[1] + 4))
for (zh, en, p, lx, ly) in [('三角窩', 'tri. fossa', (62, 32), 684, 330), ('對耳輪', 'antihelix', (36, 80), 684, 380), ('耳甲', 'concha', (62, 94), 684, 430),
                            ('耳屏', 'tragus', (82, 80), 684, 480), ('耳輪', 'helix', (10, 50), 684, 526)]:
    E.append(label(lx, ly, zh, None, cls='ls halo') + label(lx, ly + 13, en, None, cls='le halo') + leader(lx - 2, ly - 4, *e(*p)))
body.append('\n'.join(E))

cap = ('<b>圖 13-A　失眠常用穴位。</b>依 WHO 西太平洋區《標準針灸穴位定位》（2008）與中國耳穴國標重繪的示意圖。'
       '寸為「骨度分寸」：腕橫紋到肘橫紋 12 寸、內踝尖到脛骨內側髁下緣 13 寸，所以每個人的 1 寸長度不同。神門在腕橫紋尺側端、尺側腕屈肌腱的橈側；內關在腕上 2 寸兩條肌腱之間；三陰交在內踝尖上 3 寸、脛骨內側緣後方。'
       '安眠是經外奇穴，沒有 WHO 標準代碼；印堂在 2006 年後的標準中歸入督脈（GV29）。第 13 章試驗（神門＋復溜）的復溜一併標出。證據強度見本章表格。')
open('/home/user/Insomnia/figs/pl-acupoints.html', 'w').write(figure(PID, 'Plate 13·A', '失眠常用穴位', 'Acupoints commonly used for insomnia', 656,
                                                            '前臂掌側（神門、內關）、小腿內側（三陰交）、頭側面（百會、安眠、印堂）與耳穴神門的定位圖', '\n'.join(body), cap))
