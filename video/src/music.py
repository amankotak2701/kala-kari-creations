"""Original instrumental for 'One Little Elephant' (Popcorn Productions).
Melody, arrangement and sounds are all generated here from scratch.
Timeline: 140 BPM (beat 0.4285 s), first downbeat at 0.115 s, length 121.8 s."""
import numpy as np, sys
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
BEAT = 0.4285
T0 = 0.115
DUR = 121.8
N = int(DUR * SR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)


def bt(bar, beat=0.0):
    return T0 + (bar * 4 + beat) * BEAT


KEY = 392.0  # G major; the vocal sings one octave below the lead (G3-G4, natural female range)
def hz(semi, base=KEY):  # semitones above the tonic
    return base * 2 ** (semi / 12)


def add(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= N or i + len(sig) <= 0:
        return
    if i < 0:
        sig = sig[-i:]; i = 0
    sig = sig[: N - i] * gain
    lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * lg * 1.414
    R[i:i + len(sig)] += sig * rg * 1.414


def env(n, a=0.005, d=0.3, s=0.0, r=0.05, hold=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    dec = s + (1 - s) * np.exp(-(t - a).clip(0) / d)
    e = e * dec
    if hold is not None:
        rel = np.clip((t - hold) / r, 0, 1)
        e *= 1 - rel
    return e


def toy_piano(f, dur):
    n = int((dur + 0.6) * SR); t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6)
         + 0.18 * np.sin(2 * np.pi * 4.02 * f * t) * np.exp(-t * 12))
    return s * env(n, 0.003, 0.45, 0.0, 0.08, hold=dur + 0.4)


def flute(f, dur):
    n = int((dur + 0.15) * SR); t = np.arange(n) / SR
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / 0.25, 0, 1)
    ph = 2 * np.pi * f * np.cumsum(vib) / SR
    s = np.sin(ph) + 0.2 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    s += 0.02 * rng.standard_normal(n)
    return s * env(n, 0.04, 10, 0.9, 0.12, hold=dur)


def tuba(f, dur):
    n = int((dur + 0.1) * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * f * t
    s = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 7))
    sos = butter(2, 900, 'low', fs=SR, output='sos')
    s = sosfilt(sos, s)
    return s * env(n, 0.02, 0.35, 0.35, 0.08, hold=dur)


def pluck(f, dur=0.9):  # Karplus-Strong ukulele-ish
    n = int(dur * SR); p = int(SR / f)
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * np.exp(-np.arange(n) / SR * 2.5)


_pl = {}
def pluck_c(f):
    k = round(f, 2)
    if k not in _pl:
        _pl[k] = pluck(f)
    return _pl[k]


def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare():
    n = int(0.25 * SR); t = np.arange(n) / SR
    nz = sosfilt(butter(2, [1500, 8000], 'band', fs=SR, output='sos'), rng.standard_normal(n))
    return (0.7 * nz * np.exp(-t * 18) + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25))


def shaker():
    n = int(0.08 * SR); t = np.arange(n) / SR
    nz = sosfilt(butter(2, 6000, 'high', fs=SR, output='sos'), rng.standard_normal(n))
    return nz * np.minimum(1, t / 0.01) * np.exp(-t * 50)


def crash():
    n = int(2.5 * SR); t = np.arange(n) / SR
    nz = sosfilt(butter(2, 3000, 'high', fs=SR, output='sos'), rng.standard_normal(n))
    return nz * np.exp(-t * 1.6)


def glide(f0, f1, dur, kind='sine'):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) if kind == 'sine' else sum(np.sin(k * ph) / k for k in range(1, 8))
    return s * env(n, 0.02, 10, 1, 0.1, hold=dur - 0.1)


def trumpet_call(t):  # cartoon elephant "paaa"
    for f0, f1, st, d in [(330, 440, 0, 0.35), (440, 523, 0.38, 0.9)]:
        s = glide(f0, f1, d, 'saw')
        s = sosfilt(butter(2, 2500, 'low', fs=SR, output='sos'), s)
        add(s, t + st, 0.2, 0.22)


def splash(t):
    n = int(1.2 * SR); tt = np.arange(n) / SR
    nz = sosfilt(butter(2, [400, 5000], 'band', fs=SR, output='sos'), rng.standard_normal(n))
    add(nz * np.exp(-tt * 4) * np.minimum(1, tt / 0.02), t, 0, 0.35)
    for k in range(6):
        add(glide(500 + 300 * k, 1400 + 200 * k, 0.07) * 0.5, t + 0.05 + k * 0.09, (-1) ** k * 0.4, 0.12)


# ---------------- harmony ----------------
CH = {  # chord tones (semitones above F4), bass root
    'F': ([0, 4, 7], -12), 'Bb': ([5, 9, 12], -7), 'C': ([-5, -1, 2], -5),
    'Dm': ([-3, 0, 4], -3), 'Gm': ([2, 5, 9], -10), 'C7': ([-5, -2, 2], -5),
}

# melody: (semitone or None, beats)
VERSE = [
    [(7, 1), (4, .5), (4, .5), (7, 1), (4, .5), (0, .5)],
    [(2, .5), (4, .5), (5, .5), (4, .5), (2, 2)],
    [(9, 1), (7, .5), (7, .5), (5, 1), (4, .5), (4, .5)],
    [(2, 1), (4, 1), (0, 2)],
    [(4, 1), (7, 1), (12, 1), (9, 1)],
    [(7, .5), (4, .5), (5, .5), (2, .5), (7, 2)],
    [(4, .5), (4, .5), (5, .5), (5, .5), (7, .5), (7, .5), (9, .5), (9, .5)],
    [(11, .5), (11, .5), (12, 2), (None, 1)],
]
VCH = ['F', 'C', 'Bb', 'C7', 'F', 'C', 'Bb', 'F']


def play_melody(bar0, lines, inst='piano', gain=0.22, octave=0):
    for b, line in enumerate(lines):
        beat = 0
        for semi, d in line:
            if semi is not None:
                t = bt(bar0 + b, beat); f = hz(semi + octave)
                if inst in ('piano', 'both'):
                    add(toy_piano(f, d * BEAT * .9), t, 0.15, gain)
                if inst in ('flute', 'both'):
                    add(flute(f, d * BEAT * .92), t, -0.15, gain * (0.5 if inst == 'both' else 1))
            beat += d


def band(bar0, chords, drums=True, uke=True, bass=True, energy=1.0):
    for b, c in enumerate(chords):
        tones, root = CH[c]
        for beat in range(4):
            t = bt(bar0 + b, beat)
            if bass:
                semi = root if beat in (0, 2) else root + 7
                add(tuba(hz(semi - 12 + 12), BEAT * .55), t, 0, 0.28 * energy)
            if uke and beat in (1, 3):
                for k, s in enumerate(tones):
                    add(pluck_c(hz(s)), t + k * 0.012, 0.35, 0.16 * energy)
            if drums:
                if beat in (0, 2):
                    add(kick(), t, 0, 0.55 * energy)
                if beat in (1, 3):
                    add(snare(), t, 0, 0.22 * energy)
                for h in (0, .5):
                    add(shaker(), t + h * BEAT, -0.4, (0.09 if h else 0.06) * energy)


def lyric_verse(bar0, energy=1.0, inst='both'):
    band(bar0, VCH, energy=energy)
    play_melody(bar0, VERSE, inst, 0.17)


if __name__ != '__main__':
    raise ImportError('song data only')
# ---------------- arrangement ----------------
# intro: bars 0-5
band(0, ['F', 'Bb', 'C', 'F'], drums=False)
band(4, ['Bb', 'C7'], energy=.8)
for b, c in enumerate(['F', 'Bb', 'C', 'F', 'Bb', 'C7']):  # arpeggio hook
    tones, _ = CH[c]
    for k in range(8):
        add(toy_piano(hz(tones[k % 3] + 12), BEAT * .4), bt(b, k * .5), -0.3, 0.09)
add(glide(300, 900, 0.6), bt(5, 3) - 0.1, 0, 0.12)  # whoosh-up into verse
# verses
lyric_verse(6, 0.85, 'piano')                    # V1 10.4-24.1
trumpet_call(21.15)
lyric_verse(14, 1.0, 'both')                     # V2 24.1-37.8
splash(30.0)
# interlude 22-23 (water)
band(22, ['Bb', 'C7'])
for k in range(8):
    add(toy_piano(hz(12 + [0, 4, 7, 12, 7, 4, 2, -1][k]), .2), bt(22, k), 0.3, 0.12)
lyric_verse(24, 1.0, 'both')                     # V3 41.2-55.0
band(32, ['Gm', 'C7'])                           # interlude 55-58.4
for k in range(8):
    add(flute(hz([9, 7, 5, 4, 2, 4, 5, 7][k]), BEAT * .9), bt(32, k), -0.2, 0.14)
lyric_verse(34, 1.05, 'both')                    # V4 Holi 58.4-72.1
for k in range(6):
    add(glide(400, 1600, 0.25), 59 + k * 2.1, (-1) ** k * .5, 0.06)
lyric_verse(42, 1.1, 'both')                     # V5 72.1-85.8
# bridge: tension 50-51, snap at bar 51 beat 2 (~88.4)
band(50, ['Dm'], energy=1.1)
for k in range(8):
    add(toy_piano(hz(12 + k), .18), bt(50, k * .5), 0, 0.12)  # chromatic climb
for k in range(2):
    add(kick(), bt(51, k), 0, 0.6)
    add(snare(), bt(51, k + .5), 0, 0.25)
add(tuba(hz(-11), BEAT * 1.6), bt(51, 0), 0, 0.3)
add(crash(), bt(51, 2), 0, 0.35)
add(kick(), bt(51, 2), 0, 0.8)
add(glide(1400, 180, 1.4), bt(51, 2) + 0.05, 0, 0.16)    # slide-whistle fall
for k in range(3):
    add(kick() * .7, bt(51, 2) + 0.6 + k * 0.22, 0, 0.35 - k * .08)  # bumps landing
# finale bars 52-57 (lines 3-4 + tag)
band(52, ['F', 'C', 'Bb', 'F'], energy=1.15)
play_melody(52, VERSE[4:8], 'both', 0.18)
band(56, ['Bb', 'C7'], energy=1.15)
play_melody(56, [[(9, 1), (11, 1), (12, 1), (14, 1)], [(16, 1), (14, .5), (12, .5), (12, 2)]], 'both', 0.18)
add(crash(), bt(58, 0), 0, 0.25)
add(kick(), bt(58, 0), 0, 0.6)
add(tuba(hz(-12), 1.2), bt(58, 0), 0, 0.3)
for k, s in enumerate([0, 4, 7, 12]):
    add(toy_piano(hz(s + 12), 1.5), bt(58, 0) + k * .03, 0, 0.12)
# end card: gentle music-box verse bars 59-66, outro 67-69
band(59, VCH, drums=False, bass=False, energy=.7)
play_melody(59, VERSE, 'piano', 0.16, 12)
for b, c in enumerate(['F', 'Bb', 'F']):
    tones, _ = CH[c]
    for k in range(8):
        add(toy_piano(hz(tones[k % 3] + 12), BEAT * .5), bt(67 + b, k * .5), 0.3 - k * .08, 0.08)

# ---------------- mix ----------------
mix = np.stack([L, R], 1)
# small room reverb
ir_n = int(1.4 * SR); it = np.arange(ir_n) / SR
ir = rng.standard_normal((ir_n, 2)) * np.exp(-it * 4.5)[:, None]
ir = sosfilt(butter(1, 4000, 'low', fs=SR, output='sos'), ir, axis=0)
wet = np.stack([fftconvolve(mix[:, c], ir[:, c])[:N] for c in range(2)], 1)
wet *= np.abs(mix).max() / (np.abs(wet).max() + 1e-9) * 0.35
mix = mix + wet
fade = np.ones(N); fn = int(2.0 * SR); fade[-fn:] = np.linspace(1, 0, fn)
mix *= fade[:, None]
mix = np.tanh(mix / np.abs(mix).max() * 1.4) * 0.89
from scipy.io import wavfile
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print('ok', mix.shape)
