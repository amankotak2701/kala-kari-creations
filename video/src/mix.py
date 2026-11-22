import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve
sr,m=wavfile.read('music_raw.wav');m=m.astype(float)/32768
_,v=wavfile.read('vocals.wav');v=v.astype(float)/32768
n=min(len(m),len(v));m=m[:n];v=v[:n]
# presence + gentle compression
pres=sosfilt(butter(2,[2000,5000],'band',fs=sr,output='sos'),v)
v=v+0.6*pres
env=np.convolve(np.abs(v),np.ones(441)/441,'same');g=1/(1+np.maximum(0,env-0.15)*2.5);v=v*g
# doubled voice for a soft 'kids chorus' feel
d=int(0.018*sr);dbl=np.zeros_like(v);dbl[d:]=v[:-d]
vs=np.stack([v+0.35*dbl,v+0.35*np.roll(dbl,int(0.009*sr))],1)
# reverb send
rng=np.random.default_rng(3);L=int(1.6*sr);t=np.arange(L)/sr
ir=rng.standard_normal((L,2))*np.exp(-t*3.5)[:,None];ir=sosfilt(butter(1,5000,'low',fs=sr,output='sos'),ir,axis=0)
wet=np.stack([fftconvolve(vs[:,c],ir[:,c])[:n] for c in range(2)],1);wet*=np.abs(vs).max()/np.abs(wet).max()*0.25
vs=vs+wet
# level: vocals ~4 dB over band where both present
mask=np.abs(v)>0.02
rv=np.sqrt((vs[mask]**2).mean());rm=np.sqrt((m[mask]**2).mean())
vs*=rm/rv*10**(4/20)
out=m+vs
out=np.tanh(out/np.abs(out).max()*1.3)*0.9
wavfile.write('song_raw.wav',sr,(out*32767).astype(np.int16));print('ok')
