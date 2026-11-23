function lightsRow(y,n,t){g.strokeStyle='#15803D';g.lineWidth=12;g.beginPath();g.moveTo(0,y);const step=W/n;for(let k=0;k<n;k++)g.quadraticCurveTo(k*step+step/2,y+40,(k+1)*step,y);g.stroke();
  for(let k=0;k<n*2;k++){const x=k*step/2+step/4,yy=y+Math.sin(((x%step)/step)*Math.PI)*32;glow(x,yy+8,26,'rgba(255,230,120,.55)');ell(x,yy+8,7,10,['#EF4444','#FBBF24','#22C55E','#3B82F6'][k%4])}}
function famBg(){const gr=g.createRadialGradient(W*.65,H*.45,30,W*.5,H*.5,Math.max(W,H)*.85);gr.addColorStop(0,'#1F8A4C');gr.addColorStop(.6,'#0F5132');gr.addColorStop(1,'#062A1A');g.fillStyle=gr;g.fillRect(0,0,W,H);
  for(let k=0;k<40;k++){g.globalAlpha=.12+.15*rnd(k);ell(rnd(k+1)*W,rnd(k+2)*H,20+rnd(k+3)*50,20+rnd(k+3)*50,['#FDE68A','#FCA5A5','#FFFFFF'][k%3])}g.globalAlpha=1}
function crowd(cx,fy,s,t){
  xmasTree(cx+300*s,fy-10*s,.62*s,t,1);
  adult('dada',cx-330*s,fy,{s:.72*s,t,pose:'wave',happy:1,hat:1});adult('dadi',cx-200*s,fy,{s:.7*s,t,pose:'clap',happy:1,hat:1});
  adult('mom',cx+180*s,fy,{s:.74*s,t,pose:'up',happy:1,hat:1});adult('dad',cx+320*s,fy,{s:.8*s,t,pose:'wave',happy:1,hat:1});
  santa(cx,fy+10*s,.95*s,t,{wave:1,sack:1});
  kid(0,cx-260*s,fy+60*s,{s:.66*s,t,happy:1,trunk:1});kid(1,cx+130*s,fy+70*s,{s:.66*s,t,happy:1,trunk:1});kid(2,cx+270*s,fy+75*s,{s:.62*s,t,happy:1,trunk:1});
  puppy(cx-120*s,fy+80*s,.6*s,t,0);present(cx-380*s,fy+85*s,110*s,85*s,'#DC2626','#FDE68A');}
window.makeH=function(){const t=10.3;famBg();flakes(60,5);lightsRow(-10,6,t);
  ell(930,735,470,80,'rgba(255,255,255,.95)');
  crowd(930,640,.95,t);
  txt('We Wish You A',300,135,58,'#FFFFFF','#7C1D1D');
  title3d('MERRY',300,255,140,'#FF4D5E','#C1121F',22);
  title3d('CHRISTMAS',300,410,104,'#FFE26B','#F5A400',18,'#6B3A00');
  g.save();g.translate(300,540);rr(-250,-42,500,84,42,'#C1121F');g.lineWidth=6;g.strokeStyle='#FDE68A';g.stroke();txt('& Happy New Year! 🎆',0,2,44,'#fff',null);g.restore();
  popcornLogo(70,650,.15,0)};
window.makeV=function(){const t=10.3;famBg();flakes(110,9);lightsRow(-10,5,t);
  txt('We Wish You A',540,250,84,'#FFFFFF','#7C1D1D');
  title3d('MERRY',540,420,210,'#FF4D5E','#C1121F',30);
  title3d('CHRISTMAS',540,640,150,'#FFE26B','#F5A400',26,'#6B3A00');
  ell(540,1600,560,110,'rgba(255,255,255,.95)');
  crowd(540,1460,1.35,t);
  g.save();g.translate(540,1790);rr(-330,-56,660,112,56,'#C1121F');g.lineWidth=7;g.strokeStyle='#FDE68A';g.stroke();txt('& Happy New Year! 🎆',0,2,56,'#fff',null);g.restore();
  popcornLogo(110,110,.26,0)};
