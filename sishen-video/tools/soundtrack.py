"""Synthesize the soundtrack (music + SFX) for 茯苓的告白, aligned to the scene timeline.

Everything is generated procedurally with numpy so the project has no
third-party audio licensing concerns.  Output: public/soundtrack.wav
"""
import wave
import numpy as np

SR = 44100
FPS = 30
DUR = 2700 / FPS
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(3)

# scene starts (frames) — keep in sync with src/SishenLove.tsx
S1, S2, S3, S4, S5, S6, S7, S8, S9 = 0, 150, 540, 990, 1290, 1470, 1890, 2190, 2550


def fr(f):
    return f / FPS


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    pan = float(np.clip(pan, -1, 1))
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    L[i : i + len(sig)] += sig * gain * l
    R[i : i + len(sig)] += sig * gain * r


def env(n, a=0.005, d=0.3):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / d)
    return e


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def pluck(freq, dur=1.6, bright=0.5):
    """Plucked string (guzheng-ish): harmonics decaying faster as they go up, slight bend-in."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    bend = 1 + 0.012 * np.exp(-t / 0.04)
    ph = 2 * np.pi * freq * np.cumsum(bend) / SR
    out = np.zeros(n)
    for k in range(1, 8):
        out += (bright ** (k - 1)) / k * np.sin(k * ph) * np.exp(-t * (2.2 + k * 1.6) / max(dur, 0.3))
    return out * np.minimum(1, t / 0.002)


def tone(freq, dur, kind="sine", a=0.01, d=None, vib=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = 2 * np.pi * freq * t + vib * np.sin(2 * np.pi * 5 * t)
    if kind == "sine":
        s = np.sin(ph)
    elif kind == "tri":
        s = 2 / np.pi * np.arcsin(np.sin(ph))
    else:
        s = np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    e = np.minimum(1, t / a) * (np.exp(-t / d) if d else np.minimum(1, (dur - t) / 0.08))
    return s * e


def bell(freq, dur=1.8):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * freq * k * t) * np.exp(-t / (dur * dd)) for k, a, dd in [(1, 1, 0.5), (2.76, 0.4, 0.25), (5.4, 0.2, 0.12)])
    return s * np.minimum(1, t / 0.002)


def noise(dur, lo=None, hi=None):
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi:
        m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, n) / 3


def sweep(f0, f1, dur, kind="sine"):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) if kind == "sine" else 2 / np.pi * np.arcsin(np.sin(ph))
    return s * np.minimum(1, t / 0.005) * np.minimum(1, (dur - t) / 0.05)


# ---------------------------------------------------------------- music
PENTA = [0, 2, 4, 7, 9]  # C major pentatonic (gong mode)


def scale_note(root, deg):
    o, k = divmod(deg, 5)
    return root + PENTA[k] + 12 * o


sections = [
    # start, end (frames), bpm, chord roots (I-vi-IV-V-ish in pentatonic land), mood
    (S1, S3, 80, [60, 57, 53, 55], "gentle"),
    (S3, S5, 116, [60, 55, 57, 55], "bouncy"),
    (S5, S7, 100, [53, 55, 60, 57], "warm"),
    (S7, S8 + 92, 96, [57, 53, 55, 60], "rise"),
    (S8 + 92, S9, 120, [60, 55, 57, 53], "joy"),
    (S9, 2700, 90, [53, 55, 60, 60], "end"),
]

for si, (a, b, bpm, roots, mood) in enumerate(sections):
    beat = 60 / bpm
    t0, t1 = fr(a), fr(b)
    nbeats = int((t1 - t0) / beat)
    mel_deg = 5
    for bi in range(nbeats):
        t = t0 + bi * beat
        bar = bi // 4
        root = roots[bar % len(roots)]
        # pad chord each bar
        if bi % 4 == 0:
            for k, iv in enumerate([0, 7, 16]):
                pad = tone(midi(root - 12 + iv), beat * 4 + 0.3, "tri", a=0.25)
                add(pad, t, 0.035 if mood != "bouncy" else 0.025, pan=(k - 1) * 0.5)
        # bass
        if mood in ("bouncy", "joy"):
            for h in (0, 0.5):
                add(tone(midi(root - 24 + (7 if h else 0)), beat * 0.4, "rich", a=0.005, d=0.12), t + h * beat, 0.14)
        elif bi % 2 == 0:
            add(tone(midi(root - 24), beat * 1.8, "sine", a=0.02, d=0.6), t, 0.16)
        # percussion: wood block
        if mood in ("bouncy", "joy", "warm"):
            wb = tone(1400 if bi % 2 else 1000, 0.08, "sine", a=0.001, d=0.02)
            add(wb, t, 0.05 if mood == "warm" else 0.08, pan=0.3)
            if mood == "joy" and bi % 2 == 1:
                add(noise(0.08, lo=6000) * env(int(0.08 * SR), 0.001, 0.02), t + beat / 2, 0.25, pan=-0.3)
        # melody
        steps = 2 if mood in ("bouncy", "joy") else 1
        for s in range(steps):
            tt = t + s * beat / steps
            r = rng.random()
            if mood == "gentle" and r < 0.35:
                continue
            if mood == "end" and bi > nbeats - 3:
                continue
            mel_deg += int(rng.choice([-2, -1, -1, 0, 1, 1, 2]))
            mel_deg = int(np.clip(mel_deg, 2, 11))
            if bi % 4 == 0 and s == 0:
                mel_deg = int(round(mel_deg / 5) * 5) or 5  # land on root at bar start
            m = scale_note(60, mel_deg)
            add(pluck(midi(m), 1.4 if mood != "bouncy" else 0.7, 0.45), tt, 0.32, pan=rng.uniform(-0.3, 0.3))
    # ending flourish
    if mood == "end":
        for k, m in enumerate([60, 62, 64, 67, 69, 72]):
            add(pluck(midi(m + 12), 2.5), fr(b) - 2.6 + k * 0.09, 0.3, pan=(k - 2.5) / 3)

# sad slide when moisture cloud hits / collapse
for f0, mul in [(S2 + 252, 1), (S4 + 250, 1)]:
    for k in range(3):
        add(sweep(midi(64 - k * 2), midi(62 - k * 2), 0.35, "tri"), fr(f0) + k * 0.38, 0.12)

# ---------------------------------------------------------------- SFX
def boing(t, f0=220, f1=520, g=0.25):
    s = sweep(f0, f1, 0.18) * env(int(0.18 * SR), 0.003, 0.12)
    add(s, t, g)


def pop(t, g=0.3, f=900):
    add(sweep(f, f * 2.2, 0.06) * env(int(0.06 * SR), 0.001, 0.025), t, g)


def plop(t, g=0.35):
    add(sweep(260, 900, 0.09) * env(int(0.09 * SR), 0.001, 0.05), t, g)
    add(noise(0.05, lo=2500) * env(int(0.05 * SR), 0.001, 0.015), t, g * 0.4)


def thud(t, g=0.5):
    add(sweep(120, 45, 0.3) * env(int(0.3 * SR), 0.002, 0.12), t, g)
    add(noise(0.12, hi=600) * env(int(0.12 * SR), 0.001, 0.04), t, g * 0.6)


def whoosh(t, dur=0.5, g=0.25, lo=400, hi=4000):
    n = noise(dur, lo, hi)
    e = np.sin(np.linspace(0, np.pi, len(n))) ** 2
    add(n * e, t, g)


def chime(t, notes=(84, 88, 91), g=0.18, gap=0.07):
    for k, m in enumerate(notes):
        add(bell(midi(m), 1.5), t + k * gap, g, pan=(k - 1) * 0.4)


# title
chime(fr(S1 + 12), (79, 84, 88, 91))
# bedroom: snores
for k in range(3):
    add(sweep(90, 70, 0.9, "tri") * 0.5, fr(S2 + 10 + k * 30), 0.04)
for k in range(2):
    add(sweep(90, 70, 0.9, "tri") * 0.5, fr(S2 + 310 + k * 34), 0.04)
chime(fr(S2 + 95), (88, 91), 0.12)  # thought bubble
whoosh(fr(S2 + 222), 0.5, 0.15, 200, 1500)
thud(fr(S2 + 252), 0.4)
# rescue
thud(fr(S3 + 2), 0.5)  # door bang
for f in (S3 + 10, S3 + 18, S3 + 26, S3 + 34):
    boing(fr(f), 260, 480, 0.12)
for f in (S3 + 66, S3 + 172, S3 + 292):
    pop(fr(f), 0.3)
    whoosh(fr(f), 0.3, 0.15)
for k in range(9):
    add(sweep(300, 240, 0.25, "tri") * env(int(0.25 * SR), 0.01, 0.15), fr(S3 + 80 + k * 10), 0.05)  # straining
for k in range(10):
    whoosh(fr(S3 + 176 + k * 11), 0.2, 0.06, 300, 1200)  # dragging
for k in range(14):
    add(tone(180, 0.08, "sine", 0.001, 0.03), fr(S3 + 296 + k * 7), 0.2)  # heavy footsteps
# humid outside
whoosh(fr(S4), 2.5, 0.12, 200, 1200)
for k in range(24):
    plop(fr(S4 + 62 + k * 5.5), 0.12)
add(sweep(160, 520, 4.0, "tri") * np.minimum(1, np.linspace(0, 4, int(4 * SR))), fr(S4 + 70), 0.08)  # inflating
boing(fr(S4 + 190), 140, 300, 0.3)
for f in (S4 + 250, S4 + 256):
    thud(fr(f), 0.4)
# idea
chime(fr(S5 + 14), (91, 96), 0.22, 0.05)
whoosh(fr(S5 + 70), 0.4, 0.2)
for k in range(3):
    pop(fr(S5 + 86 + k * 16), 0.25, 700 + k * 150)
# cooking
for at in (40, 70, 120, 150, 180, 210, 250):
    for j in range(3):
        plop(fr(S6 + at + 16 + j * 4), 0.22)
sim = noise(11, lo=400, hi=3000)
bub = np.zeros_like(sim)
for k in range(220):
    i = int(rng.uniform(0, len(bub) - 3000))
    bub[i : i + 2000] += sweep(rng.uniform(300, 900), rng.uniform(900, 1600), 2000 / SR) * env(2000, 0.001, 0.01)
add((sim * 0.25 + bub * 0.6) * np.minimum(1, np.linspace(0, 6, len(sim))) * np.minimum(1, np.linspace(6, 0, len(sim))), fr(S6 + 60), 0.12)
chime(fr(S6 + 330), (84, 88, 91, 96), 0.22, 0.09)
# transform
for k in range(3):
    add(sweep(220, 140, 0.18) * env(int(0.18 * SR), 0.005, 0.08), fr(S7 + 66 + k * 14), 0.25)  # gulp
whoosh(fr(S7 + 112), 2.2, 0.35, 1500, 9000)  # steam hiss
add(sweep(300, 160, 1.2, "tri"), fr(S7 + 120), 0.06)  # deflate
add(sweep(300, 1400, 0.6), fr(S7 + 190), 0.12)
chime(fr(S7 + 205), (84, 88, 91, 96, 100), 0.18, 0.06)
# proposal
chime(fr(S8 + 24), (96,), 0.15)
for k in range(10):
    add(tone(320, 0.05, "sine", 0.001, 0.02), fr(S8 + 42 + k * 7), 0.15)
add(bell(midi(76), 1.6), fr(S8 + 118), 0.35)  # ding
add(bell(midi(72), 2.0), fr(S8 + 128), 0.35)  # dong
add(sweep(400, 300, 0.4, "tri") * env(int(0.4 * SR), 0.05, 0.2), fr(S8 + 150), 0.06)  # creak
chime(fr(S8 + 205), (88, 91, 93, 96), 0.15, 0.12)
for k in range(8):
    add(tone(midi(84 + (k % 3) * 2), 0.07, "sine", 0.002, 0.03), fr(S8 + 210 + k * 9), 0.05)  # giggles
for side in (-0.8, 0.8):
    add(noise(0.25, lo=200) * env(int(0.25 * SR), 0.001, 0.06), fr(S8 + 282), 0.6, pan=side)  # confetti cannons
crowd = sum(sweep(rng.uniform(300, 600), rng.uniform(500, 900), 1.6, "tri") * env(int(1.6 * SR), 0.05, 0.8) for _ in range(10))
add(crowd / 6, fr(S8 + 284), 0.18)
chime(fr(S8 + 284), (84, 88, 91, 96), 0.2, 0.05)
# end
chime(fr(S9 + 18), (79, 84, 88, 91, 96), 0.2, 0.08)

# ---------------------------------------------------------------- master
st = np.stack([L, R], 1)
fade = np.ones(N)
fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
st *= fade[:, None]
st /= max(1e-6, np.abs(st).max()) / 0.85
st = np.tanh(st * 1.1) / np.tanh(1.1)
with wave.open("public/soundtrack.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((st * 32000).astype(np.int16).tobytes())
print("ok", DUR)
