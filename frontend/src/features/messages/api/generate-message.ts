import apiClient from "@/lib/api-client";

export type MessagePlatform =
  | "whatsapp"
  | "gmail"
  | "instagram"
  | "linkedin"
  | "sms";

export type MessageRelationship =
  | "family"
  | "friend"
  | "manager"
  | "hr"
  | "professor"
  | "colleague"
  | "client";

export type MessageLanguage =
  | "english"
  | "telugu"
  | "hindi"
  | "mixed";

export type MessageTone =
  | "casual"
  | "professional"
  | "friendly"
  | "respectful"
  | "formal"
  | "apologetic";

export type GenerateMessageRequest = {
  message: string;
  platform?: MessagePlatform | null;
  relationship?: MessageRelationship | null;
  language?: MessageLanguage | null;
  tone?: MessageTone | null;
};

export type GeneratedMessageVariant = {
  style: string;
  text: string;
};

export type GenerateMessageSuccessResponse = {
  detected_language: MessageLanguage | string;
  detected_platform: MessagePlatform | string;
  detected_relationship: MessageRelationship | string;
  detected_tone: MessageTone | string;
  messages: GeneratedMessageVariant[];
  original_message: string;
};

export type GenerateMessageClarificationResponse = {
  language: MessageLanguage | string | null;
  missing_fields: string[];
  needs_clarification: true;
  platform: MessagePlatform | null;
  purpose: string | null;
  question: string | null;
  relationship: MessageRelationship | string | null;
  tone: MessageTone | string | null;
};

export type GenerateMessageResponse =
  | GenerateMessageClarificationResponse
  | GenerateMessageSuccessResponse;

export function isGenerateMessageClarificationResponse(
  response: GenerateMessageResponse,
): response is GenerateMessageClarificationResponse {
  return (
    "needs_clarification" in response &&
    response.needs_clarification === true
  );
}

export async function generateMessage(
  request: GenerateMessageRequest,
): Promise<GenerateMessageResponse> {
  const payload: Record<string, unknown> = {
    message: request.message,
  };

  if (request.platform) {
    payload.platform = request.platform;
  }
  if (request.relationship) {
    payload.relationship = request.relationship;
  }
  if (request.language) {
    payload.language = request.language;
  }
  if (request.tone) {
    payload.tone = request.tone;
  }

  const response = await apiClient.post<GenerateMessageResponse>(
    "/api/v1/generate-message",
    payload,
  );

  return response.data;
}
