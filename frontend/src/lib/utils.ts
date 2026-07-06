/**
 * Why: Shared presentation helpers keep component files small and consistent.
 * What: Exposes `cn`, a typed class-name merger used by shadcn-style UI primitives.
 * How: Components call this when composing Tailwind classes with variants.
 */
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
