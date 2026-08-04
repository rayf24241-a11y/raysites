#!/usr/bin/env python3
"""Build the one-page PDF for the Fiverr gig gallery -> fiverr/what-you-get.pdf

Run from the repo root:   python tools/make-gig-pdf.py

PIL renders the page as an image and saves it as a PDF; pypdf then lays real
clickable link annotations over the URLs, so the demo links actually work
instead of being pictures of text.
"""

import io
import os
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import RectangleObject

DPI = 150
PW, PH = int(8.27 * DPI), int(11.69 * DPI)          # A4 at 150 dpi
SCALE = 72.0 / DPI                                   # px -> PDF points

FONT_DIR = r"C:\Windows\Fonts" + os.sep
BOLD, SEMI, REG = "segoeuib.ttf", "seguisb.ttf", "segoeui.ttf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "https://raysites.vercel.app"
DEMOS = [
    ("Barbershop",            SITE + "/barbershop",  "Booking form, price menu, live opening hours"),
    ("Landscaping contractor", SITE + "/landscaping", "Quote form, service pricing, project gallery"),
    ("Car detailing",         SITE + "/detailing",   "Real-time 3D paint, drag-to-compare before/after"),
    ("Cocktail bar",          SITE + "/bar",         "Animated background, live open/closed status"),
]

INK, DIM, RULE = (18, 22, 32), (98, 110, 132), (222, 226, 236)
ACCENT = (28, 90, 216)


def f(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def build():
    img = Image.new("RGB", (PW, PH), (255, 255, 255))
    d = ImageDraw.Draw(img)
    M = 110
    links = []          # (x, y_top, w, h, url)

    # header
    d.rectangle([0, 0, PW, 14], fill=ACCENT)
    y = 96
    d.text((M, y), "RAYS WEB DESIGN", font=f(BOLD, 34), fill=ACCENT)
    y += 52
    d.text((M, y), "Custom websites for small businesses", font=f(BOLD, 58), fill=INK)
    y += 74
    d.text((M, y), "Built from scratch — not a template. Live in 48 hours.",
           font=f(REG, 30), fill=DIM)
    y += 74
    d.line([M, y, PW - M, y], fill=RULE, width=2)

    # demos
    y += 44
    d.text((M, y), "SEE THE WORK", font=f(BOLD, 24), fill=ACCENT)
    y += 46
    for name, url, blurb in DEMOS:
        d.text((M, y), name, font=f(SEMI, 32), fill=INK)
        y += 40
        uf = f(REG, 27)
        d.text((M, y), url, font=uf, fill=ACCENT)
        w = d.textlength(url, font=uf)
        d.line([M, y + 34, M + w, y + 34], fill=ACCENT, width=2)
        links.append((M, y, w, 34, url))
        y += 42
        d.text((M, y), blurb, font=f(REG, 25), fill=DIM)
        y += 52

    y += 10
    d.line([M, y, PW - M, y], fill=RULE, width=2)

    # what you get
    y += 44
    d.text((M, y), "WHAT YOU GET", font=f(BOLD, 24), fill=ACCENT)
    y += 46
    for line in [
        "A site designed around what your business actually does",
        "Works properly on phones, tablets and computers",
        "A contact form that emails you when someone fills it in",
        "Google Map, social links and visitor analytics if you want them",
        "Set up on your own domain, in your name — you own all of it",
    ]:
        d.ellipse([M + 4, y + 12, M + 14, y + 22], fill=ACCENT)
        d.text((M + 34, y), line, font=f(REG, 28), fill=INK)
        y += 44

    y += 24
    d.line([M, y, PW - M, y], fill=RULE, width=2)

    # pricing
    y += 44
    d.text((M, y), "WHAT IT COSTS", font=f(BOLD, 24), fill=ACCENT)
    y += 50
    cols = [("Single Page", "$80", "1 page"),
            ("Full Site", "$125", "Up to 5 pages"),
            ("Full Site & 3D", "$150", "5 pages + custom 3D")]
    cw = (PW - M * 2 - 40) / 3
    for i, (nm, price, note) in enumerate(cols):
        x = M + i * (cw + 20)
        d.rounded_rectangle([x, y, x + cw, y + 150], radius=12, outline=RULE, width=2)
        d.text((x + 22, y + 20), nm, font=f(SEMI, 26), fill=DIM)
        d.text((x + 22, y + 56), price, font=f(BOLD, 52), fill=INK)
        d.text((x + 22, y + 116), note, font=f(REG, 22), fill=DIM)
    y += 190

    # footer
    d.line([M, y, PW - M, y], fill=RULE, width=2)
    y += 34
    d.text((M, y), "Full portfolio:", font=f(REG, 28), fill=DIM)
    off = d.textlength("Full portfolio:  ", font=f(REG, 28))
    sf = f(SEMI, 28)
    d.text((M + off, y), SITE, font=sf, fill=ACCENT)
    sw = d.textlength(SITE, font=sf)
    d.line([M + off, y + 36, M + off + sw, y + 36], fill=ACCENT, width=2)
    links.append((M + off, y, sw, 36, SITE))

    return img, links


def main():
    img, links = build()
    out_dir = os.path.join(ROOT, "fiverr")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "what-you-get.pdf")

    buf = io.BytesIO()
    img.save(buf, "PDF", resolution=DPI)
    buf.seek(0)

    writer = PdfWriter()
    writer.append(PdfReader(buf))
    for (x, y, w, h, url) in links:
        # PIL is top-left origin, PDF is bottom-left
        writer.add_annotation(page_number=0, annotation=Link(
            rect=RectangleObject((x * SCALE, (PH - y - h) * SCALE,
                                  (x + w) * SCALE, (PH - y) * SCALE)),
            url=url))
    with open(out, "wb") as fh:
        writer.write(fh)

    print("%-34s %6.1f KB   %d clickable links" % (out, os.path.getsize(out) / 1024, len(links)))
    return out


if __name__ == "__main__":
    main()
