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

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (fetch as any).mockResolvedValue({
      ok: true,
      headers: { get: () => "application/json" },
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

    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      headers: { get: () => "application/json" },
      json: () => Promise.resolve(mockErrorResponse),
    } as unknown as Response);

    await expect(sendChatMessage({ query: "test", context_history: [] })).rejects.toThrow("Something went wrong");
  });
});
