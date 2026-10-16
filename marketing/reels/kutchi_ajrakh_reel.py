#!/usr/bin/env python3
"""Fast-cut 9:16 reel for the Ajrakh silk kurti with Kutchi work (~11.5 s, loops cleanly).

Structure tuned for retention: 1 s hook -> three punch-in detail cuts -> price -> NAV10
"last days" offer -> comment-for-link CTA. Native-style bold captions in the safe zone,
original soft Kutchi folk music (manjira, light dholak, flute, tanpura).

Usage:
    python3 kutchi_ajrakh_reel.py <fonts_dir> <photo.jpg> <out.mp4>
"""
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ads"))
sys.path.insert(0, HERE)
import make_ads as A  # noqa: E402
import music as M  # noqa: E402
import navratri_reel as N  # noqa: E402

W, H, FPS = 1080, 1920, 30
XF = 0.18
CREAM = (247, 242, 233)
GOLD = (226, 190, 110)
MAROON = (117, 44, 57)
INK = (22, 16, 14)
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-inverse.png")

# focal points / zooms on the 896x1176 product photo
SHOTS = [
    dict(kind="photo", dur=1.5, f=(.5, .42), z=(1.25, 1.0), top="This kurti was", big="printed by hand", sub="Ajrakh from Kutch"),
    dict(kind="photo", dur=1.25, f=(.5, .225), z=(2.0, 2.25), top="", big="Mirror work neckline", sub=""),
    dict(kind="photo", dur=1.25, f=(.35, .43), z=(2.0, 2.2), top="", big="Hand-block borders", sub=""),
    dict(kind="photo", dur=1.25, f=(.5, .66), z=(1.9, 2.1), top="", big="Paisley hem", sub=""),
    dict(kind="price", dur=2.1, f=(.5, .45), z=(1.0, 1.08)),
    dict(kind="offer", dur=2.3),
    dict(kind="cta", dur=2.4),
]


def ease(t):
    return A.ease(t)


def fade(t, s, d=.3):
    return ease((t - s) / d)


class Reel:
    def __init__(self, fonts_dir, photo):
        self.src = Image.open(photo).convert("RGB")
        self.inter = lambda w, s: ImageFont.truetype(INTER.format(w), s)
        cor = os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files")
        self.cor_it = lambda w, s: ImageFont.truetype(os.path.join(cor, f"cormorant-garamond-latin-{w}-italic.woff2"), s)
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo.resize((440, int(440 * logo.height / logo.width)), Image.LANCZOS)
        self.toran = N.toran()

    # native-looking caption: bold text on a soft dark pill, centred, top third
    def pill(self, img, y, text, font, fg=CREAM, bg=(0, 0, 0, 150), a=1.0, pad=(34, 18), pop=0.0):
        if a <= 0 or not text:
            return 0
        d0 = ImageDraw.Draw(img)
        tw = A.text_w(d0, text, font)
        asc, desc = font.getmetrics()
        bw, bh = tw + pad[0] * 2, asc + desc + pad[1] * 2
        lay = Image.new("RGBA", (int(bw) + 4, int(bh) + 4), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        dl.rounded_rectangle((0, 0, bw, bh), radius=22, fill=bg)
        A.draw_text(dl, (pad[0], pad[1] - 2), text, font, fg)
        s = 1 + pop * (1 - ease(a)) if pop else 1
        if s != 1:
            lay = lay.resize((int(lay.width * s), int(lay.height * s)), Image.BICUBIC)
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lay, (int((W - lay.width) / 2), int(y - (lay.height - bh) / 2)))
        return bh

    def photo(self, s, local):
        p = local / s["dur"]
        z0, z1 = s["z"]
        img = A.cover(self.src, W, H, s["f"][0], s["f"][1], z0 + (z1 - z0) * ease(p)).convert("RGBA")
        img.alpha_composite(A.gradient(W, 520, 120, 0, color=INK), (0, 0))
        return img

    def shot(self, i, local):
        s = SHOTS[i]
        k = s["kind"]
        if k == "photo":
            img = self.photo(s, local)
            y = 300
            if s["top"]:
                y += self.pill(img, y, s["top"], self.inter("SemiBold", 52), a=fade(local, 0, .15)) + 12
            self.pill(img, y, s["big"], self.inter("ExtraBold", 76 if s["top"] else 70),
                      fg=INK if s["top"] else CREAM, bg=GOLD + (245,) if s["top"] else (0, 0, 0, 160),
                      a=fade(local, .05, .2), pop=.25)
            if s["sub"]:
                self.pill(img, y + 140, s["sub"], self.inter("SemiBold", 44), a=fade(local, .35, .2))
            return img
        if k == "price":
            img = self.photo(s, local)
            img.alpha_composite(A.gradient(W, 900, 0, 220, color=INK), (0, H - 900))
            self.pill(img, 300, "Silk Ajrakh kurti with Kutchi work", self.inter("Bold", 48), a=fade(local, 0, .2))
            self.pill(img, 400, "only ₹1,450", self.inter("ExtraBold", 96), fg=INK, bg=GOLD + (250,), a=fade(local, .25, .25), pop=.35)
            self.pill(img, 560, "Limited stock", self.inter("SemiBold", 42), bg=(117, 44, 57, 220), a=fade(local, .7, .2))
            return img
        if k == "offer":
            img = Image.new("RGBA", (W, H), MAROON + (255,))
            img.alpha_composite(self.toran, (0, 0))
            d = ImageDraw.Draw(img)
            d.rectangle((36, 36, W - 36, H - 36), outline=GOLD, width=3)
            self.pill(img, 330, "NAVRATRI OFFER · LAST 3 DAYS", self.inter("Bold", 44), fg=INK, bg=GOLD + (255,), a=fade(local, 0, .2))
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            a = fade(local, .2, .3)
            A.draw_text(ImageDraw.Draw(lay), (W / 2, 480 + int((1 - a) * 40)), "10% OFF", self.inter("ExtraBold", 210), CREAM, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            a2 = fade(local, .5)
            dl = ImageDraw.Draw(lay)
            A.draw_text(dl, (W / 2, 760), "on orders above ₹3,000", self.cor_it(600, 78), GOLD, anchor="c")
            dl.rounded_rectangle((250, 900, 830, 1110), radius=20, outline=GOLD, width=4)
            A.draw_text(dl, (W / 2, 925), "USE CODE", self.inter("SemiBold", 36), CREAM, anchor="c")
            A.draw_text(dl, (W / 2, 975), "NAV10", self.inter("ExtraBold", 104), GOLD, anchor="c")
            A.draw_text(dl, (W / 2, 1170), "Ends 19 October", self.inter("SemiBold", 48), CREAM, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a2)))
            img.alpha_composite(lay)
            return img
        # CTA
        img = self.photo(dict(f=(.5, .42), z=(1.08, 1.0), dur=s["dur"]), local)
        img.alpha_composite(A.gradient(W, 1200, 0, 235, color=INK), (0, H - 1200))
        self.pill(img, 300, "Want it?", self.inter("ExtraBold", 80), a=fade(local, 0, .2))
        self.pill(img, 430, "Comment \"AJRAKH\" for the link", self.inter("ExtraBold", 60), fg=INK, bg=GOLD + (250,), a=fade(local, .2, .25), pop=.25)
        a = fade(local, .5)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        lay.alpha_composite(self.logo, ((W - self.logo.width) // 2, 1080))
        A.draw_text(dl, (W / 2, 1250), "kalakaricreations.com", self.inter("Bold", 54), GOLD, anchor="c")
        A.draw_text(dl, (W / 2, 1330), "WhatsApp +91 94081 14592", self.inter("SemiBold", 42), CREAM, anchor="c")
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lay)
        return img


# ------------------------------------------------------------------ music
def kutchi_track(path, seconds, seed=21):
    """Light, soft Kutchi folk feel: tanpura drone, manjira, gentle dholak and a flute line in Kafi."""
    sr = M.SR
    rng = np.random.default_rng(seed)
    n = int((seconds + 3) * sr)
    drone, flute, perc, pad = (np.zeros(n) for _ in range(4))
    beat = 60 / 96

    t = 0.0
    while t < seconds + 1:
        for f in (M.hz(-5), M.hz(0), M.hz(0), M.hz(-12)):
            M.add(drone, M.tanpura_pluck(f, 3.6), t)
            t += beat
    t = 0.0
    for ch in ([0, 7, 15], [-2, 5, 14], [-4, 3, 12], [-5, 2, 10]):
        if t > seconds:
            break
        for s_ in ch:
            M.add(pad, M.pad_note(M.hz(s_), beat * 8 + .6), t)
        t += beat * 8

    def manjira(dur=.9):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        x = sum(np.sin(2 * np.pi * f * tt) * a for f, a in ((2630, 1), (3970, .6), (5310, .35), (6890, .2)))
        return x * np.exp(-tt * 5.5) * .25

    def dholak(low=True, dur=.35):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        if low:
            f = 120 * np.exp(-tt * 8) + 70
            return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 11)
        return (np.sin(2 * np.pi * 420 * tt) * .5 + rng.standard_normal(m) * .25) * np.exp(-tt * 32)

    t = 0.0
    k = 0
    while t < seconds - .5:
        M.add(perc, manjira() * (1.0 if k % 2 == 0 else .55), t)
        if t > beat * 2:
            M.add(perc, dholak(True) * .55, t) if k % 4 in (0, 3) else M.add(perc, dholak(False) * .35, t + beat * .5)
        t += beat
        k += 1

    def flute_note(f, dur):
        m = int(dur * sr)
        tt = np.arange(m) / sr
        vib = 1 + .007 * np.sin(2 * np.pi * 5.4 * tt) * np.minimum(tt / .25, 1)
        ph = 2 * np.pi * np.cumsum(f * vib) / sr
        x = np.sin(ph) + .2 * np.sin(2 * ph) + .05 * np.sin(3 * ph)
        return (x + rng.standard_normal(m) * .025) * M.env(m, .06, min(.22, dur * .4))

    kafi = [0, 2, 3, 5, 7, 9, 10, 12, 14, 15]
    notes = [M.hz(s_ + 12) for s_ in kafi]
    phrase = [4, 5, 6, 5, 4, 3, 4, 2, 3, 4, 7, 6, 5, 4, 3, 2, 3, 1, 2]
    t = beat * 1.0
    i = 0
    while t < seconds - 1.2:
        d_ = beat * [1, .5, .5, 1, 1.5, .5][i % 6]
        M.add(flute, flute_note(notes[phrase[i % len(phrase)]], d_ * 1.1), t)
        t += d_
        i += 1

    mix = .24 * M.lowpass(drone, 2400) + .2 * M.lowpass(pad, 1300) + .3 * M.lowpass(flute, 3600) + .26 * perc
    mix = M.reverb(mix, seconds=1.8, mix=.2, seed=seed)[: int(seconds * sr)]
    mix *= M.env(len(mix), .3, 1.2)
    mix *= 10 ** (-3 / 20) / (np.max(np.abs(mix)) + 1e-9)
    d = int(.011 * sr)
    left, right = mix, np.concatenate([np.zeros(d), mix[:-d]]) * .95 + mix * .05
    pcm = (np.stack([left, right], axis=1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main():
    fonts_dir, photo, out = sys.argv[1:4]
    r = Reel(fonts_dir, photo)
    starts, t = [], 0.0
    for s in SHOTS:
        starts.append(t)
        t += s["dur"] - XF
    total = t + XF
    n = int(round(total * FPS))
    wav = os.path.join(tempfile.mkdtemp(), "kutchi.wav")
    kutchi_track(wav, n / FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        tt = k / FPS
        act = [i for i, s in enumerate(SHOTS) if starts[i] <= tt < starts[i] + s["dur"]]
        if len(act) == 1:
            fr = r.shot(act[0], tt - starts[act[0]])
        else:
            i, j = act[-2], act[-1]
            fr = Image.blend(r.shot(i, tt - starts[i]), r.shot(j, tt - starts[j]), ease((tt - starts[j]) / XF))
        proc.stdin.write(fr.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    print(out, f"{total:.1f}s")


if __name__ == "__main__":
    main()
