function clockGroup(s,dx,dy,t){g.save();g.translate(dx,dy);g.scale(s,s);grandfatherClock(t,1,.6);mouse(CX+60,598,1.4,t,{});birdie(CX-150,600,1.3,t,{});bee(CX+300,700,1.3,t,{dir:-1});
  txt('DONG!',CX-330,820,80,'#FDE047','#7C2D12');txt('DONG!',CX+330,980,80,'#FDE047','#7C2D12');g.restore()}
window.makeH=function(){const t=10.0;const w=g.createLinearGradient(0,0,0,H);w.addColorStop(0,'#C4B5FD');w.addColorStop(1,'#8B5CF6');g.fillStyle=w;g.fillRect(0,0,W,H);
  for(let k=0;k<14;k++){g.fillStyle='rgba(255,255,255,.12)';g.fillRect(k*100,0,40,H)}
  g.fillStyle='#A16207';g.fillRect(0,640,W,80);
  clockGroup(.4,960-540*.4,712-1710*.4,t);
  puppy(700,712,.7,t,0);hen(1200,712,.55,t,{dir:-1});
  title3d('HICKORY',290,140,110,'#FFE26B','#F59E0B',20,'#7C2D12');
  title3d('DICKORY',290,280,110,'#FF4D5E','#C1121F',20);
  title3d('DOCK 🕰️',290,420,104,'#7CF29A','#16A34A',20,'#0B3D1E');
  g.save();g.translate(290,560);rr(-220,-42,440,84,42,'#7C3AED');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 🐭',0,2,44,'#fff',null);g.restore();
  popcornLogo(1210,70,.14,0)};
window.makeV=function(){const t=10.0;hRoom(t);
  clockGroup(.85,540-540*.85,1880-1710*.85,t);
  puppy(130,1880,1.0,t,0);hen(930,1880,.85,t,{dir:-1});
  title3d('HICKORY DICKORY',540,250,118,'#FFE26B','#F59E0B',22,'#7C2D12');
  title3d('DOCK 🕰️',540,430,170,'#FF4D5E','#C1121F',28);
  g.save();g.translate(540,590);rr(-300,-50,600,100,50,'#7C3AED');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 🐭🐦🐝',0,2,52,'#fff',null);g.restore();
  popcornLogo(110,110,.26,0)};
