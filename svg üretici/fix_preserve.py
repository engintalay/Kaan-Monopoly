#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).parent
count = 0
for p in root.rglob("*.svg"):
    text = p.read_text(encoding="utf-8")
    if 'preserveAspectRatio="none"' in text:
        new = text.replace('preserveAspectRatio="none"', 'preserveAspectRatio="xMidYMid meet"')
        p.write_text(new, encoding="utf-8")
        print(f"Patched: {p}")
        count += 1

print(f"Done. Patched {count} files.")
