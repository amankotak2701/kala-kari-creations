"""Stage B: tune each FastPitch-sung line to the exact melody in the child register."""
import json, sys
import numpy as np, pyworld as pw
from scipy.io import wavfile
from scipy.signal import resample_poly, butter, sosfilt
FP = 5.0; VSR = 22050; SR = 44100
FORMANT = float(sys.argv[2]) if len(sys.argv) > 2 else 1.12
meta = json.load(open('fp_meta.json')); KEY = meta['key']
N = int(121.8 * SR); voc = np.zeros(N)
rng = np.random.default_rng(5)

def warp_env(sp, a):
    nb = sp.shape[1]; src = np.arange(nb) / a; out = np.empty_like(sp)
    for i in range(len(sp)): out[i] = np.interp(src, np.arange(nb), sp[i])
    return out

def smooth(x, k):
    k = max(1, k); return np.convolve(np.pad(x, (k, k), 'edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')

for L in meta['lines']:
    sr, x = wavfile.read(L['file']); x = x.astype(np.float64) / 32768
    f0, t = pw.harvest(x, VSR, frame_period=FP, f0_floor=100, f0_ceil=500)
    sp = pw.cheaptrick(x, f0, t, VSR); ap = pw.d4c(x, f0, t, VSR)
    voiced = f0 > 0
    # close tiny unvoiced gaps (<30ms) inside sung vowels
    gap = 0
    for i in range(len(voiced)):
        if not voiced[i]: gap += 1
        else:
            if 0 < gap <= 6 and i - gap > 0 and voiced[i - gap - 1]: voiced[i - gap:i] = True
            gap = 0
    tabs = L['t0'] + t
    notes = [n for g in L['groups'] for n in g]
    starts = np.array([n[1] for n in notes]); semis = np.array([n[0] for n in notes])
    idx = np.clip(np.searchsorted(starts, tabs + 0.02, 'right') - 1, 0, len(notes) - 1)
    lt = np.log(KEY * 2 ** (semis[idx] / 12))
    lt = smooth(lt, int(0.03 / (FP / 1000)))           # portamento between notes
    # vibrato: grows on long notes, slightly irregular rate
    since = tabs - starts[idx]; dur = np.array([n[2] for n in notes])[idx]
    rate = 5.6 + 0.4 * np.sin(tabs * 0.7)
    vib = 0.012 * np.sin(2 * np.pi * np.cumsum(rate) * FP / 1000) * np.clip((since - 0.25) / 0.25, 0, 1) * (dur > 0.5)
    # keep the voice's own micro-intonation (jitter / phrasing), toned down
    fo = np.where(f0 > 0, f0, np.nan)
    lf = np.log(np.where(np.isnan(fo), np.nanmedian(fo), fo))
    micro = np.clip((lf - smooth(lf, 12)) * 0.6, -0.04, 0.04)
    drift = smooth(rng.standard_normal(len(t)) * 0.02, 40)
    f_new = np.exp(lt + vib + micro + drift) * voiced
    sp2 = warp_env(sp, FORMANT)
    ap2 = ap.copy(); ap2[voiced] = np.minimum(1, ap2[voiced] * 1.0)
    y = pw.synthesize(f_new, sp2, ap2, VSR, FP)
    y = resample_poly(y, 2, 1)
    i0 = int(L['t0'] * SR); y = y[:N - i0]
    fade = int(0.02 * SR); y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
    voc[i0:i0 + len(y)] += y
voc = sosfilt(butter(2, 120, 'high', fs=SR, output='sos'), voc)
voc /= np.abs(voc).max() + 1e-9
wavfile.write(sys.argv[1], SR, (voc * 0.9 * 32767).astype(np.int16)); print('ok')
