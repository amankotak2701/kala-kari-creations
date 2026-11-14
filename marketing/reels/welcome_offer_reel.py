#!/usr/bin/env python3
"""15 s 9:16 "WELCOME10 is coming" reel, built on the reference trend reel: a maroon velvet panel in an Indian
miniature-art frame. In it, an auto-rickshaw drives through, gold text cards and looks slide in from the right
and out to the left, and a postage-stamp card zooms in with the dates. The reference audio is kept.

What changes:
- The other brand's round badge (top left) becomes a Kala Kari badge.
- Their content inside the panel is replaced with a clean panel plus our own: the text cards, five New Arrivals
  as cut-out figures (background removed with rembg), and our stamp text.
  - Their content is found per frame as pixels that differ from a clean frame (frame 5) after an exposure gain.
    Those pixels take the clean frame's value, so the swaying border art stays alive.
- The rickshaw intro (unbranded) and the stamp's zoom-in are kept as they are.

Usage:
    python3 welcome_offer_reel.py <ref.mp4> <out.mp4> <photo1> ... <photo5> [--preview dir f1,f2,...]
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

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-gold-flat.png")
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
RUPEE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"     # Liberation has no ₹ glyph
UP = 1.5
W, H = 1080, 1920
GOLD_TXT = (250, 196, 30)
SHADOW = (34, 82, 7)
STAMP_INK = (120, 69, 73)
BADGE = (79.5, 83.5, 49)                      # centre x, y and radius (with its ring), 720-px frame
# (first frame, last frame, kind, payload); frames are 1-based and taken from the reference's own cuts
SEGMENTS = [(43, 100, "text", ["WELCOME", "SPECIAL", "OFFER"]),
            (101, 129, "photo", 0), (130, 160, "photo", 1), (161, 190, "photo", 2),
            (191, 219, "photo", 3), (220, 249, "photo", 4),
            (250, 284, "text", ["10% OFF", "on your", "first order"]),
            (285, 315, "text", ["Use code", "WELCOME10"]),
            (316, 348, "text", ["On orders", "above", "₹999"])]
STAMP_FROM = 357                              # the stamp has reached its size; its text fades in after this
STAMP_LINES = ["Starting", "15th November"]
STAMP_BOX = (150, 498, 580, 782)              # stamp interior to clear (720-px frame)


def ease_out(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def ease_in(t):
    t = min(1.0, max(0.0, t))
    return t ** 3


def offset_x(f, a, b):
    """The reference's motion: rush in from the right, drift slowly left while held, rush out to the left."""
    n = b - a
    if f - a < 7:
        return 620 * (1 - ease_out((f - a) / 7)) + 40
    if b - f < 8:
        return 40 - 80 * (n - 15) / n - 760 * ease_in((f - (b - 8)) / 8)
    return 40 - 80 * (f - a - 7) / n


def text_card(lines):
    """Gold serif lines with the reference's green drop shadow, on a transparent 720x1280 layer."""
    lay = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(SERIF_B, 96)
    f_small = ImageFont.truetype(SERIF_B, 70)
    f_code = ImageFont.truetype(SERIF_B, 82)
    f_rupee = ImageFont.truetype(RUPEE, 96)
    pitch = 150 if len(lines) == 2 else 188
    y0 = 640 - pitch * (len(lines) - 1) / 2
    for i, s in enumerate(lines):
        ff = f_small if s.islower() or s.startswith("on ") or s == "above" else f
        if s == "WELCOME10":
            ff = f_code
        if "₹" in s:
            ff = f_rupee
        y = y0 + i * pitch
        d.text((360 + 6, y + 8), s, font=ff, fill=SHADOW + (255,), anchor="mm")
        d.text((360, y), s, font=ff, fill=GOLD_TXT + (255,), anchor="mm")
    return lay


def photo_card(path):
    """The look as a cut-out figure standing on the velvet, like the reference's illustrated figures.
    Uses the background-removed PNG in a cutouts/ folder next to the photo when there is one."""
    cut = os.path.join(os.path.dirname(path), "cutouts", os.path.splitext(os.path.basename(path))[0] + ".png")
    im = Image.open(cut if os.path.exists(cut) else path).convert("RGBA")
    h = 740
    im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    lay = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
    lay.alpha_composite(im, (360 - im.width // 2, 1010 - h))
    return lay


def badge():
    """Black round badge with a light ring and the gold Kala Kari logo, like the reference's corner badge."""
    S = 4
    R = int(BADGE[2] * UP * S)
    img = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=(214, 172, 96, 255))
    d.ellipse((5 * S, 5 * S, 2 * R - 5 * S, 2 * R - 5 * S), fill=(10, 8, 8, 255))
    d.ellipse((10 * S, 10 * S, 2 * R - 10 * S, 2 * R - 10 * S), outline=(240, 232, 220, 255), width=2 * S)
    lg = Image.open(LOGO).convert("RGBA")
    lw = int(R * 1.35)
    lg = lg.resize((lw, int(lw * lg.height / lg.width)), Image.LANCZOS)
    img.alpha_composite(lg, (R - lg.width // 2, R - lg.height // 2))
    return img.resize((2 * R // S, 2 * R // S), Image.LANCZOS)


def main():
    args = sys.argv[1:]
    preview = None
    if "--preview" in args:
        k = args.index("--preview")
        preview, args = args[k + 1:k + 3], args[:k]
    ref, out, photos = args[0], args[1], args[2:7]
    raw = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(raw, "%04d.png")], check=True)
    names = sorted(os.listdir(raw))
    frames = [cv2.imread(os.path.join(raw, n)).astype(np.float32) for n in names]
    # clean plate: per-pixel median of the in-between frames (each has a different element just entering or
    # leaving at an edge, so the median is the empty panel)
    clean = np.median(np.stack([frames[k - 1] for k in (5, 100, 130, 160, 190, 220, 250, 285, 316)]), 0)
    border = np.ones(clean.shape[:2], bool)
    border[150:1150, 90:630] = False
    border[0:200, 0:200] = False
    gain = [float(np.median(f[border]) / (np.median(clean[border]) + 1e-6)) for f in frames]

    # stamp text opacity: dark ink inside the stamp, relative to its final amount
    x0, y0, x1, y1 = STAMP_BOX
    ink = np.array([((f[y0:y1, x0:x1].max(2) < 190) & (f[y0:y1, x0:x1][..., 2] > 50)).sum() for f in frames], float)
    ink_full = np.percentile(ink[400:440], 50)
    stamp_a = np.clip(ink / max(ink_full, 1), 0, 1)
    blank = frames[STAMP_FROM - 1][y0:y1, x0:x1].copy()

    layers = {}
    for i, (a, b, kind, payload) in enumerate(SEGMENTS):
        layers[i] = text_card(payload) if kind == "text" else photo_card(photos[payload])
    bdg = badge()
    stamp_f = ImageFont.truetype(SERIF, int(50 * UP))

    def render(n):
        f = frames[n - 1].copy()
        g = gain[n - 1]
        if 43 <= n <= 348:                      # remove their content: pixels far from the (re-exposed) clean frame
            diff = np.abs(f - clean * g).mean(2)
            m = (diff > 34).astype(np.uint8)
            m = cv2.dilate(m, np.ones((7, 7), np.uint8))
            m[150:1150, 90:630] = 1             # the velvet panel itself is static: always take it clean
            mf = cv2.GaussianBlur(m.astype(np.float32), (9, 9), 0)[..., None]
            f = f * (1 - mf) + clean * g * mf
        if n >= STAMP_FROM:                     # clear their stamp text
            f[y0:y1, x0:x1] = blank * g
        # their badge out (copy the background ring around it inward), ours in
        img = cv2.resize(np.clip(f, 0, 255).astype(np.uint8), (W, H), interpolation=cv2.INTER_LANCZOS4)
        cx, cy, r = [v * UP for v in BADGE]
        mk = np.zeros(img.shape[:2], np.uint8)
        cv2.circle(mk, (int(cx), int(cy)), int(r + 4), 255, -1)
        img = cv2.inpaint(img, mk, 7, cv2.INPAINT_TELEA)
        pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert("RGBA")
        b = bdg.copy()
        b.putalpha(b.getchannel("A").point(lambda v: int(v * min(1.0, g))))
        pil.alpha_composite(b, (int(cx - b.width / 2), int(cy - b.height / 2)))
        for i, (a, bb, kind, payload) in enumerate(SEGMENTS):
            if a <= n <= bb:
                lay = layers[i]
                dx = offset_x(n, a, bb)
                big = lay.resize((W, H), Image.LANCZOS) if (i, "big") not in layers else layers[(i, "big")]
                layers[(i, "big")] = big
                pil.alpha_composite(big, (int(dx * UP), 0))
        if n >= STAMP_FROM and stamp_a[n - 1] > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            al = int(255 * stamp_a[n - 1] * min(1.0, g))
            d.text((W / 2, 588 * UP), STAMP_LINES[0], font=stamp_f, fill=STAMP_INK + (al,), anchor="mm")
            d.text((W / 2, 668 * UP), STAMP_LINES[1], font=stamp_f, fill=STAMP_INK + (al,), anchor="mm")
            pil.alpha_composite(lay)
        return cv2.cvtColor(np.asarray(pil.convert("RGB")), cv2.COLOR_RGB2BGR)

    if preview:
        d, fs = preview
        for n in map(int, fs.split(",")):
            cv2.imwrite(os.path.join(d, f"wo_{n:03d}.png"), cv2.resize(render(n), (360, 640)))
        shutil.rmtree(raw, ignore_errors=True)
        return
    up = tempfile.mkdtemp()
    for n in range(1, len(frames) + 1):
        cv2.imwrite(os.path.join(up, f"{n:04d}.png"), render(n))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", os.path.join(up, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    shutil.rmtree(raw, ignore_errors=True)
    shutil.rmtree(up, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
