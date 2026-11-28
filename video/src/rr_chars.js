// ---- "Row, Row, Row Your Boat" helpers ----
function rowBoat(x,y,s,t,o={}){const ph=o.ph??(t*Math.PI*2/(o.per||2.2));g.save();g.translate(x,y+Math.sin(t*2)*6);g.rotate(Math.sin(t*1.6)*.03);g.scale(s,s);
  // kids sit in the boat (drawn before hull so the hull hides their legs)
  (o.riders||[0,1]).forEach((k,i)=>{const kx=-90+i*170;g.save();g.translate(kx,-40);kid(k,0,0,{s:.78,t,happy:1,noHat:1,noScarf:1,dir:1,trunk:o.cheer?1:.3});g.restore()});
  // oars
  [-1,1].forEach(d=>{const a=Math.sin(ph)*.5;g.save();g.translate(d*40,-150);g.rotate(d*(.9+a)+(d>0?0:Math.PI)*0);g.restore()});
  const oar=(px,dir)=>{const a=Math.sin(ph)*.55;g.save();g.translate(px,-110);g.rotate(dir*(1.05+a));rr(-7,0,14,230,7,'#92400E');ell(0,240,20,40,'#B45309');g.restore()};
  oar(-120,1);oar(140,-1);
  // hull
  g.fillStyle=o.col||'#EF4444';g.beginPath();g.moveTo(-260,-70);g.lineTo(260,-70);g.quadraticCurveTo(230,40,150,60);g.lineTo(-150,60);g.quadraticCurveTo(-230,40,-260,-70);g.closePath();g.fill();
  rr(-270,-84,540,26,12,'#FDE047');g.fillStyle='#fff';for(let k=0;k<5;k++)ell(-170+k*85,-10,18,18,'rgba(255,255,255,.85)');
  if(o.name)txt(o.name,0,30,34,'#fff',null);
  g.restore()}
function riverScene(t,o={}){const night=o.night||0,sc=o.scroll??t*60;
  sky(night?'#1E1B4B':(o.sunset?'#F472B6':'#7DD3FC'),night?'#6D28D9':(o.sunset?'#FDBA74':'#E0F2FE'));
  if(night){for(let k=0;k<50;k++){g.globalAlpha=.4+.6*Math.abs(Math.sin(t*1.5+k));ell(rnd(k)*W,520+rnd(k+5)*600,2.5,2.5,'#fff')}g.globalAlpha=1;moonFace(820,900,60,t,0,0)}
  else mandalaSun(830,900,58,t);
  cloud(((t*12)%1500)-300,980,.7);cloud(((t*8+700)%1500)-300,1110,.55);
  hills(t,night?'#4C1D95':(o.snow?'#E0F2FE':'#A3E635'),night?'#3B0764':(o.snow?'#BAE6FD':'#84CC16'),night?'#2E1065':(o.snow?'#93C5FD':'#65A30D'));
  // far bank with trees scrolling
  g.fillStyle=o.snow?'#F8FAFC':(night?'#166534':'#4ADE80');g.fillRect(0,1340,W,120);
  for(let k=0;k<8;k++){const x=((k*190-sc*.5)%1520+1520)%1520-200;if(o.snow){g.fillStyle='#15803D';g.beginPath();g.moveTo(x,1250);g.lineTo(x-50,1360);g.lineTo(x+50,1360);g.fill();ell(x,1262,20,10,'#fff')}else folkTree(x,1380,.45,t,k)}
  // water
  const wg=g.createLinearGradient(0,1440,0,H);wg.addColorStop(0,night?'#1E3A8A':'#38BDF8');wg.addColorStop(1,night?'#172554':'#0369A1');g.fillStyle=wg;g.fillRect(0,1440,W,H-1440);
  for(let r=0;r<6;r++)for(let k=0;k<7;k++){const x=((k*200+r*90-sc*(.6+r*.15))%1400+1400)%1400-150,y=1490+r*75;g.strokeStyle='rgba(255,255,255,.45)';g.lineWidth=5;g.beginPath();g.arc(x,y,28,Math.PI*1.15,Math.PI*1.85);g.stroke()}
  // near bank reeds
  for(let k=0;k<10;k++){const x=((k*130-sc)%1300+1300)%1300-100;g.strokeStyle='#15803D';g.lineWidth=8;g.beginPath();g.moveTo(x,H);g.quadraticCurveTo(x+10,H-90,x+Math.sin(t*2+k)*10,H-150);g.stroke();ell(x+Math.sin(t*2+k)*10,H-160,10,24,'#92400E')}}
function croc(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);const C='#16A34A',D='#15803D';
  const op=o.open?.35+Math.abs(Math.sin(t*6))*.25:.05;
  ell(0,0,200,50,C);for(let k=0;k<6;k++){g.fillStyle=D;g.beginPath();g.moveTo(-150+k*55,-40);g.lineTo(-130+k*55,-70);g.lineTo(-110+k*55,-40);g.fill()}
  g.save();g.translate(170,-10);g.rotate(-op);rr(0,-30,190,34,16,C);g.fillStyle='#fff';for(let k=0;k<6;k++){g.beginPath();g.moveTo(20+k*28,4);g.lineTo(32+k*28,16);g.lineTo(44+k*28,4);g.fill()}g.restore();
  g.save();g.translate(170,-10);g.rotate(op*.4);rr(0,0,180,28,14,D);g.restore();
  ell(190,-48,26,24,C);ell(196,-52,14,14,'#fff');ell(200,-52,7,9,'#1F2937');ell(340,-30,8,5,'#14532D');g.restore()}
function lionC(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);
  for(let k=0;k<14;k++){const a=k/14*Math.PI*2;ell(Math.cos(a)*92,-180+Math.sin(a)*92,40,40,k%2?'#B45309':'#D97706')}
  ell(0,-60,90,70,'#F59E0B');ell(0,-180,80,76,'#FBBF24');ell(-25,-195,9,12,'#1F2937');ell(25,-195,9,12,'#1F2937');ell(0,-160,16,11,'#7C2D12');
  if(o.roar)ell(0,-128,30,28,'#7F1D1D');else{g.strokeStyle='#7C2D12';g.lineWidth=5;g.beginPath();g.arc(0,-150,16,.2,Math.PI-.2);g.stroke()}g.restore()}
function polarBear(x,y,s,t,o={}){g.save();g.translate(x,y+(o.shiver?Math.sin(t*60)*3:0));g.scale(s,s);const C='#F8FAFC';
  ell(0,-80,110,90,C);ell(-60,-10,34,24,C);ell(60,-10,34,24,C);ell(0,-200,72,64,C);ell(-50,-250,22,22,C);ell(50,-250,22,22,C);ell(0,-176,34,26,'#E2E8F0');
  ell(-24,-214,8,10,'#1F2937');ell(24,-214,8,10,'#1F2937');ell(0,-188,12,9,'#1F2937');
  if(o.shiver){rr(-80,-150,160,26,12,'#EF4444');for(let k=0;k<3;k++)txt('❄',-120+k*120,-300-((t*60+k*20)%60),36,'#BAE6FD',null)}
  g.restore()}
