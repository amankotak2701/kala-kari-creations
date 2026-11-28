// ================= "Row, Row, Row Your Boat" — Popcorn Productions =================
const RRB=1.7385, RRL=2*RRB, RRV=[14.4,14.4+4*RRL,62.2,62.2+4*RRL,106.0];
const RRCARD=118.8, RREND=124.4;
const RRLY=['Row, row, row your boat,','Gently down the stream.','Merrily, merrily, merrily, merrily,','Life is but a dream!'];
const RRCAPS=[];RRV.forEach((v,vi)=>RRLY.forEach((s,l)=>RRCAPS.push([v+l*RRL-.25,Math.min(v+(l+1)*RRL-.25+(l===3?.8:0),vi===4&&l===3?RRCARD:1e9),s])));
const rrVerse=t=>RRV.findIndex(v=>t>=v-.25&&t<v+4*RRL-.25);
function rrDucks(t,x0){for(let k=0;k<3;k++){const x=((x0+k*90-t*40)%1400+1400)%1400-150;duck(x,1530+Math.sin(t*3+k)*6,.9-(k?.25:0),t,k)}}
function lilyFrog(x,y,t,jump){ell(x,y,90,26,'#22C55E');g.fillStyle='#38BDF8';g.beginPath();g.moveTo(x,y);g.lineTo(x+90,y-8);g.lineTo(x+90,y+8);g.fill();
  const h=jump?Math.abs(Math.sin(t*4))*90:0;g.save();g.translate(x,y-20-h);ell(0,0,46,34,'#4ADE80');ell(-24,-30,16,16,'#4ADE80');ell(24,-30,16,16,'#4ADE80');ell(-24,-32,8,8,'#fff');ell(24,-32,8,8,'#fff');ell(-24,-32,4,5,'#1F2937');ell(24,-32,4,5,'#1F2937');
  g.strokeStyle='#14532D';g.lineWidth=4;g.beginPath();g.arc(0,-6,18,.2,Math.PI-.2);g.stroke();g.restore()}
function jumpFish(x,y,t,t0,col='#F97316'){const p=((t-t0)%2.4)/2.4;if(p>.6)return;const q=p/.6;g.save();g.translate(x+q*200,y-Math.sin(q*Math.PI)*260);g.rotate(-1+q*2);ell(0,0,46,24,col);g.fillStyle=col;g.beginPath();g.moveTo(-40,0);g.lineTo(-74,-24);g.lineTo(-74,24);g.fill();ell(22,-6,6,6,'#fff');ell(23,-6,3,3,'#1F2937');g.restore()}
function sparkles(t,n=10,y0=900,y1=1400){for(let k=0;k<n;k++){const a=Math.abs(Math.sin(t*2+k*1.7));starShape(80+rnd(k)*920,y0+rnd(k+7)*(y1-y0),10+a*14,t+k,'rgba(253,224,71,'+(.3+a*.7)+')')}}
function rrNotes(x,y,t){for(let k=0;k<5;k++){const p=((t*.5+k/5)%1);g.save();g.globalAlpha=1-p;txt(k%2?'♫':'♪',x+p*300+Math.sin(p*8+k)*40,y-p*260,56,['#FDE047','#F9A8D4','#93C5FD'][k%3],null);g.restore()}}
function dreamSky(t){const sk=g.createLinearGradient(0,0,0,H);sk.addColorStop(0,'#312E81');sk.addColorStop(.6,'#7C3AED');sk.addColorStop(1,'#F0ABFC');g.fillStyle=sk;g.fillRect(0,0,W,H);
  for(let k=0;k<70;k++){g.globalAlpha=.4+.6*Math.abs(Math.sin(t*1.5+k));ell(rnd(k)*W,480+rnd(k+5)*1300,2.5,2.5,'#fff')}g.globalAlpha=1;moonFace(820,900,70,t,0,0);
  for(let k=0;k<6;k++){const x=((k*260-t*50)%1500+1500)%1500-250;ell(x,1700+rnd(k)*120,170,55,'rgba(255,255,255,.92)');ell(x+80,1670+rnd(k)*120,110,50,'rgba(255,255,255,.92)')}}
function rrtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#0284C7';g.beginPath();g.roundRect(-360,-66,720,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Row, Row, Row Your Boat 🚣',0,2,52,'#FFFFFF',null);g.restore()}
function rrcap(t){const i=RRCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=RRCAPS[i];
  const al=Math.min(clamp((t-a)/.12),clamp((b-t)/.12));g.save();g.globalAlpha=al;let fs=64;g.font=`700 ${fs}px Fredoka, Baloo2`;let w=g.measureText(s).width;
  if(w>920){fs=Math.floor(fs*920/w);g.font=`700 ${fs}px Fredoka, Baloo2`;w=g.measureText(s).width}
  const h=120,y0=395;g.fillStyle='rgba(3,105,161,.92)';g.beginPath();g.roundRect(W/2-w/2-45,y0-h/2,w+90,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/(RRL*.9));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}

function drawRow(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const vi=rrVerse(t),per=RRB;let L=-1;if(vi>=0)L=Math.floor((t-RRV[vi]+.25)/RRL);
  g.save();g.translate(540,1700);g.scale(1.3,1.3);g.translate(-540,-1700);
  const sunset=t>=RRV[2]-.25&&t<RRV[4]-.25, night=t>=RRV[3]+4*RRL-.25&&t<RRV[4]-.25;
  if(vi===4||t>=RRV[4]-.25){ // dream: the boat sails through the clouds
    dreamSky(t);sparkles(t,16,700,1500);const y=1640+Math.sin(t*1.4)*30;g.save();g.translate(540,y);g.rotate(Math.sin(t)*.04);g.translate(-540,-y);rowBoat(540,y,1.0,t,{per,riders:[0,1,2],col:'#A855F7',cheer:L===2});g.restore();
    for(let k=0;k<3;k++)ell(540+(k-1)*200,y+60,150,50,'rgba(255,255,255,.95)');
    if(L===0)pop(t,RRV[4]+.2,'Up in the sky! ☁️',540,1180,62,'#fff','#7C3AED');if(L===3)pop(t,RRV[4]+3*RRL+.2,'Sweet dreams! ✨',540,1180,66,'#fff','#DB2777');if(L===2)rrNotes(300,1400,t)}
  else{
    if(night)riverScene(t,{night:1});else{riverScene(t,{sunset})}
    if(vi>=0){
      if(vi%2===0){rrDucks(t,200)}else{lilyFrog(240,1540,t,L===2);jumpFish(560,1660,t,RRV[vi]);jumpFish(700,1700,t,RRV[vi]+1.2,'#FACC15')}
      rowBoat(540,1650,1.0,t,{per,riders:vi<2?[0,1]:[0,1,2],cheer:L===2,col:vi<2?'#EF4444':'#2563EB'});
      if(vi>=2)puppy(760,1580,.55,t,L===2?Math.abs(Math.sin(t*6))*30:0);
      if(L===0)pop(t,RRV[vi]+.2,['Row! Row! Row! 🚣','Pull, pull! 💪','Row! Row! Row! 🚣','Pull, pull! 💪'][vi],540,1180,62,'#fff','#0284C7');
      if(L===1)pop(t,RRV[vi]+RRL+.2,['Gently... 🌊','Hello, fishy! 🐟','Gently... 🌊','Ribbit! 🐸'][vi],540,1180,62,'#fff','#0EA5E9');
      if(L===2){rrNotes(300,1300,t);pop(t,RRV[vi]+2*RRL+.2,'Merrily! 🎶',540,1180,70,'#fff','#DB2777')}
      if(L===3)pop(t,RRV[vi]+3*RRL+.2,'Life is a dream! ✨',540,1180,60,'#fff','#7C3AED')}
    else if(t<RRV[0]-.25){const q=easeOut(prog(t,1,7));rowBoat(lerp(-300,540,q),1650,1.0,t,{per,riders:[0,1]});rrDucks(t,600);pop(t,2,'All aboard! ⛵',540,1180,66,'#fff','#0284C7');pop(t,8.5,'Let\'s row! 🚣',540,1180,66,'#fff','#EA580C')}
    else if(t<RRV[2]-.25){ // break 1: friendly river animals on the bank
      const b0=RRV[1]+4*RRL;const seg=Math.floor((t-b0)/6.6);rowBoat(540,1650,1.0,t,{per,riders:[0,1],cheer:1});
      if(seg===0){croc(860,1430,.5,t,{dir:-1,open:1});pop(t,b0+.4,'A friendly crocodile! 🐊',540,1180,56,'#fff','#16A34A')}
      else if(seg===1){lionC(820,1460,.7,t,{roar:Math.sin(t*3)>0});pop(t,b0+6.9,'Hello, Mr Lion! 🦁',540,1180,60,'#fff','#D97706')}
      else{puppy(260,1430,.6,t,Math.abs(Math.sin(t*6))*40);pop(t,b0+13.5,'A new friend! 🐶',540,1180,62,'#fff','#2563EB');pop(t,RRV[2]-2,'Hop in! 🚣',540,1300,62,'#fff','#EA580C')}}
    else{ // break 2: night falls, sleepy kids
      rowBoat(540,1650,1.0,t,{per:RRB*2,riders:[0,1,2],col:'#2563EB'});puppy(760,1580,.55,t,0);zzz(620,1280,t,1.2);sparkles(t,8,1000,1400);
      pop(t,RRV[3]+4*RRL+.3,'Look at the stars! ⭐',540,1180,60,'#fff','#7C3AED');pop(t,RRV[4]-5,'Yawn... 🥱',540,1180,66,'#fff','#4338CA')}}
  g.restore();
  if(t>=RRCARD){const q=easeOut(prog(t,RRCARD,RRCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#0C4A6E';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,RRCARD,RRCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Merrily, see you soon! 🚣',W/2,990,60,'#fff','#0284C7');
    const sp=backOut(prog(t,RRCARD+.5,RRCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<RRCARD){rrtitle(t);rrcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,RREND-1.2,RREND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawRow;
