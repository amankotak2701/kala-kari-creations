#!/usr/bin/env python3
"""Render Meta ad creatives (images + videos) in 1:1, 4:5 and 9:16.

1:1  (1080x1080)  Facebook right column, Marketplace, feed
4:5  (1080x1350)  Facebook / Instagram feed
9:16 (1080x1920)  Stories, Reels, WhatsApp Status

Usage:
    python3 make_ads.py <images_dir> <fonts_dir> <cutouts_dir> <out_dir> [ad_id ...]

<images_dir> holds the photos sent in chat (1.webp .. 4.webp). <cutouts_dir> holds
background-removed product shots (8_clean.png chocolate set, 11_clean.png chanderi shirt, 15_clean.png mustard set).
Pants photos come from ../product-photos/mul-cotton-pants/photos.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reels"))
import music  # noqa: E402

W = 1080
FORMATS = {"1x1": 1080, "4x5": 1350, "9x16": 1920}
FPS = 30
XFADE = 0.5

MAROON = (117, 44, 57)
CREAM = (247, 242, 233)
CREAM_D = (236, 226, 208)
GOLD = (217, 188, 121)
GOLD_DARK = (169, 131, 58)
INK = (43, 35, 32)

LOGO = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-gold-flat.png")
PANTS = os.path.join(HERE, "..", "product-photos", "mul-cotton-pants", "photos")
FOOTER = "PAN-INDIA DELIVERY  ·  VIDEO-CALL SHOPPING  ·  CALL / WHATSAPP +91 94081 14592"

# --------------------------------------------------------------------------- ads
# photo: (source key, focal x, focal y) with focal as a fraction of the source.
# Shots: full-bleed photo ("bleed") or framed photos on cream ("panels") or a cutout ("cutout").
ADS = {
    "01-pants-3-colours": dict(
        kind="video", badge="NEW",
        shots=[
            dict(layout="panels", photos=[("pants:white-mul-pants-1-olive-kurta-full-length.jpg", .5, .55),
                                          ("pants:maroon-mul-pants-1-white-kurta-full-length.jpg", .5, .55),
                                          ("pants:black-mul-pants-1-lotus-tunic-full-length.jpg", .5, .55)],
                 labels=["White", "Maroon", "Black"], stagger=True, dur=4.2,
                 head="One pant, three moods"),
            dict(layout="panels", photos=[("pants:white-mul-pants-3-pants-closeup.jpg", .5, .5),
                                          ("pants:maroon-mul-pants-3-walking-closeup.jpg", .5, .5),
                                          ("pants:black-mul-pants-3-pants-closeup.jpg", .5, .5)],
                 dur=3.6, head="Soft, crinkled pure mul cotton"),
        ],
        end=dict(name="Pure Mul Cotton Relaxed Pants", price="₹500", note="White · Maroon · Black"),
    ),
    "02-pants-trio": dict(
        kind="image", badge="NEW", layout="panels",
        photos=[("pants:white-mul-pants-3-pants-closeup.jpg", .5, .5),
                ("pants:maroon-mul-pants-3-walking-closeup.jpg", .5, .5),
                ("pants:black-mul-pants-3-pants-closeup.jpg", .5, .5)],
        labels=["White", "Maroon", "Black"],
        head="The pants that go with everything",
        name="Pure Mul Cotton Relaxed Pants", price="₹500",
    ),
    "03-patchwork-shrug": dict(
        kind="video",
        shots=[
            dict(layout="bleed", photo=("img:1.webp", .5, .5), z=(1.12, 1.0), dur=3.2, head="Every patch tells a story"),
            dict(layout="bleed", photo=("img:1.webp", .53, .26), z=(2.2, 2.4), pan=(0, .03), dur=3.0, head="Hand block-printed patchwork"),
            dict(layout="bleed", photo=("img:1.webp", .45, .71), z=(1.5, 1.5), pan=(.2, 0), dur=3.0, head="A flared, free-flowing silhouette"),
        ],
        end=dict(name="Kutchi Patchwork Long Shrug", price="₹1,500", note="Layer it over anything"),
    ),
    "04-olive-tunic": dict(
        kind="image", layout="bleed", photo=("img:2.webp", .5, .42),
        head="Quiet colour, loud craft",
        name="Olive Smocked Cotton Tunic", price="₹850",
        sub="Pair it with our mul cotton pants · ₹500",
    ),
    "05-chanderi-shirt": dict(
        kind="video", badge="NEW",
        shots=[
            dict(layout="cutout", photo=("cut:11_clean.png", .5, .5), z=(1.0, 1.06), dur=3.2, head="A bazaar of prints in one shirt"),
            dict(layout="cutout", photo=("cut:11_clean.png", .52, .5), z=(1.7, 1.85), dur=3.0, head="Gold-coin V border"),
            dict(layout="cutout", photo=("cut:11_clean.png", .25, .45), z=(1.6, 1.6), pan=(.5, 0), dur=3.2, head="Hand block-printed Chanderi"),
        ],
        end=dict(name="Rich Red Chanderi Shirt", price="₹900", note="Lightweight Chanderi with a soft sheen"),
    ),
    "06-lotus-tunic-look": dict(
        kind="image", layout="bleed", photo=("img:4.webp", .5, .45),
        head="Bloom in black & ivory",
        name="Ivory Lotus Appliqué Tunic", price="₹800",
        sub="Complete the look with black mul pants · ₹500",
    ),
    "07-tunics-from-800": dict(
        kind="video",
        shots=[
            dict(layout="bleed", photo=("img:3.webp", .5, .45), z=(1.1, 1.0), dur=3.0, head="Ivory Leaf Appliqué · ₹800"),
            dict(layout="bleed", photo=("img:2.webp", .5, .42), z=(1.1, 1.0), dur=3.0, head="Olive Smocked Yoke · ₹850"),
            dict(layout="bleed", photo=("img:4.webp", .5, .45), z=(1.1, 1.0), dur=3.0, head="Ivory Lotus Appliqué · ₹800"),
        ],
        end=dict(name="Handcrafted Cotton Tunics", price="From ₹800", note="Everyday ease, made by hand"),
    ),
    "08-chocolate-grid-coord": dict(
        kind="image", badge="NEW", layout="cutout", photo=("cut:8_clean.png", .5, .5),
        head="Twelve little gardens, stitched by hand",
        name="Chocolate Grid Co-Ord Set", price="₹900",
    ),
    "09-mustard-folk-coord": dict(
        kind="image", badge="NEW", layout="cutout", photo=("cut:15_clean.png", .5, .5),
        head="Stories from Rajasthan, in thread",
        name="Folk-Art Embroidered Co-Ord Set", price="₹1,400",
    ),
}


# ------------------------------------------------------------------- helpers
def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


class Fonts:
    def __init__(self, d):
        cin = os.path.join(d, "fontsource-cinzel", "package", "files")
        cor = os.path.join(d, "fontsource-cormorant-garamond", "package", "files")
        self.cinzel = lambda w, s: ImageFont.truetype(os.path.join(cin, f"cinzel-latin-{w}-normal.woff2"), s)
        self.cor_it = lambda w, s: ImageFont.truetype(os.path.join(cor, f"cormorant-garamond-latin-{w}-italic.woff2"), s)


FALLBACK_CHARS = "₹→"
FALLBACK_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
_fallback_cache = {}


def glyph_font(font, ch):
    """Brand fonts lack ₹ and →; draw those from DejaVu Serif at a matching size."""
    if ch not in FALLBACK_CHARS:
        return font, 0
    key = font.size
    if key not in _fallback_cache:
        _fallback_cache[key] = ImageFont.truetype(FALLBACK_FONT, int(font.size * .82))
    fb = _fallback_cache[key]
    # align baselines
    return fb, font.getmetrics()[0] - fb.getmetrics()[0]


def text_w(d, text, font, tracking=0):
    if not any(c in FALLBACK_CHARS for c in text):
        return d.textlength(text, font=font) + tracking * max(len(text) - 1, 0)
    return sum(d.textlength(c, font=glyph_font(font, c)[0]) for c in text) + tracking * max(len(text) - 1, 0)


def draw_text(d, xy, text, font, fill, tracking=0, anchor="l"):
    x, y = xy
    w = text_w(d, text, font, tracking)
    if anchor == "c":
        x -= w / 2
    elif anchor == "r":
        x -= w
    if not tracking and not any(c in FALLBACK_CHARS for c in text):
        d.text((x, y), text, font=font, fill=fill)
        return w
    for ch in text:
        f, dy = glyph_font(font, ch)
        d.text((x, y + dy), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return w


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if d.textlength(test, font=font) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = wd
    lines.append(cur)
    return lines


def cover(src, w, h, fx=.5, fy=.5, zoom=1.0):
    """Crop src to fill w x h around focal point (fractions); zoom > 1 crops tighter."""
    sw, sh = src.size
    scale = max(w / sw, h / sh) * zoom
    cw, ch = w / scale, h / scale
    x0 = min(max(fx * sw - cw / 2, 0), sw - cw)
    y0 = min(max(fy * sh - ch / 2, 0), sh - ch)
    s = cw / w
    return src.transform((w, h), Image.AFFINE, (s, 0, x0, 0, s, y0), resample=Image.BICUBIC)


def gradient(w, h, top, bottom, color=(20, 10, 12)):
    g = Image.new("L", (1, h))
    for i in range(h):
        g.putpixel((0, i), int(lerp(top, bottom, (i / max(h - 1, 1)) ** 1.3)))
    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(g.resize((w, h)))
    return layer


def cream_bg(h):
    bg = Image.new("RGB", (W, h), CREAM)
    vig = Image.new("L", (W, h), 0)
    ImageDraw.Draw(vig).ellipse((-W * .3, -h * .25, W * 1.3, h * 1.1), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    return Image.composite(bg, Image.new("RGB", (W, h), CREAM_D), vig)


def shadowed(canvas, img, xy, blur=24, offset=(12, 18), alpha=70):
    mask = img.getchannel("A") if img.mode == "RGBA" else Image.new("L", img.size, 255)
    sh = Image.new("RGBA", (img.width + blur * 4, img.height + blur * 4), (0, 0, 0, 0))
    sh.paste(Image.new("RGBA", img.size, (60, 35, 25, alpha)), (blur * 2, blur * 2), mask)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (xy[0] - blur * 2 + offset[0], xy[1] - blur * 2 + offset[1]))
    canvas.alpha_composite(img.convert("RGBA"), xy)


# ------------------------------------------------------------------- renderer
class Renderer:
    def __init__(self, images, fonts, cutouts):
        self.dirs = {"img": images, "cut": cutouts, "pants": PANTS}
        self.f = fonts
        self.cache = {}
        logo = Image.open(LOGO).convert("RGBA")
        self.logo = logo

    def src(self, key):
        if key not in self.cache:
            kind, name = key.split(":", 1)
            im = Image.open(os.path.join(self.dirs[kind], name))
            if kind == "cut":
                im = im.convert("RGBA")
                im = im.crop(im.getbbox())
            else:
                im = im.convert("RGB")
            self.cache[key] = im
        return self.cache[key]

    # sizes scale gently with canvas height so 1:1 stays compact
    def sz(self, h, base):
        return int(base * {1080: .82, 1350: .92, 1920: 1.0}[h])

    def footer(self, img, h):
        fh = self.sz(h, 78)
        band = Image.new("RGBA", (W, fh), MAROON + (255,))
        d = ImageDraw.Draw(band)
        font = self.f.cinzel(500, self.sz(h, 21))
        draw_text(d, (W / 2, (fh - font.size) / 2 - 2), FOOTER, font, GOLD, tracking=1.2, anchor="c")
        img.alpha_composite(band, (0, h - fh))
        return fh

    def brand(self, img, h, dark):
        d = ImageDraw.Draw(img)
        m = self.sz(h, 56)
        font = self.f.cinzel(600, self.sz(h, 28))
        col = CREAM if dark else MAROON
        draw_text(d, (m, m), "KALA KARI CREATIONS", font, col, tracking=5)

    def badge(self, img, h, text):
        if not text:
            return
        d = ImageDraw.Draw(img)
        font = self.f.cinzel(700, self.sz(h, 26))
        m = self.sz(h, 50)
        tw = text_w(d, text, font, 4)
        pw, ph = tw + 40, font.size + 24
        x0, y0 = W - m - pw, m - 8
        d.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=ph // 2, fill=GOLD)
        draw_text(d, (x0 + 20, y0 + 10), text, font, MAROON, tracking=4)

    def price_cta(self, img, h, y, price, dark, align="l", alpha=1.0):
        """Price pill + Shop now button on one row. Returns row height."""
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        m = self.sz(h, 56)
        pf = self.f.cinzel(700, self.sz(h, 46))
        cf = self.f.cinzel(700, self.sz(h, 28))
        pw = text_w(d, price, pf) + 56
        rh = pf.size + 34
        cw = text_w(d, "SHOP NOW  →", cf, 3) + 64
        total = pw + 18 + cw
        x = m if align == "l" else (W - total) / 2
        d.rounded_rectangle((x, y, x + pw, y + rh), radius=10, fill=CREAM if dark else MAROON)
        draw_text(d, (x + 28, y + 13), price, pf, MAROON if dark else CREAM)
        cx = x + pw + 18
        d.rounded_rectangle((cx, y, cx + cw, y + rh), radius=10, fill=GOLD)
        draw_text(d, (cx + 32, y + (rh - cf.size) / 2 - 2), "SHOP NOW  →", cf, MAROON, tracking=3)
        if alpha < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
        img.alpha_composite(layer)
        return rh

    def text_stack(self, img, h, bottom, head, name, sub=None, price=None, dark=True, align="l", t=1.0):
        """Draw headline / name / sub / price row ending at y=bottom. t animates fade-up (0..1)."""
        d0 = ImageDraw.Draw(img)
        m = self.sz(h, 56)
        hf = self.f.cor_it(600, self.sz(h, 78))
        nf = self.f.cinzel(600, self.sz(h, 38))
        sf = self.f.cor_it(500, self.sz(h, 38))
        maxw = W - 2 * m
        blocks = []
        if head:
            for ln in wrap(d0, head, hf, maxw):
                blocks.append(("t", ln, hf, CREAM if dark else INK, 0, int(hf.size * 1.02)))
        if name:
            blocks.append(("gap", 10))
            for ln in wrap(d0, name.upper(), nf, maxw):
                blocks.append(("t", ln, nf, GOLD if dark else MAROON, 2, int(nf.size * 1.25)))
        if sub:
            for ln in wrap(d0, sub, sf, maxw):
                blocks.append(("t", ln, sf, CREAM if dark else INK, 0, int(sf.size * 1.25)))
        price_h = self.sz(h, 46) + 34 if price else 0
        total = sum(b[-1] if b[0] == "t" else b[1] for b in blocks) + (self.sz(h, 26) + price_h if price else 0)
        rise = int((1 - ease(t)) * 30)
        alpha = ease(t)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        y = bottom - total + rise
        for b in blocks:
            if b[0] == "gap":
                y += b[1]
                continue
            _, ln, font, col, tr, lh = b
            draw_text(d, (m if align == "l" else W / 2, y), ln, font, col, tracking=tr, anchor="l" if align == "l" else "c")
            y += lh
        if alpha < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
        img.alpha_composite(layer)
        if price:
            self.price_cta(img, h, y + self.sz(h, 26), price, dark, align, alpha)
        return total

    # ---- photo areas
    def bleed(self, h, photo, zoom=1.0, pan=(0, 0)):
        key, fx, fy = photo
        return cover(self.src(key), W, h, fx + pan[0], fy + pan[1], zoom).convert("RGBA")

    def panels(self, h, photos, labels=None, reveal=None, zoom=1.0, compact=False):
        img = cream_bg(h).convert("RGBA")
        top = self.sz(h, 140)
        bottom_text = ({1080: 250, 1350: 280, 1920: 330} if compact else {1080: 400, 1350: 470, 1920: 540})[h]
        gap = 18
        m = self.sz(h, 56)
        n = len(photos)
        pw = (W - 2 * m - gap * (n - 1)) // n
        ph = h - top - bottom_text
        lf = self.f.cinzel(600, self.sz(h, 24))
        for i, (key, fx, fy) in enumerate(photos):
            a = 1.0 if reveal is None else reveal[i]
            if a <= 0:
                continue
            p = cover(self.src(key), pw, ph, fx, fy, zoom).convert("RGBA")
            if labels:
                d = ImageDraw.Draw(p)
                lw = text_w(d, labels[i].upper(), lf, 3) + 30
                d.rectangle(((pw - lw) / 2, ph - lf.size - 34, (pw + lw) / 2, ph - 12), fill=CREAM)
                draw_text(d, (pw / 2, ph - lf.size - 26), labels[i].upper(), lf, MAROON, tracking=3, anchor="c")
            x, y = m + i * (pw + gap), top + int((1 - ease(a)) * 40)
            if a < 1:
                p.putalpha(p.getchannel("A").point(lambda v: int(v * ease(a))))
            shadowed(img, p, (x, y), blur=14, offset=(6, 10), alpha=int(60 * ease(a)))
        return img

    def cutout(self, h, photo, zoom=1.0, pan=(0, 0), compact=False):
        img = cream_bg(h).convert("RGBA")
        key, fx, fy = photo
        src = self.src(key)
        top = self.sz(h, 130)
        bottom_text = ({1080: 250, 1350: 280, 1920: 330} if compact else {1080: 380, 1350: 450, 1920: 520})[h]
        box_w, box_h = W - 2 * self.sz(h, 60), h - top - bottom_text
        if zoom <= 1.0001:
            s = min(box_w / src.width, box_h / src.height)
            p = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
            shadowed(img, p, ((W - p.width) // 2, top + (box_h - p.height) // 2))
        else:
            # zoom into the cutout: render it on cream at the box size, then crop around the focal point
            s = min(box_w / src.width, box_h / src.height) * zoom
            p = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
            fx2, fy2 = fx + pan[0], fy + pan[1]
            x = int(W / 2 - fx2 * p.width)
            y = int(top + box_h / 2 - fy2 * p.height)
            x = min(max(x, W - p.width - 40), 40) if p.width > W else (W - p.width) // 2
            layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
            shadowed(layer, p, (x, y))
            box = Image.new("L", img.size, 0)
            ImageDraw.Draw(box).rectangle((0, top - 20, W, top + box_h + 20), fill=255)
            box = box.filter(ImageFilter.GaussianBlur(14))
            layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", img.size, 0), box))
            img.alpha_composite(layer)
        return img

    # ---- compositions
    def compose(self, h, spec, t_text=1.0, zoom=1.0, pan=(0, 0), reveal=None, head=None, show_price=True):
        layout = spec["layout"]
        head = spec.get("head") if head is None else head
        if layout == "bleed":
            img = self.bleed(h, spec["photo"], zoom, pan)
            gh = int(h * (.62 if h > 1080 else .70))
            img.alpha_composite(gradient(W, gh, 0, 235), (0, h - gh))
            img.alpha_composite(gradient(W, self.sz(h, 260), 150, 0), (0, 0))
            dark = True
        elif layout == "panels":
            img = self.panels(h, spec["photos"], spec.get("labels"), reveal, zoom, compact=not show_price)
            dark = False
        else:
            img = self.cutout(h, spec["photo"], zoom, pan, compact=not show_price)
            dark = False
        fh = self.footer(img, h)
        self.brand(img, h, dark)
        self.badge(img, h, spec.get("badge"))
        bottom = h - fh - self.sz(h, 48)
        self.text_stack(img, h, bottom, head, spec.get("name"), spec.get("sub"),
                        spec.get("price") if show_price else None, dark=dark, t=t_text)
        return img

    def end_card(self, h, end, t):
        img = Image.new("RGBA", (W, h), MAROON + (255,))
        d = ImageDraw.Draw(img)
        inset = 34
        d.rectangle((inset, inset, W - inset, h - inset), outline=GOLD_DARK, width=2)
        lw = {1080: 300, 1350: 380, 1920: 470}[h]
        logo = self.logo.resize((lw, int(lw * self.logo.height / self.logo.width)), Image.LANCZOS)
        a = ease(t / .7)
        if a < 1:
            logo.putalpha(logo.getchannel("A").point(lambda v: int(v * a)))
        ly = {1080: 90, 1350: 150, 1920: 400}[h]
        img.alpha_composite(logo, ((W - logo.width) // 2, ly))
        y = ly + logo.height + self.sz(h, 70)
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        nf = self.f.cinzel(600, self.sz(h, 40))
        for ln in wrap(dl, end["name"].upper(), nf, W - 160):
            draw_text(dl, (W / 2, y), ln, nf, CREAM, tracking=2, anchor="c")
            y += int(nf.size * 1.3)
        if end.get("note"):
            sf = self.f.cor_it(500, self.sz(h, 44))
            draw_text(dl, (W / 2, y + 6), end["note"], sf, GOLD, anchor="c")
            y += sf.size + 20
        a2 = ease((t - .35) / .6)
        if a2 < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a2)))
        img.alpha_composite(layer)
        self.price_cta(img, h, y + self.sz(h, 34), end["price"], dark=True, align="c", alpha=ease((t - .7) / .6))
        cf = self.f.cinzel(500, self.sz(h, 24))
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        cy = h - inset - self.sz(h, 120)
        draw_text(dl, (W / 2, cy), "CALL / WHATSAPP  +91 94081 14592", cf, CREAM, tracking=2, anchor="c")
        draw_text(dl, (W / 2, cy + cf.size + 16), "PAN-INDIA DELIVERY  ·  VIDEO-CALL SHOPPING", cf, GOLD, tracking=2, anchor="c")
        a3 = ease((t - 1.0) / .6)
        if a3 < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a3)))
        img.alpha_composite(layer)
        return img


# ------------------------------------------------------------------- outputs
def render_image(r, ad, h, path):
    r.compose(h, ad).convert("RGB").save(path, quality=93)


def render_video(r, ad, h, path, seed):
    shots = ad["shots"]
    end_dur = 3.6
    starts, t = [], 0.0
    for s in shots:
        starts.append(t)
        t += s["dur"] - XFADE
    end_start = t
    total = end_start + end_dur
    n = int(round(total * FPS))

    def shot_frame(i, tt):
        s = dict(shots[i])
        s["badge"] = ad.get("badge")
        local = tt - starts[i]
        p = ease(local / s["dur"]) * .85 + (local / s["dur"]) * .15
        z0, z1 = s.get("z", (1.04, 1.0))
        pan = s.get("pan", (0, 0))
        reveal = None
        if s.get("stagger"):
            reveal = [min(max((local - .25 - .45 * k) / .6, 0), 1) for k in range(len(s["photos"]))]
        zoom = lerp(z0, z1, p) if s["layout"] != "panels" else lerp(1.0, 1.05, p)
        img = r.compose(h, s, t_text=min(local / .7, 1), zoom=zoom,
                        pan=(pan[0] * p, pan[1] * p), reveal=reveal, show_price=False)
        return img

    def frame(tt):
        layers = [(starts[i], i) for i, s in enumerate(shots) if starts[i] <= tt < starts[i] + s["dur"]]
        imgs = [shot_frame(i, tt) for _, i in layers]
        if tt >= end_start:
            imgs.append(r.end_card(h, ad["end"], tt - end_start))
            layers.append((end_start, -1))
        if len(imgs) == 1:
            return imgs[0]
        a = ease((tt - layers[-1][0]) / XFADE)
        return Image.blend(imgs[-2], imgs[-1], a)

    wav = os.path.join(tempfile.mkdtemp(), "m.wav")
    music.write_track(wav, n / FPS, seed=seed)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{h}", "-r", str(FPS), "-i", "-", "-i", wav, "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-profile:v", "high",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        proc.stdin.write(frame(k / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit(f"ffmpeg failed for {path}")


def main():
    images, fonts_dir, cutouts, out = sys.argv[1:5]
    only = sys.argv[5:] or list(ADS)
    r = Renderer(images, Fonts(fonts_dir), cutouts)
    for idx, aid in enumerate(ADS):
        if aid not in only:
            continue
        ad = ADS[aid]
        d = os.path.join(out, aid)
        os.makedirs(d, exist_ok=True)
        for fmt, h in FORMATS.items():
            ext = "mp4" if ad["kind"] == "video" else "jpg"
            path = os.path.join(d, f"kalakari-ad-{aid}-{fmt}.{ext}")
            (render_video(r, ad, h, path, seed=idx) if ad["kind"] == "video" else render_image(r, ad, h, path))
            print(path)


if __name__ == "__main__":
    main()
