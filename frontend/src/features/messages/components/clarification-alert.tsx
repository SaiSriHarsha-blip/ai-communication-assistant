"use client";

import { type GenerateMessageClarificationResponse } from "@/features/messages/api/generate-message";

type ClarificationAlertProps = {
  clarification: GenerateMessageClarificationResponse;
};

export function ClarificationAlert({ clarification }: ClarificationAlertProps) {
  return (
    <div className="mt-4 p-4 rounded-lg border border-yellow-500/30 bg-yellow-500/10 text-yellow-500 text-sm max-w-2xl">
      <p className="font-semibold">Clarification Required:</p>
      <p className="mt-1">{clarification.question}</p>
    </div>
  );
}
