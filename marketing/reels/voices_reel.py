#!/usr/bin/env python3
""""I know I should sleep… BUT THE VOICES IN MY HEAD GO" trend reel, rebuilt with our own artwork:
beige paper, maroon velvet arch, gold-outlined lotus, the same text timing, then 15 fast cuts of
Kala Kari products on the beat and a website end card in the same arch style.

Usage:
    python3 voices_reel.py <fonts_dir> <audio.wav> <out.mp4>
<audio.wav> is the trend's sound (6.5 s); it is extended under the end card.
"""
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
SRC = os.path.join(HERE, "..", "ads", "source-photos")
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-inverse.png")
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
GOLD = (214, 178, 102)
CREAM = (247, 242, 233)

TYPED = "I know I should sleep"
TYPE_END = .85
# word, appear time, left x, centre y (1080x1920)
WORDS = [("BUT", 1.10, 198, 372), ("THE", 1.533, 393, 490), ("VOICES", 1.933, 423, 820), ("IN", 2.233, 327, 943),
         ("MY", 2.533, 543, 1053), ("HEAD", 2.867, 303, 1218), ("GO", 3.267, 621, 1305)]
CUT0 = 3.433
CUTS = [3.433, 3.6, 3.767, 3.933, 4.133, 4.3, 4.467, 4.6, 4.8, 5.067, 5.267, 5.533, 5.733, 6.0, 6.2, 6.5]
# product photo, horizontal focal point
SHOTS = [("muslin2piecechikankari.jpg", .5), ("black3piececottondress.jpg", .5), ("chikankari_2_piece_sky_blue.jpg", .5),
         ("yellowjaipuri3piece.jpg", .42), ("maroonchikankarikurti.jpg", .52), ("blue3piececottonjaipuri.jpg", .45),
         ("navybluelucknowikurti.jpg", .52), ("babypinkjaipuriprint.jpg", .45), ("ajrakhkali.jpg", .5),
         ("greenchikankarikurti.jpg", .48), ("parrotgreenjaipuriprint.jpg", .42), ("lucknowikurtiwine.jpg", .5),
         ("brownjaipuriprint3piece.jpg", .42), ("redliningjaipuriprint.jpg", .42), ("jaipuripink3piece.jpg", .42)]
END_DUR = 3.2
TOTAL = CUTS[-1] + END_DUR

ARCH = (98, 52, 1002, 1710)      # x0, top, x1, bottom


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def cover(im, w, h, fx=.5, fy=.4, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = int(clamp(r.width * fx - w / 2, 0, r.width - w))
    y = int(clamp(r.height * fy - h / 2, 0, r.height - h))
    return r.crop((x, y, x + w, y + h))


def noise(rng, w, h, scale):
    small = rng.standard_normal((h // scale + 2, w // scale + 2)).astype(np.float32)
    im = Image.fromarray(((small - small.min()) / np.ptp(small) * 255).astype(np.uint8))
    return np.asarray(im.resize((w, h), Image.BICUBIC), np.float32) / 255 - .5


def paper():
    rng = np.random.default_rng(3)
    n = noise(rng, W, H, 60) * .5 + noise(rng, W, H, 14) * .3 + noise(rng, W, H, 3) * .25
    base = np.array([214, 205, 190], np.float32)
    img = base[None, None, :] + (n * 34 + rng.standard_normal((H, W)) * 3)[..., None]
    return Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert("RGBA")


def velvet():
    rng = np.random.default_rng(9)
    n = noise(rng, W, H, 160) * .6 + noise(rng, W, H, 50) * .5 + noise(rng, W, H, 12) * .25
    streak = np.asarray(Image.fromarray(((noise(rng, W, H, 6) + .5) * 255).clip(0, 255).astype(np.uint8))
                        .filter(ImageFilter.BoxBlur(1)).resize((W, H)), np.float32) / 255 - .5
    v = n * 1.0 + streak * .25
    base = np.array([96, 22, 34], np.float32)
    hi = np.array([150, 50, 64], np.float32)
    k = (v - v.min()) / np.ptp(v)
    img = base[None, None, :] * (1 - k[..., None] * .75) + hi[None, None, :] * (k[..., None] * .55)
    img = img * (.82 + .18 * k[..., None]) + rng.standard_normal((H, W, 1)) * 3
    return Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert("RGBA")


def arch_mask():
    x0, top, x1, bot = ARCH
    r = (x1 - x0) / 2
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((x0, top, x1, top + 2 * r), fill=255)
    d.rectangle((x0, top + r, x1, bot), fill=255)
    return m


def petal(cx, cy, length, width, angle, ss):
    """Pointed petal polygon from base (cx, cy), rotated by angle (deg, 0 = up)."""
    pts = []
    for i in range(41):
        t = i / 40
        y = -length * t
        w = width * math.sin(math.pi * t) ** .8 * (1 - .15 * t)
        pts.append((w, y))
    pts += [(-x, y) for x, y in reversed(pts)]
    a = math.radians(angle)
    return [((cx + x * math.cos(a) - y * math.sin(a)) * ss, (cy + x * math.sin(a) + y * math.cos(a)) * ss) for x, y in pts]


def lotus(width=760):
    ss = 3
    w, h = 800, 520
    im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 400, 420
    gold = (226, 196, 118, 255)
    layers = [  # (angles, length, width, fill)
        ([-112, 112], 330, 64, (118, 38, 54)),
        ([-88, 88], 330, 70, (134, 48, 64)),
        ([-64, 64], 330, 70, (148, 58, 74)),
        ([-42, 42], 335, 66, (160, 68, 84)),
        ([-21, 21], 330, 60, (172, 80, 94)),
        ([0], 340, 62, (184, 92, 104)),
        ([-140, 140], 220, 74, (126, 44, 60)),
        ([-165, 165], 170, 66, (140, 54, 70)),
    ]
    for angles, L, pw, fill in layers:
        for a in angles:
            poly = petal(cx, cy, L, pw, a, ss)
            d.polygon(poly, fill=fill + (255,))
            inner = petal(cx, cy - 10 * math.cos(math.radians(a)), L * .78, pw * .55, a, ss)
            d.polygon(inner, fill=tuple(min(255, c + 22) for c in fill) + (255,))
            d.line(poly + [poly[0]], fill=gold, width=4 * ss)
            d.line(inner + [inner[0]], fill=gold, width=2 * ss)
            ra = math.radians(a)
            for k in range(4, 14):                      # dotted midline
                t = k / 16
                px = cx + math.sin(ra) * L * t
                py = cy - math.cos(ra) * L * t
                r = 2.2
                d.ellipse(((px - r) * ss, (py - r) * ss, (px + r) * ss, (py + r) * ss), fill=gold)
    im = im.resize((w, h), Image.LANCZOS)
    # silver sticker edge + soft shadow
    a = im.getchannel("A")
    edge = a.filter(ImageFilter.MaxFilter(9))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (40, 20, 20, 0))
    sh.putalpha(edge.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * .45)))
    out.alpha_composite(sh, (0, 6))
    rim = Image.new("RGBA", (w, h), (196, 192, 186, 0))
    rim.putalpha(edge)
    out.alpha_composite(rim)
    out.alpha_composite(im)
    s = width / w
    return out.resize((int(w * s), int(h * s)), Image.LANCZOS)


class Reel:
    def __init__(self):
        bg = paper()
        vel = velvet()
        m = arch_mask()
        sh = Image.new("RGBA", (W, H), (30, 10, 10, 0))
        sh.putalpha(m.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * .35)))
        bg.alpha_composite(sh, (0, 8))
        bg.paste(vel, (0, 0), m)
        lt = lotus(760)
        bg.alpha_composite(lt, ((W - lt.width) // 2, 1610 - int(lt.height * .62)))
        self.base = bg
        self.small = ImageFont.truetype(INTER.format("SemiBold"), 47)
        self.big = ImageFont.truetype(INTER.format("Bold"), 100)
        self.shots = [cover(Image.open(os.path.join(SRC, n)).convert("RGB"), W, H, fx, .4).convert("RGBA") for n, fx in SHOTS]
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo.resize((640, int(640 * logo.height / logo.width)), Image.LANCZOS)

    def intro(self, t):
        img = self.base.copy()
        d = ImageDraw.Draw(img)
        n = int(len(TYPED) * clamp(t / TYPE_END) + .5)
        if n:
            a = 1 - clamp((t - 3.3) / .13)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).text((240, 666), TYPED[:n], font=self.small, fill=(255, 255, 255), anchor="lm")
            if a < 1:
                lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)
        for word, at, x, y in WORDS:
            if t >= at:
                d.text((x, y), word, font=self.big, fill=(255, 255, 255), anchor="lm")
        return img

    def shot(self, t):
        i = max(k for k in range(len(CUTS) - 1) if CUTS[k] <= t)
        local = t - CUTS[i]
        im = self.shots[i]
        z = 1 + .03 * local / (CUTS[i + 1] - CUTS[i])
        if z > 1.001:
            w2, h2 = int(W / z), int(H / z)
            im = im.crop(((W - w2) // 2, (H - h2) // 2, (W + w2) // 2, (H + h2) // 2)).resize((W, H), Image.BILINEAR)
        return im

    def end(self, t):
        img = self.base.copy()

        def put(text, font, fill, y, st):
            a = ease((t - st) / .35)
            if a > 0:
                lay = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((540, 70), text, font=font, fill=fill, anchor="mm")
                lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
                img.alpha_composite(lay, (0, int(y - 70 + (1 - a) * 14)))

        a = ease(t / .4)
        lg = self.logo.copy()
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lg, ((W - lg.width) // 2, 330))
        put("Chikankari · Jaipuri · Ajrakh", ImageFont.truetype(INTER.format("Medium"), 42), CREAM, 620, .2)
        put("SHOP NOW AT", ImageFont.truetype(INTER.format("Bold"), 64), (255, 255, 255), 790, .35)
        b = ease((t - .5) / .35)
        if b > 0:
            lay = Image.new("RGBA", (W, 160), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rounded_rectangle((130, 20, 950, 140), radius=60, fill=GOLD)
            dl.text((540, 80), "kalakaricreations.com", font=ImageFont.truetype(INTER.format("Bold"), 58), fill=(96, 22, 34), anchor="mm")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * b)))
            img.alpha_composite(lay, (0, int(860 + (1 - b) * 14)))
        put("Call / WhatsApp  +91 94081 14592", ImageFont.truetype(INTER.format("Medium"), 40), CREAM, 1110, .7)
        put("@kalakaricreations27", ImageFont.truetype(INTER.format("SemiBold"), 40), GOLD, 1180, .8)
        return img

    def frame(self, t):
        if t < CUT0:
            return self.intro(t)
        if t < CUTS[-1]:
            return self.shot(t)
        return self.end(t - CUTS[-1])


def build_audio(src, out, total):
    with wave.open(src) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, ch).astype(np.float32)
    n = int(total * sr)
    outbuf = np.zeros((n, ch), np.float32)
    outbuf[: min(n, len(a))] = a[:n]
    # under the end card: the beat section again, crossfaded in and faded out
    seg = a[int(CUT0 * sr): int(6.0 * sr)]
    start = int((CUTS[-1] - .08) * sr)
    xf = int(.08 * sr)
    while start < n:
        k = min(len(seg), n - start)
        piece = seg[:k].copy()
        piece[:min(xf, k)] *= np.linspace(0, 1, min(xf, k))[:, None]
        outbuf[start:start + k] += piece
        start += len(seg) - xf
    fo = int(1.6 * sr)
    outbuf[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    with wave.open(out, "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(outbuf.clip(-32768, 32767).astype("<i2").tobytes())


def main():
    _, audio, out = sys.argv[1:4]
    r = Reel()
    wav = os.path.splitext(out)[0] + ".wav"
    build_audio(audio, wav, TOTAL)
    n = int(round(TOTAL * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-t", f"{TOTAL:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        proc.stdin.write(r.frame(k / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    os.remove(wav)
    print(out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        r = Reel()
        for t in map(float, sys.argv[4:]):
            r.frame(t).convert("RGB").resize((360, 640)).save(os.path.join(sys.argv[3], f"v_{t:04.1f}.png"))
    else:
        main()
