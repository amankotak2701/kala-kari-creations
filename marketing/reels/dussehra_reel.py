#!/usr/bin/env python3
"""Happy Dussehra greeting reel for Instagram (1080x1920, ~18 s) with original dhol + shehnai music.

Scenes: शुभ दशहरा greeting (bow & arrow, fireworks, diyas, toran) -> Jaipuri / Chikankari / Kutchi
collections -> website / follow / contact end card. Re-uses the Navratri reel's art and layout.

Usage:
    python3 dussehra_reel.py <fonts_dir> <out.mp4>
"""
import math
import os
import random
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import music as M  # noqa: E402
import navratri_reel as N  # noqa: E402

W, H, FPS = N.W, N.H, N.FPS
GOLD, GOLD_B, CREAM = N.GOLD, N.GOLD_B, N.CREAM
XF = 0.6
T_COLL = 4.8
COLL_DUR = 3.3
T_END = T_COLL + 3 * (COLL_DUR - XF)
TOTAL = T_END + 5.2
fade, ease = N.fade, N.ease


def bow_and_arrow(size=520):
    """Gold line-art bow with a flaming arrow, the symbol of Ram's victory."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = size / 2
    col = GOLD_B + (255,)
    # bow: arc on the left, string on the right
    d.arc((c - 230, c - 230, c + 60, c + 230), 100, 260, fill=col, width=9)
    top = (c - 85 + 145 * math.cos(math.radians(260)) * 0 + 5, c - 226)
    bot = (top[0], c + 226)
    d.line([top, bot], fill=GOLD + (230,), width=3)
    for y in (c - 226, c + 226):
        d.ellipse((top[0] - 10, y - 10, top[0] + 10, y + 10), fill=col)
    # arrow
    d.line([(c - 200, c), (c + 200, c)], fill=col, width=7)
    d.polygon([(c + 235, c), (c + 185, c - 24), (c + 196, c), (c + 185, c + 24)], fill=col)
    for k in range(3):
        x = c - 200 + k * 18
        d.line([(x, c), (x - 26, c - 26)], fill=col, width=5)
        d.line([(x, c), (x - 26, c + 26)], fill=col, width=5)
    glow = img.filter(ImageFilter.GaussianBlur(10))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(glow)
    out.alpha_composite(img)
    return out


class Fireworks:
    def __init__(self, seed=4):
        r = random.Random(seed)
        self.bursts = []
        for k in range(14):
            self.bursts.append(dict(t=k * .55 + r.random() * .3, x=r.uniform(140, W - 140), y=r.uniform(260, 820),
                                    col=r.choice([GOLD_B, (255, 170, 60), (255, 120, 90), (250, 230, 170)]),
                                    n=r.randint(22, 34), r=r.uniform(120, 200)))

    def draw(self, img, t, alpha=1.0, period=8.0):
        d = ImageDraw.Draw(img)
        tt = t % period
        for b in self.bursts:
            age = tt - b["t"]
            if not 0 <= age < 1.6:
                continue
            p = ease(age / 1.1)
            a = max(0.0, 1 - age / 1.6) * alpha
            for i in range(b["n"]):
                ang = 2 * math.pi * i / b["n"]
                rr = b["r"] * p
                x = b["x"] + rr * math.cos(ang)
                y = b["y"] + rr * math.sin(ang) + 40 * age * age
                s = 5 * (1 - age / 1.6) + 1.5
                d.ellipse((x - s, y - s, x + s, y + s), fill=b["col"] + (int(255 * a),))
                tx, ty = b["x"] + rr * .8 * math.cos(ang), b["y"] + rr * .8 * math.sin(ang) + 30 * age * age
                d.line([(tx, ty), (x, y)], fill=b["col"] + (int(120 * a),), width=2)


class Dussehra(N.Reel):
    def __init__(self, fonts_dir):
        super().__init__(fonts_dir)
        self.bow = bow_and_arrow()
        self.fw = Fireworks()

    def greeting(self, t):
        img = self.festive_base(t, mandala_alpha=.6)
        self.fw.draw(img, t, fade(t, .1, .6))
        self.spark.draw(img, t, fade(t, .2, 1.2))
        img.alpha_composite(self.toran, (0, int(-230 + 230 * ease(t / .9))))
        a = fade(t, .2, .9)
        s = .85 + .15 * ease(t / 1.2)
        bow = self.bow.resize((int(520 * s), int(520 * s)), Image.BICUBIC)
        bow.putalpha(bow.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(bow, ((W - bow.width) // 2, 470 + (520 - bow.height) // 2))
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        tw = dl.textlength("शुभ दशहरा", font=self.hi)
        dl.text(((W - tw) / 2, 1010), "शुभ दशहरा", font=self.hi, fill=GOLD_B)
        al = fade(t, .5, 1.0)
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * al)))
        img.alpha_composite(layer)
        self.text(img, (W / 2, 1185), "Happy Dussehra", self.f.cor_it(600, 132), CREAM, fade(t, 1.0, .9),
                  rise=int(30 * (1 - fade(t, 1.0, .9))))
        self.text(img, (W / 2, 1345), "May goodness always win", self.f.cor_it(500, 54), GOLD, fade(t, 1.6))
        self.text(img, (W / 2, 1425), "WITH LOVE FROM KALA KARI CREATIONS", self.f.cinzel(600, 28), CREAM, fade(t, 2.1), tracking=4)
        self.diyas(img, t, a=fade(t, .3, 1.0))
        return img

    def end(self, local):
        img = super().end(local)
        self.fw.draw(img, local + 3, .55)
        return img

    def frame(self, t):
        layers = []
        if t < T_COLL + XF:
            layers.append((0.0, lambda: self.greeting(t)))
        for i in range(3):
            s = T_COLL + i * (COLL_DUR - XF)
            if s <= t < s + COLL_DUR:
                layers.append((s, lambda i=i, s=s: self.collection(i, t - s)))
        if t >= T_END:
            layers.append((T_END, lambda: self.end(t - T_END)))
        if len(layers) == 1:
            return layers[0][1]()
        (sa, fa), (sb, fb) = layers[-2], layers[-1]
        return Image.blend(fa(), fb(), ease((t - sb) / XF))


# ------------------------------------------------------------------ music
def dussehra_track(path, seconds, seed=31):
    """Festive but warm: tanpura drone, dhol groove in 4/4, a shehnai-like reed melody and a pad."""
    sr = M.SR
    rng = np.random.default_rng(seed)
    n = int((seconds + 3) * sr)
    drone, pad, reed, perc = (np.zeros(n) for _ in range(4))
    beat = 60 / 100

    t = 0.0
    while t < seconds + 1:
        for f in (M.hz(-5), M.hz(0), M.hz(0), M.hz(-12)):
            M.add(drone, M.tanpura_pluck(f, 4.0), t)
            t += beat
    t, k = 0.0, 0
    chords = [[0, 7, 16], [5, 9, 12], [-5, 2, 11], [0, 4, 7]]
    while t < seconds + 1:
        for s_ in chords[k % 4]:
            M.add(pad, M.pad_note(M.hz(s_), beat * 8 + .6), t)
        t += beat * 8
        k += 1

    def dhol_low(dur=.5):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        f = 100 * np.exp(-tt * 6) + 52
        return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 8)

    def dhol_high(dur=.22):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        return (np.sin(2 * np.pi * 350 * tt) * .5 + np.sin(2 * np.pi * 560 * tt) * .25 + rng.standard_normal(m) * .3) * np.exp(-tt * 30)

    def jhanj(dur=.6):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        x = sum(np.sin(2 * np.pi * f * tt) for f in (3100, 4630, 6020, 7710)) * .25
        return (x + rng.standard_normal(m) * .2) * np.exp(-tt * 7)

    start = beat * 4
    t = start
    bar = 0
    while t < seconds - beat * 2:
        for pos, kind in ((0, 'L'), (1, 'H'), (1.5, 'L'), (2, 'L'), (3, 'H'), (3.5, 'H')):
            M.add(perc, dhol_low() * .9 if kind == 'L' else dhol_high() * .55, t + pos * beat)
        for e in range(4):
            M.add(perc, jhanj(.25) * (.22 if e % 2 else .32), t + e * beat)
        if bar % 4 == 3:
            for r in range(4):
                M.add(perc, dhol_high() * .45, t + 3 * beat + r * beat / 4)
        t += beat * 4
        bar += 1
    perc *= M.env(n, 1.0, 0)

    def shehnai(f, dur):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        vib = 1 + .009 * np.sin(2 * np.pi * 5.8 * tt) * np.minimum(tt / .2, 1)
        ph = 2 * np.pi * np.cumsum(f * vib) / sr
        x = sum((0.8 ** h) * np.sin(h * ph) for h in range(1, 9))  # bright, nasal reed
        return x * M.env(m, .05, min(.2, dur * .35)) * .35

    scale = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]  # Bilawal (major)
    notes = [M.hz(s_ + 12) for s_ in scale]
    phrase = [4, 5, 7, 5, 4, 2, 4, 5, 4, 2, 1, 0, 2, 4, 5, 4, 7, 8, 7, 5, 4]
    durs = [1, .5, 1.5, .5, .5, 1, 2, .5, .5, 1, .5, 1.5, 1, .5, .5, 1, 1, .5, .5, 1, 2]
    t = beat * 2
    i = 0
    while t < seconds - 1.5:
        d_ = beat * durs[i % len(durs)]
        M.add(reed, shehnai(notes[phrase[i % len(phrase)]], d_ * 1.08), t)
        t += d_
        i += 1
        if i % len(phrase) == 0:
            t += beat * 2

    mix = .22 * M.lowpass(drone, 2500) + .22 * M.lowpass(pad, 1400) + .26 * M.lowpass(reed, 4200) + .34 * perc
    mix = M.reverb(mix, seconds=1.8, mix=.2, seed=seed)[: int(seconds * sr)]
    mix *= M.env(len(mix), .8, 2.0)
    mix *= 10 ** (-3 / 20) / (np.max(np.abs(mix)) + 1e-9)
    d = int(.012 * sr)
    left, right = mix, np.concatenate([np.zeros(d), mix[:-d]]) * .95 + mix * .05
    pcm = (np.stack([left, right], axis=1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main():
    fonts_dir, out = sys.argv[1:3]
    r = Dussehra(fonts_dir)
    n = int(TOTAL * FPS)
    wav = os.path.join(tempfile.mkdtemp(), "dussehra.wav")
    dussehra_track(wav, n / FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        proc.stdin.write(r.frame(k / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    print(out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
