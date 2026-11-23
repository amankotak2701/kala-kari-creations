const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+path.resolve(__dirname,process.argv[2]));await p.evaluate(()=>window.ready);
for(const t of [3,10,20,32,40,60,80,90,100,110,125,138]){try{await p.evaluate(t=>draw(t),t)}catch(e){console.log('t',t,e.message)}}console.log('ok');await b.close()})();
