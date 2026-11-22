{ sed -n 1,189p anim.html; cat nini_scenes.js; echo "window.ready=Promise.all([document.fonts.load('700 40px Baloo2','हा'),document.fonts.load('600 40px Baloo2','हा'),document.fonts.load('700 40px Fredoka'),document.fonts.load('600 40px Fredoka')]);"; echo "</script></body></html>"; } > nini.html
python3 -c "
p='nini.html';s=open(p).read();s=s.replace('  if(o.happy){',\"  if(o.sleep){g.strokeStyle='#2A1A1A';g.lineWidth=6;g.beginPath();g.arc(128,-196,13,Math.PI*.15,Math.PI*.85);g.stroke()}\n  else if(o.happy){\",1);open(p,'w').write(s)"
