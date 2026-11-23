const {chromium}=require('playwright');const path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+path.resolve(__dirname,'plthumb.html'));await p.evaluate(()=>window.ready);
const d=await p.evaluate(()=>{window.makeP();return document.getElementById('c').toDataURL('image/png')});fs.writeFileSync('plthumb.png',Buffer.from(d.split(',')[1],'base64'));await b.close()})();
