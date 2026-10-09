"""Original soft background music for the reels (no samples, royalty-free).

Tanpura-style drone + warm pad + gentle bell melody in D major pentatonic,
with a simple convolution reverb. write_track(path, seconds, seed) -> wav.
"""
import wave

import numpy as np

SR = 48000
BPM = 72
BEAT = 60 / BPM

D3 = 146.83
# D major pentatonic (Sa Re Ga Pa Dha), semitones from D
PENTA = [0, 2, 4, 7, 9]


def hz(semi, base=D3):
    return base * 2 ** (semi / 12)


def env(n, attack, release):
    e = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    if a:
        e[:a] = np.linspace(0, 1, a) ** 2
    if r:
        e[-r:] *= np.linspace(1, 0, r) ** 2
    return e


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # one-pole; fine for short clips
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def tanpura_pluck(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    tone = sum((0.9 ** k) * np.sin(2 * np.pi * f * k * t * (1 + 0.0007 * k)) / k for k in range(1, 12))
    # jawari buzz: slow swelling of upper partials
    buzz = sum(np.sin(2 * np.pi * f * k * t) for k in range(6, 14)) * 0.03 * np.minimum(t / 0.8, 1)
    return (tone + buzz) * np.exp(-t / 2.2) * env(n, 0.01, 0.3)


def pad_note(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * d * t + p) for d, p in ((1, 0), (1.003, 1.1), (0.997, 2.3)))
    x += 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return x * env(n, dur * 0.4, dur * 0.4) / 3


def bell(f, dur=2.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2.01 * f * t) * np.exp(-t / 0.4)
    x += 0.08 * np.sin(2 * np.pi * 3.0 * f * t) * np.exp(-t / 0.2)
    return x * np.exp(-t / 0.9) * env(n, 0.006, 0.2)


def add(buf, x, start):
    i = int(start * SR)
    j = min(len(buf), i + len(x))
    if i < len(buf):
        buf[i:j] += x[: j - i]


def reverb(x, seconds=2.4, mix=0.3, seed=1):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (seconds / 5))
    ir[: int(0.02 * SR)] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    wet = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return (1 - mix) * x + mix * wet


def write_track(path, seconds, seed=0):
    rng = np.random.default_rng(seed)
    n = int((seconds + 3) * SR)
    drone, pad, mel = np.zeros(n), np.zeros(n), np.zeros(n)

    # Tanpura cycle: Pa Sa Sa Sa(low)
    t, cycle = 0.0, [hz(-5), hz(0), hz(0), hz(-12)]
    while t < seconds + 1:
        for f in cycle:
            add(drone, tanpura_pluck(f, 4.0), t)
            t += BEAT * 1.0

    # Pad: D - Bm - G6 - Asus2 colours, two bars each
    chords = [[0, 7, 16], [-3, 4, 12], [-7, 2, 12], [-5, 2, 9]]
    bar = BEAT * 4
    t, k = 0.0, 0
    while t < seconds + 1:
        for s in chords[k % 4]:
            add(pad, pad_note(hz(s), bar * 2 + 1.0), t)
        t += bar * 2
        k += 1

    # Melody: gentle pentatonic phrases, a different one per seed
    notes = [hz(PENTA[i % 5] + 12 * (i // 5)) for i in range(5, 13)]
    t, idx = BEAT * 4, 3
    while t < seconds - 1.5:
        for _ in range(int(rng.integers(3, 6))):
            idx = int(np.clip(idx + rng.choice([-2, -1, 1, 1, 2]), 0, len(notes) - 1))
            add(mel, bell(notes[idx]) * rng.uniform(0.7, 1.0), t)
            t += BEAT * float(rng.choice([1, 1, 1.5, 2]))
        t += BEAT * 2  # breathe between phrases

    mix = 0.30 * lowpass(drone, 2500) + 0.45 * lowpass(pad, 1400) + 0.32 * mel
    mix = reverb(mix, seed=seed + 1)[: int(seconds * SR)]
    mix *= env(len(mix), 1.5, 2.5)
    mix *= 10 ** (-3 / 20) / (np.max(np.abs(mix)) + 1e-9)  # peak -3 dBFS

    # Slight stereo width: delayed copy on the right
    d = int(0.012 * SR)
    left, right = mix, np.concatenate([np.zeros(d), mix[:-d]]) * 0.95 + mix * 0.05
    pcm = (np.stack([left, right], axis=1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
