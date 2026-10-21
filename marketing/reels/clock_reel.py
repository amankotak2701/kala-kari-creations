#!/usr/bin/env python3
"""~15 s 9:16 "pick your favourite" clock reel: a maroon clock hand ticks round the screen, one word per
tick, and a product cut-out pops in wherever it points. Ends with number badges ("comment the number")
and a website card. Original light, fun music (pizzicato melody, offbeat strums, dholak and claps).

Usage:
    python3 clock_reel.py <fonts_dir> <out.mp4>
"""
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import music as M  # noqa: E402

W, H, FPS = 1080, 1920, 30
BIG = 1.8                      # scene is drawn at this scale so the opening zoom stays sharp
BW, BH = int(W * BIG), int(H * BIG)
MAROON = (117, 44, 57)
GOLD = (190, 150, 80)
INK = (28, 22, 20)
CREAM = (247, 242, 233)
CUT = os.path.join(HERE, "cutouts")
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-maroon-flat.png")
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"

BEAT = 0.5                     # 120 BPM; the hand ticks every two beats
T0 = 0.5                       # first tick
CENTER = (540, 860)            # clock centre (1080x1920 space)
RX, RY = 345, 560              # product ellipse

# one product per clock position (12, 1:30, 3, 4:30, 6, 7:30, 9, 10:30); the words on ticks 5-7
# land on a matching product
PRODUCTS = ["muslin2piecechikankari", "yellowjaipuri3piece", "chikankari_2_piece_sky_blue",
            "parrotgreenjaipuriprint", "black3piececottondress", "maroonchikankarikurti",
            "blue3piececottonjaipuri", "ajrakhkali"]
WORDS = ["Which", "one", "is", "your", "pick?", "Chikankari,", "Jaipuri", "or Ajrakh?",
         "Comment", "the", "number", "below!"]
BADGE_TICK = 8                 # badges pop with "Comment"
END = T0 + len(WORDS) * 1.0 + .2
TOTAL = END + 3.4


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def back(t, s=1.9):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def paper():
    rng = np.random.default_rng(7)

    def noise(scale):
        small = rng.standard_normal((BH // scale + 2, BW // scale + 2)).astype(np.float32)
        im = Image.fromarray(((small - small.min()) / np.ptp(small) * 255).astype(np.uint8))
        return np.asarray(im.resize((BW, BH), Image.BICUBIC), np.float32) / 255 - .5

    relief = noise(40) * .6 + noise(12) * .3 + noise(4) * .15
    relief = np.asarray(Image.fromarray(((relief + .5).clip(0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), np.float32) / 255
    shade = np.zeros_like(relief)
    shade[1:, 1:] = (relief[1:, 1:] - relief[:-1, :-1]) * 6       # light from the top-left
    grain = rng.standard_normal((BH, BW)).astype(np.float32) * 2.2
    base = np.array([246, 243, 239], np.float32)
    img = base[None, None, :] + (shade * 40 + grain)[..., None]
    return Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert("RGBA")


def hand_image(length, width, ss=3):
    """Ornate clock hand pointing up, pivot at the bottom-centre of the returned image."""
    L, w = length * ss, width * ss
    pad = 22 * ss
    im = Image.new("RGBA", (w + 2 * pad, L + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, py = im.width / 2, L + pad            # pivot
    col = MAROON + (255,)
    d.line((cx, py, cx, pad + L * .12), fill=col, width=int(3.2 * ss))
    # arrow head
    tip = pad
    d.polygon([(cx, tip), (cx + w * .42, tip + L * .16), (cx, tip + L * .11), (cx - w * .42, tip + L * .16)], fill=col)
    # teardrop ornament along the shaft
    oy = py - L * .48
    d.polygon([(cx, oy - L * .14), (cx + w * .32, oy), (cx, oy + L * .06), (cx - w * .32, oy)], fill=col)
    d.ellipse((cx - w * .12, oy - L * .05, cx + w * .12, oy - L * .01), fill=(0, 0, 0, 0))
    # small ring near the pivot
    ry = py - L * .2
    r = w * .2
    d.ellipse((cx - r, ry - r, cx + r, ry + r), outline=col, width=int(3 * ss))
    # hub
    r = w * .26
    d.ellipse((cx - r, py - r, cx + r, py + r), fill=col)
    r = w * .1
    d.ellipse((cx - r, py - r, cx + r, py + r), fill=CREAM + (255,))
    # square canvas with the pivot in the middle so rotation never clips the hand
    side = 2 * int(py) + 2
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.alpha_composite(im, (int(side / 2 - cx), 0))
    sq = sq.resize((side // ss, side // ss), Image.LANCZOS)
    return sq, (sq.width / 2, py / ss)


class Reel:
    def __init__(self, fonts_dir):
        self.cor = lambda w, s: ImageFont.truetype(os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-normal.woff2"), s)
        self.cor_it = lambda w, s: ImageFont.truetype(os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-italic.woff2"), s)
        self.inter = lambda w, s: ImageFont.truetype(INTER.format(w), s)
        self.bg = paper()
        self.prods = []
        for k, name in enumerate(PRODUCTS):
            im = Image.open(os.path.join(CUT, name + ".png")).convert("RGBA")
            h = int(440 * BIG)
            im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
            if im.width > 330 * BIG:              # wide dupatta shots: cap the width
                f = 330 * BIG / im.width
                im = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
            sh.putalpha(im.getchannel("A").point(lambda v: int(v * .22)).filter(ImageFilter.GaussianBlur(10)))
            a = math.radians(45 * k)
            x, y = CENTER[0] + RX * math.sin(a), CENTER[1] - RY * math.cos(a)
            self.prods.append(dict(im=im, shadow=sh, x=x * BIG, y=y * BIG))
        self.min_hand = hand_image(int(215 * BIG), int(62 * BIG))
        self.hr_hand = hand_image(int(150 * BIG), int(54 * BIG))
        self.word_font = self.inter("Bold", int(46 * BIG))
        self.badge_font = self.inter("Bold", int(40 * BIG))
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo.resize((520, int(520 * logo.height / logo.width)), Image.LANCZOS)

    # ------------------------------------------------------------ scene pieces (BIG space)
    def paste_hand(self, img, hand, angle):
        im, (px, py) = hand
        rot = im.rotate(-angle, resample=Image.BICUBIC, center=(px, py))
        img.alpha_composite(rot, (int(CENTER[0] * BIG - px), int(CENTER[1] * BIG - py)))

    def product(self, img, k, t, appear):
        p = self.prods[k]
        a = clamp((t - appear) / .35)
        if a <= 0:
            return
        s = .55 + .45 * back(a)
        bob = math.sin((t - appear) * 2.2 + k) * 4 * BIG
        im, sh = p["im"], p["shadow"]
        if s != 1:
            size = (max(1, int(im.width * s)), max(1, int(im.height * s)))
            im, sh = im.resize(size, Image.BILINEAR), sh.resize(size, Image.BILINEAR)
        if a < 1:
            im = im.copy()
            im.putalpha(im.getchannel("A").point(lambda v: int(v * min(1, a * 2))))
        x, y = int(p["x"] - im.width / 2), int(p["y"] - im.height / 2 + bob)
        img.alpha_composite(sh, (x + int(10 * BIG), y + int(14 * BIG)))
        img.alpha_composite(im, (x, y))

    def badge(self, img, k, t, appear):
        a = clamp((t - appear) / .3)
        if a <= 0:
            return
        p = self.prods[k]
        r = 36 * BIG * back(a, 2.4)
        cx = p["x"] - p["im"].width / 2 + 10 * BIG
        cy = p["y"] - p["im"].height / 2 + 40 * BIG
        d = ImageDraw.Draw(img)
        d.ellipse((cx - r - 4 * BIG, cy - r - 4 * BIG, cx + r + 4 * BIG, cy + r + 4 * BIG), fill=CREAM + (255,))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=MAROON + (255,))
        if a > .5:
            d.text((cx, cy + 1 * BIG), str(k + 1), font=self.badge_font, fill=CREAM, anchor="mm")

    def word(self, img, text, angle, a):
        if a <= 0:
            return
        rad = math.radians(angle)
        dist = (215 + 14) * BIG
        x = CENTER[0] * BIG + dist * math.sin(rad)
        y = CENTER[1] * BIG - dist * math.cos(rad)
        tw = ImageDraw.Draw(img).textlength(text, font=self.word_font)
        th = 46 * BIG
        # anchor the word so it extends outward from the tip
        ax = (math.sin(rad) + 1) / 2
        ay = (1 - math.cos(rad)) / 2
        x0 = x - tw * (1 - ax) if abs(math.sin(rad)) > .3 else x - tw / 2
        y0 = y - th * (1 - ay) if abs(math.cos(rad)) > .3 else y - th / 2
        lay = Image.new("RGBA", (int(tw + 40 * BIG), int(th + 40 * BIG)), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((20 * BIG, 20 * BIG + th / 2), text, font=self.word_font, fill=INK, anchor="lm",
                                    stroke_width=int(5 * BIG), stroke_fill=(246, 243, 239))
        s = .7 + .3 * back(clamp(a * 1.6))
        if s != 1:
            lay = lay.resize((max(1, int(lay.width * s)), max(1, int(lay.height * s))), Image.BILINEAR)
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * clamp(a * 2))))
        cx, cy = x0 + tw / 2, y0 + th / 2
        img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

    def scene(self, t):
        img = self.bg.copy()
        ticks = [T0 + i * 1.0 for i in range(len(WORDS))]
        n = sum(1 for x in ticks if x <= t)
        for k in range(len(PRODUCTS)):
            if k < len(ticks):
                self.product(img, k, t, ticks[k])
        for k in range(len(PRODUCTS)):
            self.badge(img, k, t, ticks[BADGE_TICK] + .1 + k * .12)
        # minute hand: jumps 45 degrees per tick with a little overshoot
        if n == 0:
            ang = 0.0
        else:
            i = n - 1
            prev = 45.0 * (i - 1) if i > 0 else 0.0
            ang = prev + (45.0 * i - prev) * back((t - ticks[i]) / .22, 2.2)
        self.paste_hand(img, self.hr_hand, 0)
        self.paste_hand(img, self.min_hand, ang)
        if n:
            i = n - 1
            fade_out = 1 - clamp((t - END + .1) / .3)
            self.word(img, WORDS[i], 45.0 * i, clamp((t - ticks[i]) / .25) * fade_out)
        return img

    # ------------------------------------------------------------ camera + overlays (1080 space)
    def frame(self, t):
        sc = self.scene(t)
        # open tight on the 12 o'clock product, ease out to the full clock
        z = 1 + (BIG - 1) * (1 - ease((t - 1.6) / 3.2))
        fx = 540
        fy = 960 + (500 - 960) * (1 - ease((t - 1.6) / 3.2))
        cw, ch = W * BIG / z, H * BIG / z
        x0 = clamp(fx * BIG - cw / 2, 0, BW - cw)
        y0 = clamp(fy * BIG - ch / 2, 0, BH - ch)
        img = sc.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)
        d = ImageDraw.Draw(img)
        # website pill once the full clock is visible
        a = ease((t - 4.4) / .5) * (1 - ease((t - END) / .3))
        if a > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            f = self.inter("SemiBold", 38)
            txt = "kalakaricreations.com"
            tw = dl.textlength(txt, font=f)
            dl.rounded_rectangle((540 - tw / 2 - 40, 1760, 540 + tw / 2 + 40, 1844), radius=42, fill=MAROON)
            dl.text((540, 1802), txt, font=f, fill=CREAM, anchor="mm")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)
        if t >= END:
            img = self.end_card(img, t - END)
        return img

    def end_card(self, img, local):
        a = ease(local / .45)
        veil = Image.new("RGBA", (W, H), (246, 243, 239, int(150 * a)))
        img = img.filter(ImageFilter.GaussianBlur(6 * a)) if a > 0 else img
        img.alpha_composite(veil)
        card = Image.new("RGBA", (900, 1080), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle((0, 0, 899, 1079), radius=40, fill=CREAM + (255,), outline=GOLD + (255,), width=3)
        card.alpha_composite(self.logo, ((900 - self.logo.width) // 2, 70))
        c = 450

        def put(text, font, fill, y, start):
            b = ease((local - start) / .35)
            if b > 0:
                lay = Image.new("RGBA", card.size, (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((c, y + (1 - b) * 14), text, font=font, fill=fill, anchor="mm")
                lay.putalpha(lay.getchannel("A").point(lambda v: int(v * b)))
                card.alpha_composite(lay)

        put("Found your favourite?", self.cor_it(600, 80), MAROON, 330, .3)
        put("Chikankari · Jaipuri · Ajrakh · Tunics", self.inter("Regular", 34), INK, 440, .45)
        put("Shop now at", self.inter("Medium", 34), INK, 560, .6)
        put("kalakaricreations.com", self.inter("Bold", 58), MAROON, 630, .7)
        b = ease((local - .85) / .35)
        if b > 0:
            lay = Image.new("RGBA", card.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rounded_rectangle((c - 300, 720, c + 300, 810), radius=45, fill=MAROON)
            dl.text((c, 765), "Comment your number", font=self.inter("SemiBold", 36), fill=CREAM, anchor="mm")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * b)))
            card.alpha_composite(lay)
        put("Call / WhatsApp  +91 94081 14592", self.inter("Regular", 34), INK, 890, 1.0)
        put("@kalakaricreations27", self.inter("Medium", 34), MAROON, 960, 1.1)
        s = .9 + .1 * back(clamp(local / .45))
        card = card.resize((int(900 * s), int(1080 * s)), Image.BICUBIC)
        card.putalpha(card.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(card, ((W - card.width) // 2, (H - card.height) // 2 - 20))
        return img


# ------------------------------------------------------------------ music
def fun_track(path, seconds, ticks, end, seed=11):
    """Light, playful 120 BPM groove in D major (full major scale, no pentatonic runs, no bells):
    pizzicato melody, offbeat guitar-like strums, bouncy bass, dholak, claps, shaker and a woodblock
    tick on every move of the clock hand."""
    sr = M.SR
    rng = np.random.default_rng(seed)
    n = int((seconds + 2) * sr)
    mel, strum, bass, drums, sfx = (np.zeros(n) for _ in range(5))

    def pluck(f, dur, bright=1.0, decay=3.0):
        k = int(dur * sr)
        x = np.arange(k) / sr
        y = sum((bright ** h) / h * np.sin(2 * np.pi * f * h * x) * np.exp(-x * decay * (1 + .6 * h)) for h in range(1, 9))
        y[: int(.003 * sr)] *= np.linspace(0, 1, int(.003 * sr))
        return y

    def noise_hit(dur, cutoff, decay):
        k = int(dur * sr)
        x = np.arange(k) / sr
        return M.lowpass(rng.standard_normal(k), cutoff) * np.exp(-x * decay)

    def hp(x):
        return x - M.lowpass(x, 3000)

    D4 = M.D3 * 2
    f = lambda semi: D4 * 2 ** (semi / 12)  # noqa: E731
    chords = [[0, 4, 7], [-5, -1, 2, 7], [-3, 2, 6, 9], [-7, -3, 2, 7]]   # D  A  Bm  G
    roots = [-12, -17, -15, -19]
    melody = [  # (semitone from D4 or None, eighths)
        [(4, 1), (7, 1), (12, 1), (7, 1), (9, 1), (None, 1), (7, 1), (4, 1)],
        [(2, 1), (7, 1), (11, 1), (7, 1), (9, 1), (7, 1), (6, 1), (4, 1)],
        [(6, 1), (11, 1), (14, 1), (11, 1), (13, 1), (14, 1), (16, 1), (14, 1)],
        [(12, 1), (11, 1), (7, 1), (11, 1), (9, 2), (None, 2)],
    ]
    bar = BEAT * 4
    t = 0.0
    b = 0
    while t < end:
        ch = chords[b % 4]
        # offbeat strums
        for e in range(4):
            st = t + e * BEAT + BEAT / 2
            for j, s in enumerate(ch):
                M.add(strum, pluck(f(s), .22, .8, 9), st + j * .009)
        # bass: 1, and-of-2, 3
        for off, dur in ((0, .4), (1.5, .3), (2, .4), (3.5, .2)):
            semi = roots[b % 4] + (7 if off == 3.5 else 0)
            M.add(bass, pluck(f(semi), dur, .5, 4) * np.hanning(int(dur * sr) * 2)[int(dur * sr):][: int(dur * sr)], t + off * BEAT)
        # melody from bar 1 (the opening bar is groove only)
        if b >= 1:
            pos = t
            for semi, e in melody[(b - 1) % 4]:
                if semi is not None:
                    M.add(mel, pluck(f(semi), .35, .7, 6), pos)
                pos += e * BEAT / 2
        # dholak + claps + shaker
        for beat_i in range(4):
            bt = t + beat_i * BEAT
            if beat_i in (0, 2):
                k = int(.35 * sr)
                x = np.arange(k) / sr
                fr = 70 + 40 * np.exp(-x * 20)
                M.add(drums, np.sin(2 * np.pi * np.cumsum(fr) / sr) * np.exp(-x * 9) * 1.0, bt)
            else:
                M.add(drums, noise_hit(.18, 2200, 28) * .55, bt)                      # clap
                M.add(drums, noise_hit(.18, 2600, 30) * .4, bt + .012)
            M.add(drums, pluck(D4 * 1.5, .12, .6, 30) * .35, bt + BEAT * .75)          # dholak "ta"
            for s16 in range(4):
                M.add(drums, hp(noise_hit(.05, 9000, 90)) * (.22 if s16 % 2 else .12), bt + s16 * BEAT / 4)
        t += bar
        b += 1

    # woodblock tick on every hand move
    for tk in ticks:
        k = int(.06 * sr)
        x = np.arange(k) / sr
        click = (np.sin(2 * np.pi * 1700 * x) + .5 * np.sin(2 * np.pi * 2600 * x)) * np.exp(-x * 120)
        M.add(sfx, click * .8, tk)

    # end card: a bright strummed D chord, then the groove thins out under the card
    for j, s in enumerate([-12, -5, 0, 4, 7, 12]):
        M.add(strum, pluck(f(s), 2.5, .9, 1.4) * .8, end + j * .025)
    t = end + BEAT * 2
    while t < seconds:
        for e in range(4):
            for j, s in enumerate(chords[0]):
                M.add(strum, pluck(f(s), .22, .8, 9) * .6, t + e * BEAT + BEAT / 2 + j * .009)
            M.add(drums, hp(noise_hit(.05, 9000, 90)) * .15, t + e * BEAT + BEAT / 2)
        t += bar

    mix = .30 * mel + .20 * strum + .34 * M.lowpass(bass, 900) + .26 * drums + .30 * sfx
    mix = M.reverb(mix, seconds=1.2, mix=.14, seed=seed)[: int(seconds * sr)]
    mix *= M.env(len(mix), .05, 1.4)
    mix /= np.max(np.abs(mix)) + 1e-9
    mix = np.tanh(2.2 * mix) / np.tanh(2.2)          # gentle saturation: louder without harsh peaks
    mix *= 10 ** (-1.5 / 20)
    d = int(.01 * sr)
    left, right = mix, np.concatenate([np.zeros(d), mix[:-d]]) * .9 + mix * .1
    pcm = (np.stack([left, right], axis=1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main():
    fonts_dir, out = sys.argv[1:3]
    r = Reel(fonts_dir)
    wav = os.path.splitext(out)[0] + ".wav"
    ticks = [T0 + i * 1.0 for i in range(len(WORDS))]
    fun_track(wav, TOTAL, ticks, END)
    n = int(round(TOTAL * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-t", f"{TOTAL:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p",
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
    if len(sys.argv) > 3 and sys.argv[3] == "preview":
        r = Reel(sys.argv[1])
        for t in map(float, sys.argv[4:]):
            r.frame(t).convert("RGB").resize((360, 640)).save(os.path.join(sys.argv[2], f"clk_{t}.png"))
    else:
        main()
