// ================= "O Christmas Tree" — kids decorate the tree (Popcorn Productions) =================
const OB=0.645, OBAR=3*OB, OLINE=2*OBAR, OV0=29.91, OVERSE=8*OLINE;   // 3/4, 2-bar lines, 8-line verses
const ov=k=>OV0+k*OVERSE, oline=(v,l)=>ov(v)+l*OLINE;
const OEND=163.4, OCARD=154.6;
const opulse=t=>Math.pow(Math.sin(Math.PI*((((t-OV0)/OB)%1+1)%1)),2);
const osway=t=>Math.sin(2*Math.PI*(t-OV0)/(2*OBAR));
const TX=540, TBASE=1500;                       // tree centre & base
const TIERS=[[TBASE-20,300],[TBASE-230,240],[TBASE-430,180],[TBASE-620,120]]; // [bottom y, half width]
const TAPEX=TBASE-620-300;
function treeHalfW(y){ // half width of the tree silhouette at height y
  let w=0;TIERS.forEach(([by,hw])=>{const top=by-300;if(y<=by&&y>=top){w=Math.max(w,hw*(y-top)/300)}});return w}
// decoration layouts (deterministic)
const ORN=[];for(let k=0;k<26;k++){const y=TBASE-60-rnd(k+31)*780;const w=treeHalfW(y)*.82;ORN.push([TX+(rnd(k+47)*2-1)*w,y,['#EF4444','#FBBF24','#3B82F6','#EC4899','#A855F7','#22C55E','#F97316'][k%7]])}
ORN.sort((a,b)=>b[1]-a[1]);
const LIGHTS=[];for(let k=0;k<46;k++){const u=k/45;const y=TBASE-50-u*840;const w=treeHalfW(y)*.86;LIGHTS.push([TX+Math.sin(u*Math.PI*9)*w,y,['#FDE047','#F87171','#60A5FA','#4ADE80','#F0ABFC'][k%5]])}

function bigTree(t,o={}){const tilt=o.tilt||0;g.save();if(tilt){g.translate(TX,TBASE);g.rotate(tilt);g.translate(-TX,-TBASE)}
  rr(TX-34,TBASE-30,68,90,10,'#6B4220');
  // pot
  g.fillStyle='#B91C1C';g.beginPath();g.moveTo(TX-110,TBASE+40);g.lineTo(TX+110,TBASE+40);g.lineTo(TX+85,TBASE+150);g.lineTo(TX-85,TBASE+150);g.closePath();g.fill();rr(TX-120,TBASE+30,240,30,10,'#F5C542');
  TIERS.forEach(([by,hw],i)=>{const top=by-300;
    g.fillStyle=i%2?'#167A3E':'#1B8A47';g.beginPath();g.moveTo(TX,top);g.quadraticCurveTo(TX-hw*.4,by-110,TX-hw-18,by);
    for(let k=0;k<6;k++){const x0=TX-hw-18+k*(hw*2+36)/6;g.quadraticCurveTo(x0+(hw*2+36)/12,by+26,x0+(hw*2+36)/6,by)}
    g.quadraticCurveTo(TX+hw*.4,by-110,TX,top);g.fill();
    g.fillStyle='rgba(0,0,0,.12)';g.beginPath();g.moveTo(TX,top);g.quadraticCurveTo(TX+hw*.4,by-110,TX+hw+18,by);g.lineTo(TX+hw*.2,by);g.closePath();g.fill();
    if(o.snow){g.fillStyle='rgba(255,255,255,.85)';for(let k=0;k<5;k++)ell(TX-hw*.7+k*hw*.35,by-8,26,8,'#fff')}});
  // garland (gold tinsel swags), drawn progressively
  const gp=o.garland||0;if(gp>0){g.save();g.lineCap='round';
    [[TBASE-130,.9],[TBASE-330,.85],[TBASE-520,.8],[TBASE-700,.7]].forEach(([y,f],i)=>{const p=clamp(gp*4-i);if(p<=0)return;const w=treeHalfW(y)*f;
      g.strokeStyle='#F5C542';g.lineWidth=12;g.setLineDash([2,10]);g.beginPath();g.moveTo(TX-w,y-40);g.quadraticCurveTo(TX-w+w*p,y+50,TX-w+2*w*p,y-40+ (p<1?0:0));g.stroke();
      g.setLineDash([]);g.strokeStyle='#FDE68A';g.lineWidth=4;g.beginPath();g.moveTo(TX-w,y-40);g.quadraticCurveTo(TX-w+w*p,y+50,TX-w+2*w*p,y-40);g.stroke()});g.restore()}
  // lights wire + bulbs
  const ln=o.lights||0,on=o.lightsOn||0;if(ln>0){const n=Math.floor(ln*LIGHTS.length);
    g.strokeStyle='#14532D';g.lineWidth=4;g.beginPath();LIGHTS.slice(0,n).forEach(([x,y],k)=>k?g.lineTo(x,y):g.moveTo(x,y));g.stroke();
    LIGHTS.slice(0,n).forEach(([x,y,c],k)=>{const lit=k<on*LIGHTS.length;ell(x,y,9,12,lit?c:'#6B7280');if(lit&&!o.dimPass){}})}
  // ornaments
  const orn=o.ornaments||0;ORN.forEach(([x,y,c],k)=>{const p=clamp(orn*ORN.length-k);if(p<=0)return;const s=backOut(clamp(p*2));
    g.strokeStyle='#F5C542';g.lineWidth=3;g.beginPath();g.moveTo(x,y-22*s);g.lineTo(x,y-34*s);g.stroke();
    ell(x,y,22*s,22*s,c);ell(x-7*s,y-8*s,7*s,7*s,'rgba(255,255,255,.65)');rr(x-7*s,y-28*s,14*s,8*s,2,'#F5C542')});
  g.restore()}
function treeGlow(t,o){ // bright layer drawn above the dim overlay
  const on=o.lightsOn||0;LIGHTS.forEach(([x,y,c],k)=>{if(k>=on*LIGHTS.length||k>=(o.lights||0)*LIGHTS.length)return;const tw=.6+.4*Math.sin(t*4+k*1.7);
    glow(x,y,46*tw,c.replace(')',',.0)').startsWith('#')?hexA(c,.55*tw):c);ell(x,y,9,12,c);ell(x-3,y-4,3,4,'rgba(255,255,255,.8)')});
  const st=o.star||0;if(st>0){const s=backOut(st)*(1+.06*Math.sin(t*3));g.save();g.translate(TX,TAPEX-10);g.scale(s,s);glow(0,0,170,'rgba(255,230,120,.75)');starShape(0,0,70,0,'#FFD84D');starShape(0,0,52,0,'#FFF3B0');g.restore();
    for(let k=0;k<10;k++){const a=t*1.2+k/10*Math.PI*2;starShape(TX+Math.cos(a)*120*st,TAPEX-10+Math.sin(a)*120*st,8,a,'rgba(255,240,170,.9)')}}}
function hexA(hex,a){const n=parseInt(hex.slice(1),16);return `rgba(${n>>16},${n>>8&255},${n&255},${a})`}
function treeRoom(t){
  const w=g.createLinearGradient(0,0,0,1420);w.addColorStop(0,'#2E2A6B');w.addColorStop(1,'#4B3B8F');g.fillStyle=w;g.fillRect(0,0,W,1420);
  for(let k=0;k<10;k++)for(let j=0;j<9;j++){g.globalAlpha=.07;starShape(50+k*110,80+j*160+(k%2)*80,12,0,'#FDE68A')}g.globalAlpha=1;
  [[60,600],[820,600]].forEach(([x,y])=>{g.save();g.beginPath();g.roundRect(x,y,200,300,90);g.clip();sky('#0B1446','#1E3A8A');
    for(let k=0;k<20;k++){const yy=((t*50+rnd(k+x)*300)%300)+y;ell(x+rnd(k+2+x)*200,yy,4,4,'#fff')}ell(x+100,y+300,140,40,'#E0EAFF');if(x>500)moonFace(x+130,y+70,32,t,0,0);g.restore();
    g.strokeStyle='#F5E1C0';g.lineWidth=12;g.beginPath();g.roundRect(x,y,200,300,90);g.stroke();g.lineWidth=6;g.beginPath();g.moveTo(x+100,y);g.lineTo(x+100,y+300);g.moveTo(x,y+170);g.lineTo(x+200,y+170);g.stroke()});
  const fl=g.createLinearGradient(0,1410,0,H);fl.addColorStop(0,'#8B5A2B');fl.addColorStop(1,'#5C3A1A');g.fillStyle=fl;g.fillRect(0,1410,W,H-1410);
  for(let k=0;k<8;k++){g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=3;g.beginPath();g.moveTo(0,1450+k*70);g.lineTo(W,1450+k*70);g.stroke()}
  ell(540,1690,500,110,'#15803D');ell(540,1690,440,85,'#F5C542');ell(540,1690,380,62,'#15803D');}
const OKIDS=[[0,128],[1,285],[3,795],[2,952]];
function kidsAround(t,o={}){OKIDS.forEach(([k,x],i)=>{const up=o.reach&&((Math.floor((t-OV0)/(1.5*OB))+i)%4===0);const j=o.jump?opulse(t+i*.1)*60:0;
  kid(k,x,1745-j,{s:.95,dir:x<540?1:-1,t,happy:o.happy??(opulse(t)>.5),trunk:up||o.cheer?1:.5,rot:osway(t+i*.1)*.05})})}
function holdCandles(t){OKIDS.forEach(([k,x],i)=>{const d=x<540?1:-1;const cx=x+d*55,cy=1580;rr(cx-8,cy-40,16,46,5,'#FFF7E6');const f=Math.sin(t*9+i)*3;ell(cx,cy-52+f,8,15,'#FBBF24');glow(cx,cy-52,80,'rgba(255,200,90,.55)')})}
function flyOrn(t,t0,from,to,c){const p=prog(t,t0,t0+.55);if(p<=0||p>=1)return;const x=lerp(from[0],to[0],p),y=lerp(from[1],to[1],p)-Math.sin(Math.PI*p)*160;ell(x,y,20,20,c);ell(x-6,y-7,6,6,'rgba(255,255,255,.65)')}
function insetBubble(x,y,r,draw){g.save();ell(x,y,r+10,r+10,'#FFFFFF');g.beginPath();g.arc(x,y,r,0,7);g.clip();draw();g.restore();ell(x-r*.7,y+r*.9,22,22,'#fff');ell(x-r*.95,y+r*1.2,12,12,'#fff')}
function octitle(t){g.save();g.translate(615,170);const p=backOut(prog(t,.3,1.3));g.scale(p,p);g.fillStyle='#15803D';g.beginPath();g.roundRect(-330,-66,660,132,66);g.fill();g.lineWidth=8;g.strokeStyle='#F5C542';g.stroke();txt('O Christmas Tree 🎄',0,2,60,'#FFFFFF',null);g.restore()}
const OLYR=[
 ['O Christmas Tree, O Christmas Tree,','Thy leaves are so unchanging;','O Christmas Tree, O Christmas Tree,','Thy leaves are so unchanging;','Not only green when summer\'s here,','But also when \'tis cold and drear.','O Christmas Tree, O Christmas Tree,','Thy leaves are so unchanging!'],
 ['O Christmas Tree, O Christmas Tree,','Much pleasure thou can\'st give me;','O Christmas Tree, O Christmas Tree,','Much pleasure thou can\'st give me;','How often has the Christmas tree','Afforded me the greatest glee!','O Christmas Tree, O Christmas Tree,','Much pleasure thou can\'st give me!'],
 ['O Christmas Tree, O Christmas Tree,','Thy candles shine so brightly!','O Christmas Tree, O Christmas Tree,','Thy candles shine so brightly!','From base to summit, gay and bright,','There\'s only splendor for the sight.','O Christmas Tree, O Christmas Tree,','Thy candles shine so brightly!'],
 ['O Christmas Tree, O Christmas Tree,','How richly God has decked thee!','O Christmas Tree, O Christmas Tree,','How richly God has decked thee!','Thou bidst us true and faithful be,','And trust in God unchangingly.','O Christmas Tree, O Christmas Tree,','How richly God has decked thee!']];
const OCAP=[];OLYR.forEach((v,vi)=>{for(let p=0;p<4;p++)OCAP.push([oline(vi,2*p)-OB*.6,oline(vi,2*p+2)-OB*.6,v[2*p]+' '+v[2*p+1]])});
function occaption(t){const i=OCAP.findIndex(([a,b])=>t>=a&&t<b);if(i<0)return;const [a,b,s]=OCAP[i];
  const al=Math.min(clamp((t-a)/.25),clamp((b-t)/.2));g.save();g.globalAlpha=al;g.font='700 58px Fredoka, Baloo2';
  const words=s.split(' ');let lines=[''];words.forEach(w=>{const tl=(lines[lines.length-1]+' '+w).trim();if(g.measureText(tl).width>880&&lines[lines.length-1])lines.push(w);else lines[lines.length-1]=tl});
  const h=lines.length*72+40,y0=390;g.fillStyle='rgba(120,20,30,.86)';g.beginPath();g.roundRect(60,y0-h/2,W-120,h,36);g.fill();g.lineWidth=6;g.strokeStyle='#F5C542';g.stroke();
  const prg=clamp((t-a)/((b-a)*.92));const ws=lines.map(l=>g.measureText(l).width),tot=ws.reduce((p,q)=>p+q,0);let rem=prg*tot;
  lines.forEach((ln,li)=>{const y=y0-h/2+20+36+li*72,x=W/2-ws[li]/2;g.textAlign='left';g.textBaseline='middle';g.fillStyle='#fff';g.fillText(ln,x,y);
    const fw=clamp(rem,0,ws[li]);rem-=ws[li];if(fw>0){g.save();g.beginPath();g.rect(x,y-50,fw,100);g.clip();g.fillStyle='#FFE14D';g.fillText(ln,x,y);g.restore()}});g.restore()}

function drawOCT(t){g.setTransform(1,0,0,1,0,0);g.fillStyle='#000';g.fillRect(0,0,W,H);
  // decoration state over time
  const garland=prog(t,oline(0,6),oline(1,0));
  const orn=prog(t,oline(1,0),oline(1,7));
  const lights=prog(t,oline(2,0),oline(2,4));
  const lightsOn=prog(t,oline(2,4),oline(2,5));
  const star=prog(t,oline(2,5),oline(2,5)+1.2);
  const dim=t<oline(2,4)?0:Math.min(.55,prog(t,oline(2,4),oline(2,5))*.45+(t>ov(3)?prog(t,ov(3),ov(3)+3)*.12:0));
  const deco={garland,ornaments:orn,lights,lightsOn,star};
  if(t<12.5){ // outside: kids carry the tree home through the snow
    winterSky(t,1);for(let k=0;k<60;k++){g.globalAlpha=.5+.5*Math.sin(t*3+k);ell(rnd(k)*W,rnd(k+7)*1000,2.5,2.5,'#fff')}g.globalAlpha=1;moonFace(820,640,80,t,0,0);
    snowHills(t,0,1380);g.save();g.translate(860,1540);g.scale(1.6,1.6);house(0,0,1,t);g.restore();pine(120,1600,.9);
    const x=lerp(-420,420,easeOut(prog(t,.5,11)));const bob=Math.abs(Math.sin(t*5))*12;
    g.save();g.translate(x+150,1470-bob);g.rotate(-Math.PI/2+.08);g.scale(.32,.32);g.translate(-TX,-TBASE);bigTree(t,{snow:1});g.restore();
    kid(0,x,1700-bob,{s:.72,t,happy:1,trunk:1});kid(1,x+300,1700-bob,{s:.72,t,happy:1,trunk:1});
    kid(3,x-160,1720,{s:.65,t,happy:1});present(x-110,1560,90,70,'#DC2626','#FDE68A');kid(2,x+460,1720,{s:.65,t,happy:1});puppy(x+560,1730,.5,t,Math.abs(Math.sin(t*6))*25);
  }
  else if(t<OV0-.3){ // inside: tree goes up, boxes of decorations open
    treeRoom(t);const tilt=-(1-easeOut(prog(t,13,16)))*1.2;bigTree(t,{tilt});
    const op=easeOut(prog(t,18,20));present(330,1800,170,120,'#DC2626','#FDE68A',op);present(760,1800,150,110,'#2563EB','#F9A8D4',op);
    kidsAround(t,{happy:1,cheer:t>16&&t<18});puppy(560,1830,.55,t,opulse(t)*20);
    if(t>20){const q=backOut(prog(t,20,21));g.save();g.translate(540,820);g.scale(q,q);txt('Let\'s decorate! 🎄',0,0,90,'#fff',RED);g.restore()}
    if(op>.4)for(let k=0;k<6;k++){const p=((t*.5+k/6)%1);starShape(330+(k%2)*430+Math.sin(p*7+k)*40,1700-p*300,10*(1-p),t*3,'#FDE68A')}
  }
  else if(t<ov(1)-.3){ // verse 1: green all year; garland goes on at the end
    treeRoom(t);bigTree(t,deco);kidsAround(t,{reach:t>oline(0,6)});puppy(560,1840,.55,t,0);
    const l=Math.floor((t-OV0)/OLINE);
    if(l===4||l===5){const sum=l===4;const p=easeOut(prog(t,oline(0,l),oline(0,l)+.6));g.save();g.translate(800,820);g.scale(p,p);g.translate(-800,-820);
      insetBubble(800,820,150,()=>{if(sum){sky('#7DD3FC','#E0F2FE');mandalaSun(880,720,40,t);g.fillStyle='#86EFAC';g.fillRect(650,880,320,120)}else{sky('#1E3A8A','#93C5FD');g.fillStyle='#F4F8FF';g.fillRect(650,880,320,120);for(let k=0;k<14;k++)ell(660+rnd(k)*300,((t*60+rnd(k+3)*300)%300)+670,4,4,'#fff')}pine(800,920,.75,!sum)});g.restore();
      txt(sum?'☀️ Summer':'❄️ Winter',800,1010,44,'#fff',RED)}
    if(t>oline(0,6))for(let k=0;k<8;k++){const p=((t*.8+k/8)%1);starShape(TX-280+rnd(k)*560,TBASE-100-p*600,9,t*4+k,'rgba(253,230,138,'+(1-p)+')')}
  }
  else if(t<ov(2)-.3){ // verse 2: ornaments fly onto the tree, kids jump with glee
    treeRoom(t);bigTree(t,deco);
    ORN.forEach(([x,y,c],k)=>{const tk=oline(1,0)+(k/ORN.length)*(oline(1,7)-oline(1,0));const kd=OKIDS[k%4];flyOrn(t,tk-.55,[kd[1]+(kd[1]<540?40:-40),1500],[x,y],c)});
    const l=Math.floor((t-ov(1))/OLINE);kidsAround(t,{reach:l<4||l>5,jump:l===4||l===5,cheer:l===4||l===5,happy:1});puppy(560,1840,.55,t,(l===4||l===5)?opulse(t)*50:0);
    if(l>=4&&l<=5)for(let k=0;k<5;k++){const p=((t*.7+k/5)%1);g.save();g.globalAlpha=1-p;txt(['Yay!','🎉','Wheee!','😄','Yay!'][k],150+k*190,1150-p*220,56,'#fff',RED);g.restore()}
    if(l>=6){present(380,1830,130,100,'#DC2626','#FDE68A');present(700,1835,120,90,'#22C55E','#fff')}
  }
  else if(t<OCARD){ // verses 3-4: lights base->summit, star on top, then quiet candles
    treeRoom(t);bigTree(t,deco);present(380,1830,130,100,'#DC2626','#FDE68A');present(700,1835,120,90,'#22C55E','#fff');present(560,1860,100,75,'#3B82F6','#F9A8D4');
    const v3=t<ov(3);const l=Math.floor((t-ov(v3?2:3))/OLINE);
    kidsAround(t,{reach:v3&&l<4,cheer:v3&&l>=5&&l<=6,happy:1});
    if(v3&&t>oline(2,5)-.8&&t<oline(2,5)+.4){const p=prog(t,oline(2,5)-.8,oline(2,5));const x=lerp(805,TX,p),y=lerp(1450,TAPEX-10,easeOut(p));g.save();g.translate(x,y);starShape(0,0,50,p*6,'#FFD84D');g.restore();
      for(let k=0;k<8;k++){const q=p-k*.04;starShape(lerp(805,TX,q),lerp(1450,TAPEX-10,easeOut(q)),10-k,q*8,'rgba(255,240,170,.8)')}}
    if(dim>0){g.fillStyle=`rgba(8,8,35,${dim})`;g.fillRect(0,0,W,H)}
    treeGlow(t,deco);
    if(!v3){holdCandles(t);snowfall(t,25,.4)}
    if(v3&&l===5){const p=prog(t,oline(2,5)+.4,oline(2,6));if(p<1){g.save();g.globalAlpha=Math.min(1,(1-p)*3);txt('✨ So bright! ✨',540,1060,72,'#FFE14D','#7C2D12');g.restore()}}
  }
  else{ // end card
    treeRoom(t);bigTree(t,deco);g.fillStyle='rgba(8,8,35,.7)';g.fillRect(0,0,W,H);treeGlow(t,deco);
    const ec=OCARD;const q=easeOut(prog(t,ec,ec+1));g.save();g.globalAlpha=q;g.fillStyle='rgba(8,8,35,.5)';g.fillRect(0,0,W,H);
    popcornLogo(W/2,560,.9*backOut(prog(t,ec,ec+1.2)),Math.max(0,Math.sin(Math.PI*prog(t,ec+1.2,ec+1.7)))*.25);
    txt('A Popcorn Productions video',W/2,940,46,'#FFE14D',null,'center',600);
    txt('Merry Christmas! 🎄',W/2,1060,80,'#fff',RED);
    const sp=backOut(prog(t,ec+1.4,ec+2.4));g.save();g.translate(W/2,1220);g.scale(sp,sp);rr(-250,-58,500,116,58,'#E11D48');g.lineWidth=6;g.strokeStyle='#fff';g.stroke();txt('▶  SUBSCRIBE',0,0,54,'#fff',null);g.restore();
    g.restore();kidsAround(t,{happy:1,cheer:1});holdCandles(t);
  }
  [12.5,OV0-.3,ov(1)-.3,ov(2)-.3,OCARD].forEach(c=>{const d=Math.abs(t-c);if(d<.3){g.fillStyle=`rgba(255,255,255,${(1-d/.3)*.75})`;g.fillRect(0,0,W,H)}});
  if(t<OCARD){octitle(t);occaption(t);g.save();g.globalAlpha=.9;popcornLogo(92,172,.24,0);g.restore()}
  if(t<12.5)snowfall(t,70,.8);
  if(t<.8){g.fillStyle=`rgba(0,0,0,${1-t/.8})`;g.fillRect(0,0,W,H)}
  const f=prog(t,OEND-1.5,OEND);if(f>0){g.fillStyle=`rgba(0,0,0,${f})`;g.fillRect(0,0,W,H)}
}
window.draw=drawOCT;
