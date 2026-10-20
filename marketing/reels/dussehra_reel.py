#!/usr/bin/env python3
"""Happy Dussehra greeting reel for Instagram (1080x1920, ~18 s) with original soft bansuri, tabla and tanpura music.

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

# Different pieces from the same three collections than the Navratri reel used.
N.COLLECTIONS = [
    ("black3piececottondress.jpg", .5, .36, "Jaipuri Prints", "Classic black 3-piece dress"),
    ("chikankari_2_piece_sky_blue.jpg", .5, .4, "Lucknowi Chikankari", "Sky blue chikankari suit"),
    ("kutchiprintshirt2.jpg", .45, .4, "Kutchi Work", "Hand block-printed Kutchi shirt"),
]
N.COLL_DUR = COLL_DUR


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
    """Soft Indian: tanpura drone, gentle tabla keherwa and a bansuri melody in raag Yaman with meend
    (glides between notes). No bells or pentatonic runs."""
    sr = M.SR
    rng = np.random.default_rng(seed)
    n = int((seconds + 3) * sr)
    drone, pad, flute, tabla = (np.zeros(n) for _ in range(4))
    beat = 60 / 84
    sa = M.D3  # tonic

    # tanpura: Pa Sa Sa Sa(low), slow
    t = 0.0
    while t < seconds + 1:
        for f in (M.hz(-5), M.hz(0), M.hz(0), M.hz(-12)):
            M.add(drone, M.tanpura_pluck(f, 4.5), t)
            t += beat * 1.5
    # very quiet sustained Sa-Pa bed
    m = int((seconds + 1) * sr)
    tt = np.arange(m) / sr
    bed = (np.sin(2 * np.pi * sa * tt) + .6 * np.sin(2 * np.pi * sa * 1.5 * tt) + .3 * np.sin(2 * np.pi * sa * 2 * tt))
    pad[:m] += bed * M.env(m, 2.0, 2.0) * .25

    # tabla (keherwa: dha ge na ti | na ka dhi na)
    def dayan(f0, dur, damp):
        k = int(dur * sr)
        x = np.arange(k) / sr
        partials = ((1, 1.0), (2, .55), (3, .32), (4, .18), (5, .08))
        y = sum(a * np.sin(2 * np.pi * f0 * h * x) * np.exp(-x * damp * (1 + .35 * h)) for h, a in partials)
        y += M.lowpass(rng.standard_normal(k), 2500) * np.exp(-x * 120) * .15
        return y

    def bayan(dur=.5, bend=True):
        k = int(dur * sr)
        x = np.arange(k) / sr
        f = 85 + (25 * (1 - np.exp(-x * 9)) if bend else 0)
        return np.sin(2 * np.pi * np.cumsum(np.full(k, 1.0) * f) / sr) * np.exp(-x * 7)

    f_tabla = sa * 2

    def mixb(*parts):
        k = max(len(x) for x in parts)
        out = np.zeros(k)
        for x in parts:
            out[:len(x)] += x
        return out

    bols = {"dha": lambda: mixb(dayan(f_tabla, .45, 9) * .6, bayan() * .8),
            "ge": lambda: bayan(.45) * .8,
            "na": lambda: dayan(f_tabla, .4, 10) * .65,
            "ti": lambda: dayan(f_tabla * 1.5, .15, 40) * .4,
            "ka": lambda: bayan(.12, False) * .35,
            "dhi": lambda: mixb(dayan(f_tabla, .5, 7) * .5, bayan() * .7)}
    theka = ["dha", "ge", "na", "ti", "na", "ka", "dhi", "na"]
    t = beat * 4
    while t < seconds - beat * 2:
        for k_, bol in enumerate(theka):
            M.add(tabla, bols[bol]() * (1.0 if k_ in (0, 6) else .8), t + k_ * beat / 2)
        t += beat * 4
    tabla *= M.env(n, 1.5, 0)

    # bansuri with meend: pitch glides between notes, delayed vibrato, breath
    def bansuri_line(events, start):
        total = sum(d for _, d in events) * beat
        k = int(total * sr)
        f = np.zeros(k)
        amp = np.zeros(k)
        pos = 0
        prev = None
        for semi, d in events:
            seg = int(d * beat * sr)
            target = sa * 2 * 2 ** (semi / 12)
            g = min(int(.09 * sr), seg // 3)
            if prev is None:
                f[pos:pos + seg] = target
            else:
                f[pos:pos + g] = np.linspace(prev, target, g)
                f[pos + g:pos + seg] = target
            x = np.arange(seg) / sr
            vib = 1 + .006 * np.sin(2 * np.pi * 5.0 * x) * np.clip((x - .25) / .3, 0, 1)
            f[pos:pos + seg] *= vib
            a = np.ones(seg)
            a[: int(.04 * sr)] = np.linspace(.55, 1, int(.04 * sr))
            amp[pos:pos + seg] = a
            pos += seg
            prev = target
        ph = 2 * np.pi * np.cumsum(f) / sr
        y = np.sin(ph) + .12 * np.sin(2 * ph) + .04 * np.sin(3 * ph)
        breath = M.lowpass(rng.standard_normal(k), 2500) * .06
        y = (y + breath) * amp * M.env(k, .15, .4)
        M.add(flute, y, start)
        return total

    # raag Yaman: N R G M# P D N S'
    phrases = [
        [(-1, 1), (2, 1), (4, 2), (2, .5), (0, 2.5)],
        [(4, 1), (6, 1), (9, 1.5), (7, .5), (6, 1), (4, 2.5)],
        [(6, .5), (9, .5), (11, 1), (12, 2), (11, .5), (9, .5), (7, 1), (6, .5), (4, 2)],
        [(2, 1), (4, .5), (2, .5), (-1, 1), (0, 3)],
    ]
    t = beat * 2
    k_ = 0
    while t < seconds - 2.5:
        t += bansuri_line(phrases[k_ % len(phrases)], t) + beat * 1.0
        k_ += 1

    mix = .30 * M.lowpass(drone, 2200) + .14 * M.lowpass(pad, 900) + .32 * M.lowpass(flute, 3200) + .24 * M.lowpass(tabla, 4000)
    mix = M.reverb(mix, seconds=2.2, mix=.24, seed=seed)[: int(seconds * sr)]
    mix *= M.env(len(mix), 1.0, 2.2)
    mix *= 10 ** (-5 / 20) / (np.max(np.abs(mix)) + 1e-9)
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
