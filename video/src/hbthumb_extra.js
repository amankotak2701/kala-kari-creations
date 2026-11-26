function miniBubble(x,y,sc,t,n){g.save();g.translate(x,y);g.scale(sc,sc);g.translate(-540,-850);giftBubble(540,850,230,t,()=>drawGift(n,540,850,t,0,1),1);g.restore()}
window.makeH=function(){const t=20.0;const w=g.createLinearGradient(0,0,0,H);w.addColorStop(0,'#312E81');w.addColorStop(1,'#6D28D9');g.fillStyle=w;g.fillRect(0,0,W,H);
  for(let k=0;k<80;k++){g.globalAlpha=.3+.7*rnd(k+3);ell(rnd(k)*W,rnd(k+50)*H,2,2,'#FFF6D5')}g.globalAlpha=1;
  g.fillStyle='#7C2D12';g.fillRect(0,620,W,100);ell(1000,680,260,40,'#F9A8D4');
  moonFace(1200,90,55,t,0,0);
  adult('mom',780,712,{s:.55,t,pose:'sway',happy:1});cradle(1050,650,.62,t,{});
  miniBubble(920,230,.55,t,'bird');miniBubble(1160,330,.38,t,'ring');
  title3d('HUSH',290,130,120,'#FBCFE8','#F472B6',20,'#831843');
  title3d('LITTLE',290,265,110,'#FFE26B','#F59E0B',20,'#7C2D12');
  title3d('BABY 👶',300,395,110,'#FFFFFF','#E0E7FF',20,'#3730A3');
  g.save();g.translate(290,525);rr(-210,-42,420,84,42,'#DB2777');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Lullaby 🌙',0,2,46,'#fff',null);g.restore();
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=20.0;nursery(t);adult('mom',200,1810,{s:1.2,t,pose:'sway',happy:1});cradle(700,1680,1.3,t,{});
  miniBubble(560,880,.95,t,'bird');miniBubble(880,1170,.45,t,'ring');miniBubble(250,1150,.42,t,'dog');
  title3d('HUSH LITTLE',540,240,140,'#FBCFE8','#F472B6',26,'#831843');
  title3d('BABY 👶',540,420,160,'#FFE26B','#F59E0B',28,'#7C2D12');
  g.save();g.translate(540,580);rr(-260,-50,520,100,50,'#DB2777');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Lullaby 🌙',0,2,56,'#fff',null);g.restore();
  popcornLogo(975,1830,.22,0)};
