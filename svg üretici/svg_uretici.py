#!/usr/bin/env python3
"""
Mülk SVG Üretici
Girdi: mulkler.json (gruplu yapı)
Çıktı: Her mülk için <ad>.svg (mülk kartı) ve <ad>_tapu.svg (tapu senedi)
"""

import json
import os
from pathlib import Path


def load_mulkler(json_path: str) -> list[dict]:
    """JSON dosyasından mülk verilerini düz listeye çevir"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mulkler = []
    for grup_key, grup in data['arsa'].items():
        renk = grup['renk_kodu']
        for m in grup['mulkler']:
            mulkler.append({**m, 'renk': renk})
    return mulkler


def resim_bul(ad: str, images_dir: Path) -> str:
    """Mülk adına göre resim dosyasını bul"""
    # Doğrudan eşleşme
    for ext in ['png', 'jpg', 'jpeg']:
        p = images_dir / f"{ad}.{ext}"
        if p.exists():
            return str(p.resolve())
    # Kısmi eşleşme (ör: "Pamukkale Travertenleri" -> "Pamukkale.png")
    for f in images_dir.iterdir():
        stem = f.stem.lower()
        ad_lower = ad.lower()
        if stem in ad_lower or ad_lower in stem:
            return str(f.resolve())
    return ""


def generate_mulk_svg(mulk: dict, resim_yolu: str) -> str:
    """Mülk kartı SVG'si"""
    ad = mulk['ad']
    renk = mulk['renk']
    fiyat = mulk['Fiyat']
    font_size = 2.8 if len(ad) <= 12 else 2.2 if len(ad) <= 16 else 1.8

    image_block = ""
    if resim_yolu:
        image_block = f'''  <image
     width="27.55"
     height="30"
     preserveAspectRatio="none"
     xlink:href="{resim_yolu}"
     x="0.72"
     y="15.5"
     id="image1" />'''
    else:
        image_block = '''  <rect x="0.72" y="15.5" width="27.55" height="30"
     fill="#cccccc" stroke="#999999" stroke-width="0.2" />'''

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" version="1.1"
   xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <rect style="fill:{renk}" width="28" height="10" x="0.5" y="0.5" />
  <text x="14.5" y="14" font-size="{font_size}" text-anchor="middle" fill="black"
     font-family="Arial" font-weight="bold">{ad}</text>
{image_block}
  <text x="14.5" y="58" font-size="3" text-anchor="middle" fill="black"
     font-family="Arial" font-weight="bold">₺{fiyat}</text>
</svg>
'''


def generate_tapu_svg(mulk: dict) -> str:
    """Tapu senedi SVG'si"""
    ad = mulk['ad']
    renk = mulk['renk']
    fiyat = mulk['Fiyat']
    kira = mulk['kira']  # [arsa, 1ev, 2ev, 3ev, 4ev, otel]
    ev_m = mulk['ev_maliyeti']
    otel_m = mulk['otel_maliyeti']
    ipotek = mulk['ipotek']
    font_size = 4 if len(ad) <= 12 else 3 if len(ad) <= 16 else 2.5

    # Kira x2 (tam set)
    kira_tam = kira[0] * 2

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" version="1.1"
   xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="3.5" font-size="2.5" text-anchor="middle" font-family="Arial">Tapu Senedi</text>
  <line x1="0.5" y1="5" x2="28.5" y2="5" stroke="black" stroke-width="0.3" />
  <rect x="0.5" y="5" width="28" height="7" style="fill:{renk}" />
  <text x="15" y="9.5" font-size="{font_size}" text-anchor="middle" font-family="Arial"
     font-weight="bold" fill="{"black" if renk in ["#FFFF00","#87CEEB","#FFA500","#FF69B4"] else "white"}">{ad}</text>
  <line x1="0.5" y1="12" x2="28.5" y2="12" stroke="black" stroke-width="0.3" />
  <g font-size="1.5" font-family="Arial">
    <text x="2" y="15">Kira – Sadece Arsa</text>
    <text x="28" y="15" text-anchor="end">{kira[0]} ₺</text>
    <text x="2" y="17.5">Kira – Sadece Arsa (Tam Set)</text>
    <text x="28" y="17.5" text-anchor="end">{kira_tam} ₺</text>
    <text x="2" y="20">1 Ev Kirası</text>
    <text x="28" y="20" text-anchor="end">{kira[1]} ₺</text>
    <text x="2" y="22.5">2 Ev Kirası</text>
    <text x="28" y="22.5" text-anchor="end">{kira[2]} ₺</text>
    <text x="2" y="25">3 Ev Kirası</text>
    <text x="28" y="25" text-anchor="end">{kira[3]} ₺</text>
    <text x="2" y="27.5">4 Ev Kirası</text>
    <text x="28" y="27.5" text-anchor="end">{kira[4]} ₺</text>
    <text x="2" y="30">Otel Kirası</text>
    <text x="28" y="30" text-anchor="end">{kira[5]} ₺</text>
    <line x1="2" y1="31.5" x2="28.5" y2="31.5" stroke="black" stroke-width="0.2" />
    <text x="2" y="34">Evin Maliyeti (Her biri)</text>
    <text x="28" y="34" text-anchor="end">{ev_m} ₺</text>
    <text x="2" y="36.5">Otelin Maliyeti (4 Ev +)</text>
    <text x="28" y="36.5" text-anchor="end">{otel_m} ₺</text>
    <line x1="0.5" y1="38" x2="28.5" y2="38" stroke="black" stroke-width="0.2" />
    <text x="2" y="40.5">İpotek Değeri</text>
    <text x="28" y="40.5" text-anchor="end">{ipotek} ₺</text>
  </g>
</svg>
'''


def main():
    script_dir = Path(__file__).parent.resolve()
    json_path = script_dir / "mulkler.json"
    images_dir = script_dir / "mulk_resimleri"
    output_dir = script_dir / "mulkler_svg"
    tapu_dir = script_dir / "tapu_svg"
    output_dir.mkdir(exist_ok=True)
    tapu_dir.mkdir(exist_ok=True)

    mulkler = load_mulkler(str(json_path))
    print(f"{len(mulkler)} mülk yüklendi.\n")

    for i, mulk in enumerate(mulkler, 1):
        ad = mulk['ad']
        resim_yolu = resim_bul(ad, images_dir)

        # Mülk kartı
        svg = generate_mulk_svg(mulk, resim_yolu)
        p = output_dir / f"{ad}.svg"
        with open(p, 'w', encoding='utf-8') as f:
            f.write(svg)

        # Tapu senedi
        tapu = generate_tapu_svg(mulk)
        tp = tapu_dir / f"{ad}_tapu.svg"
        with open(tp, 'w', encoding='utf-8') as f:
            f.write(tapu)

        print(f"[{i}/{len(mulkler)}] {ad} → mülk + tapu")

    print("\nTüm SVG dosyaları oluşturuldu!")


if __name__ == "__main__":
    main()
