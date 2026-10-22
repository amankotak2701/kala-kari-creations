#!/usr/bin/env python3
"""Seamless 4-slide Instagram carousel (4:5): "DIWALI DHAMAAAA…KKKAAAA SALE" stretches across slides 1-3
on one continuous background, slide 4 reveals the "Diwali Dhamaka Sale - Coming Soon" badge with the
Kala Kari logo and website. Own artwork: crimson-maroon backdrop, mandalas, kandil lanterns, fireworks,
gold lace border, 3D gold lettering.

Usage:
    python3 diwali_carousel.py <fonts_dir> <out_dir>
Writes slide-1.jpg … slide-4.jpg (1080x1350) and panorama-preview.jpg. diwali_video.py makes the video versions.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SW, SH, N = 1080, 1350, 4
PW = SW * N
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-gold-flat.png")
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
GOLD = (236, 190, 92)
GOLD_D = (176, 118, 34)
CREAM = (255, 240, 205)


def fonts(fonts_dir):
    cin = lambda w, s: ImageFont.truetype(os.path.join(fonts_dir, "fontsource-cinzel", "package", "files", f"cinzel-latin-{w}-normal.woff2"), s)  # noqa: E731
    cor = lambda w, s: ImageFont.truetype(os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-italic.woff2"), s)  # noqa: E731
    return cin, cor


# ------------------------------------------------------------------ background
def backdrop():
    y, x = np.mgrid[0:SH, 0:PW].astype(np.float32)
    # a soft glow behind each slide's centre plus a gentle curtain of vertical light
    glow = np.zeros_like(x)
    for cx in (SW * .55, SW * 1.6, SW * 2.5, SW * 3.5):
        glow = np.maximum(glow, np.exp(-(((x - cx) / 900) ** 2 + ((y - SH * .45) / 800) ** 2)))
    curtain = .04 * np.sin(x / 38) * np.exp(-((y - SH * .5) / 900) ** 2)
    v = np.clip(glow * .9 + curtain, 0, 1)[..., None]
    dark = np.array([84, 8, 30], np.float32)
    lit = np.array([170, 20, 58], np.float32)
    img = dark + (lit - dark) * v
    rng = np.random.default_rng(1)
    img += rng.standard_normal((SH, PW, 1)) * 1.6
    return Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert("RGBA")


def mandala(r, color=(255, 120, 150), alpha=34):
    s = 2
    R = r * s
    im = Image.new("RGBA", (2 * R + 4, 2 * R + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = R + 2
    col = color + (alpha,)
    w = max(2, int(r / 90)) * s
    for k, rr in enumerate((1.0, .93, .72, .64, .42, .34, .18)):
        d.ellipse((c - R * rr, c - R * rr, c + R * rr, c + R * rr), outline=col, width=w)
    for ring, (r0, r1, n) in enumerate(((.72, .93, 24), (.42, .64, 16), (.18, .34, 10))):
        for i in range(n):
            a = 2 * math.pi * i / n
            a2 = a + math.pi / n
            pts = [(c + R * r0 * math.cos(a - .5 * math.pi / n), c + R * r0 * math.sin(a - .5 * math.pi / n)),
                   (c + R * r1 * math.cos(a2 - math.pi / n), c + R * r1 * math.sin(a2 - math.pi / n)),
                   (c + R * r0 * math.cos(a + .5 * math.pi / n), c + R * r0 * math.sin(a + .5 * math.pi / n))]
            d.line(pts, fill=col, width=w)
            d.ellipse((c + R * (r1 - .03) * math.cos(a) - 3 * s, c + R * (r1 - .03) * math.sin(a) - 3 * s,
                       c + R * (r1 - .03) * math.cos(a) + 3 * s, c + R * (r1 - .03) * math.sin(a) + 3 * s), fill=col)
    for i in range(36):                                     # outer scallops
        a = 2 * math.pi * i / 36
        x, y = c + R * .965 * math.cos(a), c + R * .965 * math.sin(a)
        d.ellipse((x - R * .05, y - R * .05, x + R * .05, y + R * .05), outline=col, width=w)
    return im.resize((im.width // s, im.height // s), Image.LANCZOS)


def firework(r, seed, colors=((255, 210, 120), (255, 150, 190))):
    rng = np.random.default_rng(seed)
    s = 2
    im = Image.new("RGBA", (2 * r * s, 2 * r * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = r * s
    for i in range(46):
        a = 2 * math.pi * i / 46 + rng.uniform(-.03, .03)
        l0, l1 = r * s * rng.uniform(.18, .3), r * s * rng.uniform(.7, 1.0)
        col = colors[i % len(colors)]
        for k in range(14):                                  # dotted streak, brighter at the tip
            t = k / 13
            rr = l0 + (l1 - l0) * t
            x, y = c + rr * math.cos(a), c + rr * math.sin(a)
            dot = (1.2 + 1.8 * t) * s
            d.ellipse((x - dot, y - dot, x + dot, y + dot), fill=col + (int(60 + 150 * t),))
    im = im.resize((2 * r, 2 * r), Image.LANCZOS)
    glow = im.filter(ImageFilter.GaussianBlur(6))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(im)
    return out


def lantern(chain, scale=1.0):
    """Gold kandil lantern on a beaded chain; returns image with the chain's top at (w/2, 0)."""
    s = 3
    w, h = int(90 * scale), int((chain + 230) * scale)
    im = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = w * s / 2
    k = scale * s
    gold, dark, glowc = (232, 178, 78, 255), (150, 92, 24, 255), (255, 214, 120, 255)
    for yy in range(0, int(chain * k), int(14 * k)):            # beaded chain
        d.ellipse((cx - 4 * k, yy, cx + 4 * k, yy + 9 * k), fill=gold)
    y0 = chain * k
    d.polygon([(cx, y0), (cx + 22 * k, y0 + 30 * k), (cx - 22 * k, y0 + 30 * k)], fill=gold)          # dome
    d.rectangle((cx - 28 * k, y0 + 30 * k, cx + 28 * k, y0 + 40 * k), fill=dark)
    d.rounded_rectangle((cx - 30 * k, y0 + 40 * k, cx + 30 * k, y0 + 130 * k), radius=10 * k, fill=gold)  # body
    d.rounded_rectangle((cx - 20 * k, y0 + 50 * k, cx + 20 * k, y0 + 120 * k), radius=8 * k, fill=glowc)
    for xx in (-10, 0, 10):
        d.line((cx + xx * k, y0 + 50 * k, cx + xx * k, y0 + 120 * k), fill=dark, width=int(3 * k))
    d.rectangle((cx - 28 * k, y0 + 130 * k, cx + 28 * k, y0 + 140 * k), fill=dark)
    d.polygon([(cx - 24 * k, y0 + 140 * k), (cx + 24 * k, y0 + 140 * k), (cx, y0 + 175 * k)], fill=gold)
    for i in range(5):                                         # tassel
        d.line((cx + (i - 2) * 3 * k, y0 + 170 * k, cx + (i - 2) * 4 * k, y0 + 225 * k), fill=gold, width=int(3 * k))
    im = im.resize((w, h), Image.LANCZOS)
    g = Image.new("RGBA", im.size, (255, 200, 90, 0))
    g.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .5)))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(g)
    out.alpha_composite(im)
    return out


def lace_border(width):
    h = 70
    s = 2
    im = Image.new("RGBA", (width * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 44 * s, width * s, h * s), fill=(236, 176, 62, 255))
    d.rectangle((0, 44 * s, width * s, 48 * s), fill=(255, 226, 140, 255))
    step = 26
    for x in range(0, width + step, step):
        d.ellipse(((x - 13) * s, 30 * s, (x + 13) * s, 56 * s), fill=(250, 240, 220, 255))
        d.ellipse(((x - 3) * s, 16 * s, (x + 3) * s, 22 * s), fill=(250, 240, 220, 255))
        d.ellipse(((x - 4) * s, 40 * s, (x + 4) * s, 48 * s), fill=(214, 150, 60, 255))
    for x in range(step // 2, width + step, step):
        d.ellipse(((x - 2) * s, 26 * s, (x + 2) * s, 30 * s), fill=(250, 240, 220, 220))
    return im.resize((width, h), Image.LANCZOS)


# ------------------------------------------------------------------ 3D gold lettering
def gold_text(text, font, depth=12, outline=5):
    pad = depth + outline + 20
    bb = font.getbbox(text)
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((pad - bb[0], pad - bb[1]), text, font=font, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    edge = mask.filter(ImageFilter.MaxFilter(2 * outline + 1))
    # extrusion (dark maroon), stepped down-right
    for i in range(depth, 0, -1):
        lay = Image.new("RGBA", (w, h), (92, 14, 26, 255) if i > 2 else (130, 40, 30, 255))
        out.paste(lay, (int(i * .35), i), edge)
    # outer outline (warm cream-gold)
    out.paste(Image.new("RGBA", (w, h), (255, 232, 170, 255)), (0, 0), edge)
    inner = mask.filter(ImageFilter.MaxFilter(3))
    out.paste(Image.new("RGBA", (w, h), (150, 70, 20, 255)), (0, 0), inner)
    # gold gradient face
    top, mid, bot = np.array([255, 246, 190]), np.array([246, 196, 80]), np.array([206, 128, 30])
    face = np.zeros((h, w, 3), np.float32)
    tt = np.clip((np.arange(h) - pad) / max(1, h - 2 * pad), 0, 1)[:, None, None]
    face[:] = np.where(tt < .5, top + (mid - top) * (tt / .5), mid + (bot - mid) * ((tt - .5) / .5))
    face_im = Image.fromarray(face.clip(0, 255).astype(np.uint8)).convert("RGBA")
    out.paste(face_im, (0, 0), mask)
    # thin highlight along the top of the strokes
    hl = Image.fromarray(np.clip(np.asarray(mask, np.int16) - np.asarray(mask.transform(mask.size, Image.AFFINE, (1, 0, 0, 0, 1, 3)), np.int16), 0, 255).astype(np.uint8))
    out.paste(Image.new("RGBA", (w, h), (255, 255, 235, 255)), (0, 0), hl.point(lambda v: int(v * .7)))
    sh = Image.new("RGBA", (w, h), (30, 0, 8, 0))
    sh.putalpha(edge.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .55)))
    final = Image.new("RGBA", (w + 20, h + 24), (0, 0, 0, 0))
    final.alpha_composite(sh, (10, 18))
    final.alpha_composite(out, (0, 0))
    return final, pad


def place(img, im, cx, cy, angle=0.0):
    if angle:
        im = im.rotate(-angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


# ------------------------------------------------------------------ slide 4 badge
def diya(w):
    s = 3
    im = Image.new("RGBA", (w * s, w * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W2 = w * s
    d.chord((W2 * .1, W2 * .35, W2 * .9, W2 * .95), 0, 180, fill=(196, 92, 40, 255))
    d.chord((W2 * .1, W2 * .55, W2 * .9, W2 * .75), 0, 180, fill=(236, 170, 70, 255))
    for i in range(5):
        x = W2 * (.22 + i * .14)
        d.ellipse((x - W2 * .025, W2 * .7, x + W2 * .025, W2 * .75), fill=(255, 220, 140, 255))
    d.polygon([(W2 * .5, W2 * .1), (W2 * .6, W2 * .42), (W2 * .5, W2 * .55), (W2 * .4, W2 * .42)], fill=(255, 196, 60, 255))
    d.polygon([(W2 * .5, W2 * .25), (W2 * .55, W2 * .44), (W2 * .5, W2 * .52), (W2 * .45, W2 * .44)], fill=(255, 250, 210, 255))
    im = im.resize((w, w), Image.LANCZOS)
    g = Image.new("RGBA", im.size, (255, 190, 80, 0))
    g.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * .6)))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(g)
    out.alpha_composite(im)
    return out


def badge(cin, cor):
    """Returns (frame, parts): the empty gold frame and its pieces [(name, image, centre)] in badge coordinates."""
    s = 2
    w, h = 760, 560
    im = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def shape(inset):
        i = inset * s
        W2, H2 = w * s, h * s
        return [(W2 / 2, i), (W2 * .62, H2 * .1 + i * .6), (W2 * .82, H2 * .1 + i * .6), (W2 * .9 - i * .2, H2 * .2 + i * .4),
                (W2 - i, H2 * .32), (W2 - i, H2 * .68), (W2 * .9 - i * .2, H2 * .8 - i * .4), (W2 * .82, H2 * .9 - i * .6),
                (W2 * .62, H2 * .9 - i * .6), (W2 / 2, H2 - i), (W2 * .38, H2 * .9 - i * .6), (W2 * .18, H2 * .9 - i * .6),
                (W2 * .1 + i * .2, H2 * .8 - i * .4), (i, H2 * .68), (i, H2 * .32), (W2 * .1 + i * .2, H2 * .2 + i * .4),
                (W2 * .18, H2 * .1 + i * .6), (W2 * .38, H2 * .1 + i * .6)]
    d.polygon(shape(0), fill=(236, 180, 80, 255))
    d.polygon(shape(10), fill=(120, 22, 40, 255))
    d.polygon(shape(22), fill=(236, 180, 80, 255))
    d.polygon(shape(28), fill=(96, 10, 32, 255))
    # inner glow
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((w * s * .2, h * s * .2, w * s * .8, h * s * .8), fill=(200, 40, 80, 140))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).polygon(shape(28), fill=255)
    gl2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
    gl2.paste(glow, (0, 0), m)
    im.alpha_composite(gl2)
    d = ImageDraw.Draw(im)
    # marquee bulbs along the gold band
    pts = shape(16) + [shape(16)[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / (26 * s)))
        for k in range(n):
            t = k / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            d.ellipse((x - 4 * s, y - 4 * s, x + 4 * s, y + 4 * s), fill=(255, 250, 220, 255))
    im = im.resize((w, h), Image.LANCZOS)
    parts = [("diwali", gold_text("Diwali", cor(700, 132), depth=7, outline=4)[0], (w / 2, 170)),
             ("dhamaka", gold_text("DHAMAKA", cin(900, 96), depth=8, outline=4)[0], (w / 2, 290)),
             ("sale", gold_text("SALE", cin(900, 84), depth=7, outline=4)[0], (w / 2, 395)),
             ("diya", diya(84), (w / 2, h - 62))]
    return im, parts


BADGE_C = (SW * 3.5, 520)        # badge centre on the panorama
SOON_C = (SW * 3.5, 880)


def coming_soon():
    f = ImageFont.truetype(INTER.format("SemiBold"), 44)
    txt = "C O M I N G   S O O N"
    w = int(f.getlength(txt)) + 20
    im = Image.new("RGBA", (w, 70), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((w / 2, 35), txt, font=f, fill=GOLD, anchor="mm")
    return im


# ------------------------------------------------------------------ build
def scene(fonts_dir):
    """Panorama without the slide-4 badge and COMING SOON (so they can be animated), plus those pieces."""
    cin, cor = fonts(fonts_dir)
    img = backdrop()
    for cx, cy, r, a in ((SW * 1.5, 640, 330, 30), (SW * 2.75, 1180, 260, 26), (SW * 2.55, 40, 200, 24),
                         (SW * 0.05, 1240, 300, 22), (SW * 3.95, 1210, 280, 22)):
        mm = mandala(r, alpha=a)
        img.alpha_composite(mm, (int(cx - mm.width / 2), int(cy - mm.height / 2)))
    for cx, cy, r, seed in ((SW * .78, 150, 120, 1), (SW * 1.22, 120, 95, 2), (SW * 1.85, 210, 110, 3),
                            (SW * 2.3, 160, 120, 4), (SW * 3.5, 120, 105, 5), (SW * 3.22, 300, 80, 6),
                            (SW * .3, 330, 60, 7), (SW * 3.82, 380, 70, 8)):
        fw = firework(r, seed)
        img.alpha_composite(fw, (int(cx - r), int(cy - r)))
    for x, chain, sc in ((95, 230, 1.0), (SW - 140, 150, .9), (SW + 260, 120, .95), (SW * 2 + 820, 190, 1.0),
                         (SW * 3 + 95, 220, 1.0), (SW * 4 - 110, 140, .9)):
        ln = lantern(chain, sc)
        img.alpha_composite(ln, (int(x - ln.width / 2), 0))

    # DIWALI + the long wavy DHAMAAAA…KAAAA, ending in a big SALE on slide 3
    t, _ = gold_text("DIWALI", cin(900, 150), depth=14, outline=6)
    place(img, t, 430, 520, -3)
    word = "DHAM" + "A" * 17 + "K" * 8 + "A" * 5
    f = cin(900, 118)
    x0, x1 = 210, SW * 2 + 540
    widths = [f.getlength(c) * .9 for c in word]
    scale = (x1 - x0) / sum(widths)
    xs, x = [], x0
    for wdt in widths:
        xs.append(x + wdt * scale / 2)
        x += wdt * scale

    def path_y(xx):
        u = (xx - x0) / (x1 - x0)
        return 690 + 55 * u + 70 * math.sin(u * 2 * math.pi * 1.1 - .2)

    cache = {}
    for c, xx in zip(word, xs):
        if c not in cache:
            cache[c] = gold_text(c, f, depth=12, outline=5)[0]
        dydx = (path_y(xx + 5) - path_y(xx - 5)) / 10
        place(img, cache[c], xx, path_y(xx), math.degrees(math.atan(dydx)))
    s_img, _ = gold_text("SALE", cin(900, 190), depth=16, outline=7)
    place(img, s_img, x1 + 210, path_y(x1) - 10, 6)

    # slide 4: logo + website (the badge and COMING SOON are added by the caller)
    d = ImageDraw.Draw(img)
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((430, int(430 * logo.height / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, (int(SW * 3.5 - logo.width / 2), 990))
    d.rounded_rectangle((SW * 3.5 - 280, 1140, SW * 3.5 + 280, 1220), radius=40, fill=(236, 180, 80))
    d.text((SW * 3.5, 1180), "kalakaricreations.com", font=ImageFont.truetype(INTER.format("Bold"), 40), fill=(96, 10, 32), anchor="mm")
    # swipe hint on slide 1
    d.text((SW - 70, 1215), "SWIPE  →", font=ImageFont.truetype(INTER.format("SemiBold"), 32), fill=(255, 226, 160), anchor="rm")

    lb = lace_border(PW)
    img.alpha_composite(lb, (0, SH - lb.height))
    return img, badge(cin, cor), coming_soon()


def full_badge(frame, parts):
    b = frame.copy()
    for _, im, c in parts:
        place(b, im, *c)
    return b


def build(fonts_dir, out_dir):
    img, (frame, parts), soon = scene(fonts_dir)
    place(img, full_badge(frame, parts), *BADGE_C)
    place(img, soon, *SOON_C)
    os.makedirs(out_dir, exist_ok=True)
    rgb = img.convert("RGB")
    rgb.resize((PW // 2, SH // 2), Image.LANCZOS).save(os.path.join(out_dir, "panorama-preview.jpg"), quality=88)
    for i in range(N):
        rgb.crop((i * SW, 0, (i + 1) * SW, SH)).save(os.path.join(out_dir, f"slide-{i + 1}.jpg"), quality=95)
    print("ok")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
