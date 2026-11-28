function fdScene(t){g.save();g.translate(540,1700);g.scale(1.25,1.25);g.translate(-540,-1680);dell(t);ring(t,false);
  member(4,230,1690,t,{dir:1});member(0,560,1700,t,{pose:'up'});member(6,880,1720,t,{dir:-1});member(5,420,1790,t,{dir:1});member(7,200,1800,t,{dir:1});member(8,700,1785,t,{});
  g.restore()}
window.makeS=function(){fdScene(10.0)};
window.makeH=function(){const t=10.0;sky('#7DD3FC','#E0F2FE');
  title3d('THE FARMER',290,150,84,'#7CF29A','#16A34A',18,'#14532D');
  title3d('IN THE DELL',290,290,84,'#FFE26B','#F59E0B',18,'#7C2D12');
  g.save();g.translate(290,430);rr(-230,-42,460,84,42,'#16A34A');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Circle Game Song',0,2,40,'#fff',null);g.restore();
  ['👨‍🌾','🐄','🐶','🐱','🐭','🧀'].forEach((e,i)=>{g.save();g.translate(80+i*84,550);ell(0,0,38,38,'#fff');g.lineWidth=5;g.strokeStyle='#16A34A';g.beginPath();g.arc(0,0,38,0,7);g.stroke();txt(e,0,3,44,null,null);g.restore()});
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=10.0;fdScene(t);
  title3d('THE FARMER',540,240,140,'#7CF29A','#16A34A',26,'#14532D');
  title3d('IN THE DELL',540,420,140,'#FFE26B','#F59E0B',26,'#7C2D12');
  g.save();g.translate(540,590);rr(-300,-50,600,100,50,'#16A34A');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Circle Game Song',0,2,52,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
