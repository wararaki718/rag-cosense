import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useChat } from "./useChat";
import { sendChatMessage } from "../api/chat";

// Mock the chat API
vi.mock("../api/chat", () => ({
  sendChatMessage: vi.fn(),
}));

describe("useChat", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should initialize with empty messages and no loading state", () => {
    const { result } = renderHook(() => useChat());

    expect(result.current.messages).toEqual([]);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it("should add a user message and then an assistant message on success", async () => {
    const mockResponse = {
      status: "success" as const,
      data: {
        answer: "Hello! How can I help you?",
        sources: [
          { title: "Page 1", url: "https://scrapbox.io/project/Page_1", score: 0.9 },
        ],
      },
    };

    vi.mocked(sendChatMessage).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage("Hello");
    });

    expect(result.current.messages).toHaveLength(2);
    expect(result.current.messages[0]).toEqual({
      role: "user",
      content: "Hello",
    });
    expect(result.current.messages[1]).toEqual({
      role: "assistant",
      content: "Hello! How can I help you?",
      sources: mockResponse.data.sources,
    });
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it("should set error state when sendMessage fails", async () => {
    const errorMessage = "Network Error";
    vi.mocked(sendChatMessage).mockRejectedValue(new Error(errorMessage));

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage("Hello");
    });

    expect(result.current.messages).toHaveLength(1); // Only user message
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(errorMessage);
  });
});
