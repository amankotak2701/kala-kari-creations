function snowBg(){const gr=g.createRadialGradient(W*.65,H*.35,30,W*.5,H*.5,Math.max(W,H)*.85);gr.addColorStop(0,'#BFE3FF');gr.addColorStop(.55,'#5AA9EE');gr.addColorStop(1,'#1E5FB3');g.fillStyle=gr;g.fillRect(0,0,W,H)}
function maryGroup(cx,fy,s,t){g.save();g.translate(cx,fy);g.scale(s,s);
  ell(0,10,520,70,'#FFFFFF');xmasTree(150,-10,.62,t,1);snowman(-330,20,.42,t,3);
  kid(MARY,-110,40,{s:1.15,t,happy:1,trunk:1});lamb(160,40,1.2,t,{dir:-1,hat:1});
  present(-280,70,110,80,'#DC2626','#FDE68A');present(330,75,100,70,'#15803D','#fff');
  for(let k=0;k<6;k++){const p=k/6;txt('♥',-20+Math.sin(k*2)*90,-420-k*45,40+k*4,'#FB7185',null)}
  g.restore()}
window.makeH=function(){const t=24.3;snowBg();flakes(80,6);
  g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(0,H);for(let x=0;x<=W;x+=20)g.lineTo(x,640+Math.sin(x*.006)*25);g.lineTo(W,H);g.fill();
  maryGroup(930,650,.62,t);
  title3d('MARY HAD A',320,150,96,'#FF4D5E','#C1121F',18);
  title3d('LITTLE LAMB',320,290,104,'#FFFFFF','#DDE7F5',18,'#1E3A8A');
  g.save();g.translate(320,430);rr(-260,-44,520,88,44,'#15803D');g.lineWidth=6;g.strokeStyle='#F5C542';g.stroke();txt('Christmas Edition 🎄',0,2,46,'#fff',null);g.restore();
  popcornLogo(70,650,.15,0)};
window.makeV=function(){const t=24.3;snowBg();flakes(120,6);
  g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(0,H);for(let x=0;x<=W;x+=20)g.lineTo(x,1640+Math.sin(x*.006)*30);g.lineTo(W,H);g.fill();
  title3d('MARY HAD A',540,230,140,'#FF4D5E','#C1121F',26);
  title3d('LITTLE LAMB',540,420,150,'#FFFFFF','#DDE7F5',26,'#1E3A8A');
  g.save();g.translate(540,580);rr(-320,-52,640,104,52,'#15803D');g.lineWidth=7;g.strokeStyle='#F5C542';g.stroke();txt('Christmas Edition 🎄',0,2,54,'#fff',null);g.restore();
  maryGroup(540,1660,1.0,t);
  popcornLogo(975,1830,.22,0)};
