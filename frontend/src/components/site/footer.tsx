/**
 * Why: The landing page needs a polished close with useful project links.
 * What: Renders brand copy, GitHub access, and section anchors.
 * How: The home route places it after the main content.
 */
import { GitBranch, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { siteConfig } from "@/constants/site";

export function Footer() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-8 sm:px-6 md:flex-row md:items-center md:justify-between lg:px-8">
        <div className="flex items-center gap-3">
          <span className="flex size-9 items-center justify-center rounded-lg border border-white/10 bg-white/10">
            <Sparkles aria-hidden="true" className="size-4 text-primary" />
          </span>
          <div>
            <p className="text-sm font-semibold text-foreground">
              {siteConfig.name}
            </p>
            <p className="text-sm text-muted-foreground">
              Clearer messages, generated with care.
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {siteConfig.navItems.map((item) => (
            <Button key={item.href} variant="ghost" size="sm" asChild>
              <a href={item.href}>{item.label}</a>
            </Button>
          ))}
          <Button variant="outline" size="sm" asChild>
            <a href={siteConfig.githubUrl} target="_blank" rel="noreferrer">
              <GitBranch aria-hidden="true" />
              GitHub
            </a>
          </Button>
        </div>
      </div>
    </footer>
  );
}
