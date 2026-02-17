import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import Chat from "./Chat";
import { useChat } from "../hooks/useChat";

// Mock the useChat hook
vi.mock("../hooks/useChat", () => ({
  useChat: vi.fn(),
}));

describe("Chat Component", () => {
  it("renders welcome message when there are no messages", () => {
    (useChat as any).mockReturnValue({
      messages: [],
      isLoading: false,
      error: null,
      sendMessage: vi.fn(),
    });

    render(<Chat />);

    expect(screen.getByText(/How can I help you today\?/i)).toBeInTheDocument();
    expect(
      screen.getByText(/Ask anything about your Cosense pages/i),
    ).toBeInTheDocument();
  });

  it("renders messages correctly", () => {
    const messages = [
      { role: "user" as const, content: "Hello" },
      { role: "assistant" as const, content: "Hi there!", sources: [{ title: "Source 1", url: "#" }] },
    ];

    (useChat as any).mockReturnValue({
      messages,
      isLoading: false,
      error: null,
      sendMessage: vi.fn(),
    });

    render(<Chat />);

    expect(screen.getByText("Hello")).toBeInTheDocument();
    expect(screen.getByText("Hi there!")).toBeInTheDocument();
    expect(screen.getByText("Source 1")).toBeInTheDocument();
  });

  it("calls sendMessage when form is submitted", () => {
    const sendMessage = vi.fn();
    (useChat as any).mockReturnValue({
      messages: [],
      isLoading: false,
      error: null,
      sendMessage,
    });

    render(<Chat />);

    const input = screen.getByPlaceholderText(/Ask a question\.\.\./i);
    const form = input.closest("form");

    fireEvent.change(input, { target: { value: "Test message" } });
    fireEvent.submit(form!);

    expect(sendMessage).toHaveBeenCalledWith("Test message");
  });

  it("shows loading indicator when isLoading is true", () => {
    (useChat as any).mockReturnValue({
      messages: [{ role: "user", content: "Hello" }],
      isLoading: true,
      error: null,
      sendMessage: vi.fn(),
    });

    render(<Chat />);

    // Check for some loading text or icon if applicable
    // In our Chat.tsx, it shows Loader2 and "Thinking..."
    expect(screen.getByText(/Thinking\.\.\./i)).toBeInTheDocument();
  });
});
