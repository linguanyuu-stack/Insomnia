# helper components for plates
import math

INK = "#2a2018"

def fig(pid, pn, ptt, pte, h, aria, body, cap):
    return f'''<figure class="plate" id="{pid}">
  <div class="pt"><span class="pn">{pn}</span><span class="ptt">{ptt}</span><span class="pte">{pte}</span></div>
  <svg viewBox="0 0 760 {h}" role="img" aria-label="{aria}">
{body}
  </svg>
  <figcaption>{cap}</figcaption>
</figure>
'''

def write(pid, html):
    open(f"/home/user/Insomnia/figs_public/{pid}.html", "w").write(html)


def lab(x, y, zh, en=None, anchor="start", cls="lb", two=False, ecls="le"):
    """label: zh bold + English italic (same line or next line)."""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    if en is None:
        return f'<text x="{x}" y="{y}" class="{cls} halo"{a}>{zh}</text>'
    if two:
        return (f'<text x="{x}" y="{y}" class="{cls} halo"{a}>{zh}</text>'
                f'<text x="{x}" y="{y+13}" class="{ecls} halo"{a}>{en}</text>')
    return f'<text x="{x}" y="{y}" class="{cls} halo"{a}>{zh} <tspan class="{ecls}">{en}</tspan></text>'


def lead(pts, dot_end=True):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    m = ' marker-end="url(#ink-dot)"' if dot_end else ""
    return f'<path class="ld" d="{d}"{m}/>'


def clock(x, y, r, hh, mm, face="#fbf6ea", ink=INK, numerals=True):
    s = [f'<g transform="translate({x},{y})">',
         f'<circle r="{r+2.5}" fill="#8a6a3a" stroke="{ink}" stroke-width="1"/>',
         f'<circle r="{r}" fill="{face}" stroke="{ink}" stroke-width=".8"/>']
    for i in range(60):
        a = math.radians(i * 6)
        l = r * (0.82 if i % 5 == 0 else 0.9)
        w = 1.1 if i % 5 == 0 else .4
        s.append(f'<line x1="{r*.97*math.sin(a):.2f}" y1="{-r*.97*math.cos(a):.2f}" x2="{l*math.sin(a):.2f}" y2="{-l*math.cos(a):.2f}" stroke="{ink}" stroke-width="{w}"/>')
    ha = math.radians((hh % 12 + mm / 60) * 30)
    ma = math.radians(mm * 6)
    s.append(f'<line x1="0" y1="0" x2="{r*.5*math.sin(ha):.2f}" y2="{-r*.5*math.cos(ha):.2f}" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>')
    s.append(f'<line x1="0" y1="0" x2="{r*.78*math.sin(ma):.2f}" y2="{-r*.78*math.cos(ma):.2f}" stroke="{ink}" stroke-width="1.2" stroke-linecap="round"/>')
    s.append(f'<circle r="1.6" fill="{ink}"/></g>')
    return "".join(s)


# ---------- human head in profile, facing +x, origin ~ centre of cranium; height ~84 (crown -42 .. chin 40)
FACE = ("M18 -36 C26 -30 29 -22 30 -12 C31 -8 31 -6 29 -3 C32 2 37 7 40 10 C41 12 38 14.5 34 14 "
        "C33 15 34 16 35 17.5 C35 19 33.5 20 32 20 C34 21 34 24 32 25.5 C30 26.5 29 27.5 30 29.5 "
        "C32 33 31 37 27 39 C22 41 16 41 11 41 C9 44 9 50 10 60")
CRANIUM = "M18 -36 C6 -46 -22 -44 -30 -24 C-36 -10 -32 6 -24 16 C-20 22 -16 28 -16 34 L-16 60"
HEAD_FILL = (FACE + " L-16 60 L-16 34 C-16 28 -20 22 -24 16 C-32 6 -36 -10 -30 -24 C-22 -44 6 -46 18 -36Z")


def head(x, y, s=1.0, rot=0, eye="open", hair="short", age="adult", mouth="closed", sweat=False, pid="x", flip=False):
    fl = " scale(-1,1)" if flip else ""
    g = [f'<g transform="translate({x},{y}) rotate({rot}) scale({s}){fl}">']
    # neck/head flesh
    g.append(f'<path d="{HEAD_FILL}" fill="url(#ink-vol-flesh)" stroke="none"/>')
    # shadow under jaw & back of neck
    g.append('<path d="M-16 34 C-10 36 -2 38 8 41 C9 46 9 52 10 60 L-16 60Z" fill="url(#ink-hatch-l)"/>')
    g.append('<path d="M-6 20 C2 30 12 36 24 38 C18 40 12 41 9 41 C0 38 -8 30 -10 22Z" fill="#dcae93" opacity=".35"/>')
    # hair
    if hair == "short":
        g.append('<path d="M23 -30 C16 -47 -18 -50 -31 -28 C-38 -15 -36 3 -28 15 C-25 20 -21 22 -17 23 C-20 14 -21 4 -17 -4 '
                 'C-12 -12 -6 -16 0 -18 C6 -24 14 -25 23 -30Z" fill="#5a4330" stroke="#2a2018" stroke-width=".9"/>')
        g.append('<path d="M20 -31 C8 -40 -10 -42 -24 -30 M14 -27 C2 -36 -14 -36 -26 -22 M6 -22 C-6 -28 -20 -24 -28 -10 '
                 'M-4 -17 C-14 -18 -24 -10 -27 2 M-18 -6 C-24 2 -24 10 -21 18" fill="none" stroke="#c9a77f" stroke-width=".6" opacity=".8"/>')
    elif hair == "grey":
        g.append('<path d="M10 -40 C-6 -46 -24 -40 -31 -26 C-37 -14 -35 3 -28 15 C-25 20 -21 22 -17 23 C-20 14 -21 4 -17 -4 '
                 'C-14 -12 -14 -20 -10 -26 C-4 -34 4 -38 10 -40Z" fill="#d8d2c6" stroke="#2a2018" stroke-width=".9"/>')
        g.append('<path d="M0 -40 C-14 -40 -24 -32 -28 -20 M-6 -34 C-18 -32 -26 -20 -28 -6 M-14 -22 C-22 -12 -24 0 -22 14" fill="none" stroke="#8b8172" stroke-width=".55"/>')
        # wrinkles
        g.append('<path d="M24 -24 C26 -23 27 -22 28 -20 M23 -19 C25 -18 27 -17 29 -16 M21 2 C19 3 18 5 18 7 M30 15 C27 19 27 24 29 28 '
                 'M14 6 C16 12 22 16 28 17" class="ink2" stroke-opacity=".7"/>')
    elif hair == "long":
        g.append('<path d="M24 -29 C18 -48 -20 -52 -33 -28 C-41 -12 -38 12 -36 30 C-35 44 -30 56 -22 62 C-14 64 -8 62 -6 58 '
                 'C-14 50 -18 40 -16 30 C-20 18 -21 4 -17 -4 C-12 -12 -4 -18 2 -20 C10 -24 18 -25 24 -29Z" fill="#4b3526" stroke="#2a2018" stroke-width=".9"/>')
        g.append('<path d="M20 -31 C6 -42 -14 -44 -28 -28 M12 -26 C-2 -36 -20 -32 -32 -12 M2 -20 C-12 -24 -26 -12 -32 10 '
                 'M-18 -4 C-26 10 -30 28 -26 48 M-14 6 C-20 22 -22 40 -14 56 M-30 0 C-34 20 -32 40 -24 58" fill="none" stroke="#b08e6b" stroke-width=".6" opacity=".85"/>')
    # ear
    g.append('<path d="M-3 -6 C2 -8 4.5 0 2.5 8 C1 12 -2.5 13 -4.5 10 C-6.5 6 -8 -2.5 -3 -6Z" fill="#efc9b0" stroke="#2a2018" stroke-width=".8"/>')
    g.append('<path d="M-2 -3 C2 -4 3 2 1 7 M-3 2 C-1 2 -1 5 -2 6" class="ink2"/>')
    # contour lines
    g.append(f'<path d="{FACE}" class="ink" stroke-width="1.3"/>')
    g.append(f'<path d="{CRANIUM}" class="ink" stroke-width="1.3"/>')
    # nostril, lips line, cheek
    g.append('<path d="M33 11.5 C35 10.5 36.5 11.5 36 13" class="ink2"/>')
    if mouth == "open":
        g.append('<path d="M33 20 C30 21 29 22 30.5 23.5 C31.5 24 33 23.5 33.5 22.5" fill="#7a3a2c" stroke="#2a2018" stroke-width=".6"/>')
    else:
        g.append('<path d="M32 20 C30 20.3 28.5 20.6 27.5 21" class="ink2"/>')
    g.append('<path d="M27 8 C25 13 26 17 28 18" class="ink2" stroke-opacity=".6"/>')
    # brow & eye
    g.append('<path d="M17 -10 C21 -12.5 25.5 -12 29.5 -9.5" fill="none" stroke="#3b2a1d" stroke-width="1.6" stroke-linecap="round"/>')
    if eye == "open" or eye == "wide":
        g.append('<path d="M20 -5 C22.5 -7.5 26 -6.8 27.5 -4.6 C25.5 -2.6 22.5 -2.4 20 -5Z" fill="#fff" stroke="#2a2018" stroke-width=".7"/>')
        g.append('<circle cx="25.3" cy="-4.8" r="1.7" fill="#3a2a1c"/><circle cx="25.8" cy="-5.3" r=".45" fill="#fff"/>')
        g.append('<path d="M19.5 -5.6 C22.5 -8.6 26 -8 28 -5.2" class="ink2" stroke-width=".9"/>')
        if eye == "wide":
            g.append('<path d="M20 -8.5 C23 -10 26 -9.8 28 -8" class="ink2"/>')
    else:
        g.append('<path d="M20 -4.5 C22.5 -2.4 25.5 -2.4 27.6 -4.4" class="ink2" stroke-width="1"/>'
                 '<path d="M22 -3 l-.6 1.4 M24 -2.6 l-.2 1.5 M26 -3 l.3 1.4" class="ink2" stroke-width=".5"/>')
    if age == "old":
        g.append('<path d="M28 -5 l3 -1.5 M28.2 -3.5 l3 .3 M28 -2 l2.6 1.6" class="ink2" stroke-width=".45"/>')
    if sweat:
        for (sx, sy) in [(24, -24), (14, -30), (31, -16), (6, 30), (-4, 40)]:
            g.append(f'<path d="M{sx} {sy} c-1.6 2.4 -1.8 4 0 4.6 c1.8 -.6 1.6 -2.2 0 -4.6Z" fill="#cfe0f0" stroke="#3f6fa6" stroke-width=".6"/>')
    g.append('</g>')
    return "".join(g)


def hand(x, y, s=1.0, rot=0, fill="url(#ink-vol-flesh)"):
    """relaxed hand, lateral (thumb-side) view, wrist at origin, fingers toward +x, palm down (+y)"""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            '<path d="M0 -6 C8 -8 16 -9 22 -8 C27 -7.5 31 -6 34 -3 C36.5 -.5 37 3 35 5 C33.5 6.5 31.5 5.5 31 3.5 '
            'C29.5 1 27 0 24 .5 C22 1 20 2 22 4 C25 5.5 27.5 6.5 27 8.5 C26.4 10.2 23.5 10 21 8.8 C17 7 13 7 9 7.5 C5 8 2 7.5 0 7Z" '
            f'fill="{fill}" stroke="#2a2018" stroke-width=".9" stroke-linejoin="round"/>'
            '<path d="M22 -8 C26 -9.6 30 -9 32.6 -7 C34.4 -5.6 35 -4 34.6 -3.2 M24.5 -.6 C26 -2.8 29 -3.4 31.4 -1.8 '
            'M33.6 -2 C35.4 -.4 35.8 2 35.2 3.6 M13 1.5 C16 2.5 19 3 21.6 3.8 M19 -7.4 C19.6 -6.4 20.6 -6 21.6 -6.2" class="ink2"/>'
            '<path d="M2 -5 C8 -6.4 14 -7 20 -6.6" fill="none" stroke="#2a2018" stroke-width=".4" stroke-opacity=".5"/>'
            '</g>')


def strip(x, y, w, segs, t0, t1, ticks, h=12, title=None):
    """timeline strip: segs list of (start_h, end_h, state) with state 'sleep'|'wake'|'bed'"""
    def X(t):
        return x + (t - t0) / (t1 - t0) * w
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#efe6d2" stroke="#2a2018" stroke-width=".7"/>']
    for a, b, st in segs:
        if st == "sleep":
            o.append(f'<rect x="{X(a):.1f}" y="{y}" width="{X(b)-X(a):.1f}" height="{h}" fill="#3f6fa6" fill-opacity=".85"/>')
        elif st == "wake":
            o.append(f'<rect x="{X(a):.1f}" y="{y}" width="{X(b)-X(a):.1f}" height="{h}" fill="#e9b04a"/>'
                     f'<rect x="{X(a):.1f}" y="{y}" width="{X(b)-X(a):.1f}" height="{h}" fill="url(#ink-hatch)" opacity=".7"/>')
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#2a2018" stroke-width=".8"/>')
    for t, lbl in ticks:
        o.append(f'<line x1="{X(t):.1f}" y1="{y+h}" x2="{X(t):.1f}" y2="{y+h+3}" stroke="#2a2018" stroke-width=".7"/>'
                 f'<text x="{X(t):.1f}" y="{y+h+13}" class="ls" text-anchor="middle">{lbl}</text>')
    return "".join(o)


def capsule(x1, y1, x2, y2, r1, r2, fill="#cfdcef", sw=1.0, extra=""):
    """tapered limb segment with round ends"""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    a1 = (x1 + nx * r1, y1 + ny * r1); b1 = (x1 - nx * r1, y1 - ny * r1)
    a2 = (x2 + nx * r2, y2 + ny * r2); b2 = (x2 - nx * r2, y2 - ny * r2)
    d = (f"M{a1[0]:.1f} {a1[1]:.1f} L{a2[0]:.1f} {a2[1]:.1f} A{r2} {r2} 0 0 0 {b2[0]:.1f} {b2[1]:.1f} "
         f"L{b1[0]:.1f} {b1[1]:.1f} A{r1} {r1} 0 0 0 {a1[0]:.1f} {a1[1]:.1f}Z")
    return f'<path d="{d}" fill="{fill}" stroke="#2a2018" stroke-width="{sw}" stroke-linejoin="round"{extra}/>'


def fist(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            '<path d="M-2 -7 C5 -9.5 13 -10 18 -8 C22.5 -6 23 4 19 7.5 C14 10 5 9.5 -2 7.5Z" fill="url(#ink-vol-flesh)" stroke="#2a2018" stroke-width="1"/>'
            '<path d="M14 -9 C17 -6 17.5 0 16.5 8.5 M18.5 -7.5 C20 -3 20 2 19 7 M9 -9 C11 -4 11 2 10 9" class="ink2"/>'
            '<path d="M2 -6 C7 -4 12 -1 14 2 C15 4 13 5 11 4 C8 2 4 0 1 -1Z" fill="#efc9b0" stroke="#2a2018" stroke-width=".8"/>'
            '</g>')


# ================= public-edition helpers =================
def brain_glyph(x, y, s=1.0, fill="#f0c4b8", op=1.0, stroke="#2a2018"):
    """small lateral brain (faces +x), centre at origin, ~66x50 at s=1"""
    return (f'<g transform="translate({x},{y}) scale({s})" opacity="{op}">'
            f'<path d="M-32 6 C-37 -10 -26 -25 -8 -28 C8 -31 26 -25 32 -12 C37 -2 34 10 24 13 C20 19 10 21 2 18 '
            f'C-4 22 -16 22 -22 17 C-30 16 -33 11 -32 6Z" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
            f'<path d="M-20 16 C-16 22 -8 24 -4 20 C-8 18 -14 16 -20 16Z" fill="{fill}" stroke="{stroke}" stroke-width=".8"/>'
            f'<path d="M-2 18 C2 22 4 26 2 30" fill="none" stroke="{stroke}" stroke-width="1.4"/>'
            f'<path d="M-24 -6 C-18 -2 -8 0 2 -2 C10 -4 18 0 24 4 M-6 -26 C-8 -18 -2 -14 -4 -6 M10 -27 C6 -20 12 -16 8 -8 '
            f'M-20 -18 C-14 -16 -14 -10 -18 -6 M22 -18 C18 -14 22 -8 18 -4 M-26 4 C-20 8 -12 6 -8 10 C-4 14 4 10 8 14 '
            f'M14 6 C18 8 22 6 26 10" fill="none" stroke="{stroke}" stroke-width=".7"/></g>')


def bed_lying(W, y0, H, eye="wide", shirt="#9fb7a0", hx=58, pid="x", hair="short", blanket="#e8d6ae", head_s=.46, dark_circles=False, mouth="closed"):
    """headboard at left, person lying with head on pillow (face up). returns svg (local coords)"""
    by = y0 + H  # floor line
    o = []
    o.append(f'<path d="M8 {by} V{by-124} C8 {by-134} 30 {by-138} 34 {by-128} V{by}" fill="#a57c55" stroke="#2a2018" stroke-width="1.3"/>'
             f'<path d="M8 {by} V{by-124} C8 {by-134} 30 {by-138} 34 {by-128} V{by}" fill="url(#ink-hatch-l)"/>'
             f'<path d="M14 {by-116} V{by-6} M28 {by-116} V{by-6}" class="ink2"/>')
    o.append(f'<path d="M30 {by-40} H{W} V{by-16} H30Z" fill="#f4eee0" stroke="#2a2018" stroke-width="1"/>'
             f'<path d="M30 {by-16} H{W} V{by-8} H30Z" fill="#a57c55" stroke="#2a2018" stroke-width="1"/>'
             f'<path d="M36 {by-8} V{by}" stroke="#2a2018" stroke-width="3"/>')
    o.append(f'<path d="M30 {by-42} C24 {by-52} 30 {by-60} 44 {by-60} C60 {by-62} 82 {by-62} 92 {by-58} C98 {by-54} 96 {by-42} 92 {by-38} '
             f'C74 {by-36} 46 {by-36} 30 {by-42}Z" fill="#fbf6ea" stroke="#2a2018" stroke-width="1"/>'
             f'<path d="M36 {by-44} C48 {by-40} 70 {by-40} 88 {by-42}" class="ink2"/>')
    hy = by - 63
    o.append(head(hx, hy, head_s, -90, eye=eye, hair=hair, mouth=mouth))
    if dark_circles:
        # under-eye shadow (rotated head: eye at local (24,-4) -> (hx-4*... ) approximate)
        ex, ey = hx + (-4) * head_s * -1 * 0 + (-4.8) * head_s, hy - 25.3 * head_s
        o.append(f'<path d="M{hx-0.5*head_s*2:.1f} {hy-22*head_s:.1f} c-3 2 -3 7 0 9" fill="none" stroke="#8a6a7a" stroke-width="1.6" opacity=".55"/>')
    o.append(f'<path d="M{hx+17} {hy-8} C{hx+22} {hy-11} {hx+28} {hy-13} {hx+34} {hy-13} C{hx+40} {hy-14} {hx+44} {hy-14} {hx+46} {hy-13} '
             f'L{hx+46} {by-39} L{hx+14} {by-39} C{hx+12} {by-48} {hx+13} {hy+1} {hx+17} {hy-8}Z" fill="{shirt}" stroke="#2a2018" stroke-width="1"/>')
    bx = hx + 42
    top = (f"M{bx} {hy-11} C{bx+10} {hy-19} {bx+24} {hy-21} {bx+38} {hy-18} C{bx+50} {hy-15} {bx+56} {hy-10} {bx+66} {hy-10} "
           f"C{bx+78} {hy-10} {bx+86} {hy-15} {bx+98} {hy-14} C{bx+112} {hy-13} {bx+124} {hy-8} {bx+140} {hy-7} C{bx+170} {hy-9} {bx+200} {hy-7} {W} {hy-5}")
    o.append(f'<path d="{top} L{W} {by-12} C{W-40} {by-10} {W-70} {by-16} {W-100} {by-11} C{bx+100} {by-8} {bx+70} {by-15} {bx+40} {by-11} C{bx+20} {by-8} {bx+10} {by-14} {bx} {by-14}Z" '
             f'fill="{blanket}" stroke="#2a2018" stroke-width="1.3"/>'
             f'<path d="M{bx+38} {hy-18} C{bx+40} {hy+7} {bx+34} {by-38} {bx+38} {by-13} C{bx+31} {by-34} {bx+30} {hy+9} {bx+32} {hy-17}Z" fill="url(#ink-hatch)"/>'
             f'<path d="M{bx+98} {hy-14} C{bx+94} {hy+11} {bx+100} {by-36} {bx+94} {by-13} C{bx+102} {by-34} {bx+105} {hy+11} {bx+105} {hy-13}Z" fill="url(#ink-hatch)"/>'
             f'<path d="M{bx+66} {hy-9} C{bx+64} {hy+15} {bx+68} {by-30} {bx+64} {by-11} M{bx+140} {hy-7} C{bx+142} {hy+21} {bx+138} {by-30} {bx+142} {by-10}" class="ink2"/>')
    return "".join(o)


def window(x, y, w, h, moon=True, sky="#24334f"):
    o = [f'<rect x="{x-5}" y="{y-5}" width="{w+10}" height="{h+11}" fill="#efe6d2" stroke="#2a2018" stroke-width=".9"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{sky}" stroke="#2a2018" stroke-width="1"/>']
    import random
    r = random.Random(x * 7 + y)
    for _ in range(int(w * h / 500)):
        o.append(f'<circle cx="{x+4+r.random()*(w-8):.1f}" cy="{y+4+r.random()*(h-8):.1f}" r=".9" fill="#f6e7b0"/>')
    if moon:
        mx, my = x + w * .7, y + h * .3
        o.append(f'<path d="M{mx} {my-7} a7 7 0 1 0 5.5 11.5 a5.6 5.6 0 1 1 -5.5 -11.5Z" fill="#f6e7b0" stroke="#2a2018" stroke-width=".6"/>')
    o.append(f'<path d="M{x+w/2} {y} V{y+h} M{x} {y+h/2} H{x+w}" stroke="#efe6d2" stroke-width="3"/>'
             f'<path d="M{x+w/2} {y} V{y+h} M{x} {y+h/2} H{x+w}" class="ink2"/>')
    return "".join(o)


def bubble(cx, cy, rx, ry, tail=None, fill="#fbf6ea", seed=0):
    """cloud-like thought bubble with optional tail dots toward (tx,ty)"""
    n = 9
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + seed
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f} "
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        ox, oy = mx - cx, my - cy
        L = math.hypot(ox, oy) or 1
        k = 0.28 * (rx + ry) / 2
        c1 = (mx + ox / L * k, my + oy / L * k)
        d += f"Q{c1[0]:.1f} {c1[1]:.1f} {q[0]:.1f} {q[1]:.1f} "
    o = [f'<path d="{d}Z" fill="{fill}" stroke="#2a2018" stroke-width="1"/>']
    if tail:
        tx, ty = tail
        dx, dy = tx - cx, ty - cy
        L = math.hypot(dx / rx, dy / ry) or 1
        ex, ey = cx + dx / L * 1.25, cy + dy / L * 1.25
        for t, r in [(.15, 4.5), (.5, 3.2), (.85, 2)]:
            o.append(f'<circle cx="{ex+(tx-ex)*t:.1f}" cy="{ey+(ty-ey)*t:.1f}" r="{r}" fill="{fill}" stroke="#2a2018" stroke-width=".9"/>')
    return "".join(o)


def digital(x, y, txt, w=46, h=20, col="#e8564a"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#2b2824" stroke="#2a2018" stroke-width="1"/>'
            f'<text x="{x+w/2}" y="{y+h-5.5}" text-anchor="middle" style="font-family:monospace;font-size:13px;font-weight:700;fill:{col}">{txt}</text>')
