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
    'arrows': ('p3', [(300, 132), (368, 132), (368, 178), (300, 178)], []),
    'labelDay': ('p3', [(65, 236), (275, 236), (275, 324), (65, 324)], []),
    'labelNight': ('p3', [(400, 236), (625, 236), (625, 324), (400, 324)], []),
    # de Mairan with the magnifier
    'mairanLens': ('p4', [(150, 293), (150, 250), (170, 238), (185, 210), (213, 190), (248, 160), (268, 140), (305, 134), (335, 148), (346, 178), (350, 198), (395, 198), (412, 208), (442, 226), (442, 293)], []),
    # the cabinet experiment
    'mairanWrite': ('p5', [(0, 140), (112, 136), (172, 160), (186, 250), (264, 270), (264, 320), (0, 324)], []),
    'cabinet': ('p5', [(264, 118), (412, 118), (412, 302), (252, 302), (252, 258), (264, 250)], []),
    'bubble': ('p5', [(172, 140), (250, 140), (262, 225), (262, 252), (172, 252)], []),
    'watch': ('p5', WATCH, []),
    'note': ('p5', [(410, 185), (645, 185), (645, 324), (410, 324)], [WATCH]),
    'resultHead': ('p5', [(410, 12), (645, 12), (645, 66), (410, 66)], []),
    'resultDay': ('p5', [(421, 67), (632, 67), (632, 121), (421, 121)], []),
    'resultNight': ('p5', [(421, 125), (632, 125), (632, 179), (421, 179)], []),
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


def main():
    out_dir = ROOT / 'public' / 'el'
    out_dir.mkdir(parents=True, exist_ok=True)
    panels = {}
    manifest = {}
    rng = np.random.default_rng(3)
    for name, (panel, poly, minus) in ELEMENTS.items():
        if panel not in panels:
            img = np.asarray(Image.open(ROOT / 'assets' / 'panels' / f'{panel}_x4.png').convert('RGB')).astype(np.float32)
            field = paper_field(img)
            dist = np.linalg.norm(img - field, axis=2)
            soft = np.clip((dist - 9) / 26, 0, 1)
            ink = cv2.morphologyEx((dist > 16).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)).astype(bool)
            for a in (ink, soft):  # storyboard's white panel border is not ink
                a[:16, :] = 0; a[-16:, :] = 0; a[:, :16] = 0; a[:, -16:] = 0
            panels[panel] = (img, field, soft, ink)
        img, field, soft, ink = panels[panel]
        H, W = ink.shape
        region = poly_mask((H, W), poly)
        for mp in minus:
            region &= ~poly_mask((H, W), mp)
        m = ndimage.binary_fill_holes(ink & region) & region
        lab, n = ndimage.label(m)
        if n:
            sizes = ndimage.sum(m, lab, range(1, n + 1))
            m = np.isin(lab, 1 + np.flatnonzero(sizes >= 60))
        solid = ndimage.binary_erosion(m, iterations=2)
        alpha = cv2.GaussianBlur((np.where(solid, 1.0, soft) * m).astype(np.float32), (0, 0), 0.8) * region
        a = np.clip(alpha, 0, 1)[..., None]
        rgb = np.where(a > 0.02, (img - (1 - a) * field) / np.maximum(a, 0.02), img)
        # scissor-cut backing: silhouette grown by MARGIN with a slightly irregular edge
        blob = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
        blob = ndimage.binary_fill_holes(blob)
        d = ndimage.distance_transform_edt(~blob)
        wobble = cv2.resize(rng.normal(0, 1, (H // 24 + 1, W // 24 + 1)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
        back = np.clip((MARGIN + wobble * 4 - d) / 1.5, 0, 1)
        ys, xs = np.nonzero(back > 0.01)
        pad = 6
        x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, W)
        y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, H)
        rgba = np.dstack([np.clip(rgb, 0, 255), a[..., 0] * 255])[y0:y1, x0:x1].astype(np.uint8)
        Image.fromarray(rgba, 'RGBA').save(out_dir / f'{name}.png', optimize=True)
        Image.fromarray((back[y0:y1, x0:x1] * 255).astype(np.uint8), 'L').save(out_dir / f'{name}.back.png', optimize=True)
        manifest[name] = {'file': f'el/{name}.png', 'back': f'el/{name}.back.png', 'w': int(x1 - x0), 'h': int(y1 - y0), 'panel': panel, 'x0': int(x0), 'y0': int(y0)}
        print(f'{name:12s} {x1 - x0}x{y1 - y0}')
    (ROOT / 'src' / 'elements.json').write_text(json.dumps(manifest, indent=1))


if __name__ == '__main__':
    main()
