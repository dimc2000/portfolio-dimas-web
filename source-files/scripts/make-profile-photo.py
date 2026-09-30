"""
Foto profil (avatar di Home + gambar OG) dari foto asli → src/assets/images/profile-photo.webp

Hanya koreksi foto biasa: crop, sedikit terang di bayangan, sedikit kontras, dan penajaman ringan.
SENGAJA tanpa AI upscale / face restore / penghalus kulit: bentuk wajah tidak boleh berubah
dan hasilnya tidak boleh terlihat seperti gambar AI (permintaan Dimas, 30-09-2026).

    python source-files/scripts/make-profile-photo.py
    python source-files/scripts/make-og-image.py   # gambar preview link ikut diperbarui
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "source-files" / "profile" / "originals" / "profile-rooftop.jpg"  # 1024x1024, tidak dipublish
OUT = ROOT / "src" / "assets" / "images" / "profile-photo.webp"

# Kotak persegi: kepala dan bahu di tengah lingkaran avatar (foto asli 1024x1024)
CENTER, SIZE = (485, 520), 760

im = Image.open(SRC).convert("RGB")
cx, cy = CENTER
im = im.crop((cx - SIZE // 2, cy - SIZE // 2, cx + SIZE // 2, cy + SIZE // 2))

# Bayangan sedikit diangkat (wajah agak gelap dibanding langit), highlight tidak disentuh
x = np.arange(256) / 255
lut = np.clip(255 * (x + 0.10 * x * (1 - x) ** 2), 0, 255).astype(np.uint8).tolist()
im = im.point(lut * 3)

im = ImageEnhance.Contrast(im).enhance(1.04)
# "Clarity": kontras lokal radius besar, sangat tipis
im = im.filter(ImageFilter.UnsharpMask(radius=30, percent=10, threshold=0))
# Detail halus (rambut, mata, rajutan baju); threshold menjaga kulit tetap alami
im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=55, threshold=3))

im.save(OUT, "WEBP", quality=90, method=6)
print(f"{OUT.relative_to(ROOT)}  {im.size[0]}x{im.size[1]}  {OUT.stat().st_size / 1024:.0f} KB")
