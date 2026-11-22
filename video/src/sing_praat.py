"""Stage B (natural adult voice): gently tune each FastPitch-sung line onto the
melody (one octave below the lead) with Praat's PSOLA, keeping natural timbre."""
import json, sys
import numpy as np, parselmouth
from parselmouth.praat import call
from scipy.io import wavfile
from scipy.signal import resample_poly, butter, sosfilt
SR = 44100
meta = json.load(open('fp_meta.json')); KEY = meta['key'] / 2
N = int(121.8 * SR); voc = np.zeros(N)
def smooth(x, k):
    return np.convolve(np.pad(x, (k, k), 'edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
for L in meta['lines']:
    snd = parselmouth.Sound(L['file'])
    man = call(snd, 'To Manipulation', 0.01, 75, 600)
    pitch = snd.to_pitch(time_step=0.01, pitch_floor=75, pitch_ceiling=600)
    ts = pitch.xs(); f = pitch.selected_array['frequency']
    v = f > 0
    if v.sum() < 3: continue
    lf = np.log(np.where(v, f, np.median(f[v])))
    micro = np.clip((lf - smooth(lf, 8)) * 0.5, -0.03, 0.03)
    notes = [n for g in L['groups'] for n in g]
    starts = np.array([n[1] for n in notes]); semis = np.array([n[0] for n in notes]); durs = np.array([n[2] for n in notes])
    tabs = L['t0'] + ts
    idx = np.clip(np.searchsorted(starts, tabs + 0.02, 'right') - 1, 0, len(notes) - 1)
    lt = smooth(np.log(KEY * 2 ** (semis[idx] / 12)), 3)
    since = tabs - starts[idx]
    vib = 0.01 * np.sin(2 * np.pi * 5.3 * since) * np.clip((since - 0.3) / 0.3, 0, 1) * (durs[idx] > 0.6)
    tgt = np.exp(lt + micro + vib)
    tier = call('Create PitchTier', 'p', snd.xmin, snd.xmax)
    for t_, hz_, ok in zip(ts, tgt, v):
        if ok: call(tier, 'Add point', float(t_), float(hz_))
    call([tier, man], 'Replace pitch tier')
    out = call(man, 'Get resynthesis (overlap-add)')
    y = out.values[0]
    y = resample_poly(y, 2, 1)
    i0 = int(L['t0'] * SR); y = y[:N - i0]
    fd = int(0.015 * SR); y[:fd] *= np.linspace(0, 1, fd); y[-fd:] *= np.linspace(1, 0, fd)
    voc[i0:i0 + len(y)] += y
voc = sosfilt(butter(2, 100, 'high', fs=SR, output='sos'), voc)
voc /= np.abs(voc).max() + 1e-9
wavfile.write(sys.argv[1], SR, (voc * 0.9 * 32767).astype(np.int16)); print('ok')
