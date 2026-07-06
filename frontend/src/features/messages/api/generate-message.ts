import apiClient from "@/lib/api-client";

export type MessagePlatform =
    | "gmail"
    | "instagram"
    | "linkedin"
    | "sms"
    | "whatsapp";

export type GenerateMessageRequest = {
    message: string;
    platform: MessagePlatform;
};

export type GeneratedMessageVariant = {
    style: string;
    text: string;
};

export type GenerateMessageSuccessResponse = {
    detected_language: string;
    detected_platform: string;
    detected_relationship: string;
    detected_tone: string;
    messages: GeneratedMessageVariant[];
    original_message: string;
};

export type GenerateMessageClarificationResponse = {
    language: string | null;
    missing_fields: string[];
    needs_clarification: true;
    platform: MessagePlatform | null;
    purpose: string | null;
    question: string;
    relationship: string | null;
    tone: string | null;
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
    const response = await apiClient.post<GenerateMessageResponse>(
        "/api/v1/generate-message",
        request,
    );

    return response.data;
}
