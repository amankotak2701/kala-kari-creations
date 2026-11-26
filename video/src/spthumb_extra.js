window.makeH=function(){const t=30.5;sky('#7DD3FC','#E0F2FE');
  ['#EF4444','#F97316','#FACC15','#22C55E','#3B82F6','#8B5CF6'].forEach((c,k)=>{g.strokeStyle=c;g.lineWidth=18;g.beginPath();g.arc(1000,760,420-k*18,Math.PI,0);g.stroke()});
  rr(820,120,460,600,0,'#FDE68A');for(let r=0;r<13;r++)for(let c=0;c<6;c++)rr(820+c*90-(r%2)*45,120+r*48+4,84,40,4,r%2?'#FCD34D':'#FDE68A');
  rr(966,40,68,700,20,'#94A3B8');rr(966,40,20,700,10,'rgba(255,255,255,.35)');for(let k=0;k<4;k++)rr(960,120+k*160,80,14,6,'#64748B');
  bigCloud(1170,70,.55,'#94A3B8');for(let k=0;k<30;k++){const x=1050+rnd(k)*230,y=120+rnd(k+3)*300;g.strokeStyle='rgba(96,165,250,.9)';g.lineWidth=4;g.beginPath();g.moveTo(x,y);g.lineTo(x-6,y+26);g.stroke()}
  sunFace(760,150,70,t,0);
  g.fillStyle='#4ADE80';g.fillRect(0,640,W,80);for(let k=0;k<8;k++)marigold(600+k*90,660+(k%2)*20,.8,['#F472B6','#FBBF24','#F87171','#A78BFA'][k%4]);
  itsy(1000,400,1.25,t,{happy:1,wave:1});ladybug(700,650,.9,t);butterfly(860,380,.9,t);
  title3d('ITSY BITSY',300,170,104,'#C084FC','#7C3AED',20,'#3B0764');
  title3d('SPIDER 🕷️',300,330,120,'#FFE26B','#F59E0B',22,'#7C2D12');
  g.save();g.translate(300,480);rr(-230,-42,460,84,42,'#16A34A');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 🌧️☀️',0,2,42,'#fff',null);g.restore();
  popcornLogo(70,650,.14,0)};
window.makeV=function(){const t=30.5;spoutScene(t,{rainbow:1});sunFace(220,780,110,t,0);
  bigCloud(900,700,.55,'#94A3B8');for(let k=0;k<30;k++){const x=780+rnd(k)*260,y=760+rnd(k+3)*300;g.strokeStyle='rgba(96,165,250,.9)';g.lineWidth=4;g.beginPath();g.moveTo(x,y);g.lineTo(x-6,y+26);g.stroke()}
  itsy(PX,1150,1.9,t,{happy:1,wave:1});ladybug(200,1620,1.4,t);butterfly(300,1250,1.3,t);butterfly(900,1400,1.2,t,'#60A5FA');
  title3d('ITSY BITSY',540,240,150,'#C084FC','#7C3AED',26,'#3B0764');
  title3d('SPIDER 🕷️',540,420,160,'#FFE26B','#F59E0B',28,'#7C2D12');
  g.save();g.translate(540,580);rr(-290,-50,580,100,50,'#16A34A');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 🌧️☀️',0,2,52,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
