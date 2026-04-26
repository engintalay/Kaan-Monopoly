#!/usr/bin/env python3
"""
Mülk SVG Üretici
Girdi: mulkler.json
Çıktı: mülk kartları, tapu senetleri, ulaşım, utility, vergi kartları
"""

import json
import os
from pathlib import Path


def load_data(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def resim_bul(ad: str, images_dir: Path) -> str:
    for ext in ['png', 'jpg', 'jpeg']:
        p = images_dir / f"{ad}.{ext}"
        if p.exists():
            return str(p.resolve())
    for f in images_dir.iterdir():
        if f.stem.lower() in ad.lower() or ad.lower() in f.stem.lower():
            return str(f.resolve())
    return ""


def font_size(ad, base=2.8):
    return base if len(ad) <= 12 else base * 0.78 if len(ad) <= 16 else base * 0.64


def text_color(renk):
    return "black" if renk in ["#FFFF00", "#87CEEB", "#FFA500", "#FF69B4"] else "white"


# ── Mülk Kartı ──
def generate_mulk_svg(mulk, resim_yolu):
    ad, renk, fiyat = mulk['ad'], mulk['renk'], mulk['Fiyat']
    fs = font_size(ad)
    img = f'  <image width="27.55" height="30" preserveAspectRatio="none" xlink:href="{resim_yolu}" x="0.72" y="15.5" />' if resim_yolu else '  <rect x="0.72" y="15.5" width="27.55" height="30" fill="#cccccc" stroke="#999" stroke-width="0.2" />'
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <rect width="28" height="10" x="0.5" y="0.5" style="fill:{renk}" />
  <text x="14.5" y="14" font-size="{fs}" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
{img}
  <text x="14.5" y="58" font-size="3" text-anchor="middle" font-family="Arial" font-weight="bold">₺{fiyat}</text>
</svg>
'''


# ── Tapu Senedi ──
def generate_tapu_svg(mulk):
    ad, renk, fiyat = mulk['ad'], mulk['renk'], mulk['Fiyat']
    kira = mulk['kira']
    ev_m, otel_m, ipotek = mulk['ev_maliyeti'], mulk['otel_maliyeti'], mulk['ipotek']
    fs = font_size(ad, 4)
    tc = text_color(renk)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="3.5" font-size="2.5" text-anchor="middle" font-family="Arial">Tapu Senedi</text>
  <line x1="0.5" y1="5" x2="28.5" y2="5" stroke="black" stroke-width="0.3" />
  <rect x="0.5" y="5" width="28" height="7" style="fill:{renk}" />
  <text x="15" y="9.5" font-size="{fs}" text-anchor="middle" font-family="Arial" font-weight="bold" fill="{tc}">{ad}</text>
  <line x1="0.5" y1="12" x2="28.5" y2="12" stroke="black" stroke-width="0.3" />
  <g font-size="1.5" font-family="Arial">
    <text x="2" y="15">Kira – Sadece Arsa</text>
    <text x="28" y="15" text-anchor="end">{kira[0]} ₺</text>
    <text x="2" y="17.5">Kira – Tam Set</text>
    <text x="28" y="17.5" text-anchor="end">{kira[0]*2} ₺</text>
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


# ── Ulaşım Kartı ──
def generate_ulasim_svg(item):
    ad, fiyat = item['ad'], item['Fiyat']
    kira = item['kira']
    fs = font_size(ad, 3)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="5" font-size="{fs}" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <line x1="0.5" y1="7" x2="28.5" y2="7" stroke="black" stroke-width="0.3" />
  <text x="15" y="10" font-size="1.8" text-anchor="middle" font-family="Arial">🚂</text>
  <g font-size="1.5" font-family="Arial">
    <text x="2" y="20">1 İstasyon</text>
    <text x="28" y="20" text-anchor="end">{kira[0]} ₺</text>
    <text x="2" y="23">2 İstasyon</text>
    <text x="28" y="23" text-anchor="end">{kira[1]} ₺</text>
    <text x="2" y="26">3 İstasyon</text>
    <text x="28" y="26" text-anchor="end">{kira[2]} ₺</text>
    <text x="2" y="29">4 İstasyon</text>
    <text x="28" y="29" text-anchor="end">{kira[3]} ₺</text>
  </g>
  <text x="14.5" y="58" font-size="3" text-anchor="middle" font-family="Arial" font-weight="bold">₺{fiyat}</text>
</svg>
'''


# ── Utility Kartı ──
def generate_utility_svg(item):
    ad, fiyat = item['ad'], item['Fiyat']
    c = item['kira_carpan']
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="6" font-size="3.5" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <line x1="0.5" y1="8" x2="28.5" y2="8" stroke="black" stroke-width="0.3" />
  <g font-size="1.4" font-family="Arial">
    <text x="2" y="18">1 kurum varsa:</text>
    <text x="2" y="21">Zar × {c[0]} ₺</text>
    <text x="2" y="28">2 kurum varsa:</text>
    <text x="2" y="31">Zar × {c[1]} ₺</text>
  </g>
  <text x="14.5" y="58" font-size="3" text-anchor="middle" font-family="Arial" font-weight="bold">₺{fiyat}</text>
</svg>
'''


# ── Ulaşım Tapu ──
def generate_ulasim_tapu_svg(item):
    ad, fiyat = item['ad'], item['Fiyat']
    kira = item['kira']
    fs = font_size(ad, 3.5)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="3.5" font-size="2.5" text-anchor="middle" font-family="Arial">Tapu Senedi</text>
  <line x1="0.5" y1="5" x2="28.5" y2="5" stroke="black" stroke-width="0.3" />
  <text x="15" y="10" font-size="{fs}" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <line x1="0.5" y1="12" x2="28.5" y2="12" stroke="black" stroke-width="0.3" />
  <g font-size="1.5" font-family="Arial">
    <text x="2" y="17">1 İstasyon sahibiyseniz</text>
    <text x="28" y="17" text-anchor="end">{kira[0]} ₺</text>
    <text x="2" y="21">2 İstasyon sahibiyseniz</text>
    <text x="28" y="21" text-anchor="end">{kira[1]} ₺</text>
    <text x="2" y="25">3 İstasyon sahibiyseniz</text>
    <text x="28" y="25" text-anchor="end">{kira[2]} ₺</text>
    <text x="2" y="29">4 İstasyon sahibiyseniz</text>
    <text x="28" y="29" text-anchor="end">{kira[3]} ₺</text>
    <line x1="0.5" y1="31" x2="28.5" y2="31" stroke="black" stroke-width="0.2" />
    <text x="2" y="34">İpotek Değeri</text>
    <text x="28" y="34" text-anchor="end">{fiyat // 2} ₺</text>
  </g>
</svg>
'''


# ── Utility Tapu ──
def generate_utility_tapu_svg(item):
    ad, fiyat = item['ad'], item['Fiyat']
    c = item['kira_carpan']
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="3.5" font-size="2.5" text-anchor="middle" font-family="Arial">Tapu Senedi</text>
  <line x1="0.5" y1="5" x2="28.5" y2="5" stroke="black" stroke-width="0.3" />
  <text x="15" y="10" font-size="3.5" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <line x1="0.5" y1="12" x2="28.5" y2="12" stroke="black" stroke-width="0.3" />
  <g font-size="1.4" font-family="Arial">
    <text x="2" y="17">1 kurum sahibiyseniz:</text>
    <text x="2" y="20">Zar toplamı × {c[0]} ₺</text>
    <text x="2" y="26">2 kurum sahibiyseniz:</text>
    <text x="2" y="29">Zar toplamı × {c[1]} ₺</text>
    <line x1="0.5" y1="32" x2="28.5" y2="32" stroke="black" stroke-width="0.2" />
    <text x="2" y="35">İpotek Değeri</text>
    <text x="28" y="35" text-anchor="end">{fiyat // 2} ₺</text>
  </g>
</svg>
'''


# ── Vergi Kartı ──
def generate_vergi_svg(item):
    ad, ucret = item['ad'], item['ucret']
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="20" font-size="4" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <text x="15" y="35" font-size="3" text-anchor="middle" font-family="Arial">Öde: ₺{ucret}</text>
</svg>
'''


def save(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    script_dir = Path(__file__).parent.resolve()
    data = load_data(str(script_dir / "mulkler.json"))
    images_dir = script_dir / "mulk_resimleri"
    mulk_dir = script_dir / "mulkler_svg"
    tapu_dir = script_dir / "tapu_svg"
    for d in [mulk_dir, tapu_dir]:
        d.mkdir(exist_ok=True)

    count = 0

    # Arsalar
    for grup in data['arsa'].values():
        renk = grup['renk_kodu']
        for m in grup['mulkler']:
            m['renk'] = renk
            resim = resim_bul(m['ad'], images_dir)
            save(mulk_dir / f"{m['ad']}.svg", generate_mulk_svg(m, resim))
            save(tapu_dir / f"{m['ad']}_tapu.svg", generate_tapu_svg(m))
            count += 1
            print(f"  ✓ {m['ad']} (mülk + tapu)")

    # Ulaşım
    for item in data.get('ulasim', []):
        save(mulk_dir / f"{item['ad']}.svg", generate_ulasim_svg(item))
        save(tapu_dir / f"{item['ad']}_tapu.svg", generate_ulasim_tapu_svg(item))
        count += 1
        print(f"  🚂 {item['ad']} (kart + tapu)")

    # Utility
    for item in data.get('utility', []):
        save(mulk_dir / f"{item['ad']}.svg", generate_utility_svg(item))
        save(tapu_dir / f"{item['ad']}_tapu.svg", generate_utility_tapu_svg(item))
        count += 1
        print(f"  ⚡ {item['ad']} (kart + tapu)")

    # Vergiler
    for item in data.get('vergiler', []):
        save(mulk_dir / f"{item['ad']}.svg", generate_vergi_svg(item))
        count += 1
        print(f"  💰 {item['ad']}")

    print(f"\nToplam {count} kart oluşturuldu!")


if __name__ == "__main__":
    main()
