// Studi kasus Design & Content: dipakai di /design/, Works, dan Home.
// Detail tiap studi kasus ada di src/pages/design/<slug>.astro
// Media diolah lewat source-files/scripts/prepare-design-media.py
// Studi kasus yang dicopot diarsipkan lokal di source-files/design/<proyek>/removed-from-site/ (tidak masuk repo)
import type { ImageMetadata } from "astro";

import piriPosts from "../assets/images/design/pirichain/posts-mockup.webp";
import heyxiGarden from "../assets/images/design/heyxi/ad-eyeshadow-pen-garden-poster.jpg";
import heyxiCream from "../assets/images/design/heyxi/ad-dragon-blood-cream-poster.jpg";
import heyxiPerfume from "../assets/images/design/heyxi/ad-perfume-poster.jpg";
import ragamPostPtfe from "../assets/images/design/ragam-rubber/post-ferrule-ptfe.jpg";
import ragamPostDiaphragm from "../assets/images/design/ragam-rubber/post-diaphragm.jpg";
import ragamPostValve from "../assets/images/design/ragam-rubber/post-butterfly-valve.jpg";
import mbmLineup from "../assets/images/design/mountain-bay-mayroom/pouch-lineup.jpg";

export type DesignCase = {
  slug: string;
  name: string;
  /** Jenis klien, tanpa hal yang tidak boleh dipublikasikan */
  client: string;
  tags: string[];
  year: number;
  /** Judul kartu: masalah / kebutuhan klien */
  headline: string;
  summary: string;
  /** 1 gambar = cover biasa, 3 gambar = tiga panel berdampingan */
  cover: ImageMetadata[];
};

export const designCases: DesignCase[] = [
  {
    slug: "pirichain",
    name: "Pirichain",
    client: "Blockchain data platform",
    tags: ["Sales deck", "Explainer video", "Social posts"],
    year: 2023,
    headline: "Making a blockchain platform easy to explain to companies",
    summary: "An 11-slide sales deck with custom illustrations, a two-minute explainer video built from the same story, and announcement posts.",
    cover: [piriPosts],
  },
  {
    slug: "heyxi",
    name: "HEYXI",
    client: "Cosmetics brand",
    tags: ["Short-form video", "TikTok ads"],
    year: 2025,
    headline: "Five product ads that show the product in the first seconds",
    summary: "Script, shoot, talent direction and edit for vertical ads across three products: an eyeshadow pen, a face cream and a perfume.",
    cover: [heyxiGarden, heyxiCream, heyxiPerfume],
  },
  {
    slug: "ragam-rubber",
    name: "Ragam Rubber",
    client: "Industrial seal supplier",
    tags: ["Brand identity", "Product content"],
    year: 2025,
    headline: "From phone photos on a green cloth to a product catalog",
    summary: "Logo, product post system, catalog, poster and marketplace banner for a supplier of industrial seals and gaskets.",
    cover: [ragamPostPtfe, ragamPostDiaphragm, ragamPostValve],
  },
  {
    slug: "mountain-bay-mayroom",
    name: "Mountain Bay Mayroom",
    client: "Coffee brand",
    tags: ["Brand identity", "Packaging"],
    year: 2024,
    headline: "One label system for three coffee blends",
    summary: "Logo, label system and retail pouches for a coffee brand selling Java beans.",
    cover: [mbmLineup],
  },
];

export const getCase = (slug: string) => {
  const i = designCases.findIndex((c) => c.slug === slug);
  return { current: designCases[i], next: designCases[(i + 1) % designCases.length] };
};
