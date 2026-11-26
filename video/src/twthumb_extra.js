window.makeH=function(){const t=13.3;sky('#0B1446','#3B2A8C');for(let k=0;k<110;k++){g.globalAlpha=.3+.7*rnd(k+9);const r=1+rnd(k+2)*2.5;ell(rnd(k)*W,rnd(k+50)*H,r,r,'#FFF6D5')}g.globalAlpha=1;
  hill(t,560);bigStar(1010,250,125,t,{wave:1});kid(1,870,690,{s:.62,t,happy:1,noHat:1,noScarf:1,trunk:1});telescope(1010,640,.75,-.6);
  for(let k=0;k<6;k++)starFace([660,1200,760,1180,700,860][k],[110,520,420,130,600,80][k],22,t,k);
  title3d('TWINKLE',300,135,104,'#FFE26B','#F59E0B',20,'#5B21B6');
  title3d('TWINKLE',300,270,104,'#FFE26B','#F59E0B',20,'#5B21B6');
  title3d('LITTLE STAR ⭐',320,405,84,'#FFFFFF','#E0E7FF',18,'#3730A3');
  g.save();g.translate(310,535);rr(-230,-42,460,84,42,'#4338CA');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 🌙',0,2,44,'#fff',null);g.restore();
  popcornLogo(70,650,.14,0)};
window.makeV=function(){const t=13.3;twSky(t,0);hill(t,1500);
  bigStar(560,960,210,t,{wave:1});for(let k=0;k<10;k++){const a=k/10*Math.PI*2;starFace(560+Math.cos(a)*400,960+Math.sin(a)*300,30,t,k)}
  kid(1,300,1700,{s:1.2,t,happy:1,noHat:1,noScarf:1,trunk:1});telescope(560,1650,1.4,-.55);
  title3d('TWINKLE TWINKLE',540,250,130,'#FFE26B','#F59E0B',24,'#5B21B6');
  title3d('LITTLE STAR ⭐',540,430,140,'#FFFFFF','#E0E7FF',24,'#3730A3');
  g.save();g.translate(540,590);rr(-290,-50,580,100,50,'#4338CA');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 🌙',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
