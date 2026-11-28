// ---- "Spring Time Family Band" helpers ----
function drumKit(x,y,s,t,hit){g.save();g.translate(x,y);g.scale(s,s);
  rr(-90,-150,180,150,20,'#DC2626');ell(0,-150,90,24,'#FEF2F2');g.strokeStyle='#FDE047';g.lineWidth=6;for(let k=0;k<5;k++){g.beginPath();g.moveTo(-80+k*40,-140);g.lineTo(-60+k*40,-10);g.stroke()}
  ell(0,-6,90,18,'#991B1B');const h=hit?Math.max(0,Math.cos(t*Math.PI*2/.6185)):0;
  [-1,1].forEach(d=>{g.save();g.translate(d*60,-170-h*30);g.rotate(d*(.5-h*.4));rr(-5,-90,10,90,5,'#FCD34D');ell(0,-92,9,9,'#FCD34D');g.restore()});g.restore()}
function guitar(x,y,s,t,rot=-.6){g.save();g.translate(x,y);g.rotate(rot+Math.sin(t*4)*.05);g.scale(s,s);
  ell(0,40,70,60,'#F59E0B');ell(0,-30,52,48,'#F59E0B');ell(0,10,20,20,'#78350F');rr(-12,-220,24,190,6,'#78350F');rr(-18,-250,36,40,8,'#92400E');
  g.strokeStyle='#FEF3C7';g.lineWidth=2;for(let k=-1;k<=1;k++){g.beginPath();g.moveTo(k*6,-240);g.lineTo(k*6,70);g.stroke()}g.restore()}
function trumpet(x,y,s,t,rot=0){g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);rr(0,-10,160,20,8,'#FACC15');g.fillStyle='#FACC15';g.beginPath();g.moveTo(150,-12);g.lineTo(220,-45);g.lineTo(220,45);g.lineTo(150,12);g.fill();
  rr(40,-40,60,30,10,'#EAB308');for(let k=0;k<3;k++)rr(48+k*18,-56,8,20,3,'#CA8A04');g.restore()}
function xylophone(x,y,s,t,hit){g.save();g.translate(x,y);g.scale(s,s);const C=['#EF4444','#F97316','#FACC15','#22C55E','#3B82F6','#8B5CF6'];
  rr(-170,-20,340,20,6,'#92400E');C.forEach((c,i)=>{const hh=110-i*12,b=hit&&Math.floor(t/.309)%6===i?-8:0;rr(-160+i*56,-20-hh+b,48,hh,8,c)});
  const i=Math.floor(t/.309)%6;g.save();g.translate(-136+i*56,-150);g.rotate(-.5);rr(-4,-80,8,80,4,'#FCD34D');ell(0,-84,12,12,'#F472B6');g.restore();g.restore()}
function tambourine(x,y,s,t){g.save();g.translate(x,y+Math.sin(t*10)*8);g.rotate(Math.sin(t*10)*.3);g.scale(s,s);ell(0,0,60,60,'#F472B6');ell(0,0,46,46,'#FEF3C7');for(let k=0;k<6;k++){const a=k/6*Math.PI*2;ell(Math.cos(a)*54,Math.sin(a)*54,12,8,'#FACC15')}g.restore()}
function springGarden(t,o={}){sky('#7DD3FC','#E0F2FE');mandalaSun(830,1000,58,t);cloud(((t*12)%1500)-300,1060,.7);cloud(((t*8+700)%1500)-300,1180,.55);
  hills(t,'#A3E635','#84CC16','#65A30D');g.fillStyle='#4ADE80';g.fillRect(-300,1500,W+600,900);
  for(let k=0;k<3;k++)blossomTree(120+k*420,1520,.8,t);
  for(let k=0;k<14;k++){const x=40+rnd(k)*1000,y=1560+rnd(k+3)*340;tulip(x,y,.8,['#F472B6','#FBBF24','#F87171','#A78BFA'][k%4],t+k)}
  if(o.petals)for(let k=0;k<20;k++){const p=((t*.15+rnd(k))%1);g.save();g.translate(rnd(k+9)*W+Math.sin(t+k)*60,600+p*1300);g.rotate(t+k);ell(0,0,12,7,'#FBCFE8');g.restore()}}
function blossomTree(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);rr(-22,-260,44,260,12,'#7C4A1E');
  [[0,-330,130],[-110,-280,90],[110,-280,90],[-60,-400,90],[70,-400,90]].forEach(([a,b,r])=>ell(a,b,r,r*.85,'#F9A8D4'));
  for(let k=0;k<14;k++)ell(-140+rnd(k)*280,-440+rnd(k+4)*220,9,9,'#FDF2F8');g.restore()}
function tulip(x,y,s,c,t){g.save();g.translate(x,y);g.scale(s,s);g.rotate(Math.sin(t*1.5)*.08);g.strokeStyle='#16A34A';g.lineWidth=6;g.beginPath();g.moveTo(0,0);g.lineTo(0,-60);g.stroke();ell(-12,-30,12,6,'#22C55E',-.6);
  g.fillStyle=c;g.beginPath();g.moveTo(-18,-60);g.lineTo(-18,-90);g.lineTo(-8,-78);g.lineTo(0,-94);g.lineTo(8,-78);g.lineTo(18,-90);g.lineTo(18,-60);g.quadraticCurveTo(0,-48,-18,-60);g.fill();g.restore()}
function birdS(x,y,s,t,c='#60A5FA'){g.save();g.translate(x,y);g.scale(s,s);ell(0,0,30,24,c);ell(22,-14,16,16,c);g.fillStyle='#F59E0B';g.beginPath();g.moveTo(36,-14);g.lineTo(50,-10);g.lineTo(36,-6);g.fill();ell(26,-17,3,3,'#1F2937');
  g.save();g.rotate(Math.sin(t*18)*.6);ell(-6,-14,22,10,shade(c,-.2),-.5);g.restore();g.restore()}
