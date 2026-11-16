"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
  AlertCircle,
  ChevronDown,
  Loader2,
  RefreshCw,
  SlidersHorizontal,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useGenerateMessageContext } from "./generate-message-form";
import { ClarificationAlert } from "./clarification-alert";
import {
  type MessageLanguage,
  type MessageRelationship,
  type MessageTone,
} from "@/features/messages/api/generate-message";

const messageFormSchema = z.object({
  message: z
    .string()
    .min(5, "Message must be at least 5 characters")
    .max(1000, "Message cannot exceed 1000 characters"),
  platform: z.enum(
    ["whatsapp", "gmail", "linkedin", "instagram", "sms"] as const,
    {
      message: "Please select a valid platform",
    },
  ),
  relationship: z
    .enum([
      "",
      "family",
      "friend",
      "manager",
      "hr",
      "professor",
      "colleague",
      "client",
    ] as const)
    .optional(),
  tone: z
    .enum([
      "",
      "casual",
      "professional",
      "friendly",
      "respectful",
      "formal",
      "apologetic",
    ] as const)
    .optional(),
  language: z
    .enum(["", "english", "telugu", "hindi", "mixed"] as const)
    .optional(),
});

type MessageFormValues = z.infer<typeof messageFormSchema>;

export function MessageInputForm() {
  const { generate, isLoading, data, clarification, error, lastRequest } =
    useGenerateMessageContext();

  const [showAdvanced, setShowAdvanced] = useState(false);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<MessageFormValues>({
    resolver: zodResolver(messageFormSchema),
    defaultValues: {
      message: "",
      platform: "whatsapp",
      relationship: "",
      tone: "",
      language: "english",
    },
  });

  const watchedRelationship = watch("relationship");
  const watchedTone = watch("tone");
  const watchedLanguage = watch("language");

  const hasCustomContext = Boolean(
    watchedRelationship ||
      watchedTone ||
      (watchedLanguage && watchedLanguage !== "english"),
  );

  const onSubmit = (values: MessageFormValues) => {
    void generate({
      message: values.message,
      platform: values.platform,
      relationship: values.relationship
        ? (values.relationship as MessageRelationship)
        : undefined,
      tone: values.tone ? (values.tone as MessageTone) : undefined,
      language: values.language
        ? (values.language as MessageLanguage)
        : undefined,
    });
  };

  const handleClarificationOption = (field: string, value: string) => {
    if (
      field === "relationship" ||
      field === "tone" ||
      field === "language" ||
      field === "platform"
    ) {
      setValue(field, value as never);
    }
  };

  const handleRetry = () => {
    if (lastRequest) {
      void generate(lastRequest);
    } else {
      void handleSubmit(onSubmit)();
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="mt-9 flex flex-col gap-5 max-w-2xl"
    >
      {/* Raw Message input */}
      <div className="flex flex-col gap-2">
        <label
          htmlFor="message"
          className="text-sm font-medium text-foreground"
        >
          Raw Message
        </label>
        <textarea
          id="message"
          placeholder="Type your message intent... (e.g., Running 15 minutes late due to traffic)"
          {...register("message")}
          disabled={isLoading}
          className="w-full min-h-[100px] rounded-xl border border-white/10 bg-background/55 p-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary disabled:opacity-50"
        />
        {errors.message && (
          <span className="text-xs text-destructive mt-1">
            {errors.message.message}
          </span>
        )}
      </div>

      {/* Target Platform selector */}
      <div className="flex flex-col gap-2">
        <label
          htmlFor="platform"
          className="text-sm font-medium text-foreground"
        >
          Target Platform
        </label>
        <div className="relative">
          <select
            id="platform"
            {...register("platform")}
            disabled={isLoading}
            className="w-full rounded-xl border border-white/10 bg-background/55 px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary disabled:opacity-50 appearance-none cursor-pointer"
          >
            <option value="whatsapp" className="bg-background text-foreground">
              WhatsApp
            </option>
            <option value="gmail" className="bg-background text-foreground">
              Gmail
            </option>
            <option value="linkedin" className="bg-background text-foreground">
              LinkedIn
            </option>
            <option value="instagram" className="bg-background text-foreground">
              Instagram
            </option>
            <option value="sms" className="bg-background text-foreground">
              SMS
            </option>
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-muted-foreground">
            <ChevronDown className="size-4" aria-hidden="true" />
          </div>
        </div>
        {errors.platform && (
          <span className="text-xs text-destructive mt-1">
            {errors.platform.message}
          </span>
        )}
      </div>

      {/* Optional Context Controls (Expandable) */}
      <div className="flex flex-col gap-2">
        <button
          type="button"
          onClick={() => setShowAdvanced((prev) => !prev)}
          aria-expanded={showAdvanced}
          aria-controls="additional-context-controls"
          className="flex items-center justify-between rounded-xl border border-white/10 bg-background/40 px-3.5 py-2.5 text-xs font-medium text-foreground transition-colors hover:bg-background/60"
        >
          <div className="flex items-center gap-2">
            <SlidersHorizontal
              className="size-3.5 text-muted-foreground"
              aria-hidden="true"
            />
            <span>Additional Context (Relationship, Tone, Language)</span>
            {hasCustomContext && (
              <span className="rounded-full bg-primary/20 px-2 py-0.5 text-[10px] font-semibold text-primary">
                Customized
              </span>
            )}
          </div>
          <ChevronDown
            className={`size-4 text-muted-foreground transition-transform duration-200 ${
              showAdvanced ? "rotate-180" : ""
            }`}
            aria-hidden="true"
          />
        </button>

        {showAdvanced && (
          <div
            id="additional-context-controls"
            className="grid grid-cols-1 gap-3 rounded-xl border border-white/10 bg-background/35 p-3.5 sm:grid-cols-3"
          >
            {/* Relationship */}
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="relationship"
                className="text-xs font-medium text-muted-foreground"
              >
                Relationship (Optional)
              </label>
              <div className="relative">
                <select
                  id="relationship"
                  {...register("relationship")}
                  disabled={isLoading}
                  className="w-full rounded-lg border border-white/10 bg-background/60 px-2.5 py-2 text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary disabled:opacity-50 appearance-none cursor-pointer"
                >
                  <option value="" className="bg-background text-foreground">
                    Auto-detect
                  </option>
                  <option
                    value="family"
                    className="bg-background text-foreground"
                  >
                    Family
                  </option>
                  <option
                    value="friend"
                    className="bg-background text-foreground"
                  >
                    Friend
                  </option>
                  <option
                    value="colleague"
                    className="bg-background text-foreground"
                  >
                    Colleague
                  </option>
                  <option
                    value="manager"
                    className="bg-background text-foreground"
                  >
                    Manager
                  </option>
                  <option value="hr" className="bg-background text-foreground">
                    HR
                  </option>
                  <option
                    value="professor"
                    className="bg-background text-foreground"
                  >
                    Professor
                  </option>
                  <option
                    value="client"
                    className="bg-background text-foreground"
                  >
                    Client
                  </option>
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-muted-foreground">
                  <ChevronDown className="size-3.5" aria-hidden="true" />
                </div>
              </div>
            </div>

            {/* Tone */}
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="tone"
                className="text-xs font-medium text-muted-foreground"
              >
                Tone (Optional)
              </label>
              <div className="relative">
                <select
                  id="tone"
                  {...register("tone")}
                  disabled={isLoading}
                  className="w-full rounded-lg border border-white/10 bg-background/60 px-2.5 py-2 text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary disabled:opacity-50 appearance-none cursor-pointer"
                >
                  <option value="" className="bg-background text-foreground">
                    Auto-detect
                  </option>
                  <option
                    value="casual"
                    className="bg-background text-foreground"
                  >
                    Casual
                  </option>
                  <option
                    value="professional"
                    className="bg-background text-foreground"
                  >
                    Professional
                  </option>
                  <option
                    value="friendly"
                    className="bg-background text-foreground"
                  >
                    Friendly
                  </option>
                  <option
                    value="respectful"
                    className="bg-background text-foreground"
                  >
                    Respectful
                  </option>
                  <option
                    value="formal"
                    className="bg-background text-foreground"
                  >
                    Formal
                  </option>
                  <option
                    value="apologetic"
                    className="bg-background text-foreground"
                  >
                    Apologetic
                  </option>
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-muted-foreground">
                  <ChevronDown className="size-3.5" aria-hidden="true" />
                </div>
              </div>
            </div>

            {/* Language */}
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="language"
                className="text-xs font-medium text-muted-foreground"
              >
                Language
              </label>
              <div className="relative">
                <select
                  id="language"
                  {...register("language")}
                  disabled={isLoading}
                  className="w-full rounded-lg border border-white/10 bg-background/60 px-2.5 py-2 text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary disabled:opacity-50 appearance-none cursor-pointer"
                >
                  <option
                    value="english"
                    className="bg-background text-foreground"
                  >
                    English (Default)
                  </option>
                  <option
                    value="telugu"
                    className="bg-background text-foreground"
                  >
                    Telugu
                  </option>
                  <option
                    value="hindi"
                    className="bg-background text-foreground"
                  >
                    Hindi
                  </option>
                  <option
                    value="mixed"
                    className="bg-background text-foreground"
                  >
                    Mixed
                  </option>
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-muted-foreground">
                  <ChevronDown className="size-3.5" aria-hidden="true" />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Submission Button */}
      <div className="flex flex-col gap-3 sm:flex-row mt-2">
        <Button
          size="lg"
          type="submit"
          disabled={isLoading}
          className="w-full sm:w-auto"
        >
          {isLoading ? (
            <>
              <Loader2 className="size-4 animate-spin" aria-hidden="true" />
              Generating
            </>
          ) : (
            <>
              Generate
              <Sparkles aria-hidden="true" />
            </>
          )}
        </Button>
      </div>

      {/* Clarification Display */}
      {clarification && (
        <ClarificationAlert
          clarification={clarification}
          onSelectOption={handleClarificationOption}
        />
      )}

      {/* Success Display */}
      {data && (
        <div className="p-4 rounded-lg border border-green-500/30 bg-green-500/10 text-green-400 text-sm">
          <p className="font-semibold">Messages Generated Successfully!</p>
          <p className="text-xs text-muted-foreground mt-1">
            {data.messages.length} platform-aware variant
            {data.messages.length === 1 ? "" : "s"} ready in the preview panel.
          </p>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="p-4 rounded-lg border border-destructive/30 bg-destructive/10 text-destructive text-sm flex flex-col gap-2">
          <div className="flex items-center gap-2 font-semibold">
            <AlertCircle className="size-4 shrink-0" aria-hidden="true" />
            <span>Generation Error</span>
          </div>
          <p className="text-xs leading-relaxed">{error}</p>
          <div>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={handleRetry}
              disabled={isLoading}
              className="mt-1 border-destructive/40 text-destructive hover:bg-destructive/20 text-xs h-8"
            >
              <RefreshCw className="size-3 mr-1.5" aria-hidden="true" />
              Retry
            </Button>
          </div>
        </div>
      )}
    </form>
  );
}
