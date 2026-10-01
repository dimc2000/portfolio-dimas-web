# Panduan kerja — Portfolio Dimas Aji Samudra

> Catatan kerja internal (Bahasa Indonesia). Ringkasan proyek dalam bahasa Inggris ada di [README](../README.md).

Situs portfolio berbasis [Astro](https://astro.build), diturunkan dari Figma
"Portfolio UI - Web & Mobile" → halaman **Portfolio v2**
(font Heebo, warna coral `#ff6464`, frame desktop 1152px dan mobile 375px).

## Cara menjalankan

Butuh **Node.js 22.12 atau lebih baru**.

```bash
npm install        # sekali saja
npm run dev        # buka http://localhost:4321 — otomatis refresh saat file diubah
npm run build      # hasil siap hosting di folder dist/
npm run preview    # cek hasil build di http://localhost:4321
npm run check      # cek error TypeScript/Astro
```

> `dist/` tidak bisa dibuka dengan double-click (file://). Pakai `npm run preview`.

## Terbit (deploy)

Situs di-hosting di **Cloudflare Pages** (gratis) dan tersambung ke repo GitHub
`dimc2000/portfolio-dimas-web`. Setiap `git push` ke branch `main` otomatis di-build
(`npm run build`, folder `dist`) dan terbit di https://dimas-aji-samudra.pages.dev.
Versi Node diatur di `.node-version`. Alamat situs diatur di `astro.config.mjs` (`site`).

Alamat lama `dimas-aji-samudra.netlify.app` dialihkan ke alamat baru mulai 29 Oktober 2026, saat kuota Netlify reset
(kuota deploy Netlify gratis hanya 20 kali per bulan, jadi Netlify tidak dipakai lagi untuk terbit).

## Struktur folder

```
portfolio-dimas-web/
├─ astro.config.mjs          Konfigurasi (font Heebo self-hosted, domain situs)
├─ public/                   Di-copy apa adanya ke dist/
│  ├─ favicon.svg
│  ├─ og.jpg                 Gambar preview link default (source-files/scripts/make-og-image.py)
│  ├─ theme/                 Latar bintang tema gelap (source-files/scripts/make-star-background.py)
│  ├─ _redirects             Redirect alamat lama v1 (works.html → /works/, dst.) — Cloudflare Pages / Netlify
│  └─ _headers               Header keamanan + cache untuk file /_astro/ — Cloudflare Pages / Netlify
├─ src/
│  ├─ pages/                 Satu file = satu halaman (URL mengikuti nama file)
│  │  ├─ index.astro         /
│  │  ├─ works.astro         /works/
│  │  ├─ services.astro      /services/
│  │  ├─ contact.astro       /contact/
│  │  ├─ 404.astro
│  │  ├─ projects/           Studi kasus sistem (otomasi, dashboard)
│  │  │  ├─ climate-data-platform.astro
│  │  │  └─ content-workflow-automation.astro
│  │  └─ design/             Studi kasus desain & konten
│  │     ├─ index.astro      /design/  (daftar studi kasus + explainer)
│  │     ├─ pirichain.astro
│  │     ├─ heyxi.astro
│  │     ├─ ragam-rubber.astro
│  │     └─ mountain-bay-mayroom.astro
│  ├─ layouts/
│  │  ├─ BaseLayout.astro    <head>, SEO, header, footer — dipakai semua halaman
│  │  └─ ProjectLayout.astro Kerangka halaman detail proyek
│  ├─ components/
│  │  ├─ SiteHeader.astro / SiteFooter.astro / SocialIcon.astro
│  │  ├─ WorkItem.astro      Kartu karya di Home & Works
│  │  ├─ Row.astro           Baris Overview / Problem / Solution ...
│  │  ├─ Exhibit.astro       Bukti dengan tanda pena merah A, B, C + legenda
│  │  ├─ ZoomImage.astro     Gambar yang bisa dibuka ukuran penuh
│  │  ├─ Lightbox.astro      Jendela gambar ukuran penuh
│  │  ├─ WorkflowDiagram.astro  Diagram alur Content Workflow
│  │  ├─ DesignCard.astro    Kartu studi kasus desain
│  │  ├─ VideoReel.astro     Deretan video vertikal 9:16 (klik untuk putar)
│  │  └─ Showcase.astro      Satu bagian galeri di studi kasus desain
│  ├─ data/                  Teks yang dipakai di banyak halaman
│  │  ├─ site.ts             Nama, email, menu, link sosial
│  │  ├─ projects.ts         Daftar karya sistem (Home & Works)
│  │  ├─ design.ts           Daftar studi kasus desain (Design, Works, Home)
│  │  └─ services.ts         Daftar layanan (Home & Services)
│  ├─ styles/
│  │  ├─ tokens.css          Warna, font, lebar — ubah di sini
│  │  ├─ global.css          Gaya dasar & komponen umum
│  │  └─ project.css         Gaya halaman detail proyek
│  └─ assets/
│     ├─ images/             Gambar yang dioptimasi otomatis (WebP, beberapa ukuran)
│     │  ├─ profile-photo.webp        ← dibuat oleh make-profile-photo.py
│     │  ├─ projects/climate-data-platform/   ← sudah disensor, aman dipublish
│     │  └─ design/<proyek>/                  ← hasil prepare-design-media.py
│     └─ video/design/<proyek>/               ← video 720p siap web
└─ source-files/             TIDAK ikut dipublish
   ├─ climate-data-platform/originals/     Bukti asli (belum disensor) — di-.gitignore
   ├─ design/<proyek>/originals/           Salinan file asli dari arsip desain — di-.gitignore
   ├─ profile/originals/                   Foto profil asli — di-.gitignore
   └─ scripts/
      ├─ prepare-evidence.py               Sensor screenshot + potong foto (Climate)
      ├─ prepare-design-media.py           Kompres video + perkecil gambar (Design)
      └─ make-profile-photo.py             Foto profil: crop + koreksi ringan (tanpa AI)
```

## Menambah / mengganti bukti Climate Data Platform

1. Taruh file asli di `source-files/climate-data-platform/originals/`.
2. Atur kotak sensor & potongan di `source-files/scripts/prepare-evidence.py`.
   Cek dulu dengan `python source-files/scripts/prepare-evidence.py --preview`
   (membuat `redaction-preview.png` berisi setiap kotak bergaris merah).
3. Jalankan `npm run evidence` (butuh Python + Pillow: `pip install pillow`).
4. Posisi tanda A, B, C ditulis di `src/pages/projects/climate-data-platform.astro`
   dalam **piksel gambar asli** (`x`, `y` = titik tengah tanda).

Yang disensor: logo & nama grup klien, nama & jabatan staf, nama platform,
nama file yang memuat nama klien, dan koordinat geotag. Metadata foto (EXIF/GPS) dibuang.

## Menambah / mengganti karya desain

1. Daftarkan file di `COLLECT` pada `source-files/scripts/prepare-design-media.py`
   (sumber default: arsip `E:\M.DIMAS AJI.S\DATA PROJEK DESAIEG`).
2. Jalankan `npm run design-media`. Video jadi MP4 720p (±2–5 MB) + gambar poster,
   gambar jadi JPG (atau WebP bila transparan) maks. 2400 px, metadata dibuang.
3. `import` hasilnya di halaman `src/pages/design/...` dan, bila perlu, di `src/data/design.ts`.

## Menambah proyek baru

1. Tambah entri di `src/data/projects.ts` (muncul di Home & Works).
2. Buat `src/pages/projects/nama-proyek.astro` memakai `ProjectLayout` + `Row`
   (contoh paling sederhana: `content-workflow-automation.astro`).
3. Gambar taruh di `src/assets/images/projects/nama-proyek/` lalu `import` di halaman.

## Setelah punya domain

Isi `site` di `astro.config.mjs` (misalnya `site: "https://domain-anda.com"`) agar
canonical URL dan gambar preview link (og:image) memakai alamat lengkap.

## Catatan

- Form Contact memakai FormSubmit (gratis, tanpa server sendiri): pesan dikirim ke email Dimas.
  Pesan pertama dari alamat situs baru memicu email aktivasi dari FormSubmit, klik sekali.
  Kalau gagal terkirim, aplikasi email pengunjung terbuka dengan pesan yang sudah terisi.
- Di HP, menu ada di bawah layar (ikon Home, Works, Services, Contact, seperti Instagram); di laptop tetap di kanan atas.
  Keduanya di `src/components/SiteHeader.astro`.
- Tombol WhatsApp muncul otomatis setelah nomor diisi di `src/data/site.ts` (`whatsapp: "62..."`).
- Pirichain (deck, explainer, post) ada di /design/pirichain/.
- Warna teks abu-abu dan link sedikit digelapkan dari Figma (`#8695a4` → `#687684`,
  `#00a8cc` → `#007a99`) agar kontras teks lolos standar WCAG AA. Nilai Figma asli ada di komentar `tokens.css`.
