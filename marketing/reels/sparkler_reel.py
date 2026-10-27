#!/usr/bin/env python3
"""9 s "New festive arrivals · Coming soon" teaser, timed like the reference trend reel: Kala Kari logo on deep
maroon, a hand with a gold ring and kada holds a sparkler that lights and burns towards the fingers while
"New / festive / arrivals" fade in word by word, then "COMING SOON · STAY TUNED". Own artwork; reference music.

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
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-gold-flat.png")
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
FPS = 30
TOTAL = 9.0
W = 1080
BG = (70, 24, 26)
CREAM = (242, 230, 214)

T_LIGHT, T_OUT = .35, 6.6          # sparkler lights / burns out
X0, XE = 170, 600                  # burn point travels from the stick's tip towards the fingers
STICK_END = 722                    # where the fingers pinch the stick
WORDS = [("New", 1.1), ("festive", 2.7), ("arrivals", 5.0)]
T_SOON = 5.8


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ the hand (drawn once)
def draw_hand(h=270):
    """Back of a hand pointing left, index finger and thumb pinching a stick at the left tip. Built from a smoothed
    silhouette with soft shading, a gold kundan ring and a kada. Returns (image, stick y inside the image)."""
    ss = 3
    w = int(h * 1.42)
    k = ss * h / 300
    S = (w * ss, h * ss)

    def P(pts):
        return [(x * k, y * k) for x, y in pts]

    def finger(d, pts, width, fill=255):
        d.line(P(pts), fill=fill, width=int(width * k), joint="curve")
        for x, y in (pts[0], pts[-1]):
            r = width / 2
            d.ellipse(((x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k), fill=fill)

    def smooth(mask, r=5):
        return mask.filter(ImageFilter.GaussianBlur(r * ss)).point(lambda v: 255 if v > 118 else 0).filter(ImageFilter.GaussianBlur(ss * .7))

    # silhouettes: hand (back, index, curled fingers, wrist) and thumb separately so it can overlap
    hand = Image.new("L", S, 0)
    dh = ImageDraw.Draw(hand)
    dh.polygon(P([(300, 110), (430, 104), (430, 256), (300, 244)]), fill=255)
    dh.polygon(P([(118, 110), (172, 94), (292, 100), (318, 142), (312, 224), (240, 240), (150, 228), (112, 178)]), fill=255)
    finger(dh, [(150, 124), (96, 126), (52, 134), (22, 146)], 34)
    for cx, cy, r in ((150, 222, 27), (192, 236, 27), (234, 241, 25), (272, 236, 23)):
        dh.ellipse(((cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k), fill=255)
    hand = smooth(hand)
    thumb = Image.new("L", S, 0)
    finger(ImageDraw.Draw(thumb), [(170, 212), (120, 206), (74, 192), (40, 174)], 31)
    thumb = smooth(thumb, 4)

    def paint(mask, top, bottom, y0, y1):
        g = np.clip((np.arange(S[1]) / k - y0) / (y1 - y0), 0, 1)[:, None, None]
        col = np.array(top) * (1 - g) + np.array(bottom) * g
        im = Image.fromarray(np.repeat(col, S[0], axis=1).astype(np.uint8)).convert("RGBA")
        im.putalpha(mask)
        return im

    out = Image.new("RGBA", S, (0, 0, 0, 0))
    out.alpha_composite(paint(hand, (236, 184, 152), (196, 134, 104), 100, 250))
    # definition: darker rim inside the edge, light along the top of the knuckles
    rim = np.clip(np.asarray(hand, np.int16) - np.asarray(hand.filter(ImageFilter.MinFilter(int(6 * k) | 1)), np.int16), 0, 255)
    ri = Image.new("RGBA", S, (150, 92, 70, 0))
    ri.putalpha(Image.fromarray((rim * .45).astype(np.uint8)).filter(ImageFilter.GaussianBlur(ss)))
    out.alpha_composite(ri)
    hl = Image.new("RGBA", S, (0, 0, 0, 0))
    dl = ImageDraw.Draw(hl)
    dl.ellipse(P([(150, 100), (300, 128)])[0] + P([(150, 100), (300, 128)])[1], fill=(250, 210, 182, 60))
    for x in (178, 216, 254):
        dl.ellipse(((x - 13) * k, 108 * k, (x + 13) * k, 122 * k), fill=(252, 216, 190, 150))
    dl.ellipse(P([(40, 128), (130, 140)])[0] + P([(40, 128), (130, 140)])[1], fill=(250, 210, 182, 110))
    hl = hl.filter(ImageFilter.GaussianBlur(7 * ss))
    hl.putalpha(Image.fromarray(np.minimum(np.asarray(hl.getchannel("A")), np.asarray(hand))))
    out.alpha_composite(hl)
    d = ImageDraw.Draw(out)
    # separations between the curled fingers
    for cx in (171, 213, 253):
        d.arc(((cx - 22) * k, 214 * k, (cx + 22) * k, 262 * k), 250, 300, fill=(150, 90, 68, 190), width=int(2.2 * k))
    # thumb on top, with a soft contact shadow
    ts = Image.new("RGBA", S, (120, 60, 44, 0))
    ts.putalpha(thumb.filter(ImageFilter.GaussianBlur(5 * ss)).point(lambda v: int(v * .5)))
    out.alpha_composite(ts, (0, int(4 * k)))
    out.alpha_composite(paint(thumb, (226, 170, 140), (198, 136, 106), 168, 222))
    trim = np.clip(np.asarray(thumb, np.int16) - np.asarray(thumb.filter(ImageFilter.MinFilter(int(5 * k) | 1)), np.int16), 0, 255)
    tr = Image.new("RGBA", S, (150, 92, 70, 0))
    tr.putalpha(Image.fromarray((trim * .5).astype(np.uint8)))
    out.alpha_composite(tr)
    d = ImageDraw.Draw(out)
    # nails
    d.ellipse(((8) * k, 136 * k, 30 * k, 156 * k), fill=(240, 202, 192))
    d.ellipse(((26) * k, 164 * k, 46 * k, 182 * k), fill=(236, 198, 188))
    # gold kundan ring on the index finger
    gold, gold_d = (224, 178, 84), (156, 108, 38)

    def cap(x, y, r, fill):
        d.ellipse(((x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k), fill=fill)
    d.rounded_rectangle((96 * k, 112 * k, 108 * k, 146 * k), radius=int(4 * k), fill=gold)
    cap(102, 108, 17, gold_d)
    cap(102, 108, 14, gold)
    for a in range(8):
        cap(102 + 9.5 * math.cos(a * math.pi / 4), 108 + 9.5 * math.sin(a * math.pi / 4), 3.8, (250, 246, 232))
    cap(102, 108, 4.6, (186, 36, 58))
    # gold kada with a ruby and pearls
    d.rounded_rectangle((334 * k, 96 * k, 364 * k, 262 * k), radius=int(10 * k), fill=gold)
    d.rounded_rectangle((334 * k, 96 * k, 342 * k, 262 * k), radius=int(4 * k), fill=gold_d)
    for y in range(106, 256, 15):
        cap(367, y, 4.2, (250, 244, 228))
    d.rounded_rectangle((340 * k, 156 * k, 358 * k, 200 * k), radius=int(6 * k), fill=(172, 24, 48))
    d.rounded_rectangle((344 * k, 162 * k, 351 * k, 176 * k), radius=int(3 * k), fill=(234, 124, 134))
    im = out.resize((w, h), Image.LANCZOS)
    shadow = Image.new("RGBA", im.size, (20, 4, 6, 0))
    shadow.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * .45)))
    res = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    res.alpha_composite(shadow, (8, 14))
    res.alpha_composite(im)
    return res, 148 * h / 300


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
        self.hand, sy = draw_hand(270)
        self.hand_pos = (STICK_END - 14, int(self.y_stick - sy))
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
        v = np.linspace(-1, 1, W)[None, :] ** 2 + np.linspace(-1, 1, self.H)[:, None] ** 2
        vig = (np.clip(v / 2, 0, 1) * 70).astype(np.uint8)            # gentle vignette
        vl = Image.new("RGBA", (W, self.H), (30, 6, 8, 0))
        vl.putalpha(Image.fromarray(vig))
        self.base.alpha_composite(vl)
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
        d.line((bx if t >= T_LIGHT else X0, y, STICK_END - 70, y), fill=(196, 192, 188), width=7)
        d.line((bx if t >= T_LIGHT else X0, y - 2, STICK_END - 70, y - 2), fill=(232, 230, 226), width=2)
        d.line((STICK_END - 70, y, STICK_END + 4, y), fill=(120, 116, 112), width=3)
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
