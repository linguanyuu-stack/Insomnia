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
# heavy plates: no fade-in transform (re-rasterises big SVGs while scrolling)
# The fade-in hid every box/figure/table (opacity 0) until an IntersectionObserver fired. In in-app
# previews / some phone viewers it never fires -> large parts of the book looked blank/unfinished.
# Remove the effect so content is always visible; guard the TOC observer so a missing API can't
# stop the rest of the script (all the widgets) from running.
sub1("const rv=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');rv.unobserve(e.target);}}),{rootMargin:'0px 0px -8% 0px'});\n", "")
sub1("$$('.box,figure,.widget,.tw,.two').forEach(x=>{x.classList.add('reveal');rv.observe(x);});\n", "")
sub1("const io=new IntersectionObserver(", "const io=('IntersectionObserver' in window)?new IntersectionObserver(")
sub1("{rootMargin:'-30% 0px -60% 0px'});", "{rootMargin:'-30% 0px -60% 0px'}):{observe(){}};")
sub1('</style>', open(P('kit/plate.css'), encoding='utf-8').read() + '\n</style>')
sub1('<div class="shell">', '<div class="shell">\n' + open(P('kit/defs.svg'), encoding='utf-8').read())

# ---------- plates ----------
CIRC = re.compile(r'<circle\s+([^>]*?)/?>(?:</circle>)?')
def _merge_circles(m):
    items = []
    for c in CIRC.finditer(m.group(0)):
        a = dict(re.findall(r'([\w:-]+)=["\']([^"\']*)["\']', c.group(1)))
        if not {'cx','cy','r'} <= a.keys() or 'id' in a or 'class' in a and 'transform' in a: return m.group(0)
        geo = (float(a.pop('cx')), float(a.pop('cy')), float(a.pop('r')))
        items.append((tuple(sorted(a.items())), geo))
    out = []; i = 0
    while i < len(items):
        j = i
        while j < len(items) and items[j][0] == items[i][0]: j += 1
        attrs = ' '.join(f'{k}="{v}"' for k, v in items[i][0])
        A = dict(items[i][0]); rs = {geo[2] for _, geo in items[i:j]}
        if j - i >= 4 and len(rs) == 1 and A.get('fill', 'none') not in ('none', '') and A.get('stroke', 'none') == 'none' and not ({'fill-rule', 'stroke-width', 'opacity'} & A.keys()):
            # compact dots: zero-length round-capped strokes
            r = rs.pop(); g = lambda v: f'{round(v, 1):g}'
            B = {k: v for k, v in A.items() if k not in ('fill', 'stroke', 'fill-opacity')}
            B.update({'fill': 'none', 'stroke': A['fill'], 'stroke-width': f'{round(2*r, 2):g}', 'stroke-linecap': 'round'})
            if 'fill-opacity' in A: B['stroke-opacity'] = A['fill-opacity']
            d = ''.join(f'M{g(x)} {g(y)}h0' for _, (x, y, _r) in items[i:j])
            out.append('<path ' + ' '.join(f'{k}="{v}"' for k, v in B.items()) + f' d="{d}"/>')
        elif j - i >= 4:
            g = lambda v: f'{round(v, 2):g}'
            d = ''.join(f'M{g(x-r)} {g(y)}a{g(r)} {g(r)} 0 1 0 {g(2*r)} 0a{g(r)} {g(r)} 0 1 0 {g(-2*r)} 0' for _, (x, y, r) in items[i:j])
            out.append(f'<path {attrs} d="{d}"/>')
        else:
            for _, (x, y, r) in items[i:j]:
                out.append(f'<circle {attrs} cx="{x:g}" cy="{y:g}" r="{r:g}"/>')
        i = j
    return ''.join(out)
def slim(t):
    # 1) drop the turbulence 'hand-inked' filter: very slow to paint on phones / Safari
    t = re.sub(r'\s*filter="url\(#ink-rough\)"', '', t)
    # 2) round coordinates to 1 decimal
    num = re.compile(r'(?<![\w#.])-?\d*\.\d{2,}')
    rnd = lambda m: ('%.1f' % float(m.group(0))).replace('-0.0', '0.0')
    t = re.sub(r'\b(d|points|transform|x|y|x1|y1|x2|y2|cx|cy|width|height)=(["\'])([^"\']*)\2',
               lambda m: f'{m.group(1)}={m.group(2)}{num.sub(rnd, m.group(3))}{m.group(2)}', t)
    # 3) merge runs of plain dot circles (stipple / papillae) into single paths
    t = re.sub(r'(?:<circle\s[^>]*?/?>(?:</circle>)?\s*){4,}', _merge_circles, t)
    return t

# The Claude app's file preview only shows the first ~1 MB of a file. Raw plates are ~2.5 MB, so
# each plate is stored deflate-compressed (base64) and unpacked in the browser on load
# (DecompressionStream: Chrome 80+, Safari 16.4+, Firefox 113+). Set PLATES_RAW=1 for an uncompressed build.
import zlib, base64, html as _html
COMPRESS = os.environ.get('PLATES_RAW') != '1'
def pack(pid, snip):
    if not COMPRESS:
        return snip
    snip = re.sub(r'>\s+<', '><', snip)
    z = base64.b64encode(zlib.compress(snip.encode('utf-8'), 9)).decode()
    t = re.search(r'<span class="ptt">(.*?)</span>', snip)
    title = re.sub('<[^>]+>', '', t.group(1)) if t else ''
    return f'<div class="plate-z" data-id="{pid}" data-z="{z}">圖版載入中：{_html.escape(title)}…</div>'
if COMPRESS:
    sub1('</head>', """<style>.plate-z{margin:26px 0;padding:40px 16px;border:1px dashed #cdbf9f;border-radius:6px;background:#fbf6ea;color:#8a6a3a;text-align:center;font-size:14px}</style>
<script>
document.addEventListener('DOMContentLoaded',function(){
  var els=document.querySelectorAll('.plate-z');
  if(!('DecompressionStream' in window)){els.forEach(function(el){el.textContent='（這個瀏覽器太舊，無法顯示圖版，請用新版 Chrome 或 Safari 開啟）';});return;}
  // decompress everything first, then swap all plates in a single frame (one layout instead of 26)
  var jobs=Array.prototype.map.call(els,function(el){
    try{
      var b=atob(el.getAttribute('data-z')),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);
      return new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('deflate'))).text().catch(function(){return null;});
    }catch(e){return Promise.resolve(null);}
  });
  Promise.all(jobs).then(function(ts){requestAnimationFrame(function(){
    var y=window.scrollY,anchor=null;
    ts.forEach(function(t,i){if(t)els[i].outerHTML=t;else els[i].textContent='（圖版解壓失敗）';});
    if(location.hash){var h=document.getElementById(location.hash.slice(1));if(h)h.scrollIntoView();}
  });});
});
</script>
</head>""")

# (plate id, anchor text that must occur exactly once, 'before'|'after')
from placements import PLACEMENTS
missing = []
for pid, anchor, where in PLACEMENTS:
    f = P('figs', pid + '.html')
    if not os.path.exists(f):
        missing.append(pid); continue
    snip = open(f, encoding='utf-8').read().strip()
    snip = re.sub(r'^<!--.*?-->\s*', '', snip, flags=re.S)
    snip = slim(snip)
    n = s.count(anchor)
    if n != 1:
        sys.exit(f'{pid}: anchor found {n}x: {anchor[:80]!r}')
    i = s.index(anchor)
    if where == 'after':
        i += len(anchor)
    s = s[:i] + '\n' + pack(pid, snip) + '\n' + s[i:]

out = P('重新認識失眠_圖解版.html')
open(out, 'w', encoding='utf-8').write(s)
size = len(s.encode('utf-8'))
print('wrote', out, size // 1024, 'KB', '| missing plates:', missing or 'none')
if COMPRESS and size > 950_000:
    sys.exit('WARNING: over ~950 KB - the Claude app preview truncates around 1 MB')
