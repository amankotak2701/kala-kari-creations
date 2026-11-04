#!/usr/bin/env python3
"""3-slide square "everyday edit" carousel, laid out like the reference brand post: soft editorial photos with
elegant serif text set in the photo's empty space, and the brand in widely spaced capitals.
1. Model on the left. At the top right, a big italic headline, a small spaced-caps line, then the brand.
2. Model on the right. A one-line serif sentence at the top left, and the brand at the middle left.
3. Two photos of one product (full look | close-up). The brand at the top left, a headline at the bottom
   right.

Usage:
    python3 everyday_edit_carousel.py <fonts_dir> <photos_dir> <out_dir>
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 1080
MAROON = (110, 30, 42)
CREAM = (252, 246, 236)


def font(fonts, fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(fonts, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def load(d, key, w, h, fx=.5, fy=.5, trim=True):
    im = Image.open(glob.glob(os.path.join(d, key + ".*"))[0]).convert("RGB")
    if trim:                                   # keep the image generator's corner badge out of frame
        im = im.crop((0, 0, int(im.width * .92), int(im.height * .92)))
    s = max(w / im.width, h / im.height)
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = int(min(max(r.width * fx - w / 2, 0), r.width - w))
    y = int(min(max(r.height * fy - h / 2, 0), r.height - h))
    return r.crop((x, y, x + w, y + h)).convert("RGBA")


def spaced(d, xy, s, f, fill, spacing, anchor="l"):
    widths = [d.textlength(c, font=f) for c in s]
    total = sum(widths) + spacing * (len(s) - 1)
    x, y = xy
    if anchor == "m":
        x -= total / 2
    elif anchor == "r":
        x -= total
    for c, w in zip(s, widths):
        d.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += w + spacing
    return total


def text_on(img, draw_fn, fill, glow):
    """Draw text with a soft glow behind it (a light glow for dark text, a dark one for light text)."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay), glow + (150,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(9)))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay), fill + (255,))
    img.alpha_composite(lay)


def brand(d, x, y, fonts, fill, anchor="l", size=56):
    spaced(d, (x, y), "KALA KARI", font(fonts, "cormorant-garamond", 500, size), fill, size * .32, anchor)
    spaced(d, (x + (0 if anchor != "l" else size * .06), y + size * .62), "CREATIONS",
           font(fonts, "cormorant-garamond", 500, int(size * .38)), fill, size * .2, anchor)


def slide1(fonts, ph):
    img = load(ph, "1-ajrakh-seated", S, S, fx=1.0, fy=.5, trim=False)   # model to the left
    cx = 830

    def draw(d, col):
        f = font(fonts, "cormorant-garamond", 500, 74, "italic")
        d.text((cx, 150), "Made by Hand,", font=f, fill=col, anchor="ms")
        d.text((cx, 228), "Made for You", font=f, fill=col, anchor="ms")
        spaced(d, (cx, 286), "HANDCRAFTED ETHNICWEAR", font(fonts, "jost", 400, 19), col, 3.5, "m")
        spaced(d, (cx, 316), "FOR EVERY DAY", font(fonts, "jost", 400, 19), col, 3.5, "m")
        brand(d, cx, 420, fonts, col, "m", 44)
    text_on(img, draw, MAROON, (255, 252, 246))
    return img


def slide2(fonts, ph):
    img = load(ph, "2-pink-anarkali", S, S, fx=.4, fy=.42)

    def draw(d, col):
        f = font(fonts, "cormorant-garamond", 600, 44)
        d.text((44, 80), "Easy elegance,", font=f, fill=col, anchor="ls")
        d.text((44, 130), "from morning to evening.", font=f, fill=col, anchor="ls")
        brand(d, 46, 230, fonts, col, "l", 38)
    text_on(img, draw, MAROON, (255, 250, 246))
    return img


def slide3(fonts, ph):
    img = Image.new("RGBA", (S, S), CREAM + (255,))
    left = load(ph, "3a-red-kurta-full", 560, S, fx=.5, fy=.45)
    right = load(ph, "3b-red-kurta-closeup", 520, S, fx=.5, fy=.5)
    img.alpha_composite(left, (0, 0))
    img.alpha_composite(right, (560, 0))

    def bottom(d, col):                  # on the plain red hem of the full-length photo, clear of her face
        cx = 330
        d.text((cx, 840), "Every Stitch,", font=font(fonts, "cormorant-garamond", 500, 66), fill=col, anchor="ms")
        d.text((cx, 912), "a Story", font=font(fonts, "cormorant-garamond", 500, 66, "italic"), fill=col,
               anchor="ms")
        brand(d, cx, 990, fonts, col, "m", 34)
    text_on(img, bottom, CREAM, (60, 10, 18))
    return img


def main():
    fonts, ph, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    for i, fn in enumerate((slide1, slide2, slide3), 1):
        fn(fonts, ph).convert("RGB").save(os.path.join(out, f"slide-{i}.jpg"), quality=94)
        print(f"slide-{i}.jpg")


if __name__ == "__main__":
    main()
