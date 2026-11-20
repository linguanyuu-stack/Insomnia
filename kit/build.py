#!/usr/bin/env python3
"""Build the illustrated book: original.html + kit/plate.css + kit/defs.svg + figs/*.html -> 重新認識失眠_圖解版.html"""
import re, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
s = open(P('original.html'), encoding='utf-8').read()

def sub1(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'patch anchor found {n}x: {old[:80]!r}')
    s = s.replace(old, new)

# ---------- fixes to existing figures (label/graphic collisions) ----------
# simulator: threshold labels were crossed by the dashed threshold curves -> halo + lift
sub1("el('text',{x:X(t0)+4,y:Y(P.H0+Cc(t0,adv))-8,fill:'#a8412c'},svg,'上門檻：壓力碰到就睡著');",
     "let tm=t0;for(let t=t0;t<=t0+20;t+=.25){if(Cc(t,adv)>Cc(tm,adv))tm=t;}el('text',{x:X(tm),y:Y(P.H0+Cc(tm,adv))-10,fill:'#a8412c','stroke':'#fff','stroke-width':5,'paint-order':'stroke','stroke-linejoin':'round','text-anchor':'middle'},svg,'上門檻：壓力碰到就睡著');")
sub1("el('text',{x:X(t0)+4,y:Y(P.L0+Cc(t0,adv))-8,fill:'#2c5d9c'},svg,'下門檻：壓力降到就醒來');",
     "el('text',{x:X(tm),y:Y(P.L0+Cc(tm,adv))-10,fill:'#2c5d9c','stroke':'#fff','stroke-width':5,'paint-order':'stroke','stroke-linejoin':'round','text-anchor':'middle'},svg,'下門檻：壓力降到就醒來');")
# drug explorer: 'GABA・galanin' spilled out of the VLPO circle -> bigger circles for sleep side
sub1("else el('circle',{cx:x,cy:y,r:32,", "else el('circle',{cx:x,cy:y,r:(id==='VLPO'||id==='SCN')?42:32,")
sub1("el('path',{d:'M370 130 C 420 120 450 125 556 135'", "el('path',{d:'M370 130 C 420 120 450 125 546 132'")
sub1("el('path',{d:'M556 155 C 450 170 420 170 370 160'", "el('path',{d:'M546 152 C 450 170 420 170 370 160'")
sub1("el('text',{x:590,y:190,'text-anchor':'middle',fill:'#a8412c','font-weight':700},svg,'↑ 抑制作用被加強');",
     "el('text',{x:590,y:86,'text-anchor':'middle',fill:'#a8412c','font-weight':700},svg,'↑ 抑制作用被加強');")
sub1("VLPO:[590,140,'VLPO','GABA・galanin']", "VLPO:[590,140,'VLPO','GABA・甘丙肽']")
sub1("SCN:[590,235,'SCN','生理時鐘']", "SCN:[590,240,'SCN','生理時鐘']")

# ---------- CSS + shared defs ----------
sub1('</style>', open(P('kit/plate.css'), encoding='utf-8').read() + '\n</style>')
sub1('<div class="shell">', '<div class="shell">\n' + open(P('kit/defs.svg'), encoding='utf-8').read())

# ---------- plates ----------
# (plate id, anchor text that must occur exactly once, 'before'|'after')
from placements import PLACEMENTS
missing = []
for pid, anchor, where in PLACEMENTS:
    f = P('figs', pid + '.html')
    if not os.path.exists(f):
        missing.append(pid); continue
    snip = open(f, encoding='utf-8').read().strip()
    snip = re.sub(r'^<!--.*?-->\s*', '', snip, flags=re.S)
    n = s.count(anchor)
    if n != 1:
        sys.exit(f'{pid}: anchor found {n}x: {anchor[:80]!r}')
    i = s.index(anchor)
    if where == 'after':
        i += len(anchor)
    s = s[:i] + '\n' + snip + '\n' + s[i:]

# reveal animation: plates should also fade in like other figures (already covered by 'figure' selector)
out = P('重新認識失眠_圖解版.html')
open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, len(s)//1024, 'KB', '| missing plates:', missing or 'none')
