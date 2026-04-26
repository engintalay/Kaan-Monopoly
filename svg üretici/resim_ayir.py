#!/usr/bin/env python3
"""
Büyük resmi 6x5 grid olarak 30 ayrı resme böler.
Alt kısımdaki yazı alanını kırpar.
"""

from PIL import Image
from pathlib import Path

COLS, ROWS = 5, 6
TOP_TRIM = 5     # Üstten kırpma (önceki satırın yazısı)
BOTTOM_TRIM = 25  # Alttan kırpma (kendi yazısı)

NAMES = [
    # Satır 1
    "Kapadokya", "Hattuşaş", "Uzungöl", "Salda Gölü", "Abant Gölü",
    # Satır 2
    "Efes Antik Kenti", "Afrodisias", "Bergama", "Truva Antik Kenti", "Aspendos Tiyatrosu",
    # Satır 3
    "Perge Antik Kenti", "Pamukkale Travertenleri", "Safranbolu Evleri", "Galata Kulesi", "Sultanahmet Camii",
    # Satır 4
    "Süleymaniye Camii", "Selimiye Camii", "Ayasofya", "Topkapı Sarayı", "Sümela Manastırı",
    # Satır 5
    "Anıtkabir", "Dolmabahçe Sarayı", "Doğu Ekspresi", "Orient Express", "Hicaz Demiryolu",
    # Satır 6
    "Bağdat Demiryolu", "ASKİ", "TEDAŞ", "ÖTV", "KDV",
]

def main():
    script_dir = Path(__file__).parent.resolve()
    img = Image.open(script_dir / "9c184e20-7f2b-49f7-99c6-3b02b6a4c713.png")

    w, h = img.size
    cell_w, cell_h = w // COLS, h // ROWS

    output_dir = script_dir / "mulk_resimleri"
    output_dir.mkdir(exist_ok=True)

    for row in range(ROWS):
        for col in range(COLS):
            idx = row * COLS + col
            left = col * cell_w
            top = row * cell_h
            # Üstten ve alttan yazı alanını kırp
            crop_top = top + (TOP_TRIM if row > 0 else 0)
            crop_bottom = top + cell_h - BOTTOM_TRIM
            crop = img.crop((left, crop_top, left + cell_w, crop_bottom))

            name = NAMES[idx]
            out_path = output_dir / f"{name}.png"
            crop.save(out_path)
            print(f"[{idx+1}/30] {name}.png ({crop.size[0]}x{crop.size[1]})")

    print("\nTüm resimler ayrıldı!")

if __name__ == "__main__":
    main()
