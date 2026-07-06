/**
 * Why: Brand and navigation copy should be centralized instead of duplicated.
 * What: Defines stable metadata for the recruiter-focused marketing shell.
 * How: Layout, navbar, hero, and footer import these values for consistent product language.
 */
export const siteConfig = {
  name: "MessagePilot",
  description:
    "An AI-powered message assistant for clearer, faster communication across everyday platforms.",
  githubUrl: "https://github.com/SaiSriHarsha-blip/ai-communication-assistant",
  navItems: [
    { label: "Product", href: "#product" },
    { label: "Platforms", href: "#platforms" },
    { label: "Reliability", href: "#architecture" },
    { label: "Why MessagePilot", href: "#recruiters" },
  ],
} as const;
