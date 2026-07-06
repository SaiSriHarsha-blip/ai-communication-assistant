/**
 * Why: Theme state must run on the client while the rest of the shell stays server-rendered.
 * What: Configures next-themes for class-based light and dark mode switching.
 * How: Root layout wraps the app with this provider; toggles update its state.
 */
"use client";

import { ThemeProvider as NextThemesProvider } from "next-themes";
import type { ThemeProviderProps } from "next-themes";

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
