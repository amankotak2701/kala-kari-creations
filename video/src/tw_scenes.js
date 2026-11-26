// ================= "Twinkle Twinkle Little Star" — Popcorn Productions =================
const TWL=6.0, TWV=[11.9,53.9,95.9];
const twl=(v,l)=>TWV[v]+l*TWL;
const TWCARD=132.4, TWEND=138.0;
const twpu=t=>Math.pow(Math.sin(Math.PI*((((t-TWV[0])/1.5)%1+1)%1)),2);
const TWLYR=[
 ['Twinkle, twinkle, little star,','How I wonder what you are!','Up above the world so high,','Like a diamond in the sky.','Twinkle, twinkle, little star,','How I wonder what you are!'],
 ['When the blazing sun is gone,','When he nothing shines upon,','Then you show your little light,','Twinkle, twinkle, all the night.','Twinkle, twinkle, little star,','How I wonder what you are!']];
TWLYR.push(TWLYR[0]);

function bigStar(x,y,r,t,o={}){const tw=1+.06*Math.sin(t*4)+(o.pulse||0)*.15;g.save();g.translate(x,y);g.scale(tw,tw);if(o.rot)g.rotate(o.rot);
  glow(0,0,r*2.6*(o.bright||1),`rgba(255,236,150,${.55*(o.bright||1)})`);
  for(let k=0;k<8;k++){g.save();g.rotate(k*Math.PI/4+t*.3);g.globalAlpha=.35+.3*Math.sin(t*3+k);g.fillStyle='#FFF7C2';g.beginPath();g.moveTo(0,-r*1.55);g.lineTo(r*.06,-r*1.05);g.lineTo(-r*.06,-r*1.05);g.fill();g.restore()}
  if(o.diamond){g.fillStyle='#A5F3FC';g.beginPath();g.moveTo(0,-r);g.lineTo(r*.9,-r*.25);g.lineTo(0,r*1.05);g.lineTo(-r*.9,-r*.25);g.closePath();g.fill();
    g.fillStyle='#67E8F9';g.beginPath();g.moveTo(-r*.9,-r*.25);g.lineTo(r*.9,-r*.25);g.lineTo(0,r*1.05);g.closePath();g.fill();
    g.strokeStyle='#FFFFFF';g.lineWidth=r*.04;g.beginPath();g.moveTo(-r*.45,-r*.62);g.lineTo(-r*.3,-r*.25);g.lineTo(0,r*1.05);g.lineTo(r*.3,-r*.25);g.lineTo(r*.45,-r*.62);g.moveTo(-r*.9,-r*.25);g.lineTo(r*.9,-r*.25);g.stroke()}
  else{starShape(0,0,r,0,'#FFD84D');starShape(0,0,r*.78,0,'#FFE680');ell(-r*.25,-r*.3,r*.12,r*.08,'rgba(255,255,255,.6)',-.5)}
  // face
  const ey=-r*.02,blink=(t%3.3)<.14;
  if(o.sleep){g.strokeStyle='#7A4A00';g.lineWidth=r*.05;g.lineCap='round';g.beginPath();g.arc(-r*.2,ey,r*.09,Math.PI*.15,Math.PI*.85);g.stroke();g.beginPath();g.arc(r*.2,ey,r*.09,Math.PI*.15,Math.PI*.85);g.stroke()}
  else if(blink||o.wink){g.strokeStyle='#7A4A00';g.lineWidth=r*.05;g.beginPath();g.moveTo(-r*.28,ey);g.lineTo(-r*.12,ey);g.moveTo(r*.12,ey);g.lineTo(r*.28,ey);g.stroke()}
  else{ell(-r*.2,ey,r*.08,r*.11,'#3B2A1A');ell(r*.2,ey,r*.08,r*.11,'#3B2A1A');ell(-r*.17,ey-r*.04,r*.03,r*.03,'#fff');ell(r*.23,ey-r*.04,r*.03,r*.03,'#fff')}
  ell(-r*.36,ey+r*.15,r*.09,r*.05,'rgba(255,120,140,.55)');ell(r*.36,ey+r*.15,r*.09,r*.05,'rgba(255,120,140,.55)');
  g.fillStyle='#9A3412';g.beginPath();g.arc(0,ey+r*.15,r*.13,0,Math.PI);g.fill();
  if(o.wave){g.save();g.translate(r*.78,-r*.2);g.rotate(-.5+Math.sin(t*8)*.4);rr(-r*.07,-r*.42,r*.14,r*.42,r*.07,'#FFD84D');g.restore()}
  g.restore();
  // sparkles
  for(let k=0;k<6;k++){const a=t*.8+k;const d=r*(1.6+.3*Math.sin(t*2+k));const s=(.5+.5*Math.sin(t*5+k*2))*r*.12;starShape(x+Math.cos(a)*d,y+Math.sin(a)*d,s,a,'#FFFFFF')}}
function twSky(t,mode=0){ // 0 night, 1 sunset, 2 dusk
  if(mode===1)sky('#F97316','#FDE68A');else if(mode===2)sky('#4C1D95','#F472B6');else sky('#0B1446','#3B2A8C');
  if(mode!==1)for(let k=0;k<120;k++){const tw=.3+.7*Math.abs(Math.sin(t*(1+rnd(k)*1.5)+k));g.globalAlpha=tw*(mode===2?.6:1);const r=1.2+rnd(k+2)*2.8;ell(rnd(k)*W,rnd(k+50)*1350,r,r,'#FFF6D5')}g.globalAlpha=1}
function hill(t,y=1520){g.fillStyle='#14532D';g.beginPath();g.moveTo(0,H);g.lineTo(0,y+80);g.quadraticCurveTo(540,y-160,W,y+80);g.lineTo(W,H);g.fill();
  g.fillStyle='#166534';g.beginPath();g.moveTo(0,H);g.lineTo(0,y+200);g.quadraticCurveTo(300,y+90,700,y+180);g.quadraticCurveTo(900,y+220,W,y+160);g.lineTo(W,H);g.fill();
  for(let k=0;k<10;k++){const fx=60+k*105,fy=y+120+Math.sin(k)*30;g.globalAlpha=.6+.4*Math.sin(t*2+k);ell(fx,fy,4,4,'#FDE68A');g.globalAlpha=1}}
function telescope(x,y,s,ang){g.save();g.translate(x,y);g.scale(s,s);g.strokeStyle='#4B5563';g.lineWidth=8;g.beginPath();g.moveTo(0,0);g.lineTo(-40,90);g.moveTo(0,0);g.lineTo(40,90);g.moveTo(0,0);g.lineTo(0,95);g.stroke();
  g.rotate(ang);rr(-20,-24,170,48,18,'#2563EB');rr(130,-30,40,60,10,'#1E3A8A');rr(-40,-16,30,32,8,'#93C5FD');g.restore()}
function sunFace(x,y,r,t,bye=0){glow(x,y,r*2,'rgba(255,200,80,.55)');mandalaSun(x,y,r,t);
  g.strokeStyle='#9A3412';g.lineWidth=r*.07;g.lineCap='round';g.beginPath();g.arc(x-r*.28,y-r*.05,r*.12,Math.PI*1.1,Math.PI*1.9);g.stroke();g.beginPath();g.arc(x+r*.28,y-r*.05,r*.12,Math.PI*1.1,Math.PI*1.9);g.stroke();
  g.beginPath();g.arc(x,y+r*.18,r*.2,.2,Math.PI-.2);g.stroke();if(bye){g.save();g.translate(x+r*1.15,y-r*.3);g.rotate(-.6+Math.sin(t*7)*.5);rr(-r*.09,-r*.5,r*.18,r*.5,r*.09,'#FBBF24');g.restore()}}
function earth(x,y,r,t){g.save();ell(x,y,r,r,'#3B82F6');g.beginPath();g.arc(x,y,r,0,7);g.clip();g.translate(x,y);g.rotate(t*.1);
  [[-.4,-.3,.35,.25],[.3,-.1,.3,.4],[-.1,.45,.4,.2],[.55,.5,.2,.18]].forEach(([a,b,c,d])=>ell(a*r,b*r,c*r,d*r,'#22C55E',a));g.restore();glow(x,y,r*1.25,'rgba(147,197,253,.25)');
  g.strokeStyle='rgba(255,255,255,.5)';g.lineWidth=6;g.beginPath();g.arc(x,y,r,Math.PI*1.1,Math.PI*1.5);g.stroke()}
function sleepyKid(x,y,s,t,awake){g.save();g.translate(x,y);g.scale(s,s);
  rr(-260,-40,520,120,24,'#7C3AED');rr(-280,-150,40,260,16,'#5B21B6');rr(240,-110,40,220,16,'#5B21B6');
  ell(-170,-60,110,50,'#FFFFFF');const K=KIDS[1];ell(-160,-110,68,62,K.skin);g.fillStyle=K.hair;g.beginPath();g.ellipse(-160,-140,72,46,0,Math.PI,0);g.fill();ell(-232,-100,18,28,K.hair);ell(-88,-100,18,28,K.hair);
  if(awake){ell(-182,-112,8,11,'#2A1A1A');ell(-138,-112,8,11,'#2A1A1A')}else{g.strokeStyle='#2A1A1A';g.lineWidth=5;g.beginPath();g.arc(-182,-116,10,Math.PI*.15,Math.PI*.85);g.stroke();g.beginPath();g.arc(-138,-116,10,Math.PI*.15,Math.PI*.85);g.stroke()}
  ell(-200,-88,11,7,'rgba(240,100,120,.45)');ell(-120,-88,11,7,'rgba(240,100,120,.45)');g.strokeStyle='#9F1239';g.lineWidth=4;g.beginPath();g.arc(-160,-86,awake?12:8,.2,Math.PI-.2);g.stroke();
  const br=Math.sin(t*1.5)*6;g.fillStyle='#F9A8D4';g.beginPath();g.moveTo(-110,-40);g.quadraticCurveTo(0,-130-br,240,-60);g.lineTo(240,40);g.lineTo(-110,40);g.closePath();g.fill();
  for(let k=0;k<6;k++)starShape(-60+k*55,-40-((k%2)*30)-br*.5,14,0,'#FDE68A');g.restore()}
function twtitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#4338CA';g.beginPath();g.roundRect(-420,-66,840,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#FDE047';g.stroke();txt('Twinkle Twinkle Little Star ⭐',0,2,48,'#FFFFFF',null);g.restore()}
const TWCAPS=[];TWLYR.forEach((v,vi)=>v.forEach((s,k)=>TWCAPS.push([twl(vi,k)-.3,twl(vi,k+1)-.3+(k===5?.8:0),s])));
function twcap(t){const i=TWCAPS.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=TWCAPS[i];
  const al=Math.min(clamp((t-a)/.25),clamp((b-t)/.25));g.save();g.globalAlpha=al;g.font='700 64px Fredoka, Baloo2';
  const w=g.measureText(s).width;const h=120,y0=390;g.fillStyle='rgba(30,27,75,.85)';g.beginPath();g.roundRect(W/2-w/2-50,y0-h/2,w+100,h,40);g.fill();g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();
  const prg=clamp((t-a)/((b-a)*.85));const x=W/2-w/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(s,x,y0+2);
  g.save();g.beginPath();g.rect(x,y0-60,w*prg,120);g.clip();g.fillStyle='#FFE14D';g.fillText(s,x,y0+2);g.restore();g.restore()}

function drawTwinkle(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  const v=t<TWV[0]?-1:(t<TWV[1]-.3?0:(t<TWV[2]-.3?1:2));const L=v<0?-1:Math.floor((t-TWV[v])/TWL);const lt=v<0?0:(t-twl(v,L));
  const kidOnHill=(o={})=>{kid(o.k??1,o.x??290,o.y??1640,{s:1.15,t,happy:o.happy??1,noHat:1,noScarf:1,cap:o.cap,trunk:o.cheer?1:.5,dir:o.dir||1})};
  if(v<0){ // intro: dusk, kid sets up a telescope, first star appears
    twSky(t,2);hill(t);telescope(520,1590,1.35,-.5);kidOnHill({happy:1});
    const q=easeOut(prog(t,4,9));if(q>0)bigStar(720,860,130*q,t,{wave:t>8});
    if(t>8.5)pop(t,8.5,'Hello, little star! 👋',540,1130,62,'#fff','#4338CA');
  }
  else if(v===0||v===2){
    const night=v===2;
    if(night&&L>=4){ // bedtime ending of the last verse
      twSky(t,0);const g2=g;rr(0,1100,W,H-1100,0,'#312E81');
      g.save();g.beginPath();g.roundRect(240,560,600,520,40);g.clip();twSky(t,0);bigStar(560,800,110,t,{wave:L===5,sleep:L===5&&lt>3,bright:1});g.restore();
      g.strokeStyle='#C4B5FD';g.lineWidth=18;g.beginPath();g.roundRect(240,560,600,520,40);g.stroke();g.lineWidth=8;g.beginPath();g.moveTo(540,560);g.lineTo(540,1080);g.moveTo(240,820);g.lineTo(840,820);g.stroke();
      sleepyKid(560,1560,1.25,t,L===4&&lt<3);zzz(380,1330,t,1.3);
      for(let k=0;k<20;k++){const p=((t*.3+k/20)%1);starShape(560+Math.sin(k*3+p*4)*300,1100+p*400,6*(1-p),t,'#FDE68A')}
    }
    else{
      twSky(t,0);
      if(L===2){ // up above the world so high
        earth(540,1850,560,t);bigStar(540,840,150,t,{wave:1});kid(1,540,1300,{s:.45,t,happy:1,noHat:1,noScarf:1,trunk:1});
        txt('🌍',0,0,1,'#000',null)}
      else{hill(t);
        const zoom=L===1;telescope(520,1590,1.35,-.5);kidOnHill({cheer:L===0||L===4,happy:L!==1});
        if(L===1){ // telescope view
          bigStar(760,760,80,t,{});g.save();ell(540,1050,250,250,'#000');g.beginPath();g.arc(540,1050,236,0,7);g.clip();twSky(t,0);bigStar(540,1050,160,t,{wink:lt>2&&lt<3.2});g.restore();
          g.strokeStyle='#1E3A8A';g.lineWidth=20;g.beginPath();g.arc(540,1050,240,0,7);g.stroke();
          for(let k=0;k<3;k++){const p=((t*.6+k/3)%1);g.save();g.globalAlpha=1-p;txt('?',260+k*40,1450-p*200,60,'#FDE047','#4338CA');g.restore()}}
        else if(L===3){bigStar(560,920,180,t,{diamond:1,bright:1.3});for(let k=0;k<16;k++){const a=t+k*.4;starShape(540+Math.cos(a)*260,880+Math.sin(a)*260,10+6*Math.sin(t*6+k),a,'#E0F2FE')}pop(t,twl(v,3)+.3,'💎 Sparkle! 💎',540,1200,64,'#fff','#0891B2')}
        else{bigStar(700,880,L===4?160:145,t,{wave:L===5,pulse:twpu(t)});if(L===4)for(let k=0;k<12;k++){const a=k/12*Math.PI*2+t*.4;starFace(700+Math.cos(a)*320,880+Math.sin(a)*260,30,t,k)}}
      }
    }
  }
  else if(v===1){ // verse 2: sunset -> night -> the star lights up -> constellation
    if(L===0){const q=prog(t,twl(1,0),twl(1,1));twSky(t,1);sunFace(540,lerp(900,1500,easeOut(q)),150,t,1);hill(t);kidOnHill({happy:1});pop(t,twl(1,0)+.4,'Bye-bye, Sun! 🌇',540,700,64,'#fff','#EA580C')}
    else if(L===1){const q=prog(t,twl(1,1),twl(1,2));sky('#0B1446','#1E1B4B');g.save();g.globalAlpha=1-q;sky('#7C2D12','#F97316');g.restore();hill(t);kidOnHill({happy:0});pop(t,twl(1,1)+1,'So dark... 🌑',540,900,64,'#fff','#334155')}
    else if(L===2){twSky(t,0);hill(t);const q=easeOut(prog(t,twl(1,2),twl(1,2)+1.5));bigStar(560,900,165*q+1,t,{bright:1+q*.6,wave:q>.9});kidOnHill({cheer:1});
      if(q>0&&q<1){g.save();g.globalAlpha=1-q;g.fillStyle='#FFF7C2';g.fillRect(0,0,W,H);g.restore()}pop(t,twl(1,2)+1.4,'✨ Ta-da! ✨',540,1180,66,'#fff','#CA8A04')}
    else if(L===3){twSky(t,0);hill(t);const pts=[[300,700],[420,620],[560,680],[680,600],[800,700],[700,840],[560,920],[420,840]];const q=prog(t,twl(1,3),twl(1,4)-1);
      g.strokeStyle='rgba(253,224,71,.8)';g.lineWidth=5;g.beginPath();pts.slice(0,1+Math.floor(q*pts.length)).forEach(([x,y],k)=>k?g.lineTo(x,y):g.moveTo(x,y));if(q>=1)g.closePath();g.stroke();
      pts.forEach(([x,y],k)=>starFace(x,y,30,t,k));kidOnHill({cheer:1});bigStar(880,1000,70,t,{})}
    else{twSky(t,0);hill(t);bigStar(700,880,150,t,{wave:L===5,pulse:twpu(t)});
      [[0,180,1],[1,330,1],[3,860,-1]].forEach(([k,x,d],i)=>kid(k,x,1640-Math.max(0,Math.sin(t*Math.PI/1.5+i))*30,{s:.75,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[k],trunk:1,dir:d}))}
  }
  // interludes: shooting star / stardust between verses
  if(t>twl(0,6)-.3&&t<TWV[1]-.3){twSky(t,0);hill(t);kidOnHill({cheer:1});const q=prog(t,twl(0,6),TWV[1]-1);const sx=lerp(-100,1200,q),sy=lerp(600,1100,q);
    for(let k=0;k<20;k++)starShape(sx-k*28,sy-k*11,14-k*.6,t*4+k,'rgba(255,245,200,'+(1-k/20)+')');bigStar(sx,sy,50,t,{});pop(t,twl(0,6)+.6,'Make a wish! 🌠',540,950,70,'#fff','#7C3AED')}
  if(t>twl(1,6)-.3&&t<TWV[2]-.3){twSky(t,0);hill(t);bigStar(540,800,120,t,{wave:1});for(let k=0;k<40;k++){const p=((t*.4+k/40)%1);starShape(540+Math.sin(k*2+p*3)*350,800+p*900,8*(1-p),t*3+k,'#FDE68A')}
    [[0,200],[1,400],[3,700],[2,880]].forEach(([k,x],i)=>kid(k,x,1640,{s:.72,t,happy:1,noHat:1,noScarf:1,cap:CAPS2[k],trunk:1}));pop(t,twl(1,6)+.6,'Stardust! ✨',540,1150,70,'#fff','#CA8A04')}
  if(t>=TWCARD){const q=easeOut(prog(t,TWCARD,TWCARD+.8));g.save();g.globalAlpha=q*.75;g.fillStyle='#0B1446';g.fillRect(0,0,W,H);g.restore();g.save();g.globalAlpha=q;
    popcornLogo(W/2,520,.85*backOut(prog(t,TWCARD,TWCARD+1)),0);txt('A Popcorn Productions video',W/2,880,46,'#FFE14D',null,'center',600);txt('Good night, little star! ⭐',W/2,990,64,'#fff','#4338CA');
    const sp=backOut(prog(t,TWCARD+.6,TWCARD+1.4));g.save();g.translate(W/2,1140);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();g.restore()}
  if(t<TWCARD){twtitle(t);twcap(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  const cuts=[];for(let vv=0;vv<3;vv++)for(let k=0;k<=6;k++)cuts.push(twl(vv,k)-.3);cuts.forEach(c=>{const d=Math.abs(t-c);if(d<.25){g.fillStyle=`rgba(11,20,70,${(1-d/.25)*.7})`;g.fillRect(0,0,W,H)}});
  if(t<.6){g.fillStyle=`rgba(0,0,0,${1-t/.6})`;g.fillRect(0,0,W,H)}
  const f=prog(t,TWEND-1.2,TWEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawTwinkle;
