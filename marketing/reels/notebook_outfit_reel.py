#!/usr/bin/env python3
"""6.1 s 9:16 "PUT THAT PHONE DOWN AND GO FIND YOUR WEDDING LOOK!!!" reel, built on the reference trend reel:
a model holds an open spiral notebook while the outfit behind it changes every 3 frames, and pink words type
onto the pages.

- The notebook never moves, so its pixels are found as the static part of the reference: a low temporal
  standard deviation, and bright.
- A clean (text-free) notebook is taken from frame 1.
- Behind it, the 9 product photos play in the reference's exact per-frame order: 9 outfits on a 30-frame loop.
- The words are re-typed with "WEDDING" in place of "DIWALI".
  - The reveal follows the reference's character count per frame (one connected pink blob per character).
  - The end fade follows the reference's text opacity.
- Reference audio.

Usage:
    python3 notebook_outfit_reel.py <ref.mp4> <out.mp4> <photo1> ... <photo9> [--preview dir f1,f2,...]
Needs opencv-python-headless.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
PINK = (249, 4, 99)                                     # RGB, measured from the reference text
ORIG_CHARS = 42                                        # "...DIWALI LOOK!!!" letters, excluding spaces
ANGLE = 36                                             # text rises to the right at this angle (degrees)
XSCALE = .85                                           # the reference lettering is narrower than Liberation Bold
# per line: (word, baseline-left x, y, font size) in 720x1280 reference pixels, measured from the reference
LINES = [("PUT", 65, 642, 69), ("THAT", 94, 721, 69), ("PHONE", 118, 803, 69), ("DOWN", 175, 864, 69),
         ("AND", 241, 917, 69), ("GO", 402, 420, 60), ("FIND", 418, 493, 60), ("YOUR", 449, 556, 60),
         ("WEDDING", 471, 626, 60), ("LOOK!!!", 508, 687, 60)]
REP_FRAMES = [4, 8, 11, 14, 17, 20, 23, 26, 29]        # one frame per outfit in the first loop


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = (r.width - w) // 2
    y = int(min(max(r.height * .02, 0), r.height - h))    # keep the head near the top, like the reference
    return r.crop((x, y, x + w, y + h))


def text_layer(n_chars, scale):
    """The two pages' words with the first n_chars letters shown, on a transparent full frame."""
    W, H = int(720 * scale), int(1280 * scale)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    left = n_chars
    th = np.radians(ANGLE)
    ca, sa = np.cos(th), np.sin(th)
    for word, ax, ay, size in LINES:
        if left <= 0:
            break
        shown = word[:left]
        left -= len(word)
        f = ImageFont.truetype(FONT, int(size * scale))
        pad = 10
        tw = int(f.getlength(word)) + 2 * pad
        can = Image.new("RGBA", (tw, int(size * scale * 1.4)), (0, 0, 0, 0))
        base = can.height * .8
        ImageDraw.Draw(can).text((pad, base), shown, font=f, fill=PINK + (255,), anchor="ls")
        can = can.resize((max(1, int(can.width * XSCALE)), can.height), Image.LANCZOS)
        rot = can.rotate(ANGLE, resample=Image.BICUBIC, expand=True)
        # where the canvas's baseline-left point lands after rotating about the canvas centre
        cx, cy = pad * XSCALE - can.width / 2, base - can.height / 2
        rx, ry = cx * ca + cy * sa + rot.width / 2, -cx * sa + cy * ca + rot.height / 2
        lay.alpha_composite(rot, (int(ax * scale - rx), int(ay * scale - ry)))
    return lay


def analyse(ref_frames):
    st = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in ref_frames]).astype(np.float32)
    sd, mean = st.std(0), st.mean(0)
    nb = ((sd < 6) & (mean > 170)).astype(np.uint8) * 255
    nb = cv2.morphologyEx(nb, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))    # bridges the spiral
    nb = cv2.morphologyEx(nb, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(nb)
    big = 1 + int(np.argmax(stats[1:, 4]))
    mask = (lab == big).astype(np.float32)
    # fill the notebook's holes (spiral rings, text) so the whole sheet is replaced together
    cs, _ = cv2.findContours((mask * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    full = np.zeros_like(mask)
    cv2.drawContours(full, cs, -1, 1.0, -1)
    full = cv2.erode(full, np.ones((3, 3), np.uint8))        # undo the closing's outward bulge at the edges
    full = cv2.GaussianBlur(full, (5, 5), 0)
    # per-frame character count and text opacity, counted on the notebook only (pink outfits behind it don't count)
    inner = cv2.erode((full > .5).astype(np.uint8), np.ones((9, 9), np.uint8))
    counts, opac = [], []
    final = None
    for f in ref_frames:
        hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        m = ((hsv[..., 0] > 150) & (hsv[..., 1] > 120) & (hsv[..., 2] > 150) & (inner > 0)).astype(np.uint8)
        k, _, s, _ = cv2.connectedComponentsWithStats(m)
        counts.append(int((s[1:, 4] > 40).sum()))
    peak = int(np.argmax(counts))
    hsv = cv2.cvtColor(ref_frames[peak], cv2.COLOR_BGR2HSV)
    final = (hsv[..., 0] > 150) & (hsv[..., 1] > 120) & (hsv[..., 2] > 150) & (inner > 0)
    g_peak = ref_frames[peak][..., 1][final].mean()
    for f in ref_frames:
        g = f[..., 1][final].mean()
        opac.append(float(np.clip((255 - g) / (255 - g_peak), 0, 1)))
    counts = np.maximum.accumulate(np.array(counts))
    opac = np.array(opac)
    opac[:peak] = 1.0
    sched = []
    small = [cv2.resize(ref_frames[r - 1], (36, 64)).astype(float) for r in REP_FRAMES]
    keep = cv2.resize(1 - full, (36, 64)) > .5
    for f in ref_frames:
        a = cv2.resize(f, (36, 64)).astype(float)
        sched.append(int(np.argmin([np.abs(a - r)[keep].mean() for r in small])))
    return full, counts, opac, sched


def main():
    args = sys.argv[1:]
    preview = None
    if "--preview" in args:
        i = args.index("--preview")
        preview = args[i + 1:i + 3]
        args = args[:i]
    ref, out, photos = args[0], args[1], args[2:11]
    assert len(photos) == 9, "need 9 product photos"
    raw = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(raw, "%04d.png")], check=True)
    names = sorted(os.listdir(raw))
    ref_frames = [cv2.imread(os.path.join(raw, n)) for n in names]
    mask, counts, opac, sched = analyse(ref_frames)
    S = 1.5
    W, H = int(720 * S), int(1280 * S)
    mask_up = cv2.resize(mask, (W, H))[..., None]
    clean = cv2.resize(ref_frames[0], (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    patch = (slice(650, 700), slice(300, 360))
    base_level = ref_frames[0][patch].mean()
    bgs = [cv2.cvtColor(np.asarray(cover(Image.open(p).convert("RGB"), W, H)), cv2.COLOR_RGB2BGR).astype(np.float32)
           for p in photos]
    total = sum(len(w) for w, *_ in LINES)
    layers = {}

    def render(i):
        gain = ref_frames[i][patch].mean() / base_level            # follow any global fade in the reference
        frame = bgs[sched[i]] * (1 - mask_up) + clean * gain * mask_up
        n = int(round(counts[i] * total / ORIG_CHARS))
        img = Image.fromarray(cv2.cvtColor(np.clip(frame, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)).convert("RGBA")
        if n > 0 and opac[i] > 0:
            if n not in layers:
                layers[n] = text_layer(n, S)
            t = layers[n].copy()
            t.putalpha(t.getchannel("A").point(lambda v: int(v * opac[i])))
            img.alpha_composite(t)
        return cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            cv2.imwrite(os.path.join(d, f"nb_{f:03d}.png"), render(f - 1))
        shutil.rmtree(raw, ignore_errors=True)
        return
    up = tempfile.mkdtemp()
    for i in range(len(ref_frames)):
        cv2.imwrite(os.path.join(up, f"{i + 1:04d}.png"), render(i))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", os.path.join(up, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    shutil.rmtree(raw, ignore_errors=True)
    shutil.rmtree(up, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
