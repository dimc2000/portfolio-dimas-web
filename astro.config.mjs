// @ts-check
import { defineConfig, fontProviders } from "astro/config";

// https://docs.astro.build/en/reference/configuration-reference/
export default defineConfig({
  // Domain final (canonical URL & og:url). Ganti kalau nanti memakai domain sendiri.
  site: "https://dimas-aji-samudra.netlify.app",

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
