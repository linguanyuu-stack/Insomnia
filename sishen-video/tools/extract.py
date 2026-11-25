"""Cut character poses out of the reference sheets into transparent PNG sprites.

Background is warm paper; characters have dark-brown outlines.  We flood-fill
the paper colour from the cell border (outlines stop the fill), drop the soft
floor shadow and loose sparkle marks, then feather the alpha edge.
"""
import sys
import numpy as np
import cv2
from PIL import Image
from scipy import ndimage as ndi

SRC = sys.argv[1] if len(sys.argv) > 1 else "src_art"
OUT = sys.argv[2] if len(sys.argv) > 2 else "public/sprites"

# name: (sheet, x0, y0, x1, y1)
CELLS = {
    # sheet 1: 川芎 / 蓮子 / 白茯苓 / 芡實
    "chuanxiong_idle": ("1", 250, 0, 520, 224),
    "chuanxiong_walk": ("1", 570, 0, 870, 224),
    "chuanxiong_point": ("1", 900, 0, 1250, 224),
    "lianzi_idle": ("1", 250, 230, 520, 448),
    "lianzi_surprise": ("1", 590, 230, 870, 448),
    "lianzi_leaf": ("1", 940, 220, 1250, 460),
    "fuling_idle": ("1", 250, 460, 520, 672),
    "fuling_shy": ("1", 570, 460, 870, 672),
    "fuling_cloth": ("1", 900, 460, 1300, 672),
    "qianshi_idle": ("1", 250, 680, 520, 896),
    "qianshi_angry": ("1", 570, 680, 870, 896),
    "qianshi_run": ("1", 880, 680, 1250, 896),
    # sheet 3: 淮山 / 紅棗 / 熟地
    "huaishan_shy": ("3", 100, 0, 448, 300),
    "huaishan_calm": ("3", 520, 0, 896, 300),
    "huaishan_herb": ("3", 896, 0, 1300, 300),
    "hongzao_pour": ("3", 60, 300, 448, 600),
    "hongzao_cup": ("3", 448, 300, 896, 600),
    "hongzao_wave": ("3", 896, 300, 1300, 600),
    "shudi_yawn": ("3", 60, 600, 448, 896),
    "shudi_sleep": ("3", 448, 600, 896, 896),
    "shudi_stretch": ("3", 896, 600, 1300, 896),
    # sheet 5: 何首烏 / 當歸 / 天麻
    "heshouwu_read": ("5", 60, 0, 448, 300),
    "heshouwu_cheer": ("5", 448, 0, 896, 300),
    "heshouwu_lantern": ("5", 896, 0, 1344, 300),
    "danggui_blanket": ("5", 60, 300, 448, 600),
    "danggui_tea": ("5", 448, 300, 896, 600),
    "danggui_water": ("5", 896, 300, 1344, 600),
    "tianma_yawn": ("5", 60, 600, 448, 896),
    "tianma_sleep": ("5", 448, 600, 896, 896),
    "tianma_star": ("5", 896, 600, 1344, 896),
}


LIGHT = {n: (205, 2) for n in ["fuling_idle", "fuling_shy", "fuling_cloth"]}


def paper_mask(rgb):
    """True where pixel looks like paper (light, low-chroma warm)."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    L, a, b = lab[..., 0], lab[..., 1] - 128, lab[..., 2] - 128
    return L, a, b


def cut(rgb, edge_L=150, dil=1):
    h, w, _ = rgb.shape
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    border = np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    ref = np.median(border, axis=0)
    d = np.sqrt(((lab - ref) ** 2 * np.array([0.6, 1.0, 1.0])).sum(-1))
    # paper or soft shadow: close in colour, and not much darker
    cand = (d < 22) | ((lab[..., 0] > ref[0] - 38) & (np.abs(lab[..., 1] - ref[1]) < 9)
                       & (np.abs(lab[..., 2] - ref[2]) < 16) & (d < 34))
    # dark outlines are barriers
    edges = lab[..., 0] < edge_L
    edges = ndi.binary_dilation(edges, iterations=dil)
    cand &= ~edges
    lbl, n = ndi.label(cand)
    border_lbls = set(np.unique(np.concatenate([lbl[0], lbl[-1], lbl[:, 0], lbl[:, -1]]))) - {0}
    bg = np.isin(lbl, list(border_lbls))
    fg = ~bg
    fg = ndi.binary_opening(fg, iterations=1)
    lbl2, n2 = ndi.label(fg)
    if n2 == 0:
        return None
    sizes = ndi.sum(fg, lbl2, range(1, n2 + 1))
    biggest = sizes.max()
    keep = [i + 1 for i, s in enumerate(sizes) if s > 0.12 * biggest]
    fg = np.isin(lbl2, keep)
    fg = ndi.binary_fill_holes(fg)
    # interior holes that are clearly paper (e.g. gap between arm and body)
    holes = bg == False  # noqa
    alpha = fg.astype(np.float32)
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0.8)
    ys, xs = np.where(fg)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    pad = 4
    y0, x0 = max(0, y0 - pad), max(0, x0 - pad)
    y1, x1 = min(h, y1 + pad), min(w, x1 + pad)
    rgba = np.dstack([rgb, (alpha * 255).astype(np.uint8)])
    return rgba[y0:y1, x0:x1]


def main():
    import os
    os.makedirs(OUT, exist_ok=True)
    sheets = {}
    for name, (s, x0, y0, x1, y1) in CELLS.items():
        if s not in sheets:
            sheets[s] = np.array(Image.open(f"{SRC}/{s}.webp").convert("RGB"))
        rgb = sheets[s][y0:y1, x0:x1].copy()
        out = cut(rgb, *LIGHT.get(name, (150, 1)))
        if out is None:
            print("FAILED", name)
            continue
        Image.fromarray(out).save(f"{OUT}/{name}.png")
        print(name, out.shape[1], out.shape[0])


if __name__ == "__main__":
    main()
