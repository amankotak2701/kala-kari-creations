const {chromium}=require('playwright');const path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch();
for(const [o,w,h] of [['H',1280,720],['V',1080,1920]]){const p=await b.newPage({viewport:{width:w,height:h}});
 await p.goto('file://'+path.resolve(__dirname,`marythumb_${o}.html`));await p.evaluate(()=>window.ready);
 const d=await p.evaluate(o=>{window['make'+o]();return document.getElementById('c').toDataURL('image/png')},o);fs.writeFileSync(`marythumb_${o}.png`,Buffer.from(d.split(',')[1],'base64'))}
await b.close()})();
