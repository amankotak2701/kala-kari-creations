// ================= "Rock-a-Bye Baby" — Popcorn Productions =================
const easeInOut=x=>{x=clamp(x);return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2};
const RBAR=1.6665, RLL=4*RBAR;              // 3/4 time, 4 bars per sung line
let RV=[13.2,52.2,89.5];                      // verse starts (first line onset)
const rl=(v,l)=>RV[v]+l*RLL;
const RCARD=116.4, REND=122.1;
const RLYR=[
 ['Rock-a-bye baby, on the treetop,','When the wind blows, the cradle will rock.','When the bough breaks, the cradle will fall,','But mother will catch you, cradle and all!'],
 ['Baby is drowsy, cozy and fair,','Mother sits near in her rocking chair.','Forward and back the cradle she swings,','And though baby sleeps, he hears what she sings.'],
 ['From the high rooftops down to the sea,','No one\'s as dear as baby to me.','Wee little fingers, eyes wide and bright,','Now sound asleep until morning light.']];
const RCAPS=[];RV.forEach((v0,v)=>RLYR[v].forEach((s,k)=>RCAPS.push([v0+k*RLL-.3,v0+(k+1)*RLL-.3-(k===3?0:0),s])));

// cradle hanging from a branch on two ropes; pivot at (x,y)
function hangCradle(x,y,s,t,o={}){const sw=o.sw??Math.sin(t*Math.PI/RBAR)*.12;g.save();g.translate(x,y);g.rotate(sw);
  g.strokeStyle='#A16207';g.lineWidth=7;g.beginPath();g.moveTo(-6,0);g.lineTo(-170*s,300*s);g.moveTo(6,0);g.lineTo(150*s,300*s);g.stroke();
  ell(0,0,16,16,'#78350F');cradle(0,430*s,s,o.t2??0,{sleep:o.sleep,cry:o.cry,noRock:1});g.restore()}
function bigTree(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);
  g.fillStyle='#7C4A1E';g.beginPath();g.moveTo(-70,0);g.quadraticCurveTo(-40,-300,-50,-620);g.lineTo(50,-620);g.quadraticCurveTo(40,-300,70,0);g.closePath();g.fill();
  // the bough the cradle hangs from (can bend / break)
  const bend=o.bend||0;g.save();g.translate(30,-560);g.rotate(bend);g.fillStyle='#7C4A1E';g.beginPath();g.moveTo(0,-26);g.quadraticCurveTo(200,-60,420,-40);g.lineTo(420,-14);g.quadraticCurveTo(200,-26,0,26);g.closePath();g.fill();
  if(o.crack){g.strokeStyle='#FDE68A';g.lineWidth=5;g.beginPath();g.moveTo(140,-40);g.lineTo(155,-20);g.lineTo(140,-5);g.lineTo(158,12);g.stroke()}
  for(let k=0;k<5;k++)ell(120+k*70,-70-(k%2)*20,70,50,k%2?'#16A34A':'#22C55E');g.restore();
  const wob=Math.sin(t*1.3)*(o.windy?14:4);
  [[0,-760,260,190,'#15803D'],[-200,-640,170,140,'#16A34A'],[180,-700,190,150,'#22C55E'],[-90,-880,180,140,'#22C55E'],[110,-860,160,130,'#16A34A']].forEach(([cx,cy,rx,ry,c],i)=>ell(cx+wob*(i%2?1:-1),cy,rx,ry,c));
  for(let k=0;k<9;k++)ell(-200+rnd(k)*400+wob,-900+rnd(k+4)*300,14,14,'#F97316');
  g.restore()}
function gardenBg(t,o={}){const dusk=o.dusk||0;
  sky(dusk?'#F97316':'#7DD3FC',dusk?'#FDE68A':'#E0F2FE');if(!dusk)mandalaSun(900,660,60,t);else glow(880,1200,420,'rgba(255,200,80,.7)');
  cloud(((t*(o.windy?80:14))%1500)-300,520,.9);cloud(((t*(o.windy?60:10)+700)%1500)-300,700,.7);
  hills(t,'#A3E635','#84CC16','#65A30D');g.fillStyle='#4ADE80';g.fillRect(0,1500,W,H-1500);
  for(let k=0;k<10;k++)marigold(40+rnd(k)*1000,1580+rnd(k+3)*320,.8,['#F472B6','#FBBF24','#F87171','#A78BFA'][k%4])}
function wind(t,amt=1){for(let k=0;k<7;k++){const p=((t*.9*amt+k/7)%1);const y=620+k*120;g.save();g.globalAlpha=Math.sin(p*Math.PI)*.85;g.strokeStyle='#fff';g.lineWidth=7;g.lineCap='round';g.beginPath();const x=-200+p*1500;g.moveTo(x,y);g.bezierCurveTo(x+80,y-40,x+160,y+40,x+240,y);g.arc(x+240,y-24,24,Math.PI/2,-Math.PI*.9,true);g.stroke();g.restore()}
  for(let k=0;k<8;k++){const p=((t*.7*amt+k/8)%1);g.save();g.translate(-100+p*1300,700+rnd(k)*700+Math.sin(p*12+k)*60);g.rotate(p*14);ell(0,0,18,9,['#22C55E','#F97316','#FACC15'][k%3]);g.restore()}}
function rockingChair(x,y,s,t,rock){g.save();g.translate(x,y);g.scale(s,s);g.rotate(rock);
  g.strokeStyle='#92400E';g.lineWidth=16;g.lineCap='round';g.beginPath();g.arc(0,-260,300,Math.PI*.35,Math.PI*.65);g.stroke();
  rr(-110,-230,20,190,8,'#92400E');rr(90,-230,20,190,8,'#92400E');
  rr(-130,-250,260,34,12,'#B45309');rr(-130,-560,34,330,14,'#B45309');for(let k=0;k<4;k++)rr(-118,-530+k*70,22,40,8,'#D97706');rr(-150,-590,70,40,14,'#B45309');
  rr(-10,-380,40,140,10,'#B45309');g.restore()}
// seated mother: upper body via adult() clipped at the waist, legs drawn bent
function seatedMom(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);
  g.save();g.beginPath();g.rect(-300,-900,700,770);g.clip();adult('mom',0,40,{s:1,t,pose:o.pose||'hold',happy:o.happy??1,dir:1});g.restore();
  g.fillStyle=FAM.mom.bottom;g.beginPath();g.moveTo(-60,-150);g.lineTo(150,-150);g.lineTo(150,-90);g.lineTo(-70,-90);g.closePath();g.fill();
  rr(110,-150,40,150,16,FAM.mom.bottom);ell(150,-6,32,14,'#3F2A1E');g.restore()}
function nightRoom(t,o={}){const w=g.createLinearGradient(0,0,0,1450);w.addColorStop(0,'#1E1B4B');w.addColorStop(1,'#4C1D95');g.fillStyle=w;g.fillRect(0,0,W,1460);
  for(let k=0;k<9;k++)for(let j=0;j<10;j++){g.globalAlpha=.1;starShape(60+k*120+(j%2)*60,80+j*140,12,0,'#FDE68A')}g.globalAlpha=1;
  // window with moon
  const morning=o.morning||0;g.save();g.beginPath();g.roundRect(640,690,330,380,30);g.clip();
  if(morning>0){sky('#FDBA74','#FEF3C7');sunFace(805,990-morning*140,70,t)}else{sky('#0B1446','#1E3A8A');moonFace(820,830,62,t,0,0);for(let k=0;k<12;k++)ell(650+rnd(k)*320,700+rnd(k+3)*360,2.5,2.5,'#fff')}
  g.restore();g.strokeStyle='#E9D5FF';g.lineWidth=16;g.beginPath();g.roundRect(640,690,330,380,30);g.stroke();g.lineWidth=8;g.beginPath();g.moveTo(805,690);g.lineTo(805,1070);g.moveTo(640,880);g.lineTo(970,880);g.stroke();
  // curtains
  g.fillStyle='#F9A8D4';g.beginPath();g.moveTo(610,660);g.quadraticCurveTo(660,890,600,1110);g.lineTo(560,1110);g.lineTo(560,660);g.fill();g.beginPath();g.moveTo(1000,660);g.quadraticCurveTo(950,890,1010,1110);g.lineTo(1050,1110);g.lineTo(1050,660);g.fill();
  const fl=g.createLinearGradient(0,1440,0,H);fl.addColorStop(0,'#7C2D12');fl.addColorStop(1,'#431407');g.fillStyle=fl;g.fillRect(0,1440,W,H-1440);
  ell(560,1770,460,80,'#F9A8D4');ell(560,1770,390,58,'#FBCFE8');
  if(morning>0){g.save();g.globalAlpha=morning*.35;g.fillStyle='#FDE68A';g.fillRect(0,0,W,H);g.restore()}}
// night town + sea flyover for "from the high rooftops down to the sea"
function townSea(t,scroll){const sk=g.createLinearGradient(0,0,0,H);sk.addColorStop(0,'#0B1446');sk.addColorStop(.6,'#3E2A78');sk.addColorStop(1,'#1E3A8A');g.fillStyle=sk;g.fillRect(0,0,W,H);
  for(let k=0;k<70;k++){g.globalAlpha=.4+.6*Math.abs(Math.sin(t*1.5+k));ell(rnd(k)*W,480+rnd(k+5)*800,2.5,2.5,'#fff')}g.globalAlpha=1;
  moonFace(830,640,90,t,0,0);
  // rooftops scroll left, sea appears on right
  g.save();g.translate(-scroll,0);
  for(let k=0;k<9;k++){const hx=80+k*240,hh=260+rnd(k)*220,col=['#F472B6','#60A5FA','#FBBF24','#34D399','#A78BFA'][k%5];
    rr(hx-90,1500-hh,180,hh+40,6,shade(col,-.35));g.fillStyle=shade(col,-.55);g.beginPath();g.moveTo(hx-110,1500-hh);g.lineTo(hx,1500-hh-120);g.lineTo(hx+110,1500-hh);g.fill();
    for(let r=0;r<2;r++)for(let c=0;c<2;c++)rr(hx-60+c*70,1540-hh+r*90,46,46,6,(k+r+c)%3?'#FDE68A':'#475569')}
  g.fillStyle='#14532D';g.fillRect(-100,1500,2300,H);
  // sea
  const sx=2200;const sea=g.createLinearGradient(0,1450,0,H);sea.addColorStop(0,'#1D4ED8');sea.addColorStop(1,'#1E3A8A');g.fillStyle=sea;g.fillRect(sx-200,1420,2000,H);
  ell(sx-200,1700,260,300,'#FDE68A');
  for(let k=0;k<16;k++){g.strokeStyle='rgba(255,255,255,.6)';g.lineWidth=5;g.beginPath();const wx=sx+(k%4)*220+Math.sin(t*2+k)*20,wy=1480+Math.floor(k/4)*110;g.arc(wx,wy,30,Math.PI*1.1,Math.PI*1.9);g.stroke()}
  g.restore()}
function babyClose(t,o={}){ // big close-up of baby face + tiny hands
  const bx=540,by=1260;ell(bx,by+380,420,300,'#93C5FD');for(let k=0;k<7;k++)starShape(220+k*105,by+260+Math.abs(k-3)*14,16,0,'#fff');
  ell(bx,by,230,215,'#FFE4D6');g.fillStyle='#FDE68A';g.beginPath();g.ellipse(bx,by-70,245,200,0,Math.PI*1.05,Math.PI*1.95);g.fill();
  g.fillStyle='#FFFFFF';g.beginPath();g.ellipse(bx,by-110,260,160,0,Math.PI,0);g.fill();ell(bx,by-270,50,50,'#FFFFFF');ell(bx-230,by+10,40,52,'#FFE4D6');ell(bx+230,by+10,40,52,'#FFE4D6');
  if(o.open){const bl=(t%3.2)<.12;[-80,80].forEach(dx=>{if(bl){g.strokeStyle='#3F2A1E';g.lineWidth=10;g.beginPath();g.moveTo(bx+dx-26,by);g.lineTo(bx+dx+26,by);g.stroke()}else{ell(bx+dx,by,30,36,'#3F2A1E');ell(bx+dx+10,by-12,11,11,'#fff');ell(bx+dx-10,by+10,5,5,'#fff')}})}
  else{g.strokeStyle='#3F2A1E';g.lineWidth=10;g.lineCap='round';[-80,80].forEach(dx=>{g.beginPath();g.arc(bx+dx,by-6,30,Math.PI*.15,Math.PI*.85);g.stroke()})}
  ell(bx-130,by+80,40,24,'rgba(244,114,182,.5)');ell(bx+130,by+80,40,24,'rgba(244,114,182,.5)');ell(bx,by+30,16,12,'#F5C2A8');
  g.strokeStyle='#9F1239';g.lineWidth=9;g.beginPath();g.arc(bx,by+80,34,.25,Math.PI-.25);g.stroke();
  if(o.hands){[-1,1].forEach(d=>{g.save();g.translate(bx+d*250,by+260);g.rotate(d*(.3+Math.sin(t*6+d)*.25));ell(0,0,62,56,'#FFE4D6');for(let f=0;f<4;f++)ell(-36+f*24,-50,13,24,'#FFE4D6');ell(d*-56,-14,14,26,'#FFE4D6',d*.6);g.restore()})}}
function rbtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#DB2777';g.beginPath();g.roundRect(-340,-66,680,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Rock-a-Bye Baby 🌙',0,2,58,'#FFFFFF',null);g.restore()}
function rbcap(t){const i=RCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=RCAPS[i];
  const al=Math.min(clamp((t-a)/.15),clamp((b-t)/.15));g.save();g.globalAlpha=al;let fs=62;g.font=`700 ${fs}px Fredoka, Baloo2`;let w=g.measureText(s).width;
  if(w>900){fs=Math.floor(fs*900/w);g.font=`700 ${fs}px Fredoka, Baloo2`;w=g.measureText(s).width}
  const h=120,y0=395;g.fillStyle='rgba(157,23,77,.9)';g.beginPath();g.roundRect(W/2-w/2-45,y0-h/2,w+90,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.85));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}
function heartsUp(x,y,t,n=6,sp=160,col='#F472B6'){for(let k=0;k<n;k++){const p=((t*.6+k/n)%1);g.save();g.globalAlpha=1-p;txt('♥',x+Math.sin(k*2.3)*sp,y-p*300,48+(k%3)*10,col,null);g.restore()}}
function songNotes(x,y,t,n=5){for(let k=0;k<n;k++){const p=((t*.5+k/n)%1);g.save();g.globalAlpha=1-p;txt(k%2?'♫':'♪',x+p*260+Math.sin(p*8+k)*40,y-p*280,54,['#FDE047','#F9A8D4','#93C5FD'][k%3],null);g.restore()}}

function drawRock(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const v=RV.findIndex(v0=>t>=v0-.3&&t<v0+4*RLL-.3);const L=v>=0?Math.floor((t-RV[v]+.3)/RLL):-1;
  const TX=430,TY=1560; // tree base; branch pivot ~ (TX+30+330, TY-560)
  const PX=TX+390,PY=TY-590;
  const zoomOn=!(t>=RV[1]+4*RLL-.3&&t<RV[2]+RLL-.3)&&!(v===2&&L===2)&&t<RCARD;
  g.save();if(zoomOn){g.translate(540,1590);g.scale(1.2,1.2);g.translate(-540,-1560)}
  if(t<RV[0]-.3){ // intro: mummy carries baby to the big tree and hangs the cradle
    gardenBg(t);bigTree(TX,TY,1,t);const q=easeOut(prog(t,1,7));
    if(t<8){adult('mom',lerp(-150,640,q),1800,{s:1.0,t,pose:'hold',happy:1});g.save();g.translate(lerp(-150,640,q)+90,1520);ell(0,0,60,44,'#93C5FD');ell(10,-50,40,38,'#FFE4D6');ell(10,-70,42,26,'#FFFFFF');g.restore();pop(t,2,'Time for a swing! 🌳',540,1000,66,'#fff','#DB2777')}
    else{hangCradle(PX,PY,.75,t,{sw:Math.sin(t*1.6)*.1,t2:0});adult('mom',220,1820,{s:1.0,t,pose:'wave',happy:1});pop(t,8.3,'Wheee! 😊',540,1000,72,'#fff','#DB2777')}}
  else if(v===0){const windy=L>=1&&L<3;gardenBg(t,{windy});
    const lt=t-rl(0,L);
    if(L<2){bigTree(TX,TY,1,t,{windy});hangCradle(PX,PY,.75,t,{sw:Math.sin(t*Math.PI/RBAR)*(L===1?.28:.12),t2:0});if(L===1)wind(t,1.3);
      if(L===0){adult('mom',190,1820,{s:.95,t,pose:'sway',happy:1});pop(t,rl(0,0)+.5,'Up in the treetop! 🌳',540,1000,62,'#fff','#16A34A')}
      else{adult('mom',190,1820,{s:.95,t,pose:'sway',happy:1});pop(t,rl(0,1)+.4,'Whoosh! 💨',540,1000,80,'#fff','#2563EB')}}
    else if(L===2){wind(t,1.6);const bend=easeOut(prog(t,rl(0,2)+1.2,rl(0,2)+3.5))*.45;bigTree(TX,TY,1,t,{windy:1,bend,crack:t>rl(0,2)+.8});
      // cradle slides down gently with a little leaf parachute
      const dp=easeInOut(prog(t,rl(0,2)+2.4,rl(0,3)+.6));const cx=lerp(PX,620,dp),cy=lerp(PY,1180,dp);
      if(dp<=0)hangCradle(PX,PY+Math.sin(bend)*300,.75,t,{sw:Math.sin(t*9)*.2,t2:0,cry:t>rl(0,2)+1.5});
      else{g.save();g.translate(cx,cy+330);g.rotate(Math.sin(t*3)*.12);cradle(0,0,.75,0,{cry:0,noRock:1});g.restore();ell(cx,cy+40,200,70,'#22C55E');g.strokeStyle='#A16207';g.lineWidth=4;g.beginPath();g.moveTo(cx-180,cy+50);g.lineTo(cx-140,cy+220);g.moveTo(cx+180,cy+50);g.lineTo(cx+140,cy+220);g.stroke()}
      adult('mom',lerp(190,600,easeOut(prog(t,rl(0,2)+2,rl(0,3)))),1820,{s:.95,t,pose:t>rl(0,2)+2.5?'up':'sway',happy:t<rl(0,2)+1?1:0});
      pop(t,rl(0,2)+.8,'Crack! 😮',300,1000,84,'#fff','#DC2626');pop(t,rl(0,2)+3.6,'Gently down... 🍃',540,1000,62,'#fff','#16A34A')}
    else{bigTree(TX,TY,1,t,{bend:.45});const lp=easeOut(prog(t,rl(0,3),rl(0,3)+.8));
      adult('mom',520,1820,{s:1.0,t,pose:'hold',happy:1});g.save();g.translate(700,1600-(1-lp)*260);cradle(0,0,.6,t,{noRock:1});g.restore();
      heartsUp(620,1250,t,7,220);pop(t,rl(0,3)+.6,'Mummy caught you! 💕',540,1000,62,'#fff','#DB2777');if(t>rl(0,3)+.8)confetti(t,rl(0,3)+.8,50)}}
  else if(t<RV[1]-.3){ // break: walk home at sunset
    const q=prog(t,rl(0,4),RV[1]);gardenBg(t,{dusk:1});g.save();g.globalAlpha=.9;house(860,1520,1.3,0,'#DB2777');g.restore();
    const mx=lerp(160,720,easeInOut(q));adult('mom',mx,1820,{s:1.0,t,pose:'hold',happy:1});g.save();g.translate(mx+170,1600);cradle(0,0,.55,t,{sleep:q>.7,noRock:1});g.restore();
    if(q<.5)songNotes(mx-100,1200,t);else heartsUp(mx,1150,t,5,140);pop(t,rl(0,4)+.5,'Home we go! 🏡',540,1000,66,'#fff','#EA580C');pop(t,rl(0,4)+6,'Bedtime soon... 🌙',540,1000,62,'#fff','#7C3AED')}
  else if(v===1){ // nursery: mother in rocking chair, swinging the cradle, singing
    nightRoom(t);const rock=Math.sin(t*Math.PI/RBAR)*.06;
    g.save();g.translate(300,1760);g.rotate(rock);g.translate(-300,-1760);rockingChair(300,1760,1,t,0);seatedMom(300,1680,1,t,{pose:L>=2?'hold':'sway',happy:1});g.restore();
    const sleep=L>=3||(L===0&&((t-rl(1,0))%3.2)>2.2);
    g.save();g.translate(760,1660);if(L>=2){g.rotate(Math.sin(t*Math.PI/RBAR)*.12)}g.translate(-760,-1660);cradle(760,1660,.95,0,{sleep});g.restore();
    if(L===0){if(((t-rl(1,0))%3.2)>1.4&&((t-rl(1,0))%3.2)<2.2)pop(t,rl(1,0)+1.4,'Yaaawn! 🥱',740,1150,64,'#fff','#7C3AED');pop(t,rl(1,0)+.4,'So cozy! 🧸',540,1000,64,'#fff','#DB2777')}
    if(L===1){songNotes(330,1150,t);pop(t,rl(1,1)+.4,'Mummy\'s rocking chair 🪑',540,1000,58,'#fff','#B45309')}
    if(L===2){g.strokeStyle='#FDE047';g.lineWidth=8;g.lineCap='round';for(const d of[-1,1]){g.beginPath();g.arc(760,1500,300,-Math.PI/2+d*.5,-Math.PI/2+d*.75);g.stroke()}pop(t,rl(1,2)+.4,'Forward and back! 🎶',540,1000,62,'#fff','#2563EB')}
    if(L===3){songNotes(330,1150,t,6);zzz(820,1390,t,1.3);pop(t,rl(1,3)+.4,'Shh... sleeping 💤',540,1000,62,'#fff','#7C3AED')}}
  else if(t<RV[2]-.3){ // break: dream — the cradle floats up to the stars
    const q=prog(t,rl(1,4),RV[2]);townSea(t,0);const cy=lerp(1500,1050,easeOut(q));
    for(let k=0;k<3;k++)ell(540+(k-1)*160,cy+150,140,60,'rgba(255,255,255,.95)');g.save();g.translate(540,cy);g.rotate(Math.sin(t*1.5)*.08);cradle(0,0,.8,0,{sleep:1,noRock:1});g.restore();
    zzz(620,cy-200,t,1.2);for(let k=0;k<6;k++){const a=t*.6+k;starShape(540+Math.cos(a)*380,cy+Math.sin(a)*180-100,22,t+k,'#FDE047')}
    pop(t,rl(1,4)+.6,'Sweet dreams... ✨',540,1000,66,'#fff','#7C3AED');pop(t,rl(1,4)+8,'Let\'s fly! ☁️',540,1000,70,'#fff','#2563EB')}
  else if(v===2){
    if(L===0){const sc=easeInOut(prog(t,rl(2,0),rl(2,1)))*1700;townSea(t,sc);const cy=1050+Math.sin(t*1.4)*30;
      for(let k=0;k<3;k++)ell(540+(k-1)*160,cy+150,140,60,'rgba(255,255,255,.95)');g.save();g.translate(540,cy);g.rotate(Math.sin(t*1.5)*.08);cradle(0,0,.8,0,{sleep:0,noRock:1});g.restore();
      pop(t,rl(2,0)+.4,'Over the rooftops! 🏠',540,820,62,'#fff','#2563EB');pop(t,rl(2,0)+4,'Down to the sea! 🌊',540,820,62,'#fff','#0EA5E9')}
    else if(L===1){nightRoom(t);adult('mom',460,1820,{s:1.15,t,pose:'hold',happy:1});g.save();g.translate(640,1490);ell(0,0,90,60,'#93C5FD');ell(20,-70,58,54,'#FFE4D6');g.fillStyle='#FFFFFF';g.beginPath();g.ellipse(20,-96,60,38,0,Math.PI,0);g.fill();
      g.strokeStyle='#3F2A1E';g.lineWidth=5;g.beginPath();g.arc(0,-68,8,Math.PI*1.1,Math.PI*1.9);g.stroke();g.beginPath();g.arc(40,-68,8,Math.PI*1.1,Math.PI*1.9);g.stroke();g.strokeStyle='#9F1239';g.beginPath();g.arc(20,-48,9,.2,Math.PI-.2);g.stroke();g.restore();
      const hp=backOut(prog(t,rl(2,1)+.3,rl(2,1)+1.3));g.save();g.translate(540,1000);g.scale(hp,hp);txt('♥',0,0,240+Math.sin(t*6)*12,'#EC4899',null);g.restore();heartsUp(540,1300,t,8,300);
      pop(t,rl(2,1)+1.4,'So dear to me! 💖',540,780,60,'#fff','#DB2777')}
    else if(L===2){sky('#FBCFE8','#FDF2F8');for(let k=0;k<12;k++){g.globalAlpha=.25;starShape(rnd(k)*W,600+rnd(k+2)*1200,26,0,'#F9A8D4')}g.globalAlpha=1;babyClose(t,{open:1,hands:1});
      pop(t,rl(2,2)+.4,'Tiny fingers! 👶',540,820,64,'#fff','#DB2777');pop(t,rl(2,2)+3.4,'Bright eyes! ✨',540,820,64,'#fff','#2563EB')}
    else{const mq=prog(t,rl(2,3)+2.5,RCARD);nightRoom(t,{morning:mq});cradle(560,1660,1.1,t,{sleep:1});if(mq<.3)zzz(640,1380,t,1.3);else heartsUp(560,1250,t,5,160,'#FBBF24');
      pop(t,rl(2,3)+.4,'Night night... 🌙',540,1000,64,'#fff','#7C3AED');pop(t,rl(2,3)+4.6,'Good morning! ☀️',540,1000,66,'#fff','#EA580C')}}
  else{nightRoom(t,{morning:1});cradle(560,1660,1.1,t,{sleep:0});heartsUp(560,1250,t,5,160,'#FBBF24')}
  g.restore();
  if(t>=RCARD){const q=easeOut(prog(t,RCARD,RCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#4C1D95';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,RCARD,RCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Sleep tight, baby! 💖',W/2,990,68,'#fff','#DB2777');
    const sp=backOut(prog(t,RCARD+.5,RCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<RCARD){rbtitle(t);rbcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,REND-1.2,REND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawRock;
