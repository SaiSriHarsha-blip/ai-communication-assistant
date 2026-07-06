/**
 * Why: Next.js route-level loading keeps slow transitions polished by default.
 * What: Shows a minimal skeleton for the app shell while a route segment loads.
 * How: The App Router automatically renders this file during pending navigation.
 */
export default function Loading() {
  return (
    <main className="min-h-screen bg-background px-6 py-6">
      <div className="mx-auto max-w-7xl space-y-8">
        <div className="h-12 rounded-xl border border-border bg-muted/30" />
        <div className="grid gap-6 lg:grid-cols-[1fr_420px]">
          <div className="h-80 rounded-2xl bg-muted/20" />
          <div className="h-80 rounded-2xl border border-border bg-card/60" />
        </div>
      </div>
    </main>
  );
}
