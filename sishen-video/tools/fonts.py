"""Download glyph-subset woff2 files (only the characters the video uses) into public/fonts."""
import re, glob, urllib.parse, subprocess, os
chars = set()
for f in glob.glob("src/**/*.tsx", recursive=True):
    chars |= set(re.findall(r"[^\x00-\x7f]", open(f, encoding="utf8").read()))
chars |= set("0123456789.!?～—…「」・，。！？ ")
text = "".join(sorted(chars)) + "".join(chr(c) for c in range(32, 127))
os.makedirs("public/fonts", exist_ok=True)
for fam, wt, out in [("Huninn", "400", "huninn.woff2"), ("LXGW WenKai TC", "700", "wenkai.woff2")]:
    url = "https://fonts.googleapis.com/css2?family=" + urllib.parse.quote(fam) + f":wght@{wt}&text=" + urllib.parse.quote(text)
    css = subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0 (X11; Linux x86_64) Chrome/120", url], capture_output=True, text=True).stdout
    src = re.search(r"url\((https://[^)]+)\)", css).group(1)
    subprocess.run(["curl", "-sS", "-o", f"public/fonts/{out}", src], check=True)
    print(fam, os.path.getsize(f"public/fonts/{out}"))
