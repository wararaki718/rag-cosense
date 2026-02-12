# rag-cosense: Copilot Instructions

This repository is a Retrieval-Augmented Generation (RAG) system for Cosense (Scrapbox) data. It consists of a Python-based backend for data processing and retrieval, and a TypeScript/React-based frontend for the user interface.

## 🛠 Tech Stack & Runtimes

- **Backend:** Python 3.12+ 
  - Package Manager: `uv`
  - Libraries: `langchain`, `langchain-openai`, `chromadb`, `httpx`
  - Tooling: `ruff` (lint/format), `mypy` (types), `pytest`
- **Frontend:** TypeScript, React
  - Build Tool: `Vite`
  - Styling: `Tailwind CSS`
  - Testing: `Vitest`, `Playwright` (E2E)
  - Tooling: `ESLint`, `Prettier`

## 🏗 Build & Validation Flow

Always follow this sequence when setting up or validating changes.

### 1. Bootstrapping
- **Python:** `uv sync` (Initializes environment and installs dependencies from `pyproject.toml`)
- **Frontend:** `npm install` (Installs node modules)

### 2. Development & Running
- **Backend Agent:** `uv run agent.py`
- **Frontend Dev:** `npm run dev`

### 3. Validation (Linter & Tests)
Before submitting any changes, you **must** run these commands:

#### Backend
- **Lint & Fix:** `uv run ruff check --fix .`
- **Format:** `uv run ruff format .`
- **Type Check:** `uv run mypy .`
- **Test:** `uv run pytest`

#### Frontend
- **Lint:** `npm run lint`
- **Type Check:** `npm run type-check`
- **Test:** `npm run test`

## 📁 Project Layout

- `src/` - Core source code.
  - `src/backend/` - Python retrieval logic, agent definitions, and vector store management.
  - `src/frontend/` - React components, hooks, and state management.
- `tests/` - Backend unit and integration tests.
- `e2e/` - Playwright end-to-end tests.
- `.github/agents/` - Specific persona instructions for different roles.
- `pyproject.toml` - Python dependencies and tool configurations.
- `package.json` - Frontend dependencies and scripts.

## ⚠️ Key Rules & Boundaries

1. **Always use \`uv\`**: For all Python-related tasks, use \`uv\` instead of raw \`pip\` or \`venv\`.
2. **Type Safety**: TypeScript on the frontend and type hints in Python are mandatory.
3. **API Keys**: Never hardcode secrets. Use \`.env\` files (documented in \`README.md\` templates).
4. **Environment Variables**:
   - Backend: Standard \`.env\`
   - Frontend: \`VITE_\` prefix required for client-side access.
5. **Testing**: New features should include corresponding tests in \`tests/\` or \`*.test.ts\`.

## 🤖 Internal Agent Instructions
Refer to specialized instructions in \`.github/agents/\` for role-specific guidance:
- \`python-engineer.md\`: Backend/RAG logic.
- \`frontend-engineer.md\`: React/UI development.
- \`test-engineer.md\`: Testing strategies.
- \`linter-engineer.md\`: Code quality and formatting.
- \`document-engineer.md\`: Documentation and diagrams.

Trust these instructions as the primary source of truth for workflow and architecture. Only explore if information is missing or outdated.
