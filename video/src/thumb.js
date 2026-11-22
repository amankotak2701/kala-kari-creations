const {chromium}=require('playwright');const path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(__dirname,'thumb.html'));await p.evaluate(()=>window.ready);
for(const f of ['thumbV','thumbH']){const d=await p.evaluate(f=>{window[f]();return document.getElementById('c').toDataURL('image/png')},f);fs.writeFileSync(f+'.png',Buffer.from(d.split(',')[1],'base64'))}
await b.close()})();
