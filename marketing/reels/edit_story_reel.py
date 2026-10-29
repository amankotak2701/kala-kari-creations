#!/usr/bin/env python3
"""19.9 s 9:16 "The invite says… Dress code: unforgettable." edit reel, timed like the reference trend reel:
a slow push-in on the hero look with two text beats, four numbered product slides (occasion + poetic line), eight
fast cuts on the beat, then a cream end card with a 2x2 grid, "Shop the New Edit" and the website. Reference audio.

Usage:
    python3 edit_story_reel.py <fonts_dir> <music.wav> <out.mp4> <photos_dir>
<photos_dir> holds p1a, p1b, p2a, p2b, p3a, p3b, p4a, p4b (any image extension); "a" is each product's main photo.
"""
import glob
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
TOTAL = 19.92
CREAM = (243, 237, 228)
INK = (52, 40, 34)
GOLD = (214, 186, 130)
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"

TAG = "KALA KARI CREATIONS  ·  THE NEW EDIT"
OPEN = [("The invite says", "wedding season.", 0.3, 1.4, 3.3),
        ("Dress code:", "unforgettable.", 3.9, 5.9, 7.1)]
PRODUCTS = [  # occasion, line, caption, grid label
    ("Sangeet night.", "Gold, softly.", "CHAMPAGNE MUL CHANDERI · 3-PIECE", "SANGEET NIGHT"),
    ("Puja morning.", "Stories, woven.", "JAMDANI WORK SILK · 3-PIECE", "PUJA MORNING"),
    ("Haldi day.", "Sunshine, stitched.", "MUSTARD MUL MIRROR-WORK · 3-PIECE", "HALDI DAY"),
    ("Roka evening.", "Soft, never shy.", "DUSTY PINK MUL CHANDERI · 3-PIECE", "ROKA EVENING"),
]
SLIDES = [7.1, 8.37, 10.07, 11.5, 13.3]                # product slides 01-04
FAST = [13.3, 13.7, 14.1, 14.5, 14.9, 15.3, 15.73, 16.1, 16.5]
FAST_ORDER = ["p2b", "p3b", "p4b", "p1a", "p2a", "p3a", "p4a", "p1b"]
END = 16.5
GRID = [(270, 250), (730, 250), (270, 860), (730, 860)]
CELL = (400, 530)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def cover(im, w, h, fy=.35, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = (r.width - w) // 2
    y = int(min(max(r.height * fy - h / 2, 0), r.height - h))
    return r.crop((x, y, x + w, y + h))


class Reel:
    def __init__(self, fonts_dir, photos_dir):
        cg = os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files")
        self.serif = ImageFont.truetype(os.path.join(cg, "cormorant-garamond-latin-500-normal.woff2"), 118)
        self.italic = ImageFont.truetype(os.path.join(cg, "cormorant-garamond-latin-500-italic.woff2"), 118)
        self.end_serif = ImageFont.truetype(os.path.join(cg, "cormorant-garamond-latin-500-normal.woff2"), 82)
        self.end_italic = ImageFont.truetype(os.path.join(cg, "cormorant-garamond-latin-500-italic.woff2"), 74)
        self.mono = ImageFont.truetype(MONO, 27)
        self.mono_s = ImageFont.truetype(MONO, 21)
        self.src = {}
        for key in ("p1a", "p1b", "p2a", "p2b", "p3a", "p3b", "p4a", "p4b"):
            path = glob.glob(os.path.join(photos_dir, key + ".*"))[0]
            self.src[key] = Image.open(path).convert("RGB")
        self.full = {k: cover(v, W, H).convert("RGBA") for k, v in self.src.items()}
        self.hero_big = cover(self.src["p1a"], int(W * 1.12), int(H * 1.12), zoom=1.0)
        g = np.clip((np.arange(H) - H * .5) / (H * .5), 0, 1) ** 1.4 * 200
        self.shade = Image.new("RGBA", (W, H), (20, 12, 10, 0))
        self.shade.putalpha(Image.fromarray(np.repeat(g[:, None], W, 1).astype(np.uint8)))
        self.cells = [cover(self.src[f"p{i + 1}a"], *CELL).convert("RGBA") for i in range(4)]

    @staticmethod
    def put(img, xy, s, f, fill, a, anchor="ls", spacing=0):
        if a <= 0:
            return
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        if spacing:
            x, y = xy
            if anchor[0] == "m":
                x -= (sum(d.textlength(c, font=f) for c in s) + spacing * (len(s) - 1)) / 2
            for c in s:
                d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
                x += d.textlength(c, font=f) + spacing
        else:
            d.text(xy, s, font=f, fill=fill, anchor=anchor)
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lay)

    def opening(self, t):
        z = 1 + .1 * (t / 7.1)                                  # slow push-in
        bw, bh = int(W * 1.12 / z), int(H * 1.12 / z)
        big = self.hero_big
        x = (big.width - bw) // 2
        y = int((big.height - bh) * .35)
        img = big.crop((x, y, x + bw, y + bh)).resize((W, H), Image.BICUBIC).convert("RGBA")
        img.alpha_composite(self.shade)
        self.put(img, (84, 190), TAG, self.mono, GOLD, ease(t / .4), spacing=4)
        for l1, l2, t1, t2, tout in OPEN:
            if t1 <= t < tout:
                self.put(img, (84, 1350), l1, self.serif, (255, 255, 255), ease((t - t1) / .2))
                self.put(img, (84, 1462), l2, self.italic, (255, 255, 255), ease((t - t2) / .2))
        return img

    def slide(self, i, local):
        img = self.full[f"p{i + 1}a" if i else "p1b"].copy()
        img.alpha_composite(self.shade)
        l1, l2, cap, _ = PRODUCTS[i]
        a1, a2 = ease((local - .3) / .2), ease((local - .42) / .2)
        self.put(img, (84, 1250), f"0{i + 1} / 04", self.mono, (235, 225, 210), a1, spacing=6)
        self.put(img, (84, 1350), l1, self.serif, (255, 255, 255), a1)
        self.put(img, (84, 1462), l2, self.italic, (255, 255, 255), a2)
        self.put(img, (84, 1540), cap, self.mono_s, (225, 215, 200), a2, spacing=3)
        return img

    def end(self, local):
        img = Image.new("RGBA", (W, H), CREAM + (255,))
        self.put(img, (W / 2, 205), "THE NEW EDIT  ·  HANDCRAFTED", self.mono, (120, 96, 70), ease(local / .3), "ms", 6)
        for k, ((x, y), cell) in enumerate(zip(GRID, self.cells)):
            a = ease((local - .1 * k) / .25)
            if a > 0:
                c = cell.copy()
                c.putalpha(int(255 * a))
                img.alpha_composite(c, (x, y))
                self.put(img, (x, y + CELL[1] + 40), f"0{k + 1}   {PRODUCTS[k][3]}", self.mono_s, (90, 70, 55), a, spacing=3)
        self.put(img, (W / 2, 1530), "Shop the New Edit", self.end_serif, INK, ease((local - .5) / .3), "ms")
        self.put(img, (W / 2, 1625), "kalakaricreations.com", self.end_italic, INK, ease((local - .65) / .3), "ms")
        self.put(img, (W / 2, 1715), "CALL / WHATSAPP  +91 94081 14592", self.mono_s, (140, 118, 96),
                 ease((local - .8) / .3), "ms", 3)
        return img

    def frame(self, t):
        if t < SLIDES[0]:
            return self.opening(t)
        if t < SLIDES[-1]:
            i = max(k for k in range(4) if SLIDES[k] <= t)
            return self.slide(i, t - SLIDES[i])
        if t < END:
            i = max(k for k in range(8) if FAST[k] <= t)
            return self.full[FAST_ORDER[i]]
        return self.end(t - END)


def main():
    fonts_dir, music, out, photos_dir = sys.argv[1:5]
    r = Reel(fonts_dir, photos_dir)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", music, "-t", f"{TOTAL:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(int(TOTAL * FPS)):
        proc.stdin.write(r.frame(k / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    print(out)


if __name__ == "__main__":
    main()
