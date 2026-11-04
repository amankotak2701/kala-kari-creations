#!/usr/bin/env python3
"""29.6 s 9:16 "one map stitched from fabric" reel: the reference trend reel's footage and audio, kept as they
are, ending on a Kala Kari Creations card.

The reference zooms out to the whole fabric map of India, fades to cream and then cuts to black. Here the
cream fade becomes the brand card instead: the Kala Kari logo, "Handcrafted across India", the crafts we
carry, the Diwali offer, the website and the phone number.

Usage:
    python3 fabric_map_reel.py <fonts_dir> <ref.mp4> <out.mp4> [preview_dir f1,f2,...]
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-maroon-flat.png")
W, H = 1080, 1920
CREAM = (239, 229, 214)                  # the reference's paper colour at the fade
MAROON = (110, 32, 40)
BROWN = (96, 70, 52)
X0, X1 = 684, 700                        # cross-fade from the zoomed-out map into the card (1-based frames)


def card(fonts):
    cin = lambda w, s: ImageFont.truetype(os.path.join(fonts, "fontsource-cinzel", "package", "files",  # noqa: E731
                                                       f"cinzel-latin-{w}-normal.woff2"), s)
    cg = lambda w, s, st="normal": ImageFont.truetype(os.path.join(  # noqa: E731
        fonts, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-{st}.woff2"), s)
    rng = np.random.default_rng(4)
    paper = np.array(CREAM, np.float32)[None, None] + rng.standard_normal((H, W, 1)) * 2.2
    img = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((560, int(560 * logo.height / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, ((W - logo.width) // 2, 330))
    y = 330 + logo.height + 80
    d.text((W / 2, y), "Handcrafted across India", font=cg(600, 64, "italic"), fill=MAROON, anchor="ma")
    y += 100
    for line in ("CHIKANKARI · AJRAKH · BAGRU · SANGANERI", "CHANDERI · KALAMKARI · BANDHANI · DABU"):
        d.text((W / 2, y), line, font=cin(500, 30), fill=BROWN, anchor="ma")
        y += 50
    y += 50
    d.line((W / 2 - 220, y, W / 2 + 220, y), fill=MAROON, width=2)
    y += 44
    d.text((W / 2, y), "Diwali Sale · Flat 20% off on almost everything", font=cg(600, 44), fill=MAROON, anchor="ma")
    y += 58
    d.text((W / 2, y), "till 9 November", font=cg(500, 38, "italic"), fill=BROWN, anchor="ma")
    y += 100
    d.text((W / 2, y), "kalakaricreations.com", font=cg(600, 54), fill=MAROON, anchor="ma")
    y += 76
    d.text((W / 2, y), "CALL / WHATSAPP  +91 94081 14592", font=cin(500, 30), fill=BROWN, anchor="ma")
    return img


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def compose(frame, f, crd):
    if f < X0:
        return frame
    a = ease((f - X0) / (X1 - X0))
    out = frame.convert("RGBA").copy()
    c = crd.copy()
    c.putalpha(int(255 * a))
    out.alpha_composite(c)
    return out.convert("RGB")


def main():
    fonts, ref, out = sys.argv[1:4]
    preview = sys.argv[4:6]
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, "-vf", f"scale={W}:{H}:flags=lanczos",
                    os.path.join(tmp, "%04d.png")], check=True)
    names = sorted(os.listdir(tmp))
    crd = card(fonts)
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            im = compose(Image.open(os.path.join(tmp, names[f - 1])).convert("RGB"), f, crd)
            im.resize((360, 640)).save(os.path.join(d, f"fm_{f:03d}.png"))
        return
    for i, n in enumerate(names):
        f = i + 1
        if f >= X0:
            p = os.path.join(tmp, n)
            compose(Image.open(p).convert("RGB"), f, crd).save(p)
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                          "-of", "csv=p=0", ref], capture_output=True, text=True).stdout.strip()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", fps, "-i", os.path.join(tmp, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    print(out)


if __name__ == "__main__":
    main()
