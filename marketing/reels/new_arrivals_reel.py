#!/usr/bin/env python3
"""8.75 s 9:16 "HEY HEY HEY · STOP STOP STOP · LOOK AT · THIS…" new-arrivals reel, timed frame-for-frame like the
reference trend reel: cream paper background with a pink lotus pattern, magenta words, 7 product photos on the
beat with "THIS", then "aaaannnndddd......" and the hero product. Reference audio.

Usage:
    python3 new_arrivals_reel.py <fonts_dir> <music.wav> <out.mp4> <hero> <photo1> ... <photo7>
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
TOTAL = 8.75
MAGENTA = (240, 20, 125)
LOTUS = (238, 150, 190)
HEY = [(0.0, 156, 465), (0.07, 444, 660), (0.2, 651, 915)]          # appear time, left x, centre y
STOP = [(0.67, 786), (0.8, 1002), (0.93, 1230)]                    # appear time, centre y
T_HEY_OUT, T_STOP_OUT = 0.53, 1.2
T_LOOK, T_LOOK_OUT = 1.47, 2.37
CUTS = [2.37, 2.8, 3.33, 3.9, 4.47, 5.2, 5.87, 6.4]                 # 7 photos, then "aaaannnndddd"
T_AND, T_HERO = 6.4, 7.9
BOX = (63, 324, 1017, 1593)
HERO_BOX = (39, 291, 1041, 1626)


def font(fonts_dir, weight, size):
    return ImageFont.truetype(os.path.join(fonts_dir, "fontsource-poppins", "package", "files",
                                           f"poppins-latin-{weight}-normal.woff2"), size)


def lotus(d, cx, cy, s):
    """Small outline lotus: five petals on a base line."""
    w = max(2, int(s / 9))
    for ang, ln, wd in ((0, 1.0, .34), (-38, .82, .3), (38, .82, .3), (-72, .6, .26), (72, .6, .26)):
        a = math.radians(ang)
        pts = []
        for i in range(25):
            t = i / 24
            y = -s * ln * t
            x = s * wd * math.sin(math.pi * t) ** .9
            pts.append((x, y))
        pts += [(-x, y) for x, y in reversed(pts)]
        pts = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
        d.line(pts + [pts[0]], fill=LOTUS, width=w)
    d.line((cx - s * .7, cy + s * .08, cx + s * .7, cy + s * .08), fill=LOTUS, width=w)


def background():
    rng = np.random.default_rng(2)
    base = np.array([244, 236, 234], np.float32)
    small = rng.standard_normal((H // 6, W // 6)).astype(np.float32)
    n = np.asarray(Image.fromarray(((small - small.min()) / np.ptp(small) * 255).astype(np.uint8))
                   .resize((W, H), Image.BICUBIC), np.float32) / 255 - .5
    img = base + (n * 10 + rng.standard_normal((H, W)) * 2.2)[..., None]
    im = Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    for r, y in enumerate(range(80, H, 195)):
        for x in range(90 if r % 2 == 0 else 280, W, 380):
            lotus(d, x, y, 30)
    return im


def cover(path, box, fy=.38):
    im = Image.open(path).convert("RGB")
    bw, bh = box[2] - box[0], box[3] - box[1]
    s = max(bw / im.width, bh / im.height)
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = (r.width - bw) // 2
    y = int(min(max(r.height * fy - bh / 2, 0), r.height - bh))
    return r.crop((x, y, x + bw, y + bh)).convert("RGBA")


class Reel:
    def __init__(self, fonts_dir, hero, photos):
        self.bg = background()
        self.big = font(fonts_dir, 700, 118)
        self.and_font = font(fonts_dir, 600, 66)
        self.this_font = font(fonts_dir, 700, 104)
        self.site_font = font(fonts_dir, 600, 44)
        self.photos = [cover(p, BOX) for p in photos]
        self.hero = cover(hero, HERO_BOX)

    def text(self, img, xy, s, f, fill, anchor, shadow=False):
        d = ImageDraw.Draw(img)
        if shadow:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).text((xy[0] + 3, xy[1] + 4), s, font=f, fill=(0, 0, 0, 120), anchor=anchor)
            img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
        d.text(xy, s, font=f, fill=fill, anchor=anchor)

    def photo(self, img, im, box, this_y):
        img.alpha_composite(im, box[:2])
        self.text(img, ((box[0] + box[2]) / 2, this_y), "THIS", self.this_font, (255, 255, 255), "mm", shadow=True)

    def frame(self, t):
        img = self.bg.copy()
        if t < T_HEY_OUT:
            for t0, x, y in HEY:
                if t >= t0:
                    self.text(img, (x, y), "HEY", self.big, MAGENTA, "lm")
        elif 0.67 <= t < T_STOP_OUT:
            for t0, y in STOP:
                if t >= t0:
                    self.text(img, (W / 2, y), "STOP", self.big, MAGENTA, "mm")
        elif T_LOOK <= t < T_LOOK_OUT:
            self.text(img, (W / 2, 1014), "LOOK AT", self.big, MAGENTA, "mm")
        elif CUTS[0] <= t < T_AND:
            i = max(k for k in range(7) if CUTS[k] <= t)
            self.photo(img, self.photos[i], BOX, 1440)
        elif T_AND <= t < T_HERO:
            self.text(img, (W / 2, 990), "aaaannnndddd......", self.and_font, MAGENTA, "mm")
        elif t >= T_HERO:
            self.photo(img, self.hero, HERO_BOX, 1368)
            self.text(img, (W / 2, 1715), "New arrivals at kalakaricreations.com", self.site_font, MAGENTA, "mm")
        return img


def main():
    fonts_dir, music, out, hero = sys.argv[1:5]
    photos = sys.argv[5:12]
    assert len(photos) == 7, "need a hero photo and 7 product photos"
    r = Reel(fonts_dir, hero, photos)
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
