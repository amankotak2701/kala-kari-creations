"""Photo-style mithai on brass plates (motichoor laddoo, coconut laddoo, kaju katli, pista barfi), used as round
stickers in the mithai carousel. Each sweet is built from shaded 3D pieces: a laddoo is hundreds of glossy boondi
pearls packed on a sphere, coconut laddoo is coated in flakes, katli and barfi are thick pieces with grainy tops,
visible sides and crinkled silver varq. Warm light from the top left, contact shadows and a little film grain."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 2                                             # supersampling
LIGHT = np.array([-.45, -.6, .66])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def _grid(h, w=None):
    w = w or h
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    return x, y


def _noise(h, w, scale, rng):
    small = rng.standard_normal((max(2, h // scale + 1), max(2, w // scale + 1))).astype(np.float32)
    a = np.asarray(Image.fromarray(small).resize((w, h), Image.BICUBIC), np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)


def _fbm(h, w, rng, scales=(64, 24, 8, 3)):
    n = sum(_noise(h, w, s, rng) * (s ** .5) for s in scales)
    return n / n.std()


def _rgba(rgb, alpha):
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.clip(alpha, 0, 255)]).astype(np.uint8), "RGBA")


def _shadow(canvas, item, xy, blur, off, a):
    pad = int(blur * 3) + 2
    big = Image.new("RGBA", (item.width + pad * 2, item.height + pad * 2), (0, 0, 0, 0))
    s = Image.new("RGBA", item.size, (45, 22, 6, 0))
    s.putalpha(item.getchannel("A").point(lambda v: int(v * a / 255)))
    big.alpha_composite(s, (pad, pad))
    canvas.alpha_composite(big.filter(ImageFilter.GaussianBlur(blur)), (int(xy[0] + off[0] - pad), int(xy[1] + off[1] - pad)))


def place(canvas, item, xy, contact=True):
    """Composite with a soft cast shadow and a tight, dark contact shadow."""
    s = item.width / 100
    _shadow(canvas, item, xy, blur=5 * s, off=(4 * s, 6 * s), a=120)
    if contact:
        _shadow(canvas, item, xy, blur=1.5 * s, off=(1 * s, 2 * s), a=150)
    canvas.alpha_composite(item, (int(xy[0]), int(xy[1])))


# ------------------------------------------------------------------ plate
def plate(d, rng):
    """Brass thali seen from above: brushed circular grain, a raised rim with beading, warm highlights."""
    x, y = _grid(d)
    c = d / 2
    r = np.hypot(x - c, y - c) / c
    ang = np.arctan2(y - c, x - c)
    # brushed grain runs around the plate
    grain = _noise(256, 2048, 1, rng)
    gi = np.clip((r * 255).astype(int), 0, 255)
    gj = ((ang + math.pi) / math.tau * 2047).astype(int)
    brushed = grain[gi, gj]
    brushed = brushed * .5 + np.roll(brushed, 1, 1) * .25 + np.roll(brushed, -1, 1) * .25
    base = np.array([176, 128, 52], np.float32)
    # rim slope normals: inner wall faces inwards, outer lip faces outwards
    slope = np.where((r > .78) & (r < .86), -1.0, np.where(r > .9, 1.0, 0.0))
    nx, ny = np.cos(ang) * slope * .7, np.sin(ang) * slope * .7
    nz = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
    lam = np.clip(nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2], 0, 1)
    shade = .55 + .6 * lam
    beads = (np.cos(ang * 64) > .2) & (r > .865) & (r < .9)
    bead_light = .5 + .5 * np.cos(ang * 64 + .9)
    shade = np.where(beads, .7 + .6 * bead_light, shade)
    shade *= 1 + .05 * brushed
    # broad reflected highlight on the flat well and a hot streak on the rim
    hx, hy = c - c * .35, c - c * .42
    hl = np.exp(-(((x - hx) / (c * .55)) ** 2 + ((y - hy) / (c * .35)) ** 2)) * (r < .78) * .35
    rim_hot = np.exp(-((ang + 2.25) / .35) ** 2) * ((r > .78) & (r < .86)) * .55
    rgb = base[None, None] * shade[..., None]
    rgb = rgb + (hl + rim_hot)[..., None] * np.array([255, 226, 160])[None, None]
    rgb *= (1 - .18 * np.clip((r - .2) / .6, 0, 1) * (r < .78))[..., None]    # well darkens towards the rim
    alpha = np.clip((1 - r) * c * 1.2, 0, 1) * 255
    return _rgba(rgb, alpha)


# ------------------------------------------------------------------ round sweets
def _bead_sprite(px):
    x, y = _grid(px)
    c = (px - 1) / 2
    dx, dy = (x - c) / (c + .5), (y - c) / (c + .5)
    rr = dx * dx + dy * dy
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    lam = np.clip(dx * LIGHT[0] + dy * LIGHT[1] + z * LIGHT[2], 0, 1)
    spec = np.clip(lam, 0, 1) ** 30
    alpha = np.clip((1 - np.sqrt(rr)) * (c + .5) * 1.5, 0, 1)
    return lam, spec, alpha


def laddoo(d, rng, col=(232, 112, 24)):
    """Motichoor laddoo: a ball of tiny glossy boondi pearls, warmer and darker in the gaps."""
    D = d
    img = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    c, R = D / 2, D / 2 * .96
    # dark core so gaps between pearls read as depth
    x, y = _grid(D)
    rr = ((x - c) ** 2 + (y - c) ** 2) / R ** 2
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    core = np.array([150, 52, 8], np.float32)[None, None] * (.55 + .45 * z)[..., None]
    img.alpha_composite(_rgba(core, np.clip((1 - np.sqrt(rr)) * R, 0, 1) * 255))
    n = int(900 * (D / 300) ** .2)
    v = rng.standard_normal((n * 2, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    v = v[v[:, 2] > -.05][:n]
    v = v[np.argsort(v[:, 2])]                     # back to front
    bead = R * .085
    sprites = {}
    for vx, vy, vz in v:
        size = max(3, int(bead * 2 * rng.uniform(.85, 1.15)))
        if size not in sprites:
            sprites[size] = _bead_sprite(size)
        lam_b, spec_b, a_b = sprites[size]
        sl = max(0, vx * LIGHT[0] + vy * LIGHT[1] + vz * LIGHT[2])
        tone = np.array(col, np.float32) * rng.uniform(.9, 1.08)
        rgb = tone[None, None] * (.35 + .55 * sl + .35 * lam_b[..., None] * (.4 + .6 * sl)) + spec_b[..., None] * 255 * (.25 + .6 * sl)
        rim = .55 + .45 * max(vz, 0) ** .5             # pearls at the silhouette sit in shadow
        sp = _rgba(rgb * rim, a_b * 255)
        img.alpha_composite(sp, (int(c + vx * R * .93 - size / 2), int(c + vy * R * .93 - size / 2)))
    d_ = ImageDraw.Draw(img)
    for _ in range(4):                             # melon seeds and pistachio slivers
        a, rad = rng.uniform(0, math.tau), rng.uniform(0, .55) * R
        gx, gy = c + math.cos(a) * rad - R * .15, c + math.sin(a) * rad - R * .15
        if rng.uniform() < .5:
            d_.ellipse((gx, gy, gx + R * .16, gy + R * .08), fill=(246, 238, 214, 255), outline=(200, 180, 140, 255))
        else:
            d_.polygon([(gx, gy), (gx + R * .2, gy + R * .04), (gx + R * .05, gy + R * .08)], fill=(118, 150, 52, 255))
    return img


def coconut_laddoo(d, rng, col=(238, 150, 172)):
    """Coconut laddoo rolled in desiccated coconut, with a rose petal and a pistachio sliver."""
    D = d
    c, R = D / 2, D / 2 * .95
    x, y = _grid(D)
    dx, dy = (x - c) / R, (y - c) / R
    rr = dx * dx + dy * dy
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    lam = np.clip(dx * LIGHT[0] + dy * LIGHT[1] + z * LIGHT[2], 0, 1)
    base = np.array(col, np.float32)[None, None] * (.45 + .6 * lam)[..., None]
    img = _rgba(base, np.clip((1 - np.sqrt(rr)) * R * 1.2, 0, 1) * 255)
    lay = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    n = 1400
    v = rng.standard_normal((n * 2, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    v = v[v[:, 2] > 0][:n]
    for vx, vy, vz in v[np.argsort(v[:, 2])]:
        sl = max(0, vx * LIGHT[0] + vy * LIGHT[1] + vz * LIGHT[2])
        k = .5 + .65 * sl
        tone = np.array([252, 214, 224]) if rng.uniform() < .6 else np.array([255, 246, 246])
        col_f = tuple(int(min(255, t * k)) for t in tone) + (230,)
        ln = R * rng.uniform(.04, .08) * (.4 + .6 * vz)
        a = rng.uniform(0, math.pi)
        px, py = c + vx * R * .97, c + vy * R * .97
        dl.line((px - math.cos(a) * ln, py - math.sin(a) * ln, px + math.cos(a) * ln, py + math.sin(a) * ln),
                fill=col_f, width=max(1, int(R * .022)))
    img.alpha_composite(lay)
    d_ = ImageDraw.Draw(img)
    d_.ellipse((c - R * .2, c - R * .55, c + R * .08, c - R * .36), fill=(160, 26, 60, 255))     # dried rose petal
    d_.ellipse((c - R * .14, c - R * .52, c + R * .0, c - R * .43), fill=(196, 50, 86, 255))
    d_.polygon([(c + R * .05, c - R * .5), (c + R * .3, c - R * .44), (c + R * .1, c - R * .38)], fill=(116, 150, 50, 255))
    return img


# ------------------------------------------------------------------ flat sweets
def varq(h, w, rng, amount=.5):
    """Crinkled silver foil: irregular patches with sharp wrinkle highlights."""
    patch = _fbm(h, w, rng, (40, 14, 5))
    mask = np.clip((patch - (1.4 - amount * 2)) * 2.5, 0, 1)
    wr = _noise(h, w, 2, rng)
    wr = np.abs(wr - np.roll(wr, 1, 0)) + np.abs(wr - np.roll(wr, 1, 1))
    tone = 175 + 70 * np.clip(wr, 0, 1.2) / 1.2
    return mask, tone


def slab(poly_top, depth, top_col, side_col, rng, varq_amount=0.0, nuts=0, size=None):
    """A thick piece of mithai: shaded side faces below the top face, grainy top, optional varq and nuts."""
    w, h = size
    S = 1
    img = Image.new("RGBA", (w, h + depth), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(x, y) for x, y in poly_top]
    # side faces: draw the polygon shifted down, then each edge's quad
    for i in range(len(pts)):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
        nx, ny = (y2 - y1), -(x2 - x1)
        if ny <= 0:                                # only faces pointing towards the viewer's bottom
            continue
        ln = math.hypot(nx, ny)
        k = .55 + .3 * max(0, (nx / ln) * -LIGHT[0])
        col = tuple(int(c_ * k) for c_ in side_col) + (255,)
        d.polygon([(x1, y1), (x2, y2), (x2, y2 + depth), (x1, y1 + depth)], fill=col)
    m = Image.new("L", (w, h + depth), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    x, y = _grid(h + depth, w)
    grain = _noise(h + depth, w, 1, rng) * .6 + _noise(h + depth, w, 3, rng) * .4
    shade = 1.04 - .1 * (y / h) + .05 * grain
    top = np.array(top_col, np.float32)[None, None] * shade[..., None]
    edge = np.asarray(m.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(2)), np.float32) / 255
    top = top * (.9 + .1 * edge[..., None]) + (1 - edge[..., None]) * 12      # soft lighter bevel
    if varq_amount:
        vm, vt = varq(h + depth, w, rng, varq_amount)
        top = top * (1 - vm[..., None]) + vt[..., None] * vm[..., None]
    t_img = _rgba(top, np.asarray(m, np.float32))
    img.alpha_composite(t_img)
    if nuts:
        dn = ImageDraw.Draw(img)
        mx = np.asarray(m) > 0
        ys, xs = np.where(mx)
        for _ in range(nuts):
            i = rng.integers(0, len(xs))
            cx, cy = xs[i], ys[i]
            r = rng.uniform(.03, .06) * w
            a = rng.uniform(0, math.pi)
            p = [(cx + math.cos(a) * r, cy + math.sin(a) * r), (cx + math.cos(a + 2.6) * r * .45, cy + math.sin(a + 2.6) * r * .45),
                 (cx - math.cos(a) * r, cy - math.sin(a) * r), (cx + math.cos(a - .5) * r * .45, cy + math.sin(a - .5) * r * .45)]
            dn.polygon(p, fill=(98, 142, 46, 255))
            dn.line(p[:2], fill=(130, 70, 90, 255), width=max(1, int(r * .25)))   # purple-brown skin on one edge
    return img


def katli(w, rng):
    h = int(w * 1.45)
    pts = [(w / 2, 0), (w, h / 2), (w / 2, h), (0, h / 2)]
    return slab(pts, max(3, int(w * .07)), (238, 224, 196), (214, 196, 160), rng, varq_amount=.62, size=(w, h))


def barfi(s, rng):
    pts = [(0, 0), (s, 0), (s, s), (0, s)]
    return slab(pts, max(4, int(s * .2)), (182, 200, 126), (160, 176, 104), rng, varq_amount=.3, nuts=6, size=(s, s))


# ------------------------------------------------------------------ plates
def mithai_plate(kind, d, seed=1):
    """A brass plate of mithai, d px across, transparent around the plate."""
    rng = np.random.default_rng(seed)
    D = d * SS
    img = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    img.alpha_composite(plate(D, rng))
    c = D / 2
    if kind in ("laddoo", "coconut"):
        s = int(D * .31)
        ring = [(c + math.cos(k * math.tau / 6 + .4) * D * .2, c + math.sin(k * math.tau / 6 + .4) * D * .2) for k in range(6)]
        for px, py in sorted(ring, key=lambda p: p[1]) + [(c, c - D * .03)]:
            b = laddoo(s, rng) if kind == "laddoo" else coconut_laddoo(s, rng)
            place(img, b, (px - s / 2, py - s / 2))
    elif kind == "katli":
        w = int(D * .17)
        pieces = []
        for k in range(9):                         # overlapping fan of diamonds, slightly irregular
            a = k * math.tau / 9 + rng.uniform(-.08, .08)
            pieces.append((a, D * .22))
        for a, rad in pieces:
            dm = katli(w, rng).rotate(-math.degrees(a) - 90 + rng.uniform(-6, 6), expand=True, resample=Image.BICUBIC)
            place(img, dm, (c + math.cos(a) * rad - dm.width / 2, c + math.sin(a) * rad - dm.height / 2))
        for k in range(2):
            dm = katli(w, rng).rotate(k * 55 + 10, expand=True, resample=Image.BICUBIC)
            place(img, dm, (c - dm.width / 2 + k * D * .03, c - dm.height / 2 - k * D * .02))
    elif kind == "barfi":
        s = int(D * .17)
        spots = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for i, j in spots:
            sq = barfi(s, rng).rotate(38 + rng.uniform(-5, 5), expand=True, resample=Image.BICUBIC)
            px = c + (i - j) * s * .76 + rng.uniform(-4, 4)
            py = c + (i + j) * s * .76 - D * .02
            if math.hypot(px - c, py - c) > D * .34:
                continue
            place(img, sq, (px - sq.width / 2, py - sq.height / 2))
    # keep everything inside the plate's well
    m = Image.new("L", (D, D), 0)
    ImageDraw.Draw(m).ellipse((1, 1, D - 2, D - 2), fill=255)
    a = np.minimum(np.asarray(img.getchannel("A")), np.asarray(m))
    img.putalpha(Image.fromarray(a))
    out = img.resize((d, d), Image.LANCZOS)
    # warm grade and a touch of film grain so it sits like a photo
    arr = np.asarray(out, np.float32)
    arr[..., :3] = arr[..., :3] * np.array([1.03, 1.0, .94]) + rng.standard_normal(arr.shape[:2])[..., None] * 3
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


if __name__ == "__main__":
    import sys
    row = Image.new("RGBA", (4 * 420, 420), (110, 30, 30, 255))
    for k, kind in enumerate(["katli", "laddoo", "barfi", "coconut"]):
        row.alpha_composite(mithai_plate(kind, 400, seed=k + 1), (k * 420 + 10, 10))
    row.convert("RGB").save(sys.argv[1])
