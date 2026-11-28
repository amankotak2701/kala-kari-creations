function ttScene(t){g.save();g.translate(540,1450);g.scale(1.35,1.35);g.translate(-540,-1560);park(t);
  girlWithBasket(360,1760,1.0,t,{trunk:1});boy(790,1770,.95,t,{dir:-1,trunk:1});
  g.save();g.translate(580,1350);envelope(0,0,1.0,-.25);g.restore();for(let k=0;k<4;k++){g.strokeStyle='rgba(255,255,255,.9)';g.lineWidth=6;g.beginPath();g.moveTo(420-k*20,1300+k*30);g.lineTo(500-k*20,1300+k*30);g.stroke()}
  for(let k=0;k<5;k++)txt('♥',520+k*30,1230-k*25-(k%2)*20,34+k*4,'#F472B6',null);g.restore()}
window.makeS=function(){ttScene(10.0)};
window.makeH=function(){const t=10.0;sky('#7DD3FC','#E0F2FE');
  title3d('A TISKET,',300,135,100,'#7CF29A','#16A34A',20,'#14532D');
  title3d('A TASKET',300,275,100,'#FFE26B','#F59E0B',20,'#7C2D12');
  g.save();g.translate(300,410);basketG(0,40,.9,t,{full:0});g.restore();
  g.save();g.translate(300,555);rr(-230,-42,460,84,42,'#16A34A');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 💌',0,2,44,'#fff',null);g.restore();
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=10.0;ttScene(t);
  title3d('A TISKET,',540,240,150,'#7CF29A','#16A34A',26,'#14532D');
  title3d('A TASKET 🧺',540,420,150,'#FFE26B','#F59E0B',26,'#7C2D12');
  g.save();g.translate(540,580);rr(-280,-50,560,100,50,'#16A34A');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 💌',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
