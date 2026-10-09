#!/usr/bin/env python3
"""Render 9:16 Instagram product reels from single product photos.

Each reel: hook on the full look -> slow pans over two craft details ->
full look with product name -> maroon end card with the stacked logo and
ordering contact. Soft original background music comes from music.py.

Usage:
    python3 make_reels.py <photos_dir> <fonts_dir> <out_dir> [reel_id ...]

<photos_dir> holds 1.webp..4.webp (1611x2000). <fonts_dir> holds the
@fontsource/cinzel and @fontsource/cormorant-garamond packages extracted
as in brand/logo/README.md.
"""
import math
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import music

W, H, FPS = 1080, 1920, 30
XFADE = 0.5  # seconds of crossfade between shots

MAROON = (117, 44, 57)
CREAM = (247, 242, 233)
GOLD = (217, 188, 121)
GOLD_DARK = (168, 130, 63)

# Text sits between y=230 and y~1500 to clear Instagram's top bar and caption/buttons.
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-gold-flat.png")

# Shots: (duration, zoom start, zoom end, centre start, centre end, caption).
# Centres are in source-pixel coords; zoom 1.0 = full image height in frame.
REELS = {
    "shrug-patchwork": dict(
        photo="1.webp",
        hook=("Every patch", "tells a story"),
        name=("Patchwork Block Print", "Long Shrug"),
        tagline="Layer it. Love it. Live in it.",
        shots=[
            (3.2, 1.14, 1.00, (805, 1000), (805, 1000), None),
            (3.4, 2.10, 2.35, (850, 470), (840, 560), "Hand block-printed patchwork yoke"),
            (3.4, 1.45, 1.45, (620, 1250), (990, 1250), "A flared, free-flowing silhouette"),
            (3.4, 1.00, 1.08, (805, 1000), (805, 950), "name"),
        ],
    ),
    "tunic-olive-smocked": dict(
        photo="2.webp",
        hook=("Quiet colour,", "loud craft"),
        name=("Olive Smocked Yoke", "Tunic"),
        tagline="Everyday ease with a handmade heart.",
        shots=[
            (3.2, 1.14, 1.00, (805, 1000), (805, 1000), None),
            (3.4, 2.40, 2.65, (815, 590), (815, 620), "Hand-smocked yoke with mirror accents"),
            (3.4, 2.20, 2.35, (1040, 650), (1035, 800), "Paisley thread work on the sleeves"),
            (3.4, 1.00, 1.08, (805, 1000), (805, 940), "name"),
        ],
    ),
    "tunic-ivory-leaf": dict(
        photo="3.webp",
        hook=("Nature,", "stitched by hand"),
        name=("Ivory Leaf Appliqué", "Tunic"),
        tagline="Soft neutrals for slow mornings.",
        shots=[
            (3.2, 1.14, 1.00, (805, 1000), (805, 1000), None),
            (3.4, 2.30, 2.55, (720, 760), (735, 780), "Hand-cut appliqué leaves"),
            (3.4, 2.30, 2.45, (930, 1080), (950, 1170), "Delicate running-stitch detailing"),
            (3.4, 1.00, 1.08, (805, 1000), (805, 950), "name"),
        ],
    ),
    "tunic-ivory-lotus": dict(
        photo="4.webp",
        hook=("Bloom in", "black & ivory"),
        name=("Ivory Lotus Appliqué", "Tunic"),
        tagline="A modern classic, rooted in craft.",
        shots=[
            (3.2, 1.14, 1.00, (805, 1000), (805, 1000), None),
            (3.4, 2.40, 2.65, (815, 560), (820, 600), "Striped V-neck with silver ghungroos"),
            (3.4, 1.95, 2.05, (680, 1010), (930, 1010), "Lace lotus appliqué border"),
            (3.4, 1.00, 1.08, (805, 1000), (805, 950), "name"),
        ],
    ),
}
END_CARD = 4.5


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


class Fonts:
    def __init__(self, d):
        cin = os.path.join(d, "fontsource-cinzel", "package", "files")
        cor = os.path.join(d, "fontsource-cormorant-garamond", "package", "files")
        self.cinzel = lambda w, s: ImageFont.truetype(os.path.join(cin, f"cinzel-latin-{w}-normal.woff2"), s)
        self.cor_it = lambda w, s: ImageFont.truetype(os.path.join(cor, f"cormorant-garamond-latin-{w}-italic.woff2"), s)
        self.cor = lambda w, s: ImageFont.truetype(os.path.join(cor, f"cormorant-garamond-latin-{w}-normal.woff2"), s)


def text_layer(lines, size=(W, 600), shadow=True, spacing=1.15, tracking=0):
    """lines: list of (text, font, fill). Returns centred RGBA layer."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = 0
    placed = []
    for text, font, fill in lines:
        if tracking:
            widths = [d.textlength(c, font=font) for c in text]
            tw = sum(widths) + tracking * (len(text) - 1)
        else:
            tw = d.textlength(text, font=font)
        asc, desc = font.getmetrics()
        placed.append((text, font, fill, (size[0] - tw) / 2, y, tracking))
        y += int((asc + desc) * spacing)

    def draw_all(dd, colour=None):
        for text, font, fill, x, yy, tr in placed:
            c = colour or fill
            if tr:
                for ch in text:
                    dd.text((x, yy), ch, font=font, fill=c)
                    x += dd.textlength(ch, font=font) + tr
            else:
                dd.text((x, yy), text, font=font, fill=c)

    if shadow:
        sh = Image.new("RGBA", size, (0, 0, 0, 0))
        draw_all(ImageDraw.Draw(sh), (0, 0, 0, 170))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        layer = Image.alpha_composite(layer, sh)
        d = ImageDraw.Draw(layer)
    draw_all(d)
    return layer.crop((0, 0, size[0], max(y, 1) + 30))


def with_alpha(img, a):
    if a >= 0.999:
        return img
    r, g, b, al = img.split()
    al = al.point(lambda v: int(v * a))
    return Image.merge("RGBA", (r, g, b, al))


def paste_anim(frame, layer, y, t, t_in, t_out, rise=40):
    """Fade + rise in at t_in, fade out ending at t_out."""
    if t < t_in or t > t_out:
        return
    a = min(ease((t - t_in) / 0.6), ease((t_out - t) / 0.4))
    if a <= 0:
        return
    dy = int((1 - ease((t - t_in) / 0.8)) * rise)
    frame.alpha_composite(with_alpha(layer, a), ((W - layer.width) // 2, y + dy))


def gradient(h, top_alpha, bottom_alpha):
    g = Image.new("L", (1, h))
    for i in range(h):
        g.putpixel((0, i), int(lerp(top_alpha, bottom_alpha, i / (h - 1))))
    g = g.resize((W, h))
    layer = Image.new("RGBA", (W, h), (20, 8, 10, 0))
    layer.putalpha(g)
    return layer


def ken_burns(src, zoom, cx, cy):
    sw, sh = src.size
    ch = sh / zoom
    cw = ch * W / H
    x0 = min(max(cx - cw / 2, 0), sw - cw)
    y0 = min(max(cy - ch / 2, 0), sh - ch)
    s = cw / W
    return src.transform((W, H), Image.AFFINE, (s, 0, x0, 0, s, y0), resample=Image.BICUBIC)


def build_reel(cfg, photos, fonts, out_path, seed=0):
    src = Image.open(os.path.join(photos, cfg["photo"])).convert("RGB")
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((560, int(560 * logo.height / logo.width)), Image.LANCZOS)

    brand = text_layer([("KALA KARI CREATIONS", fonts.cinzel(600, 34), CREAM)], tracking=6)
    hook = text_layer([(cfg["hook"][0], fonts.cor_it(500, 104), CREAM),
                       (cfg["hook"][1], fonts.cor_it(500, 104), CREAM)], spacing=1.0)
    handmade = text_layer([("HANDCRAFTED  ·  MADE IN INDIA", fonts.cinzel(500, 30), GOLD)], tracking=3)
    captions = {s[5]: text_layer([(s[5], fonts.cor_it(600, 60), CREAM)])
                for s in cfg["shots"] if s[5] not in (None, "name")}
    name = text_layer([(cfg["name"][0].upper(), fonts.cinzel(600, 62), CREAM),
                       (cfg["name"][1].upper(), fonts.cinzel(600, 62), CREAM)], spacing=1.1)
    tagline = text_layer([(cfg["tagline"], fonts.cor_it(500, 58), GOLD)])
    top_shade = gradient(520, 150, 0)
    bottom_shade = gradient(1100, 0, 215)

    end = Image.new("RGBA", (W, H), MAROON + (255,))
    ed = ImageDraw.Draw(end)
    for inset, col in ((48, GOLD_DARK), (62, GOLD_DARK)):
        ed.rectangle((inset, inset, W - inset, H - inset), outline=col, width=2)
    end_logo_y = 380
    end_lines = [
        (text_layer([("DM us to order", fonts.cor_it(600, 80), CREAM)], shadow=False), 960),
        (text_layer([("CALL  /  WHATSAPP", fonts.cinzel(500, 30), GOLD)], shadow=False, tracking=4), 1110),
        (text_layer([("+91 94081 14592", fonts.cinzel(600, 84), CREAM)], shadow=False), 1160),
        (text_layer([("Video call appointments available", fonts.cor_it(500, 58), GOLD)], shadow=False), 1310),
        (text_layer([("SIZES  ·  CUSTOMISATION  ·  PAN-INDIA DELIVERY", fonts.cinzel(500, 28), GOLD)],
                    shadow=False, tracking=2), 1450),
    ]

    shots = cfg["shots"]
    starts, t = [], 0.0
    for s in shots:
        starts.append(t)
        t += s[0] - XFADE
    end_start = t
    total = end_start + END_CARD + XFADE

    def shot_frame(i, tt):
        dur, z0, z1, c0, c1, cap = shots[i]
        local = tt - starts[i]
        p = ease(local / dur) * 0.85 + (local / dur) * 0.15
        img = ken_burns(src, lerp(z0, z1, p), lerp(c0[0], c1[0], p), lerp(c0[1], c1[1], p)).convert("RGBA")
        img.alpha_composite(top_shade, (0, 0))
        img.alpha_composite(bottom_shade, (0, H - 1100))
        paste_anim(img, brand, 230, local, 0.2, dur)
        if i == 0:
            paste_anim(img, hook, 1150, local, 0.3, dur)
            paste_anim(img, handmade, 1420, local, 0.8, dur)
        elif cap == "name":
            paste_anim(img, name, 1180, local, 0.3, dur + 1)
            paste_anim(img, tagline, 1380, local, 0.9, dur + 1)
        else:
            paste_anim(img, captions[cap], 1360, local, 0.3, dur)
        return img

    def end_frame(tt):
        local = tt - end_start
        img = end.copy()
        a = ease(local / 0.8)
        s = lerp(0.92, 1.0, ease(local / 1.4))
        lg = logo.resize((int(logo.width * s), int(logo.height * s)), Image.BICUBIC)
        img.alpha_composite(with_alpha(lg, a), ((W - lg.width) // 2, end_logo_y + (logo.height - lg.height) // 2))
        for k, (layer, y) in enumerate(end_lines):
            paste_anim(img, layer, y, local, 0.4 + 0.3 * k, 99)
        return img

    def frame_at(tt):
        layers = []
        for i, s in enumerate(shots):
            if starts[i] <= tt < starts[i] + s[0]:
                layers.append((starts[i], lambda i=i: shot_frame(i, tt)))
        if tt >= end_start:
            layers.append((end_start, lambda: end_frame(tt)))
        if len(layers) == 1:
            return layers[0][1]()
        (sa, fa), (sb, fb) = layers[-2], layers[-1]
        return Image.blend(fa(), fb(), ease((tt - sb) / XFADE))

    n = int(round(total * FPS))
    wav = os.path.join(tempfile.mkdtemp(), "music.wav")
    music.write_track(wav, n / FPS, seed=seed)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav,
           "-shortest", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(n):
        proc.stdin.write(frame_at(f / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit(f"ffmpeg failed for {out_path}")
    print(f"{out_path}: {total:.1f}s, {n} frames")


def main():
    photos, fonts_dir, out = sys.argv[1:4]
    only = sys.argv[4:] or list(REELS)
    os.makedirs(out, exist_ok=True)
    fonts = Fonts(fonts_dir)
    for rid in only:
        build_reel(REELS[rid], photos, fonts, os.path.join(out, f"kalakari-reel-{rid}.mp4"),
                   seed=list(REELS).index(rid))


if __name__ == "__main__":
    main()
