"use client";

import { Check } from "lucide-react";
import { useGenerateMessageContext } from "./generate-message-form";
import { GeneratingMessageLoader } from "@/features/messages/components/generating-message-loader";

export function MessageVariants() {
  const { data, isLoading } = useGenerateMessageContext();

  return (
    <>
      {isLoading && <GeneratingMessageLoader className="mx-1 mb-2" />}
      {data && data.messages && data.messages.length > 0 && (
        <div className="mt-2 space-y-2">
          {data.messages.map((item) => (
            <article
              key={item.style}
              className="rounded-xl border border-white/10 bg-background/55 p-4"
            >
              <div className="flex items-center gap-2 text-sm font-medium text-foreground">
                <Check aria-hidden="true" className="size-4 text-emerald-400" />
                {item.style}
              </div>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                {item.text}
              </p>
            </article>
          ))}
        </div>
      )}
    </>
  );
}
