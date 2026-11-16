#!/usr/bin/env python3
"""10.7 s 9:16 "Move your thumb to the beat" reel, built on the reference trend reel. The reference audio is kept.

The reference has three parts:
1. Frames 1-104: a black card with a line-art thumb tapping, "MOVE YOUR THUMB to the beat" and a subline.
2. Frames 105-274: a left-to-right wipe opens one warm, softly lit room. Twelve times, on the beat, the furniture
   changes while the room stays the same.
3. Frames 275-320: a hard cut to a hero room, which zooms in slowly.

Our version:
1. The reference intro is kept, with the subline changed to "For the love of handcrafted ethnicwear".
2. One fixed beige plaster room with a lit arch, like the reference room. The look inside the arch changes on
   every beat (12 looks), and a small name label sits under the arch.
3. A full-frame hero look with the same slow zoom. The brand name and website sign off at the end.

Usage:
    python3 move_your_thumb_reel.py <ref.mp4> <out.mp4> <photo1> ... <photo13> [--preview dir f1,f2,...]
Photo 13 is the hero. The labels are in LABELS, in the same order as the photos.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
UP = 1.5
FONTS = os.environ.get("KK_FONTS", "/tmp/claude-0/-home-user-kala-kari-creations/"
                       "b594b16c-4df2-59b6-99e4-9ab0ec789fa6/scratchpad/fonts")
LABELS = ["Denim Button-Front Midi Dress", "Pink Jaipuri Floral Short Top", "Coffee Brown Pintuck Tunic",
          "Off-White & Black Lotus Tunic", "Denim Balloon Sleeve Top", "Maroon Mirror Work Tunic",
          "Kutchi Patchwork Long Shrug", "Olive Smocked Cotton Tunic", "Rich Red Chanderi Shirt",
          "Off-White & Brown Applique Tunic", "Kutchi Hand-Block Print Shirt", "Light Grey Chambray Midi Dress",
          "Denim Paisley Co-ord Set"]
SUBLINE = "For the love of handcrafted ethnicwear"
SUB_BOX = (140, 390, 524, 436)               # the reference subline, 720-px frame
SUB_CENTER = (330, 412)
# where the wipe's edge is, per frame (720-px frame): the room shows left of it, the black card right of it
WIPE = {105: 19, 106: 59, 107: 125, 108: 227, 109: 364, 110: 503, 111: 603, 112: 670, 113: 710}
# the frames where the reference changes the furniture (each change is a 3-frame dissolve)
CHANGES = [123, 137, 151, 165, 179, 193, 206, 221, 233, 247, 261]
HERO = 275
# the arch in the room (1080-px frame)
AX0, AX1, ATOP, ABOT = 170, 910, 300, 1540
FOCUS = {6: 0.12}                  # vertical crop anchor for tall photos (index, 0 = top)
INK = (92, 62, 44)


def font(fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(FONTS, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def cover(im, w, h, fy=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def arch_mask(pad=0):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    r = (AX1 - AX0) / 2 + pad
    cx = (AX0 + AX1) / 2
    d.ellipse((cx - r, ATOP - pad, cx + r, ATOP - pad + 2 * r), fill=255)
    d.rectangle((cx - r, ATOP - pad + r, cx + r, ABOT + pad), fill=255)
    return m


def room():
    """The fixed room: plaster wall with a cove light at the top, warm wall-washer glow, a floor, an arch."""
    rng = np.random.default_rng(7)
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(-1, 1, W)[None, :]
    base = np.array([214, 191, 160], float)
    light = 1.0 + 0.16 * np.exp(-((y - 0.06) / 0.10) ** 2) - 0.10 * x ** 2 - 0.06 * y
    img = base[None, None, :] * light[..., None]
    # plaster: soft blotches and fine grain
    blot = rng.normal(0, 1, (H // 40, W // 40)).astype(np.float32)
    blot = np.asarray(Image.fromarray(blot).resize((W, H), Image.BICUBIC))
    img *= (1 + 0.025 * blot)[..., None]
    img += rng.normal(0, 2.2, (H, W, 1))
    # ceiling and its cove line
    img[:70] = img[:70] * 0.93
    glow = np.exp(-((y * H - 74) / 26) ** 2)
    img += (glow * 60)[..., None] * np.array([1.0, 0.85, 0.6])
    # floor
    fl = 1690
    fy = np.clip((y * H - fl) / (H - fl), 0, 1)
    floor = np.array([201, 182, 156], float)[None, None, :] * (1.04 - 0.12 * fy - 0.06 * x ** 2)[..., None]
    floor += rng.normal(0, 1.8, (H, W, 1))
    img = np.where((y * H >= fl)[..., None], floor, img)
    img[fl - 3:fl + 2] *= 0.86
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    # the arch: a recess with a warm LED rim
    outer = arch_mask(14)
    sh = Image.new("RGB", (W, H), (120, 96, 72))
    soft = outer.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.35))
    im = Image.composite(sh, im, soft)
    rim = arch_mask(16)
    inner = arch_mask(2)
    ring = Image.fromarray(np.clip(np.asarray(rim, int) - np.asarray(inner, int), 0, 255).astype(np.uint8))
    halo = ring.filter(ImageFilter.GaussianBlur(14)).point(lambda v: min(255, int(v * 2.2)))
    im = Image.composite(Image.new("RGB", (W, H), (255, 214, 150)), im, halo)
    im = Image.composite(Image.new("RGB", (W, H), (255, 236, 196)), im, ring.filter(ImageFilter.GaussianBlur(2)))
    # floor glow and a soft shadow under the arch
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse((AX0 - 60, fl - 30, AX1 + 60, fl + 90), fill=110)
    im = Image.composite(Image.new("RGB", (W, H), (236, 214, 178)), im, g.filter(ImageFilter.GaussianBlur(40)))
    return im


def look_in_arch(photo, k):
    w, h = AX1 - AX0, ABOT - ATOP
    im = cover(Image.open(photo).convert("RGB"), w, h, FOCUS.get(k, 0.4))
    # a little inner shadow at the top of the recess so the photo sits inside the wall
    a = np.asarray(im, float)
    yy = np.arange(h)[:, None, None]
    a *= 1 - 0.18 * np.exp(-yy / 60)
    layer = Image.new("RGB", (W, H))
    layer.paste(Image.fromarray(a.clip(0, 255).astype(np.uint8)), (AX0, ATOP))
    return layer


def label_layer(text):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = font("cormorant-garamond", 600, 46, "italic")
    d.text((W / 2, 1618), text, font=f, fill=INK + (255,), anchor="mm")
    d.line((W / 2 - 40, 1660, W / 2 + 40, 1660), fill=INK + (150,), width=2)
    return lay


def main():
    args = sys.argv[1:]
    preview = None
    if "--preview" in args:
        k = args.index("--preview")
        preview, args = args[k + 1:k + 3], args[:k]
    ref, out, photos = args[0], args[1], args[2:15]
    raw = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(raw, "%04d.png")], check=True)
    nframes = len(os.listdir(raw))

    base = room()
    mask = arch_mask()
    scenes = []
    for k in range(12):
        sc = Image.composite(look_in_arch(photos[k], k), base, mask).convert("RGBA")
        sc.alpha_composite(label_layer(LABELS[k]))
        scenes.append(sc.convert("RGB"))
    hero = cover(Image.open(photos[12]).convert("RGB"), W, H, 0.3)

    sub_f = font("jost", 500, int(25 * UP))
    brand_f = font("cinzel", 600, 58)
    web_f = font("jost", 500, 40)
    name_f = font("cormorant-garamond", 600, 50, "italic")

    def intro(n):
        """Reference intro frame at 1080 px with their subline replaced."""
        im = Image.open(os.path.join(raw, f"{n:04d}.png")).convert("RGB").resize((W, H), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = [v * UP for v in SUB_BOX]
        d.rectangle((x0, y0, x1, y1), fill=(7, 5, 10))
        d.text((SUB_CENTER[0] * UP, SUB_CENTER[1] * UP), SUBLINE, font=sub_f, fill=(236, 236, 236), anchor="mm")
        return im

    def look(n):
        k = 0
        for i, c in enumerate(CHANGES):
            if n >= c:
                k = i + 1
        im = scenes[k]
        c = CHANGES[k - 1] if k else None
        if c is not None and n < c + 2:          # 3-frame dissolve, as in the reference
            t = (n - c + 1) / 3
            im = Image.blend(scenes[k - 1], scenes[k], t)
        return im

    def finale(n):
        t = (n - HERO) / max(1, nframes - HERO)
        s = 1.0 + 0.07 * t
        w, h = int(W * s), int(H * s)
        im = hero.resize((w, h), Image.LANCZOS).crop(((w - W) // 2, int((h - H) * 0.35),
                                                       (w - W) // 2 + W, int((h - H) * 0.35) + H))
        im = im.convert("RGBA")
        a = min(1.0, (n - HERO - 6) / 10) if n > HERO + 6 else 0.0
        if a > 0:
            # a soft cream band at the bottom (over the floor, never across the outfit) for the sign-off
            band = np.zeros((H, W), np.float32)
            yy = np.arange(H)[:, None]
            band[:] = np.clip((yy - 1480) / 200, 0, 1) * 0.86
            lay = Image.new("RGBA", (W, H), (246, 238, 226, 0))
            lay.putalpha(Image.fromarray((band * 255 * a).astype(np.uint8)))
            im.alpha_composite(lay)
            tl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(tl)
            al = int(255 * a)
            d.text((W / 2, 1700), LABELS[12], font=name_f, fill=INK + (al,), anchor="mm")
            d.text((W / 2, 1782), "KALA KARI CREATIONS", font=brand_f, fill=(70, 44, 30, al), anchor="mm")
            d.text((W / 2, 1852), "Shop now: kalakaricreations.com", font=web_f, fill=INK + (al,), anchor="mm")
            im.alpha_composite(tl, (0, int(16 * (1 - a))))
        return im.convert("RGB")

    def render(n):
        if n < min(WIPE):
            return intro(n)
        if n in WIPE:
            e = int(WIPE[n] * UP)
            im = intro(n)
            sc = look(n)
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).rectangle((0, 0, e, H), fill=255)
            return Image.composite(sc, im, m.filter(ImageFilter.GaussianBlur(3)))
        if n < HERO:
            return look(n)
        return finale(n)

    if preview:
        d, fs = preview
        for n in map(int, fs.split(",")):
            render(n).resize((540, 960), Image.LANCZOS).save(os.path.join(d, f"mt_{n:03d}.png"))
        shutil.rmtree(raw, ignore_errors=True)
        return
    up = tempfile.mkdtemp()
    for n in range(1, nframes + 1):
        render(n).save(os.path.join(up, f"{n:04d}.png"), compress_level=1)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", os.path.join(up, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    shutil.rmtree(raw, ignore_errors=True)
    shutil.rmtree(up, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
