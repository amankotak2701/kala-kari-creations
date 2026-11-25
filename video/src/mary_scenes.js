// ================= "Mary Had A Little Lamb" — Christmas edition (Popcorn Productions) =================
const MBAR=2.824, MV0=5.92, MVERSE=10*MBAR;            // 4/4, 1 line = 1 bar, verse = 8 sung bars + 2 bars interlude
const mv=k=>MV0+k*MVERSE, mline=(v,l)=>mv(v)+l*MBAR;
const MSING_END=mline(4,4)+.3, MEND=136.0, MCARD=130.6;
const mbeat=MBAR/4;
const mpulse=t=>Math.pow(Math.sin(Math.PI*((((t-MV0)/mbeat)%1+1)%1)),2);
KIDS.push({skin:'#F1C9A5',hair:'#7A4A2A',style:1,coat:'#DC2626',pants:'#1E3A8A'}); // Mary = KIDS[5]
const MARY=5;
FAM.teacher={skin:'#D9A273',hair:'#3B2A1A',style:'bun',top:'#0EA5E9',bottom:'#334155',glasses:1,skirt:1};

function lamb(x,y,s,t,o={}){const d=o.dir||1;const hop=o.hop?Math.abs(Math.sin(t*Math.PI/mbeat))*40:0;g.save();g.translate(x,y-hop);g.scale(s*d,s);if(o.rot)g.rotate(o.rot);
  const lg=(lx,p)=>{const a=o.walk?Math.sin(t*8+p)*.35:0;g.save();g.translate(lx,-60);g.rotate(a);rr(-10,0,20,62,8,'#3F3A36');ell(0,62,12,7,'#1F1B18');g.restore()};
  lg(-55,0);lg(40,Math.PI);
  // fluffy body
  const puffs=[[-70,-90,40],[-30,-115,44],[20,-115,44],[60,-90,40],[-55,-55,38],[0,-60,46],[50,-55,38],[-10,-90,50]];
  puffs.forEach(([px,py,r])=>ell(px,py,r+4,r+4,'#E5E7EB'));puffs.forEach(([px,py,r])=>ell(px,py,r,r,'#FFFFFF'));
  ell(-95,-95,16,14,'#FFFFFF');
  lg(-30,Math.PI);lg(62,0);
  // head
  g.save();g.translate(95,-120);g.rotate(o.look||0);
  ell(-28,-28,26,13,'#3F3A36',-.5);ell(30,-30,26,13,'#3F3A36',.5);ell(-26,-28,16,7,'#F9A8D4',-.5);
  ell(0,0,40,48,'#3F3A36');[[-20,-40,18],[0,-48,20],[20,-40,18]].forEach(([a,b,r])=>ell(a,b,r,r,'#FFFFFF'));
  if(o.sleep){g.strokeStyle='#fff';g.lineWidth=4;g.beginPath();g.arc(-13,0,8,Math.PI*.15,Math.PI*.85);g.stroke();g.beginPath();g.arc(13,0,8,Math.PI*.15,Math.PI*.85);g.stroke()}
  else{ell(-13,-2,9,11,'#FFFFFF');ell(13,-2,9,11,'#FFFFFF');ell(-11,0,5,7,'#111');ell(15,0,5,7,'#111');ell(-9,-3,2,2,'#fff');ell(17,-3,2,2,'#fff')}
  ell(-22,18,8,5,'rgba(249,168,212,.7)');ell(22,18,8,5,'rgba(249,168,212,.7)');
  g.strokeStyle='#fff';g.lineWidth=3;g.beginPath();g.arc(0,22,8,.2,Math.PI-.2);g.stroke();
  if(o.hat){g.save();g.translate(0,-50);g.rotate(-.3);g.fillStyle=RED;g.beginPath();g.moveTo(-34,8);g.quadraticCurveTo(0,-70,-60,-50);g.quadraticCurveTo(-5,-38,34,8);g.fill();ell(-62,-50,10,10,'#fff');rr(-38,0,76,16,8,'#fff');g.restore()}
  g.restore();
  // scarf + bell
  rr(55,-95,50,22,10,'#DC2626');rr(62,-80,18,44,8,'#DC2626');bell(98,-62,.22,Math.sin(t*9)*.4);
  g.restore()}
function schoolHouse(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);
  rr(-260,-300,520,300,10,'#B4432E');for(let j=0;j<10;j++)for(let k=0;k<9;k++)rr(-260+k*58+(j%2)*29,-300+j*30,54,26,3,'rgba(0,0,0,.08)');
  g.fillStyle='#7C2D12';g.beginPath();g.moveTo(-300,-300);g.lineTo(0,-470);g.lineTo(300,-300);g.fill();g.fillStyle='#fff';g.beginPath();g.moveTo(-300,-300);g.lineTo(0,-472);g.lineTo(300,-300);g.lineTo(275,-290);g.lineTo(0,-445);g.lineTo(-275,-290);g.fill();
  rr(-60,-600,120,140,6,'#B4432E');g.fillStyle='#7C2D12';g.beginPath();g.moveTo(-80,-600);g.lineTo(0,-680);g.lineTo(80,-600);g.fill();bell(0,-540,.6,Math.sin(t*3)*.3);
  rr(-150,-370,300,56,10,'#FDE68A');txt('SCHOOL',0,-342,40,'#7C2D12',null);
  rr(-60,-170,120,170,8,'#5A2E0E');ell(0,-200,50,50,'#15803D');ell(0,-200,30,30,'#B4432E');ell(0,-245,14,10,'#DC2626');
  [[-190,-230],[130,-230]].forEach(([wx,wy])=>{rr(wx,wy,80,90,6,'#FDE68A');g.strokeStyle='#fff';g.lineWidth=5;g.strokeRect(wx,wy,80,90)});
  for(let k=0;k<13;k++){const bx=-260+k*43;const on=(Math.floor(t*3)+k)%3;ell(bx,-292,7,10,['#EF4444','#22C55E','#FBBF24','#3B82F6'][(k+on)%4])}
  g.restore()}
function classroom(t){const w=g.createLinearGradient(0,0,0,1400);w.addColorStop(0,'#FDE9C8');w.addColorStop(1,'#F6D3A1');g.fillStyle=w;g.fillRect(0,0,W,1400);
  rr(150,560,780,400,16,'#7C4A21');rr(175,585,730,350,8,'#1F4E3D');
  g.save();g.font='700 64px Fredoka';g.textAlign='center';g.fillStyle='rgba(255,255,255,.9)';g.fillText('Merry Christmas!',540,680);g.restore();
  g.save();g.globalAlpha=.85;g.translate(400,830);g.scale(.45,.45);g.strokeStyle='#fff';g.lineWidth=6;[[-70,-90,40],[-30,-115,44],[20,-115,44],[60,-90,40],[0,-60,46]].forEach(([a,b,r])=>{g.beginPath();g.arc(a,b,r,0,7);g.stroke()});g.beginPath();g.ellipse(95,-120,40,48,0,0,7);g.stroke();g.restore();
  txt('🐑 + 🎄 = ❤️',700,840,50,'#fff',null);
  for(let k=0;k<9;k++){const x=60+k*120,y=480+Math.sin(k)*20;g.strokeStyle='#94A3B8';g.lineWidth=2;g.beginPath();g.moveTo(x,440);g.lineTo(x,y);g.stroke();starShape(x,y+20,24,t*.5+k,'#FFFFFF');starShape(x,y+20,12,t*.5+k,'#BFDBFE')}
  g.strokeStyle='#15803D';g.lineWidth=14;g.beginPath();g.moveTo(0,430);for(let x=0;x<=W;x+=216)g.quadraticCurveTo(x+108,480,x+216,430);g.stroke();
  const fl=g.createLinearGradient(0,1390,0,H);fl.addColorStop(0,'#A16207');fl.addColorStop(1,'#713F12');g.fillStyle=fl;g.fillRect(0,1390,W,H-1390);
  xmasTree(960,1420,.45,t,1)}
function desk(x,y){rr(x-90,y-20,180,26,6,'#B45309');rr(x-80,y+6,16,90,4,'#78350F');rr(x+64,y+6,16,90,4,'#78350F');rr(x-30,y-48,60,30,4,'#FBBF24')}
function snowyVillage(t,scroll=0,night=0){winterSky(t,night);if(night){for(let k=0;k<60;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*1000,2.5,2.5,'#fff')}g.globalAlpha=1}else{cloud(((t*30)%1400)-300,560,1);cloud(((t*18+700)%1400)-300,700,.8)}
  snowHills(t,scroll,1350);for(let k=0;k<6;k++){const px=((k*300-scroll*.8)%1800+1800)%1800-300;k%2?house(px,1420,.9,t,['#B45309','#2563EB','#7C3AED'][k%3]):pine(px,1440,1.0)}}
function mtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#DC2626';g.beginPath();g.roundRect(-420,-66,840,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#F5C542';g.stroke();txt('Mary Had A Little Lamb 🐑',0,2,52,'#FFFFFF',null);g.restore()}
const MLYR=[
 ['Mary had a little lamb,','little lamb, little lamb,','Mary had a little lamb,','its fleece was white as snow.','And everywhere that Mary went,','Mary went, Mary went,','everywhere that Mary went,','the lamb was sure to go.'],
 ['It followed her to school one day,','school one day, school one day,','it followed her to school one day,','which was against the rules.','It made the children laugh and play,','laugh and play, laugh and play,','it made the children laugh and play','to see a lamb at school.'],
 ['And so the teacher turned it out,','turned it out, turned it out,','and so the teacher turned it out,','but still it lingered near.','And waited patiently about,','patiently about, patiently about,','and waited patiently about','till Mary did appear.'],
 ['Why does the lamb love Mary so,','Mary so, Mary so?','Why does the lamb love Mary so?','the eager children cried.','Why, Mary loves the lamb, you know,','lamb, you know, lamb, you know,','Mary loves the lamb, you know,','the teacher did reply.'],
 ['Mary had a little lamb,','little lamb, little lamb,','Mary had a little lamb,','its fleece was white as snow!']];
const MCAP=[];MLYR.forEach((v,vi)=>{for(let p=0;p<v.length/2;p++){const a=mline(vi,2*p)-.25,b=(p===v.length/2-1)?mline(vi,2*p+2)+(vi===4?.6:0):mline(vi,2*p+2)-.25;MCAP.push([a,b,v[2*p]+' '+v[2*p+1]])}});
function mcaption(t){const i=MCAP.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=MCAP[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 58px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*72+40,y0=390;g.fillStyle='rgba(30,58,138,.86)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#F5C542';g.stroke();
  const prg=clamp((t-a)/((b-a)*.92));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+36+li*72,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}
function hearts(x,y,t,n=5,spread=60){for(let k=0;k<n;k++){const p=((t*.6+k/n)%1);g.save();g.globalAlpha=1-p;txt('♥',x+Math.sin(p*6+k)*spread,y-p*260,48,'#FB7185',null);g.restore()}}
function pop(t,t0,s,x,y,size,col='#fff',st=RED){const p=prog(t,t0,t0+1.8);if(p<=0||p>=1)return;g.save();g.globalAlpha=Math.min(1,p*6,(1-p)*4);g.translate(x,y);const q=backOut(Math.min(1,p*3));g.scale(q,q);txt(s,0,0,size,col,st);g.restore()}

function drawMary(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const L=(v)=>Math.floor((t-mv(v))/MBAR);
  if(t<mline(0,4)-.2){ // intro + "Mary had a little lamb... white as snow" in the snowy meadow
    winterSky(t);cloud(150,600,1);cloud(760,700,.8);snowHills(t,0,1330);pine(130,1430,.9);pine(950,1450,.8);
    snowman(900,1520,.5,t,3);
    kid(MARY,320,1720,{s:1.35,t,happy:1,trunk:mpulse(t)>.6?1:.5});lamb(690,1720,1.5,t,{hop:t>MV0,dir:-1});
    if(t<MV0){const q=backOut(prog(t,.5,1.6));g.save();g.translate(540,1000);g.scale(q,q);txt('Baa! 🐑',0,0,100,'#fff',RED);g.restore()}
    if(t>mline(0,3)-.2){for(let k=0;k<40;k++){const a=k/40*Math.PI*2+t;const r=120+((t*120+k*20)%240);starShape(690+Math.cos(a)*r,1560+Math.sin(a)*r*.6,8,a,'#FFFFFF')}pop(t,mline(0,3),'White as snow! ❄️',540,1000,76,'#fff','#1E3A8A')}
  }
  else if(t<mv(1)+MBAR*0-.2){ // everywhere that Mary went (walk through the Christmas village)
    const sc=(t-mline(0,4))*220;snowyVillage(t,sc);
    const bob=Math.abs(Math.sin(t*Math.PI/mbeat))*14;
    kid(MARY,640,1730-bob,{s:1.3,t,happy:1,trunk:.5,dir:1});lamb(280,1720,1.25,t,{hop:1,walk:1,dir:1});
    for(let k=0;k<6;k++){const px=((k*180-sc)%1200+1200)%1200-60;ell(px,1720,16,8,'rgba(120,140,180,.35)')}
    if(t>mline(0,8)-.2){const q=easeOut(prog(t,mline(0,8),mv(1)));g.save();g.translate(lerp(1400,800,q),0);schoolHouse(0,1500,.8,t);g.restore()}
  }
  else if(t<mline(1,4)-.2){ // followed her to school; against the rules
    winterSky(t);cloud(200,600,1);snowHills(t,0,1400);schoolHouse(540,1500,1.0,t);pine(100,1480,.8);pine(980,1500,.8);
    const q=easeOut(prog(t,mv(1),mline(1,3)));kid(MARY,lerp(120,560,q),1760,{s:1.15,t,happy:1});lamb(lerp(-150,270,q),1750,1.1,t,{hop:q<1,walk:q<1});
    if(t>mline(1,3)-.3){const p=backOut(prog(t,mline(1,3)-.3,mline(1,3)+.3));g.save();g.translate(800,1000);g.scale(p,p);g.rotate(Math.sin(t*6)*.05);rr(-200,-90,400,180,20,'#FFFFFF');g.lineWidth=10;g.strokeStyle='#DC2626';g.stroke();txt('No lambs',0,-28,52,'#DC2626',null);txt('at school! 🚫',0,38,48,'#1F2937',null);g.restore()}
  }
  else if(t<mv(2)-.2){ // laugh and play in the classroom
    classroom(t);
    [[0,200],[1,420],[3,660],[2,880]].forEach(([k,x],i)=>{const j=mpulse(t+i*.12)*50;desk(x,1560);kid(k,x,1830-j,{s:.88,t,happy:1,trunk:1})});
    lamb(540+Math.sin(t*1.5)*250,1720,1.05,t,{hop:1,dir:Math.cos(t*1.5)>0?1:-1});kid(MARY,120,1780,{s:.95,t,happy:1,trunk:1});
    for(let k=0;k<4;k++){const p=((t*.8+k/4)%1);g.save();g.globalAlpha=1-p;txt(['Ha ha!','Hee hee!','😂','Baa!'][k],180+k*240,1180-p*200,58,'#fff',RED);g.restore()}
  }
  else if(t<mline(2,4)-.2){ // teacher turns the lamb out; lingers near the window
    const l=L(2);
    if(l<2||t<mline(2,2)){classroom(t);adult('teacher',780,1790,{s:1.05,t,pose:'wave',happy:0});const q=easeOut(prog(t,mline(2,0)+.5,mline(2,2)));lamb(lerp(520,-200,q),1770,1.05,t,{walk:1,dir:-1});kid(MARY,300,1800,{s:.95,t,happy:0});
      pop(t,mline(2,0)+.3,'Out you go! 👉',540,1100,70,'#fff','#0369A1')}
    else{classroom(t);g.save();g.beginPath();g.roundRect(330,970,420,330,20);g.clip();winterSky(t);snowHills(t,0,1200);lamb(540,1290,.7,t,{look:Math.sin(t*2)*.15});g.restore();
      g.strokeStyle='#F5E1C0';g.lineWidth=16;g.beginPath();g.roundRect(330,970,420,330,20);g.stroke();g.lineWidth=8;g.beginPath();g.moveTo(540,970);g.lineTo(540,1300);g.stroke();
      adult('teacher',900,1800,{s:1.0,t,pose:'sway'});kid(MARY,180,1810,{s:.95,t,happy:0});pop(t,mline(2,3),'Peek-a-boo! 👀',540,900,64,'#fff','#7C2D12')}
  }
  else if(t<mv(3)-.2){ // waited patiently... till Mary did appear (+ interlude hug)
    winterSky(t);cloud(150,600,1);snowHills(t,0,1400);schoolHouse(540,1500,1.0,t);
    const l=L(2);
    if(l<7){lamb(330,1760,1.3,t,{sleep:l>=5,dir:1});if(l>=5)zzz(480,1440,t,1.4);
      const ck=Math.floor((t-mline(2,4))/mbeat);g.save();g.translate(820,1100);g.scale(.6,.6);clockFace(0,0,1,t);g.restore();
      for(let k=0;k<20;k++){const y=((t*80+rnd(k)*500)%500)+1300;ell(300+(rnd(k+2)-.5)*260,y-300,5,5,'#fff')}}
    else{const q=backOut(prog(t,mline(2,7),mline(2,7)+.8));kid(MARY,lerp(640,520,q),1760,{s:1.3,t,happy:1,trunk:1});lamb(300,1760-Math.abs(Math.sin(t*6))*30,1.3,t,{dir:1});
      hearts(420,1250,t,6,90);pop(t,mline(2,7)+.2,'Mary! 💖',540,1000,90,'#fff','#BE185D')}
  }
  else if(t<mline(3,4)-.2){ // why does the lamb love Mary so? (children ask)
    winterSky(t);cloud(150,600,1);snowHills(t,0,1400);pine(120,1460,.9);pine(960,1470,.9);
    kid(MARY,430,1720,{s:1.25,t,happy:1});lamb(700,1720,1.2,t,{dir:-1,hop:mpulse(t)>.7});
    [[0,130],[1,290],[3,850],[2,990]].forEach(([k,x],i)=>{kid(k,x,1830,{s:.85,dir:x<540?1:-1,t,happy:0,trunk:(Math.floor(t/MBAR)+i)%2?1:.5});const p=((t*.7+i/4)%1);g.save();g.globalAlpha=1-p;txt('?',x,1460-p*200,70,'#fff','#7C3AED');g.restore()});
    pop(t,mline(3,0)+.3,'Why? 🤔',540,1050,90,'#fff','#7C3AED');
  }
  else if(t<mv(4)-.2){ // Mary loves the lamb, you know (teacher replies), then Santa arrives
    winterSky(t,t>mline(3,8)-.2);snowHills(t,0,1400);
    if(t<mline(3,8)-.2){pine(120,1460,.9);adult('teacher',900,1760,{s:1.1,t,pose:'sway',happy:1});
      kid(MARY,330,1760,{s:1.25,t,happy:1,trunk:1});lamb(620,1750,1.2,t,{dir:-1});
      const b=1+.08*mpulse(t);g.save();g.translate(500,1150);g.scale(b,b);txt('❤️',0,0,200,'#fff',null);g.restore();hearts(500,1400,t,6,120);
      pop(t,mline(3,4)+.3,'Mary loves the lamb! 💕',540,880,68,'#fff','#BE185D')}
    else{for(let k=0;k<50;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*900,2.5,2.5,'#fff')}g.globalAlpha=1;moonFace(820,640,80,t,0,1);
      xmasTree(540,1450,.9,t,1);const q=easeOut(prog(t,mline(3,8),mline(3,8)+1.5));santa(lerp(1300,820,q),1700,.85,t,{wave:1,sack:1});
      kid(MARY,250,1760,{s:1.15,t,happy:1,trunk:1});lamb(520,1760,1.1,t,{dir:1,hat:q>.9,hop:1});
      if(q>.9)pop(t,mline(3,8)+1.6,'A gift for Lamb! 🎁',540,900,70,'#fff',RED);hoho(540,820,t,mline(3,8)+.2)}
  }
  else{ // final chorus at the Christmas tree + end card
    winterSky(t,1);for(let k=0;k<60;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*1000,2.5,2.5,'#fff')}g.globalAlpha=1;
    snowHills(t,0,1420);xmasTree(540,1470,.85,t,1);
    [[0,120],[1,260],[3,820],[2,960]].forEach(([k,x],i)=>kid(k,x,1830-mpulse(t+i*.1)*40,{s:.82,dir:x<540?1:-1,t,happy:1,trunk:1}));
    kid(MARY,390,1770,{s:1.1,t,happy:1,trunk:1});lamb(670,1770,1.1,t,{dir:-1,hat:1,hop:1});santa(540,1620,.5,t,{wave:1});
    if(t>mline(4,3)){for(let k=0;k<60;k++){const a=k/60*Math.PI*2;const r=easeOut(prog(t,mline(4,3),MSING_END))*600;starShape(540+Math.cos(a)*r,1300+Math.sin(a)*r*.8,10,a+t,'#FFFFFF')}}
    if(t>=MCARD){const q=easeOut(prog(t,MCARD,MCARD+1));g.save();g.globalAlpha=q*.7;g.fillStyle='#0B1446';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
      popcornLogo(W/2,560,.9*backOut(prog(t,MCARD,MCARD+1.2)),Math.max(0,Math.sin(Math.PI*prog(t,MCARD+1.2,MCARD+1.7)))*.25);
      txt('A Popcorn Productions video',W/2,940,46,'#FFE14D',null,'center',600);txt('Merry Christmas! 🎄🐑',W/2,1060,78,'#fff',RED);
      const sp=backOut(prog(t,MCARD+1.4,MCARD+2.4));g.save();g.translate(W/2,1220);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  }
  snowfall(t,t>=mv(1)+3*MBAR&&t<mline(2,4)?0:55,.7);
  [mline(0,4)-.2,mv(1)-.2,mline(1,4)-.2,mv(2)-.2,mline(2,4)-.2,mv(3)-.2,mline(3,4)-.2,mline(3,8)-.2,mv(4)-.2].forEach(c=>{const d=Math.abs(t-c);if(d<.22){g.fillStyle=`rgba(255,255,255,${(1-d/.22)*.75})`;g.fillRect(0,0,W,H)}});
  if(t<MCARD){mtitle(t);mcaption(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,MEND-1.5,MEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawMary;
