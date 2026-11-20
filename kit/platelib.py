import re, os
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
