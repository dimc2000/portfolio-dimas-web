// Untuk orang yang sangat sibuk (paham dalam 20 detik): judul, satu kalimat pendek, beberapa kata kunci.
// Tanpa jargon, tanpa harga, tanpa contoh yang terlalu spesifik. Seluruh kartu bisa diklik (href).
export interface Service {
  title: string;
  /** Satu kalimat pendek: hasil yang didapat klien */
  line: string;
  tags: string[];
  /** Halaman contoh karya */
  href: string;
}

export const services: Service[] = [
  {
    title: "Marketing & Branding",
    line: "Get noticed and chosen.",
    tags: ["Video", "Design", "Presentations"],
    href: "/design/",
  },
  {
    title: "Websites",
    line: "Get found on Google.",
    tags: ["Company sites", "Landing pages"],
    href: "/websites/", // sementara halaman kosong, karya lama sedang dicari
  },
  {
    title: "Automation",
    line: "Stop repeating the same tasks.",
    tags: ["Follow-ups", "Reports", "AI drafts"],
    href: "/projects/lead-follow-up-automation/",
  },
  {
    title: "Dashboards & Apps",
    line: "All your numbers on one screen.",
    tags: ["Sales", "Stock", "Team tools"],
    href: "/projects/climate-data-platform/",
  },
];
