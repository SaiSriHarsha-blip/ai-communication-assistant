"use client";

import React, { createContext, useContext, useEffect } from "react";
import { useGenerateMessage } from "@/features/messages/hooks/use-generate-message";
import { Button } from "@/components/ui/button";
import { Sparkles } from "lucide-react";
import { ClarificationAlert } from "./clarification-alert";

type GenerateMessageContextType = ReturnType<typeof useGenerateMessage>;

const GenerateMessageContext = createContext<GenerateMessageContextType | null>(null);

export function useGenerateMessageContext() {
  const context = useContext(GenerateMessageContext);
  if (!context) {
    throw new Error("useGenerateMessageContext must be used within a GenerateMessageProvider");
  }
  return context;
}

export function GenerateMessageProvider({ children }: { children: React.ReactNode }) {
  const value = useGenerateMessage();
  const { data, clarification, error } = value;

  useEffect(() => {
    if (data) {
      console.log("Generate Success Response:", data);
    }
    if (clarification) {
      console.log("Generate Clarification Response:", clarification);
    }
    if (error) {
      console.error("Generate Error:", error);
    }
  }, [data, clarification, error]);

  return (
    <GenerateMessageContext.Provider value={value}>
      {children}
    </GenerateMessageContext.Provider>
  );
}

export function GenerateMessageForm() {
  const { generate, isLoading, data, clarification, error } = useGenerateMessageContext();

  const handleGenerateClick = () => {
    void generate({
      message: "Hey manager, I will be 15 minutes late because of traffic.",
      platform: "whatsapp",
    });
  };

  return (
    <div className="mt-9 flex flex-col gap-3">
      <div className="flex flex-col gap-3 sm:flex-row">
        <Button
          size="lg"
          type="button"
          onClick={handleGenerateClick}
          disabled={isLoading}
        >
          {isLoading ? "Generating" : "Generate"}
          <Sparkles aria-hidden="true" />
        </Button>
      </div>

      {/* Clarification Display */}
      {clarification && (
        <ClarificationAlert clarification={clarification} />
      )}

      {/* Success Display */}
      {data && (
        <div className="mt-4 p-4 rounded-lg border border-green-500/30 bg-green-500/10 text-green-400 text-sm max-w-2xl">
          <p className="font-semibold">Response Received Successfully!</p>
          <p className="text-xs text-muted-foreground mt-1">
            Full response payload logged in the browser developer console.
          </p>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mt-4 p-4 rounded-lg border border-destructive/30 bg-destructive/10 text-destructive text-sm max-w-2xl">
          <p className="font-semibold">Error:</p>
          <p className="mt-1">{error}</p>
        </div>
      )}
    </div>
  );
}
