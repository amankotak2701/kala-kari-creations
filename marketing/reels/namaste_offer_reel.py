#!/usr/bin/env python3
"""16.2 s 9:16 "Namaste 🙏 behan or bhaiyoo… aapko dikhane ja rhe hai… YEH" offer reel, timed like the reference
trend reel: maroon words pop one by one on cream (the namaste hands are cut from the reference,
assets/namaste-hands.png), four big sparkles, then a maroon screen where "Get flat 20% off" slides down, a smoke
transition into the product photos (full screen, a 2x2 grid building panel by panel, a wipe), a white flash and the
Kala Kari Creations logo with the website and WhatsApp number. Reference audio.

Usage:
    python3 namaste_offer_reel.py <fonts_dir> <music.wav> <out.mp4> <p1> ... <p8>
p1 opens the photo section; p2-p5 build the grid; p6, p7 and p8 are full screen; p8 is wiped in.
Pass "preview:<dir>:t1,t2,..." as <out.mp4> to save stills instead of a video.
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HANDS = os.path.join(HERE, "assets", "namaste-hands.png")
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-maroon-flat.png")
W, H, FPS = 1080, 1920, 30
TOTAL = 16.18
CREAM = (247, 243, 231)
INK = (92, 22, 26)
MAROON = (81, 0, 14)
WHITE = (255, 255, 255)
END_BG = (251, 250, 249)

WORDS = [(0.0, 0.33, ["NAMASTE"], .53), (0.73, 1.7, ["BEHAN OR BHAIYOO"], .74),
         (3.05, 4.45, ["AAPKO", "DIKHANE", "JA RHE HAI"], .74), (4.45, 5.85, ["YEH"], .36)]
T_HANDS = (0.33, 0.73)
T_SPARK = (1.7, 3.05)
T_OFFER, T_SMOKE, T_P1, T_GRID = 5.85, 7.7, 7.95, 8.55
GRID_IN = [8.55, 8.8, 9.4, 9.6]                    # TL, TR, BL, BR panels wipe in
T_P6, T_P7, T_WIPE, T_P8, T_FLASH, T_LOGO = 10.27, 11.17, 11.65, 12.0, 13.2, 13.9
OFFER = ["Get flat", "20% off"]
OFFER_SMALL = ["on all our products", "Diwali Dhamaka Sale · till 9 Nov"]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def cover(im, w, h, fy=.4, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = (r.width - w) // 2
    y = int(min(max(r.height * fy - h / 2, 0), r.height - h))
    return r.crop((x, y, x + w, y + h))


def star(size_w, size_h, col):
    """Four-point sparkle with concave sides, like the reference."""
    img = Image.new("RGBA", (int(size_w), int(size_h)), (0, 0, 0, 0))
    cx, cy, rx, ry = size_w / 2, size_h / 2, size_w / 2, size_h / 2
    pts = []
    for q in range(4):
        a0 = q * math.pi / 2
        for i in range(24):
            t = i / 24
            a = a0 + t * math.pi / 2
            # astroid-like curve between the tips
            x = math.copysign(abs(math.cos(a)) ** 2.6, math.cos(a))
            y = math.copysign(abs(math.sin(a)) ** 2.6, math.sin(a))
            pts.append((cx + x * rx, cy - y * ry))
    ImageDraw.Draw(img).polygon(pts, fill=col)
    return img


class Reel:
    def __init__(self, fonts_dir, photos):
        rz = os.path.join(fonts_dir, "fontsource-rozha-one", "package", "files", "rozha-one-latin-400-normal.woff2")
        pp = os.path.join(fonts_dir, "fontsource-poppins", "package", "files", "poppins-latin-{}-normal.woff2")
        self.rozha = rz
        self.offer_font = ImageFont.truetype(rz, 118)
        self.small_font = ImageFont.truetype(pp.format(400), 34)
        self.small_font2 = ImageFont.truetype(pp.format(500), 30)
        self.end_font = ImageFont.truetype(pp.format(500), 38)
        self.end_font2 = ImageFont.truetype(pp.format(400), 30)
        self.words = [self.word_layer(lines, frac) for _, _, lines, frac in WORDS]
        hands = Image.open(HANDS).convert("RGBA")
        self.hands = hands.resize((int(hands.width * 1.5), int(hands.height * 1.5)), Image.LANCZOS)
        self.star = star(400, 560, INK + (255,))
        src = [Image.open(p).convert("RGB") for p in photos]
        self.full = [cover(im, W, H) for im in src]
        self.big = [cover(im, int(W * 1.08), int(H * 1.08)) for im in src]
        self.cells = [cover(im, W // 2, H // 2) for im in src[1:5]]
        self.offer = self.offer_layer()
        self.offer_shadow = self.offer_layer(shadow=True)
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo.resize((520, int(520 * logo.height / logo.width)), Image.LANCZOS)
        self.smoke = self.make_smoke()

    def word_layer(self, lines, frac):
        """Block of centred maroon lines; the widest line fills `frac` of the width."""
        f = ImageFont.truetype(self.rozha, 100)
        widest = max(f.getlength(s) for s in lines)
        f = ImageFont.truetype(self.rozha, int(100 * frac * W / widest))
        asc, desc = f.getmetrics()
        pitch = int((asc + desc) * .82)
        lay = Image.new("RGBA", (W, pitch * len(lines) + desc + 40), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for i, s in enumerate(lines):
            d.text((W / 2, 20 + i * pitch), s, font=f, fill=INK, anchor="ma")
        return lay.crop(lay.getbbox())

    def offer_layer(self, shadow=False):
        lay = Image.new("RGBA", (W, 520), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        col = (0, 0, 0, 120) if shadow else WHITE
        d.text((W / 2, 150), OFFER[0], font=self.offer_font, fill=col, anchor="ms")
        d.text((W / 2, 272), OFFER[1], font=self.offer_font, fill=col, anchor="ms")
        d.text((W / 2, 330), OFFER_SMALL[0], font=self.small_font, fill=col, anchor="ms")
        d.text((W / 2, 380), OFFER_SMALL[1], font=self.small_font2, fill=col, anchor="ms")
        return lay.filter(ImageFilter.GaussianBlur(10)) if shadow else lay

    @staticmethod
    def make_smoke():
        rng = np.random.default_rng(5)
        n = np.zeros((H // 8, W // 8))
        for s in (8, 16, 32):
            small = rng.standard_normal((H // 8 // s + 2, W // 8 // s + 2))
            n += np.asarray(Image.fromarray(small.astype(np.float32)).resize((W // 8, H // 8), Image.BICUBIC)) * s ** .7
        n = (n - n.min()) / np.ptp(n)
        n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
                       .filter(ImageFilter.GaussianBlur(40)), np.float32) / 255
        n = n ** .55
        purple = np.array([120, 80, 170], np.float32)
        white = np.array([246, 244, 252], np.float32)
        rgb = purple * (1 - n[..., None]) + white * n[..., None]
        return Image.fromarray(rgb.astype(np.uint8)), n

    def put_offer(self, img, cy, shadow):
        y = int(cy - 230)
        if shadow:
            img.alpha_composite(self.offer_shadow, (0, y + 4))
        img.alpha_composite(self.offer, (0, y))

    def zoomed(self, k, local, span):
        z = 1 + .06 * clamp(local / span)
        big = self.big[k]
        bw, bh = int(big.width / z / 1.08 * 1.0), int(big.height / z / 1.08 * 1.0)
        x, y = (big.width - bw) // 2, int((big.height - bh) * .4)
        return big.crop((x, y, x + bw, y + bh)).resize((W, H), Image.BICUBIC).convert("RGBA")

    def intro(self, t):
        img = Image.new("RGBA", (W, H), CREAM + (255,))
        for (t0, t1, _, _), lay in zip(WORDS, self.words):
            if t0 <= t < t1:
                s = 1.0
                if t1 == 1.7 and t > 1.55:                     # "BEHAN OR BHAIYOO" zooms away
                    s = 1 - .7 * ease((t - 1.55) / .15)
                if t0 == 3.05:
                    s = 1.04 - .04 * ease((t - t0) / .3)
                if t0 == 4.45:                                 # "YEH" settles smaller before the cut
                    s = 1 - .25 * ease((t - 5.1) / .7)
                l2 = lay if s == 1 else lay.resize((max(1, int(lay.width * s)), max(1, int(lay.height * s))), Image.LANCZOS)
                img.alpha_composite(l2, ((W - l2.width) // 2, int(H * .485 - l2.height / 2)))
        if T_HANDS[0] <= t < T_HANDS[1]:
            img.alpha_composite(self.hands, ((W - self.hands.width) // 2, int(H * .5 - self.hands.height / 2)))
        if T_SPARK[0] <= t < T_SPARK[1]:
            lt = t - T_SPARK[0]
            grow = ease(lt / .25) * (1 - ease((lt - 1.15) / .2))
            for k, (cx, cy) in enumerate([(30, .26 * H), (W - 30, .15 * H), (30, .84 * H), (W - 30, .77 * H)]):
                ph = lt * 5.5 + k * 1.7
                s = grow * (.85 + .2 * math.sin(ph))
                if s <= .02:
                    continue
                st = self.star.resize((max(1, int(400 * s)), max(1, int(560 * s))), Image.BICUBIC)
                st = st.rotate(14 * math.sin(ph * .8), resample=Image.BICUBIC, expand=True)
                dx = 60 * math.sin(ph * .6) * (1 if cx < W / 2 else -1)
                img.alpha_composite(st, (int(cx + dx - st.width / 2), int(cy - st.height / 2)))
        return img

    def photos(self, t):
        if t < T_GRID:
            img = self.zoomed(0, t - T_P1, T_GRID - T_P1)
        elif t < T_P6:
            img = Image.new("RGBA", (W, H), MAROON + (255,))
            for k, t0 in enumerate(GRID_IN):
                if t < t0:
                    continue
                cell = self.cells[k]
                z = 1 + .05 * clamp((t - t0) / 1.7)
                cw, ch = int(cell.width / z), int(cell.height / z)
                c = cell.crop(((cell.width - cw) // 2, (cell.height - ch) // 3, (cell.width - cw) // 2 + cw,
                               (cell.height - ch) // 3 + ch)).resize(cell.size, Image.BICUBIC)
                vis = int(cell.width * ease_out((t - t0) / .22))
                if vis > 0:
                    x0, y0 = (k % 2) * W // 2, (k // 2) * H // 2
                    img.paste(c.crop((0, 0, vis, cell.height)), (x0, y0))
        elif t < T_P7:
            img = self.zoomed(5, t - T_P6, T_P7 - T_P6)
        elif t < T_P8:
            img = self.zoomed(6, t - T_P7, T_P8 - T_P7)
            if t >= T_WIPE:                                    # next photo wipes in from the left
                x = int(W * ease((t - T_WIPE) / (T_P8 - T_WIPE)))
                if x > 0:
                    nxt = self.zoomed(7, 0, 1)
                    img.paste(nxt.crop((0, 0, x, H)), (0, 0))
        else:
            img = self.zoomed(7, t - T_P8, T_FLASH - T_P8)
        if t < T_P1 + .35:                                     # haze from the smoke clears off the first photo
            haze = Image.new("RGBA", (W, H), (210, 205, 245, int(200 * (1 - ease((t - T_P1) / .35)))))
            img.alpha_composite(haze)
        self.put_offer(img, H * (.43 + .05 * ease((t - T_SMOKE) / .4)), True)
        return img

    def offer_screen(self, t):
        img = Image.new("RGBA", (W, H), MAROON + (255,))
        cy = -H * .03 + (H * .46) * ease_out((t - T_OFFER) / (T_SMOKE - T_OFFER) * .95)
        self.put_offer(img, cy, False)
        if t >= T_SMOKE:                                       # purple-white smoke rolls over
            sm, n = self.smoke
            p = ease((t - T_SMOKE) / (T_P1 - T_SMOKE))
            a = np.clip((p * 2.2 - (1 - n) * .7) * 255, 0, 255).astype(np.uint8)
            lay = sm.convert("RGBA")
            lay.putalpha(Image.fromarray(a))
            img.alpha_composite(lay)
            self.put_offer(img, H * .43, False)
        return img

    def ending(self, t):
        if t < T_LOGO:
            img = self.zoomed(4, t - T_FLASH, 1.0)             # last look fades into white
            lt = t - T_FLASH                                   # flash to white, clear a little, then fade out
            if lt < .1:
                wa = ease(lt / .1)
            elif lt < .25:
                wa = 1 - .6 * ease((lt - .1) / .15)
            else:
                wa = .4 + .6 * ease((lt - .25) / (T_LOGO - T_FLASH - .25))
            img.alpha_composite(Image.new("RGBA", (W, H), END_BG + (int(255 * wa),)))
        else:
            img = Image.new("RGBA", (W, H), END_BG + (255,))
        a = ease((t - (T_FLASH + .4)) / .5)
        if a > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.alpha_composite(self.logo, ((W - self.logo.width) // 2, int(H * .45 - self.logo.height / 2)))
            d = ImageDraw.Draw(lay)
            y = int(H * .45 + self.logo.height / 2 + 70)
            d.text((W / 2, y), "kalakaricreations.com", font=self.end_font, fill=INK, anchor="ms")
            d.text((W / 2, y + 56), "CALL / WHATSAPP  +91 94081 14592", font=self.end_font2, fill=(120, 70, 70), anchor="ms")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)
        return img

    def frame(self, t):
        if t < T_OFFER:
            return self.intro(t)
        if t < T_P1:
            return self.offer_screen(t)
        if t < T_FLASH:
            return self.photos(t)
        return self.ending(t)


def main():
    fonts_dir, music, out = sys.argv[1:4]
    photos = sys.argv[4:12]
    assert len(photos) == 8, "need 8 product photos"
    r = Reel(fonts_dir, photos)
    if out.startswith("preview:"):
        _, d, ts = out.split(":")
        for t in map(float, ts.split(",")):
            r.frame(t).convert("RGB").resize((W // 4, H // 4)).save(os.path.join(d, f"no_{t:05.2f}.png"))
        return
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", music, "-t", f"{TOTAL:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(int(TOTAL * FPS)):
        proc.stdin.write(r.frame(k / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    print(out)


if __name__ == "__main__":
    main()
