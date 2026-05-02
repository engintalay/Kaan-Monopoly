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


def place_svgs_on_pages(c, svg_files, card_w_mm, card_h_mm, mirror_x=False, bleed_mm=0):
    card_w = card_w_mm * mm
    card_h = card_h_mm * mm
    bleed = bleed_mm * mm

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
            # If mirror_x is requested (backs page), rotate each card appropriately
            # so that when sheet is flipped for double-sided printing the
            # front and back align correctly. Rotate around card center.
            # shrink more to provide extra inner margin so text doesn't touch edges
            scale_front = 0.92
            scale_back = 0.80
            scale = scale_back if mirror_x else scale_front
            if mirror_x:
                cx = x + card_w / 2
                cy = y + card_h / 2
                c.saveState()
                c.translate(cx, cy)
                # apply inward horizontal shift (toward page center) before rotation
                # determine side: left halves shift right (+), right halves shift left (-)
                try:
                    cols_local = cols
                except NameError:
                    cols_local = 1
                shift_mm = 2.5
                shift_pts = shift_mm * mm
                shift_dir = 1 if col < (cols_local / 2) else -1
                # vertical inward shift: move toward page center (top rows move down, bottom rows move up)
                try:
                    rows_local = rows
                except NameError:
                    rows_local = 1
                shift_dir_y = -1 if row < (rows_local / 2) else 1
                shift_y_pts = shift_mm * mm
                c.translate(shift_dir * shift_pts, shift_dir_y * shift_y_pts)
                # For long-edge duplex printing, rotate 180° so front/back align
                c.rotate(180)
                # After rotating 180°, draw with same width/height (no swap)
                draw_w = card_w * scale + 2 * bleed
                draw_h = card_h * scale + 2 * bleed
                c.drawImage(img, -draw_w / 2, -draw_h / 2, draw_w, draw_h,
                            preserveAspectRatio=True, anchor='c')
                c.restoreState()
            else:
                # Draw front image with preserved aspect ratio and centered
                draw_w = card_w * scale + 2 * bleed
                draw_h = card_h * scale + 2 * bleed
                x_centered = x + (card_w - draw_w) / 2
                y_centered = y + (card_h - draw_h) / 2
                c.drawImage(img, x_centered, y_centered, draw_w, draw_h,
                            preserveAspectRatio=True, anchor='c')
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

                # Also produce a print-ready PDF with bleed and crop marks
                pdf_path_pr = output_dir / f"{prefix}_kartlari_printready.pdf"
                c_pr = canvas.Canvas(str(pdf_path_pr), pagesize=A4)
                place_svgs_on_pages(c_pr, on_svgs, 80, 55, bleed_mm=3)
                c_pr.showPage()
                place_svgs_on_pages(c_pr, arka_svgs, 80, 55, mirror_x=True, bleed_mm=3)
                c_pr.save()
                print(f"✓ {pdf_path_pr.name} ({len(on_svgs)} {label} kartı, print-ready)")

    print(f"\nPDF'ler {output_dir} klasörüne kaydedildi!")


if __name__ == "__main__":
    main()
