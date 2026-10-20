#!/usr/bin/env python3
"""15 s 9:16 brand reel after Navratri: same look and music as brand_reel_navratri.py, with the offer
removed and new Lucknowi, Jaipuri and Kutchi products.

Usage:
    python3 brand_reel.py <fonts_dir> <images_dir> <brand_dir> <out.mp4>
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_reel_navratri as B  # noqa: E402

A, W, fade = B.A, B.W, B.fade
GOLD, CREAM, MAROON, DARK = B.GOLD, B.CREAM, B.MAROON, B.DARK

# 7 shots, sum(dur) - 6 * XF = 15.0 s
B.SHOTS = [
    dict(kind="photo", src=("src", "maroonchikankarikurti.jpg"), f=(.52, .4), dur=2.6,
         eyebrow="KALA KARI CREATIONS", l1="Handcrafted.", l2="Not mass-made.", note="Maroon Lucknowi chikankari kurti  ·  ₹1,500"),
    dict(kind="photo", src=("src", "blue3piececottonjaipuri.jpg"), f=(.5, .4), dur=2.3,
         eyebrow="JAIPURI HAND-BLOCK PRINT", l1="Every stitch,", l2="by artisan hands.", note="Navy blue 3-piece dress  ·  ₹1,300"),
    dict(kind="photo", src=("src", "ajrakhkali.jpg"), f=(.5, .4), dur=2.3,
         eyebrow="HAND BLOCK-PRINTED IN KUTCH", l1="One of a kind,", l2="just like you.", note="Ajrakh kali flair kurti  ·  ₹1,600"),
    dict(kind="photo", src=("img", "3.webp"), f=(.46, .4), dur=2.1,
         eyebrow="NATURAL COTTON", l1="Easy, breathable,", l2="made to be lived in.", note="Tunics from ₹800"),
    dict(kind="trio", dur=2.1,
         srcs=[("pants", "white-mul-pants-3-pants-closeup.jpg", .5),
               ("pants", "maroon-mul-pants-3-walking-closeup.jpg", .45),
               ("pants", "black-mul-pants-3-pants-closeup.jpg", .5)],
         eyebrow="PURE MUL COTTON PANTS", l1="Everyday ease,", l2="in three colours.", note="White · Maroon · Black  ·  ₹500"),
    dict(kind="mom", dur=2.4,
         eyebrow="FROM OUR AHMEDABAD HOME", l1="Started by", l2="a mother & son.", note="Honest prices. Real craft. Small batches."),
    dict(kind="end", dur=3.6),
]


class Brand(B.Brand):
    def end_shot(self, local):
        img = Image.new("RGBA", (W, B.H), MAROON + (255,))
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
        img.alpha_composite(lg, ((W - lg.width) // 2, 490))
        put("Tradition,", self.cor(500, 120), CREAM, 720, fade(local, .25))
        put("beautifully worn.", self.cor_it(500, 120), GOLD, 850, fade(local, .4))
        put("Kurtis from ₹1,000  ·  Dresses from ₹1,300", self.inter("Regular", 36), CREAM, 1050, fade(local, .6))
        put("Easy size exchange  ·  Pan-India delivery", self.inter("Regular", 36), CREAM, 1110, fade(local, .7))
        put("kalakaricreations.com", self.inter("Regular", 44), GOLD, 1220, fade(local, .85))
        b = fade(local, 1.0)
        if b > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rectangle((cx - 190, 1320, cx + 190, 1420), fill=GOLD)
            A.draw_text(dl, (cx, 1350), "SHOP NOW", self.inter("Medium", 36), DARK, tracking=6, anchor="c")
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * b)))
            img.alpha_composite(lay)
        put("Call / WhatsApp  +91 94081 14592", self.inter("Regular", 32), CREAM, 1490, fade(local, 1.2))
        return img


B.Brand = Brand

if __name__ == "__main__":
    B.main()
