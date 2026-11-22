const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
(async()=>{const [mode,arg,out]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(__dirname,process.env.PAGE||'anim.html'));await p.evaluate(()=>window.ready);
const grab=async t=>Buffer.from((await p.evaluate(t=>{draw(t);return document.getElementById('c').toDataURL('image/jpeg',0.93)},t)).split(',')[1],'base64');
if(mode==='stills'){const fs=require('fs');for(const t of arg.split(',').map(Number))fs.writeFileSync(`${out}/s_${t}.jpg`,await grab(t));}
else{const fps=30,dur=Number(arg),N=Math.round(dur*fps);
 const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',out],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<N;i++){const buf=await grab(i/fps);if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300===0)console.log('frame',i,'/',N)}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));}
await b.close();})();
