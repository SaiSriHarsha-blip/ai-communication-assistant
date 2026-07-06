/**
 * Why: The root layout owns document metadata, fonts, and global providers.
 * What: Sets up the dark-first app shell without placing feature UI in layout.
 * How: Routes render inside AppProviders so client concerns stay isolated.
 */
import type { Metadata } from "next";

import { AppProviders } from "@/components/providers/app-providers";
import { siteConfig } from "@/constants/site";

import "./globals.css";

export const metadata: Metadata = {
  title: `${siteConfig.name} | AI Message Generator`,
  description: siteConfig.description,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background font-sans text-foreground antialiased">
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
