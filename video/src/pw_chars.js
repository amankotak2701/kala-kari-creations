// ---- characters for "Pop Goes the Weasel" ----
function monkey(x,y,s,t,o={}){const d=o.dir||1,run=o.run||0;g.save();g.translate(x,y-(o.hop||0));g.scale(s*d,s);const B='#92400E',F='#FCD9B6';
  // tail
  g.strokeStyle=B;g.lineWidth=14;g.lineCap='round';g.beginPath();g.moveTo(-50,-80);g.bezierCurveTo(-150,-60,-150,-200,-90,-210);g.stroke();
  // legs
  const lg=(lx,p)=>{const a=run?Math.sin(t*14+p)*.6:0;g.save();g.translate(lx,-70);g.rotate(a);rr(-14,0,28,70,12,B);ell(4,70,22,12,F);g.restore()};lg(-28,0);lg(28,Math.PI);
  ell(0,-120,64,72,B);ell(0,-110,40,50,F);
  // arms
  const arm=(sx,ang)=>{g.save();g.translate(sx,-160);g.rotate(ang);rr(-12,0,24,90,12,B);ell(0,94,16,16,F);g.restore()};
  const up=o.up;arm(-56,up?Math.PI-.4+Math.sin(t*9)*.2:.4+(run?Math.sin(t*14)*.6:0));arm(56,up?-(Math.PI-.4)-Math.sin(t*9)*.2:-.4-(run?Math.sin(t*14)*.6:0));
  // head
  ell(-62,-250,26,26,B);ell(62,-250,26,26,B);ell(-62,-250,15,15,F);ell(62,-250,15,15,F);
  ell(0,-250,66,62,B);ell(-20,-258,26,28,F);ell(20,-258,26,28,F);ell(0,-228,42,30,F);
  ell(-20,-262,8,10,'#1F2937');ell(20,-262,8,10,'#1F2937');ell(-18,-266,3,3,'#fff');ell(22,-266,3,3,'#fff');
  ell(-8,-238,4,3,'#78350F');ell(8,-238,4,3,'#78350F');
  if(o.surprised)ell(0,-215,12,14,'#7F1D1D');else{g.strokeStyle='#78350F';g.lineWidth=5;g.beginPath();g.arc(0,-226,16,.2,Math.PI-.2);g.stroke()}
  g.restore()}
function weasel(x,y,s,t,o={}){const d=o.dir||1;g.save();g.translate(x,y-(o.hop||0));g.scale(s*d,s);const C='#D97706',L='#FEF3C7';
  // long body (stretch for the "pop")
  const st=o.stretch||1;g.save();g.scale(1,st);
  g.strokeStyle=C;g.lineWidth=16;g.lineCap='round';g.beginPath();g.moveTo(-40,-30);g.quadraticCurveTo(-130,-20,-140,-90);g.stroke();ell(-140,-96,12,14,'#78350F');
  rr(-46,-190,92,180,46,C);rr(-28,-170,56,140,28,L);rr(-40,-30,24,34,10,C);rr(16,-30,24,34,10,C);g.restore();
  const hy=-190*st-40;ell(0,hy,58,52,C);ell(-38,hy-44,16,16,C);ell(38,hy-44,16,16,C);ell(-38,hy-44,9,9,'#FBCFE8');ell(38,hy-44,9,9,'#FBCFE8');
  ell(0,hy+18,34,24,L);ell(0,hy+4,10,7,'#1F2937');ell(-20,hy-12,8,10,'#1F2937');ell(20,hy-12,8,10,'#1F2937');ell(-18,hy-16,3,3,'#fff');ell(22,hy-16,3,3,'#fff');
  if(o.surprised)ell(0,hy+28,9,11,'#7F1D1D');else{g.strokeStyle='#78350F';g.lineWidth=4;g.beginPath();g.arc(0,hy+20,10,.2,Math.PI-.2);g.stroke()}
  g.strokeStyle='#78350F';g.lineWidth=2;g.beginPath();g.moveTo(8,hy+6);g.lineTo(46,hy);g.moveTo(8,hy+10);g.lineTo(46,hy+14);g.moveTo(-8,hy+6);g.lineTo(-46,hy);g.moveTo(-8,hy+10);g.lineTo(-46,hy+14);g.stroke();
  if(o.wave){g.save();g.translate(46,-150*st);g.rotate(-2.4+Math.sin(t*9)*.3);rr(-10,0,20,60,10,C);g.restore()}
  g.restore()}
function mulberryBush(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);
  [[-140,-120,120,'#15803D'],[140,-120,120,'#15803D'],[0,-200,150,'#16A34A'],[-80,-80,110,'#22C55E'],[80,-80,110,'#22C55E'],[0,-60,120,'#16A34A']].forEach(([a,b,r,c])=>ell(a,b,r,r*.85,c));
  for(let k=0;k<16;k++){const a=rnd(k)*Math.PI*2,r=rnd(k+5)*170;ell(Math.cos(a)*r,-130+Math.sin(a)*r*.6,13,15,k%3?'#6D28D9':'#9333EA');ell(Math.cos(a)*r-4,-134+Math.sin(a)*r*.6,4,4,'rgba(255,255,255,.6)')}
  g.restore()}
function popBurst(x,y,t,t0,col='#F43F5E'){const p=prog(t,t0,t0+.9);if(p<=0||p>=1)return;g.save();g.translate(x,y);const q=backOut(Math.min(1,p*2.5));g.globalAlpha=Math.min(1,(1-p)*3);
  g.fillStyle='#FDE047';g.beginPath();for(let k=0;k<24;k++){const a=k/24*Math.PI*2,r=(k%2?120:220)*q;g.lineTo(Math.cos(a)*r,Math.sin(a)*r)}g.closePath();g.fill();g.lineWidth=8;g.strokeStyle=col;g.stroke();
  g.rotate(-.12);txt('POP!',0,6,110*q,'#fff',col);g.restore()}
