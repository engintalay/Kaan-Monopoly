#!/usr/bin/env python3
import re
from pathlib import Path
out_dir = Path(__file__).parent / 'png_arka_extracts'
out_dir.mkdir(exist_ok=True)
svg_dir = Path(__file__).parent / 'kart_svg'
pattern = re.compile(r'data:image/(png|gif|jpeg);base64,([A-Za-z0-9+/=\n\r]+)')
count = 0
for svg in sorted(svg_dir.glob('*_arka.svg')):
    text = svg.read_text()
    for i, m in enumerate(pattern.finditer(text), start=1):
        ext = m.group(1)
        b64 = m.group(2).replace('\n','').replace('\r','')
        out_path = out_dir / f"{svg.stem}_img{i}.{ 'png' if ext=='png' else ('jpg' if ext in ('jpeg','jpg') else ext)}"
        out_path.write_bytes(__import__('base64').b64decode(b64))
        print(f'Wrote {out_path}')
        count += 1
print(f'Done — extracted {count} images to {out_dir}')
