// ================= "The Wheels On The Bus" — Popcorn Productions =================
const BBAR=1.52, BLINE=2*BBAR, BB=BBAR/4;
const BV=[12.2,36.5,73.0,109.5];                     // verse starts (8 bars each)
const bl=(v,l)=>BV[v]+l*BLINE, BVEND=v=>BV[v]+8*BBAR;
const BEND=128.0, BCARD=121.9;
const bpulse=t=>Math.pow(Math.sin(Math.PI*((((t-BV[0])/BB)%1+1)%1)),2);
const CAPS2=['#2563EB','#DB2777','#F59E0B','#7C3AED','#059669'];

// ---------- the bus ----------
function wheel(x,y,r,rot){g.save();g.translate(x,y);g.rotate(rot);ell(0,0,r,r,'#1F2937');ell(0,0,r*.62,r*.62,'#9CA3AF');ell(0,0,r*.5,r*.5,'#E5E7EB');
  g.strokeStyle='#6B7280';g.lineWidth=r*.1;for(let k=0;k<5;k++){g.beginPath();g.moveTo(0,0);g.lineTo(Math.cos(k*1.2566)*r*.48,Math.sin(k*1.2566)*r*.48);g.stroke()}ell(0,0,r*.14,r*.14,'#F59E0B');g.restore()}
function driverHead(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);ell(0,0,46,44,'#C48A5E');ell(-44,4,9,12,'#C48A5E');
  g.fillStyle='#1D4ED8';g.beginPath();g.ellipse(0,-22,50,30,0,Math.PI,0);g.fill();rr(-10,-26,78,12,6,'#1E3A8A');rr(-20,-46,40,14,4,'#FBBF24');
  ell(-14,-2,6,8,'#2A1A1A');ell(16,-2,6,8,'#2A1A1A');ell(-6,20,16,7,'#20140C',-.2);ell(10,20,16,7,'#20140C',.2);g.strokeStyle='#7F1D1D';g.lineWidth=4;g.beginPath();g.arc(2,28,10,.2,Math.PI-.2);g.stroke();g.restore()}
// side view, facing right; (x,y)=road contact at centre. o: wheelRot, bounce, kidsJump, wipe, rain, honk, doorOpen, riders
function bus(x,y,s,t,o={}){g.save();g.translate(x,y-(o.bounce||0));g.scale(s,s);
  const rot=o.wheelRot||0;
  // body
  g.fillStyle='#FBBF24';g.beginPath();g.moveTo(-400,-70);g.lineTo(-400,-330);g.quadraticCurveTo(-400,-370,-360,-370);g.lineTo(300,-370);g.quadraticCurveTo(360,-370,380,-300);g.lineTo(410,-150);g.quadraticCurveTo(420,-70,380,-70);g.closePath();g.fill();
  g.fillStyle='rgba(0,0,0,.08)';g.fillRect(-400,-150,810,80);
  rr(-400,-170,790,22,6,'#111827');rr(-400,-205,790,10,4,'#F59E0B');
  // windows with riders
  const wins=[-360,-245,-130,-15,100];
  wins.forEach((wx,i)=>{g.save();g.beginPath();g.roundRect(wx,-335,100,120,14);g.fillStyle='#BFE6FF';g.fill();g.clip();
    const r=(o.riders||[0,1,2,3,4])[i];if(r!==undefined&&r!==null){const j=o.kidsJump?Math.max(0,Math.sin(t*Math.PI/BB+i))*45:0;kid(r,wx+50,-140-j,{s:.5,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[i],trunk:o.wave?1:.5})}
    g.fillStyle='rgba(255,255,255,.35)';g.beginPath();g.moveTo(wx+60,-335);g.lineTo(wx+100,-335);g.lineTo(wx+40,-215);g.lineTo(wx,-215);g.fill();g.restore();
    g.strokeStyle='#111827';g.lineWidth=6;g.beginPath();g.roundRect(wx,-335,100,120,14);g.stroke()});
  // door
  const dop=o.doorOpen||0;rr(225,-335,70,265,10,'#111827');rr(229+dop*30,-331,31-dop*25,257,6,'#BFE6FF');rr(262,-331,31-dop*25,257,6,'#BFE6FF');
  // windshield + driver + wiper
  g.save();g.beginPath();g.moveTo(305,-345);g.lineTo(350,-345);g.quadraticCurveTo(372,-340,385,-290);g.lineTo(400,-210);g.lineTo(305,-210);g.closePath();g.fillStyle='#BFE6FF';g.fill();g.clip();
  driverHead(340,-265,.9,t);
  if(o.rain){for(let k=0;k<10;k++)ell(310+rnd(k)*90,-340+((t*200+rnd(k+2)*130)%130),3,6,'rgba(59,130,246,.6)')}
  g.restore();
  const wa=o.wipe?Math.sin(t*Math.PI/BB)*.9:-.9;g.save();g.translate(330,-215);g.rotate(-1.2+wa*.6);rr(-4,-110,8,110,4,'#111827');g.restore();
  // lights, grill, bumper, stop sign
  ell(398,-120,14,18,'#FEF3C7');glow(398,-120,o.honk?120:40,'rgba(255,240,170,.6)');rr(-410,-120,20,40,6,'#EF4444');
  rr(-420,-80,840,26,10,'#4B5563');
  g.save();g.translate(-400,-240);rr(-36,-30,36,60,4,'#DC2626');g.restore();
  txt('SCHOOL BUS',-60,-185,0.1,'#111827',null);
  g.save();g.font='700 34px Fredoka';g.fillStyle='#111827';g.textAlign='center';g.fillText('POPCORN EXPRESS',-130,-180);g.restore();
  // wheels
  [[-250],[250]].forEach(([wx])=>{ell(wx,-60,96,96,'#111827');wheel(wx,-40,78,rot)});
  g.restore()}

// ---------- town & road ----------
function townBg(t,scroll,o={}){const rain=o.rain||0,dusk=o.dusk||0;
  if(dusk)sky('#FB923C','#FDE68A');else if(rain)sky('#64748B','#CBD5E1');else sky('#7DD3FC','#E0F2FE');
  if(!rain&&!dusk)mandalaSun(860,640,70,t);
  for(let k=0;k<3;k++){const cx=((k*480-scroll*.15)%1600+1600)%1600-260;rain?bigCloud(cx,560+k%2*60,.5,'#94A3B8'):cloud(cx,560+k%2*80,.9)}
  if(o.rainbow){g.save();g.globalAlpha=o.rainbow;['#EF4444','#F97316','#FACC15','#22C55E','#3B82F6','#8B5CF6'].forEach((c,k)=>{g.strokeStyle=c;g.lineWidth=26;g.beginPath();g.arc(540,1250,560-k*26,Math.PI,0);g.stroke()});g.restore()}
  // far buildings
  for(let k=0;k<9;k++){const bx=((k*170-scroll*.35)%1530+1530)%1530-200;const hgt=260+rnd(k)*260;rr(bx,1200-hgt,150,hgt+40,8,['#93C5FD','#C4B5FD','#FCA5A5','#86EFAC','#FDE68A'][k%5]);
    for(let r=0;r<Math.floor(hgt/70);r++)for(let c=0;c<3;c++)rr(bx+18+c*42,1200-hgt+24+r*70,26,36,4,'rgba(255,255,255,.7)')}
  // near: trees & houses
  g.fillStyle='#86EFAC';g.fillRect(0,1200,W,200);
  for(let k=0;k<7;k++){const px=((k*260-scroll*.7)%1820+1820)%1820-260;if(k%2){house(px,1390,.75,t,['#F97316','#2563EB','#DB2777'][k%3])}else{rr(px-12,1280,24,110,6,'#7C4A21');ell(px,1250,80,90,'#16A34A');ell(px-30,1270,50,50,'#22C55E')}}
  // road
  rr(0,1390,W,240,0,'#4B5563');g.fillStyle='#FDE047';for(let k=0;k<8;k++){const dx=((k*200-scroll)%1600+1600)%1600-200;g.fillRect(dx,1505,110,14)}
  rr(0,1380,W,16,0,'#D1D5DB');g.fillStyle='#86EFAC';g.fillRect(0,1630,W,H-1630);
  for(let k=0;k<18;k++){const fx=((k*70-scroll)%1260+1260)%1260-90;rr(fx,1660,26,110,6,'#FFFFFF');g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(fx,1660);g.lineTo(fx+13,1640);g.lineTo(fx+26,1660);g.fill()}
  rr(-20,1690,W+40,14,4,'#FFFFFF');rr(-20,1740,W+40,14,4,'#FFFFFF');
  for(let k=0;k<8;k++){const bx=((k*170-scroll*1.2)%1360+1360)%1360-120;ell(bx,1850,110,70,'#16A34A');ell(bx+60,1830,70,55,'#22C55E');marigold(bx-30,1815,.8,['#F472B6','#FBBF24','#F87171'][k%3]);marigold(bx+50,1795,.7,['#FBBF24','#F87171','#F472B6'][k%3])}
  if(rain){for(let k=0;k<120;k++){const x=(rnd(k)*W+t*120)%W,y=((t*900+rnd(k+3)*H)%H);g.strokeStyle='rgba(191,219,254,.8)';g.lineWidth=3;g.beginPath();g.moveTo(x,y);g.lineTo(x-10,y+30);g.stroke()}}}
function duck(x,y,s,t,k){g.save();g.translate(x,y-Math.abs(Math.sin(t*10+k))*10);g.scale(s,s);ell(0,-40,48,34,'#FDE047');ell(36,-80,28,26,'#FDE047');g.fillStyle='#F97316';g.beginPath();g.moveTo(58,-84);g.lineTo(90,-76);g.lineTo(58,-68);g.fill();ell(42,-88,5,6,'#111');ell(-10,-48,26,14,'#FACC15',-.3);rr(-14,-10,8,16,3,'#F97316');rr(10,-10,8,16,3,'#F97316');g.restore()}
function busStop(x,y,s){g.save();g.translate(x,y);g.scale(s,s);rr(-8,-300,16,300,6,'#6B7280');ell(0,-310,46,46,'#2563EB');txt('BUS',0,-310,28,'#fff',null);rr(-140,-200,200,14,6,'#93C5FD');g.restore()}
function btitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#F59E0B';g.beginPath();g.roundRect(-410,-66,820,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FFFFFF';g.stroke();txt('The Wheels On The Bus 🚌',0,2,54,'#FFFFFF','#B45309');g.restore()}
const BLYR=[['round and round','The wheels on the bus go round and round,'],['swish, swish, swish','The wipers on the bus go swish, swish, swish,'],['beep, beep, beep','The horn on the bus goes beep, beep, beep,'],['up and down','The people on the bus go up and down,']];
const BCAP=[];BLYR.forEach(([w,l1],v)=>{BCAP.push([bl(v,0)-.25,bl(v,2)-.25,l1+' '+w+', '+w+'.']);BCAP.push([bl(v,2)-.25,BVEND(v)+.4,l1+' all through the town!'])});
function bcaption(t){const i=BCAP.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=BCAP[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 58px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*72+40,y0=395;g.fillStyle='rgba(29,78,216,.88)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.92));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+36+li*72,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}
const BPOPS=[[54.6,'The wheels on the bus! 🚌'],[58.6,'Yeah! 🙌'],[60.6,'Yeah! 🎉'],[66.7,'The wheels on the bus! 🚌'],[70.6,'Yeah! 🙌'],[72.0,'Yeah! 🎉'],[90.6,'The wheels on the bus! 🚌'],[96.6,'Yeah! 🙌']];
function bpop(t){BPOPS.forEach(([t0,s])=>{const p=prog(t,t0,t0+1.6);if(p<=0||p>=1)return;g.save();g.globalAlpha=Math.min(1,p*6,(1-p)*4);g.translate(540,860);const q=backOut(Math.min(1,p*3));g.scale(q,q);g.rotate(Math.sin(t*8)*.04);txt(s,0,0,80,'#FFFFFF','#DB2777');g.restore()})}
function burst(x,y,t,t0,s,col){const p=prog(t,t0,t0+.5);if(p<=0||p>=1)return;g.save();g.globalAlpha=1-p*.8;g.translate(x,y);const q=backOut(Math.min(1,p*3));g.scale(q,q);g.rotate((rnd(t0)-.5)*.4);txt(s,0,0,92,'#FFFFFF',col);g.restore()}

function drawBus(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const BX=540,BY=1560,BS=1.0;
  let scroll=0,speed=1;
  if(t<BV[0]){ // intro: kids at the bus stop, bus arrives, door opens
    const arrive=easeOut(prog(t,1,6.5));townBg(t,arrive*700);busStop(820,1390,1.0);
    const dop=prog(t,6.8,7.6);const board=prog(t,7.8,11.5);
    bus(lerp(-700,BX,arrive),BY,BS,t,{wheelRot:arrive*30,doorOpen:dop,riders:[null,null,null,null,null].map((_,i)=>i<Math.floor(board*5)?i:null)});
    [0,1,2,3,4].forEach((k,i)=>{if(i<Math.floor(board*5))return;kid(k,700+i*85,1820,{s:.72,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[i],trunk:i%2?1:.5})});
    if(t<6.5){const q=backOut(prog(t,1.5,2.5));g.save();g.translate(540,860);g.scale(q,q);txt('Here comes the bus! 🚌',0,0,72,'#fff','#B45309');g.restore()}
    if(t>7.8)burst(540,860,t,7.8,'All aboard! 🎒','#2563EB');
  }
  else if(t<BV[1]){ // wheels verse + interlude 1 (rain clouds roll in near the end)
    scroll=(t-BV[0])*420;const rainIn=prog(t,BV[1]-4,BV[1]);
    townBg(t,scroll,{rain:rainIn>.5?1:0});
    bus(BX,BY,BS,t,{wheelRot:t*7,bounce:bpulse(t)*6,wave:t>BVEND(0)});
    if(t<BVEND(0)){const l=Math.floor((t-BV[0])/BLINE);if(l===1||l===3){const z=easeOut(prog(t,bl(0,l),bl(0,l)+.4));g.save();g.globalAlpha=z;ell(540,980,200,200,'#FFFFFF');g.lineWidth=10;g.strokeStyle='#F59E0B';g.stroke();wheel(540,980,150*z,t*9);g.restore();
        for(let k=0;k<2;k++){g.save();g.translate(540,980);g.rotate(t*4+k*Math.PI);txt('↻',230,0,70,'#F59E0B',null);g.restore()}}
      const tb=Math.floor((t-BV[0])/BB);burst(540,760,t,BV[0]+tb*BB,['Round!','& round!'][tb%2],'#F59E0B')}
  }
  else if(t<BVEND(1)+1){ // wipers verse in the rain: windshield close-up alternating with the bus
    scroll=(t-BV[0])*300;const l=Math.floor((t-BV[1])/BLINE);
    if(l%2===0){townBg(t,scroll,{rain:1});bus(BX,BY,BS,t,{wheelRot:t*6,wipe:1,rain:1})}
    else{ // windshield close-up
      sky('#475569','#94A3B8');g.save();g.beginPath();g.roundRect(90,620,900,760,60);g.clip();townBg(t,scroll,{rain:1});g.restore();
      for(let k=0;k<40;k++)ell(120+rnd(k)*840,650+((t*300+rnd(k+5)*700)%700),5,9,'rgba(191,219,254,.9)');
      [[330],[750]].forEach(([wx],i)=>{const a=Math.sin(t*Math.PI/BB+i*.3)*1.0;g.save();g.translate(wx,1360);g.rotate(a);rr(-8,-560,16,560,8,'#111827');rr(-14,-560,28,220,10,'#374151');g.restore()});
      g.strokeStyle='#FBBF24';g.lineWidth=60;g.beginPath();g.roundRect(90,620,900,760,60);g.stroke();rr(90,1380,900,300,30,'#374151');g.save();g.translate(540,1560);g.rotate(Math.sin(t*2)*.2);g.strokeStyle='#111827';g.lineWidth=30;g.beginPath();g.arc(0,0,150,0,7);g.stroke();g.lineWidth=20;g.beginPath();g.moveTo(-150,0);g.lineTo(150,0);g.moveTo(0,0);g.lineTo(0,150);g.stroke();g.restore()}
    const tb=Math.floor((t-BV[1])/BB);if(t<BVEND(1))burst(540,760,t,BV[1]+tb*BB,'Swish!','#0EA5E9');
  }
  else if(t<BV[2]){ // interlude 2: sun & rainbow, happy bouncing bus
    scroll=(t-BV[0])*420;townBg(t,scroll,{rainbow:clamp((t-BVEND(1)-1)/2)});
    bus(BX,BY,BS,t,{wheelRot:t*7,bounce:Math.abs(Math.sin(t*Math.PI/BB))*30,wave:1,kidsJump:1});bpop(t);
  }
  else if(t<BVEND(2)+.5){ // horn verse: ducks crossing the road
    const stop=t<bl(2,3);scroll=(BV[2]-BV[0])*420+(stop?0:(t-bl(2,3))*420);townBg(t,scroll);
    if(stop){const q=prog(t,BV[2],bl(2,3));for(let k=0;k<4;k++)duck(820+k*65,lerp(1420,1700,clamp(q*1.3-k*.1)),.75,t,k)}
    bus(BX-150,BY,BS,t,{wheelRot:stop?0:t*7,honk:bpulse(t)>.6});
    const tb=Math.floor((t-BV[2])/BB);if(t<BVEND(2))burst(560,820,t,BV[2]+tb*BB,'BEEP!','#DC2626');
    if(t>bl(2,1)&&t<bl(2,2)){g.save();g.globalAlpha=.9;txt('Quack quack! 🦆',820,1060,56,'#fff','#CA8A04');g.restore()}
  }
  else if(t<BV[3]){ // interlude 3: over the big hill to the park, sunset
    scroll=(t-BV[0])*420;const dusk=t>BV[3]-10;townBg(t,scroll,{dusk});
    const hill=Math.sin(clamp((t-BVEND(2)-.5)/8)*Math.PI);bus(BX,BY-hill*120,BS,t,{wheelRot:t*7,bounce:bpulse(t)*8,wave:1});
    if(hill>.05){g.save();g.globalAlpha=hill;txt('Wheee! ⛰️',540,1080,72,'#fff','#16A34A');g.restore()}
    bpop(t);
  }
  else if(t<BCARD){ // people verse: everyone bounces up and down
    scroll=(t-BV[0])*300;townBg(t,scroll,{dusk:1});
    const ud=Math.abs(Math.sin(t*Math.PI/(2*BB)));bus(BX,BY,BS*1.05,t,{wheelRot:t*5,bounce:ud*40,kidsJump:1,wave:1});
    const tb=Math.floor((t-BV[3])/(2*BB));burst(540,760,t,BV[3]+tb*2*BB,['Up! ⬆️','Down! ⬇️'][tb%2],'#7C3AED');
  }
  else{ // end card: arrival at the park
    townBg(t,(BCARD-BV[0])*300,{dusk:1});bus(BX,BY,BS,t,{doorOpen:1});
    [0,1,2,3,4].forEach((k,i)=>kid(k,160+i*190,1840,{s:.7,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[i],trunk:1}));
    const q=easeOut(prog(t,BCARD,BCARD+1));g.save();g.globalAlpha=q*.72;g.fillStyle='#1E1B4B';g.fillRect(0,0,W,1450);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.9*backOut(prog(t,BCARD,BCARD+1.2)),Math.max(0,Math.sin(Math.PI*prog(t,BCARD+1.2,BCARD+1.7)))*.25);
    txt('A Popcorn Productions video',W/2,900,46,'#FFE14D',null,'center',600);txt('Ride again soon! 🚌',W/2,1010,78,'#fff','#B45309');
    const sp=backOut(prog(t,BCARD+1.4,BCARD+2.4));g.save();g.translate(W/2,1170);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  [BV[1],BVEND(1)+1,BV[2],BVEND(2)+.5,BV[3],BCARD].forEach(c=>{const d=Math.abs(t-c);if(d<.2){g.fillStyle=`rgba(255,255,255,${(1-d/.2)*.7})`;g.fillRect(0,0,W,H)}});
  if(t<BCARD){btitle(t);bcaption(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,BEND-1.5,BEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawBus;
