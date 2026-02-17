import { useState, useCallback } from "react";
import { sendChatMessage } from "../api/chat";
import type { Source } from "../types/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      setIsLoading(true);
      setError(null);

      // Add user message immediately
      const userMessage: Message = { role: "user", content };
      setMessages((prev) => [...prev, userMessage]);

      try {
        const response = await sendChatMessage({
          query: content,
          context_history: messages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        });

        const assistantMessage: Message = {
          role: "assistant",
          content: response.data.answer,
          sources: response.data.sources,
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Failed to send message");
        }
      } finally {
        setIsLoading(false);
      }
    },
    [messages],
  );

  return {
    messages,
    isLoading,
    error,
    sendMessage,
  };
}
