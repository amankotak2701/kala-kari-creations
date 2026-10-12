#!/usr/bin/env python3
"""Navratri greeting + offer reel for Instagram (1080x1920, ~24 s) with original garba-style music.

Scenes: greeting (mandala, diyas, toran) -> Jaipuri / Chikankari / Kutchi collections ->
NAV10 offer -> shop / follow / contact end card.

Usage:
    python3 navratri_reel.py <fonts_dir> <out.mp4>
"""
import math
import os
import random
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ads"))
sys.path.insert(0, HERE)
import make_ads as A  # noqa: E402  (shared fonts / text helpers)
import music as M  # noqa: E402

W, H, FPS = 1080, 1920, 30
MAROON = (94, 28, 42)
MAROON_L = (128, 40, 58)
GOLD = (217, 188, 121)
GOLD_B = (236, 205, 130)
CREAM = (247, 242, 233)
SAFFRON = (240, 140, 40)
MARIGOLD = (250, 175, 30)
LEAF = (60, 120, 50)

PHOTOS = os.path.join(HERE, "..", "ads", "source-photos")
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-gold-flat.png")

# scene timing (seconds)
T_GREET, T_COLL, T_OFFER, T_END = 0.0, 4.6, 14.0, 19.0
TOTAL = 24.5
XF = 0.6
COLLECTIONS = [
    ("yellowjaipuri3piece.jpg", .5, .38, "Jaipuri Prints", "Hand block-printed 3-piece dresses"),
    ("muslin2piecechikankari.jpg", .5, .4, "Lucknowi Chikankari", "Hand-embroidered kurtis & suits"),
    ("ajrakhsilkkutchiprint.jpg", .5, .4, "Kutchi Work", "Ajrakh prints & mirror work"),
]
COLL_DUR = (T_OFFER - T_COLL + XF * 2) / 3


def ease(t):
    return A.ease(t)


def fade(t, start, dur=.7):
    return ease((t - start) / dur)


# ------------------------------------------------------------------ static art
def radial_bg():
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / W) ** 2 + ((y - H * .42) / H) ** 2)
    t = np.clip(d / .7, 0, 1)[..., None]
    a = np.array(MAROON_L, float) * (1 - t) + np.array((52, 14, 24), float) * t
    return Image.fromarray(a.astype("uint8")).convert("RGBA")


def mandala(size=1500):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = size / 2
    col = GOLD + (120,)
    for r in (720, 690, 560, 540, 400, 385, 250, 240, 120):
        d.ellipse((c - r, c - r, c + r, c + r), outline=col, width=3)
    for ring, n, rl, w in ((630, 36, 70, 30), (470, 24, 80, 34), (320, 16, 70, 30), (180, 12, 55, 24)):
        for k in range(n):
            a = 2 * math.pi * k / n
            petal = Image.new("RGBA", (w * 2 + 8, rl * 2 + 8), (0, 0, 0, 0))
            ImageDraw.Draw(petal).ellipse((4, 4, w * 2 + 4, rl * 2 + 4), outline=col, width=3)
            petal = petal.rotate(-math.degrees(a) + 90, expand=True, resample=Image.BICUBIC)
            px, py = c + ring * math.cos(a), c + ring * math.sin(a)
            img.alpha_composite(petal, (int(px - petal.width / 2), int(py - petal.height / 2)))
    for ring, n, rr in ((705, 72, 6), (548, 48, 7), (392, 32, 6), (245, 20, 5)):
        for k in range(n):
            a = 2 * math.pi * (k + .5) / n
            px, py = c + ring * math.cos(a), c + ring * math.sin(a)
            d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=GOLD + (150,))
    d.ellipse((c - 40, c - 40, c + 40, c + 40), fill=GOLD + (90,))
    return img


def toran(width=W):
    """Marigold garland swags with mango leaves across the top."""
    img = Image.new("RGBA", (width, 230), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    swags = 4
    sw = width / swags
    rng = random.Random(3)
    for s in range(swags):
        x0 = s * sw
        for k in range(26):
            u = k / 25
            x = x0 + u * sw
            y = 18 + 70 * math.sin(math.pi * u)
            r = 15 + rng.random() * 3
            colr = MARIGOLD if k % 3 else SAFFRON
            d.ellipse((x - r, y - r, x + r, y + r), fill=colr + (255,))
            d.ellipse((x - r * .45, y - r * .45, x + r * .45, y + r * .45), fill=(255, 210, 90, 255))
        # hanging leaf + bead at each swag joint
        jx = x0
        for dx in (-14, 0, 14):
            d.polygon([(jx + dx, 20), (jx + dx - 10, 70), (jx + dx, 110), (jx + dx + 10, 70)], fill=LEAF + (255,))
        d.ellipse((jx - 9, 112, jx + 9, 130), fill=SAFFRON + (255,))
    d.line((0, 14, width, 14), fill=GOLD + (255,), width=4)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.paste(Image.new("RGBA", img.size, (0, 0, 0, 90)), (0, 6), img)
    out = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), img)
    return out


def diya(t, phase):
    img = Image.new("RGBA", (160, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    flick = 1 + .08 * math.sin(t * 13 + phase) + .05 * math.sin(t * 23 + phase * 2)
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((30, 10, 130, 110), fill=(255, 170, 40, int(110 * flick)))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))
    fh = 46 * flick
    d.ellipse((66, 84 - fh, 94, 92), fill=(255, 196, 60, 255))
    d.ellipse((73, 88 - fh * .6, 87, 92), fill=(255, 245, 200, 255))
    d.chord((20, 70, 140, 150), 0, 180, fill=(165, 75, 35, 255))
    d.rectangle((20, 106, 140, 112), fill=(190, 95, 45, 255))
    d.arc((20, 70, 140, 150), 0, 180, fill=GOLD + (255,), width=3)
    return img


class Sparkles:
    def __init__(self, n=70, seed=7):
        r = random.Random(seed)
        self.p = [(r.random() * W, r.random() * H, r.uniform(2, 5), r.uniform(20, 60), r.random() * 6.28) for _ in range(n)]

    def draw(self, img, t, alpha=1.0):
        d = ImageDraw.Draw(img)
        for x, y, s, v, ph in self.p:
            yy = (y - v * t) % H
            a = (math.sin(t * 2.2 + ph) * .5 + .5) * alpha
            if a < .08:
                continue
            col = GOLD_B + (int(220 * a),)
            d.ellipse((x - s, yy - s, x + s, yy + s), fill=col)
            if s > 3.8:
                d.line((x - s * 2.5, yy, x + s * 2.5, yy), fill=col, width=1)
                d.line((x, yy - s * 2.5, x, yy + s * 2.5), fill=col, width=1)


# ------------------------------------------------------------------ renderer
class Reel:
    def __init__(self, fonts_dir):
        self.f = A.Fonts(fonts_dir)
        self.hi = ImageFont.truetype(os.path.join(fonts_dir, "fontsource-tiro", "package", "files",
                                                  "tiro-devanagari-hindi-devanagari-400-normal.woff2"),
                                     118, layout_engine=ImageFont.Layout.RAQM)
        self.bg = radial_bg()
        self.mandala = mandala()
        self.toran = toran()
        self.spark = Sparkles()
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo.resize((360, int(360 * logo.height / logo.width)), Image.LANCZOS)
        self.photos = {c[0]: Image.open(os.path.join(PHOTOS, c[0])).convert("RGB") for c in COLLECTIONS}

    def text(self, img, xy, s, font, fill, a=1.0, tracking=0, anchor="c", rise=0):
        if a <= 0:
            return
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        A.draw_text(ImageDraw.Draw(layer), (xy[0], xy[1] + rise), s, font, fill, tracking=tracking, anchor=anchor)
        if a < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(layer)

    def festive_base(self, t, mandala_y=760, mandala_alpha=1.0):
        img = self.bg.copy()
        m = self.mandala.rotate(t * 5, resample=Image.BICUBIC)
        if mandala_alpha < 1:
            m.putalpha(m.getchannel("A").point(lambda v: int(v * mandala_alpha)))
        img.alpha_composite(m, ((W - m.width) // 2, mandala_y - m.height // 2))
        return img

    def diyas(self, img, t, y=1690, a=1.0):
        for k, x in enumerate((140, 340, 540, 740, 940)):
            dy = diya(t, k * 1.7)
            if a < 1:
                dy.putalpha(dy.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(dy, (x - 80, y - 85 + (0 if k == 2 else 20)))

    def greeting(self, t):
        img = self.festive_base(t)
        self.spark.draw(img, t, fade(t, .2, 1.2))
        img.alpha_composite(self.toran, (0, int(-230 + 230 * ease(t / .9))))
        d = ImageDraw.Draw(img)
        a = fade(t, .4, 1.0)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        tw = dl.textlength("शुभ नवरात्रि", font=self.hi)
        dl.text(((W - tw) / 2, 1010), "शुभ नवरात्रि", font=self.hi, fill=GOLD_B)
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(layer)
        self.text(img, (W / 2, 1185), "Happy Navratri", self.f.cor_it(600, 132), CREAM, fade(t, .9, .9), rise=int(30 * (1 - fade(t, .9, .9))))
        self.text(img, (W / 2, 1345), "Nine nights of colour, devotion & dance", self.f.cor_it(500, 50), GOLD, fade(t, 1.5))
        self.text(img, (W / 2, 1420), "WITH LOVE FROM KALA KARI CREATIONS", self.f.cinzel(600, 28), CREAM, fade(t, 2.0), tracking=4)
        self.diyas(img, t, a=fade(t, .3, 1.0))
        return img

    def collection(self, i, local):
        key, fx, fy, title, sub = COLLECTIONS[i]
        dur = COLL_DUR
        p = local / dur
        z = 1.12 - .1 * ease(p) if i % 2 == 0 else 1.0 + .1 * ease(p)
        img = A.cover(self.photos[key], W, H, fx, fy, z).convert("RGBA")
        img.alpha_composite(A.gradient(W, 1000, 0, 245, color=(40, 10, 18)), (0, H - 1000))
        img.alpha_composite(A.gradient(W, 420, 170, 0, color=(40, 10, 18)), (0, 0))
        img.alpha_composite(self.toran, (0, 0))
        self.spark.draw(img, local + 10, .6)
        d = ImageDraw.Draw(img)
        d.rectangle((26, 26, W - 26, H - 26), outline=GOLD + (230,), width=3)
        a = fade(local, .25, .6)
        self.text(img, (W / 2, 1180), "SHOP OUR", self.f.cinzel(600, 34), GOLD, a, tracking=8)
        self.text(img, (W / 2, 1240), title, self.f.cor_it(600, 118), CREAM, a, rise=int(30 * (1 - a)))
        self.text(img, (W / 2, 1385), sub, self.f.cor_it(500, 50), GOLD_B, fade(local, .6, .6))
        self.text(img, (W / 2, 1460), "COLLECTION", self.f.cinzel(500, 26), CREAM, fade(local, .8, .6), tracking=10)
        return img

    def offer(self, local):
        img = self.festive_base(local + 20, mandala_y=900, mandala_alpha=.7)
        self.spark.draw(img, local + 20)
        img.alpha_composite(self.toran, (0, 0))
        a = fade(local, .15, .6)
        self.text(img, (W / 2, 330), "NAVRATRI OFFER", self.f.cinzel(700, 54), GOLD_B, a, tracking=8)
        self.text(img, (W / 2, 405), "Celebrate the festive season with us", self.f.cor_it(500, 46), CREAM, fade(local, .4))
        # 10% OFF pops in
        s = .6 + .4 * ease((local - .5) / .7)
        if local > .5:
            big = Image.new("RGBA", (W, 330), (0, 0, 0, 0))
            A.draw_text(ImageDraw.Draw(big), (W / 2, 10), "10% OFF", self.f.cinzel(700, 230), CREAM, anchor="c")
            big = big.resize((int(W * s), int(330 * s)), Image.LANCZOS)
            al = fade(local, .5, .5)
            big.putalpha(big.getchannel("A").point(lambda v: int(v * al)))
            img.alpha_composite(big, ((W - big.width) // 2, 560 + (330 - big.height) // 2))
        self.text(img, (W / 2, 900), "on orders above ₹3,000", self.f.cor_it(600, 70), GOLD_B, fade(local, 1.1))
        # code box
        ca = fade(local, 1.6)
        if ca > 0:
            box = Image.new("RGBA", img.size, (0, 0, 0, 0))
            db = ImageDraw.Draw(box)
            x0, y0, x1, y1 = 230, 1040, 850, 1250
            db.rounded_rectangle((x0, y0, x1, y1), radius=24, fill=(255, 245, 225, 30))
            for x in range(x0 + 20, x1 - 20, 34):
                db.line((x, y0, x + 18, y0), fill=GOLD_B, width=4)
                db.line((x, y1, x + 18, y1), fill=GOLD_B, width=4)
            for y in range(y0 + 20, y1 - 20, 34):
                db.line((x0, y, x0, y + 18), fill=GOLD_B, width=4)
                db.line((x1, y, x1, y + 18), fill=GOLD_B, width=4)
            A.draw_text(db, (W / 2, y0 + 26), "USE CODE", self.f.cinzel(600, 34), CREAM, tracking=8, anchor="c")
            A.draw_text(db, (W / 2, y0 + 78), "NAV10", self.f.cinzel(700, 110), GOLD_B, tracking=10, anchor="c")
            box.putalpha(box.getchannel("A").point(lambda v: int(v * ca)))
            img.alpha_composite(box)
        self.text(img, (W / 2, 1310), "Valid till 19 October 2026", self.f.cor_it(500, 50), CREAM, fade(local, 2.1))
        self.diyas(img, local + 20, y=1650)
        return img

    def end(self, local):
        img = self.festive_base(local + 40, mandala_y=640, mandala_alpha=.55)
        self.spark.draw(img, local + 40, .8)
        img.alpha_composite(self.toran, (0, 0))
        a = fade(local, .1, .8)
        lg = self.logo.copy()
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lg, ((W - lg.width) // 2, 300))
        y = 300 + self.logo.height + 60
        self.text(img, (W / 2, y), "Shop Jaipuri, Chikankari, Kutchi & more at", self.f.cor_it(600, 52), CREAM, fade(local, .5))
        self.text(img, (W / 2, y + 80), "www.kalakaricreations.com", self.f.cinzel(700, 54), GOLD_B, fade(local, .8), tracking=1)
        d = ImageDraw.Draw(img)
        # follow
        fa = fade(local, 1.4)
        if fa > 0:
            layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(layer)
            fy = y + 230
            pill_w = 760
            dl.rounded_rectangle(((W - pill_w) / 2, fy, (W + pill_w) / 2, fy + 110), radius=55, fill=CREAM)
            ix, iy = (W - pill_w) / 2 + 40, fy + 25
            dl.rounded_rectangle((ix, iy, ix + 60, iy + 60), radius=16, outline=(150, 50, 90), width=6)
            dl.ellipse((ix + 16, iy + 16, ix + 44, iy + 44), outline=(150, 50, 90), width=6)
            dl.ellipse((ix + 44, iy + 9, ix + 51, iy + 16), fill=(150, 50, 90))
            A.draw_text(dl, (ix + 90, fy + 18), "FOLLOW US", self.f.cinzel(600, 24), MAROON, tracking=4)
            A.draw_text(dl, (ix + 90, fy + 50), "@kalakaricreations27", self.f.cinzel(700, 40), MAROON)
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * fa)))
            img.alpha_composite(layer)
        ty = y + 390
        self.text(img, (W / 2, ty), "CALL / WHATSAPP", self.f.cinzel(600, 28), GOLD, fade(local, 1.9), tracking=6)
        self.text(img, (W / 2, ty + 44), "+91 94081 14592", self.f.cinzel(700, 64), CREAM, fade(local, 1.9))
        self.text(img, (W / 2, ty + 140), "Pan-India delivery  ·  Video-call shopping", self.f.cor_it(500, 44), GOLD_B, fade(local, 2.3))
        self.diyas(img, local + 40, y=1700, a=.9)
        return img

    def frame(self, t):
        layers = []
        if t < T_COLL + XF:
            layers.append((T_GREET, lambda: self.greeting(t)))
        for i in range(3):
            s = T_COLL + i * (COLL_DUR - XF)
            if s <= t < s + COLL_DUR:
                layers.append((s, lambda i=i, s=s: self.collection(i, t - s)))
        if T_OFFER <= t < T_END + XF:
            layers.append((T_OFFER, lambda: self.offer(t - T_OFFER)))
        if t >= T_END:
            layers.append((T_END, lambda: self.end(t - T_END)))
        if len(layers) == 1:
            out = layers[0][1]()
        else:
            (sa, fa), (sb, fb) = layers[-2], layers[-1]
            out = Image.blend(fa(), fb(), ease((t - sb) / XF))
        return out


# ------------------------------------------------------------------ music
def garba_track(path, seconds, seed=11):
    """Soft garba feel: 6/8 dhol pattern, tanpura drone, warm pad and a flute-like melody."""
    sr = M.SR
    rng = np.random.default_rng(seed)
    n = int((seconds + 3) * sr)
    drone, pad, flute, perc = (np.zeros(n) for _ in range(4))
    eighth = 0.21
    bar = eighth * 6

    t = 0.0
    while t < seconds + 1:
        for f in (M.hz(-5), M.hz(0), M.hz(0), M.hz(-12)):
            M.add(drone, M.tanpura_pluck(f, 4.0), t)
            t += bar / 2

    chords = [[0, 7, 16], [-3, 4, 12], [-7, 2, 12], [-5, 2, 9]]
    t, k = 0.0, 0
    while t < seconds + 1:
        for s_ in chords[k % 4]:
            M.add(pad, M.pad_note(M.hz(s_), bar * 2 + .8), t)
        t += bar * 2
        k += 1

    def dhol_low(dur=.5):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        f = 95 * np.exp(-tt * 6) + 55
        return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 9)

    def dhol_high(dur=.25):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        tone = np.sin(2 * np.pi * 330 * tt) * .5 + np.sin(2 * np.pi * 520 * tt) * .3
        noise = rng.standard_normal(m) * .35
        return (tone + noise) * np.exp(-tt * 28)

    def shaker(dur=.08):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        x = rng.standard_normal(m)
        x = x - M.lowpass(x, 3000)
        return x * np.exp(-tt * 60)

    # percussion enters after the intro, eases out at the end
    start = bar * 2
    t = start
    pattern = [(0, 'L'), (2, 'H'), (3, 'L'), (5, 'H')]
    while t < seconds - bar:
        for pos, kind in pattern:
            M.add(perc, (dhol_low() * 1.0) if kind == 'L' else (dhol_high() * .6), t + pos * eighth)
        for e in range(6):
            M.add(perc, shaker() * (.18 if e % 3 else .28), t + e * eighth)
        t += bar
    pe = M.env(n, 2.0, 0)
    perc *= pe

    def flute_note(f, dur):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        vib = 1 + .006 * np.sin(2 * np.pi * 5.2 * tt) * np.minimum(tt / .3, 1)
        ph = 2 * np.pi * np.cumsum(f * vib) / sr
        x = np.sin(ph) + .18 * np.sin(2 * ph) + .06 * np.sin(3 * ph)
        breath = rng.standard_normal(m) * .03
        return (x + breath) * M.env(m, .08, min(.25, dur * .4))

    # gentle Bhupali-ish phrases (D major pentatonic), one octave up
    notes = [M.hz(s_ + 12) for s_ in (0, 2, 4, 7, 9, 12, 14)]
    phrases = [[2, 3, 4, 3, 2, 1, 2], [4, 5, 4, 3, 2, 3], [1, 2, 3, 4, 3, 2, 1, 0], [3, 4, 5, 6, 5, 4, 3]]
    t = bar * 1.5
    pi = 0
    while t < seconds - 2.5:
        for idx in phrases[pi % len(phrases)]:
            d_ = eighth * rng.choice([2, 2, 3, 1])
            M.add(flute, flute_note(notes[idx], d_ * 1.15), t)
            t += d_
        t += bar * .5
        pi += 1

    mix = .26 * M.lowpass(drone, 2500) + .32 * M.lowpass(pad, 1400) + .30 * M.lowpass(flute, 3500) + .34 * perc
    mix = M.reverb(mix, seconds=2.0, mix=.22, seed=seed)[: int(seconds * sr)]
    mix *= M.env(len(mix), 1.2, 2.2)
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
    r = Reel(fonts_dir)
    n = int(TOTAL * FPS)
    wav = os.path.join(tempfile.mkdtemp(), "garba.wav")
    garba_track(wav, n / FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        proc.stdin.write(r.frame(k / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    print(out)


if __name__ == "__main__":
    main()
