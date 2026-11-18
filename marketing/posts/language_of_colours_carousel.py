#!/usr/bin/env python3
"""6-slide 4:5 carousel, "The language of Colours", in the layout of the reference post.

Slide 1: a painted-flower background with the white title "The language of Colours" (serif "The"/"of", large
script "language"/"Colours").
Slides 2-6: one colour each, as a 2 x 2 grid with no gaps:
    product photo  | mood picture (sky, leaves, mist, golden trees, blossom)
    text tile      | second product photo
The text tile has the colour's name in script and a short line in serif, tinted to that colour.

The mood pictures and the cover flowers are painted here in code. A real mood photo saved as
<photo-dir>/mood-<colour>.jpg (e.g. mood-warm-neutrals.jpg) is used instead of the painted one.

Usage:
    python3 language_of_colours_carousel.py <photo-dir> <out-dir>
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
TW, TH = W // 2, H // 2
FONTS = os.environ.get("KK_FONTS", "/tmp/claude-0/-home-user-kala-kari-creations/"
                       "b594b16c-4df2-59b6-99e4-9ab0ec789fa6/scratchpad/fonts")

# (name, poem lines, text-tile background, script colour, poem colour, photo a, photo b, mood painter, a-focus, b-focus)
COLOURS = [
    ("Blue", ["Calm as a clear sky,", "deep as hand-dyed indigo."], (255, 255, 255), (132, 148, 214), (150, 160, 205),
     "blue-a-royal-blue-leheriya-suit", "blue-b-indigo-floral-coord", "sky", 0.25, 0.3),
    ("Green", ["Fresh as new leaves,", "rooted in tradition."], (255, 255, 255), (118, 190, 168), (128, 182, 166),
     "green-a-parrot-green-jaipuri-suit", "green-b-olive-cotton-tunic", "leaves", 0.25, 0.3),
    ("Ivory", ["Soft, quiet and timeless,", "like a misty morning."], (171, 173, 177), (250, 250, 250),
     (245, 245, 246), "ivory-a-offwhite-black-tunic", "ivory-b-white-jaipuri-suit", "mist", 0.2, 0.25),
    ("Warm Neutrals", ["Earthy tones that feel", "like golden afternoons", "and coming home."], (255, 255, 255),
     (190, 172, 118), (180, 166, 128), "warm-a-coffee-pintuck-tunic", "warm-b-offwhite-brown-tunic", "golden",
     0.25, 0.05),
    ("Pink", ["Gentle, joyful and", "a little bit dreamy."], (255, 255, 255), (238, 168, 192), (236, 176, 196),
     "pink-a-baby-pink-jaipuri-suit", "pink-b-pink-jaipuri-handblock-suit", "blossom", 0.25, 0.28),
]


def font(fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(FONTS, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def fbm(h, w, seed, octaves=6, base=4):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = base * 2 ** o
        g = rng.random((max(2, int(n * h / w)), n)).astype(np.float32)
        out += amp * np.asarray(Image.fromarray(g).resize((w, h), Image.BICUBIC))
        tot += amp
        amp *= 0.5
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


def smooth(a, lo, hi):
    t = np.clip((a - lo) / (hi - lo), 0, 1)
    return t * t * (3 - 2 * t)


def vgrad(h, w, top, bot):
    t = np.linspace(0, 1, h)[:, None, None]
    return np.array(top, float) * (1 - t) + np.array(bot, float) * t * np.ones((1, w, 1))


def to_img(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


# ---------- mood pictures ----------

def mood_sky():
    img = vgrad(TH, TW, (104, 158, 226), (176, 212, 242))
    c = fbm(TH, TW, 11, 7, 3)
    c2 = fbm(TH, TW, 12, 5, 6)
    v = c * 0.8 + c2 * 0.35 + 0.18 * np.linspace(-0.4, 0.6, TW)[None, :]
    a = smooth(v, 0.46, 0.74)[..., None]
    up = np.roll(v, 18, axis=0)                       # brighter tops, grey-blue bases
    shade = (0.80 + 0.20 * smooth(v - up, -0.05, 0.08))[..., None]
    cloud = np.array([250, 251, 255]) * shade + np.array([-20, -10, 0]) * (1 - shade)
    img = img * (1 - a) + cloud * a
    return to_img(img).filter(ImageFilter.GaussianBlur(1.1))


def leaf_cluster(d, cx, cy, r, col, tip, rng):
    n = rng.integers(22, 30)
    for k in range(n):
        ang = 2 * math.pi * k / n + rng.normal(0, 0.12)
        L = r * rng.uniform(0.7, 1.05)
        wdt = r * 0.07
        pts = [(cx, cy)]
        for s in (1, -1):
            pass
        px, py = cx + L * math.cos(ang), cy + L * math.sin(ang)
        nx, ny = -math.sin(ang) * wdt, math.cos(ang) * wdt
        mx, my = cx + 0.45 * L * math.cos(ang), cy + 0.45 * L * math.sin(ang)
        d.polygon([(cx, cy), (mx + nx, my + ny), (px, py), (mx - nx, my - ny)], fill=col)
        d.line([(cx, cy), (px, py)], fill=tip, width=max(1, int(r * 0.02)))


def mood_leaves():
    rng = np.random.default_rng(5)
    base = to_img(vgrad(TH, TW, (52, 104, 98), (36, 82, 78)) * (0.85 + 0.3 * fbm(TH, TW, 3, 5, 3))[..., None])
    for layer, (blur, rr, cnt, col, tip) in enumerate([(14, 120, 14, (84, 140, 132), (110, 165, 156)),
                                                       (6, 100, 10, (112, 176, 164), (150, 204, 192)),
                                                       (1.4, 92, 6, (136, 202, 188), (182, 228, 216))]):
        lay = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for _ in range(cnt):
            cx, cy = rng.uniform(-40, TW + 40), rng.uniform(-40, TH + 40)
            leaf_cluster(d, cx, cy, rr * rng.uniform(0.8, 1.2), col + (255,), tip + (255,), rng)
        base = base.convert("RGBA")
        base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))
    return base.convert("RGB")


def treeline(h, w, y0, amp, seed):
    """A jagged conifer skyline as a mask (1 = trees)."""
    rng = np.random.default_rng(seed)
    top = np.full(w, y0, float)
    x = 0
    while x < w:
        tw = rng.uniform(8, 22)
        th = rng.uniform(0.3, 1.0) * amp
        xs = np.arange(int(x), min(w, int(x + tw)))
        top[xs] = np.minimum(top[xs], y0 - th * (1 - np.abs((xs - x - tw / 2) / (tw / 2))))
        x += tw * rng.uniform(0.4, 0.8)
    yy = np.arange(h)[:, None]
    return (yy >= top[None, :]).astype(np.float32)


def mood_mist():
    img = vgrad(TH, TW, (236, 237, 238), (214, 216, 218))
    horizon = int(TH * 0.52)
    m = treeline(TH, TW, horizon, 150, 4)
    ramp = 0.35 + 0.65 * np.clip((np.arange(TW) - TW * 0.2) / (TW * 0.8), 0, 1)[None, :] ** 1.2
    m[horizon:] = 0
    m *= ramp
    trees = to_img(np.stack([m * 255] * 3, -1)).convert("L").filter(ImageFilter.GaussianBlur(3))
    t = np.asarray(trees, float)[..., None] / 255 * 0.7
    img = img * (1 - t) + np.array([120, 126, 128]) * t
    # reflection
    refl = np.flipud(img[horizon - (TH - horizon):horizon])
    refl = np.asarray(to_img(refl).filter(ImageFilter.GaussianBlur(5)), float)
    img[horizon:] = refl * 0.85 + np.array([222, 224, 226]) * 0.15
    mist = fbm(TH, TW, 9, 5, 3)[..., None]
    img = img * 0.82 + 255 * (0.18 + 0.06 * mist)
    im = to_img(img)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(2)
    sh = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    for _ in range(120):                      # thin reeds
        x = rng.uniform(TW * 0.25, TW) ** 1.0
        y = TH - rng.uniform(0, 90)
        d.line([(x, y), (x + rng.normal(0, 5), y - rng.uniform(20, 80))], fill=(58, 60, 58, 200), width=1)
    im = im.convert("RGBA")
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1.2)))
    return im.convert("RGB").filter(ImageFilter.GaussianBlur(0.6))


def mood_golden():
    """Warm sand dunes in hazy golden-hour light."""
    x = np.linspace(0, 1, TW)[None, :]
    y = np.linspace(0, 1, TH)[:, None]
    img = vgrad(TH, TW, (238, 226, 196), (222, 200, 160))
    sun = np.exp(-(((x - 0.7) / 0.25) ** 2 + ((y - 0.18) / 0.18) ** 2))[..., None]
    img = img * (1 - 0.5 * sun) + np.array([255, 244, 214]) * 0.5 * sun
    rng = np.random.default_rng(3)
    xs = np.linspace(0, 1, TW)
    for k, (yb, amp, col) in enumerate([(0.42, 0.05, (214, 186, 140)), (0.55, 0.07, (204, 170, 120)),
                                        (0.70, 0.09, (192, 154, 104)), (0.86, 0.10, (178, 138, 92))]):
        ph = rng.uniform(0, 6.3)
        crest = yb - amp * (0.6 * np.sin(2 * np.pi * (xs * rng.uniform(0.8, 1.4)) + ph) +
                            0.4 * np.sin(2 * np.pi * (xs * rng.uniform(1.8, 2.6)) + 2 * ph))
        below = (y >= crest[None, :]).astype(float)
        depth = np.clip((y - crest[None, :]) / 0.12, 0, 1)
        lit = 0.5 + 0.5 * np.cos(2 * np.pi * (xs * 1.1) + ph)[None, :]   # sun side vs shadow side of each dune
        shade = 0.82 + 0.22 * lit - 0.1 * depth
        layer = np.array(col, float) * shade[..., None]
        haze = 0.35 * (1 - k / 4)
        layer = layer * (1 - haze) + np.array([240, 226, 196]) * haze
        img = img * (1 - below[..., None]) + layer * below[..., None]
    img += (fbm(TH, TW, 5, 4, 60)[..., None] - 0.5) * 8          # sand grain
    return to_img(img).filter(ImageFilter.GaussianBlur(1.6))


def mood_blossom():
    rng = np.random.default_rng(8)
    base = to_img(vgrad(TH, TW, (226, 232, 240), (238, 226, 232))).convert("RGBA")
    br = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    d = ImageDraw.Draw(br)
    for y0 in (90, 260, 470):                  # branches
        pts = [(-20, y0 + rng.normal(0, 30))]
        for k in range(1, 7):
            pts.append((k * TW / 6 + rng.normal(0, 15), pts[-1][1] + rng.normal(0, 28)))
        d.line(pts, fill=(78, 58, 52, 255), width=int(rng.uniform(6, 11)), joint="curve")
    base.alpha_composite(br.filter(ImageFilter.GaussianBlur(1.2)))
    for blur, cnt, rr in ((16, 40, 40), (5, 60, 26), (0.9, 38, 24)):
        lay = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for _ in range(cnt):
            cx, cy = rng.uniform(0, TW), rng.uniform(0, TH)
            r = rr * rng.uniform(0.7, 1.3)
            tint = rng.uniform(0, 1)
            col = (int(246 - 10 * tint), int(196 + 30 * (1 - tint)), int(210 + 25 * (1 - tint)), 255)
            for k in range(5):
                a = 2 * math.pi * k / 5 + rng.uniform(0, 1)
                px, py = cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)
                d.ellipse((px - r * 0.55, py - r * 0.55, px + r * 0.55, py + r * 0.55), fill=col)
                d.ellipse((px - r * 0.3, py - r * 0.3, px + r * 0.3, py + r * 0.3),
                          fill=(min(255, col[0] + 6), min(255, col[1] + 22), min(255, col[2] + 18), 255))
            d.ellipse((cx - r * 0.14, cy - r * 0.14, cx + r * 0.14, cy + r * 0.14), fill=(222, 140, 166, 255))
        base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))
    return base.convert("RGB")


MOODS = {"sky": mood_sky, "leaves": mood_leaves, "mist": mood_mist, "golden": mood_golden, "blossom": mood_blossom}


# ---------- tiles ----------

def photo_tile(path, fy, zoom=1.16):
    """4:5 crop; the slight zoom keeps the generator's corner mark out of frame."""
    im = Image.open(path).convert("RGB")
    s = max(TW / im.width, TH / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - TW) // 2
    y = int((im.height - TH) * fy)
    return im.crop((x, y, x + TW, y + TH))


def text_tile(name, lines, bg, c_script, c_body):
    t = Image.new("RGB", (TW, TH), bg)
    d = ImageDraw.Draw(t)
    words = name.split()
    fs = font("great-vibes", 400, 118 if len(words) == 1 else 104)
    fb = font("cormorant-garamond", 500, 33)
    pitch = 46
    block = len(words) * 100 + 30 + pitch * len(lines)
    y = TH / 2 - block / 2 + 50
    for wd in words:
        d.text((TW / 2, y), wd, font=fs, fill=c_script, anchor="mm")
        y += 100
    y += 10
    for ln in lines:
        d.text((TW / 2, y), ln, font=fb, fill=c_body, anchor="mm")
        y += pitch
    return t


# ---------- cover ----------

def petal(d, cx, cy, ang, L, w, fill, line):
    pts = []
    for k in range(25):
        t = k / 24
        r = L * t
        wd = w * math.sin(math.pi * t) ** 0.8 * (1 + 0.15 * math.sin(7 * t))
        pts.append((r, wd))
    poly = [(cx + r * math.cos(ang) - s * math.sin(ang), cy + r * math.sin(ang) + s * math.cos(ang))
            for r, s in pts] + [(cx + r * math.cos(ang) + s * math.sin(ang), cy + r * math.sin(ang) - s * math.cos(ang))
                                for r, s in reversed(pts)]
    d.polygon(poly, fill=fill)
    d.line(poly + [poly[0]], fill=line, width=3)
    for k in (-0.25, 0, 0.25):                # vein strokes
        a2 = ang + k * 0.6
        d.line([(cx, cy), (cx + 0.8 * L * math.cos(a2), cy + 0.8 * L * math.sin(a2))], fill=line, width=2)


def flower(lay, cx, cy, R, rng, base, line, centre=True):
    d = ImageDraw.Draw(lay)
    n = rng.integers(6, 9)
    for k in range(n):
        a = 2 * math.pi * k / n + rng.normal(0, 0.15)
        tint = rng.uniform(-14, 14)
        fill = tuple(int(min(255, max(0, c + tint))) for c in base) + (205,)
        petal(d, cx, cy, a, R * rng.uniform(0.85, 1.1), R * 0.42, fill, line + (230,))
    if centre:
        d.ellipse((cx - R * 0.2, cy - R * 0.2, cx + R * 0.2, cy + R * 0.2), fill=(244, 188, 56, 255))
        for _ in range(26):
            a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0.15, 0.33) * R
            x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(236, 170, 40, 255))


def leaf(d, x, y, ang, L, w, col):
    petal(d, x, y, ang, L, w, col + (235,), tuple(int(c * 0.8) for c in col) + (200,))


def bud(d, x, y, ang, s):
    c = (128, 156, 210)
    d.ellipse((x - s, y - s * 0.8, x + s, y + s * 0.8), fill=c + (240,))
    d.polygon([(x - s, y), (x - s * 0.4, y - s * 1.2), (x, y - s * 0.3), (x + s * 0.4, y - s * 1.2), (x + s, y)],
              fill=(150, 176, 222, 240))
    d.ellipse((x - s * 0.18, y - s * 0.1, x + s * 0.18, y + s * 0.3), fill=(40, 52, 80, 255))
    d.line([(x - s * 0.5, y + s * 0.2), (x - s * 0.2, y + s * 0.6)], fill=(70, 90, 140, 255), width=3)


def cover():
    rng = np.random.default_rng(14)
    paper = vgrad(H, W, (222, 218, 210), (214, 210, 202)) + (fbm(H, W, 30, 6, 6)[..., None] - 0.5) * 14
    paper += rng.normal(0, 3, (H, W, 1))
    im = to_img(paper).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # stems and leaves
    olive = (176, 176, 140)
    for x0, y0, x1, y1 in ((560, 1350, 640, 300), (90, 1350, 260, 760), (980, 1350, 900, 900), (300, 0, 180, 420),
                           (760, 0, 820, 380), (40, 300, 300, 650)):
        d.line([(x0, y0), ((x0 + x1) / 2 + 40, (y0 + y1) / 2), (x1, y1)], fill=(150, 152, 112, 255), width=7,
               joint="curve")
    for _ in range(26):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        leaf(d, x, y, rng.uniform(0, 2 * math.pi), rng.uniform(120, 240), rng.uniform(26, 40),
             tuple(int(c + rng.uniform(-12, 12)) for c in olive))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.6)))
    # flowers: peach/coral blooms, as in the reference
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for cx, cy, R, base in ((700, 160, 210, (244, 178, 160)), (-20, 820, 230, (238, 128, 84)),
                            (980, 800, 220, (246, 190, 172)), (940, 1180, 210, (232, 92, 70)),
                            (600, 1000, 180, (240, 150, 110)), (60, 1240, 190, (246, 196, 180)),
                            (330, 520, 120, (246, 196, 182))):
        flower(lay, cx, cy, R, rng, base, tuple(int(c * 0.8) for c in base), centre=R < 200 or base[1] > 150)
    tex = fbm(H, W, 31, 6, 10)
    a = np.asarray(lay.getchannel("A"), float) * (0.62 + 0.38 * tex)
    lay.putalpha(to_img(a))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.2)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for (x, y) in ((70, 120), (150, 230), (60, 330), (220, 330), (110, 470), (210, 60), (330, 140),
                   (460, 1170), (540, 1260), (620, 1180), (380, 1290), (700, 1300), (520, 1110), (840, 30)):
        bud(d, x, y, 0, rng.uniform(26, 36))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.5)))
    # a soft wash so the white title reads, like the reference's muted look
    wash = Image.new("RGBA", (W, H), (205, 200, 194, 0))
    yy = np.linspace(-1, 1, H)[:, None]
    xx = np.linspace(-1, 1, W)[None, :]
    a = np.clip(1 - (xx ** 2 / 0.9 + (yy - 0.05) ** 2 / 0.35), 0, 1) * 70
    wash.putalpha(to_img(a))
    im.alpha_composite(wash)
    # title
    t = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    serif = font("cormorant-garamond", 500, 74)
    script = font("great-vibes", 400, 230)
    for txt, f, y in (("The", serif, 445), ("language", script, 560), ("of", serif, 690), ("Colours", script, 820)):
        d.text((W / 2, y), txt, font=f, fill=(255, 255, 255, 255), anchor="mm")
    sh = t.getchannel("A").filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.25))
    shadow = Image.new("RGBA", (W, H), (90, 70, 60, 0))
    shadow.putalpha(sh)
    im.alpha_composite(shadow, (2, 4))
    im.alpha_composite(t)
    return im.convert("RGB")


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    cover().save(os.path.join(out, "slide-1.jpg"), quality=94)
    for i, (name, lines, bg, cs, cb, a, b, mood, fa, fb_) in enumerate(COLOURS, 2):
        s = Image.new("RGB", (W, H))
        s.paste(photo_tile(os.path.join(src, a + ".jpg"), fa), (0, 0))
        real = os.path.join(src, f"mood-{name.lower().replace(' ', '-')}.jpg")
        s.paste(photo_tile(real, 0.5, 1.0) if os.path.exists(real) else MOODS[mood](), (TW, 0))
        s.paste(text_tile(name, lines, bg, cs, cb), (0, TH))
        s.paste(photo_tile(os.path.join(src, b + ".jpg"), fb_), (TW, TH))
        s.save(os.path.join(out, f"slide-{i}.jpg"), quality=94)
        print("slide", i, name)


if __name__ == "__main__":
    main()
