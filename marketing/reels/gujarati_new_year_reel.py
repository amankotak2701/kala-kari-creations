#!/usr/bin/env python3
"""6.7 s 9:16 "Nutan Varshabhinandan" Gujarati New Year greeting reel: the reference trend reel's animation,
title, message and audio, kept as they are. The sender's details are rewritten for Kala Kari Creations:
- the header firm name;
- the signature line;
- the phone line.

The original lines are inpainted out of every frame. The new lines are typed in left to right at the same
pace as the originals: each line's reveal progress is measured from the reference (rightmost revealed ink
against the line's final extent).

Usage:
    python3 gujarati_new_year_reel.py <fonts_dir> <ref.mp4> <out.mp4> [preview_dir f1,f2,...]
Needs opencv-python-headless.
"""
import os
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UP = 1.5                                               # reference is 720x1280; render at 1080x1920
PURPLE = (111, 32, 89)
# line boxes in reference pixels, the text to type there, font (family, weight) and size in 720 px
LINES = {
    "hdr": ((90, 428, 625, 460), "KALA KARI CREATIONS", ("jost", 700), 31),
    "name": ((110, 963, 610, 1001), "Team Kala Kari Creations", ("poppins", 500), 23),
    "call": ((240, 1003, 480, 1027), "Call / WhatsApp: 9408114592", ("poppins", 400), 13.5),
}


def font(fonts, fam, w, size):
    return ImageFont.truetype(os.path.join(fonts, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-normal.woff2"), int(size))


def ink(im, box):
    x0, y0, x1, y1 = box
    hsv = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
    return (hsv[..., 0] > 120) & (hsv[..., 0] < 175) & (hsv[..., 1] > 45) & (hsv[..., 2] < 210)


def measure(raw):
    """Per-line reveal progress (0-1) for every frame, from the reference's own typing."""
    last = raw[-1]
    prog = {}
    for k, (box, *_ ) in LINES.items():
        fin = ink(last, box)
        cols = np.where(fin.any(0))[0]
        a, b = cols.min(), cols.max()
        p = []
        for im in raw:
            xs = np.where((ink(im, box) & fin).any(0))[0]
            p.append(0.0 if len(xs) == 0 else (xs.max() - a) / max(1, b - a))
        prog[k] = np.maximum.accumulate(np.array(p))   # typing never goes backwards
    return prog


def text_mask(last):
    # clear each line's whole box: the small lines are antialiased and too light to key cleanly
    m = np.zeros(last.shape[:2], np.uint8)
    for box, *_ in LINES.values():
        x0, y0, x1, y1 = box
        m[y0 - 2:y1 + 2, x0 - 4:x1 + 4] = 255
    return cv2.resize(m, None, fx=UP, fy=UP, interpolation=cv2.INTER_NEAREST)


def line_layers(fonts, shape):
    layers = {}
    for k, (box, text, (fam, w), size) in LINES.items():
        x0, y0, x1, y1 = [v * UP for v in box]
        f = font(fonts, fam, w, size * UP)
        lay = Image.new("RGBA", (shape[1], shape[0]), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        d.text((cx, cy), text, font=f, fill=PURPLE, anchor="mm")
        bb = lay.getbbox()
        layers[k] = (lay, bb[0], bb[2])
    return layers


def frame_out(up, mask, layers, prog, i):
    clean = cv2.inpaint(up, mask, 6, cv2.INPAINT_TELEA)
    img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)).convert("RGBA")
    for k, (lay, a, b) in layers.items():
        p = float(prog[k][i])
        if p <= 0:
            continue
        x = int(a + (b - a) * p) + 2
        part = lay.crop((0, 0, x, lay.height))
        img.alpha_composite(part, (0, 0))
    return cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)


def main():
    fonts, ref, out = sys.argv[1:4]
    preview = sys.argv[4:6]
    raw_dir, up_dir = tempfile.mkdtemp(), tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(raw_dir, "%04d.png")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, "-vf", "scale=1080:1920:flags=lanczos",
                    os.path.join(up_dir, "%04d.png")], check=True)
    names = sorted(os.listdir(raw_dir))
    raw = [cv2.imread(os.path.join(raw_dir, n)) for n in names]
    prog = measure(raw)
    # the small phone line is too faint to measure reliably early on; it types alongside the header, faster
    prog["call"] = np.minimum(1, np.maximum(prog["call"], prog["hdr"] * 1.6))
    mask = text_mask(raw[-1])
    layers = line_layers(fonts, (1920, 1080))
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            up = cv2.imread(os.path.join(up_dir, names[f - 1]))
            cv2.imwrite(os.path.join(d, f"gn_{f:03d}.png"), frame_out(up, mask, layers, prog, f - 1))
        return
    for i, n in enumerate(names):
        p = os.path.join(up_dir, n)
        cv2.imwrite(p, frame_out(cv2.imread(p), mask, layers, prog, i))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", os.path.join(up_dir, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    print(out)


if __name__ == "__main__":
    main()
