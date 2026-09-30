"""
Siapkan media untuk halaman Design & Content.

1. collect : salin file terpilih dari arsip desain ke source-files/design/<proyek>/originals/
             (lewati kalau sudah ada). Arsip: E:\\M.DIMAS AJI.S\\DATA PROJEK DESAIEG
2. build   : olah originals → src/assets/
             - gambar : diperkecil (sisi terpanjang maks. 2400 px), metadata dibuang
             - video  : 720p H.264 + AAC, "faststart" agar cepat diputar, + gambar poster

Jalankan dari folder proyek:
    python source-files/scripts/prepare-design-media.py          # collect + build
    python source-files/scripts/prepare-design-media.py build    # build saja
Butuh Pillow dan ffmpeg (bawaan Shutter Encoder, atau set env FFMPEG_DIR).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = Path(r"E:\M.DIMAS AJI.S\DATA PROJEK DESAIEG")
SAMPLES = ROOT.parent / "sempel Businesses needed videos and visuals to promote their products and services"
SRC = ROOT / "source-files" / "design"
OUT_IMG = ROOT / "src" / "assets" / "images" / "design"
OUT_VID = ROOT / "src" / "assets" / "video" / "design"
FF = Path(os.environ.get("FFMPEG_DIR", r"C:\Program Files\Shutter Encoder\Library"))

A = ARCHIVE
RR = A / "RAGAM RUBBER"
PIRI = A / "piri x boba/MR.Don"
CAT = RR / "Katalok produk"

# proyek → {nama hasil: sumber}
COLLECT = {
    "heyxi": {
        "ad-eyeshadow-pen-studio.mp4": A / "HEYXI/PORTO/1186095205.mp4",
        "ad-eyeshadow-pen-garden.mp4": A / "HEYXI/PORTO/1557020207.mp4",
        "ad-eyeshadow-pen-outdoor.mp4": A / "HEYXI/PORTO/1558675233.mp4",
        "ad-dragon-blood-cream.mp4": A / "HEYXI/PORTO/528471601.mp4",
        "ad-perfume.mp4": A / "HEYXI/PORTO/644383969.mp4",
        "bts-filming.jpg": A / "HEYXI/PORTO/6327862114647131774.jpg",
        "bts-setup.jpg": A / "HEYXI/PORTO/6327862114647131794 (1).jpg",
        "bts-team.jpg": A / "HEYXI/PORTO/6327862114647131779.jpg",
        "logo.png": A / "HEYXI/images (1).png",
    },
    "ragam-rubber": {
        "logo-banner.png": RR / "About the company/Untitled-1-01.png",
        "logo-on-black.png": RR / "logo/logo hitam-01.png",
        "poster-custom-parts.png": RR / "About the company/poster baru tokpet-02.png",
        "contact-card.png": RR / "About the company/4.png",
        "marketplace-store.png": RR / "About the company/laptop tokpet.png",
        "post-diaphragm.png": CAT / "Diaphragma PTFE,EPDM/Diaphragma PTFE,EPDM 01/8.png",
        "post-ferrule-ptfe.png": CAT / "Ferrul PTFE/1/7.png",
        "post-gasket-viton.png": CAT / "Gasket Seal PHE Port Ring Viton Q030E/8.png",
        "post-ferrule-silicone.png": CAT / "Seal Ferrule Silicone/Seal Ferrule Silicone 1''/5.png",
        "post-butterfly-valve.png": CAT / "Seal butterfly valve Sanitary/Seal butterfly valve Sanitary 1mm/7.png",
        "post-ferrule-epdm.png": CAT / "Seal ferrule Silicone EPDM/Seal ferrule  EPDM 4''/21.png",
        "raw-ferrule.jpg": RR / "Raw file/IMG-20250410-WA0017.jpg",
    },
    "mountain-bay-mayroom": {
        "logo-dark.png": A / "MM.cofe/ggaha-01.png",
        "logo-light.png": A / "MM.cofe/gggg-01.png",
        "label-special-blend.png": A / "MM.cofe/12.png",
        "label-special-bisma.png": A / "MM.cofe/6.png",
        "label-natural-arabica.png": A / "MM.cofe/9.png",
        "pouch-lineup.png": A / "MM.cofe/produk/IMG_20240813_153735_635.png",
        "pouch-special-blend.png": A / "MM.cofe/produk/IMG_20240813_153636_958.png",
        "pouch-special-bisma.png": A / "MM.cofe/produk/IMG_20240813_153637_408.png",
        "pouch-natural-arabica.png": A / "MM.cofe/produk/IMG_20240813_153637_926.png",
    },
    # Studi kasus yang dicopot dari situs diarsipkan lokal di source-files/design/<proyek>/removed-from-site/
    # Pirichain: hanya deck, video explainer dan post pengumuman.
    "pirichain": {
        "explainer.mp4": SAMPLES / "explainer pirichain.mp4",
        **{f"deck-{n:02d}.png": PIRI / f"proposal/Pirichain Commercial Slide/Pirichain Commercial Slide-{n:02d}.png"
           for n in (1, 2, 3, 4, 5, 7, 8, 9, 10)},
        "posts-mockup.png": PIRI.parent / "MM Ermi (3).png",
        "post-airdrop-started.jpg": PIRI / "proposal/5855170606893482110.jpg",
        "post-airdrop-continues.jpg": PIRI / "proposal/6012355079803355349.jpg",
        "post-stake-pool.jpg": PIRI / "proposal/6260016801194818545.jpg",
        "post-docrypt.jpg": PIRI / "proposal/5945079141575540240.jpg",
    },
}

# Detik untuk gambar poster video (frame yang memperlihatkan produk)
POSTER_AT = {
    "ad-eyeshadow-pen-studio.mp4": 5.0,
    "ad-eyeshadow-pen-garden.mp4": 7.0,
    "ad-eyeshadow-pen-outdoor.mp4": 6.0,
    "ad-dragon-blood-cream.mp4": 9.0,
    "ad-perfume.mp4": 8.5,
    "explainer.mp4": 50.0,
}

# Frame diam dari video (untuk menjelaskan struktur video di halaman studi kasus)
# proyek → {video: [(detik, nama hasil), ...]}
FRAMES = {
    "pirichain": {
        "explainer.mp4": [
            (7.0, "scene-1-intro.jpg"),
            (17.0, "scene-2-context.jpg"),
            (27.0, "scene-3-problem.jpg"),
            (42.0, "scene-4-answer.jpg"),
            (52.0, "scene-5-ecosystem.jpg"),
            (90.0, "scene-6-apis.jpg"),
            (101.0, "scene-7-roadmap.jpg"),
        ],
    },
}

MAX_SIDE = 2400


def collect():
    for project, files in COLLECT.items():
        dest = SRC / project / "originals"
        dest.mkdir(parents=True, exist_ok=True)
        for name, source in files.items():
            target = dest / name
            if target.exists():
                continue
            if not source.exists():
                print("  MISSING", source)
                continue
            shutil.copy2(source, target)
            print("  copied", project, name)


def has_transparency(im: Image.Image) -> bool:
    if im.mode == "P" and "transparency" in im.info:
        im = im.convert("RGBA")
    return im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 255


def build_image(src: Path, out_dir: Path) -> Path:
    """WebP kalau ada bagian transparan (label, logo), selain itu JPG. Keduanya jauh lebih kecil dari PNG."""
    im = ImageOps.exif_transpose(Image.open(src))
    alpha = has_transparency(im)
    if alpha:
        im = im.convert("RGBA")
        im = im.crop(im.getchannel("A").getbbox())  # buang margin yang sepenuhnya transparan
        alpha = has_transparency(im)
    im = im.convert("RGBA" if alpha else "RGB")
    im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / (src.stem + (".webp" if alpha else ".jpg"))
    if alpha:
        im.save(out, quality=92, method=6)
    else:
        im.save(out, quality=88, optimize=True, progressive=True)  # tanpa exif → metadata terbuang
    return out


def build_video(src: Path, out: Path, poster: Path, poster_at: float):
    out.parent.mkdir(parents=True, exist_ok=True)
    poster.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = str(FF / "ffmpeg.exe")
    scale = "scale='if(gt(iw,ih),1280,720)':-2"  # 720p, landscape maupun portrait
    subprocess.run([ffmpeg, "-v", "error", "-y", "-i", str(src), "-vf", scale, "-c:v", "libx264", "-preset", "slow",
                    "-crf", "27", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    "-c:a", "aac", "-b:a", "96k", "-map_metadata", "-1", str(out)], check=True)
    subprocess.run([ffmpeg, "-v", "error", "-y", "-ss", str(poster_at), "-i", str(out), "-frames:v", "1",
                    "-q:v", "3", str(poster)], check=True)


def build():
    for project in COLLECT:
        for src in sorted((SRC / project / "originals").glob("*")):
            if src.suffix.lower() == ".mp4":
                out = OUT_VID / project / src.name
                poster = OUT_IMG / project / (src.stem + "-poster.jpg")
                if out.exists() and poster.exists() and out.stat().st_mtime > src.stat().st_mtime:
                    continue  # sudah dikompres
                build_video(src, out, poster, POSTER_AT.get(src.name, 1.0))
                print(f"  video {project}/{src.name}  {out.stat().st_size / 1e6:.1f} MB")
            else:
                out = build_image(src, OUT_IMG / project)
                print(f"  image {project}/{out.name}  {out.stat().st_size / 1e6:.2f} MB")
    build_frames()


def build_frames():
    ffmpeg = str(FF / "ffmpeg.exe")
    for project, videos in FRAMES.items():
        for video, frames in videos.items():
            src = SRC / project / "originals" / video
            for at, name in frames:
                out = OUT_IMG / project / name
                out.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run([ffmpeg, "-v", "error", "-y", "-ss", str(at), "-i", str(src), "-frames:v", "1",
                                "-q:v", "3", str(out)], check=True)
            print(f"  frames {project}/{video}  {len(frames)} stills")


if __name__ == "__main__":
    if "build" not in sys.argv:
        collect()
    build()
