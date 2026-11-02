#!/usr/bin/env python3
"""13.5 s 9:16 "art of precision stitching" reel: the reference trend reel's footage and audio, rebranded for
Kala Kari Creations.
- Frames 1-284: the sewing-studio cuts and black flashes, kept as they are.
- Frames 285-343: the folded white shirt. The collar label is replaced with a woven "KALA KARI" label, tracked
  with SIFT homographies and lit by the original label's shading. The pocket monogram is inpainted away.
- Frames 344-403: the dark textured end card. A cream Kala Kari medallion fades in like the original, a light
  glint sweeps across it, and the Diwali offer, website and phone number appear below it.

Usage:
    python3 stitching_brand_reel.py <fonts_dir> <ref.mp4> <out.mp4> [preview_dir f1,f2,...]
Needs opencv-python-headless.
"""
import math
import os
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-maroon-flat.png")
W, H = 1080, 1920
K = W / 720                                            # reference frames are 720x1280
SHIRT0, SHIRT1, END0 = 285, 343, 344                   # 1-based frame numbers
REF_FRAME = 300
LABEL_Q = np.float32([[264, 432], [387, 410], [393, 443], [270, 466]]) * K     # collar label in frame 300
MONO_BOX = (622, 828, 668, 870)                        # pocket monogram in frame 300 (720 px coordinates)
DISC_C, DISC_R = (359.5 * K, 591 * K), 214 * K         # original medallion, to be painted out
MED_C, MED_R = (540, 700), 270                         # new medallion
T_IN0, T_IN1 = 344, 360                                # medallion fade-in frames
T_GLINT = (374, 386)
T_TEXT0, T_TEXT1 = 354, 368
INK = (78, 46, 30)
CHAMPAGNE = (236, 214, 178)
GOLD = (218, 178, 112)


def fonts_of(d):
    cin = lambda w, s: ImageFont.truetype(os.path.join(d, "fontsource-cinzel", "package", "files",  # noqa: E731
                                                       f"cinzel-latin-{w}-normal.woff2"), s)
    cg = lambda w, s, st="normal": ImageFont.truetype(os.path.join(  # noqa: E731
        d, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-{st}.woff2"), s)
    return cin, cg


# ------------------------------------------------------------------ label for the shirt collar
def label_art(fonts):
    cin, cg = fonts
    lw, lh = 620, 170
    rng = np.random.default_rng(2)
    weave = (np.sin(np.arange(lw)[None, :] * 2.2) * 3 + np.sin(np.arange(lh)[:, None] * 2.6) * 3
             + rng.standard_normal((lh, lw)) * 2)
    base = np.array([226, 224, 218], np.float32)[None, None] + weave[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    # KK monogram from the logo's arch, then a divider and the name, like the original label's layout
    logo = Image.open(LOGO).convert("RGBA")
    mono = logo.crop((int(logo.width * .33), int(logo.height * .02), int(logo.width * .67), int(logo.height * .58)))
    mono = mono.resize((int(118 * mono.width / mono.height), 118), Image.LANCZOS)
    img.paste(mono, (40, (lh - 118) // 2), mono)
    x = 40 + mono.width + 22
    d.line((x, 40, x, lh - 40), fill=INK, width=3)
    d.text((x + 26, lh / 2 - 6), "KALA KARI", font=cin(600, 58), fill=INK, anchor="lm")
    d.text((x + 28, lh / 2 + 40), "CREATIONS", font=cin(500, 22), fill=INK, anchor="lm")
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def label_shading(frame, q):
    """Brightness field of the original label with its dark lettering closed away, relative to its median."""
    m = np.zeros(frame.shape[:2], np.uint8)
    cv2.fillPoly(m, [q.astype(np.int32)], 255)
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    g = cv2.dilate(g, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))      # remove dark letters
    g = cv2.GaussianBlur(g, (0, 0), 6)
    med = float(np.median(g[m > 0]))
    return np.clip(g / med, .55, 1.25)


def homographies(frames, idx_ref, idxs):
    sift = cv2.SIFT_create(5000)
    bf = cv2.BFMatcher()
    g0 = cv2.cvtColor(frames[idx_ref], cv2.COLOR_BGR2GRAY)
    k0, d0 = sift.detectAndCompute(g0, None)
    Hs = {}
    for i in idxs:
        if i == idx_ref:
            Hs[i] = np.eye(3)
            continue
        g = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        k1, d1 = sift.detectAndCompute(g, None)
        good = [a for a, b in bf.knnMatch(d0, d1, k=2) if a.distance < .7 * b.distance]
        p0 = np.float32([k0[m.queryIdx].pt for m in good])
        p1 = np.float32([k1[m.trainIdx].pt for m in good])
        H, _ = cv2.findHomography(p0, p1, cv2.RANSAC, 3.0)
        Hs[i] = H
    return Hs


def shirt_frame(frame, H, art):
    q = cv2.perspectiveTransform(LABEL_Q[None], H)[0]
    # pocket monogram: inpaint
    x0, y0, x1, y1 = [v * K for v in MONO_BOX]
    box = np.float32([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
    bq = cv2.perspectiveTransform(box[None], H)[0]
    mm = np.zeros(frame.shape[:2], np.uint8)
    cv2.fillPoly(mm, [bq.astype(np.int32)], 255)
    frame = cv2.inpaint(frame, mm, 9, cv2.INPAINT_TELEA)
    # label
    lh, lw = art.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [lw, 0], [lw, lh], [0, lh]]), q)
    warped = cv2.warpPerspective(art, M, (W, H_)).astype(np.float32)
    a = cv2.warpPerspective(np.full((lh, lw), 255, np.uint8), M, (W, H_)).astype(np.float32) / 255
    a = cv2.GaussianBlur(a, (3, 3), 0)
    shade = label_shading(frame, q)[..., None]
    lit = np.clip(warped * shade, 0, 255)
    lit = cv2.GaussianBlur(lit, (3, 3), 0)
    out = frame.astype(np.float32) * (1 - a[..., None]) + lit * a[..., None]
    return out.astype(np.uint8)


H_ = H


# ------------------------------------------------------------------ end card
def medallion(fonts):
    cin, cg = fonts
    S = 2
    R = MED_R * S
    D = 2 * R + 40 * S
    c = D / 2
    y, x = np.mgrid[0:D, 0:D].astype(np.float32)
    r = np.hypot(x - c, y - c)
    # champagne disc with a soft radial falloff and a slightly darker bevelled rim
    t = np.clip(r / R, 0, 1)
    tone = 1.05 - .16 * t ** 2 + .05 * ((x - y) / D)
    rim = np.clip((r - (R - 14 * S)) / (14 * S), 0, 1)
    tone = tone * (1 - .18 * rim)
    rgb = np.array(CHAMPAGNE[::-1], np.float32)[None, None] * tone[..., None]
    alpha = np.clip((R - r) / 1.5, 0, 1) * 255
    disc = np.dstack([np.clip(rgb, 0, 255), alpha]).astype(np.uint8)
    img = Image.fromarray(cv2.cvtColor(disc, cv2.COLOR_BGRA2RGBA))
    d = ImageDraw.Draw(img)
    d.ellipse((c - R + 26 * S, c - R + 26 * S, c + R - 26 * S, c + R - 26 * S), outline=INK + (200,), width=2 * S)
    logo = Image.open(LOGO).convert("RGBA")
    lw = int(R * 1.22)
    logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, (int(c - lw / 2), int(c - logo.height / 2 - 40 * S)))
    # tagline arced along the lower rim, as on the original medallion
    tag = "CRAFTED WITH TRADITION  ·  WORN WITH PRIDE"
    f = cin(600, 17 * S)
    rad = R - 46 * S
    widths = [d.textlength(ch, font=f) + 1.2 * S for ch in tag]
    total = sum(widths) / rad
    ang = math.pi / 2 + total / 2
    for ch, w_ in zip(tag, widths):
        a = ang - (w_ / 2) / rad
        cx, cy = c + rad * math.cos(a), c + rad * math.sin(a)
        g = Image.new("RGBA", (int(w_ * 3), int(f.size * 2.2)), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((g.width / 2, g.height / 2), ch, font=f, fill=INK + (255,), anchor="mm")
        g = g.rotate(-math.degrees(a - math.pi / 2), resample=Image.BICUBIC, expand=True)
        img.alpha_composite(g, (int(cx - g.width / 2), int(cy - g.height / 2)))
        ang -= w_ / rad
    return img.resize((D // S, D // S), Image.LANCZOS)


def offer_layer(fonts):
    cin, cg = fonts
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    y = 1050
    d.text((W / 2, y), "DIWALI DHAMAKA SALE", font=cin(600, 50), fill=CHAMPAGNE, anchor="ma")
    y += 84
    d.line((W / 2 - 230, y, W / 2 - 26, y), fill=GOLD, width=2)
    d.line((W / 2 + 26, y, W / 2 + 230, y), fill=GOLD, width=2)
    d.polygon([(W / 2, y - 10), (W / 2 + 10, y), (W / 2, y + 10), (W / 2 - 10, y)], outline=GOLD, width=2)
    y += 34
    d.text((W / 2, y), "FLAT 20% OFF", font=cin(700, 104), fill=GOLD, anchor="ma")
    y += 136
    d.text((W / 2, y), "on almost everything · till 9 November", font=cg(500, 44, "italic"), fill=CHAMPAGNE, anchor="ma")
    y += 108
    d.text((W / 2, y), "kalakaricreations.com", font=cg(600, 52), fill=CHAMPAGNE, anchor="ma")
    y += 74
    d.text((W / 2, y), "CALL / WHATSAPP  +91 94081 14592", font=cin(500, 30), fill=GOLD, anchor="ma")
    y += 56
    d.text((W / 2, y), "@kalakaricreations27", font=cg(500, 36, "italic"), fill=CHAMPAGNE, anchor="ma")
    return lay


def clean_background(frame):
    """The end card's dark backdrop with the original medallion removed. It is inpainted at low resolution,
    which suits the soft, dark background, then given back a little grain."""
    small = cv2.resize(frame, (W // 6, H // 6), interpolation=cv2.INTER_AREA)
    m = np.zeros(small.shape[:2], np.uint8)
    cv2.circle(m, (int(DISC_C[0] / 6), int(DISC_C[1] / 6)), int((DISC_R + 30) / 6), 255, -1)
    fill = cv2.inpaint(small, m, 12, cv2.INPAINT_TELEA)
    fill = cv2.GaussianBlur(cv2.resize(fill, (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), 8)
    rng = np.random.default_rng(1)
    fill = np.clip(fill.astype(np.float32) + rng.standard_normal((H, W, 1)) * 2.2, 0, 255).astype(np.uint8)
    big = np.zeros((H, W), np.float32)
    cv2.circle(big, (int(DISC_C[0]), int(DISC_C[1])), int(DISC_R + 30), 1.0, -1)
    big = cv2.GaussianBlur(big, (0, 0), 14)[..., None]
    return (frame.astype(np.float32) * (1 - big) + fill * big).astype(np.uint8)


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def end_frame(frame, clean_bg, f, med, offer):
    out = frame.copy()
    # paint out the original medallion with the clean background, matched to this frame's exposure
    mask = np.zeros(frame.shape[:2], np.float32)
    cv2.circle(mask, (int(DISC_C[0]), int(DISC_C[1])), int(DISC_R + 30), 1.0, -1)
    mask = cv2.GaussianBlur(mask, (0, 0), 6)[..., None]
    ring = np.zeros(frame.shape[:2], np.uint8)
    cv2.circle(ring, (int(DISC_C[0]), int(DISC_C[1])), int(DISC_R + 70), 255, 30)
    gain = (frame[ring > 0].mean(0) + 1) / (clean_bg[ring > 0].mean(0) + 1)
    bg = np.clip(clean_bg.astype(np.float32) * gain, 0, 255)
    out = (out.astype(np.float32) * (1 - mask) + bg * mask).astype(np.uint8)
    img = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).convert("RGBA")
    a = ease((f - T_IN0) / (T_IN1 - T_IN0))
    if a > 0:
        m = med.copy()
        # soft contact shadow under the medallion
        sh = Image.new("RGBA", m.size, (0, 0, 0, 0))
        sh.putalpha(m.getchannel("A").point(lambda v: int(v * .55 * a)))
        sh = Image.fromarray(cv2.GaussianBlur(np.asarray(sh), (0, 0), 14))
        x0, y0 = MED_C[0] - m.width // 2, MED_C[1] - m.height // 2
        img.alpha_composite(sh, (x0 + 10, y0 + 18))
        if T_GLINT[0] <= f <= T_GLINT[1]:                    # diagonal light glint sweeps across
            p = (f - T_GLINT[0]) / (T_GLINT[1] - T_GLINT[0])
            yy, xx = np.mgrid[0:m.height, 0:m.width].astype(np.float32)
            band = np.exp(-(((xx + yy) / (m.width + m.height) - (p * 1.4 - .2)) / .05) ** 2)
            arr = np.asarray(m).astype(np.float32)
            arr[..., :3] = np.clip(arr[..., :3] + band[..., None] * 70, 0, 255)
            m = Image.fromarray(arr.astype(np.uint8))
        m.putalpha(m.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(m, (x0, y0))
    b = ease((f - T_TEXT0) / (T_TEXT1 - T_TEXT0))
    if b > 0:
        o = offer.copy()
        o.putalpha(o.getchannel("A").point(lambda v: int(v * b)))
        img.alpha_composite(o, (0, int(16 * (1 - b))))
    return cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)


def main():
    fdir, ref, out = sys.argv[1:4]
    preview = sys.argv[4:6]
    fonts = fonts_of(fdir)
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, "-vf", f"scale={W}:{H}:flags=lanczos",
                    os.path.join(tmp, "%04d.png")], check=True)
    names = sorted(os.listdir(tmp))
    frames = {i + 1: cv2.imread(os.path.join(tmp, n)) for i, n in enumerate(names) if SHIRT0 <= i + 1 or i + 1 == REF_FRAME}
    Hs = homographies(frames, REF_FRAME, range(SHIRT0, SHIRT1 + 1))
    art = label_art(fonts)
    clean = clean_background(frames[END0 + 56])
    med = medallion(fonts)
    offer = offer_layer(fonts)

    def render(f):
        fr = frames[f]
        if SHIRT0 <= f <= SHIRT1:
            return shirt_frame(fr, Hs[f], art)
        if f >= END0:
            return end_frame(fr, clean, f, med, offer)
        return fr
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            cv2.imwrite(os.path.join(d, f"sb_{f:03d}.png"), cv2.resize(render(f), (360, 640)))
        return
    for i, n in enumerate(names):
        f = i + 1
        if f >= SHIRT0:
            cv2.imwrite(os.path.join(tmp, n), render(f))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", os.path.join(tmp, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    print(out)


if __name__ == "__main__":
    main()
