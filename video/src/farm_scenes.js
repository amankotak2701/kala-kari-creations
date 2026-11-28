// ================= "Old MacDonald Had A Farm" — Popcorn Productions =================
const FL2=2.6085, FV0=7.55, FVER=10*FL2;          // line = 2 bars; verse = 8 lines + 2 lines interlude
const fv=k=>FV0+k*FVER, fl=(v,l)=>fv(v)+l*FL2;
const FTAG=fl(4,8), FTAGEND=FTAG+2*FL2, FCARD=FTAGEND+.2, FEND2=144.0;
const fbt=FL2/4;
const fpu=t=>Math.pow(Math.sin(Math.PI*((((t-FV0)/fbt)%1+1)%1)),2);
const ANIMALS=[{n:'cow',a:'a cow',s:'moo',S:'Moo!',c:'#16A34A'},{n:'pig',a:'a pig',s:'oink',S:'Oink!',c:'#EC4899'},{n:'dog',a:'a dog',s:'woof',S:'Woof!',c:'#B45309'},{n:'duck',a:'some ducks',s:'quack',S:'Quack!',c:'#CA8A04'},{n:'sheep',a:'some sheep',s:'baa',S:'Baa!',c:'#64748B'}];
FAM.farmer={skin:'#E0AE85',hair:'#9CA3AF',style:'short',top:'#DC2626',bottom:'#2563EB',beard:'#D1D5DB'};

function cow(x,y,s,t,o={}){const d=o.dir||1;g.save();g.translate(x,y-(o.hop?Math.abs(Math.sin(t*Math.PI/fbt))*30:0));g.scale(s*d,s);
  const lg=(lx,p)=>{const a=o.walk?Math.sin(t*7+p)*.3:0;g.save();g.translate(lx,-110);g.rotate(a);rr(-16,0,32,110,12,'#FFFFFF');rr(-16,92,32,20,6,'#3F2A1E');g.restore()};
  lg(-90,0);lg(70,Math.PI);
  g.save();g.translate(-150,-190);g.rotate(Math.sin(t*4)*.3);g.strokeStyle='#FFFFFF';g.lineWidth=10;g.beginPath();g.moveTo(0,0);g.quadraticCurveTo(-30,40,-20,90);g.stroke();ell(-20,98,12,18,'#3F2A1E');g.restore();
  ell(0,-180,165,95,'#FFFFFF');ell(-60,-200,50,36,'#1F2937',.3);ell(50,-150,40,30,'#1F2937',-.2);ell(-100,-140,30,22,'#1F2937');ell(10,-112,40,18,'#F9A8D4');
  lg(-60,Math.PI);lg(100,0);
  g.save();g.translate(170,-250);ell(-55,-40,30,14,'#FFFFFF',-.5);ell(55,-40,30,14,'#FFFFFF',.5);ell(-55,-40,18,8,'#F9A8D4',-.5);
  g.fillStyle='#FDE68A';g.beginPath();g.moveTo(-30,-60);g.quadraticCurveTo(-40,-100,-20,-105);g.lineTo(-18,-62);g.fill();g.beginPath();g.moveTo(30,-60);g.quadraticCurveTo(40,-100,20,-105);g.lineTo(18,-62);g.fill();
  ell(0,0,70,72,'#FFFFFF');ell(-30,-30,22,18,'#1F2937');ell(0,40,58,38,'#F9A8D4');ell(-20,40,8,10,'#BE185D');ell(20,40,8,10,'#BE185D');
  ell(-24,-12,10,13,'#111');ell(24,-12,10,13,'#111');ell(-21,-16,3,3,'#fff');ell(27,-16,3,3,'#fff');g.restore();
  rr(130,-185,80,16,8,'#DC2626');bell(170,-150,.3,Math.sin(t*6)*.4);g.restore()}
function pig(x,y,s,t,o={}){const d=o.dir||1;g.save();g.translate(x,y-(o.hop?Math.abs(Math.sin(t*Math.PI/fbt))*30:0));g.scale(s*d,s);const P='#F9A8D4',D='#F472B6';
  const lg=(lx)=>{rr(lx-14,-60,28,60,10,D);rr(lx-14,-12,28,12,4,'#9D174D')};lg(-70);lg(50);
  g.strokeStyle=D;g.lineWidth=8;g.beginPath();g.moveTo(-125,-120);for(let k=0;k<20;k++){const a=k*.6;g.lineTo(-135-k*1.5+Math.cos(a)*10,-120+Math.sin(a)*10-k)}g.stroke();
  ell(0,-110,130,85,P);ell(-20,-80,60,30,'rgba(255,255,255,.25)');lg(-40);lg(80);
  g.save();g.translate(120,-150);g.fillStyle=D;g.beginPath();g.moveTo(-40,-50);g.lineTo(-20,-95);g.lineTo(0,-55);g.fill();g.beginPath();g.moveTo(10,-55);g.lineTo(40,-95);g.lineTo(45,-45);g.fill();
  ell(0,0,70,64,P);ell(40,15,34,26,D);ell(32,15,6,9,'#9D174D');ell(50,15,6,9,'#9D174D');ell(-12,-15,9,12,'#111');ell(20,-18,9,12,'#111');ell(-9,-19,3,3,'#fff');ell(23,-22,3,3,'#fff');
  g.strokeStyle='#9D174D';g.lineWidth=4;g.beginPath();g.arc(10,35,14,.3,Math.PI-.3);g.stroke();ell(-30,15,12,7,'rgba(236,72,153,.5)');g.restore();g.restore()}
function farmer(x,y,s,t,o={}){adult('farmer',x,y,Object.assign({s,t,happy:1},o));
  g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);if(o.rot)g.rotate(o.rot);
  // overalls straps + bib
  rr(-50,-330,22,120,6,'#2563EB');rr(28,-330,22,120,6,'#2563EB');rr(-50,-250,100,90,10,'#2563EB');ell(-38,-322,7,7,'#FBBF24');ell(38,-322,7,7,'#FBBF24');
  // straw hat
  g.save();g.translate(0,-445);ell(0,8,110,26,'#EAB308');ell(0,-18,62,44,'#FACC15');rr(-62,-8,124,18,6,'#B91C1C');for(let k=0;k<6;k++){g.strokeStyle='#CA8A04';g.lineWidth=3;g.beginPath();g.moveTo(-90+k*36,0);g.lineTo(-80+k*36,16);g.stroke()}g.restore();
  g.restore()}
function barn(x,y,s,t,doorOpen=0){g.save();g.translate(x,y);g.scale(s,s);
  g.fillStyle='#B91C1C';g.beginPath();g.moveTo(-240,0);g.lineTo(-240,-280);g.lineTo(-180,-400);g.lineTo(180,-400);g.lineTo(240,-280);g.lineTo(240,0);g.closePath();g.fill();
  g.fillStyle='#7F1D1D';g.beginPath();g.moveTo(-260,-270);g.lineTo(-190,-420);g.lineTo(190,-420);g.lineTo(260,-270);g.lineTo(240,-270);g.lineTo(180,-395);g.lineTo(-180,-395);g.lineTo(-240,-270);g.closePath();g.fill();
  rr(-50,-350,100,80,6,'#FDE68A');g.strokeStyle='#fff';g.lineWidth=6;g.strokeRect(-50,-350,100,80);
  rr(-130,-200,260,200,6,'#3F1D0E');
  [[-1],[1]].forEach(([dd])=>{g.save();g.translate(dd*130,-200);g.scale(dd*(1-doorOpen*.85),1);g.fillStyle='#DC2626';g.fillRect(-130,0,130,200);g.strokeStyle='#fff';g.lineWidth=10;g.strokeRect(-130,0,130,200);g.beginPath();g.moveTo(-130,0);g.lineTo(0,200);g.moveTo(0,0);g.lineTo(-130,200);g.stroke();g.restore()});
  g.restore()}
function silo(x,y,s){g.save();g.translate(x,y);g.scale(s,s);rr(-70,-420,140,420,10,'#9CA3AF');ell(0,-420,70,50,'#6B7280');for(let k=0;k<6;k++){g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=4;g.beginPath();g.moveTo(-70,-60-k*60);g.lineTo(70,-60-k*60);g.stroke()}g.restore()}
function farmBg(t,o={}){sky('#7DD3FC','#E0F2FE');if(!o.noSun)mandalaSun(880,620,70,t);cloud(((t*20)%1400)-300,560,1);cloud(((t*12+700)%1400)-300,680,.8);
  [['#86EFAC',1240,60,.004],['#4ADE80',1310,45,.006]].forEach(([c,y,a,f],k)=>{g.fillStyle=c;g.beginPath();g.moveTo(0,H);for(let x=0;x<=W;x+=20)g.lineTo(x,y+Math.sin(x*f+k)*a);g.lineTo(W,H);g.fill()});
  for(let k=0;k<7;k++){g.strokeStyle='rgba(22,101,52,.35)';g.lineWidth=8;g.beginPath();g.moveTo(600+k*80,1260);g.lineTo(560+k*110,1370);g.stroke()}
  silo(80,1330,.7);barn(300,1400,.85,t,o.door||0);
  ell(920,1360,80,50,'#FACC15');ell(900,1340,60,30,'#FDE047');
  g.fillStyle='#22C55E';g.fillRect(0,1380,W,H-1380);
  for(let k=0;k<12;k++){rr(k*95,1440,18,110,4,'#A16207')}rr(-10,1460,W+20,16,4,'#CA8A04');rr(-10,1510,W+20,16,4,'#CA8A04');
  for(let k=0;k<14;k++)marigold(rnd(k)*W,1580+rnd(k+3)*300,.7,['#F472B6','#FBBF24','#F87171','#FFFFFF'][k%4])}
function drawAnimal(i,x,y,s,t,o={}){const n=ANIMALS[i].n;
  if(n==='cow')cow(x,y,s,t,o);else if(n==='pig')pig(x,y,s*1.1,t,o);else if(n==='dog')puppy(x-80*s,y,s*1.4,t,o.hop?Math.abs(Math.sin(t*Math.PI/fbt))*30:0);
  else if(n==='duck'){for(let k=0;k<3;k++)duck(x-120*s+k*120*s,y-(k%2)*20*s,s*1.3,t,k)}else lamb(x,y,s*1.05,t,o)}
function bubble(x,y,s,txtS,col){g.save();g.translate(x,y);g.scale(s,s);ell(0,0,130,70,'#FFFFFF');g.lineWidth=6;g.strokeStyle=col;g.stroke();g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(-30,55);g.lineTo(-60,110);g.lineTo(10,62);g.fill();txt(txtS,0,4,62,col,null);g.restore()}
function eieio(t,t0){const L='EIEIO',cols=['#EF4444','#F59E0B','#22C55E','#3B82F6','#A855F7'];for(let k=0;k<5;k++){const tk=t0+k*fbt*.8;const p=prog(t,tk,tk+.35);if(p<=0)continue;
  const s=backOut(p);const fade=clamp((t0+FL2+.3-t)/.4);g.save();g.globalAlpha=fade;g.translate(200+k*170,900-Math.sin(k/4*Math.PI)*60+Math.sin(t*6+k)*8);g.scale(s,s);txt(L[k],0,0,140,cols[k],'#FFFFFF');g.restore()}}
function ftitle2(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#16A34A';g.beginPath();g.roundRect(-430,-66,860,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Old MacDonald Had A Farm 🚜',0,2,50,'#FFFFFF',null);g.restore()}
const FCAPS=[];ANIMALS.forEach((A,v)=>{const s2=A.s+' '+A.s;
  FCAPS.push([fl(v,0)-.25,fl(v,2)-.25,'Old MacDonald had a farm, E-I-E-I-O!']);
  FCAPS.push([fl(v,2)-.25,fl(v,4)-.25,`And on his farm he had ${A.a}, E-I-E-I-O!`]);
  FCAPS.push([fl(v,4)-.25,fl(v,6)-.25,`With a ${s2} here and a ${s2} there, here a ${A.s}, there a ${A.s}, everywhere a ${s2}!`]);
  FCAPS.push([fl(v,6)-.25,fl(v,8)+.2,'Old MacDonald had a farm, E-I-E-I-O!'])});
FCAPS.push([FTAG-.25,FTAGEND+.3,'Old MacDonald had a farm, E-I-E-I-O! 🎉']);
function fcap2(t){const i=FCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=FCAPS[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 56px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*70+40,y0=400;g.fillStyle='rgba(120,53,15,.88)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.92));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+35+li*70,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}
// friends gathered so far (small, along the fence)
function friends(t,upto,y=1760){const xs=[150,330,520,710,900];for(let i=0;i<upto;i++){drawAnimal(i,xs[i],Math.min(y,1800),.58,t,{hop:fpu(t+i*.1)>.6,dir:i%2?-1:1})}}

function drawFarm(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  if(t<FV0-.2){ // intro: tractor rolls in, farmer waves
    farmBg(t);const q=easeOut(prog(t,.4,5));
    g.save();g.translate(lerp(-300,760,q),1700);rr(-120,-160,170,110,14,'#16A34A');rr(-20,-230,90,90,10,'#15803D');rr(-10,-220,60,60,6,'#BFE6FF');rr(30,-100,140,60,10,'#16A34A');
    wheel(-60,-55,70,q*20);wheel(140,-35,45,q*20);g.restore();
    farmer(330,1720,1.0,t,{pose:'wave'});
    if(t>2){const p=backOut(prog(t,2,3));g.save();g.translate(540,960);g.scale(p,p);txt('Welcome to the farm! 🌾',0,0,72,'#fff','#15803D');g.restore()}
  }
  else if(t<FTAG-.2){
    const v=Math.min(4,Math.floor((t-FV0+.2)/FVER));const l=Math.floor((t-fv(v))/FL2);const A=ANIMALS[v];
    const door=l>=2&&l<4?easeOut(prog(t,fl(v,2),fl(v,2)+.6)):(l<2?0:1);
    farmBg(t,{door});
    if(l<2){ // Old MacDonald had a farm: farmer dances, friends so far
      farmer(540,1720,1.15,t,{pose:fpu(t)>.5?'up':'clap',rot:Math.sin(t*4)*.06});friends(t,v,1840);eieio(t,fl(v,1))}
    else if(l<4){ // animal comes out of the barn
      const q=easeOut(prog(t,fl(v,2)+.4,fl(v,3)));farmer(860,1740,1.0,t,{pose:'wave',dir:-1});
      drawAnimal(v,lerp(300,560,q),lerp(1440,1740,q),lerp(.45,1.0,q),t,{walk:q<1,hop:q>=1&&fpu(t)>.7});
      if(q>.9)bubble(700,1050,1,A.S,A.c);eieio(t,fl(v,3))}
    else if(l<6){ // here / there / everywhere
      const sub=Math.floor((t-fl(v,4))/(FL2/2));
      drawAnimal(v,540,1740,1.0,t,{hop:fpu(t)>.6});
      if(l===4){bubble(sub%2?820:260,1000,1,A.s+' '+A.s,A.c);txt(sub%2?'there 👉':'👈 here',sub%2?820:260,1140,52,'#fff',A.c)}
      else{for(let k=0;k<8;k++){const tk=fl(v,5)+k*FL2/8;const p=backOut(prog(t,tk,tk+.3));if(p>0)bubble(160+rnd(k+v*9)*760,900+rnd(k+v*9+3)*420,.55*p,A.S,A.c)}
        if(t>fl(v,5)+FL2/2)txt('everywhere! 🎉',540,1500,64,'#fff',A.c)}}
    else if(l<8){ // whole gang dances
      farmer(540,1700,1.0,t,{pose:'up',rot:Math.sin(t*5)*.06});friends(t,v+1,1840);eieio(t,fl(v,7))}
    else{ // interlude: parade to the next verse
      const q=prog(t,fl(v,8),fv(v+1));const xs=[0,1,2,3,4].slice(0,v+1);
      xs.forEach((i,k)=>drawAnimal(i,((q*1400+k*250)%1500)-200,1760,.6,t,{walk:1,hop:fpu(t+k*.1)>.6}));
      farmer(860,1700,.9,t,{pose:'clap',dir:-1});
      if(v<4){const nx=ANIMALS[v+1];const p=backOut(prog(t,fv(v+1)-2.2,fv(v+1)-1.4));if(p>0){g.save();g.translate(540,980);g.scale(p,p);txt('Who\'s next? 🤔',0,0,76,'#fff','#7C3AED');g.restore()}}}
  }
  else{ // final tag + end card
    farmBg(t,{door:1});farmer(540,1640,.95,t,{pose:'up',rot:Math.sin(t*5)*.06});friends(t,5,1840);
    if(t<FCARD)eieio(t,FTAG+FL2);
    if(t>FTAG)confetti(t,FTAG,60);
    if(t>=FCARD){const q=easeOut(prog(t,FCARD,FCARD+.8));g.save();g.globalAlpha=q*.7;g.fillStyle='#14532D';g.fillRect(0,0,W,1450);g.restore();g.save();g.globalAlpha=q;
      popcornLogo(W/2,520,.85*backOut(prog(t,FCARD,FCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('E-I-E-I-O! 🐮🐷🐶',W/2,990,74,'#fff','#15803D');
      const sp=backOut(prog(t,FCARD+.6,FCARD+1.4));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  }
  const cuts=[FV0-.2];for(let v=0;v<5;v++)cuts.push(fl(v,2),fl(v,4),fl(v,6),fl(v,8));cuts.forEach(c=>{const d=Math.abs(t-c);if(d<.15){g.fillStyle=`rgba(255,255,255,${(1-d/.15)*.6})`;g.fillRect(0,0,W,H)}});
  if(t<FCARD){ftitle2(t);fcap2(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,FEND2-1.2,FEND2);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawFarm;
