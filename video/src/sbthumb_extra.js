function sbScene(t){g.save();g.translate(540,1770);g.scale(1.3,1.3);g.translate(-540,-1840);springGarden(t,{petals:1});rainbow(1);
  g.fillStyle='rgba(253,230,138,.6)';g.beginPath();g.ellipse(540,1820,470,150,0,0,Math.PI*2);g.fill();
  SBM.filter(m=>m.y<1800).forEach(m=>sbMember(m,t,0));SBM.filter(m=>m.y>=1800).forEach(m=>sbMember(m,t,0));
  for(let j=0;j<6;j++)txt(j%2?'♫':'♪',200+j*130,1330-(j%2)*50,56,['#FDE047','#F472B6','#60A5FA'][j%3],null);g.restore()}
window.makeS=function(){sbScene(115.3)};
window.makeH=function(){const t=115.3;sky('#7DD3FC','#E0F2FE');
  title3d('SPRING TIME',290,150,82,'#FF9FD0','#DB2777',18,'#831843');
  title3d('FAMILY BAND',290,290,82,'#FFE26B','#F59E0B',18,'#7C2D12');
  g.save();g.translate(290,430);rr(-230,-42,460,84,42,'#16A34A');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Kids Music Song',0,2,42,'#fff',null);g.restore();
  ['🥁','🎸','🎺','🪇','🌸','🌈'].forEach((e,i)=>{g.save();g.translate(80+i*84,555);ell(0,0,36,36,'#fff');g.lineWidth=5;g.strokeStyle='#DB2777';g.beginPath();g.arc(0,0,36,0,7);g.stroke();txt(e,0,3,40,null,null);g.restore()});
  popcornLogo(70,665,.13,0)};
window.makeV=function(){const t=115.3;sbScene(t);
  title3d('SPRING TIME',540,240,130,'#FF9FD0','#DB2777',24,'#831843');
  title3d('FAMILY BAND',540,410,130,'#FFE26B','#F59E0B',24,'#7C2D12');
  g.save();g.translate(540,570);rr(-270,-50,540,100,50,'#16A34A');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Kids Music Song',0,2,54,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
