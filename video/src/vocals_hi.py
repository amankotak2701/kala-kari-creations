"""Hindi kid-voice lead vocal for 'Ek Nanha Haathi'.
Words are spoken by AI4Bharat's Indic-TTS Hindi voice (MIT licence), then
split into syllables and re-timed / re-pitched / formant-shifted (child-like)
with the WORLD vocoder.

  python3 vocals_hi.py words  words.json            # list of words to synthesize
  python3 vocals_hi.py sing   <wavdir> vocals.wav    # build the vocal track
"""
import sys, json, hashlib
import numpy as np

ns = {}
exec(open('music.py').read().split("if __name__ != '__main__'")[0], ns)
VERSE, bt, SR, BEAT = ns['VERSE'], ns['bt'], ns['SR'], ns['BEAT']

NUM = ['एक', 'दो', 'तीन', 'चार', 'पाँच']
# (word, syllables)
def verse_words(n):
    pl = n > 1
    l1 = [(NUM[n - 1], 1), ('नन्हे' if pl else 'नन्हा', 2), ('हाथी', 2), ('खेलने', 2), ('को', 1), ('चले' if pl else 'चला', 2)]
    l2 = [('मकड़ी', 2), ('के', 1), ('जाले', 2), ('पर', 1), ('झूलने', 2)]
    if n < 5:
        l3 = [('खूब', 1), ('मज़ा', 2), ('आया', 2), ('उन्हें' if pl else 'उसे', 2)]
        l4 = ([('दूसरे', 2), ('हाथी', 2), ('को', 1), ('उसने', 2), ('बुला', 2), ('लिया', 2)] if n == 1 else
              [('एक', 1), ('और', 1), ('हाथी', 2), ('को', 1), ('उन्होंने', 3), ('बुलाया', 3)])
    else:
        l3 = [('उछले', 2), ('कूदे', 2), ('खूब', 1), ('मज़ा', 2)]
        l4 = [('पर', 1), ('जाला', 2), ('खिंचता', 2), ('गया', 2), ('खिंचता', 2), ('गया', 2)]
    return [l1, l2, l3, l4]

FINALE = [
    (52, 2, [('धम्म', 1), ('से', 1), ('गिर', 1), ('गए', 2), ('सारे', 2)]),
    (54, 3, [('फूलों', 2), ('पे', 1), ('गिरे', 2), ('हँसते', 2), ('रहे', 2), ('हुर्रे', 2)]),
]
TAG_WORDS = [('हुर्रे', 2), ('हुर्रे', 2), ('हाथी', 2), ('भाई', 2)]
SPLIT = {0: [1] * 9 + [2], 1: [1] * 7 + [2], 2: [1, 1, 1, 1, 2, 2, 1], 3: [1] * 11}

def all_words():
    ws = []
    for v in range(5):
        for line in verse_words(v + 1):
            ws += [w for w, _ in line]
    for _, _, line in FINALE:
        ws += [w for w, _ in line]
    ws += [w for w, _ in TAG_WORDS]
    return sorted(set(ws))

def fname(w):
    return hashlib.md5(w.encode()).hexdigest()[:10] + '.wav'

if sys.argv[1] == 'words':
    json.dump([[w, fname(w)] for w in all_words()], open(sys.argv[2], 'w'), ensure_ascii=False)
    print(len(all_words()), 'words'); sys.exit()

# ------------------------------------------------------------------ sing
import pyworld as pw
from scipy.io import wavfile
from scipy.signal import resample_poly, butter, sosfilt
WAVDIR, OUT = sys.argv[2], sys.argv[3]
FP = 5.0
TRANSPOSE = 0          # sing at the melody's own (child) range F4-A5
FORMANT = 1.17         # >1 shifts formants up: smaller vocal tract = child-like
VSR = 22050

def warp_env(sp, a):
    nb = sp.shape[1]; src = np.arange(nb) / a
    out = np.empty_like(sp)
    for i in range(len(sp)):
        out[i] = np.interp(src, np.arange(nb), sp[i])
    return out

_cache = {}
def speak(word):
    if word not in _cache:
        sr, x = wavfile.read(f'{WAVDIR}/{fname(word)}')
        x = x.astype(np.float64)
        if x.ndim > 1: x = x.mean(1)
        x /= np.abs(x).max() + 1e-9
        if sr != VSR: raise SystemExit(f'rate {sr}')
        e = np.convolve(np.abs(x), np.ones(220) / 220, 'same')
        idx = np.where(e > e.max() * 0.06)[0]
        x = x[max(0, idx[0] - 110): idx[-1] + 220]
        f0, t = pw.harvest(x, VSR, frame_period=FP, f0_floor=80, f0_ceil=600)
        sp = pw.cheaptrick(x, f0, t, VSR); ap = pw.d4c(x, f0, t, VSR)
        sp = warp_env(sp, FORMANT)
        en = np.log(sp.sum(1) + 1e-12)
        _cache[word] = (f0, sp, ap, en)
    return _cache[word]

def split_word(word, n):
    f0, sp, ap, en = speak(word)
    T = len(f0)
    if n == 1:
        return [(f0, sp, ap)]
    sm = np.convolve(en, np.ones(7) / 7, 'same')
    cuts = []
    for i in range(1, n):
        c = int(T * i / n)
        lo = max(cuts[-1] + 6 if cuts else 4, c - T // (2 * n)); hi = min(T - 4, c + T // (2 * n))
        if hi <= lo: cuts.append(c); continue
        score = sm[lo:hi] - 3.0 * (f0[lo:hi] == 0)
        cuts.append(lo + int(np.argmin(score)))
    b = [0] + cuts + [T]
    return [(f0[b[i]:b[i + 1]], sp[b[i]:b[i + 1]], ap[b[i]:b[i + 1]]) for i in range(n)]

def hzv(semi):
    return 349.23 * 2 ** ((semi + TRANSPOSE) / 12)

def sing_syllable(seg, notes, t_start):
    f0, sp, ap = seg
    T = len(f0); fs = FP / 1000
    v = np.where(f0 > 0)[0]
    if len(v) < 2:
        v = np.arange(T // 3, max(T // 3 + 2, 2 * T // 3))
    on, off = v[0], v[-1] + 1
    on_n = min(on, int(0.10 / fs)); coda_n = min(T - off, int(0.09 / fs))
    D = sum(d for _, d in notes) * 0.9
    vow_n = max(8, int(D / fs) - coda_n)
    src = np.concatenate([np.arange(on - on_n, on), np.linspace(on, off - 1, vow_n), np.arange(off, off + coda_n)])
    si = np.clip(np.round(src).astype(int), 0, T - 1)
    sp2 = sp[si].copy(); ap2 = ap[si].copy()
    voiced = np.zeros(len(si), bool); voiced[on_n:on_n + vow_n] = True
    tt = (np.arange(len(si)) - on_n) * fs
    bounds = []; acc = 0
    for semi, d in notes:
        bounds.append((acc, semi)); acc += d
    lt = np.log([hzv(next(s for a, s in reversed(bounds) if a <= max(x, 0))) for x in tt])
    k = max(1, int(0.03 / fs)); lt = np.convolve(np.pad(lt, (k, k), 'edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
    vib = 0.015 * np.sin(2 * np.pi * 6.0 * tt) * np.clip((tt - 0.22) / 0.2, 0, 1)
    scoop = -0.03 * np.exp(-np.clip(tt, 0, None) / 0.04)
    f = np.exp(lt + vib + scoop) * voiced
    y = pw.synthesize(np.ascontiguousarray(f), np.ascontiguousarray(sp2), np.ascontiguousarray(ap2), VSR, FP)
    fade = int(0.025 * VSR); y[-fade:] *= np.linspace(1, 0, fade)
    return y, t_start - on_n * fs

N = int(121.8 * SR)
voc = np.zeros(N)
def place(y, t):
    y = resample_poly(y, 2 * SR // 100, 2 * VSR // 100)
    i = int(t * SR)
    if i < 0: y = y[-i:]; i = 0
    y = y[:N - i]; voc[i:i + len(y)] += y

def line_notes(bar0, pair):
    out = []
    for b, li in enumerate(pair):
        beat = 0
        for semi, d in VERSE[li]:
            if semi is not None: out.append((semi, bt(bar0 + b, beat), d * BEAT))
            beat += d
    return out

def sing_segments(segs, split, notes):
    assert len(segs) == len(split) and sum(split) == len(notes), (len(segs), len(split), sum(split), len(notes))
    k = 0
    for seg, c in zip(segs, split):
        nn = notes[k:k + c]; k += c
        y, t = sing_syllable(seg, [(s, d) for s, _, d in nn], nn[0][1]); place(y, t)

def sing_line(bar0, ml, words):
    segs = []
    for w, n in words: segs += split_word(w, n)
    sing_segments(segs, SPLIT[ml], line_notes(bar0, (2 * ml, 2 * ml + 1)))

for v, b0 in enumerate([6, 14, 24, 34, 42]):
    for li, words in enumerate(verse_words(v + 1)):
        sing_line(b0 + 2 * li, li, words)
for b0, ml, words in FINALE:
    sing_line(b0, ml, words)
TAG = [[(9, 1), (11, 1), (12, 1), (14, 1)], [(16, 1), (14, .5), (12, .5), (12, 2)]]
notes = []
for b, line in enumerate(TAG):
    beat = 0
    for semi, d in line:
        notes.append((semi, bt(56 + b, beat), d * BEAT * (1.4 if (b, beat) == (1, 2) else 1))); beat += d
segs = []
for w, n in TAG_WORDS: segs += split_word(w, n)
sing_segments(segs, [1] * 8, notes)

voc = sosfilt(butter(2, 120, 'high', fs=SR, output='sos'), voc)
voc /= np.abs(voc).max() + 1e-9
wavfile.write(OUT, SR, (voc * 0.9 * 32767).astype(np.int16))
print('ok')
