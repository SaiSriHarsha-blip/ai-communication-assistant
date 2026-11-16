"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { useGenerateMessageContext } from "./generate-message-form";
import { GeneratingMessageLoader } from "@/features/messages/components/generating-message-loader";

export function MessageVariants() {
  const { data, isLoading } = useGenerateMessageContext();
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopy = async (text: string, index: number) => {
    try {
      if (typeof navigator !== "undefined" && navigator.clipboard) {
        await navigator.clipboard.writeText(text);
      } else {
        // Fallback for environments where navigator.clipboard is unavailable
        const textarea = document.createElement("textarea");
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
      }
      setCopiedIndex(index);
      setTimeout(() => {
        setCopiedIndex(null);
      }, 2000);
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  return (
    <>
      {isLoading && <GeneratingMessageLoader className="mx-1 mb-2" />}
      {data && data.messages && data.messages.length > 0 && (
        <div className="mt-2 space-y-2.5">
          {data.messages.map((item, index) => {
            const isCopied = copiedIndex === index;
            return (
              <article
                key={`${item.style}-${index}`}
                className="group relative rounded-xl border border-white/10 bg-background/55 p-4 transition-all hover:border-white/20 hover:bg-background/70"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm font-medium text-foreground">
                    <Check
                      aria-hidden="true"
                      className="size-4 text-emerald-400"
                    />
                    <span>{item.style}</span>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleCopy(item.text, index)}
                    aria-label={`Copy ${item.style} variant`}
                    className="flex items-center gap-1.5 rounded-lg border border-white/10 bg-background/60 px-2 py-1 text-xs text-muted-foreground transition-colors hover:border-primary/40 hover:bg-primary/10 hover:text-primary focus:outline-none focus:ring-1 focus:ring-primary"
                  >
                    {isCopied ? (
                      <>
                        <Check
                          className="size-3 text-emerald-400"
                          aria-hidden="true"
                        />
                        <span className="text-emerald-400 font-medium">
                          Copied
                        </span>
                      </>
                    ) : (
                      <>
                        <Copy className="size-3" aria-hidden="true" />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                </div>
                <p className="mt-2.5 text-sm leading-relaxed text-muted-foreground select-text whitespace-pre-wrap">
                  {item.text}
                </p>
              </article>
            );
          })}
        </div>
      )}
    </>
  );
}
