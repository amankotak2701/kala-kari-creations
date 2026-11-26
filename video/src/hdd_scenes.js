// ================= "Hickory Dickory Dock" (animal version) — Popcorn Productions =================
const HL=2.125, HB=HL/4, HV0=4.5, HPER=18.06;          // 1 lyric line = 1 bar
const hv=k=>HV0+k*HPER, hl=(v,l)=>hv(v)+l*HL;
const HOUT=hv(6), HOUTEND=122.6, HCARD=122.8, HEND=128.5;
const hpu=t=>Math.pow(Math.sin(Math.PI*((((t-HV0)/HB)%1+1)%1)),2);
const CX=540, FACEY=860, FACER=165;
const HANI=[
 {n:'mouse',a:'The mouse ran up the clock.',b:'The clock struck one, the mouse ran down.'},
 {n:'bird',a:'The bird looked at the clock.',b:'The clock struck two, away she flew.'},
 {n:'dog',a:'The dog barked at the clock.',b:'The clock struck three, fiddle-dee-dee!'},
 {n:'bear',a:'The bear slept by the clock.',b:'The clock struck four, he ran out the door.'},
 {n:'bee',a:'The bee buzzed round the clock.',b:'The clock struck five, she went to her hive.'},
 {n:'hen',a:'The hen pecked at the clock.',b:'The clock struck six, oh fiddlesticks!'}];

// ---------- animals ----------
function mouse(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);if(o.rot)g.rotate(o.rot);const C='#9CA3AF';
  g.strokeStyle='#F9A8D4';g.lineWidth=6;g.beginPath();g.moveTo(-60,-30);g.quadraticCurveTo(-120,-40+Math.sin(t*8)*20,-130,-90);g.stroke();
  ell(0,-40,62,40,C);rr(-30,-12,14,16,4,'#F9A8D4');rr(20,-12,14,16,4,'#F9A8D4');
  ell(50,-75,30,30,C);ell(80,-58,22,16,C);ell(98,-60,8,7,'#F472B6');ell(38,-108,24,24,C);ell(38,-108,14,14,'#F9A8D4');ell(62,-110,18,18,C);ell(62,-110,10,10,'#F9A8D4');
  ell(64,-78,6,8,'#111');ell(66,-81,2,2,'#fff');g.strokeStyle='#4B5563';g.lineWidth=2;for(let k=-1;k<=1;k++){g.beginPath();g.moveTo(92,-58);g.lineTo(122,-60+k*10);g.stroke()}
  g.restore()}
function birdie(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);const fl=o.fly?Math.sin(t*20)*.8:Math.sin(t*3)*.1;
  ell(0,-40,46,38,'#3B82F6');ell(10,-28,30,22,'#BFDBFE');ell(40,-70,28,26,'#3B82F6');g.fillStyle='#F59E0B';g.beginPath();g.moveTo(64,-74);g.lineTo(88,-68);g.lineTo(64,-62);g.fill();
  ell(48,-76,6,7,'#111');ell(50,-79,2,2,'#fff');g.save();g.translate(-5,-50);g.rotate(-.4-fl);ell(-20,-10,36,16,'#2563EB',-.3);g.restore();
  g.fillStyle='#1D4ED8';g.beginPath();g.moveTo(-40,-40);g.lineTo(-80,-60);g.lineTo(-76,-30);g.fill();if(!o.fly){rr(-4,-6,4,10,2,'#F59E0B');rr(10,-6,4,10,2,'#F59E0B')}g.restore()}
function bear(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);const B='#92400E',L='#D6A065';
  const run=o.run?Math.sin(t*14)*.4:0;
  if(o.sleep){ell(0,-80,140,85,B);ell(10,-60,80,45,L);ell(110,-120,70,64,B);ell(70,-175,24,24,B);ell(150,-175,24,24,B);ell(150,-100,30,24,L);ell(160,-110,10,8,'#2A1A1A');
    g.strokeStyle='#2A1A1A';g.lineWidth=5;g.beginPath();g.arc(100,-130,10,Math.PI*.15,Math.PI*.85);g.stroke();g.beginPath();g.arc(135,-132,10,Math.PI*.15,Math.PI*.85);g.stroke();ell(-60,-10,40,22,B);ell(70,-10,40,22,B)}
  else{[[-40,run],[40,-run]].forEach(([lx,a])=>{g.save();g.translate(lx,-80);g.rotate(a);rr(-24,0,48,80,20,B);g.restore()});
    ell(0,-170,90,100,B);ell(0,-150,55,65,L);[[-1],[1]].forEach(([d])=>{g.save();g.translate(d*80,-220);g.rotate(d*(o.run?1.2+run:.4));rr(-18,0,36,90,18,B);g.restore()});
    ell(0,-310,70,64,B);ell(-52,-362,22,22,B);ell(52,-362,22,22,B);ell(-52,-362,12,12,L);ell(52,-362,12,12,L);ell(0,-290,30,24,L);ell(0,-300,10,8,'#2A1A1A');
    if(o.run){ell(-24,-326,10,13,'#fff');ell(24,-326,10,13,'#fff');ell(-24,-324,5,7,'#111');ell(24,-324,5,7,'#111');ell(0,-274,10,12,'#7F1D1D')}else{ell(-24,-324,6,8,'#111');ell(24,-324,6,8,'#111');g.strokeStyle='#2A1A1A';g.lineWidth=4;g.beginPath();g.arc(0,-282,10,.3,Math.PI-.3);g.stroke()}}
  g.restore()}
function bee(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);const w=Math.sin(t*40)*.5;
  g.save();g.globalAlpha=.75;ell(-10,-48,22,30,'#E0F2FE',-.4+w);ell(14,-46,20,28,'#E0F2FE',.4-w);g.restore();
  ell(0,0,44,32,'#FACC15');g.fillStyle='#1F2937';g.fillRect(-14,-30,12,60);g.fillRect(10,-30,12,60);ell(40,-4,22,20,'#1F2937');ell(46,-8,6,7,'#fff');ell(47,-7,3,4,'#111');
  g.fillStyle='#1F2937';g.beginPath();g.moveTo(-44,0);g.lineTo(-62,-6);g.lineTo(-44,8);g.fill();g.strokeStyle='#1F2937';g.lineWidth=3;g.beginPath();g.moveTo(46,-22);g.lineTo(56,-44);g.stroke();ell(57,-46,5,5,'#1F2937');g.restore()}
function hen(x,y,s,t,o={}){g.save();g.translate(x,y-(o.flap?Math.abs(Math.sin(t*10))*30:0));g.scale(s*(o.dir||1),s);if(o.peck)g.rotate(Math.max(0,Math.sin(t*Math.PI/HB))*.45);
  rr(-16,-40,8,40,3,'#F59E0B');rr(14,-40,8,40,3,'#F59E0B');
  g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(-110,-120);g.quadraticCurveTo(-140,-180,-90,-190);g.lineTo(-60,-110);g.fill();
  ell(0,-100,90,66,'#FFFFFF');g.save();g.translate(-10,-110);g.rotate(o.flap?-.8+Math.sin(t*20)*.5:.1);ell(-10,0,50,28,'#F3F4F6');g.restore();
  ell(70,-170,40,40,'#FFFFFF');[[60,-212],[76,-218],[92,-212]].forEach(([a,b])=>ell(a,b,10,13,'#EF4444'));ell(100,-150,10,16,'#EF4444');
  g.fillStyle='#F59E0B';g.beginPath();g.moveTo(104,-178);g.lineTo(136,-170);g.lineTo(104,-160);g.fill();ell(84,-178,6,8,'#111');ell(86,-181,2,2,'#fff');g.restore()}
// ---------- clock & room ----------
function grandfatherClock(t,hour,strikeGlow=0){
  g.save();g.translate(CX,0);
  // case
  g.fillStyle='#7C4A21';g.beginPath();g.moveTo(-200,1080);g.lineTo(-200,700);g.quadraticCurveTo(-200,600,-120,590);g.quadraticCurveTo(0,520,120,590);g.quadraticCurveTo(200,600,200,700);g.lineTo(200,1080);g.closePath();g.fill();
  rr(-150,1060,300,560,16,'#8B5A2B');rr(-200,1600,400,70,14,'#6B3F1A');rr(-230,1660,460,50,14,'#5C3A1A');
  ell(0,560,26,26,'#F5C542');
  // pendulum window
  rr(-100,1110,200,440,20,'#2A1A0E');const sw=Math.sin(2*Math.PI*(t-HV0)/(2*HB))*.35;
  g.save();g.beginPath();g.roundRect(-100,1110,200,440,20);g.clip();g.save();g.translate(0,1110);g.rotate(sw);rr(-6,0,12,330,4,'#D4A017');ell(0,350,46,46,'#F5C542');ell(-12,338,14,14,'rgba(255,255,255,.6)');g.restore();g.restore();
  g.restore();
  // face
  if(strikeGlow>0)glow(CX,FACEY,FACER*1.9,`rgba(255,230,120,${.55*strikeGlow})`);
  ell(CX,FACEY,FACER+22,FACER+22,'#F5C542');ell(CX,FACEY,FACER,FACER,'#FFF8E7');
  for(let k=1;k<=12;k++){const a=k/12*Math.PI*2-Math.PI/2;txt(String(k),CX+Math.cos(a)*(FACER-34),FACEY+Math.sin(a)*(FACER-34),k===hour?46:36,k===hour?'#DC2626':'#3F2A1E',null)}
  const ha=(hour%12)/12*Math.PI*2-Math.PI/2,ma=-Math.PI/2+(t%60)*0;
  g.strokeStyle='#1F2937';g.lineCap='round';g.lineWidth=16;g.beginPath();g.moveTo(CX,FACEY);g.lineTo(CX+Math.cos(ha)*85,FACEY+Math.sin(ha)*85);g.stroke();
  g.lineWidth=10;g.beginPath();g.moveTo(CX,FACEY);g.lineTo(CX+Math.cos(ma)*130,FACEY+Math.sin(ma)*130);g.stroke();ell(CX,FACEY,14,14,'#DC2626');
  // little smiling face on the clock
  g.strokeStyle='#3F2A1E';g.lineWidth=5;g.beginPath();g.arc(CX-50,FACEY+70,10,Math.PI*1.1,Math.PI*1.9);g.stroke();g.beginPath();g.arc(CX+50,FACEY+70,10,Math.PI*1.1,Math.PI*1.9);g.stroke();
  g.beginPath();g.arc(CX,FACEY+100,16,.2,Math.PI-.2);g.stroke()}
function hRoom(t){const w=g.createLinearGradient(0,0,0,1600);w.addColorStop(0,'#BFE3D0');w.addColorStop(1,'#8CC7A8');g.fillStyle=w;g.fillRect(0,0,W,1600);
  for(let k=0;k<11;k++){g.fillStyle='rgba(255,255,255,.18)';g.fillRect(k*100,0,40,1600)}
  // window (left) with sky
  g.save();g.beginPath();g.roundRect(40,620,220,300,20);g.clip();sky('#7DD3FC','#E0F2FE');cloud(80,700,.4);mandalaSun(200,690,30,t);g.restore();g.strokeStyle='#FFFFFF';g.lineWidth=12;g.beginPath();g.roundRect(40,620,220,300,20);g.stroke();g.lineWidth=6;g.beginPath();g.moveTo(150,620);g.lineTo(150,920);g.moveTo(40,770);g.lineTo(260,770);g.stroke();
  // door (right)
  rr(830,1080,210,590,14,'#B45309');ell(1005,1380,12,12,'#F5C542');rr(860,1120,150,180,10,'rgba(0,0,0,.12)');rr(860,1340,150,280,10,'rgba(0,0,0,.12)');
  const fl=g.createLinearGradient(0,1600,0,H);fl.addColorStop(0,'#A16207');fl.addColorStop(1,'#713F12');g.fillStyle=fl;g.fillRect(0,1600,W,H-1600);
  ell(540,1760,460,90,'#DC2626');ell(540,1760,400,66,'#FDE68A');ell(540,1760,340,46,'#DC2626')}
function dong(t,v){const n=v+1,t0=hl(v,2);for(let i=0;i<n;i++){const ti=t0+i*HB*1.0;const p=prog(t,ti,ti+.9);if(p<=0||p>=1)continue;
  g.save();g.globalAlpha=Math.min(1,p*6,(1-p)*3);const side=i%2?1:-1;g.translate(CX+side*(300+i*8),FACEY-140+i*55);g.scale(backOut(Math.min(1,p*3)),backOut(Math.min(1,p*3)));g.rotate(side*.15);txt('DONG!',0,0,64,'#FDE047','#7C2D12');g.restore()}
  const p=prog(t,t0-.2,t0+.4);if(p>0&&p<1){g.save();g.globalAlpha=Math.min(1,(1-p)*3+.2);g.translate(CX,FACEY);g.scale(1+p*.4,1+p*.4);txt(String(n),0,0,120,'#DC2626','#FFFFFF');g.restore()}}
function htitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#7C3AED';g.beginPath();g.roundRect(-400,-66,800,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Hickory Dickory Dock 🕰️',0,2,54,'#FFFFFF',null);g.restore()}
const HCAPS=[];HANI.forEach((A,v)=>{HCAPS.push([hl(v,0)-.25,hl(v,2)-.25,'Hickory dickory dock, '+A.a.charAt(0).toLowerCase()+A.a.slice(1)]);HCAPS.push([hl(v,2)-.25,hl(v,4)-.25,A.b]);HCAPS.push([hl(v,4)-.25,hl(v,6)+.4,'Hickory dickory dock. Tick tock, tick tock!'])});
HCAPS.push([HOUT-.25,HOUT+2*HL-.25,'Hickory dickory dock, tick tock, tick tock!']);HCAPS.push([HOUT+2*HL-.25,HOUT+4*HL-.25,'Hickory dickory dock, tick tock, tick tock!']);HCAPS.push([HOUT+4*HL-.25,HOUTEND,'Hickory dickory dock! 🕰️']);
function hcap(t){const i=HCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=HCAPS[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 58px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*72+40,y0=390;g.fillStyle='rgba(91,33,182,.88)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.92));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+36+li*72,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}
function tickTock(t){const k=Math.floor((t-HV0)/HB);const p=((t-HV0)/HB)%1;g.save();g.globalAlpha=1-p;txt(k%2?'tock':'tick',k%2?850:230,1250,54,'#fff','#7C3AED');g.restore()}

function drawHDD(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const v=t<HV0?-1:Math.min(6,Math.floor((t-HV0)/HPER));const l=v>=0?Math.floor((t-hv(v))/HL):-1;
  const hour=v<0?12:(v>=6?6:(l>=2?v+1:(v===0?12:v)));
  const strikeGlow=v>=0&&v<6?clamp(1-Math.abs(t-hl(v,2)-(v+1)*HB*.5)/((v+1)*HB*.6+.3)):0;
  hRoom(t);grandfatherClock(t,hour,strikeGlow);
  if(v<0){mouse(220,1700,.8,t,{});const q=backOut(prog(t,.6,1.6));g.save();g.translate(540,1250);g.scale(q,q);txt('Tick tock! 🕰️',0,0,80,'#fff','#7C3AED');g.restore()}
  else if(v<6){const A=HANI[v].n;
    if(A==='mouse'){let x=CX+215,y=1660,dir=1,rot=0;
      if(l<2){const q=easeOut(prog(t,hl(0,0),hl(0,2)));x=lerp(150,CX+215,Math.min(1,q*3));y=lerp(1700,640,clamp(q*1.25-.25));rot=q>.33?-Math.PI/2:0}
      else if(l<4){x=CX+130;y=600;rot=0;if(t>hl(0,3)){const q=easeOut(prog(t,hl(0,3),hl(0,4)));x=CX+215;y=lerp(640,1700,q);rot=Math.PI/2}}
      else{x=lerp(CX+215,180,clamp((t-hl(0,4))/2));y=1700;dir=-1}
      mouse(x,y,1.2,t,{dir,rot});if(l>=2&&l<3)pop(t,hl(0,2)+.9,'Eek! 🐭',CX+300,560,58,'#fff','#DB2777')}
    else if(A==='bird'){if(l<3)birdie(CX+175,575,1.45,t,{dir:-1});else{const q=easeOut(prog(t,hl(1,3),hl(1,4)));birdie(lerp(CX+175,1200,q),lerp(575,300,q),1.45,t,{fly:1})}
      if(l>=3&&l<4)pop(t,hl(1,3)+.2,'Away she flew! 🐦',540,1250,64,'#fff','#2563EB')}
    else if(A==='dog'){puppy(220,1720,1.6,t,l>=2?Math.abs(Math.sin(t*Math.PI/HB))*50:0);
      if(l<2){const tb=Math.floor((t-hv(2))/HB);if(tb%2===0)pop(t,hv(2)+tb*HB,'Woof!',260,1300,64,'#fff','#B45309')}
      if(l>=3&&l<4)pop(t,hl(2,3)+.1,'Fiddle-dee-dee! 🎶',540,1250,60,'#fff','#B45309');if(l>=3)notes(250,1400,t,hl(2,3),5)}
    else if(A==='bear'){if(l<3){bear(230,1740,1.25,t,{sleep:1});zzz(330,1440,t,1.6)}
      else{const q=prog(t,hl(3,3),hl(3,4));if(q<1){bear(lerp(250,940,q),1740,1.05,t,{run:1})}pop(t,hl(3,3)+.1,'Out the door! 🚪',540,1250,62,'#fff','#92400E')}}
    else if(A==='bee'){if(l<3){const a=(t-hv(4))*2.2;bee(CX+Math.cos(a)*270,FACEY+Math.sin(a)*250,1.5,t,{dir:-Math.sin(a)>0?1:-1});for(let k=1;k<8;k++){const b2=a-k*.18;ell(CX+Math.cos(b2)*260,FACEY+Math.sin(b2)*240,4,4,'rgba(255,255,255,.7)')}}
      g.save();const hq=easeOut(prog(t,hl(4,3)-.3,hl(4,3)+.3));g.translate(160,1050);g.scale(hq,hq);ell(0,0,80,95,'#F59E0B');for(let k=0;k<4;k++)rr(-75+k*4,-70+k*38,150-k*8,14,7,'#D97706');ell(0,40,20,20,'#5C3A1A');g.restore();
      if(l>=3){const q=easeOut(prog(t,hl(4,3),hl(4,4)));if(q<1)bee(lerp(CX+260,160,q),lerp(FACEY,1090,q),1.5,t,{dir:-1});pop(t,hl(4,3)+.2,'Buzz home! 🐝',540,1250,62,'#fff','#CA8A04')}}
    else if(A==='hen'){hen(280,1740,1.35,t,{peck:l<2,flap:l>=3&&l<4});if(l>=3){for(let k=0;k<8;k++){const p=((t*.8+k/8)%1);g.save();g.globalAlpha=1-p;ell(300+Math.sin(k*2+p*4)*140,1500-p*300,14,7,'#FFFFFF',k);g.restore()}
      if(l<4)pop(t,hl(5,3)+.1,'Oh fiddlesticks! 🐔',540,1250,60,'#fff','#DC2626')}}
    if(l>=2&&l<4)dong(t,v);if(l>=4)tickTock(t);
  }
  else{ // outro: everyone dances around the clock
    const xs=[[130,1720],[300,1820],[780,1830],[950,1720]];
    mouse(xs[0][0],xs[0][1]-hpu(t)*40,1.05,t,{});puppy(xs[1][0]-80,xs[1][1]-hpu(t+.1)*40,1.15,t,0);hen(xs[2][0],xs[2][1]-hpu(t+.2)*40,.9,t,{dir:-1});bear(xs[3][0],xs[3][1],.72,t,{dir:-1});
    birdie(CX+175,575,1.0,t,{dir:-1});const a=t*2.2;bee(CX+Math.cos(a)*260,FACEY+Math.sin(a)*240,.9,t,{dir:-Math.sin(a)>0?1:-1});tickTock(t);
    if(t>HOUT+4*HL)confetti(t,HOUT+4*HL,50);
    if(t>=HCARD){const q=easeOut(prog(t,HCARD,HCARD+.8));g.save();g.globalAlpha=q*.72;g.fillStyle='#3B0764';g.fillRect(0,0,W,1500);g.restore();g.save();g.globalAlpha=q;
      popcornLogo(W/2,520,.85*backOut(prog(t,HCARD,HCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Tick tock! 🕰️🐭',W/2,990,78,'#fff','#7C3AED');
      const sp=backOut(prog(t,HCARD+.6,HCARD+1.4));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  }
  const cuts=[];for(let k=1;k<=6;k++)cuts.push(hv(k));cuts.forEach(c=>{const d=Math.abs(t-c);if(d<.15){g.fillStyle=`rgba(255,255,255,${(1-d/.15)*.6})`;g.fillRect(0,0,W,H)}});
  if(t<HCARD){htitle(t);hcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,HEND-1.2,HEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawHDD;
