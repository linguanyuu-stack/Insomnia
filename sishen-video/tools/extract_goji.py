"""Cut the goji (枸杞) character out of the package illustration with GrabCut."""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi
im = np.array(Image.open("src_art/2.webp").convert("RGB"))
x0, y0, x1, y1 = 455, 455, 640, 650
crop = im[y0:y1, x0:x1].copy()
up = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
mask = np.zeros(up.shape[:2], np.uint8)
rect = (3 * 10, 3 * 12, 3 * 172, 3 * 180)
bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
cv2.grabCut(cv2.cvtColor(up, cv2.COLOR_RGB2BGR), mask, rect, bgd, fgd, 8, cv2.GC_INIT_WITH_RECT)
fg = (mask == 1) | (mask == 3)
fg = ndi.binary_opening(fg, iterations=2)
lbl, n = ndi.label(fg)
sizes = ndi.sum(fg, lbl, range(1, n + 1))
fg = lbl == (np.argmax(sizes) + 1)
fg = ndi.binary_fill_holes(fg)
a = cv2.GaussianBlur(fg.astype(np.float32), (5, 5), 1.2)
rgba = np.dstack([up, (a * 255).astype(np.uint8)])
ys, xs = np.where(fg)
rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
Image.fromarray(rgba).save("public/sprites/gouqi_cup.png")
print(rgba.shape)
