---
applyTo: "{backend/src/prompts/**/*.py,backend/src/agents/**/*.py}"
---
# AI & Prompt Engineering Instructions


This document defines standards for prompt engineering and AI agent logic using LangChain within the RAG system.

## 📁 Relevant Paths
- `src/backend/prompts/`: Jinja2 or f-string templates for LLMs.
- `src/backend/agents/`: Agent executors and chain definitions.

## 🛠 Tech Stack
- **Framework:** LangChain / LangGraph.
- **Models:** OpenAI (GPT-4o/mini).
- **Format:** LCEL (LangChain Expression Language).

## 📏 Prompt Standards
- **System Messages:** Always define a clear persona, constraints (e.g., "only answer based on context"), and output format.
- **Variables:** Use `{context}` for retrieved snippets and `{question}` for user input.
- **Hallucination Prevention:** 
  - Explicitly instruct the AI to say "I don't know" if information is missing from the context.
  - Require citations or source links in the response.
- **Few-Shot Prompting:** Use examples for complex reasoning or strictly formatted outputs (e.g., JSON).

## 🤖 Chain Logic
- **Streaming:** Implement streaming responses where possible for better UX.
- **Traceability:** Ensure `callbacks` (like LangSmith) can be easily integrated.
- **Fallback:** Define fallback models or behaviors if the primary LLM fails or hits rate limits.

## ⚠️ Security & Safety
- **Prompt Injection:** Sanitize user inputs before injecting into sensitive prompt templates.
- **PII:** Do not pass Personally Identifiable Information to LLMs unless explicitly required and anonymized.
