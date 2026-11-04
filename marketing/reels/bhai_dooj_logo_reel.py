#!/usr/bin/env python3
"""16.6 s 9:16 Bhai Dooj greeting reel: the reference trend reel's animation and audio, kept as they are. The
only change is the brand: the "Bunaai" wordmark becomes the Kala Kari Creations logo.

The wordmark slides in from the top twice, once with the greeting paragraph and once with "Happy Bhai Dooj".
It is found in every frame by multi-scale template matching against a crop from frame 150, and smoothed over
time. Entry frames above the top edge are extrapolated from the motion, and its fades are followed. The wordmark is inpainted out, and the
cream Kala Kari horizontal logo is placed at the same centre, moving and scaling with it.

Usage:
    python3 bhai_dooj_logo_reel.py <ref.mp4> <out.mp4> [preview_dir f1,f2,...]
Needs opencv-python-headless.
"""
import os
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-gold-flat.png")
CREAM = (250, 236, 220)
TPL_FRAME, TPL_BOX = 150, (298, 84, 424, 136)          # wordmark crop in frame 150, 720x1280 coordinates
SEGMENTS = [(100, 221), (368, 495)]                    # frames where the wordmark is on screen (1-based)
SCALES = np.arange(.94, 1.22, .02)
LOGO_W = 175                                           # new logo width at scale 1, in 720 px
UP = 1.5                                               # render at 1080x1920


def track(frames):
    g = {f: cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32) for f, im in frames.items()}
    x0, y0, x1, y1 = TPL_BOX
    tpl = g[TPL_FRAME][y0:y1, x0:x1]
    raw = {}
    for a, b in SEGMENTS:
        for f in range(a, b + 1):
            best = (-1, None, None)
            for s in SCALES:
                t = cv2.resize(tpl, None, fx=s, fy=s)
                r = cv2.matchTemplate(g[f][:520], t, cv2.TM_CCOEFF_NORMED)
                _, mx, _, loc = cv2.minMaxLoc(r)
                if mx > best[0]:
                    best = (mx, loc, s)
            mx, (lx, ly), s = best
            cx, cy = lx + tpl.shape[1] * s / 2, ly + tpl.shape[0] * s / 2
            raw[f] = (mx, cx, cy, s)
    out = {}
    for a, b in SEGMENTS:
        fs = [f for f in range(a, b + 1) if raw[f][0] > .6]
        good = np.array([[f, raw[f][1], raw[f][2], raw[f][3]] for f in fs])
        # smooth centre and scale with a small moving average over the reliable frames
        sm = good.copy()
        for i in range(len(good)):
            lo, hi = max(0, i - 2), min(len(good), i + 3)
            sm[i, 1:] = good[lo:hi, 1:].mean(0)
        first, last = int(sm[0, 0]), int(sm[-1, 0])
        vy = (sm[min(5, len(sm) - 1), 2] - sm[0, 2]) / max(1, sm[min(5, len(sm) - 1), 0] - sm[0, 0])
        for f in range(a, b + 1):
            if f < first:                              # still sliding in from above: extrapolate
                cx, cy, s = sm[0, 1], sm[0, 2] - vy * (first - f), sm[0, 3]
            elif f > last:
                continue                               # gone (the exit is a cut)
            else:
                cx, cy, s = [np.interp(f, sm[:, 0], sm[:, k]) for k in (1, 2, 3)]
            out[f] = (cx, cy, s)
    return out


def logo_img():
    im = Image.open(LOGO).convert("RGBA")
    im = im.crop(im.getbbox())
    c = Image.new("RGBA", im.size, CREAM + (0,))
    c.putalpha(im.getchannel("A"))
    return c


def replace(frame_up, cx, cy, s, logo):
    """Inpaint the wordmark box and paste the Kala Kari logo at the same centre (1080-scale frame)."""
    x0, y0, x1, y1 = TPL_BOX
    w, h = (x1 - x0) * s * UP, (y1 - y0) * s * UP
    X, Y = cx * UP, cy * UP
    mask = np.zeros(frame_up.shape[:2], np.uint8)
    cv2.rectangle(mask, (int(X - w / 2 - 8), int(Y - h / 2 - 8)), (int(X + w / 2 + 8), int(Y + h / 2 + 6)), 255, -1)
    # follow the wordmark's own fades: its contrast against the background, relative to full strength (66)
    v = cv2.cvtColor(frame_up, cv2.COLOR_BGR2HSV)[..., 2][mask > 0].astype(np.float32)
    alpha = float(np.clip((np.percentile(v, 99) - np.median(v)) / 62, 0, 1)) if v.size else 0.0
    if mask.any():
        frame_up = cv2.inpaint(frame_up, mask, 7, cv2.INPAINT_TELEA)
    lw = int(LOGO_W * s * UP)
    lg = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    img = Image.fromarray(cv2.cvtColor(frame_up, cv2.COLOR_BGR2RGB)).convert("RGBA")
    lg.putalpha(lg.getchannel("A").point(lambda a: int(a * alpha)))
    img.alpha_composite(lg, (int(X - lg.width / 2), int(Y - lg.height / 2)))
    return cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)


def main():
    ref, out = sys.argv[1:3]
    preview = sys.argv[3:5]
    raw_dir, up_dir = tempfile.mkdtemp(), tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(raw_dir, "%04d.png")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, "-vf", "scale=1080:1920:flags=lanczos",
                    os.path.join(up_dir, "%04d.png")], check=True)
    need = {TPL_FRAME} | {f for a, b in SEGMENTS for f in range(a, b + 1)}
    frames = {f: cv2.imread(os.path.join(raw_dir, f"{f:04d}.png")) for f in need}
    pos = track(frames)
    logo = logo_img()
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            im = cv2.imread(os.path.join(up_dir, f"{f:04d}.png"))
            if f in pos:
                im = replace(im, *pos[f], logo)
            cv2.imwrite(os.path.join(d, f"bd_{f:03d}.png"), cv2.resize(im, (360, 640)))
        return
    for f, p in pos.items():
        path = os.path.join(up_dir, f"{f:04d}.png")
        cv2.imwrite(path, replace(cv2.imread(path), *p, logo))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", os.path.join(up_dir, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    print(out)


if __name__ == "__main__":
    main()
