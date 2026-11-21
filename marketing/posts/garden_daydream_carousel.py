#!/usr/bin/env python3
"""4-slide 4:5 "A Little Garden Daydream" carousel for the Royal Blue Leheriya 3-Piece Suit, in the layout of the
reference post (an old-master painted landscape framed in white lace roses, then looks on a swirling mossy-green
painted backdrop with pale painted swallows).

1. A muted painted landscape; a white lace frame of roses, flowers and leaves; inside it the model stands small,
   full length; "A LITTLE GARDEN / DAYDREAM" in spaced serif capitals below, and the welcome offer under that.
2. The model from head to knee on the swirling green backdrop, a few swallows in the sky.
3. A close-up of the kurta's leheriya stripes and the bandhani dupatta.
4. The second pose on the backdrop, with the welcome offer and the website on a small lace-edged card.
The painting, lace and birds are drawn here; the model is cut out of the product photos with rembg.

Usage:
    python3 garden_daydream_carousel.py <cutouts-dir> <out-dir>
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
LACE = (238, 236, 226)


def font(fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(FONTS, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def fbm(h, w, seed, octaves=6, base=3):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = base * 2 ** o
        g = rng.random((max(2, int(n * h / w)), n)).astype(np.float32)
        out += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


def brush(img, seed, strength=10, length=21, angle=None):
    """Oil-paint brush texture: directional streaks of noise laid over the colours."""
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, img.shape[:2]).astype(np.float32)
    k = np.zeros((length, length), np.float32)
    k[length // 2] = 1
    if angle is not None:
        k = cv2.warpAffine(k, cv2.getRotationMatrix2D((length / 2, length / 2), angle, 1), (length, length))
    k /= k.sum()
    streak = cv2.filter2D(n, -1, k) * strength
    return np.clip(img + streak[..., None], 0, 255)


# ---------------- painted backgrounds ----------------

def landscape(w, h, seed=1):
    """A muted old-master landscape: hazy olive sky with soft clouds, a pale distant hill, a dark wooded bank on the
    right, grassy slopes and a path, all with oil-paint texture."""
    y = np.linspace(0, 1, h)[:, None]
    x = np.linspace(0, 1, w)[None, :]
    sky = np.array([142, 146, 116]) * (1 - y[..., None]) + np.array([178, 172, 132]) * y[..., None]
    img = np.broadcast_to(sky, (h, w, 3)).astype(np.float32).copy()
    cl = fbm(h, w, seed, 6, 3)
    img += (cv2.GaussianBlur(cl, (0, 0), 14)[..., None] - 0.5) * 12
    def hill(yb, amp, freq, s):
        xs = np.linspace(0, 1, w)
        r = np.random.default_rng(s)
        ph = r.uniform(0, 6, 3)
        return yb - amp * (0.6 * np.sin(xs * freq + ph[0]) + 0.3 * np.sin(xs * freq * 2.3 + ph[1]) +
                           0.1 * np.sin(xs * freq * 5.1 + ph[2]))
    layers = [(0.50, 0.04, 4, (128, 136, 120), 0.0),     # pale far hill
              (0.60, 0.05, 6, (98, 104, 64), 0.0),      # mid slope
              (0.72, 0.04, 5, (84, 82, 48), 0.0),       # near grass
              (0.86, 0.03, 7, (104, 88, 56), 0.0)]      # foreground bank
    for k, (yb, amp, f, col, _) in enumerate(layers):
        top = hill(yb, amp, f, seed + k)[None, :]
        m = np.clip((y - top) * h / 6, 0, 1)[..., None]
        tex = (fbm(h, w, seed + 10 + k, 6, 6)[..., None] - 0.5) * 40
        img = img * (1 - m) + (np.array(col) + tex) * m
    # dark wooded bank on the right, rising to the top right
    wood = np.clip(((x - 0.62) * 3 + (0.75 - y) * 0.8 + (fbm(h, w, seed + 20, 6, 5) - 0.5) * 0.9), 0, 1)
    wood = np.clip(wood * 2.2, 0, 1) * (y < 0.82) * np.clip((y - 0.42) / 0.12, 0, 1)   # trees stay below the sky
    wood = cv2.GaussianBlur(wood.astype(np.float32), (0, 0), 6)[..., None]
    img = img * (1 - wood * 0.8) + np.array([58, 60, 36]) * wood * 0.8
    img = brush(img, seed, 9, 25, 15)
    img = cv2.GaussianBlur(img.astype(np.float32), (0, 0), 1.2)
    return img


def swirl_backdrop(w, h, seed=5):
    """A hand-painted studio backdrop: mossy olive greens in big swirling brush strokes, lighter in the middle."""
    rng = np.random.default_rng(seed)
    n = fbm(h, w, seed, 5, 6)
    # swirl: blur the noise along circles around a point left of centre
    cx, cy = w * 0.42, h * 0.55
    # rotational blur: average the noise turned by small angles about a point, giving seamless circular strokes
    acc = np.zeros_like(n)
    angs = np.linspace(-14, 14, 29)
    for a in angs:
        M = cv2.getRotationMatrix2D((cx, cy), a, 1.0)
        acc += cv2.warpAffine(n, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    sw = acc / len(angs)
    sw = (sw - sw.min()) / (sw.max() - sw.min() + 1e-6)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    glow = np.exp(-(((xx - w * 0.5) / (w * 0.55)) ** 2 + ((yy - h * 0.45) / (h * 0.55)) ** 2))
    dark = np.array([46, 58, 26], np.float32)
    mid = np.array([104, 118, 52], np.float32)
    light = np.array([150, 160, 88], np.float32)
    t = np.clip(0.25 + 0.55 * sw + 0.35 * glow - 0.15, 0, 1)[..., None]
    img = dark * (1 - t) ** 2 + mid * 2 * t * (1 - t) + light * t ** 2
    img = brush(img, seed, 8, 31, 30)
    return cv2.GaussianBlur(img.astype(np.float32), (0, 0), 1.0)


def swallow(d, x, y, s, rot, col):
    """A small painted swallow: two swept wings and a forked tail."""
    def P(px, py):
        c, s_ = math.cos(rot), math.sin(rot)
        return (x + (px * c - py * s_) * s, y + (px * s_ + py * c) * s)
    body = [P(-0.15, 0), P(0.25, -0.05), P(0.3, 0.02), P(-0.1, 0.08)]
    lw = [P(0.05, 0), P(-0.35, -0.55), P(-0.9, -0.75), P(-0.25, -0.12)]
    rw = [P(0.08, 0.02), P(-0.1, 0.5), P(-0.6, 0.85), P(-0.12, 0.12)]
    tail = [P(-0.12, 0.02), P(-0.55, -0.12), P(-0.38, 0.03), P(-0.55, 0.18)]
    for poly in (body, lw, rw, tail):
        d.polygon(poly, fill=col)


def birds(img, spots, seed=2, alpha=150):
    lay = Image.new("RGBA", (img.shape[1], img.shape[0]), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x, y, s, r in spots:
        swallow(d, x, y, s, r, (232, 228, 204, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(1.6))
    base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    base.alpha_composite(lay)
    return np.asarray(base.convert("RGB")).astype(np.float32)


# ---------------- lace frame ----------------

def mesh(size, pitch=7, alpha=120):
    """A fine net (bobbinet) texture to fill lace motifs."""
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    for k in range(-size[1], size[0] + size[1], pitch):
        d.line([(k, 0), (k + size[1], size[1])], fill=alpha, width=1)
        d.line([(k, 0), (k - size[1], size[1])], fill=alpha, width=1)
    return m


def rose(d, cx, cy, r, ink, seed=0):
    """A lace rose: rings of scalloped, slightly irregular petals around a spiralling bud, as white outlines."""
    rng = np.random.default_rng(int(cx * 7 + cy))
    pts = []
    for k in range(60):                        # the bud's spiral
        t = k / 59
        a = t * 4 * math.pi
        rr = r * (0.06 + 0.26 * t)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(pts, fill=ink, width=max(2, int(r * 0.035)))
    for ring, rr0 in enumerate((1.0, 0.72, 0.48)):
        rr = rr0 * rng.uniform(0.95, 1.05)
        n = (9, 7, 5)[ring]
        for k in range(n):
            a0 = 2 * math.pi * k / n + ring * 0.5
            a1 = a0 + 2 * math.pi / n * 1.1
            box = (cx - r * rr, cy - r * rr, cx + r * rr, cy + r * rr)
            d.arc(box, math.degrees(a0), math.degrees(a1), fill=ink, width=max(2, int(r * 0.05)))
            mx, my = cx + r * rr * math.cos((a0 + a1) / 2), cy + r * rr * math.sin((a0 + a1) / 2)
            d.arc((mx - r * 0.22 * rr, my - r * 0.22 * rr, mx + r * 0.22 * rr, my + r * 0.22 * rr),
                  math.degrees((a0 + a1) / 2) - 70, math.degrees((a0 + a1) / 2) + 70, fill=ink,
                  width=max(2, int(r * 0.04)))


def daisy(d, cx, cy, r, ink, n=6):
    for k in range(n):
        a = 2 * math.pi * k / n
        px, py = cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)
        d.ellipse((px - r * 0.42, py - r * 0.42, px + r * 0.42, py + r * 0.42), outline=ink, width=3)
    d.ellipse((cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2), fill=ink)


def leaf(d, x, y, ang, L, w, ink):
    pts = []
    for k in range(17):
        t = k / 16
        pts.append((L * t, w * math.sin(math.pi * t)))
    c, s = math.cos(ang), math.sin(ang)
    up = [(x + a * c - b * s, y + a * s + b * c) for a, b in pts]
    dn = [(x + a * c + b * s, y + a * s - b * c) for a, b in pts[::-1]]
    d.line(up + dn + [up[0]], fill=ink, width=3)
    d.line([(x, y), (x + L * 0.9 * c, y + L * 0.9 * s)], fill=ink, width=2)
    for k in range(1, 5):                     # veins
        t = k / 5
        bx, by = x + L * t * c, y + L * t * s
        for sgn in (1, -1):
            d.line([(bx, by), (bx + w * 0.7 * math.cos(ang + sgn * 0.9), by + w * 0.7 * math.sin(ang + sgn * 0.9))],
                   fill=ink, width=2)


def lace_frame(box, seed=3):
    """White lace roses, flowers and leaves around a rectangle, filled with fine net, on a transparent layer."""
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(seed)
    outline = Image.new("L", (W, H), 0)
    fill = Image.new("L", (W, H), 0)
    do, df = ImageDraw.Draw(outline), ImageDraw.Draw(fill)
    band = 66
    # the path around the frame, as points with their direction
    pts = []
    per = 2 * ((x1 - x0) + (y1 - y0))
    for k in range(0, int(per), 6):
        p = k
        if p < x1 - x0:
            pts.append((x0 + p, y0, 0))
        elif p < (x1 - x0) + (y1 - y0):
            pts.append((x1, y0 + p - (x1 - x0), math.pi / 2))
        elif p < 2 * (x1 - x0) + (y1 - y0):
            pts.append((x1 - (p - (x1 - x0) - (y1 - y0)), y1, math.pi))
        else:
            pts.append((x0, y1 - (p - 2 * (x1 - x0) - (y1 - y0)), -math.pi / 2))
    # leaves all along the band, alternating out from the line
    for i in range(0, len(pts), 5):
        x, y, a = pts[i]
        for sgn in (1, -1):
            ang = a + sgn * rng.uniform(0.6, 1.2) + rng.normal(0, 0.2)
            L, w = rng.uniform(34, 54), rng.uniform(11, 16)
            leaf(do, x, y, ang, L, w, 255)
            leaf(df, x, y, ang, L, w, 0)
            df.polygon([(x, y), (x + L * math.cos(ang - 0.25), y + L * math.sin(ang - 0.25)),
                        (x + L * math.cos(ang + 0.25), y + L * math.sin(ang + 0.25))], fill=255)
    # small flowers
    for i in range(18, len(pts), 41):
        x, y, a = pts[i]
        r = rng.uniform(20, 28)
        ox, oy = rng.normal(0, 14), rng.normal(0, 14)
        df.ellipse((x + ox - r, y + oy - r, x + ox + r, y + oy + r), fill=255)
        daisy(do, x + ox, y + oy, r, 255)
    # roses: at the corners, mid-sides and between
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    big = [(x0, y0, 62), (x1, y0, 62), (x0, y1, 62), (x1, y1, 62), (xm, y0 - 4, 46), (xm, y1 + 4, 46),
           (x0, ym - 160, 44), (x0, ym + 160, 50), (x1, ym - 210, 50), (x1, ym + 120, 44),
           (x0 + 150, y0 - 6, 34), (x1 - 160, y0 + 4, 36), (x0 + 170, y1 + 6, 36), (x1 - 150, y1 - 2, 34)]
    for x, y, r in big:
        df.ellipse((x - r * 1.05, y - r * 1.05, x + r * 1.05, y + r * 1.05), fill=255)
        do.ellipse((x - r * 1.05, y - r * 1.05, x + r * 1.05, y + r * 1.05), fill=0)
        rose(do, x, y, r, 255)
    net = mesh((W, H), 6, 255)
    fill_np = np.asarray(fill, np.float32) / 255 * np.asarray(net, np.float32) / 255 * 0.55
    out_np = np.asarray(outline, np.float32) / 255
    a = np.clip(out_np * 0.95 + fill_np, 0, 1)
    lay = Image.new("RGBA", (W, H), LACE + (0,))
    lay.putalpha(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5)))
    return lay


# ---------------- slides ----------------

def place(img, cut, height, cx, bottom, shadow=True):
    fig = Image.open(cut).convert("RGBA")
    fig = fig.resize((round(fig.width * height / fig.height), int(height)), Image.LANCZOS)
    # warm the figure slightly towards the painting's light
    a = np.asarray(fig, np.float32)
    a[..., :3] = a[..., :3] * 0.92 + np.array([150, 150, 110]) * 0.08
    fig = Image.fromarray(a.astype(np.uint8))
    base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    x, y = int(cx - fig.width / 2), int(bottom - fig.height)
    if shadow:
        sh = Image.new("RGBA", fig.size, (20, 22, 10, 0))
        sh.putalpha(fig.getchannel("A").filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.35)))
        base.alpha_composite(sh, (x + 16, y + 10))
    base.alpha_composite(fig, (x, y))
    return base


def spaced(d, xy, text, f, fill, track):
    w = sum(d.textlength(c, font=f) + track for c in text) - track
    x = xy[0] - w / 2
    for c in text:
        d.text((x, xy[1]), c, font=f, fill=fill, anchor="lm")
        x += d.textlength(c, font=f) + track


def offer_lines(d, y, size, col, sub):
    """WELCOME10 offer and website, in the slide's spaced serif type (the ₹ sign drawn in DejaVu)."""
    f = font("cormorant-garamond", 600, size)
    spaced(d, (W / 2, y), "NEW HERE?  FLAT 10% OFF  ·  CODE WELCOME10", f, col, 2)
    fi = font("cormorant-garamond", 500, int(size * 0.92), "italic")
    fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(size * 0.68))
    parts = [("on your first order above ", fi), ("₹", fr), ("999  ·  kalakaricreations.com", fi)]
    tw = sum(d.textlength(t, font=ff) for t, ff in parts)
    x = W / 2 - tw / 2
    for t, ff in parts:
        d.text((x, y + size * 1.35), t, font=ff, fill=sub, anchor="lm")
        x += d.textlength(t, font=ff)


def slide1(cuts):
    bg = landscape(W, H, 1)
    bg = bg * 0.82                                  # the outer painting is darker than the framed view
    box = (196, 140, 884, 1000)
    inner = landscape(box[2] - box[0], box[3] - box[1], 7)
    inner = birds(inner, [(270, 190, 26, -0.2), (320, 150, 22, -0.1), (360, 180, 20, -0.25), (410, 145, 18, -0.15),
                          (240, 145, 18, -0.3)])
    bgi = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
    bgi.paste(Image.fromarray(np.clip(inner, 0, 255).astype(np.uint8)), (box[0], box[1]))
    im = place(np.asarray(bgi, np.float32), os.path.join(cuts, "rb1.png"), 400, W / 2, 900)
    im.alpha_composite(lace_frame(box))
    d = ImageDraw.Draw(im)
    f = font("cormorant-garamond", 500, 54)
    spaced(d, (W / 2, 1100), "A LITTLE GARDEN", f, (244, 240, 226, 255), 9)
    spaced(d, (W / 2, 1172), "DAYDREAM", f, (244, 240, 226, 255), 9)
    offer_lines(d, 1255, 26, (236, 222, 170, 255), (236, 232, 214, 255))
    return im.convert("RGB")


def backdrop_with_birds(seed, spots):
    return birds(swirl_backdrop(W, H, seed), spots, alpha=170)


def slide_model(cut, height, cx, bottom, seed, spots):
    return place(backdrop_with_birds(seed, spots), cut, height, cx, bottom)


def slide3(cuts):
    """Close-up: the leheriya kurta and the bandhani dupatta, filling most of the frame over the backdrop."""
    bg = backdrop_with_birds(9, [])
    fig = Image.open(os.path.join(cuts, "rb3.png")).convert("RGBA")
    s = 2.55 * H / fig.height
    fig = fig.resize((round(fig.width * s), round(fig.height * s)), Image.LANCZOS)
    a = np.asarray(fig, np.float32)
    a[..., :3] = a[..., :3] * 0.92 + np.array([150, 150, 110]) * 0.08
    fig = Image.fromarray(a.astype(np.uint8))
    base = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA")
    # frame the torso-to-hem with the dupatta on the right, like the reference's detail crop
    base.alpha_composite(fig, (int(W * 0.52 - fig.width * 0.55), int(-fig.height * 0.33)))
    return base.convert("RGB")


def slide4(cuts):
    im = slide_model(os.path.join(cuts, "rb3.png"), 1900, W * 0.48, 2000, 13,
                     [(860, 70, 46, -0.3), (960, 130, 34, -0.15)])
    # the offer on a small lace-edged cream card at the bottom
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    bx0, by0, bx1, by1 = 120, 1170, 960, 1308
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=10, fill=(242, 238, 224, 235))
    for x in range(bx0 + 14, bx1 - 10, 22):           # scalloped lace edge
        d.arc((x - 11, by0 - 11, x + 11, by0 + 11), 180, 360, fill=(242, 238, 224, 235), width=6)
        d.arc((x - 11, by1 - 11, x + 11, by1 + 11), 0, 180, fill=(242, 238, 224, 235), width=6)
    d.rectangle((bx0 + 10, by0 + 10, bx1 - 10, by1 - 10), outline=(150, 150, 110, 255), width=1)
    im.alpha_composite(lay)
    offer_lines(ImageDraw.Draw(im), by0 + 48, 30, (52, 60, 120, 255), (70, 70, 50, 255))
    return im.convert("RGB")


def main():
    cuts, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    slide1(cuts).save(os.path.join(out, "slide-1.jpg"), quality=94)
    slide_model(os.path.join(cuts, "rb1.png"), 2100, W * 0.50, 2350, 5,
                [(760, 60, 50, -0.35), (880, 110, 38, -0.2), (110, 140, 30, 0.2)]).convert("RGB").save(
        os.path.join(out, "slide-2.jpg"), quality=94)
    slide3(cuts).save(os.path.join(out, "slide-3.jpg"), quality=94)
    slide4(cuts).save(os.path.join(out, "slide-4.jpg"), quality=94)
    print(out)


if __name__ == "__main__":
    main()
