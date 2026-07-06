"use client";

import { useGenerateMessageContext } from "./generate-message-form";

export function MessageMetadata() {
  const { data } = useGenerateMessageContext();

  if (!data) return null;

  const formatMetadataValue = (val: string | null | undefined): string => {
    if (!val) return "";
    const lower = val.toLowerCase();
    if (lower === "whatsapp") return "WhatsApp";
    if (lower === "sms") return "SMS";
    if (lower === "gmail") return "Gmail";
    if (lower === "linkedin") return "LinkedIn";
    if (lower === "instagram") return "Instagram";
    return val.charAt(0).toUpperCase() + val.slice(1);
  };

  const rawItems = [
    data.detected_platform,
    data.detected_relationship,
    data.detected_language,
    data.detected_tone,
  ];

  const formattedItems = rawItems
    .map(formatMetadataValue)
    .filter((item): item is string => item.length > 0);

  if (formattedItems.length === 0) return null;

  return (
    <div className="grid gap-2 px-1 py-2 sm:grid-cols-2">
      {formattedItems.map((item) => (
        <div
          key={item}
          className="rounded-lg border border-white/10 bg-background/45 px-3 py-2 text-xs text-muted-foreground"
        >
          {item}
        </div>
      ))}
    </div>
  );
}
