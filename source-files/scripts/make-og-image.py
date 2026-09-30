"""
Buat gambar preview link (Open Graph) 1200x630 → public/og.jpg
Dipakai halaman yang tidak punya gambar sendiri (Home, Works, Services, Contact, Design).

    python source-files/scripts/make-og-image.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PHOTO = ROOT / "src" / "assets" / "images" / "profile-photo.webp"
OUT = ROOT / "public" / "og.jpg"
FONTS = Path(r"C:\Windows\Fonts")

W, H = 1200, 630
TEXT, MUTED, LINK, PRIMARY, SOFT = "#21243d", "#687684", "#007a99", "#ff6464", "#edf7fa"


def font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    heebo = sorted((ROOT / ".astro" / "fonts").glob(f"font-heebo-{700 if bold else 400}-normal-latin-*.woff2"))
    for path in heebo + [FONTS / ("segoeuib.ttf" if bold else "segoeui.ttf")]:
        try:
            fnt = ImageFont.truetype(str(path), size)
        except OSError:
            continue
        try:
            fnt.set_variation_by_axes([700 if bold else 400])  # Heebo = variable font
        except (OSError, ValueError):
            pass
        return fnt
    return ImageFont.load_default(size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=fnt) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]


im = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(im)

# Foto profil dengan lingkaran biru muda di belakangnya (seperti avatar di Home)
size = 330
cx, cy = 925, 300
d.ellipse((cx - size // 2 - 14, cy - size // 2 + 18, cx + size // 2 - 14, cy + size // 2 + 18), fill=SOFT)
photo = Image.open(PHOTO).convert("RGBA").resize((size, size), Image.LANCZOS)
mask = Image.new("L", (size, size), 0)
ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
alpha = Image.composite(photo.getchannel("A"), mask, mask)
im.paste(photo, (cx - size // 2, cy - size // 2), alpha)

x, max_w = 80, 620
d.text((x, 120), "CREATIVE DEVELOPER", font=font(True, 22), fill="#c43d3d")
d.text((x, 160), "Dimas Aji Samudra", font=font(True, 68), fill=TEXT)
y = 260
body = font(False, 34)
for line in wrap(d, "I make what your customers see, and build what runs behind it.", body, max_w):
    d.text((x, y), line, font=body, fill=TEXT)
    y += 48
d.text((x, y + 16), "Video  ·  Design  ·  Web  ·  Automation", font=font(False, 26), fill=MUTED)

d.rectangle((x, 500, x + 96, 506), fill=PRIMARY)
d.text((x, 522), "dimas-aji-samudra.netlify.app", font=font(False, 26), fill=LINK)

im.save(OUT, quality=88, optimize=True, progressive=True)
print("wrote", OUT, OUT.stat().st_size // 1024, "KB")
