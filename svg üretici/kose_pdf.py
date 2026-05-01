#!/usr/bin/env python3
"""6 SVG'yi tek bir PDF sayfasında birleştirir (2x3 grid)"""

import cairosvg
import io
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image

A4_W, A4_H = A4
MARGIN = 10 * mm
CUT_MARK_LEN = 3 * mm
DPI = 300

def draw_cut_marks(c, x, y, w, h):
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.3)
    for cx, cy, dx, dy in [
        (x, y, -1, -1), (x + w, y, 1, -1),
        (x, y, -1, 1), (x + w, y + h, 1, 1),
    ]:
        c.line(cx, cy, cx + dx * CUT_MARK_LEN, cy)
        c.line(cx, cy, cx, cy + dy * CUT_MARK_LEN)

def svg_to_png(svg_path, w_mm, h_mm):
    w_px = int(w_mm / 25.4 * DPI)
    h_px = int(h_mm / 25.4 * DPI)
    png_data = cairosvg.svg2png(url=str(svg_path), output_width=w_px, output_height=h_px)
    img = Image.open(io.BytesIO(png_data)).convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.paste(img, mask=img)
    buf = io.BytesIO()
    bg.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)

def main():
    script_dir = Path(__file__).parent.resolve()
    output_dir = script_dir / "pdf_cikti"
    output_dir.mkdir(exist_ok=True)

    svg_files = sorted(script_dir.glob("baslangic.svg")) + \
                sorted(script_dir.glob("cezaevi.svg")) + \
                sorted(script_dir.glob("ucretsiz_otopark.svg")) + \
                sorted(script_dir.glob("cezaevine_git.svg")) + \
                sorted(script_dir.glob("sans.svg")) + \
                sorted(script_dir.glob("kamu_fonu.svg"))

    if len(svg_files) < 6:
        print("6 SVG dosyası bulunamadı!")
        return

    pdf_path = output_dir / "monopoly_koseler_sans_kamu.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=A4)

    card_w = 65 * mm  # 6.5cm
    card_h = 65 * mm  # 6.5cm

    # 2x3 grid
    cols, rows = 2, 3
    total_w = cols * card_w
    total_h = rows * card_h
    x_offset = (A4_W - total_w) / 2
    y_offset = (A4_H - total_h) / 2

    positions = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
    
    for i, svg_path in enumerate(svg_files[:6]):
        col, row = positions[i]
        x = x_offset + col * card_w
        y = A4_H - y_offset - (row + 1) * card_h

        img = svg_to_png(svg_path, 65, 65)
        c.drawImage(img, x, y, card_w, card_h)
        draw_cut_marks(c, x, y, card_w, card_h)

    c.save()
    print(f"✓ monopoly_koseler_sans_kamu.pdf oluşturuldu")

if __name__ == "__main__":
    main()
