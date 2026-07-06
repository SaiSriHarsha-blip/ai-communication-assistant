/**
 * Why: Users need an accessible way to switch between dark and light themes.
 * What: Renders an icon-only shadcn-style button connected to next-themes.
 * How: The navbar imports it; theme changes flow through AppProviders.
 */
"use client";

import { Laptop, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";

const themeIcons = {
  dark: Moon,
  light: Sun,
  system: Laptop,
};

export function ThemeToggle() {
  const { setTheme, theme } = useTheme();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const activeTheme = isMounted ? theme ?? "dark" : "dark";
  const Icon = themeIcons[activeTheme as keyof typeof themeIcons] ?? Moon;
  const nextTheme = activeTheme === "dark" ? "light" : "dark";

  return (
    <Button
      type="button"
      aria-label={`Switch to ${nextTheme} theme`}
      variant="outline"
      size="icon"
      onClick={() => setTheme(nextTheme)}
      className="border-white/10 bg-white/5 text-muted-foreground backdrop-blur hover:bg-white/10 hover:text-foreground"
    >
      <Icon aria-hidden="true" />
    </Button>
  );
}
