// Usage: node kit/render_fig.js figs/pl-xxx.html [out.png]
// Wraps a <figure class="plate"> snippet with the book's CSS + shared defs, renders at the
// book's column width (780px) at 2x, saves PNG, and reports overlapping / clipped text.
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path');
(async()=>{
  const root=path.resolve(__dirname,'..');
  const file=process.argv[2]; const out=process.argv[3]||file.replace(/\.html$/,'.png');
  const orig=fs.readFileSync(path.join(root,'original.html'),'utf8');
  const css=orig.match(/<style>([\s\S]*?)<\/style>/)[1]+fs.readFileSync(path.join(root,'kit/plate.css'),'utf8');
  const defs=fs.readFileSync(path.join(root,'kit/defs.svg'),'utf8');
  const snip=fs.readFileSync(file,'utf8');
  const html=`<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body style="background:#f6f1e7"><div style="width:780px;margin:20px">${defs}${snip}</div></body></html>`;
  const tmp=path.join(root,'kit','_tmp_'+path.basename(file));
  fs.writeFileSync(tmp,html);
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:840,height:900},deviceScaleFactor:2});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+tmp); await p.waitForTimeout(300);
  const fig=await p.$('figure'); await fig.screenshot({path:out});
  const rep=await p.evaluate(()=>{
    const res=[];
    document.querySelectorAll('figure > svg, figure > div > svg').forEach(svg=>{
      const sb=svg.getBoundingClientRect();
      const ts=[...svg.querySelectorAll('text')].filter(t=>t.textContent.trim()).map(t=>({t:t.textContent.trim().slice(0,24),r:t.getBoundingClientRect()}));
      for(const a of ts){ if(a.r.left<sb.left-1||a.r.right>sb.right+1||a.r.top<sb.top-1||a.r.bottom>sb.bottom+1) res.push('CLIPPED: "'+a.t+'"'); }
      for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){const A=ts[i].r,B=ts[j].r;
        const ox=Math.min(A.right,B.right)-Math.max(A.left,B.left), oy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);
        if(ox>1.5&&oy>2) res.push('OVERLAP: "'+ts[i].t+'" <> "'+ts[j].t+'"');}
      const vb=svg.viewBox.baseVal; res.push(`svg viewBox ${vb.width}x${vb.height}, rendered ${Math.round(sb.width)}x${Math.round(sb.height)}px, ${ts.length} text nodes, scale ${(sb.width/vb.width).toFixed(2)}`);
    });
    return res;});
  console.log(rep.join('\n')); if(errs.length) console.log('PAGE ERRORS:',errs);
  fs.unlinkSync(tmp); await b.close(); console.log('saved',out);
})();
