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
    """Mülk adına göre resim dosyasını bul ve base64 data URI döndür"""
    import base64
    path = ""
    for ext in ['png', 'jpg', 'jpeg']:
        p = images_dir / f"{ad}.{ext}"
        if p.exists():
            path = p
            break
    if not path:
        for f in images_dir.iterdir():
            if f.stem.lower() in ad.lower() or ad.lower() in f.stem.lower():
                path = f
                break
    if not path:
        return ""
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    ext = str(path).rsplit('.', 1)[-1].lower()
    mime = {'png': 'png', 'jpg': 'jpeg', 'jpeg': 'jpeg'}.get(ext, 'png')
    return f"data:image/{mime};base64,{data}"


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
  <text x="14.5" y="58" font-size="3" text-anchor="middle" font-family="Arial" font-weight="bold">TL {fiyat}</text>
</svg>
'''


# ── Tapu Senedi ──
def generate_tapu_svg(mulk):
    ad, renk, fiyat = mulk['ad'], mulk['renk'], mulk['Fiyat']
    kira = mulk['kira']
    ev_m, otel_m, ipotek = mulk['ev_maliyeti'], mulk['otel_maliyeti'], mulk['ipotek']
    fs = font_size(ad, 5) 
    tc = text_color(renk)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="55mm" height="80mm" viewBox="0 0 55 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="54" height="79" fill="none" stroke="black" stroke-width="0.5" />
  <text x="27.5" y="5.5" font-size="3.5" text-anchor="middle" font-family="Arial">Tapu Senedi</text>
  <line x1="0.5" y1="7.5" x2="54.5" y2="7.5" stroke="black" stroke-width="0.3" />
  <rect x="0.5" y="7.5" width="54" height="10" style="fill:{renk}" />
  <text x="27.5" y="14" font-size="{fs}" text-anchor="middle" font-family="Arial" font-weight="bold" fill="{tc}">{ad}</text>
  <line x1="0.5" y1="17.5" x2="54.5" y2="17.5" stroke="black" stroke-width="0.3" />
  <g font-size="2.5" font-family="Arial">
    <text x="3" y="23">Kira – Sadece Arsa</text>
    <text x="52" y="23" text-anchor="end">{kira[0]} TL </text>
    <text x="3" y="27">Kira – Tam Set</text>
    <text x="52" y="27" text-anchor="end">{kira[0]*2} TL </text>
    <text x="3" y="31">1 Ev Kirası</text>
    <text x="52" y="31" text-anchor="end">{kira[1]} TL </text>
    <text x="3" y="35">2 Ev Kirası</text>
    <text x="52" y="35" text-anchor="end">{kira[2]} TL </text>
    <text x="3" y="39">3 Ev Kirası</text>
    <text x="52" y="39" text-anchor="end">{kira[3]} TL </text>
    <text x="3" y="43">4 Ev Kirası</text>
    <text x="52" y="43" text-anchor="end">{kira[4]} TL </text>
    <text x="3" y="47">Otel Kirası</text>
    <text x="52" y="47" text-anchor="end">{kira[5]} TL </text>
    <line x1="3" y1="49.5" x2="54.5" y2="49.5" stroke="black" stroke-width="0.2" />
    <text x="3" y="54">Evin Maliyeti (Her biri)</text>
    <text x="52" y="54" text-anchor="end">{ev_m} TL </text>
    <text x="3" y="58">Otelin Maliyeti (4 Ev +)</text>
    <text x="52" y="58" text-anchor="end">{otel_m} TL </text>
    <line x1="0.5" y1="60.5" x2="54.5" y2="60.5" stroke="black" stroke-width="0.2" />
    <text x="3" y="65">İpotek Değeri</text>
    <text x="52" y="65" text-anchor="end">{ipotek} TL </text>
  </g>
</svg>
'''


# ── Ulaşım Kartı ──
def generate_ulasim_svg(item, resim_yolu):
    ad, fiyat = item['ad'], item['Fiyat']
    kira = item['kira']
    fs = font_size(ad, 3)
    img = f'  <image width="27.55" height="20" preserveAspectRatio="xMidYMid slice" xlink:href="{resim_yolu}" x="0.72" y="8" />' if resim_yolu else ''
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="5" font-size="{fs}" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <line x1="0.5" y1="7" x2="28.5" y2="7" stroke="black" stroke-width="0.3" />
{img}
  <g font-size="1.5" font-family="Arial">
    <text x="2" y="32">1 İstasyon</text>
    <text x="28" y="32" text-anchor="end">{kira[0]} TL </text>
    <text x="2" y="35">2 İstasyon</text>
    <text x="28" y="35" text-anchor="end">{kira[1]} TL </text>
    <text x="2" y="38">3 İstasyon</text>
    <text x="28" y="38" text-anchor="end">{kira[2]} TL </text>
    <text x="2" y="41">4 İstasyon</text>
    <text x="28" y="41" text-anchor="end">{kira[3]} TL </text>
  </g>
  <text x="14.5" y="58" font-size="3" text-anchor="middle" font-family="Arial" font-weight="bold">TL {fiyat}</text>
</svg>
'''


# ── Utility Kartı ──
def generate_utility_svg(item, resim_yolu):
    ad, fiyat = item['ad'], item['Fiyat']
    c = item['kira_carpan']
    img = f'  <image width="27.55" height="20" preserveAspectRatio="xMidYMid slice" xlink:href="{resim_yolu}" x="0.72" y="8" />' if resim_yolu else ''
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="6" font-size="3.5" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <line x1="0.5" y1="7" x2="28.5" y2="7" stroke="black" stroke-width="0.3" />
{img}
  <g font-size="1.4" font-family="Arial">
    <text x="2" y="32">1 kurum varsa:</text>
    <text x="2" y="35">Zar × {c[0]} TL </text>
    <text x="2" y="40">2 kurum varsa:</text>
    <text x="2" y="43">Zar × {c[1]} TL </text>
  </g>
  <text x="14.5" y="58" font-size="3" text-anchor="middle" font-family="Arial" font-weight="bold">TL {fiyat}</text>
</svg>
'''


# ── Ulaşım Tapu ──
def generate_ulasim_tapu_svg(item):
    ad, fiyat = item['ad'], item['Fiyat']
    kira = item['kira']
    fs = font_size(ad, 5)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="55mm" height="80mm" viewBox="0 0 55 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="54" height="79" fill="none" stroke="black" stroke-width="0.5" />
  <text x="27.5" y="5.5" font-size="3.5" text-anchor="middle" font-family="Arial">Tapu Senedi</text>
  <line x1="0.5" y1="7.5" x2="54.5" y2="7.5" stroke="black" stroke-width="0.3" />
  <text x="27.5" y="14" font-size="{fs}" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <line x1="0.5" y1="17.5" x2="54.5" y2="17.5" stroke="black" stroke-width="0.3" />
  <g font-size="2.5" font-family="Arial">
    <text x="3" y="25">1 İstasyon sahibiyseniz</text>
    <text x="52" y="25" text-anchor="end">{kira[0]} TL </text>
    <text x="3" y="31">2 İstasyon sahibiyseniz</text>
    <text x="52" y="31" text-anchor="end">{kira[1]} TL </text>
    <text x="3" y="37">3 İstasyon sahibiyseniz</text>
    <text x="52" y="37" text-anchor="end">{kira[2]} TL </text>
    <text x="3" y="43">4 İstasyon sahibiyseniz</text>
    <text x="52" y="43" text-anchor="end">{kira[3]} TL </text>
    <line x1="0.5" y1="47" x2="54.5" y2="47" stroke="black" stroke-width="0.2" />
    <text x="3" y="53">İpotek Değeri</text>
    <text x="52" y="53" text-anchor="end">{fiyat // 2} TL </text>
  </g>
</svg>
'''


# ── Utility Tapu ──
def generate_utility_tapu_svg(item):
    ad, fiyat = item['ad'], item['Fiyat']
    c = item['kira_carpan']
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="55mm" height="80mm" viewBox="0 0 55 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="54" height="79" fill="none" stroke="black" stroke-width="0.5" />
  <text x="27.5" y="5.5" font-size="3.5" text-anchor="middle" font-family="Arial">Tapu Senedi</text>
  <line x1="0.5" y1="7.5" x2="54.5" y2="7.5" stroke="black" stroke-width="0.3" />
  <text x="27.5" y="14" font-size="5" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
  <line x1="0.5" y1="17.5" x2="54.5" y2="17.5" stroke="black" stroke-width="0.3" />
  <g font-size="2.5" font-family="Arial">
    <text x="3" y="25">1 kurum sahibiyseniz:</text>
    <text x="3" y="31">Zar toplamı × {c[0]} TL </text>
    <text x="3" y="40">2 kurum sahibiyseniz:</text>
    <text x="3" y="46">Zar toplamı × {c[1]} TL </text>
    <line x1="0.5" y1="50" x2="54.5" y2="50" stroke="black" stroke-width="0.2" />
    <text x="3" y="56">İpotek Değeri</text>
    <text x="52" y="56" text-anchor="end">{fiyat // 2} TL </text>
  </g>
</svg>
'''


# ── Vergi Kartı ──
def generate_vergi_svg(item, resim_yolu):
    ad, ucret = item['ad'], item['ucret']
    img = f'  <image width="27.55" height="25" preserveAspectRatio="xMidYMid slice" xlink:href="{resim_yolu}" x="0.72" y="8" />' if resim_yolu else ''
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="29mm" height="60mm" viewBox="0 0 29 60" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0.5" y="0.5" width="28" height="59" fill="none" stroke="black" stroke-width="0.5" />
  <text x="15" y="6" font-size="4" text-anchor="middle" font-family="Arial" font-weight="bold">{ad}</text>
{img}
  <text x="15" y="45" font-size="3" text-anchor="middle" font-family="Arial">Öde: TL {ucret}</text>
</svg>
'''


def save(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def img_to_base64(path):
    import base64
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    ext = str(path).rsplit('.', 1)[-1].lower()
    mime = {'png': 'png', 'jpg': 'jpeg', 'jpeg': 'jpeg'}.get(ext, 'png')
    return f"data:image/{mime};base64,{data}"


# ── Şans / Kamu Fonu Ön Yüz ──
def etki_ikonu_svg(etki):
    """Etkiye göre basit SVG ikon döndür"""
    if 'para_al' in etki:
        return '<circle cx="52" cy="18" r="6" fill="#4CAF50" opacity="0.15"/><text x="52" y="21" font-size="8" text-anchor="middle" font-family="Arial" fill="#4CAF50">+</text>'
    if 'para_ode' in etki:
        return '<circle cx="52" cy="18" r="6" fill="#F44336" opacity="0.15"/><text x="52" y="21" font-size="8" text-anchor="middle" font-family="Arial" fill="#F44336">-</text>'
    if 'cezaevine' in etki:
        return '<rect x="46" y="12" width="12" height="12" rx="1" fill="none" stroke="#333" stroke-width="0.8"/><line x1="49" y1="12" x2="49" y2="24" stroke="#333" stroke-width="0.6"/><line x1="52" y1="12" x2="52" y2="24" stroke="#333" stroke-width="0.6"/><line x1="55" y1="12" x2="55" y2="24" stroke="#333" stroke-width="0.6"/>'
    if 'hapisten_cikis' in etki:
        return '<rect x="46" y="12" width="12" height="12" rx="1" fill="none" stroke="#4CAF50" stroke-width="0.8"/><path d="M50 18 L54 22 L60 14" fill="none" stroke="#4CAF50" stroke-width="1"/>'
    if 'ulasim' in etki:
        return '<circle cx="52" cy="18" r="6" fill="#795548" opacity="0.15"/><text x="52" y="21" font-size="7" text-anchor="middle" font-family="Arial" fill="#795548">T</text>'
    if 'altyapi' in etki:
        return '<circle cx="52" cy="18" r="6" fill="#FF9800" opacity="0.15"/><text x="52" y="21.5" font-size="8" text-anchor="middle" font-family="Arial" fill="#FF9800">~</text>'
    if 'geri_git' in etki:
        return '<path d="M46 18 L58 18 M46 18 L50 14 M46 18 L50 22" fill="none" stroke="#333" stroke-width="0.8"/>'
    if 'pahali' in etki:
        return '<path d="M47 24 L52 12 L57 24 Z" fill="none" stroke="#333" stroke-width="0.8"/><line x1="49" y1="20" x2="55" y2="20" stroke="#333" stroke-width="0.6"/>'
    if 'herkese_para_ode' in etki or 'herkesten_para_al' in etki:
        return '<circle cx="48" cy="18" r="3" fill="none" stroke="#333" stroke-width="0.6"/><circle cx="52" cy="16" r="3" fill="none" stroke="#333" stroke-width="0.6"/><circle cx="56" cy="18" r="3" fill="none" stroke="#333" stroke-width="0.6"/>'
    return ''


def generate_kart_on_svg(kart, renk, baslik_renk):
    baslik = kart['baslik']
    aciklama = kart['aciklama']
    ikon = etki_ikonu_svg(kart['etki'])

    words = aciklama.split()
    lines, line = [], ""
    for w in words:
        if len(line + " " + w) > 32:
            lines.append(line.strip())
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        lines.append(line)

    total_h = len(lines) * 5.5
    y_start = 30 + (22 - total_h) / 2
    text_lines = "\n".join(
        f'    <text x="52" y="{y_start + i*5.5}" font-size="3.8" text-anchor="middle" font-family="Arial">{l}</text>'
        for i, l in enumerate(lines)
    )

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="80mm" height="55mm" viewBox="0 0 80 55" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="80" height="55" fill="white" />
  <rect x="0.5" y="0.5" width="79" height="54" fill="none" stroke="black" stroke-width="0.5" />
  <rect x="0.5" y="0.5" width="18" height="54" fill="{renk}" />
  <text x="9.5" y="22" font-size="5.5" text-anchor="middle" font-family="Arial" font-weight="bold" fill="{baslik_renk}" transform="rotate(-90, 9.5, 27.5)">{baslik}</text>
  <line x1="18.5" y1="0.5" x2="18.5" y2="54.5" stroke="black" stroke-width="0.3" />
  {ikon}
  <line x1="30" y1="26" x2="74" y2="26" stroke="#ddd" stroke-width="0.3" />
  <g>
{text_lines}
  </g>
</svg>
'''


# ── Şans / Kamu Fonu Arka Yüz ──
def generate_kart_arka_svg(resim_base64):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="80mm" height="55mm" viewBox="0 0 80 55" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <image width="80" height="55" preserveAspectRatio="xMidYMid slice" xlink:href="{resim_base64}" x="0" y="0" />
</svg>
'''


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
        resim = resim_bul(item['ad'], images_dir)
        save(mulk_dir / f"{item['ad']}.svg", generate_ulasim_svg(item, resim))
        save(tapu_dir / f"{item['ad']}_tapu.svg", generate_ulasim_tapu_svg(item))
        count += 1
        print(f"  🚂 {item['ad']} (kart + tapu)")

    # Utility
    for item in data.get('utility', []):
        resim = resim_bul(item['ad'], images_dir)
        save(mulk_dir / f"{item['ad']}.svg", generate_utility_svg(item, resim))
        save(tapu_dir / f"{item['ad']}_tapu.svg", generate_utility_tapu_svg(item))
        count += 1
        print(f"  ⚡ {item['ad']} (kart + tapu)")

    # Vergiler
    for item in data.get('vergiler', []):
        resim = resim_bul(item['ad'], images_dir)
        save(mulk_dir / f"{item['ad']}.svg", generate_vergi_svg(item, resim))
        count += 1
        print(f"  💰 {item['ad']}")

    print(f"\nToplam {count} kart oluşturuldu!")

    # Şans ve Kamu Fonu kartları
    kart_json = script_dir / "kamu fonu ve sans kartlari.json"
    if kart_json.exists():
        kart_data = load_data(str(kart_json))
        kart_dir = script_dir / "kart_svg"
        kart_dir.mkdir(exist_ok=True)

        resim_dir = script_dir / "sans ve komu fonu"
        sans_arka = img_to_base64(resim_dir / "sans.png")
        kamu_arka = img_to_base64(resim_dir / "kamu fonu.png")

        kart_count = 0
        for kart in kart_data.get('sans_kartlari', []):
            save(kart_dir / f"sans_{kart['id']:02d}_on.svg",
                 generate_kart_on_svg(kart, "#C41E3A", "white"))
            save(kart_dir / f"sans_{kart['id']:02d}_arka.svg",
                 generate_kart_arka_svg(sans_arka))
            kart_count += 1

        for kart in kart_data.get('kamu_fonu_kartlari', []):
            save(kart_dir / f"kamu_{kart['id']:02d}_on.svg",
                 generate_kart_on_svg(kart, "#1B3A5C", "white"))
            save(kart_dir / f"kamu_{kart['id']:02d}_arka.svg",
                 generate_kart_arka_svg(kamu_arka))
            kart_count += 1

        print(f"🎴 {kart_count} şans/kamu fonu kartı oluşturuldu (ön + arka)")


if __name__ == "__main__":
    main()
