#!/usr/bin/env python3
"""Swap a moving wordmark in a reference reel for the Kala Kari Creations logo, keeping the footage and audio.

This is the general version of bhai_dooj_logo_reel.py:
- The wordmark is cropped from one frame (the template).
- It is found in every frame by multi-scale template matching.
- The frames where it is on screen are detected automatically (match score above a threshold).
- Position and scale are smoothed, and short entries above the frame edge are extrapolated.
- The wordmark is inpainted out, and the cream Kala Kari horizontal logo is placed at the same centre. The
  logo follows the wordmark's fades, using its contrast against the background.

Usage:
    python3 logo_swap_reel.py <ref.mp4> <out.mp4> <tpl_frame> <x0,y0,x1,y1> [preview_dir f1,f2,...]
Box coordinates are in the reference's own pixels (1-based frame number). Needs opencv-python-headless.
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
SCALES = np.arange(.9, 1.24, .02)
THRESH = .6
LEAD = int(os.environ.get("LOGO_LEAD", 4))      # frames before a run to also treat (fade/slide-ins)


def track(gray, tpl, search_h):
    raw = {}
    for f, g in gray.items():
        best = (-1, None, None)
        for s in SCALES:
            t = cv2.resize(tpl, None, fx=s, fy=s)
            r = cv2.matchTemplate(g[:search_h], t, cv2.TM_CCOEFF_NORMED)
            _, mx, _, loc = cv2.minMaxLoc(r)
            if mx > best[0]:
                best = (mx, loc, s)
        mx, (lx, ly), s = best
        raw[f] = (mx, lx + tpl.shape[1] * s / 2, ly + tpl.shape[0] * s / 2, s)
    # runs of frames above the threshold, allowing 2-frame dropouts
    on = sorted(f for f, v in raw.items() if v[0] > THRESH)
    runs, cur = [], [on[0]]
    for f in on[1:]:
        if f - cur[-1] <= 3:
            cur.append(f)
        else:
            runs.append(cur)
            cur = [f]
    runs.append(cur)
    out = {}
    for run in runs:
        if len(run) < 6:
            continue
        good = np.array([[f, raw[f][1], raw[f][2], raw[f][3]] for f in run])
        sm = good.copy()
        for i in range(len(good)):
            lo, hi = max(0, i - 2), min(len(good), i + 3)
            sm[i, 1:] = good[lo:hi, 1:].mean(0)
        k = min(5, len(sm) - 1)
        vy = (sm[k, 2] - sm[0, 2]) / max(1, sm[k, 0] - sm[0, 0])
        first = int(sm[0, 0])
        for f in range(first - LEAD, int(sm[-1, 0]) + 1):  # lead-in frames: it may be sliding or fading in
            if f < 1:
                continue
            if f < first:
                out[f] = (sm[0, 1], sm[0, 2] - vy * (first - f), sm[0, 3])
            else:
                out[f] = tuple(np.interp(f, sm[:, 0], sm[:, j]) for j in (1, 2, 3))
    return out


def logo_img():
    im = Image.open(LOGO).convert("RGBA")
    im = im.crop(im.getbbox())
    c = Image.new("RGBA", im.size, CREAM + (0,))
    c.putalpha(im.getchannel("A"))
    return c


def replace(frame_up, up, box, cx, cy, s, logo, full_contrast):
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) * s * up, (y1 - y0) * s * up
    X, Y = cx * up, cy * up
    mask = np.zeros(frame_up.shape[:2], np.uint8)
    cv2.rectangle(mask, (int(X - w / 2 - 8), int(Y - h / 2 - 8)), (int(X + w / 2 + 8), int(Y + h / 2 + 6)), 255, -1)
    v = cv2.cvtColor(frame_up, cv2.COLOR_BGR2HSV)[..., 2][mask > 0].astype(np.float32)
    alpha = float(np.clip((np.percentile(v, 99) - np.median(v)) / full_contrast, 0, 1)) if v.size else 0.0
    if mask.any():
        frame_up = cv2.inpaint(frame_up, mask, 7, cv2.INPAINT_TELEA)
    lw = int((x1 - x0) * 1.45 * s * up)                  # the horizontal logo reads best a little wider
    lg = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    lg.putalpha(lg.getchannel("A").point(lambda a: int(a * alpha)))
    img = Image.fromarray(cv2.cvtColor(frame_up, cv2.COLOR_BGR2RGB)).convert("RGBA")
    img.alpha_composite(lg, (int(X - lg.width / 2), int(Y - lg.height / 2)))
    return cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)


def main():
    ref, out, tpl_frame, box = sys.argv[1:5]
    tpl_frame = int(tpl_frame)
    box = tuple(int(v) for v in box.split(","))
    preview = sys.argv[5:7]
    raw_dir, up_dir = tempfile.mkdtemp(), tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(raw_dir, "%04d.png")], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, "-vf", "scale=1080:1920:flags=lanczos",
                    os.path.join(up_dir, "%04d.png")], check=True)
    names = sorted(os.listdir(raw_dir))
    gray = {i + 1: cv2.cvtColor(cv2.imread(os.path.join(raw_dir, n)), cv2.COLOR_BGR2GRAY).astype(np.float32)
            for i, n in enumerate(names)}
    rh, rw = next(iter(gray.values())).shape
    up = 1080 / rw
    x0, y0, x1, y1 = box
    tpl = gray[tpl_frame][y0:y1, x0:x1]
    pos = track(gray, tpl, min(rh, int(y1 * 2.5) + 200))
    tf = cv2.imread(os.path.join(up_dir, names[tpl_frame - 1]))
    hsv = cv2.cvtColor(tf, cv2.COLOR_BGR2HSV)[..., 2][int(y0 * up):int(y1 * up), int(x0 * up):int(x1 * up)]
    full = max(20.0, float(np.percentile(hsv, 99) - np.median(hsv)))
    logo = logo_img()
    print("wordmark frames:", min(pos), "-", max(pos), f"({len(pos)} frames)")
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            im = cv2.imread(os.path.join(up_dir, names[f - 1]))
            if f in pos:
                im = replace(im, up, box, *pos[f], logo, full)
            cv2.imwrite(os.path.join(d, f"ls_{f:03d}.png"), im)
        return
    for f, p in pos.items():
        path = os.path.join(up_dir, names[f - 1])
        cv2.imwrite(path, replace(cv2.imread(path), up, box, *p, logo, full))
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                          "-of", "csv=p=0", ref], capture_output=True, text=True).stdout.strip()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", fps, "-i", os.path.join(up_dir, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    print(out)


if __name__ == "__main__":
    main()
