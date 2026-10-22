#!/usr/bin/env python3
"""Video versions of the Diwali Dhamaka teaser (4:5, 1080x1350):

  diwali-dhamaka-swipe.mp4   the whole post as one video: slides 1-3 swipe past like a carousel, then slide 4's
                             badge builds up (frame -> Diwali -> DHAMAKA -> SALE -> COMING SOON) and repeats,
                             timed like the reference, with the reference's music
  slide-4-animated.mp4       slide 4 alone (silent, two loops) to use as the last carousel item
  slide-N-video.mp4          the four carousel slides as separate animated videos (8.5 s each, same music):
                             twinkling fireworks, swaying lanterns and a gold shine across the lettering on
                             every slide, plus the badge build-up on slide 4

Usage:
    python3 diwali_video.py <fonts_dir> <music.wav> <out_dir>             # swipe video + slide-4 animation
    python3 diwali_video.py <fonts_dir> <music.wav> <out_dir> carousel    # four separate slide videos
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diwali_carousel as C  # noqa: E402

FPS = 30
LOOP = 4.25                       # slide-4 animation length
# (time, slide position) keyframes; between pairs the view swipes with an ease
STOPS = [(0.0, 0), (2.5, 0), (2.85, 1), (4.2, 1), (4.55, 2), (5.95, 2), (6.3, 3)]
SLIDE4_START = 6.05


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def back(t, s=1.7):
    t = max(0.0, min(1.0, t)) - 1
    return t * t * ((s + 1) * t + s) + 1


def view_x(t):
    for (t0, p0), (t1, p1) in zip(STOPS, STOPS[1:]):
        if t0 <= t < t1:
            return (p0 + (p1 - p0) * ease((t - t0) / (t1 - t0))) * C.SW
    return STOPS[-1][1] * C.SW


class Slide4:
    def __init__(self, frame, parts, soon):
        self.frame, self.parts, self.soon = frame, parts, soon

    @staticmethod
    def put(img, im, cx, cy, s, a):
        if a <= 0 or s <= 0:
            return
        if abs(s - 1) > 1e-3:
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
        if a < 1:
            im = im.copy()
            im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

    def overlay(self, u):
        """Slide-4 animated layer (1080x1350) at loop time u."""
        out = Image.new("RGBA", (C.SW, C.SH), (0, 0, 0, 0))
        if u < 0:
            return out
        b = self.frame.copy()
        starts = {"diwali": .3, "dhamaka": .75, "sale": 1.2, "diya": 1.2}
        for name, im, (cx, cy) in self.parts:
            q = (u - starts[name]) / .25
            if q > 0:
                self.put(b, im, cx, cy, 1 + .45 * (1 - back(q)), min(1.0, q * 2))
        p = u / .3
        bx, by = C.BADGE_C[0] - 3 * C.SW, C.BADGE_C[1]
        self.put(out, b, bx, by, .12 + .88 * back(p), min(1.0, p * 3))
        q = (u - 1.7) / .4
        if q > 0:
            self.put(out, self.soon, C.SOON_C[0] - 3 * C.SW, C.SOON_C[1], 1 + 2.2 * (1 - ease(q)), min(1.0, q * 1.5))
        return out


def encode(frames, out, n, audio=None, dur=None, fade=0.0):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{C.SW}x{C.SH}",
           "-r", str(FPS), "-i", "-"]
    if audio:
        cmd += ["-i", audio, "-t", f"{dur:.2f}", "-c:a", "aac", "-b:a", "192k"]
        if fade:
            cmd += ["-af", f"afade=t=out:st={dur - fade:.2f}:d={fade:.2f}"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        proc.stdin.write(frames(k / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    print(out)


SLIDE_DUR = 2 * LOOP              # 8.5 s: slide 4's build-up plays twice


class Living:
    """Per-frame animation of the static decorations for one slide of the carousel."""

    def __init__(self, layers):
        self.fireworks = layers["fireworks"]
        self.text = layers["text"]
        self.lanterns = []
        for ln, x in layers["lanterns"]:
            pad = 40
            im = Image.new("RGBA", (ln.width + 2 * pad, ln.height), (0, 0, 0, 0))
            im.alpha_composite(ln, (pad, 0))
            self.lanterns.append((im, x))

    def draw(self, img, x0, t):
        for fw, cx, cy, seed in self.fireworks:
            r = fw.width / 2
            if cx + r < x0 or cx - r > x0 + C.SW:
                continue
            ph = (t + seed * .53) % 2.6
            grow = ease(ph / .9)
            a = min(1.0, ph / .2) * (1 - ease((ph - 1.5) / .8))
            if a <= 0:
                continue
            Slide4.put(img, fw, cx - x0, cy, .35 + .65 * grow, a)
        for im, x in self.lanterns:
            if x + im.width < x0 or x - im.width > x0 + C.SW:
                continue
            ang = 2.5 * math.sin(2 * math.pi * t / 2.6 + x / 300)
            rot = im.rotate(ang, resample=Image.BICUBIC, center=(im.width / 2, 0))
            img.alpha_composite(rot, (int(x - x0 - im.width / 2), 0))
        txt = self.text.crop((x0, 0, x0 + C.SW, C.SH))
        img.alpha_composite(txt)
        ph = t % 3.0
        if ph < 1.3:                                  # gold shine sweeping across the letters
            band = -400 + (C.SW + 800) * ph / 1.3
            yy, xx = np.mgrid[0:C.SH, 0:C.SW].astype(np.float32)
            k = np.exp(-(((xx - band) + (yy - C.SH / 2) * .45) / 70) ** 2)
            a = (np.asarray(txt.getchannel("A"), np.float32) / 255 * k * 150).astype(np.uint8)
            if a.max() > 0:
                shine = Image.new("RGBA", (C.SW, C.SH), (255, 252, 230, 0))
                shine.putalpha(Image.fromarray(a))
                img.alpha_composite(shine)


def carousel_videos(fonts_dir, music, out_dir):
    base, (frame, parts), soon, layers = C.scene(fonts_dir, split=True)
    s4 = Slide4(frame, parts, soon)
    live = Living(layers)
    for k in range(C.N):
        x0 = k * C.SW
        crop = base.crop((x0, 0, x0 + C.SW, C.SH))

        def render(t, crop=crop, x0=x0, k=k):
            img = crop.copy()
            live.draw(img, x0, t)
            if k == C.N - 1:
                img.alpha_composite(s4.overlay(t % LOOP))
            return img
        encode(render, os.path.join(out_dir, f"slide-{k + 1}-video.mp4"), int(SLIDE_DUR * FPS), music, SLIDE_DUR, fade=.8)


def main():
    fonts_dir, music, out_dir = sys.argv[1:4]
    base, (frame, parts), soon = C.scene(fonts_dir)
    s4 = Slide4(frame, parts, soon)
    with __import__("wave").open(music) as w:
        dur = w.getnframes() / w.getframerate()

    def swipe(t):
        x = int(round(view_x(t)))
        img = base.crop((x, 0, x + C.SW, C.SH))
        if x > 2 * C.SW:
            u = t - SLIDE4_START
            img.alpha_composite(s4.overlay(u % LOOP if u >= 0 else u), (3 * C.SW - x, 0))
        return img

    os.makedirs(out_dir, exist_ok=True)
    encode(swipe, os.path.join(out_dir, "diwali-dhamaka-swipe.mp4"), int(dur * FPS), music, dur)

    still = base.crop((3 * C.SW, 0, 4 * C.SW, C.SH))

    def slide4(t):
        img = still.copy()
        img.alpha_composite(s4.overlay(t % LOOP))
        return img
    encode(slide4, os.path.join(out_dir, "slide-4-animated.mp4"), int(2 * LOOP * FPS))


if __name__ == "__main__":
    if len(sys.argv) > 4 and sys.argv[4] == "carousel":
        carousel_videos(*sys.argv[1:4])
    else:
        main()
