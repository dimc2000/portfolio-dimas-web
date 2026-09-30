// Data yang dipakai di banyak halaman. Ubah di sini, semua halaman ikut berubah.

export const site = {
  name: "Dimas Aji Samudra",
  email: "aji26866a@gmail.com",
  /** Nomor WhatsApp format internasional tanpa + dan spasi, contoh "6281234567890". Kosong = tombol disembunyikan. */
  whatsapp: "6285778133142",
  year: 2026,
};

/**
 * Baris angka di hero beranda. Hanya angka yang bisa dibuktikan; jangan mengarang.
 * Label satu-dua kata saja: pembacanya orang sibuk.
 * Sumber saat ini (dari isi portofolio sendiri):
 * - 4+ tahun: kata Dimas sendiri (30-09-2026: "lebih dari 4 tahun di dunia ini")
 * - 5 industri: blockchain (Pirichain), kosmetik (HEYXI), kopi (Mountain Bay Mayroom),
 *   suplai industri (Ragam Rubber), CSR/ESG (Climate Data Platform)
 * - 4 layanan: src/data/services.ts
 * Ganti dengan angka yang lebih kuat bila sudah ada datanya (jumlah proyek, views, hasil penjualan).
 */
export const stats = [
  { value: "4+", label: "Years of experience" },
  { value: "5", label: "Industries" },
  { value: "4", label: "Services" },
] as const;

export const nav = [
  { label: "Works", href: "/works/" },
  { label: "Services", href: "/services/" },
  { label: "Contact", href: "/contact/" },
] as const;

export const social = {
  linkedin: {
    label: "LinkedIn",
    handle: "Dimas Aji Samudra",
    href: "https://www.linkedin.com/in/m-dimas-aji-samudra-1143a223b/",
    show: true,
  },
  whatsapp: { label: "WhatsApp", handle: "Chat on WhatsApp", href: `https://wa.me/${site.whatsapp}`, show: site.whatsapp !== "" },
  // Disembunyikan sampai ada repo yang layak dilihat klien (misalnya workflow Content Engine). Ubah ke true untuk menampilkan.
  github: { label: "GitHub", handle: "dimc2000", href: "https://github.com/dimc2000", show: false },
  behance: { label: "Behance", handle: "dimc4", href: "https://www.behance.net/dimc4", show: true },
} as const;

export type SocialKey = keyof typeof social;

export const whatsappLink = (text = "Hi Dimas, I'd like to talk about a project.") =>
  site.whatsapp ? `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(text)}` : null;
