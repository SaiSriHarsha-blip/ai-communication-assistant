/**
 * Why: A recruiter-optimized page should make engineering decisions easy to scan.
 * What: Summarizes frontend architecture, validation, API isolation, and UX quality.
 * How: The home page renders it before recruiter outcomes for technical credibility.
 */
import { Braces, CheckCircle2, Code2, Workflow } from "lucide-react";

const pillars = [
  {
    title: "AI-powered generation",
    body: "Turn a simple note into multiple polished variants that fit the channel, relationship, and tone.",
    Icon: Braces,
  },
  {
    title: "Built to scale",
    body: "The experience is organized for more platforms, more tones, and richer messaging workflows over time.",
    Icon: Workflow,
  },
  {
    title: "Accessible by design",
    body: "Clear controls, readable contrast, and keyboard-friendly interactions support more people from the start.",
    Icon: CheckCircle2,
  },
  {
    title: "Fast and reliable",
    body: "Responsive screens, graceful loading states, and focused error handling keep the workflow calm and dependable.",
    Icon: Code2,
  },
] as const;

export function ArchitectureSection() {
  return (
    <section id="architecture" className="py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-primary">
              Product foundation
            </p>
            <h2 className="mt-4 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
              Designed for confidence from first draft to final send.
            </h2>
            <p className="mt-4 text-base leading-7 text-muted-foreground">
              The product experience emphasizes speed, clarity, accessibility,
              and trust so users can move from uncertain wording to confident
              communication without friction.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            {pillars.map(({ title, body, Icon }) => (
              <article
                key={title}
                className="rounded-xl border border-border bg-card/65 p-5 shadow-sm"
              >
                <Icon aria-hidden="true" className="size-5 text-primary" />
                <h3 className="mt-4 text-base font-semibold text-foreground">
                  {title}
                </h3>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">
                  {body}
                </p>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
