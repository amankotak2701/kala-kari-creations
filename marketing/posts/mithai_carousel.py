#!/usr/bin/env python3
"""5-slide 4:5 "Mithai moods" Diwali carousel, laid out like the reference post: a blurred festive background, cream
postage-stamp frames with scalloped edges, a cover with three looks and a headline stamp (plus a firework burst and
rockets), then one look per slide paired with a mithai of the same colour (a round, gold-rimmed photo sticker) and an italic
headline with a short line under it.

Usage:
    python3 mithai_carousel.py <fonts_dir> <photos_dir> <out_dir>
<photos_dir> holds mustard-sharara, pink-short-top, indigo-dabu, green-print and olive-kalamkari (any extension), and a
mithai/ folder with laddoo, katli, coconut and barfi photos.
"""
import glob
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

W, H = 1080, 1350
CREAM = (253, 248, 236)
CRIMSON = (176, 24, 58)

# look, crop (top fraction, bottom fraction), mithai, plate side, headline, line
SLIDES = [
    ("mustard-sharara", (0, 1), "laddoo", "left", "Motichoor mood, golden and good.",
     "Mirror-work paisleys as golden as the first laddoo of Diwali."),
    ("indigo-dabu", (0, 1), "katli", "right", "Kaju katli calm, indigo charm.",
     "Hand block-printed dabu with a silver-tasselled dupatta, timeless and sweet."),
    ("pink-short-top", (0, 1), "coconut", "left", "Gulabi and full of mithaas.",
     "A twirl of block-printed pink for the girl who saves room for dessert."),
    ("green-print", (0, .845), "barfi", "right", "Pista green, easy and serene.",
     "Soft prints for long Diwali days of guests, games and gupshup."),
]
# mithai photo, crop circle (centre x, centre y, radius) as fractions of the photo's width
MITHAI = {"laddoo": ("laddoo", (.523, .596, .433)), "katli": ("katli", (.57, .43, .28)),
          "coconut": ("coconut", (.49, .9, .4)), "barfi": ("barfi", (.5, .485, .45))}
COVER = ["olive-kalamkari", "mustard-sharara", "indigo-dabu"]
COVER_TEXT = ["Mithai moods", "& handmade", "looks this", "DIWALI"]


def font(fonts_dir, name, weight, style, size):
    return ImageFont.truetype(os.path.join(fonts_dir, f"fontsource-{name}", "package", "files",
                                           f"{name}-latin-{weight}-{style}.woff2"), size)


def load(photos_dir, key):
    return Image.open(glob.glob(os.path.join(photos_dir, key + ".*"))[0]).convert("RGB")


def cover_crop(im, w, h, fy=.35):
    s = max(w / im.width, h / im.height)
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = (r.width - w) // 2
    y = int(min(max(r.height * fy - h / 2, 0), r.height - h))
    return r.crop((x, y, x + w, y + h))


def mithai_sticker(photos_dir, kind, d):
    """The mithai photo cut into a circle inside a polished gold rim, like a plate seen from above."""
    name, (fx, fy, fr) = MITHAI[kind]
    im = load(os.path.join(photos_dir, "mithai"), name)
    cx, cy, r = fx * im.width, fy * im.width, fr * im.width
    S = 2
    D = d * S
    ring = int(D * .045)
    inner = im.crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r))).resize((D - 2 * ring, D - 2 * ring), Image.LANCZOS)
    y, x = np.mgrid[0:D, 0:D].astype(np.float32)
    c = D / 2
    rr = np.hypot(x - c, y - c)
    ang = np.arctan2(y - c, x - c)
    t = np.clip((rr - (c - ring)) / ring, 0, 1)                 # 0 inner edge .. 1 outer edge of the rim
    light = .5 + .5 * np.cos(ang + 2.3)
    prof = np.sin(t * math.pi)                                   # rounded rim
    k = .55 + .5 * prof * (.6 + .6 * light) + .25 * np.exp(-((ang + 2.3) / .4) ** 2) * prof
    gold = np.array([206, 160, 70], np.float32)[None, None] * k[..., None]
    img = Image.fromarray(np.clip(gold, 0, 255).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", inner.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, inner.width - 1, inner.height - 1), fill=255)
    img.paste(inner, (ring, ring), m)
    dd = ImageDraw.Draw(img)
    dd.ellipse((ring - S, ring - S, D - ring + S, D - ring + S), outline=(120, 80, 30, 255), width=2 * S)
    a = Image.new("L", (D, D), 0)
    ImageDraw.Draw(a).ellipse((0, 0, D - 1, D - 1), fill=255)
    img.putalpha(a)
    return img.resize((d, d), Image.LANCZOS)


def background(seed=4):
    """Warm, out-of-focus festive table: maroon and red with marigold and gold bokeh."""
    rng = np.random.default_rng(seed)
    img = Image.new("RGB", (W, H), (120, 28, 30))
    d = ImageDraw.Draw(img)
    for _ in range(140):
        x, y = rng.uniform(-100, W + 100), rng.uniform(-100, H + 100)
        r = rng.uniform(40, 170)
        col = [(150, 40, 36), (95, 18, 22), (196, 86, 52), (214, 150, 90), (232, 196, 160), (170, 60, 40),
               (80, 14, 18)][rng.integers(0, 7)]
        d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    img = img.filter(ImageFilter.GaussianBlur(38))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    for _ in range(26):                                # soft bokeh lights
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(14, 34)
        dl.ellipse((x - r, y - r, x + r, y + r), fill=(255, 214, 150, int(rng.uniform(30, 80))))
    img = img.convert("RGBA")
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(5)))
    img.alpha_composite(Image.new("RGBA", (W, H), (40, 6, 8, 70)))
    return img


def stamp(photo, w, h, edge=34, tooth=19, pitch=58):
    """Cream postage stamp with a scalloped (perforated) edge and the photo set inside it."""
    S = 2
    m = Image.new("L", (w * S, h * S), 255)
    d = ImageDraw.Draw(m)
    r = tooth * S
    nx = max(2, round(w / pitch))
    ny = max(2, round(h / pitch))
    for i in range(nx + 1):
        x = i * w * S / nx
        for y in (0, h * S):
            d.ellipse((x - r, y - r, x + r, y + r), fill=0)
    for j in range(ny + 1):
        y = j * h * S / ny
        for x in (0, w * S):
            d.ellipse((x - r, y - r, x + r, y + r), fill=0)
    m = m.resize((w, h), Image.LANCZOS)
    st = Image.new("RGBA", (w, h), CREAM + (255,))
    st.putalpha(m)
    if photo is not None:
        st.paste(cover_crop(photo, w - 2 * edge, h - 2 * edge), (edge, edge))
    return st


def drop(canvas, item, xy, blur=14, off=(0, 10), a=120):
    pad = blur * 3
    sh = Image.new("RGBA", (item.width + 2 * pad, item.height + 2 * pad), (0, 0, 0, 0))
    s = Image.new("RGBA", item.size, (20, 4, 4, 0))
    s.putalpha(item.getchannel("A").point(lambda v: int(v * a / 255)))
    sh.alpha_composite(s, (pad, pad))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (int(xy[0] + off[0] - pad), int(xy[1] + off[1] - pad)))
    canvas.alpha_composite(item, (int(xy[0]), int(xy[1])))


def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if f.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    lines.append(cur)
    return lines


def firework(size, seed=2):
    rng = np.random.default_rng(seed)
    lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = size / 2
    for k in range(46):
        a = k * math.tau / 46 + rng.uniform(-.04, .04)
        r1, r2 = size * rng.uniform(.08, .14), size * rng.uniform(.34, .48)
        col = (255, 214, 120, 255) if k % 3 else (255, 245, 210, 255)
        d.line((c + math.cos(a) * r1, c + math.sin(a) * r1, c + math.cos(a) * r2, c + math.sin(a) * r2), fill=col, width=3)
        d.ellipse((c + math.cos(a) * r2 - 4, c + math.sin(a) * r2 - 4, c + math.cos(a) * r2 + 4, c + math.sin(a) * r2 + 4), fill=col)
    glow = lay.filter(ImageFilter.GaussianBlur(8))
    out = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(glow)
    out.alpha_composite(lay)
    return out


def rocket(length, body, stripe, angle):
    """A Diwali sky-rocket: striped tube, red cone, long stick and a spark at the base."""
    S = 2
    L = length * S
    bw, bl = int(L * .13), int(L * .32)
    lay = Image.new("RGBA", (bw * 3, L + bw * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx = lay.width / 2
    top = bw
    d.polygon([(cx - bw / 2, top + bw * .9), (cx + bw / 2, top + bw * .9), (cx, top - bw * .4)], fill=(200, 30, 40, 255))
    for i in range(6):                                 # tube with diagonal bands
        y0 = top + bw * .9 + i * bl / 6
        d.rectangle((cx - bw / 2, y0, cx + bw / 2, y0 + bl / 6), fill=(body if i % 2 else stripe) + (255,))
    d.rectangle((cx - bw / 2, top + bw * .9, cx - bw / 2 + bw * .18, top + bw * .9 + bl), fill=(255, 255, 255, 60))
    d.rectangle((cx - S * 2, top + bw * .9 + bl, cx + S * 2, L), fill=(150, 100, 60, 255))
    lay = lay.resize((lay.width // S, lay.height // S), Image.LANCZOS)
    return lay.rotate(angle, expand=True, resample=Image.BICUBIC)


def text_block(img, lines_fonts, y, fill=(255, 255, 255), shadow=True):
    for s, f, gap in lines_fonts:
        if shadow:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).text((W / 2, y + 3), s, font=f, fill=(30, 4, 6, 150), anchor="ma")
            img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
        ImageDraw.Draw(img).text((W / 2, y), s, font=f, fill=fill, anchor="ma")
        y += gap
    return y


def slide(bg, fonts_dir, photos_dir, photo, crop, kind, side, head, line):
    img = bg.copy()
    fh = font(fonts_dir, "cormorant-garamond", 700, "italic", 64)
    fl = font(fonts_dir, "cormorant-garamond", 500, "normal", 45)
    rows = [(s, fh, 72) for s in wrap(head, fh, 960)]
    rows[-1] = (rows[-1][0], fh, 84)
    rows += [(s, fl, 52) for s in wrap(line, fl, 860)]
    text_block(img, rows, 56)
    t, b = crop
    ph = photo.crop((0, int(photo.height * t), photo.width, int(photo.height * b)))
    sw, sh = 640, 860
    st = stamp(ph, sw, sh)
    x, y = (W - sw) // 2, 420
    st = st.rotate(-1.2 if side == "left" else 1.2, expand=True, resample=Image.BICUBIC)
    drop(img, st, (x, y))
    d = 360
    pl = mithai_sticker(photos_dir, kind, d)
    px = x - 140 if side == "left" else x + sw - 220
    drop(img, pl, (px, y - 90), blur=10, off=(4, 10), a=150)
    return img


def cover(bg, fonts_dir, photos):
    img = bg.copy()
    sw, sh = 430, 548
    pos = [(90, 70), (560, 70), (90, 690), (560, 690)]
    fw = firework(420)
    img.alpha_composite(fw, (-70, -90))
    items = [photos[0], photos[1], None, photos[2]]
    for k, ((x, y), ph) in enumerate(zip(pos, items)):
        st = stamp(ph, sw, sh, edge=30, tooth=17, pitch=52)
        drop(img, st, (x, y))
    f = font(fonts_dir, "cormorant-garamond", 700, "normal", 58)
    fd = font(fonts_dir, "cormorant-garamond", 700, "normal", 74)
    x0, y0 = pos[2][0] + 54, pos[2][1] + 130
    d = ImageDraw.Draw(img)
    for i, s in enumerate(COVER_TEXT):
        d.text((x0, y0 + i * 70), s, font=fd if s == "DIWALI" else f, fill=CRIMSON, anchor="ls")
    fs = font(fonts_dir, "cormorant-garamond", 600, "italic", 30)
    d.text((x0, pos[2][1] + sh - 62), "KALA KARI CREATIONS", font=font(fonts_dir, "cormorant-garamond", 600, "normal", 24),
           fill=(120, 60, 50), anchor="ls")
    d.text((x0, pos[2][1] + sh - 98), "swipe for the sweet pairings", font=fs, fill=(120, 60, 50), anchor="ls")
    for (L, body, stripe, ang, x, y) in [(330, (40, 70, 160), (232, 190, 80), 28, 840, 880),
                                         (300, (190, 30, 40), (240, 200, 90), 18, 930, 860),
                                         (280, (200, 60, 30), (250, 220, 120), 36, 760, 990)]:
        r = rocket(L, body, stripe, ang)
        drop(img, r, (x, y), blur=6, off=(3, 6), a=110)
    return img


def main():
    fonts_dir, photos_dir, out_dir = sys.argv[1:4]
    os.makedirs(out_dir, exist_ok=True)
    bg = background()
    cover(bg, fonts_dir, [load(photos_dir, k) for k in COVER]).convert("RGB").save(
        os.path.join(out_dir, "slide-1-cover.jpg"), quality=94)
    for i, (key, crop, kind, side, head, line) in enumerate(SLIDES):
        img = slide(bg, fonts_dir, photos_dir, load(photos_dir, key), crop, kind, side, head, line)
        img.convert("RGB").save(os.path.join(out_dir, f"slide-{i + 2}-{key}.jpg"), quality=94)
        print(f"slide-{i + 2}-{key}.jpg")


if __name__ == "__main__":
    main()
