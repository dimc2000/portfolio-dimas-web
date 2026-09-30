"""
Latar bintang untuk tema gelap → public/theme/stars.webp (animasi) + stars-still.webp (diam)

Sumber: source-files/theme/originals/stars.gif (480x800, 18 frame, 120 ms).
- 3 baris piksel putih di dasar GIF dibuang (kalau tidak, muncul garis saat diulang).
- Enam salinan disusun 3x2 menjadi 1440x1592. Tiap salinan dimulai di frame berbeda dan
  sebagian dicerminkan, jadi bintang jatuhnya tidak bergerak serempak di layar lebar.
- stars-still.webp dipakai kalau pengunjung mematikan animasi (prefers-reduced-motion).

    python source-files/scripts/make-star-background.py
"""
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "source-files" / "theme" / "originals" / "stars.gif"
OUT = ROOT / "public" / "theme"

TILE_W, TILE_H = 480, 796          # tinggi 796: baris 797-799 berwarna putih
COLS, ROWS = 3, 2
OFFSETS = [0, 9, 4, 13, 7, 16]     # frame awal tiap salinan
MIRROR = [False, True, False, True, False, True]

gif = Image.open(SRC)
frames, durations = [], []
for i in range(gif.n_frames):
    gif.seek(i)
    frames.append(gif.convert("RGB").crop((0, 0, TILE_W, TILE_H)))
    durations.append(gif.info.get("duration", 120))

out_frames = []
for t in range(len(frames)):
    canvas = Image.new("RGB", (TILE_W * COLS, TILE_H * ROWS), "black")
    for k in range(COLS * ROWS):
        tile = frames[(t + OFFSETS[k]) % len(frames)]
        if MIRROR[k]:
            tile = ImageOps.mirror(tile)
        canvas.paste(tile, ((k % COLS) * TILE_W, (k // COLS) * TILE_H))
    out_frames.append(canvas)

OUT.mkdir(parents=True, exist_ok=True)
anim = OUT / "stars.webp"
out_frames[0].save(anim, save_all=True, append_images=out_frames[1:], duration=durations, loop=0,
                   lossless=False, quality=70, method=6)
still = OUT / "stars-still.webp"
out_frames[0].save(still, quality=70, method=6)
for f in (anim, still):
    print("wrote", f.relative_to(ROOT), f"{f.stat().st_size // 1024} KB")
