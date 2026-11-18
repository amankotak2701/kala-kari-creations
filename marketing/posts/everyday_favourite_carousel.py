#!/usr/bin/env python3
"""4-slide 4:5 "Find Your EVERYDAY FAVOURITE" carousel, in the layout of the reference post.

Every slide is the same studio set: a warm blush-greige wall, soft window light falling on the left, and an
out-of-focus leafy sprig at the bottom left. One model stands in front of it, cut out of the product photo with
rembg, with a soft shadow on the wall.
1. The model in the centre, cropped at the hips. At the top: "Find Your" in grey italic sans and
   "EVERYDAY FAVOURITE" in bold maroon caps.
2-4. The model left of centre and a serif italic line on the right, in near-black with the last words in maroon.
   Slide 4 also has a beige pill at the bottom with the website.

Usage:
    python3 everyday_favourite_carousel.py <cutouts-dir> <out-dir> [2|3]    (2, 3 = the second and third product sets;
    set 3 takes product-photos/ as <cutouts-dir>)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
FONTS = os.environ.get("KK_FONTS", "/tmp/claude-0/-home-user-kala-kari-creations/"
                       "b594b16c-4df2-59b6-99e4-9ab0ec789fa6/scratchpad/fonts")
INK = (42, 36, 36)
MAROON = (150, 32, 38)
GREY = (88, 84, 84)

# (cutout, figure height as a fraction of H, head-top y, centre x, text lines [(text, maroon?)], text centre x/y)
SLIDES = [
    ("1-pink-jaipuri-short-top", 1.36, 0.235, 0.50, None, None),
    ("2-maroon-mirror-work-tunic", 0.86, 0.13, 0.35,
     [("Short tunics", False), ("that move you", False), ("with ease.", True)], (0.775, 0.37)),
    ("3-offwhite-black-lotus-tunic", 1.12, 0.16, 0.29,
     [("Handcrafted", False), ("for the", False), ("modern minds.", True)], (0.785, 0.36)),
    ("4-coffee-pintuck-tunic", 1.18, 0.15, 0.40,
     [("Rooted in", False), ("Indian", True), ("heritage.", True)], (0.80, 0.33)),
]

# second set: the tunics and tops not in the first set or in "The language of Colours"
SLIDES_2 = [
    ("1-denim-balloon-sleeve-top", 1.36, 0.235, 0.50, None, None),
    ("2-rich-red-chanderi-shirt", 0.86, 0.13, 0.29,
     [("Tops and shirts", False), ("that move you", False), ("with ease.", True)], (0.785, 0.40)),
    ("3-kutchi-patchwork-long-shrug", 0.88, 0.12, 0.33,
     [("Handcrafted", False), ("for the", False), ("modern minds.", True)], (0.80, 0.30)),
    ("4-kutchi-hand-block-print-shirt", 1.18, 0.15, 0.38,
     [("Rooted in", False), ("Indian", True), ("heritage.", True)], (0.80, 0.33)),
]

# third set: the tunics and tops with the most stock (4 each), without the shrug. Paths are relative to product-photos/.
SLIDES_3 = [
    ("everyday-favourite/cutouts/1-pink-jaipuri-short-top", 1.36, 0.235, 0.50, None, None),
    ("everyday-favourite/cutouts/2-maroon-mirror-work-tunic", 0.86, 0.13, 0.35,
     [("Short tunics", False), ("that move you", False), ("with ease.", True)], (0.775, 0.37)),
    ("everyday-favourite-2/cutouts/1-denim-balloon-sleeve-top", 1.18, 0.15, 0.36,
     [("Handcrafted", False), ("for the", False), ("modern minds.", True)], (0.80, 0.33)),
    ("everyday-favourite-2/cutouts/2-rich-red-chanderi-shirt", 0.86, 0.13, 0.29,
     [("Rooted in", False), ("Indian", True), ("heritage.", True)], (0.785, 0.36)),
]


def font(fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(FONTS, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def fbm(h, w, seed, octaves=5, base=4):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = base * 2 ** o
        g = rng.random((max(2, int(n * h / w)), n)).astype(np.float32)
        out += amp * np.asarray(Image.fromarray(g).resize((w, h), Image.BICUBIC))
        tot += amp
        amp *= 0.5
    return out / tot


def leaf(d, x, y, ang, L, w, col):
    pts = []
    for k in range(21):
        t = k / 20
        pts.append((L * t, w * math.sin(math.pi * t) ** 0.9 * (1 - 0.3 * t)))
    poly = [(x + r * math.cos(ang) - s * math.sin(ang), y + r * math.sin(ang) + s * math.cos(ang)) for r, s in pts]
    poly += [(x + r * math.cos(ang) + s * math.sin(ang), y + r * math.sin(ang) - s * math.cos(ang))
             for r, s in reversed(pts)]
    d.polygon(poly, fill=col)


def studio(seed):
    """Blush-greige wall, soft window light from the left, a blurred leafy sprig at the bottom left."""
    x = np.linspace(0, 1, W)[None, :]
    y = np.linspace(0, 1, H)[:, None]
    base = np.array([232, 224, 220], float)
    tone = 1.0 + 0.035 * (1 - x) - 0.03 * y
    img = base[None, None] * tone[..., None]
    # window light: two tall soft bright panes on the left, slightly slanted, with a mullion between
    light = np.zeros((H, W), np.float32)
    for x0, x1 in ((0.0, 0.065), (0.085, 0.16)):
        sl = x - 0.05 * y
        light += (np.clip((sl - x0) / 0.02, 0, 1) * np.clip((x1 - sl) / 0.03, 0, 1) *
                  np.clip((y - 0.02) / 0.1, 0, 1) * np.clip((0.86 - y) / 0.25, 0, 1))
    light = np.asarray(Image.fromarray((light * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22)), float) / 255
    img += light[..., None] * np.array([26, 23, 18])
    img += (fbm(H, W, seed, 5, 6)[..., None] - 0.5) * 5
    img += np.random.default_rng(seed).normal(0, 1.4, (H, W, 1))
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    # the sprig
    rng = np.random.default_rng(4)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    stems = [((-30, 1260), (190, 1000)), ((-20, 1180), (120, 900)), ((0, 1350), (140, 1200)), ((-40, 1060), (90, 940))]
    for (x0, y0), (x1, y1) in stems:
        d.line([(x0, y0), ((x0 + x1) / 2 + 10, (y0 + y1) / 2 + 12), (x1, y1)], fill=(120, 110, 70, 255), width=4)
        for k in range(1, 7):
            t = k / 7
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            base_ang = math.atan2(y1 - y0, x1 - x0)
            for side in (-1, 1):
                ang = base_ang + side * rng.uniform(0.6, 1.1)
                c = tuple(int(v + rng.uniform(-10, 10)) for v in (138, 146, 98)) + (230,)
                leaf(d, px, py, ang, rng.uniform(30, 46), rng.uniform(10, 14), c)
        leaf(d, x1, y1, math.atan2(y1 - y0, x1 - x0), 50, 14, (146, 152, 104, 230))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4.5)))
    return im


def place_model(im, cut, fh, top, cx):
    fig = Image.open(cut).convert("RGBA")
    h = int(fh * H)
    fig = fig.resize((round(fig.width * h / fig.height), h), Image.LANCZOS)
    # warm the cut-out slightly towards the studio light so it sits in the set
    arr = np.asarray(fig, float)
    arr[..., :3] = arr[..., :3] * 0.93 + np.array([236, 226, 220]) * 0.07
    fig = Image.fromarray(arr.astype(np.uint8))
    x, y = int(cx * W - fig.width / 2), int(top * H)
    sh = Image.new("RGBA", fig.size, (90, 70, 60, 0))
    sh.putalpha(fig.getchannel("A").point(lambda v: int(v * 0.28)).filter(ImageFilter.GaussianBlur(26)))
    im.alpha_composite(sh, (x + 34, y + 18))
    im.alpha_composite(fig, (x, y))


def lines_block(im, lines, cx, cy):
    d = ImageDraw.Draw(im)
    f = font("lora", 500, 62, "italic")
    pitch = 72
    y = cy * H - pitch * (len(lines) - 1) / 2
    for text, red in lines:
        d.text((cx * W, y), text, font=f, fill=(MAROON if red else INK) + (255,), anchor="mm")
        y += pitch


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    slides = {"2": SLIDES_2, "3": SLIDES_3}.get((sys.argv[3:] or ["1"])[0], SLIDES)
    for i, (cut, fh, top, cx, lines, tpos) in enumerate(slides, 1):
        im = studio(10 + i)
        place_model(im, os.path.join(src, cut + ".png"), fh, top, cx)
        d = ImageDraw.Draw(im)
        if i == 1:
            d.text((W / 2, 150), "Find Your", font=font("open-sans", 400, 64, "italic"), fill=GREY + (255,),
                   anchor="mm")
            d.text((W / 2, 245), "EVERYDAY FAVOURITE", font=font("open-sans", 700, 70), fill=MAROON + (255,),
                   anchor="mm")
        else:
            lines_block(im, lines, *tpos)
        if i == len(slides):
            f = font("open-sans", 600, 30)
            txt = "w w w . k a l a k a r i c r e a t i o n s . c o m"
            tw = d.textlength(txt, font=f)
            bx0, by0 = W / 2 - tw / 2 - 48, H - 128
            pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(pill).rounded_rectangle((bx0, by0, W - bx0, by0 + 62), radius=31,
                                                   fill=(228, 214, 198, 235))
            im.alpha_composite(pill)
            ImageDraw.Draw(im).text((W / 2, by0 + 31), txt, font=f, fill=INK + (255,), anchor="mm")
        im.convert("RGB").save(os.path.join(out, f"slide-{i}.jpg"), quality=94)
        print("slide", i)


if __name__ == "__main__":
    main()
