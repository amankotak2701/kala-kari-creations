#!/usr/bin/env python3
"""3-slide square "everyday edit" carousel, matched to the reference brand post's tone and placement.

The reference's rules:
- Light blush-cream text (about #FEF0EC) only on mid-to-dark, muted parts of the photo. Slides 1 and 2 are
  graded moody: darker and softer, with a soft extra dip in brightness behind the text.
- Dark maroon text (about #602F2C) only on light parts (slide 3).
- No glow or box behind the text: the contrast comes from the photo itself.
- The type is an elegant italic or upright serif headline and a small spaced-caps sans line. The brand is
  small, in widely spaced serif capitals with a smaller line under it.

Layouts:
1. Model on the left half; a centred text column on the right.
2. Model right of centre; a two-line sentence at the top left and the brand at the middle left.
3. Two photos of one product side by side: the brand at the top left on the light curtain, and the headline at
   the bottom right on the light stone.

Usage:
    python3 everyday_edit_carousel.py <fonts_dir> <photos_dir> <out_dir>
"""
import glob
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

S = 1080
CREAM = (254, 240, 234)
MAROON = (96, 47, 44)
WOOD = (104, 66, 54)        # slide 1: the carved door's and the carved table's warm brown
WOOD_SOFT = (138, 98, 82)
ROSE = (150, 78, 92)        # slide 2: a deeper shade of the anarkali's block-printed flowers
ROSE_SOFT = (128, 104, 96)


def font(fonts, fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(fonts, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def crop(d, key, box, w, h):
    """Crop box (fractions of the source: x0, y0, x1, y1) and resize to w x h."""
    im = Image.open(glob.glob(os.path.join(d, key + ".*"))[0]).convert("RGB")
    x0, y0, x1, y1 = box
    return im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height))) \
        .resize((w, h), Image.LANCZOS)


def moody(im, bright=.8, sat=.88):
    """The reference's soft, slightly dim, warm grade."""
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Color(im).enhance(sat)
    a = np.asarray(im).astype(np.float32)
    a[..., 0] *= 1.03
    a[..., 2] *= .96
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def dip(im, cx, cy, rx, ry, strength):
    """Soft elliptical darkening behind a text block (feathered, so it reads as light falloff, not a box)."""
    y, x = np.mgrid[0:im.height, 0:im.width].astype(np.float32)
    r = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
    k = 1 - strength * np.clip(1.25 - r, 0, 1) ** 1.5
    a = np.asarray(im).astype(np.float32) * k[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def haze(im, cx, cy, rx, ry, strength):
    """Soft, feathered lightening behind a text block only (the outfit and model stay untouched)."""
    y, x = np.mgrid[0:im.height, 0:im.width].astype(np.float32)
    r = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
    k = strength * np.clip(1.2 - r, 0, 1) ** 1.6
    a = np.asarray(im).astype(np.float32)
    a = a * (1 - k[..., None]) + np.array([252, 248, 242], np.float32) * k[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def spaced(d, xy, s, f, fill, spacing, anchor="m"):
    widths = [d.textlength(c, font=f) for c in s]
    total = sum(widths) + spacing * (len(s) - 1)
    x, y = xy
    if anchor == "m":
        x -= total / 2
    for c, w in zip(s, widths):
        d.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += w + spacing


def brand(d, cx, y, fonts, fill, size):
    spaced(d, (cx, y), "KALA KARI", font(fonts, "cormorant-garamond", 400, size), fill, size * .34)
    spaced(d, (cx, y + size * .78), "CREATIONS", font(fonts, "cormorant-garamond", 500, int(size * .42)), fill,
           size * .2)


def slide1(fonts, ph):
    # landscape photo: square crop with the model on the left half
    im = crop(ph, "1-ajrakh-seated", (.335, 0, 1.0, 1.0), S, S)
    im = haze(im, 806, 260, 240, 240, .38)
    img = im.convert("RGBA")
    d = ImageDraw.Draw(img)
    cx = 806
    f = font(fonts, "cormorant-garamond", 400, 76, "italic")
    d.text((cx, 140), "Made by Hand,", font=f, fill=WOOD, anchor="ms")
    d.text((cx, 220), "Made for You", font=f, fill=WOOD, anchor="ms")
    fs = font(fonts, "jost", 400, 20)
    spaced(d, (cx, 284), "HANDCRAFTED ETHNICWEAR", fs, WOOD_SOFT, 4.5)
    spaced(d, (cx, 318), "FOR EVERY DAY", fs, WOOD_SOFT, 4.5)
    brand(d, cx, 396, fonts, WOOD, 40)
    return img


def slide2(fonts, ph):
    # portrait photo: a square from the top-left part puts the model right of centre
    im = crop(ph, "2-pink-anarkali", (0, .02, .84, .65), S, S)
    im = haze(im, 190, 165, 250, 170, .55)
    im = haze(im, 190, 395, 190, 80, .55)
    img = im.convert("RGBA")
    d = ImageDraw.Draw(img)
    f = font(fonts, "cormorant-garamond", 500, 52)
    fi = font(fonts, "cormorant-garamond", 500, 52, "italic")
    d.text((54, 112), "Easy elegance,", font=fi, fill=ROSE, anchor="ls")
    d.text((54, 170), "from morning", font=f, fill=ROSE, anchor="ls")
    d.text((54, 228), "to evening.", font=f, fill=ROSE, anchor="ls")
    brand(d, 190, 388, fonts, ROSE, 40)
    return img


def slide3(fonts, ph):
    # As in the reference: full look on the left (its pale arch at the top left takes the brand), close-up on
    # the right (its plain red lower kurta at the bottom right takes the cream headline).
    import cv2
    img = Image.new("RGBA", (S, S))
    left = crop(ph, "3a-red-kurta-full", (.10, 0, .74, .87), 540, S)
    right = crop(ph, "3b-red-kurta-closeup", (.20, .14, .84, .99), 540, S)
    # paint out the image generator's corner badge on the close-up (bottom right)
    a = cv2.cvtColor(np.asarray(right), cv2.COLOR_RGB2BGR)
    m = np.zeros(a.shape[:2], np.uint8)
    cv2.circle(m, (470, 1000), 44, 255, -1)
    right = Image.fromarray(cv2.cvtColor(cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))
    img.paste(left, (0, 0))
    img.paste(right, (540, 0))
    d = ImageDraw.Draw(img)
    brand(d, 112, 74, fonts, MAROON, 26)
    d.text((S - 44, 978), "Every Stitch,", font=font(fonts, "cormorant-garamond", 500, 62), fill=CREAM,
           anchor="rs")
    d.text((S - 44, 1044), "a Story", font=font(fonts, "cormorant-garamond", 500, 62, "italic"), fill=CREAM,
           anchor="rs")
    return img


def main():
    fonts, ph, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    for i, fn in enumerate((slide1, slide2, slide3), 1):
        fn(fonts, ph).convert("RGB").save(os.path.join(out, f"slide-{i}.jpg"), quality=94)
        print(f"slide-{i}.jpg")


if __name__ == "__main__":
    main()
