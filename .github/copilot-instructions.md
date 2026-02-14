# rag-cosense: Global System Instructions

This repository is a Retrieval-Augmented Generation (RAG) system for Cosense (Scrapbox) data. It provides an AI-powered interface to query and interact with personal or team knowledge bases stored in Cosense.

## 🏗 System Architecture

The project follows a decoupled client-server architecture:
- **Backend Hub:** Responsible for document processing, embedding, vector storage (ChromaDB), and retrieval logic using LangChain.
- **Frontend Interface:** A modern React-based SPA that provides a chat-like interface for interacting with the RAG system.

## 📁 Project Layout

The project is organized as a monorepo where each component is its own project with internal `src` and `tests` directories.

- `backend/` - Python-based RAG logic and API.
  - `backend/src/` - Core retrieval logic, agent definitions, and vector store management.
  - `backend/tests/` - Backend unit and integration tests.
- `frontend/` - React-based SPA.
  - `frontend/src/` - React components, hooks, and state management.
  - `frontend/tests/` - Frontend unit and component tests.
- `e2e/` - Playwright end-to-end tests covering the full system.
- `.github/instructions/` - Concrete, path-specific coding standards and technical rules.
- `.github/agents/` - Persona-specific instructions for different AI agent roles.


## ⚠️ High-Level Principles & Boundaries

1. **Security First**: Never hardcode secrets. Use `.env` files for ALL API keys and sensitive configuration.
2. **Environment Isolation**:
   - Backend configurations stay in standard `.env`.
   - Frontend configurations requiring client-side access must use `VITE_` prefix.
3. **Cross-Domain Consistency**: Ensure the API contracts between Python and TypeScript are strictly followed.
4. **Validation Pipeline**: No code should be merged without passing linting, type checks, and relevant tests.

## 🤖 Internal Agent Instructions
Refer to specialized instructions in `.github/agents/` for role-specific guidance. For technical details (libraries, commands, naming), refer to the specific markdown files in `.github/instructions/`.

