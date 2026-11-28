// ================= "Pop Goes the Weasel" — Popcorn Productions =================
const PWL=2.182, PWA=[18.31,54.31,108.6];
const PWCARD=116.6, PWEND=119.4;
const PWLY={A:['All around the mulberry bush,','The monkey chased the weasel.','The monkey thought \'twas all in fun,','POP! goes the weasel!'],
  B:['A penny for a spool of thread,','A penny for a needle.','That\'s the way the money goes,','POP! goes the weasel!']};
const PWSEC=[[PWA[0],'A'],[PWA[0]+4*PWL,'B'],[PWA[1],'A'],[PWA[1]+4*PWL,'B'],[PWA[2],'A']];
const PWCAPS=[];PWSEC.forEach(([s0,k])=>PWLY[k].forEach((s,l)=>PWCAPS.push([s0+l*PWL-.25,s0+(l+1)*PWL-.25+(l===3?.6:0),s])));
const pwSec=t=>PWSEC.findIndex(([s0])=>t>=s0-.25&&t<s0+4*PWL-.25);
const pwhop=t=>Math.abs(Math.sin(Math.PI*(t-.49)/.5455));

function pwGarden(t,o={}){sky(o.dusk?'#FB923C':'#7DD3FC',o.dusk?'#FDE68A':'#E0F2FE');mandalaSun(860,1000,60,t,o.dusk?'#FDBA74':'#FFC94A');
  cloud(((t*14)%1500)-300,1060,.7);cloud(((t*9+700)%1500)-300,1180,.55);hills(t,'#A3E635','#84CC16','#65A30D');
  g.fillStyle='#4ADE80';g.fillRect(0,1500,W,H-1500);ell(540,1720,470,130,'#86EFAC');
  for(let k=0;k<10;k++)marigold(40+rnd(k)*1000,1560+rnd(k+3)*330,.75,['#F472B6','#FBBF24','#F87171','#A78BFA'][k%4])}
function chase(t,spd,o={}){ // monkey chases weasel round the bush
  const a=t*spd,list=[['w',a],['m',a-.85]];const pos=b=>[540+Math.cos(b)*360,1700+Math.sin(b)*110,Math.sin(b)];
  const draw=([who,b])=>{const [x,y]=pos(b),dir=-Math.sin(b)>0?-1:1,sc=.9+Math.sin(b)*.08;if(who==='w')weasel(x,y,sc*.85,t,{dir,hop:pwhop(t)*20,surprised:o.wSur});else monkey(x,y,sc,t,{dir,run:1,surprised:o.mSur})};
  list.filter(e=>Math.sin(e[1])<0).forEach(draw);mulberryBush(540,1720,o.bushS||.95,t);list.filter(e=>Math.sin(e[1])>=0).forEach(draw)}
function popUp(t,t0,o={}){ // weasel pops up from behind the bush
  const p=prog(t,t0,t0+.35),q=prog(t,t0+1.6,t0+2.1);const up=backOut(p)*(1-easeOut(q));
  mulberryBush(540,1720,.95,t);g.save();g.beginPath();g.rect(0,0,W,1560);g.clip();weasel(540,1560+(1-up)*420,1.0,t,{stretch:1+up*.25,surprised:0,wave:up>.8});g.restore();
  monkey(250,1820,1.0,t,{dir:1,surprised:p>0&&p<1||up>.5,up:up>.5});popBurst(540,1080,t,t0)}
function jackBox(x,y,s,t,pop,p){g.save();g.translate(x,y);g.scale(s,s);
  rr(-110,-200,220,200,14,'#EF4444');[['#FDE047',-90],['#3B82F6',-30],['#22C55E',30]].forEach(([c,dx],i)=>{ell(dx+30,-100,22,22,c)});g.strokeStyle='#fff';g.lineWidth=6;g.strokeRect(-110,-200,220,200);
  g.save();g.translate(110,-110);g.rotate(pop?0:t*6);rr(-6,-6,60,12,6,'#94A3B8');ell(54,0,14,14,'#FDE047');g.restore();
  if(!pop){rr(-120,-224,240,30,10,'#B91C1C')}
  else{g.save();g.translate(-110,-206);g.rotate(-1.9*easeOut(Math.min(1,p*4)));rr(0,-15,240,30,10,'#B91C1C');g.restore();
    const h=backOut(Math.min(1,p*3))*200;g.strokeStyle='#94A3B8';g.lineWidth=10;g.beginPath();for(let k=0;k<=10;k++){g.lineTo((k%2?-30:30),-200-k*h/10)}g.stroke();
    g.save();g.translate(0,-200-h+60);weasel(0,0,1.15,t,{surprised:p<.4,wave:p>.4});g.restore()}
  g.restore()}
function sewingShop(t){const w=g.createLinearGradient(0,0,0,1500);w.addColorStop(0,'#FDF2F8');w.addColorStop(1,'#FBCFE8');g.fillStyle=w;g.fillRect(0,0,W,1500);
  for(let k=0;k<14;k++)for(let j=0;j<12;j++)ell(40+k*80+(j%2)*40,520+j*90,6,6,'rgba(236,72,153,.18)');
  // shelves with spools
  for(let r=0;r<2;r++){rr(80,1060+r*180,920,22,6,'#92400E');for(let k=0;k<9;k++){const c=['#EF4444','#3B82F6','#22C55E','#FDE047','#A855F7','#F97316'][(k+r*2)%6];const x=130+k*100,y=1060+r*180;rr(x-22,y-80,44,80,6,'#D6B48A');rr(x-18,y-74,36,68,4,c);for(let l=0;l<5;l++){g.strokeStyle='rgba(255,255,255,.35)';g.lineWidth=2;g.beginPath();g.moveTo(x-18,y-68+l*13);g.lineTo(x+18,y-62+l*13);g.stroke()}}}
  g.fillStyle='#A16207';g.fillRect(0,1500,W,H-1500);for(let k=0;k<12;k++){g.strokeStyle='rgba(0,0,0,.12)';g.lineWidth=4;g.beginPath();g.moveTo(k*100,1500);g.lineTo(k*100-60,H);g.stroke()}
  // shop sign
  rr(330,930,420,90,30,'#EC4899');txt('🧵 Sewing Shop',540,976,52,'#fff',null)}
function counter(){rr(380,1500,700,240,16,'#B45309');rr(360,1480,740,40,12,'#92400E');for(let k=0;k<5;k++)rr(420+k*130,1560,90,140,10,'#D97706')}
function penny(x,y,s,rot=0){g.save();g.translate(x,y);g.scale(Math.cos(rot)*s,s);ell(0,0,30,30,'#F59E0B');g.lineWidth=4;g.strokeStyle='#B45309';g.beginPath();g.arc(0,0,24,0,7);g.stroke();txt('1¢',0,2,26,'#92400E',null);g.restore()}
function spool(x,y,s,c='#3B82F6'){g.save();g.translate(x,y);g.scale(s,s);rr(-30,-70,60,14,4,'#D6B48A');rr(-30,0,60,14,4,'#D6B48A');rr(-22,-58,44,60,6,c);g.restore()}
function needle(x,y,s,rot){g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);g.fillStyle='#CBD5E1';g.beginPath();g.moveTo(0,-80);g.lineTo(6,60);g.lineTo(0,80);g.lineTo(-6,60);g.closePath();g.fill();ell(0,-62,3,8,'#fff');g.restore()}

function verseA(t,s0,dusk){const L=Math.floor((t-s0+.25)/PWL);pwGarden(t,{dusk});
  if(L===0){chase(t,1.4);pop(t,s0+.2,'Round and round! 🌳',540,1180,62,'#fff','#16A34A')}
  else if(L===1){chase(t,2.4,{wSur:1});pop(t,s0+PWL+.2,'Catch me! 🦡',540,1180,66,'#fff','#D97706')}
  else if(L===2){chase(t,2.0);for(let k=0;k<3;k++){const p=((t*.8+k/3)%1);g.save();g.globalAlpha=1-p;txt('Ha ha!',300+k*220,1330-p*200,48,'#fff','#92400E');g.restore()}pop(t,s0+2*PWL+.2,'So much fun! 😂',540,1180,62,'#fff','#92400E')}
  else popUp(t,s0+3*PWL-.05)}
function verseB(t,s0,jack){const L=Math.floor((t-s0+.25)/PWL),lt=t-s0-L*PWL;sewingShop(t);
  adult('dadi',840,1560,{s:.9,t,pose:L===3?'up':'sway',happy:1,dir:-1});counter();
  const jp=L===3?prog(t,s0+3*PWL-.05,s0+3*PWL+2):0;jackBox(560,1480,.9,t,L===3,jp);
  monkey(210,1840,1.15,t,{dir:1,surprised:L>=2,up:L===3||L===0&&lt>1.2,hop:L<2?pwhop(t)*10:0});
  if(L<2){const p=prog(t,s0+L*PWL+.3,s0+L*PWL+1.1);if(p<1)penny(lerp(320,800,p),1420-Math.sin(p*Math.PI)*200,1.2,p*12);
    if(L===0){if(lt>1.2)spool(330,1500,1.4,'#EF4444');pop(t,s0+.2,'One penny! 🪙',540,1180,62,'#fff','#CA8A04')}else{spool(330,1500,1.4,'#EF4444');if(lt>1.2)needle(420,1430,1.2,.4);pop(t,s0+PWL+.2,'And a needle! 🪡',540,1180,62,'#fff','#DB2777')}}
  else{spool(300,1500,1.2,'#EF4444');needle(380,1430,1,.4);
    if(L===2){for(let k=0;k<6;k++){const p=((t*.7+k/6)%1);penny(260+k*110+Math.sin(p*9+k)*30,1400-p*600,1,t*8+k)}pop(t,s0+2*PWL+.2,'Bye-bye, pennies! 💸',540,1180,58,'#fff','#CA8A04')}
    else popBurst(560,980,t,s0+3*PWL+.25)}}

function drawWeasel(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const si=pwSec(t);
  g.save();g.translate(540,1720);g.scale(1.3,1.3);g.translate(-540,-1720);
  if(si>=0){const [s0,k]=PWSEC[si];if(k==='A')verseA(t,s0,si===2);else verseB(t,s0,si===3)}
  else if(t<PWA[0]-.25){pwGarden(t);const q=easeOut(prog(t,1,6));mulberryBush(540,1720,.95,t);monkey(lerp(-200,250,q),1820,1.0,t,{dir:1,run:q<1,up:q>=1});
    const w2=prog(t,7,8);if(t>7)weasel(lerp(540,820,w2),1830,.85,t,{dir:-1,wave:w2>=1,hop:pwhop(t)*20});
    pop(t,2,'Hello, Monkey! 🐒',540,1180,64,'#fff','#92400E');pop(t,7.2,'Hi, Weasel! 🦡',540,1180,64,'#fff','#D97706');pop(t,12.5,'Let\'s play! 🎶',540,1180,70,'#fff','#16A34A');
    if(t>12)chase(t,1.2)}
  else if(t<PWA[1]-.25){ // break 1: they sew a bunting together with the thread & needle
    pwGarden(t);mulberryBush(540,1720,.8,t);const q=prog(t,PWA[0]+8*PWL,PWA[1]-.25);
    g.strokeStyle='#EF4444';g.lineWidth=5;g.beginPath();g.moveTo(140,1300);g.quadraticCurveTo(540,1420,940,1300);g.stroke();
    const n=Math.floor(q*9);for(let k=0;k<=n&&k<9;k++){const x=180+k*90,y=1300+Math.sin((k+.5)/9*Math.PI)*60*1.1;g.fillStyle=['#F472B6','#FDE047','#60A5FA','#4ADE80'][k%4];g.beginPath();g.moveTo(x-34,y);g.lineTo(x+34,y);g.lineTo(x,y+70);g.closePath();g.fill()}
    monkey(220,1830,1.0,t,{dir:1,up:q>.85,hop:pwhop(t)*15});weasel(860,1840,.85,t,{dir:-1,wave:q>.85,hop:pwhop(t+.2)*15});needle(300+Math.sin(t*6)*30,1560,.8,.6);
    pop(t,PWA[0]+8*PWL+.4,'Let\'s sew! 🧵',540,1180,66,'#fff','#DB2777');if(q>.85)pop(t,PWA[1]-2.4,'Ta-da! 🎉',540,1180,72,'#fff','#7C3AED')}
  else if(t<PWA[2]-.25){ // long break: berries, see-saw, hide and seek
    const b0=PWA[1]+8*PWL;pwGarden(t,{dusk:t>b0+24});
    if(t<b0+12){mulberryBush(540,1720,.95,t);monkey(260,1830,1.0,t,{dir:1,up:Math.floor(t/.5455)%2});weasel(820,1840,.85,t,{dir:-1,hop:pwhop(t)*20});
      for(let k=0;k<5;k++){const p=((t*.6+k/5)%1);ell(lerp(540,k%2?300:800,p),1500-Math.sin(p*Math.PI)*250,16,18,'#7E22CE')}pop(t,b0+.4,'Yummy mulberries! 🫐',540,1180,60,'#fff','#7E22CE')}
    else if(t<b0+24){const a=Math.sin((t-b0)*Math.PI/1.091)*.3;g.save();g.translate(540,1800);rr(-40,-80,80,80,10,'#92400E');g.rotate(a);rr(-320,-110,640,30,12,'#F97316');
      monkey(-250,-110,.9,t,{dir:1,up:a>0});weasel(250,-110,.8,t,{dir:-1,wave:a<0});g.restore();pop(t,b0+12.3,'See-saw! ⬆️⬇️',540,1180,66,'#fff','#EA580C')}
    else{mulberryBush(540,1720,.95,t);const pk=Math.sin((t-b0-24)*1.6);if(pk>.3){g.save();g.beginPath();g.rect(0,0,W,1580);g.clip();weasel(540+(pk>.7?260:-260),1560+(1-pk)*220,.9,t,{});g.restore()}
      monkey(200,1830,1.0,t,{dir:1,surprised:pk>.5});pop(t,b0+24.3,'Where\'s Weasel? 👀',540,1180,62,'#fff','#2563EB');pop(t,PWA[2]-3,'Peek-a-boo! 🦡',540,1180,66,'#fff','#D97706')}}
  else{pwGarden(t,{dusk:1});monkey(320,1820,1.0,t,{dir:1,up:1,hop:pwhop(t)*25});weasel(760,1830,.85,t,{dir:-1,wave:1,hop:pwhop(t+.2)*25});confetti(t,PWA[2]+8*PWL-.3,70);
    for(let k=0;k<5;k++){const p=((t*.6+k/5)%1);g.save();g.globalAlpha=1-p;txt('♥',540+Math.sin(k*2)*140,1450-p*250,50,'#F472B6',null);g.restore()}}
  g.restore();
  if(t>=PWCARD){const q=easeOut(prog(t,PWCARD,PWCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#7C2D12';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,PWCARD,PWCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('POP! See you soon! 🎉',W/2,990,64,'#fff','#E11D48');
    const sp=backOut(prog(t,PWCARD+.5,PWCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<PWCARD){pwtitle(t);pwcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,PWEND-1.2,PWEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
function pwtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#E11D48';g.beginPath();g.roundRect(-370,-66,740,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Pop Goes the Weasel 🐒',0,2,56,'#FFFFFF',null);g.restore()}
function pwcap(t){const i=PWCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=PWCAPS[i];
  const al=Math.min(clamp((t-a)/.12),clamp((b-t)/.12));g.save();g.globalAlpha=al;let fs=64;g.font=`700 ${fs}px Fredoka, Baloo2`;let w=g.measureText(s).width;
  if(w>920){fs=Math.floor(fs*920/w);g.font=`700 ${fs}px Fredoka, Baloo2`;w=g.measureText(s).width}
  const h=120,y0=395;g.fillStyle='rgba(190,18,60,.92)';g.beginPath();g.roundRect(W/2-w/2-45,y0-h/2,w+90,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/(PWL*.9));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}
window.draw=drawWeasel;
