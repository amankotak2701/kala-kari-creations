function rbScene(t){g.save();g.translate(540,1590);g.scale(1.2,1.2);g.translate(-540,-1560);gardenBg(t);bigTree(430,1560,1,t);
  hangCradle(740,975,.75,t,{sw:-.06,t2:0});adult('mom',250,1820,{s:1.0,t,pose:'wave',happy:1});
  for(let k=0;k<6;k++)txt(k%2?'♪':'♥',560+k*60,1000-k*40-(k%2)*30,40+k*4,k%2?'#7C3AED':'#F472B6',null);g.restore()}
window.makeS=function(){rbScene(10.0)};
window.makeH=function(){const t=10.0;sky('#7DD3FC','#E0F2FE');
  title3d('ROCK-A-BYE',290,150,80,'#FFB3D9','#DB2777',18,'#831843');
  title3d('BABY',290,300,130,'#FFE26B','#F59E0B',22,'#7C2D12');
  g.save();g.translate(290,450);rr(-220,-42,440,84,42,'#DB2777');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Lullaby Rhyme 🌙',0,2,42,'#fff',null);g.restore();
  for(let k=0;k<5;k++)txt(k%2?'♪':'♥',120+k*90,560+(k%2)*24,46,k%2?'#7C3AED':'#F472B6',null);
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=10.0;rbScene(t);
  title3d('ROCK-A-BYE',540,240,140,'#FFB3D9','#DB2777',26,'#831843');
  title3d('BABY 🌙',540,420,160,'#FFE26B','#F59E0B',26,'#7C2D12');
  g.save();g.translate(540,580);rr(-280,-50,560,100,50,'#DB2777');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Lullaby Rhyme 💖',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
