#!/usr/bin/env python3
"""17.7 s 9:16 "from silkworm to silk suit" morph reel, built on the reference trend reel (its audio is kept).

One continuous shot: silkworm -> curled worm -> cocoon -> raw silk -> silk hank -> folded silk -> silk sheet ->
pattern pieces -> stitched kurta set -> plain suit on a dress form -> embroidered Cream Coral silk suit ->
suit with dupatta under a clear cover -> a cream garment bag printed "KALA KARI / CREATIONS", on which a maroon
WELCOME10 offer card then fades in.

The keyframes are Gemini images (product-photos/silk-to-suit/01..13.png). This script:
- inpaints Gemini's sparkle mark, reframes the landscape keyframes to 9:16 (centre crop for small subjects, the
  flat-lays scaled into the frame with the paper extended above and below, the silk sheet turned upright);
- builds the final garment bag from the covered-suit frame;
- morphs between keyframes with optical flow (each frame warped part-way towards the next, then cross-faded),
  on the reference's timing, with the reference's actions for the big changes: the folded cloth opens up as the
  camera pushes in until it fills the frame; a crease splits the sheet open to reveal the pattern pieces; the
  embroidery spreads outwards from the neckline; the clear cover drops from the top with a fluttering
  edge, then the garment bag slides down over it. The camera is otherwise still, as in the reference.
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
# matched to the reference: each keyframe lands where the reference's matching stage does
TIMELINE = [("01", 1), ("02", 41), ("03", 62), ("04", 92), ("05", 128), ("06", 160), ("07", 200), ("08", 236),
            ("09", 312), ("10", 340), ("11", 398), ("13", 432), ("bag", 462)]
# long morphs where the reference changes continuously (pieces assembling, embroidery growing)
MORPH = {"02": 22, "03": 16, "04": 20, "05": 24, "06": 22, "07": 26, "08": 24, "09": 56, "10": 26, "11": 44,
         "13": 28, "bag": 24}


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
    if k == 8:                                  # the pattern sheet, turned upright like the silk sheet before it
        sheet = im.crop((330, 60, 2500, 1476)).rotate(90, expand=True)
        cw = int(sheet.height * 9 / 16)
        x = (sheet.width - cw) // 2
        return sheet.crop((x, 0, x + cw, sheet.height)).resize((W, H), Image.LANCZOS)
    return extend_to_portrait(im.crop((704, 113, 2140, 1436)))


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
    return im.convert("RGB"), np.asarray(shape, np.float32) / 255


OFFER_AT = 476                                   # the welcome-offer card fades in on the bag from this frame


def offer_card(bag):
    """The garment bag with a maroon welcome-offer card on its front."""
    im = bag.copy().convert("RGBA")
    cx, top, w, h = 540, 820, 500, 380
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((cx - w / 2, top, cx + w / 2, top + h), radius=18, fill=(117, 44, 57, 255))
    d.rounded_rectangle((cx - w / 2 + 12, top + 12, cx + w / 2 - 12, top + h - 12), radius=12,
                        outline=(217, 188, 121, 255), width=2)
    gold, cream = (222, 192, 128, 255), (247, 242, 233, 255)
    d.text((cx, top + 62), "NEW HERE?", font=font("cinzel", 600, 34), fill=gold, anchor="mm")
    d.text((cx, top + 135), "FLAT 10% OFF", font=font("cinzel", 600, 56), fill=cream, anchor="mm")
    d.line([(cx - 120, top + 186), (cx - 14, top + 186)], fill=gold, width=2)
    d.line([(cx + 14, top + 186), (cx + 120, top + 186)], fill=gold, width=2)
    d.polygon([(cx, top + 178), (cx + 8, top + 186), (cx, top + 194), (cx - 8, top + 186)], fill=gold)
    d.text((cx, top + 240), "Use code  WELCOME10", font=font("cinzel", 600, 34), fill=cream, anchor="mm")
    # "on your first order above ₹999": the ₹ sign is drawn in DejaVu, the rest in Cormorant
    fc = font("cormorant-garamond", 600, 34)
    fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 27)
    parts = [("on your first order above ", fc), ("\u20b9", fr), ("999", fc)]
    tw = sum(d.textlength(t, font=f) for t, f in parts)
    x = cx - tw / 2
    for t, f in parts:
        d.text((x, top + 306), t, font=f, fill=gold, anchor="lm")
        x += d.textlength(t, font=f)
    sh = Image.new("RGBA", (W, H), (80, 40, 30, 0))
    sh.putalpha(card.getchannel("A").filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.3)))
    im.alpha_composite(sh, (0, 8))
    im.alpha_composite(card)
    return im.convert("RGB")


def ref_frame(ref, n):
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", ref, "-vf", f"select=eq(n\\,{n - 1})", "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(H, W, 3)


def match_colour(img, ref, strength=0.75):
    """Shift the keyframe's colours so its backdrop matches the reference's warm peach at the same moment
    (gains measured on the four corners, which are plain backdrop in both)."""
    def corners(a):
        s = 90
        return np.concatenate([a[20:20 + s, 20:20 + s], a[20:20 + s, -20 - s:-20], a[-20 - s:-20, 20:20 + s],
                               a[-20 - s:-20, -20 - s:-20]]).reshape(-1, 3).astype(np.float32)
    g = np.median(corners(ref), 0) / (np.median(corners(img), 0) + 1e-3)
    g = 1 + strength * (g - 1)
    return np.clip(img.astype(np.float32) * g[None, None], 0, 255).astype(np.uint8)


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

    def blend_mask(self, a, b, tg, key, m):
        """Like blend, but the shape moves with tg while the new image shows only where the mask m (0..1) is set."""
        fab, fba = self.flows(a, b, key)
        gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        wa = cv2.remap(a, gx + tg * fba[..., 0], gy + tg * fba[..., 1], cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_REPLICATE)
        wb = cv2.remap(b, gx + (1 - tg) * fab[..., 0], gy + (1 - tg) * fab[..., 1], cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_REPLICATE)
        m = m[..., None]
        return (wa * (1 - m) + wb * m).astype(np.uint8)


GX, GY = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))


def sig(v):
    return 1 / (1 + np.exp(-np.clip(v, -30, 30)))


def drop_mask(t, soft=26, wave=22):
    """A cover sliding down from the top: its lower edge flutters as it falls."""
    front = -150 + t * (H + 300)
    edge = front + wave * np.sin(GX / 70 + t * 9) + 0.6 * wave * np.sin(GX / 31 - t * 13)
    return sig((edge - GY) / soft)


def bloom_mask(t, cx=540, cy=360):
    """Embroidery spreading out from the neckline: a growing ellipse, stretched downwards, with a ragged edge."""
    d = np.hypot((GX - cx) / 1.1, (GY - cy) / 1.6)
    r = t * 1500
    rag = 30 * np.sin(np.arctan2(GY - cy, GX - cx) * 9 + t * 5)
    return sig((r + rag - d) / 28)


def split_mask(t):
    """A crease down the middle that opens outwards to reveal the cut pieces."""
    return sig((t * 620 - np.abs(GX - 540)) / 30)


def zoom_center(img, z):
    """Zoom about the centre (z > 1 pushes in)."""
    M = np.float32([[z, 0, W / 2 * (1 - z)], [0, z, H / 2 * (1 - z)]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def unfold(a, b, t):
    """Folded cloth -> full sheet: the camera pushes in on the folded square as it opens up to fill the frame."""
    za = zoom_center(a, 1 + 1.6 * t)                        # push in on the folded square
    s = 0.42 + 0.58 * t                                    # the sheet grows out from the square's size
    bs = zoom_center(b, s)
    m = np.zeros((H, W), np.float32)
    hw, hh = W / 2 * s, H / 2 * s
    m[int(H / 2 - hh):int(H / 2 + hh), int(W / 2 - hw):int(W / 2 + hw)] = 1
    m = cv2.GaussianBlur(m, (0, 0), 18) * min(1, t * 2.2)
    m = m[..., None]
    return (za * (1 - m) + bs * m).astype(np.uint8)


# how each keyframe arrives (default: optical-flow morph)
TRANSITION = {"07": "unfold", "08": "split", "11": "bloom", "13": "drop", "bag": "drop"}


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
    for k, at in TIMELINE:
        if k != "bag":
            keys[k] = match_colour(keys[k], ref_frame(ref, max(at, 20)))
    bag_img, bag_shape = garment_bag(Image.fromarray(keys["13"]))   # built on the graded frame, so the wall matches
    keys["bag"] = np.asarray(bag_img)
    offer = np.asarray(offer_card(bag_img))
    mor = Morpher()

    def slide_bag(t):
        """The bag slides down from above the frame over the covered suit, with a soft leading shadow."""
        dy = int(-(1 - t) * 1500)
        M = np.float32([[1, 0, 0], [0, 1, dy]])
        bag = cv2.warpAffine(keys["bag"], M, (W, H), borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        m = cv2.warpAffine(bag_shape, M, (W, H))[..., None]
        sh = cv2.warpAffine(cv2.GaussianBlur(bag_shape, (0, 0), 24), np.float32([[1, 0, 10], [0, 1, dy + 26]]),
                            (W, H))[..., None] * 0.28
        base = keys["13"].astype(np.float32) * (1 - sh) + np.array([110, 70, 45]) * sh
        return (base * (1 - m) + bag * m).astype(np.uint8)

    def render(n):
        for i, (k, at) in enumerate(TIMELINE):
            nxt = TIMELINE[i + 1] if i + 1 < len(TIMELINE) else None
            if nxt and n >= nxt[1] - MORPH[nxt[0]]:
                continue
            hold_end = (nxt[1] - MORPH[nxt[0]]) if nxt else nframes
            z = 1.0
            if n >= at:
                img = keys[k]
                if k == "bag" and n >= OFFER_AT:
                    a = ease((n - OFFER_AT) / 10)
                    img = cv2.addWeighted(img, 1 - a, offer, a, 0)
                return push(img, z)
            # morphing from the previous keyframe into this one
            pk, pat = TIMELINE[i - 1]
            raw = (n - (at - MORPH[k])) / MORPH[k]
            t = ease(raw)
            prev = keys[pk]
            kind = TRANSITION.get(k, "flow")
            if kind == "unfold":
                return unfold(prev, keys[k], t)
            if kind == "split":
                return mor.blend_mask(zoom_center(prev, 1 + 0.06 * t), keys[k], 0.0, (pk, k), split_mask(t))
            if kind == "bloom":
                return mor.blend_mask(prev, keys[k], min(1, raw * 1.6), (pk, k), bloom_mask(t))
            if k == "bag":
                return slide_bag(t)
            if kind == "drop":
                return mor.blend_mask(prev, keys[k], 0.4 * t if k == "13" else 0.0, (pk, k), drop_mask(raw))
            return mor.blend(prev, keys[k], t, (pk, k))
        return offer if nframes >= OFFER_AT else keys["bag"]

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
