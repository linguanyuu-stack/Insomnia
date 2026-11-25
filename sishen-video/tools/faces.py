"""Erase painted faces so expressions can be redrawn at render time.

For each sprite we know (hand-measured, fractions of the sprite box):
  box   region holding eyes/brows/mouth
  eyes  left & right eye centres
  mouth mouth centre
Dark/red facial strokes inside the box are masked and inpainted (OpenCV Telea),
which keeps the surrounding watercolour texture.  Output:
  public/sprites/<name>__nf.png   (no face)
  src/faces.json                  anchors in sprite pixel coordinates
"""
import json
import numpy as np
import cv2
from PIL import Image
from scipy import ndimage as ndi

FACES = {
    # name: (box x0,y0,x1,y1), (eyeL), (eyeR), (mouth)
    "fuling_idle": ((0.47, 0.27, 0.89, 0.54), (0.555, 0.405), (0.80, 0.40), (0.68, 0.47)),
    "fuling_shy": ((0.42, 0.32, 0.86, 0.57), (0.53, 0.46), (0.77, 0.44), (0.645, 0.49)),
    "lianzi_idle": ((0.40, 0.30, 0.88, 0.58), (0.50, 0.47), (0.79, 0.47), (0.655, 0.52)),
    "lianzi_surprise": ((0.32, 0.21, 0.82, 0.55), (0.45, 0.385), (0.725, 0.385), (0.59, 0.48)),
    "lianzi_leaf": ((0.30, 0.36, 0.64, 0.62), (0.40, 0.46), (0.565, 0.43), (0.49, 0.53)),
    "qianshi_idle": ((0.48, 0.38, 0.92, 0.60), (0.585, 0.50), (0.82, 0.50), (0.70, 0.535)),
    "qianshi_angry": ((0.52, 0.48, 0.89, 0.74), (0.60, 0.60), (0.785, 0.575), (0.73, 0.67)),
    "qianshi_run": ((0.45, 0.19, 0.86, 0.48), (0.52, 0.27), (0.76, 0.27), (0.65, 0.37)),
    "chuanxiong_idle": ((0.53, 0.32, 0.93, 0.56), (0.62, 0.44), (0.85, 0.42), (0.73, 0.50)),
    "chuanxiong_walk": ((0.46, 0.19, 0.83, 0.45), (0.55, 0.30), (0.725, 0.30), (0.63, 0.385)),
    "chuanxiong_point": ((0.44, 0.24, 0.74, 0.55), (0.535, 0.385), (0.665, 0.37), (0.60, 0.475)),
    "danggui_tea": ((0.40, 0.30, 0.74, 0.455), (0.47, 0.37), (0.68, 0.37), (0.57, 0.405)),
    "danggui_water": ((0.50, 0.41, 0.77, 0.56), (0.56, 0.47), (0.705, 0.47), (0.63, 0.51)),
    "huaishan_herb": ((0.38, 0.33, 0.75, 0.50), (0.45, 0.405), (0.68, 0.405), (0.57, 0.45)),
    "huaishan_calm": ((0.50, 0.43, 0.81, 0.57), (0.585, 0.50), (0.725, 0.50), (0.655, 0.53)),
    "gouqi_run": ((0.42, 0.30, 0.75, 0.48), (0.50, 0.37), (0.675, 0.37), (0.565, 0.42)),
    "gouqi_jump": ((0.37, 0.28, 0.73, 0.48), (0.45, 0.355), (0.665, 0.355), (0.555, 0.42)),
    "gouqi_point": ((0.53, 0.35, 0.84, 0.53), (0.60, 0.42), (0.775, 0.41), (0.665, 0.47)),
}


def main():
    out = {}
    for name, (box, el, er, mo) in FACES.items():
        im = np.array(Image.open(f"public/sprites/{name}.png").convert("RGBA"))
        h, w = im.shape[:2]
        rgb = np.ascontiguousarray(im[..., :3])
        ext = 0 if name.startswith("danggui") else 0.07
        box = (box[0] - 0.02, box[1] - ext, box[2] + 0.02, box[3])
        x0, y0, x1, y1 = int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)
        lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
        L = lab[..., 0]
        region = np.zeros((h, w), bool)
        region[y0:y1, x0:x1] = True
        # elliptical region so corners (cups, hands) are left alone
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
        region &= ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.15
        med = np.median(L[region])
        dark = region & (L < med - 32)
        lbl, n = ndi.label(dark)
        if n:
            sz = ndi.sum(dark, lbl, range(1, n + 1))
            dark = np.isin(lbl, [i + 1 for i, v in enumerate(sz) if v >= 5])
        # snap hand-measured anchors to the nearest painted feature
        lbl, n = ndi.label(dark)
        cents = ndi.center_of_mass(dark, lbl, range(1, n + 1)) if n else []
        def snap(a):
            ax, ay = a[0] * w, a[1] * h
            best = None
            for cyy, cxx in cents:
                dd = np.hypot(cxx - ax, cyy - ay)
                if dd < 0.07 * w and (best is None or dd < best[0]):
                    best = (dd, cxx / w, cyy / h)
            return (best[1], best[2]) if best else a
        el, er, mo = snap(el), snap(er), snap(mo)
        # always clear discs around the eyes and mouth (catches pink mouth interiors)
        dist = abs(er[0] - el[0]) * w
        discs = [(el, 0.3), (er, 0.3), (mo, 0.36)]
        if not name.startswith("danggui"):
            # brows sit ~0.4 eye-distances above each eye and flare outwards
            for (ex, ey), sgn in ((el, -1), (er, 1)):
                discs.append(((ex + sgn * 0.08 * dist / w, ey - 0.42 * dist / h), 0.34))
        for (ax, ay), rr in discs:
            dark |= region & (((xx - ax * w) / (rr * dist)) ** 2 + ((yy - ay * h) / (rr * dist * 0.7)) ** 2 <= 1)
        filled = ndi.binary_fill_holes(ndi.binary_dilation(dark, iterations=2)) & region
        mask = ndi.binary_dilation(filled, iterations=2) & region
        fixed = cv2.inpaint(rgb, mask.astype(np.uint8) * 255, 6, cv2.INPAINT_TELEA)
        # soften seam
        soft = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 1.5)[..., None]
        blend = (rgb * (1 - soft) + fixed * soft).astype(np.uint8)
        res = np.dstack([blend, im[..., 3]])
        Image.fromarray(res).save(f"public/sprites/{name}__nf.png")
        skin = np.median(rgb[region & ~mask], axis=0)
        out[name] = {
            "w": w,
            "h": h,
            "eyeL": [el[0] * w, el[1] * h],
            "eyeR": [er[0] * w, er[1] * h],
            "mouth": [mo[0] * w, mo[1] * h],
            "skin": "#%02x%02x%02x" % tuple(int(v) for v in skin),
        }
        print(name, int(mask.sum()))
    json.dump(out, open("src/faces.json", "w"), indent=1)


if __name__ == "__main__":
    main()
