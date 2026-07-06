/**
 * Why: Navigation anchors the SaaS shell and keeps global actions discoverable.
 * What: Renders the brand, section links, theme toggle, and primary CTA.
 * How: The home route imports this server component above landing sections.
 */
import { GitBranch, Sparkles } from "lucide-react";

import { ThemeToggle } from "@/components/theme/theme-toggle";
import { Button } from "@/components/ui/button";
import { siteConfig } from "@/constants/site";

export function Navbar() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-background/70 backdrop-blur-xl">
      <nav
        aria-label="Primary navigation"
        className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8"
      >
        <a href="#" className="flex items-center gap-3" aria-label="Home">
          <span className="flex size-9 items-center justify-center rounded-lg border border-white/10 bg-white/10 shadow-lg shadow-black/10">
            <Sparkles aria-hidden="true" className="size-4 text-primary" />
          </span>
          <span className="text-sm font-semibold tracking-wide text-foreground">
            {siteConfig.name}
          </span>
        </a>

        <div className="hidden items-center gap-1 md:flex">
          {siteConfig.navItems.map((item) => (
            <Button
              key={item.href}
              variant="ghost"
              size="sm"
              asChild
              className="text-muted-foreground hover:text-foreground"
            >
              <a href={item.href}>{item.label}</a>
            </Button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Button
            asChild
            size="icon"
            variant="outline"
            className="hidden border-white/10 bg-white/5 text-muted-foreground backdrop-blur hover:bg-white/10 hover:text-foreground sm:inline-flex"
          >
            <a
              href={siteConfig.githubUrl}
              target="_blank"
              rel="noreferrer"
              aria-label="Open GitHub repository"
            >
              <GitBranch aria-hidden="true" />
            </a>
          </Button>
          <Button asChild size="sm" className="hidden sm:inline-flex">
            <a href="#product">Start building</a>
          </Button>
        </div>
      </nav>
    </header>
  );
}
