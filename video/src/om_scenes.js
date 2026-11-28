// ================= "This Old Man" — Popcorn Productions =================
const OB=2.4, OV0=9.6, OVL=12.0, OBRK=7.2;
const ov=k=>OV0+k*OVL+OBRK*Math.floor(k/4);
const OCARD=142.2, OEND=147.8;
const ONUM=['one','two','three','four','five','six','seven','eight','nine','ten'];
const OPLACE=['on my thumb','on my shoe','on my knee','on my door','on my hive','on my sticks','up in heaven','on my gate','on my spine','once again'];
const OCAPS=[];for(let k=0;k<10;k++){const v=ov(k);
  OCAPS.push([v-.3,v+OB-.3,`This old man, he played ${ONUM[k]},`],[v+OB-.3,v+2*OB-.3,`He played knick-knack ${OPLACE[k]},`],
    [v+2*OB-.3,v+3*OB-.3,'With a knick-knack paddywhack, give a dog a bone,'],[v+3*OB-.3,v+4*OB+.6,'This old man came rolling home!'])}
const oInVerse=t=>{for(let k=0;k<10;k++){if(t>=ov(k)-.3&&t<ov(k)+OVL-.3)return k}return -1};
const obeat=t=>Math.pow(Math.max(0,Math.cos(Math.PI*2*(t-.475)/.6)),6); // pulse on every beat

function bone(x,y,s,rot=0){g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);rr(-50,-12,100,24,12,'#FFFBEB');[-50,50].forEach(dx=>{ell(dx,-14,18,18,'#FFFBEB');ell(dx,14,18,18,'#FFFBEB')});g.strokeStyle='#D6C7A1';g.lineWidth=3;g.strokeRect(-40,-8,80,16);g.restore()}
function spoon(x,y,s,rot){g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);rr(-6,0,12,90,6,'#94A3B8');ell(0,-10,20,28,'#CBD5E1');ell(-5,-14,7,12,'#F1F5F9');g.restore()}
function knickKnack(x,y,t,t0){ // two spoons tapping the spot on the beat + "knick!" "knack!"
  const ph=((t-t0)/.6)%1,hit=Math.pow(1-ph,4);spoon(x-50,y-60,1,-.5-hit*.5);spoon(x+50,y-60,1,.5+hit*.5);
  for(let k=0;k<6;k++){const a=k/6*Math.PI*2;g.save();g.globalAlpha=hit;g.strokeStyle='#FDE047';g.lineWidth=7;g.beginPath();g.moveTo(x+Math.cos(a)*40,y+Math.sin(a)*40);g.lineTo(x+Math.cos(a)*(60+hit*30),y+Math.sin(a)*(60+hit*30));g.stroke();g.restore()}
  const w=Math.floor((t-t0)/.6)%2?'knack!':'knick!';g.save();g.globalAlpha=.4+hit*.6;txt(w,x+(w==='knick!'?-120:120),y-150-hit*20,52,'#fff','#EA580C');g.restore()}
function skates(x,y,s,t,spin){[-24,24].forEach(dx=>{const fx=x+dx*s;rr(fx-34*s,y-6*s,68*s,16*s,6*s,'#EF4444');[-20,20].forEach(w=>{ell(fx+w*s,y+16*s,11*s,11*s,'#1F2937');g.save();g.translate(fx+w*s,y+16*s);g.rotate(spin);g.strokeStyle='#FDE047';g.lineWidth=3*s;g.beginPath();g.moveTo(-8*s,0);g.lineTo(8*s,0);g.stroke();g.restore()})})}
function oldMan(x,y,s,t,o={}){adult('dada',x,y,{s,t,pose:o.pose||'sway',happy:o.happy??1,dir:o.dir||1,k:o.k});if(o.skate)skates(x,y,s,t,t*12)}
function oKid(i,x,y,s,t,o={}){kid(i,x,y,{s,t,happy:1,noHat:1,noScarf:1,dir:o.dir||1,trunk:o.trunk??.5,cap:o.cap})}
function grandpaHouse(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);rr(-170,-260,340,260,10,'#FCD34D');g.fillStyle='#B91C1C';g.beginPath();g.moveTo(-210,-250);g.lineTo(0,-420);g.lineTo(210,-250);g.closePath();g.fill();
  rr(110,-400,46,90,6,'#7F1D1D');for(let k=0;k<3;k++){const p=((t*.4+k/3)%1);g.save();g.globalAlpha=(1-p)*.7;ell(134+p*40,-420-p*140,18+p*20,14+p*14,'#E5E7EB');g.restore()}
  rr(-50,-170,100,170,10,'#92400E');ell(30,-85,8,8,'#FDE047');rr(-150,-200,80,70,8,'#BAE6FD');rr(70,-200,80,70,8,'#BAE6FD');g.strokeStyle='#fff';g.lineWidth=6;g.strokeRect(-150,-200,80,70);g.strokeRect(70,-200,80,70);g.restore()}
function oBg(t,mode){ // 0 day, 1 sunset, 2 night
  if(mode===2){sky('#1E1B4B','#6D28D9');for(let k=0;k<60;k++){g.globalAlpha=.4+.6*Math.abs(Math.sin(t*1.5+k));ell(rnd(k)*W,480+rnd(k+5)*700,2.5,2.5,'#fff')}g.globalAlpha=1;moonFace(820,1010,55,t,0,0)}
  else if(mode===1){sky('#FB923C','#FDE68A');mandalaSun(820,1040,60,t,'#FDBA74')}
  else{sky('#7DD3FC','#E0F2FE');mandalaSun(820,1010,50,t)}
  cloud(((t*14)%1500)-300,1080,.7);cloud(((t*9+700)%1500)-300,1220,.55);
  hills(t,mode===2?'#4C1D95':'#A3E635',mode===2?'#3B0764':'#84CC16',mode===2?'#2E1065':'#65A30D');
  g.fillStyle=mode===2?'#166534':'#4ADE80';g.fillRect(0,1500,W,H-1500);g.fillStyle=mode===2?'#A8A29E':'#FDE68A';g.fillRect(0,1720,W,200);
  for(let k=0;k<10;k++)marigold(40+rnd(k)*1000,1560+rnd(k+3)*130,.75,['#F472B6','#FBBF24','#F87171','#A78BFA'][k%4])}
// the "knick-knack" objects
function oObject(n,t,t0){const X=700,Y=1440;
  if(n===0){oKid(0,780,1800,1.1,t,{dir:-1});g.save();g.translate(X,Y-60);ell(0,0,64,56,KIDS[0].skin);rr(-22,-130,44,110,22,KIDS[0].skin);g.restore();knickKnack(X,Y-180,t,t0)}
  else if(n===1){g.save();g.translate(X,Y+120);g.fillStyle='#DC2626';g.beginPath();g.moveTo(-160,40);g.lineTo(-160,-90);g.quadraticCurveTo(-110,-120,-40,-90);g.lineTo(60,-30);g.quadraticCurveTo(170,-10,170,40);g.closePath();g.fill();rr(-170,30,350,26,10,'#FFFFFF');for(let k=0;k<3;k++){g.strokeStyle='#fff';g.lineWidth=6;g.beginPath();g.moveTo(-60+k*30,-70+k*12);g.lineTo(-30+k*30,-80+k*12);g.stroke()}g.restore();knickKnack(X+30,Y+40,t,t0)}
  else if(n===2){oKid(1,760,1800,1.1,t,{dir:-1});ell(735,1720,40,34,'#F59E0B');knickKnack(735,1700,t,t0)}
  else if(n===3){g.save();g.translate(X,Y+340);rr(-150,-560,300,560,14,'#92400E');rr(-120,-520,240,220,10,'#B45309');rr(-120,-270,240,220,10,'#B45309');ell(110,-280,16,16,'#FDE047');g.restore();knickKnack(X,Y-50,t,t0)}
  else if(n===4){g.save();g.translate(X,Y-200);g.strokeStyle='#78350F';g.lineWidth=10;g.beginPath();g.moveTo(0,-200);g.lineTo(0,-130);g.stroke();for(let r=0;r<5;r++)ell(0,-110+r*55,110-Math.abs(r-2)*22,36,r%2?'#F59E0B':'#FBBF24');ell(0,60,26,20,'#78350F');g.restore();
    for(let k=0;k<5;k++){const a=t*3+k*1.3;const bx=X+Math.cos(a)*200,by=Y-200+Math.sin(a*1.3)*140;ell(bx,by,20,14,'#FDE047');rr(bx-6,by-14,6,28,2,'#1F2937');rr(bx+6,by-14,6,28,2,'#1F2937');ell(bx-4,by-18,12,8,'rgba(255,255,255,.8)')}
    knickKnack(X,Y-180,t,t0)}
  else if(n===5){g.save();g.translate(X,Y+150);ell(0,0,170,60,'#DC2626');rr(-170,-120,340,120,0,'#DC2626');ell(0,-120,170,60,'#FEF3C7');for(let k=0;k<6;k++){g.strokeStyle='#FDE047';g.lineWidth=8;g.beginPath();g.moveTo(-160+k*64,-80);g.lineTo(-130+k*64,-20);g.stroke()}g.restore();
    [-1,1].forEach(d=>{g.save();g.translate(X+d*90,Y-60);g.rotate(d*.7);rr(-9,-110,18,180,9,'#B45309');ell(0,-110,16,16,'#FDE68A');g.restore()});knickKnack(X,Y+30,t,t0)}
  else if(n===6){g.save();for(let k=0;k<3;k++)ell(X-120+k*130,Y-90+(k%2)*30,140,70,'rgba(255,255,255,.95)');for(let k=0;k<8;k++)starShape(X-260+rnd(k)*520,Y-420+rnd(k+3)*200,22,t+k,'#FDE047');g.restore();knickKnack(X,Y-300,t,t0)}
  else if(n===7){g.save();g.translate(X,Y+340);for(let k=0;k<6;k++){rr(-200+k*80,-300,28,300,6,'#FFFFFF');g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(-200+k*80,-300);g.lineTo(-186+k*80,-330);g.lineTo(-172+k*80,-300);g.fill()}rr(-210,-250,450,24,6,'#F1F5F9');rr(-210,-110,450,24,6,'#F1F5F9');g.restore();knickKnack(X+20,Y+120,t,t0)}
  else if(n===8){oKid(2,760,1800,1.1,t,{dir:1});knickKnack(700,1610,t,t0)}
  else{const items=[0,1,4,5,7];items.forEach((m,i)=>{const a=t*.8+i/items.length*Math.PI*2;const x=X+Math.cos(a)*230,y=Y-120+Math.sin(a)*200;g.save();g.translate(x,y);g.scale(.32,.32);g.translate(-X,-Y);oObject(m,t,1e9);g.restore()});knickKnack(X,Y-120,t,t0)}}
function bigNumber(n,t,t0){const p=backOut(prog(t,t0,t0+.6));g.save();g.translate(540,720);g.scale(p,p);g.rotate(Math.sin(t*5)*.06);
  ell(0,0,170,170,'#FDE047');g.lineWidth=12;g.strokeStyle='#EA580C';g.beginPath();g.arc(0,0,170,0,7);g.stroke();txt(String(n+1),0,-10,190,'#EA580C',null);txt(ONUM[n].toUpperCase(),0,118,52,'#fff','#9A3412');g.restore()}
function otitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#EA580C';g.beginPath();g.roundRect(-330,-66,660,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('This Old Man 👴🦴',0,2,58,'#FFFFFF',null);g.restore()}
function ocap(t){const i=OCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=OCAPS[i];
  const al=Math.min(clamp((t-a)/.12),clamp((b-t)/.12));g.save();g.globalAlpha=al;let fs=62;g.font=`700 ${fs}px Fredoka, Baloo2`;let w=g.measureText(s).width;
  if(w>920){fs=Math.floor(fs*920/w);g.font=`700 ${fs}px Fredoka, Baloo2`;w=g.measureText(s).width}
  const h=120,y0=395;g.fillStyle='rgba(154,52,18,.92)';g.beginPath();g.roundRect(W/2-w/2-45,y0-h/2,w+90,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((Math.min(b-a,OB))*.9));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}

function drawOldMan(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const k=oInVerse(t);let numK=-1,numT=0;const mode=t<ov(4)-.3?0:(t<ov(8)-.3?1:2);
  g.save();g.translate(540,1720);g.scale(1.45,1.45);g.translate(-540,-1800);
  oBg(t,mode);
  if(k>=0){const v=ov(k),L=Math.min(4,Math.floor((t-v+.3)/OB));
    if(L===0){grandpaHouse(820,1720,.6,t);oldMan(380,1820,1.0,t,{pose:'wave'});puppy(220,1840,.75,t,obeat(t)*30);numK=k;numT=v-.2}
    else if(L===1){oldMan(330,1820,1.0,t,{pose:'clap'});oObject(k,t,v+OB);pop(t,v+OB+.1,`${k+1} ✨`,420,1180,90,'#fff','#EA580C')}
    else if(L===2){grandpaHouse(820,1720,.6,t);const q=prog(t,v+2*OB+.6,v+2*OB+1.6);oldMan(330,1820,1.0,t,{pose:q>0&&q<1?'up':'clap'});
      const jump=Math.abs(Math.sin((t-v)*Math.PI/.6))*70;puppy(700,1840,1.0,t,jump);
      if(q<1){const bx=lerp(380,760,q),by=1450-Math.sin(q*Math.PI)*300;bone(bx,by,.9,q*8)}else bone(800,1740-jump,.6,.2);
      if(t>v+2*OB+1.7)heartsUpO(760,1560,t);pop(t,v+2*OB+.2,'Paddywhack! 👏',540,1180,70,'#fff','#DB2777');pop(t,v+2*OB+1.7,'Woof woof! 🐶',540,1180,70,'#fff','#16A34A')}
    else{const q=easeOut(prog(t,v+3*OB,v+3*OB+3.6));grandpaHouse(820,1720,.6,t);const mx=lerp(-120,700,q);
      oldMan(mx,1800,1.0,t,{pose:q<1?'up':'wave',skate:q<1});puppy(mx-240,1840,.7,t,obeat(t)*30);
      for(let j=0;j<4&&q<1;j++){g.save();g.globalAlpha=.7;g.strokeStyle='#fff';g.lineWidth=6;g.beginPath();g.moveTo(mx-180-j*40,1560+j*60);g.lineTo(mx-100-j*40,1560+j*60);g.stroke();g.restore()}
      pop(t,v+3*OB+.2,'Rolling home! 🛼',540,1180,68,'#fff','#2563EB');if(q>=1)pop(t,v+3*OB+3.7,'Home! 🏡',540,1290,72,'#fff','#EA580C')}}
  else if(t<ov(0)-.3){grandpaHouse(820,1720,.6,t);const q=easeOut(prog(t,.8,6));oldMan(lerp(-150,380,q),1820,1.0,t,{pose:'wave'});puppy(lerp(-350,220,q),1840,.75,t,obeat(t)*30);
    oKid(0,700,1820,.9,t,{trunk:1,dir:-1});pop(t,2,'Hello, Grandpa! 👋',540,1180,64,'#fff','#EA580C');pop(t,5.5,'Let\'s count! 1 2 3',540,1290,62,'#fff','#2563EB')}
  else if(t<OCARD){ // instrumental breaks + ending: dance party
    const b=obeat(t);oldMan(300,1820,1.0,t,{pose:Math.floor(t/.6)%2?'up':'clap'});oKid(0,560,1820,.9,t,{trunk:Math.floor(t/.6)%2});oKid(1,800,1820,.9,t,{trunk:Math.floor(t/.6+1)%2,dir:-1});puppy(200,1870,.6,t,b*40);
    for(let j=0;j<6;j++){const p=((t*.5+j/6)%1);g.save();g.globalAlpha=1-p;txt(j%2?'♫':'♪',200+j*130,1300-p*300,60,['#FDE047','#F472B6','#60A5FA'][j%3],null);g.restore()}
    const msg=t<ov(4)?'Dance break! 💃':(t<ov(8)?'Clap along! 👏':'Yay! We counted to 10! 🎉');pop(t,t<ov(4)?ov(3)+OVL-.2:(t<ov(8)?ov(7)+OVL-.2:ov(9)+OVL-.2),msg,540,1180,60,'#fff','#7C3AED');if(t>ov(9)+OVL-.3)confetti(t,ov(9)+OVL-.3,70)}
  g.restore();
  if(numK>=0){bigNumber(numK,t,numT);for(let j=0;j<=numK;j++){const a=Math.PI/2+(j-numK/2)*.28;starShape(540+Math.cos(a)*250,720+Math.sin(a)*250,22,t,'#FDE047')}}
  if(t>=OCARD){const q=easeOut(prog(t,OCARD,OCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#7C2D12';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,OCARD,OCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Knick-knack, see you soon! 👴',W/2,990,60,'#fff','#EA580C');
    const sp=backOut(prog(t,OCARD+.5,OCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<OCARD){otitle(t);ocap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,OEND-1.2,OEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
function heartsUpO(x,y,t){for(let k=0;k<5;k++){const p=((t*.7+k/5)%1);g.save();g.globalAlpha=1-p;txt('♥',x+Math.sin(k*2.1)*120,y-p*260,48,'#F472B6',null);g.restore()}}
window.draw=drawOldMan;
