#!/usr/bin/env python3
"""17.7 s 9:16 "from silkworm to silk suit" morph reel, built on the reference trend reel (its audio is kept).

One continuous shot: silkworm -> curled worm -> cocoon -> raw silk -> silk hank -> folded silk -> silk sheet ->
pattern pieces -> stitched kurta set -> plain suit on a dress form -> embroidered Cream Coral silk suit ->
suit with dupatta under a clear cover -> a cream garment bag printed "KALA KARI / CREATIONS".

The keyframes are Gemini images (product-photos/silk-to-suit/01..13.png). This script:
- inpaints Gemini's sparkle mark, reframes the landscape keyframes to 9:16 (centre crop for small subjects, the
  flat-lays scaled into the frame with the paper extended above and below, the silk sheet turned upright);
- builds the final garment bag from the covered-suit frame;
- morphs between keyframes with optical flow (each frame warped part-way towards the next, then cross-faded),
  on the reference's timing, with a slow push-in while each keyframe holds.
Keyframe 12 (dupatta) is skipped: it shows the kurta without the coral yoke.

Usage:
    python3 silk_to_suit_reel.py <keyframes-dir> <ref.mp4> <out.mp4> [--preview dir f1,f2,...]
"""
import os
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FONTS = os.environ.get("KK_FONTS", "/tmp/claude-0/-home-user-kala-kari-creations/"
                       "b594b16c-4df2-59b6-99e4-9ab0ec789fa6/scratchpad/fonts")
# (keyframe, frame at which it is fully formed). The morph into each keyframe takes MORPH frames before that.
TIMELINE = [("01", 1), ("02", 42), ("03", 68), ("04", 92), ("05", 125), ("06", 156), ("07", 186), ("08", 222),
            ("09", 278), ("10", 322), ("11", 372), ("13", 420), ("bag", 462)]
MORPH = {"02": 16, "03": 14, "04": 14, "05": 16, "06": 14, "07": 16, "08": 18, "09": 18, "10": 18, "11": 18,
         "13": 16, "bag": 16}


def font(fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(FONTS, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def unmark(im):
    """Inpaint the sparkle mark in the bottom-right corner."""
    a = cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2BGR)
    h, w = a.shape[:2]
    s = int(min(w, h) * 0.11)
    m = np.zeros((h, w), np.uint8)
    m[h - s:h - int(s * 0.05), w - s:w - int(s * 0.05)] = 255
    a = cv2.inpaint(a, m, 11, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB))


def extend_to_portrait(crop):
    """Scale a landscape crop to the full width and extend the plain paper above and below it."""
    s = W / crop.width
    c = crop.resize((W, round(crop.height * s)), Image.LANCZOS)
    a = np.asarray(c, np.float32)
    top = int((H - c.height) / 2)
    out = np.zeros((H, W, 3), np.float32)
    out[top:top + c.height] = a
    t_col = np.median(a[:8].reshape(-1, 3), 0)               # the plain paper colour along each edge
    b_col = np.median(a[-8:].reshape(-1, 3), 0)
    out[:top] = t_col
    out[top + c.height:] = b_col
    noise = np.random.default_rng(3).normal(0, 1.2, (H, W, 1))
    out[:top] += noise[:top]
    out[top + c.height:] += noise[top + c.height:]
    # soften the seams
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    for y in (top, top + c.height):
        d.rectangle((0, y - 30, W, y + 30), fill=255)
    return Image.composite(im.filter(ImageFilter.GaussianBlur(14)), im, m.filter(ImageFilter.GaussianBlur(16)))


def load_keyframe(src, key):
    im = unmark(Image.open(os.path.join(src, key + ".png")))
    if im.height > im.width:                    # already 9:16
        return im.resize((W, H), Image.LANCZOS)
    w, h = im.size
    k = int(key)
    if k <= 6 or k == 10:                       # small subject / dress form: centre crop to 9:16
        cw = int(h * 9 / 16)
        x = (w - cw) // 2
        return im.crop((x, 0, x + cw, h)).resize((W, H), Image.LANCZOS)
    if k == 7:                                  # the silk sheet: turn it upright
        return im.rotate(90, expand=True).resize((W, H), Image.LANCZOS)
    box = {8: (394, 127, 2436, 1422), 9: (704, 113, 2140, 1436)}[k]
    return extend_to_portrait(im.crop(box))


def garment_bag(covered):
    """The final frame: the covered suit becomes a closed cream garment bag with the brand printed on it."""
    im = covered.copy().convert("RGBA")
    x0, x1, y0, y1 = 236, 844, 230, 1620                            # the clear cover's outline in keyframe 13
    cx = (x0 + x1) / 2
    shape = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(shape)
    d.ellipse((x0, y0, x1, y0 + 340), fill=255)                      # rounded shoulders
    d.rectangle((x0, y0 + 170, x1, y1), fill=255)
    shape = shape.filter(ImageFilter.GaussianBlur(2))
    # soft shadow on the wall
    sh = Image.new("RGBA", (W, H), (120, 80, 50, 0))
    sh.putalpha(shape.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * 0.35)))
    im.alpha_composite(sh, (18, 22))
    # matte cream fabric with gentle folds and edge shading
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.array([238, 228, 212], np.float32)
    fold = 0.035 * np.sin((xx - cx) / 38.0 + yy / 260.0) * np.clip((yy - 700) / 700, 0, 1)
    edge = 1 - 0.10 * np.clip(np.abs(xx - cx) / ((x1 - x0) / 2), 0, 1) ** 3
    fab = base[None, None] * (edge + fold)[..., None]
    fab += np.random.default_rng(5).normal(0, 1.6, (H, W, 1))
    fab_im = Image.fromarray(np.clip(fab, 0, 255).astype(np.uint8)).convert("RGBA")
    fab_im.putalpha(shape)
    im.alpha_composite(fab_im)
    # a seam line down the front, and the brand
    d = ImageDraw.Draw(im)
    d.line([(cx, y0 + 420), (cx, y1 - 10)], fill=(214, 202, 184, 255), width=2)
    f1, f2 = font("cinzel", 600, 54), font("cormorant-garamond", 600, 24)
    d.text((cx, y0 + 250), "KALA KARI", font=f1, fill=(72, 58, 52, 255), anchor="mm")
    t = "CREATIONS"
    tw = sum(d.textlength(c, font=f2) + 10 for c in t) - 10
    x = cx - tw / 2
    for c in t:
        d.text((x, y0 + 300), c, font=f2, fill=(110, 88, 64, 255), anchor="lm")
        x += d.textlength(c, font=f2) + 10
    return im.convert("RGB")


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


class Morpher:
    def __init__(self):
        self.dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
        self.cache = {}

    def flows(self, a, b, key):
        if key not in self.cache:
            s = 0.25
            ga = cv2.resize(cv2.cvtColor(a, cv2.COLOR_RGB2GRAY), None, fx=s, fy=s)
            gb = cv2.resize(cv2.cvtColor(b, cv2.COLOR_RGB2GRAY), None, fx=s, fy=s)
            fab = self.dis.calc(ga, gb, None)
            fba = self.dis.calc(gb, ga, None)
            up = lambda f: cv2.resize(f, (W, H)) / s
            self.cache[key] = (up(fab), up(fba))
        return self.cache[key]

    def blend(self, a, b, t, key):
        fab, fba = self.flows(a, b, key)
        gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        # a moves part-way towards b; b comes from part-way back towards a
        wa = cv2.remap(a, gx + t * fba[..., 0], gy + t * fba[..., 1], cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_REPLICATE)
        wb = cv2.remap(b, gx + (1 - t) * fab[..., 0], gy + (1 - t) * fab[..., 1], cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_REPLICATE)
        return cv2.addWeighted(wa, 1 - t, wb, t, 0)


def push(img, z):
    """Slow push-in: crop the centre by zoom z and scale back to full size."""
    if z <= 1.0001:
        return img
    w, h = int(W / z), int(H / z)
    x, y = (W - w) // 2, (H - h) // 2
    return cv2.resize(img[y:y + h, x:x + w], (W, H), interpolation=cv2.INTER_LINEAR)


def main():
    args = sys.argv[1:]
    preview = None
    if "--preview" in args:
        k = args.index("--preview")
        preview, args = args[k + 1:k + 3], args[:k]
    src, ref, out = args
    nframes = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                                  "stream=nb_read_packets", "-of", "csv=p=0", ref], capture_output=True,
                                 text=True).stdout.strip())
    keys = {}
    for k, _ in TIMELINE:
        if k != "bag":
            keys[k] = np.asarray(load_keyframe(src, k))
    keys["bag"] = np.asarray(garment_bag(Image.fromarray(keys["13"])))
    mor = Morpher()

    def render(n):
        for i, (k, at) in enumerate(TIMELINE):
            nxt = TIMELINE[i + 1] if i + 1 < len(TIMELINE) else None
            if nxt and n >= nxt[1] - MORPH[nxt[0]]:
                continue
            hold_end = (nxt[1] - MORPH[nxt[0]]) if nxt else nframes
            z = 1 + 0.03 * ease((n - at) / max(1, hold_end - at))
            if n >= at:
                return push(keys[k], z)
            # morphing from the previous keyframe into this one
            pk, pat = TIMELINE[i - 1]
            t = ease((n - (at - MORPH[k])) / MORPH[k])
            prev = push(keys[pk], 1.03)
            return mor.blend(prev, keys[k], t, (pk, k))
        return keys["bag"]

    if preview:
        d, fs = preview
        for n in map(int, fs.split(",")):
            Image.fromarray(render(n)).resize((360, 640)).save(os.path.join(d, f"st_{n:03d}.png"))
        return
    tmp = tempfile.mkdtemp()
    try:
        for n in range(1, nframes + 1):
            Image.fromarray(render(n)).save(os.path.join(tmp, f"{n:04d}.png"), compress_level=1)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", os.path.join(tmp, "%04d.png"),
                        "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                        out], check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
