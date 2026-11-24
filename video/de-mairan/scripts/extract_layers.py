"""Cut the storyboard panels into transparent layers for the 2.5D (Three.js) scenes.

Input : assets/panels/<panel>_x4.png  (4x upscaled panel, see scripts/README)
Output: public/layers/<panel>/<layer>.png + src/layers.json (positions in panel px x4)

How a layer is cut: pixels that differ from the local paper colour are "ink";
ink inside the layer's lasso polygon (first matching polygon wins) becomes the
layer, with enclosed areas filled so pale faces / leaves stay opaque. Colours are
un-premultiplied against the paper so layers composite cleanly on any paper.
"""
import json, pathlib
import numpy as np, cv2
from PIL import Image
from scipy import ndimage

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = 4  # upscale factor; polygons below are in original storyboard-panel pixels

# panel -> ordered layers {name: lasso polygon}. Earlier entries win overlaps.
LAYERS = {
    'p1': {  # 1729
        'props': [(128, 128), (212, 128), (214, 150), (292, 150), (294, 210), (126, 210)],
        'banner': [(0, 0), (432, 0), (432, 218), (0, 218)],
    },
    'p2': {  # portrait
        'telescope': [(255, 170), (401, 170), (401, 310), (262, 310), (255, 240)],
        'orbit': [(240, 0), (401, 0), (401, 98), (240, 98)],
        'name': [(250, 98), (401, 98), (401, 175), (255, 175)],
        'person': [(0, 0), (240, 0), (248, 100), (252, 200), (295, 330), (295, 368), (0, 368)],
    },
    'p3': {  # mimosa day / night
        'title': [(250, 5), (430, 5), (430, 84), (250, 84)],
        'arrows': [(300, 132), (368, 132), (368, 178), (300, 178)],
        'plantR': [(360, 80), (455, 80), (470, 100), (640, 108), (645, 240), (360, 250)],
        'skyNight': [(425, 0), (671, 0), (671, 125), (425, 125)],
        'skyDay': [(25, 0), (245, 0), (245, 92), (25, 92)],
        'plantL': [(5, 55), (305, 55), (305, 245), (5, 255)],
        'labelL': [(65, 236), (275, 236), (275, 324), (65, 324)],
        'labelR': [(400, 236), (625, 236), (625, 324), (400, 324)],
    },
    'p4': {  # de Mairan with the magnifier
        'mairan': [(150, 293), (150, 250), (170, 238), (185, 210), (213, 190), (248, 160), (268, 140), (305, 134), (335, 148), (346, 178), (350, 198), (395, 198), (412, 208), (442, 226), (442, 293)],
        'title': [(220, 5), (382, 5), (382, 75), (220, 75)],
        'arrows': [(268, 95), (322, 95), (322, 135), (268, 135)],
        'plantR': [(335, 72), (440, 72), (565, 85), (565, 200), (345, 205)],
        'skyNight': [(380, 0), (586, 0), (586, 100), (380, 100)],
        'skyDay': [(0, 0), (205, 0), (205, 45), (130, 80), (0, 80)],
        'plantL': [(5, 55), (268, 55), (268, 148), (240, 172), (205, 198), (5, 218)],
        'labelL': [(28, 198), (168, 198), (168, 268), (28, 268)],
        'labelR': [(418, 198), (568, 198), (568, 268), (418, 268)],
    },
    'p5': {  # the cabinet experiment
        'watch': [(535, 180), (645, 180), (645, 262), (535, 262)],
        'note': [(410, 185), (645, 185), (645, 324), (410, 324)],
        'results': [(410, 12), (645, 12), (645, 185), (410, 185)],
        'arrowR': [(372, 92), (416, 92), (416, 126), (372, 126)],
        'bubble': [(160, 140), (250, 140), (262, 225), (262, 255), (160, 255)],
        'cabinet': [(246, 118), (412, 118), (412, 302), (246, 302)],
        'title': [(255, 5), (388, 5), (388, 75), (255, 75)],
        'recap': [(0, 0), (252, 0), (252, 135), (0, 135)],
        'mairan': [(0, 130), (112, 130), (172, 160), (186, 250), (264, 270), (264, 320), (0, 324)],
    },
}


def paper_field(img):
    """smooth estimate of the paper colour under the drawing"""
    small = cv2.resize(img, (img.shape[1] // 8, img.shape[0] // 8), interpolation=cv2.INTER_AREA).astype(np.float32)
    ref = np.median(small.reshape(-1, 3), axis=0)
    near = (np.linalg.norm(small - ref, axis=2) < 22).astype(np.float32)
    num = cv2.GaussianBlur(small * near[..., None], (0, 0), 12)
    den = cv2.GaussianBlur(near, (0, 0), 12)[..., None] + 1e-4
    field = num / den
    field[den[..., 0] < 0.02] = ref
    return cv2.resize(field, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC), ref


def main():
    manifest = {}
    for panel, layers in LAYERS.items():
        img = np.asarray(Image.open(ROOT / 'assets' / 'panels' / f'{panel}_x4.png').convert('RGB')).astype(np.float32)
        H, W = img.shape[:2]
        field, ref = paper_field(img)
        dist = np.linalg.norm(img - field, axis=2)
        soft = np.clip((dist - 9) / 26, 0, 1)  # faint pencil -> partly transparent
        ink = cv2.morphologyEx((dist > 16).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
        # ignore the storyboard's white panel border
        ink[:16, :] = 0; ink[-16:, :] = 0; ink[:, :16] = 0; ink[:, -16:] = 0
        soft[:16, :] = 0; soft[-16:, :] = 0; soft[:, :16] = 0; soft[:, -16:] = 0
        taken = np.zeros((H, W), bool)
        out = {'size': [W, H], 'paper': [int(c) for c in ref], 'layers': []}
        (ROOT / 'public' / 'layers' / panel).mkdir(parents=True, exist_ok=True)
        for name, poly in layers.items():
            region = np.zeros((H, W), np.uint8)
            cv2.fillPoly(region, [np.array([(x * S, y * S) for x, y in poly], np.int32)], 1)
            region = region.astype(bool) & ~taken
            m = ink.astype(bool) & region
            m = ndimage.binary_fill_holes(m) & region
            lab, n = ndimage.label(m)  # drop specks
            if n:
                sizes = ndimage.sum(m, lab, range(1, n + 1))
                m = np.isin(lab, 1 + np.flatnonzero(sizes >= 60))
            solid = ndimage.binary_erosion(m, iterations=2)
            alpha = np.where(solid, 1.0, soft) * m
            alpha = cv2.GaussianBlur(alpha.astype(np.float32), (0, 0), 0.8) * region
            taken |= m
            a = np.clip(alpha, 0, 1)[..., None]
            rgb = np.where(a > 0.02, (img - (1 - a) * field) / np.maximum(a, 0.02), img)
            ys, xs = np.nonzero(a[..., 0] > 0.01)
            if not len(xs):
                continue
            x0, x1, y0, y1 = max(xs.min() - 4, 0), min(xs.max() + 5, W), max(ys.min() - 4, 0), min(ys.max() + 5, H)
            rgba = np.dstack([np.clip(rgb, 0, 255), a[..., 0] * 255])[y0:y1, x0:x1].astype(np.uint8)
            Image.fromarray(rgba, 'RGBA').save(ROOT / 'public' / 'layers' / panel / f'{name}.png', optimize=True)
            out['layers'].append({'name': name, 'file': f'layers/{panel}/{name}.png', 'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0)})
            print(panel, name, x1 - x0, 'x', y1 - y0)
        manifest[panel] = out
    (ROOT / 'src' / 'layers.json').write_text(json.dumps(manifest, indent=1))


if __name__ == '__main__':
    main()
