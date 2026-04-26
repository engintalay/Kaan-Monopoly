# Monopoly Türkiye — Yapılacaklar

## Durum Göstergesi
- [ ] Bekliyor
- [x] Tamamlandı
- [~] Devam ediyor

---

## Tamamlanan İşler

- [x] `monopoly_square_tile.FCMacro` — puzzle bağlantı sistemi (boyun+kafa, 8×5mm, r=5.5mm)
- [x] `monopoly_corner_tiles.FCMacro` — her köşeye özel puzzle bağlantı tarafları
- [x] `monopoly_buildings.FCMacro` — ev çatısı solid prism, `import math` kaldırıldı
- [x] `monopoly_tokens.FCMacro` — köpek bacakları z-offset düzeltildi
- [x] Tüm grup makroları (01-08) — puzzle bağlantı sistemi
- [x] `monopoly_istasyonlar.FCMacro` — puzzle bağlantı sistemi
- [x] `monopoly_ozel_kareler.FCMacro` — puzzle bağlantı sistemi
- [x] `CLAUDE.md` ve `YAPILACAKLAR.md` oluşturuldu
- [x] Tüm makrolardan kabartma metin kaldırıldı (Draft/FONT/add_embossed_text) — üstüne kağıt yapıştırılacak
- [x] `monopoly_taban_plaka.FCMacro` — FlashForge AD5X (220×220mm) uyumlu 12 parça ray sistemi

---

## Yapılacaklar

### Renk Grupları (Mülk Kareleri)
- [x] `monopoly_group_01_mor.FCMacro` — Çatalhöyük (60₺), Divriği Ulu Camii (60₺)
- [x] `monopoly_group_02_acik_mavi.FCMacro` — Aspendos (100₺), Perge (100₺), Side (120₺)
- [x] `monopoly_group_03_pembe.FCMacro` — Harran (140₺), Göbekli Tepe (140₺), Nemrut Dağı (160₺)
- [x] `monopoly_group_04_turuncu.FCMacro` — Afrodisyas (180₺), Pamukkale (180₺), Efes (200₺)
- [x] `monopoly_group_05_kirmizi.FCMacro` — Troya (220₺), Bergama (220₺), Sardes (240₺)
- [x] `monopoly_group_06_sari.FCMacro` — Kapadokya (260₺), Konya (260₺), Edirne (280₺)
- [x] `monopoly_group_07_yesil.FCMacro` — Eyüp Sultan (300₺), Topkapı (300₺), Dolmabahçe (320₺)
- [x] `monopoly_group_08_lacivert.FCMacro` — Sultanahmet (350₺), Ayasofya (400₺)

### İstasyonlar
- [x] `monopoly_istasyonlar.FCMacro` — Süleymaniye, Selimiye, Anıtkabir, Bursa Ulu Camii (her biri 200₺)

### Özel Kareler
- [x] `monopoly_ozel_kareler.FCMacro` — Şans ×3, Topluluk Fonu ×3, Gelir Vergisi, Lüks Vergisi, Boğaz Köprüsü, İpek Yolu

---

## Teknik Notlar

- Tüm tile yüzeyleri düz — üstüne kağıt etiket yapıştırılacak (Draft/metin kodu kaldırıldı)
- Mülk değerleri tarihi/kültürel öneme + UNESCO statüsüne göre ölçeklendi
- `make_tile_shape()` fonksiyonu puzzle bağlantılı tile geometrisini üretir
- İstasyonlar ve özel kareler: renk şeridi yok, düz taban
- Taban plaka: U-kanal ray sistemi, tile puzzle tabları segmentleri birbirine kilitler
- Köşe tablası: düz plaka (4 köşe için identical, montajda döndürülür)
- Basım: Ray Kısa 160×47×8mm, Ray Uzun 200×47×8mm, Köşe 66×66×3mm — hepsi 220mm'e sığar

---

## Renk Referansı

| Grup | RGB |
|---|---|
| Mor | (0.55, 0.0, 0.55) |
| Açık Mavi | (0.4, 0.7, 1.0) |
| Pembe | (1.0, 0.4, 0.7) |
| Turuncu | (1.0, 0.6, 0.0) |
| Kırmızı | (0.9, 0.1, 0.1) |
| Sarı | (1.0, 0.9, 0.0) |
| Yeşil | (0.0, 0.7, 0.2) |
| Lacivert | (0.0, 0.0, 0.8) |
| İstasyon | (0.5, 0.5, 0.5) |
