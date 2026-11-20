// node kit/visible.js file.html -> loads WITHOUT scrolling, counts blocks that are invisible (opacity 0)
const {chromium,webkit}=require('playwright');const path=require('path');
(async()=>{for(const [name,bt] of [['chromium',chromium],['webkit',webkit]]){let b;try{b=await bt.launch()}catch(e){console.log(name,'n/a');continue}
 const p=await b.newPage({viewport:{width:390,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+path.resolve(process.argv[2]),{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
 const r=await p.evaluate(()=>{const all=[...document.querySelectorAll('.box,figure,.widget,.tw,.two')];return {blocks:all.length,hidden:all.filter(e=>getComputedStyle(e).opacity==='0').length}});
 console.log(name,JSON.stringify(r),'errors:',errs);await b.close();}})();
