// ================= "Ninni Aa Gayi" lullaby scenes (Popcorn Productions) =================
const NB=0.6475,NPH=0.4; // 92.7 BPM
const rock=t=>Math.sin(2*Math.PI*(t-NPH)/(2*NB));       // gentle sway every 2 beats
const pulse=t=>Math.pow(Math.sin(Math.PI*((((t-NPH)/NB)%1+1)%1)),2);
ELE.push({c:'#B79BE0',bl:'#9D2B5E',name:'Mumma'},{c:'#7F9CC4',bl:'#1F4E79',name:'Papa'});
const END=151.5;

// ---------- night elements ----------
function village(t){g.fillStyle='#17123D';g.beginPath();g.moveTo(0,H);for(let x=0;x<=W;x+=30)g.lineTo(x,1540+Math.sin(x*.006)*50);g.lineTo(W,H);g.fill();
  for(let k=0;k<6;k++){const hx=60+k*180,hy=1530+Math.sin(hx*.006)*50;g.fillStyle='#221A55';g.fillRect(hx,hy-90,120,110);g.beginPath();g.moveTo(hx-15,hy-90);g.lineTo(hx+60,hy-150);g.lineTo(hx+135,hy-90);g.fill();
    const lit=.5+.5*Math.sin(t*.7+k*2);g.fillStyle=`rgba(253,224,71,${.35+.5*lit})`;g.fillRect(hx+20,hy-65,28,28);g.fillRect(hx+72,hy-65,28,28)}}
function nightSky(t,top='#0B1446',bot='#3E2A78',vil=true){sky(top,bot);
  for(let k=0;k<110;k++){const x=rnd(k)*W,y=rnd(k+50)*H*.75,tw=.35+.65*Math.abs(Math.sin(t*(.8+rnd(k+9))+k));
    g.globalAlpha=tw;ell(x,y,1.5+rnd(k+3)*2.5,1.5+rnd(k+3)*2.5,'#FFF6D5')}g.globalAlpha=1;
  const sp=(t%9)/9;if(sp<.12){const q=sp/.12;g.save();g.globalAlpha=1-q;g.strokeStyle='#fff';g.lineWidth=4;g.beginPath();const x0=900-q*700,y0=200+q*300;g.moveTo(x0,y0);g.lineTo(x0+120,y0-50);g.stroke();g.restore()}if(vil)village(t)}
function glow(x,y,r,col){const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,col);gr.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=gr;g.fillRect(x-r,y-r,2*r,2*r)}
function sleepyEye(x,y,r,open=0){g.strokeStyle='#3A2A2A';g.lineWidth=r*.35;g.lineCap='round';
  if(open>.5){ell(x,y,r,r*1.1,'#fff');ell(x+r*.2,y+r*.1,r*.55,r*.65,'#2A1A1A');ell(x+r*.35,y-r*.2,r*.18,r*.18,'#fff')}
  else{g.beginPath();g.arc(x,y-r*.3,r,Math.PI*.15,Math.PI*.85);g.stroke()}}
function moonFace(x,y,r,t,wink=0,open=0){glow(x,y,r*2.2,'rgba(255,240,180,.45)');
  ell(x,y,r,r,'#FFF1B8');ell(x-r*.35,y-r*.4,r*.16,r*.12,'#F3DC8C');ell(x+r*.45,y+r*.45,r*.12,r*.1,'#F3DC8C');ell(x+r*.5,y-r*.2,r*.08,r*.08,'#F3DC8C');
  sleepyEye(x-r*.33,y-r*.05,r*.13,open);if(wink>.5){g.strokeStyle='#3A2A2A';g.lineWidth=r*.05;g.beginPath();g.moveTo(x+r*.2,y-r*.05);g.lineTo(x+r*.46,y-r*.05);g.stroke()}else sleepyEye(x+r*.33,y-r*.05,r*.13,open);
  ell(x-r*.55,y+r*.2,r*.14,r*.09,'rgba(255,140,150,.55)');ell(x+r*.55,y+r*.2,r*.14,r*.09,'rgba(255,140,150,.55)');
  g.strokeStyle='#3A2A2A';g.lineWidth=r*.05;g.beginPath();g.arc(x,y+r*.18,r*.2,.2,Math.PI-.2);g.stroke()}
function starShape(x,y,r,rot,fill){g.save();g.translate(x,y);g.rotate(rot);g.beginPath();for(let k=0;k<10;k++){const a=k*Math.PI/5-Math.PI/2,rr_=k%2?r*.48:r;g.lineTo(Math.cos(a)*rr_,Math.sin(a)*rr_)}g.closePath();g.fillStyle=fill;g.fill();g.restore()}
function starFace(x,y,r,t,k=0,wave=0){glow(x,y,r*2,'rgba(255,230,120,.35)');const rot=Math.sin(t*1.5+k)*.12;starShape(x,y,r,rot,'#FFD84D');starShape(x,y,r*.8,rot,'#FFE680');
  sleepyEye(x-r*.22,y,r*.11,0);sleepyEye(x+r*.22,y,r*.11,0);g.strokeStyle='#7A4A00';g.lineWidth=r*.06;g.beginPath();g.arc(x,y+r*.15,r*.13,.2,Math.PI-.2);g.stroke();
  if(wave){g.save();g.translate(x+r*.85,y-r*.1);g.rotate(-.6+Math.sin(t*8)*.5);rr(-r*.08,-r*.45,r*.16,r*.45,r*.08,'#FFD84D');g.restore()}}
function owl(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);
  ell(0,0,80,100,'#8B5E3C');ell(0,25,55,65,'#E8C9A0');for(let k=0;k<6;k++){g.strokeStyle='#C9A27A';g.lineWidth=4;g.beginPath();g.arc(-20+(k%3)*20,10+Math.floor(k/3)*28,8,0,Math.PI);g.stroke()}
  g.fillStyle='#8B5E3C';g.beginPath();g.moveTo(-70,-70);g.lineTo(-55,-125);g.lineTo(-25,-85);g.fill();g.beginPath();g.moveTo(70,-70);g.lineTo(55,-125);g.lineTo(25,-85);g.fill();
  const bl=(t%4)<.15;ell(-32,-45,30,30,'#FFF');ell(32,-45,30,30,'#FFF');
  if(bl){g.strokeStyle='#2A1A1A';g.lineWidth=5;g.beginPath();g.moveTo(-50,-45);g.lineTo(-14,-45);g.moveTo(14,-45);g.lineTo(50,-45);g.stroke()}
  else{ell(-30,-42,15,17,'#2A1A1A');ell(34,-42,15,17,'#2A1A1A');ell(-25,-48,5,5,'#fff');ell(39,-48,5,5,'#fff')}
  g.fillStyle='#F59E0B';g.beginPath();g.moveTo(-10,-20);g.lineTo(10,-20);g.lineTo(0,0);g.fill();
  g.save();g.rotate(Math.sin(t*3)*.1);ell(-78,10,25,55,'#6E4A2E',.2);g.restore();ell(78,10,25,55,'#6E4A2E',-.2);
  g.fillStyle='#F59E0B';ell(-22,98,14,8);g.fill();ell(22,98,14,8);g.fill();g.restore()}
function branch(x0,y0,x1,y1){g.strokeStyle='#4A3020';g.lineCap='round';g.lineWidth=34;g.beginPath();g.moveTo(x0,y0);g.quadraticCurveTo((x0+x1)/2,y0+30,x1,y1);g.stroke();
  for(let k=0;k<5;k++){const u=.15+k*.18,bx=lerp(x0,x1,u),by=lerp(y0,y1,u)+10;ell(bx,by-30,28,14,'#2F6B3C',-.5+k*.3)}}
function teddy(x,y,s,t,wave=1){g.save();g.translate(x,y);g.scale(s,s);const B='#B9824F',L='#E8C39E';
  ell(-70,-10,35,60,B,.3);ell(70+0,-10,35,60,B,-.3);
  ell(0,40,110,120,B);ell(0,60,65,75,L);ell(-60,160,45,35,B);ell(60,160,45,35,B);ell(-60,165,25,18,L);ell(60,165,25,18,L);
  g.save();g.translate(95,-20);g.rotate(wave?-1.9+Math.sin(t*7)*.45:-.2);rr(-28,-10,56,120,28,B);g.restore();
  ell(-95,40,30,55,B,.25);
  ell(-70,-170,38,38,B);ell(70,-170,38,38,B);ell(-70,-170,20,20,L);ell(70,-170,20,20,L);
  ell(0,-110,100,90,B);ell(0,-80,45,35,L);ell(0,-98,16,11,'#3A2418');
  ell(-35,-125,11,13,'#2A1A1A');ell(35,-125,11,13,'#2A1A1A');ell(-31,-129,4,4,'#fff');ell(39,-129,4,4,'#fff');
  g.strokeStyle='#3A2418';g.lineWidth=5;g.beginPath();g.arc(0,-78,16,.3,Math.PI-.3);g.stroke();
  g.fillStyle='#E11D48';g.beginPath();g.moveTo(0,-30);g.lineTo(-40,-50);g.lineTo(-40,-10);g.closePath();g.moveTo(0,-30);g.lineTo(40,-50);g.lineTo(40,-10);g.closePath();g.fill();ell(0,-30,12,12,'#BE123C');
  g.restore()}
function clockFace(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);g.rotate(Math.sin(t*2)*.05);
  ell(-90,-140,45,35,'#F59E0B');ell(90,-140,45,35,'#F59E0B');rr(-8,-185,16,40,8,'#B45309');
  g.strokeStyle='#B45309';g.lineWidth=14;g.beginPath();g.moveTo(-70,140);g.lineTo(-100,190);g.moveTo(70,140);g.lineTo(100,190);g.stroke();
  ell(0,0,170,170,'#EF4444');ell(0,0,140,140,'#FFF8E7');
  for(let k=0;k<12;k++){const a=k*Math.PI/6;ell(Math.cos(a)*118,Math.sin(a)*118,k%3?5:9,k%3?5:9,'#7C2D12')}
  sleepyEye(-50,-30,22,0);sleepyEye(50,-30,22,0);ell(-80,20,18,11,'rgba(255,120,140,.5)');ell(80,20,18,11,'rgba(255,120,140,.5)');
  g.strokeStyle='#3A2A2A';g.lineWidth=7;g.beginPath();g.arc(0,40,26,.2,Math.PI-.2);g.stroke();
  const tick=Math.floor((t-NPH)/NB);g.strokeStyle='#1F2937';g.lineCap='round';g.lineWidth=10;g.save();g.rotate(tick*Math.PI/30);g.beginPath();g.moveTo(0,0);g.lineTo(0,-105);g.stroke();g.restore();
  g.lineWidth=14;g.save();g.rotate(-.9);g.beginPath();g.moveTo(0,0);g.lineTo(0,-65);g.stroke();g.restore();ell(0,0,12,12,'#1F2937');
  // nightcap
  g.save();g.translate(30,-150);g.rotate(.35);g.fillStyle='#6366F1';g.beginPath();g.moveTo(-90,20);g.quadraticCurveTo(10,-90,130,40);g.quadraticCurveTo(40,-10,-90,20);g.fill();ell(132,40,20,20,'#fff');rr(-100,10,120,30,15,'#fff');g.restore();
  g.restore()}
function zzz(x,y,t,s=1){for(let k=0;k<3;k++){const p=((t*.4+k/3)%1);g.save();g.globalAlpha=1-p;txt('z',x+p*60*s+k*10,y-p*160*s,(34+k*10)*s,'#E0E7FF','#4338CA');g.restore()}}
function nest(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);
  // sparrow
  ell(0,-60,75,60,'#A0693F');ell(10,-40,50,35,'#EBD3B0');ell(55,-95,42,40,'#A0693F');ell(70,-88,26,20,'#EBD3B0');
  sleepyEye(62,-102,10,0);g.fillStyle='#F59E0B';g.beginPath();g.moveTo(95,-95);g.lineTo(122,-88);g.lineTo(95,-80);g.fill();
  ell(-60,-70,40,20,'#7A4A2A',-.4);ell(64,-120,10,8,'#E11D48');
  // nest bowl
  g.fillStyle='#8B5A2B';g.beginPath();g.ellipse(0,-10,150,70,0,0,Math.PI);g.fill();
  g.strokeStyle='#5C3A1A';g.lineWidth=5;for(let k=0;k<14;k++){g.beginPath();g.arc(-130+k*20,-10+rnd(k)*30,30,Math.PI*.1,Math.PI*.9);g.stroke()}
  g.restore()}
function bigCloud(x,y,s,col='rgba(255,255,255,.95)'){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle=col;
  [[-180,0,90],[-80,-60,110],[60,-70,120],[180,-10,95],[0,20,120],[-120,40,80],[140,40,80]].forEach(([a,b,r])=>{g.beginPath();g.arc(a,b,r,0,7);g.fill()});g.restore()}
function bunny(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);const hop=pulse(t)*60;g.translate(0,-hop);g.rotate(rock(t)*.15);
  ell(0,0,70,85,'#FFFFFF');ell(0,20,40,50,'#FFE4EC');
  g.save();g.translate(-30,-150);g.rotate(-.2+Math.sin(t*4)*.1);ell(0,0,22,70,'#fff');ell(0,5,11,52,'#FBB6CE');g.restore();
  g.save();g.translate(30,-150);g.rotate(.2-Math.sin(t*4)*.1);ell(0,0,22,70,'#fff');ell(0,5,11,52,'#FBB6CE');g.restore();
  ell(0,-85,62,55,'#FFFFFF');ell(-22,-92,9,11,'#2A1A1A');ell(22,-92,9,11,'#2A1A1A');ell(-19,-96,3,3,'#fff');ell(25,-96,3,3,'#fff');
  ell(0,-72,9,7,'#F472B6');ell(-38,-70,12,7,'rgba(244,114,182,.4)');ell(38,-70,12,7,'rgba(244,114,182,.4)');
  const a=Math.sin(t*6)*.6;g.save();g.translate(-60,-10);g.rotate(-1.2+a);ell(0,-30,16,34,'#fff');g.restore();g.save();g.translate(60,-10);g.rotate(1.2-a);ell(0,-30,16,34,'#fff');g.restore();
  ell(-30,80,30,16,'#fff');ell(30,80,30,16,'#fff');g.restore()}
// baby elephant tucked in bed, viewed from the side; head on pillow
function bedScene(t,eyes=0,o={}){
  // room
  const gr=g.createLinearGradient(0,0,0,H);gr.addColorStop(0,'#2B2160');gr.addColorStop(1,'#1B1540');g.fillStyle=gr;g.fillRect(0,0,W,H);
  // wallpaper dots
  for(let k=0;k<60;k++){g.globalAlpha=.12;starShape(rnd(k)*W,rnd(k+3)*1300,8+rnd(k+4)*8,0,'#FDE68A')}g.globalAlpha=1;
  // arched window
  g.save();g.beginPath();g.moveTo(300,1000);g.lineTo(300,520);g.arc(540,520,240,Math.PI,0);g.lineTo(780,1000);g.closePath();g.clip();
  nightSky(t,undefined,undefined,false);moonFace(640,470,95,t,o.wink?1:0,0);g.restore();
  g.strokeStyle='#C9A86A';g.lineWidth=22;g.beginPath();g.moveTo(300,1000);g.lineTo(300,520);g.arc(540,520,240,Math.PI,0);g.lineTo(780,1000);g.closePath();g.stroke();
  g.lineWidth=10;g.beginPath();g.moveTo(540,280);g.lineTo(540,1000);g.moveTo(300,700);g.lineTo(780,700);g.stroke();
  // curtains
  g.fillStyle='#9D2B5E';g.beginPath();g.moveTo(230,250);g.quadraticCurveTo(330,700,250,1060);g.lineTo(170,1060);g.lineTo(170,250);g.fill();
  g.beginPath();g.moveTo(850,250);g.quadraticCurveTo(750,700,830,1060);g.lineTo(910,1060);g.lineTo(910,250);g.fill();
  // floor
  g.fillStyle='#3B2A1E';g.fillRect(0,1500,W,H-1500);
  ell(540,1640,430,90,'#9D2B5E');ell(540,1640,370,65,'#C2410C');ell(540,1640,300,45,'#F59E0B');
  [['#EF4444',230],['#3B82F6',300],['#22C55E',265]].forEach(([c,x],k)=>{rr(x,1585-(k==2?60:0),60,60,8,c);txt('ABC'[k],x+30,1615-(k==2?60:0),36,'#fff',null)});
  ell(800,1600,45,45,'#F472B6');ell(800,1600,45,12,'#FDE68A');
  if(o.behind)o.behind();
  // bed
  rr(110,1120,860,120,30,'#8B5A2B');rr(80,1020,60,420,24,'#6B4220');rr(940,1080,60,360,24,'#6B4220');
  rr(130,1200,820,90,40,'#F7F2E9');
  // pillow + baby head
  ell(260,1170,150,70,'#FFFFFF');
  const sway=rock(t)*3;
  const c=ELE[0].c,dk=shade(c,-.22);
  ell(300,1120+sway,95,88,c);
  g.save();g.translate(240,1110+sway);g.rotate(-.3);ell(0,0,62,78,dk);ell(2,4,46,60,'#F6B3C8');g.restore();
  // trunk curled
  g.strokeStyle=c;g.lineWidth=34;g.lineCap='round';g.beginPath();g.moveTo(380,1140+sway);g.quadraticCurveTo(440,1160,430,1210);g.stroke();
  sleepyEye(340,1100+sway,17,eyes);ell(355,1135+sway,18,10,'rgba(240,90,120,.45)');
  // nightcap
  g.save();g.translate(290,1040+sway);g.rotate(-.3);g.fillStyle='#6366F1';g.beginPath();g.moveTo(-90,10);g.quadraticCurveTo(-10,-110,-170,-60);g.quadraticCurveTo(-40,-60,90,10);g.fill();ell(-172,-60,20,20,'#fff');rr(-95,-5,190,32,16,'#fff');g.restore();
  // blanket (patchwork, breathing)
  const br=Math.sin(t*1.6)*6;
  g.save();g.beginPath();g.moveTo(400,1250);g.quadraticCurveTo(470,1060-br,700,1080-br);g.quadraticCurveTo(900,1100-br,950,1250);g.closePath();g.clip();
  for(let i=0;i<8;i++)for(let j=0;j<3;j++){g.fillStyle=['#F59E0B','#9D2B5E','#2B6CB0','#16A34A','#E11D48'][(i+j)%5];g.fillRect(400+i*70,1040+j*70-br,70,70);ell(435+i*70,1075+j*70-br,10,10,'#FDE68A')}
  g.restore();rr(400,1240,550,40,20,'#F7F2E9');
}
function parents(t,a=1){g.save();g.globalAlpha=a;
  elephant(5,190,1090,{s:.95,dir:1,t,trunk:.45+rock(t)*.1,happy:1,noShadow:1});
  elephant(6,890,1100,{s:1.0,dir:-1,t,trunk:.4-rock(t)*.1,happy:1,noShadow:1});g.restore()}
function caption(t,list){const c=list.find(([a,b])=>t>=a&&t<b);if(!c)return;const [a,b,s]=c;const al=Math.min(clamp((t-a)/.35),clamp((b-t)/.35));
  g.save();g.globalAlpha=al;g.font='700 66px Fredoka, Baloo2';const w=Math.min(960,g.measureText(s).width+90);
  g.fillStyle='rgba(15,12,45,.72)';g.beginPath();g.roundRect(W/2-w/2,1395,w,110,55);g.fill();g.lineWidth=5;g.strokeStyle='#FDE68A';g.stroke();
  const sc=1+.03*pulse(t);g.translate(W/2,1452);g.scale(sc,sc);txt(s,0,0,66,'#FFF7D6',null);g.restore()}
function ntitle(t){g.save();g.translate(W/2,170);const p=backOut(prog(t,.2,1.2));g.scale(p,p);
  g.fillStyle='rgba(15,12,45,.85)';g.beginPath();g.roundRect(-330,-70,660,140,70);g.fill();g.lineWidth=7;g.strokeStyle='#FFE600';g.stroke();
  txt('निन्नी आ गई 🌙',0,4,70,'#FFE600',null);g.restore()}

const CAPS=[
 [0.6,3.2,'निन्नी आ गई'],[3.2,6.5,'आँखें बंद करो'],[9,12,'निन्नी आ गई'],[12,15,'आँखें बंद करो'],[15,18.3,'चंदा मामा आए'],[18.3,22.2,'सपने सुंदर'],
 [22.5,27,'बेबी सो भी जाओ'],[27,30,'तारे नीचे आए'],[30.5,33.2,'चम चम चम ✨'],[33.2,36.4,'Teddy बोले come come come'],[36.4,39.4,'Soft pillow पे head रखो'],[39.4,42.4,'मम्मा की गोदी में सो'],
 [42.4,45.3,'टिक टिक टिक टिक'],[45.3,51,'चिड़िया रानी भी सोई'],[51,56.5,'बेबी भी अब सो जाए'],
 [57,60,'Twinkle twinkle ✨'],[60,63,'निन्नी आ गई'],[63,66.5,'आँखें बंद करो'],[66.5,69.5,'चंदा मामा आए'],[69.5,74.5,'सपने सुंदर'],
 [75,79,'Cloud पे bunny dance करे'],[79,84,'Tiny tiny stars ✨'],[84,89.5,'प्यारा सा dreamland'],
 [90,93,'Twinkle twinkle little star'],[93,96,'Little stars say good night'],[96,99,'ला ला ला 🎵'],[99,102,'बेबी मेरा superstar ⭐'],[102,105,'सो जा, सो जा'],[105,108,'कल करेंगे fun हज़ार'],
 [108,111,'निन्नी आ गई'],[111,114,'बेबी sleepy हो'],[114,120,'मम्मा पापा पास हैं'],[123,126,'Good night baby'],[126,129,'Sweet dreams 💤'],
 [129,132,'निन्नी आ गई'],[132,135.5,'आँखें बंद करो'],[138,141,'निन्नी आ गई'],
];

function drawNini(t){
  g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,W,H);
  if(t<22.5||(t>=129&&t<END)){ // chorus A / C: bedroom with window moon
    const local=t<22.5?t:t-129;
    const eyes=local<3.2?1:(local<9?0:(local<12?1:0));
    bedScene(t,eyes,{wink:local>16.2&&local<17.2});
    if(local>15&&local<18.3){g.save();g.globalAlpha=.6*Math.sin(Math.PI*prog(local,15,18.3));glow(640,470,320,'rgba(255,240,180,.7)');g.restore()}
    if(local>18.3&&local<22.4){const q=easeOut(prog(local,18.3,19.3));g.save();g.globalAlpha=q;ell(620,880,170,110,'rgba(255,255,255,.85)');ell(480,990,30,22,'rgba(255,255,255,.8)');ell(430,1040,16,12,'rgba(255,255,255,.75)');
      bunny(560,940,.45,t);starFace(700,850,40,t,1);g.restore()}
    if(eyes<.5)zzz(430,1000,t);
  }
  else if(t<33.2){ // stars come down + owl
    nightSky(t);moonFace(820,330,110,t);
    for(let k=0;k<7;k++){const p=easeOut(prog(t,22.5+k*.5,27+k*.5));starFace(150+k*130,lerp(-80,520+(k%2)*160,p),48,t,k,t>27&&k%3==0)}
    if(t>27){const q=easeOut(prog(t,27,28.5));branch(-40,1200,700,1150);owl(lerp(-200,330,q),1040,1.1,t);
      if(t>30.5)for(let k=0;k<14;k++){const a=t*2+k*.45;starShape(330+Math.cos(a)*(200+k*6),980+Math.sin(a)*120,14,a,'#FDE68A')}}
    g.fillStyle='#1E1B4B';g.beginPath();g.moveTo(0,1700);for(let x=0;x<=W;x+=40)g.lineTo(x,1600+Math.sin(x*.01)*40);g.lineTo(W,H);g.lineTo(0,H);g.fill();
  }
  else if(t<39.4){ // teddy + pillow
    nightSky(t,'#1E1650','#5B3A8C');moonFace(860,300,80,t);
    rr(140,1330,800,60,30,'#8B5A2B');
    if(t<36.4){teddy(540,1100,1.25,t,1)}
    else{const q=easeOut(prog(t,36.4,37.2));ell(540,1260,260*q+1,90*q+1,'#FFFFFF');ell(540,1240,220*q+1,60*q+1,'#F3F4F6');teddy(820,1150,.7,t,0);
      g.save();g.translate(470,1180);elephant(0,0,0,{s:.85,t,sleep:1,trunk:.1,noShadow:1});g.restore()}
  }
  else if(t<42.4){ // mumma's lap
    nightSky(t,'#24185A','#6B3F8E');moonFace(850,320,80,t);
    g.fillStyle='#2E1F5E';g.fillRect(0,1500,W,H-1500);
    elephant(5,360,1330,{s:1.7,t,trunk:.05,happy:1});
    ell(700,1320,190,40,'#FFFFFF');g.save();g.translate(720,1300+rock(t)*4);elephant(0,0,0,{s:.85,dir:-1,t,sleep:1,trunk:.1,noShadow:1});g.restore();
    for(let k=0;k<5;k++){const p=((t*.5+k/5)%1);g.save();g.globalAlpha=(1-p)*.8;txt('♥',600+Math.sin(p*6+k)*40,850-p*250,46,'#FB7185',null);g.restore()}
  }
  else if(t<51){ // clock, then sparrow
    nightSky(t,'#1A1446','#3E2A78');moonFace(850,300,75,t);
    if(t<45.3){clockFace(540,1000,1.5,t);zzz(780,760,t,1.2)}
    else{branch(1150,1250,250,1200);nest(560,1150,1.3,t);zzz(700,940,t);
      for(let k=0;k<3;k++)starFace(220+k*320,420+(k%2)*120,40,t,k)}
  }
  else if(t<57){ // baby asleep
    bedScene(t,0);zzz(430,1000,t,1.4);
  }
  else if(t<75){ // chorus B: big sky of stars with faces
    nightSky(t,'#0E1450','#4C2D88');
    moonFace(540,lerp(1100,560,easeOut(prog(t,57,62))),170,t,t>67&&t<68,0);
    for(let k=0;k<9;k++){const a=k/9*Math.PI*2+t*.15;starFace(540+Math.cos(a)*400,620+Math.sin(a)*330,44,t,k)}
    for(let k=0;k<3;k++)bigCloud(160+k*380,1350+k%2*60,.7,'rgba(255,255,255,.18)');
    if(t>69.5){const q=easeOut(prog(t,69.5,70.5));g.save();g.globalAlpha=q;bigCloud(540,1210,.6,'rgba(255,255,255,.9)');bunny(540,1150,.5,t);g.restore()}
  }
  else if(t<90){ // dreamland: bunny on cloud, tiny stars
    sky('#6D5BD0','#F0ABFC');
    for(let k=0;k<40;k++){const tw=.4+.6*Math.abs(Math.sin(t*2+k));g.globalAlpha=tw;starShape(rnd(k)*W,rnd(k+9)*1000,10+rnd(k+2)*14,t*.3+k,'#FFF7C2')}g.globalAlpha=1;
    moonFace(860,330,80,t);
    bigCloud(200,1350,.6,'rgba(255,255,255,.6)');bigCloud(880,1250,.55,'rgba(255,255,255,.6)');
    bigCloud(540,1150,1.1);bunny(540,1000,.9,t);
    if(t>79)for(let k=0;k<6;k++){const a=k/6*Math.PI*2+t*.4;starFace(540+Math.cos(a)*330,650+Math.sin(a)*120,32,t,k)}
    if(t>84){g.save();g.globalAlpha=prog(t,84,85);for(let k=0;k<4;k++){ell(150+k*260,820+Math.sin(t+k)*20,40,26,['#F9A8D4','#A5B4FC','#FDE68A','#99F6E4'][k]);g.strokeStyle='#fff';g.lineWidth=2;g.beginPath();g.moveTo(150+k*260,846);g.lineTo(150+k*260,960);g.stroke()}g.restore()}
  }
  else if(t<108){ // twinkle / superstar / so ja / fun hazaar
    nightSky(t,'#13104A','#5B2F8A');moonFace(860,300,80,t,t>93&&t<93.6);
    if(t<99){for(let k=0;k<5;k++){const x=180+k*180,y=800+Math.sin(t*2+k)*40;starFace(x,y,62,t,k,t>93&&t<96)}
      if(t>96)notes(540,1250,t,96,6)}
    else if(t<105){const q=backOut(prog(t,99,100));elephant(0,540,1320,{s:1.3,t,trunk:.6,happy:1});
      g.save();g.translate(610,990);g.scale(q,q);starShape(0,0,90,rock(t)*.15,'#FFD84D');starShape(0,0,70,rock(t)*.15,'#FFE680');g.restore();
      if(t>102){g.save();g.globalAlpha=prog(t,102,103)*.6;g.fillStyle='#0B0A2A';g.fillRect(0,0,W,H);g.restore();zzz(700,900,t,1.2)}}
    else{sky('#7DD3FC','#FDE68A');g.fillStyle='#86EFAC';g.fillRect(0,1300,W,H-1300);
      for(let k=0;k<7;k++){const bx=120+k*140,by=900-((t-105)*120+k*90)%600;ell(bx,by,45,56,['#EF4444','#F59E0B','#22C55E','#3B82F6','#A855F7','#EC4899','#14B8A6'][k]);g.strokeStyle='#555';g.lineWidth=2;g.beginPath();g.moveTo(bx,by+56);g.lineTo(bx+Math.sin(t*3+k)*10,by+200);g.stroke()}
      elephant(0,540,1320-pulse(t)*50,{s:1.15,t,trunk:.9,happy:1});
      g.save();g.globalAlpha=.25;g.fillStyle='#fff';g.fillRect(0,0,W,H);g.restore();ell(540,700,420,260,'rgba(255,255,255,0)')}
  }
  else if(t<123){ // mumma papa beside the bed
    bedScene(t,0,{behind:()=>parents(t,easeOut(prog(t,108,109.5)))});zzz(430,1000,t);
    if(t>114)for(let k=0;k<6;k++){const p=((t*.4+k/6)%1);g.save();g.globalAlpha=(1-p);txt('♥',300+k*90+Math.sin(p*5)*20,1300-p*400,44,'#FB7185',null);g.restore()}
  }
  else { // 123-129 good night, sweet dreams: dream bubble
    nightSky(t,'#0B1446','#3E2A78');moonFace(540,520,150,t);
    const q=easeOut(prog(t,123,124.5));g.save();g.globalAlpha=q;bigCloud(540,1150,1.2,'rgba(255,255,255,.92)');
    bunny(380,1080,.55,t);starFace(560,1010,50,t,2,1);owl(720,1080,.5,t);g.restore();
  }
  // gentle cross-fades between scenes
  [22.5,33.2,39.4,42.4,51,57,75,90,99,105,108,123,129].forEach(c=>{const d=Math.abs(t-c);if(d<.35){g.fillStyle=`rgba(8,6,30,${(1-d/.35)*.9})`;g.fillRect(0,0,W,H)}});
  if(t<END-11){ntitle(t);caption(t,CAPS);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  // end card
  if(t>=END-11){const q=easeOut(prog(t,END-11,END-9.6));g.save();g.globalAlpha=q*.75;g.fillStyle='#07061F';g.fillRect(0,0,W,H);g.restore();
    g.save();g.globalAlpha=q;popcornLogo(W/2,640,.95*backOut(prog(t,END-11,END-9.8)),Math.max(0,Math.sin(Math.PI*prog(t,END-9.8,END-9.3)))*.25);
    txt('A Popcorn Productions video',W/2,1040,46,'#FFE600',null,'center',600);
    txt('शुभ रात्रि! Good night 🌙',W/2,1140,58,'#FFF7D6',null);
    const sp=backOut(prog(t,END-9,END-8));g.translate(W/2,1290);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();
    caption(t,CAPS)}
  if(t<.8){g.fillStyle=`rgba(0,0,0,${1-t/.8})`;g.fillRect(0,0,W,H)}
  const f=prog(t,END-1.8,END);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawNini;
