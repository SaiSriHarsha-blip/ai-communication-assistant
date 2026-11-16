"use client";

import { useCallback, useMemo, useState } from "react";
import axios from "axios";

import {
  generateMessage,
  isGenerateMessageClarificationResponse,
  type GenerateMessageClarificationResponse,
  type GenerateMessageRequest,
  type GenerateMessageSuccessResponse,
} from "@/features/messages/api/generate-message";

type GenerateMessageStatus = "idle" | "loading" | "success" | "clarification" | "error";

export type UseGenerateMessageResult = {
  clarification: GenerateMessageClarificationResponse | null;
  data: GenerateMessageSuccessResponse | null;
  error: string | null;
  generate: (request: GenerateMessageRequest) => Promise<void>;
  isClarification: boolean;
  isError: boolean;
  isLoading: boolean;
  isSuccess: boolean;
  lastRequest: GenerateMessageRequest | null;
  reset: () => void;
  status: GenerateMessageStatus;
};

const initialState = {
  clarification: null,
  data: null,
  error: null,
  lastRequest: null,
  status: "idle",
} satisfies {
  clarification: GenerateMessageClarificationResponse | null;
  data: GenerateMessageSuccessResponse | null;
  error: string | null;
  lastRequest: GenerateMessageRequest | null;
  status: GenerateMessageStatus;
};

function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data;
    if (typeof data?.error === "string" && data.error.trim().length > 0) {
      return data.error;
    }
    const detail = data?.detail;
    if (typeof detail === "string" && detail.trim().length > 0) {
      return detail;
    }
    if (Array.isArray(detail) && detail.length > 0) {
      return detail
        .map((err) =>
          typeof err === "object" && err && "msg" in err
            ? String((err as { msg: unknown }).msg)
            : JSON.stringify(err),
        )
        .join(", ");
    }
    if (data?.message && typeof data.message === "string") {
      return data.message;
    }
    if (error.message && error.message.trim().length > 0) {
      return error.message;
    }
  }

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
  const [lastRequest, setLastRequest] = useState<GenerateMessageRequest | null>(
    initialState.lastRequest,
  );

  const reset = useCallback(() => {
    setClarification(initialState.clarification);
    setData(initialState.data);
    setError(initialState.error);
    setStatus(initialState.status);
    setLastRequest(initialState.lastRequest);
  }, []);

  const generate = useCallback(async (request: GenerateMessageRequest) => {
    setLastRequest(request);
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
      lastRequest,
      reset,
      status,
    }),
    [clarification, data, error, generate, lastRequest, reset, status],
  );
}
