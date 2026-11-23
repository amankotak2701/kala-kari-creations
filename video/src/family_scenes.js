// ================= "We Wish You A Merry Christmas" — happy family + Santa (Popcorn Productions) =================
const FBAR=1.405, FBEAT=FBAR/3, FS0=6.04, FSEC=16*FBAR;     // 3/4 waltz, 16-bar verses
const fsec=k=>FS0+k*FSEC;
const FEND=142.0;
const fpulse=t=>Math.pow(Math.sin(Math.PI*((((t-FS0)/FBEAT)%1+1)%1)),2);
const fdown=t=>Math.pow(Math.sin(Math.PI*((((t-FS0)/FBAR)%1+1)%1)),2);
const fsway=t=>Math.sin(2*Math.PI*(t-FS0)/(2*FBAR));

// ---------- grown-ups ----------
const FAM={
 dada:{skin:'#C9956B',hair:'#D8D8D8',style:'bald',top:'#1D4ED8',bottom:'#374151',glasses:1,mustache:'#E5E7EB'},
 dadi:{skin:'#D6A27A',hair:'#D1D5DB',style:'bun',top:'#7C3AED',bottom:'#9D174D',glasses:1,skirt:1},
 mom:{skin:'#E0AE85',hair:'#1A120C',style:'long',top:'#DC2626',bottom:'#1E3A8A',skirt:1,bindi:1},
 dad:{skin:'#C48A5E',hair:'#20140C',style:'short',top:'#15803D',bottom:'#1F2937',beard:'#20140C'},
};
function adult(who,x,y,o={}){const P=FAM[who],s=o.s||1,d=o.dir||1,t=o.t||0;g.save();g.translate(x,y);g.scale(s*d,s);if(o.rot)g.rotate(o.rot);
  // legs / skirt
  if(P.skirt){g.fillStyle=P.bottom;g.beginPath();g.moveTo(-50,-175);g.lineTo(50,-175);g.lineTo(72,-14);g.lineTo(-72,-14);g.closePath();g.fill();
    g.strokeStyle='#F5C542';g.lineWidth=6;g.beginPath();g.moveTo(-70,-30);g.lineTo(70,-30);g.stroke()}
  else{rr(-38,-160,34,160,14,P.bottom);rr(4,-160,34,160,14,P.bottom)}
  ell(-24,-4,30,14,'#3F2A1E');ell(24,-4,30,14,'#3F2A1E');
  const arm=(sx,ang,front)=>{g.save();g.translate(sx,-320);g.rotate(ang);rr(-17,0,34,120,17,shade(P.top,front?0:-.12));ell(0,124,17,17,P.skin);g.restore()};
  const pose=o.pose||'sway',wv=Math.sin(t*7+(o.k||0));
  const A={sway:[.2+fsway(t)*.1,-.2+fsway(t)*.1],wave:[.25,-2.6+wv*.35],up:[Math.PI-.4+wv*.15,-(Math.PI-.4)-wv*.15],hold:[-1.25,1.25],clap:[-.9+Math.abs(wv)*.3,.9-Math.abs(wv)*.3]}[pose];
  arm(-58,A[0],0);
  // sweater with Christmas pattern
  g.fillStyle=P.top;g.beginPath();g.moveTo(-60,-340);g.quadraticCurveTo(0,-356,60,-340);g.lineTo(68,-160);g.quadraticCurveTo(0,-148,-68,-160);g.closePath();g.fill();
  g.save();g.clip();g.strokeStyle='#FFFFFF';g.lineWidth=7;g.beginPath();for(let k=0;k<9;k++){const xx=-72+k*18;g.lineTo(xx,-255+(k%2?-12:12))}g.stroke();
  for(let k=0;k<4;k++){starShape(-45+k*30,-210,8,0,'#FFFFFF')}rr(-70,-176,140,16,0,shade(P.top,-.25));g.restore();
  // head
  const hy=-405;
  if(P.style==='long'){rr(-74,hy-50,40,170,20,P.hair);rr(34,hy-50,40,170,20,P.hair)}
  if(P.style==='bun'){ell(0,hy-70,34,30,P.hair)}
  rr(-16,hy+40,32,30,8,P.skin);
  ell(0,hy,64,62,P.skin);ell(-62,hy+6,12,16,P.skin);ell(62,hy+6,12,16,P.skin);
  g.fillStyle=P.hair;g.beginPath();
  if(P.style==='short'){g.ellipse(0,hy-28,66,40,0,Math.PI,0);g.fill();ell(-60,hy-10,10,22,P.hair)}
  else if(P.style==='long'){g.ellipse(0,hy-26,68,44,0,Math.PI,0);g.fill()}
  else if(P.style==='bun'){g.ellipse(0,hy-26,66,42,0,Math.PI,0);g.fill()}
  else{ell(-58,hy-12,14,22,P.hair);ell(58,hy-12,14,22,P.hair)}
  // face
  const happy=o.happy??(fdown(t)>.6);
  if(happy){g.strokeStyle='#2A1A1A';g.lineWidth=6;g.lineCap='round';g.beginPath();g.arc(-22,hy+2,10,Math.PI*1.1,Math.PI*1.9);g.stroke();g.beginPath();g.arc(22,hy+2,10,Math.PI*1.1,Math.PI*1.9);g.stroke()}
  else{ell(-22,hy,8,11,'#2A1A1A');ell(22,hy,8,11,'#2A1A1A');ell(-19,hy-4,3,3,'#fff');ell(25,hy-4,3,3,'#fff')}
  if(P.glasses){g.strokeStyle='#4B5563';g.lineWidth=4;g.beginPath();g.arc(-22,hy,17,0,7);g.stroke();g.beginPath();g.arc(22,hy,17,0,7);g.stroke();g.beginPath();g.moveTo(-5,hy);g.lineTo(5,hy);g.stroke()}
  if(P.bindi)ell(0,hy-30,5,5,'#DC2626');
  ell(-38,hy+22,12,7,'rgba(240,100,120,.4)');ell(38,hy+22,12,7,'rgba(240,100,120,.4)');
  if(P.beard){g.fillStyle=P.beard;g.beginPath();g.moveTo(-58,hy+5);g.quadraticCurveTo(-50,hy+72,0,hy+76);g.quadraticCurveTo(50,hy+72,58,hy+5);g.quadraticCurveTo(40,hy+40,0,hy+44);g.quadraticCurveTo(-40,hy+40,-58,hy+5);g.fill()}
  if(P.mustache){ell(-14,hy+20,16,7,P.mustache,-.2);ell(14,hy+20,16,7,P.mustache,.2)}
  g.fillStyle='#9F1239';g.beginPath();g.arc(0,hy+30,13,0,Math.PI);g.fill();
  if(o.hat){g.save();g.translate(0,hy-48);g.rotate(-.15);g.fillStyle=RED;g.beginPath();g.moveTo(-68,10);g.quadraticCurveTo(10,-120,-120,-80);g.quadraticCurveTo(-10,-55,68,10);g.fill();ell(-122,-80,18,18,'#fff');rr(-74,-4,148,30,15,'#fff');g.restore()}
  arm(58,A[1],1);
  if(o.carry)o.carry();
  g.restore()}
function puppy(x,y,s,t,jump=0){g.save();g.translate(x,y-jump);g.scale(s,s);const C='#F3D9A4',D='#C9A26B';
  g.save();g.translate(-70,-70);g.rotate(Math.sin(t*14)*.5);ell(-10,-20,12,30,C,-.6);g.restore();
  ell(0,-60,75,50,C);rr(-55,-40,22,42,10,C);rr(30,-40,22,42,10,C);
  ell(65,-110,48,44,C);ell(40,-130,18,32,D,.4);ell(95,-130,18,32,D,-.4);ell(95,-98,20,15,'#FFF3DC');ell(108,-104,8,6,'#2A1A1A');
  ell(62,-118,6,8,'#2A1A1A');ell(86,-118,6,8,'#2A1A1A');g.fillStyle='#F472B6';g.beginPath();g.ellipse(98,-86,7,10,0,0,Math.PI);g.fill();
  rr(30,-78,70,12,6,RED);bell(66,-58,.2,Math.sin(t*10)*.3);g.restore()}
function pudding(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);
  ell(0,10,120,24,'#E5E7EB');ell(0,4,104,18,'#F9FAFB');
  g.fillStyle='#6B3410';g.beginPath();g.moveTo(-90,0);g.quadraticCurveTo(-95,-120,0,-125);g.quadraticCurveTo(95,-120,90,0);g.closePath();g.fill();
  for(let k=0;k<14;k++)ell(-70+rnd(k)*140,-20-rnd(k+3)*90,6,5,'#3B1A08');
  g.fillStyle='#FFF7E6';g.beginPath();g.moveTo(-70,-90);g.quadraticCurveTo(0,-140,70,-90);for(let k=0;k<6;k++){const xx=70-k*28;g.quadraticCurveTo(xx-6,-60-(k%2)*18,xx-14,-86)}g.closePath();g.fill();
  ell(-14,-128,16,9,'#15803D',-.5);ell(14,-128,16,9,'#15803D',.5);ell(0,-126,7,7,'#DC2626');ell(9,-120,6,6,'#DC2626');
  for(let k=0;k<3;k++){const p=((t*.6+k/3)%1);g.save();g.globalAlpha=(1-p)*.6;g.strokeStyle='#fff';g.lineWidth=6;g.beginPath();g.moveTo(-30+k*30,-140-p*60);g.quadraticCurveTo(-15+k*30,-160-p*60,-30+k*30,-185-p*60);g.stroke();g.restore()}
  g.restore()}
function bowl(x,y,s,full=1){g.save();g.translate(x,y);g.scale(s,s);if(full)ell(0,-18,40,16,'#6B3410');g.fillStyle='#F9FAFB';g.beginPath();g.ellipse(0,-14,48,12,0,0,Math.PI*2);g.fill();g.beginPath();g.moveTo(-48,-14);g.quadraticCurveTo(0,40,48,-14);g.fill();g.strokeStyle='#DC2626';g.lineWidth=4;g.beginPath();g.moveTo(-44,-4);g.quadraticCurveTo(0,22,44,-4);g.stroke();g.restore()}
function firework(x,y,t,t0,col){const p=(t-t0)/1.6;if(p<0||p>1)return;
  if(p<.25){const q=p/.25;ell(x,lerp(1500,y,q),5,12,'#FFF7C2');return}
  const q=(p-.25)/.75;for(let k=0;k<22;k++){const a=k/22*Math.PI*2;const r=easeOut(q)*170;g.globalAlpha=1-q;ell(x+Math.cos(a)*r,y+Math.sin(a)*r+q*q*60,6,6,col);ell(x+Math.cos(a)*r*.6,y+Math.sin(a)*r*.6+q*q*40,4,4,'#FFF7C2')}g.globalAlpha=1}
function livingRoom(t){
  const w=g.createLinearGradient(0,0,0,1350);w.addColorStop(0,'#7A2E3A');w.addColorStop(1,'#B4533F');g.fillStyle=w;g.fillRect(0,0,W,1350);
  for(let k=0;k<12;k++)for(let j=0;j<9;j++){g.globalAlpha=.08;starShape(45+k*90,60+j*150+(k%2)*75,10,0,'#FDE68A')}g.globalAlpha=1;
  // window with snowy night
  g.save();g.beginPath();g.roundRect(380,520,320,360,20);g.clip();sky('#1E3A8A','#3B82F6');for(let k=0;k<30;k++){const yy=(t*60+rnd(k)*400)%400+520;ell(380+rnd(k+2)*320,yy,4,4,'#fff')}ell(540,900,260,60,'#F4F8FF');g.restore();
  g.strokeStyle='#F5E1C0';g.lineWidth=16;g.beginPath();g.roundRect(380,520,320,360,20);g.stroke();g.lineWidth=8;g.beginPath();g.moveTo(540,520);g.lineTo(540,880);g.moveTo(380,700);g.lineTo(700,700);g.stroke();
  // garland with lights across the top
  g.strokeStyle='#15803D';g.lineWidth=18;g.beginPath();g.moveTo(0,470);for(let x=0;x<=W;x+=180)g.quadraticCurveTo(x+90,560,x+180,470);g.stroke();
  for(let k=0;k<14;k++){const x=k*80+20,y=470+Math.sin((x%180)/180*Math.PI)*60;const on=(Math.floor(t*4)+k)%2;glow(x,y+8,26,on?'rgba(255,230,120,.6)':'rgba(255,120,120,.4)');ell(x,y+8,8,11,['#EF4444','#FBBF24','#22C55E','#3B82F6'][k%4])}
  // fireplace (left)
  rr(40,1020,280,330,14,'#9A3412');for(let j=0;j<6;j++)for(let k=0;k<4;k++)rr(40+k*70+(j%2)*35,1020+j*55,64,50,4,'rgba(0,0,0,.12)');
  rr(20,990,320,44,10,'#F5E1C0');rr(95,1130,170,220,60,'#1F1307');
  for(let k=0;k<5;k++){const fl=Math.sin(t*12+k*2)*12;g.fillStyle=['#F97316','#FBBF24','#EF4444'][k%3];g.beginPath();g.moveTo(120+k*30,1340);g.quadraticCurveTo(110+k*30,1260-fl,135+k*30,1210-fl-(k%2)*30);g.quadraticCurveTo(160+k*30,1270,150+k*30,1340);g.fill()}
  glow(180,1260,160,'rgba(255,170,60,.35)');
  ['#DC2626','#15803D','#2563EB'].forEach((c,k)=>{g.save();g.translate(80+k*95,1034);g.rotate(Math.sin(t*2+k)*.05);rr(-20,0,40,80,8,c);ell(10,82,30,18,c);rr(-24,-6,48,20,8,'#fff');g.restore()});
  // tree (right)
  xmasTree(870,1360,.75,t,1);present(780,1360,90,70,'#DC2626','#FDE68A');present(960,1365,80,60,'#2563EB','#F9A8D4');
  // floor + rug
  const fl=g.createLinearGradient(0,1340,0,H);fl.addColorStop(0,'#8B5A2B');fl.addColorStop(1,'#5C3A1A');g.fillStyle=fl;g.fillRect(0,1340,W,H-1340);
  for(let k=0;k<8;k++){g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=3;g.beginPath();g.moveTo(0,1380+k*70);g.lineTo(W,1380+k*70);g.stroke()}
  ell(540,1640,470,95,'#B91C1C');ell(540,1640,410,70,'#F5C542');ell(540,1640,350,50,'#B91C1C');
}
function familyLine(t,y=1640,o={}){const S=.78,K=.74,sw=k=>fsway(t+k*.1)*.05;
  adult('dada',115,y,{s:S*.95,t,k:0,pose:o.pose||'sway',rot:sw(0),hat:o.hats});
  adult('dadi',255,y,{s:S*.92,t,k:1,pose:o.pose||'sway',rot:sw(1),hat:o.hats});
  kid(0,385,y,{s:K,t,happy:1,trunk:o.kidUp?1:.5,rot:sw(2)});
  adult('mom',525,y,{s:S,t,k:2,pose:o.pose||'sway',rot:sw(3),hat:o.hats});
  adult('dad',680,y,{s:S*1.05,t,k:3,pose:o.pose||'sway',rot:sw(4),hat:o.hats});
  kid(1,815,y,{s:K,t,happy:1,trunk:o.kidUp?1:.5,rot:sw(5)});
  kid(2,950,y,{s:K*.95,t,happy:1,trunk:o.kidUp?1:.5,rot:sw(6)});
  if(!o.noDog)puppy(600,y+10,.6,t,fpulse(t)*30)}
function diningTable(t,food=1,empty=0){g.fillStyle='#7C2D12';g.fillRect(70,1330,940,40);
  g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(50,1250);g.lineTo(1030,1250);g.lineTo(1050,1420);g.lineTo(30,1420);g.closePath();g.fill();
  g.fillStyle='#DC2626';for(let k=0;k<12;k++){g.beginPath();g.moveTo(30+k*85,1420);g.lineTo(72+k*85,1460);g.lineTo(115+k*85,1420);g.fill()}
  rr(120,1420,30,250,8,'#7C2D12');rr(930,1420,30,250,8,'#7C2D12');
  for(let k=0;k<5;k++)bowl(150+k*195,1300,.9,!empty);
  if(food)pudding(420,1275,1.05,t);}
function fcaption(t){const i=FL.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=FL[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.15));g.save();g.globalAlpha=al;g.font='700 58px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*72+40,y0=390;g.fillStyle='rgba(21,80,40,.86)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#F5C542';g.stroke();
  const prg=clamp((t-a)/((b-a)*.92));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+36+li*72,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}
const TIDE='Good tidings we bring to you and your kin;',WISH='We wish you a Merry Christmas and a Happy New Year!';
const VERSES=[
 ['We wish you a Merry Christmas, we wish you a Merry Christmas,',WISH,TIDE,WISH],
 ['Now bring us some figgy pudding, now bring us some figgy pudding,','Now bring us some figgy pudding and bring it out here!',TIDE,WISH],
 ['For we all like figgy pudding, we all like figgy pudding,','We all like figgy pudding, so bring it right here!',TIDE,WISH],
 ['And we won\'t go until we get some, we won\'t go until we get some,','We won\'t go until we get some, so bring some out here!',TIDE,WISH],
 ['We wish you a Merry Christmas, we wish you a Merry Christmas,',WISH,TIDE,WISH]];
const FL=[];VERSES.forEach((v,k)=>v.forEach((s,j)=>FL.push([fsec(k)+j*4*FBAR-FBEAT,fsec(k)+(j+1)*4*FBAR-FBEAT,s])));
function ftitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.2,1.2));g.scale(p,p);
  g.fillStyle='#15803D';g.beginPath();g.roundRect(-420,-66,840,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#F5C542';g.stroke();
  txt('We Wish You A Merry Christmas',0,2,52,'#FFFFFF',null);g.restore()}
function hny(t,t0){const p=prog(t,t0,t0+1.6);if(p<=0||p>=1)return;g.save();g.globalAlpha=Math.min(1,p*5,(1-p)*4);g.translate(540,760);const s=backOut(Math.min(1,p*3));g.scale(s,s);txt('Happy New Year! 🎆',0,0,84,'#FFE14D','#7C2D12');g.restore()}

function drawFamily(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const lineIdx=k=>Math.floor((t-fsec(k)+FBEAT)/(4*FBAR));
  if(t<fsec(0)-.5){ // intro: house at night
    winterSky(t,1);for(let k=0;k<60;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*1000,2.5,2.5,'#fff')}g.globalAlpha=1;moonFace(830,640,80,t,0,1);
    snowHills(t,0,1380);g.save();g.translate(540,1560);g.scale(2.4,2.4);house(0,0,1,t,'#B45309');g.restore();
    g.save();g.translate(540,1360);ell(0,0,46,46,'#15803D');ell(0,0,26,26,'#B45309');ell(0,-40,14,10,'#DC2626');g.restore();
    pine(140,1620,1.1);pine(950,1640,1.0);
  }
  else if(t<fsec(1)-.5){ // verse 1: family singing in the living room, Santa arrives
    livingRoom(t);const li=lineIdx(0);
    familyLine(t,1640,{pose:li>=1?'clap':'sway'});
    if(li>=2){const q=easeOut(prog(t,fsec(0)+8*FBAR-FBEAT,fsec(0)+9*FBAR));g.save();g.globalAlpha=q;santa(lerp(1250,540,q),1500,.78,t,{wave:1,sack:1});g.restore();
      if(q>.6){const p=prog(t,fsec(0)+9*FBAR,fsec(0)+11*FBAR);if(p<1){g.save();g.globalAlpha=Math.min(1,(1-p)*3);txt('Ho ho ho! 🎅',540,760,84,'#fff',RED);g.restore()}}}
  }
  else if(t<fsec(2)-.5){ // verse 2: bring us figgy pudding -> mom carries pudding to the table
    livingRoom(t);const li=lineIdx(1);
    if(li<2){familyLine(t,1640,{pose:'clap',kidUp:1});santa(540,1520,.72,t,{wave:fdown(t)>.5});
      const q=easeOut(prog(t,fsec(1)+4*FBAR,fsec(1)+8*FBAR));if(q>0){g.save();g.translate(lerp(-200,260,q),0);adult('mom',0,1620,{s:.8,t,pose:'hold',carry:()=>pudding(150,-300,.8,t)});g.restore()}}
    else{ // at the table
      santa(625,1395,.7,t,{wave:fdown(t)>.6});
      adult('dada',150,1400,{s:.72,t,pose:'clap'});adult('dadi',300,1400,{s:.7,t,pose:'sway'});adult('mom',780,1400,{s:.74,t,pose:'clap'});adult('dad',930,1400,{s:.78,t,pose:'clap'});
      diningTable(t,1);kid(0,240,1700,{s:.6,t,happy:1,trunk:1});kid(1,840,1700,{s:.6,t,happy:1,trunk:1})}
  }
  else if(t<fsec(3)-.5){ // verse 3: we all like figgy pudding — feast
    livingRoom(t);const li=lineIdx(2);
    santa(625,1395,.7,t,{wave:fdown(t)>.6});
    adult('dada',150,1400,{s:.72,t,pose:li%2?'up':'clap',k:0});adult('dadi',300,1400,{s:.7,t,pose:'clap',k:1});adult('mom',780,1400,{s:.74,t,pose:li%2?'clap':'up',k:2});adult('dad',930,1400,{s:.78,t,pose:'up',k:3});
    diningTable(t,1);kid(0,240,1700,{s:.6,t,happy:1,trunk:1});kid(1,840,1700,{s:.6,t,happy:1,trunk:fpulse(t)>.5?1:.5});kid(2,420,1720,{s:.55,t,happy:1,trunk:1});
    puppy(680,1760,.6,t,fpulse(t)*40);
    for(let k=0;k<4;k++){const p=((t*.7+k/4)%1);g.save();g.globalAlpha=1-p;txt(['Yum!','😋','Yummy!','😋'][k],200+k*230,1000-p*180,60,'#fff',RED);g.restore()}
  }
  else if(t<fsec(4)-.5){ // verse 4: won't go until we get some -> Santa's gifts
    livingRoom(t);const li=lineIdx(3);
    if(li<2){diningTable(t,0,1);santa(625,1395,.7,t,{wave:1});
      [[0,220],[1,420],[2,660],[0,860]].forEach(([kk,x],k)=>{const j=fpulse(t+k*.1)*60;kid(kk===0&&k===3?3:kk,x,1700-j,{s:.6,t,happy:1,trunk:1});bowl(x+40,1460-j,.6,0)});
      puppy(560,1780,.6,t,fpulse(t)*50);
      if(li==1){const q=easeOut(prog(t,fsec(3)+4*FBAR,fsec(3)+6*FBAR));g.save();g.translate(lerp(1300,700,q),0);adult('dadi',0,1620,{s:.75,t,pose:'hold',carry:()=>pudding(140,-300,.8,t)});g.restore()}}
    else{familyLine(t,1640,{kidUp:1,pose:'clap'});santa(540,1500,.8,t,{sack:1,wave:1});
      const op=easeOut(prog(t,fsec(3)+8*FBAR,fsec(3)+10*FBAR));present(300,1700,140,110,'#DC2626','#FDE68A',op);present(780,1700,130,100,'#2563EB','#F9A8D4',op);present(540,1720,120,90,'#15803D','#fff',op);
      if(op>.3)confetti(t,fsec(3)+9*FBAR,50)}
  }
  else if(t<fsec(5)-.4){ // verse 5: outside, everyone + Santa, New Year fireworks
    winterSky(t,1);for(let k=0;k<60;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*1000,2.5,2.5,'#fff')}g.globalAlpha=1;
    [[1.5,250,620,'#F472B6'],[5.6,800,700,'#FDE047'],[7.0,400,760,'#60A5FA'],[12.8,700,620,'#4ADE80'],[16.9,300,650,'#F97316'],[18.3,820,760,'#C084FC'],[19.5,540,600,'#FDE047']].forEach(([dt,x,y,c])=>firework(x,y,t,fsec(4)+dt,c));
    snowHills(t,0,1300);g.save();g.translate(220,1380);g.scale(1.3,1.3);house(0,0,1,t);g.restore();xmasTree(870,1430,.7,t,1);
    familyLine(t,1680,{hats:1,kidUp:fdown(t)>.5,pose:'up'});santa(540,1560,.66,t,{wave:1});
    [4*FBAR,12*FBAR].forEach(d=>hny(t,fsec(4)+d+2*FBAR));
  }
  else if(t<FEND-8){ // instrumental: Santa flies away across the moon, family waves
    winterSky(t,1);for(let k=0;k<60;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*1000,2.5,2.5,'#fff')}g.globalAlpha=1;
    moonFace(540,760,230,t,0,1);
    const q=prog(t,fsec(5),FEND-9);const sx=lerp(-700,1300,q),sy=900-Math.sin(q*Math.PI)*260;
    for(let k=0;k<16;k++){const tq=q-k*.012;starShape(lerp(-700,1300,tq)+80,900-Math.sin(tq*Math.PI)*260+30,10-k*.5,t*3+k,'#FDE68A')}
    team(sx,sy,.42,t,[0,1],{happy:1});
    snowHills(t,0,1380);g.save();g.translate(540,1560);g.scale(2.0,2.0);house(0,0,1,t);g.restore();
    familyLine(t,1760,{pose:'wave',noDog:0});
  }
  else { // end card
    winterSky(t,1);for(let k=0;k<60;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*H,2.5,2.5,'#fff')}g.globalAlpha=1;
    const ec=FEND-8;const q=easeOut(prog(t,ec,ec+1));g.save();g.globalAlpha=q;
    popcornLogo(W/2,560,.9*backOut(prog(t,ec,ec+1.2)),Math.max(0,Math.sin(Math.PI*prog(t,ec+1.2,ec+1.7)))*.25);
    txt('A Popcorn Productions video',W/2,940,46,'#FFE14D',null,'center',600);
    txt('Merry Christmas',W/2,1060,84,'#fff',RED);txt('& Happy New Year! 🎄',W/2,1160,70,'#fff',RED);
    const sp=backOut(prog(t,ec+1.4,ec+2.4));g.save();g.translate(W/2,1320);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();
    g.restore();
    familyLine(t,1800,{pose:'wave',hats:1});santa(540,1700,.55,t,{wave:1});
  }
  if(t<fsec(5)-.4||t>=FEND-8)snowfall(t,50,.7);
  [fsec(0)-.5,fsec(1)-.5,fsec(2)-.5,fsec(3)-.5,fsec(4)-.5,fsec(5)-.4,FEND-8].forEach(c=>{const d=Math.abs(t-c);if(d<.25){g.fillStyle=`rgba(255,255,255,${(1-d/.25)*.8})`;g.fillRect(0,0,W,H)}});
  if(t<FEND-8){ftitle(t);fcaption(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,FEND-1.5,FEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawFamily;
