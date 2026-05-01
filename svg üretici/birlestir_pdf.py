#!/usr/bin/env python3
"""4 SVG dosyasını tek bir PDF sayfasında birleştirir"""

import subprocess
from pathlib import Path

svg_files = ["baslangic.svg", "cezaevi.svg", "ucretsiz_otopark.svg", "cezaevine_git.svg"]
pdf_files = []

# Her SVG'yi PDF'e dönüştür
for svg in svg_files:
    pdf = svg.replace(".svg", ".pdf")
    subprocess.run(["inkscape", "--export-type=pdf", f"--export-filename={pdf}", svg], 
                   capture_output=True, check=True)
    pdf_files.append(pdf)
    print(f"✓ {pdf}")

# PDF'leri birleştir
output_pdf = "monopoly_koseler.pdf"
cmd = ["pdfunite"] + pdf_files + [output_pdf]
subprocess.run(cmd, check=True)
print(f"✓ {output_pdf} oluşturuldu")

# Geçici PDF'leri sil
for pdf in pdf_files:
    Path(pdf).unlink()
