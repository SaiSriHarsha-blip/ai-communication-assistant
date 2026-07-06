/**
 * Why: App-wide client providers belong in one boundary to protect server components.
 * What: Combines theme management and toast infrastructure for the product shell.
 * How: Root layout renders this once around all routes.
 */
"use client";

import { Toaster } from "sonner";

import { ThemeProvider } from "@/components/providers/theme-provider";

type AppProvidersProps = {
  children: React.ReactNode;
};

export function AppProviders({ children }: AppProvidersProps) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="dark"
      disableTransitionOnChange
      enableSystem
    >
      {children}
      <Toaster richColors closeButton position="top-right" />
    </ThemeProvider>
  );
}
