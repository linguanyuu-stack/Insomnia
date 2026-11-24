"""Cut the storyboard drawings into individual elements (characters, plants, props, labels).

Input : assets/panels/<panel>_x4.png   (storyboard panels upscaled 4x)
Output: public/el/<name>.png       art, transparent background (colours un-premultiplied)
        public/el/<name>.back.png  "paper cut-out" backing: the art's silhouette grown
                                   by a scissor-cut margin (used for the collage look + shadow)
        src/elements.json          sizes + position inside the panel, in px (x4)

Polygons are lassos in storyboard-panel pixels (before the 4x upscale).
`minus` removes areas that belong to a neighbouring element.
"""
import json, pathlib
import numpy as np, cv2
from PIL import Image
from scipy import ndimage

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = 4
MARGIN = 16  # backing margin in x4 px

PROPS = [(128, 128), (212, 128), (214, 150), (292, 150), (294, 210), (126, 210)]
PLANT_CLOSED = [(360, 80), (455, 80), (470, 100), (640, 108), (645, 234), (360, 234)]
WATCH = [(535, 180), (645, 180), (645, 262), (535, 262)]
# the cabinet, taken apart so it can be animated (see cut_cabinet)
CAB_BODY = [(255, 119), (384, 119), (384, 144), (368, 144), (368, 300), (255, 300)]
CAB_INSIDE = (270, 148, 363, 279)  # the dark opening (x0, y0, x1, y1)
CAB_PLANT = [(270, 168), (356, 168), (356, 277), (270, 277)]
DOOR_QUAD = [(366, 146), (404, 129), (404, 287), (367, 285)]  # the open door, seen at an angle
DOOR_FRONT = (268, 146, 366, 288)  # where the closed door sits (x0, y0, x1, y1)

ELEMENTS = {
    # 1729
    'banner': ('p1', [(0, 0), (432, 0), (432, 218), (0, 218)], [PROPS]),
    'globe': ('p1', [(128, 122), (204, 122), (204, 212), (128, 212)], []),
    'books': ('p1', [(198, 150), (294, 150), (294, 210), (198, 210)], []),
    # the astronomer
    'portrait': ('p2', [(0, 0), (240, 0), (248, 100), (252, 200), (295, 330), (295, 368), (0, 368)], []),
    'orbit': ('p2', [(240, 0), (401, 0), (401, 98), (240, 98)], []),
    'name': ('p2', [(250, 98), (401, 98), (401, 175), (255, 175)], []),
    'telescope': ('p2', [(255, 170), (401, 170), (401, 310), (262, 310), (255, 240)], []),
    # mimosa, day & night
    'plantOpen': ('p3', [(5, 95), (140, 95), (140, 66), (250, 66), (250, 88), (305, 88), (305, 236), (5, 236)], []),
    'plantClosed': ('p3', PLANT_CLOSED, []),
    'sun': ('p3', [(25, 0), (140, 0), (140, 92), (25, 92)], []),
    'cloud': ('p3', [(140, 15), (245, 15), (245, 62), (140, 62)], []),
    'nightSky': ('p3', [(425, 0), (671, 0), (671, 125), (425, 125)], [PLANT_CLOSED]),
    'title': ('p3', [(250, 5), (430, 5), (430, 84), (250, 84)], []),
    # de Mairan with the magnifier
    'mairanLens': ('p4', [(150, 293), (150, 250), (170, 238), (185, 210), (213, 190), (248, 160), (268, 140), (305, 134), (335, 148), (346, 178), (350, 198), (395, 198), (412, 208), (442, 226), (442, 293)], []),
    # the cabinet experiment
    'mairanWrite': ('p5', [(0, 140), (112, 136), (172, 160), (186, 250), (264, 270), (264, 320), (0, 324)], []),
    'watch': ('p5', WATCH, []),
    # key words only (the rest of the storyboard text is acted out instead)
    'kwDark': ('p5', [(175, 192), (209, 192), (209, 206), (175, 206)], []),
    'kwClock': ('p5', [(436, 230), (530, 230), (530, 254), (436, 254)], []),
}


def paper_field(img):
    small = cv2.resize(img, (img.shape[1] // 8, img.shape[0] // 8), interpolation=cv2.INTER_AREA).astype(np.float32)
    ref = np.median(small.reshape(-1, 3), axis=0)
    near = (np.linalg.norm(small - ref, axis=2) < 22).astype(np.float32)
    num = cv2.GaussianBlur(small * near[..., None], (0, 0), 12)
    den = cv2.GaussianBlur(near, (0, 0), 12)[..., None] + 1e-4
    field = num / den
    field[den[..., 0] < 0.02] = ref
    return cv2.resize(field, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)


def poly_mask(shape, poly):
    m = np.zeros(shape, np.uint8)
    cv2.fillPoly(m, [np.array([(x * S, y * S) for x, y in poly], np.int32)], 1)
    return m.astype(bool)


def emit(out_dir, manifest, rng, name, panel, rgb, alpha, m, ox=0, oy=0):
    """save art + scissor-cut backing; (ox, oy) = where this array sits in the panel (x4 px)"""
    H, W = m.shape
    a = np.clip(alpha, 0, 1)[..., None]
    blob = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    blob = ndimage.binary_fill_holes(blob)
    blob = np.pad(blob, MARGIN * 2)  # room for the margin
    d = ndimage.distance_transform_edt(~blob)
    Hp, Wp = blob.shape
    wobble = cv2.resize(rng.normal(0, 1, (Hp // 24 + 1, Wp // 24 + 1)).astype(np.float32), (Wp, Hp), interpolation=cv2.INTER_CUBIC)
    back = np.clip((MARGIN + wobble * 4 - d) / 1.5, 0, 1)
    P = MARGIN * 2
    rgba = np.zeros((Hp, Wp, 4), np.float32)
    rgba[P:P + H, P:P + W, :3] = np.clip(rgb, 0, 255)
    rgba[P:P + H, P:P + W, 3] = a[..., 0] * 255
    ys, xs = np.nonzero((back > 0.01) | (rgba[..., 3] > 2))
    pad = 6
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, Wp)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, Hp)
    Image.fromarray(rgba[y0:y1, x0:x1].astype(np.uint8), 'RGBA').save(out_dir / f'{name}.png', optimize=True)
    Image.fromarray((back[y0:y1, x0:x1] * 255).astype(np.uint8), 'L').save(out_dir / f'{name}.back.png', optimize=True)
    manifest[name] = {'file': f'el/{name}.png', 'back': f'el/{name}.back.png', 'w': int(x1 - x0), 'h': int(y1 - y0),
                      'panel': panel, 'x0': int(ox + x0 - P), 'y0': int(oy + y0 - P)}
    print(f'{name:12s} {x1 - x0}x{y1 - y0}')


def load_panel(panel):
    img = np.asarray(Image.open(ROOT / 'assets' / 'panels' / f'{panel}_x4.png').convert('RGB')).astype(np.float32)
    field = paper_field(img)
    dist = np.linalg.norm(img - field, axis=2)
    soft = np.clip((dist - 9) / 26, 0, 1)
    ink = cv2.morphologyEx((dist > 16).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)).astype(bool)
    for a in (ink, soft):  # storyboard's white panel border is not ink
        a[:16, :] = 0; a[-16:, :] = 0; a[:, :16] = 0; a[:, -16:] = 0
    return img, field, soft, ink


def lasso(img, field, soft, ink, region):
    m = ndimage.binary_fill_holes(ink & region) & region
    lab, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, 1 + np.flatnonzero(sizes >= 60))
    solid = ndimage.binary_erosion(m, iterations=2)
    alpha = cv2.GaussianBlur((np.where(solid, 1.0, soft) * m).astype(np.float32), (0, 0), 0.8) * region
    a = np.clip(alpha, 0, 1)[..., None]
    rgb = np.where(a > 0.02, (img - (1 - a) * field) / np.maximum(a, 0.02), img)
    return rgb, alpha, m


def cut_cabinet(out_dir, manifest, rng):
    """the storyboard cabinet → empty cabinet body, the potted plant, and a flat front door"""
    img, field, soft, ink = load_panel('p5')
    H, W = ink.shape
    # potted plant: everything inside that is not the dark hatched interior
    lum = img.mean(axis=2)
    sat = (img.max(axis=2) - img.min(axis=2)) / np.maximum(img.max(axis=2), 1)
    plant_box = poly_mask((H, W), CAB_PLANT)
    pm = plant_box & ((lum > 105) | ((sat > 0.3) & (lum > 60)))
    pm = cv2.morphologyEx(pm.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    pm = cv2.morphologyEx(pm, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)).astype(bool)
    lab, n = ndimage.label(pm)
    sizes = ndimage.sum(pm, lab, range(1, n + 1))
    pm = lab == 1 + int(np.argmax(sizes))  # the plant + pot is the one big piece
    pm = pm | (ndimage.binary_fill_holes(pm) & (lum > 100))
    palpha = cv2.GaussianBlur(ndimage.binary_erosion(pm, iterations=1).astype(np.float32), (0, 0), 1.0)
    ys, xs = np.nonzero(pm)
    y0, y1, x0, x1 = ys.min() - 4, ys.max() + 5, xs.min() - 4, xs.max() + 5
    emit(out_dir, manifest, rng, 'pot', 'p5', img[y0:y1, x0:x1], palpha[y0:y1, x0:x1], pm[y0:y1, x0:x1], x0, y0)
    # empty cabinet: repaint the whole dark opening with pencil hatching, leave the open door behind
    ix0, iy0, ix1, iy1 = [v * S for v in CAB_INSIDE]
    hole = np.zeros((H, W), np.uint8)
    hole[iy0:iy1, ix0:ix1] = 1
    dark = np.median(img[iy0:iy1, ix0:ix1][~pm[iy0:iy1, ix0:ix1]], axis=0)
    noise = rng.normal(0, 1, (H, W)).astype(np.float32)
    k = np.zeros((31, 31), np.float32)
    cv2.line(k, (0, 30), (30, 0), 1.0, 1)
    streak = cv2.filter2D(noise, -1, k / k.sum())  # long diagonal pencil strokes
    streak = streak / streak.std()
    shade = np.linspace(-6, 10, iy1 - iy0)[:, None]  # a little lighter towards the floor
    bare = img.copy()
    bare[iy0:iy1, ix0:ix1] = dark + (streak[iy0:iy1, ix0:ix1, None] * 9 + shade[..., None]) * np.array([1, 1, 1.05])
    region = poly_mask((H, W), CAB_BODY)
    rgb, alpha, m = lasso(bare, field, soft, ink | (hole > 0), region)
    emit(out_dir, manifest, rng, 'cabinetBare', 'p5', rgb, alpha, m)
    # the door: un-warp the angled open door into a flat front panel the size of the opening
    fx0, fy0, fx1, fy1 = [v * S for v in DOOR_FRONT]
    dw, dh = fx1 - fx0, fy1 - fy0
    src = np.float32([(x * S, y * S) for x, y in DOOR_QUAD])
    dst = np.float32([(0, 0), (dw, 0), (dw, dh), (0, dh)])
    door = cv2.warpPerspective(img, cv2.getPerspectiveTransform(src, dst), (dw, dh), flags=cv2.INTER_CUBIC)
    dmask = np.ones((dh, dw), bool)
    dalpha = np.ones((dh, dw), np.float32)
    dalpha[:, :3] = 0.5
    cut_bottom = int(dh * 0.035)  # the warp catches a sliver of the cabinet base
    dalpha[-cut_bottom:, :] = 0
    dmask[-cut_bottom:, :] = False
    emit(out_dir, manifest, rng, 'door', 'p5', door, dalpha, dmask, fx0, fy0)


def main():
    out_dir = ROOT / 'public' / 'el'
    out_dir.mkdir(parents=True, exist_ok=True)
    panels = {}
    manifest = {}
    rng = np.random.default_rng(3)
    for name, (panel, poly, minus) in ELEMENTS.items():
        if panel not in panels:
            panels[panel] = load_panel(panel)
        img, field, soft, ink = panels[panel]
        H, W = ink.shape
        region = poly_mask((H, W), poly)
        for mp in minus:
            region &= ~poly_mask((H, W), mp)
        rgb, alpha, m = lasso(img, field, soft, ink, region)
        emit(out_dir, manifest, rng, name, panel, rgb, alpha, m)
    cut_cabinet(out_dir, manifest, rng)
    (ROOT / 'src' / 'elements.json').write_text(json.dumps(manifest, indent=1))


if __name__ == '__main__':
    main()
