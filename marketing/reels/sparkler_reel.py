#!/usr/bin/env python3
"""9 s "New festive arrivals · Coming soon" teaser, timed like the reference trend reel: Kala Kari logo on deep
maroon, the hand with a gold ring and kada (cut from the reference reel, assets/sparkler-hand.png) holds a
sparkler that lights and burns towards the fingers while
"New / festive / arrivals" fade in word by word, then "COMING SOON · STAY TUNED". Reference music.

Usage:
    python3 sparkler_reel.py <fonts_dir> <music.wav> <out.mp4> [4x5|9x16]
    python3 sparkler_reel.py <fonts_dir> preview <out_dir> <4x5|9x16> t1 t2 ...
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HAND = os.path.join(HERE, "assets", "sparkler-hand.png")
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-gold-flat.png")
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
FPS = 30
TOTAL = 9.0
W = 1080
BG = (71, 26, 25)                  # the reference's flat maroon, so the hand cut-out blends in
CREAM = (242, 230, 214)

T_LIGHT, T_OUT = .35, 6.6          # sparkler lights / burns out
X0, XE = 194, 650                  # burn point travels from the stick's tip towards the fingers
SILVER_END = 675                   # end of the sparkler coating; bare wire from here into the fingers
HAND_X, HAND_STICK_Y = 750, 103    # hand cut-out position and the stick's height inside it
WORDS = [("New", 1.1), ("festive", 2.7), ("arrivals", 5.0)]
T_SOON = 5.8


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ sparks
class Sparks:
    def __init__(self, seed=3):
        self.rng = np.random.default_rng(seed)
        self.p = np.zeros((0, 7))                 # x, y, vx, vy, age, life, kind

    def step(self, dt, x, y, rate):
        n = int(rate * dt + self.rng.uniform())
        if n:
            a = self.rng.uniform(0, 2 * np.pi, n)
            sp = self.rng.uniform(180, 760, n)
            life = self.rng.uniform(.12, .55, n)
            kind = (self.rng.uniform(size=n) < .25).astype(float)      # some crackle into a little star
            new = np.stack([np.full(n, x), np.full(n, y), np.cos(a) * sp, np.sin(a) * sp, np.zeros(n), life, kind], 1)
            self.p = np.vstack([self.p, new])
        p = self.p
        p[:, 0] += p[:, 2] * dt
        p[:, 1] += p[:, 3] * dt
        p[:, 3] += 520 * dt
        p[:, 2] *= .985
        p[:, 4] += dt
        self.p = p[p[:, 4] < p[:, 5]]

    def draw(self, lay):
        d = ImageDraw.Draw(lay)
        for x, y, vx, vy, age, life, kind in self.p:
            f = age / life
            col = (255, 250, 230) if f < .35 else ((255, 214, 130) if f < .7 else (240, 150, 70))
            a = int(255 * (1 - f) ** .6)
            tail = .028
            d.line((x, y, x - vx * tail, y - vy * tail), fill=col + (a,), width=2)
            if kind and .45 < f < .8:                                    # crackle star
                r = 7 * (1 - f) + 2
                for k in range(4):
                    ang = k * math.pi / 4 + x
                    d.line((x - r * math.cos(ang), y - r * math.sin(ang), x + r * math.cos(ang), y + r * math.sin(ang)),
                           fill=(255, 236, 190, a), width=1)


# ------------------------------------------------------------------ reel
class Reel:
    def __init__(self, fonts_dir, fmt="4x5"):
        self.H = 1350 if fmt == "4x5" else 1920
        off = 0 if fmt == "4x5" else (1920 - 1350) // 2
        self.y_logo, self.y_text, self.y_stick, self.y_soon = 255 + off, 528 + off, 742 + off, 1066 + off
        self.hand = Image.open(HAND).convert("RGBA")
        self.hand_pos = (HAND_X, int(self.y_stick - HAND_STICK_Y))
        cor = ImageFont.truetype(os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files",
                                              "cormorant-garamond-latin-500-normal.woff2"), 74)
        self.font = cor
        widths = [cor.getlength(wd) for wd, _ in WORDS]
        space = cor.getlength(" ")
        total = sum(widths) + space * (len(WORDS) - 1)
        x = W / 2 - total / 2
        self.word_x = []
        for wdt in widths:
            self.word_x.append(x)
            x += wdt + space
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo.resize((420, int(420 * logo.height / logo.width)), Image.LANCZOS)
        self.soon_font = ImageFont.truetype(INTER.format("Regular"), 27)
        self.sparks = Sparks()
        self.last_t = 0.0
        self.base = Image.new("RGBA", (W, self.H), BG + (255,))
        self.base.alpha_composite(self.logo, ((W - self.logo.width) // 2, int(self.y_logo - self.logo.height / 2)))

    def burn_x(self, t):
        return X0 + (XE - X0) * clamp((t - T_LIGHT) / (T_OUT - T_LIGHT)) ** 1.05

    def frame(self, t):
        img = self.base.copy()
        d = ImageDraw.Draw(img)
        y = self.y_stick
        bx = self.burn_x(t)
        lit = T_LIGHT <= t < T_OUT
        # stick: charred wire left of the burn point, silver coating to the right
        if t >= T_LIGHT:
            d.line((X0 - 4, y, bx, y), fill=(34, 26, 26), width=3)
        d.line((bx if t >= T_LIGHT else X0, y, SILVER_END, y), fill=(196, 192, 188), width=7)
        d.line((bx if t >= T_LIGHT else X0, y - 2, SILVER_END, y - 2), fill=(232, 230, 226), width=2)
        d.line((SILVER_END, y, HAND_X + 20, y), fill=(120, 116, 112), width=3)
        # sparks + glow
        dt = max(1 / FPS, t - self.last_t) if t > self.last_t else 1 / FPS
        self.last_t = t
        rate = 0 if not lit else 900 * ease((t - T_LIGHT) / .35) * (1 - ease((t - (T_OUT - .5)) / .5))
        self.sparks.step(dt, bx, y, rate)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        self.sparks.draw(lay)
        if lit:
            dl = ImageDraw.Draw(lay)
            fl = 1 + .15 * math.sin(t * 47) + .1 * math.sin(t * 23)
            for r, a in ((46, 40), (22, 120), (10, 255)):
                rr = r * fl
                dl.ellipse((bx - rr, y - rr, bx + rr, y + rr), fill=(255, 236 if r > 10 else 252, 190 if r > 10 else 240, a))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
        img.alpha_composite(lay)
        img.alpha_composite(self.hand, self.hand_pos)
        # words, each fading in at its final place in the centred line
        for (word, t0), x in zip(WORDS, self.word_x):
            a = ease((t - t0) / .35)
            if a > 0:
                tl = Image.new("RGBA", img.size, (0, 0, 0, 0))
                ImageDraw.Draw(tl).text((x, self.y_text), word, font=self.font, fill=CREAM + (int(255 * a),), anchor="lm")
                img.alpha_composite(tl)
        a = ease((t - T_SOON) / .4)
        if a > 0:
            tl = Image.new("RGBA", img.size, (0, 0, 0, 0))
            txt = "COMING SOON   ·   STAY TUNED"
            ImageDraw.Draw(tl).text((W / 2, self.y_soon), txt, font=self.soon_font, fill=CREAM + (int(235 * a),), anchor="mm")
            img.alpha_composite(tl)
        return img


def render(fonts_dir, music, out, fmt):
    r = Reel(fonts_dir, fmt)
    n = int(TOTAL * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{r.H}",
           "-r", str(FPS), "-i", "-", "-i", music, "-t", f"{TOTAL:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        proc.stdin.write(r.frame(k / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    print(out)


if __name__ == "__main__":
    if sys.argv[2] == "preview":
        fonts_dir, _, out_dir, fmt = sys.argv[1:5]
        times = sorted(map(float, sys.argv[5:]))
        r = Reel(fonts_dir, fmt)
        t, k = 0.0, 0
        while k < len(times):                    # run the spark simulation up to each preview time
            fr = r.frame(t)
            if t >= times[k] - 1e-6:
                fr.convert("RGB").resize((W // 3, r.H // 3)).save(os.path.join(out_dir, f"sp_{times[k]:04.1f}.png"))
                k += 1
            t += 1 / FPS
    else:
        render(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "4x5")
