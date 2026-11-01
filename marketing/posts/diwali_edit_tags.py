#!/usr/bin/env python3
"""3-slide 4:5 "The Diwali Edit" product carousel, laid out like the reference post: a soft beige wall and a
wooden rod with jute strings.
1. A close-up photo hanging from the rod, with a deckle-edged cream card clipped on by a wooden peg and a small
   kraft tag.
2. A tall cream gift tag with the heading on top and the embroidery close-up filling its lower half.
3. The full look in a photo frame hung from the rod, with the product name on a cream label.

Usage:
    python3 diwali_edit_tags.py <fonts_dir> <photos_dir> <out_dir>
<photos_dir> holds pose-closeup, neckline-detail and courtyard-full (any extension).
"""
import glob
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
WALL = (214, 190, 160)
CARD = (244, 236, 222)
INK = (92, 62, 44)
GOLD = (176, 132, 62)
JUTE = (170, 132, 86)
HEAD = ["THE", "DIWALI EDIT"]
SUB = ["Silk · Hand-Embroidered", "Cream Coral 3 Piece Suit Set"]


def font(fonts_dir, name, weight, size, style="normal"):
    return ImageFont.truetype(os.path.join(fonts_dir, f"fontsource-{name}", "package", "files",
                                           f"{name}-latin-{weight}-{style}.woff2"), size)


def load(d, key):
    return Image.open(glob.glob(os.path.join(d, key + ".*"))[0]).convert("RGB")


def cover(im, w, h, fx=.5, fy=.4):
    s = max(w / im.width, h / im.height)
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = int(min(max(r.width * fx - w / 2, 0), r.width - w))
    y = int(min(max(r.height * fy - h / 2, 0), r.height - h))
    return r.crop((x, y, x + w, y + h))


def wall(seed=1):
    """Soft beige plaster wall with a gentle light falloff from the top left."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    light = 1.06 - .16 * np.hypot((x - W * .3) / W, (y - H * .2) / H)
    small = rng.standard_normal((H // 8, W // 8)).astype(np.float32)
    n = np.asarray(Image.fromarray(small).resize((W, H), Image.BICUBIC)) * 2.2 + rng.standard_normal((H, W)) * 1.4
    rgb = np.array(WALL, np.float32)[None, None] * light[..., None] + n[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")


def shadow(canvas, item, xy, blur=16, off=(8, 14), a=90):
    pad = blur * 3
    sh = Image.new("RGBA", (item.width + 2 * pad, item.height + 2 * pad), (0, 0, 0, 0))
    s = Image.new("RGBA", item.size, (60, 40, 24, 0))
    s.putalpha(item.getchannel("A").point(lambda v: int(v * a / 255)))
    sh.alpha_composite(s, (pad, pad))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (int(xy[0] + off[0] - pad), int(xy[1] + off[1] - pad)))
    canvas.alpha_composite(item, (int(xy[0]), int(xy[1])))


def rod(canvas, y, x0=-20, x1=W + 20, t=34):
    """Polished wooden rod with grain."""
    lay = Image.new("RGBA", (x1 - x0, t), (0, 0, 0, 0))
    a = np.zeros((t, x1 - x0, 3), np.float32)
    prof = np.sin(np.linspace(0, math.pi, t))[:, None]
    hi = np.exp(-((np.arange(t) - t * .3) / (t * .12)) ** 2)[:, None]
    rng = np.random.default_rng(3)
    grain = np.asarray(Image.fromarray(rng.standard_normal((t // 2 + 1, (x1 - x0) // 40 + 2)).astype(np.float32))
                       .resize((x1 - x0, t), Image.BICUBIC))
    base = np.array([122, 78, 46], np.float32)
    a[:] = base * (.55 + .45 * prof[..., None]) * (1 + .06 * grain[..., None]) + hi[..., None] * 60
    lay = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    shadow(canvas, lay, (x0, y), blur=10, off=(0, 12), a=110)


def string(d, p0, p1, width=4):
    """Twisted jute string between two points."""
    (x0, y0), (x1, y1) = p0, p1
    n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 6))
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        a, b = (x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0), (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)
        d.line((a, b), fill=JUTE + (255,) if i % 2 else (196, 160, 110, 255), width=width)


def lotus(d, cx, cy, s, col=GOLD, w=2):
    """Small line-drawn lotus: three petals, two side leaves, a base line."""
    def petal(ang, ln, wd):
        pts = []
        for i in range(21):
            t = i / 20
            pts.append((wd * math.sin(math.pi * t), -ln * t))
        pts = pts + [(-x, y) for x, y in reversed(pts)]
        a = math.radians(ang)
        return [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    for ang, ln, wd in ((0, s, s * .32), (-40, s * .8, s * .26), (40, s * .8, s * .26), (-75, s * .55, s * .2),
                        (75, s * .55, s * .2)):
        d.line(petal(ang, ln, wd), fill=col, width=w)
    d.line((cx - s * .7, cy + s * .12, cx + s * .7, cy + s * .12), fill=col, width=w)


def divider(d, cx, y, half, s=22):
    d.line((cx - half, y, cx - s * 1.1, y), fill=GOLD, width=2)
    d.line((cx + s * 1.1, y, cx + half, y), fill=GOLD, width=2)
    lotus(d, cx, y + s * .3, s)


def deckle(w, h, seed=2, rough=7):
    """Cream handmade-paper card with torn (deckle) edges and a faint fibre texture."""
    rng = np.random.default_rng(seed)
    m = Image.new("L", (w, h), 0)
    pts = []
    for side in range(4):
        n = 60
        for i in range(n):
            t = i / n
            j = rng.uniform(0, rough)
            if side == 0:
                pts.append((t * w, j))
            elif side == 1:
                pts.append((w - j, t * h))
            elif side == 2:
                pts.append((w - t * w, h - j))
            else:
                pts.append((j, h - t * h))
    ImageDraw.Draw(m).polygon(pts, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(.8))
    fib = rng.standard_normal((h, w)) * 3 + np.asarray(
        Image.fromarray(rng.standard_normal((h // 6 + 1, w // 6 + 1)).astype(np.float32)).resize((w, h))) * 3
    rgb = np.array(CARD, np.float32)[None, None] + fib[..., None]
    card = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    card.putalpha(m)
    return card


def peg(h=110, w=30):
    """Wooden clothes peg with a metal spring."""
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=6, fill=(196, 150, 98, 255))
    d.rounded_rectangle((w * .45, 0, w * .55, h - 1), radius=2, fill=(160, 116, 70, 255))
    d.rectangle((2, h * .36, w - 3, h * .46), fill=(150, 150, 150, 255))
    d.line((2, h * .38, w - 3, h * .38), fill=(210, 210, 210, 255), width=2)
    return lay


def tag(w, h, col=CARD, hole=True, radius=10, cut=60):
    """Luggage-style tag: rectangle with clipped top corners and a brass eyelet."""
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.polygon([(cut, 0), (w - cut, 0), (w, cut), (w, h), (0, h), (0, cut)], fill=col + (255,))
    if hole:
        cx, cy, r = w / 2, cut * .62, max(8, w * .035)
        d.ellipse((cx - r * 1.7, cy - r * 1.7, cx + r * 1.7, cy + r * 1.7), fill=(184, 140, 70, 255))
        d.ellipse((cx - r * 1.2, cy - r * 1.2, cx + r * 1.2, cy + r * 1.2), fill=(222, 184, 110, 255))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(0, 0, 0, 0))
    return lay


def heading(d, f, cx, y, title_big, title_small, sub_f, width, sub=SUB):
    d.text((cx, y), HEAD[0], font=title_small, fill=INK, anchor="ma")
    y += title_small.size + 4
    d.text((cx, y), HEAD[1], font=title_big, fill=INK, anchor="ma")
    y += title_big.size + 26
    divider(d, cx, y, width / 2)
    y += 34
    for s in sub:
        d.text((cx, y), s, font=sub_f, fill=INK, anchor="ma")
        y += sub_f.size + 8
    return y


def slide1(fonts, photo):
    img = wall(1)
    # the close-up hangs from the rod on the right, like the garment in the reference
    ph = cover(photo, 560, 1230, fx=.42, fy=.52).convert("RGBA")
    shadow(img, ph, (W - 560, 95), blur=18, off=(-10, 16), a=90)
    rod(img, 40)
    d = ImageDraw.Draw(img)
    # deckle card on a jute string, clipped with a peg
    card = deckle(470, 360)
    cx, cy = 50, 300
    string(d, (cx + 235, 74), (cx + 235, cy + 6))
    shadow(img, card.rotate(-1.5, expand=True, resample=Image.BICUBIC), (cx, cy), blur=14, off=(6, 12), a=80)
    d = ImageDraw.Draw(img)
    heading(d, None, cx + 238, cy + 54, font(fonts, "cinzel", 500, 56), font(fonts, "cinzel", 500, 42),
            font(fonts, "cormorant-garamond", 500, 30), 300)
    pg = peg()
    shadow(img, pg, (cx + 222, cy - 70), blur=5, off=(3, 5), a=110)
    # small kraft tag with a lotus on the photo side
    kt = tag(110, 200, col=(176, 128, 98), cut=26)
    dk = ImageDraw.Draw(kt)
    lotus(dk, 55, 110, 24, col=(236, 214, 170), w=2)
    dk.line((55, 140, 55, 176), fill=(236, 214, 170), width=2)
    d = ImageDraw.Draw(img)
    string(d, (690, 74), (690, 200), width=3)
    shadow(img, kt.rotate(4, expand=True, resample=Image.BICUBIC), (632, 188), blur=8, off=(5, 8), a=100)
    return img


def slide2(fonts, photo):
    img = wall(2)
    rod(img, 40)
    d = ImageDraw.Draw(img)
    # second plain tag behind, slightly turned, with a lotus line
    back = tag(470, 900, col=(236, 226, 208), cut=80)
    db = ImageDraw.Draw(back)
    lotus(db, 340, 470, 34, w=2)
    db.line((340, 300, 340, 430), fill=GOLD, width=2)
    db.line((340, 500, 340, 640), fill=GOLD, width=2)
    string(d, (600, 74), (640, 230), width=4)
    shadow(img, back.rotate(-6, expand=True, resample=Image.BICUBIC), (420, 190), blur=16, off=(8, 14), a=80)
    # main tag: heading on top, embroidery close-up in the lower half
    tw, th = 600, 1130
    main = tag(tw, th, cut=90)
    dm = ImageDraw.Draw(main)
    heading(dm, None, tw / 2, 120, font(fonts, "cinzel", 500, 64), font(fonts, "cinzel", 500, 46),
            font(fonts, "cormorant-garamond", 500, 32), 340)
    pw, phh = tw - 60, th - 470
    win = cover(photo, pw, phh, fx=.5, fy=.4)
    main.paste(win, (30, 440))
    d = ImageDraw.Draw(img)
    x0, y0 = (W - tw) // 2 - 40, 150
    string(d, (W / 2 - 70, 74), (x0 + tw / 2 - 18, y0 + 60), width=5)
    string(d, (W / 2 - 10, 74), (x0 + tw / 2 + 18, y0 + 60), width=5)
    shadow(img, main, (x0, y0), blur=18, off=(10, 16), a=95)
    d = ImageDraw.Draw(img)
    d.ellipse((x0 + tw / 2 - 30, y0 + 40, x0 + tw / 2 + 30, y0 + 82), outline=JUTE, width=5)   # string loop through eyelet
    return img


def slide3(fonts, photo):
    img = wall(3)
    rod(img, 40)
    d = ImageDraw.Draw(img)
    # full look in a thin cream-mounted frame hung from the rod by two jute strings
    fw, fh = 560, 1100
    frame = Image.new("RGBA", (fw, fh), CARD + (255,))
    photo = photo.crop((0, 0, int(photo.width * .88), photo.height))     # keep the corner badge out of frame
    frame.paste(cover(photo, fw - 40, fh - 40, fx=.5, fy=.42), (20, 20))
    fx, fy = (W - fw) // 2, 100
    string(d, (fx + 120, 74), (fx + 120, fy + 6))
    string(d, (fx + fw - 120, 74), (fx + fw - 120, fy + 6))
    shadow(img, frame, (fx, fy), blur=20, off=(10, 18), a=100)
    # product label under the frame
    label = deckle(620, 112, seed=5, rough=5)
    dl = ImageDraw.Draw(label)
    dl.text((310, 22), "Cream Coral Silk Embroidered 3-Piece Suit Set", font=font(fonts, "cormorant-garamond", 600, 30),
            fill=INK, anchor="ma")
    lotus(dl, 310, 80, 14, w=2)
    dl.text((180, 72), "THE DIWALI EDIT", font=font(fonts, "cinzel", 500, 20), fill=INK, anchor="ma")
    dl.text((440, 72), "kalakaricreations.com", font=font(fonts, "cormorant-garamond", 500, 22, "italic"), fill=INK,
            anchor="ma")
    shadow(img, label, ((W - 620) // 2, fy + fh - 40), blur=10, off=(5, 8), a=80)
    return img


def main():
    fonts, photos, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    for name, fn, key in (("slide-1-teaser.jpg", slide1, "pose-closeup"),
                          ("slide-2-detail-tag.jpg", slide2, "neckline-detail"),
                          ("slide-3-full-look.jpg", slide3, "courtyard-full")):
        fn(fonts, load(photos, key)).convert("RGB").save(os.path.join(out, name), quality=94)
        print(name)


if __name__ == "__main__":
    main()
