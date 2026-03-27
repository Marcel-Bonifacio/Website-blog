/**
 * posts.js — All Blog Posts
 *
 * To add a new post:
 *  1. Add an entry to the POSTS array below.
 *  2. External post  (Kumparan / Medium): set external: true  and  url to the full link.
 *  3. Own post       (hosted here)      : set external: false and  url to "posts/your-file.html",
 *     then place the HTML file in the posts/ folder (run: python new-post.py _drafts/your-file.html).
 *  4. Set featured: true on the ONE post you want as the hero on the homepage.
 *
 * Auto-sync: run  python sync.py  (or let GitHub Actions do it daily)
 *            to pull new articles from Medium and Kumparan automatically.
 */

var POSTS = [
  {
    id: "tarif-listrik-naik",
    title: "Tarif Listrik Naik, Apakah Salah Energi Baru Terbarukan?",
    dateISO: "2022-02-27",
    dateDisplay: "February 27, 2022",
    platform: "Kumparan",
    excerpt: "Electricity tariffs are rising in Indonesia — and renewable energy is getting the blame. But a closer look at IRENA data tells a different story: solar and wind are now cheaper than fossil fuels. So who, or what, is really driving up the cost of power?",
    url: "https://kumparan.com/marcel-bonifacio-tirta-wijata/tarif-listrik-naik-apakah-salah-energi-baru-terbarukan-1xaUHV1Me9z",
    external: true,
    tags: ["Renewable Energy", "Indonesia", "Energy Policy"],
    featured: false
  },

  {
    id: "why-indonesia-283-million-people-arent-making-it-rich",
    title: "Why Indonesia\u2019s 283 Million People Aren\u2019t Making It Rich",
    dateISO: "2025-07-22",
    dateDisplay: "July 22, 2025",
    platform: "Medium",
    excerpt: "With 283 million people and 68% in their prime working years, Indonesia should be an economic powerhouse. Yet the demographic dividend is slipping away — and if the country doesn't act before the mid-2030s population ages, the window may close for good.",
    url: "https://medium.com/@marcelbonifaciotirtawijata/why-indonesias-283-million-people-aren-t-making-it-rich-17d7c7162635",
    external: true,
    tags: ["Indonesia", "Economy", "Demographics"],
    featured: false
  },

  {
    id: "economic-impact-carbon-tax-indonesia",
    title: "The Economic Impact of Indonesia\u2019s Carbon Tax on Middle and Lower-Income Population",
    dateISO: "2024-10-03",
    dateDisplay: "October 3, 2024",
    platform: "Medium",
    excerpt: "Indonesia's carbon tax is designed to fight climate change — but at IDR 30 per kg of CO\u2082e, it risks hitting the poorest households hardest. With coal still powering 67.2% of the grid, the transition cost falls unevenly. Can the policy be redesigned to protect the vulnerable?",
    url: "https://medium.com/@marcelbonifaciotirtawijata/the-economic-impact-of-indonesias-carbon-tax-on-middle-and-lower-income-population-a3bcf4578eda",
    external: true,
    tags: ["Climate Policy", "Indonesia", "Carbon Tax"],
    featured: false
  },

  {
    id: "nickel-mining-dirty-secret",
    title: "Nickel Mining\u2019s Dirty Secret Wrecking Indonesia\u2019s Environment",
    dateISO: "2024-09-07",
    dateDisplay: "September 7, 2024",
    platform: "Medium",
    excerpt: "Indonesia is the world's top nickel producer — fuelling the EV boom with 1.8 million metric tons in 2023. But behind the green energy narrative lies a trail of deforestation, toxic contamination, and displaced communities. The governance failures are severe, and largely invisible.",
    url: "https://medium.com/@marcelbonifaciotirtawijata/nickel-minings-dirty-secret-wrecking-indonesia-s-environment-99709d748db4",
    external: true,
    tags: ["Environment", "Indonesia", "Mining"],
    featured: true
  },

  {
    id: "asean-renewable-energy-roadmap-transportation",
    title: "Shaping the Future of Transportation: The Impact of ASEAN\u2019s Long-Term Renewable Energy Roadmap",
    dateISO: "2024-08-27",
    dateDisplay: "August 27, 2024",
    platform: "Medium",
    excerpt: "ASEAN's transport sector runs on oil — 91% of its energy comes from petroleum. The region's long-term renewable roadmap aims to flip that, targeting 67% renewable energy by 2050. What will it take to electrify the way Southeast Asia moves?",
    url: "https://medium.com/@marcelbonifaciotirtawijata/shaping-the-future-of-transportation-the-impact-of-aseans-long-term-renewable-energy-roadmap-e2c595a7f511",
    external: true,
    tags: ["ASEAN", "Renewable Energy", "Transportation"],
    featured: false
  },

  {
    id: "asean-renewable-energy-long-term-roadmap",
    title: "The ASEAN Renewable Energy Long-Term Roadmap: Why It Matters and What Are the Challenges",
    dateISO: "2024-08-18",
    dateDisplay: "August 18, 2024",
    platform: "Medium",
    excerpt: "ASEAN is the world's fifth-largest economy — yet one of its most fossil-fuel dependent. A new long-term roadmap targets 23% renewable energy in primary supply by 2025 and 35% in power generation. The ambition is real. So are the obstacles.",
    url: "https://medium.com/@marcelbonifaciotirtawijata/the-asean-renewable-energy-long-term-roadmap-why-it-matters-and-what-are-the-challenges-4da9b103e0bb",
    external: true,
    tags: ["ASEAN", "Renewable Energy", "Policy"],
    featured: false
  }
];
