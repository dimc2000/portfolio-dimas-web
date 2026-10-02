"""
Screenshot n8n Dimas (workflow Lead Follow-up) → gambar untuk situs.
Hanya potong: bilah browser, menu n8n dan tombol "Execute workflow" dibuang; isi kanvas tidak diubah.

    python source-files/scripts/prepare-lead-screens.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "source-files" / "lead-follow-up-automation" / "originals" / "n8n-screenshot.png"  # 1749x995
OUT = ROOT / "src" / "assets" / "images" / "projects" / "lead-follow-up-automation"

CROPS = {
    "n8n-canvas.png": (118, 226, 1690, 931),  # seluruh workflow
    "thumb.png": (850, 300, 1480, 760),       # kartu karya: classifier + cabang demo-ready & nurture
}

im = Image.open(SRC).convert("RGB")
OUT.mkdir(parents=True, exist_ok=True)
for name, box in CROPS.items():
    im.crop(box).save(OUT / name, optimize=True)
    print(name, box[2] - box[0], "x", box[3] - box[1])
