const {chromium}=require('playwright');const path=require('path'),fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+path.resolve(__dirname,'omthumb_V.html'));await p.evaluate(()=>window.ready);
const d=await p.evaluate(()=>{window.makeS();return document.getElementById('c').toDataURL('image/png')});fs.writeFileSync('omS.png',Buffer.from(d.split(',')[1],'base64'));await b.close()})();
