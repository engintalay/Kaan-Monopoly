#!/usr/bin/env python3
"""4 köşe SVG'ini tek bir sayfada birleştirir (2x2 grid)"""

from pathlib import Path
import re

def combine_svgs():
    svgs = []
    for name in ["baslangic", "cezaevi", "ucretsiz_otopark", "cezaevine_git"]:
        svg_path = Path(f"{name}.svg")
        if svg_path.exists():
            with open(svg_path, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', content)
            if match:
                w, h = float(match.group(1)), float(match.group(2))
                inner = re.search(r'<svg[^>]*>(.*?)</svg>', content, re.DOTALL)
                if inner:
                    svgs.append((inner.group(1), w, h))
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="13cm" height="13cm" viewBox="0 0 13 13" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
'''
    positions = [(0, 0), (6.5, 0), (0, 6.5), (6.5, 6.5)]
    for i, (inner, w, h) in enumerate(svgs):
        x, y = positions[i]
        svg_content += f'  <g transform="translate({x}, {y})">\n'
        svg_content += inner.strip() + '\n'
        svg_content += '  </g>\n'
    
    svg_content += '</svg>\n'
    
    with open("monopoly_koseler.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("✓ monopoly_koseler.svg oluşturuldu")

if __name__ == "__main__":
    combine_svgs()
