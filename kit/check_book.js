// node kit/check_book.js [outdir] [width]  -> screenshots every figure.plate in the built book, reports text overlaps & JS errors
const {chromium}=require('playwright');const path=require('path');
(async()=>{
  const out=process.argv[2]||'/tmp/book_shots', W=+(process.argv[3]||1300);
  require('fs').mkdirSync(out,{recursive:true});
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:W,height:900}});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto('file://'+path.resolve(__dirname,'..','重新認識失眠_圖解版.html'));
  await p.addStyleTag({content:'.reveal{opacity:1!important;transform:none!important}'});await p.waitForTimeout(800);
  const rep=await p.evaluate(()=>{const res=[];
    document.querySelectorAll('figure.plate').forEach(f=>{const svg=f.querySelector(':scope > svg');const sb=svg.getBoundingClientRect();
      const ts=[...svg.querySelectorAll('text')].filter(t=>t.textContent.trim()&&!t.closest('defs,symbol')).map(t=>({t:t.textContent.trim().slice(0,20),r:t.getBoundingClientRect()})).filter(a=>a.r.width>0);
      let n=0;for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){const A=ts[i].r,B=ts[j].r;
        if(Math.min(A.right,B.right)-Math.max(A.left,B.left)>1.5&&Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top)>0.35*Math.min(A.height,B.height)){n++;if(n<4)res.push(f.id+' OVERLAP "'+ts[i].t+'" <> "'+ts[j].t+'"');}}
      res.push(f.id+': '+Math.round(sb.width)+'x'+Math.round(sb.height)+' texts='+ts.length+' overlaps='+n);});
    res.push('page scrollWidth='+document.documentElement.scrollWidth+' innerWidth='+innerWidth);return res;});
  console.log(rep.join('\n'));console.log('errors:',errs);
  const figs=await p.$$('figure.plate');let i=0;for(const f of figs){i++;const id=await f.getAttribute('id');await f.screenshot({path:`${out}/${String(i).padStart(2,'0')}_${id}.png`});}
  await b.close();})();
