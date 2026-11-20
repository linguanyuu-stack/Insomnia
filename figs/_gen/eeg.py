"""Plate 1-F: synthetic but textbook-shaped PSG waveforms.
Waveforms are generated here (numpy, fixed seeds) and written as SVG polylines.
Convention: EEG negative is plotted UP. Scale: 1 s = 95 px, 50 uV = 20 px."""
import sys, os, math, random, io, contextlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from plib import *
with contextlib.redirect_stdout(io.StringIO()):
    import scn

P = 'pl-eeg'
FS = 150            # samples / s
DUR = 5.0           # seconds per row
PX_S = 95.0         # px per second
PX_UV = 20 / 50.0   # px per microvolt
X0 = 272            # trace start x
N = int(FS * DUR)
t = np.arange(N) / FS


def band(lo, hi, rms, seed, n=N):
    r = np.random.default_rng(seed)
    w = r.standard_normal(n * 4)
    F = np.fft.rfft(w)
    fr = np.fft.rfftfreq(len(w), 1 / FS)
    F[(fr < lo) | (fr > hi)] = 0
    x = np.fft.irfft(F, len(w))[n:2 * n]
    return x / (x.std() + 1e-9) * rms


def gauss(t0, sd):
    return np.exp(-((t - t0) / sd) ** 2)


def env(t0, t1):
    e = np.zeros(N)
    m = (t >= t0) & (t <= t1)
    e[m] = np.sin(np.pi * (t[m] - t0) / (t1 - t0)) ** 1.5
    return e


S = {}
# --- Wake: eyes open (beta) -> eyes closed (alpha, posterior)
eo = t < 1.4
alpha = band(9, 11.5, 16, 1) * (0.75 + 0.35 * np.sin(2 * np.pi * 0.45 * t + 1))
S['wake'] = np.where(eo, band(15, 30, 5, 2) + band(2, 8, 4, 3), alpha + band(15, 30, 3, 4) + band(2, 7, 3, 5))
S['wake'] += np.where(eo, 0, 0) - 0
S['emg_w'] = band(25, 70, 9, 6)
# --- N1: theta, vertex sharp wave, slow rolling eye movements
S['n1'] = band(4, 7.5, 12, 7) + band(1, 3, 6, 8) + band(8, 13, 2.5, 9)
S['n1'] += 95 * gauss(3.05, 0.035) - 30 * gauss(3.16, 0.06)
S['eog1'] = 70 * np.sin(2 * np.pi * 0.32 * t + 0.6) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.11 * t)) + band(1, 6, 2, 10)
# --- N2: spindle + K-complex
S['n2'] = band(4, 7.5, 12, 11) + band(1, 3, 8, 12)
S['n2'] += 26 * np.sin(2 * np.pi * 13.2 * t) * env(0.75, 1.75)
S['n2'] += 125 * gauss(3.05, 0.075) - 95 * gauss(3.38, 0.15)
S['n2'] += 14 * np.sin(2 * np.pi * 12.8 * t) * env(3.6, 4.2)
# --- N3: delta
d = (62 * np.sin(2 * np.pi * 1.05 * t + .4) * (0.85 + 0.2 * np.sin(2 * np.pi * 0.23 * t)) + 22 * np.sin(2 * np.pi * 1.7 * t + 1.3)
     + 14 * np.sin(2 * np.pi * 0.6 * t + 2.1) + band(0.5, 2.0, 12, 13))
S['n3'] = d + band(4, 8, 6, 14) + band(10, 14, 2, 15)
# --- REM: low-voltage mixed + sawtooth burst; EOG REMs; EMG atonia
saw = np.zeros(N)
m = (t > 1.9) & (t < 3.3)
ph = (t * 3.2) % 1.0
saw_shape = np.where(ph < 0.72, ph / 0.72, (1 - ph) / 0.28) - 0.5
saw[m] = saw_shape[m] * 42 * np.sin(np.pi * (t[m] - 1.9) / 1.4) ** .6
S['rem'] = band(3, 10, 8, 16) + band(12, 25, 3, 17) + saw + 4 * np.sin(2 * np.pi * 6.4 * t) * m
pos = np.zeros(N)
rr = random.Random(5)
for ts, a in [(0.45, 120), (0.8, -110), (1.55, 140), (1.85, -90), (2.05, 80), (3.05, -150), (3.4, 120), (4.25, -130), (4.5, 90)]:
    pos += a / (1 + np.exp(-(t - ts) / 0.012))
# AC coupling (high-pass, tau 0.4 s)
eog = np.zeros(N); a_ = 0.4 / (0.4 + 1 / FS)
for i in range(1, N):
    eog[i] = a_ * (eog[i - 1] + pos[i] - pos[i - 1])
S['eog_r'] = eog + band(1, 8, 3, 18)
S['emg_r'] = band(25, 70, 1.2, 19) + band(25, 70, 9, 20) * env(2.55, 2.68)


def trace(sig, y, scale=PX_UV, clip=None):
    xs = X0 + t * PX_S
    ys = y - sig * scale           # positive value (=negative potential) plotted up
    return ' '.join('%.1f,%.1f' % (a, b) for a, b in zip(xs, ys))


O = []
add = O.append
AN = '#a8412c'
ROWS = [  # key, y, zh, en, sub, scale
    ('wake', 66, '清醒', 'Wake', 'α 8–12 Hz（閉眼）'),
    ('n1', 162, 'N1 入睡期', 'Stage N1', 'θ 4–7 Hz、頂部銳波'),
    ('n2', 300, 'N2 淺睡期', 'Stage N2', '紡錘波＋K 複合波'),
    ('n3', 412, 'N3 深睡期', 'Stage N3 (SWS)', 'δ 0.5–2 Hz，≥75 µV'),
    ('rem', 520, 'REM 快速動眼期', 'Stage R', '低電壓、鋸齒波'),
]
# row backgrounds / separators
for i, (k, y, zh, en, sub) in enumerate(ROWS):
    if i:
        add('<path d="M134 %s H748" stroke="#d8c9a8" stroke-width=".8" stroke-dasharray="1 3"/>' % {'n1': 112, 'n2': 230, 'n3': 350, 'rem': 470}[k])
    add('<text x="136" y="%s" class="lb">%s</text><text x="136" y="%s" class="le">%s</text><text x="136" y="%s" class="ls">%s</text>' % (y - 8, zh, y + 6, en, y + 20, sub))
    add('<polyline points="%s" fill="none" stroke="%s" stroke-width=".9" stroke-linejoin="round"/>' % (trace(S[k], y), INK))
# extra channels
add('<text x="266" y="%s" text-anchor="end" class="ls" style="font-size:9.5px">EMG</text>' % 101)
add('<polyline points="%s" fill="none" stroke="#5d4b38" stroke-width=".6"/>' % trace(S['emg_w'], 98, .5))
add('<text x="266" y="%s" text-anchor="end" class="ls" style="font-size:9.5px">EOG</text>' % 199)
add('<polyline points="%s" fill="none" stroke="%s" stroke-width=".9"/>' % (trace(S['eog1'], 196, .2), WEST))
add('<text x="266" y="%s" text-anchor="end" class="ls" style="font-size:9.5px">EOG</text>' % 565)
add('<polyline points="%s" fill="none" stroke="%s" stroke-width=".9"/>' % (trace(S['eog_r'], 562, .14), WEST))
add('<text x="266" y="%s" text-anchor="end" class="ls" style="font-size:9.5px">EMG</text>' % 625)
add('<polyline points="%s" fill="none" stroke="#5d4b38" stroke-width=".6"/>' % trace(S['emg_r'], 622, .5))
for y in (66, 162, 300, 412, 520):
    add('<text x="266" y="%s" text-anchor="end" class="ls" style="font-size:9.5px">EEG</text>' % (y + 3))


def X(sec):
    return X0 + sec * PX_S


def brace(x0, x1, y, txt, en=None, up=True, col=AN, anchor='middle'):
    s = -1 if up else 1
    o = '<path d="M%s %s v%s H%s v%s" fill="none" stroke="%s" stroke-width=".9"/>' % (f(x0), f(y - s * 4), f(s * 4), f(x1), f(-s * 4), col)
    tx = (x0 + x1) / 2 if anchor == 'middle' else x0
    ty = y + s * 6 + (0 if up else 8)
    o += '<text x="%s" y="%s" text-anchor="%s" class="ls halo" style="fill:%s;font-weight:600">%s%s</text>' % (
        f(tx), f(ty), anchor, col, txt, (' <tspan class="le" style="font-weight:400">%s</tspan>' % en) if en else '')
    return o


# annotations
add(brace(X(0.05), X(1.35), 40, 'β 睜眼', None))
add('<path d="M%s 30 V108" stroke="%s" stroke-width=".8" stroke-dasharray="3 2"/><text x="%s" y="28" class="ls halo" style="fill:%s">閉眼 ↓</text>' % (f(X(1.4)), AN, f(X(1.4) + 3), AN))
add(brace(X(1.6), X(4.9), 38, 'α 波', 'alpha rhythm ≈10 Hz'))
add(brace(X(0.2), X(2.6), 134, 'θ 波', 'theta'))
add('<text x="%s" y="116" class="ls halo" style="fill:%s;font-weight:600" text-anchor="middle">頂部銳波 <tspan class="le" style="font-weight:400">vertex sharp wave</tspan></text>' % (f(X(3.05)), AN))
add('<text x="%s" y="224" class="ls halo" style="fill:%s;font-weight:600" text-anchor="end">慢速滾動眼動 <tspan class="le" style="font-weight:400">slow rolling eye movements</tspan></text>' % (f(X(5)), WEST))
add(brace(X(0.75), X(1.75), 262, '睡眠紡錘波', 'spindle 12–14 Hz'))
add(brace(X(2.85), X(3.62), 246, 'K 複合波', 'K-complex ≥0.5 s'))
add(brace(X(0.1), X(4.9), 368, 'δ 慢波', 'delta, high amplitude'))
add(brace(X(1.9), X(3.3), 494, '鋸齒波', 'sawtooth waves'))
add(brace(X(0.35), X(4.6), 592, '快速眼動', 'rapid eye movements', up=False, col=WEST))
add(brace(X(0.2), X(2.4), 636, '下巴肌電幾乎平直＝肌張力消失', 'atonia', up=False, col='#5d4b38'))
add('<text x="%s" y="%s" class="ls halo" style="fill:#5d4b38">肌肉小抽動 twitch</text>' % (f(X(2.75)), 640))

# 75 uV reference in N3
yref = 380 - 75 * PX_UV / 2
add('<path d="M%s %s H%s M%s %s H%s" stroke="%s" stroke-width=".6" stroke-dasharray="4 3" opacity=".8"/>' % (
    f(X(0)), f(412 - 37.5 * PX_UV), f(X(5)), f(X(0)), f(412 + 37.5 * PX_UV), f(X(5)), WEST))
add('<text x="%s" y="%s" class="ls halo" style="fill:%s" text-anchor="end">虛線間距＝75 µV（N3 判讀門檻）</text>' % (f(X(5)), 462, WEST))

# scale bars
sy = 676
add('<path d="M%s %s H%s M%s %s V%s" stroke="%s" stroke-width="1.8"/>' % (f(X(3.6)), sy, f(X(4.6)), f(X(4.6)), sy, f(sy - 50 * PX_UV), INK))
add('<text x="%s" y="%s" text-anchor="middle" class="ls">1 秒</text><text x="%s" y="%s" class="ls">50 µV</text>' % (f(X(4.1)), sy + 14, f(X(4.6) + 5), f(sy - 6)))
add('<text x="%s" y="%s" class="ls" style="font-style:italic">EEG 依慣例負電位朝上；EOG、EMG 為不同增益。</text>' % (f(X(0)), sy + 6))

# ---------- mini heads (left) ----------
H = []
c = (66, 124); R = 44
H.append('<text x="12" y="30" class="lb">電極位置</text><text x="12" y="44" class="le">10–20 system</text>')
H.append('<path d="M%s %s l-8 -12 l-8 12z" fill="%s" class="ink"/>' % (c[0] + 8, c[1] - R + 2, FLESH))
for sg in (-1, 1):
    H.append('<path d="%s" fill="%s" class="ink"/>' % (cr([(c[0] + sg * (R - 2), c[1] - 10), (c[0] + sg * (R + 7), c[1] - 6), (c[0] + sg * (R + 7), c[1] + 10), (c[0] + sg * (R - 2), c[1] + 12)]), FLESH))
H.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/><circle cx="%s" cy="%s" r="%s" fill="url(#ink-stipple-l)"/><circle cx="%s" cy="%s" r="%s" class="ink3"/>' % (c[0], c[1], R, FLESH, c[0], c[1], R, c[0], c[1], R))
H.append('<path d="M%s %s V%s M%s %s H%s" stroke="#bfae8a" stroke-width=".6" stroke-dasharray="2 2"/>' % (c[0], c[1] - R, c[1] + R, c[0] - R, c[1], c[0] + R))
H.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#bfae8a" stroke-width=".6" stroke-dasharray="2 2"/>' % (c[0], c[1], R * .8))
E = {'Fz': (0, -.4), 'Cz': (0, 0), 'Pz': (0, .4), 'F3': (-.32, -.42), 'F4': (.32, -.42), 'C4': (.4, 0), 'P3': (-.32, .42), 'P4': (.32, .42),
     'Fp1': (-.25, -.76), 'Fp2': (.25, -.76), 'O2': (.25, .76), 'T3': (-.8, 0), 'T4': (.8, 0)}
for k, (u, v) in E.items():
    H.append('<circle cx="%s" cy="%s" r="2.6" fill="#fbf6ea" stroke="#8a7a60" stroke-width=".7"/>' % (f(c[0] + u * R), f(c[1] + v * R)))
for k, (u, v), col in [('C3', (-.4, 0), AN), ('O1', (-.25, .76), AN)]:
    x, y = c[0] + u * R, c[1] + v * R
    H.append('<circle cx="%s" cy="%s" r="4.4" fill="%s" stroke="%s" stroke-width=".8"/>' % (f(x), f(y), col, INK))
    H.append('<text x="%s" y="%s" class="lb halo" style="fill:%s;font-size:11.5px" text-anchor="middle">%s</text>' % (f(x), f(y - 7), col, k))
H.append('<circle cx="%s" cy="%s" r="3.6" fill="%s" stroke="%s" stroke-width=".8"/><text x="%s" y="%s" class="ls halo" text-anchor="end">M2 參考</text>' % (
    c[0] + R + 4, c[1] + 16, WEST, INK, c[0] + R + 6, c[1] + 32))
H.append('<text x="%s" y="%s" text-anchor="middle" class="ls">鼻 nose ▲</text>' % (c[0], c[1] - R - 16))
H.append('<text x="12" y="%s" class="ls">中央 C3、枕部 O1</text><text x="12" y="%s" class="ls">（α 波在 O1 最大）</text>' % (c[1] + R + 22, c[1] + R + 36))
# profile head with EOG / EMG
hp = [(x, y) for x, y in scn.head if y < 400]
k = .21; ox, oy = 2, 262
pp = [(ox + (x - 80) * k, oy + (y - 40) * k) for x, y in hp]
cut = [(ox + (196 - 80) * k, oy + (400 - 40) * k), (ox + (380 - 80) * k, oy + (400 - 40) * k)]
pd = cr(pp[:pp.index(min(pp, key=lambda p: -p[1]))] if False else pp, True, k=.8)
H.append('<path d="%s" fill="%s"/><path d="%s" fill="url(#ink-stipple-l)"/><path d="%s" class="ink" stroke-width="1.3"/>' % (pd, FLESH, pd, pd))
H.append('<path d="%s" fill="none" stroke="#6b5440" stroke-width="1.3"/>' % cr([(ox + (122 - 80) * k, oy + (136 - 40) * k), (ox + (200 - 80) * k, oy + (52 - 40) * k), (ox + (330 - 80) * k, oy + (58 - 40) * k), (ox + (420 - 80) * k, oy + (170 - 40) * k)]))
H.append('<path d="M%s %s q3 -2 6 0" class="ink2"/>' % (ox + (128 - 80) * k, oy + (210 - 40) * k))
H.append('<ellipse cx="%s" cy="%s" rx="4" ry="5" fill="%s" class="ink2"/>' % (ox + (300 - 80) * k, oy + (230 - 40) * k, FLESH_D))
for (x, y, col) in [((150 - 80) * k + ox, (212 - 40) * k + oy, WEST), ((170 - 80) * k + ox, (385 - 40) * k + oy, '#5d4b38'),
                    ((300 - 80) * k + ox, (60 - 40) * k + oy, AN), ((418 - 80) * k + ox, (150 - 40) * k + oy, AN)]:
    H.append('<circle cx="%s" cy="%s" r="3.4" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(x), f(y), col, INK))
H.append(label('R', 70, 306, 'EOG', None, ((150 - 80) * k + ox + 3, (212 - 40) * k + oy), stub=4, color=WEST))
H.append(label('R', 70, 352, 'EMG 下巴', None, ((170 - 80) * k + ox + 3, (385 - 40) * k + oy), stub=4, color='#5d4b38'))
H.append('<text x="12" y="%s" class="ls">眼電：眼角外側</text><text x="12" y="%s" class="ls">肌電：下巴</text>' % (oy + 110, oy + 124))

body = inline_classes('\n'.join(H)) + '\n' + '\n'.join(O)
cap = ('<b>圖 1-F　每個睡眠階段的腦波長相。</b>每列 5 秒。清醒閉眼時枕部出現 α 波；N1 變成較慢的 θ 波，常見頂部銳波與慢速滾動的眼動；N2 的招牌是紡錘波與 K 複合波；'
       'N3 是又高又慢的 δ 波（峰對峰 ≥75 µV、0.5–2 Hz）；REM 的腦波反而又低又快、像清醒，夾雜鋸齒波，同時眼睛快速轉動、下巴肌電幾乎平直（肌張力消失）。'
       '波形由程式依教科書特徵合成（figs/_gen/eeg.py），並非真實病人記錄；判讀依 AASM 分期規則的描述。')
write(P, 'Plate 1·F', '每個睡眠階段的腦波長相', 'What each sleep stage looks like on the EEG', 700, body,
      '清醒、N1、N2、N3 與 REM 各階段的腦波、眼電與肌電示意波形，含時間與電壓比例尺', cap)
