import { describe, it, expect, vi, beforeEach } from "vitest";
import { sendChatMessage } from "./chat";

describe("chat api", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  it("sendChatMessage calls fetch with correct parameters", async () => {
    const mockResponse = {
      status: "success",
      data: { answer: "test answer", sources: [] },
    };

    (fetch as any).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const payload = { query: "test query", context_history: [] };
    const result = await sendChatMessage(payload);

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/chat"),
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(payload),
      }),
    );
    expect(result).toEqual(mockResponse);
  });

  it("throws ServiceError when response is not ok", async () => {
    const mockErrorResponse = {
      status: "error",
      message: "Something went wrong",
      code: "API_ERROR",
    };

    (fetch as any).mockResolvedValue({
      ok: false,
      json: () => Promise.resolve(mockErrorResponse),
    });

    await expect(sendChatMessage({ query: "test", context_history: [] })).rejects.toThrow("Something went wrong");
  });
});
