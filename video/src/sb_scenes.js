// ================= "Spring Time Family Band" — Popcorn Productions =================
const SBB=.6185, SBBAR=4*SBB, SBP=8*SBBAR, SB0=.58;
const sbp=k=>SB0+k*SBP;
const SBCARD=131.6, SBEND=138.1;
function bfly(x,y,s,t,c='#F472B6'){g.save();g.translate(x,y);g.scale(s,s);const f=Math.abs(Math.sin(t*12));g.save();g.scale(f*.8+.2,1);ell(-30,-14,30,24,c);ell(-24,18,20,16,c);ell(30,-14,30,24,c);ell(24,18,20,16,c);g.restore();rr(-5,-26,10,52,5,'#3F2A1E');g.restore()}
// band members: join time, label
const SBM=[
 {k:'dad',  x:300,y:1680,join:sbp(1),       lab:'🥁 Daddy plays the drums!'},
 {k:'mom',  x:540,y:1680,join:sbp(1)+SBP/2, lab:'🎸 Mummy plays the guitar!'},
 {k:'sis',  x:180,y:1900,join:sbp(2),       lab:'🎵 Sister plays the xylophone!'},
 {k:'bro',  x:420,y:1900,join:sbp(2)+SBP/2, lab:'🪇 Brother shakes the tambourine!'},
 {k:'dada', x:800,y:1680,join:sbp(3),       lab:'🎺 Grandpa plays the trumpet!'},
 {k:'dadi', x:660,y:1900,join:sbp(3)+SBP/2, lab:'👵 Grandma sings la la la!'}];
const SBCAPS=[[sbp(0)+1,sbp(1)-.3,'Spring is here! 🌸'],...SBM.map(m=>[m.join-.3,m.join+SBP/2-.3,m.lab]),
  [sbp(4)-.3,sbp(4)+SBP/2-.3,'The whole family band! 🎶'],[sbp(4)+SBP/2-.3,sbp(5)-.3,'Everybody dance! 🐰🦋'],
  [sbp(5)-.3,sbp(5)+SBP/2-.3,'Pitter-patter, spring rain! 🌧️'],[sbp(5)+SBP/2-.3,sbp(6)-.3,'Look, a rainbow! 🌈'],[sbp(6)-.3,SBCARD,'Take a bow! 👏 La la la!']];
const sbbeat=t=>Math.pow(Math.max(0,Math.cos(Math.PI*2*(t-SB0)/SBB)),4);
function sbMember(m,t,fin){const q=easeOut(prog(t,m.join,m.join+1.4));if(q<=0)return;const x=lerp(m.x<500?-200:1280,m.x,q),y=m.y,walking=q<1,b=sbbeat(t);
  if(m.k==='dad'){adult('dad',x,y,{s:.68,t,pose:fin?'up':'hold',happy:1});if(!fin)drumKit(x,y,.9,t,!walking)}
  else if(m.k==='mom'){adult('mom',x,y,{s:.68,t,pose:fin?'up':'hold',happy:1});if(!fin)guitar(x+10,y-160,.75,t)}
  else if(m.k==='dada'){adult('dada',x,y,{s:.68,t,pose:fin?'up':'hold',happy:1,dir:-1});if(!fin){trumpet(x-30,y-255,.6,t,Math.PI+.15);if(!walking&&t>m.join+1.4)for(let j=0;j<3;j++){const p=((t*.6+j/3)%1);g.save();g.globalAlpha=1-p;txt('♪',x-180-p*120,y-280-p*120,46,'#FACC15',null);g.restore()}}}
  else if(m.k==='dadi'){adult('dadi',x,y-b*12,{s:.68,t,pose:'up',happy:1,dir:-1});if(!walking)for(let j=0;j<3;j++){const p=((t*.5+j/3)%1);g.save();g.globalAlpha=1-p;txt('la',x-60+j*40,y-330-p*160,40,'#fff','#DB2777');g.restore()}}
  else if(m.k==='sis'){kid(1,x,y-(fin?b*30:0),{s:.75,t,happy:1,noHat:1,noScarf:1,trunk:fin?1:.5});if(!fin)xylophone(x,y-30,.55,t,!walking)}
  else if(m.k==='bro'){kid(0,x,y-b*20,{s:.75,t,happy:1,noHat:1,noScarf:1,trunk:1});if(!fin)tambourine(x+50,y-190,.6,t)}}
function rainCloud(t,a){for(let k=0;k<3;k++){g.save();g.globalAlpha=a;ell(250+k*290,1080,170,70,'#94A3B8');ell(320+k*290,1040,110,60,'#CBD5E1');g.restore()}
  g.save();g.globalAlpha=a;g.strokeStyle='#60A5FA';g.lineWidth=5;for(let k=0;k<60;k++){const x=rnd(k)*W,p=((t*1.6+rnd(k+3))%1);g.beginPath();g.moveTo(x,1100+p*800);g.lineTo(x-8,1130+p*800);g.stroke()}g.restore()}
function rainbow(a){g.save();g.globalAlpha=a;['#EF4444','#F97316','#FACC15','#22C55E','#3B82F6','#8B5CF6'].forEach((c,i)=>{g.strokeStyle=c;g.lineWidth=32;g.beginPath();g.arc(540,1500,520-i*32,Math.PI,0);g.stroke()});g.restore()}
function umbrella(x,y,s,c){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle=c;g.beginPath();g.arc(0,0,150,Math.PI,0);g.closePath();g.fill();rr(-5,0,10,180,5,'#78350F');g.restore()}
function drawBand(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  g.save();g.translate(540,1770);g.scale(1.3,1.3);g.translate(-540,-1840);
  const rainA=t>=sbp(5)-.3&&t<sbp(5)+SBP/2?Math.min(clamp((t-sbp(5)+.3)/1.5),clamp((sbp(5)+SBP/2-t)/1.2)):0;
  springGarden(t,{petals:t<sbp(5)||t>sbp(5)+SBP/2});
  if(t>=sbp(5)+SBP/2-1)rainbow(clamp((t-sbp(5)-SBP/2+1)/1.5));
  g.fillStyle='rgba(253,230,138,.6)';g.beginPath();g.ellipse(540,1820,470,150,0,0,Math.PI*2);g.fill();
  const fin=t>=sbp(6)-.3;
  if(t<sbp(1)-.3){ // intro: family walks in carrying instruments, flowers bloom
    const q=easeOut(prog(t,2,10));[['dad',-1],['mom',-.5],['dada',.5],['dadi',1]].forEach(([w,o],i)=>adult(w,lerp(o<0?-200:1280,540+o*240,q),1760,{s:.62,t,pose:q>=1?'wave':'sway',happy:1,dir:o<0?1:-1}));
    kid(0,lerp(-300,430,q),1900,{s:.7,t,happy:1,noHat:1,noScarf:1,trunk:q>=1?1:.5});kid(1,lerp(1380,650,q),1900,{s:.7,t,happy:1,noHat:1,noScarf:1,trunk:q>=1?1:.5,dir:-1});
    for(let k=0;k<3;k++)birdS(((t*80+k*400)%1400)-200,1150+k*60+Math.sin(t*3+k)*20,.8,t,['#60A5FA','#F472B6','#FACC15'][k]);
    pop(t,2.5,'Spring is here! 🌸',540,1240,64,'#fff','#DB2777');pop(t,11,'Let\'s make music! 🎶',540,1240,62,'#fff','#2563EB')}
  else{
    SBM.filter(m=>m.y<1800).forEach(m=>sbMember(m,t,fin));SBM.filter(m=>m.y>=1800).forEach(m=>sbMember(m,t,fin));
    SBM.forEach(m=>pop(t,m.join+.2,m.lab.split(' ')[0],m.x,m.y-(m.y<1800?470:330),80,'#fff',null));
    if(t>=sbp(4)-.3&&t<sbp(5)){bunny(880,1880,.45,t);bunny(140,1700,.4,t+.3);for(let k=0;k<4;k++)bfly(200+k*220+Math.sin(t*2+k)*60,1250+Math.sin(t*3+k)*60,.7,t,['#F472B6','#FACC15','#A78BFA','#60A5FA'][k]);
      for(let j=0;j<6;j++){const p=((t*.5+j/6)%1);g.save();g.globalAlpha=1-p;txt(j%2?'♫':'♪',200+j*130,1450-p*280,56,['#FDE047','#F472B6','#60A5FA'][j%3],null);g.restore()}}
    if(rainA>0){rainCloud(t,rainA);umbrella(300,1430,.9*rainA,'#EF4444');umbrella(780,1430,.9*rainA,'#3B82F6')}
    if(t>=sbp(5)+SBP/2)for(let k=0;k<3;k++)birdS(((t*80+k*400)%1400)-200,1100+k*70,.8,t,['#60A5FA','#F472B6','#FACC15'][k]);
    if(fin){confetti(t,sbp(6)-.3,70);pop(t,sbp(6)+.3,'The Family Band! 👏',540,1240,64,'#fff','#DB2777')}}
  g.restore();
  if(t>=SBCARD){const q=easeOut(prog(t,SBCARD,SBCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#831843';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,SBCARD,SBCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Happy spring! 🌸🎶',W/2,990,64,'#fff','#DB2777');
    const sp=backOut(prog(t,SBCARD+.5,SBCARD+1.3));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<SBCARD){sbtitle(t);sbcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,SBEND-1.2,SBEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
function sbtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#DB2777';g.beginPath();g.roundRect(-370,-66,740,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Spring Time Family Band 🌸',0,2,50,'#FFFFFF',null);g.restore()}
function sbcap(t){const i=SBCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=SBCAPS[i];
  const al=Math.min(clamp((t-a)/.2),clamp((b-t)/.2));g.save();g.globalAlpha=al;let fs=60;g.font=`700 ${fs}px Fredoka, Baloo2`;let w=g.measureText(s).width;
  if(w>920){fs=Math.floor(fs*920/w);g.font=`700 ${fs}px Fredoka, Baloo2`;w=g.measureText(s).width}
  const h=116,y0=395;g.fillStyle='rgba(21,128,61,.92)';g.beginPath();g.roundRect(W/2-w/2-45,y0-h/2,w+90,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/2.4);const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}
window.draw=drawBand;
