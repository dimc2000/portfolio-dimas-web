// Daftar karya untuk Home & Works. Detail tiap proyek ada di src/pages/projects/.
import type { ImageMetadata } from "astro";
import climateThumb from "../assets/images/projects/climate-data-platform/thumb.png";
import heyxiPoster from "../assets/images/design/heyxi/ad-eyeshadow-pen-garden-poster.jpg";
import ragamPost from "../assets/images/design/ragam-rubber/post-ferrule-ptfe.jpg";
import piriDeck from "../assets/images/design/pirichain/deck-01.jpg";
import { designCases } from "./design";

export type Work = {
  name: string;
  tags: string[];
  problem: string;
  solution: string;
  /** Halaman detail. Kosong = kartu tidak bisa diklik. */
  href?: string;
  /** Gambar kartu. Kalau kosong, dipakai ilustrasi sesuai `visual`. */
  image?: ImageMetadata;
  /** Tiga gambar berdampingan (menggantikan `image`) */
  images?: ImageMetadata[];
  visual?: "workflow";
  /** Ajakan klik di bawah teks, untuk kartu yang berisi beberapa proyek */
  cta?: string;
};

export const works: Work[] = [
  {
    name: "Climate Data Platform",
    tags: ["Web platform", "Dashboards", "IoT"],
    problem: "Program data was scattered and hard for auditors to trace",
    solution:
      "Built one platform with CSR and ESG dashboards, an evidence module and an IoT field unit, so every reported number links back to its source.",
    href: "/projects/climate-data-platform/",
    image: climateThumb,
  },
  {
    name: "Content Workflow Automation",
    tags: ["Automation", "AI", "In progress"],
    problem: "Regular content took hours, and every claim needed checking",
    solution:
      "Designing an n8n and Claude API workflow that drafts content, flags risky claims and waits for human approval before publishing. In progress.",
    href: "/projects/content-workflow-automation/",
    visual: "workflow",
  },
];

// Semua karya desain dalam SATU kartu (Home & Works); klik → /design/ berisi semua proyeknya (src/data/design.ts)
export const designSummary: Work = {
  name: "Design & Content",
  tags: ["Sales decks", "Video", "Brand identity"],
  problem: "Businesses needed videos and visuals to promote their products and services",
  solution:
    "A sales deck and explainer video for a blockchain platform, short-form video ads for a cosmetics brand, plus brand identity and packaging.",
  href: "/design/",
  images: [piriDeck, heyxiPoster, ragamPost],
  cta: `See all ${designCases.length} projects`,
};
