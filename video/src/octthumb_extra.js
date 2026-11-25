const FULL={garland:1,ornaments:1,lights:1,lightsOn:1,star:1};
function nightBokeh(){const gr=g.createRadialGradient(W*.6,H*.45,30,W*.5,H*.5,Math.max(W,H)*.85);gr.addColorStop(0,'#4B3B8F');gr.addColorStop(.6,'#2A1E6B');gr.addColorStop(1,'#0B0A2E');g.fillStyle=gr;g.fillRect(0,0,W,H);
  for(let k=0;k<45;k++){g.globalAlpha=.1+.18*rnd(k);ell(rnd(k+1)*W,rnd(k+2)*H,18+rnd(k+3)*50,18+rnd(k+3)*50,['#FDE68A','#FCA5A5','#A5F3FC','#FFFFFF'][k%4])}g.globalAlpha=1}
function treeGroup(sc,dx,dy,t,kidY){g.save();g.translate(dx,dy);g.scale(sc,sc);
  ell(540,1700,560,90,'rgba(255,255,255,.9)');bigTree(t,FULL);present(380,1690,130,100,'#DC2626','#FDE68A');present(700,1695,120,90,'#22C55E','#fff');present(560,1720,100,75,'#3B82F6','#F9A8D4');
  [[0,150],[1,300],[3,780],[2,930]].forEach(([k,x],i)=>kid(k,x,kidY,{s:.95,dir:x<540?1:-1,t,happy:1,trunk:1}));puppy(470,1760,.55,t,0);
  g.fillStyle='rgba(8,8,35,.22)';g.fillRect(-2000,-2000,6000,6000);treeGlow(t,FULL);g.restore()}
window.makeH=function(){const t=118.3;nightBokeh();flakes(60,4);
  treeGroup(.55,930-540*.55,705-1780*.55,t,1700);
  txt('Sing along! 🎶',300,120,52,'#FFFFFF','#3B0A45');
  title3d('O CHRISTMAS',300,240,104,'#FF4D5E','#C1121F',18);
  title3d('TREE 🎄',300,385,140,'#7CF29A','#16A34A',22,'#0B3D1E');
  g.save();g.translate(300,530);rr(-250,-42,500,84,42,'#F5C542');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('Kids Christmas Carol',0,2,44,'#7C1D1D',null);g.restore();
  popcornLogo(70,650,.15,0)};
window.makeV=function(){const t=118.3;nightBokeh();flakes(110,8);
  treeGroup(.92,540-540*.92,1890-1780*.92,t,1700);
  title3d('O CHRISTMAS',540,250,150,'#FF4D5E','#C1121F',26);
  title3d('TREE 🎄',540,440,190,'#7CF29A','#16A34A',30,'#0B3D1E');
  g.save();g.translate(540,600);rr(-300,-48,600,96,48,'#F5C542');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('Kids Christmas Carol 🎶',0,2,48,'#7C1D1D',null);g.restore();
  popcornLogo(110,110,.26,0)};
