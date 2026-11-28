// ---- extra characters for "The Farmer in the Dell" ----
function kitty(x,y,s,t,o={}){const d=o.dir||1;g.save();g.translate(x,y-(o.hop||0));g.scale(s*d,s);const C='#FB923C',D='#EA580C';
  g.save();g.translate(-80,-70);g.rotate(Math.sin(t*5)*.4);g.strokeStyle=C;g.lineWidth=18;g.lineCap='round';g.beginPath();g.moveTo(0,0);g.quadraticCurveTo(-60,-40,-40,-120);g.stroke();g.restore();
  ell(0,-60,85,52,C);for(let k=0;k<3;k++){g.strokeStyle=D;g.lineWidth=8;g.beginPath();g.moveTo(-40+k*30,-108);g.lineTo(-30+k*30,-80);g.stroke()}
  rr(-60,-30,22,36,10,C);rr(36,-30,22,36,10,C);ell(-49,6,16,9,'#FFF7ED');ell(47,6,16,9,'#FFF7ED');
  ell(70,-120,58,52,C);g.fillStyle=C;[[30,-160,40,-205,62,-165],[78,-165,104,-205,110,-150]].forEach(([a,b,c,dd,e,f])=>{g.beginPath();g.moveTo(a,b);g.lineTo(c,dd);g.lineTo(e,f);g.fill()});
  g.fillStyle='#FBCFE8';g.beginPath();g.moveTo(42,-165);g.lineTo(46,-190);g.lineTo(56,-168);g.fill();
  ell(50,-125,8,11,'#1F2937');ell(92,-125,8,11,'#1F2937');ell(52,-129,3,3,'#fff');ell(94,-129,3,3,'#fff');ell(72,-106,7,5,'#F472B6');
  g.strokeStyle='#1F2937';g.lineWidth=3;[[-1,0],[1,0]].forEach(([k])=>{g.beginPath();g.moveTo(72+k*12,-102);g.lineTo(72+k*50,-110);g.moveTo(72+k*12,-98);g.lineTo(72+k*50,-94);g.stroke()});
  g.beginPath();g.arc(66,-98,6,0,Math.PI);g.arc(78,-98,6,0,Math.PI);g.stroke();g.restore()}
function mouseC(x,y,s,t,o={}){const d=o.dir||1;g.save();g.translate(x,y-(o.hop||0));g.scale(s*d,s);const C='#A8A29E';
  g.strokeStyle='#F9A8D4';g.lineWidth=7;g.lineCap='round';g.beginPath();g.moveTo(-60,-30);g.quadraticCurveTo(-120,-10+Math.sin(t*6)*20,-140,-60);g.stroke();
  ell(0,-40,62,40,C);ell(-25,-4,14,8,'#F9A8D4');ell(25,-4,14,8,'#F9A8D4');ell(50,-62,38,34,C);ell(36,-98,26,26,C);ell(36,-98,16,16,'#FBCFE8');ell(72,-92,22,22,C);ell(72,-92,13,13,'#FBCFE8');
  ell(62,-66,6,8,'#1F2937');ell(88,-52,8,7,'#F472B6');g.strokeStyle='#57534E';g.lineWidth=2;g.beginPath();g.moveTo(86,-52);g.lineTo(118,-60);g.moveTo(86,-50);g.lineTo(118,-44);g.stroke();g.restore()}
function cheese(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);if(o.wobble)g.rotate(Math.sin(t*6)*.05);
  g.fillStyle='#FACC15';g.beginPath();g.moveTo(-110,0);g.lineTo(110,0);g.lineTo(110,-90);g.lineTo(-110,-150);g.closePath();g.fill();
  g.fillStyle='#FDE047';g.beginPath();g.moveTo(-110,-150);g.lineTo(110,-90);g.lineTo(140,-110);g.lineTo(-80,-170);g.closePath();g.fill();
  g.fillStyle='#EAB308';g.beginPath();g.moveTo(110,0);g.lineTo(140,-20);g.lineTo(140,-110);g.lineTo(110,-90);g.closePath();g.fill();
  [[-60,-50,18],[10,-30,12],[60,-60,16],[-20,-100,10],[-80,-100,9]].forEach(([a,b,r])=>ell(a,b,r,r,'#CA8A04'));
  if(o.face){const sad=o.sad;ell(-30,-70,9,12,'#3F2A1E');ell(30,-58,9,12,'#3F2A1E');g.strokeStyle='#3F2A1E';g.lineWidth=5;g.beginPath();if(sad)g.arc(0,-20,16,Math.PI*1.15,Math.PI*1.85);else g.arc(0,-40,16,.2,Math.PI-.2);g.stroke();
    if(sad){ell(-30,-48+((t*50)%30),5,8,'#60A5FA')}}
  g.restore()}
function nurseP(x,y,s,t,o={}){adult('teacher',x,y,Object.assign({s,t,happy:1},o));g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);
  rr(-48,-530,96,40,12,'#FFFFFF');rr(-10,-528,20,36,3,'#EF4444');rr(-18,-520,36,20,3,'#EF4444');g.restore()}
