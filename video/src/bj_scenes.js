// ================= "Are You Sleeping, Brother John?" — Popcorn Productions =================
const JL2=4.13, JV0=16.0;
const jln=n=>JV0+n*JL2;                       // line n on the global grid
const JVERSES=[0,8,16,20];                    // first line index of each sung verse
const JOHNCARD=119.8, JOHNEND=123.8;
const jpu=t=>Math.pow(Math.sin(Math.PI*((((t-JV0)/(JL2/4))%1+1)%1)),2);
const JLYR=['Are you sleeping? Are you sleeping?','Brother John, Brother John?','Morning bells are ringing, morning bells are ringing,','Ding, ding, dong! Ding, ding, dong!'];

function johnInBed(x,y,s,t,st='sleep'){g.save();g.translate(x,y);g.scale(s,s);
  rr(-330,-40,660,130,26,'#1D4ED8');rr(-350,-200,44,320,16,'#1E3A8A');rr(306,-140,44,260,16,'#1E3A8A');ell(-220,-60,120,52,'#FFFFFF');
  const K=KIDS[0],hx=-210,hy=-112+(st==='awake'?-40:0);
  if(st!=='under'&&st!=='empty'){ell(hx,hy,70,64,K.skin);g.fillStyle=K.hair;g.beginPath();g.ellipse(hx,hy-30,72,42,0,Math.PI,0);g.fill();
    if(st==='sleep'){g.strokeStyle='#2A1A1A';g.lineWidth=5;g.beginPath();g.arc(hx-24,hy-4,10,Math.PI*.15,Math.PI*.85);g.stroke();g.beginPath();g.arc(hx+24,hy-4,10,Math.PI*.15,Math.PI*.85);g.stroke();ell(hx,hy+30,10,8+Math.abs(Math.sin(t*2))*6,'#7F1D1D')}
    else if(st==='yawn'){g.strokeStyle='#2A1A1A';g.lineWidth=5;g.beginPath();g.moveTo(hx-34,hy-4);g.lineTo(hx-14,hy-4);g.moveTo(hx+14,hy-4);g.lineTo(hx+34,hy-4);g.stroke();ell(hx,hy+30,18,24,'#7F1D1D')}
    else{ell(hx-24,hy-4,10,13,'#2A1A1A');ell(hx+24,hy-4,10,13,'#2A1A1A');ell(hx-21,hy-8,3,3,'#fff');ell(hx+27,hy-8,3,3,'#fff');g.fillStyle='#7F1D1D';g.beginPath();g.arc(hx,hy+24,18,0,Math.PI);g.fill()}
    ell(hx-42,hy+20,12,7,'rgba(240,100,120,.45)');ell(hx+42,hy+20,12,7,'rgba(240,100,120,.45)');
    // nightcap
    g.save();g.translate(hx,hy-46);g.rotate(-.25);g.fillStyle='#60A5FA';g.beginPath();g.moveTo(-70,10);g.quadraticCurveTo(-20,-110,-170,-70);g.quadraticCurveTo(-40,-60,70,10);g.fill();ell(-172,-70,20,20,'#FFFFFF');rr(-76,-4,152,28,14,'#FFFFFF');g.restore()}
  const br=Math.sin(t*1.4)*8;const top=st==='under'?-210:(st==='empty'?-20:-60);g.fillStyle='#93C5FD';g.beginPath();g.moveTo(st==='under'?-330:-130,-40);g.quadraticCurveTo(-60,top-br,320,-70);g.lineTo(320,60);g.lineTo(-330,60);g.closePath();g.fill();
  for(let k=0;k<7;k++){starShape(-200+k*70,-20-(k%2)*30-br*.5,14,0,'#FDE68A');ell(-170+k*70,20,8,8,'#DBEAFE')}
  if(st==='under'){g.save();g.translate(-230,-150);ell(0,0,30,20,'#93C5FD');g.restore()}
  g.restore()}
function bellTower(x,y,s,t,swing=0){g.save();g.translate(x,y);g.scale(s,s);rr(-130,-500,260,500,10,'#E7E5E4');for(let r=0;r<10;r++)for(let c=0;c<3;c++)rr(-130+c*90-(r%2)*45+4,-500+r*50+4,82,42,4,'rgba(0,0,0,.05)');
  g.fillStyle='#B91C1C';g.beginPath();g.moveTo(-160,-500);g.lineTo(0,-700);g.lineTo(160,-500);g.fill();rr(-6,-760,12,70,4,'#F5C542');rr(-26,-740,52,12,4,'#F5C542');
  g.fillStyle='#1F2937';g.beginPath();g.moveTo(-90,-200);g.lineTo(-90,-370);g.arc(0,-370,90,Math.PI,0);g.lineTo(90,-200);g.closePath();g.fill();
  bell(0,-330,1.35,swing);rr(-60,-120,120,120,60,'#7C2D12');g.restore()}
function rooster(x,y,s,t,crow=0){g.save();g.translate(x,y);g.scale(s,s);
  ['#16A34A','#2563EB','#DC2626'].forEach((c,k)=>{g.save();g.translate(-80,-120);g.rotate(-.6+k*.35+Math.sin(t*4)*.05);ell(-30,-40,26,70,c,-.3);g.restore()});
  rr(-16,-40,8,40,3,'#F59E0B');rr(14,-40,8,40,3,'#F59E0B');ell(0,-100,80,60,'#F97316');ell(-10,-90,46,28,'#FB923C');
  g.save();g.translate(55,-170+(crow?-15:0));g.rotate(crow?-.4:0);ell(0,0,40,40,'#F97316');[[-14,-42],[2,-48],[18,-42]].forEach(([a,b])=>ell(a,b,11,15,'#DC2626'));ell(28,30,10,18,'#DC2626');
  g.fillStyle='#FBBF24';if(crow){g.beginPath();g.moveTo(32,-8);g.lineTo(70,-22);g.lineTo(40,0);g.fill();g.beginPath();g.moveTo(32,6);g.lineTo(70,20);g.lineTo(40,4);g.fill()}else{g.beginPath();g.moveTo(34,-8);g.lineTo(66,0);g.lineTo(34,8);g.fill()}
  ell(14,-8,6,8,'#111');g.restore();g.restore()}
function pancakes(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);ell(0,10,140,26,'#FFFFFF');for(let k=0;k<4;k++){ell(0,-k*26,110,26,'#D97706');ell(0,-k*26-6,104,20,'#F59E0B')}
  g.fillStyle='#92400E';g.beginPath();g.ellipse(0,-84,70,16,0,0,7);g.fill();g.beginPath();g.moveTo(40,-80);g.quadraticCurveTo(50,-40,44,-20);g.lineTo(36,-20);g.quadraticCurveTo(40,-50,30,-80);g.fill();rr(-20,-110,40,26,6,'#FEF3C7');g.restore()}
function aroma(x0,y0,x1,y1,t,col='rgba(255,255,255,.8)'){for(let k=0;k<3;k++){g.save();g.strokeStyle=col;g.lineWidth=8;g.lineCap='round';g.beginPath();for(let i=0;i<=30;i++){const u=i/30;const x=lerp(x0,x1,u),y=lerp(y0,y1,u)+Math.sin(u*12+t*4+k*2)*24+(k-1)*40;i?g.lineTo(x,y):g.moveTo(x,y)}g.stroke();g.restore()}}
function bedroom(t,dawn=0){const w=g.createLinearGradient(0,0,0,1400);w.addColorStop(0,'#FDE7C7');w.addColorStop(1,'#F9C98A');g.fillStyle=w;g.fillRect(0,0,W,1400);
  for(let k=0;k<12;k++)for(let j=0;j<10;j++){g.globalAlpha=.08;ell(40+k*95+(j%2)*45,60+j*140,14,14,'#B45309')}g.globalAlpha=1;
  g.save();g.beginPath();g.roundRect(560,560,380,420,30);g.clip();
  const top=dawn<.5?'#1E3A8A':'#7DD3FC',bot=dawn<.5?'#F472B6':'#FEF3C7';sky(top,bot);
  if(dawn>0)sunFace(750,lerp(1050,720,clamp(dawn)),70,t,0);else{for(let k=0;k<12;k++)ell(580+rnd(k)*340,580+rnd(k+3)*360,2.5,2.5,'#fff');moonFace(820,660,40,t,0,0)}
  g.restore();g.strokeStyle='#FFFFFF';g.lineWidth=16;g.beginPath();g.roundRect(560,560,380,420,30);g.stroke();g.lineWidth=8;g.beginPath();g.moveTo(750,560);g.lineTo(750,980);g.moveTo(560,770);g.lineTo(940,770);g.stroke();
  g.fillStyle='#F87171';g.beginPath();g.moveTo(520,540);g.quadraticCurveTo(600,780,530,1010);g.lineTo(480,1010);g.lineTo(480,540);g.fill();g.beginPath();g.moveTo(980,540);g.quadraticCurveTo(900,780,970,1010);g.lineTo(1020,1010);g.lineTo(1020,540);g.fill();
  const fl=g.createLinearGradient(0,1390,0,H);fl.addColorStop(0,'#A16207');fl.addColorStop(1,'#713F12');g.fillStyle=fl;g.fillRect(0,1390,W,H-1390);
  ell(540,1800,460,80,'#60A5FA');ell(540,1800,400,58,'#BFDBFE')}
function jtitle2(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#0EA5E9';g.beginPath();g.roundRect(-420,-66,840,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Are You Sleeping, Brother John? 🛏️',0,2,42,'#FFFFFF',null);g.restore()}
const JCAPS=[];JVERSES.forEach(n0=>{for(let k=0;k<4;k++)JCAPS.push([jln(n0+k)-.3,jln(n0+k+1)-.3+(k===3?.5:0),JLYR[k]])});JCAPS.push([jln(24)-.3,jln(24)+JL2,JLYR[3]]);
function jcap2(t){const i=JCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=JCAPS[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 60px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*74+40,y0=395;g.fillStyle='rgba(12,74,110,.88)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.9));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+37+li*74,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}
function dingdong(t,t0,n=6){for(let i=0;i<n;i++){const ti=t0+i*JL2/6;const p=prog(t,ti,ti+.8);if(p<=0||p>=1)continue;g.save();g.globalAlpha=Math.min(1,p*6,(1-p)*3);const side=i%2?1:-1;
  g.translate(540+side*(250+(i%3)*30),760+(i%3)*90);g.scale(backOut(Math.min(1,p*3)),backOut(Math.min(1,p*3)));g.rotate(side*.12);txt(['DING!','DING!','DONG!'][i%3],0,0,72,'#FDE047','#B45309');g.restore()}}
const swingBell=t=>Math.sin(t*Math.PI/(JL2/4))*.5;
function sister(x,y,s,t,o={}){kid(1,x,y,Object.assign({s,t,happy:1,noHat:1,noScarf:1,dir:-1},o))}

function drawJohn(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const n=Math.floor((t-JV0)/JL2);const lk=((n%4)+4)%4;
  if(t<JV0-.2){ // intro: night falls into dawn, John snoring
    bedroom(t,prog(t,6,15));johnInBed(560,1560,1.3,t,'sleep');zzz(330,1140,t,1.8);
    if(t<5){const q=backOut(prog(t,.5,1.5));g.save();g.translate(540,860);g.scale(q,q);txt('Shhh... 🤫',0,0,80,'#fff','#0EA5E9');g.restore()}
    else pop(t,9,'Zzz... snore! 😴',540,860,66,'#fff','#6366F1')}
  else if(n<4||(n>=8&&n<12)){ // verses 1 & 2: wake-up attempts
    const v2=n>=8;
    if(lk<2){bedroom(t,1);johnInBed(560,1560,1.3,t,v2&&lk===1?'yawn':'sleep');if(!(v2&&lk===1))zzz(330,1140,t,1.8);
      sister(900,1800,1.1,t,{trunk:lk===1?1:.5});
      if(v2){g.save();g.translate(880,1180);g.rotate(Math.sin(t*40)*.12);g.scale(.55,.55);clockFace(0,0,1,t);g.restore();pop(t,jln(8)+.2,'RIIING! ⏰',540,860,78,'#fff','#DC2626')}
      else pop(t,jln(lk)+.2,lk===0?'Psst... wake up! 👋':'Brother John! 📣',540,860,64,'#fff','#0EA5E9')}
    else{ // bells ringing at sunrise
      sky('#7DD3FC','#FEF3C7');sunFace(830,720,110,t,0);cloud(120,640,.9);
      g.fillStyle='#86EFAC';g.fillRect(0,1500,W,H-1500);for(let k=0;k<5;k++)house(110+k*215,1560,.7,t,['#F97316','#2563EB','#DB2777','#16A34A','#7C3AED'][k]);
      bellTower(540,1500,1.1,t,swingBell(t));if(lk===3)dingdong(t,jln(n));
      for(let k=0;k<3;k++){const p=((t*.8+k/3)%1);g.save();g.globalAlpha=1-p;txt('♪',360+k*170,1000-p*220,70,'#7C3AED',null);g.restore()}}
  }
  else if(n<8){ // interlude 1: rooster crows, puppy jumps on the bed, John hides under the blanket
    const q=prog(t,jln(4),jln(8));
    if(q<.45){sky('#7DD3FC','#FEF3C7');sunFace(830,720,110,t,0);g.fillStyle='#86EFAC';g.fillRect(0,1500,W,H-1500);rr(0,1450,W,24,4,'#A16207');for(let k=0;k<12;k++)rr(k*95,1380,16,100,4,'#A16207');
      const crow=(t%2)<1;rooster(540,1600,1.6,t,crow);if(crow)pop(t,Math.floor(t/2)*2,'Cock-a-doodle-doo! 🐓',540,950,62,'#fff','#EA580C')}
    else{bedroom(t,1);johnInBed(560,1560,1.3,t,'under');puppy(600,1380-Math.abs(Math.sin(t*6))*80,1.0,t,0);pop(t,jln(4)+(jln(8)-jln(4))*.5,'Woof! Wake up! 🐶',540,860,64,'#fff','#B45309');
      pop(t,jln(4)+(jln(8)-jln(4))*.75,'Five more minutes... 😴',540,1000,58,'#fff','#6366F1')}
  }
  else if(n<16){ // interlude 2: pancake smell wakes John up!
    const q=prog(t,jln(12),jln(16));bedroom(t,1);
    if(q<.55){johnInBed(560,1560,1.3,t,q<.3?'sleep':'yawn');rr(840,1230,200,20,6,'#92400E');pancakes(940,1220,.7,t);aroma(920,1100,320,1240,t);pop(t,jln(12)+1,'Sniff sniff... 👃',540,860,66,'#fff','#D97706')}
    else{const p=backOut(prog(q,.55,.7));johnInBed(560,1560,1.3,t,q>.7?'empty':'awake');const jy=1520-Math.sin(Math.PI*clamp((q-.55)/.2))*300;
      if(q>.7){kid(0,300,1780,{s:1.0,t,happy:1,noHat:1,noScarf:1,cap:'#60A5FA',trunk:1});pancakes(780,1680,.9,t);sister(950,1780,.85,t,{trunk:1})}
      pop(t,jln(12)+(jln(16)-jln(12))*.56,'PANCAKES?! 🥞',540,860,84,'#fff','#D97706');if(q>.8)pop(t,jln(12)+(jln(16)-jln(12))*.82,'Good morning! ☀️',540,1000,72,'#fff','#16A34A')}
  }
  else if(t<JOHNCARD){ // verses 3-4: John awake, bell-ringing party
    sky('#7DD3FC','#FEF3C7');sunFace(860,720,100,t,0);g.fillStyle='#86EFAC';g.fillRect(0,1500,W,H-1500);
    bellTower(540,1500,.85,t,swingBell(t));
    [[0,180,'#60A5FA'],[1,370,CAPS2[1]],[3,710,CAPS2[3]],[2,900,CAPS2[2]]].forEach(([k,x,c],i)=>{const j=jpu(t+i*.1)*40;kid(k,x,1820-j,{s:.85,t,happy:1,noHat:1,noScarf:1,cap:c,trunk:1,dir:x<540?1:-1});
      g.save();g.translate(x+(x<540?75:-75),1480-j);rr(-7,-80,14,60,5,'#7C2D12');bell(0,0,1.0,swingBell(t+i*.2));g.restore()});
    puppy(540,1860,.6,t,jpu(t)*30);if(lk===3)dingdong(t,jln(n));if(n>=24)dingdong(t,jln(24));
    for(let k=0;k<4;k++){const p=((t*.7+k/4)%1);g.save();g.globalAlpha=1-p;txt('♪',200+k*230,1150-p*220,64,'#7C3AED',null);g.restore()}
    if(n>=20)confetti(t,jln(20),40)}
  else{ // end card
    sky('#7DD3FC','#FEF3C7');sunFace(860,720,100,t,0);g.fillStyle='#86EFAC';g.fillRect(0,1500,W,H-1500);bellTower(540,1500,.85,t,swingBell(t)*.3);
    const q=easeOut(prog(t,JOHNCARD,JOHNCARD+.8));g.save();g.globalAlpha=q*.72;g.fillStyle='#0C4A6E';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,JOHNCARD,JOHNCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Good morning! ☀️🔔',W/2,990,74,'#fff','#0EA5E9');
    const sp=backOut(prog(t,JOHNCARD+.5,JOHNCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  const cuts=[jln(0),jln(2),jln(4),jln(8),jln(10),jln(12),jln(16)].map(c=>c-.25);cuts.forEach(c=>{const d=Math.abs(t-c);if(d<.15){g.fillStyle=`rgba(255,255,255,${(1-d/.15)*.6})`;g.fillRect(0,0,W,H)}});
  if(t<JOHNCARD){jtitle2(t);jcap2(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,JOHNEND-1.2,JOHNEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawJohn;
