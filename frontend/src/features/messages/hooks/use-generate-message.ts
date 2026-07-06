"use client";

import { useCallback, useMemo, useState } from "react";

import {
  generateMessage,
  isGenerateMessageClarificationResponse,
  type GenerateMessageClarificationResponse,
  type GenerateMessageRequest,
  type GenerateMessageSuccessResponse,
} from "@/features/messages/api/generate-message";

type GenerateMessageStatus = "idle" | "loading" | "success" | "clarification" | "error";

type UseGenerateMessageResult = {
  clarification: GenerateMessageClarificationResponse | null;
  data: GenerateMessageSuccessResponse | null;
  error: string | null;
  generate: (request: GenerateMessageRequest) => Promise<void>;
  isClarification: boolean;
  isError: boolean;
  isLoading: boolean;
  isSuccess: boolean;
  reset: () => void;
  status: GenerateMessageStatus;
};

const initialState = {
  clarification: null,
  data: null,
  error: null,
  status: "idle",
} satisfies {
  clarification: GenerateMessageClarificationResponse | null;
  data: GenerateMessageSuccessResponse | null;
  error: string | null;
  status: GenerateMessageStatus;
};

function getErrorMessage(error: unknown): string {
  if (error instanceof Error && error.message.trim().length > 0) {
    return error.message;
  }

  return "Unable to generate a message. Please try again.";
}

export function useGenerateMessage(): UseGenerateMessageResult {
  const [clarification, setClarification] =
    useState<GenerateMessageClarificationResponse | null>(
      initialState.clarification,
    );
  const [data, setData] = useState<GenerateMessageSuccessResponse | null>(
    initialState.data,
  );
  const [error, setError] = useState<string | null>(initialState.error);
  const [status, setStatus] = useState<GenerateMessageStatus>(
    initialState.status,
  );

  const reset = useCallback(() => {
    setClarification(initialState.clarification);
    setData(initialState.data);
    setError(initialState.error);
    setStatus(initialState.status);
  }, []);

  const generate = useCallback(async (request: GenerateMessageRequest) => {
    setClarification(null);
    setData(null);
    setError(null);
    setStatus("loading");

    try {
      const response = await generateMessage(request);

      if (isGenerateMessageClarificationResponse(response)) {
        setClarification(response);
        setStatus("clarification");
        return;
      }

      setData(response);
      setStatus("success");
    } catch (caughtError: unknown) {
      setError(getErrorMessage(caughtError));
      setStatus("error");
    }
  }, []);

  return useMemo(
    () => ({
      clarification,
      data,
      error,
      generate,
      isClarification: status === "clarification",
      isError: status === "error",
      isLoading: status === "loading",
      isSuccess: status === "success",
      reset,
      status,
    }),
    [clarification, data, error, generate, reset, status],
  );
}
