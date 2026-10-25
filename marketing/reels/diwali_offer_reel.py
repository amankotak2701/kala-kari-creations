#!/usr/bin/env python3
"""9.8 s 9:16 Diwali Dhamaka offer reel (FLAT 20% OFF on all products, till 9 Nov), timed like the reference
trend reel: the camera tilts down from a dusk sky to a lit palace avenue while a rocket climbs, its burst brings in
the Diwali Dhamaka Sale badge (Diwali -> DHAMAKA -> SALE), the offer pops in under it with fireworks, everything
clears, then "TILL 9 NOV" zooms in with the website. Own artwork; the reference's music.

Usage:
    python3 diwali_offer_reel.py <fonts_dir> <music.wav> <out.mp4>
<fonts_dir> holds the fontsource packages cinzel, cormorant-garamond, alfa-slab-one, rozha-one and poppins
(npm pack @fontsource/<name>, extracted to <fonts_dir>/fontsource-<name>).
    python3 diwali_offer_reel.py <fonts_dir> preview <out_dir> t1 t2 ...
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "posts"))
import diwali_carousel as C  # noqa: E402

W, H, FPS = 1080, 1920, 30
PAN = 700                        # extra sky above the frame for the opening tilt
CH = H + PAN
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-gold-flat.png")
TOTAL = 9.8

BADGE_IN, T_DIWALI, T_DHAMAKA, T_SALE = .75, 1.0, 1.6, 2.3
T_OFFER, T_ALL = 2.9, 3.25
T_OUT = 5.95
T_TILL, T_WEB = 6.9, 7.7


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def back(t, s=1.7):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def noise(rng, w, h, scale):
    small = rng.standard_normal((h // scale + 2, w // scale + 2)).astype(np.float32)
    im = Image.fromarray(((small - small.min()) / np.ptp(small) * 255).astype(np.uint8))
    return np.asarray(im.resize((w, h), Image.BICUBIC), np.float32) / 255 - .5


# ------------------------------------------------------------------ scenery (canvas W x CH)
HORIZON = CH - 560


def sky():
    rng = np.random.default_rng(4)
    y = np.linspace(0, 1, CH)[:, None]
    stops = [(0.0, (26, 16, 70)), (.45, (64, 30, 120)), (.66, (120, 44, 150)), (.76, (206, 80, 140)),
             (.82, (246, 140, 110)), (.86, (255, 176, 110)), (1.0, (120, 50, 70))]
    img = np.zeros((CH, W, 3), np.float32)
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = ((y >= a) & (y <= b)).astype(np.float32)
        t = np.clip((y - a) / (b - a), 0, 1)
        img += m[..., None] * (np.array(ca) + (np.array(cb) - np.array(ca)) * t[..., None])
    # painterly clouds: stretched noise, purple-pink tinted, strongest in the upper half
    n = noise(rng, W, CH, 160) * .7 + noise(rng, W, CH, 60) * .4 + noise(rng, W, CH, 18) * .2
    n = np.asarray(Image.fromarray(((n + .5).clip(0, 1) * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(3)), np.float32) / 255 - .5
    tint = np.array([150, 70, 170], np.float32)
    k = np.clip(n * 1.6, -1, 1)[..., None] * (1 - np.clip((y[..., None] - .7) / .2, 0, 1)) * .35
    img = img * (1 - np.abs(k)) + np.where(k > 0, tint, img * .6) * np.abs(k)
    # brush texture
    img += noise(rng, W, CH, 3)[..., None] * 10
    return Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert("RGBA")


def string_lights(d, glow, x0, y0, x1, y1, sag, n, r=3):
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 226, 150, 255))
        glow.ellipse((x - r * 4, y - r * 4, x + r * 4, y + r * 4), fill=(255, 190, 90, 120))


def palace(img, glow, x, base, w, h, seed):
    """A lit palace block: warm gradient facade, jharokha windows, corner towers with domes and strands of lights."""
    rng = np.random.default_rng(seed)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    top = base - h
    # facade with a vertical warm gradient (dark at the roof, glowing near the street)
    grad = np.linspace(0, 1, h)[:, None, None]
    face = np.array([92, 44, 52]) * (1 - grad) + np.array([214, 132, 84]) * grad
    face_im = Image.fromarray(np.repeat(face, w, axis=1).astype(np.uint8)).convert("RGBA")
    lay.paste(face_im, (x, top))
    lit = (255, 214, 140, 255)
    # rows of small arched windows
    for row in range(4):
        yy = top + 50 + row * (h - 80) / 4
        for col in range(int((w - 20) / 34)):
            xx = x + 14 + col * 34
            d.rectangle((xx, yy + 9, xx + 14, yy + 30), fill=lit)
            d.pieslice((xx, yy, xx + 14, yy + 18), 180, 360, fill=lit)
            glow.ellipse((xx - 8, yy - 6, xx + 22, yy + 40), fill=(255, 170, 80, 60))
        d.rectangle((x, yy + 36, x + w, yy + 41), fill=(120, 60, 50, 255))
    # corner towers with onion domes
    for tx in (x - 10, x + w - 50):
        th = h + 90
        d.rectangle((tx, base - th, tx + 60, base), fill=(150, 80, 64, 255))
        for row in range(6):
            yy = base - th + 30 + row * th / 6
            d.rectangle((tx + 22, yy, tx + 38, yy + 22), fill=lit)
        d.ellipse((tx - 6, base - th - 70, tx + 66, base - th + 10), fill=(170, 92, 70, 255))
        d.line((tx + 30, base - th - 70, tx + 30, base - th - 100), fill=lit, width=4)
    # chhatris on the roof
    for k in range(3):
        cx = x + w * (.25 + k * .25)
        d.rectangle((cx - 22, top - 34, cx + 22, top), fill=(140, 74, 60, 255))
        d.pieslice((cx - 30, top - 64, cx + 30, top - 6), 180, 360, fill=(166, 90, 70, 255))
    # vertical strands of fairy lights hanging from the roof
    for k in range(int(w / 26)):
        sx = x + 8 + k * 26 + rng.uniform(-4, 4)
        L = h * rng.uniform(.55, .95)
        for yy in np.arange(top + 6, top + L, 15):
            d.ellipse((sx - 2.5, yy - 2.5, sx + 2.5, yy + 2.5), fill=(255, 236, 170, 255))
            glow.ellipse((sx - 9, yy - 9, sx + 9, yy + 9), fill=(255, 200, 100, 70))
    img.alpha_composite(lay)


def scenery():
    img = sky()
    lay = Image.new("RGBA", (W, CH), (0, 0, 0, 0))
    glow_l = Image.new("RGBA", (W, CH), (0, 0, 0, 0))
    d, g = ImageDraw.Draw(lay), ImageDraw.Draw(glow_l)
    hz = HORIZON + 60
    vx = W / 2                                                   # vanishing point of the avenue
    # road first (a soft, wet, reflective lane)
    road = Image.new("RGBA", (W, CH), (0, 0, 0, 0))
    ImageDraw.Draw(road).polygon([(vx - 20, hz), (vx + 20, hz), (W + 260, CH), (-260, CH)], fill=(150, 70, 80, 255))
    grad = np.clip((np.arange(CH) - hz) / (CH - hz), 0, 1)[:, None]
    a = np.asarray(road.getchannel("A"), np.float32) * (.55 + .45 * grad)
    road.putalpha(Image.fromarray(a.astype(np.uint8)))
    lay.alpha_composite(road)
    # far trees and lamp posts converging on the centre
    rng = np.random.default_rng(8)
    for side in (-1, 1):
        for i in range(12):
            t = i / 11
            x = vx + side * (30 + 330 * t ** 1.3)
            size = 24 + 120 * t ** 1.4
            ybase = hz + 10 + 150 * t ** 1.4
            col = (60 + int(20 * t), 30 + int(8 * t), 70 + int(10 * t), 255)
            for _ in range(6):
                ox, oy = rng.uniform(-.5, .5) * size, rng.uniform(-1.0, -.3) * size
                r = size * rng.uniform(.35, .6)
                d.ellipse((x + ox - r, ybase + oy - r, x + ox + r, ybase + oy + r), fill=col)
            for _ in range(int(4 + 10 * t)):                    # fairy lights in the trees
                ox, oy = rng.uniform(-.7, .7) * size, rng.uniform(-1.3, -.2) * size
                rr = 1.5 + 2.5 * t
                d.ellipse((x + ox - rr, ybase + oy - rr, x + ox + rr, ybase + oy + rr), fill=(255, 230, 160, 255))
                g.ellipse((x + ox - rr * 4, ybase + oy - rr * 4, x + ox + rr * 4, ybase + oy + rr * 4), fill=(255, 190, 90, 80))
            lx = x + side * size * .45
            lh = size * 1.25
            d.line((lx, ybase, lx, ybase - lh), fill=(50, 26, 34, 255), width=max(2, int(size / 26)))
            rr = max(3, size / 12)
            d.ellipse((lx - rr, ybase - lh - rr, lx + rr, ybase - lh + rr), fill=(255, 232, 160, 255))
            g.ellipse((lx - rr * 6, ybase - lh - rr * 6, lx + rr * 6, ybase - lh + rr * 6), fill=(255, 180, 80, 120))
            # its reflection on the wet road
            ry = ybase + (ybase - (ybase - lh)) * .35
            g.ellipse((lx - rr * 2, ry - rr * .6, lx + rr * 2, ry + rr * 5), fill=(255, 170, 80, 90))
    # palaces on both sides
    palace(lay, g, -30, hz + 260, 300, 360, 1)
    palace(lay, g, 810, hz + 270, 300, 380, 2)
    # foreground: gifts, marigolds and a big diya (left), a silk drape (right)
    fy = CH - 170
    for gx, gw, gh, col, rib in ((20, 190, 150, (128, 26, 64), (232, 186, 90)), (170, 150, 190, (176, 46, 96), (250, 210, 120)),
                                 (0, 120, 95, (238, 204, 160), (190, 60, 80))):
        d.rectangle((gx, fy - gh + 70, gx + gw, fy + 70), fill=col + (255,))
        d.rectangle((gx + gw / 2 - 8, fy - gh + 70, gx + gw / 2 + 8, fy + 70), fill=rib + (255,))
        d.rectangle((gx, fy - gh / 2 + 60, gx + gw, fy - gh / 2 + 74), fill=rib + (255,))
        d.ellipse((gx + gw / 2 - 34, fy - gh + 40, gx + gw / 2, fy - gh + 74), outline=rib + (255,), width=7)
        d.ellipse((gx + gw / 2, fy - gh + 40, gx + gw / 2 + 34, fy - gh + 74), outline=rib + (255,), width=7)
    d.polygon([(600, CH), (680, fy + 10), (880, fy - 40), (W + 40, fy - 10), (W + 40, CH)], fill=(150, 30, 72, 255))
    for k in range(7):
        y = fy + 10 + k * 26
        d.line((650 + k * 8, y + 24, W, y - 18), fill=(232, 176, 90, 220), width=3)
    for i in range(40):                                         # marigolds
        x = rng.uniform(10, 560)
        y = rng.uniform(fy + 60, CH - 6)
        r = rng.uniform(9, 15)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 150 + int(rng.uniform(0, 50)), 30, 255))
        d.ellipse((x - r * .4, y - r * .4, x + r * .4, y + r * .4), fill=(226, 104, 20, 255))
    for x, sz in ((430, 130), (560, 80), (1000, 70)):
        dy = C.diya(sz)
        lay.alpha_composite(dy, (int(x - sz / 2), int(fy + 40 - sz * .4)))
        g.ellipse((x - sz * .9, fy - sz * .3, x + sz * .9, fy + sz * 1.1), fill=(255, 170, 70, 60))
    glow = glow_l.filter(ImageFilter.GaussianBlur(12))
    img.alpha_composite(glow)
    img.alpha_composite(lay)
    img.alpha_composite(glow_l.filter(ImageFilter.GaussianBlur(3)))
    return img


# ------------------------------------------------------------------ fireworks
class Fireworks:
    def __init__(self):
        # (rocket launch time, burst time, burst x, burst y [frame coords], radius, palette, seed)
        gold = [(255, 226, 140), (255, 246, 210), (255, 190, 90)]
        pink = [(255, 160, 200), (255, 230, 240), (255, 200, 120)]
        self.shows = [(0.0, .75, 540, 690, 260, gold, 1), (1.9, 2.6, 190, 300, 230, gold, 2),
                      (2.3, 2.95, 930, 640, 170, pink, 3), (3.4, 4.0, 210, 260, 240, gold, 4),
                      (4.0, 4.6, 900, 430, 180, gold, 5), (4.6, 5.2, 160, 820, 150, pink, 6),
                      (5.3, 5.9, 880, 300, 210, gold, 7), (5.9, 6.4, 260, 520, 200, gold, 8),
                      (6.1, 6.7, 880, 380, 190, pink, 9), (7.0, 7.6, 190, 300, 230, gold, 10),
                      (7.6, 8.2, 920, 690, 170, gold, 11), (8.2, 8.8, 300, 260, 240, gold, 12),
                      (8.7, 9.3, 860, 470, 190, pink, 13)]
        self.parts = {}
        for _, _, _, _, r, _, seed in self.shows:
            rng = np.random.default_rng(seed)
            n = 150
            ang = rng.uniform(0, 2 * np.pi, n)
            spd = r * rng.uniform(.55, 1.0, n)
            self.parts[seed] = (ang, spd, rng.integers(0, 3, n), rng.uniform(.0, .4, n))

    def draw(self, img, t, view):
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for t0, tb, bx, by, r, pal, seed in self.shows:
            by_c = by + (PAN - view)                       # follow the camera during the opening tilt
            if t0 <= t < tb:                               # rocket climbing
                p = (t - t0) / (tb - t0)
                sx = bx + (seed % 3 - 1) * 30
                y0 = H + 80 + (PAN - view)
                y = y0 + (by_c - y0) * (1 - (1 - p) ** 2)
                x = sx + (bx - sx) * p
                for k in range(10):
                    yy = y + k * 14
                    a = int(220 * (1 - k / 10))
                    d.ellipse((x - 3, yy - 3, x + 3, yy + 3), fill=(255, 236, 180, a))
                d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(255, 255, 230, 255))
            age = t - tb
            if 0 <= age < 2.0:
                ang, spd, ci, delay = self.parts[seed]
                for trail in (0, .05, .1):
                    a_ = age - trail
                    if a_ <= 0:
                        continue
                    dist = spd * (1 - np.exp(-a_ * 3.2))
                    xs = bx + np.cos(ang) * dist
                    ys = by_c + np.sin(ang) * dist + 60 * a_ ** 2
                    fade = clamp(1 - (a_ - .6) / 1.3) * (1 - trail * 6)
                    twinkle = (np.sin(a_ * 40 + delay * 50) > -.3)
                    for x, y, c, tw in zip(xs, ys, ci, twinkle):
                        if not tw and trail == 0 and a_ > .7:
                            continue
                        s = 3.2 if trail == 0 else 2.0
                        d.ellipse((x - s, y - s, x + s, y + s), fill=pal[c] + (int(255 * fade),))
                if age < .12:                              # small soft flash at the moment of the burst
                    rr = 14 * (1 - age / .12) + 6
                    d.ellipse((bx - rr, by_c - rr, bx + rr, by_c + rr), fill=(255, 240, 200, int(80 * (1 - age / .12))))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(5)))
        img.alpha_composite(lay)


# ------------------------------------------------------------------ titles
def put(img, im, cx, cy, s=1.0, a=1.0, blur=0.0):
    if a <= 0 or s <= 0:
        return
    if abs(s - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
    if blur > .5:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    if a < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


# ------------------------------------------------------------------ lettering
def _shift(mask, dx, dy):
    return mask.transform(mask.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy))


def lux_text(text, font, depth=14, outline=6, bulbs=0, tracking=0):
    """Marquee-style festive lettering: metallic gold face with bevel, red 3D sides, gold rim + dark keyline,
    warm glow and (optionally) light bulbs inside the strokes. Returns (bulbs on, bulbs dimmed) images."""
    pad = depth + outline + 30
    if tracking:
        widths = [font.getlength(c) for c in text]
        tw = sum(widths) + tracking * (len(text) - 1)
    else:
        tw = font.getlength(text)
    asc, desc = font.getmetrics()
    w, h = int(tw) + 2 * pad, asc + desc + 2 * pad
    mask = Image.new("L", (w, h), 0)
    dm = ImageDraw.Draw(mask)
    if tracking:
        x = pad
        for c, cw in zip(text, widths):
            dm.text((x, pad), c, font=font, fill=255)
            x += cw + tracking
    else:
        dm.text((pad, pad), text, font=font, fill=255)
    bb = mask.getbbox()
    rim = mask.filter(ImageFilter.MaxFilter(2 * outline + 1))
    key = rim.filter(ImageFilter.MaxFilter(5))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow = Image.new("RGBA", (w, h), (255, 160, 60, 0))
    glow.putalpha(key.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * .45)))
    out.alpha_composite(glow)
    for i in range(depth, 0, -1):                                # red 3D sides, darker towards the back
        t = i / depth
        col = (int(190 - 90 * t), int(34 - 20 * t), int(40 - 18 * t), 255)
        out.paste(Image.new("RGBA", (w, h), col), (int(i * .3), i), key)
    out.paste(Image.new("RGBA", (w, h), (70, 6, 20, 255)), (0, 0), key)            # dark keyline
    # gold rim with its own light-to-dark gradient
    yy = np.clip((np.arange(h) - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)[:, None, None]
    rim_col = np.array([255, 236, 170]) * (1 - yy) + np.array([196, 120, 30]) * yy
    out.paste(Image.fromarray(np.repeat(rim_col, w, axis=1).astype(np.uint8)).convert("RGBA"), (0, 0), rim)
    # metallic face: banded gradient
    stops = [(0, (255, 251, 222)), (.32, (255, 214, 96)), (.58, (214, 136, 26)), (.74, (255, 222, 120)), (1, (182, 102, 18))]
    face = np.zeros((h, 1, 3), np.float32)
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = ((yy >= a) & (yy <= b)).astype(np.float32)
        face += m * (np.array(ca) + (np.array(cb) - np.array(ca)) * np.clip((yy - a) / (b - a), 0, 1))
    out.paste(Image.fromarray(np.repeat(face, w, axis=1).clip(0, 255).astype(np.uint8)).convert("RGBA"), (0, 0), mask)
    # bevel: bright top edges, darker bottom edges
    m = np.asarray(mask, np.int16)
    top = np.clip(m - np.asarray(_shift(mask, 0, 4), np.int16), 0, 255).astype(np.uint8)
    bot = np.clip(m - np.asarray(_shift(mask, 0, -4), np.int16), 0, 255).astype(np.uint8)
    out.paste(Image.new("RGBA", (w, h), (255, 255, 240, 255)), (0, 0), Image.fromarray(top).point(lambda v: int(v * .85)))
    out.paste(Image.new("RGBA", (w, h), (140, 70, 10, 255)), (0, 0), Image.fromarray(bot).point(lambda v: int(v * .6)))
    dim = out.copy()
    if bulbs:
        core = mask.filter(ImageFilter.MinFilter(int(bulbs * 1.4) | 1))
        ca = np.asarray(core) > 128
        on = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        off = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        don, doff = ImageDraw.Draw(on), ImageDraw.Draw(off)
        halo = Image.new("RGBA", (w, h), (255, 190, 80, 0))
        dh = ImageDraw.Draw(halo)
        step = int(bulbs * 2.6)
        k = 0
        for y in range(bb[1], bb[3], step):
            for x in range(bb[0] + (step // 2 if (y // step) % 2 else 0), bb[2], step):
                if 0 <= y < h and 0 <= x < w and ca[y, x]:
                    r = bulbs * .5
                    big = (k % 2 == 0)
                    don.ellipse((x - r, y - r, x + r, y + r), fill=(255, 252, 228, 255))
                    dh.ellipse((x - r * 2.6, y - r * 2.6, x + r * 2.6, y + r * 2.6), fill=(255, 200, 90, 150))
                    doff.ellipse((x - r, y - r, x + r, y + r), fill=(255, 246, 210, 255) if big else (236, 176, 70, 255))
                    k += 1
        halo = halo.filter(ImageFilter.GaussianBlur(bulbs * .8))
        out.alpha_composite(halo)
        out.alpha_composite(on)
        dim.alpha_composite(off)
    box = out.getbbox()
    return out.crop(box), dim.crop(box)


def ribbon(text, font, tracking=6, fill=(122, 16, 44), edge=(240, 196, 100), ink=(255, 236, 190)):
    widths = [font.getlength(c) for c in text]
    tw = int(sum(widths) + tracking * (len(text) - 1))
    asc, desc = font.getmetrics()
    bh = asc + desc + 34
    tail = 46
    w = tw + 120 + 2 * tail
    s = 2
    im = Image.new("RGBA", (w * s, (bh + 24) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y0, y1 = 12 * s, (12 + bh) * s
    dark = tuple(int(c * .6) for c in fill)
    for side in (0, 1):                                          # folded tails
        x0 = 0 if side == 0 else (w - tail - 30) * s
        pts = [(x0, y0 + 18 * s), (x0 + (tail + 30) * s, y0 + 18 * s), (x0 + (tail + 30) * s, y1 + 12 * s), (x0, y1 + 12 * s)]
        notch = (x0 + 22 * s, (y0 + y1) / 2 + 15 * s) if side == 0 else (x0 + (tail + 8) * s, (y0 + y1) / 2 + 15 * s)
        d.polygon(pts[:2] + ([pts[2], pts[3], notch] if side == 0 else [notch, pts[2], pts[3]]) if False else
                  ([pts[0], pts[1], pts[2], pts[3], notch] if side == 0 else [pts[0], pts[1], notch, pts[2], pts[3]]), fill=dark + (255,))
    d.rectangle((tail * s, y0, (w - tail) * s, y1), fill=fill + (255,))
    d.rectangle((tail * s, y0 + 6 * s, (w - tail) * s, y0 + 10 * s), fill=edge + (255,))
    d.rectangle((tail * s, y1 - 10 * s, (w - tail) * s, y1 - 6 * s), fill=edge + (255,))
    im = im.resize((w, bh + 24), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    x = (w - tw) / 2
    for c, cw in zip(text, widths):
        d.text((x, 12 + bh / 2 + 1), c, font=font, fill=ink, anchor="lm")
        x += cw + tracking
    sh = Image.new("RGBA", im.size, (30, 0, 10, 0))
    sh.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * .5)))
    out = Image.new("RGBA", (im.width, im.height + 10), (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 8))
    out.alpha_composite(im)
    return out


def shine(im, phase):
    """Diagonal light sweep across an image's opaque pixels; phase 0..1 moves it left to right."""
    if not 0 <= phase <= 1:
        return im
    w, h = im.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    band = -w * .4 + w * 1.8 * phase
    k = np.exp(-(((xx - band) + (yy - h / 2) * .5) / (w * .06)) ** 2)
    a = (np.asarray(im.getchannel("A"), np.float32) / 255 * k * 170).astype(np.uint8)
    out = im.copy()
    lay = Image.new("RGBA", im.size, (255, 255, 240, 0))
    lay.putalpha(Image.fromarray(a))
    out.alpha_composite(lay)
    return out


class Titles:
    def __init__(self, fonts_dir):
        fs = lambda pkg, f, s: ImageFont.truetype(os.path.join(fonts_dir, f"fontsource-{pkg}", "package", "files", f), s)  # noqa: E731
        alfa = lambda s: fs("alfa-slab-one", "alfa-slab-one-latin-400-normal.woff2", s)  # noqa: E731
        rozha = lambda s: fs("rozha-one", "rozha-one-latin-400-normal.woff2", s)  # noqa: E731
        pop = lambda s: fs("poppins", "poppins-latin-800-normal.woff2", s)  # noqa: E731
        cin, cor = C.fonts(fonts_dir)
        frame, _ = C.badge(cin, cor)
        k = .9
        self.frame = frame.resize((int(frame.width * k), int(frame.height * k)), Image.LANCZOS)
        fw, fh = self.frame.size
        self.parts = [("diwali", lux_text("Diwali", rozha(128), depth=8, outline=4), (fw / 2, fh * .3)),
                      ("dhamaka", lux_text("DHAMAKA", alfa(92), depth=9, outline=4, tracking=2), (fw / 2, fh * .52)),
                      ("sale", lux_text("SALE", alfa(78), depth=8, outline=4, tracking=6), (fw / 2, fh * .72)),
                      ("diya", (C.diya(80),) * 2, (fw / 2, fh - 56))]
        flat = lux_text("FLAT", alfa(104), depth=10, outline=5, tracking=4)[0]
        off = lux_text("OFF", alfa(104), depth=10, outline=5, tracking=8)[0]
        self.pct = lux_text("20%", alfa(300), depth=18, outline=8, bulbs=15)
        left = Image.new("RGBA", (max(flat.width, off.width), flat.height + off.height - 18), (0, 0, 0, 0))
        left.alpha_composite(flat, ((left.width - flat.width) // 2, 0))
        left.alpha_composite(off, ((left.width - off.width) // 2, flat.height - 18))
        self.left = left
        self.all = ribbon("ON ALL PRODUCTS", pop(46), tracking=5)
        self.till_rb = ribbon("OFFER VALID TILL", pop(44), tracking=5)
        self.date = lux_text("9 NOV", alfa(230), depth=16, outline=7, bulbs=13, tracking=6)
        pill = Image.new("RGBA", (820, 130), (0, 0, 0, 0))
        dp = ImageDraw.Draw(pill)
        g = np.linspace(0, 1, 120)[:, None, None]
        grad = np.array([255, 230, 150]) * (1 - g) + np.array([214, 150, 50]) * g
        gi = Image.fromarray(np.repeat(grad, 810, axis=1).astype(np.uint8)).convert("RGBA")
        m = Image.new("L", (810, 120), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, 809, 119), radius=60, fill=255)
        dp.rounded_rectangle((0, 0, 819, 129), radius=65, fill=(110, 14, 40, 255))
        pill.paste(gi, (5, 5), m)
        dp.text((410, 50), "SHOP NOW AT", font=pop(26), fill=(110, 14, 40), anchor="mm")
        dp.text((410, 88), "kalakaricreations.com", font=pop(44), fill=(110, 14, 40), anchor="mm")
        self.pill = pill
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo.resize((520, int(520 * logo.height / logo.width)), Image.LANCZOS)

    @staticmethod
    def pick(pair, t):
        return pair[int(t / .22) % 2]                              # twinkling bulbs

    def draw(self, img, t):
        out_a = 1 - clamp((t - T_OUT) / .15)
        out_s = 1 - .35 * ease((t - T_OUT) / .15)
        if t >= BADGE_IN and out_a > 0:
            b = self.frame.copy()
            starts = {"diwali": T_DIWALI, "dhamaka": T_DHAMAKA, "sale": T_SALE, "diya": T_SALE}
            for n, pair, (cx, cy) in self.parts:
                q = (t - starts[n]) / .25
                if q > 0:
                    put(b, pair[0], cx, cy, 1 + .45 * (1 - back(q)), min(1.0, q * 2))
            p = (t - BADGE_IN) / .3
            put(img, b, W / 2, 680, (.1 + .9 * back(p)) * out_s, min(1.0, p * 3) * out_a)
        q = (t - T_OFFER) / .3
        if q > 0 and out_a > 0:
            pct = shine(self.pick(self.pct, t), ((t - T_OFFER - .35) % 2.0) / .8)
            gap = 10
            total = self.left.width + gap + pct.width
            fit = min(1.0, 990 / total)                         # keep the whole group inside the frame
            s = (.2 + .8 * back(q, 2.2)) * out_s * fit
            a = min(1.0, q * 3) * out_a
            put(img, self.left, W / 2 - total * s / 2 + self.left.width * s / 2, 1140, s, a)
            put(img, pct, W / 2 + total * s / 2 - pct.width * s / 2, 1130, s, a)
        q = (t - T_ALL) / .3
        if q > 0 and out_a > 0:
            put(img, self.all, W / 2, 1352, (.6 + .4 * back(q)) * out_s, min(1.0, q * 2) * out_a)
        q = (t - T_TILL) / .4
        if q > 0:
            put(img, self.till_rb, W / 2, 790, .7 + .3 * back(q), min(1.0, q * 2))
            date = shine(self.pick(self.date, t), ((t - T_TILL - .5) % 2.0) / .8)
            put(img, date, W / 2, 960, 1 + .9 * (1 - ease(q)), min(1.0, q * 1.6), blur=14 * (1 - ease(q)))
        q = (t - T_WEB) / .3
        if q > 0:
            put(img, self.pill, W / 2, 1180, .6 + .4 * back(q), min(1.0, q * 2))
            put(img, self.logo, W / 2, 600, 1.0, min(1.0, max(0.0, q - .3) * 2))


class Reel:
    def __init__(self, fonts_dir):
        self.scene = scenery()
        self.fw = Fireworks()
        self.titles = Titles(fonts_dir)

    def frame(self, t):
        vy = int(round(PAN * ease(t / .65)))                   # tilt down: top of the sky -> the avenue
        img = self.scene.crop((0, vy, W, vy + H))
        self.fw.draw(img, t, vy)
        self.titles.draw(img, t)
        return img


def main():
    fonts_dir, music, out = sys.argv[1:4]
    r = Reel(fonts_dir)
    n = int(TOTAL * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
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
        r = Reel(sys.argv[1])
        for t in map(float, sys.argv[4:]):
            r.frame(t).convert("RGB").resize((360, 640)).save(os.path.join(sys.argv[3], f"do_{t:04.1f}.png"))
    else:
        main()
