from common import smooth, f

# profile head facing +x, unit height ~60 (top 0 .. chin 52), origin = top of skull
FRONT = [(0, 0), (12, 4), (18, 12), (20, 20), (19.4, 24.5), (20.2, 27), (23.5, 32), (26.5, 36), (24, 37.6), (21.2, 38.2),
         (21.8, 40.5), (20.6, 42), (21.4, 43.8), (19.6, 46.4), (20.6, 50), (18, 53.5), (12, 55), (8.5, 58), (8.5, 72)]
BACK = [(-9.5, 72), (-10, 60), (-13, 51), (-19, 42), (-22, 30), (-20, 14), (-12, 3)]

def head(x, y, s=1.0, rot=0, eyes='open', hair='#4a3626', skin='url(#ink-vol-flesh)', neck=True, pid='h'):
    P = FRONT + BACK
    d = smooth(P, close=True, t=0.5)
    g = []
    g.append('<path d="%s" fill="%s" stroke="#2a2018" stroke-width="1.2"/>' % (d, skin))
    # ear
    g.append('<path d="%s" fill="#f0cdb6" stroke="#2a2018" stroke-width=".8"/>' % smooth([(-3, 27), (1, 25.5), (3, 30), (2.6, 37), (-1, 41), (-4, 38)], close=True))
    g.append('<path d="M-.5 30 q2 3 0 7" fill="none" stroke="#2a2018" stroke-width=".5"/>')
    # hair mass
    H = [(-11, 46), (-20, 38), (-23.5, 26), (-21, 10), (-12, 0), (2, -3.5), (13, 1), (19.5, 10), (20, 16), (14, 12), (6, 11), (2, 16), (0, 24), (-6, 26), (-8, 36)]
    g.append('<path d="%s" fill="%s" stroke="#2a2018" stroke-width=".8"/>' % (smooth(H, close=True), hair))
    for k in range(5):
        g.append('<path d="%s" fill="none" stroke="#1e140c" stroke-width=".4" stroke-opacity=".7"/>' % smooth([(-18 + k * 4, 6 + k), (-16 + k * 4, 18 + k * 2), (-12 + k * 3, 32 + k)]))
    # eye & brow
    g.append('<path d="M12.5 21.5 q3 -1.6 6.3 .4" fill="none" stroke="#2a2018" stroke-width="1"/>')
    if eyes == 'open':
        g.append('<path d="M13.5 26 q2.6 -1.8 5 .2 q-2.4 1.4 -5 -.2z" fill="#fbf6ea" stroke="#2a2018" stroke-width=".6"/><circle cx="16.8" cy="26.1" r="1.1" fill="#2a2018"/>')
    else:
        g.append('<path d="M13.4 26.4 q2.6 1.6 5 0" fill="none" stroke="#2a2018" stroke-width=".8"/>')
    # nostril, mouth line, cheek, jaw
    g.append('<path d="M21.5 35.6 q1.5 1 2.6 .6" fill="none" stroke="#2a2018" stroke-width=".55"/>')
    g.append('<path d="M17.5 41.6 l3.2 .3" fill="none" stroke="#2a2018" stroke-width=".7"/>')
    g.append('<path d="M4 46 q6 5 13 6.5" fill="none" stroke="#2a2018" stroke-width=".45" stroke-opacity=".6"/>')
    g.append('<path d="M10 33 q3 2 6 1.4" fill="none" stroke="#2a2018" stroke-width=".4" stroke-opacity=".5"/>')
    return '<g transform="translate(%s %s) rotate(%s) scale(%s)">%s</g>' % (f(x), f(y), f(rot), f(s), ''.join(g))
