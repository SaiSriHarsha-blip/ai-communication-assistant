/**
 * Why: Recruiters should immediately see the product handles real communication channels.
 * What: Lists supported platforms with compact, accessible cards.
 * How: The home page renders this after the hero as the first scannable proof point.
 */
import {
  BriefcaseBusiness,
  Camera,
  Mail,
  MessageCircle,
  Smartphone,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";

const platforms = [
  {
    name: "WhatsApp",
    description: "Conversational, relationship-aware replies.",
    Icon: MessageCircle,
  },
  {
    name: "Gmail",
    description: "Professional email-ready phrasing.",
    Icon: Mail,
  },
  {
    name: "LinkedIn",
    description: "Career-safe outreach and follow-ups.",
    Icon: BriefcaseBusiness,
  },
  {
    name: "SMS",
    description: "Short, direct messages for mobile.",
    Icon: Smartphone,
  },
  {
    name: "Instagram",
    description: "Casual social DMs with cleaner tone.",
    Icon: Camera,
  },
] as const;

export function SupportedPlatformsSection() {
  return (
    <section id="platforms" className="border-y border-border/70 bg-card/30 py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <Badge variant="secondary">Supported platforms</Badge>
          <h2 className="mt-5 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            One writing experience for the places people actually talk.
          </h2>
          <p className="mt-4 text-base leading-7 text-muted-foreground">
            MessagePilot adapts each draft to the expectations of the selected
            platform, helping your message feel native whether it is formal,
            social, quick, or conversational.
          </p>
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {platforms.map(({ name, description, Icon }) => (
            <article
              key={name}
              className="rounded-xl border border-border bg-background/60 p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-primary/40 hover:bg-background/80"
            >
              <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                <Icon aria-hidden="true" className="size-5" />
              </div>
              <h3 className="mt-5 text-base font-semibold text-foreground">
                {name}
              </h3>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                {description}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
