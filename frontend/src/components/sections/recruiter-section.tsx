/**
 * Why: Recruiter-facing content should translate implementation choices into hiring signals.
 * What: Highlights product polish, collaboration discipline, and backend respect.
 * How: The home page renders this as the final conversion section before the footer.
 */
import { BadgeCheck, Bot, ShieldCheck, Zap } from "lucide-react";

import { Badge } from "@/components/ui/badge";

const signals = [
  {
    metric: "3",
    label: "message styles generated",
    Icon: ShieldCheck,
  },
  {
    metric: "24/7",
    label: "ready when wording matters",
    Icon: BadgeCheck,
  },
  {
    metric: "5",
    label: "supported platforms",
    Icon: Zap,
  },
] as const;

export function RecruiterSection() {
  return (
    <section id="recruiters" className="pb-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="rounded-2xl border border-white/10 bg-card/75 p-6 shadow-2xl shadow-black/20 backdrop-blur sm:p-8 lg:p-10">
          <div className="grid gap-10 lg:grid-cols-[1fr_0.9fr] lg:items-center">
            <div>
              <Badge variant="outline" className="border-white/10 bg-white/5">
                <Bot aria-hidden="true" />
                Why MessagePilot
              </Badge>
              <h2 className="mt-5 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
                Helpful AI that respects context.
              </h2>
              <p className="mt-4 text-base leading-7 text-muted-foreground">
                MessagePilot focuses on everyday communication pressure: saying
                the right thing, in the right tone, on the right platform. It is
                fast enough for quick replies and refined enough for important
                conversations.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
              {signals.map(({ metric, label, Icon }) => (
                <div
                  key={label}
                  className="flex items-center gap-4 rounded-xl border border-white/10 bg-background/55 p-4"
                >
                  <span className="flex size-11 items-center justify-center rounded-lg bg-primary/10 text-primary">
                    <Icon aria-hidden="true" className="size-5" />
                  </span>
                  <div>
                    <p className="text-2xl font-semibold text-foreground">
                      {metric}
                    </p>
                    <p className="text-sm text-muted-foreground">{label}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
