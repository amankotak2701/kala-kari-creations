function title3d(s,x,y,size,top,bot,lw,dark='#5B0A14'){g.font=`800 ${size}px Fredoka, Baloo2`;g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';
  for(let d=14;d>0;d-=2){g.lineWidth=lw;g.strokeStyle=dark;g.strokeText(s,x,y+d);g.fillStyle=dark;g.fillText(s,x,y+d)}
  g.lineWidth=lw;g.strokeStyle='#FFFFFF';g.strokeText(s,x,y);const gr=g.createLinearGradient(0,y-size*.5,0,y+size*.5);gr.addColorStop(0,top);gr.addColorStop(1,bot);g.fillStyle=gr;g.fillText(s,x,y)}
function flakes(n,seed){for(let k=0;k<n;k++){const r=2+rnd(k+seed)*7;g.globalAlpha=.55+.45*rnd(k+seed+1);ell(rnd(k+seed+2)*W,rnd(k+seed+3)*H,r,r,'#fff')}g.globalAlpha=1}
function thumbBg(){const gr=g.createRadialGradient(W*.6,H*.35,30,W*.5,H*.5,Math.max(W,H)*.85);gr.addColorStop(0,'#7CC4F2');gr.addColorStop(.6,'#2F7BD1');gr.addColorStop(1,'#123E8A');g.fillStyle=gr;g.fillRect(0,0,W,H)}
function hillsAt(y0){[['#D6E6F7',y0-60,40,.006],['#EEF4FC',y0,30,.009],['#FFFFFF',y0+50,20,.012]].forEach(([c,y,a,f],k)=>{g.fillStyle=c;g.beginPath();g.moveTo(0,H);for(let x=0;x<=W;x+=20)g.lineTo(x,y+Math.sin(x*f+k*2)*a);g.lineTo(W,H);g.fill()})}
window.makeH=function(){const t=24.0;thumbBg();flakes(90,3);hillsAt(560);
  pine(1200,600,.55);pine(640,590,.45);
  team(745,655,.58,t,[0,1,3],{happy:1});
  g.save();g.translate(1150,110);bellPair(0,0,1.0,24.2);g.restore();
  title3d('JINGLE',290,165,150,'#FF4D5E','#C1121F',22);
  title3d('BELLS',290,330,150,'#FFE26B','#F5A400',22,'#6B3A00');
  bell(500,320,.9,.35);
  g.save();g.translate(290,470);rr(-245,-44,490,88,44,'#15803D');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('Christmas Song 🎅',0,2,46,'#fff',null);g.restore();
  popcornLogo(70,650,.15,0)};
window.makeV=function(){const t=24.0;thumbBg();flakes(150,7);hillsAt(1320);
  pine(140,1380,1.0);pine(960,1400,.9);
  team(330,1500,1.0,t,[0,1,3],{happy:1});
  bellPair(150,560,1.3,24.2);bellPair(930,560,1.3,24.5);
  title3d('JINGLE',540,230,230,'#FF4D5E','#C1121F',32);
  title3d('BELLS 🔔',540,470,210,'#FFE26B','#F5A400',30,'#6B3A00');
  g.save();g.translate(540,1760);rr(-340,-60,680,120,60,'#15803D');g.lineWidth=7;g.strokeStyle='#fff';g.stroke();txt('Christmas Song for Kids 🎅',0,2,52,'#fff',null);g.restore();
  popcornLogo(985,1790,.22,0)};
