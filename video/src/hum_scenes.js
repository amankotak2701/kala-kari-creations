// ================= "Humpty Dumpty" — Popcorn Productions =================
const UL=3.43, UBEAT=UL/8;
const UV=[18.4,47.6,90.0];
const ul=(v,l)=>UV[v]+l*UL;
const UP1=119.6, UP2=126.4, UCARD=130.6, UEND=136.6;
const upu=t=>Math.pow(Math.sin(Math.PI*((((t-UV[0])/(2*UBEAT))%1+1)%1)),2);
const WALLX0=230, WALLX1=850, WALLTOP=1300, GROUND=1700;

function humpty(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);if(o.rot)g.rotate(o.rot);
  const sit=o.sit,sw=Math.sin(t*5)*.4;
  // legs
  const leg=(lx,a)=>{g.save();g.translate(lx,-40);g.rotate(a);g.strokeStyle='#1E3A8A';g.lineWidth=14;g.lineCap='round';g.beginPath();g.moveTo(0,0);g.lineTo(0,sit?70:80);g.stroke();ell(sit?6:10,sit?78:86,22,12,'#B91C1C');g.restore()};
  if(!o.split){leg(-35,sit?sw:(o.walk?Math.sin(t*10)*.4:.05));leg(35,sit?-sw:(o.walk?-Math.sin(t*10)*.4:-.05))}
  // arms
  const wv=o.wave?-2.3+Math.sin(t*8)*.4:(o.up?-2.6:.4);
  if(!o.split)[[-1,o.up?-wv:-.4],[1,wv]].forEach(([d,a])=>{g.save();g.translate(d*92,-170);g.rotate(d*a);g.strokeStyle='#1E3A8A';g.lineWidth=12;g.lineCap='round';g.beginPath();g.moveTo(0,0);g.lineTo(0,70);g.stroke();ell(0,78,16,16,'#FFFFFF');g.restore()});
  // egg body
  const eggPath=()=>{g.beginPath();g.moveTo(0,-330);g.bezierCurveTo(95,-330,115,-170,110,-110);g.bezierCurveTo(105,-30,60,0,0,0);g.bezierCurveTo(-60,0,-105,-30,-110,-110);g.bezierCurveTo(-115,-170,-95,-330,0,-330);g.closePath()};
  const drawEgg=()=>{eggPath();const gr=g.createLinearGradient(-110,-330,110,0);gr.addColorStop(0,'#FFFBEB');gr.addColorStop(1,'#F5DEB3');g.fillStyle=gr;g.fill();
    // belt + bow tie
    rr(-108,-120,216,26,8,'#2563EB');rr(-16,-120,32,26,4,'#FBBF24');
    g.fillStyle='#DC2626';g.beginPath();g.moveTo(0,-150);g.lineTo(-38,-172);g.lineTo(-38,-128);g.closePath();g.moveTo(0,-150);g.lineTo(38,-172);g.lineTo(38,-128);g.closePath();g.fill();ell(0,-150,10,10,'#B91C1C');
    // face
    const hy=-235;
    if(o.dizzy){g.strokeStyle='#1F2937';g.lineWidth=5;[[-34],[34]].forEach(([ex])=>{g.beginPath();g.moveTo(ex-12,hy-12);g.lineTo(ex+12,hy+12);g.moveTo(ex+12,hy-12);g.lineTo(ex-12,hy+12);g.stroke()})}
    else if(o.happy){g.strokeStyle='#1F2937';g.lineWidth=6;g.lineCap='round';g.beginPath();g.arc(-34,hy+4,13,Math.PI*1.1,Math.PI*1.9);g.stroke();g.beginPath();g.arc(34,hy+4,13,Math.PI*1.1,Math.PI*1.9);g.stroke()}
    else{ell(-34,hy,15,19,'#FFFFFF');ell(34,hy,15,19,'#FFFFFF');ell(-31,hy+2,9,12,'#1F2937');ell(37,hy+2,9,12,'#1F2937');ell(-28,hy-3,3,3,'#fff');ell(40,hy-3,3,3,'#fff');if(o.scared){ell(-34,hy,15,19,'rgba(255,255,255,.0)')}}
    g.strokeStyle='#1F2937';g.lineWidth=4;g.beginPath();g.moveTo(-52,hy-34);g.quadraticCurveTo(-34,hy-(o.scared?52:44),-16,hy-36);g.moveTo(16,hy-36);g.quadraticCurveTo(34,hy-(o.scared?52:44),52,hy-34);g.stroke();
    ell(-60,hy+34,15,9,'rgba(244,114,182,.5)');ell(60,hy+34,15,9,'rgba(244,114,182,.5)');
    if(o.scared){ell(0,hy+48,18,22,'#7F1D1D')}else{g.fillStyle='#7F1D1D';g.beginPath();g.arc(0,hy+36,30,0,Math.PI);g.fill();ell(0,hy+50,14,8,'#F472B6')}
    if(o.bandage){g.save();g.translate(50,hy-60);g.rotate(.6);rr(-50,-14,100,28,8,'#FDE68A');g.rotate(-1.2);rr(-50,-14,100,28,8,'#FDE68A');ell(0,0,6,6,'#F59E0B');g.restore()}
    if(o.crack!==undefined&&o.crack>0){g.strokeStyle='#78350F';g.lineWidth=6;g.beginPath();const pts=[[-110,-140],[-70,-170],[-40,-135],[0,-175],[40,-135],[75,-172],[110,-140]];const n=Math.ceil(o.crack*pts.length);pts.slice(0,n).forEach(([a,b],k)=>k?g.lineTo(a,b):g.moveTo(a,b));g.stroke()}
    if(o.helmet){g.save();g.beginPath();g.ellipse(0,-280,112,82,0,Math.PI,0);g.fillStyle='#F97316';g.fill();rr(-118,-292,236,22,10,'#EA580C');rr(-14,-358,28,70,10,'#FDBA74');g.restore()}
  };
  if(o.split){ // two halves apart on the ground
    const d=o.split;g.save();g.translate(-d,0);g.rotate(-.35*Math.min(1,d/80));g.beginPath();g.rect(-200,-400,200,420);g.clip();drawEgg();g.restore();
    g.save();g.translate(d,0);g.rotate(.35*Math.min(1,d/80));g.beginPath();g.rect(0,-400,200,420);g.clip();drawEgg();g.restore()}
  else drawEgg();
  if(o.dizzy){for(let k=0;k<4;k++){const a=t*4+k*Math.PI/2;starShape(Math.cos(a)*110,-380+Math.sin(a)*24,16,a,'#FACC15')}}
  g.restore()}
function brickWall(x0,x1,top,bot){rr(x0,top,x1-x0,bot-top,6,'#C2410C');for(let r=0;r*48<bot-top;r++)for(let c=0;c*96<x1-x0+96;c++){const bx=x0+c*96-(r%2)*48;const xa=Math.max(x0,bx),xb=Math.min(x1,bx+92);if(xb>xa)rr(xa,top+r*48+3,xb-xa,42,4,r%2?'#EA580C':'#F97316')}rr(x0-14,top-24,x1-x0+28,30,8,'#9A3412')}
function castleBg(t){sky('#93C5FD','#E0F2FE');cloud(((t*15)%1400)-300,600,1);cloud(((t*10+700)%1400)-300,720,.8);mandalaSun(900,640,60,t);
  g.save();g.globalAlpha=.9;const C='#CBD5E1',D='#94A3B8';rr(140,760,800,560,8,C);for(let k=0;k<11;k++)rr(140+k*76,730,46,40,4,C);
  [[100,600],[900,600],[520,520]].forEach(([x,y])=>{rr(x-60,y,160,760-y+560,8,D);for(let k=0;k<3;k++)rr(x-60+k*58,y-36,40,40,4,D);g.fillStyle='#1D4ED8';g.beginPath();g.moveTo(x-75,y-36);g.lineTo(x+20,y-170);g.lineTo(x+115,y-36);g.fill();g.strokeStyle='#4B5563';g.lineWidth=5;g.beginPath();g.moveTo(x+20,y-170);g.lineTo(x+20,y-240);g.stroke();g.fillStyle='#DC2626';g.beginPath();g.moveTo(x+20,y-240);g.lineTo(x+80+Math.sin(t*4)*8,y-222);g.lineTo(x+20,y-205);g.fill();rr(x,y+80,40,70,20,'#1E3A8A')});
  rr(470,1120,140,200,70,'#78350F');g.restore();
  g.fillStyle='#4ADE80';g.fillRect(0,1320,W,H-1320);for(let k=0;k<16;k++)marigold(rnd(k+40)*W,1760+rnd(k+41)*150,.7,['#F472B6','#FBBF24','#F87171','#FFFFFF'][k%4])}
function soldier(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);const mar=o.march?Math.sin(t*8):0;
  [[-18,mar],[18,-mar]].forEach(([lx,a])=>{g.save();g.translate(lx,-120);g.rotate(a*.3);rr(-12,0,24,120,8,'#1E3A8A');ell(0,120,18,9,'#111');g.restore()});
  rr(-45,-260,90,150,20,'#DC2626');rr(-45,-150,90,14,4,'#FFFFFF');g.strokeStyle='#FFFFFF';g.lineWidth=8;g.beginPath();g.moveTo(-40,-255);g.lineTo(40,-150);g.moveTo(40,-255);g.lineTo(-40,-150);g.stroke();for(let k=0;k<3;k++)ell(0,-235+k*30,5,5,'#FBBF24');
  g.save();g.translate(45,-240);g.rotate(o.salute?-2.4:.2+mar*.2);rr(-10,0,20,80,8,'#DC2626');ell(0,84,11,11,'#F1C9A5');g.restore();
  ell(0,-300,42,40,'#F1C9A5');ell(-14,-300,5,6,'#111');ell(14,-300,5,6,'#111');g.strokeStyle='#7F1D1D';g.lineWidth=3;g.beginPath();g.arc(0,-286,8,.2,Math.PI-.2);g.stroke();
  rr(-40,-430,80,120,36,'#111827');rr(-44,-322,88,10,4,'#FBBF24');
  if(o.drum){rr(-60,-160,120,70,12,'#FDE68A');g.strokeStyle='#DC2626';g.lineWidth=4;for(let k=0;k<5;k++){g.beginPath();g.moveTo(-60+k*30,-160);g.lineTo(-45+k*30,-90);g.stroke()}}
  g.restore()}
function royalHorse(x,y,s,t,o={}){pony(x,y,s,t,o.run??1,0);g.save();g.translate(x,y);g.scale(s,s);g.fillStyle='#7C3AED';g.beginPath();g.moveTo(130,-300);g.quadraticCurveTo(110,-370,150,-380);g.quadraticCurveTo(140,-340,145,-300);g.fill();
  g.fillStyle='#1D4ED8';g.beginPath();g.moveTo(-70,-190);g.lineTo(60,-190);g.lineTo(80,-110);g.lineTo(-90,-110);g.closePath();g.fill();for(let k=0;k<6;k++)ell(-80+k*30,-108,8,10,'#FBBF24');g.restore()}
function pillow(x,y,s,t,squash=0){g.save();g.translate(x,y);g.scale(s*(1+squash*.25),s*(1-squash*.35));ell(0,-60,260,70,'#F9A8D4');ell(-150,-90,90,46,'#FBCFE8');ell(140,-92,96,48,'#FBCFE8');ell(0,-110,120,40,'#FDE2F3');
  g.strokeStyle='#EC4899';g.lineWidth=5;g.setLineDash([12,10]);g.beginPath();g.ellipse(0,-60,240,56,0,0,7);g.stroke();g.setLineDash([]);g.restore()}
function utitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#2563EB';g.beginPath();g.roundRect(-370,-66,740,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FBBF24';g.stroke();txt('Humpty Dumpty 🥚',0,2,60,'#FFFFFF',null);g.restore()}
const ULYR=['Humpty Dumpty sat on a wall,','Humpty Dumpty had a great fall.','All the king\'s horses and all the king\'s men','couldn\'t put Humpty together again!'];
const UCAPS=[];UV.forEach(v0=>{for(let k=0;k<4;k++)UCAPS.push([v0+k*UL-.3,v0+(k+1)*UL-.3,ULYR[k]])});UCAPS.push([UP1-.3,UP1+UL,ULYR[0]]);UCAPS.push([UP2-.3,UP2+UL,ULYR[1]]);
function ucap(t){const i=UCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=UCAPS[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 60px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*74+40,y0=390;g.fillStyle='rgba(30,58,138,.88)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#FBBF24';g.stroke();
  const prg=clamp((t-a)/((b-a)*.9));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+37+li*74,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}
const UKIDS=[[0,150],[1,330],[3,750],[2,930]];
function ukids(t,o={}){UKIDS.forEach(([k,x],i)=>kid(k,x,1850-(o.jump?Math.max(0,Math.sin(t*Math.PI/(2*UBEAT)+i))*50:0),{s:.72,dir:x<540?1:-1,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[k],trunk:o.cheer?1:.5}))}
// one verse of the rhyme. mode: 'crash' (breaks), 'pillow' (safe landing)
function verse(t,v,mode){const L=Math.floor((t-UV[v])/UL);const lt=t-ul(v,L);
  castleBg(t);brickWall(WALLX0,WALLX1,WALLTOP,GROUND);
  if(mode==='pillow')pillow(540,GROUND+60,1.1,t,t>ul(v,1)+1.3&&t<ul(v,1)+1.7?1:0);
  const fallT0=ul(v,1)+.6,fallT1=fallT0+.8;
  if(t<fallT0){humpty(540,WALLTOP-4,.95,t,{sit:1,wave:L===0,helmet:v===2,bandage:v>=1,scared:L===1,rot:L===1?Math.sin(t*14)*.12:0});
    if(L===1&&t>ul(v,1)+.1)pop(t,ul(v,1)+.1,'Whoa! 😱',540,860,72,'#fff','#DC2626')}
  else if(t<fallT1){const q=prog(t,fallT0,fallT1);humpty(540+q*60,lerp(WALLTOP,GROUND+(mode==='pillow'?-10:20),q*q),.95,t,{rot:q*1.4,scared:1,helmet:v===2,bandage:v>=1})}
  else if(mode==='pillow'){const b=prog(t,fallT1,fallT1+1.6);const hop=Math.sin(Math.PI*b)*520*(b<1?1:0);humpty(600,GROUND-10-hop,.95,t,{happy:1,up:1,helmet:1,bandage:1,rot:b<1?b*Math.PI*2:0});
    pop(t,fallT1,'BOING! 🎈',540,820,90,'#fff','#EC4899');if(L>=3)pop(t,ul(v,3),'He\'s OK! 🎉',540,900,84,'#fff','#16A34A')}
  else{const sp=Math.min(80,(t-fallT1)*300);humpty(600,GROUND+30,.95,t,{split:sp,dizzy:1,bandage:v>=1});pop(t,fallT1,'CRACK! 💥',540,860,90,'#fff','#B45309')}
  if(L>=2){const q=easeOut(prog(t,ul(v,2),ul(v,2)+1.6));
    royalHorse(lerp(-300,150,q),1720,.55,t,{run:q<1});soldier(lerp(1300,900,q),1820,.8,t,{march:q<1,dir:-1,drum:1,salute:mode==='pillow'});soldier(lerp(1450,760,q),1840,.75,t,{march:q<1,dir:-1,salute:mode==='pillow'});
    if(mode!=='pillow'&&L===3){const tq=prog(t,ul(v,3),ul(v,3)+UL);const push=Math.abs(Math.sin(tq*Math.PI*3));if(lt>2.4)pop(t,ul(v,3)+2.4,'Oh no! 😢',540,860,80,'#fff','#1D4ED8');else pop(t,ul(v,3)+.2,'Push! 💪',540,860,70,'#fff','#7C3AED')}}
}
function drawHumpty(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  if(t<UV[0]-.2){ // intro: Humpty waddles in and climbs the ladder
    castleBg(t);brickWall(WALLX0,WALLX1,WALLTOP,GROUND);
    rr(870,1280,18,430,6,'#92400E');rr(950,1280,18,430,6,'#92400E');for(let k=0;k<8;k++)rr(870,1300+k*52,98,12,4,'#B45309');
    if(t<9){const q=easeOut(prog(t,2,9));humpty(lerp(-150,1000,q),GROUND+10,.8,t,{walk:q<1,happy:q>.9});if(t>2.5)pop(t,2.5,'Hello! I\'m Humpty! 🥚',540,880,62,'#fff','#2563EB')}
    else if(t<14){const q=prog(t,9,14);humpty(920,lerp(GROUND+10,WALLTOP-20,q),.8,t,{walk:1})}
    else{const q=easeOut(prog(t,14,16.5));humpty(lerp(920,540,q),WALLTOP-4,lerp(.8,.95,q),t,{sit:q>.95,walk:q<.95,happy:1})}
    const q=backOut(prog(t,.4,1.4));if(t<2.5){g.save();g.translate(540,880);g.scale(q,q);txt('🥁 Ta-da!',0,0,80,'#fff','#7C3AED');g.restore()}
  }
  else if(t<ul(0,4)-.3)verse(t,0,'crash');
  else if(t<UV[1]-.3){ // interlude 1: kids fix Humpty with bandages
    castleBg(t);brickWall(WALLX0,WALLX1,WALLTOP,GROUND);const q=prog(t,ul(0,4),UV[1]-1.5);
    ukids(t,{cheer:q>.7});
    if(q<.45){humpty(600,GROUND+30,.95,t,{split:Math.max(0,80*(1-q/.45)),dizzy:q<.3});if(t<ul(0,4)+3)pop(t,ul(0,4)+.3,'We can help! 🩹',540,860,70,'#fff','#DB2777')}
    else{humpty(560,GROUND+30,.95,t,{happy:1,bandage:1,up:q>.7});pop(t,ul(0,4)+(UV[1]-ul(0,4))*.5,'Good as new! ✨',540,860,74,'#fff','#16A34A');for(let k=0;k<8;k++){const a=t*2+k;starShape(560+Math.cos(a)*170,1550+Math.sin(a)*120,12,a,'#FDE047')}}
    if(t>UV[1]-2){const p=prog(t,UV[1]-2,UV[1]-.3)}
  }
  else if(t<ul(1,4)-.3)verse(t,1,'crash');
  else if(t<UV[2]-.3){ // long interlude: fix again, helmet, pillow, dance party
    castleBg(t);brickWall(WALLX0,WALLX1,WALLTOP,GROUND);const s0=ul(1,4);const q=prog(t,s0,UV[2]-.3);
    if(q<.25){humpty(600,GROUND+30,.95,t,{split:Math.max(0,80*(1-q/.25)),dizzy:q<.18,bandage:1});ukids(t,{});pop(t,s0+.3,'Again?! 😅',540,860,74,'#fff','#DB2777')}
    else if(q<.5){humpty(560,GROUND+30,.95,t,{happy:1,bandage:1,helmet:q>.38});ukids(t,{cheer:1});pop(t,s0+(UV[2]-s0)*.38,'Safety helmet! ⛑️',540,860,70,'#fff','#EA580C')}
    else if(q<.7){const pq=easeOut(prog(q,.5,.62));pillow(540,GROUND+60,1.1*pq,t);humpty(560,GROUND-150,.8,t,{happy:1,bandage:1,helmet:1,up:1});ukids(t,{cheer:1});pop(t,s0+(UV[2]-s0)*.52,'A soft pillow! 🛏️',540,860,70,'#fff','#EC4899')}
    else{pillow(540,GROUND+60,1.1,t);const tt=(t-s0);humpty(540,GROUND-120-Math.abs(Math.sin(t*Math.PI/(2*UBEAT)))*80,.8,t,{happy:1,bandage:1,helmet:1,up:1,rot:Math.sin(t*4)*.15});
      royalHorse(150,1720,.5,t,{run:0});soldier(900,1820,.75,t,{dir:-1,drum:1});ukids(t,{jump:1,cheer:1});notes(300,1300,t,s0,5);notes(780,1300,t,s0+.4,5);
      if(q>.9){const cq=prog(q,.9,1);humpty(540,lerp(GROUND-120,WALLTOP,cq),.0001,t,{})}}
  }
  else if(t<ul(2,4)-.3)verse(t,2,'pillow');
  else if(t<UCARD){ // celebration + short sung lines on a safe low step
    castleBg(t);pillow(540,GROUND+60,1.1,t);rr(330,1500,420,200,8,'#F97316');brickWall(330,750,1500,1700);
    const fallen=t>UP2+.8;
    if(!fallen)humpty(540,1500,.85,t,{sit:1,happy:1,helmet:1,bandage:1,wave:1});else{const b=prog(t,UP2+.8,UP2+2);humpty(560,GROUND-10-Math.sin(Math.PI*b)*300*(b<1?1:0),.85,t,{happy:1,up:1,helmet:1,bandage:1})}
    if(t>UP2+.8)pop(t,UP2+.8,'Boing! 😄',540,880,80,'#fff','#EC4899');
    royalHorse(130,1740,.45,t,{run:0});soldier(930,1830,.7,t,{dir:-1,drum:1,salute:1});ukids(t,{jump:1,cheer:1});confetti(t,ul(2,4),40);
  }
  else{ // end card
    castleBg(t);pillow(540,GROUND+60,1.1,t);humpty(540,GROUND-10,.85,t,{happy:1,up:1,helmet:1,bandage:1});ukids(t,{cheer:1});
    const q=easeOut(prog(t,UCARD,UCARD+.8));g.save();g.globalAlpha=q*.72;g.fillStyle='#1E3A8A';g.fillRect(0,0,W,1450);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,UCARD,UCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Be safe, Humpty! 🥚⛑️',W/2,990,72,'#fff','#2563EB');
    const sp=backOut(prog(t,UCARD+.6,UCARD+1.4));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  [UV[0]-.2,ul(0,4)-.3,UV[1]-.3,ul(1,4)-.3,UV[2]-.3,ul(2,4)-.3,UCARD].forEach(c=>{const d=Math.abs(t-c);if(d<.18){g.fillStyle=`rgba(255,255,255,${(1-d/.18)*.6})`;g.fillRect(0,0,W,H)}});
  if(t<UCARD){utitle(t);ucap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,UEND-1.2,UEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawHumpty;
