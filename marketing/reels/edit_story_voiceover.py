#!/usr/bin/env python3
"""New narration for the "new edit" reel, read by the open-source Kokoro TTS voice (Apache-2.0) and placed in the
same time slots as the reference reel's voiceover, over a soft original music bed (electric piano, pad, bass), then
muxed onto the rendered video. Indian words are given as phonemes so they are pronounced correctly.

Usage:
    python3 edit_story_voiceover.py <kokoro_dir> <video.mp4> <out.mp4>
<kokoro_dir> holds kokoro-v1.0.onnx and voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases).
"""
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import music as M  # noqa: E402

VOICE, LANG, SPEED = "am_michael", "en-us", 0.92
SR_OUT = 48000
TOTAL = 19.92
# (slot start, slot end, line) -- slots measured from the reference voiceover; "/.../" lines are phonemes
LINES = [(0.25, 0.95, "The invite says"),
         (1.5, 2.75, "wedding season."),
         (3.5, 4.6, "The dress code says"),
         (5.5, 6.4, "unforgettable."),
         (7.25, 7.95, "/sʌŋɡˈiːt nˈaɪt./"),            # "Sung-geet"
         (8.5, 9.35, "/pˈuːdʒɑː mˈɔːɹnɪŋ./"),          # "Poojaa"
         (10.25, 10.95, "/hˈʌldiː dˈeɪ./"),             # "Hul-dee"
         (11.6, 12.6, "Roka evening."),
         (13.5, 14.1, "Every piece,"),
         (14.5, 15.9, "hand-embroidered in Jaipur."),
         (16.6, 17.15, "Shop at"),
         (17.5, 18.9, "/kˈɑːlɑː kˈɑːɹiː kɹiːˈeɪʃənz./")]


def trim(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    return x[max(0, idx[0] - 240): idx[-1] + 960] if len(idx) else x


def soft_bed(seconds):
    """Soft, light music bed: slow broken electric-piano chords, a low pad and a gentle bass (D - Bm - G - A)."""
    sr = M.SR
    n = int((seconds + 3) * sr)
    keys, pad, bass = np.zeros(n), np.zeros(n), np.zeros(n)
    beat = .75
    f = lambda semi: M.D3 * 2 ** (semi / 12)  # noqa: E731

    def epiano(fr, dur, amp):
        k_ = int(dur * sr)
        x = np.arange(k_) / sr
        y = np.sin(2 * np.pi * fr * x) + .25 * np.sin(4 * np.pi * fr * x) * np.exp(-x * 3)
        y *= np.exp(-x * 1.1)
        y[: int(.008 * sr)] *= np.linspace(0, 1, int(.008 * sr))
        return y * M.env(k_, 0, .25) * amp

    chords = [([0, 4, 7, 11], -12), ([-3, 2, 6, 9], -15), ([-5, 2, 7, 11], -17), ([-3, 4, 7, 9], -10)]
    t, b = 0.0, 0
    while t < seconds:
        semis, root = chords[b % 4]
        for s_ in semis:
            M.add(pad, M.pad_note(f(s_), beat * 4 + .8) * .5, t)
        k_ = int((beat * 4 + .5) * sr)
        M.add(bass, np.sin(2 * np.pi * f(root) * np.arange(k_) / sr) * M.env(k_, .05, .6) * .7, t)
        for e, idx in enumerate([0, 1, 2, 3, 2, 1, 2, 1]):
            M.add(keys, epiano(f(semis[idx] + 12), 1.6, .8 if e % 2 else .9), t + e * beat / 2)
        t += beat * 4
        b += 1
    mix = .34 * M.lowpass(keys, 1800) + .3 * M.lowpass(pad, 900) + .3 * M.lowpass(bass, 400)
    mix = M.reverb(mix, seconds=2.4, mix=.28)[: int(seconds * sr)]
    mix *= M.env(len(mix), 1.0, 2.0)
    return (mix / (np.abs(mix).max() + 1e-9)).astype(np.float32)


def main():
    kdir, video, out = sys.argv[1:4]
    k = Kokoro(os.path.join(kdir, "kokoro-v1.0.onnx"), os.path.join(kdir, "voices-v1.0.bin"))
    track = np.zeros(int(TOTAL * SR_OUT), np.float32)
    for i, (s, e, text) in enumerate(LINES):
        ph = text.startswith("/")
        audio, sr = k.create(text.strip("/") if ph else text, voice=VOICE, speed=SPEED, lang=LANG, is_phonemes=ph)
        audio = trim(np.asarray(audio, np.float32))
        tmp_in, tmp_out = f"{out}.{i}.in.wav", f"{out}.{i}.out.wav"
        sf.write(tmp_in, audio, sr)
        slot = (e - s) + .25                           # may run a little into the following pause
        dur = len(audio) / sr
        tempo = min(1.25, max(1.0, dur / slot))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_in, "-af", f"atempo={tempo:.3f}",
                        "-ar", str(SR_OUT), "-ac", "1", tmp_out], check=True)
        seg, _ = sf.read(tmp_out, dtype="float32")
        os.remove(tmp_in)
        os.remove(tmp_out)
        a = int(s * SR_OUT)
        b = min(len(track), a + len(seg))
        track[a:b] += seg[: b - a]
        print(f"{text!r}: {dur:.2f}s in a {e - s:.2f}s slot, tempo {tempo:.2f}")
    track /= np.abs(track).max() + 1e-9
    # soft music bed well under the voice, dipping a little more while he speaks
    bed = soft_bed(TOTAL)[: len(track)]
    env = np.convolve(np.abs(track), np.ones(SR_OUT // 5) / (SR_OUT // 5), "same")
    duck = 1 - .35 * np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
    mix = track + bed * 10 ** (-17 / 20) * duck
    mix *= 10 ** (-1.5 / 20) / (np.abs(mix).max() + 1e-9)
    wav = out + ".vo.wav"
    sf.write(wav, np.stack([mix, mix], 1).astype(np.float32), SR_OUT)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", out],
                   check=True)
    os.remove(wav)
    print(out)


if __name__ == "__main__":
    main()
