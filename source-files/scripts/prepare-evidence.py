"""
Siapkan foto & screenshot bukti Climate Data Platform untuk website.

- Screenshot dasbor: logo klien, nama grup, nama staf, nama platform,
  nama file berisi nama klien, dan koordinat geotag disensor (pixelate + blur,
  tidak bisa dibaca ulang).
- Foto IoT: orientasi dibetulkan, metadata (EXIF/GPS) dibuang, foto yang
  memperlihatkan isi ruangan dipotong.

Sumber : source-files/climate-data-platform/originals/   (TIDAK dipublish)
Hasil  : src/assets/images/projects/climate-data-platform/

Jalankan dari folder proyek:
    python source-files/scripts/prepare-evidence.py            # buat gambar
    python source-files/scripts/prepare-evidence.py --preview  # cek kotak sensor
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "source-files" / "climate-data-platform" / "originals"
OUT = ROOT / "src" / "assets" / "images" / "projects" / "climate-data-platform"
PREVIEW = ROOT / "source-files" / "climate-data-platform" / "redaction-preview.png"

# Kotak yang disensor, dalam piksel gambar asli: (kiri, atas, kanan, bawah)
REDACT = {
    "dashboard-overview.png": [
        (14, 10, 140, 50),       # logo klien
        (1536, 12, 1814, 50),    # nama & jabatan staf (header)
        (1603, 70, 1770, 108),   # nama & jabatan staf (menu)
        (334, 76, 446, 104),     # nama grup klien
        (14, 910, 122, 934),     # nama platform
    ],
    "pillar-dashboard.png": [
        (12, 6, 138, 46),
        (1530, 8, 1812, 44),
        (331, 70, 444, 99),
        (12, 906, 118, 930),
    ],
    "regulatory-compliance.png": [
        (18, 12, 142, 52),
        (1535, 12, 1816, 50),
        (336, 76, 449, 104),
        (18, 910, 124, 934),
        (1322, 612, 1560, 634),  # nama file berisi nama klien
        (1322, 968, 1560, 988),
    ],
    "evidence-vault.png": [
        (12, 10, 138, 50),
        (1531, 10, 1813, 48),
        (333, 74, 446, 103),
        (12, 910, 118, 933),
        (1286, 683, 1404, 709),  # koordinat geotag
        (1286, 862, 1409, 888),
    ],
}

# Foto IoT: (nama asli, nama hasil, kotak potong atau None)
PHOTOS = [
    ("iot-unit-interior.jpg", "iot-unit-interior.jpg", None),
    ("iot-unit-enclosure-open.jpg", "iot-unit-enclosure-open.jpg", None),
    ("iot-unit-solar-mount.jpg", "iot-unit-solar-mount.jpg", (0, 720, 1152, 1560)),
]

# Thumbnail kartu karya (Home & Works), dipotong dari screenshot yang SUDAH disensor
THUMBS = [
    ("dashboard-overview.png", "thumb.png", (262, 128, 1290, 860)),
]


def redact(img, box):
    """Pixelate kasar lalu blur, supaya teks di dalam kotak tidak bisa dipulihkan."""
    region = img.crop(box)
    w, h = region.size
    block = 14
    small = region.resize((max(1, w // block), max(1, h // block)), Image.BILINEAR)
    region = small.resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(6))
    img.paste(region, box[:2])


def preview():
    """Satu gambar berisi potongan setiap kotak (garis merah) untuk dicek manual."""
    tiles = []
    for name, boxes in REDACT.items():
        img = Image.open(SRC / name).convert("RGB")
        for box in boxes:
            pad = 30
            crop_box = (max(0, box[0] - pad), max(0, box[1] - pad),
                        min(img.width, box[2] + pad), min(img.height, box[3] + pad))
            tile = img.crop(crop_box)
            ImageDraw.Draw(tile).rectangle(
                (box[0] - crop_box[0], box[1] - crop_box[1],
                 box[2] - crop_box[0], box[3] - crop_box[1]), outline="red", width=2)
            tiles.append(tile)
    width = max(t.width for t in tiles)
    sheet = Image.new("RGB", (width, sum(t.height + 8 for t in tiles)), "white")
    y = 0
    for t in tiles:
        sheet.paste(t, (0, y))
        y += t.height + 8
    sheet.save(PREVIEW)
    print("preview:", PREVIEW)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, boxes in REDACT.items():
        img = Image.open(SRC / name).convert("RGB")
        for box in boxes:
            redact(img, box)
        img.save(OUT / name, optimize=True)
        print("redacted:", name)
    for src_name, out_name, crop in PHOTOS:
        img = ImageOps.exif_transpose(Image.open(SRC / src_name)).convert("RGB")
        if crop:
            img = img.crop(crop)
        img.save(OUT / out_name, quality=90, optimize=True)  # tanpa exif=, jadi metadata terbuang
        print("photo:", out_name, img.size)
    for src_name, out_name, crop in THUMBS:
        Image.open(OUT / src_name).crop(crop).save(OUT / out_name, optimize=True)
        print("thumb:", out_name)


if __name__ == "__main__":
    preview() if "--preview" in sys.argv else build()
