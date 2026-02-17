import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App Component", () => {
  it("renders the header and Chat component", () => {
    render(<App />);
    
    expect(screen.getByText("Rag Cosense")).toBeInTheDocument();
    // Since Chat is rendered, we should see the welcome message or input
    expect(screen.getByPlaceholderText(/Ask a question\.\.\./i)).toBeInTheDocument();
  });
});
