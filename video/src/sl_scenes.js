// ================= "Skip to My Lou" — Popcorn Productions =================
const SLB=2.33, SLS=4*SLB, SL0=4.54;
const sls=k=>SL0+k*SLS;
const SLCARD=165.3, SLEND=169.2;
const SLPLAN=['C','fly','C','cat','C','break','cow','C','wagon','C','texas','C','break2','lost','C','found','C','tail'];
const SLVERSE={fly:'Flies in the buttermilk, shoo, fly, shoo!',cat:'Cat\'s in the cream jar, ooh, ooh, ooh!',cow:'Cows in the pasture, moo, moo, moo!',wagon:'Little red wagon, painted blue!',texas:'Off to Texas, two by two!',lost:'Lost my partner, what\'ll I do?',found:'Found my partner, love is true!'};
const SLCAPS=[];SLPLAN.forEach((k,i)=>{const s0=sls(i);if(k.startsWith('break'))return;
  const ls=k==='C'?['Lou, Lou, skip to my Lou,','Lou, Lou, skip to my Lou,','Lou, Lou, skip to my Lou,','Skip to my Lou, my darling!']:(k==='tail'?[null,null,null,null]:[SLVERSE[k],SLVERSE[k],SLVERSE[k],'Skip to my Lou, my darling!']);
  if(k==='tail'){SLCAPS.push([s0-.25,SLCARD,'Skip to my Lou, my darling!']);return}
  ls.forEach((s,l)=>SLCAPS.push([s0+l*SLB-.25,s0+(l+1)*SLB-.25+(l===3?.5:0),s]))});
const slhop=t=>Math.abs(Math.sin(Math.PI*(t-.465)/.5825));
function slKids(t,n,y,o={}){ // a line of skipping kids holding hands
  const sp=o.sp||170,x0=(o.x0??540)-(n-1)*sp/2,move=o.move||0;
  for(let i=0;i<n;i++){const x=x0+i*sp+Math.sin(t*2)*move,h=slhop(t+i*.29)*(o.h??50);kid(o.ids?o.ids[i]:i,x,y-h,{s:o.s||.85,t,happy:1,noHat:1,noScarf:1,trunk:o.cheer?1:.5,dir:o.dir||1})}}
function slNotes(t,y=1250){for(let j=0;j<6;j++){const p=((t*.5+j/6)%1);g.save();g.globalAlpha=1-p;txt(j%2?'♫':'♪',200+j*130,y-p*280,58,['#FDE047','#F472B6','#60A5FA'][j%3],null);g.restore()}}
function cactus(x,y,s){g.save();g.translate(x,y);g.scale(s,s);rr(-26,-220,52,220,26,'#16A34A');rr(-90,-160,30,90,15,'#16A34A');rr(-90,-90,80,28,14,'#16A34A');rr(60,-190,30,100,15,'#16A34A');rr(14,-110,76,28,14,'#16A34A');g.restore()}
function signPost(x,y,txtS){rr(x-10,y-220,20,220,6,'#92400E');g.save();g.translate(x,y-190);g.fillStyle='#B45309';g.beginPath();g.moveTo(-90,-40);g.lineTo(90,-40);g.lineTo(130,0);g.lineTo(90,40);g.lineTo(-90,40);g.closePath();g.fill();txt(txtS,10,2,38,'#fff',null);g.restore()}
function haystack(x,y,s){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle='#FACC15';g.beginPath();g.moveTo(-170,0);g.quadraticCurveTo(-160,-260,0,-280);g.quadraticCurveTo(160,-260,170,0);g.closePath();g.fill();
  g.strokeStyle='#CA8A04';g.lineWidth=5;for(let k=0;k<12;k++){g.beginPath();g.moveTo(-140+k*25,-20);g.lineTo(-130+k*25,-60-((k*37)%80));g.stroke()}g.restore()}
function slVerse(k,t,s0){const L=Math.floor((t-s0+.25)/SLB),lt=t-s0;farmBg(t,{noSun:1});
  if(k==='fly'){churn(560,1800,1.2,t);for(let j=0;j<4;j++){const a=t*3+j*1.6;fly(560+Math.cos(a)*(160+j*30),1420+Math.sin(a*1.3)*90,1.2,t)}
    kid(1,270,1820,{s:1.0,t,happy:1,noHat:1,noScarf:1,trunk:1,dir:1});pop(t,s0+.2,'Shoo, fly, shoo! 🪰',540,1180,62,'#fff','#16A34A');if(L===3)slKids(t,2,1840,{x0:820,s:.7,sp:140})}
  else if(k==='cat'){g.save();g.translate(640,1800);rr(-80,-180,160,180,30,'#E0F2FE');ell(0,-180,80,22,'#FEFCE8');g.restore();
    kitty(440,1830,1.3,t,{dir:1,hop:L%2?slhop(t)*20:0});ell(560,1700,14,10,'#FEFCE8');for(let j=0;j<3;j++){const p=((t*.8+j/3)%1);g.save();g.globalAlpha=1-p;txt('Ooh!',360+j*160,1500-p*200,50,'#fff','#EA580C');g.restore()}
    pop(t,s0+.2,'Cream for kitty! 🐱🥛',540,1180,58,'#fff','#EA580C')}
  else if(k==='cow'){for(let j=0;j<3;j++)cow(300+j*240,1840-(j%2)*90,.5,t,{dir:j%2?-1:1,hop:L===3});
    const j=Math.floor(lt/.75)%3;bubble(300+j*240,1480-(j%2)*90,.7,'Moo!','#16A34A');pop(t,s0+.2,'Moo, moo, moo! 🐄',540,1180,62,'#fff','#16A34A')}
  else if(k==='wagon'){const p=clamp((lt-.3)/(3*SLB));wagon(540,1840,1.4,t,{col:'#EF4444'});
    g.save();g.beginPath();g.rect(540-230,1600,460*p,200);g.clip();wagon(540,1840,1.4,t,{col:'#3B82F6'});g.restore();
    const bx=540-230+460*p;g.save();g.translate(bx,1620);g.rotate(-.4+Math.sin(t*10)*.2);rr(-8,-120,16,120,6,'#92400E');rr(-18,-10,36,40,6,'#3B82F6');g.restore();
    kid(2,bx+60,1880,{s:.8,t,happy:1,noHat:1,noScarf:1,dir:-1});pop(t,s0+.2,'Paint it blue! 🖌️',540,1180,62,'#fff','#2563EB');if(p>=1)pop(t,s0+3*SLB,'All blue! 💙',540,1180,70,'#fff','#2563EB')}
  else if(k==='texas'){cactus(250,1600,.6);signPost(820,1640,'Texas');const q=prog(t,s0,s0+4*SLB);
    for(let p=0;p<3;p++){const x=lerp(80,760,(q*1.2+p*.33)%1.0);[0,1].forEach(j=>kid((p*2+j)%6,x+j*95,1800+p*0-(slhop(t+p*.3+j*.15))*30,{s:.62,t,happy:1,noHat:1,noScarf:1,trunk:.5,cap:j?'#B45309':'#92400E',dir:1}))}
    pop(t,s0+.2,'Two by two! 👫',540,1180,64,'#fff','#B45309');pop(t,s0+2*SLB,'Yee-haw! 🤠',540,1180,70,'#fff','#EA580C')}
  else if(k==='lost'){haystack(740,1830,.9);const peek=Math.sin(lt*2)>.5;if(peek)kid(1,830,1720,{s:.7,t,happy:1,noHat:1,noScarf:1,dir:-1});haystack(740,1830,.9);
    kid(0,380+Math.sin(lt*1.5)*90,1840,{s:1.0,t,happy:0,noHat:1,noScarf:1,dir:Math.cos(lt*1.5)>0?1:-1});
    for(let j=0;j<3;j++){const p=((t*.7+j/3)%1);g.save();g.globalAlpha=1-p;txt('?',260+j*150,1380-p*200,80,'#fff','#2563EB');g.restore()}pop(t,s0+.2,'Where did you go? 🥺',540,1180,60,'#fff','#2563EB')}
  else if(k==='found'){haystack(880,1830,.6);const q=easeOut(prog(t,s0,s0+1.5));kid(0,lerp(240,450,q),1840,{s:1.0,t,happy:1,noHat:1,noScarf:1,trunk:1,dir:1});kid(1,lerp(840,630,q),1840,{s:1.0,t,happy:1,noHat:1,noScarf:1,trunk:1,dir:-1});
    for(let j=0;j<6;j++){const p=((t*.6+j/6)%1);g.save();g.globalAlpha=1-p;txt('♥',540+Math.sin(j*2.2)*170,1450-p*280,54,'#F472B6',null);g.restore()}pop(t,s0+.4,'Found you! 💕',540,1180,68,'#fff','#DB2777')}}
function slChorus(t,s0,i){farmBg(t,{noSun:1});const L=Math.floor((t-s0+.25)/SLB);const n=Math.min(4,2+Math.floor(i/3));
  const x0=i%4===0?540:(i%4===2?lerp(-200,1280,clamp((t-s0)/SLS)):540);
  slKids(t,n,1840,{x0,s:.85,sp:175,cheer:L===3});if(i>=7)puppy(x0-n*88-10,1880,.6,t,slhop(t)*40);
  if(L===0)pop(t,s0+.2,'Skip, skip, skip! 🎵',540,1180,64,'#fff','#DB2777');if(L===3){slNotes(t);pop(t,s0+3*SLB+.1,'My darling! 💖',540,1180,66,'#fff','#DB2777')}}

function drawSkip(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const i=Math.floor((t-SL0+.25)/SLS),k=i>=0&&i<SLPLAN.length?SLPLAN[i]:null,s0=sls(i);
  g.save();g.translate(540,1770);g.scale(1.4,1.4);g.translate(-540,-1840);
  if(t<SL0-.25){farmBg(t,{noSun:1});const q=easeOut(prog(t,.5,4));slKids(t,2,1840,{x0:lerp(-200,540,q)});pop(t,1.2,'Let\'s skip! 🎶',540,1180,70,'#fff','#DB2777')}
  else if(k==='C'||k==='tail')slChorus(t,s0,i);
  else if(k==='break'||k==='break2'){farmBg(t,{door:1,noSun:1});const b=slhop(t);slKids(t,4,1840,{s:.8,sp:165,cheer:Math.floor(t/.5825)%2,h:60});cow(230,1690,.4,t,{hop:1});kitty(850,1700,.7,t,{dir:-1,hop:b*30});slNotes(t);
    pop(t,s0+.3,k==='break'?'Barn dance! 💃':'Hide and seek! 🙈',540,1180,66,'#fff','#7C3AED');if(k==='break')confetti(t,s0,40)}
  else if(k)slVerse(k,t,s0);
  else{farmBg(t,{noSun:1});slKids(t,4,1840,{s:.8,sp:165,cheer:1})}
  g.restore();
  if(t>=SLCARD){const q=easeOut(prog(t,SLCARD,SLCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#831843';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,SLCARD,SLCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Skip along with us! 💖',W/2,990,64,'#fff','#DB2777');
    const sp=backOut(prog(t,SLCARD+.5,SLCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<SLCARD){sltitle(t);slcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,SLEND-1.2,SLEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
function sltitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#DB2777';g.beginPath();g.roundRect(-330,-66,660,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Skip to My Lou 💃',0,2,58,'#FFFFFF',null);g.restore()}
function slcap(t){const i=SLCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=SLCAPS[i];
  const al=Math.min(clamp((t-a)/.12),clamp((b-t)/.12));g.save();g.globalAlpha=al;let fs=64;g.font=`700 ${fs}px Fredoka, Baloo2`;let w=g.measureText(s).width;
  if(w>920){fs=Math.floor(fs*920/w);g.font=`700 ${fs}px Fredoka, Baloo2`;w=g.measureText(s).width}
  const h=120,y0=395;g.fillStyle='rgba(157,23,77,.92)';g.beginPath();g.roundRect(W/2-w/2-45,y0-h/2,w+90,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/(SLB*.9));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}
window.draw=drawSkip;
