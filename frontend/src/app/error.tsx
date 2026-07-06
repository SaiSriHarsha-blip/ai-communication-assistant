/**
 * Why: Route errors should be recoverable and styled consistently.
 * What: Provides a client error boundary with a reset action.
 * How: Next.js invokes this boundary for uncaught errors in the route tree.
 */
"use client";

import { RotateCcw } from "lucide-react";

import { Button } from "@/components/ui/button";

type ErrorPageProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-6">
      <section className="max-w-md rounded-2xl border border-border bg-card/80 p-8 text-center shadow-2xl shadow-black/20 backdrop-blur">
        <p className="text-sm font-medium text-muted-foreground">
          Something interrupted the interface.
        </p>
        <h1 className="mt-3 text-2xl font-semibold text-foreground">
          The page could not finish loading.
        </h1>
        <p className="mt-3 text-sm leading-6 text-muted-foreground">
          {error.message || "Please retry the route. The backend was not changed."}
        </p>
        <Button type="button" onClick={reset} className="mt-6">
          <RotateCcw aria-hidden="true" />
          Try again
        </Button>
      </section>
    </main>
  );
}
