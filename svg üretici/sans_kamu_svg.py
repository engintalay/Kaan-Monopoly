#!/usr/bin/env python3
"""Şans ve Kamu Fonu kartları SVG üretir"""

import json
from pathlib import Path
import base64


def load_data(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def resim_to_base64(path):
    with open(path, 'rb') as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"


def generate_sans_kamu_svg(kart, resim_base64, renk):
    baslik = kart['baslik']
    aciklama = kart['aciklama']
    
    lines = []
    words = aciklama.split()
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= 35:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    text_y = 25
    text_content = ""
    for line in lines:
        text_content += f'  <text x="14.5" y="{text_y}" font-size="2.2" text-anchor="middle" font-family="Arial">{line}</text>\n'
        text_y += 3
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <rect width="28" height="10" x="0.5" y="0.5" style="fill:{renk}" />
  <text x="14.5" y="14" font-size="3" text-anchor="middle" font-family="Arial" font-weight="bold">{baslik}</text>
    <image width="27.55" height="25" preserveAspectRatio="xMidYMid meet" xlink:href="{resim_base64}" x="0.72" y="16" />
{text_content}
</svg>
'''


def main():
    script_dir = Path(__file__).parent.resolve()
    data = load_data(str(script_dir / "kamu fonu ve sans kartlari.json"))
    
    # Resimler
    sans_resim = script_dir / "sans ve komu fonu" / "sans.png"
    kamu_resim = script_dir / "sans ve komu fonu" / "kamu fonu.png"
    sans_base64 = resim_to_base64(sans_resim) if sans_resim.exists() else ""
    kamu_base64 = resim_to_base64(kamu_resim) if kamu_resim.exists() else ""
    
    # SVG klasörü
    svg_dir = script_dir / "kart_svg"
    svg_dir.mkdir(exist_ok=True)
    
    # Şans kartları
    for kart in data['sans_kartlari']:
        svg = generate_sans_kamu_svg(kart, sans_base64, "#FF69B4")
        with open(svg_dir / f"sans_{kart['id']}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"✓ sans_{kart['id']}.svg")
    
    # Kamu fonu kartları
    for kart in data['kamu_fonu_kartlari']:
        svg = generate_sans_kamu_svg(kart, kamu_base64, "#008000")
        with open(svg_dir / f"kamu_fonu_{kart['id']}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"✓ kamu_fonu_{kart['id']}.svg")
    
    print(f"\nToplam {len(data['sans_kartlari']) + len(data['kamu_fonu_kartlari'])} kart oluşturuldu!")


if __name__ == "__main__":
    main()
