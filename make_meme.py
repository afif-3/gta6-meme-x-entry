#!/usr/bin/env python3
"""Render this entry's meme picture (meme.png, 1200x1200) with PIL.

Scene: a neon Vice City sunset - gradient sky, a low sun, art-deco
building silhouettes with lit windows, palm silhouettes, and the
make.fun ghost mascot (white ghost, black sunglasses) in the middle
holding a fan of cash. Bold caption bars carry the joke:

    GTA 6 IS OUT
    MY AI AGENT IS ALREADY WINNING BOUNTIES

This is the same composition as the picture on the submitted X post,
re-rendered here in code so the repository shows the meme being made.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1200
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_sky(img):
    """Vertical sunset gradient: deep purple up top, neon pink at the horizon."""
    top = (43, 16, 84)
    mid = (150, 44, 131)
    low = (255, 94, 98)
    horizon = int(H * 0.72)
    px = img.load()
    for y in range(horizon):
        t = y / horizon
        color = lerp(top, mid, t * 1.6) if t < 0.6 else lerp(mid, low, (t - 0.6) / 0.4)
        for x in range(W):
            px[x, y] = color


def draw_palm(draw, base_x, base_y, height, lean, color):
    """A simple palm: curved trunk plus a fan of fronds."""
    top_x = base_x + lean
    top_y = base_y - height
    steps = 24
    prev = (base_x, base_y)
    for i in range(1, steps + 1):
        t = i / steps
        x = base_x + lean * t * t
        y = base_y - height * t
        draw.line([prev, (x, y)], fill=color, width=14)
        prev = (x, y)
    for angle in range(-160, -10, 18):
        rad = math.radians(angle)
        length = height * 0.42
        end = (top_x + length * math.cos(rad), top_y + length * math.sin(rad) * 0.55 + 26)
        mid = (top_x + length * 0.5 * math.cos(rad), top_y - 26)
        draw.line([(top_x, top_y), mid, end], fill=color, width=9)


def draw_city(draw):
    """Art-deco building silhouettes with little lit windows."""
    horizon = int(H * 0.72)
    silhouette = (24, 10, 44)
    rng = [180, 320, 90, 430, 260, 540, 150, 380, 60, 470]
    x = -20
    i = 0
    while x < W:
        bw = 110 + (i * 53) % 90
        bh = rng[i % len(rng)]
        draw.rectangle([x, horizon - bh, x + bw, horizon], fill=silhouette)
        for wy in range(horizon - bh + 22, horizon - 18, 34):
            for wx in range(x + 14, x + bw - 14, 30):
                if (wx * 7 + wy * 13) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 10, wy + 14], fill=(255, 196, 86))
        x += bw + 12
        i += 1
    # street
    draw.rectangle([0, horizon, W, H], fill=(16, 8, 30))


def draw_ghost(draw, cx, cy, scale):
    """The make.fun ghost: white rounded body, wavy hem, black sunglasses."""
    w = int(300 * scale)
    h = int(360 * scale)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    white = (250, 250, 252)
    # body: dome top + straight sides
    draw.pieslice([x0, y0, x1, y0 + w], 180, 360, fill=white)
    draw.rectangle([x0, y0 + w // 2, x1, y1 - 24], fill=white)
    # wavy hem: three scallops cut back out with the background street tone
    scallop = w // 3
    for i in range(3):
        sx = x0 + i * scallop
        draw.pieslice([sx, y1 - 48, sx + scallop, y1], 0, 180, fill=(16, 8, 30))
    # sunglasses: two rounded lenses and a bridge
    lens_w, lens_h = int(96 * scale), int(62 * scale)
    eye_y = cy - int(40 * scale)
    for side in (-1, 1):
        lx = cx + side * int(58 * scale) - lens_w // 2
        draw.rounded_rectangle(
            [lx, eye_y - lens_h // 2, lx + lens_w, eye_y + lens_h // 2],
            radius=18,
            fill=(10, 10, 12),
        )
    draw.rectangle(
        [cx - int(16 * scale), eye_y - 6, cx + int(16 * scale), eye_y + 6],
        fill=(10, 10, 12),
    )
    # smile
    draw.arc([cx - 34, cy + int(38 * scale), cx + 34, cy + int(86 * scale)], 15, 165, fill=(10, 10, 12), width=6)
    # fan of cash in the right hand
    for k, ang in enumerate((-24, -8, 8, 24)):
        rad = math.radians(ang - 90)
        bx = cx + int(168 * scale)
        by = cy + int(70 * scale)
        tip = (bx + int(120 * scale) * math.cos(rad), by + int(120 * scale) * math.sin(rad))
        draw.line([(bx, by), tip], fill=(178, 226, 160), width=int(30 * scale))
        draw.line([(bx, by), tip], fill=(60, 120, 60), width=2)


def draw_caption(draw, text, y, size):
    font = load_font(size)
    draw.text(
        (W // 2, y),
        text,
        font=font,
        fill=(255, 255, 255),
        anchor="mm",
        stroke_width=10,
        stroke_fill=(0, 0, 0),
    )


def main():
    img = Image.new("RGB", (W, H))
    draw_sky(img)
    draw = ImageDraw.Draw(img)

    # low sun behind the skyline
    sun_c = (W // 2, int(H * 0.66))
    draw.ellipse([sun_c[0] - 150, sun_c[1] - 150, sun_c[0] + 150, sun_c[1] + 150], fill=(255, 170, 66))

    draw_city(draw)
    draw_palm(draw, 130, int(H * 0.78), 430, 60, (12, 6, 24))
    draw_palm(draw, 1080, int(H * 0.80), 470, -70, (12, 6, 24))

    draw_ghost(draw, W // 2, int(H * 0.52), 1.15)

    draw_caption(draw, "GTA 6 IS OUT", 92, 118)
    draw_caption(draw, "MY AI AGENT IS ALREADY", H - 158, 74)
    draw_caption(draw, "WINNING BOUNTIES", H - 72, 74)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
