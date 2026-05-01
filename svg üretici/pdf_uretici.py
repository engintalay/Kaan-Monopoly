#!/usr/bin/env python3
"""
SVG kartlarını birebir ölçüde A4 PDF sayfalarına yerleştirir.
SVG → PNG (cairosvg) → PDF (reportlab)
"""

import cairosvg
import io
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

A4_W, A4_H = A4
MARGIN = 10 * mm
CUT_MARK_LEN = 3 * mm
DPI = 300


def draw_cut_marks(c, x, y, w, h):
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.3)
    for cx, cy, dx, dy in [
        (x, y, -1, -1), (x + w, y, 1, -1),
        (x, y + h, -1, 1), (x + w, y + h, 1, 1),
    ]:
        c.line(cx, cy, cx + dx * CUT_MARK_LEN, cy)
        c.line(cx, cy, cx, cy + dy * CUT_MARK_LEN)


def svg_to_png(svg_path, w_mm, h_mm):
    """SVG'yi PNG byte'larına çevir (300 DPI, beyaz arka plan)"""
    from PIL import Image
    w_px = int(w_mm / 25.4 * DPI)
    h_px = int(h_mm / 25.4 * DPI)
    png_data = cairosvg.svg2png(
        url=str(svg_path),
        output_width=w_px,
        output_height=h_px,
    )
    # Beyaz arka plan ekle
    img = Image.open(io.BytesIO(png_data)).convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.paste(img, mask=img)
    buf = io.BytesIO()
    bg.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def place_svgs_on_pages(c, svg_files, card_w_mm, card_h_mm, mirror_x=False):
    card_w = card_w_mm * mm
    card_h = card_h_mm * mm

    cols = int((A4_W - 2 * MARGIN) // card_w)
    rows = int((A4_H - 2 * MARGIN) // card_h)
    per_page = cols * rows

    x_offset = (A4_W - cols * card_w) / 2
    y_offset = (A4_H - rows * card_h) / 2

    for i, svg_path in enumerate(svg_files):
        if i > 0 and i % per_page == 0:
            c.showPage()

        pos = i % per_page
        col = pos % cols
        row = pos // cols

        # Arka yüzde yatay sırayı tersle (kağıt çevrilince eşleşsin)
        if mirror_x:
            col = (cols - 1) - col

        x = x_offset + col * card_w
        y = A4_H - y_offset - (row + 1) * card_h

        try:
            img = svg_to_png(svg_path, card_w_mm, card_h_mm)
            c.drawImage(img, x, y, card_w, card_h)
        except Exception as e:
            print(f"  ⚠ {svg_path.name}: {e}")

        draw_cut_marks(c, x, y, card_w, card_h)


def main():
    script_dir = Path(__file__).parent.resolve()
    mulk_dir = script_dir / "mulkler_svg"
    tapu_dir = script_dir / "tapu_svg"
    output_dir = script_dir / "pdf_cikti"
    output_dir.mkdir(exist_ok=True)

    mulk_svgs = sorted(mulk_dir.glob("*.svg"))
    if mulk_svgs:
        pdf_path = output_dir / "mulk_kartlari.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        place_svgs_on_pages(c, mulk_svgs, 29, 60)
        c.save()
        print(f"✓ {pdf_path.name} ({len(mulk_svgs)} kart)")

    tapu_svgs = sorted(tapu_dir.glob("*.svg"))
    if tapu_svgs:
        pdf_path = output_dir / "tapu_senetleri.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        place_svgs_on_pages(c, tapu_svgs, 55, 80)
        c.save()
        print(f"✓ {pdf_path.name} ({len(tapu_svgs)} kart)")

    # Şans ve Kamu Fonu kartları (ön-arka çift taraflı)
    kart_dir = script_dir / "kart_svg"
    if kart_dir.exists():
        for prefix, label in [("sans", "Şans"), ("kamu", "Kamu Fonu")]:
            on_svgs = sorted(kart_dir.glob(f"{prefix}_*_on.svg"))
            arka_svgs = sorted(kart_dir.glob(f"{prefix}_*_arka.svg"))
            if on_svgs:
                pdf_path = output_dir / f"{prefix}_kartlari.pdf"
                c = canvas.Canvas(str(pdf_path), pagesize=A4)
                # Ön yüzler
                place_svgs_on_pages(c, on_svgs, 80, 55)
                # Arka yüzler (yatay aynalı sıra, çift taraflı baskı için)
                c.showPage()
                place_svgs_on_pages(c, arka_svgs, 80, 55, mirror_x=True)
                c.save()
                print(f"✓ {pdf_path.name} ({len(on_svgs)} {label} kartı, ön + arka)")

    print(f"\nPDF'ler {output_dir} klasörüne kaydedildi!")


if __name__ == "__main__":
    main()
