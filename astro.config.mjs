// @ts-check
import { defineConfig, fontProviders } from "astro/config";
import sitemap from "@astrojs/sitemap";

// https://docs.astro.build/en/reference/configuration-reference/
export default defineConfig({
  // Domain final (canonical URL & og:url). Ganti kalau nanti memakai domain sendiri.
  site: "https://dimas-aji-samudra.netlify.app",

  // sitemap-index.xml untuk Google (lihat public/robots.txt). Halaman noindex tidak dimasukkan:
  // /websites/ masih kosong — hapus dari daftar ini saat noindex di websites.astro dicabut.
  integrations: [
    sitemap({ filter: (page) => !["/websites/", "/404"].some((path) => page.includes(path)) }),
  ],

  // Heebo di-download saat build dan di-hosting sendiri (tanpa request ke Google saat halaman dibuka)
  fonts: [
    {
      provider: fontProviders.google(),
      name: "Heebo",
      cssVariable: "--font-heebo",
      weights: [400, 500, 700],
      styles: ["normal"],
      subsets: ["latin"],
      fallbacks: ["system-ui", "sans-serif"],
    },
  ],
});
