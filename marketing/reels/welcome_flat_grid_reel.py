#!/usr/bin/env python3
"""9.2 s 9:16 "FLAT 10% OFF" welcome-offer reel, built on the reference trend reel. The reference audio is kept.

The reference: on cream textured paper, 12 full-length outfit figures pop in one per beat to fill a 4 x 3 grid.
Then pink typewriter letters replace the figures one per beat to spell FLAT / 20% / OFF. Two figures are left:
one beside "20%" and one beside "OFF".

Ours: the same paper, grid and beats with our 12 looks (backgrounds removed with rembg). It spells
FLAT / 10% / OFF, then the WELCOME10 details and the brand sign-off appear on the beat in the same type.

Usage:
    python3 welcome_flat_grid_reel.py <ref.mp4> <out.mp4> <cutout1.png> ... <cutout12.png> [--preview dir f1,f2]
Cut-outs go in reading order. Numbers 8 and 9 stay on screen at the end.
"""
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
UP = 1.5
FONTS = os.environ.get("KK_FONTS", "/tmp/claude-0/-home-user-kala-kari-creations/"
                       "b594b16c-4df2-59b6-99e4-9ab0ec789fa6/scratchpad/fonts")
TYPE = os.path.join(FONTS, "fontsource-special-elite", "package", "files", "special-elite-latin-400-normal.woff2")
RUPEE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"      # Special Elite has no ₹ glyph
PINK = (235, 138, 140)
ROSE = (176, 84, 92)
# grid (720-px frame): column and row centres, figure height
CX = [189, 304, 428, 553]
CY = [328, 636, 948]
FIG_H = 250
# the frames where each figure pops in, and where each letter replaces a figure (from the reference)
FIG_AT = [9, 16, 24, 31, 39, 46, 54, 61, 69, 76, 84, 91]
LETTERS = [(0, "F", 99), (1, "L", 106), (2, "A", 114), (3, "T", 121), (4, "1", 129), (5, "0", 136), (6, "%", 144),
           (9, "O", 151), (10, "F", 159), (11, "F", 166)]
# sign-off lines: (frame, text, y in 720-px frame, size, colour)
LINES = [(174, "WELCOME OFFER", 168, 40, ROSE),
         (182, "on your first order above ₹999", 1105, 30, ROSE),
         (190, "Use code: WELCOME10", 1158, 38, PINK),
         (198, "KALA KARI CREATIONS  ·  kalakaricreations.com", 1222, 24, ROSE)]


def text_mixed(d, xy, s, size, fill):
    """Centred text in the typewriter face, with ₹ drawn from DejaVu."""
    f = ImageFont.truetype(TYPE, size)
    fr = ImageFont.truetype(RUPEE, int(size * 0.9))
    parts = [(ch, fr if ch == "₹" else f) for ch in s]
    widths = [d.textlength(ch, font=ff) for ch, ff in parts]
    x = xy[0] - sum(widths) / 2
    for (ch, ff), w in zip(parts, widths):
        d.text((x, xy[1]), ch, font=ff, fill=fill, anchor="lm")
        x += w


def main():
    args = sys.argv[1:]
    preview = None
    if "--preview" in args:
        k = args.index("--preview")
        preview, args = args[k + 1:k + 3], args[:k]
    ref, out, cuts = args[0], args[1], args[2:14]
    raw = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(raw, "%04d.png")], check=True)
    nframes = len(os.listdir(raw))
    paper = Image.open(os.path.join(raw, "0001.png")).convert("RGB").resize((W, H), Image.LANCZOS)

    figs = []
    for i, p in enumerate(cuts):
        im = Image.open(p).convert("RGBA")
        h = int(FIG_H * UP)
        im = im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
        a = im.getchannel("A").point(lambda v: 0 if v < 30 else v).filter(ImageFilter.GaussianBlur(0.6))
        im.putalpha(a)
        figs.append(im)

    def cell(i):
        return CX[i % 4] * UP, CY[i // 4] * UP

    letter_f = ImageFont.truetype(TYPE, int(120 * UP))

    def render(n):
        im = paper.copy().convert("RGBA")
        replaced = {c: ch for c, ch, at in LETTERS if n >= at}
        for i, at in enumerate(FIG_AT):
            if n >= at and i not in replaced:
                x, y = cell(i)
                f = figs[i]
                im.alpha_composite(f, (int(x - f.width / 2), int(y - f.height / 2)))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for i, ch in replaced.items():
            x, y = cell(i)
            d.text((x, y), ch, font=letter_f, fill=PINK + (255,), anchor="mm")
        for at, s, y, size, col in LINES:
            if n >= at:
                text_mixed(d, (W / 2, y * UP), s, int(size * UP), col + (255,))
        # a slight ink-bleed softness like the reference's printed letters
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.7)))
        return im.convert("RGB")

    if preview:
        d, fs = preview
        for n in map(int, fs.split(",")):
            render(n).resize((540, 960), Image.LANCZOS).save(os.path.join(d, f"wg_{n:03d}.png"))
        shutil.rmtree(raw, ignore_errors=True)
        return
    up = tempfile.mkdtemp()
    for n in range(1, nframes + 1):
        render(n).save(os.path.join(up, f"{n:04d}.png"), compress_level=1)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "25", "-i", os.path.join(up, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    shutil.rmtree(raw, ignore_errors=True)
    shutil.rmtree(up, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
