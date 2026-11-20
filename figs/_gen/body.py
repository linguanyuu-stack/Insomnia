"""Front-view standing human figure (anatomical position, palms forward), 7.5 heads.
Local coords: x=0 midline, y=0 top of head, sole at 452. Positive x = viewer's right."""
import math
from common import smooth, f, pts

def _arm_off(y):
    return max(0, (y - 92)) * 0.13

# right half (viewer's right) contour, top of head -> crotch
HEAD = [(0, 0), (13, 2), (22, 9), (26, 21), (26.5, 32), (24, 43), (19, 52), (11, 58.5), (0, 61)]
def right_half():
    P = []
    P += [(0, 0), (13, 2), (22, 9), (26, 21)]
    # ear
    P += [(27.5, 27), (29.5, 30), (29, 38), (26, 42)]
    P += [(23, 47), (18, 53), (11, 58.5)]
    # neck
    P += [(11.5, 64), (13, 72)]
    # trapezius & shoulder
    P += [(26, 79), (42, 84), (53, 89)]
    arm_outer = [(60, 100), (63, 115), (62, 135), (60, 160), (59, 180), (57, 200), (54, 225), (50, 242)]
    hand_o = [(50, 252), (51, 266), (49, 282), (45, 296), (40, 300), (36, 296)]
    hand_i = [(33, 284), (31, 272), (28, 264), (30, 258), (35, 256), (37, 248)]
    arm_inner = [(40, 228), (44, 200), (46, 182), (45, 160), (43, 140), (39, 124)]
    for (x, y) in arm_outer + hand_o + hand_i + arm_inner:
        P.append((x + _arm_off(y), y))
    # torso side
    P += [(36, 132), (37, 150), (33, 175), (31, 190), (34, 210), (40, 230), (43, 250)]
    # leg outer
    P += [(42, 275), (39, 305), (35, 335), (33, 350), (34, 368), (34, 388), (30, 415), (26, 432)]
    # foot (front view, toes forward)
    P += [(27, 440), (29, 448), (25, 453), (12, 453), (8, 447)]
    # leg inner
    P += [(10, 436), (12, 418), (14, 395), (12, 370), (13, 350), (13, 335), (12, 300), (8, 268), (4, 250), (0, 244)]
    return P

def outline(cx, top, s):
    R = right_half()
    L = [(-x, y) for (x, y) in reversed(R)]
    allp = R[:-1] + L[1:-1]
    T = [(cx + x * s, top + y * s) for (x, y) in allp]
    return smooth(T, close=True, t=0.45)

def details(cx, top, s, eyes='open', sex_neutral=True):
    """inner contour lines: clavicles, chest, navel, knees, face, hair, hands."""
    def T(P):
        return [(cx + x * s, top + y * s) for (x, y) in P]
    out = []
    def line(P, cls='ink2', extra=''):
        out.append('<path d="%s" class="%s"%s/>' % (smooth(T(P)), cls, extra))
    for sg in (1, -1):
        m = lambda P: [(sg * x, y) for (x, y) in P]
        line(m([(3, 80), (14, 79), (28, 81), (44, 86)]))                      # clavicle
        line(m([(6, 104), (16, 116), (30, 118), (38, 112)]))                  # pectoral lower edge
        line(m([(22, 96), (36, 100), (44, 110)]), extra=' stroke-opacity=".6"')  # deltopectoral
        line(m([(10, 150), (14, 172), (16, 196), (22, 222), (6, 240)]), extra=' stroke-opacity=".5"')  # linea semilunaris / inguinal
        line(m([(18, 340), (24, 336), (28, 344), (26, 356), (19, 358), (16, 349), (18, 340)]))   # patella
        line(m([(20, 380), (24, 405), (22, 425)]), extra=' stroke-opacity=".5"')  # tibia
        line(m([(42 + _arm_off(180), 178), (52 + _arm_off(185), 186)]), extra=' stroke-opacity=".6"')  # elbow crease
        # fingers (palm forward): lines on hand
        for k, xx in enumerate([36, 40, 44]):
            line(m([(xx + _arm_off(270), 276 + k), (xx + _arm_off(290) - 1, 294 - k * 0.5)]), extra=' stroke-width=".4"')
        line(m([(30 + _arm_off(262), 262), (34 + _arm_off(272), 270)]), extra=' stroke-width=".45"')  # thumb crease
        # ear detail
        line(m([(27, 30), (28, 35), (27, 39)]), extra=' stroke-width=".4"')
        # brow
        line(m([(4, 22), (10, 20), (17, 22)]), cls='ink2', extra=' stroke-width=".9"')
        # eyes
        if eyes == 'open':
            out.append('<path d="%s" class="ink2" stroke-width=".7" style="fill:#fbf6ea"/>' % smooth(T(m([(5, 28.5), (10, 26), (16, 28.5), (10, 30.5)])), close=True))
            ix, iy = T([(sg * 10.3, 28.3)])[0]
            out.append('<circle cx="%s" cy="%s" r="%s" fill="#3a2a1c"/>' % (f(ix), f(iy), f(1.9 * s)))
        else:
            line(m([(5, 29), (10, 30.6), (16, 29)]), extra=' stroke-width=".8"')
            for xx in (8, 11, 14):
                line(m([(xx, 30.4), (xx - .3, 32)]), extra=' stroke-width=".35"')
    line([(0, 166), (0, 167)], 'ink')                      # navel
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" class="ink2"/>' % (f(cx), f(top + 168 * s), f(1.6 * s), f(2.2 * s)))
    line([(0, 84), (0, 132)], extra=' stroke-opacity=".45"')   # sternum
    # nose & mouth
    line([(-1.5, 31), (-2.5, 40), (-4, 42.5), (0, 44), (4, 42.5)])
    line([(-6, 49), (-2, 48.4), (0, 49), (2, 48.4), (6, 49)], extra=' stroke-width=".8"')
    line([(-4, 52), (0, 53), (4, 52)], extra=' stroke-opacity=".6"')
    # neck lines (sternocleidomastoid)
    line([(-9, 60), (-4, 76)], extra=' stroke-opacity=".5"'); line([(9, 60), (4, 76)], extra=' stroke-opacity=".5"')
    return '\n'.join(out)

def hair(cx, top, s, fill='#3a2a1c'):
    P = [(-27, 26), (-28, 12), (-20, 1), (-6, -4), (8, -4), (21, 1), (28, 12), (27, 26), (24, 20), (22, 12), (14, 8), (2, 10), (-10, 8), (-20, 12), (-24, 20)]
    T = [(cx + x * s, top + y * s) for (x, y) in P]
    # topknot (Ming-style hair bun)
    K = [(-7, -3), (-8, -10), (-3, -15), (3, -15), (8, -10), (7, -3)]
    TK = [(cx + x * s, top + y * s) for (x, y) in K]
    return ('<path d="%s" fill="%s" stroke="#2a2018" stroke-width=".8"/>' % (smooth(T, close=True), fill) +
            '<path d="%s" fill="%s" stroke="#2a2018" stroke-width=".8"/>' % (smooth(TK, close=True), fill) +
            '<path d="M%s %s h%s" stroke="#c9962e" stroke-width="1.6"/>' % (f(cx - 8 * s), f(top - 4 * s), f(16 * s)))

def pt(cx, top, s, x, y):
    return (cx + x * s, top + y * s)
