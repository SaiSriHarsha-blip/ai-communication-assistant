"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useGenerateMessageContext } from "./generate-message-form";
import { ClarificationAlert } from "./clarification-alert";

const messageFormSchema = z.object({
  message: z
    .string()
    .min(5, "Message must be at least 5 characters")
    .max(1000, "Message cannot exceed 1000 characters"),
  platform: z.enum(["whatsapp", "gmail", "linkedin", "instagram", "sms"] as const, {
    message: "Please select a valid platform",
  }),
});

type MessageFormValues = z.infer<typeof messageFormSchema>;

export function MessageInputForm() {
  const { generate, isLoading, data, clarification, error } = useGenerateMessageContext();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<MessageFormValues>({
    resolver: zodResolver(messageFormSchema),
    defaultValues: {
      message: "",
      platform: "whatsapp",
    },
  });

  const onSubmit = (values: MessageFormValues) => {
    void generate({
      message: values.message,
      platform: values.platform,
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="mt-9 flex flex-col gap-5 max-w-2xl">
      <div className="flex flex-col gap-2">
        <label htmlFor="message" className="text-sm font-medium text-foreground">
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
          <span className="text-xs text-destructive mt-1">{errors.message.message}</span>
        )}
      </div>

      <div className="flex flex-col gap-2">
        <label htmlFor="platform" className="text-sm font-medium text-foreground">
          Target Platform
        </label>
        <div className="relative">
          <select
            id="platform"
            {...register("platform")}
            disabled={isLoading}
            className="w-full rounded-xl border border-white/10 bg-background/55 px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary disabled:opacity-50 appearance-none cursor-pointer"
          >
            <option value="whatsapp" className="bg-background text-foreground">WhatsApp</option>
            <option value="gmail" className="bg-background text-foreground">Gmail</option>
            <option value="linkedin" className="bg-background text-foreground">LinkedIn</option>
            <option value="instagram" className="bg-background text-foreground">Instagram</option>
            <option value="sms" className="bg-background text-foreground">SMS</option>
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-muted-foreground">
            <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
            </svg>
          </div>
        </div>
        {errors.platform && (
          <span className="text-xs text-destructive mt-1">{errors.platform.message}</span>
        )}
      </div>

      <div className="flex flex-col gap-3 sm:flex-row mt-2">
        <Button
          size="lg"
          type="submit"
          disabled={isLoading}
          className="w-full sm:w-auto"
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
        <div className="p-4 rounded-lg border border-green-500/30 bg-green-500/10 text-green-400 text-sm">
          <p className="font-semibold">Response Received Successfully!</p>
          <p className="text-xs text-muted-foreground mt-1">
            Full response payload logged in the browser developer console.
          </p>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="p-4 rounded-lg border border-destructive/30 bg-destructive/10 text-destructive text-sm">
          <p className="font-semibold">Error:</p>
          <p className="mt-1">{error}</p>
        </div>
      )}
    </form>
  );
}
