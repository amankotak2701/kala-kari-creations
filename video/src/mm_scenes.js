// ================= "The Muffin Man" — Popcorn Productions =================
const ML=2.667, MV=[10.0,42.0,74.0];
const ml=(v,l)=>MV[v]+l*ML;
const MCARD2=103.2, MEND2=108.1;
const mpu2=t=>Math.pow(Math.sin(Math.PI*((((t-MV[0])/(ML/2))%1+1)%1)),2);
FAM.baker={skin:'#F1C9A5',hair:'#4B2E1A',style:'short',top:'#FFFFFF',bottom:'#1E3A8A',mustache:'#4B2E1A'};
const MQ=['Do you know the muffin man,','The muffin man, the muffin man?','Do you know the muffin man,','Who lives on Drury Lane?'];
const MA=['Yes, we know the muffin man,','The muffin man, the muffin man.','Yes, we know the muffin man,','Who lives on Drury Lane!'];

function muffin(x,y,s,t,o={}){g.save();g.translate(x,y-(o.hop?Math.abs(Math.sin(t*Math.PI/(ML/2)+(o.k||0)))*40:0));g.scale(s,s);if(o.rot)g.rotate(o.rot);
  const cup=o.cup||'#F472B6',top=o.top||'#92400E';
  g.fillStyle=cup;g.beginPath();g.moveTo(-60,-70);g.lineTo(60,-70);g.lineTo(46,0);g.lineTo(-46,0);g.closePath();g.fill();
  g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=4;for(let k=0;k<7;k++){g.beginPath();g.moveTo(-54+k*18,-70);g.lineTo(-42+k*14,0);g.stroke()}
  g.fillStyle=top;g.beginPath();g.moveTo(-72,-66);g.quadraticCurveTo(-80,-150,0,-160);g.quadraticCurveTo(80,-150,72,-66);g.quadraticCurveTo(0,-50,-72,-66);g.fill();
  if(o.dots)for(let k=0;k<7;k++)ell(-44+rnd(k+o.dots)*88,-130+rnd(k+o.dots+3)*60,8,8,o.dots===1?'#1E3A8A':'#3F1D0E');
  if(o.sprinkles)for(let k=0;k<10;k++){g.save();g.translate(-50+rnd(k+9)*100,-140+rnd(k+4)*70);g.rotate(rnd(k)*3);rr(-7,-2,14,4,2,['#EF4444','#FDE047','#22C55E','#3B82F6','#FFFFFF'][k%5]);g.restore()}
  if(o.cherry){ell(0,-166,14,14,'#DC2626');g.strokeStyle='#15803D';g.lineWidth=3;g.beginPath();g.moveTo(0,-178);g.quadraticCurveTo(6,-196,16,-200);g.stroke()}
  if(o.face!==false){ell(-20,-38,8,10,'#2A1A1A');ell(20,-38,8,10,'#2A1A1A');ell(-17,-42,3,3,'#fff');ell(23,-42,3,3,'#fff');ell(-34,-24,9,6,'rgba(255,255,255,.45)');ell(34,-24,9,6,'rgba(255,255,255,.45)');
    g.strokeStyle='#7F1D1D';g.lineWidth=4;g.beginPath();g.arc(0,-26,10,.2,Math.PI-.2);g.stroke()}
  if(o.arms){[[-1],[1]].forEach(([d])=>{g.save();g.translate(d*52,-40);g.rotate(d*(-1.2+Math.sin(t*8+(o.k||0))*.4));g.strokeStyle='#7F1D1D';g.lineWidth=6;g.beginPath();g.moveTo(0,0);g.lineTo(0,-40);g.stroke();ell(0,-44,8,8,'#FFFFFF');g.restore()})}
  g.restore()}
const MUFS=[{cup:'#F472B6',top:'#92400E',dots:2},{cup:'#60A5FA',top:'#C4B5FD',dots:1},{cup:'#FBBF24',top:'#F9A8D4',sprinkles:1,cherry:1},{cup:'#34D399',top:'#78350F',sprinkles:1}];
function muffinMan(x,y,s,t,o={}){const tray=o.tray!==false;
  adult('baker',x,y,{s,t,dir:o.dir||1,pose:o.pose||(tray?'hold':'wave'),happy:1,carry:tray?()=>{rr(20,-330,300,18,8,'#9CA3AF');for(let k=0;k<3;k++){g.save();g.translate(70+k*95,-334);g.scale(.62,.62);muffin(0,0,1,t,Object.assign({face:false},MUFS[k]));g.restore()}}:null});
  g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);
  rr(-56,-300,112,150,14,'#FDE68A');rr(-56,-300,112,16,6,'#FBBF24');ell(0,-220,10,10,'#F472B6');  // apron
  g.save();g.translate(0,-470);rr(-60,-10,120,40,10,'#FFFFFF');[[-44,-50,34],[0,-80,40],[44,-50,34],[-22,-74,30],[22,-74,30]].forEach(([a,b,r])=>ell(a,b,r,r,'#FFFFFF'));g.restore();
  g.restore()}
function bakery(t,o={}){
  rr(140,620,800,830,10,'#FDBA74');for(let r=0;r<16;r++)for(let c=0;c<9;c++)rr(140+c*92-(r%2)*46+2,620+r*52+3,86,46,4,r%2?'#FB923C':'#FDBA74');
  g.fillStyle='#7C2D12';g.beginPath();g.moveTo(110,640);g.lineTo(540,470);g.lineTo(970,640);g.fill();
  rr(220,700,640,110,20,'#DB2777');txt('MUFFIN SHOP 🧁',540,755,58,'#FFFFFF',null);
  for(let k=0;k<10;k++){g.fillStyle=k%2?'#FFFFFF':'#EC4899';g.beginPath();g.moveTo(160+k*76,850);g.lineTo(236+k*76,850);g.lineTo(236+k*76,920);g.quadraticCurveTo(198+k*76,950,160+k*76,920);g.closePath();g.fill()}
  rr(180,960,400,330,16,'#FEF3C7');g.strokeStyle='#7C2D12';g.lineWidth=12;g.strokeRect(180,960,400,330);
  for(let k=0;k<4;k++){g.save();g.translate(240+k*95,1140);g.scale(.5,.5);muffin(0,0,1,t,Object.assign({},MUFS[k%4]));g.restore();g.save();g.translate(240+k*95,1270);g.scale(.45,.45);muffin(0,0,1,t,Object.assign({face:false},MUFS[(k+1)%4]));g.restore()}
  rr(650,1030,220,420,14,'#7C2D12');const dop=o.door||0;rr(660+dop*150,1040,200-dop*150,400,10,'#B45309');ell(840-dop*150,1240,10,10,'#FDE047');
  g.save();g.translate(760,960);bell(0,0,.4,Math.sin(t*3)*.2);g.restore()}
function drury(t,o={}){sky('#7DD3FC','#E0F2FE');mandalaSun(930,520,60,t);cloud(((t*15)%1400)-300,460,.9);
  house(70,1450,1.0,t,'#2563EB');house(1040,1450,1.0,t,'#16A34A');
  bakery(t,o);
  rr(0,1450,W,210,0,'#9CA3AF');for(let k=0;k<12;k++)rr(k*95,1450,90,10,2,'#6B7280');rr(0,1650,W,H-1650,0,'#D1D5DB');for(let k=0;k<9;k++)rr(k*130,1680+(k%2)*40,110,60,6,'rgba(0,0,0,.06)');
  // Drury Lane sign
  rr(966,1100,14,350,4,'#374151');g.save();g.translate(973,1110);g.rotate(o.signWiggle?Math.sin(t*10)*.08:0);rr(-120,-36,240,70,10,'#15803D');g.lineWidth=4;g.strokeStyle='#FFFFFF';g.strokeRect(-112,-28,224,54);txt('Drury Lane',0,0,36,'#FFFFFF',null);g.restore()}
function mmtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#DB2777';g.beginPath();g.roundRect(-330,-66,660,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('The Muffin Man 🧁',0,2,60,'#FFFFFF',null);g.restore()}
const MCAPS3=[];MV.forEach(v0=>{for(let k=0;k<4;k++){MCAPS3.push([v0+k*ML-.25,v0+(k+1)*ML-.25,MQ[k]]);MCAPS3.push([v0+(k+4)*ML-.25,v0+(k+5)*ML-.25+(k===3?.5:0),MA[k]])}});MCAPS3.sort((a,b)=>a[0]-b[0]);
function mmcap(t){const i=MCAPS3.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=MCAPS3[i];
  const al=Math.min(clamp((t-a)/.15),clamp((b-t)/.15));g.save();g.globalAlpha=al;g.font='700 64px Fredoka, Baloo2';
  const w=g.measureText(s).width;const h=120,y0=395;g.fillStyle='rgba(131,24,67,.88)';g.beginPath();g.roundRect(W/2-w/2-50,y0-h/2,w+100,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.85));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}
const MKIDS=[[0,120],[1,280],[3,440]];
function mkids(t,o={}){MKIDS.forEach(([k,x],i)=>kid(k,x+(o.dx||0),1800-(o.jump?mpu2(t+i*.1)*40:0),{s:.85,t,happy:o.happy??1,noHat:1,noScarf:1,cap:CAPS2[k],trunk:o.cheer?1:.5,dir:1}))}

function drawMuffin(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const vi=MV.findIndex(v0=>t>=v0-.25&&t<v0+8*ML-.25);const L=vi>=0?Math.floor((t-MV[vi]+.25)/ML):-1;
  if(t<MV[0]-.25){ // intro: walking down Drury Lane
    drury(t,{});const q=easeOut(prog(t,.5,8));mkids(t,{dx:lerp(-500,0,q)});
    if(t>2)pop(t,2,'Mmm... what smells so yummy? 👃',540,1000,54,'#fff','#DB2777');for(let k=0;k<3;k++){const p=((t*.5+k/3)%1);g.save();g.globalAlpha=(1-p)*.7;g.strokeStyle='#fff';g.lineWidth=6;g.beginPath();g.moveTo(420+k*40,960-p*160);g.quadraticCurveTo(440+k*40,920-p*160,420+k*40,880-p*160);g.stroke();g.restore()}}
  else if(vi>=0&&L<4){ // the question: kids ask, sign wiggles on "Drury Lane"
    drury(t,{signWiggle:L===3});
    if(vi===1){muffinMan(830,1790,.9,t,{pose:'sway'})}
    mkids(t,{cheer:L%2===0});
    for(let k=0;k<3;k++){const p=((t*.7+k/3)%1);g.save();g.globalAlpha=1-p;txt('?',140+k*160,1400-p*220,70,'#FFFFFF','#DB2777');g.restore()}
    if(L===3)pop(t,ml(vi,3),'📍 Drury Lane!',800,980,60,'#fff','#15803D')}
  else if(vi>=0){ // the answer: door opens, the Muffin Man appears with muffins
    const q=prog(t,ml(vi,4),ml(vi,4)+1.2);drury(t,{door:easeOut(q*1.4)});
    const mx=lerp(760,700,easeOut(q));muffinMan(mx,1790,1.0,t,{});mkids(t,{jump:1,cheer:1});
    pop(t,ml(vi,4)+.2,'Yes, we know! 🙌',540,1000,72,'#fff','#16A34A');
    if(L>=6)for(let k=0;k<3;k++){const p=prog(t,ml(vi,6)+k*.4,ml(vi,6)+k*.4+1);if(p>0&&p<1){g.save();g.translate(lerp(820,140+k*160,p),lerp(1440,1480,p)-Math.sin(Math.PI*p)*200);g.scale(.5,.5);muffin(0,0,1,t,MUFS[k]);g.restore()}}}
  else if(t<MV[1]-.25){ // interlude 1: baking in the oven
    const w=g.createLinearGradient(0,0,0,H);w.addColorStop(0,'#FEF3C7');w.addColorStop(1,'#FDE68A');g.fillStyle=w;g.fillRect(0,0,W,H);
    for(let k=0;k<9;k++)rr(k*125,0,60,H,0,'rgba(251,191,36,.15)');
    rr(160,900,560,620,30,'#9CA3AF');rr(200,980,480,380,24,'#1F2937');const heat=.5+.5*Math.sin(t*6);g.fillStyle=`rgba(249,115,22,${.3+.3*heat})`;g.fillRect(210,990,460,360);
    const q=prog(t,ml(0,8),MV[1]-.5);for(let k=0;k<3;k++){g.save();g.translate(290+k*150,1320);g.scale(.8,.8*(.4+.6*clamp(q*1.5)));muffin(0,0,1,t,Object.assign({face:q>.6},MUFS[k]));g.restore()}
    for(let k=0;k<5;k++)ell(250+k*100,1560,30,30,'#4B5563');muffinMan(880,1800,.95,t,{tray:false,pose:'wave'});
    pop(t,ml(0,8)+.5,'Baking time! 🔥',540,760,72,'#fff','#EA580C');if(q>.6)pop(t,ml(0,8)+(MV[1]-ml(0,8))*.62,'Ding! Ready! 🧁',540,760,66,'#fff','#DB2777')}
  else if(t<MV[2]-.25){ // interlude 2: muffin characters dance
    sky('#FBCFE8','#FEF3C7');for(let k=0;k<30;k++){g.save();g.translate(rnd(k)*W,((t*80+rnd(k+3)*1900)%1900));g.rotate(t*2+k);rr(-10,-3,20,6,3,['#EF4444','#FDE047','#22C55E','#3B82F6'][k%4]);g.restore()}
    g.fillStyle='#F9A8D4';g.fillRect(0,1600,W,H-1600);MUFS.forEach((m,k)=>muffin(160+k*250,1560,1.75,t,Object.assign({hop:1,arms:1,k},m)));
    pop(t,ml(1,8)+.4,'Muffin dance! 💃🧁',540,900,72,'#fff','#DB2777');notes(540,1300,t,ml(1,8),6)}
  else{ // outro: muffin party + end card
    drury(t,{door:1});muffinMan(700,1790,1.0,t,{pose:'wave',tray:false});mkids(t,{jump:1,cheer:1});MUFS.forEach((m,k)=>muffin(560+k*130,1880,.5,t,Object.assign({hop:1,k},m)));
    confetti(t,ml(2,8),40);pop(t,ml(2,8)+.3,'Yum yum! 😋',540,1000,80,'#fff','#DB2777');
    if(t>=MCARD2){const q=easeOut(prog(t,MCARD2,MCARD2+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#831843';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
      popcornLogo(W/2,520,.85*backOut(prog(t,MCARD2,MCARD2+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Muffins for everyone! 🧁',W/2,990,66,'#fff','#DB2777');
      const sp=backOut(prog(t,MCARD2+.5,MCARD2+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}}
  const cuts=[];MV.forEach(v0=>cuts.push(v0-.25,v0+4*ML-.25,v0+8*ML-.25));cuts.forEach(c=>{const d=Math.abs(t-c);if(d<.15){g.fillStyle=`rgba(255,255,255,${(1-d/.15)*.6})`;g.fillRect(0,0,W,H)}});
  if(t<MCARD2){mmtitle(t);mmcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,MEND2-1.2,MEND2);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawMuffin;
