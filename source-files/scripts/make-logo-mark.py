"""
Logo (kelelawar) → public/brand/logo-mark.png: hitam dengan latar transparan, dipotong rapat.
Di situs dipakai sebagai CSS mask, jadi warnanya ikut token --c-text (hitam di tema terang, putih di tema gelap).

Jalankan dari folder proyek:  python source-files/scripts/make-logo-mark.py
Sumber: source-files/brand/originals/logo-black-on-white.png (logo hitam di atas putih)
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "source-files" / "brand" / "originals" / "logo-black-on-white.png"
OUT = ROOT / "public" / "brand" / "logo-mark.png"
WIDTH = 320  # cukup tajam untuk tampil ±40 px di layar retina

im = Image.open(SRC).convert("L")
alpha = ImageOps.invert(im)  # hitam → buram, putih → transparan
alpha = alpha.point(lambda v: 0 if v < 8 else v)  # buang noise tipis di latar
alpha = alpha.crop(alpha.getbbox())
alpha = alpha.resize((WIDTH, round(alpha.height * WIDTH / alpha.width)), Image.LANCZOS)

mark = Image.new("RGBA", alpha.size, (0, 0, 0, 0))
mark.putalpha(alpha)
OUT.parent.mkdir(parents=True, exist_ok=True)
mark.save(OUT, optimize=True)
print(OUT.relative_to(ROOT), mark.size, f"{OUT.stat().st_size / 1024:.1f} KB")
