function rrScene(t){g.save();g.translate(540,1700);g.scale(1.3,1.3);g.translate(-540,-1700);riverScene(t,{});rrDucks(t,780);
  rowBoat(540,1650,1.0,t,{per:RRB,riders:[0,1,2],cheer:1,col:'#EF4444'});puppy(760,1580,.55,t,20);
  g.restore()}
window.makeS=function(){rrScene(10.0)};
window.makeH=function(){const t=10.0;sky('#7DD3FC','#E0F2FE');
  title3d('ROW, ROW, ROW',290,155,64,'#7DD3FC','#0284C7',18,'#0C4A6E');
  title3d('YOUR BOAT',290,290,100,'#FFE26B','#F59E0B',20,'#7C2D12');
  g.save();g.translate(290,435);rr(-230,-42,460,84,42,'#0284C7');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme',0,2,42,'#fff',null);g.restore();
  for(let k=0;k<6;k++){g.strokeStyle='#38BDF8';g.lineWidth=7;g.beginPath();g.arc(90+k*80,560,30,Math.PI*1.15,Math.PI*1.85);g.stroke()}
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=10.0;rrScene(t);
  title3d('ROW, ROW, ROW',540,240,130,'#7DD3FC','#0284C7',24,'#0C4A6E');
  title3d('YOUR BOAT',540,420,160,'#FFE26B','#F59E0B',26,'#7C2D12');
  g.save();g.translate(540,590);rr(-260,-50,520,100,50,'#0284C7');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
