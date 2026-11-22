"""Synthesized lead vocal for 'One Little Elephant'.
Each word is spoken by a CC0 Piper TTS voice (Kathleen), split into syllables,
then re-timed and re-pitched to the melody with the WORLD vocoder."""
import sys, wave, io
import numpy as np, pyworld as pw
from scipy.signal import resample_poly, butter, sosfilt
from piper import PiperVoice, SynthesisConfig

VOICE = sys.argv[1]; OUT = sys.argv[2]
ns = {}
exec(open('music.py').read().split("if __name__ != '__main__'")[0], ns)
VERSE, bt, SR = ns['VERSE'], ns['bt'], ns['SR']

voice = PiperVoice.load(VOICE)
VSR = voice.config.sample_rate
FP = 5.0  # WORLD frame period ms
TRANSPOSE = -12

_cache = {}
def speak(word):
    if word not in _cache:
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w:
            voice.synthesize_wav(word, w, syn_config=SynthesisConfig(length_scale=1.15, noise_scale=0.5, noise_w_scale=0.6))
        buf.seek(0)
        with wave.open(buf) as w:
            sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
        if sr != VSR:
            raise SystemExit(f'unexpected rate {sr}')
        # trim silence
        e = np.convolve(np.abs(x), np.ones(160) / 160, 'same')
        idx = np.where(e > e.max() * 0.06)[0]
        x = x[max(0, idx[0] - 80): idx[-1] + 160]
        f0, t = pw.harvest(x, VSR, frame_period=FP, f0_floor=70, f0_ceil=500)
        sp = pw.cheaptrick(x, f0, t, VSR); ap = pw.d4c(x, f0, t, VSR)
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
        c = int(T * i / n); lo, hi = max(cuts[-1] + 6 if cuts else 4, c - T // (2 * n)), min(T - 4, c + T // (2 * n))
        if hi <= lo:
            cuts.append(c); continue
        # prefer energy dips / unvoiced frames
        score = sm[lo:hi] - 3.0 * (f0[lo:hi] == 0)
        cuts.append(lo + int(np.argmin(score)))
    b = [0] + cuts + [T]
    return [(f0[b[i]:b[i + 1]], sp[b[i]:b[i + 1]], ap[b[i]:b[i + 1]]) for i in range(n)]


def hzv(semi):
    return 349.23 * 2 ** ((semi + TRANSPOSE) / 12)


def sing_syllable(seg, notes, t_start):
    """notes: list of (semi, dur_sec). Vowel onset lands on t_start."""
    f0, sp, ap = seg
    T = len(f0); fs = FP / 1000
    v = np.where(f0 > 0)[0]
    if len(v) < 2:
        v = np.arange(T // 3, max(T // 3 + 2, 2 * T // 3))
    on, off = v[0], v[-1] + 1
    on_n = min(on, int(0.12 / fs)); coda_n = min(T - off, int(0.10 / fs))
    D = sum(d for _, d in notes) * 0.9
    vow_n = max(8, int(D / fs) - coda_n)
    src = np.concatenate([np.arange(on - on_n, on), np.linspace(on, off - 1, vow_n), np.arange(off, off + coda_n)])
    si = np.clip(np.round(src).astype(int), 0, T - 1)
    sp2 = sp[si].copy(); ap2 = ap[si].copy()
    voiced = np.zeros(len(si), bool); voiced[on_n:on_n + vow_n] = True
    # pitch contour
    tt = (np.arange(len(si)) - on_n) * fs
    f = np.zeros(len(si)); acc = 0
    bounds = []
    for semi, d in notes:
        bounds.append((acc, semi)); acc += d
    target = np.array([hzv(semi) for semi in [next(s for a, s in reversed(bounds) if a <= max(x, 0)) for x in tt]])
    lt = np.log(target)
    k = max(1, int(0.035 / fs)); lt = np.convolve(np.pad(lt, (k, k), 'edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
    vib = 0.018 * np.sin(2 * np.pi * 5.5 * tt) * np.clip((tt - 0.25) / 0.2, 0, 1)
    scoop = -0.03 * np.exp(-np.clip(tt, 0, None) / 0.05)  # tiny scoop up into note
    f = np.exp(lt + vib + scoop) * voiced
    # fade amplitude: keep spectral envelope, shape ending
    y = pw.synthesize(np.ascontiguousarray(f), np.ascontiguousarray(sp2), np.ascontiguousarray(ap2), VSR, FP)
    fade = int(0.03 * VSR)
    y[-fade:] *= np.linspace(1, 0, fade)
    return y, t_start - on_n * fs


NUMS = ['One', 'Two', 'Three', 'Four', 'Five']
def verse_words(n):
    who = 'He' if n == 1 else 'They'
    l1 = [(NUMS[n - 1], 1), ('little', 2), ('elephant' if n == 1 else 'elephants', 3), ('went', 1), ('out', 1), ('to', 1), ('play', 1)]
    l2 = [('upon', 2), ('uh', 1), ("spider's", 2), ('web', 1), ('one', 1), ('day', 1)]
    if n < 5:
        l3 = [(who, 1), ('had', 1), ('such', 1), ('enormous', 3), ('fun', 1)]
        l4 = [(who, 1), ('called', 1), ('for', 1), ('another', 3), ('elephant', 3), ('to', 1), ('come', 1)]
    else:
        l3 = [('They', 1), ('bounced', 1), ('and', 1), ('bounced', 1), ('oh', 1), ('what', 1), ('fun', 1)]
        l4 = [('But', 1), ('the', 1), ('web', 1), ('went', 1), ('stretchy', 2), ('stretchy', 2), ('stretchy', 2), ('oh', 1)]
    return [l1, l2, l3, l4]

# notes-per-syllable for each melody line
SPLIT = {0: [1] * 9 + [2], 1: [1] * 7 + [2], 2: [1, 1, 1, 1, 2, 2, 1], 3: [1] * 11}

def line_notes(bar0, line_idx_pair):
    out = []
    for b, li in enumerate(line_idx_pair):
        beat = 0
        for semi, d in VERSE[li]:
            if semi is not None:
                out.append((semi, bt(bar0 + b, beat), d * ns['BEAT']))
            beat += d
    return out

N = int(121.8 * SR)
voc = np.zeros(N)

def place(y, t, gain=1.0):
    y = resample_poly(y, SR, VSR)
    i = int(t * SR)
    if i < 0:
        y = y[-i:]; i = 0
    y = y[:N - i]
    voc[i:i + len(y)] += y * gain

def sing_line(bar0, melody_line, words, split):
    notes = line_notes(bar0, (2 * melody_line, 2 * melody_line + 1))
    segs = []
    for w, n in words:
        segs += split_word(w, n)
    assert len(segs) == len(split), (words, len(segs), len(split))
    assert sum(split) == len(notes), (words, sum(split), len(notes))
    k = 0
    for seg, c in zip(segs, split):
        nn = notes[k:k + c]; k += c
        y, t = sing_syllable(seg, [(s, d) for s, _, d in nn], nn[0][1])
        place(y, t)

for v, b0 in enumerate([6, 14, 24, 34, 42]):
    for li, words in enumerate(verse_words(v + 1)):
        sing_line(b0 + 2 * li, li, words, SPLIT[li])
    print('verse', v + 1)
# finale (bars 52-55 use melody lines 3,4; 56-57 tag)
sing_line(52, 2, [('Down', 1), ('they', 1), ('tumbled', 2), ('one', 1), ('by', 1), ('one', 1)], SPLIT[2])
sing_line(54, 3, [('into', 2), ('the', 1), ('flowers', 2), ('all', 1), ('safe', 1), ('and', 1), ('sound', 1), ('hooray', 2)], SPLIT[3])
TAG = [[(9, 1), (11, 1), (12, 1), (14, 1)], [(16, 1), (14, .5), (12, .5), (12, 2)]]
tag_notes = []
for b, line in enumerate(TAG):
    beat = 0
    for semi, d in line:
        tag_notes.append((semi, bt(56 + b, beat), d * ns['BEAT'])); beat += d
segs = split_word('hooray', 2) + split_word('hooray', 2) + split_word('for', 1) + split_word('elephants', 3)
for seg, (s, t, d) in zip(segs, tag_notes):
    y, tt = sing_syllable(seg, [(s, d if t < bt(57, 2) else d * 1.4)], t)
    place(y, tt)

# gentle presence EQ + normalize
voc = sosfilt(butter(2, 90, 'high', fs=SR, output='sos'), voc)
voc /= np.abs(voc).max() + 1e-9
from scipy.io import wavfile
wavfile.write(OUT, SR, (voc * 0.9 * 32767).astype(np.int16))
print('ok')
