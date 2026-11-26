window.makeH=function(){const t=59.0;sky('#60B8F0','#D6EEFF');mandalaSun(1180,110,55,t);cloud(560,120,.8);cloud(900,200,.6);
  for(let k=0;k<9;k++){const bx=440+k*100,hgt=150+rnd(k)*170;rr(bx,560-hgt,88,hgt+20,6,['#93C5FD','#C4B5FD','#FCA5A5','#86EFAC','#FDE68A'][k%5]);for(let r=0;r<Math.floor(hgt/45);r++)for(let c=0;c<2;c++)rr(bx+14+c*36,560-hgt+14+r*45,22,26,3,'rgba(255,255,255,.7)')}
  g.fillStyle='#86EFAC';g.fillRect(0,560,W,40);rr(0,595,W,125,0,'#4B5563');g.fillStyle='#FDE047';for(let k=0;k<8;k++)g.fillRect(k*170,655,90,10);
  bus(890,700,.62,t,{wheelRot:.5,wave:1,kidsJump:0});
  g.save();g.globalAlpha=.95;const gr=g.createLinearGradient(0,0,560,0);gr.addColorStop(0,'rgba(255,255,255,.0)');g.restore();
  title3d('THE WHEELS',300,140,104,'#FFE26B','#F59E0B',20,'#7C2D12');
  title3d('ON THE BUS',300,280,104,'#FF4D5E','#C1121F',20);
  g.save();g.translate(300,410);rr(-240,-42,480,84,42,'#2563EB');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('Nursery Rhyme 🚌',0,2,46,'#fff',null);g.restore();
  popcornLogo(70,655,.14,0)};
window.makeV=function(){const t=59.0;townBg(t,900,{rainbow:1});bus(540,1560,1.0,t,{wheelRot:.5,wave:1});
  title3d('THE WHEELS',540,330,150,'#FFE26B','#F59E0B',26,'#7C2D12');
  title3d('ON THE BUS',540,520,150,'#FF4D5E','#C1121F',26);
  g.save();g.translate(540,690);rr(-300,-50,600,100,50,'#2563EB');g.lineWidth=7;g.strokeStyle='#fff';g.stroke();txt('Nursery Rhyme 🚌',0,2,54,'#fff',null);g.restore();
  popcornLogo(110,110,.26,0)};
