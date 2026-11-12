#!/usr/bin/env python3
"""12.9 s 9:16 "double click the block with your favourite look" reel, built on the reference trend reel's
footage and audio.

The reference footage is a stone-tile floor with flowers and the model's feet. Eight look photos pop onto the
tiles in a 2x4 grid one by one, flicker, fade, and then the brand logo appears.

- Each cell's on-screen opacity is measured per frame: the correlation of the cell with its fully shown
  version (frame 130), normalised between that cell's empty and full values.
- The reference's photo is replaced by ours; during fades ours blends over a clean floor frame.
- The brand logo is inpainted out of the floor, frame by frame, and the Kala Kari logo fades in and out on
  the same curve.

Usage:
    python3 tile_grid_reel.py <ref.mp4> <out.mp4> <photo1> ... <photo8> [--preview dir f1,f2,...]
Photos go row by row (left, right). Needs opencv-python-headless.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-gold-flat.png")
UP = 1.5
FULL = 130                                            # frame with all eight looks fully shown
COLS = [(186, 362), (372, 545)]
ROWS = [(75, 242), (247, 410), (415, 582), (587, 758)]
CELLS = [(x0, y0, x1, y1) for (y0, y1) in ROWS for (x0, x1) in COLS]
LOGO_BOX = (180, 440, 560, 580)                       # reference wordmark region (720-px frame)
LOGO_CLEAN = 262                                      # last frame before the wordmark fades in
CREAM = (250, 238, 222)


def square_photo(path, w, h):
    """Full-length look fitted to the cell's height, with the sides filled by a blurred copy of the photo."""
    im = Image.open(path).convert("RGB")
    im = im.crop((0, 0, im.width, int(im.height * .92)))   # drop the generator's corner badge
    s = h / im.height
    fg = im.resize((max(1, int(im.width * s)), h), Image.LANCZOS)
    bg = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    bg = bg.crop((0, (bg.height - h) // 2, w, (bg.height - h) // 2 + h)).filter(ImageFilter.GaussianBlur(14))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (236, 226, 212)), .25)
    bg.paste(fg, ((w - fg.width) // 2, 0))
    return np.asarray(bg).astype(np.float32)[..., ::-1]


def main():
    args = sys.argv[1:]
    preview = None
    if "--preview" in args:
        k = args.index("--preview")
        preview, args = args[k + 1:k + 3], args[:k]
    ref, out, photos = args[0], args[1], args[2:10]
    assert len(photos) == 8, "need 8 photos"
    raw = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(raw, "%04d.png")], check=True)
    names = sorted(os.listdir(raw))
    frames = [cv2.imread(os.path.join(raw, n)) for n in names]
    gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in frames]

    # per-frame opacity of each cell
    alpha = np.zeros((len(frames), 8), np.float32)
    for c, (x0, y0, x1, y1) in enumerate(CELLS):
        t = gray[FULL - 1][y0 + 8:y1 - 8, x0 + 8:x1 - 8]
        t = t - t.mean()
        cc = []
        for g in gray:
            s = g[y0 + 8:y1 - 8, x0 + 8:x1 - 8]
            s = s - s.mean()
            cc.append((s * t).mean() / (s.std() * t.std() + 1e-6))
        cc = np.array(cc)
        empty, full = cc[0], np.percentile(cc, 99)
        alpha[:, c] = np.clip((cc - empty - .06) / (full - empty - .06), 0, 1)

    # wordmark: mask from its fully visible frame, presence per frame
    lx0, ly0, lx1, ly1 = LOGO_BOX
    base = gray[14][ly0:ly1, lx0:lx1]                      # early frame: no looks, no wordmark
    pres = np.array([np.percentile(g[ly0:ly1, lx0:lx1] - base, 99.5) for g in gray])
    peak = int(np.argmax(pres))
    lm = ((gray[peak][ly0:ly1, lx0:lx1] - base) > 40).astype(np.uint8) * 255
    lm = cv2.dilate(lm, np.ones((5, 5), np.uint8))
    logo_mask = np.zeros(gray[0].shape, np.uint8)
    logo_mask[ly0:ly1, lx0:lx1] = lm
    la = np.clip((pres - 30) / (pres[peak] - 30), 0, 1)
    la[:LOGO_CLEAN - 1] = 0

    W, H = int(720 * UP), int(1280 * UP)
    their = cv2.resize(frames[FULL - 1], (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    # clean floor under the grid: an early frame, before any look or the logo appears
    clean = cv2.resize(frames[14], (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    ours = []
    for (x0, y0, x1, y1), p in zip(CELLS, photos):
        ours.append(square_photo(p, int((x1 - x0) * UP), int((y1 - y0) * UP)))
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    cream = Image.new("RGBA", logo.size, CREAM + (0,))
    cream.putalpha(logo.getchannel("A"))
    lw = int(380 * UP)
    cream = cream.resize((lw, int(lw * cream.height / cream.width)), Image.LANCZOS)
    cl = np.asarray(cream).astype(np.float32)
    cx, cy = int((lx0 + lx1) / 2 * UP), int((ly0 + ly1) / 2 * UP)

    def render(i):
        f = frames[i]
        if i >= LOGO_CLEAN - 20:                          # wordmark can start faintly; inpainting bare floor is harmless
            f = cv2.inpaint(f, logo_mask, 5, cv2.INPAINT_TELEA)
        img = cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        for c, (x0, y0, x1, y1) in enumerate(CELLS):
            a = alpha[i, c]
            if a <= 0:
                continue
            X0, Y0 = int(x0 * UP), int(y0 * UP)
            h, w = ours[c].shape[:2]
            if a > .97:
                img[Y0:Y0 + h, X0:X0 + w] = ours[c]
            else:                                         # fades: blend over the clean floor, no ghosting
                img[Y0:Y0 + h, X0:X0 + w] = clean[Y0:Y0 + h, X0:X0 + w] * (1 - a) + ours[c] * a
        if la[i] > 0:
            h, w = cl.shape[:2]
            X0, Y0 = cx - w // 2, cy - h // 2
            a = cl[..., 3:4] / 255 * la[i]
            img[Y0:Y0 + h, X0:X0 + w] = img[Y0:Y0 + h, X0:X0 + w] * (1 - a) + cl[..., 2::-1] * a
        return np.clip(img, 0, 255).astype(np.uint8)

    if preview:
        d, fs = preview
        for n in map(int, fs.split(",")):
            cv2.imwrite(os.path.join(d, f"tg_{n:03d}.png"), cv2.resize(render(n - 1), (360, 640)))
        shutil.rmtree(raw, ignore_errors=True)
        return
    up = tempfile.mkdtemp()
    for i in range(len(frames)):
        cv2.imwrite(os.path.join(up, f"{i + 1:04d}.png"), render(i))
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                          "-of", "csv=p=0", ref], capture_output=True, text=True).stdout.strip()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", fps, "-i", os.path.join(up, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    shutil.rmtree(raw, ignore_errors=True)
    shutil.rmtree(up, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
