// ================= "Itsy Bitsy Spider" — Popcorn Productions =================
const SL=4.8, SV=[19.3,57.7,96.1];
const sl=(v,l)=>SV[v]+l*SL;
const SCARD=124.4, SEND=128.0;
const spu=t=>Math.pow(Math.sin(Math.PI*((((t-SV[0])/(SL/8))%1+1)%1)),2);
const PX=650, PTOP=700, PBOT=1630;
const SLYR=['The itsy bitsy spider went up the water spout,','Down came the rain and washed the spider out.','Out came the sun and dried up all the rain,','And the itsy bitsy spider went up the spout again!'];

function itsy(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);if(o.rot)g.rotate(o.rot);
  const walk=o.walk?t*14:0;
  g.strokeStyle='#4C1D95';g.lineWidth=9;g.lineCap='round';
  for(let side of[-1,1])for(let k=0;k<4;k++){const a=Math.sin(walk+k*1.3+(side>0?Math.PI:0))*.25;const bx=side*30,by=-10+k*14-20;
    g.beginPath();g.moveTo(bx,by);const kx=bx+side*(55+k*4),ky=by-40+k*12+a*30;g.quadraticCurveTo(kx,ky-10,bx+side*(85+k*6),by+30+k*8+a*20);g.stroke()}
  ell(0,0,56,48,'#7C3AED');ell(-14,-18,18,12,'rgba(255,255,255,.25)',-.4);
  // face
  ell(-18,-8,16,19,'#FFFFFF');ell(18,-8,16,19,'#FFFFFF');
  if(o.happy){g.strokeStyle='#1F1147';g.lineWidth=5;g.beginPath();g.arc(-18,-6,9,Math.PI*1.1,Math.PI*1.9);g.stroke();g.beginPath();g.arc(18,-6,9,Math.PI*1.1,Math.PI*1.9);g.stroke()}
  else{ell(-15,-5,9,12,'#1F1147');ell(21,-5,9,12,'#1F1147');ell(-12,-9,3,3,'#fff');ell(24,-9,3,3,'#fff')}
  ell(-34,14,9,6,'rgba(249,168,212,.7)');ell(34,14,9,6,'rgba(249,168,212,.7)');
  g.strokeStyle='#F9A8D4';g.lineWidth=4;g.beginPath();if(o.wow)g.arc(0,22,8,0,7);else g.arc(0,16,11,.2,Math.PI-.2);g.stroke();
  // little bow
  g.fillStyle='#F472B6';g.beginPath();g.moveTo(20,-46);g.lineTo(0,-58);g.lineTo(0,-34);g.closePath();g.moveTo(20,-46);g.lineTo(40,-58);g.lineTo(40,-34);g.closePath();g.fill();ell(20,-46,6,6,'#DB2777');
  if(o.wet)for(let k=0;k<4;k++){const p=((t*2+k/4)%1);ell(-40+k*26,40+p*60,5,8,`rgba(96,165,250,${1-p})`)}
  if(o.wave){g.save();g.translate(70,-40);g.rotate(-.8+Math.sin(t*9)*.5);g.strokeStyle='#4C1D95';g.lineWidth=9;g.beginPath();g.moveTo(0,0);g.lineTo(30,-50);g.stroke();g.restore()}
  if(o.umbrella){g.save();g.translate(-10,-60);g.strokeStyle='#374151';g.lineWidth=5;g.beginPath();g.moveTo(0,0);g.lineTo(0,-100);g.stroke();
    if(o.umbrella===2){g.fillStyle='#F59E0B';g.beginPath();g.moveTo(-70,-180+Math.sin(t*20)*8);g.quadraticCurveTo(0,-80,70,-185+Math.cos(t*20)*8);g.lineTo(0,-100);g.closePath();g.fill()}
    else{g.fillStyle='#F59E0B';g.beginPath();g.arc(0,-100,75,Math.PI,0);g.fill();g.fillStyle='#FDE047';g.beginPath();g.moveTo(-75,-100);g.quadraticCurveTo(-38,-170,0,-175);g.quadraticCurveTo(-20,-130,-25,-100);g.fill()}g.restore()}
  g.restore()}
function spoutScene(t,o={}){
  if(o.rain)sky('#64748B','#CBD5E1');else sky('#7DD3FC','#E0F2FE');
  if(o.rainbow){g.save();g.globalAlpha=o.rainbow;['#EF4444','#F97316','#FACC15','#22C55E','#3B82F6','#8B5CF6'].forEach((c,k)=>{g.strokeStyle=c;g.lineWidth=24;g.beginPath();g.arc(260,1350,480-k*24,Math.PI,0);g.stroke()});g.restore()}
  // house wall + roof
  rr(380,560,700,1100,0,'#FDE68A');for(let r=0;r<22;r++)for(let c=0;c<8;c++)rr(380+c*90-(r%2)*45,560+r*50+4,84,42,4,r%2?'#FCD34D':'#FDE68A');
  g.fillStyle='#B91C1C';g.beginPath();g.moveTo(330,580);g.lineTo(720,330);g.lineTo(1110,580);g.fill();rr(330,570,780,24,6,'#991B1B');
  rr(820,880,180,200,10,'#BFE6FF');g.strokeStyle='#fff';g.lineWidth=10;g.strokeRect(820,880,180,200);g.beginPath();g.moveTo(910,880);g.lineTo(910,1080);g.stroke();
  // gutter + spout
  rr(540,620,240,34,12,'#94A3B8');rr(PX-34,PTOP-40,68,PBOT-PTOP+40,20,'#94A3B8');rr(PX-34,PTOP-40,20,PBOT-PTOP+40,10,'rgba(255,255,255,.35)');
  g.fillStyle='#94A3B8';g.beginPath();g.moveTo(PX-34,PBOT-20);g.quadraticCurveTo(PX-34,PBOT+60,PX+60,PBOT+60);g.lineTo(PX+100,PBOT+60);g.lineTo(PX+100,PBOT-8);g.lineTo(PX+60,PBOT-8);g.quadraticCurveTo(PX+34,PBOT-8,PX+34,PBOT-20);g.fill();
  for(let k=0;k<5;k++)rr(PX-40,PTOP+k*200,80,14,6,'#64748B');
  // garden
  g.fillStyle='#4ADE80';g.fillRect(0,1650,W,H-1650);g.fillStyle='#22C55E';g.fillRect(0,1650,W,24);
  for(let k=0;k<7;k++){const fx=40+k*50+((k*37)%40),fy=1580+(k%3)*30;g.strokeStyle='#15803D';g.lineWidth=6;g.beginPath();g.moveTo(fx,1680);g.lineTo(fx,fy);g.stroke();marigold(fx,fy,1.1,['#F472B6','#FBBF24','#F87171','#A78BFA'][k%4])}
  for(let k=0;k<10;k++)marigold(rnd(k+70)*W,1760+rnd(k+71)*140,.8,['#F472B6','#FBBF24','#FFFFFF'][k%3]);
  if(o.puddle>0){ell(PX+170,1720,200*o.puddle,40*o.puddle,'rgba(96,165,250,.75)');ell(PX+150,1712,120*o.puddle,16*o.puddle,'rgba(255,255,255,.5)')}
  if(o.rain){bigCloud(560,560,.9,'#94A3B8');bigCloud(250,640,.6,'#9CA3AF');for(let k=0;k<110;k++){const x=(rnd(k)*W),y=((t*900+rnd(k+3)*1500)%1500)+500;g.strokeStyle='rgba(191,219,254,.85)';g.lineWidth=4;g.beginPath();g.moveTo(x,y);g.lineTo(x-8,y+34);g.stroke()}}
  if(o.gush>0){for(let k=0;k<26;k++){const p=((t*2.2+k/26)%1);ell(PX+100+p*260,PBOT+30+p*p*80,14*o.gush,10*o.gush,'rgba(59,130,246,.75)')}}
}
function ladybug(x,y,s,t){g.save();g.translate(x,y-Math.abs(Math.sin(t*6))*14);g.scale(s,s);ell(0,0,40,32,'#DC2626');g.strokeStyle='#111';g.lineWidth=4;g.beginPath();g.moveTo(0,-30);g.lineTo(0,30);g.stroke();[[-18,-10],[16,-12],[-14,14],[18,12]].forEach(([a,b])=>ell(a,b,7,7,'#111'));ell(36,0,18,16,'#111');ell(42,-4,5,5,'#fff');g.restore()}
function butterfly(x,y,s,t,c='#F472B6'){g.save();g.translate(x,y);g.scale(s,s);const f=Math.abs(Math.sin(t*12));g.save();g.scale(f*.8+.2,1);ell(-30,-14,30,24,c);ell(-24,18,20,16,c);ell(30,-14,30,24,c);ell(24,18,20,16,c);g.restore();rr(-5,-26,10,52,5,'#3F2A1E');g.restore()}
function sptitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#7C3AED';g.beginPath();g.roundRect(-370,-66,740,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Itsy Bitsy Spider 🕷️',0,2,58,'#FFFFFF',null);g.restore()}
const SCAPS=[];SV.forEach(v0=>SLYR.forEach((s,k)=>SCAPS.push([v0+k*SL-.3,v0+(k+1)*SL-.3+(k===3?.6:0),s])));
function spcap(t){const i=SCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=SCAPS[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 60px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*74+40,y0=395;g.fillStyle='rgba(76,29,149,.88)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.9));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+37+li*74,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}

function verseSp(t,v){const L=Math.floor((t-SV[v])/SL);const q=prog(t,sl(v,L),sl(v,L+1));
  const friends=v===2;
  if(L===0){spoutScene(t,{});const y=lerp(PBOT-40,PTOP+120+(v===2?0:200),easeOut(q));itsy(PX,y,1.35,t,{rot:-Math.PI/2*0+0,walk:1,umbrella:v===1?1:0});
    if(friends){ladybug(180,1600,1.35,t);butterfly(260,1250+Math.sin(t*2)*40,1.35,t);pop(t,sl(2,0)+.3,'Go, Itsy, go! 📣',300,1100,58,'#fff','#DB2777')}}
  else if(L===1){spoutScene(t,{rain:1,gush:clamp(q*3),puddle:clamp(q*2)});const sy=lerp(PTOP+(v===2?120:320),PBOT+20,easeOut(clamp(q*1.6-.2)));const sx=q>.55?lerp(PX,PX+260,easeOut(prog(q,.55,1))):PX;
    itsy(sx,sy,1.35,t,{wet:1,wow:1,umbrella:v===1?(q>.25?2:1):0,rot:q>.55?q*4:0});pop(t,sl(v,1)+1.2,v===1?'Oops! ☂️💨':'Whoosh! 💦',540,1050,80,'#fff','#2563EB')}
  else if(L===2){spoutScene(t,{puddle:1-q,rainbow:v===2?q:0});sunFace(220,780,120,t,0);
    for(let k=0;k<6;k++){const p=((t*.8+k/6)%1);g.save();g.globalAlpha=(1-p)*.6*(1-q);g.strokeStyle='#fff';g.lineWidth=6;g.beginPath();g.moveTo(PX+100+k*40,1700-p*150);g.quadraticCurveTo(PX+115+k*40,1670-p*150,PX+100+k*40,1640-p*150);g.stroke();g.restore()}
    itsy(PX+260,1690,1.35,t,{happy:1,wet:q<.5,rot:Math.sin(t*20)*.1*(q<.5?1:0)});pop(t,sl(v,2)+1,'Ahh, warm sun! ☀️',540,1050,66,'#fff','#EA580C')}
  else{spoutScene(t,{rainbow:v===2?1:0});sunFace(220,780,100,t,0);
    const top=v===2;const q2=easeOut(q);const x=q<.15?lerp(PX+260,PX,q/.15):PX;const y=q<.15?1690:lerp(PBOT-40,top?PTOP-60:PTOP+260,easeOut(prog(q,.15,1)));
    itsy(x,y,1.35,t,{walk:1,happy:top&&q>.9});
    if(friends){ladybug(180,1600,1.35,t);butterfly(260,1250+Math.sin(t*2)*40,1.35,t);butterfly(900,1300+Math.cos(t*2)*40,1.25,t,'#60A5FA')}
    pop(t,sl(v,3)+.5,top?'Up, up, up! 💪':'Try again! 💪',540,1050,70,'#fff','#7C3AED')}
}
function drawSpider(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  if(t<SV[0]-.2){ // intro: Itsy drops in on a thread
    spoutScene(t,{});sunFace(220,780,100,t,0);const q=easeOut(prog(t,1,5));const y=lerp(300,1300,q);g.strokeStyle='rgba(255,255,255,.9)';g.lineWidth=3;g.beginPath();g.moveTo(300,300);g.lineTo(300,y);g.stroke();
    if(t<10)itsy(300,y+30,1.4,t,{wave:t>5,happy:1});else{const w=easeOut(prog(t,10,17));itsy(lerp(300,PX,w),lerp(1330,1690,w),1.4,t,{walk:w<1,happy:1})}
    if(t>5)pop(t,5,'Hi! I\'m Itsy! 🕷️',540,1050,70,'#fff','#7C3AED');if(t>12)pop(t,12,'Let\'s climb! 🧗',540,1050,70,'#fff','#16A34A')}
  else if(t<sl(0,4)-.3)verseSp(t,0);
  else if(t<SV[1]-.3){ // interlude 1: web spinning, rainbow, butterflies
    spoutScene(t,{rainbow:clamp((t-sl(0,4))/2)});sunFace(220,780,100,t,0);const q=prog(t,sl(0,4),SV[1]-1);
    const cx=230,cy=1350;g.strokeStyle='rgba(255,255,255,.95)';g.lineWidth=3;const n=Math.floor(q*12);for(let k=0;k<12;k++){const a=k/12*Math.PI*2;if(k<n){g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+Math.cos(a)*170,cy+Math.sin(a)*170);g.stroke()}}
    for(let r=1;r<=Math.floor(q*6);r++){g.beginPath();for(let k=0;k<=12;k++){const a=k/12*Math.PI*2;const rr2=r*26;k?g.lineTo(cx+Math.cos(a)*rr2,cy+Math.sin(a)*rr2):g.moveTo(cx+Math.cos(a)*rr2,cy+Math.sin(a)*rr2)}g.stroke()}
    itsy(cx+Math.cos(t*2)*120*q,cy+Math.sin(t*2)*120*q,.8,t,{walk:1,happy:1});butterfly(820,1250+Math.sin(t*2)*50,1,t);
    pop(t,sl(0,4)+1,'Never give up! 💪',540,1050,70,'#fff','#16A34A');if(t>SV[1]-6)pop(t,SV[1]-6,'This time... an umbrella! ☂️',540,1050,58,'#fff','#F59E0B')}
  else if(t<sl(1,4)-.3)verseSp(t,1);
  else if(t<SV[2]-.3){ // interlude 2: friends arrive and cheer
    spoutScene(t,{});sunFace(220,780,100,t,0);itsy(PX+120,1690-spu(t)*40,1.35,t,{happy:1,wave:1});
    const q=easeOut(prog(t,sl(1,4),sl(1,4)+3));ladybug(lerp(-100,200,q),1640,1.1,t);butterfly(lerp(-100,300,q),1250+Math.sin(t*2)*60,1.1,t);butterfly(lerp(1200,880,q),1300+Math.cos(t*2)*60,1,t,'#60A5FA');
    pop(t,sl(1,4)+1.5,'Friends are here! 🐞🦋',540,1050,64,'#fff','#DB2777');notes(540,1500,t,sl(1,4)+4,5);if(t>SV[2]-6)pop(t,SV[2]-6,'One more try! 🙌',540,1050,70,'#fff','#7C3AED')}
  else if(t<sl(2,4)-.3)verseSp(t,2);
  else{ // finale: Itsy at the top, party, end card
    spoutScene(t,{rainbow:1});sunFace(220,780,100,t,0);
    rr(PX+20,PTOP-230,8,150,4,'#6B7280');g.fillStyle='#22C55E';g.beginPath();g.moveTo(PX+28,PTOP-230);g.lineTo(PX+120+Math.sin(t*5)*8,PTOP-200);g.lineTo(PX+28,PTOP-170);g.fill();
    itsy(PX,PTOP-60-spu(t)*30,1.3,t,{happy:1,wave:1});ladybug(180,1600,1,t);butterfly(260,1250+Math.sin(t*2)*40,1,t);butterfly(900,1300+Math.cos(t*2)*40,.9,t,'#60A5FA');
    confetti(t,sl(2,4),50);pop(t,sl(2,4)+.3,'Made it! 🏁🎉',540,1050,84,'#fff','#16A34A');
    if(t>=SCARD){const q=easeOut(prog(t,SCARD,SCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#3B0764';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
      popcornLogo(W/2,520,.85*backOut(prog(t,SCARD,SCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Never give up! 🕷️💪',W/2,990,72,'#fff','#7C3AED');
      const sp=backOut(prog(t,SCARD+.5,SCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  }
  const cuts=[];SV.forEach(v0=>{for(let k=0;k<=4;k++)cuts.push(v0+k*SL-.3)});cuts.forEach(c=>{const d=Math.abs(t-c);if(d<.15){g.fillStyle=`rgba(255,255,255,${(1-d/.15)*.6})`;g.fillRect(0,0,W,H)}});
  if(t<SCARD){sptitle(t);spcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,SEND-1.2,SEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawSpider;
