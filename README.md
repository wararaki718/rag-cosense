# rag-cosense

A Retrieval-Augmented Generation (RAG) system for Cosense (Scrapbox) data. This project provides a seamless way to query your Cosense knowledge base using LLMs through a modern web interface.

## 🚀 Features

- **Cosense (Scrapbox) Integration**: Automatically fetches and indexes pages from your Cosense projects.
- **RAG Implementation**: Leverages LangChain and ChromaDB for high-quality retrieval and LLM-based answering.
- **Modern UI**: A responsive React-based frontend built with Vite and Tailwind CSS.
- **Docker Ready**: Full containerization support for easy deployment and development environment consistency.
- **AI Agent-Driven Development**: Specialized instructions for various engineering roles (Backend, Frontend, Test, Linter, Infra).

## 🛠 Tech Stack

### Backend
- **Language**: Python 3.12+
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **AI Framework**: LangChain
- **Vector Database**: ChromaDB
- **Tools**: Ruff (Linter/Formatter), Mypy (Type Check), Pytest

### Frontend
- **Framework**: React / TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Testing**: Vitest, Playwright (E2E)

### Infrastructure
- **Containerization**: Docker, Docker Compose

## 🔧 Setup & Development

### Prerequisites
- Python 3.12+
- Node.js (Latest LTS)
- Docker & Docker Compose
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Initial Setup
```bash
# Backend setup
uv sync

# Frontend setup
npm install
```

### Running the Application

#### Standard Development
```bash
# Terminal 1: Backend
uv run agent.py

# Terminal 2: Frontend
npm run dev
```

#### Using Docker
```bash
docker-compose up --build
```

## ✅ Validation

Before committing, ensure all checks pass:

### Backend
```bash
uv run ruff check --fix .
uv run ruff format .
uv run mypy .
uv run pytest
```

### Frontend
```bash
npm run lint
npm run type-check
npm run test
```

## 📁 Project Structure

```text
rag-cosense/
├── src/
│   ├── backend/     # Python RAG logic & retriever
│   └── frontend/    # React components & UI logic
├── tests/           # Backend unit / integration tests
├── e2e/             # Playwright E2E tests
├── .github/
│   ├── agents/      # Specialized persona-based instructions
│   └── copilot-instructions.md # Project-wide AI guidelines
├── pyproject.toml
├── package.json
└── README.md
```

## 🤖 AI Agents

This repository is optimized for AI-assisted development. Refer to the specialized personas in `.github/agents/`:
- **Python Engineer**: Backend & RAG logic.
- **Frontend Engineer**: UI & React development.
- **Test Engineer**: Quality assurance and automation.
- **Linter Engineer**: Code style and static analysis.
- **Infra Engineer**: Docker & Deployment.

## 📄 License

[MIT](LICENSE)
