/**
 * Why: The hero is the first recruiter-facing signal for the product.
 * What: Presents the product promise, stack credibility, and a live generation state.
 * How: The home route composes it first; future phases can wire CTAs to the generator form.
 */
"use client";

import { motion } from "framer-motion";
import { MessageSquareText, ServerCog, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { siteConfig } from "@/constants/site";
import { GenerateMessageProvider } from "@/features/messages/components/generate-message-form";
import { MessageInputForm } from "@/features/messages/components/message-input-form";
import { MessageMetadata } from "@/features/messages/components/message-metadata";
import { MessageVariants } from "@/features/messages/components/message-variants";

export function HeroSection() {
  return (
    <section className="relative min-h-screen overflow-hidden pt-16" id="product">
      <div
        aria-hidden="true"
        className="absolute inset-0 bg-[linear-gradient(to_right,color-mix(in_oklch,var(--border)_45%,transparent)_1px,transparent_1px),linear-gradient(to_bottom,color-mix(in_oklch,var(--border)_35%,transparent)_1px,transparent_1px)] bg-[size:72px_72px] opacity-35"
      />
      <div
        aria-hidden="true"
        className="absolute inset-x-0 top-0 h-80 bg-[linear-gradient(135deg,color-mix(in_oklch,var(--primary)_18%,transparent),transparent_55%),linear-gradient(225deg,color-mix(in_oklch,#34d399_12%,transparent),transparent_45%)] blur-3xl"
      />

      <GenerateMessageProvider>
        <div className="relative mx-auto flex min-h-[calc(100vh-4rem)] max-w-7xl flex-col justify-center px-4 py-16 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="max-w-3xl"
          >
            <Badge
              variant="outline"
              className="border-white/10 bg-white/5 backdrop-blur"
            >
              <ServerCog aria-hidden="true" />
              AI-powered message assistant
            </Badge>
            <h1 className="mt-8 max-w-4xl text-balance text-5xl font-semibold leading-tight text-foreground sm:text-6xl lg:text-7xl">
              Write clearer messages for every platform.
            </h1>
            <p className="mt-6 max-w-2xl text-pretty text-lg leading-8 text-muted-foreground sm:text-xl">
              {siteConfig.name} turns rough intent into platform-aware messages
              that sound polished, natural, and appropriate for the moment. Choose
              the channel, relationship, tone, and language, then get ready-to-send
              options in seconds.
            </p>
            
            <MessageInputForm />

            <div className="mt-10 grid max-w-2xl gap-3 text-sm text-muted-foreground sm:grid-cols-3">
              {["Personalized drafts", "Cross-platform support", "Tone-aware output"].map(
                (item) => (
                  <div key={item} className="flex items-center gap-2">
                    <Sparkles aria-hidden="true" className="size-4 text-primary" />
                    {item}
                  </div>
                ),
              )}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 24, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: 0.18, duration: 0.7, ease: "easeOut" }}
            className="mt-12 rounded-2xl border border-white/10 bg-card/75 p-3 shadow-2xl shadow-black/30 backdrop-blur-xl lg:absolute lg:bottom-16 lg:right-8 lg:mt-0 lg:w-[31rem]"
          >
            <div className="flex items-center justify-between px-3 py-2">
              <div className="flex items-center gap-2 text-sm font-medium text-foreground">
                <MessageSquareText aria-hidden="true" className="size-4 text-primary" />
                Message variants
              </div>
              <div className="flex gap-1.5" aria-hidden="true">
                <span className="size-2.5 rounded-full bg-rose-400/80" />
                <span className="size-2.5 rounded-full bg-amber-300/80" />
                <span className="size-2.5 rounded-full bg-emerald-400/80" />
              </div>
            </div>
            <Separator className="my-2 bg-white/10" />
            <MessageMetadata />
            <MessageVariants />
          </motion.div>
        </div>
      </GenerateMessageProvider>
    </section>
  );
}

