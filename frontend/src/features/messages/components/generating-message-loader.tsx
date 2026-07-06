/**
 * Why: Message generation needs a calm loading state that feels premium, not noisy.
 * What: Renders a reusable animated status strip for the eventual submit flow.
 * How: The hero previews it now; Phase 2 can show it while the message hook is pending.
 */
"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

import { cn } from "@/lib/utils";

type GeneratingMessageLoaderProps = {
  className?: string;
};

const bars = [0.4, 0.7, 1, 0.65] as const;

export function GeneratingMessageLoader({
  className,
}: GeneratingMessageLoaderProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      className={cn(
        "flex items-center justify-between rounded-xl border border-white/10 bg-background/50 px-4 py-3 text-sm text-muted-foreground",
        className,
      )}
    >
      <div className="flex min-w-0 items-center gap-3">
        <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <Sparkles aria-hidden="true" className="size-4" />
        </span>
        <span className="truncate">Generating polished variants</span>
      </div>
      <div className="flex h-5 items-end gap-1.5" aria-hidden="true">
        {bars.map((scale, index) => (
          <motion.span
            key={scale}
            className="w-1.5 rounded-full bg-primary/80"
            initial={{ height: 6 }}
            animate={{ height: [6, 18 * scale, 6] }}
            transition={{
              duration: 1.2,
              ease: "easeInOut",
              repeat: Infinity,
              delay: index * 0.12,
            }}
          />
        ))}
      </div>
    </div>
  );
}
