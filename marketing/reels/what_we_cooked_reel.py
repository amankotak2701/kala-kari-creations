#!/usr/bin/env python3
"""15 s 9:16 "WHAT WE COOKED / HOW IT LOOKED" reel, timed frame-for-frame like the reference trend reel.

- The screen is split in two. The top half shows a kurta folded on a dinner plate ("what we cooked") and the
  bottom half shows the model wearing it ("how it looked").
- The intro types both lines on black, in the reference's own rhythm: each line's reveal is measured from the
  reference, frame by frame.
- Five products cut on the reference's beats. A "Wedding Season, the Kala Kari way" card fades in from white,
  then the logo card with the website ends the reel.
- The audio is the reference's.

Usage:
    python3 what_we_cooked_reel.py <fonts_dir> <ref.mp4> <out.mp4> <plate1> <look1> ... [--preview dir f1,f2,...]
Pairs are plate/look image paths in order (five pairs fill the reference exactly; fewer stretch the last one).
A look path may end in "@fx,fy" to set the crop centre (fractions of the image), e.g. look.jpg@.6,.5
"""
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_H = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-horizontal-gold-flat.png")
LOGO_S = os.path.join(HERE, "..", "..", "brand", "logo", "kalakari-logo-stacked-maroon-flat.png")
W, H, HALF = 1080, 1920, 960
FPS = 30
# 1-based reference frames: intro, first plate, first look, product slot starts, card, logo card, end
T_PLATE1, T_LOOK1 = 30, 80
SLOTS = [30, 115, 165, 215, 265]
T_CARD, T_LOGO, N = 340, 403, 447
# line geometry in 720-px reference coordinates: (left, right, baseline)
TOP_LINE, BOT_LINE = (204, 527, 361), (229, 502, 921)
MAROON = (128, 24, 40)
CREAM = (248, 241, 228)
GOLD = (190, 150, 84)


def font(fonts, fam, w, size, style="normal"):
    return ImageFont.truetype(os.path.join(fonts, f"fontsource-{fam}", "package", "files",
                                           f"{fam}-latin-{w}-{style}.woff2"), size)


def cover(im, w, h, fx=.5, fy=.5):
    s = max(w / im.width, h / im.height)
    r = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = int(min(max(r.width * fx - w / 2, 0), r.width - w))
    y = int(min(max(r.height * fy - h / 2, 0), r.height - h))
    return r.crop((x, y, x + w, y + h))


def load(spec, w, h, default=(.5, .5)):
    path, _, at = spec.partition("@")
    fx, fy = map(float, at.split(",")) if at else default
    im = Image.open(path).convert("RGB")
    # trim 7% off the right and bottom edges: keeps the image generator's corner badge out of frame
    im = im.crop((0, 0, int(im.width * .93), int(im.height * .93)))
    return cover(im, w, h, fx, fy)


def reveal_curves(ref):
    """Fraction of each line revealed per reference frame (rightmost white pixel vs. the line's full extent)."""
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ref, "-frames:v", "100",
                    os.path.join(tmp, "%04d.png")], check=True)
    out = {}
    for key, (l, r, base) in (("top", TOP_LINE), ("bot", BOT_LINE)):
        cur = []
        for n in sorted(os.listdir(tmp)):
            a = np.asarray(Image.open(os.path.join(tmp, n)).convert("RGB")).astype(int)[base - 25:base + 3]
            xs = np.where((a.min(2) > 235).any(0))[0]
            cur.append(0.0 if len(xs) < 2 else float(np.clip((xs.max() - l) / (r - l), 0, 1)))
        out[key] = np.maximum.accumulate(np.array(cur))
    shutil.rmtree(tmp, ignore_errors=True)
    return out


class Reel:
    def __init__(self, fonts, ref, pairs):
        self.f_line = font(fonts, "poppins", 600, 46)
        self.rev = reveal_curves(ref)
        self.plates = [load(p, W, HALF) for p, _ in pairs]
        self.looks = [load(lk, W, HALF, (.5, .45)) for _, lk in pairs]
        lg = Image.open(LOGO_H).convert("RGBA")
        lg = lg.crop(lg.getbbox())
        c = Image.new("RGBA", lg.size, (255, 255, 255, 0))
        c.putalpha(lg.getchannel("A"))
        self.logo = c.resize((250, int(250 * c.height / c.width)), Image.LANCZOS)
        sh = Image.new("RGBA", (self.logo.width + 24, self.logo.height + 24), (0, 0, 0, 0))
        dark = Image.new("RGBA", self.logo.size, (40, 25, 15, 0))
        dark.putalpha(self.logo.getchannel("A").point(lambda v: int(v * .55)))
        sh.alpha_composite(dark, (12, 12))
        self.logo_sh = sh.filter(ImageFilter.GaussianBlur(4))
        n = len(pairs)
        starts = SLOTS[:n]
        self.bounds = starts + [T_CARD]
        self.lines = {k: self.text_layer(s, line) for k, s, line in
                      (("top", "WHAT WE COOKED", TOP_LINE), ("bot", "HOW IT LOOKED", BOT_LINE))}
        self.card = self.make_card(fonts)
        self.end = self.make_end(fonts)

    def text_layer(self, s, line):
        l, r, base = [v * 1.5 for v in line]
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        tw = d.textlength(s, font=self.f_line)
        x = (l + r) / 2 - tw / 2
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x + 2, base + 3), s, font=self.f_line, fill=(0, 0, 0, 110), anchor="ls")
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
        d.text((x, base), s, font=self.f_line, fill=(255, 255, 255, 255), anchor="ls")
        return lay, x, x + tw

    def put_line(self, img, key, frac):
        if frac <= 0:
            return
        lay, a, b = self.lines[key]
        cut = int(a + (b - a) * frac) + 3
        img.alpha_composite(lay.crop((0, 0, cut, H)))

    def make_card(self, fonts):
        img = Image.new("RGBA", (W, H), CREAM + (255,))
        rng = np.random.default_rng(3)
        g = np.asarray(img).astype(np.float32)
        g[..., :3] += rng.standard_normal((H, W, 1)) * 2
        img = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(img)
        for m in (46, 60):
            d.rectangle((m, m, W - m, H - m), outline=GOLD, width=2)
        lg = Image.open(LOGO_S).convert("RGBA")
        lg = lg.resize((300, int(300 * lg.height / lg.width)), Image.LANCZOS)
        img.alpha_composite(lg, ((W - lg.width) // 2, 170))
        y = 760
        d.text((W / 2, y), "Wedding Season", font=font(fonts, "cormorant-garamond", 700, 150, "italic"),
               fill=MAROON, anchor="ms")
        y += 74
        d.text((W / 2, y), "The Kala Kari Way", font=font(fonts, "cormorant-garamond", 600, 58),
               fill=MAROON, anchor="ms")
        for cx in (W / 2 - 290, W / 2 + 290):                      # little diyas either side
            d.chord((cx - 26, y - 34, cx + 26, y + 6), 0, 180, fill=GOLD)
            d.polygon([(cx, y - 52), (cx + 7, y - 36), (cx, y - 28), (cx - 7, y - 36)], fill=(226, 120, 40))
        y += 40
        f = font(fonts, "poppins", 600, 34)
        s = "Dressed by Us! Celebrated by You!"
        tw = d.textlength(s, font=f)
        d.rectangle((W / 2 - tw / 2 - 26, y, W / 2 + tw / 2 + 26, y + 62), fill=MAROON)
        d.text((W / 2, y + 31), s, font=f, fill=(255, 255, 255), anchor="mm")
        # small gold diamonds at the head and foot of the frame
        for yy in (60, H - 60):
            d.polygon([(W / 2, yy - 16), (W / 2 + 16, yy), (W / 2, yy + 16), (W / 2 - 16, yy)], fill=GOLD)
        return img

    def make_end(self, fonts):
        img = Image.new("RGBA", (W, H), (250, 249, 250, 255))
        d = ImageDraw.Draw(img)
        lg = Image.open(LOGO_S).convert("RGBA")
        lg = lg.resize((460, int(460 * lg.height / lg.width)), Image.LANCZOS)
        img.alpha_composite(lg, ((W - lg.width) // 2, 560))
        y = 560 + lg.height + 90
        d.text((W / 2, y), "www.kalakaricreations.com", font=font(fonts, "poppins", 500, 34), fill=(30, 30, 30),
               anchor="ma")
        y += 110
        f = font(fonts, "poppins", 600, 46)
        tw = d.textlength("SHOP NOW", font=f)
        d.rectangle((W / 2 - tw / 2 - 22, y, W / 2 + tw / 2 + 22, y + 74), fill=MAROON)
        d.text((W / 2, y + 37), "SHOP NOW", font=f, fill=(255, 255, 255), anchor="mm")
        d.text((W / 2, y + 110), "from our website!", font=font(fonts, "poppins", 600, 40), fill=(20, 20, 20),
               anchor="ma")
        d.text((W / 2, y + 190), "Call / WhatsApp  +91 94081 14592", font=font(fonts, "poppins", 500, 30),
               fill=(90, 90, 90), anchor="ma")
        return img

    def frame(self, f):
        if f >= T_LOGO:
            return self.end
        if f >= T_CARD:
            a = min(1.0, (f - T_CARD) / 12)
            img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
            c = self.card.copy()
            c.putalpha(int(255 * a))
            img.alpha_composite(c)
            return img
        img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        if f < T_PLATE1:
            self.put_line(img, "top", self.rev["top"][f - 1])
            return img
        i = max(k for k in range(len(self.bounds) - 1) if self.bounds[k] <= f)
        img.paste(self.plates[i], (0, 0))
        if i > 0 or f >= T_LOOK1:
            img.paste(self.looks[i], (0, HALF))
        x0 = W - self.logo.width - 36
        img.alpha_composite(self.logo_sh, (x0 - 12, 44 - 12 + 3))
        img.alpha_composite(self.logo, (x0, 44))
        self.put_line(img, "top", 1.0)
        self.put_line(img, "bot", 1.0 if (i > 0 or f >= T_LOOK1) else self.rev["bot"][min(f, 99) - 1])
        return img


def main():
    args = sys.argv[1:]
    preview = None
    if "--preview" in args:
        k = args.index("--preview")
        preview, args = args[k + 1:k + 3], args[:k]
    fonts, ref, out, imgs = args[0], args[1], args[2], args[3:]
    pairs = list(zip(imgs[0::2], imgs[1::2]))
    r = Reel(fonts, ref, pairs)
    if preview:
        d, fs = preview
        for f in map(int, fs.split(",")):
            r.frame(f).convert("RGB").save(os.path.join(d, f"wc_{f:03d}.png"))
        return
    tmp = tempfile.mkdtemp()
    for f in range(1, N + 1):
        r.frame(f).convert("RGB").save(os.path.join(tmp, f"{f:04d}.png"))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%04d.png"),
                    "-i", ref, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(out)


if __name__ == "__main__":
    main()
