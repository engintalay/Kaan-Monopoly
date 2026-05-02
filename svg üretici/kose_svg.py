#!/usr/bin/env python3
"""Monopoly köşeleri - sadece resimler"""

import base64
from pathlib import Path

def resim_to_base64(path):
    with open(path, 'rb') as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

def generate_corner_svg(resim_yolu):
    img = resim_to_base64(resim_yolu)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="6.5cm" height="6.5cm" viewBox="0 0 65 65" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <image width="65" height="65" preserveAspectRatio="xMidYMid meet" xlink:href="{img}" x="0" y="0" />
</svg>
'''

# Koseler klasöründen
images_dir = Path("koseler")
resimler = sorted(images_dir.glob("*.png"))

# Sans ve kamu fonu
sans_dir = Path("sans ve komu fonu")
sans_resim = sorted(sans_dir.glob("*.png"))

koseler = [
    ("baslangic.svg", resimler[0]),
    ("cezaevi.svg", resimler[1]),
    ("ucretsiz_otopark.svg", resimler[2]),
    ("cezaevine_git.svg", resimler[3]),
]

sans_kamu = [
    ("sans.svg", sans_resim[0]),
    ("kamu_fonu.svg", sans_resim[1]),
]

for filename, resim in koseler:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(generate_corner_svg(resim))
    print(f"✓ {filename}")

for filename, resim in sans_kamu:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(generate_corner_svg(resim))
    print(f"✓ {filename}")
