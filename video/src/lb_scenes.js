// ================= "London Bridge Is Falling Down" — Popcorn Productions =================
const LBL=2.727, LBV=4*LBL, LBPAIR=12*LBL, LB0=10.2;
const lbv=v=>LB0+Math.floor(v/2)*LBPAIR+(v%2)*LBV;       // verse v start (0..7)
const lbl=(v,l)=>lbv(v)+l*LBL;
const LBCARD=131.0, LBEND=134.1;
const lbpu=t=>Math.pow(Math.sin(Math.PI*((((t-LB0)/(LBL/2))%1+1)%1)),2);
const LBLYR=[
 ['London Bridge is falling down,','Falling down, falling down.'],
 ['Build it up with sticks and stones,','Sticks and stones, sticks and stones.'],
 ['Sticks and stones will all fall down,','All fall down, all fall down.'],
 ['Build it up with wood and clay,','Wood and clay, wood and clay.'],
 ['Wood and clay will wash away,','Wash away, wash away.'],
 ['Build it up with iron and steel,','Iron and steel, iron and steel.'],
 ['Iron and steel will bend and bow,','Bend and bow, bend and bow.'],
 ['London Bridge is falling down,','Falling down, falling down.']];
const BX0=150,BX1=930,DECK=1290;

function river(t,o={}){const rise=o.rise||0;sky(o.rain?'#64748B':'#7DD3FC',o.rain?'#CBD5E1':'#E0F2FE');
  if(!o.rain){mandalaSun(900,560,60,t);cloud(((t*15)%1400)-300,520,.9)}else{bigCloud(300,560,.8,'#94A3B8');bigCloud(800,520,.7,'#9CA3AF');for(let k=0;k<100;k++){const x=rnd(k)*W,y=((t*900+rnd(k+3)*1400)%1400)+450;g.strokeStyle='rgba(191,219,254,.85)';g.lineWidth=4;g.beginPath();g.moveTo(x,y);g.lineTo(x-8,y+30);g.stroke()}}
  // skyline (generic city)
  g.fillStyle='rgba(100,116,139,.55)';[[60,300,120],[200,380,90],[310,260,110],[440,420,80],[540,330,130],[690,280,100],[800,400,90],[900,300,140]].forEach(([x,h,w])=>{g.fillRect(x,1180-h,w,h)});
  g.fillStyle='rgba(71,85,105,.65)';g.fillRect(470,700,70,480);g.beginPath();g.moveTo(460,700);g.lineTo(505,600);g.lineTo(550,700);g.fill();ell(505,760,26,26,'#F8FAFC');g.strokeStyle='#334155';g.lineWidth=4;g.beginPath();g.moveTo(505,760);g.lineTo(505,742);g.moveTo(505,760);g.lineTo(518,764);g.stroke();
  // banks + river
  g.fillStyle='#4ADE80';g.fillRect(0,1180,W,140);
  const wy=1360-rise*80;const gr=g.createLinearGradient(0,wy,0,1700);gr.addColorStop(0,'#38BDF8');gr.addColorStop(1,'#0369A1');g.fillStyle=gr;g.fillRect(BX0-20,wy,BX1-BX0+40,1700-wy);
  for(let k=0;k<10;k++){const x=BX0+((k*90+t*60)%(BX1-BX0));g.strokeStyle='rgba(255,255,255,.6)';g.lineWidth=4;g.beginPath();g.moveTo(x,wy+40+(k%3)*80);g.quadraticCurveTo(x+20,wy+30+(k%3)*80,x+40,wy+40+(k%3)*80);g.stroke()}
  g.fillStyle='#16A34A';g.fillRect(0,1290,BX0,H-1290);g.fillRect(BX1,1290,W-BX1,H-1290);g.fillStyle='#A16207';g.fillRect(0,1690,W,H-1690);
  for(let k=0;k<6;k++)marigold(20+k*22,1760+(k%2)*40,.7,['#F472B6','#FBBF24'][k%2]);}
// bridge types: old, stone, wood, steel. build 0..1 grows the bridge; fall 0..1 breaks it.
function bridgeOld(t,fall=0){const n=12;for(let k=0;k<n;k++){const x=BX0+k*(BX1-BX0)/n;const f=clamp(fall*1.6-k*.05);g.save();g.translate(x+32,DECK+f*f*420);g.rotate(f*(k%2?1.2:-1.2));rr(-32,-12,64,24,4,'#A16207');g.restore()}
  for(let k=0;k<4;k++){const x=BX0+60+k*230;const f=clamp(fall*1.3-k*.08);g.save();g.translate(x,DECK+20+f*300);g.rotate(f*.8);rr(-14,0,28,140,4,'#78350F');g.restore()}}
function bridgeStone(t,build=1,fall=0){const piers=[260,540,820];piers.forEach((px,i)=>{for(let r=0;r<5;r++){const k=i*5+r;const p=clamp(build*16-k);if(p<=0)continue;const f=clamp(fall*1.6-(k*.04));
    ell(px+(r%2?14:-14)+f*(k%2?60:-60),DECK+130-r*30+f*f*320+(1-backOut(p))*-200,34,18,['#9CA3AF','#6B7280','#A8A29E'][k%3])}});
  const dp=clamp(build*1.5-.5);if(dp>0)for(let k=0;k<10;k++){if(k/10>dp)break;const x=BX0+k*(BX1-BX0)/10;const f=clamp(fall*1.6-k*.05);g.save();g.translate(x+39,DECK-8+f*f*380);g.rotate(f*(k%2?1:-1));g.strokeStyle='#92400E';g.lineWidth=12;g.lineCap='round';g.beginPath();g.moveTo(-36,0);g.lineTo(36,0);g.moveTo(-30,-40);g.lineTo(-30,0);g.stroke();g.restore()}}
function bridgeWood(t,build=1,wash=0){const piers=[300,560,800];piers.forEach((px,i)=>{const p=clamp(build*4-i);if(p<=0)return;const dx=wash*(400+i*120),dy=Math.sin(t*3+i)*10*wash;
    for(let r=0;r<4;r++)rr(px-40+dx,DECK+20+r*36+dy+(1-backOut(p))*-200,80,32,4,'#B45309')});
  const dp=clamp(build*2-1);for(let k=0;k<12;k++){if(k/12>dp)break;const x=BX0+k*(BX1-BX0)/12;const dx=wash*(300+k*40),rot=wash*Math.sin(k)*.6;g.save();g.translate(x+32+dx,DECK+wash*140+Math.sin(t*3+k)*8*wash);g.rotate(rot);rr(-32,-14,64,28,4,'#D97706');rr(-32,-14,64,6,3,'#FBBF24');g.restore()}}
function bridgeSteel(t,build=1,bend=0){const sag=x=>bend*220*Math.sin(Math.PI*clamp((x-BX0)/(BX1-BX0)));
  const dp=clamp(build);const xEnd=BX0+(BX1-BX0)*dp;g.strokeStyle='#64748B';g.lineWidth=18;g.lineCap='round';
  g.beginPath();for(let x=BX0;x<=xEnd;x+=10)x===BX0?g.moveTo(x,DECK+sag(x)):g.lineTo(x,DECK+sag(x));g.stroke();
  g.beginPath();for(let x=BX0;x<=xEnd;x+=10)x===BX0?g.moveTo(x,DECK-140+sag(x)*1.1):g.lineTo(x,DECK-140+sag(x)*1.1);g.stroke();
  g.lineWidth=10;g.strokeStyle='#94A3B8';for(let k=0;k<12;k++){const x0=BX0+k*65,x1=x0+65;if(x1>xEnd)break;g.beginPath();g.moveTo(x0,DECK+sag(x0));g.lineTo(x1,DECK-140+sag(x1)*1.1);g.lineTo(x1,DECK+sag(x1));g.stroke()}
  for(let k=0;k<12;k++){const x=BX0+k*65;if(x>xEnd)break;ell(x,DECK+sag(x),7,7,'#F5C542')}
  if(build<1&&build>0){for(let k=0;k<6;k++){const a=t*12+k;starShape(xEnd+Math.cos(a)*30,DECK-60+Math.sin(a)*30,8,a,'#FDE047')}}}
function builder(k,x,y,s,t,carry){kid(k,x,y,{s,t,happy:1,noHat:1,noScarf:1,cap:'#FACC15',trunk:1});if(carry){g.save();g.translate(x,y-s*400);
  if(carry==='stick'){g.strokeStyle='#92400E';g.lineWidth=12;g.lineCap='round';for(let i=0;i<3;i++){g.beginPath();g.moveTo(-60,-i*12);g.lineTo(60,-i*12-10);g.stroke()}}
  else if(carry==='stone'){ell(0,0,40,26,'#9CA3AF');ell(-10,-6,14,8,'rgba(255,255,255,.3)')}
  else if(carry==='wood'){rr(-70,-14,140,28,4,'#D97706')}
  else if(carry==='clay'){rr(-36,-24,72,48,6,'#B45309')}
  else if(carry==='steel'){rr(-80,-12,160,24,4,'#64748B');ell(-60,0,6,6,'#F5C542');ell(60,0,6,6,'#F5C542')}
  g.restore()}}
function fairLady(x,y,s,t,o={}){kid(3,x,y,Object.assign({s,t,happy:1,noHat:1,noScarf:1,dir:-1},o));g.save();g.translate(x,y-s*(o.trunk===1?375:375));g.scale(s,s);
  g.fillStyle='#FBBF24';g.beginPath();g.moveTo(-50,0);g.lineTo(-50,-40);g.lineTo(-25,-18);g.lineTo(0,-50);g.lineTo(25,-18);g.lineTo(50,-40);g.lineTo(50,0);g.closePath();g.fill();ell(0,-34,7,7,'#EC4899');g.restore()}
function elephantWalk(x,t){elephant(0,x,DECK-10,{s:.75,t,walk:t*1.5,trunk:.6,happy:1})}
function lbtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#1D4ED8';g.beginPath();g.roundRect(-420,-66,840,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FBBF24';g.stroke();txt('London Bridge Is Falling Down',0,2,50,'#FFFFFF',null);g.restore()}
const LBCAPS=[];LBLYR.forEach(([a,b],v)=>{LBCAPS.push([lbl(v,0)-.25,lbl(v,1)-.25,a]);LBCAPS.push([lbl(v,1)-.25,lbl(v,2)-.25,b]);LBCAPS.push([lbl(v,2)-.25,lbl(v,3)-.25,a]);LBCAPS.push([lbl(v,3)-.25,lbl(v,4)-.15,'My fair lady! 👑'])});
function lbcap(t){const i=LBCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=LBCAPS[i];
  const al=Math.min(clamp((t-a)/.15),clamp((b-t)/.15));g.save();g.globalAlpha=al;g.font='700 60px Fredoka, Baloo2';
  const w=Math.min(g.measureText(s).width,920);const h=120,y0=395;g.fillStyle='rgba(30,58,138,.88)';g.beginPath();g.roundRect(W/2-w/2-50,y0-h/2,w+100,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FBBF24';g.stroke();
  const prg=clamp((t-a)/((b-a)*.85));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2,920);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2,920);g.restore();g.restore()}

function drawLondon(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const v=[0,1,2,3,4,5,6,7].filter(k=>t>=lbv(k)-.25).pop();const inVerse=v!==undefined&&t<lbv(v)+LBV-.25;const L=inVerse?Math.floor((t-lbv(v)+.25)/LBL):-1;
  const q=inVerse?prog(t,lbv(v),lbv(v)+LBV):0;
  const kidsBank=(carry,cheer)=>{builder(0,305,1720,.6,t,carry);builder(2,800,1720,.6,t,carry==='stick'?'stone':carry==='wood'?'clay':carry)};
  const riverScene=!(inVerse&&v===7)&&!(t>=lbv(7)+LBV);if(riverScene){g.save();g.translate(540,1250);g.scale(1.6,1.6);g.translate(-540,-1400)}
  if(t<LB0-.25){river(t);bridgeOld(t,0);fairLady(560,1735,.55,t,{trunk:1});kid(0,250,1720,{s:.6,t,happy:1,noHat:1,noScarf:1,cap:'#FACC15'});
    if(t>2)pop(t,2,'A wobbly old bridge... 😬',540,1090,60,'#fff','#1D4ED8');for(let k=0;k<3;k++){}}
  else if(inVerse&&v===0){river(t);bridgeOld(t,q);fairLady(560,1735,.55,t,{trunk:L===3?1:.5});kid(0,250,1720,{s:.6,t,happy:0,noHat:1,noScarf:1,cap:'#FACC15'});
    for(let k=0;k<6;k++){const p=prog(t,lbv(0)+.5+k*.6,lbv(0)+1.5+k*.6);if(p>0&&p<1)ell(250+k*110,1360,40*p+10,14*p+4,`rgba(255,255,255,${1-p})`)}pop(t,lbl(0,1)+.3,'SPLASH! 💦',540,1090,80,'#fff','#0369A1')}
  else if(inVerse&&(v===1||v===3||v===5)){ // build verses
    const type=v===1?'stone':v===3?'wood':'steel';river(t);if(type==='stone')bridgeStone(t,q);else if(type==='wood')bridgeWood(t,q);else bridgeSteel(t,q);
    const c=v===1?(L%2?'stone':'stick'):v===3?(L%2?'clay':'wood'):'steel';kidsBank(c);fairLady(560,1735,.55,t,{trunk:L===3?1:.5});
    pop(t,lbv(v)+.3,v===1?'Sticks & stones! 🪨':v===3?'Wood & clay! 🪵':'Iron & steel! 🔩',540,1090,66,'#fff','#CA8A04');
    if(L===3)pop(t,lbl(v,3)+.2,'Ta-da! 🎉',540,1170,70,'#fff','#16A34A')}
  else if(inVerse&&v===2){river(t);bridgeStone(t,1,q);kidsBank(null);fairLady(560,1735,.55,t,{});pop(t,lbl(2,1)+.2,'Oh no! 😱',540,1090,80,'#fff','#DC2626')}
  else if(inVerse&&v===4){river(t,{rain:1,rise:clamp(q*2)});bridgeWood(t,1,easeOut(clamp(q*1.4-.2)));kidsBank(null);fairLady(560,1735,.55,t,{});pop(t,lbl(4,1)+.2,'Washing away! 🌊',540,1090,70,'#fff','#0369A1')}
  else if(inVerse&&v===6){river(t);const b=clamp(q*1.5);bridgeSteel(t,1,easeOut(b)*.9);const ex=lerp(-200,540,clamp(q*2));g.save();g.translate(0,220*.9*easeOut(b)*Math.sin(Math.PI*clamp((ex-BX0)/(BX1-BX0))));elephantWalk(ex,t);g.restore();
    kidsBank(null);fairLady(560,1735,.55,t,{});pop(t,lbl(6,1)+.2,'Booiiing! 🐘',540,1060,74,'#fff','#7C3AED')}
  else if(inVerse&&v===7){ // the playground game: arch + catch the fair lady
    sky('#7DD3FC','#E0F2FE');mandalaSun(900,560,60,t);cloud(150,560,1);g.fillStyle='#86EFAC';g.fillRect(0,1350,W,H-1350);
    const close=L===3&&t>lbl(7,3)+.4;const arch=close?0:.6;
    kid(0,400,1820,{s:1.0,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[0],trunk:1});kid(2,680,1820,{s:1.0,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[2],trunk:1,dir:-1});
    g.strokeStyle='#F1C9A5';g.lineWidth=22;g.lineCap='round';g.beginPath();g.moveTo(460,1430);g.quadraticCurveTo(540,1300-arch*120,620,1430);g.stroke();
    const walkers=[[1,0],[3,1],[4,2]];walkers.forEach(([k,i])=>{const x=close&&k===3?540:((t*140+i*300)%1400)-200;const lady=k===3;
      if(lady)fairLady(x,1860,.85,t,{trunk:close?1:.5});else kid(k,x,1860,{s:.85,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[k]})});
    if(close)pop(t,lbl(7,3)+.4,'Caught you! 😆👑',540,1090,76,'#fff','#DB2777');else pop(t,lbv(7)+.2,'Let\'s play London Bridge! 🙌',540,1090,56,'#fff','#1D4ED8')}
  else{ // interludes and outro
    const k=Math.floor((t-LB0)/LBPAIR);
    if(t>=lbv(7)+LBV){sky('#7DD3FC','#E0F2FE');g.fillStyle='#86EFAC';g.fillRect(0,1350,W,H-1350);[[0,150],[1,320],[3,540],[2,760],[4,930]].forEach(([kk,x],i)=>{if(kk===3)fairLady(x,1860-lbpu(t+i*.1)*40,.8,t,{trunk:1});else kid(kk,x,1860-lbpu(t+i*.1)*40,{s:.8,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[kk],trunk:1})});confetti(t,lbv(7)+LBV,50)}
    else if(k===0){river(t);bridgeStone(t,1);const bq=prog(t,lbv(1)+LBV,lbv(2));g.save();g.translate(lerp(-100,1200,bq),1440);ell(0,0,90,24,'#DC2626');rr(-10,-90,8,90,3,'#78350F');g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(-2,-88);g.lineTo(60,-30);g.lineTo(-2,-30);g.fill();g.restore();
      kidsBank(null);fairLady(560,1735,.55,t,{trunk:1});pop(t,lbv(1)+LBV+.5,'Hooray! A bridge! 🎉',540,1090,64,'#fff','#16A34A');if(t>lbv(2)-3)pop(t,lbv(2)-3,'Uh-oh... wobble wobble 😬',540,1170,56,'#fff','#DC2626')}
    else if(k===1){river(t,{rain:prog(t,lbv(3)+LBV,lbv(4))>.5?1:0});bridgeWood(t,1);kidsBank(null);fairLady(560,1735,.55,t,{});pop(t,lbv(3)+LBV+.5,'Rain clouds coming! 🌧️',540,1090,62,'#fff','#475569')}
    else if(k===2){river(t);bridgeSteel(t,1);kidsBank(null);fairLady(560,1735,.55,t,{trunk:1});pop(t,lbv(5)+LBV+.5,'Super strong! 💪',540,1090,66,'#fff','#475569');if(t>lbv(6)-3.5){const ex=lerp(-300,-150,prog(t,lbv(6)-3.5,lbv(6)));elephantWalk(ex,t);pop(t,lbv(6)-3.5,'Here comes a big friend! 🐘',540,1170,54,'#fff','#7C3AED')}}
  }
  if(riverScene)g.restore();
  if(t>=LBCARD){const q2=easeOut(prog(t,LBCARD,LBCARD+.6));g.save();g.globalAlpha=q2*.78;g.fillStyle='#1E3A8A';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q2;
    popcornLogo(W/2,560,.85*backOut(prog(t,LBCARD,LBCARD+.8)),0);txt('A Popcorn Productions video',W/2,900,46,'#FFE14D',null,'center',600);txt('My fair lady! 👑',W/2,1010,72,'#fff','#DB2777');
    const sp=backOut(prog(t,LBCARD+.3,LBCARD+1));g.save();g.translate(W/2,1160);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  const cuts=[];for(let k=0;k<8;k++)cuts.push(lbv(k)-.25);cuts.forEach(c=>{const d=Math.abs(t-c);if(d<.15){g.fillStyle=`rgba(255,255,255,${(1-d/.15)*.6})`;g.fillRect(0,0,W,H)}});
  if(t<LBCARD){lbtitle(t);lbcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,LBEND-.8,LBEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawLondon;
