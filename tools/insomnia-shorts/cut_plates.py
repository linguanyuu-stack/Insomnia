"""Cut pieces of the rendered public-edition plates (books/insomnia-shorts/art/plates/*.png, from render_plates.js) into
site/insomnia-shorts/img/*.webp and write their sizes into img/art.js (merged with what is there).
Boxes are in the 742-px-wide preview's coordinates (x3 for the 3x render).
    uv run --with pillow python3 tools/insomnia-shorts/cut_plates.py
"""
import json, re
from pathlib import Path
from PIL import Image
SRC = Path("books/insomnia-shorts/art/plates"); OUT = Path("site/insomnia-shorts/img")
CUTS = {
    "pl-day":     ("pp-mimosa", (12, 32, 184, 228)),
    "pl-night":   ("pp-mimosa", (186, 32, 359, 228)),
    "pl-cabinet": ("pp-mimosa", (382, 32, 731, 300)),
    "pl-cave":    ("pp-cave",   (12, 84, 359, 384)),
    "pl-acto":    ("pp-cave",   (432, 72, 728, 304)),
    "pl-fly":     ("pp-nobel",  (88, 36, 298, 264)),
    "pl-medal":   ("pp-nobel",  (540, 322, 668, 484)),
    "pl-cell":    ("pp-nobel",  (102, 342, 378, 618)),
    "pl-body":    ("pp-clocks", (140, 72, 322, 594)),
    "pl-sun":     ("pp-clocks", (14, 28, 112, 120)),
    "pl-scn":     ("pp-clocks", (464, 56, 680, 274)),
}
art_js = OUT / "art.js"
txt = art_js.read_text() if art_js.exists() else ""
m = re.search(r"=\s*(\{.*\})\s*;", txt, re.S)
art = json.loads(m.group(1)) if m else {}
for name, (src, (x0, y0, x1, y1)) in CUTS.items():
    im = Image.open(SRC / f"{src}.png").convert("RGBA").crop((x0 * 3, y0 * 3, x1 * 3, y1 * 3))
    im.save(OUT / f"{name}.webp", quality=88, method=6)
    art[name] = list(im.size)
    print(name, im.size)
art_js.write_text("window.ART = " + json.dumps(art, indent=1) + ";\n")
