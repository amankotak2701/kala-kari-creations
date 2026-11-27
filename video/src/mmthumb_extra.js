window.makeH=function(){const t=24.0;sky('#FBCFE8','#FEF3C7');for(let k=0;k<30;k++){g.save();g.translate(rnd(k)*W,rnd(k+3)*H);g.rotate(rnd(k+5)*3);rr(-9,-3,18,6,3,['#EF4444','#FDE047','#22C55E','#3B82F6','#EC4899'][k%5]);g.restore()}
  g.save();g.translate(640,40);g.scale(.62,.62);g.translate(-140,-470);bakery(t,{door:1});g.restore();
  g.fillStyle='#D1D5DB';g.fillRect(0,640,W,80);
  muffinMan(1060,712,.6,t,{});
  muffin(700,712,.75,t,Object.assign({},MUFS[0]));muffin(820,716,.62,t,Object.assign({},MUFS[1]));muffin(1220,716,.6,t,Object.assign({},MUFS[2]));
  title3d('THE',290,110,90,'#FFFFFF','#FCE7F3',18,'#831843');
  title3d('MUFFIN',290,240,120,'#FF6FAE','#DB2777',20,'#831843');
  title3d('MAN 🧁',300,380,120,'#FFE26B','#F59E0B',20,'#7C2D12');
  g.save();g.translate(290,515);rr(-220,-42,440,84,42,'#7C2D12');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme',0,2,44,'#fff',null);g.restore();
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=24.0;drury(t,{door:1});
  muffinMan(560,1820,1.3,t,{});
  muffin(180,1850,.9,t,Object.assign({hop:0},MUFS[0]));muffin(340,1880,.75,t,MUFS[1]);muffin(880,1860,.85,t,MUFS[2]);
  title3d('THE MUFFIN',540,240,140,'#FF6FAE','#DB2777',26,'#831843');
  title3d('MAN 🧁',540,420,160,'#FFE26B','#F59E0B',28,'#7C2D12');
  g.save();g.translate(540,575);rr(-280,-50,560,100,50,'#7C2D12');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme',0,2,56,'#fff',null);g.restore();
  popcornLogo(110,110,.26,0)};
