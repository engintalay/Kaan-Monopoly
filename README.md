# 🎲 Kaan Monopoly — Türkiye Temalı Monopoly Oyunu

Türkiye'nin tarihi ve kültürel mekanlarını konu alan, tamamen özel tasarım bir Monopoly oyunu. 3D baskı ile üretilen oyun tahtası, özel mülk kartları ve tapu senetleri içerir.

## 🗺️ Oyun İçeriği

| Tür | Adet | Açıklama |
|-----|-------|----------|
| Arsa Mülkleri | 22 | 8 renk grubunda Türkiye mekanları |
| Ulaşım | 4 | Doğu Ekspresi, Orient Express, Hicaz/Bağdat Demiryolu |
| Kurum | 2 | ASKİ, TEDAŞ |
| Vergi | 2 | ÖTV, KDV |

### 🏘️ Renk Grupları

| Renk | Mülkler | Fiyat Aralığı |
|------|---------|---------------|
| 🟤 Kahverengi | Kapadokya, Hattuşaş | 60 TL |
| 🔵 Açık Mavi | Uzungöl, Salda Gölü, Abant Gölü | 100–120 TL |
| 🩷 Pembe | Efes, Afrodisias, Bergama | 140–160 TL |
| 🟠 Turuncu | Truva, Aspendos, Perge | 180–200 TL |
| 🔴 Kırmızı | Pamukkale, Safranbolu, Galata Kulesi | 220–240 TL |
| 🟡 Sarı | Sultanahmet, Süleymaniye, Selimiye | 260–280 TL |
| 🟢 Yeşil | Ayasofya, Topkapı Sarayı, Sümela | 300–320 TL |
| 🔵 Mavi | Anıtkabir, Dolmabahçe Sarayı | 350–400 TL |

## 📁 Proje Yapısı

```
Kaan Monopoly/
├── svg üretici/
│   ├── mulkler.json          # Tüm oyun verileri (mülk, kira, maliyet)
│   ├── svg_uretici.py        # Mülk kartı + tapu senedi SVG üretici
│   ├── resim_ayir.py         # Kaynak resmi 30 parçaya böler
│   ├── pdf_uretici.py        # SVG'lerden baskıya hazır A4 PDF üretir
│   ├── mulk.svg              # Örnek mülk kartı şablonu
│   ├── tapuSenedi.svg        # Örnek tapu senedi şablonu
│   ├── mulkler_svg/          # Üretilen mülk kartları (29×60mm)
│   ├── tapu_svg/             # Üretilen tapu senetleri (55×80mm)
│   ├── mulk_resimleri/       # Kesilmiş mülk resimleri
│   ├── pdf_cikti/            # Baskıya hazır PDF dosyaları
│   └── 3D oyun/              # Oyun tahtası STL dosyaları
├── monopoly_*.FCMacro        # FreeCAD makroları (3D parçalar)
└── YAPILACAKLAR.md           # Proje takip listesi
```

## 🛠️ Kullanım

### Gereksinimler

```bash
pip install Pillow cairosvg reportlab svglib
```

### Kartları Üret

```bash
cd "svg üretici"

# 1. Kaynak resmi 30 parçaya böl
python3 resim_ayir.py

# 2. Mülk kartları + tapu senetleri oluştur
python3 svg_uretici.py

# 3. Baskıya hazır A4 PDF üret
python3 pdf_uretici.py
```

### Çıktılar

- **`pdf_cikti/mulk_kartlari.pdf`** — 30 mülk kartı, A4 sayfalarda kesim çizgileriyle (29×60mm)
- **`pdf_cikti/tapu_senetleri.pdf`** — 28 tapu senedi, A4 sayfalarda kesim çizgileriyle (55×80mm)

> 💡 Yazdırırken **"Gerçek Boyut"** veya **"%100 Ölçek"** seçeneğini kullanın.

## 🖨️ 3D Baskı

`3D oyun/` klasöründeki STL dosyaları:

| Dosya | Açıklama |
|-------|----------|
| `tabla_son.stl` | Oyun tahtası |
| `tile_son.stl` | Kare parçalar |
| `corner_son.stl` | Köşe parçaları |
| `Tumu_bir_arada.stl` | Tüm parçalar birleşik |

FreeCAD makroları (`monopoly_*.FCMacro`) ile 3D modeller düzenlenebilir.

## 📝 Lisans

Bu proje kişisel kullanım amaçlı tasarlanmıştır.
