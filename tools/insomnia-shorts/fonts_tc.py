"""Copy the Noto Sans TC chunks (fontsource, OFL) that cover the series' Chinese text into site/insomnia-shorts/lib/fonts/
and write lib/fonts-tc.css with their @font-face rules. Rerun after the text changes.

    npm pack @fontsource/noto-sans-tc   (unpacked into DIR)
    python3 tools/insomnia-shorts/fonts_tc.py DIR/package
"""
import re, shutil, sys
from pathlib import Path

PKG = Path(sys.argv[1]); SITE = Path("site/insomnia-shorts"); OUT = SITE / "lib/fonts"
WEIGHTS = ["500", "600"]
text = "".join(p.read_text() for p in list(SITE.glob("ch*/index.html")) + list(SITE.glob("ch*/audio/*/timings.js")) +
               [SITE / "lib/insomnia.js", SITE / "lib/engine.js", SITE / "lib/contents.js"] if p.exists())
need = {ord(c) for c in text if ord(c) > 0x2E7F}


def ranges(s):
    out = []
    for part in s.split(","):
        a, _, b = part.strip()[2:].partition("-")
        out.append((int(a, 16), int(b or a, 16)))
    return out


css, files = ["/* Noto Sans TC (SIL Open Font License 1.1), from fontsource: only the chunks this series' text uses */"], set()
for w in WEIGHTS:
    src = (PKG / f"{w}.css").read_text()
    for block in re.findall(r"@font-face\s*\{[^}]*\}", src):
        rng = re.search(r"unicode-range:\s*([^;]+);", block).group(1)
        rs = ranges(rng)
        if not any(a <= c <= b for c in need for a, b in rs): continue
        f = re.search(r"url\(\./files/([^)]+\.woff2)\)", block).group(1)
        shutil.copy(PKG / "files" / f, OUT / f); files.add(f)
        css.append(f"@font-face {{\n  font-family: 'Noto Sans TC';\n  font-style: normal;\n  font-weight: {w};\n  font-display: block;\n"
                   f"  src: url(../lib/fonts/{f}) format('woff2');\n  unicode-range: {rng};\n}}")
(SITE / "lib/fonts-tc.css").write_text("\n".join(css) + "\n")
shutil.copy(PKG / "LICENSE", OUT / "OFL-NotoSansTC.txt")
print(len(need), "characters,", len(files), "chunk files,", sum((OUT / f).stat().st_size for f in files) // 1024, "KiB")
