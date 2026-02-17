import React, { useState, useRef, useEffect } from "react";
import { useChat } from "../hooks/useChat";
import { Send, Loader2, ExternalLink, User, Bot } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function Chat() {
  const { messages, isLoading, error, sendMessage } = useChat();
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <div className="flex flex-col h-[70vh] w-full bg-white rounded-xl shadow-sm border overflow-hidden">
      {/* Messages area */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-2">
            <Bot size={48} className="opacity-20" />
            <p className="text-lg font-medium">How can I help you today?</p>
            <p className="text-sm">Ask anything about your Cosense pages.</p>
          </div>
        )}

        {messages.map((message, i) => (
          <div
            key={i}
            className={cn(
              "flex w-full gap-4",
              message.role === "user" ? "flex-row-reverse" : "flex-row",
            )}
          >
            <div
              className={cn(
                "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
                message.role === "user"
                  ? "bg-blue-100 text-blue-600"
                  : "bg-gray-100 text-gray-600",
              )}
            >
              {message.role === "user" ? <User size={18} /> : <Bot size={18} />}
            </div>

            <div
              className={cn(
                "flex flex-col max-w-[80%] space-y-2",
                message.role === "user" ? "items-end" : "items-start",
              )}
            >
              <div
                className={cn(
                  "px-4 py-2 rounded-2xl",
                  message.role === "user"
                    ? "bg-blue-600 text-white rounded-tr-none"
                    : "bg-gray-100 text-gray-800 rounded-tl-none border border-gray-200",
                )}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
              </div>

              {message.sources && message.sources.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {message.sources.map((source, j) => (
                    <a
                      key={j}
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs bg-white border border-gray-200 hover:border-blue-300 px-2 py-1 rounded text-gray-500 hover:text-blue-600 transition-colors"
                    >
                      <span>{source.title}</span>
                      <ExternalLink size={10} />
                    </a>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex w-full gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 text-gray-600 flex items-center justify-center">
              <Bot size={18} />
            </div>
            <div className="bg-gray-100 text-gray-500 px-4 py-2 rounded-2xl rounded-tl-none border border-gray-200 flex items-center gap-2">
              <Loader2 size={16} className="animate-spin" />
              <span>Thinking...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="p-3 bg-red-50 border border-red-100 text-red-600 text-sm rounded-lg text-center">
            {error}
          </div>
        )}
      </div>

      {/* Input area */}
      <form
        onSubmit={handleSubmit}
        className="p-4 border-t bg-gray-50 flex gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 bg-white border border-gray-200 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white p-2 rounded-lg transition-colors flex items-center justify-center w-10 h-10"
        >
          {isLoading ? (
            <Loader2 size={20} className="animate-spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </form>
    </div>
  );
}
