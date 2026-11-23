// ================= "Jingle Bells" (music: Sascha Ende, CC BY 4.0) — Popcorn Productions =================
const OFF=15.38, U=0.313, BARJ=8*U, X0=20.39;            // audio offset, beat unit, bar, first chorus downbeat
const bar=n=>X0+n*BARJ;                                    // audio time of bar n
const jb=t=>Math.pow(Math.sin(Math.PI*((((t-X0)/(2*U))%1+1)%1)),2); // pulse per quarter
const swingJ=t=>Math.sin(2*Math.PI*(t-X0)/(4*U));
const JEND=bar(64);                                        // audio end
ELE.push({c:'#F2A04E',bl:'#15803D',name:'Gappu'});
const RED='#D62839',GRN='#1B7F3B',SNOW='#F4F8FF';

// ---------- winter elements ----------
function winterSky(t,night=0){if(night)sky('#0C1B4D','#3B4DA0');else sky('#8EC9F5','#E3F2FF')}
function snowfall(t,n=90,spd=1){for(let k=0;k<n;k++){const r=2+rnd(k)*6,sp=(60+rnd(k+1)*90)*spd;const y=((t*sp+rnd(k+2)*H)%(H+40))-20;const x=(rnd(k+3)*W+Math.sin(t*(.6+rnd(k))+k)*40)%W;g.globalAlpha=.6+.4*rnd(k+4);ell(x,y,r,r,'#FFFFFF')}g.globalAlpha=1}
function snowHills(t,scroll=0,y0=1350){[[ '#DCE8F7',y0-120,80,.004,.25],['#EEF4FC',y0-30,60,.006,.55],[SNOW,y0+60,40,.008,1]].forEach(([c,y,a,f,p],k)=>{g.fillStyle=c;g.beginPath();g.moveTo(0,H);
  for(let x=0;x<=W;x+=20)g.lineTo(x,y+Math.sin((x+scroll*p)*f+k*2)*a);g.lineTo(W,H);g.fill()})}
function pine(x,y,s,snow=1){g.save();g.translate(x,y);g.scale(s,s);rr(-14,-20,28,40,6,'#6B4220');
  for(let k=0;k<3;k++){const w=150-k*35,yy=-30-k*85;g.fillStyle=k%2?'#1E6B3A':'#17803F';g.beginPath();g.moveTo(-w/2,yy);g.lineTo(0,yy-130);g.lineTo(w/2,yy);g.fill();
    if(snow){g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(-w/2,yy);g.quadraticCurveTo(-w/4,yy-25,0,yy-10);g.quadraticCurveTo(w/4,yy-25,w/2,yy);g.quadraticCurveTo(0,yy+8,-w/2,yy);g.fill()}}
  g.restore()}
function bell(x,y,s,rot,col='#F5C542'){g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);
  g.fillStyle=col;g.beginPath();g.moveTo(-40,30);g.quadraticCurveTo(-42,-40,0,-48);g.quadraticCurveTo(42,-40,40,30);g.quadraticCurveTo(0,40,-40,30);g.fill();
  ell(0,32,44,10,shade(col,-.2));ell(0,44,10,10,'#B7791F');ell(-14,-18,8,16,'rgba(255,255,255,.5)',-.3);
  g.strokeStyle=RED;g.lineWidth=8;g.beginPath();g.arc(0,-52,10,Math.PI,0);g.stroke();g.restore()}
function bellPair(x,y,s,t){const r=swingJ(t)*.35;
  g.save();g.translate(x,y);g.fillStyle=GRN;for(let k=0;k<5;k++){ell(-30+k*15,-8,18,10,GRN,k*.6)}
  bell(-38,40,s,r);bell(38,40,s,-r);ell(0,-5,22,14,RED);g.fillStyle=RED;g.beginPath();g.moveTo(0,-5);g.lineTo(-45,30);g.lineTo(-25,30);g.closePath();g.moveTo(0,-5);g.lineTo(45,30);g.lineTo(25,30);g.closePath();g.fill();g.restore()}
function santaHat(o){ // drawn in elephant-local coords
  g.save();g.translate(100,-240);g.rotate(-.25);
  g.fillStyle=RED;g.beginPath();g.moveTo(-85,20);g.quadraticCurveTo(-10,-130,-150,-95);g.quadraticCurveTo(-30,-70,85,20);g.fill();
  ell(-152,-95,22,22,'#fff');rr(-92,5,184,36,18,'#fff');g.restore()}
function scarf(){g.save();rr(30,-150,120,34,16,RED);g.fillStyle='#fff';for(let k=0;k<4;k++)g.fillRect(45+k*28,-150,10,34);rr(40,-130,30,80,12,RED);g.restore()}
function santaEle(i,x,y,o={}){g.save();g.translate(x,y);elephant(i,0,0,Object.assign({noShadow:1},o));
  const s=o.s||1,d=o.dir||1;g.scale(s*d,s);if(o.rot)g.rotate(o.rot);scarf();santaHat();g.restore()}
function pony(x,y,s,t,run=1,tired=0){g.save();g.translate(x,y);g.scale(s,s);const B=tired?'#A08670':'#C47A3D',D=shade(B,-.25);
  const ph=t*(run?7:0);
  const leg=(lx,p,front)=>{const a=run?Math.sin(ph+p)*.5:0;g.save();g.translate(lx,-90);g.rotate(a);rr(-12,0,24,90,10,front?B:D);ell(0,92,16,9,'#3A2A1A');g.restore()};
  leg(-60,Math.PI,0);leg(55,0,0);
  // tail with bell (bobtail)
  g.save();g.translate(-110,-150);g.rotate(-.4+Math.sin(t*6)*.25);ell(-20,10,22,40,'#5A3A20',.5);bell(-35,45,.35,Math.sin(t*9)*.4);g.restore();
  ell(0,-130,120,60,B);
  // harness
  rr(-40,-185,26,110,8,RED);for(let k=0;k<4;k++)bell(-27,-170+k*28,.22,Math.sin(t*10+k)*.3);
  // neck/head
  g.save();g.translate(95,-170);g.rotate(-.5);rr(-28,-90,60,120,28,B);g.restore();
  ell(150,-250,62,44,B,.3);ell(195,-232,30,24,shade(B,.2));ell(200,-240,5,4,'#3A2A1A');
  ell(130,-300,12,24,D,-.3);// ear
  // mane
  for(let k=0;k<6;k++)ell(85+k*12,-255+k*14,16,24,'#5A3A20',.6);
  if(tired){g.strokeStyle='#3A2A2A';g.lineWidth=5;g.beginPath();g.arc(160,-262,10,Math.PI*.1,Math.PI*.9);g.stroke();
    g.fillStyle='#7FD3F5';g.beginPath();g.moveTo(120,-300);g.quadraticCurveTo(132,-280,120,-272);g.quadraticCurveTo(108,-280,120,-300);g.fill()}
  else{ell(162,-262,11,13,'#fff');ell(165,-262,7,9,'#2A1A1A');ell(167,-266,3,3,'#fff')}
  g.strokeStyle='#3A2A2A';g.lineWidth=4;g.beginPath();g.arc(205,-222,10,.2,Math.PI-.2);g.stroke();
  leg(-35,0,1);leg(80,Math.PI,1);g.restore()}
function sleigh(x,y,s,t,riders=[0,1,2],o={}){g.save();g.translate(x,y);g.scale(s,s);
  const bob=Math.sin(t*9)*4;g.translate(0,bob);
  // back panel
  g.fillStyle='#A81E2C';g.beginPath();g.moveTo(-240,-150);g.quadraticCurveTo(-270,-300,-200,-310);g.lineTo(-170,-160);g.fill();
  // riders
  riders.forEach((r,k)=>{const jb_=jb(t+k*.1);santaEle(r,-150+k*120,-110-jb_*18,{s:.55,t,trunk:o.trunks??(.5+jb_*.5),happy:o.happy??1,dir:1})});
  // body
  g.fillStyle=RED;g.beginPath();g.moveTo(-250,-170);g.lineTo(200,-170);g.quadraticCurveTo(300,-170,290,-260);g.quadraticCurveTo(330,-260,320,-200);g.quadraticCurveTo(300,-60,180,-50);g.lineTo(-220,-50);g.quadraticCurveTo(-260,-60,-250,-170);g.fill();
  g.strokeStyle='#F5C542';g.lineWidth=10;g.stroke();
  for(let k=0;k<5;k++){g.strokeStyle='#F5C542';g.lineWidth=5;g.beginPath();g.arc(-160+k*80,-110,22,0,Math.PI*2);g.stroke();ell(-160+k*80,-110,8,8,'#F5C542')}
  // runners
  g.strokeStyle='#E5B53A';g.lineWidth=12;g.lineCap='round';g.beginPath();g.moveTo(-240,0);g.lineTo(240,0);g.quadraticCurveTo(320,0,320,-60);g.quadraticCurveTo(320,-90,290,-80);g.stroke();
  g.lineWidth=9;[-160,0,160].forEach(px=>{g.beginPath();g.moveTo(px,-50);g.lineTo(px,0);g.stroke()});
  g.restore()}
function team(x,y,s,t,riders,o={}){ // pony + sleigh, moving right
  sleigh(x,y,s,t,riders,o);pony(x+ (o.ponyGap||480)*s,y,s*1.0,t,o.run??1,o.tired);
  g.strokeStyle='#5A3A20';g.lineWidth=5*s;g.beginPath();g.moveTo(x+310*s,y-200*s);g.quadraticCurveTo(x+400*s,y-120*s,x+(o.ponyGap||480)*s-40*s,y-160*s);g.stroke()}
function house(x,y,s,t,col='#B45309'){g.save();g.translate(x,y);g.scale(s,s);rr(-110,-150,220,150,8,col);
  g.fillStyle='#7C2D12';g.beginPath();g.moveTo(-140,-150);g.lineTo(0,-260);g.lineTo(140,-150);g.fill();g.fillStyle='#fff';g.beginPath();g.moveTo(-140,-150);g.lineTo(0,-262);g.lineTo(140,-150);g.lineTo(120,-140);g.lineTo(0,-235);g.lineTo(-120,-140);g.fill();
  rr(-80,-110,55,55,6,'#FDE68A');rr(25,-110,55,55,6,'#FDE68A');rr(-25,-80,50,80,6,'#5A2E0E');
  for(let k=0;k<9;k++){const bx=-130+k*32,by=-150+Math.abs(k-4)*-24+10;const on=(Math.floor(t*3)+k)%3;ell(bx,by+18,7,10,['#EF4444','#22C55E','#FBBF24','#3B82F6'][(k+on)%4])}
  g.restore()}
function xmasTree(x,y,s,t,deco=1){g.save();g.translate(x,y);g.scale(s,s);rr(-30,-40,60,60,8,'#6B4220');
  const L=[[300,-40],[240,-200],[180,-350],[120,-490]];
  L.forEach(([w,yy],k)=>{g.fillStyle=k%2?'#15803D':'#16A34A';g.beginPath();g.moveTo(-w/2-20,yy);g.lineTo(0,yy-220);g.lineTo(w/2+20,yy);g.quadraticCurveTo(0,yy+30,-w/2-20,yy);g.fill()});
  const cols=['#EF4444','#FBBF24','#3B82F6','#EC4899','#A855F7','#F97316'];
  for(let k=0;k<22;k++){const p=k/22;const yy=-60-p*560,ww=(1-p)*150;const xx=(rnd(k)*2-1)*ww;
    if(p<deco){const pop=backOut(clamp((deco-p)*6));ell(xx,yy,14*pop,14*pop,cols[k%6]);ell(xx-4,yy-4,4*pop,4*pop,'rgba(255,255,255,.7)')}}
  if(deco>.95){const tw=1+.12*jb(t);g.save();g.translate(0,-700);g.scale(tw,tw);glow(0,0,90,'rgba(255,230,120,.6)');starShape(0,0,50,0,'#FFD84D');g.restore()}
  g.restore()}
function snowman(x,y,s,t,stage=3){g.save();g.translate(x,y);g.scale(s,s);
  if(stage>=1){ell(0,-90,110,95,'#FFFFFF');ell(-30,-120,40,30,'rgba(200,220,240,.5)')}
  if(stage>=2){ell(0,-240,80,70,'#FFFFFF');for(let k=0;k<3;k++)ell(0,-270+k*35,8,8,'#1F2937')}
  if(stage>=3){ell(0,-360,60,55,'#FFFFFF');ell(-20,-372,7,8,'#1F2937');ell(20,-372,7,8,'#1F2937');
    g.fillStyle='#F97316';g.beginPath();g.moveTo(0,-358);g.lineTo(55,-350);g.lineTo(0,-345);g.fill();
    for(let k=0;k<5;k++)ell(-24+k*12,-330+Math.abs(k-2)*-3,4,4,'#1F2937');
    rr(-55,-430,110,18,6,'#1F2937');rr(-38,-500,76,75,8,'#1F2937');rr(-38,-445,76,14,0,RED);
    rr(-70,-310,140,26,12,RED);rr(30,-300,28,80,10,RED);
    g.strokeStyle='#6B4220';g.lineWidth=8;g.beginPath();g.moveTo(-70,-250);g.lineTo(-170,-300+Math.sin(t*5)*20);g.moveTo(70,-250);g.lineTo(170,-310);g.stroke()}
  g.restore()}
function present(x,y,w,h,c1,c2,open=0){g.save();g.translate(x,y);rr(-w/2,-h,w,h,6,c1);g.fillStyle=c2;g.fillRect(-10,-h,20,h);
  g.save();g.translate(0,-h-open*80);g.rotate(open*.5);rr(-w/2-8,-24,w+16,26,6,c1);g.fillStyle=c2;g.fillRect(-10,-24,20,26);ell(-22,-34,22,14,c2,-.4);ell(22,-34,22,14,c2,.4);g.restore();g.restore()}
function pond(y){ell(540,y,400,130,'#BFE6F7');ell(540,y,360,105,'#D9F2FC');g.strokeStyle='rgba(255,255,255,.9)';g.lineWidth=6;for(let k=0;k<3;k++){g.beginPath();g.moveTo(300+k*170,y-60+k*25);g.lineTo(380+k*170,y-80+k*25);g.stroke()}}

// ---------- captions (karaoke) ----------
const CH1='Jingle bells, jingle bells, jingle all the way!',CH2='Oh, what fun it is to ride in a one-horse open sleigh, hey!';
const JL=[];
function chorus(b){[CH1,CH2,CH1,CH2].forEach((s,k)=>JL.push([bar(b+k*2),bar(b+k*2+2),s]))}
chorus(0);
['Dashing through the snow','In a one-horse open sleigh','O\'er the fields we go','Laughing all the way — ha ha ha!','Bells on bobtail ring','Making spirits bright','What fun it is to ride and sing','A sleighing song tonight!'].forEach((s,k)=>JL.push([bar(8+k),bar(9+k),s]));
chorus(16);
['A day or two ago','I thought I\'d take a ride','And soon Miss Fanny Bright','Was seated by my side','The horse was lean and lank','Misfortune seemed his lot','He got into a drifted bank','And we — got — upsot!'].forEach((s,k)=>JL.push([bar(28+k),bar(29+k),s]));
chorus(36);chorus(46);
for(let k=0;k<7;k++)JL.push([bar(54+k*1.0)+0.1,bar(55+k*1.0),'La la la la la 🎶']);
function jcaption(t){const i=JL.findIndex(([a,b])=>t>=a-.1&&t<b);if(i<0)return;const [a,b,s]=JL[i];
  const al=Math.min(clamp((t-a+.1)/.2),clamp((b-t)/.15));g.save();g.globalAlpha=al;g.font='700 60px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*74+40,y0=380;g.fillStyle='rgba(120,10,25,.82)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#F5C542';g.stroke();
  const prg=clamp((t-a)/((b-a)*.9));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+37+li*74,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}
function jtitle(t){g.save();g.translate(W/2,170);const p=backOut(prog(t,OFF+.2,OFF+1.2));g.scale(p,p);
  g.fillStyle=RED;g.beginPath();g.roundRect(-330,-70,660,140,70);g.fill();g.lineWidth=8;g.strokeStyle='#F5C542';g.stroke();
  txt('Jingle Bells 🔔',0,2,72,'#FFFFFF',null);g.restore()}

const CAM=()=>{g.save();g.translate(540,1450);g.scale(1.5,1.5);g.translate(-540,-1500)},UNCAM=()=>g.restore();
// ---------- the show ----------
function drawJB(tv){const t=tv+OFF;g.setTransform(1,0,0,1,0,0);g.fillStyle=SNOW;g.fillRect(0,0,W,H);
  if(t<bar(0)){ // intro: snowy village, bells
    winterSky(t);cloud(100,500,1);cloud(700,620,.8);CAM();snowHills(t);house(270,1330,1,t);house(800,1350,.9,t,'#2563EB');pine(530,1360,1.1);UNCAM();
    bellPair(540,760,1.6,t);
    const q=backOut(prog(t,OFF+.4,OFF+1.6));g.save();g.translate(540,1080);g.scale(q,q);txt('Ding dong! 🔔',0,0,100,'#fff',RED);g.restore();
  }
  else if(t<bar(8)||(t>=bar(16)&&t<bar(24))){ // choruses 1 & 2: sleigh ride across hills (day / evening village)
    const night=t>=bar(16);winterSky(t,night);if(night){for(let k=0;k<50;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*900,2.5,2.5,'#fff')}g.globalAlpha=1;moonFace(820,640,80,t,0,1)}
    else{cloud(((t*40)%1400)-300,480,1);cloud(((t*25+600)%1400)-300,640,.8)}
    CAM();const sc=t*260;snowHills(t,sc);
    for(let k=0;k<6;k++){const px=((k*260-sc*.9)%1560+1560)%1560-240;night?house(px,1380,.7,t,['#B45309','#2563EB','#7C3AED'][k%3]):pine(px,1400,.9)}
    team(390,1500,.62,t,[0,1,2]);UNCAM();
    bellPair(150,610,1.0,t);bellPair(930,610,1.0,t+.2);
  }
  else if(t<bar(16)){ // verse 1 vignettes
    const ln=Math.floor((t-bar(8))/BARJ);winterSky(t,ln>=6);
    if(ln>=6){moonFace(800,640,90,t,0,1);for(let k=0;k<40;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*900,2.5,2.5,'#fff')}g.globalAlpha=1}
    CAM();const sc=t*(ln==0?520:260);snowHills(t,sc);
    if(ln==0){for(let k=0;k<7;k++){const px=((k*200-sc*1.2)%1400+1400)%1400-200;pine(px,1420,1.3)}team(390,1520,.62,t,[0,1,2]);
      for(let k=0;k<8;k++){g.strokeStyle='rgba(255,255,255,.7)';g.lineWidth=6;const y=1150+k*40;g.beginPath();g.moveTo(((t*900+k*300)%1300)-200,y);g.lineTo(((t*900+k*300)%1300)-80,y);g.stroke()}}
    else if(ln==1){pony(430,1500,1.4,t,1);sleigh(-160,1500,1.0,t,[0])}
    else if(ln==2){team(420,1440,.5,t,[0,1,2]);for(let k=0;k<3;k++)pine(160+k*380,1600,.7)}
    else if(ln==3){sleigh(560,1500,1.25,t,[0,1,2],{happy:1});for(let k=0;k<3;k++){const p=((t*1.2+k/3)%1);g.save();g.globalAlpha=1-p;txt('Ha ha!',300+k*240,1000-p*200,64,'#fff',RED);g.restore()}}
    else if(ln==4){pony(620,1560,1.7,t,0);g.save();g.translate(250,1100);g.scale(1.6,1.6);bell(0,0,1.2,Math.sin(t*10)*.5);g.restore();notes(250,900,t,bar(12),4)}
    else if(ln==5){team(390,1500,.62,t,[0,1,2]);for(let k=0;k<20;k++){const a=t*2+k;starShape(rnd(k)*W,500+rnd(k+3)*600,10+8*Math.abs(Math.sin(a)),a,'#FDE68A')}}
    else{team(390,1500,.62,t,[0,1,2]);notes(400,1100,t,bar(14),6)}
    UNCAM();
  }
  else if(t<bar(28)){ // instrumental: build a snowman
    winterSky(t);cloud(150,520,1);CAM();snowHills(t);pine(200,1380,.9);pine(880,1400,.8);
    const st=Math.min(3,1+Math.floor((t-bar(24))/(BARJ*.9)));snowman(540,1500,.95,t,st);
    santaEle(0,300,1560,{s:.6,t,trunk:.8,happy:1});santaEle(1,780,1560,{s:.6,dir:-1,t,trunk:.8,happy:1});
    const q=((t-bar(24))%1.25)/1.25;ell(lerp(330,760,q),1300-Math.sin(Math.PI*q)*350,22,22,'#fff');UNCAM();
  }
  else if(t<bar(36)){ // verse 2: ride with Pinky, tired pony, tumble
    const ln=Math.floor((t-bar(28))/BARJ);winterSky(t);cloud(200,520,1);
    CAM();const sc=t*(ln>=4?120:240);snowHills(t,sc);
    for(let k=0;k<5;k++){const px=((k*300-sc)%1500+1500)%1500-200;pine(px,1400,.9)}
    if(ln<6){const riders=ln>=2?[0,4]:[0];team(390,1520,.62,t,riders,{tired:ln>=4});
      if(ln>=2&&ln<4){g.save();g.globalAlpha=prog(t,bar(30),bar(30)+.5);txt('♥',420,1120,60,'#FB7185',null);g.restore()}
      if(ln==5){const cx=390+480*.62+100;bigCloud(cx,850,.45,'#9CA3AF');for(let k=0;k<10;k++){const p=((t*2+k/10)%1);ell(cx-120+k*26,900+p*300,4,12,'#60A5FA')}}}
    else{ // crash into drift, everyone pops out
      const q=prog(t,bar(34),bar(35));ell(700,1470,300,160,'#FFFFFF');ell(650,1420,180,110,'#F4F8FF');
      if(t<bar(35)+.3){g.save();g.translate(lerp(390,480,easeOut(q)),0);g.rotate(q*.25);team(0,1520,.62,t,[0,4],{tired:1,run:1-q});g.restore()}
      else{const p=backOut(prog(t,bar(35)+.3,bar(35)+1.2));[[0,430],[4,620],[2,800]].forEach(([e,x],k)=>{g.save();g.translate(x,1460-p*120);g.rotate(Math.sin(t*6+k)*.15);
          santaEle(e,0,0,{s:.55,t,happy:1,trunk:1});ell(80,-170,60,30,'#fff');g.restore()});
        pony(220,1560,.55,t,0);for(let k=0;k<12;k++){const a=k/12*Math.PI*2;const r=180*prog(t,bar(35)+.3,bar(35)+1);ell(650+Math.cos(a)*r,1350+Math.sin(a)*r*.5,14,14,'rgba(255,255,255,.9)')}
        g.save();g.translate(540,850);g.scale(p,p);txt('Upsot! 😂',0,0,120,'#fff',RED);g.restore()}
    }
    UNCAM();
  }
  else if(t<bar(44)){ // chorus 3: decorate the tree
    winterSky(t,1);for(let k=0;k<50;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*900,2.5,2.5,'#fff')}g.globalAlpha=1;
    CAM();snowHills(t,0,1400);house(240,1380,.6,t);house(840,1390,.6,t,'#2563EB');
    xmasTree(540,1520,.85,t,prog(t,bar(36),bar(43)));
    [[0,300,1],[1,790,-1],[7,400,1]].forEach(([e,x,d],k)=>santaEle(e,x,1600-jb(t+k*.15)*40,{s:.5,dir:d,t,trunk:.9,happy:1}));UNCAM();
  }
  else if(t<bar(46)){ // gifts
    winterSky(t,1);CAM();snowHills(t,0,1400);xmasTree(540,1520,.85,t,1);
    const op=easeOut(prog(t,bar(44)+.5,bar(45)));present(360,1610,140,115,'#EF4444','#FDE68A',op);present(720,1610,130,105,'#3B82F6','#F9A8D4',op);present(540,1630,120,95,'#22C55E','#fff',op);UNCAM();
    if(op>.3){confetti(t,bar(44)+.6,60);g.save();g.translate(540,860);const p=backOut(prog(t,bar(44)+.6,bar(45)+.2));g.scale(p,p);txt('Surprise! 🎁',0,0,110,'#fff',RED);g.restore()}
  }
  else if(t<bar(54)){ // chorus 4: ice skating
    winterSky(t);cloud(((t*30)%1400)-300,520,1);CAM();snowHills(t,0,1300);pine(220,1380,.9);pine(860,1390,.9);
    pond(1500);
    [0,1,2,7,4].forEach((e,k)=>{const a=t*1.4+k/5*Math.PI*2;const x=540+Math.cos(a)*290,y=1500+Math.sin(a)*80;const d=-Math.sin(a)>0?1:-1;
      santaEle(e,x,y,{s:.45,dir:d,t,trunk:.6,happy:1,rot:Math.sin(t*4+k)*.08})});
    for(let k=0;k<6;k++){g.strokeStyle='rgba(255,255,255,.8)';g.lineWidth=4;const a=t*1.4+k;g.beginPath();g.ellipse(540,1500,290,80,0,a,a+.6);g.stroke()}
    UNCAM();
  }
  else{ // la la la party + end card
    winterSky(t,1);for(let k=0;k<50;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*900,2.5,2.5,'#fff')}g.globalAlpha=1;
    CAM();snowHills(t,0,1400);xmasTree(540,1480,.8,t,1);
    const xs=[260,380,700,820,540];[0,1,2,7,4].forEach((e,k)=>{if(k==4)return;const p=jb(t+k*.12);santaEle(e,xs[k],1600-p*90,{s:.45,dir:k<2?1:-1,t,trunk:.4+p*.6,happy:1})});
    UNCAM();notes(300,1100,t,bar(54),5);notes(760,1100,t,bar(54)+.5,5);confetti(t,bar(54),50);
    for(let k=0;k<10;k++){const bx=100+k*100;bell(bx,640+Math.sin(t*3+k)*20,.5,swingJ(t+k*.1)*.4)}
  }
  snowfall(t,t>=bar(44)&&t<bar(46)?40:90,1);
  // scene cuts flash
  [bar(0),bar(8),bar(16),bar(24),bar(28),bar(36),bar(44),bar(46),bar(54)].forEach(c=>{const d=Math.abs(t-c);if(d<.2){g.fillStyle=`rgba(255,255,255,${(1-d/.2)*.8})`;g.fillRect(0,0,W,H)}});
  const ec=JEND-7.5;
  if(t<ec){jtitle(t);jcaption(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  else{const q=easeOut(prog(t,ec,ec+1.2));g.save();g.globalAlpha=q*.78;g.fillStyle='#4A0D16';g.fillRect(0,0,W,H);g.restore();
    g.save();g.globalAlpha=q;popcornLogo(W/2,600,.9*backOut(prog(t,ec,ec+1.2)),Math.max(0,Math.sin(Math.PI*prog(t,ec+1.2,ec+1.7)))*.25);
    txt('A Popcorn Productions video',W/2,980,46,'#FFE14D',null,'center',600);
    txt('Merry Christmas! 🎄',W/2,1085,72,'#fff',RED);
    const sp=backOut(prog(t,ec+1.5,ec+2.5));g.save();g.translate(W/2,1240);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();
    txt('Music: "Jingle Bells" by Sascha Ende',W/2,1390,34,'#F4F8FF',null,'center',600);txt('ende.app · CC BY 4.0',W/2,1440,30,'#F4F8FF',null,'center',600);g.restore()}
  if(tv<.6){g.fillStyle=`rgba(0,0,0,${1-tv/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,JEND-1.6,JEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawJB;
