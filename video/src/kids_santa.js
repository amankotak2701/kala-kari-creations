// ---------- kids & Santa (replace the elephant riders) ----------
const KIDS=[
 {skin:'#F1C9A5',hair:'#2B1B12',style:0,coat:'#2563EB',pants:'#1E3A8A'},
 {skin:'#E8B48A',hair:'#1A120C',style:1,coat:'#DB2777',pants:'#4C1D95'},
 {skin:'#B97A4E',hair:'#20140C',style:3,coat:'#F59E0B',pants:'#1F2937'},
 {skin:'#F5D3B3',hair:'#6B3F1F',style:4,coat:'#7C3AED',pants:'#BE185D'},
 {skin:'#D9A273',hair:'#1A120C',style:2,coat:'#059669',pants:'#1E3A8A'}];
const KMAP={0:0,1:1,2:2,4:3,7:4,3:3};
function kid(i,x,y,o={}){const K=KIDS[i%5],s=o.s||1,d=o.dir||1,t=o.t||0;g.save();g.translate(x,y);g.scale(s*d,s);if(o.rot)g.rotate(o.rot);
  const cheer=(o.trunk??.5)>.75,wv=Math.sin(t*8+i);
  // legs + boots
  rr(-34,-90,28,90,12,K.pants);rr(6,-90,28,90,12,K.pants);ell(-22,-4,26,14,'#3F2A1E');ell(22,-4,26,14,'#3F2A1E');
  // arms (behind for back arm)
  const arm=(sx,ang)=>{g.save();g.translate(sx,-175);g.rotate(ang);rr(-15,0,30,82,15,K.coat);ell(0,86,15,15,K.skin);g.restore()};
  arm(-48,cheer?Math.PI-.5+wv*.2:.25+wv*.1);
  // coat
  g.fillStyle=K.coat;g.beginPath();g.moveTo(-55,-200);g.quadraticCurveTo(0,-215,55,-200);g.lineTo(62,-80);g.quadraticCurveTo(0,-68,-62,-80);g.closePath();g.fill();
  rr(-64,-92,128,18,9,'#FFFFFF');for(let k=0;k<3;k++)ell(0,-170+k*30,6,6,'#FDE68A');
  // scarf
  rr(-48,-215,96,26,13,'#E11D48');rr(18,-200,24,60,10,'#E11D48');g.fillStyle='#fff';g.fillRect(-30,-215,8,26);g.fillRect(-6,-215,8,26);g.fillRect(18,-215,8,26);
  arm(48,cheer?-(Math.PI-.5)-wv*.2:-.25-wv*.1);
  // head
  const hy=-275;
  if(K.style===2){g.fillStyle=K.hair;g.beginPath();g.ellipse(0,hy+20,78,90,0,0,7);g.fill()}
  if(K.style===4){ell(-70,hy+10,22,48,K.hair,-.3)}
  ell(0,hy,70,66,K.skin);ell(-68,hy+5,12,16,K.skin);ell(68,hy+5,12,16,K.skin);
  // hair
  g.fillStyle=K.hair;g.beginPath();
  if(K.style===0){g.ellipse(0,hy-30,72,44,0,Math.PI,0);g.fill();ell(30,hy-38,30,20,K.hair,.3)}
  else if(K.style===1){g.ellipse(0,hy-28,72,46,0,Math.PI,0);g.fill();ell(-78,hy+10,20,30,K.hair);ell(78,hy+10,20,30,K.hair);ell(-70,hy-18,10,10,'#F472B6');ell(70,hy-18,10,10,'#F472B6')}
  else if(K.style===2){g.ellipse(0,hy-30,74,46,0,Math.PI,0);g.fill();g.fillRect(-60,hy-36,120,22)}
  else if(K.style===3){for(let k=0;k<9;k++)ell(-60+k*15,hy-42+Math.abs(k-4)*-3,18,18,K.hair)}
  else{g.ellipse(0,hy-28,72,46,0,Math.PI,0);g.fill();ell(-80,hy-30,16,12,'#F472B6',-.4)}
  // face
  if(o.happy){g.strokeStyle='#2A1A1A';g.lineWidth=6;g.lineCap='round';g.beginPath();g.arc(-24,hy+2,11,Math.PI*1.1,Math.PI*1.9);g.stroke();g.beginPath();g.arc(24,hy+2,11,Math.PI*1.1,Math.PI*1.9);g.stroke()}
  else{ell(-24,hy,9,12,'#2A1A1A');ell(24,hy,9,12,'#2A1A1A');ell(-21,hy-4,3,3,'#fff');ell(27,hy-4,3,3,'#fff')}
  ell(-42,hy+22,13,8,'rgba(240,100,120,.45)');ell(42,hy+22,13,8,'rgba(240,100,120,.45)');
  g.fillStyle='#9F1239';g.beginPath();g.arc(0,hy+24,16,0,Math.PI);g.fill();ell(0,hy+32,8,5,'#FB7185');
  // santa hat
  g.save();g.translate(0,hy-48);g.rotate(-.15);g.fillStyle=RED;g.beginPath();g.moveTo(-70,10);g.quadraticCurveTo(10,-120,-120,-80);g.quadraticCurveTo(-10,-55,70,10);g.fill();
  ell(-122,-80,18,18,'#fff');rr(-76,-4,152,30,15,'#fff');g.restore();
  g.restore()}
function santaEle(i,x,y,o={}){kid(KMAP[i]??0,x,y,Object.assign({},o,{s:(o.s||1)*.95}))}
function santa(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s*(o.dir||1),s);if(o.rot)g.rotate(o.rot);
  const wave=o.wave?Math.sin(t*7)*.35:0;
  if(o.sack){g.save();g.translate(-95,-170);g.rotate(-.2);ell(0,0,70,85,'#8B5A2B');rr(-22,-90,44,30,10,'#6B4220');ell(-20,-20,12,30,'rgba(0,0,0,.12)');g.restore()}
  rr(-55,-95,46,95,16,RED);rr(10,-95,46,95,16,RED);rr(-62,-30,58,32,12,'#1F1A17');rr(6,-30,58,32,12,'#1F1A17');
  ell(0,-170,105,100,RED);rr(-108,-120,216,26,10,'#1F1A17');rr(-24,-126,48,38,6,'#F5C542');rr(-12,-117,24,20,4,'#1F1A17');
  g.fillStyle='#fff';g.fillRect(-12,-270,24,140);
  // arms
  g.save();g.translate(-90,-230);g.rotate(.5);rr(-22,0,44,100,20,RED);ell(0,102,22,20,'#fff');ell(0,118,20,18,'#1F1A17');g.restore();
  g.save();g.translate(90,-230);g.rotate(o.wave?-2.5+wave:(o.reins?-1.1:-.5));rr(-22,0,44,100,20,RED);ell(0,102,22,20,'#fff');ell(0,118,20,18,'#1F1A17');g.restore();
  // head
  ell(0,-310,68,64,'#F6CBA8');
  g.fillStyle='#FFFFFF';g.beginPath();g.moveTo(-72,-310);g.quadraticCurveTo(-80,-180,0,-170);g.quadraticCurveTo(80,-180,72,-310);g.quadraticCurveTo(0,-250,-72,-310);g.fill();
  ell(-26,-282,30,16,'#FFFFFF',-.2);ell(26,-282,30,16,'#FFFFFF',.2);ell(0,-292,13,11,'#F4A3A3');
  ell(-24,-320,8,10,'#2A1A1A');ell(24,-320,8,10,'#2A1A1A');ell(-21,-323,3,3,'#fff');ell(27,-323,3,3,'#fff');
  g.strokeStyle='#FFFFFF';g.lineWidth=7;g.beginPath();g.moveTo(-40,-342);g.lineTo(-12,-346);g.moveTo(12,-346);g.lineTo(40,-342);g.stroke();
  ell(-46,-298,14,9,'rgba(240,100,120,.5)');ell(46,-298,14,9,'rgba(240,100,120,.5)');
  g.fillStyle='#9F1239';g.beginPath();g.arc(0,-262,14,0,Math.PI);g.fill();
  // hat
  g.save();g.translate(0,-360);g.rotate(-.18);g.fillStyle=RED;g.beginPath();g.moveTo(-72,10);g.quadraticCurveTo(10,-140,-130,-95);g.quadraticCurveTo(-10,-60,72,10);g.fill();
  ell(-132,-95,22,22,'#fff');rr(-80,-6,160,36,18,'#fff');g.restore();
  g.restore()}
function hoho(x,y,t,t0){if(t<t0)return;const p=prog(t,t0,t0+1.8);g.save();g.globalAlpha=Math.min(1,p*4,(1-p)*3);g.translate(x,y-p*60);const s=backOut(Math.min(1,p*3));g.scale(s,s);txt('Ho ho ho! 🎅',0,0,72,'#fff',RED);g.restore()}
