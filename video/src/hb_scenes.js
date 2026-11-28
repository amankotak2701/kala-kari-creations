// ================= "Hush Little Baby" — Popcorn Productions =================
const HBL=4.21, HB0=8.0, HCOUP=2*HBL;
const hc=k=>HB0+k*HCOUP;                      // couplet slot k
// couplet slots that are sung, with [line a, line b, gift shown on b, mishap on a]
const HSONG=[
 [0,'Hush, little baby, don\'t say a word,','Mama\'s gonna buy you a mockingbird.',null,'bird'],
 [1,'And if that mockingbird won\'t sing,','Mama\'s gonna buy you a diamond ring.','bird','ring'],
 [3,'And if that diamond ring turns brass,','Mama\'s gonna buy you a looking glass.','ring','glass'],
 [4,'And if that looking glass gets broke,','Mama\'s gonna buy you a billy goat.','glass','goat'],
 [6,'And if that billy goat won\'t pull,','Mama\'s gonna buy you a cart and bull.','goat','bull'],
 [7,'And if that cart and bull turn over,','Mama\'s gonna buy you a dog named Rover.','bull','dog'],
 [10,'And if that dog named Rover won\'t bark,','Mama\'s gonna buy you a horse and cart.','dog','horse'],
 [11,'And if that horse and cart fall down,','You\'ll still be the sweetest little baby in town.','horse','town']];
const HLALA=143.5, HCARD2=147.6, HEND2=153.0;
const hpu2=t=>Math.pow(Math.sin(Math.PI*((((t-HB0)/(HBL/2))%1+1)%1)),2);

function cradle(x,y,s,t,o={}){const rock=Math.sin(t*1.6)*.06;g.save();g.translate(x,y);g.scale(s,s);g.rotate(rock);
  if(!o.noRock){g.strokeStyle='#92400E';g.lineWidth=14;g.beginPath();g.arc(0,40,230,Math.PI*.15,Math.PI*.85);g.stroke();}
  g.fillStyle='#D97706';g.beginPath();g.moveTo(-200,-80);g.quadraticCurveTo(0,90,200,-80);g.lineTo(200,-60);g.quadraticCurveTo(0,110,-200,-60);g.closePath();g.fill();
  g.fillStyle='#FBBF24';g.beginPath();g.moveTo(-200,-80);g.quadraticCurveTo(0,60,200,-80);g.quadraticCurveTo(0,40,-200,-80);g.fill();
  for(let k=0;k<9;k++){g.strokeStyle='#B45309';g.lineWidth=4;g.beginPath();g.moveTo(-170+k*42,-60+Math.abs(k-4)*-6+10);g.lineTo(-165+k*42,10);g.stroke()}
  // canopy
  g.fillStyle='#F9A8D4';g.beginPath();g.moveTo(-210,-90);g.quadraticCurveTo(-230,-260,-80,-280);g.quadraticCurveTo(-120,-160,-110,-80);g.closePath();g.fill();
  // baby
  const bx=-40,by=-155;ell(bx,by+10,62,56,'#FFE4D6');g.fillStyle='#FDE68A';g.beginPath();g.ellipse(bx,by-10,70,62,0,Math.PI*1.05,Math.PI*1.95);g.fill();
  g.fillStyle='#FFFFFF';g.beginPath();g.ellipse(bx,by-22,74,48,0,Math.PI,0);g.fill();ell(bx,by-70,16,16,'#FFFFFF');
  if(o.sleep){g.strokeStyle='#3F2A1E';g.lineWidth=5;g.beginPath();g.arc(bx-20,by+8,9,Math.PI*.15,Math.PI*.85);g.stroke();g.beginPath();g.arc(bx+20,by+8,9,Math.PI*.15,Math.PI*.85);g.stroke()}
  else{ell(bx-20,by+6,8,10,'#3F2A1E');ell(bx+20,by+6,8,10,'#3F2A1E');ell(bx-17,by+2,3,3,'#fff');ell(bx+23,by+2,3,3,'#fff')}
  ell(bx-36,by+28,11,7,'rgba(244,114,182,.55)');ell(bx+36,by+28,11,7,'rgba(244,114,182,.55)');
  if(o.cry){ell(bx,by+34,12,14,'#7F1D1D');ell(bx-24,by+24+((t*60)%30),5,8,'#60A5FA');ell(bx+24,by+24+((t*60+15)%30),5,8,'#60A5FA')}
  else{g.strokeStyle='#9F1239';g.lineWidth=4;g.beginPath();g.arc(bx,by+28,10,.2,Math.PI-.2);g.stroke()}
  // blanket
  g.fillStyle='#93C5FD';g.beginPath();g.moveTo(-200,-62);g.quadraticCurveTo(-60,-130,190,-70);g.quadraticCurveTo(0,80,-200,-62);g.fill();for(let k=0;k<6;k++)starShape(-130+k*55,-60+Math.abs(k-2.5)*6,10,0,'#FFFFFF');
  g.restore()}
function nursery(t){const w=g.createLinearGradient(0,0,0,1450);w.addColorStop(0,'#312E81');w.addColorStop(1,'#6D28D9');g.fillStyle=w;g.fillRect(0,0,W,1450);
  for(let k=0;k<10;k++)for(let j=0;j<10;j++){g.globalAlpha=.1;starShape(50+k*110+(j%2)*55,60+j*140,12,0,'#FDE68A')}g.globalAlpha=1;
  g.save();g.beginPath();g.arc(160,640,120,0,7);g.clip();sky('#0B1446','#1E3A8A');moonFace(180,640,60,t,0,0);for(let k=0;k<10;k++)ell(60+rnd(k)*200,540+rnd(k+3)*200,2.5,2.5,'#fff');g.restore();
  g.strokeStyle='#E9D5FF';g.lineWidth=14;g.beginPath();g.arc(160,640,120,0,7);g.stroke();
  const fl=g.createLinearGradient(0,1440,0,H);fl.addColorStop(0,'#7C2D12');fl.addColorStop(1,'#431407');g.fillStyle=fl;g.fillRect(0,1440,W,H-1440);
  ell(600,1760,430,80,'#F9A8D4');ell(600,1760,370,58,'#FBCFE8');
  // mobile above the cradle
  g.strokeStyle='#E9D5FF';g.lineWidth=3;g.beginPath();g.moveTo(760,1100);g.lineTo(760,1180);g.stroke();g.save();g.translate(760,1180);g.rotate(Math.sin(t)*.2);rr(-110,-4,220,8,4,'#E9D5FF');
  [[-100,'#FDE047'],[0,'#F9A8D4'],[100,'#93C5FD']].forEach(([dx,c])=>{g.beginPath();g.moveTo(dx,0);g.lineTo(dx,40);g.stroke();starShape(dx,56,18,t+dx,c)});g.restore()}
// ---------- gifts ----------
function ring(x,y,s,t,brass=0){g.save();g.translate(x,y);g.scale(s,s);g.strokeStyle=brass?'#92400E':'#F5C542';g.lineWidth=18;g.beginPath();g.ellipse(0,30,70,60,0,0,7);g.stroke();
  const c=brass?'#A16207':'#A5F3FC';g.fillStyle=c;g.beginPath();g.moveTo(0,-90);g.lineTo(46,-50);g.lineTo(0,-10);g.lineTo(-46,-50);g.closePath();g.fill();
  if(!brass)for(let k=0;k<5;k++){const a=t*2+k*1.3;starShape(Math.cos(a)*90,-50+Math.sin(a)*70,10,a,'#FFFFFF')}g.restore()}
function mirror(x,y,s,t,crack=0){g.save();g.translate(x,y);g.scale(s,s);rr(-14,40,28,110,10,'#DB2777');ell(0,-20,82,96,'#DB2777');ell(0,-20,68,82,'#BFE6FF');ell(-22,-48,16,30,'rgba(255,255,255,.6)',-.4);
  if(crack){g.strokeStyle='#1F2937';g.lineWidth=4;g.beginPath();g.moveTo(0,-20);g.lineTo(-40,-70);g.moveTo(0,-20);g.lineTo(46,-60);g.moveTo(0,-20);g.lineTo(-30,40);g.moveTo(0,-20);g.lineTo(50,20);g.moveTo(-20,-45);g.lineTo(10,-60);g.stroke()}g.restore()}
function goat(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);
  [-50,40].forEach(lx=>rr(lx-10,-80,20,80,8,'#E5E7EB'));ell(0,-110,90,55,'#FFFFFF');g.save();g.translate(-90,-130);g.rotate(Math.sin(t*6)*.3);ell(-10,-10,12,22,'#FFFFFF');g.restore();
  g.save();g.translate(90,-170);g.rotate(o.stubborn?.3:0);ell(0,0,44,40,'#FFFFFF');g.strokeStyle='#A16207';g.lineWidth=10;g.lineCap='round';g.beginPath();g.moveTo(-14,-34);g.quadraticCurveTo(-30,-70,-50,-62);g.moveTo(10,-34);g.quadraticCurveTo(0,-74,-20,-72);g.stroke();
  ell(-34,-6,18,9,'#FFFFFF',-.4);ell(16,-6,6,8,'#111');g.fillStyle='#D1D5DB';g.beginPath();g.moveTo(10,30);g.lineTo(26,70);g.lineTo(-6,36);g.fill();ell(30,14,8,6,'#F9A8D4');g.restore();
  [-30,60].forEach(lx=>rr(lx-10,-80,20,80,8,'#FFFFFF'));g.restore()}
function bull(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);if(o.rot)g.rotate(o.rot);
  // cart behind
  rr(-330,-140,180,90,10,'#B45309');rr(-340,-150,200,20,6,'#92400E');wheel(-240,-30,40,o.wheel||0);g.strokeStyle='#92400E';g.lineWidth=8;g.beginPath();g.moveTo(-150,-90);g.lineTo(-90,-100);g.stroke();
  [-60,50].forEach(lx=>rr(lx-14,-90,28,90,10,'#78350F'));ell(0,-130,110,62,'#92400E');
  g.save();g.translate(120,-170);ell(0,0,52,46,'#92400E');g.strokeStyle='#FEF3C7';g.lineWidth=10;g.lineCap='round';g.beginPath();g.moveTo(-30,-30);g.quadraticCurveTo(-56,-60,-40,-80);g.moveTo(30,-30);g.quadraticCurveTo(56,-60,40,-80);g.stroke();
  ell(20,26,30,20,'#D6A065');ell(12,24,4,6,'#111');ell(30,24,4,6,'#111');ell(-14,-6,7,9,'#111');ell(18,-6,7,9,'#111');g.strokeStyle='#F5C542';g.lineWidth=5;g.beginPath();g.arc(22,38,10,0,Math.PI);g.stroke();g.restore();
  [-30,80].forEach(lx=>rr(lx-14,-90,28,90,10,'#92400E'));g.restore()}
function horseCart(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);rr(-380,-150,200,100,10,'#DC2626');rr(-390,-160,220,20,6,'#991B1B');
  if(!o.lost)wheel(-280,-30,42,o.wheel||0);else{wheel(-280+o.lost*300,-30+Math.sin(o.lost*10)*-10,42,o.lost*20);g.save();g.translate(-380,-60);g.rotate(.25);g.restore()}
  g.strokeStyle='#92400E';g.lineWidth=8;g.beginPath();g.moveTo(-180,-100);g.lineTo(-120,-120);g.stroke();g.restore();
  pony(x+40*s,y,s*.85,t,o.run??1,0)}
function giftBubble(x,y,r,t,draw,p){const s=backOut(clamp(p));if(s<=0)return;g.save();g.translate(x,y);g.scale(s,s);g.translate(-x,-y);
  glow(x,y,r*1.4,'rgba(253,224,71,.35)');ell(x,y,r,r,'rgba(255,255,255,.92)');g.lineWidth=10;g.strokeStyle='#FDE047';g.stroke();g.save();g.beginPath();g.arc(x,y,r-6,0,7);g.clip();draw();g.restore();
  for(let k=0;k<8;k++){const a=t*1.2+k*.8;starShape(x+Math.cos(a)*(r+30),y+Math.sin(a)*(r+30),10+4*Math.sin(t*5+k),a,'#FDE047')}g.restore()}
function drawGift(n,x,y,t,fail=0,p=1){
  if(n==='bird'){birdie(x,y+40,1.6,t,{});if(fail){txt('...',x+90,y-90,64,'#6B7280',null)}else{for(let k=0;k<3;k++){const q=((t*.8+k/3)%1);g.save();g.globalAlpha=1-q;txt('♪',x+60+k*30,y-60-q*120,50,'#2563EB',null);g.restore()}}}
  else if(n==='ring')ring(x,y+20,1.1,t,fail&&p>.3?1:0);
  else if(n==='glass')mirror(x,y+10,1.1,t,fail&&p>.25);
  else if(n==='goat')goat(x-30,y+110,.95,t,{stubborn:fail});
  else if(n==='bull')bull(x+90,y+110,.75,t,{rot:fail?Math.min(1.2,p*2)*.9:0,wheel:t*3});
  else if(n==='dog'){puppy(x-70,y+110,1.3,t,0);rr(x-10,y+10,80,40,10,'#FDE047');txt('Rover',x+30,y+30,24,'#7C2D12',null);if(fail)zzz(x+60,y-60,t,1.2)}
  else if(n==='horse')horseCart(x+40,y+110,.6,t,{lost:fail?clamp(p*1.5):0,run:fail?0:1,wheel:t*4});
  else if(n==='town'){for(let k=0;k<5;k++)house(x-200+k*100,y+150,.55,t,['#F97316','#2563EB','#DB2777','#16A34A','#7C3AED'][k]);txt('👑',x,y-60,110,'#000',null);for(let k=0;k<6;k++){const q=((t*.7+k/6)%1);g.save();g.globalAlpha=1-q;txt('♥',x-120+k*48,y+40-q*160,44,'#F472B6',null);g.restore()}}}
function hbtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#DB2777';g.beginPath();g.roundRect(-340,-66,680,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Hush Little Baby 👶',0,2,58,'#FFFFFF',null);g.restore()}
const HCAPS2=[];HSONG.forEach(([k,a,b])=>{HCAPS2.push([hc(k)-.3,hc(k)+HBL-.3,a]);HCAPS2.push([hc(k)+HBL-.3,hc(k)+HCOUP-.1,b])});HCAPS2.push([HLALA-.2,HCARD2,'La la la la la la la... 🎵']);
function hbcap(t){const i=HCAPS2.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=HCAPS2[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 60px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*74+40,y0=395;g.fillStyle='rgba(131,24,67,.88)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.9));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+37+li*74,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}

function drawHush(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  nursery(t);
  const BX=540,BY=850,BR=230;
  // which sung couplet are we in?
  const ci=HSONG.findIndex(([k])=>t>=hc(k)-.3&&t<hc(k)+HCOUP-.3);
  const asleep=t>118;
  adult('mom',200,1810,{s:1.2,t,pose:ci>=0?'hold':'sway',happy:1,carry:()=>{}});
  cradle(700,1680,1.3,t,{cry:ci===0&&t<hc(0)+HBL*.6,sleep:asleep});
  if(ci>=0){const [k,a,b,prev,next]=HSONG[ci];const inB=t>=hc(k)+HBL-.3;
    if(!inB){ if(prev){const p=prog(t,hc(k),hc(k)+HBL);giftBubble(BX,BY,BR,t,()=>drawGift(prev,BX,BY,t,1,p),1);
        const msg={bird:'Not singing! 🤐',ring:'Oh no, brass! 😮',glass:'Crack! 🪞',goat:'Won\'t pull! 🐐',bull:'Whoops! 🐂',dog:'No bark... 😴',horse:'Fell down! 🐴'}[prev];pop(t,hc(k)+1.2,msg,540,1240,58,'#fff','#7C3AED')}
      else{pop(t,hc(0)+.4,'Shh... 🤫',540,1050,80,'#fff','#DB2777')}}
    else{const p=prog(t,hc(k)+HBL-.3,hc(k)+HBL+.3);giftBubble(BX,BY,BR,t,()=>drawGift(next,BX,BY,t,0,1),p);
      if(next!=='town')pop(t,hc(k)+HBL+.1,'✨ A gift! ✨',540,1240,58,'#fff','#CA8A04');else pop(t,hc(k)+HBL+.2,'Sweetest baby in town! 💖',540,1240,54,'#fff','#DB2777')}}
  else if(t<HB0-.3){const q=backOut(prog(t,.5,1.5));g.save();g.translate(540,900);g.scale(q,q);txt('Goodnight, baby! 🌙',0,0,72,'#fff','#DB2777');g.restore()}
  else if(!asleep){ // short instrumental breaks: notes & hearts, baby giggles
    for(let k=0;k<5;k++){const p=((t*.5+k/5)%1);g.save();g.globalAlpha=1-p;txt(k%2?'♥':'♪',380+k*90,1200-p*300,56,k%2?'#F472B6':'#FDE047',null);g.restore()}
    const last=HSONG.filter(([k])=>hc(k)<t).pop();if(last)giftBubble(BX,BY,BR*.75,t,()=>drawGift(last[4],BX,BY,t,0,1),1);}
  else if(t<HLALA){ // long ending: dream parade of all the gifts around the moon
    for(let k=0;k<60;k++){g.globalAlpha=.4+.6*Math.abs(Math.sin(t+k));ell(rnd(k)*W,520+rnd(k+5)*700,2.5,2.5,'#fff')}g.globalAlpha=1;
    moonFace(540,880,110,t,0,0);const items=['bird','ring','glass','goat','dog','horse'];
    items.forEach((n,i)=>{const a=t*.35+i/items.length*Math.PI*2;const x=540+Math.cos(a)*350,y=900+Math.sin(a)*260;g.save();g.translate(x,y);g.scale(.42,.42);g.translate(-x,-y);drawGift(n,x,y,t,0,1);g.restore()});
    zzz(560,1450,t,1.4);if(t<124)pop(t,118.5,'Sweet dreams... 💤',540,1250,62,'#fff','#6D28D9')}
  else{zzz(560,1450,t,1.4);moonFace(540,880,110,t,0,0);for(let k=0;k<5;k++){const p=((t*.5+k/5)%1);g.save();g.globalAlpha=1-p;txt('♪',260+k*40,1300-p*300,56,'#FDE047',null);g.restore()}}
  if(t>=HCARD2){const q=easeOut(prog(t,HCARD2,HCARD2+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#1E1B4B';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,HCARD2,HCARD2+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Sweet dreams, baby! 💖',W/2,990,68,'#fff','#DB2777');
    const sp=backOut(prog(t,HCARD2+.5,HCARD2+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<HCARD2){hbtitle(t);hbcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,HEND2-1.2,HEND2);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawHush;
