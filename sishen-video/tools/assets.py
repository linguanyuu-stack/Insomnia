"""Make supporting assets: sprite size map, paper texture, package crops."""
import json, glob, os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
import sys
sys.path.insert(0, os.path.dirname(__file__))
from extract import cut

sizes = {}
for f in sorted(glob.glob("public/sprites/*.png")):
    im = Image.open(f)
    sizes[os.path.basename(f)[:-4]] = [im.width, im.height]
json.dump(sizes, open("src/sprites.json", "w"), indent=1)

# warm watercolour paper grain (multiplied over every scene)
rng = np.random.default_rng(7)
h, w = 1080, 1920
n = rng.normal(0, 1, (h // 2, w // 2))
n = ndi.gaussian_filter(n, 1.2) * 0.6 + ndi.gaussian_filter(rng.normal(0, 1, (h // 2, w // 2)), 18) * 6
n = (n - n.min()) / (n.max() - n.min())
v = (232 + n * 23).clip(0, 255)
img = np.dstack([v, v * 0.985, v * 0.955]).astype(np.uint8)
Image.fromarray(img).resize((w, h), Image.BICUBIC).save("public/paper.jpg", quality=88)

# package front for the end card
pk = np.array(Image.open("src_art/2.webp").convert("RGB"))
front = cut(pk[0:896, 40:680].copy(), 235, 1)
Image.fromarray(front).save("public/package_front.png")
back = cut(pk[0:896, 690:1320].copy(), 235, 1)
Image.fromarray(back).save("public/package_back.png")
print(len(sizes), front.shape, back.shape)
