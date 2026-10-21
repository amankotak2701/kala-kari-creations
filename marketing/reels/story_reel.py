#!/usr/bin/env python3
"""~32 s 9:16 cartoon story reel: two friends (Riya & Priya) are let down by a big fashion store and a
shopping app (both fictional, unnamed brands), find Kala Kari Creations, order, love it, and it becomes
their fashion destination. Flat-vector characters drawn in Pillow, real product photos for the Kala Kari
parts, original music that follows the mood, plus small sound effects.

Usage:
    python3 story_reel.py <fonts_dir> <out.mp4>
    python3 story_reel.py <fonts_dir> <out_dir> preview t1 t2 ...
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
XF = .3
MAROON = (117, 44, 57)
GOLD = (214, 178, 102)
CREAM = (247, 242, 233)
INK = (40, 30, 34)
SRC = os.path.join(HERE, "..", "ads", "source-photos")
CUT = os.path.join(HERE, "cutouts")
LOGO_DIR = os.path.join(HERE, "..", "..", "brand", "logo")
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# scene name, duration
SCENES = [("intro", 3.6), ("store", 4.8), ("app", 5.4), ("sad", 2.8), ("found", 3.8),
          ("order", 3.8), ("unbox", 4.2), ("dest", 3.0), ("end", 3.6)]
STARTS = []
_t = 0.0
for _n, _d in SCENES:
    STARTS.append(_t)
    _t += _d - XF
TOTAL = _t + XF
START = {n: s for (n, _), s in zip(SCENES, STARTS)}


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def back(t, s=1.8):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


# ------------------------------------------------------------------ text with colour emoji
class Text:
    def __init__(self):
        self.emoji = ImageFont.truetype(EMOJI, 109)
        self.fonts = {}
        self.cache = {}

    def font(self, w, s):
        k = (w, s)
        if k not in self.fonts:
            self.fonts[k] = ImageFont.truetype(INTER.format(w), s)
        return self.fonts[k]

    @staticmethod
    def is_emoji(c):
        o = ord(c)
        return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or o in (0x2B50, 0x2764)

    def line(self, text, weight, size, color):
        k = (text, weight, size, color)
        if k in self.cache:
            return self.cache[k]
        f = self.font(weight, size)
        runs, cur = [], ""
        for c in text:
            if c in "️‍":
                continue
            if self.is_emoji(c):
                if cur:
                    runs.append(("t", cur))
                    cur = ""
                runs.append(("e", c))
            else:
                cur += c
        if cur:
            runs.append(("t", cur))
        es = int(size * 1.15)
        parts = []
        for kind, s in runs:
            if kind == "t":
                w = int(f.getlength(s)) + 2
                im = Image.new("RGBA", (w, int(size * 1.5)), (0, 0, 0, 0))
                ImageDraw.Draw(im).text((0, size * .75), s, font=f, fill=color, anchor="lm")
            else:
                im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
                ImageDraw.Draw(im).text((0, 0), s, font=self.emoji, embedded_color=True)
                bb = im.getbbox() or (0, 0, 1, 1)
                im = im.crop(bb).resize((es, int(es * (bb[3] - bb[1]) / max(1, bb[2] - bb[0]))), Image.LANCZOS)
                pad = Image.new("RGBA", (es + 6, int(size * 1.5)), (0, 0, 0, 0))
                pad.alpha_composite(im, (3, max(0, (pad.height - im.height) // 2)))
                im = pad
            parts.append(im)
        w = sum(p.width for p in parts) or 1
        out = Image.new("RGBA", (w, int(size * 1.5)), (0, 0, 0, 0))
        x = 0
        for p in parts:
            out.alpha_composite(p, (x, 0))
            x += p.width
        self.cache[k] = out
        return out

    def block(self, text, weight, size, color, max_w, align="c", spacing=1.08):
        lines = []
        for para in text.split("\n"):
            words, cur = para.split(" "), ""
            for wd in words:
                trial = (cur + " " + wd).strip()
                if self.line(trial, weight, size, color).width > max_w and cur:
                    lines.append(cur)
                    cur = wd
                else:
                    cur = trial
            lines.append(cur)
        ims = [self.line(s, weight, size, color) for s in lines]
        lh = int(size * 1.5 * spacing * .85)
        w = max(i.width for i in ims)
        out = Image.new("RGBA", (w, lh * (len(ims) - 1) + ims[-1].height), (0, 0, 0, 0))
        for i, im in enumerate(ims):
            x = (w - im.width) // 2 if align == "c" else 0
            out.alpha_composite(im, (x, i * lh))
        return out


def fade_img(im, a):
    if a >= 1:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im


def scaled(im, s):
    if abs(s - 1) < 1e-3:
        return im
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)


# ------------------------------------------------------------------ characters
RIYA = dict(name="riya", hair="long", skin=(196, 138, 104), hair_col=(34, 22, 20), bindi=True,
            kurti=(46, 139, 140), pattern="plain", pcol=(255, 255, 255), pants=(236, 226, 205), dupatta=None)
PRIYA = dict(name="priya", hair="bun", skin=(226, 172, 138), hair_col=(52, 32, 26), bindi=False,
             kurti=(176, 150, 214), pattern="plain", pcol=(255, 255, 255), pants=(64, 60, 92), dupatta=None)
RIYA_KK = dict(RIYA, name="riya_kk", kurti=(128, 28, 40), pattern="chikan", pcol=(250, 246, 238), pants=(128, 28, 40))
PRIYA_KK = dict(PRIYA, name="priya_kk", kurti=(244, 220, 92), pattern="jaipuri", pcol=(200, 70, 60), pants=(244, 220, 92),
                dupatta=(250, 236, 150))

SS = 3
GW, GH = 500, 920


def arm_points(sx, sy, side, a, b, l1=118, l2=112):
    ra, rb = math.radians(a), math.radians(a + b)
    ex, ey = sx + side * l1 * math.sin(ra), sy + l1 * math.cos(ra)
    hx, hy = ex + side * l2 * math.sin(rb), ey + l2 * math.cos(rb)
    return (ex, ey), (hx, hy)


POSES = {  # (right-arm a, b), (left-arm a, b)  -- right arm is on the viewer's left
    "idle": ((10, -6), (10, -6)),
    "phone": ((10, -128), (10, -128)),
    "hips": ((38, -112), (38, -112)),
    "cheer": ((158, 8), (158, 8)),
    "point": ((10, -6), (78, 4)),
    "clasp": ((14, -60), (14, -60)),
    "shrug": ((52, 70), (52, 70)),
}


def draw_girl(spec, expr="happy", pose="idle", wave=0.0, blink=False):
    s = SS
    im = Image.new("RGBA", (GW * s, GH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def P(*pts):
        return [(x * s, y * s) for x, y in pts]

    def E(x0, y0, x1, y1):
        return (x0 * s, y0 * s, x1 * s, y1 * s)

    skin, hair, kc = spec["skin"], spec["hair_col"], spec["kurti"]
    shade = mix(kc, (0, 0, 0), .18)
    cx = 250
    # hair behind
    if spec["hair"] == "long":
        d.polygon(P((158, 170), (342, 170), (360, 470), (330, 500), (170, 500), (140, 470)), fill=hair)
    d.ellipse(E(160, 92, 340, 300), fill=hair)
    if spec["hair"] == "bun":
        d.ellipse(E(205, 40, 295, 120), fill=hair)
        d.ellipse(E(214, 96, 286, 112), fill=(200, 60, 80))   # scrunchie
    # legs (palazzo) + feet
    d.polygon(P((178, 620), (322, 620), (346, 868), (154, 868)), fill=spec["pants"])
    d.line(P((250, 660), (250, 866)), fill=mix(spec["pants"], (0, 0, 0), .15), width=3 * s)
    for fx in (200, 300):
        d.ellipse(E(fx - 32, 860, fx + 32, 888), fill=mix(skin, (0, 0, 0), .1))
        d.rectangle(E(fx - 30, 866, fx + 30, 874), fill=(150, 90, 60))
    # neck
    d.rectangle(E(232, 262, 268, 320), fill=mix(skin, (0, 0, 0), .08))
    # kurti
    body = P((178, 312), (322, 312), (352, 420), (378, 668), (122, 668), (148, 420))
    d.polygon(body, fill=kc)
    d.polygon(P((178, 312), (322, 312), (330, 336), (170, 336)), fill=kc)
    # pattern
    if spec["pattern"] != "plain":
        pat = Image.new("RGBA", im.size, (0, 0, 0, 0))
        pd = ImageDraw.Draw(pat)
        pc = spec["pcol"]
        if spec["pattern"] == "chikan":
            for yy in range(328, 420, 16):                       # dense yoke embroidery
                for xx in range(196, 306, 16):
                    r = 4
                    pd.ellipse(E(xx - r, yy - r, xx + r, yy + r), outline=pc, width=2 * s)
            for j, yy in enumerate(range(450, 660, 52)):           # floral buttis
                for xx in range(150 + (j % 2) * 30, 360, 60):
                    for k in range(5):
                        an = k * 72
                        px, py = xx + 8 * math.sin(math.radians(an)), yy - 8 * math.cos(math.radians(an))
                        pd.ellipse(E(px - 4.5, py - 4.5, px + 4.5, py + 4.5), fill=pc)
                    pd.ellipse(E(xx - 3, yy - 3, xx + 3, yy + 3), fill=kc)
            pd.rectangle(E(110, 640, 390, 668), fill=pc)
            for xx in range(120, 390, 14):
                pd.ellipse(E(xx - 4, 650, xx + 4, 658), fill=kc)
        else:  # jaipuri block print
            for j, yy in enumerate(range(340, 640, 40)):
                for xx in range(140 + (j % 2) * 22, 370, 44):
                    pd.ellipse(E(xx - 7, yy - 7, xx + 7, yy + 7), fill=pc)
                    pd.ellipse(E(xx - 3, yy - 3, xx + 3, yy + 3), fill=(250, 240, 200))
                    pd.ellipse(E(xx + 6, yy + 4, xx + 14, yy + 10), fill=(70, 130, 80))
            pd.rectangle(E(110, 628, 390, 668), fill=pc)
            for xx in range(116, 390, 20):
                pd.polygon(P((xx, 668), (xx + 10, 640), (xx + 20, 668)), fill=(250, 220, 90))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon(body, fill=255)
        pat.putalpha(Image.fromarray(np.minimum(np.asarray(pat.getchannel("A")), np.asarray(mask))))
        im.alpha_composite(pat)
        d = ImageDraw.Draw(im)
    # neckline
    d.polygon(P((226, 312), (274, 312), (250, 356)), fill=mix(skin, (0, 0, 0), .08))
    d.line(P((226, 312), (250, 356), (274, 312)), fill=shade, width=4 * s)
    # dupatta over the left shoulder
    if spec["dupatta"]:
        d.polygon(P((292, 306), (330, 312), (368, 640), (330, 660)), fill=spec["dupatta"])
        d.line(P((330, 312), (368, 640)), fill=spec["pcol"], width=6 * s)
    # arms
    (ra, rb), (la, lb) = POSES.get(pose, POSES["idle"])
    if pose == "wave":
        (ra, rb), (la, lb) = (10, -6), (150, -30 + 30 * math.sin(wave))
    for side, sx, a, b in ((-1, 176, ra, rb), (1, 324, la, lb)):
        (ex, ey), (hx, hy) = arm_points(sx, 326, side, a, b)
        mx, my = lerp(ex, hx, .45), lerp(ey, hy, .45)
        d.line(P((sx, 326), (ex, ey)), fill=kc, width=38 * s)
        d.ellipse(E(ex - 19, ey - 19, ex + 19, ey + 19), fill=kc)
        d.line(P((mx, my), (hx, hy)), fill=skin, width=27 * s)
        d.line(P((ex, ey), (mx, my)), fill=kc, width=34 * s)
        d.ellipse(E(sx - 21, 326 - 21, sx + 21, 326 + 21), fill=kc)
        d.ellipse(E(hx - 17, hy - 17, hx + 17, hy + 17), fill=skin)
        d.line(P((lerp(ex, hx, .43), lerp(ey, hy, .43)), (lerp(ex, hx, .47), lerp(ey, hy, .47))), fill=GOLD, width=30 * s)
    if pose == "phone":
        (_, _), (h1x, h1y) = arm_points(176, 326, -1, 10, -128)
        (_, _), (h2x, h2y) = arm_points(324, 326, 1, 10, -128)
        px, py = (h1x + h2x) / 2, (h1y + h2y) / 2 - 20
        d.rounded_rectangle(E(px - 30, py - 50, px + 30, py + 50), radius=8 * s, fill=(30, 30, 40))
        d.rounded_rectangle(E(px - 25, py - 44, px + 25, py + 44), radius=5 * s, fill=(120, 190, 240))
        for hx in (h1x, h2x):
            d.ellipse(E(hx - 17, h1y - 17, hx + 17, h1y + 17), fill=skin)
    # head
    d.ellipse(E(172, 104, 328, 284), fill=skin)
    d.ellipse(E(162, 180, 182, 214), fill=skin)
    d.ellipse(E(318, 180, 338, 214), fill=skin)
    for ex_ in (172, 328):                                   # jhumkas
        d.ellipse(E(ex_ - 6, 212, ex_ + 6, 224), fill=GOLD)
        d.polygon(P((ex_ - 10, 238), (ex_, 222), (ex_ + 10, 238)), fill=GOLD)
    # hair front
    if spec["hair"] == "long":
        d.chord(E(164, 92, 336, 250), 180, 360, fill=hair)
        d.polygon(P((250, 96), (326, 150), (334, 210), (300, 140)), fill=hair)
        d.polygon(P((250, 96), (176, 150), (168, 230), (196, 140)), fill=hair)
    else:
        d.chord(E(166, 94, 334, 238), 180, 360, fill=hair)
        d.polygon(P((190, 150), (230, 120), (300, 120), (318, 170), (270, 140), (220, 150)), fill=hair)
    # face
    ey0 = 196
    for ex_ in (216, 284):
        if blink or expr == "love":
            if expr == "love":
                hx_, hy_ = ex_, ey0
                d.ellipse(E(hx_ - 14, hy_ - 12, hx_ + 1, hy_ + 3), fill=(225, 50, 80))
                d.ellipse(E(hx_ - 1, hy_ - 12, hx_ + 14, hy_ + 3), fill=(225, 50, 80))
                d.polygon(P((hx_ - 14, hy_ - 3), (hx_ + 14, hy_ - 3), (hx_, hy_ + 14)), fill=(225, 50, 80))
            else:
                d.arc(E(ex_ - 14, ey0 - 8, ex_ + 14, ey0 + 10), 20, 160, fill=INK, width=4 * s)
        else:
            big = 1.25 if expr == "shock" else 1.0
            d.ellipse(E(ex_ - 14 * big, ey0 - 16 * big, ex_ + 14 * big, ey0 + 16 * big), fill=(255, 255, 255))
            d.ellipse(E(ex_ - 9, ey0 - 11, ex_ + 9, ey0 + 11), fill=(50, 32, 28))
            d.ellipse(E(ex_ - 4, ey0 - 8, ex_ + 2, ey0 - 2), fill=(255, 255, 255))
            d.line(P((ex_ - 16, ey0 - 14), (ex_ - 6, ey0 - 18), (ex_ + 12, ey0 - 16)), fill=INK, width=3 * s)
    # brows
    by = 166
    for ex_, sg in ((216, -1), (284, 1)):
        if expr == "sad":
            d.line(P((ex_ - 16, by + 2 * sg * 0 + 6), (ex_ + 16 * 1, by - 6)) if sg < 0 else P((ex_ - 16, by - 6), (ex_ + 16, by + 6)), fill=hair, width=5 * s)
        elif expr == "annoyed":
            d.line(P((ex_ - 16, by - 6), (ex_ + 16, by + 4)) if sg < 0 else P((ex_ - 16, by + 4), (ex_ + 16, by - 6)), fill=hair, width=6 * s)
        elif expr == "shock":
            d.arc(E(ex_ - 18, by - 22, ex_ + 18, by + 4), 200, 340, fill=hair, width=5 * s)
        else:
            d.arc(E(ex_ - 18, by - 14, ex_ + 18, by + 8), 210, 330, fill=hair, width=5 * s)
    # nose, blush, bindi
    d.arc(E(244, 210, 258, 232), 300, 60, fill=mix(skin, (0, 0, 0), .3), width=3 * s)
    if expr in ("happy", "love", "grin"):
        for bx in (198, 302):
            d.ellipse(E(bx - 16, 222, bx + 16, 236), fill=mix(skin, (240, 110, 120), .45))
    if spec["bindi"]:
        d.ellipse(E(245, 166, 255, 176), fill=(200, 30, 50))
    # mouth
    lip = (175, 60, 70)
    if expr in ("happy", "love"):
        d.chord(E(226, 230, 274, 266), 0, 180, fill=lip)
        d.chord(E(232, 232, 268, 246), 0, 180, fill=(255, 255, 255))
    elif expr == "grin":
        d.chord(E(218, 226, 282, 274), 0, 180, fill=lip)
        d.chord(E(224, 228, 276, 246), 0, 180, fill=(255, 255, 255))
    elif expr == "sad":
        d.arc(E(230, 248, 270, 274), 200, 340, fill=lip, width=5 * s)
    elif expr == "shock":
        d.ellipse(E(238, 238, 262, 270), fill=lip)
    elif expr == "annoyed":
        d.line(P((232, 254), (268, 250)), fill=lip, width=5 * s)
    else:
        d.arc(E(232, 236, 268, 258), 20, 160, fill=lip, width=5 * s)
    return im.resize((GW, GH), Image.LANCZOS)


class Cast:
    def __init__(self):
        self.cache = {}

    def get(self, spec, expr, pose, wave=0.0, blink=False):
        q = round((wave % (2 * math.pi)) / (2 * math.pi) * 10) % 10 if pose == "wave" else 0
        k = (spec["name"], expr, pose, q, blink)
        if k not in self.cache:
            self.cache[k] = draw_girl(spec, expr, pose, q / 10 * 2 * math.pi, blink)
        return self.cache[k]


def blinking(t, seed):
    return (t * 1.0 + seed * .37) % 3.1 < .12


# ------------------------------------------------------------------ backgrounds
def grad(c1, c2, w=W, h=H):
    g = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(c1)[None, None, :] * (1 - g) + np.array(c2)[None, None, :] * g
    return Image.fromarray(np.repeat(arr, w, axis=1).astype(np.uint8)).convert("RGBA")


def bg_room(wall1=(252, 228, 222), wall2=(246, 206, 200)):
    im = grad(wall1, wall2)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1480, W, H), fill=(214, 168, 124))
    for x in range(-200, W + 200, 160):
        d.line((x, 1480, x - 120, H), fill=(196, 150, 108), width=4)
    d.rectangle((0, 1470, W, 1490), fill=(255, 255, 255))
    # window
    d.rounded_rectangle((620, 360, 960, 800), radius=16, fill=(255, 255, 255))
    d.rectangle((640, 380, 940, 780), fill=(176, 222, 246))
    d.ellipse((700, 430, 800, 530), fill=(255, 238, 170))
    d.rectangle((785, 380, 795, 780), fill=(255, 255, 255))
    d.rectangle((640, 575, 940, 585), fill=(255, 255, 255))
    # frame + plant
    d.rectangle((140, 430, 400, 640), fill=(255, 255, 255))
    d.rectangle((158, 448, 382, 622), fill=(234, 180, 120))
    d.polygon([(170, 610), (240, 520), (290, 580), (330, 540), (372, 610)], fill=(176, 110, 70))
    d.polygon([(90, 1470), (180, 1470), (166, 1360), (104, 1360)], fill=(200, 110, 80))
    for k, (lx, ly) in enumerate(((80, 1220), (135, 1180), (190, 1230), (110, 1270), (165, 1280))):
        d.ellipse((lx - 30, ly - 60, lx + 30, ly + 60), fill=(70, 150, 90) if k % 2 else (90, 170, 100))
    return im


def bg_store():
    im = grad((246, 240, 230), (232, 222, 206))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1480, W, H), fill=(220, 214, 206))
    for x in range(0, W, 120):
        d.line((x, 1480, x, H), fill=(204, 198, 190), width=3)
    d.line((0, 1700, W, 1700), fill=(204, 198, 190), width=3)
    # big sign (fictional)
    d.rounded_rectangle((90, 300, 990, 470), radius=20, fill=(30, 40, 70))
    f = ImageFont.truetype(INTER.format("Black"), 74)
    d.text((540, 385), "BIG FASHION STORE", font=f, fill=(255, 214, 90), anchor="mm")
    for x in range(110, 990, 60):
        d.ellipse((x - 6, 312, x + 6, 324), fill=(255, 230, 150))
    # shelves with folded clothes
    cols = [(220, 90, 90), (90, 120, 200), (240, 190, 80), (120, 180, 140), (200, 120, 190), (90, 90, 90)]
    for row, y in enumerate((620, 800)):
        d.rectangle((60, y, 1020, y + 16), fill=(150, 110, 80))
        for k, x in enumerate(range(80, 1000, 110)):
            c = cols[(k + row) % len(cols)]
            for j in range(3):
                d.rounded_rectangle((x, y - 30 - j * 30, x + 90, y - 4 - j * 30), radius=6, fill=mix(c, (255, 255, 255), j * .12))
    # rack
    d.line((60, 960, 1020, 960), fill=(120, 120, 130), width=10)
    for k, x in enumerate(range(110, 1000, 120)):
        c = cols[k % len(cols)]
        d.arc((x - 16, 950, x + 16, 990), 180, 360, fill=(120, 120, 130), width=5)
        d.polygon([(x - 40, 990), (x + 40, 990), (x + 56, 1180), (x - 56, 1180)], fill=c)
    # sale tags
    d.rounded_rectangle((760, 520, 980, 590), radius=10, fill=(220, 40, 50))
    d.text((870, 555), "NEW SEASON", font=ImageFont.truetype(INTER.format("Bold"), 30), fill=(255, 255, 255), anchor="mm")
    return im


def bg_bedroom():
    im = grad((232, 226, 250), (214, 206, 240))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1480, W, H), fill=(190, 160, 140))
    d.rectangle((0, 1470, W, 1490), fill=(255, 255, 255))
    d.rounded_rectangle((60, 1100, 560, 1480), radius=30, fill=(250, 250, 255))
    d.rounded_rectangle((40, 980, 120, 1480), radius=20, fill=(160, 120, 180))
    d.rounded_rectangle((90, 1060, 300, 1160), radius=40, fill=(255, 220, 230))
    d.rectangle((60, 1260, 560, 1480), fill=(170, 140, 210))
    d.rounded_rectangle((700, 340, 980, 760), radius=16, fill=(255, 255, 255))
    d.rectangle((720, 360, 960, 740), fill=(186, 220, 250))
    d.rectangle((835, 360, 845, 740), fill=(255, 255, 255))
    d.ellipse((860, 1180, 1000, 1240), fill=(120, 90, 150))
    d.rectangle((920, 1240, 940, 1470), fill=(120, 90, 150))
    d.polygon([(860, 1180), (1000, 1180), (970, 1090), (890, 1090)], fill=(255, 220, 140))
    return im


def bg_night():
    im = grad((52, 60, 98), (70, 76, 118))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1480, W, H), fill=(80, 64, 70))
    d.rounded_rectangle((640, 330, 980, 780), radius=16, fill=(90, 96, 140))
    d.rectangle((660, 350, 960, 760), fill=(30, 36, 66))
    d.ellipse((860, 390, 920, 450), fill=(240, 240, 210))
    d.rectangle((805, 350, 815, 760), fill=(90, 96, 140))
    # sofa behind the girls
    d.rounded_rectangle((60, 1130, 1020, 1480), radius=50, fill=(120, 70, 90))
    d.rounded_rectangle((100, 1060, 980, 1260), radius=50, fill=(140, 84, 104))
    return im


def bg_burst(t, c1=(255, 236, 190), c2=(250, 200, 120)):
    im = Image.new("RGBA", (W, H), c1 + (255,))
    d = ImageDraw.Draw(im)
    cx, cy = 540, 860
    for k in range(18):
        a0 = math.radians(k * 20 + t * 14)
        a1 = a0 + math.radians(10)
        R = 2200
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=c2)
    return im


# ------------------------------------------------------------------ props
def kurti_prop(color, faded=False, w=300):
    s = 2
    im = Image.new("RGBA", (w * s, int(w * 1.5) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = w * s / 300

    def P(*pts):
        return [(x * k, y * k) for x, y in pts]
    d.arc(P((130, 0), (170, 40))[0] + P((130, 0), (170, 40))[1], 180, 360, fill=(120, 120, 130), width=int(5 * k))
    d.line(P((150, 20), (150, 40)), fill=(120, 120, 130), width=int(5 * k))
    d.polygon(P((60, 70), (150, 40), (240, 70), (290, 160), (250, 180), (240, 130), (262, 440), (38, 440), (60, 130), (50, 180), (10, 160)), fill=color)
    d.polygon(P((130, 50), (170, 50), (150, 90)), fill=(0, 0, 0, 0))
    if faded:
        rng = np.random.default_rng(3)
        for _ in range(26):
            x, y = rng.uniform(60, 240), rng.uniform(90, 420)
            r = rng.uniform(14, 40)
            d.ellipse(P((x - r, y - r * .7), (x + r, y + r * .7)), fill=mix(color, (240, 240, 235), rng.uniform(.25, .5)))
        for _ in range(9):                                   # loose threads
            x = rng.uniform(50, 250)
            d.line(P((x, 440), (x + rng.uniform(-12, 12), 440 + rng.uniform(18, 40))), fill=mix(color, (0, 0, 0), .2), width=int(2 * k))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon(P((60, 70), (150, 40), (240, 70), (290, 160), (250, 180), (240, 130), (262, 440), (38, 440), (60, 130), (50, 180), (10, 160)), fill=255)
        mask = mask.filter(ImageFilter.MaxFilter(9))
        a = np.minimum(np.asarray(im.getchannel("A")), np.asarray(mask) | (np.asarray(im.getchannel("A")) > 0) * 255)
        im.putalpha(Image.fromarray(a.astype(np.uint8)))
    else:
        for y in range(120, 420, 50):                       # machine "chikankari" print: flat grid
            for x in range(80, 230, 40):
                d.ellipse(P((x - 6, y - 6), (x + 6, y + 6)), fill=mix(color, (255, 255, 255), .55))
    return im.resize((w, int(w * 1.5)), Image.LANCZOS)


def parcel(w, brand=None, open_amt=0.0, logo=None):
    s = 2
    im = Image.new("RGBA", (w * s, int(w * 1.1) * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W2 = w * s
    box_c = (210, 160, 110) if brand is None else (128, 36, 52)
    top = int(W2 * .32)
    d.rectangle((0, top, W2, im.height), fill=box_c)
    d.rectangle((0, top, W2, top + 10 * s), fill=mix(box_c, (0, 0, 0), .2))
    flap = int(W2 * .25 * (1 - open_amt))
    lid_c = mix(box_c, (255, 255, 255), .12)
    if open_amt < .5:
        d.rectangle((0, top - 12 * s - flap * 0, W2, top + 10 * s), fill=lid_c)
    else:
        d.polygon([(0, top), (-0 + W2 * .05, top - W2 * .28), (W2 * .45, top - W2 * .3), (W2 * .5, top)], fill=lid_c)
        d.polygon([(W2, top), (W2 * .95, top - W2 * .28), (W2 * .55, top - W2 * .3), (W2 * .5, top)], fill=lid_c)
    if brand is None:
        d.rectangle((W2 * .45, top, W2 * .55, im.height), fill=(230, 200, 150))
        d.rounded_rectangle((W2 * .12, top + W2 * .2, W2 * .4, top + W2 * .4), radius=8, fill=(255, 255, 255))
        for y in range(3):
            d.line((W2 * .15, top + W2 * (.25 + y * .05), W2 * .37, top + W2 * (.25 + y * .05)), fill=(120, 120, 120), width=3 * s)
    elif logo is not None:
        lg = logo.resize((int(W2 * .8), int(W2 * .8 * logo.height / logo.width)), Image.LANCZOS)
        im.alpha_composite(lg, (int(W2 * .1), int(top + (im.height - top - lg.height) / 2)))
        d.rectangle((0, top + 10 * s, W2, top + 18 * s), fill=GOLD)
    return im.resize((w, int(w * 1.1)), Image.LANCZOS)


def phone_frame(screen_fn, w=560, t=0.0):
    h = int(w * 2.0)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=60, fill=(28, 28, 36))
    sw, sh = w - 36, h - 36
    scr = Image.new("RGBA", (sw, sh), (255, 255, 255, 255))
    screen_fn(scr, t)
    m = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, sw - 1, sh - 1), radius=44, fill=255)
    im.paste(scr, (18, 18), m)
    d.rounded_rectangle((w / 2 - 70, 30, w / 2 + 70, 62), radius=16, fill=(28, 28, 36))
    return im


def tap(img, x, y, t):
    """Expanding ring at a tap point; t = time since tap."""
    if not 0 <= t < .5:
        return
    r = 20 + 60 * t / .5
    a = int(200 * (1 - t / .5))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse((x - r, y - r, x + r, y + r), outline=(60, 60, 60, a), width=8)
    d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(60, 60, 60, a // 2))
    img.alpha_composite(lay)


def hearts(img, t, seed=1, n=10, area=(80, 600, 1000, 1500), color=(230, 70, 100)):
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x0 = rng.uniform(area[0], area[2])
        y0 = rng.uniform(area[1], area[3])
        sp = rng.uniform(80, 160)
        ph = rng.uniform(0, 3)
        tt = (t + ph) % 3
        y = y0 - sp * tt
        x = x0 + 20 * math.sin(tt * 3 + ph)
        r = rng.uniform(16, 28) * (1 - tt / 3 * .3)
        a = int(255 * clamp(1 - tt / 3) * clamp(t * 3))
        c = color + (a,)
        lay = Image.new("RGBA", (int(r * 3), int(r * 3)), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        dl.ellipse((0, 0, r * 1.5, r * 1.5), fill=c)
        dl.ellipse((r * 1.5 - r * .1, 0, r * 3 - r * .1, r * 1.5), fill=c)
        dl.polygon([(r * .1, r), (r * 2.9, r), (r * 1.45, r * 2.8)], fill=c)
        img.alpha_composite(lay, (int(x), int(y)))
    return d


def confetti(img, t, seed=5, n=70):
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(img)
    cols = [(230, 70, 100), (250, 200, 60), (80, 170, 130), (90, 130, 230), (214, 178, 102), (180, 90, 200)]
    for _ in range(n):
        x0 = rng.uniform(0, W)
        sp = rng.uniform(300, 600)
        y = -50 + (rng.uniform(0, 1) * 600 + sp * t) % (H + 100) - 300 * (t < .01)
        x = x0 + 40 * math.sin(t * 3 + x0)
        a = rng.uniform(0, math.pi) + t * rng.uniform(2, 6)
        w, h = 18, 10
        pts = [(x + w * math.cos(a) - h * math.sin(a), y + w * math.sin(a) + h * math.cos(a)),
               (x - w * math.cos(a) - h * math.sin(a), y - w * math.sin(a) + h * math.cos(a)),
               (x - w * math.cos(a) + h * math.sin(a), y - w * math.sin(a) - h * math.cos(a)),
               (x + w * math.cos(a) + h * math.sin(a), y + w * math.sin(a) - h * math.cos(a))]
        d.polygon(pts, fill=cols[int(x0) % len(cols)])


# ------------------------------------------------------------------ reel
class Reel:
    def __init__(self, fonts_dir):
        self.tx = Text()
        self.cor_it = lambda w, s: ImageFont.truetype(os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-italic.woff2"), s)
        self.cast = Cast()
        self.bgs = dict(room=bg_room(), store=bg_store(), bedroom=bg_bedroom(), night=bg_night())
        self.logo_maroon = Image.open(os.path.join(LOGO_DIR, "kalakari-logo-horizontal-maroon-flat.png")).convert("RGBA")
        self.logo_inv = Image.open(os.path.join(LOGO_DIR, "kalakari-logo-horizontal-inverse.png")).convert("RGBA")
        self.logo_gold = Image.open(os.path.join(LOGO_DIR, "kalakari-logo-horizontal-gold-flat.png")).convert("RGBA")
        self.photo_chikan = Image.open(os.path.join(SRC, "maroonchikankarikurti.jpg")).convert("RGB")
        self.photo_jaipur = Image.open(os.path.join(SRC, "yellowjaipuri3piece.jpg")).convert("RGB")
        self.cut_chikan = Image.open(os.path.join(CUT, "maroonchikankarikurti.png")).convert("RGBA")
        self.cut_jaipur = Image.open(os.path.join(CUT, "yellowjaipuri3piece.png")).convert("RGBA")
        self.kurti_store = kurti_prop((236, 200, 210), w=300)
        self.kurti_faded = kurti_prop((210, 120, 60), faded=True, w=320)
        self.box_plain = [parcel(380, None, o) for o in (0, 1)]
        self.box_kk = [parcel(420, "kk", o, self.logo_gold) for o in (0, 1)]

    # ---------- helpers
    def girl(self, img, spec, x, feet_y, h, expr, pose, t, seed=0, enter=None, flip=False, wave=0.0):
        g = self.cast.get(spec, expr, pose, wave, blinking(t, seed))
        if flip:
            g = g.transpose(Image.FLIP_LEFT_RIGHT)
        s = h / GH
        bob = math.sin(t * 3.2 + seed) * 4
        sc = s
        a = 1.0
        if enter is not None:
            p = clamp((t - enter) / .45)
            sc = s * (.6 + .4 * back(p))
            a = clamp(p * 2)
            if p <= 0:
                return
        gi = scaled(g, sc)
        gi = fade_img(gi, a)
        img.alpha_composite(gi, (int(x - gi.width / 2), int(feet_y - gi.height + bob)))

    def caption(self, img, text, t, t_in=0.0, y=150, bg=MAROON, fg=CREAM, size=50):
        p = clamp((t - t_in) / .35)
        if p <= 0:
            return
        blk = self.tx.block(text, "Bold", size, fg, 880)
        pw, ph = blk.width + 70, blk.height + 50
        lay = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=30, fill=bg)
        lay.alpha_composite(blk, (35, 25))
        lay = fade_img(scaled(lay, .85 + .15 * back(p)), clamp(p * 2))
        img.alpha_composite(lay, (int(540 - lay.width / 2), int(y + (1 - p) * -20)))

    def bubble(self, img, text, x, y, t, t_in, tail="down-left", size=44, t_out=None):
        """Speech bubble; (x, y) is the tail tip, the bubble sits above it."""
        p = clamp((t - t_in) / .3)
        if p <= 0 or (t_out is not None and t > t_out):
            return
        blk = self.tx.block(text, "SemiBold", size, INK, 560)
        pw, ph = blk.width + 60, blk.height + 44
        lay = Image.new("RGBA", (pw + 8, ph + 70), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle((4, 4, pw + 3, ph + 3), radius=36, fill=(255, 255, 255), outline=INK, width=4)
        tx_ = pw * (.25 if tail == "down-left" else .75)
        tip = (tx_ + (-40 if tail == "down-left" else 40), ph + 64)
        d.polygon([(tx_ - 26, ph - 2), (tx_ + 26, ph - 2), tip], fill=(255, 255, 255))
        d.line([(tx_ - 26, ph + 2), tip, (tx_ + 26, ph + 2)], fill=INK, width=4)
        lay.alpha_composite(blk, (34, 26))
        s = .5 + .5 * back(p, 2.4)
        lay2 = fade_img(scaled(lay, s), clamp(p * 2))
        ox = x - tip[0] * s
        oy = y - tip[1] * s
        img.alpha_composite(lay2, (int(clamp(ox, 10, W - lay2.width - 10)), int(oy)))

    # ---------- scenes (local time)
    def intro(self, t):
        img = self.bgs["room"].copy()
        self.girl(img, RIYA, 320, 1720, 860, "happy", "wave", t, 0, enter=.2, wave=t * 9)
        self.girl(img, PRIYA, 770, 1720, 840, "grin", "idle", t, 1, enter=.45)
        self.caption(img, "Meet Riya & Priya 👭", t, .1)
        self.caption(img, "Best friends. Big ethnic-wear lovers.", t, .9, y=290, bg=CREAM, fg=MAROON, size=40)
        self.bubble(img, "Hiii! 👋", 400, 840, t, 1.2, t_out=1.95)
        self.bubble(img, "Let's go kurti shopping! 🛍️", 680, 840, t, 2.0, tail="down-right")
        return img

    def store(self, t):
        img = self.bgs["store"].copy()
        sw = math.sin(t * 2.4) * 3
        k = self.kurti_store.rotate(sw, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(k, (540 - k.width // 2, 1000))
        expr_p = "shock" if t < 2.4 else "annoyed"
        self.girl(img, PRIYA, 830, 1760, 780, expr_p, "hips" if t > 2.4 else "idle", t, 1)
        self.girl(img, RIYA, 240, 1760, 800, "annoyed" if t > 2.4 else "shock", "point" if t < 2.4 else "hips", t, 0)
        # price tag hanging on the kurti
        d = ImageDraw.Draw(img)
        p = back(clamp((t - .6) / .35))
        if p > 0:
            tag = Image.new("RGBA", (300, 150), (0, 0, 0, 0))
            dt = ImageDraw.Draw(tag)
            dt.polygon([(0, 75), (40, 0), (300, 0), (300, 150), (40, 150)], fill=(255, 225, 90))
            dt.ellipse((30, 63, 54, 87), fill=(246, 240, 230))
            dt.text((175, 75), "₹4,999", font=self.tx.font("Black", 62), fill=(200, 30, 40), anchor="mm")
            tag = scaled(tag, (.5 + .5 * p) * .9)
            d.line((540, 1090, 420, 1250), fill=(120, 120, 120), width=3)
            img.alpha_composite(tag, (410, 1250 - tag.height // 2))
        self.caption(img, "First stop: a big fashion store 🏬", t, .05, y=120)
        self.bubble(img, "₹4,999 for THIS?! 😳", 760, 1000, t, .9, tail="down-right", t_out=2.55)
        self.bubble(img, "And it's machine-made, not real chikankari 🙄", 300, 1000, t, 2.6)
        return img

    def app_screen(self, scr, t):
        d = ImageDraw.Draw(scr)
        w, h = scr.size
        d.rectangle((0, 0, w, 130), fill=(255, 140, 60))
        d.text((w / 2, 85), "MegaShop", font=self.tx.font("Black", 42), fill=(255, 255, 255), anchor="mm")
        d.rounded_rectangle((30, 160, w - 30, 680), radius=24, fill=(250, 236, 226))
        k = kurti_prop((236, 140, 80), w=220)
        scr.alpha_composite(k, (int(w / 2 - 110), 180))
        d.text((40, 720), "Jaipuri Kurti (Designer)", font=self.tx.font("Bold", 34), fill=INK)
        d.text((40, 770), "₹899   ★ 3.9", font=self.tx.font("SemiBold", 34), fill=(90, 90, 90))
        d.text((40, 820), "Delivery in 9 days", font=self.tx.font("Regular", 28), fill=(140, 140, 140))
        bc = (255, 140, 60) if t < 1.2 else (220, 110, 40)
        d.rounded_rectangle((40, 880, w - 40, 970), radius=20, fill=bc)
        d.text((w / 2, 925), "BUY NOW" if t < 1.25 else "ORDERED", font=self.tx.font("Bold", 36), fill=(255, 255, 255), anchor="mm")

    def app(self, t):
        img = self.bgs["bedroom"].copy()
        if t < 2.4:
            ph = phone_frame(self.app_screen, 520, t)
            p = back(clamp(t / .4))
            ph = scaled(ph, .7 + .3 * p)
            img.alpha_composite(ph, (int(540 - ph.width / 2), 300))
            tap(img, 540, 300 + 18 + 925, t - 1.2)
            self.girl(img, PRIYA, 860, 1800, 640, "happy", "phone", t, 1)
            self.caption(img, "Next: a famous shopping app 📱", t, .05, y=110)
        else:
            lt = t - 2.4
            opened = lt > .7
            box = self.box_plain[1 if opened else 0]
            jump = abs(math.sin(lt * 9)) * 20 * (1 - clamp(lt / .6))
            img.alpha_composite(box, (540 - box.width // 2, int(1300 - jump)))
            if opened:
                p = back(clamp((lt - .7) / .5))
                k = scaled(self.kurti_faded, .4 + .6 * p)
                img.alpha_composite(k, (540 - k.width // 2, int(1330 - k.height * (.2 + .8 * p))))
            self.girl(img, RIYA, 190, 1800, 700, "sad" if opened else "happy", "shrug" if opened else "clasp", t, 0)
            self.girl(img, PRIYA, 890, 1800, 690, "sad" if opened else "happy", "idle", t, 1)
            self.caption(img, "The parcel finally arrives… 📦", lt, 0, y=110)
            self.bubble(img, "Colour faded after ONE wash 😩", 820, 1150, lt, 1.2, tail="down-right", t_out=1.95)
            self.bubble(img, "Wrong size… and no exchange 😤", 260, 1130, lt, 2.0)
        return img

    def sad(self, t):
        img = self.bgs["night"].copy()
        d = ImageDraw.Draw(img)
        rng = np.random.default_rng(2)
        for _ in range(40):                                   # rain on the window
            x = rng.uniform(665, 955)
            y = 350 + (rng.uniform(0, 410) + t * 500) % 410
            d.line((x, y, x - 6, y + 26), fill=(150, 170, 220), width=3)
        self.girl(img, RIYA, 330, 1760, 820, "sad", "clasp", t, 0)
        self.girl(img, PRIYA, 760, 1760, 800, "sad", "phone", t, 1)
        self.caption(img, "Is a real, handcrafted kurti too much to ask? 😔", t, .1, y=150, bg=(30, 34, 60))
        return img

    def insta_screen(self, scr, t):
        d = ImageDraw.Draw(scr)
        w, h = scr.size
        d.rectangle((0, 0, w, 120), fill=(255, 255, 255))
        d.line((0, 120, w, 120), fill=(230, 230, 230), width=2)
        d.ellipse((24, 140, 104, 220), fill=(128, 36, 52))
        lg = self.logo_gold.resize((70, int(70 * self.logo_gold.height / self.logo_gold.width)), Image.LANCZOS)
        scr.alpha_composite(lg, (29, int(180 - lg.height / 2)))
        d.text((120, 162), "kalakaricreations27", font=self.tx.font("Bold", 30), fill=INK)
        d.text((120, 198), "Handcrafted in Ahmedabad", font=self.tx.font("Regular", 24), fill=(120, 120, 120))
        ph = self.photo_chikan
        sw = w
        shh = int(sw * 1.15)
        sc = max(sw / ph.width, shh / ph.height)
        im = ph.resize((int(ph.width * sc), int(ph.height * sc)), Image.LANCZOS)
        x0 = int(im.width * .52 - sw / 2)
        im = im.crop((x0, 0, x0 + sw, shh))
        scr.paste(im, (0, 240))
        y = 240 + shh + 20
        hp = back(clamp((t - 1.3) / .3), 3)
        r = 22 * (1 + .3 * hp) if hp > 0 else 22
        c = (230, 50, 80) if hp > 0 else (60, 60, 60)
        hx, hy = 50, y + 24
        d.ellipse((hx - r, hy - r * .9, hx, hy + r * .1), fill=c)
        d.ellipse((hx - 4, hy - r * .9, hx + r - 4, hy + r * .1), fill=c)
        d.polygon([(hx - r, hy - r * .3), (hx + r - 4, hy - r * .3), (hx - 2, hy + r)], fill=c)
        d.text((100, y + 4), "Real hand chikankari", font=self.tx.font("Bold", 30), fill=INK)
        d.text((24, y + 60), "Chikankari · Jaipuri · Ajrakh · Tunics", font=self.tx.font("Regular", 26), fill=(90, 90, 90))

    def found(self, t):
        img = bg_burst(t)
        ph = phone_frame(self.insta_screen, 560, t)
        p = back(clamp(t / .5))
        ph = scaled(ph, .5 + .5 * p)
        img.alpha_composite(ph, (int(540 - ph.width / 2), int(330 + (1 - p) * 200)))
        tap(img, 540 - 280 + 18 + 50, 330 + 18 + 240 + int(524 * 1.15) + 20 + 24, t - 1.3)
        d = ImageDraw.Draw(img)
        for k in range(10):                                   # sparkles
            a = k * 36 + t * 40
            rr = 520 + 30 * math.sin(t * 4 + k)
            x, y = 540 + rr * math.cos(math.radians(a)) * .9, 900 + rr * math.sin(math.radians(a))
            s = 14 + 8 * math.sin(t * 6 + k)
            d.polygon([(x, y - s * 2), (x + s * .5, y - s * .5), (x + s * 2, y), (x + s * .5, y + s * .5),
                       (x, y + s * 2), (x - s * .5, y + s * .5), (x - s * 2, y), (x - s * .5, y - s * .5)], fill=(255, 255, 255))
        self.girl(img, RIYA, 190, 1960, 700, "love", "clasp", t, 0, enter=.5)
        self.girl(img, PRIYA, 890, 1960, 690, "shock" if t < 1.5 else "love", "idle", t, 1, enter=.7)
        self.caption(img, "Then they found… Kala Kari Creations ✨", t, .15, y=110)
        return img

    def site_screen(self, scr, t):
        d = ImageDraw.Draw(scr)
        w, h = scr.size
        d.rectangle((0, 0, w, 120), fill=(245, 240, 232))
        d.rounded_rectangle((24, 56, w - 24, 106), radius=24, fill=(255, 255, 255))
        d.text((w / 2, 81), "kalakaricreations.com", font=self.tx.font("SemiBold", 26), fill=INK, anchor="mm")
        lg = self.logo_maroon.resize((300, int(300 * self.logo_maroon.height / self.logo_maroon.width)), Image.LANCZOS)
        scr.alpha_composite(lg, (int(w / 2 - 150), 136))
        top = 136 + lg.height + 14
        ph = self.photo_jaipur
        sw, shh = w - 48, 470
        sc = max(sw / ph.width, shh / ph.height)
        im = ph.resize((int(ph.width * sc), int(ph.height * sc)), Image.LANCZOS)
        x0 = int(im.width / 2 - sw / 2)
        im = im.crop((x0, 0, x0 + sw, shh))
        scr.paste(im, (24, top))
        y = top + shh + 16
        d.text((24, y), "Yellow Jaipuri 3-Piece Dress", font=self.tx.font("Bold", 30), fill=INK)
        d.text((24, y + 44), "₹2,080  ·  Easy size exchange", font=self.tx.font("SemiBold", 28), fill=MAROON)
        done = t > 1.5
        d.rounded_rectangle((24, y + 100, w - 24, y + 186), radius=18, fill=(46, 140, 90) if done else MAROON)
        d.text((w / 2, y + 143), "Order placed ✓" if done else "BUY NOW", font=self.tx.font("Bold", 34), fill=(255, 255, 255), anchor="mm")
        self._buy_y = y + 143

    def order(self, t):
        img = self.bgs["room"].copy()
        ph = phone_frame(self.site_screen, 500, t)
        p = back(clamp(t / .4))
        ph = scaled(ph, .7 + .3 * p)
        px, py = int(540 - ph.width / 2), 300
        img.alpha_composite(ph, (px, py))
        tap(img, 540, py + 18 + getattr(self, "_buy_y", 900), t - 1.4)
        self.girl(img, PRIYA, 880, 1830, 620, "grin", "phone", t, 1)
        self.girl(img, RIYA, 190, 1830, 640, "happy", "clasp", t, 0)
        self.caption(img, "Ordered on kalakaricreations.com 🛍️", t, .05, y=110)
        p = back(clamp((t - 2.0) / .35))
        if p > 0:
            ban = Image.new("RGBA", (860, 190), (0, 0, 0, 0))
            db = ImageDraw.Draw(ban)
            db.rounded_rectangle((0, 0, 859, 189), radius=34, fill=(255, 255, 255), outline=(37, 211, 102), width=5)
            db.ellipse((26, 45, 126, 145), fill=(37, 211, 102))
            db.text((76, 95), "KK", font=self.tx.font("Bold", 34), fill=(255, 255, 255), anchor="mm")
            db.text((150, 52), "Kala Kari Creations · WhatsApp", font=self.tx.font("Bold", 30), fill=INK, anchor="lm")
            ban.alpha_composite(self.tx.block("Size doubt? We'll help on chat or video call 😊", "Regular", 30, INK, 680, align="l"), (150, 82))
            img.alpha_composite(fade_img(ban, clamp(p * 2)), (110, int(1335 + (1 - p) * 120)))
        return img

    def unbox(self, t):
        img = self.bgs["room"].copy()
        if t < 1.9:
            opened = t > .6
            box = self.box_kk[1 if opened else 0]
            jump = abs(math.sin(t * 9)) * 22 * (1 - clamp(t / .5))
            img.alpha_composite(box, (540 - box.width // 2, int(1250 - jump)))
            if opened:
                for k, (cut, dx) in enumerate(((self.cut_chikan, -230), (self.cut_jaipur, 230))):
                    p = back(clamp((t - .7 - k * .15) / .5))
                    if p <= 0:
                        continue
                    card = Image.new("RGBA", (360, 520), (255, 255, 255, 255))
                    c = cut.resize((int(cut.width * 480 / cut.height), 480), Image.LANCZOS)
                    if c.width > 340:
                        c = c.resize((340, int(c.height * 340 / c.width)), Image.LANCZOS)
                    card.alpha_composite(c, ((360 - c.width) // 2, 520 - c.height - 10))
                    ImageDraw.Draw(card).rectangle((0, 0, 359, 519), outline=GOLD, width=6)
                    card = scaled(card.rotate(-8 if k == 0 else 8, expand=True, resample=Image.BICUBIC), .3 + .7 * p)
                    cx = 540 + dx * p
                    cy = 1250 - 420 * p
                    img.alpha_composite(card, (int(cx - card.width / 2), int(cy - card.height / 2)))
            self.caption(img, "Their Kala Kari parcel arrives 💝", t, .05, y=110)
            hearts(img, max(0, t - .7), seed=3, n=8, area=(200, 900, 880, 1300))
            return img
        lt = t - 1.9
        self.girl(img, RIYA_KK, 310, 1760, 860, "love", "clasp", lt, 0, enter=0)
        self.girl(img, PRIYA_KK, 780, 1760, 840, "love", "idle", lt, 1, enter=.15)
        hearts(img, lt, seed=4, n=12)
        self.caption(img, "And they LOVED it 😍", lt, 0, y=110)
        self.bubble(img, "Real hand chikankari! 🤍", 380, 860, lt, .35, t_out=1.05)
        self.bubble(img, "Perfect fit, so soft! 💛", 700, 860, lt, 1.05, tail="down-right")
        return img

    def dest(self, t):
        img = bg_burst(t * .6, (255, 240, 226), (252, 222, 206))
        confetti(img, t)
        self.girl(img, RIYA_KK, 330, 1760, 860, "grin", "cheer", t, 0)
        self.girl(img, PRIYA_KK, 760, 1760, 840, "grin", "wave", t, 1, wave=t * 9)
        self.caption(img, "Now Kala Kari Creations is their fashion destination 💛", t, .1, y=130, size=52)
        return img

    def end(self, t):
        img = Image.new("RGBA", (W, H), MAROON + (255,))
        d = ImageDraw.Draw(img)
        d.rectangle((40, 40, W - 40, H - 40), outline=GOLD, width=2)
        lg = self.logo_inv.resize((600, int(600 * self.logo_inv.height / self.logo_inv.width)), Image.LANCZOS)
        img.alpha_composite(fade_img(lg, ease(t / .5)), ((W - lg.width) // 2, 230))

        def put(text, font, fill, y, st):
            a = ease((t - st) / .4)
            if a > 0:
                lay = Image.new("RGBA", (W, 120), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((540, 60), text, font=font, fill=fill, anchor="mm")
                img.alpha_composite(fade_img(lay, a), (0, int(y - 60 + (1 - a) * 16)))

        put("Handcrafted.", self.cor_it(600, 110), CREAM, 520, .2)
        put("Not mass-made.", self.cor_it(600, 110), GOLD, 640, .35)
        put("Chikankari · Jaipuri · Ajrakh · Tunics", self.tx.font("Regular", 38), CREAM, 770, .5)
        a = ease((t - .65) / .4)
        if a > 0:
            lay = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rounded_rectangle((150, 15, 930, 125), radius=55, fill=GOLD)
            dl.text((540, 70), "kalakaricreations.com", font=self.tx.font("Bold", 54), fill=MAROON, anchor="mm")
            img.alpha_composite(fade_img(lay, a), (0, 850))
        put("Call / WhatsApp  +91 94081 14592", self.tx.font("Regular", 38), CREAM, 1060, .8)
        put("Follow @kalakaricreations27", self.tx.font("SemiBold", 38), GOLD, 1130, .9)
        self.girl(img, RIYA_KK, 330, 1860, 640, "happy", "wave", t, 0, wave=t * 9, enter=.6)
        self.girl(img, PRIYA_KK, 750, 1860, 625, "happy", "idle", t, 1, enter=.75)
        return img

    def frame(self, t):
        act = [i for i, (n, d) in enumerate(SCENES) if STARTS[i] <= t < STARTS[i] + d]
        if not act:
            act = [len(SCENES) - 1]
        i = act[0]
        fr = getattr(self, SCENES[i][0])(t - STARTS[i])
        if len(act) > 1:
            j = act[1]
            fj = getattr(self, SCENES[j][0])(t - STARTS[j])
            fr = Image.blend(fr, fj, ease((t - STARTS[j]) / XF))
        return fr


# ------------------------------------------------------------------ audio
def story_track(path, seconds, seed=21):
    sr = M.SR
    rng = np.random.default_rng(seed)
    n = int((seconds + 2) * sr)
    mel, strum, bass, drums, pad, sfx = (np.zeros(n) for _ in range(6))
    beat = .5
    D4 = M.D3 * 2
    f = lambda semi: D4 * 2 ** (semi / 12)  # noqa: E731

    def pluck(fr, dur, bright=.8, decay=4.0):
        k = int(dur * sr)
        x = np.arange(k) / sr
        y = sum((bright ** h) / h * np.sin(2 * np.pi * fr * h * x) * np.exp(-x * decay * (1 + .6 * h)) for h in range(1, 9))
        y[: int(.003 * sr)] *= np.linspace(0, 1, int(.003 * sr))
        return y

    def noise_hit(dur, cutoff, decay):
        k = int(dur * sr)
        x = np.arange(k) / sr
        return M.lowpass(rng.standard_normal(k), cutoff) * np.exp(-x * decay)

    def hp(x):
        return x - M.lowpass(x, 3000)

    def kick(t0, amp=1.0):
        k = int(.35 * sr)
        x = np.arange(k) / sr
        fr = 70 + 40 * np.exp(-x * 20)
        M.add(drums, np.sin(2 * np.pi * np.cumsum(fr) / sr) * np.exp(-x * 9) * amp, t0)

    def groove(t0, t1, chords, roots, melody, mel_amp=1.0, full=True):
        t = t0
        b = 0
        while t < t1 - .01:
            ch = chords[b % len(chords)]
            for e in range(4):
                st = t + e * beat + beat / 2
                if st >= t1:
                    break
                for j, s in enumerate(ch):
                    M.add(strum, pluck(f(s), .22, .8, 9), st + j * .009)
            for off, dur in ((0, .4), (1.5, .3), (2, .4), (3.5, .2)):
                if t + off * beat < t1:
                    k = int(dur * sr)
                    M.add(bass, pluck(f(roots[b % len(roots)]), dur, .5, 4) * np.linspace(1, 0, k) ** .5, t + off * beat)
            if melody:
                pos = t
                for semi, e in melody[b % len(melody)]:
                    if semi is not None and pos < t1:
                        M.add(mel, pluck(f(semi), .35, .7, 6) * mel_amp, pos)
                    pos += e * beat / 2
            for bi in range(4):
                bt = t + bi * beat
                if bt >= t1:
                    break
                if bi in (0, 2):
                    kick(bt)
                elif full:
                    M.add(drums, noise_hit(.18, 2200, 28) * .55, bt)
                    M.add(drums, noise_hit(.18, 2600, 30) * .4, bt + .012)
                M.add(drums, pluck(D4 * 1.5, .12, .6, 30) * .35, bt + beat * .75)
                for s16 in range(4):
                    M.add(drums, hp(noise_hit(.05, 9000, 90)) * (.2 if s16 % 2 else .1), bt + s16 * beat / 4)
            t += beat * 4
            b += 1

    major = [[0, 4, 7], [-5, -1, 2, 7], [-3, 2, 6, 9], [-7, -3, 2, 7]]          # D A Bm G
    roots = [-12, -17, -15, -19]
    mel_a = [
        [(4, 1), (7, 1), (12, 1), (7, 1), (9, 1), (None, 1), (7, 1), (4, 1)],
        [(2, 1), (7, 1), (11, 1), (7, 1), (9, 1), (7, 1), (6, 1), (4, 1)],
        [(6, 1), (11, 1), (14, 1), (11, 1), (13, 1), (14, 1), (16, 1), (14, 1)],
        [(12, 1), (11, 1), (7, 1), (11, 1), (9, 2), (None, 2)],
    ]
    t_app_box = START["app"] + 2.4 + .7
    t_sad = START["sad"]
    t_found = START["found"]
    # 1) fun intro through the store and the app, groove only under the parcel reveal
    groove(0, t_app_box, major, roots, mel_a)
    # comedic "womp womp" on the faded kurti
    for k, semi in enumerate([4, 3, 2, -1]):
        dur = .32 if k < 3 else .9
        st = t_app_box + .15 + k * .34
        kk = int(dur * sr)
        x = np.arange(kk) / sr
        fr = f(semi - 12) * (1 - .04 * (x / dur) * (k == 3))
        ph = 2 * np.pi * np.cumsum(fr * (1 + .01 * np.sin(2 * np.pi * 6 * x))) / sr
        y = (np.sin(ph) + .5 * np.sin(2 * ph) + .3 * np.sin(3 * ph) + .15 * np.sin(4 * ph)) * M.env(kk, .02, .12)
        M.add(mel, M.lowpass(y, 1400) * 1.1, st)
    # thin groove (no melody) until the sad scene
    groove(t_app_box + 1.6, t_sad, major[2:], roots[2:], None, full=False)
    # 2) sad: B minor pad + slow flute, no drums
    for k, (chord, dur) in enumerate((([-3, 2, 6], 1.6), ([-7, -3, 2], 1.6))):
        for s in chord:
            M.add(pad, M.pad_note(f(s), dur + .6) * .9, t_sad + k * 1.5)
    for semi, st, dur in ((9, .2, .7), (7, .9, .5), (6, 1.4, .9), (4, 2.3, .8)):
        kk = int(dur * sr)
        x = np.arange(kk) / sr
        ph = 2 * np.pi * f(semi) * x * (1 + .005 * np.sin(2 * np.pi * 5 * x))
        M.add(mel, (np.sin(ph) + .12 * np.sin(2 * ph)) * M.env(kk, .08, .3) * .6, t_sad + st)
    # 3) discovery: rising harp-like run (major scale, no bells) then bright groove to the end
    run = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19]
    for k, s in enumerate(run):
        M.add(mel, pluck(f(s), .5, .6, 5) * .8, t_found - .35 + k * .04)
    k_ = int(.8 * sr)
    sw = hp(rng.standard_normal(k_)) * np.linspace(0, 1, k_) ** 2 * .25
    M.add(sfx, sw, t_found - .8)
    t_end = START["end"]
    groove(t_found + .2, t_end, major, roots, mel_a, mel_amp=1.1)
    # end card: big strummed chord, light groove
    for j, s in enumerate([-12, -5, 0, 4, 7, 12]):
        M.add(strum, pluck(f(s), 2.5, .9, 1.4) * .9, t_end + j * .025)
    groove(t_end + 1.0, seconds, major[:1], roots[:1], None, full=False)

    # sound effects: pops for bubbles/captions, taps, knock for the parcels
    def pop(t0, fr=900):
        kk = int(.09 * sr)
        x = np.arange(kk) / sr
        M.add(sfx, np.sin(2 * np.pi * np.cumsum(fr * np.exp(-x * 18) + 300) / sr) * np.exp(-x * 40) * .6, t0)

    def knock(t0):
        for d_ in (0, .16):
            kk = int(.12 * sr)
            x = np.arange(kk) / sr
            M.add(sfx, (np.sin(2 * np.pi * 180 * x) + M.lowpass(rng.standard_normal(kk), 800) * .6) * np.exp(-x * 45), t0 + d_)

    S = START
    for t0 in (S["intro"] + 1.2, S["intro"] + 2.0, S["store"] + .9, S["store"] + 2.6, S["app"] + 2.4 + 1.2,
               S["app"] + 2.4 + 2.0, S["unbox"] + 1.9 + .5, S["unbox"] + 1.9 + 1.2, S["order"] + 2.0):
        pop(t0)
    for t0 in (S["store"] + .6,):
        pop(t0, 1300)
    for t0 in (S["app"] + 1.2, S["order"] + 1.4, S["found"] + 1.3):
        pop(t0, 1600)
    knock(S["app"] + 2.4)
    knock(S["unbox"])

    out = .30 * mel + .2 * strum + .34 * M.lowpass(bass, 900) + .24 * drums + .22 * pad + .35 * sfx
    out = M.reverb(out, seconds=1.4, mix=.15, seed=seed)[: int(seconds * sr)]
    out *= M.env(len(out), .05, 1.5)
    out /= np.max(np.abs(out)) + 1e-9
    out = np.tanh(2.2 * out) / np.tanh(2.2)
    out *= 10 ** (-1.5 / 20)
    d = int(.01 * sr)
    left, right = out, np.concatenate([np.zeros(d), out[:-d]]) * .9 + out * .1
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
    story_track(wav, TOTAL)
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
            r.frame(t).convert("RGB").resize((360, 640)).save(os.path.join(sys.argv[2], f"st_{t:05.1f}.png"))
    else:
        main()
