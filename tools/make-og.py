#!/usr/bin/env python3
"""Generate the Open Graph preview cards in og/.

Run from the repo root:   python tools/make-og.py

Needs Pillow (pip install pillow) and the Segoe UI fonts that ship with
Windows. On macOS/Linux, point FONT_DIR at any directory containing a
bold/semibold/regular sans family and rename the three constants below.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
FONT_DIR = r"C:\Windows\Fonts" + os.sep
BOLD, SEMI, REG = "segoeuib.ttf", "seguisb.ttf", "segoeui.ttf"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def hx(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def glow(size, bg, blobs):
    """Soft radial blooms: rendered tiny, then upscaled. Cheap and smooth."""
    sw, sh = 160, 84
    img = Image.new("RGB", (sw, sh), hx(bg))
    px = img.load()
    for y in range(sh):
        for x in range(sw):
            r, g, b = px[x, y]
            for (cx, cy, rad, col, amt) in blobs:
                dx, dy = (x / sw - cx), (y / sh - cy)
                d = (dx * dx + dy * dy) ** .5
                k = max(0.0, 1.0 - d / rad) ** 2 * amt
                cr, cg, cb = hx(col)
                r = min(255, int(r + cr * k))
                g = min(255, int(g + cg * k))
                b = min(255, int(b + cb * k))
            px[x, y] = (r, g, b)
    return img.resize(size, Image.BICUBIC)


def track(d, xy, text, f, fill, sp):
    """Letter-spaced text — PIL has no tracking, so step glyph by glyph."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + sp
    return x


def card(path, bg, blobs, accent, label, title, sub, strip, light=False, rings=()):
    img = glow((W, H), bg, blobs)
    d = ImageDraw.Draw(img, "RGBA")

    for rad, alpha in rings:
        d.ellipse([980 - rad, 300 - rad, 980 + rad, 300 + rad],
                  outline=hx(accent) + (alpha,), width=3)

    ink = hx("#12181c") if light else hx("#f5f7ff")
    muted = hx("#5f6f66") if light else hx("#9aa3c4")

    track(d, (76, 74), label, font(BOLD, 21), hx(accent), 5)
    d.rectangle([76, 118, 150, 123], fill=hx(accent))

    y = 176
    for line, size in title:
        d.text((76, y), line, font=font(BOLD, size), fill=ink)
        y += int(size * 1.12)

    d.text((76, y + 22), sub, font=font(REG, 30), fill=muted)
    d.rectangle([76, H - 118, W - 76, H - 117], fill=muted + (70,))
    d.text((76, H - 92), strip, font=font(SEMI, 25), fill=hx(accent))

    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    img.save(full, "PNG", optimize=True)
    return os.path.getsize(full)


CARDS = [
    ("og/portfolio.png", "#05060a",
     [(.72, .18, .62, "#b98cff", .55), (.14, .86, .55, "#7af0ff", .34),
      (.94, .80, .45, "#ff7ac8", .30)],
     "#7af0ff", "RAY  \u00b7  WEB DESIGN",
     [("Websites that", 84), ("don't look cheap.", 84)],
     "Custom built. Live in 48 hours.",
     "$150 FLAT   \u00b7   YOU PAY AFTER YOU SEE IT",
     False, [(150, 60), (196, 38), (242, 22)]),

    ("og/barbershop.png", "#0d0b09",
     [(.78, .22, .60, "#d99a4e", .50), (.10, .90, .55, "#8c3b2b", .45)],
     "#d99a4e", "IRONSIDE BARBER CO.",
     [("A proper cut,", 82), ("and nothing rushed.", 82)],
     "Straight razor shaves. Classic fades.",
     "EST. 2011   \u00b7   WALK-INS WELCOME, 7 DAYS",
     False, [(150, 55), (196, 34)]),

    ("og/landscaping.png", "#fbfaf7",
     [(.80, .16, .58, "#cfe4d6", .85), (.10, .92, .55, "#e3ecd9", .85)],
     "#1d6444", "CEDAR & STONE LANDSCAPING",
     [("A yard you're", 80), ("proud to pull up to.", 80)],
     "Lawn care, garden design and patios.",
     "FREE ESTIMATES   \u00b7   FAMILY OWNED SINCE 2009",
     True, [(150, 45), (196, 28)]),

    ("og/detailing.png", "#07080b",
     [(.74, .20, .60, "#c8d0dd", .34), (.16, .88, .55, "#e03131", .46)],
     "#e03131", "APEX AUTO DETAILING",
     [("Make it look", 84), ("better than new.", 84)],
     "Paint correction and 9H ceramic coating.",
     "MOBILE   \u00b7   ONE CAR A DAY   \u00b7   5 YEAR WARRANTY",
     False, [(150, 70), (200, 44), (250, 26)]),

    ("og/bar.png", "#0a0705",
     [(.68, .42, .66, "#e8873c", .52), (.16, .86, .50, "#8e2f3f", .46)],
     "#e8873c", "THE EMBER ROOM",
     [("Low light,", 88), ("long list.", 88)],
     "A small dark room behind an unmarked door.",
     "COCKTAILS   \u00b7   OPEN LATE   \u00b7   CLOSED MONDAYS",
     False, [(150, 58), (198, 36)]),
]

if __name__ == "__main__":
    for args in CARDS:
        print("%-26s %6.1f KB" % (args[0], card(*args) / 1024))
