#!/usr/bin/env python3
"""Finish the Gemini images for the "A Little Garden Daydream" carousel (Royal Blue Leheriya suit):
inpaint the sparkle mark, crop to 4:5 (1080x1350), and add the reference's type.

1. Lace-frame cover: "A LITTLE GARDEN / DAYDREAM" in spaced serif capitals under the frame, then the welcome offer
   and website in small type. The painting is widened by mirroring its edges so the whole frame fits in 4:5.
2. Head-to-knee on the swirl backdrop (studio clamps cropped off).  3. Detail close-up.
4. Second pose, with the offer and website stacked in the free backdrop at the top left.

Usage:
    python3 garden_daydream_finish.py <gemini-dir> <out-dir>
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
FONTS = os.environ.get("KK_FONTS", "/tmp/claude-0/-home-user-kala-kari-creations/"
                       "b594b16c-4df2-59b6-99e4-9ab0ec789fa6/scratchpad/fonts")
CREAM = (244, 239, 224, 255)
SOFT = (226, 220, 196, 255)
RUPEE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(w, size, style="normal"):
    return ImageFont.truetype(os.path.join(FONTS, "fontsource-cormorant-garamond", "package", "files",
                                           f"cormorant-garamond-latin-{w}-{style}.woff2"), size)


def unmark(path):
    """Inpaint Gemini's sparkle mark: a square around where it sits (about 93% across, 94-95% down)."""
    a = cv2.imread(path)
    h, w = a.shape[:2]
    cx, cy = int(w * 0.935), int(h * (0.954 if h / w > 1.45 else 0.94))
    r = int(w * 0.05)
    m = np.zeros((h, w), np.uint8)
    cv2.rectangle(m, (cx - r, cy - r), (cx + r, cy + r), 255, -1)
    return cv2.inpaint(a, m, 25, cv2.INPAINT_TELEA)


def to_pil(a):
    return Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB))


def spaced(d, x, y, text, f, fill, track, anchor="m"):
    w = sum(d.textlength(c, font=f) + track for c in text) - track
    x = x - w / 2 if anchor == "m" else x
    for c in text:
        d.text((x, y), c, font=f, fill=fill, anchor="lm")
        x += d.textlength(c, font=f) + track


def mixed(d, x, y, parts, fill, anchor="m"):
    """Text runs in different fonts on one line (for the ₹ sign)."""
    tw = sum(d.textlength(t, font=f) for t, f in parts)
    x = x - tw / 2 if anchor == "m" else x
    for t, f in parts:
        d.text((x, y), t, font=f, fill=fill, anchor="lm")
        x += d.textlength(t, font=f)


def slide1(src):
    a = unmark(os.path.join(src, "1.png"))
    h, w = a.shape[:2]
    a = a[128:h]                                     # keep the full frame and the landscape below it
    ch = a.shape[0]
    cw = int(ch * 4 / 5)
    pad = (cw - w) // 2
    if pad > 0:                                      # widen the painting by mirroring its edges, softly
        a = cv2.copyMakeBorder(a, 0, 0, pad, cw - w - pad, cv2.BORDER_REFLECT)
        blur = cv2.GaussianBlur(a, (0, 0), 12)
        m = np.zeros(a.shape[:2], np.float32)
        m[:, :pad + 30] = 1
        m[:, -(cw - w - pad) - 30:] = 1
        m = cv2.GaussianBlur(m, (0, 0), 20)[..., None]
        a = (a * (1 - m) + blur * m).astype(np.uint8)
    im = to_pil(cv2.resize(a, (W, H), interpolation=cv2.INTER_AREA)).convert("RGBA")
    d = ImageDraw.Draw(im)
    f = font(500, 50)
    spaced(d, W / 2, 1186, "A LITTLE GARDEN", f, CREAM, 9)
    spaced(d, W / 2, 1246, "DAYDREAM", f, CREAM, 9)
    f2 = font(600, 22)
    spaced(d, W / 2, 1300, "NEW HERE?  FLAT 10% OFF  ·  CODE WELCOME10  ·  KALAKARICREATIONS.COM", f2, SOFT, 2)
    return im.convert("RGB")


def crop45(src, name, top):
    a = unmark(os.path.join(src, name))
    h, w = a.shape[:2]
    ch = int(w * 5 / 4)
    top = min(top, h - ch)
    return to_pil(cv2.resize(a[top:top + ch], (W, H), interpolation=cv2.INTER_AREA))


def slide4(src):
    im = crop45(src, "4.png", 0).convert("RGBA")
    d = ImageDraw.Draw(im)
    x, y = 64, 92
    spaced(d, x, y, "NEW HERE?", font(600, 26), SOFT, 4, anchor="l")
    spaced(d, x, y + 52, "FLAT 10% OFF", font(500, 46), CREAM, 5, anchor="l")
    spaced(d, x, y + 106, "CODE WELCOME10", font(600, 26), CREAM, 4, anchor="l")
    fi = font(500, 26, "italic")
    mixed(d, x, y + 148, [("on your first order above ", fi), ("₹", ImageFont.truetype(RUPEE, 19)),
                          ("999", fi)], SOFT, anchor="l")
    spaced(d, x, y + 194, "KALAKARICREATIONS.COM", font(600, 22), SOFT, 3, anchor="l")
    return im.convert("RGB")


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    slide1(src).save(os.path.join(out, "slide-1.jpg"), quality=94)
    crop45(src, "2.png", 150).save(os.path.join(out, "slide-2.jpg"), quality=94)
    crop45(src, "3.png", 0).save(os.path.join(out, "slide-3.jpg"), quality=94)
    slide4(src).save(os.path.join(out, "slide-4.jpg"), quality=94)
    print(out)


if __name__ == "__main__":
    main()
