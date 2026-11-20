// node kit/perf.js file.html [width]  -> load time, scroll jank (4x CPU throttle), widget click tests, errors
const {chromium}=require('playwright');const path=require('path');
(async()=>{const f=path.resolve(process.argv[2]);const W=+(process.argv[3]||1300);
 const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:W,height:850}});const p=await ctx.newPage();
 const errs=[];p.on('pageerror',e=>errs.push('pageerror: '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text())});
 const cdp=await ctx.newCDPSession(p);await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
 const t0=Date.now();await p.goto('file://'+f,{waitUntil:'load',timeout:120000});const load=Date.now()-t0;
 const r=await p.evaluate(async()=>{const H=document.documentElement.scrollHeight;let worst=0,long=0,frames=0;let last=performance.now();
   const t0=performance.now();
   for(let y=0;y<H;y+=400){scrollTo(0,y);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const n=performance.now();const d=n-last;last=n;frames++;if(d>worst)worst=d;if(d>200)long++;}
   return {H,frames,total:Math.round(performance.now()-t0),worst:Math.round(worst),long};});
 // widget tests
 const tests=[];const tryc=async(name,fn)=>{try{await fn();tests.push(name+' ok')}catch(e){tests.push(name+' FAIL '+e.message.split('\n')[0])}};
 await cdp.send('Emulation.setCPUThrottlingRate',{rate:1});
 await tryc('drug btn',async()=>{await p.click('#drug-btns .btn[data-k="dora"]',{timeout:5000});const t=await p.textContent('#drug-out');if(!t.includes('Orexin'))throw new Error('no output')});
 await tryc('hypno btn',async()=>{await p.click('#w-hypno .btn[data-h="old"]',{timeout:5000});});
 await tryc('sim preset',async()=>{await p.click('#w-sim button:has-text("陳伯伯的作息")',{timeout:5000});});
 await tryc('tree',async()=>{await p.click('#tree-box button >> nth=0',{timeout:5000});});
 await tryc('card flip',async()=>{await p.click('.card >> nth=0',{timeout:5000});});
 await tryc('toc link',async()=>{await p.click('nav.toc a[href="#ch13"]',{timeout:5000});});
 console.log(JSON.stringify({load,...r}),'\n'+tests.join('\n'),'\nerrors:',errs);await b.close();})();
