#!/usr/bin/env python3
"""4-slide 4:5 "Most Wanted Fits" carousel: neon-sunset, game-cover style illustrations of three looks.

1. Cover: five diagonal panels cut from the illustrations, split by thick black borders; a sunset-filled "KK"
   monogram badge; and "most / wanted / fits" stacked in a heavy condensed lowercase face, white with a black
   outline and a red-pink rim.
2. Denim Paisley co-ord.  3. Folk-Art Mustard co-ord.
4. Green Jaipuri suit with "mission" (blue-violet-magenta gradient) and a smaller "passed" under it on the right.
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


PASSION = os.path.join(FONTS, "fontsource-passion-one", "package", "files", "passion-one-latin-900-normal.woff2")


def word_layer(text, size, stretch=1.18):
    """A word in the heavy condensed display face, stretched taller like the reference's title type.
    Returns (glyph mask, offset) on a padded canvas."""
    f = ImageFont.truetype(PASSION, size)
    bb = f.getbbox(text)
    pad = int(size * 0.3)
    m = Image.new("L", (bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad), 0)
    ImageDraw.Draw(m).text((pad - bb[0], pad - bb[1]), text, font=f, fill=255)
    return m.resize((m.width, int(m.height * stretch)), Image.LANCZOS)


def stroke(mask, px):
    return mask.filter(ImageFilter.MaxFilter(px * 2 + 1)) if px > 0 else mask


def stamp(canvas, mask, cx, cy, face, rims, shadow=(0, 0, 0, 150), shadow_off=(8, 12)):
    """Composite a word: drop shadow, then rims (outermost first), then the face (a colour or an RGBA image)."""
    x, y = int(cx - mask.width / 2), int(cy - mask.height / 2)
    outer = stroke(mask, rims[0][1])
    sh = Image.new("RGBA", mask.size, shadow)
    sh.putalpha(outer.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * shadow[3] / 255)))
    canvas.alpha_composite(sh, (x + shadow_off[0], y + shadow_off[1]))
    for col, px in rims:
        lay = Image.new("RGBA", mask.size, col + (255,))
        lay.putalpha(stroke(mask, px))
        canvas.alpha_composite(lay, (x, y))
    if isinstance(face, Image.Image):
        lay = face.resize(mask.size).convert("RGBA")
    else:
        lay = Image.new("RGBA", mask.size, face + (255,))
    lay.putalpha(mask)
    canvas.alpha_composite(lay, (x, y))


def vgrad(size, stops):
    w, h = size
    t = np.linspace(0, 1, h)[:, None]
    pos = np.array([p for p, _ in stops])
    cols = np.array([c for _, c in stops], float)
    out = np.stack([np.interp(t[:, 0], pos, cols[:, k]) for k in range(3)], -1)
    return Image.fromarray(np.repeat(out[:, None, :], w, 1).astype(np.uint8))


def sunset_scene(w, h):
    """Sunset fill for the badge letters: gradient sky, a striped sun, a skyline and palm silhouettes."""
    im = vgrad((w, h), [(0, (255, 70, 150)), (0.45, (255, 120, 90)), (0.75, (255, 190, 80)), (1, (255, 225, 120))])
    d = ImageDraw.Draw(im)
    r = w * 0.2
    d.ellipse((w / 2 - r, h * 0.42 - r, w / 2 + r, h * 0.42 + r), fill=(255, 225, 110))
    for k in range(5):
        y = h * 0.47 + k * h * 0.045
        d.rectangle((0, y, w, y + 3 + k * 2), fill=(255, 110, 120))
    rng = np.random.default_rng(4)
    x = 0
    while x < w:                                       # skyline
        bw, bh = rng.uniform(w * 0.03, w * 0.06), rng.uniform(h * 0.05, h * 0.16)
        d.rectangle((x, h * 0.84 - bh, x + bw, h), fill=(150, 40, 110))
        x += bw * rng.uniform(0.8, 1.2)
    d.rectangle((0, h * 0.84, w, h), fill=(110, 30, 90))
    for px, ph, lean in ((w * 0.12, h * 0.72, 0.06), (w * 0.88, h * 0.75, -0.06), (w * 0.36, h * 0.5, 0.04), (w * 0.64, h * 0.55, -0.04)):
        base = (px, h)
        top = (px + lean * w, h - ph)
        d.line([base, top], fill=(60, 15, 60), width=max(4, int(w * 0.012)))
        L = w * 0.15
        # tapered fronds fanning out to the sides and drooping under their own weight
        for vx, vy in ((-1, -0.45), (-1, 0.05), (-0.45, -0.9), (1, -0.45), (1, 0.05), (0.45, -0.9), (0.05, -1)):
            n = math.hypot(vx, vy)
            vx, vy = vx / n, vy / n
            spine = [(top[0] + vx * L * t, top[1] + vy * L * t + L * 0.6 * t * t) for t in np.linspace(0, 1, 14)]
            left, right = [], []
            for j, (x, y) in enumerate(spine):
                t = j / 13
                wdt = L * 0.11 * math.sin(math.pi * min(1, t * 1.1)) + 1
                nx, ny = -vy, vx
                left.append((x + nx * wdt, y + ny * wdt))
                right.append((x - nx * wdt, y - ny * wdt))
            d.polygon(left + right[::-1], fill=(60, 15, 60))
    return im


def cover(den, mus, grn):
    im = fit(grn, W, H)
    # panels in paint order: (image, scale, dx, dy, polygon); each image is placed so its subject sits in its panel
    panels = [
        (grn, 0.72, 400, 150, [(432, 520), (1080, 380), (1080, 1350), (700, 1350), (560, 900)]),
        (den, 0.75, -520, -150, [(0, 0), (640, 0), (432, 520), (300, 860), (0, 760)]),
        (mus, 0.60, 230, -70, [(640, 0), (1080, 0), (1080, 380), (432, 520)]),
        (den, 0.70, -990, 235, [(0, 760), (300, 860), (430, 1350), (0, 1350)]),
        (mus, 0.70, 470, 700, [(300, 860), (560, 900), (700, 1350), (430, 1350)]),
    ]
    edges = []
    for src, sc, dx, dy, poly in panels:
        big = src.resize((round(src.width * sc), round(src.height * sc)), Image.LANCZOS)
        layer = fit(src, W, H)
        layer.paste(big, (dx, dy))
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon(poly, fill=255)
        im.paste(layer, (0, 0), m)
        edges.append(poly)
    d = ImageDraw.Draw(im)
    on_edge = lambda p: p[0] in (0, W) or p[1] in (0, H)
    for poly in edges:                                # thick black borders between panels (not round the slide)
        for a, b in zip(poly, poly[1:] + poly[:1]):
            if not (on_edge(a) and on_edge(b)):
                d.line([a, b], fill=(8, 6, 10), width=18)
    im = im.convert("RGBA")
    # the badge: our KK monogram letters filled with a sunset scene, outlined in black and hot pink
    kk = word_layer("KK", 470, 1.12)
    scene = sunset_scene(kk.width, kk.height)
    stamp(im, kk, W / 2, 445, scene, [((232, 40, 110), 16), ((8, 6, 10), 11)])
    # title: white, black outline, a thin red-pink rim, stacked and overlapping like the reference
    for text, size, cy in (("most", 205, 660), ("wanted", 205, 810), ("fits", 205, 960)):
        stamp(im, word_layer(text, size), W / 2, cy, (255, 255, 255), [((226, 34, 74), 17), ((8, 6, 10), 12)])
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
    m1 = word_layer("mission", 250, 1.15)
    stamp(s4, m1, W / 2, 175, vgrad(m1.size, [(0, (150, 210, 255)), (0.45, (190, 150, 255)), (1, (236, 60, 220))]),
          [((40, 10, 60), 12)], shadow=(20, 0, 40, 200), shadow_off=(6, 10))
    m2 = word_layer("passed", 120, 1.15)
    stamp(s4, m2, W / 2 + m1.width / 2 - m2.width / 2 - 40, 335,
          vgrad(m2.size, [(0, (255, 140, 240)), (1, (210, 40, 200))]), [((40, 10, 60), 9)],
          shadow=(20, 0, 40, 200), shadow_off=(5, 8))
    s4.convert("RGB").save(os.path.join(out, "slide-4.jpg"), quality=94)
    print(out)


if __name__ == "__main__":
    main()
