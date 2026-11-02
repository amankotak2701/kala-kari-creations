#!/usr/bin/env python3
"""10.1 s 9:16 billboard-reveal reel: the reference trend reel's footage, where a helicopter lifts the cloth off a
city billboard, with the billboard's poster replaced by a Kala Kari Creations Diwali offer poster. The original
audio is kept.

How it works:
- The poster quad is tracked through every frame. It is detected on the last frame (the maroon panel), then
  carried backwards with SIFT homographies inside a region around the board.
- Revealed frames are snapped to the detected maroon panel.
- The new poster is warped into the quad. It shows only where the original frame shows poster: saturated
  maroon/gold, not the white cloth, the helicopter or the cable.
- It is lit by the original poster's blurred shading, so the cloth shadows and sun falloff carry over.

Usage:
    python3 billboard_reveal_reel.py <fonts_dir> <ref.mp4> <out.mp4> [preview_dir f1,f2,...]
Needs opencv-python-headless.
"""
import os
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-gold-flat.png")
PW, PH = 1020, 1500                                  # poster artwork size
MAROON = (86, 30, 34)
GOLD = (214, 172, 104)
CREAM = (244, 226, 196)


# ------------------------------------------------------------------ poster artwork
def poster(fonts):
    cinzel = lambda w, s: ImageFont.truetype(os.path.join(fonts, "fontsource-cinzel", "package", "files",  # noqa: E731
                                                          f"cinzel-latin-{w}-normal.woff2"), s)
    cg = lambda w, s, st="normal": ImageFont.truetype(os.path.join(  # noqa: E731
        fonts, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-{st}.woff2"), s)
    rng = np.random.default_rng(3)
    base = np.array(MAROON, np.float32)[None, None] * (1 + rng.standard_normal((PH, PW, 1)) * .015)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    # thin double gold frame
    d.rectangle((34, 34, PW - 35, PH - 35), outline=GOLD, width=3)
    d.rectangle((48, 48, PW - 49, PH - 49), outline=GOLD, width=1)

    # gold line-art vines up both sides, drawn in place of the reference's florals
    def vine(x0, flip):
        pts = []
        for i in range(120):
            t = i / 119
            y = 1340 - t * 1040
            x = x0 + flip * (26 * np.sin(t * 7.5))
            pts.append((x, y))
        d.line(pts, fill=GOLD, width=3)
        for i in range(8, 120, 9):
            x, y = pts[i]
            side = 1 if (i // 9) % 2 else -1
            for k, (ln, ang) in enumerate(((46, .9), (34, .5))):
                a = ang * side * flip
                ex, ey = x + side * flip * ln * np.cos(a), y - ln * np.sin(abs(a)) - 10
                d.line((x, y, ex, ey), fill=GOLD, width=2)
                d.ellipse((ex - 9, ey - 5, ex + 9, ey + 5), outline=GOLD, width=2)
    vine(110, 1)
    vine(PW - 110, -1)
    # logo
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((440, int(440 * logo.height / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, ((PW - logo.width) // 2, 110))
    y = 110 + logo.height + 60
    d.text((PW / 2, y), "DIWALI DHAMAKA SALE", font=cinzel(600, 54), fill=CREAM, anchor="ma")
    y += 96
    d.line((PW / 2 - 260, y, PW / 2 - 30, y), fill=GOLD, width=2)
    d.line((PW / 2 + 30, y, PW / 2 + 260, y), fill=GOLD, width=2)
    d.polygon([(PW / 2, y - 12), (PW / 2 + 12, y), (PW / 2, y + 12), (PW / 2 - 12, y)], outline=GOLD, width=2)
    y += 40
    d.text((PW / 2, y), "FLAT", font=cinzel(500, 66), fill=GOLD, anchor="ma")
    y += 78
    d.text((PW / 2, y), "20% OFF", font=cinzel(700, 168), fill=GOLD, anchor="ma")
    y += 200
    d.text((PW / 2, y), "on almost everything · till 9 November", font=cg(500, 42, "italic"), fill=CREAM, anchor="ma")
    # a row of three line-art diyas
    y += 120
    for cx in (PW / 2 - 150, PW / 2, PW / 2 + 150):
        d.chord((cx - 62, y - 30, cx + 62, y + 50), 0, 180, outline=GOLD, width=3)
        d.line((cx - 62, y + 10, cx + 62, y + 10), fill=GOLD, width=3)
        d.polygon([(cx, y - 52), (cx + 15, y - 14), (cx, y + 4), (cx - 15, y - 14)], fill=(240, 196, 110))
    y += 110
    d.text((PW / 2, y), "kalakaricreations.com", font=cg(600, 44), fill=CREAM, anchor="ma")
    d.text((PW / 2, y + 62), "CALL / WHATSAPP  +91 94081 14592", font=cinzel(500, 26), fill=GOLD, anchor="ma")
    return cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)


# ------------------------------------------------------------------ tracking
def detect_panel(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    m = (((h < 12) | (h > 165)) & (s > 80) & (v > 40) & (v < 170)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cs:
        return None, 0
    c = max(cs, key=cv2.contourArea)
    ap = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True).reshape(-1, 2).astype(np.float32)
    if len(ap) != 4:
        return None, cv2.contourArea(c)
    # order TL, TR, BR, BL
    s_ = ap.sum(1)
    d_ = np.diff(ap, axis=1).ravel()
    q = np.float32([ap[s_.argmin()], ap[d_.argmin()], ap[s_.argmax()], ap[d_.argmax()]])
    return q, cv2.contourArea(c)


def track(frames):
    n = len(frames)
    q_last, _ = detect_panel(frames[-1])
    Q = [None] * n
    Q[-1] = q_last
    sift = cv2.SIFT_create(4000)
    bf = cv2.BFMatcher()
    gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]
    for i in range(n - 2, -1, -1):
        q = Q[i + 1]
        m = np.zeros(gray[i].shape, np.uint8)
        c = q.mean(0)
        cv2.fillPoly(m, [((q - c) * 1.35 + c).astype(np.int32)], 255)
        k1, d1 = sift.detectAndCompute(gray[i + 1], m)
        k2, d2 = sift.detectAndCompute(gray[i], m)
        H = None
        if d1 is not None and d2 is not None and len(k1) > 8 and len(k2) > 8:
            good = [a for a, b in bf.knnMatch(d1, d2, k=2) if a.distance < .75 * b.distance]
            if len(good) >= 10:
                p1 = np.float32([k1[g.queryIdx].pt for g in good])
                p2 = np.float32([k2[g.trainIdx].pt for g in good])
                H, inl = cv2.findHomography(p1, p2, cv2.RANSAC, 3.0)
                if H is not None and inl.sum() < 8:
                    H = None
        Q[i] = q if H is None else cv2.perspectiveTransform(q[None], H)[0]
        # once the panel is mostly revealed, trust direct detection
        qd, area = detect_panel(frames[i])
        if qd is not None and area > .85 * cv2.contourArea(Q[i].astype(np.float32)):
            Q[i] = qd
    # light temporal smoothing of the corners
    A = np.stack(Q)
    S = A.copy()
    for i in range(n):
        lo, hi = max(0, i - 2), min(n, i + 3)
        S[i] = A[lo:hi].mean(0)
    return list(S)


# ------------------------------------------------------------------ compositing
def composite(frame, q, art, flat_v):
    h, w = frame.shape[:2]
    src = np.float32([[0, 0], [PW, 0], [PW, PH], [0, PH]])
    M = cv2.getPerspectiveTransform(src, q.astype(np.float32))
    warped = cv2.warpPerspective(art, M, (w, h), flags=cv2.INTER_LINEAR)
    inside = cv2.warpPerspective(np.full((PH, PW), 255, np.uint8), M, (w, h))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    hh, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    red = ((hh < 11) | (hh > 160)).astype(np.float32)          # maroon hue; warm cream cloth sits near 15-20
    # poster where the original pixel is saturated (maroon or gold), cloth and helicopter where it is not
    soft = np.clip((s - 62) / 28, 0, 1) * red
    # the old poster's gold line art and lettering is thin and sits inside maroon: close the maroon mask over it,
    # so it is replaced too, while the large cloth and helicopter regions stay out; keep the dark cable visible
    mar_px = ((s > 70) & (red > 0) & (inside > 0)).astype(np.uint8)
    closed = cv2.morphologyEx(mar_px, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    closed = closed.astype(np.float32) * ~((v < 60) & (s < 70))
    # big pale cloth/helicopter regions (opening drops the thin gold strokes) are never poster
    pale = ((s < 50) & (v > 100)).astype(np.uint8)
    pale = cv2.morphologyEx(pale, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    pale = cv2.dilate(pale, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))).astype(np.float32)
    a = np.maximum(soft, closed) * (1 - pale) * (inside / 255)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (5, 5), 0)
    # shading: blurred brightness of the original poster (maroon pixels only) relative to its clean level
    mar = ((s > 80) & (v < 170)).astype(np.float32) * (inside / 255)
    num = cv2.GaussianBlur(v * mar, (0, 0), 18)
    den = cv2.GaussianBlur(mar, (0, 0), 18) + 1e-3
    shade = np.where(den > .05, num / den / flat_v, 1.0)
    shade = np.clip(shade, .35, 1.35)[..., None]
    lit = np.clip(warped.astype(np.float32) * shade, 0, 255)
    lit = cv2.GaussianBlur(lit, (3, 3), 0)                   # match the footage's softness
    out = frame.astype(np.float32) * (1 - a[..., None]) + lit * a[..., None]
    return out.astype(np.uint8)


def main():
    fonts, ref, out = sys.argv[1:4]
    preview = sys.argv[4:6]
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, os.path.join(tmp, "%04d.png")], check=True)
    names = sorted(os.listdir(tmp))
    frames = [cv2.imread(os.path.join(tmp, n)) for n in names]
    Q = track(frames)
    art = poster(fonts)
    last = cv2.cvtColor(frames[-1], cv2.COLOR_BGR2HSV)
    m = (last[..., 1] > 80) & (last[..., 2] < 170)
    flat_v = float(np.median(last[..., 2][m]))
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            cv2.imwrite(os.path.join(d, f"bb_{f:03d}.png"), cv2.resize(composite(frames[f], Q[f], art, flat_v), (360, 640)))
        return
    for n, f, q in zip(names, frames, Q):
        cv2.imwrite(os.path.join(tmp, n), composite(f, q, art, flat_v))
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                          "-of", "csv=p=0", ref], capture_output=True, text=True).stdout.strip()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", fps, "-i", os.path.join(tmp, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-vf", "scale=1080:1920:flags=lanczos",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)


if __name__ == "__main__":
    main()
