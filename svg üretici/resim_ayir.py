#!/usr/bin/env python3
"""
Büyük resmi 4x5 grid olarak 20 ayrı resme böler.
"""

from PIL import Image
from pathlib import Path

COLS, ROWS = 5, 4

NAMES = [
    "Kapadokya", "Hattuşaş", "Anıtkabir", "Dolmabahçe Sarayı", "Ayasofya",
    "Topkapı Sarayı", "Sümela Manastırı", "Sultanahmet Camii", "Süleymaniye Camii", "Selimiye Camii",
    "Pamukkale", "Safranbolu Evleri", "Galata Kulesi", "Truva Antik Kenti", "Aspendos Tiyatrosu",
    "Perge Antik Kenti", "Efes Antik Kenti", "Afrodisias", "Bergama Antik Kenti", "Nemrut Dağı",
]

def main():
    script_dir = Path(__file__).parent.resolve()
    img = Image.open(script_dir / "1a3e34f9-5085-4285-8b8b-1df1d9057def.png")
    
    w, h = img.size
    cell_w, cell_h = w // COLS, h // ROWS
    
    output_dir = script_dir / "mulk_resimleri"
    output_dir.mkdir(exist_ok=True)
    
    for row in range(ROWS):
        for col in range(COLS):
            idx = row * COLS + col
            left = col * cell_w
            top = row * cell_h
            crop = img.crop((left, top, left + cell_w, top + cell_h))
            
            name = NAMES[idx]
            out_path = output_dir / f"{name}.png"
            crop.save(out_path)
            print(f"[{idx+1}/20] {name}.png")
    
    print("\nTüm resimler ayrıldı!")

if __name__ == "__main__":
    main()
