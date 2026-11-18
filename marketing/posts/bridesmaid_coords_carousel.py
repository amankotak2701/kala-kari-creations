#!/usr/bin/env python3
"""9-slide 4:5 "If you're a 2026 bridesmaid" co-ord carousel, in the layout of the reference post.

1. A full-bleed model photo with a cream papercut-style frame in the middle: "IF YOU'RE A / 2026 / BRIDESMAID"
   in rust serif caps, "This is for you!" in italic, a dhol on each side, and the brand name under the frame.
2-8. A burnt-orange background, one co-ord look cut out with a white sticker outline, a line in bold white caps
   (one or two words per line), and one flat festive illustration: a marigold urli, a chhatri, dhols with laddoos,
   a toran, a dhol with sticks, bangles, or garlanded matkas on a rangoli.
9. The papercut frame on orange: "YOUR PRE-WEDDING WARDROBE, SORTED / Save this for your next wedding invite."
   with a pair of kaleere, and the brand name under it.

The illustrations and the frame are drawn here in code.

Usage:
    python3 bridesmaid_coords_carousel.py <photo-dir> <out-dir>
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
SS = 2                                     # supersampling for the drawings
FONTS = os.environ.get("KK_FONTS", "/tmp/claude-0/-home-user-kala-kari-creations/"
                       "b594b16c-4df2-59b6-99e4-9ab0ec789fa6/scratchpad/fonts")
ORANGE = (190, 82, 36)
CREAM = (246, 241, 232)
RUST = (186, 78, 34)
BRAND = (58, 38, 34)
MARIGOLD = (245, 150, 30)
YELLOW = (250, 200, 50)
PINK = (226, 52, 120)
GREEN = (60, 140, 60)
GOLD = (222, 168, 60)
BROWN = (120, 62, 34)

# (cutout, model side, words, illustration, illustration box (x0, y0, x1, y1) as fractions, text top y)
SLIDES = [
    ("2-denim-paisley", "R", ["NOT", "EVERY", "FUNCTION", "NEEDS", "A", "LEHENGA"], "urli",
     (0.09, 0.60, 0.44, 0.86), 0.255),
    ("3-mustard-folk-art", "R", ["SOMETIMES,", "A PRETTY", "CO-ORD SET", "DOES ALL", "THE", "TALKING."], "chhatri",
     (0.06, 0.18, 0.40, 0.46), 0.475),
    ("4-black-white", "L", ["FOR THE", "GIRLS", "WHO", "LOVE A", "LITTLE", "DRAMA"], "laddoo",
     (0.48, 0.66, 0.92, 0.92), 0.29),
    ("5-indigo-floral", "R", ["A LITTLE", "TWIRL", "NEVER", "HURT", "ANYONE"], "toran",
     (0.08, 0.0, 0.37, 0.44), 0.52),
    ("6-black-sleeveless", "L", ["BECAUSE", "THE", "CELEBRATIONS", "START WAY", "BEFORE THE", "WEDDING", "DAY"],
     "dhol", (0.47, 0.67, 0.90, 0.92), 0.275),
    ("7-black-collared", "L", ["YOUR", "OUTFIT", "SHOULD", "MATCH", "THE", "MOOD,", "NOT JUST", "THE", "OCCASION"],
     "bangles", (0.62, 0.20, 0.83, 0.33), 0.355),
    ("8-offwhite-deer", "L", ["YOUR PRE-", "WEDDING", "WARDROBE ,", "SORTED"], "matkas",
     (0.50, 0.58, 0.94, 1.0), 0.28),
]


def font(fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(FONTS, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def canvas(w, h):
    return Image.new("RGBA", (int(w * SS), int(h * SS)), (0, 0, 0, 0))


def down(im, w, h):
    return im.resize((int(w), int(h)), Image.LANCZOS)


def shade(c, k):
    return tuple(int(max(0, min(255, v * k))) for v in c[:3])


# ---------------- illustrations (flat, festive) ----------------

def marigold(d, x, y, r, col):
    for ring, rr in ((0, 1.0), (1, 0.72), (2, 0.45)):
        n = 14 - ring * 3
        c = shade(col, 1.0 - ring * 0.06)
        for k in range(n):
            a = 2 * math.pi * k / n + ring * 0.3
            px, py = x + rr * r * 0.62 * math.cos(a), y + rr * r * 0.62 * math.sin(a)
            pr = r * 0.32 * rr + r * 0.06
            d.ellipse((px - pr, py - pr, px + pr, py + pr), fill=c + (255,), outline=shade(c, 0.8) + (255,),
                      width=max(1, int(r * 0.03)))
    d.ellipse((x - r * 0.18, y - r * 0.18, x + r * 0.18, y + r * 0.18), fill=shade(col, 0.75) + (255,))


def jasmine(d, x, y, r, rot=0.0):
    for k in range(5):
        a = rot + 2 * math.pi * k / 5
        px, py = x + r * 0.5 * math.cos(a), y + r * 0.5 * math.sin(a)
        d.ellipse((px - r * 0.42, py - r * 0.22, px + r * 0.42, py + r * 0.22), fill=(255, 255, 255, 255))
        d.polygon([(x, y), (x + r * math.cos(a - 0.25), y + r * math.sin(a - 0.25)),
                   (x + r * 1.05 * math.cos(a), y + r * 1.05 * math.sin(a)),
                   (x + r * math.cos(a + 0.25), y + r * math.sin(a + 0.25))], fill=(255, 255, 255, 255))
    d.ellipse((x - r * 0.15, y - r * 0.15, x + r * 0.15, y + r * 0.15), fill=(250, 210, 90, 255))


def ill_urli(w, h):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S = im.width
    cx = S * 0.5
    # copper bowl
    by0, by1 = im.height * 0.5, im.height * 0.86
    d.ellipse((S * 0.1, by0 - S * 0.06, S * 0.9, by0 + S * 0.06), fill=(196, 120, 92, 255))
    d.chord((S * 0.1, by0 - (by1 - by0), S * 0.9, by1), 0, 180, fill=(214, 140, 110, 255))
    d.chord((S * 0.16, by0 - (by1 - by0) * 0.85, S * 0.84, by1 - (by1 - by0) * 0.08), 10, 170,
            fill=(236, 172, 140, 255))
    d.ellipse((S * 0.35, by1 - S * 0.03, S * 0.65, by1 + S * 0.03), fill=(170, 96, 70, 255))
    rng = np.random.default_rng(3)
    for k in range(16):                     # the marigold mound
        a = rng.uniform(0.0, math.pi)
        rr = rng.uniform(0.0, 0.34) * S
        x = cx + rr * math.cos(a) * 1.05
        y = by0 - rr * math.sin(a) * 0.62 - S * 0.03
        marigold(d, x, y, S * rng.uniform(0.075, 0.1), YELLOW if k % 3 == 0 else MARIGOLD)
    for _ in range(7):
        a = rng.uniform(0.2, math.pi - 0.2)
        jasmine(d, cx + S * 0.3 * math.cos(a), by0 - S * 0.2 * math.sin(a) - S * 0.02, S * 0.045, rng.uniform(0, 6))
    for x, y in ((0.12, 0.93), (0.3, 0.96), (0.8, 0.95)):      # fallen petals
        d.ellipse((S * x, im.height * y, S * x + S * 0.04, im.height * y + S * 0.02), fill=YELLOW + (255,))
    jasmine(d, S * 0.88, im.height * 0.93, S * 0.04, 0.3)
    return down(im, w, h)


def ill_chhatri(w, h):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    cx, cy, R = S * 0.5, Hh * 0.42, S * 0.46
    d.line([(cx, cy - R * 0.55), (cx + R * 0.25, Hh * 0.98)], fill=BROWN + (255,), width=int(S * 0.02))
    cols = [GREEN, MARIGOLD, GREEN, YELLOW, GREEN, MARIGOLD, GREEN, YELLOW]
    for k in range(8):                      # dome segments
        a0, a1 = math.pi + k * math.pi / 8, math.pi + (k + 1) * math.pi / 8
        d.pieslice((cx - R, cy - R * 0.62, cx + R, cy + R * 0.62), math.degrees(a0), math.degrees(a1),
                   fill=cols[k] + (255,))
        am = (a0 + a1) / 2                    # a little leaf motif on each segment
        mx, my = cx + R * 0.62 * math.cos(am), cy + R * 0.62 * 0.62 * math.sin(am)
        d.ellipse((mx - S * 0.025, my - S * 0.04, mx + S * 0.025, my + S * 0.04), fill=(250, 236, 200, 255))
    d.rectangle((cx - R, cy - 2, cx + R, cy + S * 0.035), fill=(214, 60, 60, 255))
    for k in range(19):                     # tassels
        x = cx - R + k * 2 * R / 18
        L = S * (0.18 if k % 2 else 0.26)
        d.line([(x, cy + S * 0.035), (x, cy + L)], fill=(230, 170, 50, 255), width=int(S * 0.006))
        c = [PINK, GREEN, (230, 60, 50), YELLOW][k % 4]
        d.ellipse((x - S * 0.012, cy + L * 0.55, x + S * 0.012, cy + L * 0.55 + S * 0.024), fill=c + (255,))
        d.polygon([(x - S * 0.018, cy + L), (x + S * 0.018, cy + L), (x, cy + L - S * 0.05)], fill=c + (255,))
        d.rectangle((x - S * 0.012, cy + L, x + S * 0.012, cy + L + S * 0.05), fill=c + (255,))
    d.ellipse((cx - S * 0.03, cy - R * 0.62 - S * 0.06, cx + S * 0.03, cy - R * 0.62), fill=(200, 120, 50, 255))
    return down(im, w, h)


def drum(d, x0, y0, x1, y1, body, band, rope):
    w = x1 - x0
    e = w * 0.16
    d.rectangle((x0, y0 + e / 2, x1, y1 - e / 2), fill=body + (255,))
    d.ellipse((x0, y1 - e, x1, y1), fill=body + (255,))
    for yy in (y0 + e * 0.9, y1 - e * 0.9):
        d.rectangle((x0, yy - e * 0.18, x1, yy + e * 0.18), fill=band + (255,))
    n = 6
    for k in range(n):
        xa = x0 + w * k / n
        xb = x0 + w * (k + 0.5) / n
        xc = x0 + w * (k + 1) / n
        d.line([(xa, y0 + e * 0.9), (xb, y1 - e * 0.9), (xc, y0 + e * 0.9)], fill=rope + (255,), width=max(2, int(w * 0.012)))
    d.ellipse((x0, y0, x1, y0 + e), fill=(246, 222, 170, 255), outline=band + (255,), width=max(2, int(w * 0.02)))


def tassel(d, x, y, s, c):
    d.line([(x, y), (x, y + s)], fill=c + (255,), width=max(2, int(s * 0.15)))
    d.polygon([(x - s * 0.25, y + s * 1.6), (x + s * 0.25, y + s * 1.6), (x, y + s * 0.8)], fill=c + (255,))


def ill_laddoo(w, h):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    rng = np.random.default_rng(5)
    for side in (-1, 1):                    # golden wheat sprigs
        bx = S * (0.5 + side * 0.44)
        for k in range(4):
            y = Hh * (0.25 + 0.18 * k)
            for j in range(3):
                a = -math.pi / 2 + side * (0.6 + 0.2 * j)
                d.ellipse((bx + side * j * S * 0.03 - S * 0.03, y - S * 0.015 - j * S * 0.02,
                           bx + side * j * S * 0.03 + S * 0.03, y + S * 0.015 - j * S * 0.02), fill=GOLD + (255,))
    drum(d, S * 0.17, Hh * 0.45, S * 0.47, Hh * 0.9, (110, 50, 34), (226, 70, 60), (240, 200, 80))
    drum(d, S * 0.38, Hh * 0.22, S * 0.72, Hh * 0.82, (236, 150, 60), (230, 120, 40), (190, 90, 40))
    # the dhol on its side in front
    x0, y0, x1, y1 = S * 0.45, Hh * 0.6, S * 0.88, Hh * 0.95
    d.rounded_rectangle((x0, y0, x1, y1), radius=(y1 - y0) * 0.3, fill=(236, 140, 52, 255))
    for k in range(6):
        xa = x0 + (x1 - x0) * k / 6
        d.line([(xa, y0 + 6), (xa + (x1 - x0) / 12, y1 - 6), (xa + (x1 - x0) / 6, y0 + 6)], fill=(250, 220, 140, 255),
               width=4)
    d.ellipse((x0 - S * 0.03, y0, x0 + S * 0.05, y1), fill=(246, 222, 170, 255), outline=(40, 100, 200, 255), width=8)
    for k in range(9):                      # laddoo pile on the dark drum
        r = S * 0.04
        row = 0 if k < 4 else (1 if k < 7 else 2)
        idx = k - (0, 4, 7)[row]
        x = S * 0.24 + idx * r * 1.8 + row * r * 0.9
        y = Hh * 0.47 - row * r * 1.5
        d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 200, 60, 255), outline=(230, 170, 40, 255), width=3)
    for x in np.linspace(S * 0.4, S * 0.7, 5):
        tassel(d, x, Hh * 0.24, S * 0.035, [(40, 140, 200), PINK, YELLOW, GREEN, (40, 140, 200)][int(x) % 5])
    for _ in range(14):
        x, y = rng.uniform(0.05, 0.95) * S, rng.uniform(0.15, 1.0) * Hh
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=[(40, 120, 220), PINK, YELLOW][rng.integers(3)] + (255,))
    return down(im, w, h)


def ill_toran(w, h):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    cx, cy, R = S * 0.5, Hh * 0.34, S * 0.38
    for k in range(5):                      # top string of pink flowers
        y = k * Hh * 0.045
        marigold(d, cx, y, S * 0.045, (230, 70, 140))
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(232, 66, 140, 255), width=int(S * 0.07))
    for k in range(16):
        a = 2 * math.pi * k / 16
        c = YELLOW if k % 2 else MARIGOLD
        d.line([(cx, cy), (cx + R * 0.92 * math.cos(a), cy + R * 0.92 * math.sin(a))], fill=c + (255,),
               width=int(S * 0.045))
    d.ellipse((cx - S * 0.07, cy - S * 0.07, cx + S * 0.07, cy + S * 0.07), fill=(232, 66, 140, 255))
    for j, xo in enumerate((-0.42, -0.21, 0.0, 0.21, 0.42)):
        x = cx + xo * S
        y = cy + R * (0.75 if abs(xo) > 0.3 else 0.95)
        L = 4 + (j % 2)
        for k in range(L):
            c = [(232, 66, 140), GREEN, MARIGOLD, YELLOW][(k + j) % 4]
            marigold(d, x, y + k * S * 0.075, S * 0.038, c)
        by = y + L * S * 0.075
        d.polygon([(x - S * 0.055, by + S * 0.08), (x + S * 0.055, by + S * 0.08), (x + S * 0.03, by),
                   (x - S * 0.03, by)], fill=(240, 200, 50, 255))
        d.ellipse((x - S * 0.015, by + S * 0.07, x + S * 0.015, by + S * 0.1), fill=(200, 150, 30, 255))
    return down(im, w, h)


def ill_dhol(w, h):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    x0, y0, x1, y1 = S * 0.12, Hh * 0.25, S * 0.72, Hh * 0.85
    # bead string behind
    pts = [(S * 0.05 + S * 0.9 * t, Hh * (0.22 + 0.55 * math.sin(math.pi * t) ** 0.7)) for t in np.linspace(0, 1, 40)]
    for k, (x, y) in enumerate(pts[:24]):
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=[PINK, YELLOW, (60, 170, 220), (240, 120, 60)][k % 4] + (255,))
    d.rounded_rectangle((x0, y0, x1, y1), radius=(y1 - y0) * 0.35, fill=(130, 64, 34, 255))
    for t in (0.1, 0.9):
        xx = x0 + (x1 - x0) * t
        d.rectangle((xx - 6, y0 + 8, xx + 6, y1 - 8), fill=(220, 140, 60, 255))
    d.rectangle((x0 + (x1 - x0) * 0.35, y0 + 6, x0 + (x1 - x0) * 0.65, y1 - 6), fill=(170, 50, 110, 255))
    for k in range(8):                      # rope lacing
        ya = y0 + (y1 - y0) * k / 8
        yb = y0 + (y1 - y0) * (k + 1) / 8
        d.line([(x0 + 20, ya), (x1 - 20, yb)], fill=(240, 210, 110, 255), width=5)
        d.line([(x0 + 20, yb), (x1 - 20, ya)], fill=(240, 210, 110, 255), width=5)
    d.ellipse((x0 + (x1 - x0) * 0.43, (y0 + y1) / 2 - 30, x0 + (x1 - x0) * 0.57, (y0 + y1) / 2 + 30),
              fill=(60, 170, 220, 255))
    d.ellipse((x1 - S * 0.07, y0 - 6, x1 + S * 0.1, y1 + 6), fill=(246, 230, 200, 255), outline=(150, 90, 50, 255),
              width=8)
    for (ax, ay, bx, by) in ((0.68, 0.6, 0.98, 0.98), (0.72, 0.38, 0.98, 0.05)):   # sticks
        d.line([(S * ax, Hh * ay), (S * bx, Hh * by)], fill=(120, 70, 40, 255), width=int(S * 0.018))
    return down(im, w, h)


def ill_bangles(w, h):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    cols = [(196, 40, 50), GOLD, (30, 110, 70), (196, 40, 50), GOLD, (30, 110, 70)]
    for k, c in enumerate(cols):
        x = S * (0.12 + 0.13 * k)
        bw = S * 0.2
        d.ellipse((x, Hh * 0.04, x + bw, Hh * 0.96), fill=c + (255,), outline=shade(c, 0.7) + (255,), width=6)
        d.ellipse((x + bw * 0.35, Hh * 0.12, x + bw * 0.75, Hh * 0.88), fill=shade(c, 0.6) + (255,))
        for j in range(5):                  # little floral dots
            y = Hh * (0.18 + 0.16 * j)
            d.ellipse((x + bw * 0.12, y - 8, x + bw * 0.12 + 16, y + 8), fill=(250, 240, 220, 255))
    return down(im, w, h)


def ill_matkas(w, h):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    cx = S * 0.5
    # rangoli base
    for k, (r, c) in enumerate(((0.5, (230, 70, 60)), (0.44, (40, 140, 200)), (0.38, (250, 200, 50)),
                                (0.32, (232, 66, 140)), (0.26, (250, 236, 200)))):
        d.ellipse((cx - S * r, Hh * 0.88 - S * r * 0.18, cx + S * r, Hh * 0.88 + S * r * 0.18), fill=c + (255,))
    for k in range(24):
        a = 2 * math.pi * k / 24
        d.ellipse((cx + S * 0.47 * math.cos(a) - 8, Hh * 0.88 + S * 0.085 * math.sin(a) - 8,
                   cx + S * 0.47 * math.cos(a) + 8, Hh * 0.88 + S * 0.085 * math.sin(a) + 8),
                  fill=(250, 220, 90, 255))
    for k, (yc, r) in enumerate(((0.73, 0.2), (0.47, 0.17), (0.23, 0.15))):     # three pots, largest at the bottom
        y = Hh * yc
        R = S * r
        d.ellipse((cx - R, y - R * 0.9, cx + R, y + R * 0.9), fill=(204, 140, 70, 255))
        d.ellipse((cx - R * 0.95, y - R * 0.85, cx + R * 0.3, y + R * 0.6), fill=(222, 162, 92, 255))
        d.rectangle((cx - R * 0.45, y - R * 1.05, cx + R * 0.45, y - R * 0.8), fill=(190, 124, 60, 255))
        d.ellipse((cx - R * 0.55, y - R * 1.15, cx + R * 0.55, y - R * 0.95), fill=(150, 90, 40, 255))
        for j in range(9):                  # marigold garland around the rim
            t = j / 8
            gx = cx - R * 0.95 + 1.9 * R * t
            gy = y - R * 0.55 + math.sin(math.pi * t) * R * 0.25
            marigold(d, gx, gy, S * 0.032, YELLOW if j % 2 else MARIGOLD)
            if j % 2 == 0:
                for q in range(3):
                    marigold(d, gx, gy + (q + 1) * S * 0.05, S * 0.024, MARIGOLD)
        for j in range(6):
            lx = cx - R * 0.8 + j * R * 0.32
            d.ellipse((lx - 10, y - R * 0.55 - 26, lx + 10, y - R * 0.55 - 6), fill=GREEN + (255,))
    return down(im, w, h)


def ill_kaleere(w, h):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    for k, cx in enumerate((S * 0.28, S * 0.72)):
        top = Hh * (0.02 if k == 0 else 0.06)
        d.line([(cx, top), (cx, top + Hh * 0.28)], fill=GOLD + (255,), width=6)
        dy = top + Hh * 0.28
        R = S * 0.2
        d.chord((cx - R, dy - R * 0.4, cx + R, dy + R * 1.0), 180, 360, fill=(230, 180, 70, 255))
        d.rectangle((cx - R, dy + R * 0.28, cx + R, dy + R * 0.38), fill=(200, 140, 40, 255))
        for j in range(9):
            x = cx - R + j * 2 * R / 8
            L = Hh * (0.18 + 0.07 * (j % 3))
            d.line([(x, dy + R * 0.35), (x, dy + R * 0.35 + L)], fill=(214, 164, 60, 255), width=4)
            for q in range(3):
                yy = dy + R * 0.35 + L * (q + 1) / 3
                d.ellipse((x - 8, yy - 8, x + 8, yy + 8), fill=[(30, 110, 70), GOLD, (196, 40, 50)][q] + (255,))
        d.ellipse((cx - R * 0.5, dy + R * 0.85, cx + R * 0.5, dy + R * 1.05), fill=(214, 164, 60, 255))
    return down(im, w, h)


def ill_small_dhol(w, h, flip=False):
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    x0, y0, x1, y1 = S * 0.12, Hh * 0.22, S * 0.88, Hh * 0.78
    d.rounded_rectangle((x0, y0, x1, y1), radius=(y1 - y0) * 0.4, fill=(70, 140, 60, 255))
    d.rectangle((x0 + (x1 - x0) * 0.3, y0 + 4, x0 + (x1 - x0) * 0.7, y1 - 4), fill=(226, 70, 70, 255))
    for k in range(6):
        ya, yb = y0 + (y1 - y0) * k / 6, y0 + (y1 - y0) * (k + 1) / 6
        d.line([(x0 + 10, ya), (x1 - 10, yb)], fill=(250, 220, 120, 255), width=4)
    d.ellipse((x1 - S * 0.15, y0 - 4, x1 + S * 0.08, y1 + 4), fill=(246, 232, 210, 255), outline=(40, 40, 40, 255),
              width=6)
    d.ellipse((x1 - S * 0.06, (y0 + y1) / 2 - 10, x1 - S * 0.02, (y0 + y1) / 2 + 10), fill=(40, 40, 40, 255))
    im = down(im, w, h).rotate(-28 if not flip else 28, resample=Image.BICUBIC, expand=False)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


ILLS = {"urli": ill_urli, "chhatri": ill_chhatri, "laddoo": ill_laddoo, "toran": ill_toran, "dhol": ill_dhol,
        "bangles": ill_bangles, "matkas": ill_matkas}


# ---------------- the papercut frame ----------------

def frame(w, h, tint):
    """Cream papercut frame: a scalloped outer shape with corner flourishes, a lace ring, a plain oval centre."""
    im = canvas(w, h)
    d = ImageDraw.Draw(im)
    S, Hh = im.width, im.height
    cx, cy = S / 2, Hh / 2
    # outer body: a rounded rectangle plus side points, scalloped edge
    m = S * 0.07
    body = Image.new("L", im.size, 0)
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle((m, m, S - m, Hh - m), radius=S * 0.07, fill=255)
    bd.polygon([(0, cy), (m * 1.4, cy - Hh * 0.12), (m * 1.4, cy + Hh * 0.12)], fill=255)
    bd.polygon([(S, cy), (S - m * 1.4, cy - Hh * 0.12), (S - m * 1.4, cy + Hh * 0.12)], fill=255)
    bd.polygon([(cx, m * 0.2), (cx - S * 0.1, m * 1.3), (cx + S * 0.1, m * 1.3)], fill=255)
    bd.polygon([(cx, Hh - m * 0.2), (cx - S * 0.1, Hh - m * 1.3), (cx + S * 0.1, Hh - m * 1.3)], fill=255)
    for k in range(48):                     # scallops all around
        t = k / 48
        per = 2 * (S + Hh)
        p = t * per
        if p < S:
            x, y = p, m
        elif p < S + Hh:
            x, y = S - m, p - S
        elif p < 2 * S + Hh:
            x, y = 2 * S + Hh - p, Hh - m
        else:
            x, y = m, per - p
        x = min(max(x, m), S - m)
        y = min(max(y, m), Hh - m)
        bd.ellipse((x - m * 0.45, y - m * 0.45, x + m * 0.45, y + m * 0.45), fill=255)
    cream = Image.new("RGBA", im.size, CREAM + (255,))
    im.paste(cream, (0, 0), body)
    # corner paisleys filled with a dot mesh, and corner flowers
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = cx + sx * S * 0.355, cy + sy * Hh * 0.31
            pw, ph = S * 0.065, Hh * 0.09
            d.ellipse((px - pw, py - ph, px + pw, py + ph), outline=tint + (255,), width=6)
            for i in range(-4, 5):
                for j in range(-4, 5):
                    qx, qy = px + i * pw / 4.5, py + j * ph / 4.5
                    if ((qx - px) / pw) ** 2 + ((qy - py) / ph) ** 2 < 0.8:
                        d.ellipse((qx - 7, qy - 7, qx + 7, qy + 7), fill=tint + (255,))
            fx, fy = cx + sx * S * 0.27, cy + sy * Hh * 0.36
            for k in range(8):
                a = 2 * math.pi * k / 8
                d.ellipse((fx + 26 * math.cos(a) - 14, fy + 26 * math.sin(a) - 14, fx + 26 * math.cos(a) + 14,
                           fy + 26 * math.sin(a) + 14), outline=tint + (255,), width=5)
            d.ellipse((fx - 12, fy - 12, fx + 12, fy + 12), outline=tint + (255,), width=5)
    # lace ring: zigzag band between two ovals
    ox, oy = S * 0.4, Hh * 0.36
    d.ellipse((cx - ox - 30, cy - oy - 30, cx + ox + 30, cy + oy + 30), fill=CREAM + (255,), outline=tint + (255,),
              width=5)
    n = 120
    pts = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        r = 1.0 if k % 2 else 1.055
        pts.append((cx + (ox + 14) * r * math.cos(a), cy + (oy + 14) * r * math.sin(a)))
    d.line(pts, fill=tint + (255,), width=5)
    d.ellipse((cx - ox, cy - oy, cx + ox, cy + oy), fill=CREAM + (255,), outline=tint + (255,), width=4)
    return down(im, w, h)


# ---------------- slides ----------------

def sticker(path, height):
    fig = Image.open(path).convert("RGBA")
    fig = fig.resize((round(fig.width * height / fig.height), int(height)), Image.LANCZOS)
    pad = 16
    big = Image.new("RGBA", (fig.width + 2 * pad, fig.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(fig, (pad, pad))
    a = big.getchannel("A").point(lambda v: 255 if v > 90 else 0)
    outline = a.filter(ImageFilter.MaxFilter(23)).filter(ImageFilter.GaussianBlur(1.5))
    white = Image.new("RGBA", big.size, (255, 255, 255, 0))
    white.putalpha(outline)
    white.alpha_composite(big)
    return white


def caps_block(im, words, x, y, align="l"):
    d = ImageDraw.Draw(im)
    f = font("lato", 900, 62)
    pitch = 74
    for k, wd in enumerate(words):
        spaced = wd
        d.text((x, y + k * pitch), spaced, font=f, fill=(255, 250, 244, 255), anchor="la", spacing=0,
               features=None)


def tracked(d, xy, text, f, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += d.textlength(ch, font=f) + track


def text_lines(im, words, x, ytop, right=None):
    """Bold white caps, one phrase per line, as large as the reference's (shrunk only if a line won't fit)."""
    d = ImageDraw.Draw(im)
    right = right or W * 0.95
    size = 72
    while size > 40:
        f = font("lato", 900, size)
        widest = max(sum(d.textlength(c, font=f) + 3 for c in wd) for wd in words)
        if x + widest <= right and int(size * 1.17) * len(words) <= H * 0.56:
            break
        size -= 2
    pitch = int(size * 1.17)
    for k, wd in enumerate(words):
        tracked(d, (x, ytop + size * 0.86 + k * pitch), wd, f, (255, 250, 244, 255), 3)


def brand(im, y, colour=BRAND):
    d = ImageDraw.Draw(im)
    f = font("cinzel", 600, 50)
    txt = "KALA KARI"
    tw = sum(d.textlength(c, font=f) + 9 for c in txt) - 9
    tracked(d, (W / 2 - tw / 2, y), txt, f, colour + (255,), 9)
    f2 = font("cinzel", 600, 18)
    t2 = "CREATIONS"
    tw2 = sum(d.textlength(c, font=f2) + 7 for c in t2) - 7
    tracked(d, (W / 2 - tw2 / 2, y + 32), t2, f2, colour + (255,), 7)


def framed_text(im, lines, sub, sub_font, deco, tint, deco_side):
    fw, fh = 960, 690
    fr = frame(fw, fh, tint)
    x0, y0 = (W - fw) // 2, int(H * 0.5 - fh / 2)
    im.alpha_composite(fr, (x0, y0))
    d = ImageDraw.Draw(im)
    f = font("bodoni-moda", 400, 78 if len(lines) == 3 else 70)
    pitch = 90 if len(lines) == 3 else 68
    ty = H * 0.5 - pitch * (len(lines)) / 2 - 22
    for k, ln in enumerate(lines):
        d.text((W / 2 - (56 if deco_side == "r" else 0), ty + k * pitch), ln, font=f, fill=RUST + (255,), anchor="mt")
    d.text((W / 2, ty + len(lines) * pitch + 26), sub, font=sub_font, fill=(80, 60, 52, 255) if deco_side != "r"
           else RUST + (255,), anchor="mt")
    return x0, y0, fw, fh


def slide_cover(photo):
    ph = Image.open(photo).convert("RGB")
    s = max(W / ph.width, H / ph.height)
    ph = ph.resize((round(ph.width * s), round(ph.height * s)), Image.LANCZOS)
    x = (ph.width - W) // 2
    ph = ph.crop((x, 0, x + W, H))
    # a soft warm wash like the reference's muted cover
    a = np.asarray(ph, float) * 0.86 + np.array([120, 70, 40]) * 0.14
    im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    x0, y0, fw, fh = framed_text(im, ["IF YOU’RE A", "2026", "BRIDESMAID"], "This is for you!",
                                 font("cormorant-garamond", 500, 42, "italic"), None, (214, 120, 120), "c")
    for flip, dx in ((False, x0 + 66), (True, x0 + fw - 66 - 128)):
        im.alpha_composite(ill_small_dhol(128, 110, flip), (dx, H // 2 - 80))
    brand(im, int(H * 0.89))
    return im


def slide_end():
    im = Image.new("RGBA", (W, H), ORANGE + (255,))
    lines = ["YOUR PRE-", "WEDDING", "WARDROBE ,", "SORTED"]
    x0, y0, fw, fh = framed_text(im, lines, "", font("lato", 900, 28), None, (200, 96, 60), "r")
    d = ImageDraw.Draw(im)
    f = font("lato", 900, 31)
    d.text((W / 2, y0 + fh * 0.745), "Save this for your next wedding", font=f, fill=RUST + (255,), anchor="mm")
    d.text((W / 2, y0 + fh * 0.745 + 34), "invite.", font=f, fill=RUST + (255,), anchor="mm")
    im.alpha_composite(ill_kaleere(130, 165), (x0 + fw - 262, int(H / 2) - 92))
    brand(im, int(H * 0.89))
    return im


def slide_product(src, cut, side, words, ill, box, ty):
    im = Image.new("RGBA", (W, H), ORANGE + (255,))
    st = sticker(os.path.join(src, "cutouts", cut + ".png"), H * 0.8)
    bleed = cut.startswith("8-")             # the deer co-ord photo has no feet: let it run off the bottom
    if bleed:
        st = sticker(os.path.join(src, "cutouts", cut + ".png"), H * 0.86)
    cx = W * (0.70 if side == "R" else 0.27)
    y = int(H * 0.115) if not bleed else H - st.height + 30
    im.alpha_composite(st, (int(cx - st.width / 2), y))
    bx0, by0, bx1, by1 = box
    art = ILLS[ill](int((bx1 - bx0) * W), int((by1 - by0) * H))
    im.alpha_composite(art, (int(bx0 * W), int(by0 * H)))
    tx = W * (0.11 if side == "R" else (0.53 if ill not in ("matkas",) else 0.49))
    if ill == "dhol":
        tx = W * 0.50
    model_x0 = cx - st.width / 2 + 10            # the sticker's left edge, so text on the left never touches it
    text_lines(im, words, tx, ty * H, right=model_x0 - 18 if side == "R" else None)
    return im


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    slide_cover(os.path.join(src, "0-cover-mustard-folk-art.jpg")).convert("RGB").save(
        os.path.join(out, "slide-1.jpg"), quality=94)
    for i, s in enumerate(SLIDES, 2):
        slide_product(src, *s).convert("RGB").save(os.path.join(out, f"slide-{i}.jpg"), quality=94)
        print("slide", i)
    slide_end().convert("RGB").save(os.path.join(out, "slide-9.jpg"), quality=94)


if __name__ == "__main__":
    main()
