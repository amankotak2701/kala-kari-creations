"""Procedurally drawn mithai on brass plates (motichoor laddoo, pink coconut laddoo, kaju katli, pista barfi), used as
round stickers in the mithai carousel. Everything is drawn with numpy shading, so no stock photos are needed."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 2                                             # supersampling


def _grid(n):
    y, x = np.mgrid[0:n, 0:n].astype(np.float32)
    return x, y


def _noise(n, scale, rng):
    small = rng.standard_normal((max(2, n // scale), max(2, n // scale))).astype(np.float32)
    im = Image.fromarray(small).resize((n, n), Image.BICUBIC)
    a = np.asarray(im, np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)


def _rgba(rgb, alpha):
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.clip(alpha, 0, 255)]).astype(np.uint8), "RGBA")


def plate(d, rng):
    """Round brass thali with a raised, embossed rim."""
    x, y = _grid(d)
    c = d / 2
    r = np.hypot(x - c, y - c) / c
    ang = np.arctan2(y - c, x - c)
    light = .55 + .45 * np.cos(ang + 2.3)          # light from the top left
    base = np.array([184, 136, 58], np.float32)
    rgb = np.repeat(base[None, None], d, 0).repeat(d, 1)
    rim = (r > .8)
    shade = np.where(rim, .75 + .55 * light, 1.02 - .25 * r)
    # embossed beads on the rim
    beads = (np.cos(ang * 48) > .55) & (r > .86) & (r < .93)
    shade = shade * np.where(beads, 1.18, 1.0)
    shade *= np.where((r > .79) & (r < .81), .6, 1.0)
    shade *= np.where((r > .95), .7, 1.0)
    shade += _noise(d, 3, rng) * .025
    spec = np.exp(-((x - c * .6) ** 2 + (y - c * .55) ** 2) / (2 * (c * .35) ** 2)) * .22 * (r < .8)
    rgb = rgb * shade[..., None] + spec[..., None] * 255
    alpha = np.clip((1 - r) * c * 1.5, 0, 1) * 255
    return _rgba(rgb, alpha)


def sphere(d, col, rng, grain="beads"):
    """Shaded ball: motichoor beads or coconut flakes."""
    x, y = _grid(d)
    c = d / 2
    dx, dy = (x - c) / c, (y - c) / c
    rr = dx * dx + dy * dy
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    lx, ly, lz = -.5, -.6, .62
    lam = np.clip(dx * lx + dy * ly + z * lz, 0, 1)
    shade = .42 + .7 * lam
    if grain == "beads":                           # tiny fried boondi beads
        cell = max(3, d // 26)
        gx, gy = (x // cell), (y // cell)
        jitter = rng.uniform(-.3, .3, (d // cell + 2, d // cell + 2, 2))
        fx = (x % cell) / cell - .5 - jitter[gy.astype(int), gx.astype(int), 0]
        fy = (y % cell) / cell - .5 - jitter[gy.astype(int), gx.astype(int), 1]
        bead = np.clip(1 - (fx * fx + fy * fy) * 3.2, 0, 1)
        shade *= .78 + .38 * bead
    else:                                          # desiccated coconut
        flakes = _noise(d, 1, rng)
        shade *= 1 + .12 * np.clip(flakes, -1.5, 2.5)
    rgb = np.array(col, np.float32)[None, None] * shade[..., None]
    spec = np.clip(lam, 0, 1) ** 18 * (70 if grain == "beads" else 22)
    rgb += spec[..., None]
    alpha = np.clip((1 - np.sqrt(rr)) * c * 1.2, 0, 1) * 255
    return _rgba(rgb, alpha)


def diamond(w, h, col, rng, varq=True):
    """Kaju katli: a flat rhombus with silver varq and a lighter bevel."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon([(w / 2, 0), (w, h / 2), (w / 2, h), (0, h / 2)], fill=255)
    x, y = np.mgrid[0:h, 0:w][1].astype(np.float32), np.mgrid[0:h, 0:w][0].astype(np.float32)
    shade = 1 - .12 * (y / h) + .05 * (1 - x / w)
    tex = _noise(max(w, h), 2, rng)[:h, :w]
    rgb = np.array(col, np.float32)[None, None] * shade[..., None] * (1 + .04 * tex[..., None])
    if varq:
        v = _noise(max(w, h), 4, rng)[:h, :w]
        silver = np.clip(v - .2, 0, 1)[..., None]
        rgb = rgb * (1 - silver * .6) + np.array([232, 230, 226])[None, None] * silver * .6
    edge = np.asarray(m.filter(ImageFilter.MinFilter(9)), np.float32) / 255
    rgb = rgb * (.86 + .14 * edge[..., None])
    img = _rgba(rgb, np.asarray(m, np.float32))
    return img


def square(s, col, rng, nuts=True):
    """Pista barfi: a soft-edged square with chopped pistachio and a little varq."""
    x, y = _grid(s)
    edge = np.minimum.reduce([x, y, s - 1 - x, s - 1 - y]) / (s * .08)
    shade = .9 + .1 * np.clip(edge, 0, 1) - .06 * (y / s)
    tex = _noise(s, 2, rng)
    rgb = np.array(col, np.float32)[None, None] * (shade * (1 + .05 * tex))[..., None]
    img = _rgba(rgb, np.clip(edge * 255, 0, 255))
    if nuts:
        d = ImageDraw.Draw(img)
        for _ in range(int(s * .06)):
            cx, cy = rng.uniform(.15, .85, 2) * s
            r = rng.uniform(.025, .05) * s
            a = rng.uniform(0, math.pi)
            g = rng.choice([(96, 140, 48), (120, 160, 60), (150, 110, 70)])
            pts = [(cx + r * math.cos(a + k * 2.1) * (1.4 if k == 0 else .8), cy + r * math.sin(a + k * 2.1)) for k in range(3)]
            d.polygon(pts, fill=tuple(int(v) for v in g) + (255,))
        v = _noise(s, 5, rng)
        lay = np.asarray(img, np.float32)
        silver = (np.clip(v - 1.1, 0, 1) * 1.2)[..., None]
        lay[..., :3] = lay[..., :3] * (1 - silver * .5) + 235 * silver * .5
        img = Image.fromarray(lay.astype(np.uint8), "RGBA")
    return img


def _shadowed(canvas, item, xy, blur=6, off=(5, 7), a=110):
    sh = Image.new("RGBA", item.size, (40, 20, 5, 0))
    sh.putalpha(item.getchannel("A").point(lambda v: int(v * a / 255)))
    pad = blur * 3
    big = Image.new("RGBA", (item.width + pad * 2, item.height + pad * 2), (0, 0, 0, 0))
    big.alpha_composite(sh, (pad, pad))
    big = big.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(big, (int(xy[0] + off[0] - pad), int(xy[1] + off[1] - pad)))
    canvas.alpha_composite(item, (int(xy[0]), int(xy[1])))


def mithai_plate(kind, d, seed=1):
    """A brass plate of mithai, d px across, transparent around the plate."""
    rng = np.random.default_rng(seed)
    D = d * SS
    img = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    _shadowed(img, plate(D, rng), (0, 0), blur=4 * SS, off=(0, 3 * SS), a=0)
    c = D / 2
    if kind in ("laddoo", "coconut"):
        col = (236, 128, 34) if kind == "laddoo" else (240, 160, 182)
        grain = "beads" if kind == "laddoo" else "flakes"
        s = int(D * .3)
        spots = [(c + math.cos(k * math.tau / 6 + .3) * D * .2, c + math.sin(k * math.tau / 6 + .3) * D * .2) for k in range(6)]
        spots.sort(key=lambda p: p[1])
        for px, py in spots + [(c, c - D * .02)]:
            b = sphere(s, col, rng, grain)
            _shadowed(img, b, (px - s / 2, py - s / 2), blur=5 * SS)
            dd = ImageDraw.Draw(img)
            if kind == "laddoo":                   # a few pistachio slivers and melon seeds on top
                for _ in range(3):
                    gx, gy = px + rng.uniform(-.18, .1) * s, py + rng.uniform(-.25, .05) * s
                    dd.ellipse((gx, gy, gx + s * .07, gy + s * .035), fill=(110, 150, 50, 255))
            else:                                  # rose petal and pistachio on each coconut laddoo
                dd.ellipse((px - s * .09, py - s * .3, px + s * .07, py - s * .2), fill=(196, 40, 80, 255))
                dd.ellipse((px + s * .02, py - s * .27, px + s * .12, py - s * .22), fill=(120, 160, 60, 255))
    elif kind == "katli":
        w, h = int(D * .18), int(D * .27)
        for k in range(8):                         # a star of diamonds around one in the middle
            a = k * math.tau / 8
            dm = diamond(w, h, (236, 220, 188), rng).rotate(-math.degrees(a) - 90, expand=True, resample=Image.BICUBIC)
            px, py = c + math.cos(a) * D * .22, c + math.sin(a) * D * .22
            _shadowed(img, dm, (px - dm.width / 2, py - dm.height / 2), blur=3 * SS, off=(2 * SS, 3 * SS))
        dm = diamond(w, h, (238, 222, 190), rng)
        _shadowed(img, dm, (c - w / 2, c - h / 2), blur=3 * SS, off=(2 * SS, 3 * SS))
        dd = ImageDraw.Draw(img)
        dd.ellipse((c - D * .02, c - D * .02, c + D * .02, c + D * .02), fill=(200, 40, 90, 255))
    elif kind == "barfi":
        s = int(D * .155)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) + abs(j) > 1 and (i, j) not in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
                    continue
                sq = square(s, (176, 204, 118), rng).rotate(45, expand=True, resample=Image.BICUBIC)
                px = c + (i - j) * s * .74
                py = c + (i + j) * s * .74
                _shadowed(img, sq, (px - sq.width / 2, py - sq.height / 2), blur=3 * SS, off=(2 * SS, 3 * SS))
    # keep everything inside the plate
    m = Image.new("L", (D, D), 0)
    ImageDraw.Draw(m).ellipse((0, 0, D - 1, D - 1), fill=255)
    a = np.minimum(np.asarray(img.getchannel("A")), np.asarray(m))
    img.putalpha(Image.fromarray(a))
    return img.resize((d, d), Image.LANCZOS)


if __name__ == "__main__":
    import sys
    row = Image.new("RGBA", (4 * 420, 420), (110, 30, 30, 255))
    for k, kind in enumerate(["katli", "laddoo", "barfi", "coconut"]):
        row.alpha_composite(mithai_plate(kind, 400, seed=k + 1), (k * 420 + 10, 10))
    row.convert("RGB").save(sys.argv[1])
