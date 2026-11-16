"use client";

import { useState } from "react";
import { AlertCircle, ArrowRight, Check, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  type GenerateMessageClarificationResponse,
  type GenerateMessageRequest,
  type MessageLanguage,
  type MessagePlatform,
  type MessageRelationship,
  type MessageTone,
} from "@/features/messages/api/generate-message";
import { useGenerateMessageContext } from "./generate-message-form";

type ClarificationAlertProps = {
  clarification: GenerateMessageClarificationResponse;
  onSelectOption?: (field: string, value: string) => void;
};

type OptionItem = {
  value: string;
  label: string;
};

const FIELD_CONFIGS: Record<
  string,
  {
    title: string;
    options: OptionItem[];
  }
> = {
  relationship: {
    title: "Recipient Relationship",
    options: [
      { value: "family", label: "Family" },
      { value: "friend", label: "Friend" },
      { value: "colleague", label: "Colleague" },
      { value: "manager", label: "Manager" },
      { value: "hr", label: "HR" },
      { value: "professor", label: "Professor" },
      { value: "client", label: "Client" },
    ],
  },
  platform: {
    title: "Target Platform",
    options: [
      { value: "whatsapp", label: "WhatsApp" },
      { value: "gmail", label: "Gmail" },
      { value: "linkedin", label: "LinkedIn" },
      { value: "instagram", label: "Instagram" },
      { value: "sms", label: "SMS" },
    ],
  },
  language: {
    title: "Preferred Language",
    options: [
      { value: "english", label: "English" },
      { value: "telugu", label: "Telugu" },
      { value: "hindi", label: "Hindi" },
      { value: "mixed", label: "Mixed" },
    ],
  },
  tone: {
    title: "Preferred Tone",
    options: [
      { value: "casual", label: "Casual" },
      { value: "professional", label: "Professional" },
      { value: "friendly", label: "Friendly" },
      { value: "respectful", label: "Respectful" },
      { value: "formal", label: "Formal" },
      { value: "apologetic", label: "Apologetic" },
    ],
  },
};

export function ClarificationAlert({
  clarification,
  onSelectOption,
}: ClarificationAlertProps) {
  const { generate, isLoading, isError, error, lastRequest } =
    useGenerateMessageContext();

  const [selectedValues, setSelectedValues] = useState<Record<string, string>>({});

  // Determine which fields are missing from backend response
  const missingFields =
    clarification.missing_fields && clarification.missing_fields.length > 0
      ? clarification.missing_fields
      : ["relationship"];

  const handleSelect = (field: string, value: string) => {
    setSelectedValues((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const hasSelectedAllMissing = missingFields.every(
    (field) => Boolean(selectedValues[field]),
  );

  const handleSubmit = async () => {
    if (!hasSelectedAllMissing || isLoading) {
      return;
    }

    const baseMessage = lastRequest?.message || "";
    const basePlatform =
      (selectedValues.platform as MessagePlatform | undefined) ||
      lastRequest?.platform ||
      clarification.platform ||
      "whatsapp";

    const baseRelationship =
      (selectedValues.relationship as MessageRelationship | undefined) ||
      lastRequest?.relationship ||
      (clarification.relationship as MessageRelationship | null) ||
      undefined;

    const baseTone =
      (selectedValues.tone as MessageTone | undefined) ||
      lastRequest?.tone ||
      (clarification.tone as MessageTone | null) ||
      undefined;

    const baseLanguage =
      (selectedValues.language as MessageLanguage | undefined) ||
      lastRequest?.language ||
      (clarification.language as MessageLanguage | null) ||
      undefined;

    const updatedRequest: GenerateMessageRequest = {
      message: baseMessage,
      platform: basePlatform,
      relationship: baseRelationship,
      tone: baseTone,
      language: baseLanguage,
    };

    // Notify parent to sync form controls
    if (onSelectOption) {
      Object.entries(selectedValues).forEach(([field, val]) => {
        onSelectOption(field, val);
      });
    }

    await generate(updatedRequest);
  };

  return (
    <div
      role="region"
      aria-labelledby="clarification-title"
      className="mt-4 rounded-xl border border-amber-500/40 bg-amber-500/10 p-5 text-amber-200 backdrop-blur-sm"
    >
      <div className="flex items-start gap-3">
        <AlertCircle className="mt-0.5 size-5 shrink-0 text-amber-400" aria-hidden="true" />
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h2 id="clarification-title" className="text-sm font-semibold text-amber-300">
              Clarification Needed
            </h2>
            <span className="rounded-full bg-amber-500/20 px-2 py-0.5 text-[11px] font-medium text-amber-300">
              Action Required
            </span>
          </div>

          <p className="mt-1.5 text-sm text-amber-100/90 leading-relaxed">
            {clarification.question ||
              "Please provide additional details so we can tailor your message."}
          </p>

          <div className="mt-4 space-y-4">
            {missingFields.map((field) => {
              const config = FIELD_CONFIGS[field] || {
                title: field.charAt(0).toUpperCase() + field.slice(1),
                options: [],
              };

              const currentValue = selectedValues[field] || "";

              return (
                <div key={field} className="flex flex-col gap-2">
                  <label className="text-xs font-medium uppercase tracking-wider text-amber-300/80">
                    Select {config.title}
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {config.options.map((option) => {
                      const isSelected = currentValue === option.value;
                      return (
                        <button
                          key={option.value}
                          type="button"
                          disabled={isLoading}
                          aria-pressed={isSelected}
                          onClick={() => handleSelect(field, option.value)}
                          className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
                            isSelected
                              ? "bg-amber-400 text-black shadow-md shadow-amber-500/20 ring-2 ring-amber-300 font-semibold"
                              : "border border-amber-500/30 bg-background/60 text-amber-100 hover:border-amber-400/60 hover:bg-amber-500/20"
                          } disabled:cursor-not-allowed disabled:opacity-50`}
                        >
                          {isSelected && (
                            <Check className="size-3 text-black stroke-[3]" aria-hidden="true" />
                          )}
                          {option.label}
                        </button>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>

          {isError && error && (
            <div className="mt-3 rounded-lg border border-red-500/40 bg-red-500/10 p-2.5 text-xs text-red-300">
              {error}
            </div>
          )}

          <div className="mt-5 flex flex-col gap-2 sm:flex-row sm:items-center">
            <Button
              type="button"
              size="sm"
              onClick={handleSubmit}
              disabled={!hasSelectedAllMissing || isLoading}
              className="bg-amber-500 font-medium text-black hover:bg-amber-400 disabled:bg-amber-500/30 disabled:text-amber-200/50"
            >
              {isLoading ? (
                <>
                  <Loader2 className="size-4 animate-spin" aria-hidden="true" />
                  Generating...
                </>
              ) : (
                <>
                  Continue Generation
                  <ArrowRight className="size-4" aria-hidden="true" />
                </>
              )}
            </Button>
            {!hasSelectedAllMissing && (
              <span className="text-xs text-amber-300/70">
                Please select an option above to continue
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
