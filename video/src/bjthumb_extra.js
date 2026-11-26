function bigZ(x,y,s){[[0,0,1],[50,-70,.75],[90,-130,.55]].forEach(([dx,dy,k])=>txt('Z',x+dx*s,y+dy*s,90*s*k,'#C7D2FE','#4338CA'))}
window.makeH=function(){const t=20.3;const w=g.createLinearGradient(0,0,0,H);w.addColorStop(0,'#FDE7C7');w.addColorStop(1,'#F9C98A');g.fillStyle=w;g.fillRect(0,0,W,H);
  for(let k=0;k<14;k++)for(let j=0;j<6;j++){g.globalAlpha=.08;ell(40+k*95+(j%2)*45,40+j*120,12,12,'#B45309')}g.globalAlpha=1;
  g.fillStyle='#A16207';g.fillRect(0,600,W,120);
  johnInBed(930,600,.72,t,'sleep');bigZ(760,330,1.2);
  sister(1210,700,.7,t,{trunk:1});g.save();g.translate(1110,300);g.rotate(.15);g.scale(.32,.32);clockFace(0,0,1,t);g.restore();txt('RIIING!',1110,170,44,'#fff','#DC2626');
  g.save();g.translate(640,120);bell(0,0,.9,.35);g.restore();txt('DING DONG!',660,230,40,'#FDE047','#B45309');
  title3d('ARE YOU',290,130,104,'#60A5FA','#1D4ED8',20,'#1E3A8A');
  title3d('SLEEPING?',290,265,104,'#FFE26B','#F59E0B',20,'#7C2D12');
  title3d('Brother John',290,395,72,'#FFFFFF','#E0E7FF',16,'#1E3A8A');
  g.save();g.translate(290,515);rr(-220,-42,440,84,42,'#0EA5E9');g.lineWidth=6;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 🔔',0,2,44,'#fff',null);g.restore();
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=20.3;bedroom(t,1);johnInBed(560,1560,1.3,t,'sleep');bigZ(300,1180,1.5);
  sister(900,1800,1.1,t,{trunk:1});g.save();g.translate(880,1180);g.rotate(.15);g.scale(.55,.55);clockFace(0,0,1,t);g.restore();txt('RIIING! ⏰',760,1010,60,'#fff','#DC2626');
  title3d('ARE YOU SLEEPING?',540,250,104,'#FFE26B','#F59E0B',22,'#7C2D12');
  title3d('Brother John',540,410,120,'#60A5FA','#1D4ED8',22,'#1E3A8A');
  g.save();g.translate(540,560);rr(-280,-50,560,100,50,'#0EA5E9');g.lineWidth=7;g.strokeStyle='#FDE047';g.stroke();txt('Nursery Rhyme 🔔',0,2,54,'#fff',null);g.restore();
  popcornLogo(110,110,.26,0)};
