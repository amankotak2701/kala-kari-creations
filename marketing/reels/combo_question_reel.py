#!/usr/bin/env python3
"""25.9 s 9:16 "Does this ___ & ___ combo work?" reel, timed like the reference trend reel.
- A torn paper unfolds on a textured background, and an ivory card slides over it with a paper clip.
- "DOES THIS / colour one / & / colour two / COMBO WORK?" writes in line by line.
- A sticker (an indigo block-print leaf lifted from the dupatta photo) slides in, then the card fades to black.
- Nine product shots follow on the beat, with slow zooms and pans and soft light-leak cuts.
- It ends on a Kala Kari Creations card. Reference audio.

Usage:
    python3 combo_question_reel.py <fonts_dir> <music.wav> <photos_dir> <out.mp4>
    python3 combo_question_reel.py <fonts_dir> preview <photos_dir> <out_dir> t1,t2,...
"""
import glob
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-maroon-flat.png")
W, H, FPS = 1080, 1920, 30
TOTAL = 25.86
BG = (34, 48, 82)                    # deep indigo plaster behind the card
UNDER = (206, 218, 232)              # pale indigo torn paper under the card
CARD = (247, 243, 232)
INK = (40, 44, 58)
LINES = ["DOES THIS", "Indigo Blue", "&", "Ivory White", "COMBO WORK?"]
LINE_T = [1.25, 2.0, 2.5, 2.75, 3.25]
T_STICKER, T_DARK, T_BLACK = 3.5, 5.2, 6.0
PRODUCT = "Indigo Dabu Block Print Cotton 3-Piece Suit Set"
# (start, photo, crop box in source px (x0, y0, x1, y1), zoom from -> to, drift (dx, dy) as a fraction of the box)
SHOTS = [
    (6.25, "courtyard", (465, 122, 1025, 1117), 1.0, 1.08, (0, 0)),             # yoke close-up
    (7.57, "dupatta-spread", (1040, 880, 1490, 1680), 1.06, 1.0, (0, .05)),     # leaf motifs and jhumki tassels
    (9.47, "verandah-chai", (450, 178, 1150, 1422), 1.1, 1.0, (0, 0)),          # yoke with bead tassels
    (11.63, "courtyard", None, 1.12, 1.0, (0, 0)),                              # full look (product name here)
    (15.4, "cafe-walk", None, 1.0, 1.07, (0, -.03)),
    (17.3, "dupatta-spread", "fit", 1.0, 1.04, (0, 0)),                         # whole spread on a blurred fill
    (19.13, "workshop", None, 1.0, 1.1, (0, -.04)),
    (21.03, "verandah-chai", (80, 1150, 530, 1950), 1.0, 1.08, (.05, 0)),       # dupatta border and latkans
    (22.63, "verandah-chai", None, 1.1, 1.0, (0, 0)),
]
T_END = 24.7


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def load(d, key):
    return Image.open(glob.glob(os.path.join(d, key + ".*"))[0]).convert("RGB")


def fbm(h, w, rng, scales):
    n = np.zeros((h, w), np.float32)
    for s in scales:
        small = rng.standard_normal((h // s + 2, w // s + 2)).astype(np.float32)
        n += np.asarray(Image.fromarray(small).resize((w, h), Image.BICUBIC)) * s ** .5
    return n / n.std()


def background():
    rng = np.random.default_rng(7)
    n = fbm(H, W, rng, (160, 60, 20, 6))
    rgb = np.array(BG, np.float32)[None, None] * (1 + .1 * n[..., None]) + rng.standard_normal((H, W, 1)) * 2
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")


def torn(w, h, col, seed, rough=14):
    rng = np.random.default_rng(seed)
    pts = []
    for side in range(4):
        for i in range(70):
            t = i / 70
            j = rng.uniform(0, rough) + (rough * .6 if rng.uniform() < .08 else 0)
            pts.append([(t * w, j), (w - j, t * h), (w - t * w, h - j), (j, h - t * h)][side])
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    fib = rng.standard_normal((h, w)) * 2.5
    rgb = np.array(col, np.float32)[None, None] + fib[..., None]
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    im.putalpha(m.filter(ImageFilter.GaussianBlur(.8)))
    # a lighter fibrous rim where the paper was torn
    edge = Image.eval(m.filter(ImageFilter.MinFilter(7)), lambda v: 255 - v)
    lay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(edge), np.asarray(m)) // 2))
    im.alpha_composite(lay)
    return im


def clip_img(s=1.0):
    """Silver paper clip."""
    w, h = int(46 * s), int(150 * s)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for off, col in ((0, (120, 124, 130, 255)), (2, (214, 218, 224, 255))):
        d.rounded_rectangle((3 + off * .3, 3, w - 4, h - 4), radius=w // 2 - 4, outline=col, width=int(5 * s))
        d.rounded_rectangle((12, 22, w - 13, h - 30), radius=w // 2 - 12, outline=col, width=int(5 * s))
    return lay


def shadow(canvas, item, xy, blur=14, off=(6, 12), a=110):
    pad = int(blur * 3)
    sh = Image.new("RGBA", (item.width + 2 * pad, item.height + 2 * pad), (0, 0, 0, 0))
    s = Image.new("RGBA", item.size, (8, 10, 20, 0))
    s.putalpha(item.getchannel("A").point(lambda v: int(v * a / 255)))
    sh.alpha_composite(s, (pad, pad))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (int(xy[0] + off[0] - pad), int(xy[1] + off[1] - pad)))
    canvas.alpha_composite(item, (int(xy[0]), int(xy[1])))


def leaf_sticker(photos):
    """The indigo leaf block print from the dupatta photo, keyed out of the cream cloth."""
    src = load(photos, "dupatta-spread").crop((278, 990, 372, 1130))
    src = src.resize((src.width * 4, src.height * 4), Image.LANCZOS)
    a = np.asarray(src, np.float32)
    lum = a.mean(2)
    blueness = a[..., 2] - a[..., 0]
    alpha = np.clip((175 - lum) / 50, 0, 1) * np.clip((blueness + 5) / 25, 0, 1)
    ink = np.array([38, 58, 104], np.float32)[None, None] * (.85 + .3 * (lum[..., None] / 255))   # true indigo ink
    im = Image.fromarray(np.clip(ink, 0, 255).astype(np.uint8)).convert("RGBA")
    im.putalpha(Image.fromarray((np.clip(alpha * 1.4, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1)))
    im = im.resize((int(im.width * .6), int(im.height * .6)), Image.LANCZOS)
    # white die-cut sticker border so it reads on both the card and the indigo wall
    pad = 14
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(im, (pad, pad))
    solid = big.getchannel("A").point(lambda v: 255 if v > 60 else 0).filter(ImageFilter.MaxFilter(9))
    solid = solid.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1.5))
    out = Image.new("RGBA", big.size, (250, 248, 242, 0))
    out.putalpha(solid)
    out.alpha_composite(big)
    return out


def spaced(d, xy, s, f, fill, spacing, anchor_mid=True):
    total = sum(d.textlength(c, font=f) for c in s) + spacing * (len(s) - 1)
    x, y = xy
    if anchor_mid:
        x -= total / 2
    for c in s:
        d.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += d.textlength(c, font=f) + spacing


class Reel:
    def __init__(self, fonts, photos):
        cg = os.path.join(fonts, "fontsource-cormorant-garamond", "package", "files")
        self.big = ImageFont.truetype(os.path.join(cg, "cormorant-garamond-latin-500-normal.woff2"), 108)
        self.amp = ImageFont.truetype(os.path.join(cg, "cormorant-garamond-latin-500-normal.woff2"), 84)
        self.small = ImageFont.truetype(os.path.join(fonts, "fontsource-jost", "package", "files", "jost-latin-500-normal.woff2"), 26)
        self.name_f = ImageFont.truetype(os.path.join(cg, "cormorant-garamond-latin-600-italic.woff2"), 54)
        self.end_f = ImageFont.truetype(os.path.join(cg, "cormorant-garamond-latin-600-normal.woff2"), 46)
        self.end_s = ImageFont.truetype(os.path.join(fonts, "fontsource-jost", "package", "files", "jost-latin-400-normal.woff2"), 30)
        self.bg = background()
        self.under = torn(640, 900, UNDER, 1)
        self.card = torn(600, 860, CARD, 2, rough=6)
        self.clip = clip_img()
        self.leaf = leaf_sticker(photos)
        self.photos = {k: load(photos, k) for k in {s[1] for s in SHOTS}}
        self.fit_cache = {}
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo.resize((560, int(560 * logo.height / logo.width)), Image.LANCZOS)

    # ------------------------------------------------------------ intro
    def card_layer(self, t):
        """The ivory card with whatever text has been written by time t."""
        c = self.card.copy()
        d = ImageDraw.Draw(c)
        ys = [190, 335, 420, 520, 640]
        for i, (s, t0, y) in enumerate(zip(LINES, LINE_T, ys)):
            a = ease((t - t0) / .4)
            if a <= 0:
                continue
            lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            if i in (0, 4):
                spaced(dl, (300, y), s, self.small, INK, 6)
            else:
                f = self.amp if s == "&" else self.big
                dl.text((300, y), s, font=f, fill=INK, anchor="ms")
                if i in (1, 3):                                       # written in from the left
                    reveal = int(c.width * ease_out((t - t0) / .55))
                    m = Image.new("L", c.size, 0)
                    ImageDraw.Draw(m).rectangle((0, 0, reveal, c.height), fill=255)
                    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel("A")), np.asarray(m))))
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            c.alpha_composite(lay)
        return c

    def intro(self, t):
        img = self.bg.copy()
        cx, cy = W / 2, H * .47
        # torn under-paper unfolds
        if t >= .2:
            p = ease_out((t - .2) / .35)
            u = self.under.resize((max(1, int(self.under.width * (.35 + .65 * p))), max(1, int(self.under.height * (.55 + .45 * p)))))
            u = u.rotate(-8 + 10 * p, expand=True, resample=Image.BICUBIC)
            shadow(img, u, (cx - u.width / 2 - 18, cy - u.height / 2 + 14))
        # ivory card slides in from the right and settles
        if t >= .5:
            p = ease_out((t - .5) / .4)
            card = self.card_layer(t).rotate(-1.2, expand=True, resample=Image.BICUBIC)
            x = cx - card.width / 2 + 12 + (1 - p) * W * .8
            shadow(img, card, (x, cy - card.height / 2 - 6))
            if t >= .85:
                shadow(img, self.clip, (x + card.width - 130, cy - card.height / 2 - 70), blur=4, off=(3, 5), a=120)
        # leaf sticker slides in at the bottom-right corner of the card
        if t >= T_STICKER:
            p = ease_out((t - T_STICKER) / .4)
            lf = self.leaf.rotate(-25 + 10 * p, expand=True, resample=Image.BICUBIC)
            x = cx + 285 + (1 - p) * 300
            y = cy + 380 + (1 - p) * 200
            shadow(img, lf, (x - lf.width / 2, y - lf.height / 2), blur=6, off=(4, 7), a=120)
        # slow push-in, then fade to black
        if t >= T_DARK - .3:
            z = 1 + .05 * ease((t - (T_DARK - .3)) / 1.2)
            w2, h2 = int(W / z), int(H / z)
            img = img.crop(((W - w2) // 2, (H - h2) // 2, (W - w2) // 2 + w2, (H - h2) // 2 + h2)).resize((W, H), Image.BICUBIC)
        if t >= T_DARK:
            img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * ease((t - T_DARK) / (T_BLACK - T_DARK))))))
        return img

    # ------------------------------------------------------------ product shots
    def shot_frame(self, i, local, span):
        _, key, box, z0, z1, (dx, dy) = SHOTS[i]
        im = self.photos[key]
        if box == "fit":                                          # whole photo on a blurred, darkened fill
            if i not in self.fit_cache:
                im = im.crop((0, 0, im.width, int(im.height * .91)))   # keep the corner badge out of frame
                fill = im.resize((W // 8, int(W // 8 * 16 / 9)), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))
                fill = fill.resize((W, H), Image.BICUBIC)
                fill = Image.blend(fill, Image.new("RGB", (W, H), (20, 26, 40)), .35)
                fg = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS)
                fill.paste(fg, (0, (H - fg.height) // 2))
                self.fit_cache[i] = fill
            base = self.fit_cache[i]
            box = (0, 0, W, H)
            im = base
        elif box is None:                                         # full-height 9:16 crop, centred
            w = im.height * 9 / 16
            box = ((im.width - w) / 2, 0, (im.width + w) / 2, im.height)
        x0, y0, x1, y1 = box
        p = ease(local / span)
        z = z0 + (z1 - z0) * p
        bw, bh = (x1 - x0) / z, (y1 - y0) / z
        cxx = (x0 + x1) / 2 + dx * (x1 - x0) * (p - .5)
        cyy = (y0 + y1) / 2 + dy * (y1 - y0) * (p - .5)
        l, t_ = max(0, cxx - bw / 2), max(0, cyy - bh / 2)
        l, t_ = min(l, im.width - bw), min(t_, im.height - bh)
        return im.crop((int(l), int(t_), int(l + bw), int(t_ + bh))).resize((W, H), Image.BICUBIC).convert("RGBA")

    def product(self, t):
        starts = [s[0] for s in SHOTS] + [T_END]
        i = max(k for k in range(len(SHOTS)) if starts[k] <= t)
        local, span = t - starts[i], starts[i + 1] - starts[i]
        img = self.shot_frame(i, local, span)
        if i == 0 and local < .5:                                 # first shot rises out of black
            img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - ease(local / .5))))))
        if i > 0 and local < .3:                                  # warm light-leak cut
            prev = self.shot_frame(i - 1, starts[i] - starts[i - 1], starts[i] - starts[i - 1])
            k = ease(local / .3)
            img = Image.blend(prev, img, k)
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 244, 228, int(150 * math.sin(math.pi * k)))))
        if SHOTS[i][1] == "courtyard" and SHOTS[i][2] is None:     # product name on the full look
            a = ease((local - .5) / .5) * (1 - ease((local - (span - .5)) / .4))
            if a > 0:
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                g = np.clip((np.arange(H) - H * .7) / (H * .3), 0, 1) ** 1.3 * 170
                sh = Image.new("RGBA", (W, H), (10, 14, 28, 0))
                sh.putalpha(Image.fromarray(np.repeat(g[:, None], W, 1).astype(np.uint8)))
                lay.alpha_composite(sh)
                d = ImageDraw.Draw(lay)
                d.text((W / 2, H - 230), "Indigo Dabu Block Print", font=self.name_f, fill=(255, 255, 255), anchor="ms")
                d.text((W / 2, H - 165), "Cotton 3-Piece Suit Set", font=self.name_f, fill=(255, 255, 255), anchor="ms")
                lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
                img.alpha_composite(lay)
        return img

    def ending(self, t):
        local = t - T_END
        last = self.shot_frame(len(SHOTS) - 1, T_END - SHOTS[-1][0], T_END - SHOTS[-1][0])
        img = last.copy()
        img.alpha_composite(Image.new("RGBA", (W, H), CARD + (int(255 * ease(local / .3)),)))
        a = ease((local - .15) / .3)
        if a > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.alpha_composite(self.logo, ((W - self.logo.width) // 2, int(H * .4 - self.logo.height / 2)))
            d = ImageDraw.Draw(lay)
            y = int(H * .4 + self.logo.height / 2 + 90)
            d.text((W / 2, y), PRODUCT, font=self.end_f, fill=INK, anchor="ms")
            d.text((W / 2, y + 80), "kalakaricreations.com", font=self.end_s, fill=INK, anchor="ms")
            d.text((W / 2, y + 130), "Call / WhatsApp  +91 94081 14592", font=self.end_s, fill=(90, 90, 100), anchor="ms")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)
        return img

    def frame(self, t):
        if t < SHOTS[0][0]:
            return self.intro(t)
        if t < T_END:
            return self.product(t)
        return self.ending(t)


def main():
    fonts, music, photos, out = sys.argv[1:5]
    r = Reel(fonts, photos)
    if music == "preview":
        for t in map(float, sys.argv[5].split(",")):
            r.frame(t).convert("RGB").resize((W // 4, H // 4)).save(os.path.join(out, f"cq_{t:05.2f}.png"))
        return
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
