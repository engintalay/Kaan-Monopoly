#!/usr/bin/env python3
from pathlib import Path
import re

src_dir = Path(__file__).parent / 'kart_svg'
for on_path in sorted(src_dir.glob('*_on.svg')):
    base = on_path.name.rsplit('_on.svg',1)[0]
    arka_path = src_dir / f"{base}_arka.svg"
    # If arka exists and looks non-empty, skip; otherwise overwrite
    if arka_path.exists() and arka_path.stat().st_size > 200:
      print(f"Skip existing: {arka_path.name}")
      continue
    s = on_path.read_text(encoding='utf-8')
    # extract inner svg contents
    m = re.search(r"<svg[^>]*>(.*)</svg>", s, flags=re.DOTALL)
    inner = m.group(1) if m else ''
    # Build back svg: rotate 180 around center (40,27.5)
    back_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="80mm" height="55mm" viewBox="0 0 80 55" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(40,27.5) rotate(180) translate(-40,-27.5)">
{inner}
  </g>
</svg>
'''
    arka_path.write_text(back_svg, encoding='utf-8')
    print(f"Created {arka_path.name}")
print('Done')
