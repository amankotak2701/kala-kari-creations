#!/usr/bin/env python3
"""15 s 9:16 brand reel: chikankari, Jaipuri, Kutchi Ajrakh, tunics, pants, the mother & son story,
the Navratri offer and the brand end card. Re-uses the original brand reel's music.

Usage:
    python3 brand_reel_navratri.py <fonts_dir> <images_dir> <brand_dir> <out.mp4>

<brand_dir> holds music.wav and mom.png extracted from the original 5-brand-reel video.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ads"))
sys.path.insert(0, HERE)
import make_ads as A  # noqa: E402
import navratri_reel as N  # noqa: E402

W, H, FPS = 1080, 1920, 30
XF = 0.4
GOLD = (214, 178, 102)
CREAM = (247, 242, 233)
MAROON = (117, 44, 57)
DARK = (24, 18, 16)
SRC = os.path.join(HERE, "..", "ads", "source-photos")
PANTS = os.path.join(HERE, "..", "product-photos", "mul-cotton-pants", "photos")
LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-inverse.png")
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"

SHOTS = [
    dict(kind="photo", src=("src", "muslin2piecechikankari.jpg"), f=(.5, .42), dur=2.2,
         eyebrow="KALA KARI CREATIONS", l1="Handcrafted.", l2="Not mass-made.", note="Lucknowi chikankari suit  ·  ₹2,450"),
    dict(kind="photo", src=("src", "black3piececottondress.jpg"), f=(.5, .4), dur=1.9,
         eyebrow="JAIPURI HAND-BLOCK PRINT", l1="Every stitch,", l2="by artisan hands.", note="3-piece dresses from ₹1,300"),
    dict(kind="photo", src=("src", "ajrakhsilkkutchiprint.jpg"), f=(.5, .4), dur=1.9,
         eyebrow="HAND BLOCK-PRINTED IN KUTCH", l1="One of a kind,", l2="just like you.", note="Ajrakh kurti with Kutchi work  ·  ₹1,450"),
    dict(kind="photo", src=("img", "2.webp"), f=(.5, .42), dur=1.9,
         eyebrow="NATURAL COTTON", l1="Easy, breathable,", l2="made to be lived in.", note="Tunics from ₹800"),
    dict(kind="trio", dur=1.9,
         srcs=[("pants", "white-mul-pants-3-pants-closeup.jpg", .5),
               ("pants", "maroon-mul-pants-3-walking-closeup.jpg", .45),
               ("pants", "black-mul-pants-3-pants-closeup.jpg", .5)],
         eyebrow="PURE MUL COTTON PANTS", l1="Everyday ease,", l2="in three colours.", note="White · Maroon · Black  ·  ₹500"),
    dict(kind="mom", dur=2.4,
         eyebrow="FROM OUR AHMEDABAD HOME", l1="Started by", l2="a mother & son.", note="Honest prices. Real craft. Small batches."),
    dict(kind="offer", dur=2.4),
    dict(kind="end", dur=3.2),
]


def ease(t):
    return A.ease(t)


def fade(t, s, d=.5):
    return ease((t - s) / d)


class Brand:
    def __init__(self, fonts_dir, images_dir, brand_dir):
        self.dirs = {"src": SRC, "img": images_dir, "pants": PANTS}
        self.cor = lambda w, s: ImageFont.truetype(os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-normal.woff2"), s)
        self.cor_it = lambda w, s: ImageFont.truetype(os.path.join(fonts_dir, "fontsource-cormorant-garamond", "package", "files", f"cormorant-garamond-latin-{w}-italic.woff2"), s)
        self.inter = lambda w, s: ImageFont.truetype(INTER.format(w), s)
        self.cache = {}
        logo = Image.open(LOGO).convert("RGBA")
        self.logo_sm = logo.resize((300, int(300 * logo.height / logo.width)), Image.LANCZOS)
        self.logo_lg = logo.resize((560, int(560 * logo.height / logo.width)), Image.LANCZOS)
        self.mom = self.make_mom(os.path.join(brand_dir, "mom.png"))
        self.toran = N.toran()
        self.shade = A.gradient(W, 1050, 0, 250, color=DARK)
        self.top = A.gradient(W, 360, 140, 0, color=DARK)

    def img(self, kind, name):
        k = (kind, name)
        if k not in self.cache:
            self.cache[k] = Image.open(os.path.join(self.dirs[kind], name)).convert("RGB")
        return self.cache[k]

    def make_mom(self, path):
        # the clean photo area of the original frame (above its text), extended into a dark fade
        fr = Image.open(path).convert("RGB")
        photo = fr.crop((160, 0, 920, 790))
        photo = photo.resize((W, int(W * photo.height / photo.width)), Image.LANCZOS)
        canvas = Image.new("RGBA", (W, H), DARK + (255,))
        canvas.paste(photo, (0, 0))
        fadeh = 320
        canvas.alpha_composite(A.gradient(W, fadeh, 0, 255, color=DARK), (0, photo.height - fadeh))
        return canvas

    # ---- text block in the original's style
    def caption(self, img, local, eyebrow, l1, l2, note):
        m = 80
        y = 1330
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        A.draw_text(d, (m, y), eyebrow, self.inter("Medium", 26), GOLD, tracking=6)
        a1, a2, a3 = fade(local, .15), fade(local, .35), fade(local, .55)

        def put(text, font, fill, yy, a, rise):
            if a <= 0:
                return
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            A.draw_text(ImageDraw.Draw(lay), (m, yy + int((1 - a) * rise)), text, font, fill)
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)

        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * fade(local, .05))))
        img.alpha_composite(layer)
        put(l1, self.cor(500, 104), CREAM, y + 48, a1, 24)
        put(l2, self.cor_it(500, 104), GOLD, y + 160, a2, 24)
        put(note, self.inter("Regular", 34), CREAM, y + 300, a3, 12)

    def brand_mark(self, img, local):
        lg = self.logo_sm.copy()
        a = fade(local, 0, .4)
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lg, (70, 90))

    def photo_shot(self, s, local):
        p = local / s["dur"]
        kind, name = s["src"]
        img = A.cover(self.img(kind, name), W, H, s["f"][0], s["f"][1], 1.0 + .07 * ease(p)).convert("RGBA")
        img.alpha_composite(self.top, (0, 0))
        img.alpha_composite(self.shade, (0, H - 1050))
        return img

    def trio_shot(self, s, local):
        img = Image.new("RGBA", (W, H), DARK + (255,))
        gap = 8
        pw = (W - 2 * gap) // 3
        for i, (kind, name, fx) in enumerate(s["srcs"]):
            a = fade(local, .1 + .18 * i, .45)
            if a <= 0:
                continue
            ph = A.cover(self.img(kind, name), pw, H, fx, .3, 1.0 + .05 * ease(local / s["dur"])).convert("RGBA")
            ph.putalpha(int(255 * a))
            img.alpha_composite(ph, (i * (pw + gap), int((1 - a) * 40)))
        img.alpha_composite(self.top, (0, 0))
        img.alpha_composite(self.shade, (0, H - 1050))
        return img

    def offer_shot(self, local):
        img = Image.new("RGBA", (W, H), MAROON + (255,))
        d = ImageDraw.Draw(img)
        d.rectangle((40, 40, W - 40, H - 40), outline=GOLD, width=2)
        img.alpha_composite(self.toran, (0, 0))
        cx = W / 2

        def put(text, font, fill, y, a, tracking=0):
            if a <= 0:
                return
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            A.draw_text(ImageDraw.Draw(lay), (cx, y + int((1 - a) * 20)), text, font, fill, tracking=tracking, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)

        put("NAVRATRI OFFER", self.inter("Medium", 34), GOLD, 520, fade(local, .05), tracking=10)
        put("10% off", self.cor(600, 250), CREAM, 600, fade(local, .2))
        put("on orders above ₹3,000", self.cor_it(500, 76), GOLD, 900, fade(local, .4))
        a = fade(local, .6)
        if a > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rounded_rectangle((260, 1060, 820, 1250), radius=14, outline=GOLD, width=3)
            A.draw_text(dl, (cx, 1085), "USE CODE", self.inter("Medium", 28), CREAM, tracking=8, anchor="c")
            A.draw_text(dl, (cx, 1125), "NAV10", self.cor(700, 110), GOLD, tracking=12, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)
        put("Valid till 19 October  ·  Shop at kalakaricreations.com", self.inter("Regular", 32), CREAM, 1320, fade(local, .8))
        return img

    def end_shot(self, local):
        img = Image.new("RGBA", (W, H), MAROON + (255,))
        cx = W / 2

        def put(text, font, fill, y, a, tracking=0):
            if a <= 0:
                return
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            A.draw_text(ImageDraw.Draw(lay), (cx, y + int((1 - a) * 18)), text, font, fill, tracking=tracking, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)

        lg = self.logo_lg.copy()
        a = fade(local, .05, .6)
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lg, ((W - lg.width) // 2, 470))
        put("Tradition,", self.cor(500, 120), CREAM, 700, fade(local, .25))
        put("beautifully worn.", self.cor_it(500, 120), GOLD, 830, fade(local, .4))
        put("Kurtis from ₹1,000  ·  Dresses from ₹1,300", self.inter("Regular", 36), CREAM, 1030, fade(local, .6))
        put("Easy size exchange  ·  Pan-India delivery", self.inter("Regular", 36), CREAM, 1090, fade(local, .7))
        put("Navratri: 10% off above ₹3,000 with NAV10", self.inter("Medium", 34), GOLD, 1170, fade(local, .8))
        put("kalakaricreations.com", self.inter("Regular", 44), GOLD, 1270, fade(local, .9))
        b = fade(local, 1.0)
        if b > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rectangle((cx - 190, 1370, cx + 190, 1470), fill=GOLD)
            A.draw_text(dl, (cx, 1400), "SHOP NOW", self.inter("Medium", 36), DARK, tracking=6, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * b)))
            img.alpha_composite(lay)
        put("Call / WhatsApp  +91 94081 14592", self.inter("Regular", 32), CREAM, 1540, fade(local, 1.2))
        return img

    def shot(self, i, local):
        s = SHOTS[i]
        k = s["kind"]
        if k == "photo":
            img = self.photo_shot(s, local)
        elif k == "trio":
            img = self.trio_shot(s, local)
        elif k == "mom":
            img = self.mom.copy()
        elif k == "offer":
            return self.offer_shot(local)
        else:
            return self.end_shot(local)
        self.brand_mark(img, local)
        self.caption(img, local, s["eyebrow"], s["l1"], s["l2"], s["note"])
        return img


def main():
    fonts_dir, images_dir, brand_dir, out = sys.argv[1:5]
    b = Brand(fonts_dir, images_dir, brand_dir)
    starts, t = [], 0.0
    for s in SHOTS:
        starts.append(t)
        t += s["dur"] - XF
    total = t + XF
    n = int(round(total * FPS))
    music = os.path.join(brand_dir, "music.wav")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", music,
           "-af", f"atrim=0:{total:.2f},afade=t=out:st={total - 1.3:.2f}:d=1.3", "-t", f"{total:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        tt = k / FPS
        act = [i for i, s in enumerate(SHOTS) if starts[i] <= tt < starts[i] + s["dur"]]
        if len(act) == 1:
            fr = b.shot(act[0], tt - starts[act[0]])
        else:
            i, j = act[-2], act[-1]
            fr = Image.blend(b.shot(i, tt - starts[i]), b.shot(j, tt - starts[j]), ease((tt - starts[j]) / XF))
        proc.stdin.write(fr.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    print(out, f"{total:.1f}s")


if __name__ == "__main__":
    main()
