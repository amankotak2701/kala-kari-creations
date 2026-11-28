function omScene(t){g.save();g.translate(540,1720);g.scale(1.45,1.45);g.translate(-540,-1800);oBg(t,0);grandpaHouse(820,1720,.6,t);
  oldMan(380,1800,1.0,t,{pose:'up',skate:1});for(let j=0;j<4;j++){g.save();g.globalAlpha=.8;g.strokeStyle='#fff';g.lineWidth=6;g.beginPath();g.moveTo(200-j*30,1560+j*60);g.lineTo(280-j*30,1560+j*60);g.stroke();g.restore()}
  puppy(620,1840,.95,t,60);bone(735,1698,.42,0);g.restore()}
window.makeS=function(){omScene(10.0)};
window.makeH=function(){const t=10.0;sky('#7DD3FC','#E0F2FE');
  title3d('THIS OLD',290,150,104,'#FFD08A','#EA580C',20,'#7C2D12');
  title3d('MAN',290,300,140,'#FFE26B','#F59E0B',22,'#7C2D12');
  g.save();g.translate(290,450);rr(-230,-42,460,84,42,'#EA580C');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Count 1 to 10! 🔢',0,2,42,'#fff',null);g.restore();
  bone(170,570,.8,-.2);txt('🐶',300,575,70,null,null);g.save();g.translate(420,575);ell(0,0,46,46,'#FDE047');g.lineWidth=6;g.strokeStyle='#EA580C';g.beginPath();g.arc(0,0,46,0,7);g.stroke();txt('10',0,-2,48,'#EA580C',null);g.restore();
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=10.0;omScene(t);
  title3d('THIS OLD',540,240,160,'#FFD08A','#EA580C',26,'#7C2D12');
  title3d('MAN 👴',540,430,170,'#FFE26B','#F59E0B',26,'#7C2D12');
  g.save();g.translate(540,600);rr(-290,-50,580,100,50,'#EA580C');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Count 1 to 10! 🔢',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
