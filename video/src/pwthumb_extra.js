function pwScene(t){g.save();g.translate(540,1720);g.scale(1.3,1.3);g.translate(-540,-1720);pwGarden(t);
  mulberryBush(540,1720,.95,t);g.save();g.beginPath();g.rect(0,0,W,1560);g.clip();weasel(560,1560,1.05,t,{stretch:1.2,wave:1});g.restore();
  monkey(240,1830,1.05,t,{dir:1,surprised:1,up:1});
  g.save();g.translate(770,1250);g.fillStyle='#FDE047';g.beginPath();for(let k=0;k<24;k++){const a=k/24*Math.PI*2,r=(k%2?80:150);g.lineTo(Math.cos(a)*r,Math.sin(a)*r)}g.closePath();g.fill();g.lineWidth=7;g.strokeStyle='#F43F5E';g.stroke();g.rotate(-.12);txt('POP!',0,6,76,'#fff','#F43F5E');g.restore();
  g.restore()}
window.makeS=function(){pwScene(10.0)};
window.makeH=function(){const t=10.0;sky('#7DD3FC','#E0F2FE');
  title3d('POP GOES',290,170,100,'#FF9FB2','#E11D48',20,'#881337');
  title3d('THE WEASEL',290,310,84,'#FFE26B','#F59E0B',20,'#7C2D12');
  g.save();g.translate(290,450);rr(-230,-42,460,84,42,'#E11D48');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme',0,2,42,'#fff',null);g.restore();
  for(let k=0;k<7;k++)ell(110+k*60,560+(k%2)*22,16,18,k%2?'#6D28D9':'#9333EA');
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=10.0;pwScene(t);
  title3d('POP GOES',540,240,160,'#FF9FB2','#E11D48',26,'#881337');
  title3d('THE WEASEL',540,420,140,'#FFE26B','#F59E0B',26,'#7C2D12');
  g.save();g.translate(540,590);rr(-260,-50,520,100,50,'#E11D48');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
