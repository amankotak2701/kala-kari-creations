#!/usr/bin/env python3
"""15 s 9:16 "a little surprise: the Diwali sale is extended" reel, with an original soft music bed.

Timeline:
  0.0–2.4   cream card: "Psst… a little surprise for you" (words fade up one by one)
  2.4–4.6   "Our Diwali Sale is" / "EXTENDED" with a soft gold shimmer
  4.6–6.8   "FLAT 20% OFF on almost everything", "5 extra days", the dates 10–14 Nov ticking in, "till 14 Nov,
            midnight"
  6.8–10.4  THE NEW EDIT: 3 photos with slow push-ins and an offer ribbon
  10.4–13.4 CHIKANKARI: 4 photos
  13.4–15.0 end card: logo, "Sale ends 14 Nov, midnight", website, WhatsApp

Usage:
    python3 sale_extended_reel.py <fonts_dir> <out.mp4>
"""
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import music as M  # noqa: E402

ROOT = os.path.join(HERE, "..")
LOGO = os.path.join(ROOT, "..", "brand", "logo", "kalakari-logo-stacked-maroon-flat.png")
W, H, FPS, TOTAL = 1080, 1920, 30, 15.0
CREAM = (248, 241, 230)
MAROON = (110, 28, 42)
GOLD = (190, 148, 80)
INK = (70, 40, 34)

NEW = [("product-photos/cream-coral-silk-embroidered-3pc/courtyard-full.webp", .5, .45),
       ("product-photos/new-edit-ai/p1a.webp", .5, .5),
       ("posts/everyday-edit/photos/3a-red-kurta-full.webp", .5, .45)]
CHIKAN = [("reels/what-we-cooked/images/2-look-maroon.webp", .5, .5),
          ("reels/what-we-cooked/images/3-look-wine.webp", .5, .45),
          ("reels/what-we-cooked/images/5-look-navy.jpg", .62, .5),
          ("reels/what-we-cooked/images/4-look-pink.jpg", .45, .45)]
T_EXT, T_OFFER, T_NEW, T_CHIK, T_END = 2.4, 4.6, 6.8, 10.4, 13.4


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def font(fonts, fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(fonts, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def cover(path, fx, fy, zoom=1.08):
    im = Image.open(os.path.join(ROOT, path)).convert("RGB")
    w, h = int(W * zoom), int(H * zoom)
    s = max(w / im.width, h / im.height)
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = int(min(max(r.width * fx - w / 2, 0), r.width - w))
    y = int(min(max(r.height * fy - h / 2, 0), r.height - h))
    return r.crop((x, y, x + w, y + h))


def spaced(d, cx, y, s, f, fill, spacing):
    widths = [d.textlength(c, font=f) for c in s]
    x = cx - (sum(widths) + spacing * (len(s) - 1)) / 2
    for c, w in zip(s, widths):
        d.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += w + spacing


class Reel:
    def __init__(self, fonts):
        self.fonts = fonts
        f = lambda *a: font(fonts, *a)  # noqa: E731
        self.f_psst = f("cormorant-garamond", 500, 140, "italic")
        self.f_mid = f("cormorant-garamond", 500, 92, "italic")
        self.f_big = f("cinzel", 600, 150)
        self.f_offer = f("cinzel", 700, 170)
        self.f_caps = f("jost", 500, 38)
        self.f_small = f("jost", 400, 30)
        self.f_day = f("cinzel", 600, 54)
        self.f_label = f("cinzel", 600, 58)
        self.f_rib = f("jost", 500, 34)
        rng = np.random.default_rng(2)
        paper = np.array(CREAM, np.float32)[None, None] + rng.standard_normal((H, W, 1)) * 2.2
        self.paper = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)).convert("RGBA")
        d = ImageDraw.Draw(self.paper)
        for m in (48, 62):
            d.rectangle((m, m, W - m, H - m), outline=GOLD, width=2)
        self.new = [(cover(p, fx, fy), "THE NEW EDIT") for p, fx, fy in NEW]
        self.chik = [(cover(p, fx, fy), "CHIKANKARI") for p, fx, fy in CHIKAN]
        lg = Image.open(LOGO).convert("RGBA")
        self.logo = lg.resize((440, int(440 * lg.height / lg.width)), Image.LANCZOS)
        self.small_logo = lg.resize((150, int(150 * lg.height / lg.width)), Image.LANCZOS)

    def text(self, img, xy, s, f, fill, a, anchor="ms", dy=0):
        if a <= 0:
            return
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((xy[0], xy[1] + dy * (1 - a)), s, font=f, fill=fill + (int(255 * a),), anchor=anchor)
        img.alpha_composite(lay)

    def sparkles(self, img, t, cx, cy, spread, n=14, seed=4):
        rng = np.random.default_rng(seed)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for k in range(n):
            x, y = cx + rng.uniform(-spread, spread), cy + rng.uniform(-spread * .45, spread * .45)
            ph = rng.uniform(0, 6.28)
            a = max(0.0, np.sin(t * 3.2 + ph)) ** 2
            r = rng.uniform(7, 15) * (.6 + .4 * a)
            col = GOLD + (int(220 * a),)
            d.polygon([(x, y - r * 2), (x + r * .35, y - r * .35), (x + r * 2, y), (x + r * .35, y + r * .35),
                       (x, y + r * 2), (x - r * .35, y + r * .35), (x - r * 2, y), (x - r * .35, y - r * .35)], fill=col)
        img.alpha_composite(lay)

    def intro(self, t):
        img = self.paper.copy()
        if t < T_EXT:
            words = [("Psst…", 820, .15), ("a little surprise", 980, .7), ("for you", 1110, 1.2)]
            for s, y, t0 in words:
                f = self.f_psst if s == "Psst…" else self.f_mid
                self.text(img, (W / 2, y), s, f, MAROON, ease((t - t0) / .45), dy=24)
            self.sparkles(img, t, W / 2, 980, 330, seed=3)
            return img
        if t < T_OFFER:
            lt = t - T_EXT
            self.text(img, (W / 2, 820), "Our Diwali Sale is", self.f_mid, INK, ease(lt / .4), dy=20)
            a = ease((lt - .45) / .35)
            if a > 0:
                s = 1.25 - .25 * ease((lt - .45) / .5)
                lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((W / 2, 1010), "EXTENDED", font=self.f_big, fill=MAROON + (int(255 * a),),
                                         anchor="ms")
                lay = lay.resize((int(W * s), int(H * s)), Image.LANCZOS)
                img.alpha_composite(lay.crop((int((lay.width - W) / 2), int(1010 * s - 1010),
                                              int((lay.width - W) / 2) + W, int(1010 * s - 1010) + H)))
            self.sparkles(img, t, W / 2, 960, 420, n=20, seed=7)
            self.text(img, (W / 2, 1100), "✦", self.f_caps, GOLD, a)
            return img
        lt = t - T_OFFER
        self.text(img, (W / 2, 640), "FLAT", self.f_label, INK, ease(lt / .35), dy=16)
        self.text(img, (W / 2, 800), "20% OFF", self.f_offer, MAROON, ease((lt - .1) / .35), dy=20)
        self.text(img, (W / 2, 870), "on almost everything", self.f_mid, INK, ease((lt - .3) / .4), dy=16)
        self.text(img, (W / 2, 1010), "5  EXTRA  DAYS  FOR  YOU", self.f_caps, GOLD, ease((lt - .6) / .4))
        # the five extra days tick in one by one
        days = ["10", "11", "12", "13", "14"]
        x0, step = W / 2 - 2 * 150, 150
        for i, dd in enumerate(days):
            a = ease((lt - .8 - i * .14) / .25)
            if a <= 0:
                continue
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            cx, cy = x0 + i * step, 1120
            d.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), outline=GOLD + (int(255 * a),), width=3,
                      fill=(MAROON if i == 4 else CREAM) + (int(255 * a),))
            d.text((cx, cy + 4), dd, font=self.f_day, fill=(CREAM if i == 4 else MAROON) + (int(255 * a),), anchor="mm")
            img.alpha_composite(lay)
        self.text(img, (W / 2, 1222), "NOVEMBER", self.f_small, INK, ease((lt - 1.4) / .3))
        self.text(img, (W / 2, 1330), "till 14 Nov, midnight", self.f_mid, MAROON, ease((lt - 1.5) / .35), dy=14)
        return img

    def photo(self, t):
        if t < T_CHIK:
            items, t0, span = self.new, T_NEW, (T_CHIK - T_NEW) / len(self.new)
        else:
            items, t0, span = self.chik, T_CHIK, (T_END - T_CHIK) / len(self.chik)
        i = min(len(items) - 1, int((t - t0) / span))
        lt = t - t0 - i * span
        big, label = items[i]
        z = 1.0 + .06 * (lt / span)                                # slow push-in
        cw, ch = int(big.width / (1.08 / 1.0) / z * 1.0), int(big.height / 1.08 / z)
        x, y = (big.width - cw) // 2, (big.height - ch) // 2
        img = big.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BICUBIC).convert("RGBA")
        if lt < .18 and (i > 0 or t0 == T_CHIK):                  # soft white flash between photos
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 252, 246, int(170 * (1 - lt / .18)))))
        if t0 == T_NEW and i == 0 and lt < .3:                    # first photo rises out of the cream card
            img.alpha_composite(Image.new("RGBA", (W, H), CREAM + (int(255 * (1 - ease(lt / .3))),)))
        # top: section label on a soft dark fade
        g = np.clip((300 - np.arange(H)) / 300, 0, 1) ** 1.3 * 175
        sh = Image.new("RGBA", (W, H), (30, 14, 12, 0))
        sh.putalpha(Image.fromarray(np.repeat(g[:, None], W, 1).astype(np.uint8)))
        img.alpha_composite(sh)
        d = ImageDraw.Draw(img)
        spaced(d, W / 2, 112, label, self.f_label, CREAM, 10)
        # bottom ribbon (also covers the image generator's corner badge)
        rib = Image.new("RGBA", (W, 190), MAROON + (236,))
        dr = ImageDraw.Draw(rib)
        dr.line((0, 8, W, 8), fill=GOLD + (255,), width=2)
        spaced(dr, W / 2, 86, "SALE EXTENDED TILL 14 NOV, MIDNIGHT", self.f_rib, (255, 240, 222), 3)
        spaced(dr, W / 2, 140, "kalakaricreations.com", self.f_small, (236, 204, 160), 3)
        img.alpha_composite(rib, (0, H - 190))
        return img

    def end(self, t):
        lt = t - T_END
        img = self.paper.copy()
        a = ease(lt / .35)
        lg = self.logo.copy()
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lg, ((W - lg.width) // 2, 470))
        y = 470 + self.logo.height + 110
        self.text(img, (W / 2, y), "Sale ends 14 Nov, midnight", self.f_mid, MAROON, ease((lt - .15) / .35), dy=14)
        self.text(img, (W / 2, y + 90), "FLAT 20% OFF ON ALMOST EVERYTHING", self.f_caps, INK, ease((lt - .3) / .35))
        self.text(img, (W / 2, y + 200), "kalakaricreations.com", self.f_mid, INK, ease((lt - .45) / .35))
        self.text(img, (W / 2, y + 270), "CALL / WHATSAPP  +91 94081 14592", self.f_small, GOLD, ease((lt - .55) / .35))
        self.sparkles(img, t, W / 2, 420, 380, n=10, seed=11)
        return img

    def frame(self, t):
        if t < T_NEW:
            return self.intro(t)
        if t < T_END:
            return self.photo(t)
        return self.end(t)


# ------------------------------------------------------------------ soft original music
def soft_music(seconds):
    """Warm e-piano broken chords (D, Bm, G, A), a soft pad and bass, low-passed with reverb, plus three
    gentle low chimes on the surprise, the reveal and the end card. No bright or high sounds."""
    sr = M.SR
    n = int((seconds + 3) * sr)
    keys, pad, bass, chime = (np.zeros(n) for _ in range(4))
    beat = .6                                     # 100 BPM: a little lift, still calm
    f = lambda semi: M.D3 * 2 ** (semi / 12)  # noqa: E731

    def epiano(fr, dur, amp):
        k = int(dur * sr)
        x = np.arange(k) / sr
        y = np.sin(2 * np.pi * fr * x) + .25 * np.sin(4 * np.pi * fr * x) * np.exp(-x * 3)
        y *= np.exp(-x * 1.3)
        y[: int(.008 * sr)] *= np.linspace(0, 1, int(.008 * sr))
        return y * M.env(k, 0, .25) * amp

    chords = [([0, 4, 7, 11], -12), ([-3, 2, 6, 9], -15), ([-5, 2, 7, 11], -17), ([-3, 4, 7, 9], -10)]
    t, b = 0.0, 0
    while t < seconds:
        semis, root = chords[b % 4]
        for s_ in semis:
            M.add(pad, M.pad_note(f(s_), beat * 4 + .8) * .5, t)
        k = int((beat * 4 + .5) * sr)
        M.add(bass, np.sin(2 * np.pi * f(root) * np.arange(k) / sr) * M.env(k, .05, .6) * .7, t)
        for e, idx in enumerate([0, 1, 2, 3, 2, 1, 2, 1]):
            M.add(keys, epiano(f(semis[idx] + 12), 1.4, .8 if e % 2 else .95), t + e * beat / 2)
        t += beat * 4
        b += 1
    for tc, semi in ((.2, 24), (T_EXT + .45, 19), (T_END, 24)):
        k = int(2.2 * sr)
        x = np.arange(k) / sr
        y = (np.sin(2 * np.pi * f(semi) * x) + .3 * np.sin(2 * np.pi * f(semi) * 2.01 * x)) * np.exp(-x * 2.2)
        M.add(chime, y * .5, tc)
    mix = .34 * M.lowpass(keys, 1900) + .3 * M.lowpass(pad, 900) + .3 * M.lowpass(bass, 400) + .22 * M.lowpass(chime, 2200)
    mix = M.reverb(mix, seconds=2.4, mix=.28)[: int(seconds * sr)]
    mix *= M.env(len(mix), .8, 1.4)
    return (mix / (np.abs(mix).max() + 1e-9) * .8).astype(np.float32)


def main():
    fonts, out = sys.argv[1:3]
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "music.wav")
    a = soft_music(TOTAL)
    sf.write(wav, np.stack([a, a], 1), M.SR)
    r = Reel(fonts)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-t", f"{TOTAL:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    if len(sys.argv) > 3:                                           # preview stills
        for ts in sys.argv[3].split(","):
            r.frame(float(ts)).convert("RGB").resize((360, 640)).save(os.path.join(os.path.dirname(out), f"se_{float(ts):05.2f}.png"))
        return
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(int(TOTAL * FPS)):
        p.stdin.write(r.frame(k / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait():
        raise SystemExit("ffmpeg failed")
    shutil.rmtree(tmp, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
