#!/usr/bin/env python3
"""4-slide 4:5 "Most Wanted Fits" carousel: neon-sunset, game-cover style illustrations of three looks.

1. Cover: the three illustrations as diagonal panels split by black bars, with a sunset badge in the middle and a
   chunky white "MOST WANTED FITS" title outlined in black and hot pink. (An original title treatment: no game logo.)
2. Denim Paisley co-ord.  3. Folk-Art Mustard co-ord.  4. Green Jaipuri suit with "MISSION COMPLETE" at the top.
The Gemini sparkle mark in each illustration's bottom-right corner is inpainted out.

Usage:
    python3 most_wanted_fits_carousel.py <illustrations-dir> <out-dir>
"""
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
FONTS = os.environ.get("KK_FONTS", "/tmp/claude-0/-home-user-kala-kari-creations/"
                       "b594b16c-4df2-59b6-99e4-9ab0ec789fa6/scratchpad/fonts")
BUNGEE = os.path.join(FONTS, "fontsource-bungee", "package", "files", "bungee-latin-400-normal.woff2")
PINK = (232, 40, 120)


def load(path):
    """The illustration with its bottom-right sparkle mark inpainted away."""
    im = cv2.cvtColor(np.asarray(Image.open(path).convert("RGB")), cv2.COLOR_RGB2BGR)
    h, w = im.shape[:2]
    m = np.zeros((h, w), np.uint8)
    s = int(min(w, h) * 0.075)
    m[h - s - int(h * 0.01):h - int(h * 0.005), w - s - int(w * 0.01):w - int(w * 0.005)] = 255
    im = cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))


def fit(im, w, h, fy=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def outlined(lay, xy, text, size, fill=(255, 255, 255), inner=(15, 10, 20), outer=PINK, anchor="mm", grad=None):
    """Chunky title text: a hot-pink outer stroke, a black inner stroke, a white or gradient face."""
    f = ImageFont.truetype(BUNGEE, size)
    d = ImageDraw.Draw(lay)
    d.text(xy, text, font=f, fill=outer + (255,), anchor=anchor, stroke_width=int(size * 0.16), stroke_fill=outer + (255,))
    d.text(xy, text, font=f, fill=inner + (255,), anchor=anchor, stroke_width=int(size * 0.09), stroke_fill=inner + (255,))
    if grad is None:
        d.text(xy, text, font=f, fill=fill + (255,), anchor=anchor)
        return
    # gradient face: draw the glyphs as a mask and fill it with a vertical gradient
    m = Image.new("L", lay.size, 0)
    ImageDraw.Draw(m).text(xy, text, font=f, fill=255, anchor=anchor)
    bb = m.getbbox()
    g = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3] + 1):
        t = (y - bb[1]) / max(1, bb[3] - bb[1])
        c = tuple(int(grad[0][k] * (1 - t) + grad[1][k] * t) for k in range(3))
        gd.line([(bb[0], y), (bb[2], y)], fill=c + (255,))
    lay.paste(g, (0, 0), m)


def cover(den, mus, grn):
    im = Image.new("RGB", (W, H), (10, 8, 14))
    # three panels split by diagonal lines: top-left (denim), right (green), bottom-left (mustard). Each
    # illustration is scaled and shifted so its figure sits in its panel: (image, scale, dx, dy, polygon)
    panels = [
        (den, 0.80, -520, -150, [(0, 0), (720, 0), (330, H * 0.62), (0, H * 0.70)]),
        (grn, 0.70, 380, -10, [(720, 0), (W, 0), (W, H), (560, H), (330, H * 0.62)]),
        (mus, 0.62, -380, 830, [(0, H * 0.70), (330, H * 0.62), (560, H), (0, H)]),
    ]
    for src, sc, dx, dy, poly in panels:
        big = src.resize((round(src.width * sc), round(src.height * sc)), Image.LANCZOS)
        layer = fit(src, W, H)                    # filler behind, in case the scaled image doesn't cover the panel
        layer.paste(big, (dx, dy))
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon(poly, fill=255)
        im.paste(layer, (0, 0), m)
    d = ImageDraw.Draw(im)
    for a, b in (((720, 0), (330, H * 0.62)), ((330, H * 0.62), (0, H * 0.70)), ((330, H * 0.62), (560, H))):
        d.line([a, b], fill=(10, 8, 14), width=16)
    # the sunset badge behind the title: a slanted shield with a sun, stripes and palms
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bx0, by0, bx1, by1 = 250, 430, 830, 960
    badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    for y in range(by0, by1):
        t = (y - by0) / (by1 - by0)
        c = (int(250 - 40 * t), int(80 + 110 * t), int(150 - 100 * t))
        bd.line([(bx0, y), (bx1, y)], fill=c + (255,))
    bd.ellipse((W / 2 - 150, by0 + 40, W / 2 + 150, by0 + 340), fill=(255, 214, 90, 255))
    for k in range(5):
        y = by0 + 220 + k * 22
        bd.rectangle((bx0, y, bx1, y + 8 + k), fill=(236, 90, 130, 255))
    shield = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shield).polygon([(bx0 + 30, by0), (bx1, by0 - 20), (bx1 - 30, by1), (bx0, by1 + 20)], fill=255)
    stroke = shield.filter(ImageFilter.MaxFilter(25))
    lay.paste(Image.new("RGBA", (W, H), (10, 8, 14, 255)), (0, 0), stroke)
    lay.paste(badge, (0, 0), shield)
    im = im.convert("RGBA")
    im.alpha_composite(lay)
    t = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for word, y, s in (("MOST", 560, 150), ("WANTED", 700, 132), ("FITS", 840, 150)):
        outlined(t, (W / 2, y), word, s)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(t.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6)))
    im.alpha_composite(sh, (6, 10))
    im.alpha_composite(t)
    return im.convert("RGB")


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    den = load(os.path.join(src, "denim-coord-parking.webp"))
    mus = load(os.path.join(src, "mustard-coord-car.webp"))
    grn = load(os.path.join(src, "green-suit-boutique.webp"))
    cover(den, mus, grn).save(os.path.join(out, "slide-1.jpg"), quality=94)
    fit(den, W, H).save(os.path.join(out, "slide-2.jpg"), quality=94)
    fit(mus, W, H).save(os.path.join(out, "slide-3.jpg"), quality=94)
    s4 = fit(grn, W, H, 0.07).convert("RGBA")
    t = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    outlined(t, (W / 2, 120), "MISSION", 150, grad=((150, 200, 255), (236, 60, 210)), outer=(20, 10, 30),
             inner=(255, 255, 255))
    outlined(t, (W / 2 + 150, 245), "COMPLETE", 78, grad=((255, 120, 220), (200, 40, 200)), outer=(20, 10, 30),
             inner=(255, 255, 255))
    s4.alpha_composite(t)
    s4.convert("RGB").save(os.path.join(out, "slide-4.jpg"), quality=94)
    print(out)


if __name__ == "__main__":
    main()
