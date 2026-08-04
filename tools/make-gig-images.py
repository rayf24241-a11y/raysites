#!/usr/bin/env python3
"""Generate Fiverr gig gallery images (1280 x 769) into fiverr/.

Run from the repo root:   python tools/make-gig-images.py

Fiverr allows three gallery images per service. The first one is what shows
in search results, so it carries the offer; the second proves range; the
third leads with the thing almost no other seller at this price can do.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 769
FONT_DIR = r"C:\Windows\Fonts" + os.sep
BOLD, SEMI, REG = "segoeuib.ttf", "seguisb.ttf", "segoeui.ttf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Starting price shown on image 1. Change it here, rerun, re-upload.
BASE_PRICE = 80


def font(n, s):
    return ImageFont.truetype(FONT_DIR + n, s)


def hx(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def glow(size, bg, blobs):
    sw, sh = 160, 96
    img = Image.new("RGB", (sw, sh), hx(bg))
    px = img.load()
    for y in range(sh):
        for x in range(sw):
            r, g, b = px[x, y]
            for (cx, cy, rad, col, amt) in blobs:
                dx, dy = (x / sw - cx), (y / sh - cy)
                k = max(0.0, 1.0 - ((dx * dx + dy * dy) ** .5) / rad) ** 2 * amt
                cr, cg, cb = hx(col)
                r = min(255, int(r + cr * k)); g = min(255, int(g + cg * k)); b = min(255, int(b + cb * k))
            px[x, y] = (r, g, b)
    return img.resize(size, Image.BICUBIC)


def centre(d, y, text, f, fill, w=W):
    d.text(((w - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)


def track(d, xy, text, f, fill, sp):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + sp
    return x


def track_w(d, text, f, sp):
    return sum(d.textlength(c, font=f) + sp for c in text) - sp


def browser(d, x, y, w, h, accent, bg="#0d1018", *, hero_h=None, cards=3):
    """A browser window with an abstract page inside — reads as 'website'
    instantly at thumbnail size, which is the entire job of image one."""
    bar = max(26, int(h * 0.075))
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=hx(bg),
                        outline=(255, 255, 255, 40), width=2)
    d.rounded_rectangle([x, y, x + w, y + bar], radius=14, fill=(255, 255, 255, 16))
    d.rectangle([x, y + bar - 14, x + w, y + bar], fill=(255, 255, 255, 16))
    for i in range(3):
        cx = x + 20 + i * 17
        d.ellipse([cx, y + bar / 2 - 5, cx + 10, y + bar / 2 + 5], fill=(120, 132, 160))
    d.rounded_rectangle([x + 78, y + bar * 0.24, x + w - 22, y + bar * 0.76],
                        radius=7, fill=(255, 255, 255, 20))

    inner_y = y + bar
    hh = hero_h if hero_h else int(h * 0.42)
    d.rectangle([x, inner_y, x + w, inner_y + hh], fill=hx(accent))
    pad = int(w * 0.055)
    d.rounded_rectangle([x + pad, inner_y + hh * 0.30, x + pad + w * 0.44, inner_y + hh * 0.30 + 15],
                        radius=7, fill=(255, 255, 255, 220))
    d.rounded_rectangle([x + pad, inner_y + hh * 0.52, x + pad + w * 0.30, inner_y + hh * 0.52 + 9],
                        radius=4, fill=(255, 255, 255, 140))
    d.rounded_rectangle([x + pad, inner_y + hh * 0.70, x + pad + w * 0.17, inner_y + hh * 0.70 + 20],
                        radius=6, fill=(255, 255, 255, 245))

    cy = inner_y + hh + int(h * 0.06)
    cw = (w - pad * 2 - (cards - 1) * 14) / cards
    ch = h - (cy - y) - int(h * 0.07)
    for i in range(cards):
        cx = x + pad + i * (cw + 14)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=9, fill=(255, 255, 255, 26))
        d.rounded_rectangle([cx + 12, cy + 14, cx + cw * 0.62, cy + 24], radius=4, fill=(255, 255, 255, 120))
        d.rounded_rectangle([cx + 12, cy + 34, cx + cw * 0.82, cy + 41], radius=3, fill=(255, 255, 255, 60))


def orb(diameter, base, rim="#7af0ff"):
    """A properly shaded sphere — diffuse falloff, a clearcoat specular and a
    fresnel rim. Rendered small and upscaled so the gradients stay smooth."""
    s = 240
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    px = img.load()
    br, bg_, bb = hx(base)
    rr, rg, rb = hx(rim)
    lx, ly, lz = -0.42, -0.62, 0.66          # key light, upper-left-front
    for y in range(s):
        for x in range(s):
            nx = (x - s / 2) / (s / 2)
            ny = (y - s / 2) / (s / 2)
            d2 = nx * nx + ny * ny
            if d2 > 1.0:
                continue
            nz = (1.0 - d2) ** .5
            diff = max(0.0, nx * lx + ny * ly + nz * lz)
            spec = diff ** 48
            fres = (1.0 - nz) ** 3
            r = br * (0.16 + diff * 0.95) + 255 * spec * 0.95 + rr * fres * 0.55
            g = bg_ * (0.16 + diff * 0.95) + 255 * spec * 0.95 + rg * fres * 0.55
            b = bb * (0.16 + diff * 0.95) + 255 * spec * 0.95 + rb * fres * 0.55
            a = 255 if d2 < 0.985 else int(255 * (1 - (d2 - 0.985) / 0.015))
            px[x, y] = (min(255, int(r)), min(255, int(g)), min(255, int(b)), a)
    return img.resize((diameter, diameter), Image.LANCZOS)


# ---------------------------------------------------------------- image 1
def card_offer(path):
    img = glow((W, H), "#05060a", [(.74, .14, .60, "#b98cff", .55),
                                   (.12, .88, .55, "#7af0ff", .34),
                                   (.95, .84, .45, "#ff7ac8", .30)])
    d = ImageDraw.Draw(img, "RGBA")
    f = font(BOLD, 24)
    track(d, ((W - track_w(d, "RAYS WEB DESIGN", f, 6)) / 2, 58), "RAYS WEB DESIGN", f, hx("#7af0ff"), 6)
    centre(d, 100, "Custom Website", font(BOLD, 82), hx("#f4f6ff"))
    centre(d, 186, "in 48 Hours", font(BOLD, 82), hx("#f4f6ff"))
    browser(d, 300, 300, 680, 330, "#1d2450")
    strip = "FROM $%d   ·   CUSTOM BUILT, NOT A TEMPLATE" % BASE_PRICE
    sf = font(BOLD, 27)
    sw = d.textlength(strip, font=sf)
    x0, x1 = 300, 980
    assert sw < (x1 - x0) - 48, "price strip overflows its pill: %.0f px" % sw
    d.rounded_rectangle([x0, 668, x1, 736], radius=16, fill=(255, 255, 255, 24),
                        outline=hx("#7af0ff") + (150,), width=2)
    d.text(((W - sw) / 2, 689), strip, font=sf, fill=hx("#eaf3ff"))
    img.save(os.path.join(ROOT, path), "PNG", optimize=True)
    return path


# ---------------------------------------------------------------- image 2
def card_range(path):
    img = glow((W, H), "#05060a", [(.5, .10, .70, "#b98cff", .40), (.10, .92, .50, "#7af0ff", .26)])
    d = ImageDraw.Draw(img, "RGBA")
    centre(d, 48, "Built From Scratch For Your Business", font(BOLD, 56), hx("#f4f6ff"))
    centre(d, 118, "Not a template. Every site designed around what you actually do.",
           font(REG, 28), hx("#9aa3c4"))

    shots = [("#8c3b2b", "BARBERSHOP"), ("#1d6444", "LANDSCAPING"),
             ("#9e1f1f", "CAR DETAILING"), ("#b8632c", "BAR / RESTAURANT")]
    bw, bh, gx, gy = 560, 250, 40, 34
    x0 = (W - (bw * 2 + gx)) / 2
    for i, (accent, label) in enumerate(shots):
        bx = x0 + (i % 2) * (bw + gx)
        by = 190 + (i // 2) * (bh + gy + 34)
        browser(d, bx, by, bw, bh, accent, cards=3)
        f = font(BOLD, 19)
        track(d, (bx + 4, by + bh + 10), label, f, hx("#8f9ab6"), 3)
    img.save(os.path.join(ROOT, path), "PNG", optimize=True)
    return path


# ---------------------------------------------------------------- image 3
def card_3d(path):
    img = glow((W, H), "#06070b", [(.66, .40, .62, "#2f6bd8", .48),
                                   (.16, .86, .52, "#e03131", .34),
                                   (.90, .16, .42, "#c8d0dd", .26)])
    d = ImageDraw.Draw(img, "RGBA")
    f = font(BOLD, 24)
    track(d, (72, 58), "SOMETHING MOST CHEAP SITES CAN'T DO", f, hx("#7af0ff"), 5)
    # left column must clear the browser window at x=700
    hf = font(BOLD, 62)
    for i, line in enumerate(["Real-time 3D,", "right in the browser."]):
        assert 72 + d.textlength(line, font=hf) < 690, "headline overflows into the mockup: " + line
        d.text((72, 112 + i * 72), line, font=hf, fill=hx("#f4f6ff"))
    d.text((72, 274), "No plugin. No app. Spin it, zoom it,", font=font(REG, 30), fill=hx("#9aa3c4"))
    d.text((72, 314), "recolour it — on a phone.", font=font(REG, 30), fill=hx("#9aa3c4"))

    # a browser window with a real shaded 3D object sitting inside it
    bx, by, bw, bh = 700, 120, 508, 400
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16, fill=hx("#0a0d16"),
                        outline=(255, 255, 255, 46), width=2)
    d.rounded_rectangle([bx, by, bx + bw, by + 34], radius=16, fill=(255, 255, 255, 18))
    d.rectangle([bx, by + 20, bx + bw, by + 34], fill=(255, 255, 255, 18))
    for i in range(3):
        cx = bx + 18 + i * 16
        d.ellipse([cx, by + 12, cx + 9, by + 21], fill=(120, 132, 160))
    d.rounded_rectangle([bx + 70, by + 9, bx + bw - 18, by + 25], radius=6, fill=(255, 255, 255, 22))

    d.ellipse([bx + 118, by + 322, bx + bw - 118, by + 356], fill=(0, 0, 0, 150))
    ball = orb(250, "#1b4fb0")
    img.paste(ball, (bx + int((bw - 250) / 2), by + 68), ball)

    for i, t in enumerate(["Interactive 3D", "Loads in under a second", "Works on any phone"]):
        x, y = 72, 470 + i * 52
        d.ellipse([x, y + 9, x + 13, y + 22], fill=hx("#7af0ff"))
        d.text((x + 28, y), t, font=font(SEMI, 27), fill=hx("#cfe0ff"))
    img.save(os.path.join(ROOT, path), "PNG", optimize=True)
    return path


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "fiverr"), exist_ok=True)
    for fn, p in ((card_offer, "fiverr/1-offer.png"),
                  (card_range, "fiverr/2-range.png"),
                  (card_3d,    "fiverr/3-3d.png")):
        fn(p)
        print("%-22s %6.1f KB" % (p, os.path.getsize(os.path.join(ROOT, p)) / 1024))
