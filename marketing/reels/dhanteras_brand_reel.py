#!/usr/bin/env python3
"""10.1 s 9:16 "Something golden is coming" Dhanteras greeting reel: the reference footage and audio, kept as
they are (the temple corridor, the gold kalash under falling coins, the glowing "Happy Dhanteras" mandala).
The reference carries no brand, so Kala Kari signs it: once "Happy Dhanteras" is on screen, a soft dark band
rises at the bottom with the gold Kala Kari logo and the website, and holds to the end.

Usage:
    python3 dhanteras_brand_reel.py <fonts_dir> <ref.mp4> <out.mp4> [preview_dir f1,f2,...]
"""
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-gold-flat.png")
W, H = 1080, 1920
T0, T1 = 168, 188                       # fade in (1-based frames, 24 fps); holds to the end
GOLD = (236, 200, 128)


def overlay(fonts):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = np.clip((np.arange(H) - 1430) / 330, 0, 1) ** 1.2 * 190
    band = np.zeros((H, W, 4), np.uint8)
    band[..., 0:3] = (24, 12, 6)
    band[..., 3] = g[:, None].astype(np.uint8)
    lay.alpha_composite(Image.fromarray(band))
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    logo = logo.resize((560, int(560 * logo.height / logo.width)), Image.LANCZOS)
    lay.alpha_composite(logo, ((W - logo.width) // 2, 1640))
    cg = ImageFont.truetype(os.path.join(fonts, "fontsource-cormorant-garamond", "package", "files",
                                         "cormorant-garamond-latin-600-italic.woff2"), 40)
    d = ImageDraw.Draw(lay)
    d.text((W / 2, 1640 + logo.height + 30), "kalakaricreations.com", font=cg, fill=GOLD, anchor="ma")
    return lay


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def compose(path, f, ov):
    if f < T0:
        return
    a = ease((f - T0) / (T1 - T0))
    img = Image.open(path).convert("RGBA")
    o = ov.copy()
    o.putalpha(o.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(o, (0, int(30 * (1 - a))))
    img.convert("RGB").save(path)


def main():
    fonts, ref, out = sys.argv[1:4]
    preview = sys.argv[4:6]
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, "-vf", f"scale={W}:{H}:flags=lanczos",
                    os.path.join(tmp, "%04d.png")], check=True)
    names = sorted(os.listdir(tmp))
    ov = overlay(fonts)
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            p = os.path.join(tmp, names[f - 1])
            compose(p, f, ov)
            Image.open(p).resize((360, 640)).save(os.path.join(d, f"dh_{f:03d}.png"))
        return
    for i, n in enumerate(names):
        compose(os.path.join(tmp, n), i + 1, ov)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "24", "-i", os.path.join(tmp, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
