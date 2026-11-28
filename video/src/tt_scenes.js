// ================= "A Tisket, A Tasket" — Popcorn Productions =================
const TL=2.4, TV=[9.8,38.6,81.8];
const tl=(v,l)=>TV[v]+l*TL;
const TCARD=157.0, TEND=163.5;
const tpu=t=>Math.pow(Math.sin(Math.PI*((((t-TV[0])/(TL/2))%1+1)%1)),2);
const TLYR=['A tisket, a tasket,','A green and yellow basket.','I wrote a letter to my love,','And on the way I dropped it.','I dropped it, I dropped it,','And on the way I dropped it.','A little boy, he picked it up,','And put it in his pocket!'];

function basketG(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);g.strokeStyle='#CA8A04';g.lineWidth=10;g.beginPath();g.arc(0,-40,70,Math.PI,0);g.stroke();
  if(o.full){ell(-30,-60,24,24,'#EF4444');ell(10,-66,22,22,'#F59E0B');ell(40,-58,20,20,'#A3E635');ell(-5,-80,14,14,'#DC2626')}
  else if(o.letter){g.save();g.translate(10,-70);g.rotate(-.2);envelope(0,0,.6)}
  if(o.letter&&!o.full)g.restore();
  g.fillStyle='#16A34A';g.beginPath();g.moveTo(-80,-40);g.lineTo(80,-40);g.lineTo(62,60);g.lineTo(-62,60);g.closePath();g.fill();
  g.save();g.clip();for(let r=0;r<4;r++){g.fillStyle=r%2?'#FDE047':'#16A34A';g.fillRect(-90,-40+r*25,180,25)}for(let k=0;k<7;k++){g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=4;g.beginPath();g.moveTo(-70+k*23,-40);g.lineTo(-58+k*20,60);g.stroke()}g.restore();
  rr(-86,-46,172,14,6,'#CA8A04');g.restore()}
function envelope(x,y,s,rot=0,open=0){g.save();g.translate(x,y);g.scale(s,s);g.rotate(rot);rr(-60,-40,120,80,8,'#FFFFFF');g.strokeStyle='#E5E7EB';g.lineWidth=3;g.strokeRect(-60,-40,120,80);
  g.fillStyle=open?'#FDE68A':'#F3F4F6';g.beginPath();if(open){g.moveTo(-60,-40);g.lineTo(0,-90);g.lineTo(60,-40)}else{g.moveTo(-60,-40);g.lineTo(0,6);g.lineTo(60,-40)}g.closePath();g.fill();g.stroke();
  txt('♥',0,open?-50:4,40,'#EF4444',null);g.restore()}
function girlWithBasket(x,y,s,t,o={}){kid(1,x,y-(o.skip?Math.abs(Math.sin(t*Math.PI/(TL/2)))*40:0),{s,t,happy:o.happy??1,noHat:1,noScarf:1,dir:o.dir||1,trunk:o.trunk??.5});basketG(x+(o.dir||1)*95*s,y-150*s-(o.skip?Math.abs(Math.sin(t*Math.PI/(TL/2)))*40:0),.75*s,t,{letter:o.letter,full:o.full})}
function boy(x,y,s,t,o={}){kid(0,x,y,{s,t,happy:o.happy??1,noHat:1,noScarf:1,cap:'#2563EB',dir:o.dir||-1,trunk:o.trunk??.5})}
function park(t,o={}){sky(o.dusk?'#FDBA74':'#7DD3FC',o.dusk?'#FEF3C7':'#E0F2FE');if(!o.dusk)mandalaSun(880,560,60,t);cloud(((t*15)%1400)-300,520,.9);cloud(((t*10+700)%1400)-300,650,.7);
  hills(t,'#A3E635','#84CC16','#65A30D');folkTree(120,1500,.9,t,3);folkTree(960,1520,.85,t,5);
  g.fillStyle='#4ADE80';g.fillRect(0,1500,W,H-1500);g.fillStyle='#FDE68A';g.beginPath();g.moveTo(380,1500);g.quadraticCurveTo(300,1700,160,H);g.lineTo(920,H);g.quadraticCurveTo(780,1700,700,1500);g.closePath();g.fill();
  for(let k=0;k<12;k++)marigold(40+rnd(k)*1000,1560+rnd(k+3)*340,.8,['#F472B6','#FBBF24','#F87171','#A78BFA'][k%4]);
  if(o.bench){rr(620,1520,300,22,8,'#92400E');rr(620,1460,300,18,8,'#92400E');rr(640,1540,16,70,4,'#78350F');rr(884,1540,16,70,4,'#78350F')}}
function flutter(t,t0,x0,y0,x1,y1,dur=1.8){const p=prog(t,t0,t0+dur);if(p<=0)return null;const x=lerp(x0,x1,p)+Math.sin(p*14)*50*(1-p),y=lerp(y0,y1,easeOut(p));envelope(x,y,.65,Math.sin(p*12)*.6);return p}
function tttitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#16A34A';g.beginPath();g.roundRect(-360,-66,720,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('A Tisket, A Tasket 🧺',0,2,58,'#FFFFFF',null);g.restore()}
const TCAPS=[];TV.forEach(v0=>TLYR.forEach((s,k)=>TCAPS.push([v0+k*TL-.25,v0+(k+1)*TL-.25+(k===7?.6:0),s])));
function ttcap(t){const i=TCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=TCAPS[i];
  const al=Math.min(clamp((t-a)/.15),clamp((b-t)/.15));g.save();g.globalAlpha=al;g.font='700 64px Fredoka, Baloo2';
  const w=g.measureText(s).width;const h=120,y0=395;g.fillStyle='rgba(21,128,61,.9)';g.beginPath();g.roundRect(W/2-w/2-50,y0-h/2,w+100,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.85));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}
function tinPhone(x,y,s,t,ring){g.save();g.translate(x,y);g.scale(s,s);if(ring)g.rotate(Math.sin(t*40)*.15);rr(-30,-40,60,80,10,'#94A3B8');ell(0,-40,30,10,'#CBD5E1');g.restore()}

function verseT(t,v){const L=Math.floor((t-TV[v]+.25)/TL);const lt=t-tl(v,L);
  park(t,{bench:L===2});
  const gx=L<2?lerp(260,560,prog(t,tl(v,0),tl(v,2))):(L===2?720:lerp(520,880,prog(t,tl(v,3),tl(v,6))));
  if(L===2){kid(1,770,1640,{s:.95,t,happy:1,noHat:1,noScarf:1,trunk:.5});basketG(620,1470,.7,t,{});g.save();g.translate(860,1400);g.rotate(-.2);envelope(0,0,.9,0,1);g.restore();
    g.strokeStyle='#F59E0B';g.lineWidth=10;g.lineCap='round';g.beginPath();g.moveTo(880+Math.sin(t*14)*20,1380);g.lineTo(930,1300);g.stroke();for(let k=0;k<3;k++){const p=((t*.8+k/3)%1);g.save();g.globalAlpha=1-p;txt('♥',860+k*30,1280-p*160,44,'#EF4444',null);g.restore()}
    pop(t,tl(v,2)+.2,'Dear Mummy... 💌',540,1000,64,'#fff','#DB2777')}
  else if(L<3){girlWithBasket(gx,1760,1.0,t,{skip:1,letter:1});pop(t,tl(v,1)+.2,'Green & yellow! 💚💛',540,1000,64,'#fff','#16A34A')}
  else if(L<6){girlWithBasket(gx,1760,1.0,t,{skip:1});
    const p=flutter(t,tl(v,3)+.3,gx-200,1500,260,1810,2.2);if(p!==null&&p>=1)envelope(260,1810,.65,.2);
    if(L>=4){envelope(260,1810,.65,.2);for(let k=0;k<4;k++){const q=((t*1.2+k/4)%1);g.strokeStyle=`rgba(255,255,255,${1-q})`;g.lineWidth=5;g.beginPath();g.moveTo(80+q*300,1650+k*30);g.lineTo(160+q*300,1650+k*30);g.stroke()}}
    pop(t,tl(v,3)+.6,'Oops! 💨',300,1300,72,'#fff','#DC2626')}
  else{const bq=easeOut(prog(t,tl(v,6),tl(v,6)+1.2));boy(lerp(-150,330,bq),1780,1.0,t,{dir:1,trunk:L===6&&bq>.9?1:.5});
    if(L===6&&bq<1)envelope(260,1810,.65,.2);else if(L===6){envelope(380,1500,.65,0)}
    if(L===7){g.save();g.translate(330,1650);rr(-30,-20,60,44,8,'#1D4ED8');g.restore();pop(t,tl(v,7)+.2,'In my pocket! 😉',540,1000,64,'#fff','#2563EB')}
    if(L===6)pop(t,tl(v,6)+1.1,'Ooh, a letter! 💌',540,1000,64,'#fff','#2563EB');
    girlWithBasket(900,1760,.8,t,{dir:1})}
}
function drawTisket(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const vi=TV.findIndex(v0=>t>=v0-.25&&t<v0+8*TL-.25);
  g.save();g.translate(540,1450);g.scale(1.35,1.35);g.translate(-540,-1560);
  if(t<TV[0]-.25){park(t);girlWithBasket(lerp(-150,380,easeOut(prog(t,1,8))),1760,1.0,t,{skip:1,full:0});pop(t,2,'La la la! 🎵',540,1000,72,'#fff','#16A34A')}
  else if(vi>=0)verseT(t,vi);
  else if(t<TV[1]-.25){ // where's my letter?
    park(t);const q=prog(t,tl(0,8),TV[1]);girlWithBasket(540+Math.sin(t*2)*200,1760,1.0,t,{happy:0,dir:Math.cos(t*2)>0?1:-1});
    for(let k=0;k<3;k++){const p=((t*.7+k/3)%1);g.save();g.globalAlpha=1-p;txt('?',380+k*150,1300-p*200,80,'#fff','#DC2626');g.restore()}pop(t,tl(0,8)+.4,'Where\'s my letter? 😟',540,1000,64,'#fff','#DC2626')}
  else if(t<TV[2]-.25){ // boy reads the letter; tin-can phone rings at 66 & 76
    const q=prog(t,tl(1,8),TV[2]);park(t,{dusk:q>.7});
    boy(300,1760,1.0,t,{dir:1});girlWithBasket(860,1760,1.0,t,{dir:-1,happy:t>66.5});
    if(t<65){g.save();g.translate(430,1440);envelope(0,0,1.1,0,1);g.restore();pop(t,tl(1,8)+.5,'"To Mummy, with love ♥"',540,1000,58,'#fff','#DB2777');pop(t,tl(1,8)+3.5,'It\'s hers! 😮',540,1120,64,'#fff','#2563EB')}
    // tin-can phone string
    g.strokeStyle='#A16207';g.lineWidth=4;g.beginPath();g.moveTo(400,1450);g.quadraticCurveTo(580,1600,760,1450);g.stroke();
    const ring=(t>66&&t<68)||(t>76&&t<78);tinPhone(400,1450,1,t,ring&&t<70);tinPhone(760,1450,1,t,ring&&t>70);
    if(t>66)pop(t,66,'Ring ring! 📞',540,1000,72,'#fff','#7C3AED');if(t>68.5)pop(t,68.5,'I found your letter! 💌',540,1120,58,'#fff','#2563EB');if(t>76)pop(t,76,'Ring ring! 📞',540,1000,72,'#fff','#7C3AED');if(t>78.3)pop(t,78.3,'Thank you! 🥰',540,1120,64,'#fff','#DB2777')}
  else{ // long ending: return the letter, deliver to Mummy, picnic
    park(t);const q=prog(t,tl(2,8),TCARD);
    if(q<.2){boy(lerp(200,440,easeOut(q/.2)),1760,1.0,t,{dir:1,trunk:1});girlWithBasket(700,1760,1.0,t,{dir:-1,trunk:1});envelope(lerp(320,560,q/.2),1450,.8,0);pop(t,tl(2,8)+.5,'Here you go! 💌',540,1000,66,'#fff','#2563EB')}
    else if(q<.45){adult('mom',860,1800,{s:1.0,t,pose:q>.32?'up':'sway',happy:1});boy(250,1780,.85,t,{dir:1,trunk:1});girlWithBasket(500,1780,.9,t,{dir:1,trunk:1});
      g.save();g.translate(720,1400);envelope(0,0,.9,0,q>.3?1:0);g.restore();if(q>.3)for(let k=0;k<6;k++){const p=((t*.6+k/6)%1);g.save();g.globalAlpha=1-p;txt('♥',600+Math.sin(k*2)*160,1300-p*300,52,'#F472B6',null);g.restore()}
      pop(t,tl(2,8)+(TCARD-tl(2,8))*.2,'For you, Mummy! 💝',540,1000,64,'#fff','#DB2777')}
    else{g.fillStyle='#F87171';g.save();g.translate(540,1700);for(let r=0;r<4;r++)for(let c=0;c<8;c++){g.fillStyle=(r+c)%2?'#FFFFFF':'#EF4444';g.fillRect(-360+c*90,-120+r*60,90,60)}g.restore();
      basketG(540,1620,1.3,t,{full:1});adult('mom',150,1840,{s:.85,t,pose:'clap',happy:1});
      girlWithBasket(350,1860-tpu(t)*30,.85,t,{dir:1,trunk:1});boy(760,1860-tpu(t+.2)*30,.85,t,{dir:-1,trunk:1});puppy(940,1860,.6,t,tpu(t)*30);notes(540,1300,t,tl(2,8),6);
      pop(t,tl(2,8)+(TCARD-tl(2,8))*.46,'Picnic time! 🧺🍎',540,1000,70,'#fff','#16A34A');if(q>.8)confetti(t,TCARD-11,40)}}
  g.restore();
  if(t>=TCARD){const q2=easeOut(prog(t,TCARD,TCARD+.8));g.save();g.globalAlpha=q2*.75;g.fillStyle='#14532D';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q2;
    popcornLogo(W/2,520,.85*backOut(prog(t,TCARD,TCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('A green & yellow basket! 🧺',W/2,990,62,'#fff','#16A34A');
    const sp=backOut(prog(t,TCARD+.5,TCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  const cuts=[];TV.forEach(v0=>{[0,2,3,6,8].forEach(k=>cuts.push(v0+k*TL-.25))});cuts.forEach(c=>{const d=Math.abs(t-c);if(d<.14){g.fillStyle=`rgba(255,255,255,${(1-d/.14)*.55})`;g.fillRect(0,0,W,H)}});
  if(t<TCARD){tttitle(t);ttcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,TEND-1.2,TEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawTisket;
