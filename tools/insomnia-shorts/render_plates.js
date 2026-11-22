// Render the public edition's plates (figs_public/pp-*.html) as their bare SVG, labels hidden, at 3x, for cutting into
// pieces for the shorts: node tools/insomnia-shorts/render_plates.js pp-mimosa pp-cave ...
const {chromium}=require('playwright'); const fs=require('fs'),path=require('path');
(async()=>{
  const root=path.resolve(__dirname,'..','..');
  const orig=fs.readFileSync(path.join(root,'original.html'),'utf8');
  const css=orig.match(/<style>([\s\S]*?)<\/style>/)[1]+fs.readFileSync(path.join(root,'kit/plate.css'),'utf8');
  const defs=fs.readFileSync(path.join(root,'kit/defs.svg'),'utf8');
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:840,height:900},deviceScaleFactor:3});
  for(const id of process.argv.slice(2)){
    const snip=fs.readFileSync(path.join(root,'figs_public',id+'.html'),'utf8');
    await p.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>${css} text,.ld{display:none}</style></head><body style="background:transparent;margin:0"><div style="width:780px;margin:0">${defs}${snip}</div></body></html>`);
    await p.waitForTimeout(300);
    const svg=await p.$('figure svg'); const vb=await svg.evaluate(s=>[s.viewBox.baseVal.width,s.getBoundingClientRect().width]);
    await svg.screenshot({path:path.join(root,'books/insomnia-shorts/art/plates',id+'.png'),omitBackground:true});
    console.log(id,'viewBox w',vb[0],'css w',vb[1].toFixed(1));
  }
  await b.close();
})();
