#!/usr/bin/env python3
"""New narration for the "new edit" reel, read by the open-source Kokoro TTS voice (Apache-2.0) and placed in the
same time slots as the reference reel's voiceover, then muxed onto the rendered video.

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

VOICE, LANG, SPEED = "am_michael", "en-us", 0.92
SR_OUT = 48000
TOTAL = 19.92
# (slot start, slot end, line) -- slots measured from the reference voiceover
LINES = [(0.25, 0.95, "The invite says"),
         (1.5, 2.75, "wedding season."),
         (3.5, 4.6, "The dress code says"),
         (5.5, 6.4, "unforgettable."),
         (7.25, 7.95, "Sangeet night."),
         (8.5, 9.35, "Puja morning."),
         (10.25, 10.95, "Haldi day."),
         (11.6, 12.6, "Roka evening."),
         (13.5, 14.1, "Every piece,"),
         (14.5, 15.9, "hand-embroidered in Jaipur."),
         (16.6, 17.15, "Shop at"),
         (17.5, 18.9, "Kala Kari Creations.")]


def trim(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    return x[max(0, idx[0] - 240): idx[-1] + 960] if len(idx) else x


def main():
    kdir, video, out = sys.argv[1:4]
    k = Kokoro(os.path.join(kdir, "kokoro-v1.0.onnx"), os.path.join(kdir, "voices-v1.0.bin"))
    track = np.zeros(int(TOTAL * SR_OUT), np.float32)
    for i, (s, e, text) in enumerate(LINES):
        audio, sr = k.create(text, voice=VOICE, speed=SPEED, lang=LANG)
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
    track *= 10 ** (-3 / 20) / (np.abs(track).max() + 1e-9)
    wav = out + ".vo.wav"
    sf.write(wav, np.stack([track, track], 1), SR_OUT)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", out],
                   check=True)
    os.remove(wav)
    print(out)


if __name__ == "__main__":
    main()
