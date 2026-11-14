#!/usr/bin/env python3
"""12 s 9:16 "LAST DAY of the sale" Instagram story, with an original soft-but-urgent music bed.

Timeline:
  0.0–2.6   cream card: "Last call…", then "TODAY IS THE" / "LAST DAY" pulsing gently, with gold sparkles
  2.6–5.0   "FLAT 20% OFF on almost everything", "Sale ends tonight at 12 midnight", and a clock that sweeps
            to midnight
  5.0–10.0  quick looks (new arrivals and chikankari), 0.62 s each, with a "LAST DAY · ENDS TONIGHT" ribbon
            near the bottom, above Instagram's reply bar
  10.0–12.0 end card: "Shop before midnight", website, WhatsApp. The lower middle is kept clear for a story
            link sticker.

Shares its look and helpers with sale_extended_reel.py.

Usage:
    python3 last_day_story.py <fonts_dir> <out.mp4> [t1,t2,... (preview stills next to out)]
"""
import math
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import music as M  # noqa: E402
from sale_extended_reel import (CREAM, GOLD, H, INK, LOGO, MAROON, W, cover, ease, font,  # noqa: E402
                                spaced)

FPS, TOTAL = 30, 12.0
T_OFFER, T_LOOKS, T_END = 2.6, 5.0, 10.0
LOOKS = [("product-photos/website-new-arrivals/01.jpg", .5, .4),
         ("reels/what-we-cooked/images/2-look-maroon.webp", .5, .5),
         ("product-photos/website-new-arrivals/04.jpg", .5, .4),
         ("reels/what-we-cooked/images/5-look-navy.jpg", .62, .5),
         ("product-photos/website-new-arrivals/08.jpg", .5, .4),
         ("reels/what-we-cooked/images/3-look-wine.webp", .5, .45),
         ("product-photos/website-new-arrivals/03.jpg", .5, .4),
         ("product-photos/cream-coral-silk-embroidered-3pc/courtyard-full.webp", .5, .45)]


class Story:
    def __init__(self, fonts):
        f = lambda *a: font(fonts, *a)  # noqa: E731
        self.f_it = f("cormorant-garamond", 500, 96, "italic")
        self.f_it_s = f("cormorant-garamond", 500, 70, "italic")
        self.f_caps = f("jost", 500, 40)
        self.f_small = f("jost", 400, 30)
        self.f_huge = f("cinzel", 700, 170)
        self.f_offer = f("cinzel", 700, 160)
        self.f_label = f("cinzel", 600, 54)
        self.f_rib = f("jost", 600, 36)
        rng = np.random.default_rng(5)
        paper = np.array(CREAM, np.float32)[None, None] + rng.standard_normal((H, W, 1)) * 2.2
        self.paper = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)).convert("RGBA")
        d = ImageDraw.Draw(self.paper)
        for m in (48, 62):
            d.rectangle((m, m, W - m, H - m), outline=GOLD, width=2)
        self.looks = []
        for p, fx, fy in LOOKS:
            im = Image.open(os.path.join(HERE, "..", p)).convert("RGB")
            im = im.crop((0, 0, im.width, int(im.height * .94)))      # drop the generator's corner badge
            tmp = os.path.join(tempfile.gettempdir(), "kk_look.png")
            im.save(tmp)
            self.looks.append(cover(os.path.relpath(tmp, os.path.join(HERE, "..")), fx, fy, zoom=1.06))
            os.remove(tmp)
        lg = Image.open(LOGO).convert("RGBA")
        self.logo = lg.resize((380, int(380 * lg.height / lg.width)), Image.LANCZOS)

    def text(self, img, xy, s, f, fill, a, anchor="ms", dy=0, scale=1.0):
        if a <= 0:
            return
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((xy[0], xy[1] + dy * (1 - a)), s, font=f, fill=fill + (int(255 * a),), anchor=anchor)
        if scale != 1.0:
            big = lay.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
            ox, oy = int(xy[0] * scale - xy[0]), int(xy[1] * scale - xy[1])
            lay = big.crop((ox, oy, ox + W, oy + H))
        img.alpha_composite(lay)

    def sparkles(self, img, t, cx, cy, spread, n=16, seed=4):
        rng = np.random.default_rng(seed)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for _ in range(n):
            x, y = cx + rng.uniform(-spread, spread), cy + rng.uniform(-spread * .5, spread * .5)
            a = max(0.0, math.sin(t * 3.4 + rng.uniform(0, 6.28))) ** 2
            r = rng.uniform(7, 15) * (.6 + .4 * a)
            d.polygon([(x, y - r * 2), (x + r * .35, y - r * .35), (x + r * 2, y), (x + r * .35, y + r * .35),
                       (x, y + r * 2), (x - r * .35, y + r * .35), (x - r * 2, y), (x - r * .35, y - r * .35)],
                      fill=GOLD + (int(220 * a),))
        img.alpha_composite(lay)

    def clock(self, img, t, cx, cy, r, a):
        """A small clock whose hands sweep to 12 (midnight)."""
        if a <= 0:
            return
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        al = int(255 * a)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=MAROON + (al,), width=6)
        for k in range(12):
            ang = k * math.pi / 6
            r0 = r * (.78 if k % 3 else .7)
            d.line((cx + r0 * math.sin(ang), cy - r0 * math.cos(ang), cx + r * .9 * math.sin(ang),
                    cy - r * .9 * math.cos(ang)), fill=MAROON + (al,), width=4 if k % 3 == 0 else 2)
        p = ease((t - T_OFFER - .6) / 1.4)
        hour = math.radians(-60 * (1 - p))                 # from 10 o'clock to 12
        minute = math.radians(-360 * 2 * (1 - p))
        d.line((cx, cy, cx + r * .5 * math.sin(hour), cy - r * .5 * math.cos(hour)), fill=MAROON + (al,), width=8)
        d.line((cx, cy, cx + r * .75 * math.sin(minute), cy - r * .75 * math.cos(minute)), fill=GOLD + (al,), width=5)
        d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=MAROON + (al,))
        img.alpha_composite(lay)

    def intro(self, t):
        img = self.paper.copy()
        if t < T_OFFER:
            self.text(img, (W / 2, 700), "Last call…", self.f_it, INK, ease((t - .15) / .4), dy=22)
            self.text(img, (W / 2, 860), "TODAY IS THE", self.f_caps, GOLD, ease((t - .6) / .35))
            pulse = 1 + .03 * math.sin(max(0.0, t - 1.0) * 6.0)
            self.text(img, (W / 2, 1060), "LAST DAY", self.f_huge, MAROON, ease((t - .8) / .35), scale=pulse)
            self.text(img, (W / 2, 1160), "of our Diwali Dhamaka Sale", self.f_it_s, INK, ease((t - 1.2) / .4))
            self.sparkles(img, t, W / 2, 980, 420, seed=3)
            return img
        lt = t - T_OFFER
        self.text(img, (W / 2, 560), "FLAT", self.f_label, INK, ease(lt / .3), dy=14)
        self.text(img, (W / 2, 720), "20% OFF", self.f_offer, MAROON, ease((lt - .1) / .3), dy=18)
        self.text(img, (W / 2, 800), "on almost everything", self.f_it_s, INK, ease((lt - .3) / .35), dy=14)
        self.clock(img, t, W / 2, 1010, 120, ease((lt - .45) / .35))
        self.text(img, (W / 2, 1230), "Sale ends tonight", self.f_it, MAROON, ease((lt - .7) / .35), dy=16)
        self.text(img, (W / 2, 1310), "AT 12 MIDNIGHT", self.f_caps, GOLD, ease((lt - .9) / .35))
        return img

    def look(self, t):
        span = (T_END - T_LOOKS) / len(self.looks)
        i = min(len(self.looks) - 1, int((t - T_LOOKS) / span))
        lt = t - T_LOOKS - i * span
        big = self.looks[i]
        z = 1.0 + .04 * (lt / span)
        cw, ch = int(W / z), int(H / z)
        x, y = (big.width - cw) // 2, (big.height - ch) // 2
        img = big.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BICUBIC).convert("RGBA")
        if lt < .12:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 250, 242, int(150 * (1 - lt / .12)))))
        # bottom ribbon: urgency (the top of a story sits under Instagram's own bar, and faces live there)
        rib = Image.new("RGBA", (W, 200), MAROON + (232,))
        dr = ImageDraw.Draw(rib)
        dr.line((0, 8, W, 8), fill=GOLD + (255,), width=2)
        spaced(dr, W / 2, 92, "LAST DAY · ENDS TONIGHT", self.f_rib, (255, 240, 222), 4)
        spaced(dr, W / 2, 144, "FLAT 20% OFF ON ALMOST EVERYTHING", self.f_small, (236, 204, 160), 3)
        img.alpha_composite(rib, (0, H - 260))
        return img

    def end(self, t):
        lt = t - T_END
        img = self.paper.copy()
        a = ease(lt / .3)
        lg = self.logo.copy()
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lg, ((W - lg.width) // 2, 230))
        y = 230 + self.logo.height + 120
        self.text(img, (W / 2, y), "Shop before midnight", self.f_it, MAROON, ease((lt - .1) / .3), dy=14)
        self.text(img, (W / 2, y + 80), "FLAT 20% OFF · LAST DAY", self.f_caps, INK, ease((lt - .2) / .3))
        # lower middle left clear for an Instagram link sticker
        self.text(img, (W / 2, 1600), "kalakaricreations.com", self.f_it_s, INK, ease((lt - .3) / .3))
        self.text(img, (W / 2, 1670), "CALL / WHATSAPP  +91 94081 14592", self.f_small, GOLD, ease((lt - .4) / .3))
        self.sparkles(img, t, W / 2, 200, 380, n=10, seed=11)
        return img

    def frame(self, t):
        if t < T_LOOKS:
            return self.intro(t)
        if t < T_END:
            return self.look(t)
        return self.end(t)


def music(seconds):
    """Soft electric piano with a gently ticking pulse underneath (a quiet clock-like tick on every beat)
    and soft chimes on 'LAST DAY', on the clock reaching midnight and on the end card."""
    sr = M.SR
    n = int((seconds + 3) * sr)
    keys, pad, bass, tick, chime = (np.zeros(n) for _ in range(5))
    beat = .5                                          # 120 BPM: a little urgency, still soft
    f = lambda semi: M.D3 * 2 ** (semi / 12)  # noqa: E731

    def epiano(fr, dur, amp):
        k = int(dur * sr)
        x = np.arange(k) / sr
        y = np.sin(2 * np.pi * fr * x) + .25 * np.sin(4 * np.pi * fr * x) * np.exp(-x * 3)
        y *= np.exp(-x * 1.6)
        y[: int(.008 * sr)] *= np.linspace(0, 1, int(.008 * sr))
        return y * M.env(k, 0, .2) * amp

    chords = [([-3, 0, 4, 7], -15), ([-5, -1, 2, 7], -17), ([0, 4, 7, 11], -12), ([-3, 2, 6, 9], -15)]
    t, b = 0.0, 0
    while t < seconds:
        semis, root = chords[b % 4]
        for s_ in semis:
            M.add(pad, M.pad_note(f(s_), beat * 4 + .6) * .45, t)
        k = int((beat * 4 + .4) * sr)
        M.add(bass, np.sin(2 * np.pi * f(root) * np.arange(k) / sr) * M.env(k, .04, .5) * .7, t)
        for e, idx in enumerate([0, 2, 1, 3, 2, 1, 3, 2]):
            M.add(keys, epiano(f(semis[idx] + 12), 1.1, .8 if e % 2 else .95), t + e * beat / 2)
        t += beat * 4
        b += 1
    k = int(.05 * sr)
    x = np.arange(k) / sr
    tk = np.sin(2 * np.pi * 1300 * x) * np.exp(-x * 120)
    tt = 0.0
    while tt < T_LOOKS:                                # ticking only under the intro and the countdown
        M.add(tick, tk * (.45 if int(tt / beat) % 2 == 0 else .3), tt)
        tt += beat
    for tc, semi in ((.8, 24), (T_OFFER + 2.0, 19), (T_END, 24)):
        k = int(2.0 * sr)
        x = np.arange(k) / sr
        M.add(chime, (np.sin(2 * np.pi * f(semi) * x) + .3 * np.sin(2 * np.pi * f(semi) * 2.01 * x))
              * np.exp(-x * 2.4) * .5, tc)
    mix = (.34 * M.lowpass(keys, 2000) + .3 * M.lowpass(pad, 900) + .3 * M.lowpass(bass, 400)
           + .07 * M.lowpass(tick, 3000) + .22 * M.lowpass(chime, 2200))
    mix = M.reverb(mix, seconds=2.0, mix=.25)[: int(seconds * sr)]
    mix *= M.env(len(mix), .4, 1.2)
    return (mix / (np.abs(mix).max() + 1e-9) * .8).astype(np.float32)


def main():
    fonts, out = sys.argv[1:3]
    s = Story(fonts)
    if len(sys.argv) > 3:
        for ts in sys.argv[3].split(","):
            s.frame(float(ts)).convert("RGB").resize((360, 640)).save(
                os.path.join(os.path.dirname(out), f"ld_{float(ts):05.2f}.png"))
        return
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "music.wav")
    a = music(TOTAL)
    sf.write(wav, np.stack([a, a], 1), M.SR)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-t", f"{TOTAL:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(int(TOTAL * FPS)):
        p.stdin.write(s.frame(k / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait():
        raise SystemExit("ffmpeg failed")
    shutil.rmtree(tmp, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
