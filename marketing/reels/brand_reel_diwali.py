#!/usr/bin/env python3
"""15 s 9:16 brand reel with the Diwali Dhamaka offer (FLAT 20% OFF on all products, till 9 Nov): the current
brand reel (brand_reel.py) plus a Diwali offer scene before the end card and the offer line on the end card.

Usage:
    python3 brand_reel_diwali.py <fonts_dir> <images_dir> <brand_dir> <out.mp4>
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "posts"))
import brand_reel as BR  # noqa: E402  (sets up brand_reel_navratri with the current products)
import diwali_carousel as DC  # noqa: E402

B = BR.B
A, W, H, fade, ease = B.A, B.W, B.H, B.fade, B.ease
GOLD, CREAM, MAROON, DARK = B.GOLD, B.CREAM, B.MAROON, B.DARK

# 8 shots, sum(dur) - 7 * XF = 15.0 s
B.SHOTS = [
    dict(kind="photo", src=("src", "maroonchikankarikurti.jpg"), f=(.52, .4), dur=2.2,
         eyebrow="KALA KARI CREATIONS", l1="Handcrafted.", l2="Not mass-made.", note="Maroon Lucknowi chikankari kurti  ·  ₹1,500"),
    dict(kind="photo", src=("src", "blue3piececottonjaipuri.jpg"), f=(.5, .4), dur=2.0,
         eyebrow="JAIPURI HAND-BLOCK PRINT", l1="Every stitch,", l2="by artisan hands.", note="Navy blue 3-piece dress  ·  ₹1,300"),
    dict(kind="photo", src=("src", "ajrakhkali.jpg"), f=(.5, .4), dur=2.0,
         eyebrow="HAND BLOCK-PRINTED IN KUTCH", l1="One of a kind,", l2="just like you.", note="Ajrakh kali flair kurti  ·  ₹1,600"),
    dict(kind="photo", src=("img", "3.webp"), f=(.46, .4), dur=1.9,
         eyebrow="NATURAL COTTON", l1="Easy, breathable,", l2="made to be lived in.", note="Tunics from ₹800"),
    dict(kind="trio", dur=1.9,
         srcs=[("pants", "white-mul-pants-3-pants-closeup.jpg", .5),
               ("pants", "maroon-mul-pants-3-walking-closeup.jpg", .45),
               ("pants", "black-mul-pants-3-pants-closeup.jpg", .5)],
         eyebrow="PURE MUL COTTON PANTS", l1="Everyday ease,", l2="in three colours.", note="White · Maroon · Black  ·  ₹500"),
    dict(kind="mom", dur=2.2,
         eyebrow="FROM OUR AHMEDABAD HOME", l1="Started by", l2="a mother & son.", note="Honest prices. Real craft. Small batches."),
    dict(kind="offer", dur=2.3),
    dict(kind="end", dur=3.3),
]


class Diwali(BR.Brand):
    def __init__(self, *a):
        super().__init__(*a)
        self.diyas = [DC.diya(s) for s in (120, 96)]

    def _put(self, img, text, font, fill, y, a, tracking=0, rise=20):
        if a <= 0:
            return
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        A.draw_text(ImageDraw.Draw(lay), (W / 2, y + int((1 - a) * rise)), text, font, fill, tracking=tracking, anchor="c")
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lay)

    def offer_shot(self, local):
        img = Image.new("RGBA", (W, H), MAROON + (255,))
        d = ImageDraw.Draw(img)
        d.rectangle((40, 40, W - 40, H - 40), outline=GOLD, width=2)
        img.alpha_composite(self.toran, (0, 0))
        # soft golden sparkles drifting in the background
        for k in range(26):
            x = (k * 97) % 150 + (80 if k % 2 else 850)          # keep them in the side margins, off the text
            y = 360 + (k * 233) % 1100
            tw = .5 + .5 * math.sin(local * 5 + k)
            r = 2 + 3 * tw
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 220, 140, int(90 + 120 * tw)))
        self._put(img, "DIWALI DHAMAKA OFFER", self.inter("Medium", 34), GOLD, 470, fade(local, .05), tracking=10)
        self._put(img, "FLAT", self.cor_it(600, 96), GOLD, 540, fade(local, .15))
        self._put(img, "20% OFF", self.cor(700, 230), CREAM, 640, fade(local, .25))
        self._put(img, "on all products", self.cor_it(500, 80), GOLD, 920, fade(local, .4))
        a = fade(local, .55)
        if a > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rounded_rectangle((180, 1060, 900, 1250), radius=14, outline=GOLD, width=3)
            A.draw_text(dl, (W / 2, 1085), "VALID TILL", self.inter("Medium", 28), CREAM, tracking=8, anchor="c")
            A.draw_text(dl, (W / 2, 1130), "9 NOVEMBER", self.cor(700, 84), GOLD, tracking=4, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)
        self._put(img, "Shop now at kalakaricreations.com", self.inter("Regular", 34), CREAM, 1320, fade(local, .7))
        # a row of flickering diyas
        a = fade(local, .3)
        if a > 0:
            glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
            dg = ImageDraw.Draw(glow)
            for i, x in enumerate((200, 380, 540, 700, 880)):
                big = i == 2
                dy = self.diyas[0 if big else 1]
                fl = 1 + .06 * math.sin(local * 18 + i * 1.7)
                im = dy.resize((int(dy.width * fl), int(dy.height * fl)), Image.BICUBIC)
                im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
                y = 1560 if big else 1580
                dg.ellipse((x - 120, y - 110, x + 120, y + 90), fill=(255, 170, 70, int(80 * a)))
                img.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
            img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(30)))
        return img

    def end_shot(self, local):
        img = Image.new("RGBA", (W, H), MAROON + (255,))
        cx = W / 2
        lg = self.logo_lg.copy()
        a = fade(local, .05, .6)
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lg, ((W - lg.width) // 2, 470))
        self._put(img, "Tradition,", self.cor(500, 120), CREAM, 700, fade(local, .25), rise=18)
        self._put(img, "beautifully worn.", self.cor_it(500, 120), GOLD, 830, fade(local, .4), rise=18)
        self._put(img, "Kurtis from ₹1,000  ·  Dresses from ₹1,300", self.inter("Regular", 36), CREAM, 1030, fade(local, .6), rise=18)
        self._put(img, "Easy size exchange  ·  Pan-India delivery", self.inter("Regular", 36), CREAM, 1090, fade(local, .7), rise=18)
        self._put(img, "Diwali: FLAT 20% OFF on all products · till 9 Nov", self.inter("Medium", 34), GOLD, 1170, fade(local, .8), rise=18)
        self._put(img, "kalakaricreations.com", self.inter("Regular", 44), GOLD, 1270, fade(local, .9), rise=18)
        b = fade(local, 1.0)
        if b > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rectangle((cx - 190, 1370, cx + 190, 1470), fill=GOLD)
            A.draw_text(dl, (cx, 1400), "SHOP NOW", self.inter("Medium", 36), DARK, tracking=6, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * b)))
            img.alpha_composite(lay)
        self._put(img, "Call / WhatsApp  +91 94081 14592", self.inter("Regular", 32), CREAM, 1540, fade(local, 1.2), rise=18)
        return img


B.Brand = Diwali

if __name__ == "__main__":
    B.main()
