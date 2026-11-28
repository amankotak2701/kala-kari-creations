function lbScene(t){river(t);bridgeOld(t,.42);builder(0,305,1720,.6,t,'stone');builder(2,800,1720,.6,t,'stick');fairLady(560,1735,.55,t,{trunk:1});
  for(let k=0;k<5;k++)ell(330+k*110,1380,50,16,'rgba(255,255,255,.85)');txt('SPLASH! 💦',560,1110,70,'#fff','#0369A1')}
window.makeH=function(){const t=17.0;sky('#7DD3FC','#E0F2FE');
  g.save();g.beginPath();g.rect(600,0,680,720);g.clip();g.translate(940,330);g.scale(.62,.62);g.translate(-540,-1400);g.save();g.translate(540,1250);g.scale(1.6,1.6);g.translate(-540,-1400);lbScene(t);g.restore();g.restore();
  title3d('LONDON',300,120,104,'#60A5FA','#1D4ED8',20,'#1E3A8A');
  title3d('BRIDGE 🌉',310,250,100,'#FFE26B','#F59E0B',20,'#7C2D12');
  title3d('is falling down!',300,375,64,'#FF6B7A','#DC2626',16,'#7F1D1D');
  g.save();g.translate(300,505);rr(-220,-42,440,84,42,'#1D4ED8');g.lineWidth=6;g.strokeStyle='#FBBF24';g.stroke();txt('Nursery Rhyme',0,2,46,'#fff',null);g.restore();
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=17.0;g.save();g.translate(540,1250);g.scale(1.6,1.6);g.translate(-540,-1400);lbScene(t);g.restore();
  title3d('LONDON BRIDGE',540,240,128,'#60A5FA','#1D4ED8',26,'#1E3A8A');
  title3d('is falling down!',540,410,110,'#FFE26B','#F59E0B',24,'#7C2D12');
  g.save();g.translate(540,570);rr(-260,-50,520,100,50,'#DC2626');g.lineWidth=7;g.strokeStyle='#FBBF24';g.stroke();txt('Nursery Rhyme 🌉',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
