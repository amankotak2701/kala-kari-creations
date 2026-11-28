function slScene(t){g.save();g.translate(540,1770);g.scale(1.4,1.4);g.translate(-540,-1840);farmBg(t,{noSun:1});g.fillStyle='#22C55E';g.fillRect(-200,1900,1500,300);for(let k=0;k<6;k++)marigold(80+k*180,1950,.75,['#F472B6','#FBBF24','#F87171'][k%3]);
  wagon(760,1810,.65,t,{col:'#3B82F6'});slKids(t,3,1840,{x0:420,s:.9,sp:175,cheer:1,h:60});puppy(745,1735,.55,t,10);
  for(let j=0;j<5;j++)txt(j%2?'♫':'♪',260+j*120,1420-(j%2)*50,56,['#FDE047','#F472B6','#60A5FA'][j%3],null);g.restore()}
window.makeS=function(){slScene(10.2)};
window.makeH=function(){const t=10.0;sky('#7DD3FC','#E0F2FE');
  title3d('SKIP TO',290,160,110,'#FF9FD0','#DB2777',20,'#831843');
  title3d('MY LOU',290,315,120,'#FFE26B','#F59E0B',22,'#7C2D12');
  g.save();g.translate(290,460);rr(-230,-42,460,84,42,'#DB2777');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme',0,2,42,'#fff',null);g.restore();
  ['🪰','🐱','🐄','🖌️','🤠','💕'].forEach((e,i)=>{g.save();g.translate(80+i*84,575);ell(0,0,36,36,'#fff');g.lineWidth=5;g.strokeStyle='#DB2777';g.beginPath();g.arc(0,0,36,0,7);g.stroke();txt(e,0,3,40,null,null);g.restore()});
  popcornLogo(70,665,.13,0)};
window.makeV=function(){const t=10.2;slScene(t);
  title3d('SKIP TO',540,250,170,'#FF9FD0','#DB2777',26,'#831843');
  title3d('MY LOU',540,450,180,'#FFE26B','#F59E0B',28,'#7C2D12');
  g.save();g.translate(540,630);rr(-260,-50,520,100,50,'#DB2777');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
