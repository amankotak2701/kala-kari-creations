// ---- "Skip to My Lou" helpers ----
function fly(x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);g.save();g.globalAlpha=.7;ell(-14,-20,16,24,'#E0F2FE',-.4+Math.sin(t*60)*.3);ell(14,-20,16,24,'#E0F2FE',.4-Math.sin(t*60)*.3);g.restore();
  ell(0,0,20,16,'#1F2937');ell(16,-4,12,12,'#1F2937');ell(20,-8,5,5,'#EF4444');g.restore()}
function churn(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle='#B45309';g.beginPath();g.moveTo(-70,0);g.lineTo(70,0);g.lineTo(55,-200);g.lineTo(-55,-200);g.closePath();g.fill();
  for(let k=0;k<3;k++)rr(-72+k*4,-40-k*70,144-k*8,14,4,'#78350F');ell(0,-200,58,16,'#FEFCE8');rr(-6,-300,12,110,6,'#92400E');txt('MILK',0,-110,30,'#FEF3C7',null);g.restore()}
function wagon(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);rr(-160,-120,320,90,14,o.col||'#EF4444');rr(-170,-130,340,20,8,shade(o.col||'#EF4444',-.2));
  [-100,100].forEach(dx=>{g.save();g.translate(dx,-20);g.rotate(t*(o.roll||0));ell(0,0,40,40,'#1F2937');ell(0,0,16,16,'#9CA3AF');for(let k=0;k<4;k++){g.rotate(Math.PI/4);rr(-3,-36,6,72,3,'#9CA3AF')}g.restore()});
  g.strokeStyle='#1F2937';g.lineWidth=8;g.beginPath();g.moveTo(160,-80);g.lineTo(260,-150);g.stroke();g.restore()}
function sbarn(t,o={}){farmBg(t,o)}
