function crescent(x,y,r,off){const c2=document.createElement('canvas');c2.width=c2.height=Math.ceil(r*2.4);const q=c2.getContext('2d');const cx=c2.width/2;
  const gr=q.createRadialGradient(cx-r*.3,cx-r*.3,r*.1,cx,cx,r);gr.addColorStop(0,'#FFF9D6');gr.addColorStop(1,'#FFD54A');
  q.fillStyle=gr;q.beginPath();q.arc(cx,cx,r,0,7);q.fill();q.globalCompositeOperation='destination-out';q.beginPath();q.arc(cx+off[0],cx+off[1],r*.86,0,7);q.fill();
  glow(x,y,r*1.9,'rgba(255,225,120,.55)');g.drawImage(c2,x-cx,y-cx);
  // sleepy face on crescent
  g.strokeStyle='#8A5A00';g.lineWidth=r*.05;g.lineCap='round';g.beginPath();g.arc(x-r*.62,y-r*.05,r*.11,Math.PI*.15,Math.PI*.85);g.stroke();
  ell(x-r*.68,y+r*.2,r*.1,r*.06,'rgba(255,130,140,.6)');g.beginPath();g.arc(x-r*.6,y+r*.32,r*.08,Math.PI*.3,Math.PI*1.1);g.stroke()}
function capOn(x,y,s,rot){g.save();g.translate(x,y);g.scale(s,s);g.rotate(rot||0);g.translate(95,-245);g.rotate(-.35);
  g.fillStyle='#6366F1';g.beginPath();g.moveTo(-80,15);g.quadraticCurveTo(-20,-120,-175,-70);g.quadraticCurveTo(-30,-55,80,15);g.fill();
  for(let k=0;k<4;k++)starShape(-40-k*30,-30-k*14,9,0,'#FDE68A');ell(-178,-70,20,20,'#fff');rr(-88,0,176,34,17,'#fff');g.restore()}
function hangStar(x,len,r,t,k){g.strokeStyle='rgba(255,255,255,.6)';g.lineWidth=2;g.beginPath();g.moveTo(x,0);g.lineTo(x,len);g.stroke();starFace(x,len+r*.8,r,t,k)}
function title3d(s,x,y,size,top,bot,lw){g.font=`800 ${size}px Fredoka, Baloo2`;g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';
  for(let d=12;d>0;d-=2){g.lineWidth=lw;g.strokeStyle='#1A0B3D';g.strokeText(s,x,y+d);g.fillStyle='#1A0B3D';g.fillText(s,x,y+d)}
  g.lineWidth=lw;g.strokeStyle='#2A1458';g.strokeText(s,x,y);const gr=g.createLinearGradient(0,y-size*.5,0,y+size*.5);gr.addColorStop(0,top);gr.addColorStop(1,bot);g.fillStyle=gr;g.fillText(s,x,y);
  g.save();g.globalAlpha=.35;g.lineWidth=lw*.18;g.strokeStyle='#fff';g.strokeText(s,x,y-size*.04);g.restore()}
function bg(){const gr=g.createRadialGradient(W*.68,H*.42,20,W*.6,H*.5,Math.max(W,H)*.8);gr.addColorStop(0,'#5B3FB0');gr.addColorStop(.5,'#2A1E7A');gr.addColorStop(1,'#0B0F3D');g.fillStyle=gr;g.fillRect(0,0,W,H);
  for(let k=0;k<160;k++){g.globalAlpha=.3+.7*rnd(k+5);const r=1+rnd(k+2)*2.5;ell(rnd(k)*W,rnd(k+50)*H,r,r,'#FFF6D5')}g.globalAlpha=1}
function moti(x,y,s,t){g.save();g.translate(x,y);g.rotate(-.12);elephant(0,0,0,{s,t:1.2,sleep:1,trunk:.05,noShadow:1});capOn(0,0,s,0);g.restore()}
window.makeH=function(){const t=2.2;bg();
  for(let k=0;k<4;k++)bigCloud(700+k*190,700+(k%2)*30,.55,'rgba(255,255,255,.22)');
  hangStar(760,90,38,t,1);hangStar(1180,150,44,t,2);hangStar(1060,40,30,t,3);
  crescent(930,360,250,[110,-70]);
  moti(880,520,.95,t);
  zzz(1040,300,0.9,1.4);
  title3d('निन्नी',330,215,190,'#FFF36B','#FFB300',30);
  title3d('आ गई',300,415,150,'#FFFFFF','#E0E7FF',26);
  g.save();g.translate(330,580);rr(-235,-46,470,92,46,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('Hindi Lullaby 🌙',0,2,50,'#fff',null);g.restore();
  popcornLogo(1205,650,.16,0)};
window.makeV=function(){const t=2.2;bg();
  hangStar(160,180,50,t,1);hangStar(930,120,56,t,2);hangStar(780,40,38,t,3);hangStar(300,60,36,t,4);
  for(let k=0;k<4;k++)bigCloud(100+k*300,1180+(k%2)*40,.75,'rgba(255,255,255,.2)');
  crescent(600,760,340,[150,-95]);moti(520,980,1.25,t);zzz(760,640,0.9,1.8);
  title3d('निन्नी',540,1380,250,'#FFF36B','#FFB300',40);title3d('आ गई 🌙',540,1620,190,'#FFFFFF','#E0E7FF',32);
  g.save();g.translate(540,1800);rr(-320,-55,640,110,55,'#E11D48');g.lineWidth=7;g.strokeStyle='#fff';g.stroke();txt('Hindi Lullaby • लोरी',0,2,58,'#fff',null);g.restore();
  popcornLogo(110,110,.28,0)};
window.ready=Promise.all([document.fonts.load('700 40px Baloo2','हा'),document.fonts.load('800 40px Baloo2','हा'),document.fonts.load('700 40px Fredoka')]);
</script></body></html>
