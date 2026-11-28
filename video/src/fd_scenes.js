// ================= "The Farmer in the Dell" — Popcorn Productions =================
const DFL=2.0, DV0=8.35;
const dv=k=>DV0+(k>>1)*20+(k&1)*8;
const DCARD=106.6, DEND=111.1;
const DWHO=['farmer','wife','child','nurse','cow','dog','cat','mouse','cheese'];
const DEMO=['👨‍🌾','👩','🧒','👩‍⚕️','🐄','🐶','🐱','🐭','🧀'];
const DLINES=k=>{if(k===0)return['The farmer in the dell,','The farmer in the dell,','Hi-ho, the derry-o,','The farmer in the dell!'];
  if(k===9)return['The cheese stands alone,','The cheese stands alone,','Hi-ho, the derry-o,','The cheese stands alone!'];
  const s=`The ${DWHO[k-1]} takes the ${DWHO[k]},`;return[s,s,'Hi-ho, the derry-o,',s.replace(/,$/,'!')]};
const DCAPS=[];for(let k=0;k<10;k++)DLINES(k).forEach((s,l)=>DCAPS.push([dv(k)+l*DFL-.25,dv(k)+(l+1)*DFL-.25+(l===3?.5:0),s]));
const fInVerse=t=>{for(let k=0;k<10;k++)if(t>=dv(k)-.25&&t<dv(k)+4*DFL-.25)return k;return -1};
const fhop=t=>Math.abs(Math.sin(Math.PI*(t-.355)/.5));

function member(i,x,y,t,o={}){const h=o.hop||0,d=o.dir||1,s=o.s||1;
  if(i===0)farmer(x,y-h,.72*s,t,{dir:d,pose:o.pose||'sway'});
  else if(i===1)adult('mom',x,y-h,{s:.7*s,t,pose:o.pose||'sway',happy:1,dir:d});
  else if(i===2)kid(3,x,y-h,{s:.8*s,t,happy:1,noHat:1,noScarf:1,dir:d,trunk:o.pose==='up'?1:.5});
  else if(i===3)nurseP(x,y-h,.7*s,t,{dir:d,pose:o.pose||'sway'});
  else if(i===4)cow(x,y-h,.62*s,t,{dir:d,walk:o.walk});
  else if(i===5){g.save();g.translate(x,0);g.scale(d,1);puppy(-70*s,y,1.15*s,t,h);g.restore()}
  else if(i===6)kitty(x,y,1.15*s,t,{dir:d,hop:h});
  else if(i===7)mouseC(x,y,1.45*s,t,{dir:d,hop:h});
  else cheese(x,y-h,.95*s,t,{face:1,sad:o.sad,wobble:1})}
function ring(t,front,spd=.6){for(let j=0;j<6;j++){const a=t*spd+j*Math.PI/3,sn=Math.sin(a);if((sn>0)!==front)continue;if(front&&Math.abs(Math.cos(a))<.6)continue;
  const x=540+Math.cos(a)*440,y=1640+sn*120,sc=.5+sn*.08;kid(j,x,y-fhop(t)*14,{s:sc,t,happy:1,noHat:1,noScarf:1,trunk:1,dir:Math.cos(a)>0?-1:1})}}
function dell(t){farmBg(t);ell(540,1680,520,150,'rgba(255,255,255,.25)')}
function chain(t,n){ // collected members strip below the caption
  const w=108,x0=540-(n-1)*w/2;for(let i=0;i<n;i++){const p=backOut(prog(t,dv(i)+.2,dv(i)+.8));g.save();g.translate(x0+i*w,560);g.scale(p,p);ell(0,0,50,50,'rgba(255,255,255,.95)');g.lineWidth=6;g.strokeStyle='#16A34A';g.beginPath();g.arc(0,0,50,0,7);g.stroke();txt(DEMO[i],0,4,58,null,null);g.restore()}}
function fdtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#16A34A';g.beginPath();g.roundRect(-360,-66,720,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('The Farmer in the Dell 👨‍🌾',0,2,54,'#FFFFFF',null);g.restore()}
function fdcap(t){const i=DCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=DCAPS[i];
  const al=Math.min(clamp((t-a)/.12),clamp((b-t)/.12));g.save();g.globalAlpha=al;let fs=64;g.font=`700 ${fs}px Fredoka, Baloo2`;let w=g.measureText(s).width;
  if(w>920){fs=Math.floor(fs*920/w);g.font=`700 ${fs}px Fredoka, Baloo2`;w=g.measureText(s).width}
  const h=120,y0=395;g.fillStyle='rgba(21,128,61,.92)';g.beginPath();g.roundRect(W/2-w/2-45,y0-h/2,w+90,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/(DFL*.9));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}

function drawDell(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const k=fInVerse(t);let nChain=0;
  g.save();g.translate(540,1700);g.scale(1.25,1.25);g.translate(-540,-1680);dell(t);
  if(k>=0){const v=dv(k),L=Math.floor((t-v+.25)/DFL),hop=L===2?fhop(t)*40:0;nChain=Math.min(k+1,9);
    ring(t,false,L===2?1.2:.6);
    if(k===0){member(0,540,1720,t,{pose:L===2?'up':'wave',hop});pop(t,v+.2,'Hello, Farmer! 👋',540,1180,64,'#fff','#16A34A')}
    else if(k<9){const A=k-1,B=k;const q=easeOut(prog(t,v,v+1.6));
      member(A,400,1720,t,{pose:L>=1?'up':'sway',hop});member(B,lerp(1200,690,q),1720,t,{dir:-1,hop:L===2?fhop(t+.25)*40:0,walk:q<1,pose:L>=1?'up':'sway'});
      if(L===1||L===3){for(let j=0;j<5;j++){const p=((t*.7+j/5)%1);g.save();g.globalAlpha=1-p;txt('♥',545+Math.sin(j*2.2)*90,1380-p*220,46,'#F472B6',null);g.restore()}}
      pop(t,v+.3,`Here comes the ${DWHO[B]}! ${DEMO[B]}`,540,1180,58,'#fff','#16A34A');if(L===2)pop(t,v+2*DFL+.1,'Hi-ho! 🎶',540,1180,72,'#fff','#EA580C')}
    else{const sad=L<3;cheese(540,1720,1.25,t,{face:1,sad,wobble:1});if(sad)pop(t,v+.3,'All alone... 🥺',540,1180,62,'#fff','#2563EB');else pop(t,v+3*DFL+.1,'Wait for us! 💛',540,1180,62,'#fff','#DB2777')}
    ring(t,true,L===2?1.2:.6)}
  else if(t<dv(0)-.25){ring(t,false);const q=easeOut(prog(t,1,6));member(0,lerp(-200,540,q),1720,t,{pose:'wave'});ring(t,true);pop(t,2,'Let\'s play a circle game! 🎶',540,1180,56,'#fff','#16A34A')}
  else if(t<dv(9)){ // music break after each pair: everyone collected dances in a line
    const n=Math.min(9,[1,3,5,7].find(m=>t<dv(m+1))+1);nChain=n;ring(t,false,1.3);
    const sp=Math.min(130,820/Math.max(1,n-1));for(let i=0;i<n;i++)member(i,540-(n-1)*sp/2+i*sp,1720,t,{s:.85,hop:fhop(t+i*.12)*40,pose:'up'});ring(t,true,1.3);
    for(let j=0;j<6;j++){const p=((t*.5+j/6)%1);g.save();g.globalAlpha=1-p;txt(j%2?'♫':'♪',240+j*120,1300-p*260,58,['#FDE047','#F472B6','#60A5FA'][j%3],null);g.restore()}
    const bs=[1,3,5,7].map(m=>dv(m)+8).filter(b=>b<=t).pop();pop(t,bs+.1,'Dance break! 💃',540,1180,64,'#fff','#7C3AED')}
  else{ // happy ending: everyone hugs the cheese
    nChain=9;ring(t,false,.8);const n=8,sp=110;for(let i=0;i<n;i++){const x=540+(i<4?-1:1)*(150+(i%4)*sp);member(i,x,1720,t,{s:.8,hop:fhop(t+i*.1)*30,pose:'up',dir:i<4?1:-1})}
    cheese(540,1720,.95,t,{face:1,wobble:1});for(let j=0;j<6;j++){const p=((t*.6+j/6)%1);g.save();g.globalAlpha=1-p;txt('♥',540+Math.sin(j*2.2)*160,1450-p*260,52,'#F472B6',null);g.restore()}
    ring(t,true,.8);pop(t,dv(9)+8,'Not alone anymore! 🧀💛',540,1180,58,'#fff','#DB2777');confetti(t,dv(9)+8,60)}
  g.restore();
  if(t<DCARD)chain(t,nChain);
  if(t>=DCARD){const q=easeOut(prog(t,DCARD,DCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#14532D';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,DCARD,DCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Hi-ho, the derry-o! 🎶',W/2,990,64,'#fff','#16A34A');
    const sp=backOut(prog(t,DCARD+.5,DCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<DCARD){fdtitle(t);fdcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,DEND-1.2,DEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawDell;
